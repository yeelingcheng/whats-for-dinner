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
    document.getElementById("left-side").style.backgroundImage = "url('{{ url_for('static', filename='images/fridge-open.png') }}')";
    document.getElementById("open").style.display="none";
    document.getElementById("ingredients").style.display="block";
    document.getElementById("button-options").style.display="block";
}

var list=[];

function addItem(p1) {
	var txt=document.getElementById(p1).value;
	list.push(txt);
	var res=document.getElementById("entirelist");
	res.value=list.toString();
}

function send1() {
	addItem("chicken");
}

function send2() {
	addItem("beef");
}