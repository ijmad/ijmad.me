$( document ).ready(
  function () {
    $('<link/>', { rel: 'stylesheet', type: 'text/css', href: 'static/modal.css' }).appendTo('head');
    $('<div/>', { id: 'modal' }).appendTo('body');
  }
);

function checkCaptcha() {
  if ( ! $('#modal').children().length ) {
    $('<div/>', { id: 'recaptcha' }).appendTo($('#modal'));
    $('<a/>', { id: 'cancel', href: 'javascript:hideCaptcha();' }).html('OK, I admit it. BEEP BOOP. &#129302;').appendTo($('#modal'));
    
    grecaptcha.render('recaptcha', {
      'sitekey' : '{{ RECAPTCHA_SITEKEY }}',
      callback: function (response) {
        $('#recaptcha').hide();
        $('<div/>', { id: 'spinner' }).appendTo($('#modal'));
        $.post('/api/email', {'g-recaptcha-response' : response}, function(data, textStatus) {
          var email = data['email'];
          
          $('#spinner').remove();
          $('#cancel').remove();
          
          $('<a/>', { id: 'email', href: 'mailto:' + email }).html(email).appendTo($('#modal'));
          $('<a/>', { id: 'close', href: 'javascript:hideCaptcha();' }).html('Close').appendTo($('#modal'));
          
          $('#recaptcha').remove();
        }, 'json');
      }
    });
  }
  
  $('#modal').fadeIn();
}

function hideCaptcha() {
  $('#modal').fadeOut();
}