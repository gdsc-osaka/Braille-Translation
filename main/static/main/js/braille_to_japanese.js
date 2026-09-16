import {
    createInputState,
    getDotNumberFromKey,
    handleBackspace,
    moveToFollowingCell,
    moveToNextCell,
    moveToPreviousCell,
    toggleCurrentDot,
} from "./braille_input_state.js?v=3";


function requireElement(id, expectedType) {
    const element = document.getElementById(id);

    if (!(element instanceof expectedType)) {
        throw new Error(`画面要素 #${id} が見つかりません。`);
    }

    return element;
}


const form = requireElement("braille-conversion-form", HTMLFormElement);
const inputArea = requireElement("braille-input", HTMLElement);
const cellTemplate = requireElement("braille-cell-template", HTMLTemplateElement);
const payloadInput = requireElement("braille-dots-payload", HTMLInputElement);
const convertButton = requireElement("convert-button", HTMLButtonElement);
const errorElement = requireElement("braille-input-error", HTMLElement);
const statusElement = requireElement("braille-input-status", HTMLElement);
const resultElement = requireElement("japanese-result", HTMLElement);

let inputState = createInputState();


function focusInputArea() {
    inputArea.focus({preventScroll: true});
}


function renderCells() {
    const fragment = document.createDocumentFragment();

    inputState.cells.forEach((cell, cellIndex) => {
        const cellFragment = cellTemplate.content.cloneNode(true);
        const cellElement = cellFragment.querySelector(".braille-cell");

        if (!(cellElement instanceof HTMLElement)) {
            throw new Error("点字セルのテンプレートが正しくありません。");
        }

        const isCurrent = cellIndex === inputState.currentIndex;
        cellElement.classList.toggle("is-current", isCurrent);
        cellElement.setAttribute(
            "aria-label",
            `点字セル${cellIndex + 1}${isCurrent ? "、選択中" : ""}`,
        );

        cellElement.querySelectorAll("[data-dot-number]").forEach((element) => {
            const dotNumber = Number(element.getAttribute("data-dot-number"));
            element.classList.toggle("is-on", cell[dotNumber - 1] === 1);
        });

        fragment.append(cellFragment);
    });

    inputArea.replaceChildren(fragment);
    payloadInput.value = JSON.stringify(inputState.cells);
    statusElement.textContent = `${inputState.currentIndex + 1}文字目を入力中です。`;
}


function getResponseMessage(data, key, fallback) {
    if (
        typeof data === "object"
        && data !== null
        && key in data
        && typeof data[key] === "string"
    ) {
        return data[key];
    }

    return fallback;
}


function handleKeydown(event) {
    const dotNumber = getDotNumberFromKey(event.key, event.code);

    if (dotNumber !== null) {
        event.preventDefault();
        inputState = toggleCurrentDot(inputState, dotNumber);
        errorElement.textContent = "";
        renderCells();
        return;
    }

    if (event.key === "Enter") {
        event.preventDefault();
        inputState = moveToNextCell(inputState);
        errorElement.textContent = "";
        renderCells();
        return;
    }

    if (event.key === "ArrowRight") {
        event.preventDefault();
        inputState = moveToFollowingCell(inputState);
        errorElement.textContent = "";
        renderCells();
        return;
    }

    if (event.key === "ArrowLeft") {
        event.preventDefault();
        inputState = moveToPreviousCell(inputState);
        errorElement.textContent = "";
        renderCells();
        return;
    }

    if (event.key === "Backspace") {
        event.preventDefault();
        inputState = handleBackspace(inputState);
        errorElement.textContent = "";
        renderCells();
    }
}


inputArea.addEventListener("keydown", handleKeydown);


document.addEventListener("keydown", (event) => {
    if (event.target instanceof Node && inputArea.contains(event.target)) {
        return;
    }

    if (
        event.target instanceof HTMLInputElement
        || event.target instanceof HTMLTextAreaElement
        || event.target instanceof HTMLSelectElement
        || event.target instanceof HTMLButtonElement
        || event.target instanceof HTMLAnchorElement
    ) {
        return;
    }

    if (
        getDotNumberFromKey(event.key, event.code) !== null
        || event.key === "Backspace"
        || event.key === "Enter"
        || event.key === "ArrowLeft"
        || event.key === "ArrowRight"
    ) {
        focusInputArea();
        handleKeydown(event);
    }
});


form.addEventListener("submit", async (event) => {
    event.preventDefault();
    errorElement.textContent = "";
    convertButton.disabled = true;

    try {
        const response = await fetch(form.action, {
            method: "POST",
            body: new FormData(form),
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(getResponseMessage(
                data,
                "error",
                "点字を変換できませんでした。",
            ));
        }

        resultElement.textContent = getResponseMessage(data, "result", "");
    } catch (error) {
        errorElement.textContent = error instanceof Error
            ? error.message
            : "点字を変換できませんでした。";
    } finally {
        convertButton.disabled = false;
        focusInputArea();
    }
});


renderCells();
focusInputArea();
window.addEventListener("load", focusInputArea, {once: true});
