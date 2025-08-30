// script.js - Funcionalidades JavaScript del Planeador Escolar
document.addEventListener('DOMContentLoaded', () => {
    // Inicializar reloj en todas las páginas
    initializeClock();
    
    // Inicializar funcionalidades específicas según la página
    if (document.querySelector('.clock-panel')) {
        // Página principal
        initializeMainPage();
    }
    
    if (document.querySelector('.subject-details')) {
        // Página de detalle de materia
        initializeSubjectDetailPage();
    }
});

// =============================================================================
// FUNCIONES DEL RELOJ
// =============================================================================

function initializeClock() {
    const timeElements = document.querySelectorAll('.clock .time, .header-clock .time');
    const dayElements = document.querySelectorAll('.clock .day, .header-clock .day');
    
    if (timeElements.length === 0) return;
    
    const daysOfWeek = [
        "Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"
    ];
    
    function updateClock() {
        const now = new Date();
        let hours = now.getHours();
        const minutes = now.getMinutes();
        const ampm = hours >= 12 ? 'PM' : 'AM';
        
        hours = hours % 12;
        hours = hours ? hours : 12;
        
        const minutesStr = minutes < 10 ? '0' + minutes : minutes;
        const dayIndex = now.getDay();
        const dayName = daysOfWeek[dayIndex];
        
        const timeString = `${hours}:${minutesStr}`;
        const dayString = `${ampm} | ${dayName}`;
        
        timeElements.forEach(element => {
            element.textContent = timeString;
        });
        
        dayElements.forEach(element => {
            element.textContent = dayString;
        });
    }
    
    updateClock();
    setInterval(updateClock, 1000);
}

// =============================================================================
// FUNCIONES DE LA PÁGINA PRINCIPAL
// =============================================================================

function initializeMainPage() {
    // Funcionalidades específicas de la página principal ya están implementadas
    // a través de las funciones globales window.*
}

// Función para mostrar/ocultar formularios
window.showAddForm = function(dayOrSection) {
    const formId = "addForm" + dayOrSection;
    const form = document.getElementById(formId);
    if (form) {
        form.style.display = form.style.display === "none" ? "block" : "none";
    }
};

// Función para agregar una nueva materia
window.addMateria = function(event) {
    event.preventDefault();
    const materiaNameInput = document.getElementById('materiaName');

    if (materiaNameInput) {
        const materiaName = materiaNameInput.value;

        fetch('/add_materia', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: materiaName
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                addMateriaToDOM(data.materia_id, materiaName);
                materiaNameInput.value = '';
                document.getElementById('addFormMaterias').style.display = 'none';
            } else {
                console.error('Error al agregar la materia:', data.message);
            }
        })
        .catch(error => {
            console.error('Error de red:', error);
        });
    }
};

function addMateriaToDOM(materiaId, materiaName) {
    const materiasList = document.getElementById('materiasList');
    if (!materiasList) return;

    const newLi = document.createElement('li');
    newLi.setAttribute('data-materia-id', materiaId);
    newLi.innerHTML = `<a href="/materia/${materiaId}">${materiaName}</a> <button class="delete-button" onclick="deleteMateria(this)">🗑️</button>`;
    materiasList.appendChild(newLi);
}

// Función para eliminar una materia
window.deleteMateria = function(buttonElement) {
    if (confirm('¿Estás seguro de que quieres eliminar esta materia? Se eliminarán también todos los datos asociados.')) {
        const listItem = buttonElement.closest('li');
        const materiaId = listItem.getAttribute('data-materia-id');

        if (!materiaId) return;

        fetch('/delete_materia', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                materia_id: materiaId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                listItem.remove();
            } else {
                alert('Error al eliminar la materia: ' + data.message);
            }
        })
        .catch(error => {
            alert('Error de red al eliminar la materia.');
        });
    }
};

