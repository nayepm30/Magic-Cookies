/*
document.addEventListener('DOMContentLoaded', function() {
    // 1. Función para verificar sesión
    async function checkSession() {
        try {
            const response = await fetch('/carrito/check-session');
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error al verificar sesión:', error);
            return { 
                isLoggedIn: false, 
                loginUrl: '/login' 
            };
        }
    }

    // 2. Función para mostrar alertas
    function showCustomAlert(message, isError = false) {
        // Eliminar alertas anteriores para evitar duplicados
        const existingAlerts = document.querySelectorAll('.custom-alert');
        existingAlerts.forEach(alert => alert.remove());

        const alertDiv = document.createElement('div');
        alertDiv.className = `custom-alert ${isError ? 'error' : 'success'}`;
        alertDiv.innerHTML = `
            <div class="alert-content">
                <i class="fas ${isError ? 'fa-exclamation-circle' : 'fa-check-circle'}"></i>
                <span>${message}</span>
            </div>
            <button class="custom-alert-close">&times;</button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Animación de entrada
        alertDiv.style.animation = 'fadeIn 0.3s forwards';
        
        // Cerrar al hacer click
        alertDiv.querySelector('.custom-alert-close').addEventListener('click', () => {
            alertDiv.style.animation = 'fadeOut 0.3s forwards';
            setTimeout(() => alertDiv.remove(), 300);
        });
        
        // Eliminar automáticamente después de 3 segundos
        setTimeout(() => {
            alertDiv.style.animation = 'fadeOut 0.3s forwards';
            setTimeout(() => alertDiv.remove(), 300);
        }, 3000);
    }


    // 3. Manejador para botones "Añadir al carrito"
    function setupAddToCartButtons() {
        document.querySelectorAll('.btn-add-to-cart').forEach(button => {
            button.addEventListener('click', async function(e) {
                e.preventDefault();
                
                // Verificar sesión primero
                const sessionData = await checkSession();
                
                if (!sessionData.isLoggedIn) {
                    showCustomAlert('Debes iniciar sesión para agregar productos. Redirigiendo...', true);
                    setTimeout(() => {
                        window.location.href = sessionData.loginUrl;
                    }, 2000);
                    return;
                }
                
                // Si el usuario está logueado, continuar
                const productCard = this.closest('.product-card');
                const productName = productCard.querySelector('h3').textContent;
                const presentationSelect = productCard.querySelector('.presentation-select');
                const selectedOption = presentationSelect.options[presentationSelect.selectedIndex];
                const [presentation, price] = selectedOption.text.split(' - ');
                
                // Aquí puedes agregar la lógica para enviar al backend
                // const productId = this.dataset.productId; // Necesitarías agregar data attributes
                
                showCustomAlert(`${productName} (${presentation}) añadido al carrito`);
                
                // Actualizar contador del carrito
                updateCartCounter(1);
            });
        });
    }

    // Inicializar todo cuando el DOM esté listo
    setupAddToCartButtons();
});

// En carrito.js
document.addEventListener("DOMContentLoaded", function() {
    // Función para actualizar el contador del carrito en el header
    function updateCartCounter() {
        const carrito = JSON.parse(localStorage.getItem("carrito")) || [];
        const totalItems = carrito.reduce((total, item) => total + item.cantidad, 0);
        document.querySelectorAll(".content-shopping-cart .number").forEach(el => {
            el.textContent = `(${totalItems})`;
        });
    }

    // Manejar el evento de agregar al carrito
    document.querySelectorAll(".btn-add-to-cart").forEach(button => {
        button.addEventListener("click", function() {
            const productCard = button.closest(".product-card");
            const id = productCard.dataset.productId;
            const nombre = productCard.querySelector("h3").textContent;
            const presentacion = productCard.querySelector(".presentation-select").value;
            const cantidad = parseInt(productCard.querySelector(".quantity-input").value);
            const precioUnitario = calcularPrecioUnitario(productCard, presentacion);
            const subtotal = (precioUnitario * cantidad).toFixed(2);
            const imagen = nombre.toLowerCase().replace(/ /g, "_") + ".jpg";

            const carrito = JSON.parse(localStorage.getItem("carrito")) || [];

            // Verificar si ya existe
            const existente = carrito.find(p => p.id === id && p.presentacion === presentacion);
            if (existente) {
                existente.cantidad += cantidad;
                existente.subtotal = (existente.precioUnitario * existente.cantidad).toFixed(2);
            } else {
                carrito.push({ id, nombre, presentacion, cantidad, precioUnitario, subtotal, imagen });
            }

            localStorage.setItem("carrito", JSON.stringify(carrito));
            updateCartCounter();
            alert("Producto añadido al carrito");
        });
    });

    function calcularPrecioUnitario(card, presentacion) {
        const precioBase = parseFloat(card.dataset.precio);
        const pesoBase = parseFloat(card.dataset.peso);
        if (presentacion === "pieza") return precioBase;
        if (presentacion === "700g") return (700 / pesoBase) * precioBase;
        if (presentacion === "1kg") return (1000 / pesoBase) * precioBase;
        return precioBase;
    }

    // Inicializar el contador al cargar la página
    updateCartCounter();
});
*/
