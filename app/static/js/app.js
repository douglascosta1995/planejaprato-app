window.showToast = function(message, type = "info", duration = 3000) {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const toast = document.createElement("div");
    toast.classList.add("toast", type);
    toast.textContent = message;

    container.appendChild(toast);

    requestAnimationFrame(() => {
        toast.classList.add("show");
    });

    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 300);
    }, duration);
};


window.setButtonLoading = function(button, text = "Carregando...") {
    if (!button) return;

    button.disabled = true;
    button.dataset.originalText = button.innerHTML;
    button.innerHTML = text;
};

document.getElementById("meal-plan-form")?.addEventListener("submit", function () {

    const button = document.getElementById("meal-plan-submit");

    setButtonLoading(button, "Criando...");
});

window.setLinkLoading = function(link, text = "Carregando...") {
    if (!link) return;

    link.dataset.originalText = link.innerHTML;
    link.innerHTML = text;
    link.style.pointerEvents = "none";
};

document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".loading-link").forEach(function (link) {

        link.addEventListener("click", function () {
            setLinkLoading(this, "Carregando...");
        });

    });

});

document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".loading-form").forEach(function (form) {

    form.addEventListener("submit", function () {

        const button = this.querySelector('button[type="submit"]');

        setButtonLoading(button, "Excluindo...");

    });

});

});
