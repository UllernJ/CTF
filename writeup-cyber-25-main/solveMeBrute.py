from pwn import *
import string
import itertools
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

chars = string.ascii_lowercase
all_combos = [''.join(c) for c in itertools.product(chars, repeat=4)]

def try_combo(combo: str):
    try:
        p = process("solveMe.o", level='error')
        #1
        p.recvuntil(b":")
        p.sendline(b"SuperSecretPass!")
        #2
        p.recvuntil(b":")
        p.sendline(b"a beautiful pass")
        #3
        expected = [-0x708baa70, 0x6b838889, 0x8c5d8485, 0x6283616a]
        password = []
        local_e8 = 0

        for i in range(4):
            local_dc = local_e8 * 0x1010101 + 0x10203
            local_e8 += 4
            
            chunk = ((expected[i] - 0x23232323) ^ local_dc)
            for j in range(4):
                password.append(chr((chunk >> (j * 8)) & 0xFF))
        password = ''.join(password)

        p.recvuntil(b":")
        p.sendline(password.encode())

        #4
        p.recvuntil(b":")
        p.sendline(combo.encode())
        p.recvuntil(b"fourth password")
        result = p.recvall(timeout=1)
        p.close()
        if b"flag{" in result.lower():
            return combo
        return None
    except:
        return None

if __name__ == '__main__':
    with Pool(cpu_count()) as pool:
        for result in tqdm(pool.imap_unordered(try_combo, all_combos), total=len(all_combos), desc="Testing passwords"):
            if result:
                print(f"\n[+] Password found: {result}")
                pool.terminate()
                break
        else:
            print("\n[-] Password not found")