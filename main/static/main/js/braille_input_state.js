const BRAILLE_DOT_COUNT = 6;


function validateCell(cell) {
    const isValid = Array.isArray(cell)
        && cell.length === BRAILLE_DOT_COUNT
        && cell.every((dot) => dot === 0 || dot === 1);

    if (!isValid) {
        throw new TypeError("点字セルは6個の0または1で指定してください。");
    }
}


function validateState(state) {
    const isValid = typeof state === "object"
        && state !== null
        && Array.isArray(state.cells)
        && state.cells.length > 0
        && state.cells.every((cell) => {
            try {
                validateCell(cell);
                return true;
            } catch {
                return false;
            }
        })
        && Number.isInteger(state.currentIndex)
        && state.currentIndex >= 0
        && state.currentIndex < state.cells.length;

    if (!isValid) {
        throw new TypeError("点字入力状態が正しくありません。");
    }
}


export function createEmptyCell() {
    return Array(BRAILLE_DOT_COUNT).fill(0);
}


export function createInputState() {
    return {
        cells: [createEmptyCell()],
        currentIndex: 0,
    };
}


export function getDotNumberFromKey(key, code) {
    if (/^[1-6]$/.test(key)) {
        return Number(key);
    }

    if (/^[１-６]$/.test(key)) {
        return key.charCodeAt(0) - "０".charCodeAt(0);
    }

    const codeMatch = /^(?:Digit|Numpad)([1-6])$/.exec(code);
    return codeMatch ? Number(codeMatch[1]) : null;
}


export function toggleDot(cell, dotNumber) {
    validateCell(cell);

    if (!Number.isInteger(dotNumber) || dotNumber < 1 || dotNumber > BRAILLE_DOT_COUNT) {
        throw new RangeError("点番号は1から6で指定してください。");
    }

    return cell.map((dot, index) => (
        index === dotNumber - 1 ? Number(dot === 0) : dot
    ));
}


export function clearCell(cell) {
    validateCell(cell);
    return createEmptyCell();
}


export function hasRaisedDots(cell) {
    validateCell(cell);
    return cell.some((dot) => dot === 1);
}


export function toggleCurrentDot(state, dotNumber) {
    validateState(state);

    return {
        cells: state.cells.map((cell, index) => (
            index === state.currentIndex ? toggleDot(cell, dotNumber) : [...cell]
        )),
        currentIndex: state.currentIndex,
    };
}


export function moveToNextCell(state) {
    validateState(state);

    if (state.currentIndex < state.cells.length - 1) {
        return {
            cells: state.cells.map((cell) => [...cell]),
            currentIndex: state.currentIndex + 1,
        };
    }

    return {
        cells: [...state.cells.map((cell) => [...cell]), createEmptyCell()],
        currentIndex: state.currentIndex + 1,
    };
}


export function moveToPreviousCell(state) {
    validateState(state);

    return {
        cells: state.cells.map((cell) => [...cell]),
        currentIndex: Math.max(0, state.currentIndex - 1),
    };
}


export function moveToFollowingCell(state) {
    validateState(state);

    return {
        cells: state.cells.map((cell) => [...cell]),
        currentIndex: Math.min(state.cells.length - 1, state.currentIndex + 1),
    };
}


export function handleBackspace(state) {
    validateState(state);
    const currentCell = state.cells[state.currentIndex];

    if (hasRaisedDots(currentCell)) {
        return {
            cells: state.cells.map((cell, index) => (
                index === state.currentIndex ? clearCell(cell) : [...cell]
            )),
            currentIndex: state.currentIndex,
        };
    }

    if (state.cells.length === 1) {
        return {
            cells: [[...currentCell]],
            currentIndex: 0,
        };
    }

    return {
        cells: state.cells
            .filter((_, index) => index !== state.currentIndex)
            .map((cell) => [...cell]),
        currentIndex: Math.max(0, state.currentIndex - 1),
    };
}
