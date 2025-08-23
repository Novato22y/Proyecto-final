// @ts-nocheck
console.log("Script cargado correctamente."); // Agregado para verificar si el script se carga
// Espera a que todo el contenido del HTML esté cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', () => {

    // Selecciona los elementos del DOM donde se mostrará la hora y el día (para index.html)
    const timeElement = document.querySelector('.clock .time');
    const dayElement = document.querySelector('.clock .day');

    // Array con los nombres de los días de la semana en español
    const daysOfWeek = [
    "Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"
    ];

    // Función para actualizar el reloj (para index.html)
    function updateClock() {
      // Obtiene la fecha y hora actual
    const now = new Date();

      // Obtiene las horas, minutos y segundos
    let hours = now.getHours();
    const minutes = now.getMinutes();
      // const seconds = now.getSeconds(); // Descomentar si quieres mostrar segundos

      // Determina si es AM o PM
    const ampm = hours >= 12 ? 'PM' : 'AM';

      // Convierte la hora al formato de 12 horas
    hours = hours % 12;
      hours = hours ? hours : 12; // La hora '0' debe ser '12'

      // Formatea los minutos para que siempre tengan dos dígitos (ej: 05 en lugar de 5)
    const minutesStr = minutes < 10 ? '0' + minutes : minutes;
      // const secondsStr = seconds < 10 ? '0' + seconds : seconds; // Para segundos

      // Obtiene el día de la semana (0 para Domingo, 1 para Lunes, etc.)
    const dayIndex = now.getDay();
      const dayName = daysOfWeek[dayIndex]; // Obtiene el nombre del día en español

      // Construye la cadena de texto para la hora (HH:MM)
    const timeString = `${hours}:${minutesStr}`;
      // const timeString = `${hours}:${minutesStr}:${secondsStr}`; // Incluyendo segundos

      // Construye la cadena de texto para el día (AM/PM | NombreDia)
    const dayString = `${ampm} | ${dayName}`;

      // Actualiza el contenido de los elementos HTML
    if (timeElement) {
        timeElement.textContent = timeString;
    }
    if (dayElement) {
        dayElement.textContent = dayString;
    }
    }

    // Llama a updateClock inmediatamente para mostrar la hora al cargar la página
    // Asegúrate de que solo se ejecute en la página principal
    if (document.querySelector('.clock-panel')) { // Comprobar si estamos en la página principal
        updateClock();
        // Establece un intervalo para llamar a updateClock cada segundo (1000 milisegundos)
        // Esto mantiene el reloj actualizado
        setInterval(updateClock, 1000);
    }

});

// Función para mostrar el formulario de agregar (reutilizada para días y materias)
window.showAddForm = function(dayOrSection) {
    const formId = "addForm" + dayOrSection;
    const form = document.getElementById(formId);
    if (form) {
        form.style.display = form.style.display === "none" ? "block" : "none";
    }
};

// =============================================================================
// Funciones específicas de la página principal (index.html)
// =============================================================================

// Función para agregar una nueva materia (llamada desde el formulario de Materias)
window.addMateria = function(event) {
    console.log('addMateria called');
    event.preventDefault(); // Evita que el formulario se envíe de forma predeterminada
    const materiaNameInput = document.getElementById('materiaName');

    if (materiaNameInput) {
        const materiaName = materiaNameInput.value;

        fetch('/add_materia', { // Ruta para agregar materia
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
                console.log('Materia agregada correctamente en el servidor.');
                // Agregar la nueva materia al DOM
                addMateriaToDOM(data.materia_id, materiaName); // Asumiendo que el backend devuelve el ID
                // Limpiar el campo del formulario
                materiaNameInput.value = '';
                // Ocultar el formulario
                document.getElementById('addFormMaterias').style.display = 'none';
            } else {
                console.error('Error al agregar la materia en el servidor:', data.message);
            }
        })
        .catch(error => {
            console.error('Error de red o del servidor al agregar la materia:', error);
        });
    }
};

