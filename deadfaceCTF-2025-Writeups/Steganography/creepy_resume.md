# Creepy Resume - DEADFACE CTF 2025

**Category:** `STEG`


## Challenge Description
![Creepy Resume](images/creepy_resume.png)

>A DEADFACE member landed an interview at Spooky Coffee using a resume that whispers in Unicode and charms every AI it touches. Those who can read between the glyphs say it speaks in riddles, crafted to bypass filters and impress any CAPTCHA-checking HR daemon.
>>Analyze the resume PDF. Can you find the secret string?
>>>Submit the flag as deadface{here_is_the_answer}.

## Environment
- WSL Ubuntu 
- Tools used: `pdfinfo`, `pdftotext`, `exiftool`, `python3`

## Methodology

- **Sanity check** – Confirm the PDF opens and contains ordinary resume text:
  ```bash
  pdfinfo lambiresume.pdf
  pdftotext lambiresume.pdf 
  ```
  Nothing suspicious appeared in the visible content; no embedded files (`pdfdetach -list`) and no images (`pdfimages -list`).

- **Inspect metadata** – Rich metadata often hides clues. `exiftool` exposes all info streams, even ones hidden from normal viewers:
  ```bash
  exiftool lambiresume.pdf
  ```
  The `UserComment` and `Copyright` fields contained unusual characters: an emoji followed by glyphs rendered as empty squares in most terminals. Their Unicode code points (Plane‑14 variation selectors) hinted at “emoji smuggling.”

- **Extract raw metadata values**:
  ```bash
  exiftool -UserComment -s3 lambiresume.pdf
  exiftool -Copyright -s3 lambiresume.pdf
  ```
  Output resembled `🥰󠅔󠅕󠅑...` (emoji + many `U+E0xxx` code points).

- **Decode the variation selectors** – Plane‑14 variation selectors are named `VARIATION SELECTOR-n`, so their numeric suffix can be treated as a value. Mapping each suffix to its ASCII equivalent (n → `chr(n)`) revealed an intelligible string, but still offset by 1.

  ```bash
  exiftool -UserComment -s3 lambiresume.pdf \
  | python3 - <<'PY'
  import sys, unicodedata
  text = sys.stdin.read().strip()
  decoded = []
  for ch in text:
      try:
          name = unicodedata.name(ch)
      except ValueError:
          continue
      if "VARIATION SELECTOR" in name:
          decoded.append(chr(int(name.split('-')[-1])))
  plain = ''.join(decoded)
  flag = ''.join(chr(ord(c)-1) for c in plain)  # Caesar shift -1
  print("raw :", plain)
  print("flag:", flag)
  PY
  ```

  - `plain` produced `efbegbdf|Mppl\`A\`n4"""~`.
  - Shifting every character back by 1 yielded `deadface{Look_@_m3!!!}`.

- The same technique on the `Copyright` field spits out an Easter egg (`deadface{I_could_enjoy_a_pizza_right_now}`), but the challenge flag is the first string.

## Flag
`deadface{Look_@_m3!!!}`

## Notes
- Variation-selector smuggling is a common Unicode steganography trick. Because many renderers ignore Plane‑14 selectors, they pass visually unnoticed.
- The Caesar `-1` shift is hinted by the trailing `~` (last printable ASCII code), an indicator to “wrap back” into readable characters.
