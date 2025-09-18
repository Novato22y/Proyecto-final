// Sistema de Tareas - EduNote
// Gestión completa de tareas con calendario y tablero Kanban

class SistemaTareas {
    constructor() {
        this.fechaActual = new Date();
        this.fechaSeleccionada = null;
        this.tareaEditando = null;
        this.kanbanColapsado = false;
        this.todasLasTareas = [];
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.renderCalendario();
        this.cargarTodasLasTareas();
        this.setupModal();
        this.setupKanban();
    }

    setupEventListeners() {
        // Navegación del calendario
        document.getElementById('prev-btn').addEventListener('click', () => {
            this.fechaActual.setMonth(this.fechaActual.getMonth() - 1);
            this.renderCalendario();
        });
        
        document.getElementById('next-btn').addEventListener('click', () => {
            this.fechaActual.setMonth(this.fechaActual.getMonth() + 1);
            this.renderCalendario();
        });
        
        // Botones agregar tarea
        const btnCalendar = document.getElementById('add-task-calendar');
        const btnKanban = document.getElementById('add-task-kanban');
        
        if (btnCalendar) {
            btnCalendar.addEventListener('click', () => {
                this.abrirModal();
            });
        }
        
        if (btnKanban) {
            btnKanban.addEventListener('click', () => {
                this.abrirModal(null, true); // Sin fecha para que vaya a inbox
            });
        }
        
        // Toggle Kanban
        document.getElementById('toggle-kanban').addEventListener('click', () => {
            this.toggleKanban();
        });
        
        // Modal
        document.querySelector('.close-btn').addEventListener('click', () => {
            this.cerrarModal();
        });
        
        // Formulario
        document.getElementById('tarea-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.guardarTarea();
        });
        
        // Campos dinámicos tipo tags
        document.getElementById('add-enlace-btn').addEventListener('click', () => {
            this.agregarEnlaceTag();
        });
        
