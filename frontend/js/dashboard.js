/**
 * Dashboard & Visualization Controller
 */
import {
  simulateImprovement,
  fetchDashboardStats,
  fetchPrivacyChecklist
} from "./api.js";

let currentAssessment = null;
let currentAnswers = {};
let categoryChartInstance = null;
let distChartInstance = null;

document.addEventListener("DOMContentLoaded", async () => {
  loadAssessmentData();
  setupEventListeners();
  loadTelemetryStats();
});

function loadAssessmentData() {
  const cached = sessionStorage.getItem("last_assessment");
  const cachedAnswers = sessionStorage.getItem("last_answers");

  if (cached) {
    currentAssessment = JSON.parse(cached);
    currentAnswers = cachedAnswers ? JSON.parse(cachedAnswers) : {};
  } else {
    // Default demonstration profile (High Exposure scenario)
    currentAssessment = {
      assessment_id: "demo_high_risk",
      overall_score: 72.0,
      risk_level: "CRITICAL",
      disclaimer: "Educational risk framework demonstration.",
      priority_actions: [
        "CRITICAL: Remove publicly visible phone number to stop SIM swapping.",
        "CRITICAL: Enable Multi-Factor Authentication (MFA) immediately.",
        "CRITICAL: Turn off real-time location check-ins.",
        "HIGH: Enable timeline tag review queue."
      ],
      category_scores: {
        profile_visibility: { category_name: "Profile Visibility", score: 85.0 },
        personal_information: { category_name: "Personal Info", score: 95.0 },
        location_privacy: { category_name: "Location Privacy", score: 90.0 },
        posts_content: { category_name: "Posts & Content", score: 70.0 },
        friends_followers: { category_name: "Friends/Followers", score: 65.0 },
        tagging_mentions: { category_name: "Tagging Permissions", score: 80.0 },
        account_security: { category_name: "Account Security", score: 75.0 },
        third_party_apps: { category_name: "Third-Party Apps", score: 60.0 },
        social_engineering: { category_name: "Social Engineering", score: 70.0 },
        digital_footprint: { category_name: "Digital Footprint", score: 55.0 }
      },
      findings: [
        {
          id: "find_q_pi_1",
          severity: "CRITICAL",
          item: "Phone number publicly exposed on profile",
          explanation: "Public phone numbers allow attackers to perform SIM swapping and SMS phishing.",
          recommendation: "Remove phone number from public profile view immediately.",
          priority: "IMMEDIATE"
        },
        {
          id: "find_q_sec_1",
          severity: "CRITICAL",
          item: "Multi-Factor Authentication (MFA) disabled",
          explanation: "Accounts without MFA can be compromised in credential stuffing attacks.",
          recommendation: "Enable MFA using an authenticator app (Google Authenticator / Aegis).",
          priority: "IMMEDIATE"
        },
        {
          id: "find_q_loc_1",
          severity: "CRITICAL",
          item: "Real-time location check-ins actively posted",
          explanation: "Broadcasting real-time whereabouts exposes users to physical stalking and break-ins.",
          recommendation: "Post updates only after leaving the location.",
          priority: "IMMEDIATE"
        },
        {
          id: "find_q_tag_1",
          severity: "HIGH",
          item: "Tag review approval queue disabled",
          explanation: "Strangers and bots can tag you in scam promotions or sensitive photos.",
          recommendation: "Enable 'Review posts you are tagged in' in settings.",
          priority: "IMPORTANT"
        }
      ],
      recommendations: [
        {
          category: "Personal Information",
          issue: "Phone number publicly exposed",
          severity: "CRITICAL",
          recommendation: "Remove phone number from public view.",
          priority: "IMMEDIATE"
        },
        {
          category: "Account Security",
          issue: "MFA disabled",
          severity: "CRITICAL",
          recommendation: "Enable MFA using an authenticator app.",
          priority: "IMMEDIATE"
        },
        {
          category: "Location Privacy",
          issue: "Real-time check-ins enabled",
          severity: "CRITICAL",
          recommendation: "Avoid broadcasting live physical coordinates.",
          priority: "IMMEDIATE"
        }
      ]
    };

    currentAnswers = {
      q_pi_1: "YES",
      q_pi_2: "YES",
      q_pi_3: "YES",
      q_loc_1: "YES",
      q_loc_2: "YES",
      q_sec_1: "NO",
      q_sec_2: "YES",
      q_tag_1: "NO",
      q_app_1: "NO",
      q_df_1: "NO"
    };
  }

  renderAssessmentUI();
}

