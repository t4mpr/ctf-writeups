# QnQSec CTF 2025 – Execution Challenge Write-up

## Challenge Summary
- **Category:** Forensics – Execution
- **Prompt:** Investigate a compromised Windows system using the provided `Execution.reg` hive dump (do **not** import it) and identify both the MITRE ATT&CK technique and the C2 endpoint. Flag format `QnQSec{Txxxx.xxx_IP:PORT}`.
- **Goal:** Derive the malicious persistence mechanism and extract the C2 IP:PORT embedded in the attacker payload.

## Prerequisites
- Linux/macOS shell with standard CLI tooling (`iconv`, `rg`, `sed`, `python3`, `curl`, `strings`).
- Internet access to retrieve the staged payload.
- Ensure the working directory is the challenge root, e.g. `/mnt/c/ctf/QnQSecCTF/forensics/Execution`.
- Do **not** import the `.reg` file into a live Windows registry.

## Step-by-Step Reproduction

### 1. Inspect the Registry Dump Safely
1. Convert the UTF-16LE encoded registry export to UTF-8 so CLI tools can process it:
   ```bash
   iconv -f utf-16le -t utf-8 Execution.reg > Execution_utf8.reg
   ```
2. Search for suspicious Image File Execution Options (IFEO) debugger entries:
   ```bash
   rg -n "Image File Execution Options" -n Execution_utf8.reg
   sed -n '709360,709420p' Execution_utf8.reg
   ```
   You should spot a `Debugger` value under `...\Image File Execution Options\AtBroker.exe` that launches `bitsadmin` to fetch a remote executable `w1n.exe` from GitHub.

### 2. Map the Activity to MITRE ATT&CK
- The IFEO debugger hijack corresponds to **T1546.012 – Event Triggered Execution: Image File Execution Options Injection**.
- Note this technique ID for the flag later.

### 3. Retrieve the Staged Payload
1. Reuse the URL from the registry value to manually download the payload (we use `curl` rather than `bitsadmin`):
   ```bash
   curl -L -o /tmp/image.jpg https://github.com/0xS1rx58/Update/releases/download/app/image.jpg
   ```
   Despite the `.jpg` extension, `file` will confirm it is a Windows PE:
   ```bash
   file /tmp/image.jpg
   # PE32+ executable (console) x86-64, for MS Windows...
   ```

### 4. Analyze the Payload Configuration
1. Run `strings` to hunt for encoded configuration values:
   ```bash
   strings -n 5 /tmp/image.jpg | rg 'eyJ'
   ```
   A Base64 blob such as `eyJDcW8yc05zWUlvIjoiMTMuNTkuMTUuMTg1IiwiSkZud2pNbElRVyI6IjgwMjEiLCJoQ1dXMk1EMVlHIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmhkWFJvYjNKcGVtVmtJanAwY25WbExDSmxlSEFpT2pFM056VXhOVGc0TlRnc0luVnpaWElpT2lKa1pXWmhkV3gwSW4wLmU2Tkw3YzJDU0RWUW1VRXFDU1B0NDktWHBWYzB2LWxUMW5JX2E0WHVRajAifQ==` will appear.
2. Decode it to reveal the embedded CHAOS RAT config:
   ```bash
   python3 - <<'PY'
import base64, json
blob = "eyJDcW8yc05zWUlvIjoiMTMuNTkuMTUuMTg1IiwiSkZud2pNbElRVyI6IjgwMjEiLCJoQ1dXMk1EMVlHIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmhkWFJvYjNKcGVtVmtJanAwY25WbExDSmxlSEFpT2pFM056VXhOVGc0TlRnc0luVnpaWElpT2lKa1pXWmhkV3gwSW4wLmU2Tkw3YzJDU0RWUW1VRXFDU1B0NDktWHBWYzB2LWxUMW5JX2E0WHVRajAifQ=="
print(json.dumps(json.loads(base64.b64decode(blob)), indent=2))
PY
   ```
   Output:
   ```json
   {
     "Cqo2sNsYIo": "13.59.15.185",
     "JFnwjMlIQW": "8021",
     "hCWW2MD1YG": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
   }
   ```
   The obfuscated keys map to `ServerAddress`, `Port`, and `Token`; the critical values are `13.59.15.185` and `8021`.

### 5. Assemble the Flag
- Technique ID: `T1546.012`
- C2 endpoint: `13.59.15.185:8021`
- Final flag: `QnQSec{T1546.012_13.59.15.185:8021}`

## Verification Checklist
- [x] Confirmed IFEO debugger persistence in the registry dump.
- [x] Matched activity to MITRE ATT&CK T1546.012.
- [x] Retrieved staged payload and validated it is a PE file.
- [x] Extracted Base64 configuration and decoded C2 IP:PORT.
- [x] Constructed flag in the required format.

## Notes & Safety
- Avoid executing the downloaded payload. Analysis was limited to static inspection using `file` and `strings`.
- The registry entry alone proves persistence; the payload analysis confirms the C2 endpoint.

## Final Answer
`QnQSec{T1546.012_13.59.15.185:8021}`
