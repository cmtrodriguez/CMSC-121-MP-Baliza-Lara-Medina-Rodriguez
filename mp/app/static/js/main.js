// Function to open the sidebar
function openMenu() {
  document.getElementById("sideMenu").style.width = "250px";
}

// Function to close the sidebar
function closeMenu() {
  document.getElementById("sideMenu").style.width = "0";  
}


// ------------------------ CLICKING PRODUCT --------------------------- //
// Function to view product details (example: show alert for product name)
function viewProduct(productName) {
  alert("You clicked on " + productName);
  // You can redirect here if needed
}

// ------------------------ EDIT --------------------------- //
// Open Modal for Editing Product Details
function openModal(productName, productPrice, productId) {
  // Open the modal
  document.getElementById('editModal').style.display = 'block';

  // Pre-fill the modal form fields with the current product's details
  document.getElementById('product-name').value = productName;
  document.getElementById('product-price').value = productPrice;

  // Store the productId in a global variable to reference when saving
  currentProductId = productId;
}

// Close Modal
function closeModal() {
  document.getElementById('editModal').style.display = 'none';
}

// Delete the selected product
function deleteProduct() {
  if (currentProductId) {
      // Example: Remove the product from your display
      document.getElementById(`product-${currentProductId}`).remove(); 
      
      // Close the modal after deletion
      closeModal();
  }
}

// Handle form submission to update product details dynamically
const editForm = document.getElementById('editForm');
if (editForm) {
  editForm.addEventListener('submit', function(event) {
    event.preventDefault();

    const productName = document.getElementById('product-name').value;
    let productPrice = document.getElementById('product-price').value;

    // If the price doesn't contain a decimal, add .00
    if (!productPrice.includes('.')) {
        productPrice += '.00';
    }

    if (currentProductId) {
        // Update the product details immediately
        document.getElementById(`product-name-${currentProductId}`).innerText = productName;
        document.getElementById(`product-price-${currentProductId}`).innerText = `Php ${parseFloat(productPrice).toFixed(2)}`;
    }

    // Close the modal after saving changes
    closeModal();
  });
}

// ------------------------ IMAGE --------------------------- //
// Preview the uploaded image
function previewImage(event) {
  const file = event.target.files[0]; 

  if (file) {
      const reader = new FileReader();
      
      // When file is loaded, display it
      reader.onload = function(e) {
          const preview = document.getElementById('image-preview');
          const previewContainer = document.getElementById('image-preview-container');
          
          preview.src = e.target.result; 
          previewContainer.style.display = 'block'; 
      }

      reader.readAsDataURL(file);
  }
}

// ------------------------ ADD PRODUCT --------------------------- //
let isAdding = false;

// Open Add Product Modal
function openAddModal() {
  isAdding = true;
  currentProductId = null;

  const modal = document.getElementById('editModal');
  modal.style.display = 'block';

  // Clear form fields
  document.getElementById('product-name').value = '';
  document.getElementById('product-price').value = '';
  document.getElementById('product-image').value = '';
  document.getElementById('image-preview-container').style.display = 'none';

  // Set placeholders
  document.getElementById('product-name').placeholder = 'Enter product name';
  document.getElementById('product-price').placeholder = 'Enter product price';
}

// Get the user's name from localStorage and display it
const userNameElement = document.getElementById("userName");
if (userNameElement) {
  const userName = localStorage.getItem("username");  
  if (userName) {
      userNameElement.innerText = userName;
  }
}

// ------------------------ BUYER PAGE --------------------------- //
function addToCart(productId) {
  console.log('addToCart called for product:', productId);
  alert(`Added ${productId} to cart.`);
  // Logic to actually add to cart can be added here
}

function checkoutProduct(productId) {
  console.log('checkoutProduct called for product:', productId);
  window.location.href = `/checkout/${productId}/`;
}

function searchProducts(event) {
  event.preventDefault();
  const query = document.getElementById('searchInput').value.trim();
  if (query) {
      window.location.href = `/search/?q=${encodeURIComponent(query)}`;
  }
  return false;
}

// ------------------------ DROPDOWNS --------------------------- //
// Function to filter products by price range
function filterByPrice() {
  const priceRange = document.getElementById('price-range').value;
  const [minPrice, maxPrice] = priceRange.split('-').map(Number);
  const products = document.querySelectorAll('.product');

  products.forEach(product => {
      const price = Number(product.getAttribute('data-price'));
      
      if (price >= minPrice && price <= maxPrice) {
          product.style.display = 'block'; 
      } else {
          product.style.display = 'none'; 
      }
  });
}

// Function to filter products by category
function filterProducts() {
  console.log('filterProducts function called'); // Debug log
  const searchInput = document.getElementById('searchInput');
  const searchText = searchInput ? searchInput.value.toLowerCase() : '';
  const categoryFilter = document.getElementById('category-filter');
  const categoryValue = categoryFilter ? categoryFilter.value : 'all';
  const products = document.querySelectorAll('.product');

  products.forEach(product => {
      const productCategory = product.getAttribute('data-category');
      const productName = product.querySelector('.product-name').textContent.toLowerCase();

      const matchesSearch = productName.includes(searchText);
      const matchesCategory = categoryValue === 'all' || categoryValue === productCategory;

      if (matchesSearch && matchesCategory) {
          product.style.display = 'block'; 
      } else {
          product.style.display = 'none'; 
      }
  });
}