// Funciones para el horario semanal
function addSubjectToDOM(day, time, subject) {
    const ulElement = document.querySelector(`div[data-day="${day.toLowerCase()}"] ul`);
    if (!ulElement) return;

    const newLi = document.createElement('li');
    newLi.setAttribute('data-day', day);
    newLi.setAttribute('data-time', time);
    newLi.innerHTML = `<span class="schedule-time">${time}</span> <span class="schedule-subject" contenteditable="true" onblur="saveSubject(this)">${subject}</span> <button class="delete-button" onclick="deleteSubject(this)">🗑️</button>`;

    // Insertar ordenado por hora
    const items = Array.from(ulElement.children);
    let inserted = false;
    for (let i = 0; i < items.length; i++) {
        const existingTime = items[i].getAttribute('data-time');
        if (time < existingTime) {
            ulElement.insertBefore(newLi, items[i]);
            inserted = true;
            break;
        }
    }

    if (!inserted) {
        ulElement.appendChild(newLi);
    }
}

window.saveSubject = function(element) {
    const listItem = element.closest('li');
    const day = listItem.getAttribute('data-day');
    const time = listItem.getAttribute('data-time');
    const subject = element.textContent;

    fetch('/save_schedule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            day: day,
            time: time,
            subject: subject
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status !== 'success') {
            console.error('Error al guardar la materia:', data.message);
        }
    })
    .catch(error => {
        console.error('Error de red:', error);
    });
};

window.deleteSubject = function(buttonElement) {
    const listItem = buttonElement.closest('li');
    const day = listItem.getAttribute('data-day');
    const time = listItem.getAttribute('data-time');

    fetch('/delete_schedule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            day: day,
            time: time
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            listItem.remove();
        } else {
            console.error('Error al eliminar la materia:', data.message);
        }
    })
    .catch(error => {
        console.error('Error de red:', error);
    });
};

window.addSubject = function(day, event) {
    event.preventDefault();
    const timeInputId = "time" + day;
    const subjectInputId = "subject" + day;
    const timeInput = document.getElementById(timeInputId);
    const subjectInput = document.getElementById(subjectInputId);

    if (timeInput && subjectInput) {
        const time = timeInput.value;
        const subject = subjectInput.value;

        fetch('/add_schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                day: day,
                time: time,
                subject: subject
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                addSubjectToDOM(day, time, subject);
                timeInput.value = '';
                subjectInput.value = '';
                const formId = "addForm" + day;
                const form = document.getElementById(formId);
                if (form) {
                    form.style.display = "none";
                }
            } else {
                console.error('Error al agregar la materia:', data.message);
            }
        })
        .catch(error => {
            console.error('Error de red:', error);
        });
    }
};

// =============================================================================
// FUNCIONES DE LA PÁGINA DE DETALLE DE MATERIA
// =============================================================================

function initializeSubjectDetailPage() {
    // Las funcionalidades específicas ya están implementadas
    // a través de las funciones globales window.*
}

// Función para agregar una nueva tarea
window.addTask = function(event, materiaId) {
    event.preventDefault();
    const descriptionInput = document.getElementById('taskDescription');
    const dueDateInput = document.getElementById('taskDueDate');

    if (descriptionInput) {
        const description = descriptionInput.value;
        const dueDate = dueDateInput.value || null;

        fetch('/add_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                materia_id: materiaId,
                description: description,
                due_date: dueDate
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                addTaskToDOM(data.task_id, description, dueDate, false);
                descriptionInput.value = '';
                dueDateInput.value = '';
                document.getElementById('addFormTask').style.display = 'none';
            } else {
                console.error('Error al agregar la tarea:', data.message);
            }
        })
        .catch(error => {
            console.error('Error de red:', error);
        });
    }
};

function addTaskToDOM(taskId, description, dueDate, completed) {
    const tasksList = document.getElementById('tasksList');
    if (!tasksList) return;

    const newLi = document.createElement('li');
    newLi.setAttribute('data-task-id', taskId);
    const dueDateFormatted = dueDate ? ` (Fecha límite: ${dueDate})` : '';
    const completedStatus = completed ? ' ✅' : '';
    newLi.innerHTML = `${description}${dueDateFormatted}${completedStatus} <button class="delete-button" onclick="deleteTask(this)">🗑️</button>`;
    tasksList.appendChild(newLi);
}

