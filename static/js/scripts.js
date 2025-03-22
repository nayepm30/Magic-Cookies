document.addEventListener('DOMContentLoaded', function () {
    // Variables del primer script
    const container = document.getElementById('container');
    const registerBtn = document.getElementById('register');
    const loginBtn = document.getElementById('login');

    // Variables del segundo script
    const menusItemsDropDown = document.querySelectorAll('.menu-item-dropdown');
    const menusItemsStatic = document.querySelectorAll('.menu-item-static');
    const sidebar = document.getElementById('sidebar');
    const menuBtn = document.getElementById('menu-btn');
    const sidebarBtn = document.getElementById('sidebar-btn');

    // Funcionalidad del primer script (login/register)
    if (registerBtn && loginBtn) {
        registerBtn.addEventListener('click', () => {
            container.classList.add('active');
        });

        loginBtn.addEventListener('click', () => {
            container.classList.remove('active');
        });
    }

    // Funcionalidad del segundo script (sidebar y menús desplegables)
    if (sidebarBtn) {
        sidebarBtn.addEventListener('click', () => {
            document.body.classList.toggle('sidebar-hidden');
        });
    }

    if (menuBtn) {
        menuBtn.addEventListener('click', () => {
            sidebar.classList.toggle('minimize');
        });
    }

    menusItemsDropDown.forEach((menuItem) => {
        menuItem.addEventListener('click', () => {
            const subMenu = menuItem.querySelector('.sub-menu');
            const isActive = menuItem.classList.toggle('sub-menu-toggle');
            if (subMenu) {
                if (isActive) {
                    subMenu.style.height = `${subMenu.scrollHeight + 6}px`;
                    subMenu.style.padding = '0.2rem 0';
                } else {
                    subMenu.style.height = '0';
                    subMenu.style.padding = '0';
                }
            }
            menusItemsDropDown.forEach((item) => {
                if (item !== menuItem) {
                    const otherSubMenu = item.querySelector('.sub-menu');
                    if (otherSubMenu) {
                        item.classList.remove('sub-menu-toggle');
                        otherSubMenu.style.height = '0';
                        otherSubMenu.style.padding = '0';
                    }
                }
            });
        });
    });

    menusItemsStatic.forEach((menuItem) => {
        menuItem.addEventListener('mouseenter', () => {
            if (!sidebar.classList.contains('minimize')) return;

            menusItemsDropDown.forEach((item) => {
                if (item !== menuItem) {
                    const otherSubMenu = item.querySelector('.sub-menu');
                    if (otherSubMenu) {
                        item.classList.remove('sub-menu-toggle');
                        otherSubMenu.style.height = '0';
                        otherSubMenu.style.padding = '0';
                    }
                }
            });
        });
    });

    // Función para verificar el tamaño de la ventana
    function checkWindowsSize() {
        sidebar.classList.remove('minimize');
    }

    checkWindowsSize();
    window.addEventListener('resize', checkWindowsSize); // Corregí el nombre del evento a 'resize'
});