/**
 * Questionnaire Logic & User Interaction
 */
import { fetchQuestions, submitAssessment, analyzeJsonProfile } from "./api.js";

let allQuestions = [];
let allCategories = {};
const userAnswers = {};

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const data = await fetchQuestions();
    allCategories = data.categories;
    allQuestions = data.questions;

    renderCategoryPills();
    renderQuestions();
    attachPresetListeners();
    attachJsonModeListeners();
  } catch (err) {
    document.getElementById("questions-render-area").innerHTML = `
      <div class="alert alert-warning">
        <i class="fa-solid fa-triangle-exclamation"></i>
        <div>Failed to load questions. Please ensure the backend server is running. (${err.message})</div>
      </div>
    `;
  }
});

function renderCategoryPills() {
  const container = document.getElementById("category-pills");
  container.innerHTML = "";

  Object.values(allCategories).forEach((cat) => {
    const pill = document.createElement("a");
    pill.href = `#cat-${cat.id}`;
    pill.className = "option-btn";
    pill.style.textDecoration = "none";
    pill.style.fontSize = "0.78rem";
    pill.style.padding = "0.3rem 0.7rem";
    pill.innerHTML = `<i class="fa-solid fa-folder"></i> ${cat.name}`;
    container.appendChild(pill);
  });
}

