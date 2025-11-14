// tabela_ajustada_tooltip.js — versão: tooltip em todas as células
document.addEventListener("DOMContentLoaded", function () {
console.debug("[TOOLTIP] DOMContentLoaded disparado.");

const tabela = document.querySelector("#tabela-clientes");
if (!tabela) {
    console.warn("[TOOLTIP] Tabela #tabela-clientes não encontrada.");
    return;
}

// Cria o elemento tooltip
const tooltip = document.createElement("div");
tooltip.id = "custom-dt-tooltip";
document.body.appendChild(tooltip);
console.debug("[TOOLTIP] Tooltip container criado.");

// Função: definir tooltip para TODAS as células
function prepararTooltips() {
    console.debug("[TOOLTIP] Preparando tooltips em todas as células...");
    let contador = 0;
    tabela.querySelectorAll("tbody td").forEach(td => {
        const texto = td.textContent.trim();
        if (texto) {
            td.dataset.tooltip = texto;
            contador++;
        } else {
            delete td.dataset.tooltip;
        }
    });
    console.debug(`[TOOLTIP] ${contador} células com tooltip configurado.`);
}

function mostrarTooltip(e) {
    const texto = e.currentTarget.dataset.tooltip;
    if (!texto) return;
    tooltip.textContent = texto;
    tooltip.style.display = "block";
    posicionarTooltip(e);
}

function moverTooltip(e) {
    if (tooltip.style.display === "none") return;
    posicionarTooltip(e);
}

function esconderTooltip() {
    tooltip.style.display = "none";
}

function posicionarTooltip(e) {
    const offset = 16;
    const maxWidth = 500;
    tooltip.style.maxWidth = `${maxWidth}px`;

    let x = e.clientX + offset;
    let y = e.clientY + offset;

    const rect = tooltip.getBoundingClientRect();
    const vw = window.innerWidth;
    const vh = window.innerHeight;

    if (x + rect.width > vw - 10) x = e.clientX - rect.width - offset;
    if (y + rect.height > vh - 10) y = e.clientY - rect.height - offset;

    tooltip.style.left = `${x}px`;
    tooltip.style.top = `${y}px`;
}

function aplicarEventos() {
    const cels = tabela.querySelectorAll("tbody td[data-tooltip]");
    console.debug(`[TOOLTIP] Aplicando eventos em ${cels.length} células.`);
    cels.forEach(td => {
        td.removeEventListener("mouseenter", mostrarTooltip);
        td.removeEventListener("mousemove", moverTooltip);
        td.removeEventListener("mouseleave", esconderTooltip);
        td.addEventListener("mouseenter", mostrarTooltip);
        td.addEventListener("mousemove", moverTooltip);
        td.addEventListener("mouseleave", esconderTooltip);
        // Acessibilidade via teclado
        td.addEventListener("focus", mostrarTooltip);
        td.addEventListener("blur", esconderTooltip);
        td.tabIndex = 0;
        
    });
}

prepararTooltips();
aplicarEventos();

if (window.jQuery && jQuery.fn.dataTable) {
    console.debug("[TOOLTIP] Detectado DataTables, ouvindo evento draw.dt...");
    jQuery("#tabela-clientes").on("draw.dt", function () {
        console.debug("[TOOLTIP] draw.dt — reaplicando tooltips.");
        prepararTooltips();
        aplicarEventos();
    });
} else {
    console.warn("[TOOLTIP] DataTables não detectado. Tooltips estáticos apenas.");
}

});