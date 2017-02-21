$(document).ready(function() {
	$(window).scroll(function() {
  	if($(document).scrollTop() > 10) {
    	$('#transition-nav').addClass('shrink');
    }
    else {
    $('#transition-nav').removeClass('shrink');
    }
  });
});
