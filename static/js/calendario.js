// --- Selección de Elementos del DOM ---
const mesAnioH2 = document.getElementById('mes-anio');
const gridDiasDiv = document.getElementById('grid-dias');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const modal = document.getElementById('modal-form');
const closeBtn = document.querySelector('.close-btn');
const diaSeleccionadoSpan = document.getElementById('dia-seleccionado');
const formRecordatorio = document.getElementById('recordatorio-form');
const recordatoriosListaDiv = document.getElementById('recordatorios-existentes');

let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();
let recordatorios = [];

// --- API Flask ---
async function cargarRecordatoriosMes(year, month) {
    recordatorios = [];
    const diasEnElMes = new Date(year, month + 1, 0).getDate();
    for (let i = 1; i <= diasEnElMes; i++) {
        const fechaStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
        try {
            const res = await fetch(`/api/recordatorios/${fechaStr}`);
            if (res.ok) {
                const data = await res.json();
                recordatorios = recordatorios.concat(data);
            }
        } catch (e) {}
    }
}

async function guardarRecordatorioAPI(fecha, titulo, descripcion, importancia) {
    const res = await fetch('/api/recordatorios', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fecha, titulo, descripcion, importancia })
    });
    return res.ok;
}

async function eliminarRecordatorioAPI(id) {
    const res = await fetch(`/api/recordatorios/${id}`, { method: 'DELETE' });
    return res.ok;
}

// --- Calendario ---
async function generarCalendario(year, month) {
    gridDiasDiv.innerHTML = '';
    const today = new Date();
    const primerDiaDelMes = new Date(year, month, 1);
    const ultimoDiaDelMes = new Date(year, month + 1, 0);
    const diasEnElMes = ultimoDiaDelMes.getDate();
    const diaDeInicio = primerDiaDelMes.getDay();
    mesAnioH2.textContent = `${primerDiaDelMes.toLocaleString('es-ES', { month: 'long' })} ${year}`;
    for (let i = 0; i < diaDeInicio; i++) {
        const divVacio = document.createElement('div');
        divVacio.classList.add('dia', 'vacio');
        gridDiasDiv.appendChild(divVacio);
    }
    await cargarRecordatoriosMes(year, month);
    for (let i = 1; i <= diasEnElMes; i++) {
        const diaDiv = document.createElement('div');
        diaDiv.classList.add('dia');
        const numeroDia = document.createElement('span');
        numeroDia.classList.add('numero-dia');
        numeroDia.textContent = i;
        diaDiv.appendChild(numeroDia);
        const fechaStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
        diaDiv.dataset.fecha = fechaStr;
        if (i === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
            diaDiv.classList.add('hoy');
        }
        const recordatoriosDia = recordatorios.filter(r => r.fecha === fechaStr);
        recordatoriosDia.forEach(r => {
            const recordatorioItem = document.createElement('div');
            recordatorioItem.classList.add('recordatorio-item');
            recordatorioItem.classList.add(r.importancia); // clase según importancia
            recordatorioItem.textContent = r.titulo;
            diaDiv.appendChild(recordatorioItem);
        });
        diaDiv.addEventListener('click', () => abrirFormulario(fechaStr));
        gridDiasDiv.appendChild(diaDiv);
    }
}

// --- Modal ---
function abrirFormulario(fecha) {
    diaSeleccionadoSpan.textContent = fecha;
    recordatoriosListaDiv.innerHTML = '';
    const recordatoriosDia = recordatorios.filter(r => r.fecha === fecha);
        if (recordatoriosDia.length > 0) {
            recordatoriosDia.forEach(r => {
                const detalleDiv = document.createElement('div');
                detalleDiv.classList.add('recordatorio-detalle');
                detalleDiv.innerHTML = `
                    <div>
                        <h4>${r.titulo}</h4>
                        <p>${r.descripcion || ''}</p>
                        <span class="importancia-label ${r.importancia}">${r.importancia ? r.importancia.charAt(0).toUpperCase() + r.importancia.slice(1) : ''}</span>
                    </div>
                    <div style="display:flex; gap:8px; align-items:center;">
                        <button class="editar-btn" data-id="${r.id}">✎</button>
                        <button class="eliminar-btn" data-id="${r.id}">&times;</button>
                    </div>
                `;
                // Eliminar
                detalleDiv.querySelector('.eliminar-btn').addEventListener('click', async () => {
                    await eliminarRecordatorioAPI(r.id);
                    await generarCalendario(currentYear, currentMonth);
                    abrirFormulario(fecha);
                });
                // Editar
                detalleDiv.querySelector('.editar-btn').addEventListener('click', () => {
                    document.getElementById('titulo').value = r.titulo;
                    document.getElementById('descripcion').value = r.descripcion;
                    document.getElementById('importancia').value = r.importancia;
                    // Actualizar visualmente el selector de importancia
                    botonesImportancia.forEach(b => {
                        b.classList.remove('seleccionada');
                        if (b.dataset.importance === r.importancia) {
                            b.classList.add('seleccionada');
                        }
                    });
                    formRecordatorio.dataset.editId = r.id;
                });
                recordatoriosListaDiv.appendChild(detalleDiv);
            });
        } else {
            recordatoriosListaDiv.innerHTML = '<p>No hay recordatorios para este día.</p>';
        }
    modal.style.display = 'flex';
}

