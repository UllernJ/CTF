xhr = new XMLHttpRequest();
xhr.open("POST","/admin/update", true);
xhr.setRequestHeader('Content-type','application/x-www-form-urlencoded');
xhr.send("service=apache&version=2.4.49");  //vi får admin til å nedgradere anvilshop.utl