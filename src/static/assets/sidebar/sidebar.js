$(function(){
	$('.link-yellow').hover(
		function(){
			// alert("mouseover");
			$(this).addClass('selected');
		},
		function(){
			$(this).removeClass('selected');
		})


})