function renderQuestions() {
  const renderArea = document.getElementById("questions-render-area");
  renderArea.innerHTML = "";

  // Group questions by category
  const grouped = {};
  Object.keys(allCategories).forEach((catId) => (grouped[catId] = []));

  allQuestions.forEach((q) => {
    if (!grouped[q.category_id]) grouped[q.category_id] = [];
    grouped[q.category_id].push(q);
  });

  Object.keys(grouped).forEach((catId) => {
    const cat = allCategories[catId] || { name: catId, description: "" };
    const qList = grouped[catId];

    // Category Header
    const catHeader = document.createElement("div");
    catHeader.id = `cat-${catId}`;
    catHeader.className = "question-category-header";
    catHeader.innerHTML = `
      <h3 style="font-size: 1.25rem; font-weight: 700; color: #fff;">
        <i class="fa-solid fa-shield" style="color: var(--accent-cyan); margin-right: 8px;"></i>
        ${cat.name}
      </h3>
      <p style="color: var(--text-muted); font-size: 0.88rem; margin-top: 0.25rem;">
        ${cat.description}
      </p>
    `;
    renderArea.appendChild(catHeader);

    // Questions in this category
    qList.forEach((q, idx) => {
      const qCard = document.createElement("div");
      qCard.className = "question-card";
      qCard.id = `card-${q.id}`;

      qCard.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem;">
          <div class="question-text">
            <span style="color: var(--accent-cyan); margin-right: 6px;">Q${q.id.replace("q_", "").toUpperCase()}:</span>
            ${q.question}
          </div>
          <span class="badge badge-mod" style="font-size: 0.7rem;">${q.severity || "MEDIUM"}</span>
        </div>
        <div class="question-help"><i class="fa-solid fa-circle-info"></i> ${q.explanation}</div>
        <div class="options-group" id="opts-${q.id}">
          ${q.options
            .map(
              (opt) => `
            <button type="button" class="option-btn" data-qid="${q.id}" data-val="${opt}">
              ${opt.replace("_", " ")}
            </button>
          `
            )
            .join("")}
        </div>
      `;
      renderArea.appendChild(qCard);
    });
  });

  // Attach button click listeners
  renderArea.querySelectorAll(".option-btn[data-qid]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const qid = btn.getAttribute("data-qid");
      const val = btn.getAttribute("data-val");
      selectAnswer(qid, val);
    });
  });

  updateProgress();
}

function selectAnswer(qid, val) {
  userAnswers[qid] = val;

  // Highlight selected button
  const group = document.getElementById(`opts-${qid}`);
  if (group) {
    group.querySelectorAll(".option-btn").forEach((b) => {
      if (b.getAttribute("data-val") === val) {
        b.classList.add("selected");
      } else {
        b.classList.remove("selected");
      }
    });
  }

  updateProgress();
}

function updateProgress() {
  const answered = Object.keys(userAnswers).length;
  const total = allQuestions.length;
  const percent = total > 0 ? Math.round((answered / total) * 100) : 0;

  const bar = document.getElementById("progress-bar-fill");
  const text = document.getElementById("progress-text");
  const bottomStatus = document.getElementById("bottom-status-count");

  if (bar) bar.style.width = `${percent}%`;
  if (text) text.textContent = `${answered} / ${total} Answered (${percent}%)`;
  if (bottomStatus) bottomStatus.textContent = `${answered} of ${total} completed`;
}

function attachPresetListeners() {
  // High-Risk Preset (Simulates high exposure user)
  document.getElementById("btn-fill-high-risk").addEventListener("click", () => {
    allQuestions.forEach((q) => {
      // Pick highest risk option from mapping
      const mapping = q.risk_mapping;
      let worstOpt = q.options[0];
      let maxScore = -1;
      for (const opt in mapping) {
        if (mapping[opt] > maxScore) {
          maxScore = mapping[opt];
          worstOpt = opt;
        }
      }
      selectAnswer(q.id, worstOpt);
    });
  });

  // Low-Risk Preset (Simulates privacy-hardened user)
  document.getElementById("btn-fill-low-risk").addEventListener("click", () => {
    allQuestions.forEach((q) => {
      const mapping = q.risk_mapping;
      let bestOpt = q.options[0];
      let minScore = 999;
      for (const opt in mapping) {
        if (mapping[opt] < minScore) {
          minScore = mapping[opt];
          bestOpt = opt;
        }
      }
      selectAnswer(q.id, bestOpt);
    });
  });

  // Submit assessment form
  document.getElementById("assessment-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const submitBtn = document.getElementById("btn-submit-assessment");
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing Exposure...`;

    try {
      const result = await submitAssessment(userAnswers);
      // Cache result and original answers in sessionStorage
      sessionStorage.setItem("last_assessment", JSON.stringify(result));
      sessionStorage.setItem("last_answers", JSON.stringify(userAnswers));
      // Redirect to dashboard
      window.location.href = `/dashboard?id=${result.assessment_id}`;
    } catch (err) {
      alert(`Submission error: ${err.message}`);
      submitBtn.disabled = false;
      submitBtn.innerHTML = `<i class="fa-solid fa-calculator"></i> Calculate Privacy Risk Score`;
    }
  });
}

function attachJsonModeListeners() {
  const jsonBox = document.getElementById("json-mode-box");
  const toggleBtn = document.getElementById("btn-toggle-json");
  const closeBtn = document.getElementById("btn-close-json");
  const loadSampleBtn = document.getElementById("btn-load-sample-json");
  const submitJsonBtn = document.getElementById("btn-submit-json");

  toggleBtn.addEventListener("click", () => {
    jsonBox.style.display = jsonBox.style.display === "none" ? "block" : "none";
  });

  closeBtn.addEventListener("click", () => {
    jsonBox.style.display = "none";
  });

  // Sample data loader
  loadSampleBtn.addEventListener("click", () => {
    const sampleProfile = {
      platform: "instagram",
      username: "alex.rivers.tech",
      display_name: "Alex Rivers",
      bio: "Senior DevOps @ CloudMatrix • Marathon Runner • Contact: alex.rivers@workmail.io or +1 (415) 555-0199",
      email: "alex.rivers@workmail.io",
      phone: "+1 415 555 0199",
      location: "San Francisco, CA",
      privacy: { account_private: false, show_activity: true, allow_message_requests: true },
      links: ["https://linktr.ee/alexrivers", "https://github.com/alexrivers"]
    };

    const samplePosts = [
      {
        id: "post_101",
        text: "Daily 7am run along the Embarcadero before clocking in at CloudMatrix 5th floor!",
        geo: { lat: 37.79, lon: -122.39 },
        media: { type: "image", exif: { created_local: "2026-05-10 07:05:12" } }
      },
      {
        id: "post_102",
        text: "First day of school for my daughter Emily at Lincoln Elementary! #kids #school",
        media: { type: "image", is_child_present: true }
      },
      {
        id: "post_103",
        text: "Picked up my new all-access security badge and ID card for CloudMatrix HQ building 4!",
        media: { type: "image" }
      }
    ];

    document.getElementById("json-profile-input").value = JSON.stringify(sampleProfile, null, 2);
    document.getElementById("json-posts-input").value = JSON.stringify(samplePosts, null, 2);
  });

  submitJsonBtn.addEventListener("click", async () => {
    try {
      const profText = document.getElementById("json-profile-input").value;
      const postsText = document.getElementById("json-posts-input").value || "[]";

      if (!profText) {
        alert("Please paste or load profile.json content.");
        return;
      }

      const prof = JSON.parse(profText);
      const posts = JSON.parse(postsText);

      submitJsonBtn.disabled = true;
      submitJsonBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...`;

      const result = await analyzeJsonProfile(prof, posts);

      // Adapt result for dashboard display
      const adapted = {
        assessment_id: `feed_${Date.now()}`,
        created_at: new Date().toISOString(),
        overall_score: result.overall_score,
        risk_level: result.risk_level,
        category_scores: {},
        findings: result.findings.map((f, i) => ({
          id: `feed_f_${i}`,
          category_name: f.cat,
          severity: f.severity,
          item: f.item,
          explanation: f.item,
          recommendation: f.fix,
          priority: f.severity === "CRITICAL" ? "IMMEDIATE" : f.severity === "HIGH" ? "IMPORTANT" : "GOOD_PRACTICE"
        })),
        recommendations: result.findings.map((f) => ({
          category: f.cat,
          issue: f.item,
          severity: f.severity,
          recommendation: f.fix,
          priority: f.severity === "CRITICAL" ? "IMMEDIATE" : f.severity === "HIGH" ? "IMPORTANT" : "GOOD_PRACTICE"
        })),
        priority_actions: result.findings.slice(0, 3).map((f) => f.fix),
        disclaimer: "Synthetically parsed profile and post feed risk evaluation."
      };

      Object.keys(result.category_scores).forEach((cat) => {
        adapted.category_scores[cat] = {
          category_id: cat,
          category_name: cat,
          score: result.category_scores[cat],
          weight: 0.15,
          risk_level: result.category_scores[cat] > 70 ? "CRITICAL" : result.category_scores[cat] > 40 ? "HIGH" : "LOW"
        };
      });

      sessionStorage.setItem("last_assessment", JSON.stringify(adapted));
      window.location.href = `/dashboard?id=${adapted.assessment_id}`;
    } catch (e) {
      alert(`Invalid JSON format: ${e.message}`);
      submitJsonBtn.disabled = false;
      submitJsonBtn.innerHTML = `<i class="fa-solid fa-play"></i> Analyze JSON Feed`;
    }
  });
}
