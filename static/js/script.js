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
});