function renderAssessmentUI() {
  const data = currentAssessment;
  if (!data) return;

  // 1. KPI Cards
  const scoreElem = document.getElementById("kpi-overall-score");
  const badgeElem = document.getElementById("kpi-risk-badge");
  scoreElem.textContent = Math.round(data.overall_score);

  const level = data.risk_level.toUpperCase();
  badgeElem.textContent = level;
  badgeElem.className = `badge badge-${level === "CRITICAL" ? "crit" : level === "HIGH" ? "high" : level === "MODERATE" ? "mod" : "low"}`;

  if (level === "CRITICAL") scoreElem.style.color = "var(--risk-crit)";
  else if (level === "HIGH") scoreElem.style.color = "var(--risk-high)";
  else if (level === "MODERATE") scoreElem.style.color = "var(--risk-mod)";
  else scoreElem.style.color = "var(--risk-low)";

  document.getElementById("kpi-findings-count").textContent = data.findings ? data.findings.length : 0;
  
  const immCount = (data.findings || []).filter(f => f.priority === "IMMEDIATE" || f.severity === "CRITICAL").length;
  document.getElementById("kpi-immediate-count").textContent = immCount;

  // 2. Priority actions
  const priorityList = document.getElementById("priority-actions-list");
  priorityList.innerHTML = "";
  if (data.priority_actions && data.priority_actions.length > 0) {
    data.priority_actions.forEach(action => {
      const li = document.createElement("li");
      li.style.padding = "0.6rem 0";
      li.style.borderBottom = "1px solid var(--border-color)";
      li.style.fontSize = "0.9rem";
      li.innerHTML = `<i class="fa-solid fa-arrow-right-to-bracket" style="color: var(--accent-cyan); margin-right: 8px;"></i> ${action}`;
      priorityList.appendChild(li);
    });
  }

  // 3. Render Category Chart (Radar or Bar)
  renderCategoryChart(data.category_scores);

  // 4. Render Findings
  renderFindings(data.findings || []);

  // 5. Render Recommendations
  renderRecommendations(data.recommendations || []);
}

function renderCategoryChart(categoryScores) {
  const ctx = document.getElementById("categoryChart");
  if (!ctx) return;

  const labels = [];
  const scores = [];

  Object.values(categoryScores).forEach(cat => {
    labels.push(cat.category_name || cat.category_id);
    scores.push(cat.score);
  });

  if (categoryChartInstance) {
    categoryChartInstance.destroy();
  }

  categoryChartInstance = new Chart(ctx, {
    type: "radar",
    data: {
      labels: labels,
      datasets: [{
        label: "Assessed Exposure (0-100)",
        data: scores,
        backgroundColor: "rgba(6, 182, 212, 0.25)",
        borderColor: "rgba(6, 182, 212, 1)",
        pointBackgroundColor: "#ef4444",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "#ef4444",
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          min: 0,
          max: 100,
          ticks: { stepSize: 20, color: "#9ca3af", backdropColor: "transparent" },
          grid: { color: "rgba(55, 65, 81, 0.6)" },
          pointLabels: { color: "#e5e7eb", font: { size: 11, weight: "bold" } }
        }
      },
      plugins: {
        legend: { labels: { color: "#f3f4f6" } }
      }
    }
  });
}

function renderFindings(findings) {
  const container = document.getElementById("findings-container");
  container.innerHTML = "";

  if (findings.length === 0) {
    container.innerHTML = `<div class="card" style="text-align:center; color: var(--risk-low);"><i class="fa-solid fa-check-circle"></i> No high-risk privacy weaknesses detected! Excellent defensive posture.</div>`;
    return;
  }

  findings.forEach(f => {
    const item = document.createElement("div");
    item.className = `finding-item sev-${f.severity}`;
    item.innerHTML = `
      <div style="font-size: 1.4rem; color: ${f.severity === 'CRITICAL' ? 'var(--risk-crit)' : f.severity === 'HIGH' ? 'var(--risk-high)' : 'var(--risk-mod)'};">
        <i class="fa-solid fa-triangle-exclamation"></i>
      </div>
      <div class="finding-content" style="flex: 1;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
          <h4>${f.item}</h4>
          <span class="badge badge-${f.severity === 'CRITICAL' ? 'crit' : f.severity === 'HIGH' ? 'high' : 'mod'}">${f.severity}</span>
        </div>
        <p>${f.explanation}</p>
        <div class="finding-fix"><i class="fa-solid fa-screwdriver-wrench"></i> Fix: ${f.recommendation}</div>
      </div>
    `;
    container.appendChild(item);
  });
}