        document.getElementById('enlace-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.agregarEnlaceTag();
            }
        });
        
        document.getElementById('add-contacto-btn').addEventListener('click', () => {
            this.agregarContactoTag();
        });
        
        document.getElementById('contacto-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.agregarContactoTag();
            }
        });
        
        // Importancia
        document.querySelectorAll('.boton-importancia').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.boton-importancia').forEach(b => b.classList.remove('seleccionada'));
                e.target.classList.add('seleccionada');
                document.getElementById('importancia').value = e.target.dataset.importance;
            });
        });
    }
    
    // === CALENDARIO ===
    renderCalendario() {
        const año = this.fechaActual.getFullYear();
        const mes = this.fechaActual.getMonth();
        
        // Actualizar título
        const meses = [
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ];
        document.getElementById('mes-anio').textContent = `${meses[mes]} ${año}`;
        
        // Generar días
        const gridDias = document.getElementById('grid-dias');
        gridDias.innerHTML = '';
        
        const primerDia = new Date(año, mes, 1);
        const ultimoDia = new Date(año, mes + 1, 0);
        const diasMes = ultimoDia.getDate();
        const diaSemana = primerDia.getDay();
        
        // Días vacíos del mes anterior
        for (let i = 0; i < diaSemana; i++) {
            const diaVacio = document.createElement('div');
            diaVacio.className = 'dia-vacio';
            gridDias.appendChild(diaVacio);
        }
        
        // Días del mes actual
        for (let dia = 1; dia <= diasMes; dia++) {
            const divDia = document.createElement('div');
            divDia.className = 'dia';
            divDia.textContent = dia;
            
            const fechaDia = new Date(año, mes, dia);
            const fechaString = fechaDia.toISOString().split('T')[0];
            
            // Marcar día actual
            const hoy = new Date();
            if (fechaDia.toDateString() === hoy.toDateString()) {
                divDia.classList.add('dia-actual');
            }
            
            // Agregar indicador si hay tareas
            this.agregarIndicadorTareas(divDia, fechaString);
            
            // Click en día
            divDia.addEventListener('click', () => {
                this.seleccionarDia(fechaString, divDia);
            });
            
            gridDias.appendChild(divDia);
        }
    }
    
    agregarIndicadorTareas(divDia, fecha) {
        const tareasDelDia = this.todasLasTareas.filter(tarea => tarea.fecha === fecha);
        if (tareasDelDia.length > 0) {
            const indicador = document.createElement('div');
            indicador.className = 'indicador-tarea';
            indicador.textContent = tareasDelDia.length;
            divDia.appendChild(indicador);
            divDia.classList.add('con-tareas');
        }
    }
    
    seleccionarDia(fecha, elemento) {
        // Remover selección anterior
        document.querySelectorAll('.dia-seleccionado').forEach(d => d.classList.remove('dia-seleccionado'));
        elemento.classList.add('dia-seleccionado');
        
        this.fechaSeleccionada = fecha;
        this.abrirModal(fecha);
    }
    
    // === KANBAN ===
    setupKanban() {
        // Hacer las columnas drag & drop
        this.setupDragAndDrop();
    }
    
    renderKanban() {
        const inbox = document.getElementById('kanban-inbox');
        const incompletas = document.getElementById('kanban-incompletas');
        const completas = document.getElementById('kanban-completas');
        
        // Limpiar columnas
        inbox.innerHTML = '';
        incompletas.innerHTML = '';
        completas.innerHTML = '';
        
        // Organizar tareas por status
        this.todasLasTareas.forEach(tarea => {
            const tarjetaTarea = this.crearTarjetaTarea(tarea);
            
            switch (tarea.status) {
                case 'inbox':
                    inbox.appendChild(tarjetaTarea);
                    break;
                case 'incompleta':
                    incompletas.appendChild(tarjetaTarea);
                    break;
                case 'completa':
                    completas.appendChild(tarjetaTarea);
                    break;
            }
        });
    }
    
    crearTarjetaTarea(tarea) {
        const tarjeta = document.createElement('div');
        tarjeta.className = `task-card ${tarea.importancia || ''}`;
        tarjeta.dataset.tareaId = tarea.id;
        
        tarjeta.innerHTML = `
            <div class="task-title">${tarea.titulo}</div>
            <div class="task-description">${tarea.descripcion || ''}</div>
            <div class="task-meta">
                <span class="task-asunto">${tarea.asunto || ''}</span>
                <span class="task-fecha">${tarea.fecha || 'Sin fecha'}</span>
            </div>
            <div class="task-actions" style="margin-top: 8px;">
                <button onclick="sistemaTareas.editarTarea(${tarea.id})" style="font-size: 0.7rem; padding: 2px 6px; margin-right: 4px;">✏️</button>
                <button onclick="sistemaTareas.eliminarTarea(${tarea.id})" style="font-size: 0.7rem; padding: 2px 6px; background: #e53e3e; color: white; border: none; border-radius: 3px;">🗑️</button>
            </div>
        `;
        
        // Hacer la tarjeta arrastrable
        tarjeta.draggable = true;
        tarjeta.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', tarea.id);
        });
        
        return tarjeta;
    }
    
    setupDragAndDrop() {
        const columnas = document.querySelectorAll('.kanban-tasks');
        
        columnas.forEach(columna => {
            columna.addEventListener('dragover', (e) => {
                e.preventDefault();
                columna.style.backgroundColor = '#f0f8ff';
            });
            
            columna.addEventListener('dragleave', () => {
                columna.style.backgroundColor = '';
            });
            
            columna.addEventListener('drop', (e) => {
                e.preventDefault();
                columna.style.backgroundColor = '';
                
                const tareaId = e.dataTransfer.getData('text/plain');
                const nuevoStatus = columna.id.replace('kanban-', '');
                
                this.cambiarStatusTarea(tareaId, nuevoStatus);
            });
        });
    }
    
    async cambiarStatusTarea(tareaId, nuevoStatus) {
        try {
            const response = await fetch(`/api/tareas/${tareaId}`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({status: nuevoStatus})
            });
            
            if (response.ok) {
                await this.cargarTodasLasTareas();
                this.renderKanban();
                this.renderCalendario();
            }
        } catch (error) {
            console.error('Error al cambiar status:', error);
        }
    }
    
    toggleKanban() {
        const kanbanSection = document.getElementById('kanban-sidebar');
        this.kanbanColapsado = !this.kanbanColapsado;
        
        if (this.kanbanColapsado) {
            kanbanSection.classList.add('collapsed');
        } else {
            kanbanSection.classList.remove('collapsed');
        }
    }
    
    // === MODAL ===
    setupModal() {
        // Cerrar modal al hacer click fuera
        document.getElementById('modal-form').addEventListener('click', (e) => {
            if (e.target.id === 'modal-form') {
                this.cerrarModal();
            }
        });
    }
    
    abrirModal(fecha = null, sinFecha = false) {
        const modal = document.getElementById('modal-form');
        const tituloModal = document.getElementById('modal-title');
        const diaSeleccionado = document.getElementById('dia-seleccionado');
        const inputFecha = document.getElementById('fecha');
        
        // Limpiar formulario
        this.limpiarFormulario();
        
        if (sinFecha) {
            tituloModal.textContent = 'Nueva Tarea - Inbox';
            diaSeleccionado.textContent = 'Sin fecha (irá al Inbox)';
            inputFecha.value = '';
        } else if (fecha) {
            tituloModal.textContent = 'Nueva Tarea';
            diaSeleccionado.textContent = this.formatearFecha(fecha);
            inputFecha.value = fecha;
        } else {
            tituloModal.textContent = 'Nueva Tarea';
            diaSeleccionado.textContent = 'Fecha opcional';
        }
        
        modal.style.display = 'flex';
        document.getElementById('titulo').focus();
        
        // Cargar tareas existentes si hay fecha
        if (fecha) {
            this.cargarTareasDelDia(fecha);
        }
    }
    
    cerrarModal() {
        document.getElementById('modal-form').style.display = 'none';
        this.tareaEditando = null;
        this.limpiarFormulario();
    }
    
    limpiarFormulario() {
        document.getElementById('tarea-form').reset();
        document.getElementById('importancia').value = 'baja';
        document.querySelectorAll('.boton-importancia').forEach(b => b.classList.remove('seleccionada'));
        document.querySelector('.boton-importancia.baja').classList.add('seleccionada');
        
        // Limpiar contenedores de tags
        document.getElementById('enlaces-tags').innerHTML = '';
        document.getElementById('contactos-tags').innerHTML = '';
        
        // Limpiar inputs
        document.getElementById('enlace-input').value = '';
        document.getElementById('contacto-input').value = '';
    }
    
    async guardarTarea() {
        const datos = this.recogerDatosFormulario();
        
        try {
            let response;
            if (this.tareaEditando) {
                response = await fetch(`/api/tareas/${this.tareaEditando}`, {
                    method: 'PUT',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(datos)
                });
            } else {
                response = await fetch('/api/tareas', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(datos)
                });
            }
            
            if (response.ok) {
                await this.cargarTodasLasTareas();
                this.renderKanban();
                this.renderCalendario();
                this.cerrarModal();
                
                if (datos.fecha) {
                    this.cargarTareasDelDia(datos.fecha);
                }
            } else {
                const error = await response.json();
                alert('Error al guardar: ' + (error.error || 'Error desconocido'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error de conexión');
        }
    }
    
    recogerDatosFormulario() {
        return {
            titulo: document.getElementById('titulo').value.trim(),
            descripcion: document.getElementById('descripcion').value.trim(),
            fecha: document.getElementById('fecha').value || null,
            importancia: document.getElementById('importancia').value || null,
            asunto: document.getElementById('asunto').value.trim() || null,
            enlaces: this.recogerEnlacesTags(),
            contactos: this.recogerContactosTags()
        };
    }
    
    recogerEnlacesTags() {
        const enlaces = [];
        document.querySelectorAll('#enlaces-tags .tag span').forEach(span => {
            const texto = span.textContent.trim();
            if (texto) {
                enlaces.push(texto); // Como string simple
            }
        });
        return enlaces;
    }
    
    recogerContactosTags() {
        const contactos = [];
        document.querySelectorAll('#contactos-tags .tag span').forEach(span => {
            const texto = span.textContent.trim();
            if (texto) {
                contactos.push({nombre: texto}); // Como objeto con nombre
            }
        });
        return contactos;
    }
    
    // === ENLACES Y CONTACTOS COMO TAGS ===
    agregarEnlaceTag() {
        const input = document.getElementById('enlace-input');
        const valor = input.value.trim();
        
        if (valor) {
            const container = document.getElementById('enlaces-tags');
            const tag = document.createElement('div');
            tag.className = 'tag';
            tag.innerHTML = `
                <span>${valor}</span>
                <button type="button" class="remove-tag" onclick="this.parentElement.remove()">×</button>
            `;
            container.appendChild(tag);
            input.value = '';
            input.focus();
        }
    }
    
    agregarContactoTag() {
        const input = document.getElementById('contacto-input');
        const valor = input.value.trim();
        
        if (valor) {
            const container = document.getElementById('contactos-tags');
            const tag = document.createElement('div');
            tag.className = 'tag';
            tag.innerHTML = `
                <span>${valor}</span>
                <button type="button" class="remove-tag" onclick="this.parentElement.remove()">×</button>
            `;
            container.appendChild(tag);
            input.value = '';
            input.focus();
        }
    }
    
    // === API CALLS ===
    async cargarTodasLasTareas() {
        try {
            const response = await fetch('/api/tareas');
            if (response.ok) {
                this.todasLasTareas = await response.json();
                this.renderKanban();
            }
        } catch (error) {
            console.error('Error al cargar tareas:', error);
        }
    }
    
    async cargarTareasDelDia(fecha) {
        try {
            const response = await fetch(`/api/tareas/fecha/${fecha}`);
            if (response.ok) {
                const tareas = await response.json();
                this.mostrarTareasExistentes(tareas);
            }
        } catch (error) {
            console.error('Error al cargar tareas del día:', error);
        }
    }
    
    mostrarTareasExistentes(tareas) {
        const container = document.getElementById('recordatorios-existentes');
        container.innerHTML = '';
        
        if (tareas.length === 0) {
            container.innerHTML = '<p>No hay tareas para este día.</p>';
            return;
        }
        
        tareas.forEach(tarea => {
            const div = document.createElement('div');
            div.className = 'tarea-existente';
            div.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px; background: #f8f9fa; margin: 4px 0; border-radius: 4px;">
                    <div>
                        <strong>${tarea.titulo}</strong>
                        <br><small>${tarea.descripcion || ''}</small>
                        <br><span class="badge ${tarea.importancia}">${tarea.importancia || 'sin prioridad'}</span>
                    </div>
                    <div>
                        <button onclick="sistemaTareas.editarTarea(${tarea.id})" style="margin: 0 2px; padding: 4px 8px; font-size: 0.8rem;">✏️</button>
                        <button onclick="sistemaTareas.eliminarTarea(${tarea.id})" style="margin: 0 2px; padding: 4px 8px; font-size: 0.8rem; background: #dc3545; color: white; border: none; border-radius: 3px;">🗑️</button>
                    </div>
                </div>
            `;
            container.appendChild(div);
        });
    }
    
    async editarTarea(id) {
        const tarea = this.todasLasTareas.find(t => t.id === id);
        if (!tarea) return;
        
        this.tareaEditando = id;
        this.abrirModal(tarea.fecha);
        
        // Llenar formulario con datos existentes
        document.getElementById('titulo').value = tarea.titulo;
        document.getElementById('descripcion').value = tarea.descripcion || '';
        document.getElementById('fecha').value = tarea.fecha || '';
        document.getElementById('asunto').value = tarea.asunto || '';
        document.getElementById('importancia').value = tarea.importancia || 'baja';
        
        // Seleccionar importancia
        document.querySelectorAll('.boton-importancia').forEach(b => b.classList.remove('seleccionada'));
        document.querySelector(`[data-importance="${tarea.importancia || 'baja'}"]`).classList.add('seleccionada');
        
        // Cargar enlaces existentes como tags
        const enlacesContainer = document.getElementById('enlaces-tags');
        enlacesContainer.innerHTML = '';
        if (tarea.enlaces && tarea.enlaces.length > 0) {
            tarea.enlaces.forEach(enlace => {
                const tag = document.createElement('div');
                tag.className = 'tag';
                const valor = enlace.titulo ? `${enlace.titulo} (${enlace.url})` : enlace.url;
                tag.innerHTML = `
                    <span>${valor}</span>
                    <button type="button" class="remove-tag" onclick="this.parentElement.remove()">×</button>
                `;
                enlacesContainer.appendChild(tag);
            });
        }
        
        // Cargar contactos existentes como tags
        const contactosContainer = document.getElementById('contactos-tags');
        contactosContainer.innerHTML = '';
        if (tarea.contactos && tarea.contactos.length > 0) {
            tarea.contactos.forEach(contacto => {
                const tag = document.createElement('div');
                tag.className = 'tag';
                const valor = `${contacto.nombre}${contacto.email ? ' (' + contacto.email + ')' : ''}`;
                tag.innerHTML = `
                    <span>${valor}</span>
                    <button type="button" class="remove-tag" onclick="this.parentElement.remove()">×</button>
                `;
                contactosContainer.appendChild(tag);
            });
        }
    }
    
    async eliminarTarea(id) {
        if (!confirm('¿Estás seguro de que quieres eliminar esta tarea?')) return;
        
        try {
            const response = await fetch(`/api/tareas/${id}`, {method: 'DELETE'});
            if (response.ok) {
                await this.cargarTodasLasTareas();
                this.renderKanban();
                this.renderCalendario();
                
                // Actualizar lista de tareas existentes si el modal está abierto
                if (this.fechaSeleccionada) {
                    this.cargarTareasDelDia(this.fechaSeleccionada);
                }
            }
        } catch (error) {
            console.error('Error al eliminar tarea:', error);
        }
    }
    
    // === UTILIDADES ===
    formatearFecha(fecha) {
        const fechaObj = new Date(fecha + 'T00:00:00');
        return fechaObj.toLocaleDateString('es-ES', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
}

// Inicializar el sistema cuando se carga la página
let sistemaTareas;
document.addEventListener('DOMContentLoaded', function() {
    sistemaTareas = new SistemaTareas();
});