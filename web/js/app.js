// Frontend de EcoRutas: se comunica con la API Flask (/api/...)

// Atajo para buscar un elemento por su id.
const $ = (id) => document.getElementById(id);

// Escapa HTML para que un texto escrito por el usuario no se ejecute como código (evita XSS).
function esc(texto) {
  const d = document.createElement("div");
  d.textContent = texto == null ? "" : texto;
  return d.innerHTML;
}

// Llama a la API y devuelve el JSON; si el servidor responde con error, lanza una excepción con su mensaje.
async function api(url, opciones) {
  const r = await fetch(url, opciones);
  const datos = await r.json();
  if (!r.ok) throw new Error(datos.error || "Error en el servidor");
  return datos;
}

// Envía datos como formulario (application/x-www-form-urlencoded), el formato que lee Flask en request.form.
function enviarFormulario(url, metodo, campos) {
  return api(url, {
    method: metodo,
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams(campos).toString()
  });
}

// Muestra un mensaje de éxito (verde) o de error (rojo) debajo de un formulario.
function mostrarMensaje(id, texto, esError) {
  const el = $(id);
  el.textContent = texto;
  el.className = "mensaje" + (esError ? " error" : "");
}

// ---------- Pestañas ----------
document.querySelectorAll(".tab").forEach((boton) => {
  boton.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((b) => b.classList.remove("activo"));
    document.querySelectorAll(".vista").forEach((v) => v.classList.remove("visible"));
    boton.classList.add("activo");
    $("vista-" + boton.dataset.vista).classList.add("visible");
    if (boton.dataset.vista === "admin") cargarAdmin();
  });
});

// ---------- Barrios ----------
// Llena los tres <select> de barrios (filtro, reporte y nueva ruta) con los datos de la API.
async function cargarBarrios() {
  const barrios = await api("/api/barrios");
  const opciones = barrios.map((b) => `<option value="${b.id}">${esc(b.nombre)} (${esc(b.sector)})</option>`).join("");
  $("filtroBarrio").innerHTML = `<option value="">Todos los barrios</option>` + opciones;
  $("repBarrio").innerHTML = opciones;
  $("rutBarrio").innerHTML = opciones;
}

// ---------- Rutas ----------
// Pinta las tarjetas de rutas, filtradas por el barrio elegido.
async function cargarRutas() {
  const barrio = $("filtroBarrio").value;
  const rutas = await api("/api/rutas" + (barrio ? "?barrio=" + barrio : ""));
  const cont = $("listaRutas");
  if (rutas.length === 0) {
    cont.innerHTML = `<p class="vacio">No hay rutas registradas para este barrio.</p>`;
    return;
  }
  cont.innerHTML = rutas.map((r) => `
    <article class="tarjeta">
      <h3>${esc(r.nombre)}</h3>
      <span class="etiqueta">📍 ${esc(r.barrio)}</span>
      <span class="etiqueta">📅 ${esc(r.dia)}</span>
      <span class="etiqueta">🕒 ${esc(r.hora)}</span>
      <div><small>🚛 ${esc(r.vehiculo)}</small></div>
      <ol>${r.paradas.map((p) => `<li>${esc(p.direccion)}${p.referencia ? ` <small>· ${esc(p.referencia)}</small>` : ""}</li>`).join("")}</ol>
    </article>`).join("");
}
$("filtroBarrio").addEventListener("change", cargarRutas);

// ---------- Reportes ----------
$("formReporte").addEventListener("submit", async (e) => {
  e.preventDefault();
  try {
    await enviarFormulario("/api/reportes", "POST", {
      barrio: $("repBarrio").value,
      direccion: $("repDireccion").value,
      tipo: $("repTipo").value,
      descripcion: $("repDescripcion").value
    });
    $("formReporte").reset();
    mostrarMensaje("msgReporte", "¡Reporte enviado! Gracias por avisar.", false);
  } catch (err) {
    mostrarMensaje("msgReporte", err.message, true);
  }
});

// ---------- Administración ----------
$("formRuta").addEventListener("submit", async (e) => {
  e.preventDefault();
  try {
    await enviarFormulario("/api/rutas", "POST", {
      nombre: $("rutNombre").value,
      barrio: $("rutBarrio").value,
      dia: $("rutDia").value,
      hora: $("rutHora").value,
      vehiculo: $("rutVehiculo").value,
      paradas: $("rutParadas").value
    });
    $("formRuta").reset();
    mostrarMensaje("msgRuta", "Ruta guardada.", false);
    cargarAdmin();
    cargarRutas();
  } catch (err) {
    mostrarMensaje("msgRuta", err.message, true);
  }
});

async function eliminarRuta(id) {
  if (!confirm("¿Eliminar esta ruta y sus paradas?")) return;
  await api("/api/rutas/" + id, { method: "DELETE" });
  cargarAdmin();
  cargarRutas();
}

async function cambiarEstado(id, estado) {
  await enviarFormulario("/api/reportes/" + id, "PUT", { estado });
}

// Carga el panel de administración: lista de rutas y tabla de reportes.
async function cargarAdmin() {
  const [rutas, reportes] = await Promise.all([api("/api/rutas"), api("/api/reportes")]);
  $("adminRutas").innerHTML = rutas.map((r) => `
    <div class="fila-ruta">
      <span><b>${esc(r.nombre)}</b><br><small>${esc(r.dia)} · ${esc(r.hora)} · ${r.paradas.length} paradas</small></span>
      <button class="boton peligro" onclick="eliminarRuta(${r.id})">Eliminar</button>
    </div>`).join("") || `<p class="vacio">Aún no hay rutas.</p>`;

  const estados = ["Pendiente", "En atención", "Resuelto"];
  $("tablaReportes").innerHTML = reportes.map((p) => `
    <tr>
      <td>${esc(p.fecha)}</td><td>${esc(p.barrio)}</td><td>${esc(p.direccion)}</td>
      <td>${esc(p.tipo)}</td><td>${esc(p.descripcion)}</td>
      <td><select onchange="cambiarEstado(${p.id}, this.value)">
        ${estados.map((s) => `<option ${s === p.estado ? "selected" : ""}>${s}</option>`).join("")}
      </select></td>
    </tr>`).join("") || `<tr><td colspan="6" class="vacio">Sin reportes.</td></tr>`;
}

// ---------- Inicio ----------
cargarBarrios().then(cargarRutas).catch((err) => {
  $("listaRutas").innerHTML = `<p class="vacio">No se pudo cargar la información: ${esc(err.message)}</p>`;
});
