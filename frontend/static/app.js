"use strict";

const API_BASE = "http://localhost:8000";

// ─── State ──────────────────────────────────────────────────────────────────

const state = {
  projects: [],
  currentProjectId: null,
  filterStatus: "",
  filterPriority: "",
};

// ─── DOM References ─────────────────────────────────────────────────────────

const dom = {
  // Stats
  statTotal:     () => document.getElementById("stat-total-value"),
  statActive:    () => document.getElementById("stat-active-value"),
  statCompleted: () => document.getElementById("stat-completed-value"),
  statOverdue:   () => document.getElementById("stat-overdue-value"),

  // Filters
  filterStatus:   () => document.getElementById("filter-status"),
  filterPriority: () => document.getElementById("filter-priority"),
  btnClearFilters: () => document.getElementById("btn-clear-filters"),

  // Projects
  projectsGrid:    () => document.getElementById("projects-grid"),
  projectsEmpty:   () => document.getElementById("projects-empty"),
  projectsLoading: () => document.getElementById("projects-loading"),
  projectsError:   () => document.getElementById("projects-error"),
  projectsErrorMsg:() => document.getElementById("projects-error-msg"),
  btnRetry:        () => document.getElementById("btn-retry"),

  // Add Project Modal
  modalAdd:         () => document.getElementById("modal-add-project"),
  btnAddProject:    () => document.getElementById("btn-add-project"),
  btnCloseAddModal: () => document.getElementById("btn-close-add-modal"),
  btnCancelAdd:     () => document.getElementById("btn-cancel-add"),
  formAdd:          () => document.getElementById("form-add-project"),
  addTitle:         () => document.getElementById("add-title"),
  addDescription:   () => document.getElementById("add-description"),
  addPriority:      () => document.getElementById("add-priority"),
  addDeadline:      () => document.getElementById("add-deadline"),
  addTitleError:    () => document.getElementById("add-title-error"),
  addFormError:     () => document.getElementById("add-form-error"),
  btnSubmitAdd:     () => document.getElementById("btn-submit-add"),

  // Detail Modal
  modalDetail:       () => document.getElementById("modal-detail"),
  btnCloseDetail:    () => document.getElementById("btn-close-detail"),
  btnCancelDetail:   () => document.getElementById("btn-cancel-detail"),
  detailLoading:     () => document.getElementById("detail-loading"),
  detailContent:     () => document.getElementById("detail-content"),
  detailError:       () => document.getElementById("detail-error"),
  detailErrorMsg:    () => document.getElementById("detail-error-msg"),
  formEdit:          () => document.getElementById("form-edit-project"),
  detailProjectId:   () => document.getElementById("detail-project-id"),
  detailTitleInput:  () => document.getElementById("detail-title-input"),
  detailTitleError:  () => document.getElementById("detail-title-error"),
  detailDescription: () => document.getElementById("detail-description"),
  detailStatus:      () => document.getElementById("detail-status"),
  detailPriority:    () => document.getElementById("detail-priority"),
  detailDeadline:    () => document.getElementById("detail-deadline"),
  detailFormError:   () => document.getElementById("detail-form-error"),
  btnSaveProject:    () => document.getElementById("btn-save-project"),
  btnDeleteProject:  () => document.getElementById("btn-delete-project"),
  taskList:          () => document.getElementById("task-list"),
  taskListEmpty:     () => document.getElementById("task-list-empty"),
  formAddTask:       () => document.getElementById("form-add-task"),
  newTaskInput:      () => document.getElementById("new-task-input"),
  btnAddTask:        () => document.getElementById("btn-add-task"),
  taskError:         () => document.getElementById("task-error"),

  // Confirm Delete Modal
  modalConfirmDelete: () => document.getElementById("modal-confirm-delete"),
  btnCancelDelete:    () => document.getElementById("btn-cancel-delete"),
  btnConfirmDelete:   () => document.getElementById("btn-confirm-delete"),

  // Toast
  toast: () => document.getElementById("toast"),
};

// ─── Toast ───────────────────────────────────────────────────────────────────

let toastTimer = null;

function showToast(message, type = "success") {
  const toast = dom.toast();
  toast.textContent = message;
  toast.className = `toast toast--${type}`;
  toast.hidden = false;

  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toast.hidden = true;
  }, 3000);
}

// ─── API Helpers ──────────────────────────────────────────────────────────────