// Función para agregar una nueva materia al DOM
function addMateriaToDOM(materiaId, materiaName) {
    console.log('addMateriaToDOM called for ID:', materiaId, 'Name:', materiaName);
    const materiasList = document.getElementById('materiasList');
    if (!materiasList) {
        console.error('No se encontró la lista UL para Materias');
        return;
    }

    // Crear el nuevo elemento li
    const newLi = document.createElement('li');
    newLi.setAttribute('data-materia-id', materiaId);
    newLi.innerHTML = `<a href="/materia/${materiaId}">${materiaName}</a> <button class="delete-button" onclick="deleteMateria(this)">🗑️</button>`;

    // Agregar el nuevo elemento a la lista
    materiasList.appendChild(newLi);
}

// Función para eliminar una materia (llamada desde el botón en el li)
window.deleteMateria = function(buttonElement) {
    console.log('deleteMateria called');
    // Mostrar mensaje de confirmación
    if (confirm('¿Estás seguro de que quieres eliminar esta materia? Se eliminarán también todos los datos asociados (tareas, exámenes, notas).')) {
        // Obtener el ID de la materia del atributo data-materia-id del elemento li padre
        const listItem = buttonElement.closest('li');
        const materiaId = listItem.getAttribute('data-materia-id');

        if (!materiaId) {
            console.error('No se encontró el ID de la materia en el elemento li.');
            return;
        }

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
                console.log('Materia eliminada correctamente del servidor.');
                // Eliminar el elemento de la lista del DOM
                listItem.remove();
            } else {
                console.error('Error al eliminar la materia en el servidor:', data.message);
                alert('Error al eliminar la materia: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error de red o del servidor al eliminar la materia:', error);
            alert('Error de red o del servidor al eliminar la materia.');
        });
    }
};

// Funciones originales para el horario semanal

// Función para agregar una nueva materia al DOM y mantener el orden
  function addSubjectToDOM(day, time, subject) {
      console.log('addSubjectToDOM called for day:', day, 'time:', time, 'subject:', subject); // Log 4
      // const ulElement = document.querySelector(`.day-card:has(h3:contains('${day}')) ul`); // Selector anterior problemático
      const ulElement = document.querySelector(`div[data-day="${day.toLowerCase()}"] ul`); // Nuevo selector
      if (!ulElement) {
          console.error(`No se encontró la lista UL para el día ${day}`); // Log 5 (Error case)
          return;
      } else {
          console.log('UL element found:', ulElement); // Log 5 (Success case)
      }

      // Crear el nuevo elemento li
      const newLi = document.createElement('li');
      newLi.setAttribute('data-day', day);
      newLi.setAttribute('data-time', time);
      newLi.innerHTML = `<span class=\"schedule-time\">${time}</span> <span class=\"schedule-subject\" contenteditable=\"true\" onblur=\"saveSubject(this)\">${subject}</span> <button class=\"delete-button\" onclick=\"deleteSubject(this)\">🗑️</button>`; // Usando variables JS time y subject

      // Encontrar la posición correcta para insertar el nuevo elemento (ordenado por hora)
      const items = Array.from(ulElement.children);
      let inserted = false;
      for (let i = 0; i < items.length; i++) {
          const existingTime = items[i].getAttribute('data-time');
          console.log('Comparando nuevo tiempo', time, 'con tiempo existente', existingTime); // Log 7
          if (time < existingTime) {
              ulElement.insertBefore(newLi, items[i]);
              inserted = true;
              console.log('Insertado antes de:', items[i]); // Log 7 (Insertion)
              break;
          }
      }

      // Si no se insertó (es la hora más tardía o la lista está vacía), agregarlo al final
      if (!inserted) {
          ulElement.appendChild(newLi);
          console.log('Agregado al final:', newLi); // Log 7 (Append)
      }
  }

// Función para guardar la materia en la base de datos
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
          if (data.status === 'success') {
              console.log('Materia guardada correctamente.');
          } else {
              console.error('Error al guardar la materia:', data.message);
          }
      })
      .catch(error => {
          console.error('Error de red:', error);
      });
  };


// Función para eliminar una materia del horario
  window.deleteSubject = function(buttonElement) {
      // Obtener el ID del día y la hora del atributo data-*
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
              console.log('Materia eliminada correctamente.');
              // Encontrar y eliminar el elemento de la lista del DOM
              listItem.remove();
          } else {
              console.error('Error al eliminar la materia:', data.message);
          }
      })
      .catch(error => {
          console.error('Error de red:', error);
      });
  };

