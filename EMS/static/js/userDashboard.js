$(document).ready(function(){
  $('.scroll-down').click (function() {
    $('html, body').animate({scrollTop: $('section#two').offset().top }, 'slow');
    return false;
  });
});
