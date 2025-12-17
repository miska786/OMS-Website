const services = [
    "Import",
    "Export",
    "Container-Inspection",
    "Allied-Service"
];

let index = 0;

function rotateService() {
    const el = document.getElementById("serviceText");
    if (!el) return; // do nothing if rotator is not on this page
    el.textContent = services[index];
    index = (index + 1) % services.length;
}

document.addEventListener("DOMContentLoaded", () => {
    rotateService();
    setInterval(rotateService, 3000);
});
