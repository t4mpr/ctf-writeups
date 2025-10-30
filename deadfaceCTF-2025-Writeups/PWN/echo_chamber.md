# Echo Chamber - DEADFACE CTF 2025

## Challenge Description
<img src="images/echo_chamber.png" alt="creepy resume" width="200"/> 

>DEADFACE loves their vintage tech, but their "Echo Chamber" chat bot has a critical flaw from the old days. It echoes messages without sanitizing input, potentially leaking sensitive data. As a Turbo Tactical operative, connect to the remote service at echochamber.deadface.io:13337 and exploit it to reveal a hidden flag.
>>Submit the flag as deadface{flag_text}.
>>>echochamber.deadface.io:13337


## Challenge Overview
- Target: `echochamber.deadface.io:13337`
- Goal: Exploit the unsanitized echo service to recover the hidden flag.

## Steps
1. Connected with `nc echochamber.deadface.io 13337` and confirmed it parrots any input.
2. Noticed the prompt text hinting at “vintage” flaws; tested with format string payloads like `%p` and observed raw pointers in the echoed output, confirming a classic format-string vulnerability.
3. Sent a bare `%s`, causing `printf` to treat the first stack value as a C-string pointer—which resolved to the in-memory flag—and the service printed it directly.

## Flag
`deadface{r3tr0_f0rm4t_l34k_3xp0s3d}`
