function rateSimething(  ){
$.ajax({
	type: "POST",
	url: arguments[0],
	data: {'id': arguments[1], 'rate': arguments[2], 'csrfmiddlewaretoken': arguments[3], 'identif': arguments[4]},
	dataType: "json",
	success: function(response) {
		if(response.newRate){
			var span = $('#rateSpan'+response.identif);
			span.text(''+response.newRate);
			for(var i=1;i<=5;i++){
				var star = $('#star-'+response.identif+"-"+i);
				if(i<=response.rate){
					star.removeClass('inactive');
					star.addClass('active');
				}else{
					star.removeClass('active');
					star.addClass('inactive');
				}
			}
		}
		},
	error: function(rs, e) {

	}
});
};