const searchInput = document.getElementById('searchInput');
if (searchInput) {
    searchInput.addEventListener('input', filterProducts);
}

// Initialize filters and username display when the page loads
window.onload = function() {
  const categoryFilterSelect = document.getElementById('category-filter');
  const priceRangeSelect = document.getElementById('price-range');
  const searchInput = document.getElementById('searchInput');
  if (categoryFilterSelect || priceRangeSelect || searchInput) {
      filterProducts();
  }
};


// ------------------------ CART --------------------------- //

var productToRemove;

function increaseQuantity(productId) {
  console.log('increaseQuantity called for product:', productId);
    var inputField = document.getElementById('quantity-' + productId);
    if (inputField) {
      inputField.value = parseInt(inputField.value) + 1;
    }
}

function decreaseQuantity(productId) {
  console.log('decreaseQuantity called for product:', productId);
    var inputField = document.getElementById('quantity-' + productId);
    if (inputField) {
      if (parseInt(inputField.value) > 1) {
          inputField.value = parseInt(inputField.value) - 1;
      }
    }
}

function openRemoveModal(productId) {
    console.log('openRemoveModal called for product:', productId);
    productToRemove = productId;
    const removeModal = document.getElementById('removeModal');
    if (removeModal) {
      removeModal.style.display = 'block';
    }
}

function closeRemoveModal() {
    console.log('closeRemoveModal called');
    const removeModal = document.getElementById('removeModal');
    if (removeModal) {
      removeModal.style.display = 'none';
    }
}

function removeProduct() {
    console.log('removeProduct called', productToRemove);
    if (productToRemove) {
        // Remove the product from the cart items container
        var productElement = document.getElementById('product-' + productToRemove);
        if (productElement) {
          productElement.remove();
        }

        // Remove the product from localStorage
        var cartData = JSON.parse(localStorage.getItem('cartData')) || [];
        cartData = cartData.filter(item => item.id !== productToRemove);
        localStorage.setItem('cartData', JSON.stringify(cartData));

        // Show message if cart is empty
        const cartItemsContainer = document.getElementById('cart-items');
        if (cartItemsContainer) {
          if (cartData.length === 0) {
              cartItemsContainer.innerHTML = "<div class='empty-cart-message'>Your cart is empty!</div>";
          }
        }

        closeRemoveModal();
    }
}

function saveCartAndProceed() {
    console.log('saveCartAndProceed called');
    var cartData = [
        {
            id: 1,
            name: 'Product 1',
            quantity: document.getElementById('quantity-1').value,
            price: 30.00,
        },
        {
            id: 2,
            name: 'Product 2',
            quantity: document.getElementById('quantity-2').value,
            price: 20.00,
        }
    ];

    // Save cart data in localStorage
    localStorage.setItem('cartData', JSON.stringify(cartData));

    // Proceed to checkout
    window.location.href = '/checkout';
}

// ------------------------ CHECKOUT --------------------------- //
// Payment selection
function selectPaymentMethod(method) {
  alert('You selected ' + method + ' as the payment method. It has been noted.');
}


// ------------------------ THINGS TO DO --------------------------- //
// Make other buttons work
// Make sure that the producst will only display if the seller adds a product
// The products there are just placeholders
// Category button is working but the product's edit model isn't reflecting to the set category (eg. the set category is shorts but when clicked edit button the category is saying that it's pajama) 
// Same  with buyer page, the products added by the must be displayed
// makethe SELLER and BUYER page buttons functional
// make sure that the images can be reflected in the products
// Make the search engine work
// For the checkout and add to cart we only placed placeholders, make the buyer's product buttons connect with add to cart and checkout
// SET UP THE DATABASE FOR EVERYTHING. ILL BE SENDING A GUIDE ON HOW TO INJECT POSTGRESQL SA GC//


document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.querySelector('.logout-btn');
   
    if (logoutBtn) {
       logoutBtn.addEventListener('click', function() {
           alert('Logout clicked! Redirecting to login page...');
       });
    }
   
});

// Function to toggle notifications (placeholder)
function toggleNotifications() {
    console.log('toggleNotifications function called');
    alert('Notifications feature coming soon!');
}

// Function to toggle home (placeholder)
function toggleHome() {
    console.log('toggleHome function called');
    window.location.href = "{% url 'buyer' %}";
}

// ------------------------ SELLER PAGE SPECIFIC FUNCTIONS --------------------------- //

// Function to toggle notifications on the seller page
function sellerToggleNotifications() {
    console.log('sellerToggleNotifications function called'); // Debug log
    alert('Notifications feature coming soon!');
}

// Function to toggle home on the seller page
function sellerToggleHome(buttonElement) {
    console.log('sellerToggleHome function called'); // Debug log
    const sellerUrl = buttonElement.dataset.sellerUrl; // Read the data attribute
}
