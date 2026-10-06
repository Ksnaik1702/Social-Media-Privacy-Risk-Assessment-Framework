/**
 * EXIF Inspector & Scrubber Controller
 */
import { inspectMetadata, stripMetadata } from "./api.js";

let selectedFile = null;

document.addEventListener("DOMContentLoaded", () => {
  const dropArea = document.getElementById("drop-area");
  const fileInput = document.getElementById("file-input");

  // Drag and drop events
  ["dragenter", "dragover"].forEach(eventName => {
    dropArea.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropArea.classList.add("dragover");
    });
  });

  ["dragleave", "drop"].forEach(eventName => {
    dropArea.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropArea.classList.remove("dragover");
    });
  });

  dropArea.addEventListener("drop", (e) => {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFile(files[0]);
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
      handleFile(e.target.files[0]);
    }
  });

  // Strip button
  document.getElementById("btn-strip-download").addEventListener("click", async () => {
    if (!selectedFile) return;
    const btn = document.getElementById("btn-strip-download");
    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Sanitizing Image...`;

    try {
      const blob = await stripMetadata(selectedFile);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `sanitized_${selectedFile.name}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (e) {
      alert(`Stripping failed: ${e.message}`);
    } finally {
      btn.disabled = false;
      btn.innerHTML = `<i class="fa-solid fa-download"></i> Strip Metadata & Download Clean Image`;
    }
  });
});

async function handleFile(file) {
  selectedFile = file;
  const panel = document.getElementById("metadata-results-panel");
  panel.style.display = "block";

  const findingsList = document.getElementById("meta-findings-list");
  const tbody = document.getElementById("raw-meta-tbody");
  findingsList.innerHTML = `<div style="padding: 1rem;"><i class="fa-solid fa-spinner fa-spin"></i> Inspecting EXIF markers in memory...</div>`;
  tbody.innerHTML = "";

  try {
    const res = await inspectMetadata(file);

    // Detected leaks
    if (res.risk_findings && res.risk_findings.length > 0) {
      document.getElementById("meta-finding-badge").textContent = `${res.risk_findings.length} RISKS DETECTED`;
      document.getElementById("meta-finding-badge").className = "badge badge-crit";

      findingsList.innerHTML = res.risk_findings.map(f => `
        <div style="padding: 0.75rem 0; border-bottom: 1px solid var(--border-color);">
          <div style="font-weight: 700; color: ${f.severity === 'CRITICAL' ? 'var(--risk-crit)' : 'var(--risk-high)'};">
            <i class="fa-solid fa-triangle-exclamation"></i> ${f.item}
          </div>
          <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.2rem;">${f.risk}</div>
          ${res.gps && f.severity === 'CRITICAL' ? `
            <div style="margin-top: 0.4rem;">
              <a href="${res.gps.map_url}" target="_blank" style="color: var(--accent-cyan); font-size: 0.85rem; text-decoration: none;">
                <i class="fa-solid fa-map-location-dot"></i> View on OpenStreetMap
              </a>
            </div>
          ` : ''}
        </div>
      `).join("");
    } else {
      document.getElementById("meta-finding-badge").textContent = "CLEAN";
      document.getElementById("meta-finding-badge").className = "badge badge-low";
      findingsList.innerHTML = `<div style="padding: 1rem; color: var(--risk-low);"><i class="fa-solid fa-circle-check"></i> No sensitive GPS or hardware identifiers detected in this photo.</div>`;
    }

    // Raw Metadata Table
    const keys = Object.keys(res.metadata || {});
    document.getElementById("meta-field-count").textContent = `${keys.length} Tags Found`;

    if (keys.length === 0) {
      tbody.innerHTML = `<tr><td colspan="2" style="padding: 1rem; text-align: center; color: var(--text-muted);">No EXIF tags present.</td></tr>`;
    } else {
      tbody.innerHTML = keys.map(k => `
        <tr style="border-bottom: 1px solid var(--border-color);">
          <td style="padding: 0.6rem 1rem; font-family: monospace; color: var(--accent-cyan);">${k}</td>
          <td style="padding: 0.6rem 1rem; color: var(--text-main);">${res.metadata[k]}</td>
        </tr>
      `).join("");
    }

  } catch (err) {
    findingsList.innerHTML = `<div class="alert alert-warning">${err.message}</div>`;
  }
}