// Funciones originales para agregar schedule - pueden ser innecesarias si addSubjectToDOM es llamada por save_schedule_route
window.addSubject = function(day, event) {
    console.log('addSubject called for day:', day); // Log 1
    event.preventDefault(); // Evita que el formulario se envíe de forma predeterminada
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
                console.log('Materia agregada correctamente en el servidor.'); // Log 2
                // Agregar la nueva materia al DOM y reordenar
                addSubjectToDOM(day, time, subject); // Llama a la función para actualizar el DOM
                // Limpiar los campos del formulario
                timeInput.value = '';
                subjectInput.value = '';
                // Ocultar el formulario después de agregar la materia
                const formId = "addForm" + day;
                const form = document.getElementById(formId);
                if (form) {
                    form.style.display = "none";
                }
            } else {
                console.error('Error al agregar la materia en el servidor:', data.message); // Log 3
            }
        })
        .catch(error => {
            console.error('Error de red o del servidor al agregar la materia:', error); // Log 3
        });
    }
};


// =============================================================================
// Funciones específicas de la página de detalle de Materia (subject_detail.html)
// =============================================================================

// Función para agregar una nueva Tarea
window.addTask = function(event, materiaId) {
    console.log('addTask called for materiaId:', materiaId);
    event.preventDefault();
    const descriptionInput = document.getElementById('taskDescription');
    const dueDateInput = document.getElementById('taskDueDate');

    if (descriptionInput) {
        const description = descriptionInput.value;
        const dueDate = dueDateInput.value || null; // Usar null si la fecha está vacía

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
                console.log('Tarea agregada correctamente en el servidor.');
                addTaskToDOM(data.task_id, description, dueDate, false); // false para completed
                descriptionInput.value = '';
                dueDateInput.value = '';
                document.getElementById('addFormTask').style.display = 'none';
            } else {
                console.error('Error al agregar la tarea:', data.message);
            }
        })
        .catch(error => {
            console.error('Error de red o del servidor al agregar la tarea:', error);
        });
    }
};

// Función para agregar una Tarea al DOM
function addTaskToDOM(taskId, description, dueDate, completed) {
    console.log('addTaskToDOM called for ID:', taskId, 'Description:', description);
    const tasksList = document.getElementById('tasksList');
    if (!tasksList) {
        console.error('No se encontró la lista UL para Tareas');
        return;
    }

    const newLi = document.createElement('li');
    newLi.setAttribute('data-task-id', taskId);
    // Formatear la fecha si existe
    const dueDateFormatted = dueDate ? ` (Fecha límite: ${dueDate})` : '';
    const completedStatus = completed ? ' ✅' : '';
    newLi.innerHTML = `${description}${dueDateFormatted}${completedStatus} <button class="delete-button" onclick="deleteTask(this)">🗑️</button>`;

    tasksList.appendChild(newLi);
}

// Función para eliminar una Tarea
window.deleteTask = function(buttonElement) {
    console.log('deleteTask called');
    if (confirm('¿Estás seguro de que quieres eliminar esta tarea?')) {
        const listItem = buttonElement.closest('li');
        const taskId = listItem.getAttribute('data-task-id');

        if (!taskId) {
             console.error('No se encontró el ID de la tarea en el elemento li.');
            return;
        }

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
                console.log('Tarea eliminada correctamente del servidor.');
                listItem.remove();
            } else {
                console.error('Error al eliminar la tarea:', data.message);
                alert('Error al eliminar la tarea: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error de red o del servidor al eliminar la tarea:', error);
            alert('Error de red o del servidor al eliminar la tarea.');
        });
    }
};

// Función para agregar un nuevo Examen
window.addExam = function(event, materiaId) {
    console.log('addExam called for materiaId:', materiaId);
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
                console.log('Examen agregado correctamente en el servidor.');
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
            console.error('Error de red o del servidor al agregar el examen:', error);
        });
    }
};

// Función para agregar un Examen al DOM
function addExamToDOM(examId, topic, examDate, grade) {
    console.log('addExamToDOM called for ID:', examId, 'Topic:', topic);
    const examsList = document.getElementById('examsList');
    if (!examsList) {
        console.error('No se encontró la lista UL para Exámenes');
        return;
    }

    const newLi = document.createElement('li');
    newLi.setAttribute('data-exam-id', examId);
    const examDateFormatted = examDate ? ` (Fecha: ${examDate})` : '';
    const gradeDisplay = grade !== null ? ` Nota: ${grade}` : ' Nota: N/A';
    newLi.innerHTML = `${topic}${examDateFormatted}${gradeDisplay} <button class="delete-button" onclick="deleteExam(this)">🗑️</button>`;

    examsList.appendChild(newLi);
}

