/* ═══════════════════════════════════════════════════════════════════════════
   Daily Report Analyzer - Frontend JavaScript
   ═══════════════════════════════════════════════════════════════════════════ */

// ─── DOM Elements ────────────────────────────────────────────────────────────
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

const uploadZone = $('#uploadZone');
const fileInput = $('#fileInput');
const uploadProgress = $('#uploadProgress');
const progressFill = $('#progressFill');
const progressText = $('#progressText');
const statsBar = $('#statsBar');
const resultsSection = $('#resultsSection');
const latestAnalysis = $('#latestAnalysis');
const toastContainer = $('#toastContainer');
const fetchBtn = $('#fetchBtn');
const analyzeBtn = $('#analyzeBtn');
const fetchProgressCard = $('#fetchProgressCard');
const fetchProgressFill = $('#fetchProgressFill');
const fetchStatusText = $('#fetchStatusText');
const classeraUser = $('#classeraUser');
const classeraPass = $('#classeraPass');
const toggleClasseraVis = $('#toggleClasseraVis');
const classeraStatus = $('#classeraStatus');

// ─── Theme Toggle ────────────────────────────────────────────────────────────
const themeToggle = $('#themeToggle');
const html = document.documentElement;

function initTheme() {
    const saved = localStorage.getItem('theme') || 'dark';
    html.setAttribute('data-theme', saved);
    updateThemeIcon(saved);
}

function toggleTheme() {
    const current = html.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    updateThemeIcon(next);
}

function updateThemeIcon(theme) {
    themeToggle.innerHTML = theme === 'dark'
        ? '<i class="fas fa-sun"></i>'
        : '<i class="fas fa-moon"></i>';
}

themeToggle.addEventListener('click', toggleTheme);
initTheme();

// ─── Settings Modal ──────────────────────────────────────────────────────────
const settingsModal = $('#settingsModal');
const settingsBtn = $('#settingsBtn');
const closeSettingsBtn = $('#closeSettingsBtn');
const apiKeyInput = $('#apiKeyInput');
const toggleKeyVisibility = $('#toggleKeyVisibility');
const saveSettingsBtn = $('#saveSettingsBtn');
const apiStatus = $('#apiStatus');

function openSettings() {
    settingsModal.removeAttribute('hidden');
    settingsModal.style.display = 'flex';
    checkApiStatus();
}

function closeSettings() {
    settingsModal.setAttribute('hidden', '');
    settingsModal.style.display = 'none';
}

settingsBtn.addEventListener('click', openSettings);

closeSettingsBtn.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    closeSettings();
});

settingsModal.addEventListener('click', (e) => {
    if (e.target === settingsModal) closeSettings();
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeSettings();
});

toggleKeyVisibility.addEventListener('click', () => {
    const isPassword = apiKeyInput.type === 'password';
    apiKeyInput.type = isPassword ? 'text' : 'password';
    toggleKeyVisibility.innerHTML = isPassword
        ? '<i class="fas fa-eye-slash"></i>'
        : '<i class="fas fa-eye"></i>';
});

toggleClasseraVis.addEventListener('click', () => {
    const isPassword = classeraPass.type === 'password';
    classeraPass.type = isPassword ? 'text' : 'password';
    toggleClasseraVis.innerHTML = isPassword
        ? '<i class="fas fa-eye-slash"></i>'
        : '<i class="fas fa-eye"></i>';
});

saveSettingsBtn.addEventListener('click', async () => {
    const key = apiKeyInput.value.trim();
    const cUser = classeraUser.value.trim();
    const cPass = classeraPass.value.trim();

    if (!key && !cUser && !cPass) {
        showToast('Nothing to save', 'error');
        return;
    }

    saveSettingsBtn.disabled = true;
    saveSettingsBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';

    try {
        // Save Gemini key if provided
        if (key) {
            const res = await fetch('/api/settings/key', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ key })
            });
            const data = await res.json();
            if (!data.success) {
                showToast(data.error || 'Failed to save API key', 'error');
            }
        }

        // Save Classera creds if provided
        if (cUser && cPass) {
            const res = await fetch('/api/settings/classera', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: cUser, password: cPass })
            });
            const data = await res.json();
            if (!data.success) {
                showToast(data.error || 'Failed to save Classera credentials', 'error');
            }
        }

        showToast('Settings saved successfully!', 'success');
        closeSettings();
        apiKeyInput.value = '';
        classeraUser.value = '';
        classeraPass.value = '';
    } catch (err) {
        showToast('Failed to save settings: ' + err.message, 'error');
    }

    saveSettingsBtn.disabled = false;
    saveSettingsBtn.innerHTML = '<i class="fas fa-save"></i> Save All';
    checkApiStatus();
});

