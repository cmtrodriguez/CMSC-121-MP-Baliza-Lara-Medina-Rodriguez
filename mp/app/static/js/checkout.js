console.log('checkout.js loaded');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded fired');

    const paymentButtons = document.querySelectorAll('.payment-method');
    const hiddenPaymentMethodInput = document.getElementById('selected-payment-method');
    const checkoutButton = document.querySelector('.checkout-btn');
    const addressInput = document.getElementById('address'); // Get address input
    const form = document.querySelector('form'); // Get the form element

    if (!hiddenPaymentMethodInput) {
        console.error('Hidden payment method input not found!');
        return; // Stop execution if essential element is missing
    }

    if (paymentButtons.length === 0) {
        console.warn('No payment method buttons found.');
    } else {
        console.log(`Found ${paymentButtons.length} payment method buttons. Attaching listeners.`);
        paymentButtons.forEach(button => {
            button.addEventListener('click', function() {
                const method = this.dataset.method;
                console.log('Payment method selected:', method); // Log the selected method
                hiddenPaymentMethodInput.value = method; // Set hidden input value

                // Optional: Add visual feedback
                paymentButtons.forEach(btn => btn.classList.remove('selected'));
                this.classList.add('selected');
            });
        });
    }

    if (checkoutButton) {
        console.log('Checkout button found. Attaching listener.');
        // Remove any previous listeners to avoid duplicates
        checkoutButton.removeEventListener('click', handleCheckoutButtonClick);
        // Attach the new listener
        checkoutButton.addEventListener('click', handleCheckoutButtonClick);
    } else {
        console.error('Checkout button not found!');
    }

    // Function to handle checkout button click and validation
    function handleCheckoutButtonClick(event) {
        console.log('Checkout button clicked. Running validation.');
        const address = addressInput ? addressInput.value.trim() : '';
        const paymentMethod = hiddenPaymentMethodInput.value; // Read directly from the hidden input

        console.log('Address for validation:', address);
        console.log('Payment method for validation:', paymentMethod);

        if (!address) {
            alert('Please provide a delivery address.');
            return; // Stop if validation fails
        }

        if (!paymentMethod) {
            alert('Please select a payment method.');
            return; // Stop if validation fails
        }

        console.log('Validation successful. Submitting form.');
        // If validation passes, trigger the form submission
        form.submit();
        // Note: Using form.submit() is simpler than fetch for basic form submission
        // If you need to prevent default form submission and use fetch,
        // you would add event.preventDefault() at the beginning of this function
        // and then use the fetch logic.
    }
}); 