async function apiFetch(path, options = {}) {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });

  if (res.status === 204) return null; // No Content

  let data;
  try {
    data = await res.json();
  } catch {
    throw new Error(`Server returned ${res.status} with non-JSON body.`);
  }

  if (!res.ok) {
    const msg = data?.detail || `Request failed with status ${res.status}`;
    throw new Error(typeof msg === "string" ? msg : JSON.stringify(msg));
  }

  return data;
}

// ─── Date Helpers ─────────────────────────────────────────────────────────────

function isOverdue(deadline, status) {
  if (!deadline || status === "completed") return false;
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const dl = new Date(deadline);
  return dl < today;
}

function formatDate(dateStr) {
  if (!dateStr) return null;
  const d = new Date(dateStr + "T00:00:00");
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

// ─── Badge Builders ───────────────────────────────────────────────────────────

function statusBadge(status) {
  const el = document.createElement("span");
  el.className = `badge badge-status-${status}`;
  el.textContent = status;
  return el;
}

function priorityBadge(priority) {
  const el = document.createElement("span");
  el.className = `badge badge-priority-${priority}`;
  el.textContent = priority;
  return el;
}

// ─── Stats ────────────────────────────────────────────────────────────────────

async function loadStats() {
  try {
    const stats = await apiFetch("/api/stats");
    dom.statTotal().textContent     = stats.total_projects;
    dom.statActive().textContent    = stats.by_status?.active ?? 0;
    dom.statCompleted().textContent = stats.by_status?.completed ?? 0;
    dom.statOverdue().textContent   = stats.overdue_count;
  } catch (err) {
    // Stats failure is non-critical, show dashes
    dom.statTotal().textContent     = "—";
    dom.statActive().textContent    = "—";
    dom.statCompleted().textContent = "—";
    dom.statOverdue().textContent   = "—";
  }
}

// ─── Projects List ────────────────────────────────────────────────────────────

async function loadProjects() {
  showProjectsState("loading");

  const params = new URLSearchParams();
  if (state.filterStatus)   params.set("status", state.filterStatus);
  if (state.filterPriority) params.set("priority", state.filterPriority);

  const query = params.toString() ? `?${params}` : "";

  try {
    const projects = await apiFetch(`/api/projects${query}`);
    state.projects = projects;
    renderProjectCards(projects);
    if (projects.length === 0) {
      showProjectsState("empty");
    } else {
      showProjectsState("list");
    }
  } catch (err) {
    dom.projectsErrorMsg().textContent = `Failed to load projects: ${err.message}`;
    showProjectsState("error");
  }
}

function showProjectsState(stateKey) {
  dom.projectsGrid().hidden    = stateKey !== "list";
  dom.projectsEmpty().hidden   = stateKey !== "empty";
  dom.projectsLoading().hidden = stateKey !== "loading";
  dom.projectsError().hidden   = stateKey !== "error";
}

function renderProjectCards(projects) {
  const grid = dom.projectsGrid();
  grid.innerHTML = "";

  for (const p of projects) {
    const card = buildProjectCard(p);
    grid.appendChild(card);
  }
}

function buildProjectCard(p) {
  const totalTasks = p.total_tasks ?? 0;
  const doneTasks  = p.done_tasks ?? 0;
  const overdue    = isOverdue(p.deadline, p.status);
  const pct        = totalTasks > 0 ? Math.round((doneTasks / totalTasks) * 100) : 0;

  const card = document.createElement("article");
  card.className = "project-card";
  card.setAttribute("role", "listitem");
  card.setAttribute("tabindex", "0");
  card.dataset.projectId = p.id;
  card.setAttribute("aria-label", `Project: ${p.title}`);

  // Top row
  const cardTop = document.createElement("div");
  cardTop.className = "card-top";

  const titleEl = document.createElement("h2");
  titleEl.className = "card-title";
  titleEl.textContent = p.title;

  const badges = document.createElement("div");
  badges.className = "card-badges";
  badges.appendChild(statusBadge(p.status));
  badges.appendChild(priorityBadge(p.priority));

  cardTop.appendChild(titleEl);
  cardTop.appendChild(badges);

  // Description
  const desc = document.createElement("p");
  desc.className = "card-description";
  desc.textContent = p.description || "No description provided.";

  // Progress bar
  const progressWrap = document.createElement("div");
  progressWrap.className = "progress-bar-wrap";
  const progressFill = document.createElement("div");
  progressFill.className = "progress-bar-fill";
  progressFill.style.width = `${pct}%`;
  progressWrap.appendChild(progressFill);

  // Footer
  const footer = document.createElement("div");
  footer.className = "card-footer";

  const deadlineEl = document.createElement("span");
  deadlineEl.className = `card-deadline${overdue ? " card-deadline--overdue" : ""}`;
  if (p.deadline) {
    deadlineEl.textContent = `${overdue ? "⚠ " : ""}${formatDate(p.deadline)}`;
  } else {
    deadlineEl.textContent = "No deadline";
  }

  const progressLabel = document.createElement("span");
  progressLabel.className = "card-progress";
  progressLabel.textContent = totalTasks > 0
    ? `${doneTasks}/${totalTasks} tasks`
    : "No tasks";

  footer.appendChild(deadlineEl);
  footer.appendChild(progressLabel);

  card.appendChild(cardTop);
  card.appendChild(desc);
  card.appendChild(progressWrap);
  card.appendChild(footer);

  // Click / keyboard to open detail
  card.addEventListener("click", () => openDetailModal(p.id));
  card.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      openDetailModal(p.id);
    }
  });

  return card;
}

