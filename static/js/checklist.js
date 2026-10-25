/**
 * Debugging Checklist Client Controller
 * Manages interactive checklist toggling, progress tracking, and filtering.
 */

document.addEventListener("DOMContentLoaded", () => {
    const checkboxes = document.querySelectorAll(".checklist-checkbox");
    checkboxes.forEach(cb => {
        cb.addEventListener("change", (e) => {
            const itemId = e.target.dataset.itemId;
            const isCompleted = e.target.checked;
            toggleChecklistItem(itemId, isCompleted);
        });
    });

    // Filter buttons
    const filterBtns = document.querySelectorAll(".checklist-filter-btn");
    filterBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            filterBtns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            const filter = btn.dataset.filter;
            const items = document.querySelectorAll(".checklist-item");

            items.forEach(item => {
                const isChecked = item.querySelector(".checklist-checkbox").checked;
                if (filter === "all") {
                    item.style.display = "flex";
                } else if (filter === "completed") {
                    item.style.display = isChecked ? "flex" : "none";
                } else if (filter === "pending") {
                    item.style.display = !isChecked ? "flex" : "none";
                }
            });
        });
    });
});

function toggleChecklistItem(itemId, completed) {
    fetch("/api/checklist/toggle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            item_id: itemId,
            completed: completed
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            // Update UI Counters
            const completedCountEl = document.getElementById("checklistCompletedCount");
            const percentageEl = document.getElementById("checklistPercentageText");
            const progressBar = document.getElementById("checklistProgressBar");

            if (completedCountEl) completedCountEl.textContent = `${data.completed} of ${data.total}`;
            if (percentageEl) percentageEl.textContent = `${data.percentage}%`;
            if (progressBar) progressBar.style.width = `${data.percentage}%`;

            if (completed) {
                showToast("Checklist item marked complete!", "success");
            }
        }
    })
    .catch(() => showToast("Failed to update checklist item", "error"));
}
