$(document).ready(function(){
	$('#linkupload').click(function(event){
		event.preventDefault();
		$('#fileupload').toggle();
	});

	$('.acomment').on("click",function(event){
		event.preventDefault();
		console.log($(this).parent().parent().attr('class'));
		$(this).parent().parent().siblings('.divcomment').toggle();
	});

	$('#formpost').submit(function(event){
		event.preventDefault();
		
		form_data = $(this).serialize();
		fd = new FormData();
		if ($('#fileupload')[0].files[0]){
		fd.append("fileupload", $('#fileupload')[0].files[0]);
		}
		$.each(form_data.split("&"), function(index, value){
			jsonobj = value.split("=");
			console.log(jsonobj[1])
			fd.append(jsonobj[0], jsonobj[1].replace(/\+/g," "));
		});
		$.ajax({
		       url: "/postcontent",
		       type: "POST",
		       data: fd,
		       processData: false,
		       contentType: false,
		       success: function(response) {
		           $('#pre_post').replaceWith("<div id='pre_post'></div>"+response);
		           $('#formpost').reset();
		       },
		       error: function(jqXHR, textStatus, errorMessage) {
		           console.log(errorMessage); // Optional
		       }
		    });

	});
});
