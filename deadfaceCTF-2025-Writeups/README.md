# DDEADFACE CTF 2025 - Writeups

This repository contains comprehensive writeups for all challenges I solved during the deadface CTF competition held in October 2025.

## Competition Overview

- **Event:** [deadface CTF 2025](https://ctf.deadface.io/)
- **Team:** [BLACK MIRROR](https://ctf.deadface.io/teams/467)
- **Final Rank:** 28th Place / 815 teams
- **Final Score:** 6,751 points
- **Duration:** October 25-26, 2025
- **Team Challenges Solved:** 63 



## Quick Stats
### [t4mpr](https://ctf.deadface.io/users/934)

- **Cryptography:** 2 challenges (600 points)
- **SQL/Database:** 1 challenge(400 points)
- **Web:** 2 challenges (405 points)
- **Forensics/Traffic Analysis:** 2 challenges (350 points)
- **Linux Privilege Escalation:** 2 challenges (425 points)
- **Steganography:** 1 challenge (30 points)
- **OSINT:** 1 challenge (50 points)
- **PWN:** 1 challenge (20 points)

## Writeups by Category

### Cryptography

| Challenge | Points | Difficulty | Writeup | 
|-----------|--------|------------|---------|
| Dis-connec-ted  | 150 | Medium | [writeup](Cryptography/dis-connec-ted.md) 🩸 |
| Retro Rewind | 450 | Hard | [writeup](Cryptography/retro_rewind.md) |

**Skills:** FSK audio demodulation, AES-CBC decryption, time-based key derivation

### SQL/Database Challenges (EpicSales)

| Challenge | Points | Difficulty | Writeup |
|-----------|--------|------------|---------|
| Undervalued | 400 | Hard | [writeup](EpicSales/undervalued.md) |
|

**Skills:** SQL aggregation, JOIN operations, complex queries, data analysis

### Web Security

| Challenge | Points | Difficulty | Writeup |
|-----------|--------|------------|---------|
| The Invisible Man (Hack the Night) | 205 | Medium | [writeup](Web/invisible_man.md) |
| Goblin Hoard | 200 | Medium |  |

**Skills:** SQL injection, IDOR, API enumeration, credential discovery



### Linux Privilege Escalation (Hostbusters)

| Challenge | Points | Difficulty | Writeup |
|-----------|--------|------------|---------|
| Read 'Em and Weep | 300 | Hard | [writeup](Hostbusters/read_em_and_weep.md) |
| Pulse Check | 125 | Medium | [writeup](Hostbusters/pulse_check.md) |

**Skills:** SSH enumeration, sudo exploitation, command injection, binary analysis, RSA decryption, XOR deobfuscation

### Forensics/Traffic Analysis (Stolen Secrets)

| Challenge | Points | Difficulty | Writeup |
|-----------|--------|------------|---------|
| Patchwork | 250 | Hard | [writeup](StolenSecrets/patchwork.md) |
| Tell No One | 100 | Easy |  |

**Skills:** PCAP analysis, HTTP stream extraction, password-protected archives, PyInstaller analysis

### Steganography

| Challenge | Points | Difficulty | Writeup |
|-----------|--------|------------|---------|
| Creepy Resume | 30 | Easy | [writeup](Steganography/creepy_resume.md) |

**Skills:** PDF metadata analysis, Unicode steganography, Emoji smuggling, Caesar cipher

### OSINT

| Challenge | Points | Difficulty | Writeup |
|-----------|--------|------------|---------|
| Diss Track | 50 | Easy | [writeup](OSINT/diss_track.md) |

**Skills:** Forum reconnaissance, Spotify playlist discovery

### PWN/Binary Exploitation

| Challenge | Points | Difficulty | Writeup |
|-----------|--------|------------|---------|
| Echo Chamber | 20 | Easy | [writeup](PWN/echo_chamber.md) |

**Skills:** Format string vulnerabilities, netcat


## Tools & Technologies Used

### Cryptography
- `minimodem` - FSK audio demodulation
- `pycryptodome` - Python cryptography library
- `openssl` - RSA operations
- Custom Python scripts for key derivation

### Forensics & Network Analysis
- `tshark`/`wireshark` - PCAP analysis
- `exiftool` - Metadata extraction
- `binwalk` - Binary analysis
- `strings` - String extraction

### Reconnaissance & Enumeration
- `curl` - HTTP client for web challenges
- `nmap` - Network scanning
- `dirb`/`gobuster` - Directory enumeration
- Browser Developer Tools

### Web Exploitation
- `sqlmap`
- SQL injection techniques
- API fuzzing and enumeration

### Steganography
- `pdfinfo`/`pdftotext` - PDF analysis
- `exiftool` - Metadata extraction
- Python for Unicode analysis

### Linux/Binary Analysis
- `ssh` - Remote access
- `sudo -l` - Privilege enumeration
- `base64` - Encoding/decoding
- Python for binary analysis and XOR operations
- `objdump`/`xxd` - Binary inspection

### Database
- `mysql` client - Direct database access
- SQL query optimization
- Python3 
- Claude Code CLI

### Programming Languages
- Python 3 - Primary scripting language
- Bash - Automation and one-liners
- SQL - Database queries



## Key Learnings

### Technical Skills

1. **Cryptography:**
   - FSK audio demodulation using minimodem
   - Time-based key derivation algorithms
   - AES-CBC mode encryption/decryption
   - Understanding of initialization vectors

2. **Database:**
   - Complex SQL aggregation queries
   - JOIN operations across multiple tables
   - SQL performance optimization
   - Data analysis and pattern recognition

3. **Web Security:**
   - SQL injection bypass techniques
   - IDOR vulnerability exploitation
   - API endpoint enumeration and abuse
   - Session management weaknesses

4. **Forensics:**
   - PCAP analysis and HTTP stream extraction
   - Multipart form data parsing
   - Password-protected archive handling
   - PyInstaller binary analysis

5. **Linux Privilege Escalation:**
   - Sudo misconfiguration exploitation
   - Command injection in privileged contexts
   - Path traversal vulnerabilities
   - Binary reverse engineering for flag extraction



### Problem-Solving Approaches

1. **Systematic Enumeration:** Always start with thorough reconnaissance before attempting exploitation
2. **Chain Multiple Vulnerabilities:** Many challenges required combining multiple techniques
3. **Read Everything:** HTML comments, API responses, and error messages often contain crucial hints
4. **Artifact Preservation:** Save all intermediate files and outputs for later analysis
5. **Documentation:** Detailed notes during exploitation make writeup creation much easier

## Highlights

### Most Challenging: Retro Rewind 
- Required understanding of custom time-based key derivation
- Multiple failed approaches before discovering the correct algorithm
- Testing different interpretations of "positional variance"
- Success came from combining the full timestamp with position index

### Most Rewarding: Dis-connec-ted 
- First Blood!
- Required creative thinking to understand what artifacts you were given and how to use tools like minimodem to decrypt hidden messages 
- Learned about AES-256-CBC encryption & PKCS5/PKCS7 padding


## Competition Reflections

This CTF was an excellent learning experience that covered a broad range of security domains. The challenges were well-designed with realistic scenarios that mirror real-world vulnerabilities. The DeadFace storyline and theming made the competition more engaging.

### What Went Well:
- Systematic approach to each challenge
- Good time management across multiple domains
- Effective use of automation and scripting
- Thorough documentation during exploitation

### Areas for Improvement:
- Could have been faster on SQL challenges with better query optimization
- Initial attempts at crypto challenges took multiple iterations
- More practice with binary analysis would speed up PWN challenges

## Setup & Usage

### Prerequisites

```bash
# Python dependencies
pip install pycryptodome requests beautifulsoup4

# System tools (Kali Linux / Ubuntu)
sudo apt-get install tshark wireshark curl ncat exiftool minimodem
sudo apt-get install mysql-client pdfinfo poppler-utils

# Optional but recommended
sudo apt-get install burpsuite dirb sqlmap
```

### Running Solver Scripts

Solver scripts are located in the `artifacts/` directory and can be run with `python3`

```bash
# Crypto solvers
python3 dis-connec-ted_decrypt.py
python3 retro_rewind_decrypt.py
```

### Reproducing Exploits

Most web challenges may still be accessible. Check individual writeups for current availability and reproduction instructions.

## Acknowledgments

- **deadface CTF** - For creating an amazing event with phenominal challenges.
- **My Team** - For working with me to solve these challenges and help eachother along the way. For tools, techniques, and shared knowledge

## Contact & Links

- **Author:** [Stephen Mosillo](https://www.linkedin.com/in/smosillo/) aka t4mpr
- **Competition:** [DeadFace CTF](https://ctf.deadface.io/)
- **Organizers:** [Cyber Hacktics](https://cyberhacktics.com/)

---

## Disclaimer

These writeups are provided for educational purposes only. The techniques demonstrated should only be used in authorized security testing scenarios, CTF competitions, or educational environments. Unauthorized access to computer systems is illegal.

---

**Last Updated:** October 27, 2024
