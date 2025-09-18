document.addEventListener("DOMContentLoaded", () => {
  const productContainer = document.getElementById("product-container");
  const cartBadge = document.getElementById("cart-badge");
  const cartModal = document.getElementById("cart-modal");
  const closeModalButton = document.getElementById("close-cart-modal");
  const checkoutButton = document.getElementById("checkout-button");
  const cartItemsContainer = document.getElementById("cart-items");
  const subtotalElement = document.getElementById("subtotal");
  const couponInput = document.getElementById("coupon-input");
  const couponButton = document.getElementById("apply-coupon");
  const productForm = document.getElementById("product-form");
  const searchInput = document.getElementById("search");
  const sortSelect = document.getElementById("sort");

  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  let products = [
    { id: 1, name: "Caderno Universitário", price: 15.90, stock: 10, image: "https://universalpapelaria.com.br/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/w/h/whatsapp_image_2022-10-28_at_10.18.00_1.jpeg" },
    { id: 2, name: "Caneta Azul", price: 2.50, stock: 50, image: "https://images.tcdn.com.br/img/img_prod/1140357/caneta_esferografica_bic_cristal_dura_mais_azul_ponta_media_de_1_0mm_2637_2_0156dd57ba414a1c3af6683b4614af4f.jpg" },
    { id: 3, name: "Mochila Escolar", price: 89.90, stock: 5, image: "https://a-static.mlcdn.com.br/800x560/mochila-feminina-moda-qualidade-original-premium-resistente-espacosa-escolar-alta-qualidade-reforcado-unissex-blogueira-meimi-amores/franshopmix8/15966817785/5fa32872484a3334d4ea62fe7f3e473b.jpeg" }
  ];
  let discount = 0;

  function updateCartBadge() {
    const totalItems = cart.reduce((acc, item) => acc + item.quantity, 0);
    cartBadge.textContent = totalItems > 0 ? totalItems : "";
  }

  // Toast utility
  const toast = document.getElementById('toast');
  function showToast(message, ms = 2000, type = 'info') {
    if (!toast) return;
    toast.textContent = message;
    toast.className = 'toast show ' + (type ? 'toast-' + type : '');
    setTimeout(() => toast.classList.remove('show'), ms);
  }

  function renderProducts(prodList) {
    productContainer.innerHTML = "";
    prodList.forEach(product => {
      const card = document.createElement("div");
      card.className = "product-card";
      card.innerHTML = `
        <img src="${product.image}" alt="${product.name}">
        <h3>${product.name}</h3>
        <p>Preço: R$ ${product.price.toFixed(2)}</p>
        <p>Estoque: ${product.stock}</p>
        <button class="add-to-cart" data-id="${product.id}" ${product.stock === 0 ? "disabled" : ""}>
          ${product.stock === 0 ? "Esgotado" : "Adicionar"}
        </button>
      `;
      productContainer.appendChild(card);
    });
  }

  function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    const item = cart.find(i => i.id === productId);

    if (item) {
      if (item.quantity < product.stock) {
        item.quantity++;
      } else {
        alert("Estoque insuficiente!");
        return;
      }
    } else {
      cart.push({ id: productId, quantity: 1 });
    }
    localStorage.setItem("cart", JSON.stringify(cart));
    updateCartBadge();
  showToast('Produto adicionado ao carrinho');
  }

  function openCartModal() {
    cartModal.style.display = "block";
    renderCartItems();
  }

  function closeCartModal() {
    cartModal.style.display = "none";
  }

  function renderCartItems() {
    cartItemsContainer.innerHTML = "";
    let subtotal = 0;

    cart.forEach(item => {
      const product = products.find(p => p.id === item.id);
      if (!product) return;

      const itemSubtotal = product.price * item.quantity;
      subtotal += itemSubtotal;

      const cartItem = document.createElement("div");
      cartItem.className = "cart-item";
      cartItem.innerHTML = `
        <span>${product.name} - R$ ${product.price.toFixed(2)} x ${item.quantity}</span>
        <button class="remove-from-cart" data-id="${item.id}">Remover</button>
      `;
      cartItemsContainer.appendChild(cartItem);
    });

    subtotal -= discount;
    subtotalElement.textContent = `Subtotal: R$ ${subtotal.toFixed(2)}`;
  }

  function validateCoupon() {
    const subtotalRaw = cart.reduce((acc, item) => {
      const product = products.find(p => p.id === item.id);
      return acc + (product ? product.price * item.quantity : 0);
    }, 0);

    if (couponInput.value === "ALUNO10" && subtotalRaw >= 50) {
      discount = subtotalRaw * 0.10;
      alert(`Cupom aplicado! Desconto: R$ ${discount.toFixed(2)}`);
    } else if (couponInput.value === "LR1211") {
      discount = subtotalRaw * 0.35;
      alert(`Cupom LR1211 aplicado! Desconto: R$ ${discount.toFixed(2)}`);
    } else {
      discount = 0;
      alert("Cupom inválido ou subtotal insuficiente.");
    }
    renderCartItems();
  }

  // Event Listeners
  productContainer.addEventListener("click", e => {
    if (e.target.classList.contains("add-to-cart")) {
      const productId = parseInt(e.target.dataset.id);
      addToCart(productId);
    }
  });

  cartItemsContainer.addEventListener("click", e => {
    if (e.target.classList.contains("remove-from-cart")) {
      const id = parseInt(e.target.dataset.id);
      cart = cart.filter(item => item.id !== id);
      localStorage.setItem("cart", JSON.stringify(cart));
      renderCartItems();
      updateCartBadge();
    }
  });

  couponButton.addEventListener("click", validateCoupon);
  closeModalButton.addEventListener("click", closeCartModal);
  checkoutButton.addEventListener("click", openCartModal);

  // Tabs: Produtos / Admin
  const tabProducts = document.getElementById('tab-products');
  const tabAdmin = document.getElementById('tab-admin');
  const adminSection = document.getElementById('admin');
  const catalogSection = document.querySelector('.catalog');
  if (tabProducts && tabAdmin && adminSection && catalogSection) {
    tabProducts.addEventListener('click', () => {
      tabProducts.classList.add('active');
      tabAdmin.classList.remove('active');
      catalogSection.classList.remove('hidden');
      adminSection.classList.add('hidden');
    });
    tabAdmin.addEventListener('click', () => {
      tabAdmin.classList.add('active');
      tabProducts.classList.remove('active');
      catalogSection.classList.add('hidden');
      adminSection.classList.remove('hidden');
    });
  }

  // Confirm purchase behavior
  const confirmOrderBtn = document.getElementById('confirm-order');
  if (confirmOrderBtn) {
    confirmOrderBtn.addEventListener('click', () => {
      if (cart.length === 0) {
        showToast('Carrinho vazio');
        return;
      }
      // Simula confirmação: limpa carrinho
      cart = [];
      localStorage.removeItem('cart');
      updateCartBadge();
      renderCartItems();
      closeCartModal();
      showToast('Compra efetuada com sucesso!', 3000);
    });
  }

  // Admin form
  productForm.addEventListener("submit", e => {
    e.preventDefault();
    const currentUser = JSON.parse(sessionStorage.getItem('currentUser')) || null;
    if (!currentUser || !currentUser.loggedIn || currentUser.username !== 'admin') {
      showToast('Acesso negado. Faça login como admin para adicionar produtos.');
      return;
    }
    const newProduct = {
      id: products.length + 1,
      name: document.getElementById("nome").value,
      description: document.getElementById("descricao").value,
      price: parseFloat(document.getElementById("preco").value),
      stock: parseInt(document.getElementById("estoque").value),
      category: document.getElementById("categoria").value,
      sku: document.getElementById("sku").value,
      image: "https://via.placeholder.com/150?text=Novo+Produto"
    };
    products.push(newProduct);
    renderProducts(products);
    productForm.reset();
    showToast('Produto adicionado com sucesso');
  });

  // --- Simple user system (localStorage) ---
  const loginBtn = document.getElementById('login-btn');
  const createUserBtn = document.getElementById('create-user-btn');
  const logoutBtn = document.getElementById('logout-btn');
  const loginMessage = document.getElementById('login-message');
  const adminPanel = document.getElementById('admin-panel');

  function getUsers() {
    return JSON.parse(localStorage.getItem('users')) || [];
  }
  function saveUsers(u) {
    localStorage.setItem('users', JSON.stringify(u));
  }

  function showAdminIfAuthorized() {
    const cur = JSON.parse(sessionStorage.getItem('currentUser')) || null;
    if (cur && cur.loggedIn && cur.username === 'admin') {
      adminPanel.classList.remove('hidden');
      document.getElementById('login-area').classList.add('hidden');
      logoutBtn.style.display = 'inline-block';
    } else {
      adminPanel.classList.add('hidden');
      document.getElementById('login-area').classList.remove('hidden');
      logoutBtn.style.display = 'none';
    }
    // update top tab label to show username if logged in
    const tabAdminBtn = document.getElementById('tab-admin');
    if (tabAdminBtn) {
      if (cur && cur.loggedIn) {
        tabAdminBtn.textContent = cur.username;
        tabAdminBtn.classList.add('user-badge');
      } else {
        tabAdminBtn.textContent = 'Login';
        tabAdminBtn.classList.remove('user-badge');
      }
    }
  }

  // Create a user (stores username + password plaintext in localStorage for demo only)
  createUserBtn.addEventListener('click', () => {
    const username = document.getElementById('login-username').value.trim();
    const password = document.getElementById('login-password').value;
    if (!username || !password) {
      loginMessage.textContent = 'Informe usuário e senha para criar conta.';
      return;
    }
    const users = getUsers();
    if (users.find(u => u.username === username)) {
      loginMessage.textContent = 'Usuário já existe.';
      return;
    }
    users.push({ username, password });
    saveUsers(users);
    loginMessage.textContent = 'Conta criada. Você pode entrar agora.';
  });

  // Login
  loginBtn.addEventListener('click', () => {
    const username = document.getElementById('login-username').value.trim();
    const password = document.getElementById('login-password').value;
    const users = getUsers();
    const match = users.find(u => u.username === username && u.password === password);
    // allow the special built-in admin credentials
    if (!match && !(username === 'admin' && password === '123')) {
      loginMessage.textContent = 'Credenciais inválidas.';
      return;
    }
    const cur = { username, loggedIn: true };
    sessionStorage.setItem('currentUser', JSON.stringify(cur));
    loginMessage.textContent = '';
    showAdminIfAuthorized();
    // nicer feedback
    showToast(`Bem vindo, ${username}!`, 2500, 'success');
    // small animation on top tab
    const tabAdminBtn = document.getElementById('tab-admin');
    if (tabAdminBtn) {
      tabAdminBtn.classList.add('pulse');
      setTimeout(() => tabAdminBtn.classList.remove('pulse'), 1200);
    }
  });

  logoutBtn.addEventListener('click', () => {
  sessionStorage.removeItem('currentUser');
  loginMessage.textContent = 'Desconectado.';
  showAdminIfAuthorized();
  showToast('Sessão encerrada.', 1800, 'info');
  });

  // Initialize admin visibility
  showAdminIfAuthorized();

  // Busca
  searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase();
    const filtered = products.filter(p => p.name.toLowerCase().includes(query));
    renderProducts(filtered);
  });

  // Ordenação
  sortSelect.addEventListener("change", () => {
    let sorted = [...products];
    switch (sortSelect.value) {
      case "name-asc": sorted.sort((a,b) => a.name.localeCompare(b.name)); break;
      case "name-desc": sorted.sort((a,b) => b.name.localeCompare(a.name)); break;
      case "price-asc": sorted.sort((a,b) => a.price - b.price); break;
      case "price-desc": sorted.sort((a,b) => b.price - a.price); break;
    }
    renderProducts(sorted);
  });

  // Inicializa
  renderProducts(products);
  updateCartBadge();
});
