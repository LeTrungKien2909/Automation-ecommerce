/* AutomationPro - Main JavaScript */

document.addEventListener('DOMContentLoaded', function () {

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });

    // Product grid / list view toggle
    const gridViewBtn = document.getElementById('gridView');
    const listViewBtn = document.getElementById('listView');
    const productGrid = document.getElementById('productGrid');

    if (gridViewBtn && listViewBtn && productGrid) {
        gridViewBtn.addEventListener('click', function () {
            productGrid.querySelectorAll('.product-item').forEach(function (item) {
                item.className = 'col-sm-6 col-xl-4 product-item';
            });
            gridViewBtn.classList.add('active');
            listViewBtn.classList.remove('active');
            localStorage.setItem('viewMode', 'grid');
        });

        listViewBtn.addEventListener('click', function () {
            productGrid.querySelectorAll('.product-item').forEach(function (item) {
                item.className = 'col-12 product-item';
            });
            listViewBtn.classList.add('active');
            gridViewBtn.classList.remove('active');
            localStorage.setItem('viewMode', 'list');
        });

        // Restore view mode
        const savedMode = localStorage.getItem('viewMode');
        if (savedMode === 'list' && listViewBtn) {
            listViewBtn.click();
        }
    }

    // Quantity input: prevent values below 0
    document.querySelectorAll('input[type="number"][name="quantity"]').forEach(function (input) {
        input.addEventListener('change', function () {
            if (parseInt(this.value) < 0) this.value = 0;
        });
    });

    // Confirm before removing cart items (handled via onclick in template)

    // Tooltip initialization (Bootstrap)
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (el) {
        new bootstrap.Tooltip(el);
    });

    // Add to cart button loading state
    document.querySelectorAll('a[href*="add_to_cart"]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const icon = btn.querySelector('i');
            if (icon) {
                icon.className = 'bi bi-hourglass-split';
                btn.style.pointerEvents = 'none';
            }
        });
    });

    // Highlight active nav link
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(function (link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});
