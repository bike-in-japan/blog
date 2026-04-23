(function () {
    const els = document.querySelectorAll('[data-obf-email]');
    els.forEach(el => {
        const u = el.dataset.u;
        const d = el.dataset.d;
        el.href = "mailto:" + u + "@" + d;
    });
})();