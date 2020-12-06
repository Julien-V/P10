$('#fr_FR').click(function(e) {
	e.preventDefault(e);
	document.cookie = "lang=fr_FR"
	location.reload()
})

$('#en_GB').click(function(e) {
	e.preventDefault(e);
	document.cookie = "lang=en_GB"
	location.reload()
})


$(':checkbox').click(function() {
    $(':checkbox').not(this).prop('checked', false);
});


$(':checkbox').change(function() {
	if ($(this).is(':checked')) {
		let val = $(this)[0].value;
		document.cookie = "lang="+val;
		let csrf = $('input[name="csrfmiddlewaretoken"]')[0].value;
		$.post("/ch_lang", {lang: val, csrfmiddlewaretoken: csrf})
			.done(function(data) {
				if (data) {
					location.reload();
				}
			});
	}
});