function renderRecommendations(recommendations) {
  const container = document.getElementById("recommendations-container");
  container.innerHTML = "";

  if (recommendations.length === 0) {
    container.innerHTML = `<div class="card" style="text-align: center; color: var(--text-muted);">No remediation steps required at this time.</div>`;
    return;
  }

  recommendations.forEach(r => {
    const card = document.createElement("div");
    card.className = "card";
    card.style.marginBottom = "0.75rem";
    card.style.padding = "1rem 1.25rem";
    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
          <span style="font-size: 0.75rem; text-transform: uppercase; color: var(--accent-cyan); font-weight: 700;">${r.category || 'General'}</span>
          <div style="font-weight: 600; font-size: 1rem; margin: 0.2rem 0;">${r.issue || r.recommendation}</div>
        </div>
        <span class="badge badge-${r.priority === 'IMMEDIATE' ? 'crit' : r.priority === 'IMPORTANT' ? 'high' : 'low'}">${r.priority}</span>
      </div>
      <p style="color: var(--text-muted); font-size: 0.88rem; margin-top: 0.4rem;">
        <i class="fa-solid fa-circle-check" style="color: var(--risk-low); margin-right: 6px;"></i> ${r.recommendation}
      </p>
    `;
    container.appendChild(card);
  });
}

function setupEventListeners() {
  // Print Report
  document.getElementById("btn-print-report").addEventListener("click", () => {
    window.print();
  });

  // Privacy Checklist Modal
  const modal = document.getElementById("checklist-modal");
  document.getElementById("btn-view-checklist").addEventListener("click", async () => {
    modal.style.display = "flex";
    const data = await fetchPrivacyChecklist();
    const area = document.getElementById("checklist-items-area");
    area.innerHTML = data.checklist.map(item => `
      <label style="display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0; border-bottom: 1px solid var(--border-color); cursor: pointer;">
        <input type="checkbox" style="width: 18px; height: 18px; accent-color: var(--accent-cyan);">
        <span><b style="color: var(--accent-cyan);">[${item.cat}]</b> ${item.action}</span>
      </label>
    `).join("");
  });

  document.getElementById("btn-close-checklist").addEventListener("click", () => {
    modal.style.display = "none";
  });

  // Privacy Improvement Simulator Button
  document.getElementById("btn-run-simulation").addEventListener("click", async () => {
    const btn = document.getElementById("btn-run-simulation");
    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Calculating Reduction...`;

    // Gather selected improvements
    const changes = {};
    document.querySelectorAll(".sim-check:checked").forEach(cb => {
      const qid = cb.getAttribute("data-qid");
      const val = cb.getAttribute("data-newval");
      changes[qid] = val;
    });

    try {
      const res = await simulateImprovement(currentAnswers, changes);

      const panel = document.getElementById("sim-result-panel");
      panel.style.display = "block";

      document.getElementById("sim-orig-score").textContent = `${Math.round(res.original_score)} (${res.original_risk_level})`;
      document.getElementById("sim-new-score").textContent = `${Math.round(res.simulated_score)} (${res.simulated_risk_level})`;
      document.getElementById("sim-delta-score").textContent = `-${res.risk_reduction_points} pts (-${res.risk_reduction_percent}%)`;

      const resolvedList = document.getElementById("sim-resolved-list");
      if (res.resolved_findings.length > 0) {
        resolvedList.innerHTML = `
          <strong><i class="fa-solid fa-circle-check" style="color: var(--risk-low);"></i> Resolved Weaknesses with Hardened Settings:</strong>
          <ul style="margin-top: 0.5rem; padding-left: 1.5rem; color: #9ca3af;">
            ${res.resolved_findings.map(item => `<li>${item}</li>`).join("")}
          </ul>
        `;
      } else {
        resolvedList.innerHTML = `<span>Settings already hardened for these items.</span>`;
      }

      btn.disabled = false;
      btn.innerHTML = `<i class="fa-solid fa-calculator"></i> Simulate Improvements`;
    } catch (e) {
      alert(`Simulation error: ${e.message}`);
      btn.disabled = false;
      btn.innerHTML = `<i class="fa-solid fa-calculator"></i> Simulate Improvements`;
    }
  });
}

async function loadTelemetryStats() {
  try {
    const stats = await fetchDashboardStats();
    
    // Benchmark average
    const avgElem = document.getElementById("kpi-benchmark-avg");
    if (avgElem && stats.average_score) {
      avgElem.textContent = stats.average_score;
    }

    // Top cohort weaknesses
    const weakList = document.getElementById("benchmark-weaknesses-list");
    if (weakList && stats.top_weaknesses) {
      weakList.innerHTML = stats.top_weaknesses.map(w => `
        <li style="display: flex; justify-content: space-between; padding: 0.4rem 0; border-bottom: 1px solid var(--border-color); font-size: 0.85rem;">
          <span>${w.item}</span>
          <span style="color: var(--accent-cyan); font-weight: 700;">${w.count} users</span>
        </li>
      `).join("");
    }

    // Risk tier distribution chart
    const distCanvas = document.getElementById("distChart");
    if (distCanvas && stats.risk_distribution) {
      if (distChartInstance) distChartInstance.destroy();

      distChartInstance = new Chart(distCanvas, {
        type: "doughnut",
        data: {
          labels: ["LOW (0-20)", "MODERATE (21-40)", "HIGH (41-70)", "CRITICAL (71-100)"],
          datasets: [{
            data: [
              stats.risk_distribution.LOW || 10,
              stats.risk_distribution.MODERATE || 25,
              stats.risk_distribution.HIGH || 40,
              stats.risk_distribution.CRITICAL || 25
            ],
            backgroundColor: ["#10b981", "#f59e0b", "#f97316", "#ef4444"],
            borderColor: "#111827",
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: "right", labels: { color: "#9ca3af", font: { size: 11 } } }
          }
        }
      });
    }
  } catch (err) {
    console.warn("Could not load aggregate telemetry stats:", err);
  }
}