window.deleteTask = function(buttonElement) {
    if (confirm('¿Estás seguro de que quieres eliminar esta tarea?')) {
        const listItem = buttonElement.closest('li');
        const taskId = listItem.getAttribute('data-task-id');

        if (!taskId) return;

        fetch('/delete_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                task_id: taskId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                listItem.remove();
            } else {
                alert('Error al eliminar la tarea: ' + data.message);
            }
        })
        .catch(error => {
            alert('Error de red al eliminar la tarea.');
        });
    }
};

// Función para agregar un nuevo examen
window.addExam = function(event, materiaId) {
    event.preventDefault();
    const topicInput = document.getElementById('examTopic');
    const examDateInput = document.getElementById('examDate');
    const examGradeInput = document.getElementById('examGrade');

    if (topicInput) {
        const topic = topicInput.value;
        const examDate = examDateInput.value || null;
        const grade = examGradeInput.value || null;

        fetch('/add_exam', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                materia_id: materiaId,
                topic: topic,
                exam_date: examDate,
                grade: grade
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                addExamToDOM(data.exam_id, topic, examDate, grade);
                topicInput.value = '';
                examDateInput.value = '';
                examGradeInput.value = '';
                document.getElementById('addFormExam').style.display = 'none';
            } else {
                console.error('Error al agregar el examen:', data.message);
            }
        })
        .catch(error => {
            console.error('Error de red:', error);
        });
    }
};

function addExamToDOM(examId, topic, examDate, grade) {
    const examsList = document.getElementById('examsList');
    if (!examsList) return;

    const newLi = document.createElement('li');
    newLi.setAttribute('data-exam-id', examId);
    const examDateFormatted = examDate ? ` (Fecha: ${examDate})` : '';
    const gradeDisplay = grade !== null ? ` Nota: ${grade}` : ' Nota: N/A';
    newLi.innerHTML = `${topic}${examDateFormatted}${gradeDisplay} <button class="delete-button" onclick="deleteExam(this)">🗑️</button>`;
    examsList.appendChild(newLi);
}

window.deleteExam = function(buttonElement) {
    if (confirm('¿Estás seguro de que quieres eliminar este examen?')) {
        const listItem = buttonElement.closest('li');
        const examId = listItem.getAttribute('data-exam-id');

        if (!examId) return;

        fetch('/delete_exam', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                exam_id: examId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                listItem.remove();
            } else {
                alert('Error al eliminar el examen: ' + data.message);
            }
        })
        .catch(error => {
            alert('Error de red al eliminar el examen.');
        });
    }
};

// Función para agregar una nueva nota
window.addNote = function(event, materiaId) {
    event.preventDefault();
    const contentInput = document.getElementById('noteContent');

    if (contentInput) {
        const content = contentInput.value;

        fetch('/add_note', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                materia_id: materiaId,
                content: content
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                addNoteToDOM(data.note_id, content, data.created_at);
                contentInput.value = '';
                document.getElementById('addFormNote').style.display = 'none';
            } else {
                console.error('Error al agregar la nota:', data.message);
            }
        })
        .catch(error => {
            console.error('Error de red:', error);
        });
    }
};

function addNoteToDOM(noteId, content, createdAt) {
    const notesList = document.getElementById('notesList');
    if (!notesList) return;

    const newLi = document.createElement('li');
    newLi.setAttribute('data-note-id', noteId);
    newLi.innerHTML = `${content}<br><small>Creado: ${createdAt}</small> <button class="delete-button" onclick="deleteNote(this)">🗑️</button>`;
    notesList.appendChild(newLi);
}

window.deleteNote = function(buttonElement) {
    if (confirm('¿Estás seguro de que quieres eliminar esta nota?')) {
        const listItem = buttonElement.closest('li');
        const noteId = listItem.getAttribute('data-note-id');

        if (!noteId) return;

        fetch('/delete_note', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                note_id: noteId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                listItem.remove();
            } else {
                alert('Error al eliminar la nota: ' + data.message);
            }
        })
        .catch(error => {
            alert('Error de red al eliminar la nota.');
        });
    }
};
