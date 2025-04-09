document.addEventListener("DOMContentLoaded", function() {
    // Control del menú desplegable del usuario
    const dropdown = document.getElementById("userDropdown");
    let dropdownTimeout;
    
    if (dropdown) {
        const dropdownContent = dropdown.querySelector(".dropdown-content");
        
        // Asegurarse que el menú esté oculto inicialmente
        dropdownContent.style.display = "none";
        
        dropdown.addEventListener("mouseenter", () => {
            clearTimeout(dropdownTimeout);
            dropdownContent.style.display = "block";
        });
        
        dropdown.addEventListener("mouseleave", () => {
            dropdownTimeout = setTimeout(() => {
                dropdownContent.style.display = "none";
            }, 300); // 300ms de espera antes de cerrarse
        });
        
        // Evitar que se cierre cuando el mouse está sobre el menú
        dropdownContent.addEventListener("mouseenter", () => {
            clearTimeout(dropdownTimeout);
        });
        
        dropdownContent.addEventListener("mouseleave", () => {
            dropdownContent.style.display = "none";
        });
    }

    // Función para actualizar el contador del carrito
    async function updateCartCounter() {
        try {
            const response = await fetch('/carrito/carrito-count');
            if (response.ok) {
                const data = await response.json();
                document.querySelectorAll('.number').forEach(el => {
                    el.textContent = `(${data.count || 0})`;
                });
            }
        } catch (error) {
            console.error('Error al actualizar contador:', error);
        }
    }

    // Actualizar el contador al cargar la página
    updateCartCounter();

    // Opcional: Actualizar periódicamente (cada 30 segundos)
    setInterval(updateCartCounter, 30000);
});