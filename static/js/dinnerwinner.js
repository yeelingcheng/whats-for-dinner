function choose() {
	document.getElementById("choose").style.display="none";
	document.getElementById("main").style.display="block";
}

function choose2() {
	document.getElementById("choose").style.display="none";
	document.getElementById("main").style.display="block";
	document.getElementById("meat").style.display="none";
}

function myFunction() {
    document.getElementById("left-side").style.backgroundImage = url({{url_for('static', filename='images/fridgeopen.png')}});
    document.getElementById("open").style.display="none";
    document.getElementById("ingredients").style.display="block";
    document.getElementById("button-options").style.display="block";
}
