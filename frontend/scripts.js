document.addEventListener('DOMContentLoaded', () => {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartBadge = document.getElementById('cart-badge');
    const productContainer = document.getElementById('product-container');
    const couponInput = document.getElementById('coupon-input');
    const couponButton = document.getElementById('apply-coupon');
    const cartModal = document.getElementById('cart-modal');
    const closeModalButton = document.getElementById('close-cart-modal');
    const checkoutButton = document.getElementById('checkout-button');

    function updateCartBadge() {
        const totalItems = cart.reduce((acc, item) => acc + item.quantity, 0);
        cartBadge.textContent = totalItems > 0 ? totalItems : '';
    }

    function renderProducts(products) {
        productContainer.innerHTML = '';
        products.forEach(product => {
            const productCard = document.createElement('div');
            productCard.className = 'product-card';
            productCard.innerHTML = `
                <img src="${product.image}" alt="${product.name}">
                <h3>${product.name}</h3>
                <p>Preço: R$ ${product.price.toFixed(2)}</p>
                <p>Estoque: ${product.stock}</p>
                <button class="add-to-cart" data-id="${product.id}" ${product.stock === 0 ? 'disabled' : ''}>Adicionar ao Carrinho</button>
            `;
            productContainer.appendChild(productCard);
        });
    }

    function addToCart(productId) {
        const product = cart.find(item => item.id === productId);
        if (product) {
            product.quantity += 1;
        } else {
            cart.push({ id: productId, quantity: 1 });
        }
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartBadge();
    }

    function openCartModal() {
        cartModal.style.display = 'block';
        renderCartItems();
    }

    function closeCartModal() {
        cartModal.style.display = 'none';
    }

    function renderCartItems() {
        const cartItemsContainer = document.getElementById('cart-items');
        cartItemsContainer.innerHTML = '';
        let subtotal = 0;

        cart.forEach(item => {
            const product = products.find(p => p.id === item.id);
            const itemSubtotal = product.price * item.quantity;
            subtotal += itemSubtotal;

            const cartItem = document.createElement('div');
            cartItem.className = 'cart-item';
            cartItem.innerHTML = `
                <p>${product.name} - R$ ${product.price.toFixed(2)} x ${item.quantity}</p>
                <button class="remove-from-cart" data-id="${item.id}">Remover</button>
            `;
            cartItemsContainer.appendChild(cartItem);
        });

        const subtotalElement = document.getElementById('subtotal');
        subtotalElement.textContent = `Subtotal: R$ ${subtotal.toFixed(2)}`;
    }

    function validateCoupon() {
        const couponCode = couponInput.value;
        const subtotal = parseFloat(document.getElementById('subtotal').textContent.replace('Subtotal: R$ ', '').replace(',', '.'));
        if (couponCode === 'ALUNO10' && subtotal >= 50) {
            const discount = subtotal * 0.10;
            const totalFinal = subtotal - discount;
            alert(`Cupom aplicado! Desconto de R$ ${discount.toFixed(2)}. Total final: R$ ${totalFinal.toFixed(2)}`);
        } else {
            alert('Cupom inválido ou subtotal abaixo de R$ 50,00.');
        }
    }

    productContainer.addEventListener('click', (event) => {
        if (event.target.classList.contains('add-to-cart')) {
            const productId = parseInt(event.target.dataset.id);
            addToCart(productId);
        }
    });

    couponButton.addEventListener('click', validateCoupon);
    closeModalButton.addEventListener('click', closeCartModal);
    checkoutButton.addEventListener('click', openCartModal);
    updateCartBadge();
});