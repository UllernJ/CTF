## Legacy - HTB
<h2>nmap</h2>

```
nmap 10.10.10.4 -sV -sC
Starting Nmap 7.80 ( https://nmap.org ) at 2022-02-09 11:19 CET
Nmap scan report for 10.10.10.4
Host is up (0.042s latency).
Not shown: 997 filtered ports
PORT     STATE  SERVICE       VERSION
139/tcp  open   netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open   microsoft-ds  Microsoft Windows XP microsoft-ds
3389/tcp closed ms-wbt-server
Service Info: OSs: Windows, Windows XP; CPE: cpe:/o:microsoft:windows, cpe:/o:microsoft:windows_xp
```
```
sudo nmap --script=vuln 10.10.10.4
Starting Nmap 7.80 ( https://nmap.org ) at 2022-02-09 11:28 CET
Pre-scan script results:
| broadcast-avahi-dos: 
|   Discovered hosts:
|     224.0.0.251
|   After NULL UDP avahi packet DoS (CVE-2011-1002).
|_  Hosts are all up (not vulnerable).
Nmap scan report for 10.10.10.4
Host is up (0.038s latency).
Not shown: 997 filtered ports
PORT     STATE  SERVICE
139/tcp  open   netbios-ssn
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
445/tcp  open   microsoft-ds
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
3389/tcp closed ms-wbt-server

Host script results:
|_samba-vuln-cve-2012-1182: NT_STATUS_ACCESS_DENIED
| smb-vuln-ms08-067: 
|   VULNERABLE:
|   Microsoft Windows system vulnerable to remote code execution (MS08-067)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2008-4250
|           The Server service in Microsoft Windows 2000 SP4, XP SP2 and SP3, Server 2003 SP1 and SP2,
|           Vista Gold and SP1, Server 2008, and 7 Pre-Beta allows remote attackers to execute arbitrary
|           code via a crafted RPC request that triggers the overflow during path canonicalization.
|           
|     Disclosure date: 2008-10-23
|     References:
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2008-4250
|_      https://technet.microsoft.com/en-us/library/security/ms08-067.aspx
|_smb-vuln-ms10-054: false
|_smb-vuln-ms10-061: ERROR: Script execution failed (use -d to debug)
| smb-vuln-ms17-010: 
|   VULNERABLE:
|   Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2017-0143
|     Risk factor: HIGH
|       A critical remote code execution vulnerability exists in Microsoft SMBv1
|        servers (ms17-010).
|           
|     Disclosure date: 2017-03-14
|     References:
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143
|       https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/
|_      https://technet.microsoft.com/en-us/library/security/ms17-010.aspx
```

Dette åpner opp for <a href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2008-4250">CVE-20088-4250</a> og <a href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143">CVE-2017-0143.</a>
<p>Etter litt søking finner vi ut at serveren er sårbar for remote command execution, og med dette kan vi få et reverse shell, vi har ferdige verktøy vi kan bruke til dette med metasploit.</p>
<p>Med denne exploiten blir vi da admin og vi finner root og user flag i "Documents and settings".</p>