// ─── Detail Modal ─────────────────────────────────────────────────────────────

async function openDetailModal(projectId) {
  state.currentProjectId = projectId;
  const modal = dom.modalDetail();
  modal.hidden = false;
  document.body.style.overflow = "hidden";

  // Show loading
  dom.detailLoading().hidden = false;
  dom.detailContent().hidden = true;
  dom.detailError().hidden   = true;
  hideError(dom.detailFormError());
  hideError(dom.taskError());

  try {
    const project = await apiFetch(`/api/projects/${projectId}`);
    populateDetailForm(project);
    renderTaskList(project.tasks || []);

    dom.detailLoading().hidden = true;
    dom.detailContent().hidden = false;
  } catch (err) {
    dom.detailLoading().hidden = true;
    dom.detailErrorMsg().textContent = `Failed to load project: ${err.message}`;
    dom.detailError().hidden = false;
  }
}

function closeDetailModal() {
  dom.modalDetail().hidden = true;
  document.body.style.overflow = "";
  state.currentProjectId = null;
}

function populateDetailForm(project) {
  dom.detailProjectId().value    = project.id;
  dom.detailTitleInput().value   = project.title;
  dom.detailDescription().value  = project.description || "";
  dom.detailStatus().value       = project.status;
  dom.detailPriority().value     = project.priority;
  dom.detailDeadline().value     = project.deadline || "";
  hideError(dom.detailTitleError());
  hideError(dom.detailFormError());
}

// ─── Edit Project ─────────────────────────────────────────────────────────────

async function saveProject(e) {
  e.preventDefault();

  const id = dom.detailProjectId().value;
  const title = dom.detailTitleInput().value.trim();

  if (!title) {
    showError(dom.detailTitleError(), "Title is required.");
    dom.detailTitleInput().focus();
    return;
  }
  hideError(dom.detailTitleError());

  const deadline = dom.detailDeadline().value || null;

  const body = {
    title,
    description: dom.detailDescription().value.trim() || null,
    status:      dom.detailStatus().value,
    priority:    dom.detailPriority().value,
    deadline,
  };

  setButtonLoading(dom.btnSaveProject(), true);
  hideError(dom.detailFormError());

  try {
    await apiFetch(`/api/projects/${id}`, {
      method: "PUT",
      body: JSON.stringify(body),
    });
    showToast("Project saved successfully.", "success");
    closeDetailModal();
    await Promise.all([loadProjects(), loadStats()]);
  } catch (err) {
    showError(dom.detailFormError(), `Failed to save: ${err.message}`);
  } finally {
    setButtonLoading(dom.btnSaveProject(), false);
  }
}

// ─── Delete Project ───────────────────────────────────────────────────────────

function openConfirmDelete() {
  dom.modalConfirmDelete().hidden = false;
}

function closeConfirmDelete() {
  dom.modalConfirmDelete().hidden = true;
}

