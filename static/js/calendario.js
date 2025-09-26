// Envuelve toda la inicialización que toca el DOM para asegurarnos de que
// los elementos existen al ejecutarse el script (evita errores en cargas tempranas)
document.addEventListener('DOMContentLoaded', () => {
    console.log('calendario.js: DOMContentLoaded - inicializando calendario');
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

    // --- Selección de Importancia ---
    const botonesImportancia = document.querySelectorAll('.boton-importancia');
    const inputImportancia = document.getElementById('importancia');

    // Manejo visual del selector de importancia
    botonesImportancia.forEach(boton => {
        boton.addEventListener('click', () => {
            botonesImportancia.forEach(b => b.classList.remove('seleccionada'));
            boton.classList.add('seleccionada');
            inputImportancia.value = boton.dataset.importance;
        });
    });

// --- API Flask ---
async function cargarRecordatoriosMes(year, month) {
    recordatorios = [];
    const diasEnElMes = new Date(year, month + 1, 0).getDate();
    console.log(`cargarRecordatoriosMes: solicitando recordatorios para ${year}-${String(month+1).padStart(2,'0')}`);
    // --- También obtener Tareas (modelo Tarea) para mostrarlas en el calendario ---
    try {
        console.log('fetch -> /api/tareas (obtener todas las tareas del usuario)');
        const tareasRes = await fetch('/api/tareas');
        if (tareasRes.ok) {
            const tareasData = await tareasRes.json();
            // Filtrar tareas que tienen fecha en el mes solicitado y convertir al formato esperado
            const prefijoMes = `${year}-${String(month+1).padStart(2,'0')}`;
            const tareasMes = (tareasData || []).filter(t => t.fecha && t.fecha.startsWith(prefijoMes));
            tareasMes.forEach(t => {
                recordatorios.push({
                    id: t.id,
                    fecha: t.fecha,
                    titulo: t.titulo,
                    descripcion: t.descripcion || '',
                    importancia: t.importancia || 'baja',
                    _fuente: 'tarea'
                });
            });
            console.log(`Tareas añadidas desde /api/tareas para ${prefijoMes}:`, tareasMes.length);
        } else {
            console.warn('/api/tareas respondió con status', tareasRes.status);
        }
    } catch (e) {
        console.error('Error obteniendo /api/tareas:', e);
    }
    for (let i = 1; i <= diasEnElMes; i++) {
        const fechaStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
        try {
            console.log('fetch ->', `/api/recordatorios/${fechaStr}`);
            const res = await fetch(`/api/recordatorios/${fechaStr}`);
            console.log(`fetch status for ${fechaStr}:`, res.status);
            if (res.ok) {
                try {
                    const data = await res.json();
                    if (Array.isArray(data) && data.length > 0) {
                        console.log(`Recordatorios para ${fechaStr}:`, data);
                    }
                    // Asegurarse de concatenar un array
                    if (Array.isArray(data)) recordatorios = recordatorios.concat(data.map(d => ({...d, _fuente: 'recordatorio'})));
                } catch (parseErr) {
                    console.error(`Error parseando JSON para ${fechaStr}:`, parseErr);
                }
            } else {
                let body = '';
                try { body = await res.text(); } catch (e) { body = '<no body>'; }
                console.warn(`Error HTTP obteniendo ${fechaStr}:`, res.status, body);
            }
        } catch (e) {
            console.error(`Excepción al obtener recordatorios para ${fechaStr}:`, e);
        }
    }
    console.log('Recordatorios cargados para el mes:', recordatorios);
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
});

// Actualizar recordatorio (declarada aquí para uso desde el submit)
async function actualizarRecordatorioAPI(id, fecha, titulo, descripcion, importancia) {
    const res = await fetch(`/api/recordatorios/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fecha, titulo, descripcion, importancia })
    });
    return res.ok;
}

    // --- Inicialización ---
    generarCalendario(currentYear, currentMonth);

    // --- Modal lateral (social) ---
    // Elementos del nuevo modal lateral
    const socialModal = document.getElementById('social-modal');
    const openSocialModalBtn = document.getElementById('open-social-modal');
    const closeSocialModalBtn = document.querySelector('.close-lateral-modal');

    if (openSocialModalBtn && socialModal) {
        openSocialModalBtn.addEventListener('click', function(e) {
            e.preventDefault(); // Evita que el enlace recargue la página
            socialModal.classList.add('visible');
        });
    }
    if (closeSocialModalBtn) {
        closeSocialModalBtn.addEventListener('click', function() {
            socialModal.classList.remove('visible');
        });
    }
    if (socialModal) {
        socialModal.addEventListener('click', function(e) {
            if (e.target === socialModal) {
                socialModal.classList.remove('visible');
            }
        });
    }

});