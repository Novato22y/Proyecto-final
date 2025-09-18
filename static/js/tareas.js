// Sistema de Tareas - EduNote
// Gestión completa de tareas con calendario y tablero Kanban

class SistemaTareas {
    constructor() {
        this.fechaActual = new Date();
        this.fechaSeleccionada = null;
        this.tareaEditandoId = null;
        this.kanbanColapsado = false;
        this.todasLasTareas = [];
    this.isSaving = false;
        
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
            // Click event
            btn.addEventListener('click', (e) => {
                this.seleccionarImportancia(e.target);
            });
            
            // Keyboard events para accesibilidad
            btn.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.seleccionarImportancia(e.target);
                }
            });
        });
    }
    
    seleccionarImportancia(elemento) {
        // Remover selección anterior
        document.querySelectorAll('.boton-importancia').forEach(b => {
            b.classList.remove('seleccionada');
            b.setAttribute('aria-checked', 'false');
        });
        
        // Seleccionar nuevo elemento
        elemento.classList.add('seleccionada');
        elemento.setAttribute('aria-checked', 'true');
        document.getElementById('importancia').value = elemento.dataset.importance;
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
        console.log('Renderizando Kanban con tareas IDs:', this.todasLasTareas.map(t=>t.id));
        
        // Organizar tareas por status
        const seen = new Set();
        this.todasLasTareas.forEach(tarea => {
            if (seen.has(tarea.id)) {
                console.warn('Omitiendo tarea duplicada en memoria id=', tarea.id);
                return;
            }
            seen.add(tarea.id);
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
        console.log('Creando tarjeta para tarea id=', tarea.id);
        // Evitar crear dos tarjetas con mismo id en DOM
        const existing = document.querySelector(`.task-card[data-tarea-id="${tarea.id}"]`);
        if (existing) {
            console.warn('Tarjeta ya existe en DOM para id=', tarea.id, '; se reemplazara.');
            existing.remove();
        }
        const tarjeta = document.createElement('div');
        tarjeta.className = `task-card ${tarea.importancia || ''}`;
        tarjeta.dataset.tareaId = tarea.id;
        
        // Crear HTML para enlaces si existen
        let enlacesHtml = '';
        if (tarea.enlaces && tarea.enlaces.length > 0) {
            enlacesHtml = `
                <div class="task-enlaces" style="margin-top: 6px;">
                    <span style="font-size: 0.7rem; color: #666;">🔗 Enlaces:</span>
                    <div style="margin-top: 2px;">
                        ${tarea.enlaces.map(enlaceObj => {
                            // Manejar tanto objetos {url: "...", titulo: "..."} como strings directos
                            const url = typeof enlaceObj === 'object' ? enlaceObj.url : enlaceObj;
                            const titulo = typeof enlaceObj === 'object' ? (enlaceObj.titulo || url) : url;
                            const displayText = titulo.length > 25 ? titulo.substring(0, 25) + '...' : titulo;
                            const fullUrl = url.startsWith('http') ? url : 'https://' + url;
                            return `<a href="${fullUrl}" target="_blank" rel="noopener" style="font-size: 0.7rem; color: #0066cc; text-decoration: none; display: inline-block; margin-right: 8px;" title="${titulo}">🌐 ${displayText}</a>`;
                        }).join('')}
                    </div>
                </div>
            `;
        }
        
        tarjeta.innerHTML = `
            <div class="task-title">${tarea.titulo}</div>
            <div class="task-description">${tarea.descripcion || ''}</div>
            <div class="task-meta">
                <span class="task-asunto">${tarea.asunto || ''}</span>
                <span class="task-fecha">${tarea.fecha || 'Sin fecha'}</span>
            </div>
            ${enlacesHtml}
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
        this.limpiarFormulario();
    }
    
    limpiarFormulario() {
        document.getElementById('tarea-form').reset();
        document.getElementById('importancia').value = 'baja';
        
        // Resetear importancia con atributos ARIA
        document.querySelectorAll('.boton-importancia').forEach(b => {
            b.classList.remove('seleccionada');
            b.setAttribute('aria-checked', 'false');
        });
        const botonBaja = document.querySelector('.boton-importancia[data-importance="baja"]');
        if (botonBaja) {
            botonBaja.classList.add('seleccionada');
            botonBaja.setAttribute('aria-checked', 'true');
        }
        
        // Limpiar contenedores de tags
        document.getElementById('enlaces-tags').innerHTML = '';
        document.getElementById('contactos-tags').innerHTML = '';
        
        // Limpiar inputs
        document.getElementById('enlace-input').value = '';
        document.getElementById('contacto-input').value = '';
        
        // Limpiar el ID de edición
        console.log('Limpiando tareaEditandoId, era:', this.tareaEditandoId);
        this.tareaEditandoId = null;
    }
    
    async guardarTarea() {
        const datos = this.recogerDatosFormulario();
        console.log('=== GUARDANDO TAREA ===');
        console.log('Datos a guardar:', datos);
        console.log('tareaEditandoId antes de guardar:', this.tareaEditandoId);
        console.log('¿Es edición?:', !!this.tareaEditandoId);
        if (this.isSaving) {
            console.warn('Ignorando guardado: ya hay una operación en curso');
            return;
        }

        this.isSaving = true;
        let response = null;
        try {
            if (this.tareaEditandoId) {
                console.log('Editando tarea existente ID:', this.tareaEditandoId);
                const url = `/api/tareas/${this.tareaEditandoId}`;
                console.log('Enviando fetch:', 'PUT', url);
                response = await fetch(url, {
                    method: 'PUT',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(datos)
                });
            } else {
                const url = '/api/tareas';
                console.log('Creando nueva tarea - Enviando fetch:', 'POST', url);
                response = await fetch(url, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(datos)
                });
            }

            if (response && response.ok) {
                const result = await response.json();
                console.log('Respuesta de la API:', result);

                // Limpiar estado de edición PRIMERO
                this.cerrarModal();

                // Luego actualizar las vistas
                await this.cargarTodasLasTareas();
                this.renderKanban();
                this.renderCalendario();

                if (datos.fecha) {
                    this.cargarTareasDelDia(datos.fecha);
                }
            } else if (response) {
                const error = await response.json();
                console.error('Error del servidor:', error);
                alert('Error al guardar: ' + (error.error || 'Error desconocido'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error de conexión');
        } finally {
            this.isSaving = false;
            console.log('tareaEditandoId después de guardar:', this.tareaEditandoId);
        }
    }
    
    recogerDatosFormulario() {
        // Recoger importancia de los botones seleccionados
        const importanciaSeleccionada = document.querySelector('.boton-importancia.seleccionada');
        const importanciaValue = importanciaSeleccionada ? importanciaSeleccionada.dataset.importance : 'baja';
        
        return {
            titulo: document.getElementById('titulo').value.trim(),
            descripcion: document.getElementById('descripcion').value.trim(),
            fecha: document.getElementById('fecha').value || null,
            importancia: importanciaValue,
            asunto: document.getElementById('asunto-categoria').value.trim() || null,
            enlaces: this.recogerEnlacesTags(),
            contactos: this.recogerContactosTags()
        };
    }
    
    recogerEnlacesTags() {
        const enlaces = [];
        // Buscar elementos de enlace con prioridad al data-original-url
        document.querySelectorAll('#enlaces-tags .tag .tag-link').forEach(element => {
            const textoOriginal = element.dataset.originalUrl || element.textContent.trim();
            if (textoOriginal) {
                enlaces.push(textoOriginal);
            }
        });
        
        // Fallback para enlaces antiguos sin data-original-url
        if (enlaces.length === 0) {
            document.querySelectorAll('#enlaces-tags .tag span').forEach(element => {
                const texto = element.textContent.trim();
                if (texto) {
                    enlaces.push(texto);
                }
            });
        }
        
        console.log('Enlaces recolectados:', enlaces);
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
        const valorOriginal = input.value.trim();
        
        if (valorOriginal) {
            // Crear URL completa para el href
            let valorCompleto = valorOriginal;
            if (!valorOriginal.startsWith('http://') && !valorOriginal.startsWith('https://')) {
                valorCompleto = 'https://' + valorOriginal;
            }
            
            const container = document.getElementById('enlaces-tags');
            const tag = document.createElement('div');
            tag.className = 'tag';
            tag.innerHTML = `
                <a href="${valorCompleto}" target="_blank" rel="noopener noreferrer" class="tag-link" data-original-url="${valorOriginal}">${valorOriginal}</a>
                <button type="button" class="remove-tag" onclick="this.parentElement.remove()">×</button>
            `;
            container.appendChild(tag);
            input.value = '';
            input.focus();
            console.log('Enlace agregado visualmente:', valorOriginal);
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
        if (this.isLoading) {
            console.warn('Ignorando cargarTodasLasTareas: ya hay una carga en curso');
            return;
        }
        this.isLoading = true;
        try {
            console.log('Fetching /api/tareas ...');
            const response = await fetch('/api/tareas');
            if (response.ok) {
                this.todasLasTareas = await response.json();
                console.log('Tareas cargadas:', this.todasLasTareas.map(t=>t.id));
                this.renderKanban();
            }
        } catch (error) {
            console.error('Error al cargar tareas:', error);
        } finally {
            this.isLoading = false;
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
            const isCompleted = tarea.status === 'completa';
            
            div.innerHTML = `
                <div class="tarea-contenedor ${isCompleted ? 'tarea-completada' : ''}" data-tarea-id="${tarea.id}" style="display: flex; justify-content: space-between; align-items: center; padding: 8px; background: ${isCompleted ? '#d4edda' : '#f8f9fa'}; margin: 4px 0; border-radius: 4px; cursor: pointer; transition: background-color 0.3s;">
                    <div class="tarea-info" style="flex: 1; padding-right: 8px;">
                        <strong style="${isCompleted ? 'text-decoration: line-through; opacity: 0.7;' : ''}">${tarea.titulo}</strong>
                        <br><small style="${isCompleted ? 'text-decoration: line-through; opacity: 0.7;' : ''}">${tarea.descripcion || ''}</small>
                        <br><span class="badge ${tarea.importancia}">${tarea.importancia || 'sin prioridad'}</span>
                    </div>
                    <div class="tarea-botones" style="display: flex; gap: 2px;">
                        <button class="btn-completar" data-action="completar" data-id="${tarea.id}" 
                                style="padding: 6px 8px; font-size: 0.8rem; background: ${isCompleted ? '#6c757d' : '#28a745'}; color: white; border: none; border-radius: 3px; min-width: 28px; cursor: pointer;">
                            ${isCompleted ? '↻' : '✓'}
                        </button>
                        <button class="btn-eliminar" data-action="eliminar" data-id="${tarea.id}" 
                                style="padding: 6px 8px; font-size: 0.8rem; background: #dc3545; color: white; border: none; border-radius: 3px; cursor: pointer;">🗑️</button>
                    </div>
                </div>
            `;
            
            // Agregar al contenedor primero
            container.appendChild(div);
            
            // Agregar event listeners usando delegación
            const tareaContenedor = div.querySelector('.tarea-contenedor');
            if (tareaContenedor) {
                tareaContenedor.addEventListener('click', (e) => {
                    console.log('Click detectado en tarea:', e.target);
                    const button = e.target.closest('button');
                    
                    if (button) {
                        console.log('Click en botón:', button);
                        e.stopPropagation();
                        const action = button.dataset.action;
                        const id = parseInt(button.dataset.id);
                        
                        if (action === 'completar') {
                            this.toggleCompletarTarea(id);
                        } else if (action === 'eliminar') {
                            this.eliminarTarea(id);
                        }
                    } else {
                        // Click en la tarea (no en botones) - abrir modal
                        console.log('Abriendo modal para tarea:', tarea.titulo);
                        this.abrirTareaDetalle(tarea);
                    }
                });
            }
        });
    }
    
    async editarTarea(id) {
        const tarea = this.todasLasTareas.find(t => t.id === id);
        if (!tarea) return;
        
        console.log('Iniciando edición de tarea ID:', id);
        this.abrirModal(tarea.fecha);
        this.tareaEditandoId = id;
        
        // Llenar formulario con datos existentes
        document.getElementById('titulo').value = tarea.titulo;
        document.getElementById('descripcion').value = tarea.descripcion || '';
        document.getElementById('fecha').value = tarea.fecha || '';
        document.getElementById('asunto-categoria').value = tarea.asunto || '';
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
    
    async toggleCompletarTarea(id) {
        console.log('Toggling tarea completada:', id);
        try {
            const tarea = this.todasLasTareas.find(t => t.id === id);
            if (!tarea) {
                console.log('Tarea no encontrada:', id);
                return;
            }
            
            // Toggle entre completa e incompleta
            tarea.status = tarea.status === 'completa' ? 'incompleta' : 'completa';
            
            const response = await fetch(`/api/tareas/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ status: tarea.status })
            });
            
            if (response.ok) {
                await this.cargarTodasLasTareas();
                this.renderKanban();
                this.renderCalendario();
                
                // Actualizar lista si el modal está abierto
                if (this.fechaSeleccionada) {
                    this.cargarTareasDelDia(this.fechaSeleccionada);
                }
            }
        } catch (error) {
            console.error('Error al completar tarea:', error);
        }
    }
    
    abrirTareaDetalle(tarea) {
        console.log('Abriendo tarea detalle:', tarea);
        
        // Preparar el modal con los datos de la tarea
        document.getElementById('titulo').value = tarea.titulo || '';
        document.getElementById('descripcion').value = tarea.descripcion || '';
        document.getElementById('asunto-categoria').value = tarea.asunto || '';
        document.getElementById('fecha').value = tarea.fecha || '';
        
        // Marcar la importancia
        const importanciaBtns = document.querySelectorAll('.boton-importancia');
        importanciaBtns.forEach(btn => {
            btn.classList.remove('seleccionada');
            btn.setAttribute('aria-checked', 'false');
            if (btn.dataset.importance === tarea.importancia) {
                btn.classList.add('seleccionada');
                btn.setAttribute('aria-checked', 'true');
            }
        });
        
        // Llenar enlaces
        const enlacesContainer = document.getElementById('enlaces-tags');
        enlacesContainer.innerHTML = '';
        if (tarea.enlaces && tarea.enlaces.length > 0) {
            console.log('Cargando enlaces:', tarea.enlaces); // Debug
            tarea.enlaces.forEach(enlaceObj => {
                // Manejar tanto objetos {url: "...", titulo: "..."} como strings directos
                const enlace = typeof enlaceObj === 'object' ? enlaceObj.url : enlaceObj;
                const titulo = typeof enlaceObj === 'object' ? (enlaceObj.titulo || enlace) : enlace;
                
                // Crear URL completa para el href
                let valorCompleto = enlace;
                if (!enlace.startsWith('http://') && !enlace.startsWith('https://')) {
                    valorCompleto = 'https://' + enlace;
                }
                
                const tag = document.createElement('div');
                tag.className = 'tag';
                tag.innerHTML = `
                    <a href="${valorCompleto}" target="_blank" rel="noopener noreferrer" class="tag-link" data-original-url="${enlace}">${titulo}</a>
                    <button type="button" class="remove-tag" onclick="this.parentElement.remove()">×</button>
                `;
                enlacesContainer.appendChild(tag);
            });
        }
        
        // Llenar contactos
        const contactosContainer = document.getElementById('contactos-tags');
        contactosContainer.innerHTML = '';
        if (tarea.contactos && tarea.contactos.length > 0) {
            tarea.contactos.forEach(contacto => {
                const tag = document.createElement('div');
                tag.className = 'tag';
                tag.innerHTML = `
                    <span>${contacto}</span>
                    <button type="button" class="remove-tag" onclick="this.parentElement.remove()">×</button>
                `;
                contactosContainer.appendChild(tag);
            });
        }
        
        // Abrir modal PRIMERO (esto limpia el formulario)
        this.abrirModal();
        
        // DESPUÉS establecer el ID para edición (para que no se limpie)
        console.log('Estableciendo ID para edición:', tarea.id);
        this.tareaEditandoId = tarea.id;
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