async function checkApiStatus() {
    try {
        const res = await fetch('/api/health');
        const data = await res.json();

        if (data.gemini_configured) {
            apiStatus.className = 'status-indicator ok';
            apiStatus.innerHTML = '<i class="fas fa-circle"></i><span>Gemini: Connected</span>';
        } else {
            apiStatus.className = 'status-indicator error';
            apiStatus.innerHTML = '<i class="fas fa-circle"></i><span>Gemini: Not configured</span>';
        }

        if (data.classera_configured) {
            classeraStatus.className = 'status-indicator ok';
            classeraStatus.innerHTML = '<i class="fas fa-circle"></i><span>Classera: Credentials saved</span>';
        } else {
            classeraStatus.className = 'status-indicator error';
            classeraStatus.innerHTML = '<i class="fas fa-circle"></i><span>Classera: Not configured</span>';
        }
    } catch {
        apiStatus.className = 'status-indicator error';
        apiStatus.innerHTML = '<i class="fas fa-circle"></i><span>Cannot reach server</span>';
        classeraStatus.className = 'status-indicator error';
        classeraStatus.innerHTML = '<i class="fas fa-circle"></i><span>Cannot reach server</span>';
    }
}

// ─── File Upload ─────────────────────────────────────────────────────────────
uploadZone.addEventListener('click', () => fileInput.click());

uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.classList.add('drag-over');
});

uploadZone.addEventListener('dragleave', () => {
    uploadZone.classList.remove('drag-over');
});

uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file) handleFileUpload(file);
});

fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (file) handleFileUpload(file);
    fileInput.value = '';
});

async function handleFileUpload(file) {
    if (!file.name.toLowerCase().endsWith('.pdf')) {
        showToast('Only PDF files are supported', 'error');
        return;
    }

    if (file.size > 16 * 1024 * 1024) {
        showToast('File too large. Maximum 16MB', 'error');
        return;
    }

    // Show progress
    uploadZone.classList.add('analyzing');
    uploadProgress.hidden = false;
    progressFill.style.width = '0%';
    progressText.textContent = `Uploading ${file.name}...`;

    // Animate progress
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += Math.random() * 8;
        if (progress > 85) progress = 85;
        progressFill.style.width = progress + '%';
    }, 300);

    // Update messages during analysis
    setTimeout(() => {
        progressText.textContent = '🤖 Sending to Gemini AI for analysis...';
    }, 1500);
    setTimeout(() => {
        progressText.textContent = '📝 Extracting homework & reminders...';
    }, 4000);

    try {
        const formData = new FormData();
        formData.append('file', file);

        const res = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });

        clearInterval(progressInterval);
        progressFill.style.width = '100%';
        progressText.textContent = '✅ Done!';

        const data = await res.json();

        if (data.success) {
            showToast('Report analyzed successfully!', 'success');
            displayAnalysis(data.data, data.date);
            loadMemory();
        } else {
            showToast(data.error || 'Analysis failed', 'error');
        }
    } catch (err) {
        clearInterval(progressInterval);
        showToast('Upload failed: ' + err.message, 'error');
    }

    // Reset upload zone
    setTimeout(() => {
        uploadZone.classList.remove('analyzing');
        uploadProgress.hidden = true;
        progressFill.style.width = '0%';
    }, 1500);
}

// ─── Display Analysis Results ────────────────────────────────────────────────
function displayAnalysis(data, date) {
    // Show latest analysis card
    latestAnalysis.hidden = false;
    $('#analysisDate').textContent = formatDate(date);
    $('#analysisSummary').textContent = data.summary || 'Analysis complete.';

    resultsSection.hidden = false;
}

