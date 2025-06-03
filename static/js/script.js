document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Añadir efecto de scroll al cargar la página
window.addEventListener('load', () => {
    const hash = window.location.hash;
    if (hash) {
        document.querySelector(hash).scrollIntoView({ behavior: 'smooth' });
    }
    generateCalendar();
});

function generateCalendar() {
    const calendar = document.getElementById('calendar');
    calendar.innerHTML = ''; // Limpiar contenido previo

    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();

    // Crear tabla
    const table = document.createElement('table');
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');

    // Encabezados de la semana
    const days = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
    const headerRow = document.createElement('tr');
    days.forEach(day => {
        const th = document.createElement('th');
        th.textContent = day;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    // Calcular el primer día de la semana
    let startDay = firstDay.getDay();
    let dayCount = 1;

    // Generar filas de la tabla
    for (let i = 0; i < 6; i++) {
        const row = document.createElement('tr');
        for (let j = 0; j < 7; j++) {
            const cell = document.createElement('td');
            if (i === 0 && j < startDay) {
                // Espacio vacío antes del primer día
            } else if (dayCount <= daysInMonth) {
                const date = new Date(year, month, dayCount);
                cell.textContent = dayCount;
                if (date.getDay() === 0) {
                    cell.classList.add('sunday'); // Marcar domingos
                }
                cell.addEventListener('click', () => {
                    document.querySelectorAll('.selected').forEach(el => el.classList.remove('selected'));
                    cell.classList.add('selected');
                    const fecha = `${year}-${String(month + 1).padStart(2, '0')}-${String(dayCount).padStart(2, '0')}`;
                    document.getElementById('fecha_cita').value = fecha;
                });
                dayCount++;
            }
            row.appendChild(cell);
        }
        tbody.appendChild(row);
        if (dayCount > daysInMonth) break;
    }

    table.appendChild(thead);
    table.appendChild(tbody);
    calendar.appendChild(table);
}