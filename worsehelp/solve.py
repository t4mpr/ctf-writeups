#!/usr/bin/env python3
"""
Solver for k17ctf worsehelp

Approach:
- Choose (a, b) such that (a^2 + b^2 + ab + 3a + 3b) = 2 * (2ab + 7).
  This enforces r = 2 in the challenge, making d = k^2 (small private exponent).
- Use a Pell-type parametrization to generate infinitely many integer pairs (a,b)
  satisfying the above, then pick a prime a (>=1024 bits) and composite b.
- Query the service with (a, b), retrieve (c, e, n), perform Wiener's attack to
  recover d, and decrypt c.

Usage:
  python3 solve.py [--host challenge.secso.cc --port 7008] [--attempts 12]
"""

import argparse
import re
import socket
import sys
import time
from math import isqrt
import secrets


def gen_ab_S2_kbase(k: int, y0: int = 5, x0: int = 3):
    """Generate (a, b) satisfying a^2 + b^2 - 3ab + 3a + 3b - 14 = 0.

    Derivation: Let u=a-3, v=b-3. Then u^2 + v^2 - 3uv = 5.
    With x=u-v, y=u+v => y^2 - 5 x^2 = -20.
    Particular solution (y0, x0) = (5, 3), and general solutions via
    multiplication by the fundamental unit (9 + 4√5)^k.

    We compute (y, x) from (y0 + x0√5) * (9 + 4√5)^k and then map back to (a, b).
    """

    a1, b1 = 9, 4  # fundamental unit for x^2 - 5 y^2 = 1

    def mul(p, q):
        (a, b) = p
        (c, d) = q
        return (a * c + 5 * b * d, a * d + b * c)

    def pow_unit(exp: int):
        res = (1, 0)
        base = (a1, b1)
        k = exp
        while k > 0:
            if k & 1:
                res = mul(res, base)
            base = mul(base, base)
            k //= 2
        return res

    A, B = pow_unit(k)
    # (y + x√5) = (y0 + x0√5) * (A + B√5) = (y0*A + 5*x0*B) + (y0*B + x0*A) √5
    y = y0 * A + 5 * x0 * B
    x = y0 * B + x0 * A
    # Back to u, v then a, b
    u = (y + x) // 2
    v = (y - x) // 2
    a = u + 3
    b = v + 3
    return a, b


def is_probable_prime(n: int, rounds: int = 24) -> bool:
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    for p in small_primes:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def find_params(bitlen: int = 1024, k_start: int = 200, k_end: int = 2000):
    """Search k to get a prime a (>=bitlen) and composite b (>=bitlen)."""
    for k in range(k_start, k_end + 1):
        a, b = gen_ab_S2_kbase(k)
        if a <= 0 or b <= 0:
            continue
        if a.bit_length() < bitlen or b.bit_length() < bitlen:
            continue
        # Quick small prime filters on a
        sm = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        if any(a % p == 0 for p in sm):
            continue
        if not is_probable_prime(a):
            continue
        if is_probable_prime(b):
            continue
        return k, a, b
    return None


def wiener_attack(e: int, n: int):
    def contfrac(a, b):
        while b:
            q, a, b = a // b, b, a % b
            yield q

    def convergents(cf):
        p0, q0 = 1, 0
        p1, q1 = cf[0], 1
        yield p1, q1
        for a in cf[1:]:
            p0, p1 = p1, a * p1 + p0
            q0, q1 = q1, a * q1 + q0
            yield p1, q1

    cf = list(contfrac(e, n))
    for k, d in convergents(cf):
        if k == 0:
            continue
        if (e * d - 1) % k != 0:
            continue
        phi = (e * d - 1) // k
        s = n - phi + 1
        D = s * s - 4 * n
        if D < 0:
            continue
        r = isqrt(D)
        if r * r != D:
            continue
        p = (s + r) // 2
        q = (s - r) // 2
        if p * q == n:
            return d, p, q
    return None


def get_cen(host: str, port: int, a: int, b: int):
    """Connect to the remote service and fetch c, e, n for chosen (a, b)."""
    s = socket.create_connection((host, port), timeout=10)
    f = s.makefile("rwb", buffering=0)
    try:
        # Send immediately; the service prompts but doesn't require us to wait
        f.write((str(a) + ", " + str(b) + "\n").encode())
        s.settimeout(20)
        out = b""
        while True:
            line = f.readline()
            if not line:
                break
            out += line
            # Either we get three lines with '= ' or an error
            if out.count(b"= ") >= 3 or b"invertible" in out:
                break
        text = out.decode("utf-8", "ignore")
        if "invertible" in text:
            raise RuntimeError("Denominator not invertible mod phi (try again)")
        m = {}
        for name in ["c", "e", "n"]:
            m[name] = int(re.search(rf"{name}\s*=\s*(\d+)", text).group(1))
        return m["c"], m["e"], m["n"]
    finally:
        try:
            s.close()
        except Exception:
            pass


def int_to_bytes(x: int) -> bytes:
    if x == 0:
        return b"\x00"
    length = (x.bit_length() + 7) // 8
    return x.to_bytes(length, "big")


def main():
    ap = argparse.ArgumentParser(description="Solve the worsehelp RSA challenge")
    ap.add_argument("--host", default="challenge.secso.cc")
    ap.add_argument("--port", type=int, default=7008)
    ap.add_argument("--attempts", type=int, default=12, help="max tries to get a Wiener-susceptible instance")
    ap.add_argument("--bitlen", type=int, default=1024, help="min bit-length for a and b")
    ap.add_argument("--kstart", type=int, default=200)
    ap.add_argument("--kend", type=int, default=2000)
    args = ap.parse_args()

    # Find parameters once; they tend to work across attempts
    sys.stdout.write("[+] Searching parameters...\n")
    found = find_params(bitlen=args.bitlen, k_start=args.kstart, k_end=args.kend)
    if not found:
        sys.stderr.write("[-] Failed to find (a,b) meeting constraints in k range\n")
        sys.exit(1)
    k, a, b = found
    sys.stdout.write(f"[+] Using k={k} with a_bits={a.bit_length()} b_bits={b.bit_length()}\n")

    # Try multiple times to beat the invertibility hiccup and get a Wiener-susceptible instance
    for attempt in range(1, args.attempts + 1):
        sys.stdout.write(f"[+] Attempt {attempt}/{args.attempts} connecting...\n")
        try:
            c, e, n = get_cen(args.host, args.port, a, b)
        except Exception as ex:
            sys.stdout.write(f"[!] Remote error: {ex}\n")
            time.sleep(0.5)
            continue

        wd = wiener_attack(e, n)
        if not wd:
            sys.stdout.write("[!] Wiener attack failed; retrying...\n")
            time.sleep(0.5)
            continue

        d, p, q = wd
        sys.stdout.write(f"[+] Recovered d (bits={d.bit_length()})\n")
        m = pow(c, d, n)
        msg = int_to_bytes(m)
        sys.stdout.write(f"[+] Plaintext: {msg!r}\n")
        # Try to print clean flag line if it matches
        try:
            text = msg.decode("utf-8", "ignore")
            m = re.search(r"K17\{.*\}", text)
            if m:
                sys.stdout.write(f"[+] Flag: {m.group(0)}\n")
        except Exception:
            pass
        break
    else:
        sys.stderr.write("[-] All attempts failed. Try increasing attempts or k range.\n")
        sys.exit(2)


if __name__ == "__main__":
    main()

