# Crypto

## BASED

Vi får en base64 string som lett kan dekrypteres.

```
SU5GRUNURUR7ZHVfZXJfOTRONUtlXzg0NWVEX0s0Tl9tNE5fNTEhfQ==

INFECTED{du_er_94N5Ke_845eD_K4N_m4N_51!}
```

## Spinnvill

```
TYQPNEPO{u00_5a1Y_Xp_c19S7_C0fyo}

Dette ser ut som en variant av Caesar og kan lett dekrypteres med verktøy på nett.

INFECTED{j00_5p1N_Me_r19H7_R0und}
```

## Repetisjon er moro

```
Vi får dette cipher_texten, hele stringen er kryptert med en veldig dårlig key som vi kan finne ut av med bare av å vite de 4 første bokstavene.
49b4469b43ae459a7ba230ac5f9353816da35fb8348c30ab729337bb5fb9528750cd30a3

from pwn import xor

cipher_text = bytes.fromhex("49b4469b43ae459a7ba230ac5f9353816da35fb8348c30ab729337bb5fb9528750cd30a3")

partial_key = xor(cipher_text[:4], 'INFE')

print(xor(cipher_text, partial_key).decode('utf-8'))

INFECTED{X0r_iS_mY_f4v0uri7e_CRYP70}
```

## HashMeow

```
Vi får en zip fil som er kryptert med et passord som er lekket i rockyou.txt (dette er en veldig kjent passord liste).
Vi løser det ved å hente ut hashen fra zip filen og bruteforce den med hashcat med rockyou som wordlist.
Da får vi åpnet zip filen og vi får flagget.
```

## Xtremely hidden? OR is it?

```
Ved å lese litt på hvordan BMP filen fungerer kan vi se at det er en del ubrukte bytes i datafilen. Da kan vi xore disse for å fa keyen.
Siden det ble kryptert ubrukte bytes så ble keyen rett og slett også bare skrevet ut i hex.
Keyen var FADEBABE og vi får flagget:
INFECTED{ikke_veldig_bra}
```
