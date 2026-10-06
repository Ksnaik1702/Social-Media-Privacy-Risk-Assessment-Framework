/**
 * API Client for Social Media Privacy Risk Assessment Framework
 */
const API_BASE = "/api";

export async function fetchQuestions() {
  const res = await fetch(`${API_BASE}/questions`);
  if (!res.ok) throw new Error("Failed to load questionnaire data.");
  return await res.json();
}

export async function submitAssessment(answers, customWeights = null) {
  const payload = { answers, custom_weights: customWeights };
  const res = await fetch(`${API_BASE}/assessment`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Assessment submission failed.");
  }
  return await res.json();
}

export async function simulateImprovement(originalAnswers, simulatedChanges) {
  const payload = {
    original_answers: originalAnswers,
    simulated_changes: simulatedChanges
  };
  const res = await fetch(`${API_BASE}/assessment/simulate-improvement`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error("Improvement simulation failed.");
  return await res.json();
}

export async function fetchDashboardStats() {
  const res = await fetch(`${API_BASE}/dashboard/stats`);
  if (!res.ok) throw new Error("Failed to load dashboard statistics.");
  return await res.json();
}

export async function fetchPrivacyChecklist() {
  const res = await fetch(`${API_BASE}/privacy-checklist`);
  if (!res.ok) throw new Error("Failed to load privacy checklist.");
  return await res.json();
}

export async function analyzeJsonProfile(profile, posts) {
  const res = await fetch(`${API_BASE}/analyze-json`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ profile, posts })
  });
  if (!res.ok) throw new Error("JSON profile analysis failed.");
  return await res.json();
}

export async function inspectMetadata(file) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API_BASE}/metadata/inspect`, {
    method: "POST",
    body: formData
  });
  if (!res.ok) throw new Error("Metadata inspection failed.");
  return await res.json();
}

export async function stripMetadata(file) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API_BASE}/metadata/strip`, {
    method: "POST",
    body: formData
  });
  if (!res.ok) throw new Error("Metadata stripping failed.");
  return await res.blob();
}
