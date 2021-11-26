function validate(){
	var re = /^[0-9a-zA-Z\s#-]+$/;
	const text = document.getElementById('keyword').value.trim();
	if(text === '' || text == null){
		alert('book title is required');
		return false;
	}
	if(!text.match(re)){
		alert('book title should only contain letters and digits');
		return false;
	}
	return true;
}
