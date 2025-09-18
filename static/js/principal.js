// Funcionalidad del reloj
function updateClock() {
    const now = new Date();
    
    // Obtener elementos del reloj
    const timeText = document.querySelector('.hora-texto');
    const dayText = document.querySelector('.dia-texto');
    
    // Formatear hora y fecha
    let hours = now.getHours();
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const ampm = hours >= 12 ? 'PM' : 'AM';
    
    hours = hours % 12;
    hours = hours ? hours : 12; // Si es 0, mostrar 12
    const timeString = `${hours}:${minutes}`;
    
    // Actualizar elementos
    timeText.innerHTML = `<span>${timeString}</span><span class="sub-texto-hora">${ampm}</span>`;
    
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    dayText.textContent = now.toLocaleDateString('en-US', options);
}

// Actualizar cada segundo
setInterval(updateClock, 1000);
updateClock(); // Ejecutar inmediatamente al cargar

// Funcionalidad de los iconos
document.addEventListener('DOMContentLoaded', () => {
    const iconLinks = document.querySelectorAll('.enlace-icono');

    iconLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            // Si el enlace es el icono de usuario, permite la navegación
            const img = link.querySelector('img');
            if (img && img.alt === 'Usuario') {
                return;
            }
            // Sólo prevenir la acción por defecto si el enlace es un placeholder (ej. href="#")
            const href = link.getAttribute('href');
            const isPlaceholder = !href || href === '#' || href.trim() === '' || href.startsWith('javascript:');
            if (isPlaceholder) e.preventDefault();
            // Eliminar la clase activa de todos los enlaces
            iconLinks.forEach(item => {
                item.classList.remove('icono-activo');
            });
            // Añadir la clase activa al enlace clicado
            link.classList.add('icono-activo');
        });
    });
});