async function confirmDeleteProject() {
  const id = state.currentProjectId;
  if (!id) return;

  setButtonLoading(dom.btnConfirmDelete(), true);

  try {
    await apiFetch(`/api/projects/${id}`, { method: "DELETE" });
    showToast("Project deleted.", "success");
    closeConfirmDelete();
    closeDetailModal();
    await Promise.all([loadProjects(), loadStats()]);
  } catch (err) {
    showToast(`Delete failed: ${err.message}`, "error");
    setButtonLoading(dom.btnConfirmDelete(), false);
  }
}

// ─── Add Project ──────────────────────────────────────────────────────────────

function openAddModal() {
  dom.formAdd().reset();
  hideError(dom.addTitleError());
  hideError(dom.addFormError());
  dom.modalAdd().hidden = false;
  document.body.style.overflow = "hidden";
  dom.addTitle().focus();
}

function closeAddModal() {
  dom.modalAdd().hidden = true;
  document.body.style.overflow = "";
}

async function submitAddProject(e) {
  e.preventDefault();

  const title = dom.addTitle().value.trim();
  if (!title) {
    showError(dom.addTitleError(), "Title is required.");
    dom.addTitle().focus();
    return;
  }
  hideError(dom.addTitleError());

  const deadline = dom.addDeadline().value || null;

  const body = {
    title,
    description: dom.addDescription().value.trim() || null,
    priority:    dom.addPriority().value,
    deadline,
    status:      "active",
  };

  setButtonLoading(dom.btnSubmitAdd(), true);
  hideError(dom.addFormError());

  try {
    await apiFetch("/api/projects", {
      method: "POST",
      body: JSON.stringify(body),
    });
    showToast("Project created!", "success");
    closeAddModal();
    await Promise.all([loadProjects(), loadStats()]);
  } catch (err) {
    showError(dom.addFormError(), `Failed to create project: ${err.message}`);
  } finally {
    setButtonLoading(dom.btnSubmitAdd(), false);
  }
}

// ─── Tasks ────────────────────────────────────────────────────────────────────

function renderTaskList(tasks) {
  const list = dom.taskList();
  list.innerHTML = "";

  if (tasks.length === 0) {
    dom.taskListEmpty().hidden = false;
  } else {
    dom.taskListEmpty().hidden = true;
    for (const task of tasks) {
      list.appendChild(buildTaskItem(task));
    }
  }
}

function buildTaskItem(task) {
  const li = document.createElement("li");
  li.className = "task-item";
  li.dataset.taskId = task.id;

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.className = "task-checkbox";
  checkbox.checked = task.is_done;
  checkbox.setAttribute("aria-label", `Toggle: ${task.title}`);
  checkbox.addEventListener("change", () => handleToggleTask(task.id, li, checkbox));

  const titleSpan = document.createElement("span");
  titleSpan.className = `task-title${task.is_done ? " task-title--done" : ""}`;
  titleSpan.textContent = task.title;

  const deleteBtn = document.createElement("button");
  deleteBtn.className = "task-delete-btn";
  deleteBtn.setAttribute("aria-label", `Delete task: ${task.title}`);
  deleteBtn.textContent = "✕";
  deleteBtn.addEventListener("click", () => handleDeleteTask(task.id, li));

  li.appendChild(checkbox);
  li.appendChild(titleSpan);
  li.appendChild(deleteBtn);

  return li;
}

async function handleToggleTask(taskId, liEl, checkbox) {
  // Optimistic UI update
  const titleSpan = liEl.querySelector(".task-title");
  const wasDone = !checkbox.checked; // before optimistic flip, checked is already toggled by browser
  titleSpan.classList.toggle("task-title--done", checkbox.checked);

  try {
    await apiFetch(`/api/tasks/${taskId}/toggle`, { method: "PATCH" });
    // Update cards in background (task count)
    loadProjects();
  } catch (err) {
    // Revert optimistic update
    checkbox.checked = wasDone;
    titleSpan.classList.toggle("task-title--done", wasDone);
    showToast(`Failed to update task: ${err.message}`, "error");
  }
}

async function handleDeleteTask(taskId, liEl) {
  liEl.style.opacity = "0.4";
  liEl.style.pointerEvents = "none";

  try {
    await apiFetch(`/api/tasks/${taskId}`, { method: "DELETE" });
    liEl.remove();
    const list = dom.taskList();
    if (list.children.length === 0) {
      dom.taskListEmpty().hidden = false;
    }
    loadProjects(); // refresh card progress
  } catch (err) {
    liEl.style.opacity = "";
    liEl.style.pointerEvents = "";
    showToast(`Failed to delete task: ${err.message}`, "error");
  }
}

