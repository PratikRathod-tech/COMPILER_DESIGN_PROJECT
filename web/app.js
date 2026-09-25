const editor = document.getElementById("editor");
const runBtn = document.getElementById("runBtn");
const clearBtn = document.getElementById("clearBtn");
const workflowBtn = document.getElementById("workflowBtn");
const statusIndicator = document.getElementById("statusIndicator");

const resultView = document.getElementById("resultView");
const phaseView = document.getElementById("phaseView");
const phaseContent = document.getElementById("phaseContent");
const workflowView = document.getElementById("workflowView");
const pipelineFlow = document.getElementById("pipelineFlow");

const phaseButtons = document.querySelectorAll(".phase-btn");
const presetButtons = document.querySelectorAll(".preset-btn");

let lastCompilationData = null;
let currentPhase = "result";

const PRESETS = {
  matrix: `matrix A = [[1,2],[3,4]]
matrix B = [[5,6],[7,8]]

C = A * B

show C`,
  linear: `solve 2*x + 5 = 15`,
  linear_system: `solve:
2*x + y = 10
x - y = 2`,
  metrics: `actual = [3, -0.5, 2, 7]
predicted = [2.5, 0, 2, 8]

show mae(actual, predicted)
show mse(actual, predicted)
show rmse(actual, predicted)
show r2(actual, predicted)`
};

// Initialize with matrix preset
editor.value = PRESETS.matrix;

presetButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    const key = btn.getAttribute("data-preset");
    if (PRESETS[key]) {
      editor.value = PRESETS[key];
    }
  });
});

clearBtn.addEventListener("click", () => {
  editor.value = "";
  lastCompilationData = null;
  resultView.innerHTML = '<div class="placeholder-msg">Click "Run" or "Workflow" to compile and execute program.</div>';
  phaseContent.textContent = "";
  pipelineFlow.innerHTML = "";
  statusIndicator.textContent = "Ready";
});

runBtn.addEventListener("click", () => {
  compileProgram(false);
});

workflowBtn.addEventListener("click", () => {
  compileProgram(true);
});

async function compileProgram(showWorkflowImmediately = false) {
  const source = editor.value.trim();
  if (!source) {
    statusIndicator.textContent = "Editor is empty";
    return;
  }

  statusIndicator.textContent = "Compiling...";

  try {
    const response = await fetch("/api/compile", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source })
    });

    const res = await response.json();

    if (!res.success) {
      statusIndicator.textContent = "Error";
      showError(res.error);
      return;
    }

    statusIndicator.textContent = "Compiled Successfully";
    lastCompilationData = res.data;

    renderResultView(res.data);
    renderWorkflowView(res.data);

    if (showWorkflowImmediately) {
      selectPhase("workflow");
    } else {
      selectPhase("result");
    }
  } catch (err) {
    statusIndicator.textContent = "Server Connection Error";
    showError("Could not reach backend server: " + err.message);
  }
}

function showError(errorText) {
  resultView.innerHTML = `
    <div class="error-banner">
      <strong>COMPILATION ERROR</strong>\n\n${escapeHtml(errorText)}
    </div>
  `;
  resultView.classList.remove("hidden");
  phaseView.classList.add("hidden");
  workflowView.classList.add("hidden");
  setActivePhaseBtn("result");
}

function renderResultView(data) {
  resultView.innerHTML = `
    <div class="result-card">
      <div class="sec-title">RESULT</div>
      <div class="divider"></div>
      <div class="result-val">${escapeHtml(data.execution)}</div>

      <div class="result-grid">
        <div class="meta-box">
          <div class="label">Operation</div>
          <div class="val">${escapeHtml(data.operation)}</div>
        </div>
        <div class="meta-box">
          <div class="label">ML Classification</div>
          <div class="val">${escapeHtml(data.ml_category)} (${data.ml_confidence}%)</div>
        </div>
      </div>

      <div class="sec-title" style="margin-top: 10px;">MATHEMATICAL EXPLANATION</div>
      <div class="explanation-box">${escapeHtml(data.explanation)}</div>
    </div>
  `;
}

function renderWorkflowView(data) {
  const phases = [
    { title: "SOURCE CODE", content: data.source },
    { title: "LEXICAL ANALYSIS", content: data.tokens },
    { title: "SYNTAX ANALYSIS", content: data.syntax },
    { title: "AST", content: data.ast },
    { title: "SEMANTIC ANALYSIS", content: data.semantic },
    { title: "SYMBOL TABLE", content: data.symbols },
    { title: "ML CLASSIFICATION", content: data.ml_text },
    { title: "INTERMEDIATE REPRESENTATION", content: data.ir },
    { title: "OPTIMIZATION", content: data.opt_ir },
    { title: "EXECUTION", content: data.execution }
  ];

  let html = "";
  phases.forEach((p, idx) => {
    html += `
      <div class="workflow-phase" id="phase-step-${idx}">
        <div class="phase-header" onclick="togglePhaseStep(${idx})">
          <div><span class="step-badge">[${idx + 1}]</span> ${p.title}</div>
          <span class="toggle-icon" id="toggle-icon-${idx}">▼</span>
        </div>
        <div class="phase-body" id="phase-body-${idx}">${escapeHtml(p.content)}</div>
      </div>
    `;
    if (idx < phases.length - 1) {
      html += `<div class="phase-down-arrow">↓</div>`;
    }
  });

  pipelineFlow.innerHTML = html;
}

window.togglePhaseStep = function(idx) {
  const body = document.getElementById(`phase-body-${idx}`);
  const icon = document.getElementById(`toggle-icon-${idx}`);
  if (body.classList.contains("hidden")) {
    body.classList.remove("hidden");
    icon.textContent = "▼";
  } else {
    body.classList.add("hidden");
    icon.textContent = "▶";
  }
};

phaseButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    const phaseKey = btn.getAttribute("data-phase");
    selectPhase(phaseKey);
  });
});

function setActivePhaseBtn(phaseKey) {
  phaseButtons.forEach(b => {
    if (b.getAttribute("data-phase") === phaseKey) {
      b.classList.add("active");
    } else {
      b.classList.remove("active");
    }
  });
}

function selectPhase(phaseKey) {
  currentPhase = phaseKey;
  setActivePhaseBtn(phaseKey);

  if (!lastCompilationData) {
    return;
  }

  if (phaseKey === "result") {
    resultView.classList.remove("hidden");
    phaseView.classList.add("hidden");
    workflowView.classList.add("hidden");
  } else if (phaseKey === "workflow") {
    resultView.classList.add("hidden");
    phaseView.classList.add("hidden");
    workflowView.classList.remove("hidden");
  } else {
    resultView.classList.add("hidden");
    phaseView.classList.remove("hidden");
    workflowView.classList.add("hidden");

    let content = "";
    switch (phaseKey) {
      case "tokens":
        content = lastCompilationData.tokens;
        break;
      case "ast":
        content = lastCompilationData.ast;
        break;
      case "semantic":
        content = lastCompilationData.semantic;
        break;
      case "symbols":
        content = lastCompilationData.symbols;
        break;
      case "ml":
        content = lastCompilationData.ml_text;
        break;
      case "ir":
        content = lastCompilationData.ir;
        break;
      case "opt_ir":
        content = lastCompilationData.opt_ir;
        break;
      case "execution":
        content = lastCompilationData.execution;
        break;
      default:
        content = lastCompilationData.execution;
    }
    phaseContent.textContent = content;
  }
}

function escapeHtml(text) {
  if (typeof text !== "string") return String(text);
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
