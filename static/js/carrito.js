document.addEventListener('DOMContentLoaded', function() {
    // Función para verificar sesión
    function checkSession() {
        return fetch('/carrito/check-session')
            .then(response => response.json())
            .then(data => data.isLoggedIn)
            .catch(error => {
                console.error('Error:', error);
                return false;
            });
    }

    // Función para mostrar alerta personalizada
    function showCustomAlert(message, isError = false) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `custom-alert ${isError ? 'error' : ''}`;
        alertDiv.innerHTML = `
            <div>
                <i class="fas ${isError ? 'fa-exclamation-circle' : 'fa-check-circle'}"></i>
                ${message}
            </div>
            <button class="custom-alert-close">&times;</button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Cerrar al hacer click en la X
        alertDiv.querySelector('.custom-alert-close').addEventListener('click', () => {
            alertDiv.style.animation = 'fadeOut 0.5s forwards';
            setTimeout(() => alertDiv.remove(), 500);
        });
        
        // Eliminar la alerta después de 5 segundos (5000 ms) en lugar de 3
        setTimeout(() => {
            alertDiv.style.animation = 'fadeOut 0.5s forwards';
            setTimeout(() => alertDiv.remove(), 500);
        }, 5000); // Cambiado de 3000 a 5000
    }

    // Manejar clic en botones de añadir al carrito
    document.querySelectorAll('.btn-add-to-cart').forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            
            const isLoggedIn = await checkSession();
            
            if (!isLoggedIn) {
                showCustomAlert('Debes iniciar sesión para agregar productos al carrito', true);
                setTimeout(() => {
                    window.location.href = '/login';
                }, 3000); 
                return;
            }
            
            const productCard = this.closest('.product-card');
            const productName = productCard.querySelector('h3').textContent;
            const selectedOption = productCard.querySelector('.presentation-select').options[
                productCard.querySelector('.presentation-select').selectedIndex
            ];
            const [presentation, price] = selectedOption.text.split(' - ');
            
            showCustomAlert(`${productName} (${presentation}) añadido al carrito`);
            
            const cartCount = document.querySelector('.content-shopping-cart .number');
            const currentCount = parseInt(cartCount.textContent.match(/\d+/)[0]) || 0;
            cartCount.textContent = `(${currentCount + 1})`;
        });
    });
});