/**
 * AI Coding Tutor for C Programming - Global JS Utilities
 */

document.addEventListener("DOMContentLoaded", () => {
    // Mobile sidebar toggle
    const mobileToggle = document.getElementById("mobileToggle");
    const appSidebar = document.getElementById("appSidebar");
    if (mobileToggle && appSidebar) {
        mobileToggle.addEventListener("click", () => {
            appSidebar.classList.toggle("open");
        });
    }

    // Close sidebar on outer click on mobile
    document.addEventListener("click", (e) => {
        if (window.innerWidth <= 992 && appSidebar && appSidebar.classList.contains("open")) {
            if (!appSidebar.contains(e.target) && !mobileToggle.contains(e.target)) {
                appSidebar.classList.remove("open");
            }
        }
    });

    // Check host compiler status on load
    fetchCompilerStatus();
});

function showToast(message, type = "info") {
    let container = document.getElementById("toast-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    let icon = "fa-info-circle";
    if (type === "success") icon = "fa-check-circle";
    if (type === "error") icon = "fa-exclamation-circle";

    toast.innerHTML = `<i class="fas ${icon}"></i> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = "0";
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

function fetchCompilerStatus() {
    fetch("/api/compiler/status")
        .then(res => res.json())
        .then(data => {
            const statusDot = document.getElementById("compilerStatusDot");
            const statusText = document.getElementById("compilerStatusText");
            if (statusDot && statusText) {
                if (data.available) {
                    statusDot.className = "status-dot active";
                    statusText.textContent = `${data.name.toUpperCase()} (Active)`;
                } else {
                    statusDot.className = "status-dot inactive";
                    statusText.textContent = "GCC Not in PATH";
                }
            }
        })
        .catch(() => {});
}
