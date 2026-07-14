/**
 * AI Resume Screening System - AegisScreen AI
 * Core JavaScript Logic & Client-Side Interactive Engine
 */

// ==========================================================================
// DUMMY SEED DATABASE (REPRESENTING NLP-PARSED APPLICANT LOGS)
// ==========================================================================
const SEED_CANDIDATES = [];

// ==========================================================================
// STATE MANAGEMENT & LOCAL STORAGE UTILITIES
// ==========================================================================
class Database {
  static getCandidates() {
    let list = localStorage.getItem("aegis_candidates");
    if (!list) {
      localStorage.setItem("aegis_candidates", JSON.stringify([]));
      return [];
    }
    const parsed = JSON.parse(list);
    if (parsed.some(c => c.id === "marcus_vance" || c.id === "elena_rostova" || c.id === "jonathan_wu" || c.id === "clara_diaz")) {
      localStorage.setItem("aegis_candidates", JSON.stringify([]));
      return [];
    }
    return parsed;
  }

  static saveCandidates(candidates) {
    localStorage.setItem("aegis_candidates", JSON.stringify(candidates));
  }

  static addCandidate(candidate) {
    const list = this.getCandidates();
    list.unshift(candidate); // Insert new uploads at top
    this.saveCandidates(list);
  }

  static updateCandidateStatus(id, newStatus) {
    const list = this.getCandidates();
    const candidate = list.find(c => c.id === id);
    if (candidate) {
      candidate.status = newStatus;
      this.saveCandidates(list);
    }
  }
}

// Initialize database storage on script load
Database.getCandidates();

// ==========================================================================
// GLOBAL COMMON INTERACTIVES (NAVBARS, MENU TRIGGERS, FOOTERS)
// ==========================================================================
document.addEventListener("DOMContentLoaded", () => {
  initGlobalNavbar();
  initBackToTop();
  
  // Route to page-specific controllers
  const path = window.location.pathname;
  if (path.includes("login.html")) {
    initLoginPage();
  } else if (path.includes("upload.html")) {
    initUploadPage();
  } else if (path.includes("dashboard.html")) {
    initDashboardPage();
  } else if (path.includes("about.html")) {
    initAboutPage();
  } else {
    // We are on index.html
    initHomePage();
  }
});

// Scroll Effects and Hamburger Menus
function initGlobalNavbar() {
  const navbar = document.getElementById("mainNavbar");
  const menuToggle = document.getElementById("menuToggle");
  const navLinks = document.getElementById("navLinks");

  // Scrolled navbar transition
  window.addEventListener("scroll", () => {
    if (window.scrollY > 20) {
      navbar?.classList.add("navbar-scrolled");
    } else {
      navbar?.classList.remove("navbar-scrolled");
    }
  });

  // Toggle mobile drawer menu
  menuToggle?.addEventListener("click", () => {
    navLinks?.classList.toggle("active");
    // Simple hamburger animation
    const spans = menuToggle.querySelectorAll("span");
    spans.forEach(s => s.classList.toggle("active"));
  });
}