// --- Eventos ---
prevBtn.addEventListener('click', async () => {
    currentMonth--;
    if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    }
    await generarCalendario(currentYear, currentMonth);
});

nextBtn.addEventListener('click', async () => {
    currentMonth++;
    if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    }
    await generarCalendario(currentYear, currentMonth);
});

closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
    formRecordatorio.reset();
});

formRecordatorio.addEventListener('submit', async (e) => {
    e.preventDefault();
    const titulo = document.getElementById('titulo').value;
    const descripcion = document.getElementById('descripcion').value;
    const fecha = diaSeleccionadoSpan.textContent;
    const importancia = document.getElementById('importancia').value;
    if (formRecordatorio.dataset.editId) {
        // Actualizar
        await actualizarRecordatorioAPI(formRecordatorio.dataset.editId, fecha, titulo, descripcion, importancia);
        delete formRecordatorio.dataset.editId;
    } else {
        // Crear nuevo
        await guardarRecordatorioAPI(fecha, titulo, descripcion, importancia);
    }
    await generarCalendario(currentYear, currentMonth);
    modal.style.display = 'none';
    formRecordatorio.reset();
    // Restaurar selector de importancia a baja
    botonesImportancia.forEach(b => b.classList.remove('seleccionada'));
    botonesImportancia.forEach(b => { if (b.dataset.importance === 'baja') b.classList.add('seleccionada'); });
// Actualizar recordatorio
async function actualizarRecordatorioAPI(id, fecha, titulo, descripcion, importancia) {
    const res = await fetch(`/api/recordatorios/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fecha, titulo, descripcion, importancia })
    });
    return res.ok;
}
});

// --- Inicialización ---
generarCalendario(currentYear, currentMonth);

// --- Selección de Importancia ---
// --- Selección de Importancia ---
const botonesImportancia = document.querySelectorAll('.boton-importancia');
const inputImportancia = document.getElementById('importancia');

botonesImportancia.forEach(boton => {
    boton.addEventListener('click', () => {
        // Quitar la clase 'seleccionada' de todos los botones
        botonesImportancia.forEach(b => b.classList.remove('seleccionada'));
        // Agregar la clase 'seleccionada' al botón clicado
        boton.classList.add('seleccionada');
        // Actualizar el valor del input oculto
        inputImportancia.value = boton.dataset.importance;
    });
});



function abrirFormulario(fecha) {
    diaSeleccionadoSpan.textContent = fecha;
    recordatoriosListaDiv.innerHTML = '';
    const recordatoriosDia = recordatorios.filter(r => r.fecha === fecha);
    if (recordatoriosDia.length > 0) {
        recordatoriosDia.forEach(r => {
            const detalleDiv = document.createElement('div');
            detalleDiv.classList.add('recordatorio-detalle');
            detalleDiv.innerHTML = `
                <div>
                    <h4>${r.titulo}</h4>
                    <p>${r.descripcion || ''}</p>
                    <span class="importancia-label ${r.importancia}">${r.importancia ? r.importancia.charAt(0).toUpperCase() + r.importancia.slice(1) : ''}</span>
                </div>
                <div style="display:flex; gap:8px; align-items:center;">
                    <button class="editar-btn" data-id="${r.id}">✎</button>
                    <button class="eliminar-btn" data-id="${r.id}">&times;</button>
                </div>
            `;
            // Eliminar
            detalleDiv.querySelector('.eliminar-btn').addEventListener('click', async () => {
                await eliminarRecordatorioAPI(r.id);
                await generarCalendario(currentYear, currentMonth);
                abrirFormulario(fecha);
            });
            // Editar
            detalleDiv.querySelector('.editar-btn').addEventListener('click', () => {
                document.getElementById('titulo').value = r.titulo;
                document.getElementById('descripcion').value = r.descripcion;
                document.getElementById('importancia').value = r.importancia;
                // Actualizar visualmente el selector de importancia
                botonesImportancia.forEach(b => {
                    b.classList.remove('seleccionada');
                    if (b.dataset.importance === r.importancia) {
                        b.classList.add('seleccionada');
                    }
                });
                formRecordatorio.dataset.editId = r.id;
            });
            recordatoriosListaDiv.appendChild(detalleDiv);
        });
    } else {
        recordatoriosListaDiv.innerHTML = '<p>No hay recordatorios para este día.</p>';
    }
    modal.style.display = 'flex';
}

// calendario.js o en un <script> al final del body

document.addEventListener('DOMContentLoaded', function() {
    
    // Elementos del nuevo modal lateral
    const socialModal = document.getElementById('social-modal');
    const openSocialModalBtn = document.getElementById('open-social-modal');
    const closeSocialModalBtn = document.querySelector('.close-lateral-modal');

    // Abrir el modal
    openSocialModalBtn.addEventListener('click', function(e) {
        e.preventDefault(); // Evita que el enlace recargue la página
        socialModal.classList.add('visible');
    });

    // Cerrar el modal con el botón X
    closeSocialModalBtn.addEventListener('click', function() {
        socialModal.classList.remove('visible');
    });

    // Cerrar el modal al hacer clic fuera del contenido
    socialModal.addEventListener('click', function(e) {
        if (e.target === socialModal) {
            socialModal.classList.remove('visible');
        }
    });

});