// Función para eliminar un Examen
window.deleteExam = function(buttonElement) {
    console.log('deleteExam called');
    if (confirm('¿Estás seguro de que quieres eliminar este examen?')) {
        const listItem = buttonElement.closest('li');
        const examId = listItem.getAttribute('data-exam-id');

         if (!examId) {
             console.error('No se encontró el ID del examen en el elemento li.');
            return;
        }

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
                console.log('Examen eliminado correctamente del servidor.');
                listItem.remove();
            } else {
                console.error('Error al eliminar el examen:', data.message);
                alert('Error al eliminar el examen: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error de red o del servidor al eliminar el examen:', error);
            alert('Error de red o del servidor al eliminar el examen.');
        });
    }
};

// Función para agregar una nueva Nota
window.addNote = function(event, materiaId) {
    console.log('addNote called for materiaId:', materiaId);
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
                console.log('Nota agregada correctamente en el servidor.');
                // Pasar la fecha de creación devuelta por el backend
                addNoteToDOM(data.note_id, content, data.created_at);
                contentInput.value = '';
                document.getElementById('addFormNote').style.display = 'none';
            } else {
                console.error('Error al agregar la nota:', data.message);
            }
        })
        .catch(error => {
            console.error('Error de red o del servidor al agregar la nota:', error);
        });
    }
};

// Función para agregar una Nota al DOM
function addNoteToDOM(noteId, content, createdAt) {
    console.log('addNoteToDOM called for ID:', noteId);
    const notesList = document.getElementById('notesList');
    if (!notesList) {
        console.error('No se encontró la lista UL para Notas');
        return;
    }

    const newLi = document.createElement('li');
    newLi.setAttribute('data-note-id', noteId);
    // Mostrar el contenido y la fecha de creación
    newLi.innerHTML = `${content}<br><small>Creado: ${createdAt}</small> <button class="delete-button" onclick="deleteNote(this)">🗑️</button>`;

    notesList.appendChild(newLi);
}

// Función para eliminar una Nota
window.deleteNote = function(buttonElement) {
    console.log('deleteNote called for ID:', buttonElement.closest('li').getAttribute('data-note-id'));
    if (confirm('¿Estás seguro de que quieres eliminar esta nota?')) {
        const listItem = buttonElement.closest('li');
        const noteId = listItem.getAttribute('data-note-id');

        if (!noteId) {
             console.error('No se encontró el ID de la nota en el elemento li.');
            return;
        }

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
                console.log('Nota eliminada correctamente del servidor.');
                listItem.remove();
            } else {
                console.error('Error al eliminar la nota:', data.message);
                alert('Error al eliminar la nota: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error de red o del servidor al eliminar la nota:', error);
            alert('Error de red o del servidor al eliminar la nota.');
        });
    }
};

// Función para actualizar el reloj en la página de detalle
function updateClockSubjectDetail() {
    const timeElement = document.querySelector('.header-clock .time');
    const dayElement = document.querySelector('.header-clock .day');
    const daysOfWeek = [
        "Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"
    ];

    const now = new Date();
    let hours = now.getHours();
    const minutes = now.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // La hora '0' debe ser '12'
    const minutesStr = minutes < 10 ? '0' + minutes : minutes;
    const dayIndex = now.getDay();
    const dayName = daysOfWeek[dayIndex];

    const timeString = `${hours}:${minutesStr}`;
    const dayString = `${ampm} | ${dayName}`;

    if (timeElement) {
        timeElement.textContent = timeString;
    }
    if (dayElement) {
        dayElement.textContent = dayString;
    }
}

// Llama a updateClockSubjectDetail al cargar la página de detalle
// y establece un intervalo para actualizarlo
// Asegúrate de que esta parte solo se ejecute en la página de detalle
if (document.querySelector('.subject-details')) { // Comprobar si estamos en la página de detalle
    updateClockSubjectDetail();
    setInterval(updateClockSubjectDetail, 1000);
}