// ─── Load Memory ─────────────────────────────────────────────────────────────
async function loadMemory() {
    try {
        const res = await fetch('/api/memory');
        const result = await res.json();

        if (!result.success) return;

        const { data, summary } = result;

        // Update stats
        statsBar.hidden = false;
        $('#statPending').textContent = summary.pending || 0;
        $('#statCompleted').textContent = summary.completed || 0;
        $('#statReminders').textContent = summary.total_reminders || 0;
        $('#statReports').textContent = summary.total_reports || 0;

        // Show results section if there's data
        if (summary.total_homework > 0 || summary.total_reminders > 0 || summary.total_reports > 0) {
            resultsSection.hidden = false;
        }

        // Render homework
        renderHomework(data.homework || []);

        // Render reminders
        renderReminders(data.reminders || []);

        // Render report history
        renderReportHistory(data.reports || []);

        // Update counts
        $('#hwCount').textContent = (data.homework || []).length;
        $('#reminderCount').textContent = (data.reminders || []).length;

    } catch (err) {
        console.error('Failed to load memory:', err);
    }
}

function renderHomework(homework) {
    const container = $('#homeworkList');
    if (!homework.length) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-inbox"></i>
                <p>No homework yet. Upload a report!</p>
            </div>`;
        return;
    }

    container.innerHTML = homework.map(hw => `
        <div class="hw-item ${hw.completed ? 'completed' : ''}" data-id="${hw.id}">
            <input type="checkbox" class="hw-checkbox"
                   ${hw.completed ? 'checked' : ''}
                   onchange="toggleHomework('${hw.id}')">
            <div class="hw-info">
                <div class="hw-subject">${escapeHtml(hw.subject)}</div>
                <div class="hw-task">${escapeHtml(hw.task)}</div>
                <div class="hw-meta">
                    ${hw.due_date ? `<span><i class="fas fa-calendar"></i> Due: ${escapeHtml(hw.due_date)}</span>` : ''}
                    <span><i class="fas fa-clock"></i> ${formatDate(hw.added_date)}</span>
                </div>
            </div>
        </div>
    `).join('');
}

function renderReminders(reminders) {
    const container = $('#reminderList');
    if (!reminders.length) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-bell-slash"></i>
                <p>No reminders yet. Upload a report!</p>
            </div>`;
        return;
    }

    container.innerHTML = reminders.map(r => `
        <div class="reminder-item">
            <div class="reminder-priority ${r.priority || 'medium'}"></div>
            <div>
                <div class="reminder-text">${escapeHtml(r.text)}</div>
                <div class="reminder-date"><i class="fas fa-clock"></i> ${formatDate(r.added_date)}</div>
            </div>
        </div>
    `).join('');
}

function renderReportHistory(reports) {
    const container = $('#reportHistory');
    if (!reports.length) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-folder-open"></i>
                <p>No reports analyzed yet</p>
            </div>`;
        return;
    }

    container.innerHTML = reports.map(r => `
        <div class="report-entry">
            <div class="report-date-info">
                <i class="fas fa-file-pdf"></i>
                <span>${formatDate(r.date)}</span>
            </div>
            <div class="report-counts">
                <span><i class="fas fa-book"></i> ${r.homework_count} HW</span>
                <span><i class="fas fa-bell"></i> ${r.reminder_count} Reminders</span>
            </div>
        </div>
    `).join('');
}

// ─── Toggle Homework ─────────────────────────────────────────────────────────
async function toggleHomework(id) {
    try {
        const res = await fetch(`/api/homework/${id}/toggle`, { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            loadMemory(); // Refresh
        }
    } catch (err) {
        showToast('Failed to update homework', 'error');
    }
}

// ─── Clear Memory ────────────────────────────────────────────────────────────
$('#clearMemoryBtn').addEventListener('click', async () => {
    if (!confirm('Are you sure you want to clear all stored data?')) return;

    try {
        const res = await fetch('/api/memory/clear', { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            showToast('Memory cleared', 'info');
            loadMemory();
            latestAnalysis.hidden = true;
        }
    } catch (err) {
        showToast('Failed to clear memory', 'error');
    }
});

// ─── Toast Notifications ─────────────────────────────────────────────────────
function showToast(message, type = 'info') {
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-circle-exclamation',
        info: 'fa-info-circle'
    };

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas ${icons[type] || icons.info}"></i>
        <span>${escapeHtml(message)}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">
            <i class="fas fa-xmark"></i>
        </button>
    `;

    toastContainer.appendChild(toast);

    // Auto-remove after 5s
    setTimeout(() => {
        if (toast.parentElement) {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(40px)';
            setTimeout(() => toast.remove(), 300);
        }
    }, 5000);
}

