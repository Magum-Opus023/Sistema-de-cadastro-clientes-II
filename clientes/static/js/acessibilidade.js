document.addEventListener("DOMContentLoaded", function () {
  const html = document.documentElement;
  const body = document.body;
  const toggleContrastBtn = document.getElementById("toggle-contrast");
  const increaseFontBtn = document.getElementById("increase-font");
  const decreaseFontBtn = document.getElementById("decrease-font");
  const resetBtn = document.getElementById("reset-accessibility");

  // === Recuperar preferências ===
  const savedContrast = localStorage.getItem("altoContraste");
  const savedFontSize = localStorage.getItem("fontSize");

  // ✅ Aplica o contraste salvo
  if (savedContrast === "true") {
    body.classList.add("alto-contraste");
    html.setAttribute("data-bs-theme", "dark");
  }

  // ✅ Aplica o tamanho de fonte salvo
  if (savedFontSize) {
    document.documentElement.style.fontSize = savedFontSize;
  }

  updateContrastButton(savedContrast === "true");

  // === Alternar alto contraste ===
  toggleContrastBtn?.addEventListener("click", function () {
    const active = body.classList.toggle("alto-contraste");
    html.setAttribute("data-bs-theme", active ? "dark" : "light");
    localStorage.setItem("altoContraste", active ? "true" : "false");
    updateContrastButton(active);
  });

  // === Aumentar fonte ===
  increaseFontBtn?.addEventListener("click", function () {
    const currentSize = parseFloat(
      window.getComputedStyle(document.documentElement).fontSize
    );
    const newSize = Math.min(currentSize + 1, 24);
    document.documentElement.style.fontSize = newSize + "px";
    localStorage.setItem("fontSize", newSize + "px");
  });

  // === Diminuir fonte ===
  decreaseFontBtn?.addEventListener("click", function () {
    const currentSize = parseFloat(
      window.getComputedStyle(document.documentElement).fontSize
    );
    const newSize = Math.max(currentSize - 1, 10);
    document.documentElement.style.fontSize = newSize + "px";
    localStorage.setItem("fontSize", newSize + "px");
  });

  // === Resetar ===
  resetBtn?.addEventListener("click", function () {
    body.classList.remove("alto-contraste");
    html.setAttribute("data-bs-theme", "light");
    document.documentElement.style.fontSize = "";
    localStorage.removeItem("altoContraste");
    localStorage.removeItem("fontSize");
    updateContrastButton(false);
  });

  // === Atualiza o botão dinamicamente ===
  function updateContrastButton(active) {
    if (!toggleContrastBtn) return;
    toggleContrastBtn.textContent = active ? "Modo normal" : "Alto contraste";
    toggleContrastBtn.classList.toggle("btn-warning", active);
    toggleContrastBtn.classList.toggle("btn-dark", !active);
  }
});

