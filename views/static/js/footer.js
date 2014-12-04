$(document).ready(function(){
	console.log("Loaded");
	$('#linkupload').click(function(event){
		event.preventDefault();
		$('#fileupload').toggle();
	})

	$('#formregister').submit(function(event){
		event.preventDefault();
		form_data = $(this).serialize();

		$.post('/register', form_data, function(data,status){
            alert(data);
        });
	});

	$('#formlogin').submit(function(event){
		event.preventDefault();
		form_data = $(this).serialize();

		$.post('/login', form_data, function(data,status){
            if(data == "1"){
            	window.location.replace("/wall");
            }
            else{
            	$('#loginwarn').text("Invalid login");
            }
        });
	});
});

