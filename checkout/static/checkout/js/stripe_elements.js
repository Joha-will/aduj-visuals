// Stripe payment setup

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);

var clientSecret = $('#id_client_secret').text().slice(1, -1);

var stripe = Stripe(stripePublicKey);

var elements = stripe.elements();
const appearance = {
  theme: 'stripe',
  variables: {
    fontFamily: ' "Gill Sans", sans-serif',
    fontLineHeight: '1.5',
    borderRadius: '10px',
    colorBackground: '#F6F8FA',
    colorPrimaryText: '#262626'
  },
  rules: {
    '.Block': {
      backgroundColor: 'var(--colorBackground)',
      boxShadow: 'none',
      padding: '12px'
    },
    '.Input': {
      padding: '12px'
    },
    '.Input:disabled, .Input--invalid:disabled': {
      color: 'lightgray'
    },
    '.Tab': {
      padding: '10px 12px 8px 12px',
      border: 'none'
    },
    '.Tab:hover': {
      border: 'none',
      boxShadow: '0px 1px 1px rgba(0, 0, 0, 0.03), 0px 3px 7px rgba(18, 42, 66, 0.04)'
    },
    '.Tab--selected, .Tab--selected:focus, .Tab--selected:hover': {
      border: 'none',
      backgroundColor: '#fff',
      boxShadow: '0 0 0 1.5px var(--colorPrimaryText), 0px 1px 1px rgba(0, 0, 0, 0.03), 0px 3px 7px rgba(18, 42, 66, 0.04)'
    },
    '.Label': {
      fontWeight: '500'
    }
  }
};


// Create and mount the Payment Element and Pass the appearance object to the Elements instance

const card = elements.create('card', { appearance: appearance});
card.mount('#payment-element');

// Handle validation errors on card element

card.addEventListener('change', function (e) {

  var errorMsg = document.getElementById('error-message');

  if (e.error) {

    $(errorMsg).html(`<p class="alert alert-danger" role="alert"> <i class="fa-solid fa-square-xmark"></i> ${e.error.message} </p>`);

  } else {
    errorMsg.textContent = '';
  }

});


// Form Submit js

const form = document.getElementById('payment-form');

form.addEventListener('submit', function (event) {

  event.preventDefault();

  card.update({'disabled': true});

  $('#submit-button').attr('disable', true);

  $('#payment-form').fadeToggle(100);

  $('.spinner-container').addClass('show-spinner');

  var saveDetails = Boolean($('#save-details').attr('checked'));

  // Get {% csrf_token %} from form element

  var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

  var postData = {

    'csrfmiddlewaretoken': csrfToken,

    'client_secret': clientSecret,

    'save_details': saveDetails,
  };

  var url = '/checkout/cache_checkout_data/';

  $.post(url, postData).done(function() {

    stripe.confirmCardPayment(clientSecret, {

      payment_method: {
  
        card: card,
        
        billing_details: {

          name: $.trim(form.full_name.value),
          phone: $.trim(form.phone_number.value),
          email: $.trim(form.email.value),
          address: {
            line1: $.trim(form.address1.value),
            line2: $.trim(form.address2.value),
            city: $.trim(form.city.value),
            state: $.trim(form.county.value),
            country: $.trim(form.country.value),
  
          }
        }
  
      },
  
      shipping: {
        name: $.trim(form.full_name.value),
        phone: $.trim(form.phone_number.value),
        address: {
          line1: $.trim(form.address1.value),
          line2: $.trim(form.address2.value),
          city: $.trim(form.city.value),
          state: $.trim(form.county.value),
          country: $.trim(form.country.value),
          postal_code: $.trim(form.postal_code.value),
  
        }
      },
  
    }).then(function(result) {
  
      if (result.error) {
  
        const messageContainer = document.querySelector('#error-message');
  
        $(messageContainer).html(`<p class="alert alert-danger" role="alert"> <i class="fa-solid fa-square-xmark"></i> ${result.error.message} </p>`);
  
        $('#payment-form').fadeToggle(100);
  
        $('.spinner-container').removeClass('show-spinner');
  
        card.update({'disabled': false});
        
        $('#submit-button').attr('disable', false);
  
      } else {
  
        if (result.paymentIntent.status === 'succeeded'){
  
          form.submit();
          
      }
  
      }
    });

  }).fail(function() {

    location.reload();

  });

  
});