// Back to Top Button
function initBackToTop() {
  const btn = document.getElementById("backToTop");
  if (!btn) return;

  window.addEventListener("scroll", () => {
    if (window.scrollY > 300) {
      btn.classList.add("visible");
    } else {
      btn.classList.remove("visible");
    }
  });

  btn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

// ==========================================================================
// HOME PAGE INTERACTIVE MODULES (`index.html`)
// ==========================================================================
function initHomePage() {
  // FAQ Accordeons
  const triggers = document.querySelectorAll(".faq-trigger");
  triggers.forEach(trigger => {
    trigger.addEventListener("click", () => {
      const parent = trigger.parentElement;
      const isActive = parent.classList.contains("active");
      
      // Close all FAQs first
      document.querySelectorAll(".faq-item").forEach(item => {
        item.classList.remove("active");
      });

      if (!isActive) {
        parent.classList.add("active");
      }
    });
  });
}

// ==========================================================================
// LOGIN PAGE CONTROLLER (`login.html`)
// ==========================================================================
function initLoginPage() {
  const form = document.getElementById("loginForm");
  const alertBanner = document.getElementById("loginAlert");
  const emailInput = document.getElementById("emailInput");
  const passwordInput = document.getElementById("passwordInput");
  const passToggle = document.getElementById("passwordToggle");
  const createAccountBtn = document.getElementById("createAccountBtn");
  const forgotPasswordBtn = document.getElementById("forgotPasswordBtn");

  // Show/Hide password toggle
  passToggle?.addEventListener("click", () => {
    const isPass = passwordInput.getAttribute("type") === "password";
    passwordInput.setAttribute("type", isPass ? "text" : "password");
    passToggle.style.color = isPass ? "var(--color-accent)" : "var(--text-secondary)";
  });

  // Form Submission
  form?.addEventListener("submit", (e) => {
    e.preventDefault();
    const email = emailInput.value.trim();

    // Extract Name from Email for visual layout purposes
    let recruiterName = "Recruiter Profile";
    const parts = email.split("@")[0].split(".");
    if (parts.length > 0) {
      recruiterName = parts.map(p => p.charAt(0).toUpperCase() + p.slice(1)).join(" ");
    }
    localStorage.setItem("aegis_recruiter_name", recruiterName);

    // Redirect directly to dashboard
    window.location.href = "dashboard.html";
  });

  // Create Recruiter UI
  createAccountBtn?.addEventListener("click", () => {
    alert("Recruiter account registration will be integrated with the Flask database backend.");
  });

  // Forgot password
  forgotPasswordBtn?.addEventListener("click", (e) => {
    e.preventDefault();
    alert("Password recovery services will be integrated with the Flask authentication APIs.");
  });
}

// ==========================================================================
// UPLOAD RESUME PAGE CONTROLLER (`upload.html`)
// ==========================================================================
function initUploadPage() {
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("fileInput");
  const browseBtn = document.getElementById("browseBtn");
  const selectedFilesList = document.getElementById("selectedFilesList");
  const progressWrapper = document.getElementById("progressWrapper");
  const progressBarFill = document.getElementById("progressBarFill");
  const progressStatus = document.getElementById("progressStatus");
  const progressPercentage = document.getElementById("progressPercentage");
  const analyzeBtn = document.getElementById("analyzeBtn");
  const clearFilesBtn = document.getElementById("clearFilesBtn");

  let filesToUpload = [];

  // Drag and Drop Listeners
  ["dragenter", "dragover"].forEach(eventName => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropzone.classList.add("dragover");
    }, false);
  });

  ["dragleave", "drop"].forEach(eventName => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropzone.classList.remove("dragover");
    }, false);
  });

  dropzone.addEventListener("drop", (e) => {
    const dt = e.dataTransfer;
    const files = Array.from(dt.files);
    handleSelectedFiles(files);
  });

  browseBtn.addEventListener("click", () => {
    fileInput.click();
  });

  fileInput.addEventListener("change", () => {
    const files = Array.from(fileInput.files);
    handleSelectedFiles(files);
  });

  // Handle files selection
  function handleSelectedFiles(files) {
    // Filter out unsupported extensions
    const supportedTypes = ["pdf", "doc", "docx"];
    const filtered = files.filter(f => {
      const ext = f.name.split(".").pop().toLowerCase();
      return supportedTypes.includes(ext);
    });

    if (filtered.length === 0) {
      alert("Unsupported format. Please select only PDF, DOC or DOCX files.");
      return;
    }

    filesToUpload = [...filesToUpload, ...filtered];
    renderFilesList();
    toggleUploadButtons();
  }

  // Display selected files
  function renderFilesList() {
    selectedFilesList.innerHTML = "";
    filesToUpload.forEach((file, index) => {
      const formattedSize = (file.size / (1024 * 1024)).toFixed(2) + " MB";
      const fileCard = document.createElement("div");
      fileCard.className = "file-item";
      fileCard.innerHTML = `
        <div class="file-info">
          <svg class="file-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
          <div class="file-details">
            <span class="file-name" title="${file.name}">${file.name}</span>
            <span class="file-size">${formattedSize}</span>
          </div>
        </div>
        <button class="file-remove-btn" data-index="${index}">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      `;
      selectedFilesList.appendChild(fileCard);
    });

    // Attach deletion triggers
    document.querySelectorAll(".file-remove-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const index = parseInt(btn.getAttribute("data-index"));
        filesToUpload.splice(index, 1);
        renderFilesList();
        toggleUploadButtons();
      });
    });
  }

  function toggleUploadButtons() {
    const hasFiles = filesToUpload.length > 0;
    analyzeBtn.disabled = !hasFiles;
    clearFilesBtn.style.display = hasFiles ? "inline-flex" : "none";
  }

  clearFilesBtn.addEventListener("click", () => {
    filesToUpload = [];
    renderFilesList();
    toggleUploadButtons();
    progressWrapper.style.display = "none";
  });

  // Run Upload Analysis Simulation
  analyzeBtn.addEventListener("click", () => {
    if (filesToUpload.length === 0) return;

    analyzeBtn.disabled = true;
    clearFilesBtn.style.display = "none";
    progressWrapper.style.display = "block";
    progressBarFill.style.width = "0%";
    progressPercentage.innerText = "0%";
    progressStatus.innerText = "Reading document formatting structure...";

    let percent = 0;
    const interval = setInterval(() => {
      percent += 10;
      progressBarFill.style.width = percent + "%";
      progressPercentage.innerText = percent + "%";

      if (percent === 30) {
        progressStatus.innerText = "Ingesting file layers...";
      } else if (percent === 60) {
        progressStatus.innerText = "Running Named Entity Recognition & Skill Parsing...";
      } else if (percent === 80) {
        progressStatus.innerText = "Calculating job compatibility index and ATS weights...";
      } else if (percent === 100) {
        clearInterval(interval);
        progressStatus.innerText = "Upload complete! Awaiting Flask backend connection...";
        alert("Upload simulation finished. In the production app, this will POST the selected resume file to your Flask API endpoint for processing.");
        
        // Reset controls
        filesToUpload = [];
        renderFilesList();
        toggleUploadButtons();
        progressWrapper.style.display = "none";
      }
    }, 250);
  });
}

