# Tell No One - DEADFACE CTF

**Category:** Forensics / Traffic Analysis
**Points:** 100
**Flag:** `deadface{l3ts_get_Th3s3_fiL3$}`

## Challenge Description

DEADFACE stole a sensitive document from the MyShare application! Find the document and present the flag shown within.

Submit the flag as deadface{flag}.

NOTE: deadface{h1dd3n_c0mm$!!} is NOT the flag. It's a leftover remnant that was supposed to have been removed.

## Solution

### Tools Used
- tshark
- Wireshark (optional)

### Analysis

The challenge provides a PCAP file (`cap-1753106207.pcap`) containing network traffic from the MyShare web application compromise.

1. **Initial Traffic Analysis**

First, I examined the HTTP traffic in the PCAP:

```bash
tshark -r cap-1753106207.pcap -q -z http,tree
```

This revealed 2615 HTTP request packets, with a mix of GET and POST requests.

2. **Following HTTP Streams**

I started examining HTTP streams to understand the attacker's activity:

```bash
tshark -r cap-1753106207.pcap -q -z follow,http,ascii,0
```

3. **Discovery of the Flag**

In the very first HTTP stream (stream 0), I found the flag hidden in a custom HTTP header:

```http
POST / HTTP/1.1
Host: files.techglobalresearch.com
User-Agent: curl/8.14.1
Accept: */*
FLAG: deadface{l3ts_get_Th3s3_fiL3$}
Content-Length: 437
Content-Type: application/x-www-form-urlencoded
```

The attacker included the flag as a custom HTTP header in their initial POST request to the application. The POST body contained a base64-encoded taunt message from the attacker "mirveal":

> I've gained full access to your network. Every file, every credential, every system — under my control. You didn't notice because I didn't want you to.
>
> This wasn't luck. It was precision. Your defenses were inadequate, and I've proven it.
>
> This attack is brought to you by mirveal. Thanks for the secrets!

### Key Findings

- The flag was embedded in the initial POST request as a custom HTTP header
- The attacker used `curl/8.14.1` as their user agent
- The attack targeted `files.techglobalresearch.com`
- The "sensitive document" was essentially the network traffic itself containing the flag

### Flag

`deadface{l3ts_get_Th3s3_fiL3$}`
