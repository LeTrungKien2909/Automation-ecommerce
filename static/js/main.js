/* AutoTech Main JavaScript */

document.addEventListener('DOMContentLoaded', function () {
    // Auto-hide messages after 5 seconds
    autoHideMessages();

    // Confirm before removing cart item
    setupCartRemoveConfirm();

    // Form validation feedback
    setupFormValidation();
});

/**
 * Auto-hide Bootstrap alerts after 5 seconds
 */
function autoHideMessages() {
    const alerts = document.querySelectorAll('.auto-dismiss');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });
}

/**
 * Confirm dialog before removing item from cart
 */
function setupCartRemoveConfirm() {
    // Called via onsubmit="return confirmRemove(event)"
}

function confirmRemove(event) {
    const confirmed = window.confirm('Bạn có chắc muốn xóa sản phẩm này khỏi giỏ hàng?');
    if (!confirmed) {
        event.preventDefault();
        return false;
    }
    return true;
}

/**
 * Change main product image when clicking thumbnail
 */
function changeMainImage(src) {
    const mainImg = document.getElementById('mainImage');
    if (mainImg) {
        mainImg.src = src;
        // Highlight selected thumbnail
        document.querySelectorAll('.thumbnail-img').forEach(function (img) {
            img.style.borderColor = img.src === src ? '#1a56db' : '';
            img.style.borderWidth = img.src === src ? '2px' : '';
        });
    }
}

/**
 * Adjust quantity input for product detail page
 */
function adjustQty(delta) {
    const input = document.getElementById('qtyInput');
    if (!input) return;
    const current = parseInt(input.value, 10) || 1;
    const max = parseInt(input.max, 10) || 9999;
    const newVal = current + delta;
    if (newVal >= 1 && newVal <= max) {
        input.value = newVal;
    }
}

/**
 * Bootstrap form validation styling
 */
function setupFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * AJAX cart quantity update
 */
function updateCartItemAjax(itemId, quantity, csrfToken) {
    const formData = new FormData();
    formData.append('item_id', itemId);
    formData.append('quantity', quantity);
    formData.append('csrfmiddlewaretoken', csrfToken);

    fetch('/orders/update/', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: formData,
    })
        .then(function (response) {
            if (!response.ok) throw new Error('Network error');
            return response.json();
        })
        .then(function (data) {
            if (data.success) {
                // Update total display if present
                const totalEl = document.getElementById('cartTotal');
                if (totalEl && data.total) {
                    totalEl.textContent = parseInt(data.total, 10).toLocaleString('vi-VN') + ' ₫';
                }
            }
        })
        .catch(function (err) {
            console.error('Cart update failed:', err);
        });
}
