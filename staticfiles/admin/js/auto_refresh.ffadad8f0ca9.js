// Auto refresh Django admin changelist every 30s
(function() {
    document.addEventListener("DOMContentLoaded", function() {
        if (document.body.classList.contains("change-list")) {
            setTimeout(function() {
                window.location.reload();
            }, 30000); // 30 seconds
        }
    });
})();