// ==========================================================================
// RECRUITER DASHBOARD CONTROLLER (`dashboard.html`)
// ==========================================================================
function initDashboardPage() {
  const tableBody = document.getElementById("candidateTableBody");
  const searchInput = document.getElementById("candidateSearchInput");
  const profName = document.getElementById("profName");
  const profAvatar = document.getElementById("profAvatar");
  const profPredictedRole = document.getElementById("profPredictedRole");
  const profConfidence = document.getElementById("profConfidenceBadge");
  const profRatingStars = document.getElementById("profRatingStars");
  const profStatusBadge = document.getElementById("profStatusBadge");
  const profAtsScore = document.getElementById("profAtsScore");
  const profStrengthFill = document.getElementById("profStrengthFill");
  const profStrengthLabel = document.getElementById("profStrengthLabel");
  const profSummary = document.getElementById("profSummary");
  const profExtractedSkills = document.getElementById("profExtractedSkills");
  const profExperienceTimeline = document.getElementById("profExperienceTimeline");
  const profEducationTimeline = document.getElementById("profEducationTimeline");
  const profMissingSkills = document.getElementById("profMissingSkills");
  const profRecommendedSkills = document.getElementById("profRecommendedSkills");
  
  const btnShortlist = document.getElementById("btnShortlist");
  const btnReject = document.getElementById("btnReject");
  const btnDownloadReport = document.getElementById("btnDownloadReport");

  // Metrics elements
  const metricTotal = document.getElementById("totalResumesMetric");
  const metricShortlisted = document.getElementById("shortlistedResumesMetric");
  const metricRejected = document.getElementById("rejectedResumesMetric");
  const metricAvgAts = document.getElementById("avgAtsMetric");
  const candidateCountLabel = document.getElementById("candidateCountLabel");

  // Recruiter Profile Initial
  const recruiterNameText = document.getElementById("recruiterNameText");
  const storedRecruiterName = localStorage.getItem("aegis_recruiter_name");
  if (storedRecruiterName && recruiterNameText) {
    recruiterNameText.innerText = storedRecruiterName;
    const sidebarAvatar = document.querySelector(".sidebar-footer .recruiter-avatar");
    if (sidebarAvatar) {
      sidebarAvatar.innerText = storedRecruiterName.split(" ").map(n => n[0]).join("");
    }
  }

  // Handle Mobile sidebar draw
  const sidebar = document.getElementById("dashboardSidebar");
  const sidebarToggle = document.getElementById("mobileSidebarToggle");
  sidebarToggle?.addEventListener("click", () => {
    sidebar.classList.toggle("active");
  });

  let candidates = Database.getCandidates();
  let currentCandidate = candidates[0]; // Default selection

  // Query parameter check (e.g. upload redirect)
  const urlParams = new URLSearchParams(window.location.search);
  const paramCandidate = urlParams.get("candidate");
  if (paramCandidate) {
    const matched = candidates.find(c => c.name.toLowerCase() === paramCandidate.toLowerCase());
    if (matched) {
      currentCandidate = matched;
    }
  }

  // Populate recruiter menu alert indicators
  const notifyBtn = document.getElementById("notificationBtn");
  notifyBtn?.addEventListener("click", () => {
    alert("Active Alerts: System operational. Parsed pipeline data is stored in the local cache. Future alerts will notify of automated background imports.");
    const badge = notifyBtn.querySelector(".notification-badge");
    if (badge) badge.style.display = "none";
  });

  // Search Filter listener
  searchInput?.addEventListener("input", () => {
    renderCandidateList(searchInput.value.trim());
  });

  // ==========================================================================
  // TAB NAVIGATION SYSTEM
  // ==========================================================================
  const menuItems = document.querySelectorAll("#sidebarMenu .sidebar-item");
  const tabPanels = document.querySelectorAll(".dashboard-tab-panel");

  menuItems.forEach(item => {
    const tabName = item.getAttribute("data-tab");
    // Ignore items that link directly to pages (like Upload Resume)
    if (!tabName) return;

    item.querySelector("a").addEventListener("click", (e) => {
      e.preventDefault();
      
      // Update sidebar active classes
      menuItems.forEach(mi => mi.classList.remove("active"));
      item.classList.add("active");

      // Hide all panels
      tabPanels.forEach(panel => panel.style.display = "none");

      // Show target panel
      const targetPanel = document.getElementById(`tab-content-${tabName}`);
      if (targetPanel) {
        targetPanel.style.display = "flex";
      }

      // Refresh specific tab data
      if (tabName === "dashboard") {
        renderDashboard();
      } else if (tabName === "candidates") {
        renderRegistryTable();
      } else if (tabName === "analytics") {
        renderAnalyticsData();
      } else if (tabName === "settings") {
        initSettingsTab();
      }
      
      // Close mobile drawer if active
      sidebar?.classList.remove("active");
    });
  });

  // Initial render
  renderDashboard();

  function renderDashboard() {
    candidates = Database.getCandidates();
    // Fallback if current candidate was deleted
    if (candidates.length > 0 && !candidates.find(c => c.id === currentCandidate?.id)) {
      currentCandidate = candidates[0];
    }
    updateMetrics();
    renderCandidateList();
    if (candidates.length > 0) {
      renderCandidateDetail(currentCandidate);
      document.getElementById("profilerContainer").style.display = "flex";
    } else {
      // Empty candidate state
      clearCandidateDetail();
      document.getElementById("profilerContainer").style.display = "flex";
      if (tableBody) {
        tableBody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding: 2rem; color:var(--text-secondary);">No resumes analyzed yet.</td></tr>`;
      }
    }
  }

  // Recalculate KPIs
  function updateMetrics() {
    if (!metricTotal) return;
    const total = candidates.length;
    const shortlisted = candidates.filter(c => c.status === "Shortlisted").length;
    const rejected = candidates.filter(c => c.status === "Rejected").length;
    
    // Average ATS
    const sumAts = candidates.reduce((sum, c) => sum + c.atsScore, 0);
    const avgAts = total > 0 ? (sumAts / total).toFixed(1) + "%" : "0%";

    metricTotal.innerText = total;
    metricShortlisted.innerText = shortlisted;
    metricRejected.innerText = rejected;
    metricAvgAts.innerText = avgAts;
    candidateCountLabel.innerText = `${total} Total`;
  }

  // Render Table
  function renderCandidateList(query = "") {
    if (!tableBody) return;
    tableBody.innerHTML = "";
    
    const search = query.toLowerCase();
    const filtered = candidates.filter(c => {
      return c.name.toLowerCase().includes(search) || 
             c.role.toLowerCase().includes(search) ||
             c.skills.some(s => s.toLowerCase().includes(search));
    });

    if (candidates.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding: 2rem; color:var(--text-secondary);">No resumes analyzed yet.</td></tr>`;
      return;
    }

    if (filtered.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding: 2rem; color:var(--text-secondary);">No applicants match search parameters.</td></tr>`;
      return;
    }

    filtered.forEach(c => {
      const row = document.createElement("tr");
      if (currentCandidate && c.id === currentCandidate.id) {
        row.className = "selected-row";
      }

      // Status Badge mapping
      let badgeClass = "badge-info";
      if (c.status === "Shortlisted") badgeClass = "badge-success";
      if (c.status === "Rejected") badgeClass = "badge-danger";

      row.innerHTML = `
        <td>
          <div style="font-weight:600;">${c.name}</div>
        </td>
        <td>${c.role}</td>
        <td><strong>${c.atsScore}%</strong></td>
        <td>${c.id === "marcus_vance" || c.id === "elena_rostova" ? "8 yrs" : "4 yrs"}</td>
        <td><span class="badge ${badgeClass}">${c.status}</span></td>
      `;

      row.addEventListener("click", () => {
        currentCandidate = c;
        // Update table selection CSS
        document.querySelectorAll("#candidateTableBody tr").forEach(r => r.classList.remove("selected-row"));
        row.classList.add("selected-row");
        
        // Render Detail Panel
        renderCandidateDetail(c);
      });

      tableBody.appendChild(row);
    });
  }

  // Render Candidate Profiler Panel
  function renderCandidateDetail(c) {
    if (!c || !profName) return;

    profName.innerText = c.name;
    profAvatar.innerText = c.avatar;
    profPredictedRole.innerText = c.role;
    profConfidence.innerText = `Prediction Conf: ${c.confidence}`;
    profAtsScore.innerText = `${c.atsScore}%`;
    profStrengthFill.style.width = `${c.strength}%`;
    profStrengthLabel.innerText = c.strengthLabel;
    profSummary.innerText = c.summary;

    // Status Styling
    profStatusBadge.className = "badge";
    if (c.status === "Shortlisted") {
      profStatusBadge.classList.add("badge-success");
      profStatusBadge.innerText = "Shortlisted";
    } else if (c.status === "Rejected") {
      profStatusBadge.classList.add("badge-danger");
      profStatusBadge.innerText = "Rejected";
    } else {
      profStatusBadge.classList.add("badge-info");
      profStatusBadge.innerText = "Pending Review";
    }

    // Stars
    profRatingStars.innerHTML = "";
    for (let i = 1; i <= 5; i++) {
      if (i <= c.rating) {
        profRatingStars.innerHTML += "★";
      } else {
        profRatingStars.innerHTML += "☆";
      }
    }

    // Extracted Skills
    profExtractedSkills.innerHTML = "";
    c.skills.forEach(skill => {
      const pill = document.createElement("span");
      pill.className = "pill pill-accent";
      pill.innerText = skill;
      profExtractedSkills.appendChild(pill);
    });

    // Missing Skills
    profMissingSkills.innerHTML = "";
    c.missingSkills.forEach(skill => {
      const pill = document.createElement("span");
      pill.className = "pill pill-danger";
      pill.innerText = skill;
      profMissingSkills.appendChild(pill);
    });

    // Recommended Skills
    profRecommendedSkills.innerHTML = "";
    c.recommendedSkills.forEach(skill => {
      const pill = document.createElement("span");
      pill.className = "pill";
      pill.innerText = skill;
      profRecommendedSkills.appendChild(pill);
    });

    // Employment Timeline
    profExperienceTimeline.innerHTML = "";
    c.experience.forEach(exp => {
      const item = document.createElement("div");
      item.className = "timeline-item";
      item.innerHTML = `
        <div class="timeline-title">${exp.role}</div>
        <div class="timeline-subtitle">${exp.company} | ${exp.years}</div>
        <div class="timeline-desc">${exp.desc}</div>
      `;
      profExperienceTimeline.appendChild(item);
    });

    // Academic Timeline
    profEducationTimeline.innerHTML = "";
    c.education.forEach(edu => {
      const item = document.createElement("div");
      item.className = "timeline-item";
      item.innerHTML = `
        <div class="timeline-title">${edu.degree}</div>
        <div class="timeline-subtitle">${edu.school} | ${edu.years}</div>
        <div class="timeline-desc">${edu.desc}</div>
      `;
      profEducationTimeline.appendChild(item);
    });
  }

  function clearCandidateDetail() {
    if (!profName) return;
    profName.innerText = "No candidate selected";
    profAvatar.innerText = "--";
    profPredictedRole.innerText = "Results will appear after AI analysis";
    profConfidence.innerText = "Awaiting Ingestion";
    profAtsScore.innerText = "0%";
    profStrengthFill.style.width = "0%";
    profStrengthLabel.innerText = "Waiting for upload";
    profSummary.innerText = "No candidate selected. Upload a resume to begin analysis.";
    profRatingStars.innerHTML = "";
    profExtractedSkills.innerHTML = "";
    profMissingSkills.innerHTML = "";
    profRecommendedSkills.innerHTML = "";
    profExperienceTimeline.innerHTML = "";
    profEducationTimeline.innerHTML = "";
    profStatusBadge.className = "badge";
    profStatusBadge.innerText = "Awaiting Review";
  }

  // Recruiter Decision Actions
  btnShortlist?.addEventListener("click", () => {
    if (!currentCandidate) return;
    Database.updateCandidateStatus(currentCandidate.id, "Shortlisted");
    renderDashboard();
  });

  btnReject?.addEventListener("click", () => {
    if (!currentCandidate) return;
    Database.updateCandidateStatus(currentCandidate.id, "Rejected");
    renderDashboard();
  });

  btnDownloadReport?.addEventListener("click", () => {
    if (!currentCandidate) return;
    
    // Convert Candidate Object to JSON formatted text
    const jsonStr = JSON.stringify(currentCandidate, null, 2);
    
    // Create element download
    const blob = new Blob([jsonStr], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `candidate_analysis_${currentCandidate.id}.json`;
    document.body.appendChild(a);
    a.click();
    
    // Clean up
    setTimeout(() => {
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    }, 0);
  });

  // ==========================================================================
  // CANDIDATES REGISTRY TAB CONTROLLER
  // ==========================================================================
  const registryTableBody = document.getElementById("registryTableBody");
  const filterStatus = document.getElementById("registryFilterStatus");
  const filterRole = document.getElementById("registryFilterRole");

  // Attach filters listeners
  [filterStatus, filterRole].forEach(filter => {
    filter?.addEventListener("change", renderRegistryTable);
  });

  function renderRegistryTable() {
    if (!registryTableBody) return;
    registryTableBody.innerHTML = "";
    
    candidates = Database.getCandidates();
    const statusVal = filterStatus ? filterStatus.value : "All";
    const roleVal = filterRole ? filterRole.value : "All";

    const filtered = candidates.filter(c => {
      const matchStatus = (statusVal === "All" || c.status === statusVal);
      
      let matchRole = true;
      if (roleVal !== "All") {
        if (roleVal === "DevOps") matchRole = c.role.includes("DevOps") || c.role.includes("Cloud");
        else if (roleVal === "ML") matchRole = c.role.includes("ML") || c.role.includes("Scientist");
        else if (roleVal === "Fullstack") matchRole = c.role.includes("Fullstack") || c.role.includes("Frontend");
        else if (roleVal === "Designer") matchRole = c.role.includes("Designer") || c.role.includes("UI");
      }

      return matchStatus && matchRole;
    });

    if (candidates.length === 0) {
      registryTableBody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 2rem; color:var(--text-secondary);">No resumes analyzed yet.</td></tr>`;
      return;
    }

    if (filtered.length === 0) {
      registryTableBody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 2rem; color:var(--text-secondary);">No registry candidates match filters.</td></tr>`;
      return;
    }

    filtered.forEach(c => {
      const row = document.createElement("tr");

      let badgeClass = "badge-info";
      if (c.status === "Shortlisted") badgeClass = "badge-success";
      if (c.status === "Rejected") badgeClass = "badge-danger";

      row.innerHTML = `
        <td><strong>${c.name}</strong></td>
        <td>${c.role}</td>
        <td><strong>${c.atsScore}%</strong></td>
        <td>${c.confidence}</td>
        <td><span class="badge ${badgeClass}">${c.status}</span></td>
        <td>
          <div style="display:flex; gap:0.5rem;">
            <button class="btn btn-success btn-sm btn-action-short" data-id="${c.id}" style="padding: 0.35rem 0.6rem; font-size:0.75rem;">Shortlist</button>
            <button class="btn btn-danger btn-sm btn-action-reject" data-id="${c.id}" style="padding: 0.35rem 0.6rem; font-size:0.75rem;">Reject</button>
            <button class="btn btn-secondary btn-sm btn-action-delete" data-id="${c.id}" style="padding: 0.35rem 0.6rem; font-size:0.75rem; color:var(--color-danger);">Delete</button>
          </div>
        </td>
      `;

      // Button listeners
      row.querySelector(".btn-action-short").addEventListener("click", () => {
        Database.updateCandidateStatus(c.id, "Shortlisted");
        renderRegistryTable();
      });

      row.querySelector(".btn-action-reject").addEventListener("click", () => {
        Database.updateCandidateStatus(c.id, "Rejected");
        renderRegistryTable();
      });

      row.querySelector(".btn-action-delete").addEventListener("click", () => {
        if (confirm(`Are you sure you want to permanently delete candidate ${c.name}?`)) {
          let list = Database.getCandidates();
          list = list.filter(item => item.id !== c.id);
          Database.saveCandidates(list);
          renderRegistryTable();
        }
      });

      registryTableBody.appendChild(row);
    });
  }

  // ==========================================================================
  // ANALYTICS TAB CONTROLLER
  // ==========================================================================
  function renderAnalyticsData() {
    candidates = Database.getCandidates();
    const total = candidates.length;

    const placeholder = document.getElementById("analyticsPlaceholder");
    const content = document.getElementById("analyticsContent");

    if (total === 0) {
      if (placeholder) placeholder.style.display = "flex";
      if (content) content.style.display = "none";
      return;
    } else {
      if (placeholder) placeholder.style.display = "none";
      if (content) content.style.display = "flex";
    }
    
    // Average ATS
    const sumAts = candidates.reduce((sum, c) => sum + c.atsScore, 0);
    const avgAts = total > 0 ? (sumAts / total).toFixed(1) + "%" : "0%";
    const metricAnalyticsAvgAts = document.getElementById("analyticsAvgAts");
    if (metricAnalyticsAvgAts) metricAnalyticsAvgAts.innerText = avgAts;

    // Status Percentages
    const shortlistedCount = candidates.filter(c => c.status === "Shortlisted").length;
    const pendingCount = candidates.filter(c => c.status === "Pending Review").length;
    const rejectedCount = candidates.filter(c => c.status === "Rejected").length;

    const shortPct = total > 0 ? ((shortlistedCount / total) * 100).toFixed(0) : 0;
    const pendPct = total > 0 ? ((pendingCount / total) * 100).toFixed(0) : 0;
    const rejectPct = total > 0 ? ((rejectedCount / total) * 100).toFixed(0) : 0;

    // Set Text Labels
    const labelShort = document.getElementById("analyticsShortlistedPct");
    const labelPend = document.getElementById("analyticsPendingPct");
    const labelReject = document.getElementById("analyticsRejectedPct");
    if (labelShort) labelShort.innerText = `${shortPct}%`;
    if (labelPend) labelPend.innerText = `${pendPct}%`;
    if (labelReject) labelReject.innerText = `${rejectPct}%`;

    // Set Widths
    const fillShort = document.getElementById("analyticsShortlistedFill");
    const fillPend = document.getElementById("analyticsPendingFill");
    const fillReject = document.getElementById("analyticsRejectedFill");
    if (fillShort) fillShort.style.width = `${shortPct}%`;
    if (fillPend) fillPend.style.width = `${pendPct}%`;
    if (fillReject) fillReject.style.width = `${rejectPct}%`;

    // Calculate Distribution ranges count
    const range1 = candidates.filter(c => c.atsScore < 75).length;
    const range2 = candidates.filter(c => c.atsScore >= 75 && c.atsScore < 80).length;
    const range3 = candidates.filter(c => c.atsScore >= 80 && c.atsScore < 85).length;
    const range4 = candidates.filter(c => c.atsScore >= 85 && c.atsScore < 90).length;
    const range5 = candidates.filter(c => c.atsScore >= 90).length;

    const ranges = [range1, range2, range3, range4, range5];
    const maxCount = Math.max(...ranges, 1); // Avoid divide by zero

    // Update charts bar heights and tooltips
    for (let i = 1; i <= 5; i++) {
      const bar = document.getElementById(`bar-range-${i}`);
      const tooltip = document.getElementById(`tooltip-range-${i}`);
      const count = ranges[i - 1];

      if (bar) {
        const heightPct = total > 0 ? (count / maxCount) * 100 : 0;
        bar.style.height = `${Math.max(heightPct, heightPct > 0 ? 10 : 0)}%`; // Minimum 10% height for visual block if count > 0
      }
      if (tooltip) {
        tooltip.innerText = `${count} Candidate${count !== 1 ? "s" : ""}`;
      }
    }
  }

  // ==========================================================================
  // CONFIGURATION SETTINGS TAB CONTROLLER
  // ==========================================================================
  function initSettingsTab() {
    const sliders = [
      { slider: "cfgShortlistThreshold", label: "cfgShortlistThresholdVal", suffix: "%" },
      { slider: "cfgWeightSkills", label: "cfgWeightSkillsVal", suffix: "%" },
      { slider: "cfgWeightExp", label: "cfgWeightExpVal", suffix: "%" }
    ];

    sliders.forEach(s => {
      const elSlider = document.getElementById(s.slider);
      const elLabel = document.getElementById(s.label);

      if (elSlider && elLabel) {
        // Read previous stored weight or use default value
        const storedVal = localStorage.getItem(`aegis_setting_${s.slider}`);
        if (storedVal) {
          elSlider.value = storedVal;
          elLabel.innerText = storedVal + s.suffix;
        }

        // Live update labels on slide drag
        elSlider.addEventListener("input", () => {
          elLabel.innerText = elSlider.value + s.suffix;
        });
      }
    });

    const settingsForm = document.getElementById("systemSettingsForm");
    settingsForm?.addEventListener("submit", (e) => {
      e.preventDefault();
      
      // Save settings to LocalStorage
      sliders.forEach(s => {
        const elSlider = document.getElementById(s.slider);
        if (elSlider) {
          localStorage.setItem(`aegis_setting_${s.slider}`, elSlider.value);
        }
      });
      
      const enableOcr = document.getElementById("cfgEnableOcr");
      const enableDiag = document.getElementById("cfgEnableDiagnostics");
      if (enableOcr) localStorage.setItem("aegis_setting_cfgEnableOcr", enableOcr.checked);
      if (enableDiag) localStorage.setItem("aegis_setting_cfgEnableDiagnostics", enableDiag.checked);

      alert("Recruiter matching configurations and parser thresholds updated successfully!");
    });
  }
}

// ==========================================================================
// ABOUT PAGE CONTROLLER (`about.html`)
// ==========================================================================
function initAboutPage() {
  const contactForm = document.getElementById("aboutContactForm");
  
  contactForm?.addEventListener("submit", (e) => {
    e.preventDefault();
    alert("Thank you! Your inquiry has been logged successfully. An integration representative will reach out to your team shortly.");
    contactForm.reset();
  });
}
