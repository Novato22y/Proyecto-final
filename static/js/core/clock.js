// core/clock.js
export function initializeClock() {
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
