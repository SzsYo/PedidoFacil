/*
 * Validaciones del lado del cliente para los formularios de productos y pedidos.
 * Se activan con el atributo data-validar="producto" | "pedido" en el <form>.
 * Estas validaciones mejoran la experiencia, pero NO sustituyen a las de Django.
 */
(function () {
  "use strict";

  const esNumero = (v) => v !== "" && Number.isFinite(Number(v));

  const reglas = {
    producto: {
      nombre(v) {
        v = v.trim();
        if (!v) return "El nombre es obligatorio.";
        if (v.length < 3) return "El nombre debe tener al menos 3 caracteres.";
        return "";
      },
      precio(v) {
        v = v.trim();
        if (!v) return "El precio es obligatorio.";
        if (!esNumero(v)) return "El precio debe ser un número.";
        if (Number(v) <= 0) return "El precio debe ser mayor que cero.";
        return "";
      },
      cantidad_disponible(v) {
        v = v.trim();
        if (!v) return "La cantidad disponible es obligatoria.";
        if (!esNumero(v)) return "La cantidad debe ser un número.";
        if (Number(v) < 0) return "La cantidad no puede ser negativa.";
        if (!Number.isInteger(Number(v))) return "La cantidad debe ser un número entero.";
        return "";
      },
      descripcion(v, campo) {
        const max = Number(campo.dataset.max) || 500;
        if (v.length > max) return `La descripción no puede superar los ${max} caracteres (tiene ${v.length}).`;
        return "";
      },
    },
    pedido: {
      numero_pedido(v) {
        if (!v.trim()) return "El número de pedido es obligatorio.";
        return "";
      },
      cliente(v) {
        if (!v.trim()) return "El nombre del cliente es obligatorio.";
        return "";
      },
      descripcion(v, campo) {
        const max = Number(campo.dataset.max) || 500;
        if (!v.trim()) return "La descripción del pedido es obligatoria.";
        if (v.length > max) return `La descripción no puede superar los ${max} caracteres (tiene ${v.length}).`;
        return "";
      },
      valor_total(v) {
        v = v.trim();
        if (!v) return "El valor total es obligatorio.";
        if (!esNumero(v)) return "El valor total debe ser un número.";
        if (Number(v) <= 0) return "El valor total debe ser mayor que cero.";
        return "";
      },
      estado(v, campo) {
        const permitidos = Array.from(campo.options || []).map((o) => o.value);
        if (!permitidos.includes(v)) return "Selecciona un estado válido: pendiente, confirmado o cancelado.";
        return "";
      },
    },
  };

  function mostrar(campo, mensaje) {
    const aviso = campo.parentElement.querySelector(".invalid-feedback");
    if (mensaje) {
      campo.classList.add("is-invalid");
      campo.classList.remove("is-valid");
      if (aviso) aviso.textContent = mensaje;
    } else {
      campo.classList.remove("is-invalid");
      campo.classList.add("is-valid");
      if (aviso) aviso.textContent = "";
    }
  }

  function validarCampo(form, tipo, nombre) {
    const campo = form.elements[nombre];
    if (!campo) return "";
    const mensaje = reglas[tipo][nombre](campo.value, campo);
    mostrar(campo, mensaje);
    return mensaje;
  }

  document.querySelectorAll("form[data-validar]").forEach((form) => {
    const tipo = form.dataset.validar;
    const nombres = Object.keys(reglas[tipo] || {});
    const resumen = form.querySelector("#resumen-errores");

    nombres.forEach((nombre) => {
      const campo = form.elements[nombre];
      if (!campo) return;
      // Revalida mientras el usuario corrige, y al salir del campo
      ["input", "change", "blur"].forEach((evento) =>
        campo.addEventListener(evento, () => validarCampo(form, tipo, nombre))
      );
    });

    form.addEventListener("submit", (e) => {
      const errores = [];
      let primero = null;
      nombres.forEach((nombre) => {
        const mensaje = validarCampo(form, tipo, nombre);
        if (mensaje) {
          errores.push(mensaje);
          if (!primero) primero = form.elements[nombre];
        }
      });
      if (errores.length) {
        e.preventDefault();
        if (resumen) {
          resumen.classList.remove("d-none");
          resumen.textContent = `Corrige ${errores.length} campo(s) antes de guardar.`;
        }
        primero.focus();
      }
    });
  });
})();
