document.addEventListener("DOMContentLoaded", function () {
  const regionSelect = document.getElementById("region");
  const comunaSelect = document.getElementById("comuna");
  const contactarPor = document.getElementById("contactar_por");
  const otroContactoContainer = document.getElementById("otro_contacto_container");
  const otroContactoInput = document.getElementById("otro_contacto");
  const temaSelect = document.getElementById("tema");
  const otroTemaContainer = document.getElementById("otro_tema_container");
  const otroTemaInput = document.getElementById("otro_tema");
  const agregarFotoBtn = document.getElementById("agregar_foto");
  const fotosContainer = document.getElementById("fotos_container");
  const form = document.getElementById("activity-form");
  const confirmation = document.getElementById("confirmation");

  // --- Cargar regiones ---
  fetch("/api/regiones")
    .then(res => res.json())
    .then(regiones => {
      regiones.forEach(region => {
        const option = document.createElement("option");
        option.value = region.id;
        option.textContent = region.nombre;
        regionSelect.appendChild(option);
      });
    });

  // --- Cargar comunas al cambiar región ---
  regionSelect.addEventListener("change", function () {
    comunaSelect.innerHTML = '<option value="">Seleccione una comuna</option>';
    if (!this.value) return;

    fetch(`/api/comunas/${this.value}`)
      .then(res => res.json())
      .then(comunas => {
        comunas.forEach(comuna => {
          const option = document.createElement("option");
          option.value = comuna.id;
          option.textContent = comuna.nombre;
          comunaSelect.appendChild(option);
        });
      });
  });

  // --- Mostrar input si red social es "otra" ---
  contactarPor.addEventListener("change", function () {
    if (this.value === "otra") {
      otroContactoContainer.style.display = "block";
    } else {
      otroContactoContainer.style.display = "none";
      otroContactoInput.value = "";
    }
  });

  // --- Mostrar input si tema es "otro" ---
  temaSelect.addEventListener("change", function () {
    if (this.value === "otro") {
      otroTemaContainer.style.display = "block";
    } else {
      otroTemaContainer.style.display = "none";
      otroTemaInput.value = "";
    }
  });

  // --- Agregar campos de archivo (hasta 5) ---
  agregarFotoBtn.addEventListener("click", function () {
    const inputs = fotosContainer.querySelectorAll("input[type='file']");
    if (inputs.length >= 5) return;
    const newInput = document.createElement("input");
    newInput.type = "file";
    newInput.name = "fotos[]";
    newInput.accept = "image/*";
    fotosContainer.appendChild(newInput);
  });

  // --- Confirmar antes de enviar ---
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    confirmation.style.display = "block";
    form.style.display = "none";
  });

  document.getElementById("confirm_yes").addEventListener("click", function () {
    
    form.submit();
  });

  document.getElementById("confirm_no").addEventListener("click", function () {
    confirmation.style.display = "none";
    form.style.display = "block";
  });
  
});
