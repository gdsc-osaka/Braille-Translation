function requireElement(id, expectedType) {
    const element = document.getElementById(id);

    if (!(element instanceof expectedType)) {
        throw new Error(`画面要素 #${id} が見つかりません。`);
    }

    return element;
}


function requireDataUrl(element, name) {
    const url = element.dataset[name];

    if (!url) {
        throw new Error(`data-${name} が設定されていません。`);
    }

    return url;
}


const pageElement = document.querySelector("main.jtb-page");

if (!(pageElement instanceof HTMLElement)) {
    throw new Error("画面要素 main.jtb-page が見つかりません。");
}

const convertUrl = requireDataUrl(pageElement, "convertUrl");
const readingUrl = requireDataUrl(pageElement, "readingUrl");
const flipUrl = requireDataUrl(pageElement, "flipUrl");

const textInput = requireElement("japanese-text", HTMLTextAreaElement);
const readingInput = requireElement("japanese-reading", HTMLTextAreaElement);
const convertButton = requireElement("japanese-convert-button", HTMLButtonElement);
const editButton = requireElement("japanese-reading-edit-button", HTMLButtonElement);
const surfaceSelect = requireElement("braille-surface", HTMLSelectElement);
const brailleOutput = requireElement("braille-output", HTMLElement);
const errorElement = requireElement("jtb-error", HTMLElement);

const csrfInput = pageElement.querySelector("input[name='csrfmiddlewaretoken']");

if (!(csrfInput instanceof HTMLInputElement)) {
    throw new Error("CSRFトークンが見つかりません。");
}

const RAISED_SURFACE = "raised";
const RECESSED_SURFACE = "recessed";

// 現在「点字」欄に表示している文字列（プレースホルダーを除いた実データ）
let currentBraille = "";
let currentSurface = surfaceSelect.value;


// 表示面を確定し、凹面（裏面）のときは点字欄を右詰めにする
function applySurface(surface) {
    currentSurface = surface;
    brailleOutput.classList.toggle("is-recessed", surface === RECESSED_SURFACE);
}


applySurface(currentSurface);


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


async function postForm(url, fields, fallbackMessage) {
    const body = new FormData();
    body.append("csrfmiddlewaretoken", csrfInput.value);

    Object.entries(fields).forEach(([name, value]) => {
        body.append(name, value);
    });

    const response = await fetch(url, {
        method: "POST",
        body,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
    });

    let data = null;

    try {
        data = await response.json();
    } catch {
        throw new Error(fallbackMessage);
    }

    if (!response.ok) {
        throw new Error(getResponseMessage(data, "error", fallbackMessage));
    }

    return data;
}


// 既存の内容をすべて消して、戻り値のみを表示する
function showBraille(braille) {
    currentBraille = braille;
    brailleOutput.textContent = braille;
}


function setBusy(isBusy) {
    convertButton.disabled = isBusy;
    editButton.disabled = isBusy;
    surfaceSelect.disabled = isBusy;
}


function showError(error, fallbackMessage) {
    errorElement.textContent = error instanceof Error
        ? error.message
        : fallbackMessage;
}


// 変換・修正の結果は凸面（表面）で返るので、表示面の選択も凸面に戻す
function resetSurface() {
    surfaceSelect.value = RAISED_SURFACE;
    applySurface(RAISED_SURFACE);
}


// #1 「変換」：convert_kanji → convert_braille_to_kana
convertButton.addEventListener("click", async () => {
    const fallbackMessage = "文章を変換できませんでした。";
    errorElement.textContent = "";
    setBusy(true);

    try {
        const data = await postForm(
            convertUrl,
            {text: textInput.value},
            fallbackMessage,
        );

        showBraille(getResponseMessage(data, "braille", ""));
        readingInput.value = getResponseMessage(data, "reading", "");
        resetSurface();
    } catch (error) {
        showError(error, fallbackMessage);
    } finally {
        setBusy(false);
    }
});


// #2 「修正」：convert_kana
editButton.addEventListener("click", async () => {
    const fallbackMessage = "読みを点字に変換できませんでした。";
    errorElement.textContent = "";
    setBusy(true);

    try {
        const data = await postForm(
            readingUrl,
            {reading: readingInput.value},
            fallbackMessage,
        );

        showBraille(getResponseMessage(data, "braille", ""));
        resetSurface();
    } catch (error) {
        showError(error, fallbackMessage);
    } finally {
        setBusy(false);
    }
});


// #3 表示面の切り替え：flip_dots
surfaceSelect.addEventListener("change", async () => {
    const fallbackMessage = "表示面を切り替えられませんでした。";
    const requestedSurface = surfaceSelect.value;
    errorElement.textContent = "";

    if (currentBraille === "") {
        applySurface(requestedSurface);
        return;
    }

    setBusy(true);

    try {
        const data = await postForm(
            flipUrl,
            {braille: currentBraille},
            fallbackMessage,
        );

        showBraille(getResponseMessage(data, "braille", ""));
        applySurface(requestedSurface);
    } catch (error) {
        // 反転に失敗した場合は、表示内容と選択を一致させるため元に戻す
        surfaceSelect.value = currentSurface;
        showError(error, fallbackMessage);
    } finally {
        setBusy(false);
        surfaceSelect.focus();
    }
});
