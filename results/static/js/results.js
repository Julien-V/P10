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