// ─── Utilities ───────────────────────────────────────────────────────────────
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateStr) {
    if (!dateStr) return '';
    try {
        const date = new Date(dateStr);
        if (isNaN(date.getTime())) return dateStr;

        const today = new Date();
        const diff = Math.floor((today - date) / (1000 * 60 * 60 * 24));

        if (diff === 0) return 'Today';
        if (diff === 1) return 'Yesterday';
        if (diff < 7) return `${diff} days ago`;

        return date.toLocaleDateString('en-US', {
            month: 'short', day: 'numeric'
        });
    } catch {
        return dateStr;
    }
}

// ─── Fetch from Classera ─────────────────────────────────────────────────────
let fetchPollInterval = null;

fetchBtn.addEventListener('click', async () => {
    fetchBtn.disabled = true;
    fetchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Starting...';
    analyzeBtn.disabled = true;

    try {
        const res = await fetch('/api/fetch', { method: 'POST' });
        const data = await res.json();

        if (!data.success) {
            showToast(data.error || 'Failed to start fetch', 'error');
            fetchBtn.disabled = false;
            fetchBtn.innerHTML = '<i class="fas fa-download"></i> Fetch from Classera';
            return;
        }

        // Show progress card and start polling
        fetchProgressCard.hidden = false;
        fetchProgressCard.removeAttribute('hidden');
        resetFetchSteps();
        startFetchPolling();

    } catch (err) {
        showToast('Failed to start fetch: ' + err.message, 'error');
        fetchBtn.disabled = false;
        fetchBtn.innerHTML = '<i class="fas fa-download"></i> Fetch from Classera';
    }
});

function startFetchPolling() {
    fetchPollInterval = setInterval(async () => {
        try {
            const res = await fetch('/api/fetch/status');
            const data = await res.json();

            // Update progress bar
            fetchProgressFill.style.width = data.progress + '%';
            fetchStatusText.textContent = data.status || 'Working...';

            // Update step indicators
            updateFetchSteps(data.progress);

            // Check if done
            if (!data.running) {
                clearInterval(fetchPollInterval);
                fetchPollInterval = null;

                if (data.error) {
                    showToast('Fetch failed: ' + data.error, 'error');
                    fetchProgressCard.hidden = true;
                    fetchBtn.disabled = false;
                    fetchBtn.innerHTML = '<i class="fas fa-download"></i> Fetch from Classera';
                } else if (data.has_file) {
                    showToast('Report downloaded successfully!', 'success');
                    fetchBtn.disabled = false;
                    fetchBtn.innerHTML = '<i class="fas fa-download"></i> Fetch from Classera';
                    analyzeBtn.disabled = false;

                    // Mark all steps as done
                    $$('.fetch-step').forEach(s => {
                        s.classList.remove('active');
                        s.classList.add('done');
                    });

                    // Auto-hide progress after delay
                    setTimeout(() => {
                        fetchProgressCard.hidden = true;
                    }, 3000);
                }
            }
        } catch (err) {
            console.error('Polling error:', err);
        }
    }, 1500);
}

function resetFetchSteps() {
    $$('.fetch-step').forEach(s => {
        s.classList.remove('active', 'done');
    });
    fetchProgressFill.style.width = '0%';
}

function updateFetchSteps(progress) {
    const steps = $$('.fetch-step');
    const thresholds = [10, 40, 70, 100]; // login, navigate, download, done

    steps.forEach((step, i) => {
        if (progress >= thresholds[i]) {
            step.classList.remove('active');
            step.classList.add('done');
        } else if (i === 0 || progress >= thresholds[i - 1]) {
            step.classList.add('active');
            step.classList.remove('done');
        } else {
            step.classList.remove('active', 'done');
        }
    });
}

// ─── Analyze Fetched Report ──────────────────────────────────────────────────
analyzeBtn.addEventListener('click', async () => {
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';

    try {
        const res = await fetch('/api/analyze/fetched', { method: 'POST' });
        const data = await res.json();

        if (data.success) {
            showToast('Report analyzed successfully!', 'success');
            displayAnalysis(data.data, data.date);
            loadMemory();
        } else {
            showToast(data.error || 'Analysis failed', 'error');
        }
    } catch (err) {
        showToast('Analysis failed: ' + err.message, 'error');
    }

    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = '<i class="fas fa-wand-magic-sparkles"></i> Analyze Report';
});

// ─── Keyboard Shortcuts ──────────────────────────────────────────────────────
document.addEventListener('keydown', (e) => {
    // Ctrl+U to upload
    if (e.ctrlKey && e.key === 'u') {
        e.preventDefault();
        fileInput.click();
    }
});

// ─── Init ────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    loadMemory();
    checkApiStatus();
});