async function handleAddTask(e) {
  e.preventDefault();
  const input = dom.newTaskInput();
  const title = input.value.trim();
  if (!title) return;

  const projectId = state.currentProjectId;
  if (!projectId) return;

  dom.btnAddTask().disabled = true;
  hideError(dom.taskError());

  try {
    const task = await apiFetch(`/api/projects/${projectId}/tasks`, {
      method: "POST",
      body: JSON.stringify({ title }),
    });
    input.value = "";
    dom.taskListEmpty().hidden = true;
    const list = dom.taskList();
    list.appendChild(buildTaskItem(task));
    loadProjects(); // refresh card progress
  } catch (err) {
    showError(dom.taskError(), `Failed to add task: ${err.message}`);
  } finally {
    dom.btnAddTask().disabled = false;
    input.focus();
  }
}

// ─── Filters ──────────────────────────────────────────────────────────────────

function applyFilters() {
  state.filterStatus   = dom.filterStatus().value;
  state.filterPriority = dom.filterPriority().value;
  loadProjects();
}

function clearFilters() {
  dom.filterStatus().value   = "";
  dom.filterPriority().value = "";
  state.filterStatus   = "";
  state.filterPriority = "";
  loadProjects();
}

// ─── UI Utilities ─────────────────────────────────────────────────────────────

function showError(el, message) {
  el.textContent = message;
  el.hidden = false;
}

function hideError(el) {
  el.hidden = true;
  el.textContent = "";
}

function setButtonLoading(btn, loading) {
  const textEl   = btn.querySelector(".btn-text");
  const spinnerEl = btn.querySelector(".btn-spinner");
  btn.disabled = loading;
  if (textEl)    textEl.style.opacity = loading ? "0" : "1";
  if (spinnerEl) spinnerEl.hidden = !loading;
}

// ─── Modal Overlay Click to Close ────────────────────────────────────────────

function handleOverlayClick(e) {
  if (e.target === dom.modalAdd()) closeAddModal();
  if (e.target === dom.modalDetail()) closeDetailModal();
  if (e.target === dom.modalConfirmDelete()) closeConfirmDelete();
}

// ─── Keyboard Escape ──────────────────────────────────────────────────────────

document.addEventListener("keydown", (e) => {
  if (e.key !== "Escape") return;
  if (!dom.modalConfirmDelete().hidden) { closeConfirmDelete(); return; }
  if (!dom.modalAdd().hidden)    { closeAddModal();    return; }
  if (!dom.modalDetail().hidden) { closeDetailModal(); return; }
});

// ─── Event Wiring ─────────────────────────────────────────────────────────────

function wireEvents() {
  // Add project
  dom.btnAddProject().addEventListener("click", openAddModal);
  dom.btnCloseAddModal().addEventListener("click", closeAddModal);
  dom.btnCancelAdd().addEventListener("click", closeAddModal);
  dom.formAdd().addEventListener("submit", submitAddProject);

  // Detail modal
  dom.btnCloseDetail().addEventListener("click", closeDetailModal);
  dom.btnCancelDetail().addEventListener("click", closeDetailModal);
  dom.formEdit().addEventListener("submit", saveProject);
  dom.btnDeleteProject().addEventListener("click", openConfirmDelete);

  // Tasks
  dom.formAddTask().addEventListener("submit", handleAddTask);

  // Confirm delete
  dom.btnCancelDelete().addEventListener("click", closeConfirmDelete);
  dom.btnConfirmDelete().addEventListener("click", confirmDeleteProject);

  // Filters
  dom.filterStatus().addEventListener("change", applyFilters);
  dom.filterPriority().addEventListener("change", applyFilters);
  dom.btnClearFilters().addEventListener("click", clearFilters);

  // Retry
  dom.btnRetry().addEventListener("click", loadProjects);

  // Modal overlay backdrop click
  dom.modalAdd().addEventListener("click", handleOverlayClick);
  dom.modalDetail().addEventListener("click", handleOverlayClick);
  dom.modalConfirmDelete().addEventListener("click", handleOverlayClick);
}

// ─── Boot ─────────────────────────────────────────────────────────────────────

async function init() {
  wireEvents();
  await Promise.all([loadStats(), loadProjects()]);
}

document.addEventListener("DOMContentLoaded", init);
