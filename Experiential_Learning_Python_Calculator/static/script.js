const expressionInput = document.getElementById("expression");
const resultOutput = document.getElementById("result");
const message = document.getElementById("message");
const historyContainer = document.getElementById("history");
const HISTORY_KEY = "calclab-history-v1";
let historyItems = [];

try {
  historyItems = JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
  if (!Array.isArray(historyItems)) historyItems = [];
} catch {
  historyItems = [];
}

function showMessage(text, isError = false) {
  message.textContent = text;
  message.classList.toggle("error", isError);
}

function formatResult(value) {
  if (typeof value === "number" && !Number.isInteger(value)) {
    return Number(value.toPrecision(12)).toString();
  }
  return String(value);
}

function renderHistory() {
  historyContainer.replaceChildren();
  if (!historyItems.length) {
    const empty = document.createElement("div");
    empty.className = "empty-history";
    const symbol = document.createElement("span");
    symbol.textContent = "↗";
    const paragraph = document.createElement("p");
    paragraph.textContent = "Your calculations will appear here.";
    empty.append(symbol, paragraph);
    historyContainer.append(empty);
    return;
  }
  historyItems.slice(0, 6).forEach((item) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "history-item";
    const expr = document.createElement("span");
    expr.className = "history-expression";
    expr.textContent = item.expression;
    const answer = document.createElement("span");
    answer.className = "history-result";
    answer.textContent = item.result;
    button.append(expr, answer);
    button.addEventListener("click", () => {
      expressionInput.value = item.expression;
      expressionInput.focus();
    });
    historyContainer.append(button);
  });
}

function saveHistory(expression, result) {
  historyItems.unshift({ expression, result, timestamp: Date.now() });
  historyItems = historyItems.slice(0, 20);
  try { localStorage.setItem(HISTORY_KEY, JSON.stringify(historyItems)); } catch {}
  renderHistory();
}

async function calculate() {
  const expression = expressionInput.value.trim();
  if (!expression) {
    showMessage("Enter an expression first.", true);
    expressionInput.focus();
    return;
  }
  showMessage("Calculating…");
  try {
    const response = await fetch("/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ expression })
    });
    const data = await response.json();
    if (!response.ok || !data.ok) {
      resultOutput.textContent = "—";
      showMessage(data.error || "Unable to calculate this expression.", true);
      return;
    }
    const formatted = formatResult(data.result);
    resultOutput.textContent = formatted;
    showMessage("Calculation complete");
    saveHistory(expression, formatted);
  } catch {
    resultOutput.textContent = "—";
    showMessage("Could not reach the calculator service. Try again.", true);
  }
}

function insertAtCursor(value) {
  const start = expressionInput.selectionStart ?? expressionInput.value.length;
  const end = expressionInput.selectionEnd ?? expressionInput.value.length;
  const current = expressionInput.value;
  expressionInput.value = current.slice(0, start) + value + current.slice(end);
  const position = start + value.length;
  expressionInput.focus();
  expressionInput.setSelectionRange(position, position);
}

document.getElementById("keypad").addEventListener("click", (event) => {
  const button = event.target.closest("button");
  if (!button) return;
  const action = button.dataset.action;
  if (action === "clear") {
    expressionInput.value = "";
    resultOutput.textContent = "0";
    showMessage("Ready for your next calculation");
    expressionInput.focus();
  } else if (action === "backspace") {
    const start = expressionInput.selectionStart ?? expressionInput.value.length;
    const end = expressionInput.selectionEnd ?? expressionInput.value.length;
    if (start !== end) {
      insertAtCursor("");
    } else if (start > 0) {
      expressionInput.setRangeText("", start - 1, start, "end");
    }
    expressionInput.focus();
  } else if (action === "calculate") {
    calculate();
  } else if (action === "sign") {
    const value = expressionInput.value.trim();
    if (value.startsWith("-(") && value.endsWith(")")) expressionInput.value = value.slice(2, -1);
    else if (value) expressionInput.value = `-(${value})`;
    else expressionInput.value = "-";
    expressionInput.focus();
  } else if (button.dataset.insert) {
    insertAtCursor(button.dataset.insert);
  }
});

expressionInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    calculate();
  } else if (event.key === "Escape") {
    expressionInput.value = "";
    resultOutput.textContent = "0";
    showMessage("Ready for your next calculation");
  }
});

document.getElementById("clear-history").addEventListener("click", () => {
  historyItems = [];
  try { localStorage.removeItem(HISTORY_KEY); } catch {}
  renderHistory();
});

renderHistory();
