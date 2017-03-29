function choose() {
	document.getElementById("choose").style.display="none";
	document.getElementById("main").style.display="block";
}

function choose2() {
	document.getElementById("choose").style.display="none";
	document.getElementById("main").style.display="block";
	document.getElementById("meat").style.display="none";
}

function clearout() {
	document.getElementById("form1").reset();
}

var list=[];
function transpose(p1) {
	var txt=document.getElementById(p1).value;
	list.push(txt);
	var res=document.getElementById("totallist");
	res.value=list.toString(); 
}
function adding1() {
	transpose("visa");
}
function adding2() {
	transpose("mastercard");
}
function adding3() {
	transpose("lloyds");
}
function adding4() {
	transpose("hsbc");
}
function adding5() {
	transpose("rbs");
}
function adding6() {
	transpose("cheese");
}
function adding7() {
	transpose("ham");
}
function adding8() {
	transpose("mayo");
}
function adding9() {
	transpose("bread");
}

function news() {
	document.getElementById("results").style.display="none";
	document.getElementById("newsearch").style.display="block";
}
