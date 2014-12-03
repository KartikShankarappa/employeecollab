$(document).ready(function(){
	console.log("Loaded");
	$('#linkupload').click(function(event){
		event.preventDefault();
		$('#fileupload').toggle();
	})

});