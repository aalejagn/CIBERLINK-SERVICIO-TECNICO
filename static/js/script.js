document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

window.addEventListener('load', () => {
    const hash = window.location.hash;
    if (hash) {
        document.querySelector(hash).scrollIntoView({ behavior: 'smooth' });
    }
    initializeCalendar();
});

function initializeCalendar() {
    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth', // Vista de mes por defecto
        selectable: true, // Permitir selección de fechas
        selectAllow: function(info) {
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            const selectedDate = new Date(info.startStr);
            const day = selectedDate.getDay();
            return selectedDate >= today && day !== 0; // No permitir días pasados ni domingos
        },
        dateClick: function(info) {
            const fecha = info.dateStr;
            document.getElementById('fecha_cita').value = fecha;
            // Opcional: Resaltar visualmente el día seleccionado
            calendar.gotoDate(fecha);
        },
        events: function(fetchInfo, successCallback, failureCallback) {
            fetch('/api/citas')
                .then(response => response.json())
                .then(data => {
                    const events = data.map(cita => ({
                        title: 'Cita(s): ' + cita.citas_count,
                        start: cita.fecha_cita,
                        backgroundColor: cita.citas_count >= 5 ? '#ff0000' : '#00ff00', // Rojo si >= 5 citas, verde si no
                        borderColor: cita.citas_count >= 5 ? '#ff0000' : '#00ff00',
                        textColor: '#1a1a1a'
                    }));
                    successCallback(events);
                })
                .catch(error => {
                    console.error('Error al cargar citas:', error);
                    failureCallback(error);
                });
        },
        dayCellClassNames: function(arg) {
            if (arg.date.getDay() === 0) {
                return ['sunday']; // Marcar domingos
            }
            return [];
        }
    });
    calendar.render();
}