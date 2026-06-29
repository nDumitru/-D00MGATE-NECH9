#!/usr/bin/env python3
"""
D00MGATE-NECH9 — CTF Challenge Demo
=====================================
Author: Dumitru Nechita
License: D00MGATE-NECH9 Proprietary License v1.0

NOTICE: This file contains the PUBLIC DEMO layer only.
Core protocol mechanics are not present in this code.

"You can see the gate. You cannot dial it without the address."
"""

import hashlib
import time
import os
import argparse

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Fore:
        GREEN=RED=YELLOW=CYAN=WHITE=""
    class Style:
        RESET_ALL=""

BANNER = """
 ____   ___   ___  __  __  ____    _  _____  _____       _   _  _____  ____ _  _   ___  
|  _ \ / _ \ / _ \|  \/  |/ ___|  / \|_   _| | ____|    | \ | || ____||  __| || | / _ \ 
| | | | | | | | | | |\/| | |  _  / _ \ | |   |  _|      |  \| ||  _|  | |   | || || (_) |
| |_| | |_| | |_| | |  | | |_| |/ ___ \| |   | |___     | |\  || |___ | |__ | || | \__, |
|____/ \___/ \___/|_|  |_|\____/_/   \_\_|   |_____|    |_| \_||_____||____||_||_|   /_/ 

        "Built on the Intelligence of Four Races" -- by Dumitru Nechita
"""

def _demo_luhn_check(number: str) -> bool:
    digits = [int(d) for d in number if d.isdigit()]
    digits.reverse()
    total = 0
    for i, d in enumerate(digits):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0

def _generate_demo_token(window: int = 30) -> str:
    ts = int(time.time()) // window
    base = hashlib.sha256(f"DEMO_ONLY_{ts}".encode()).hexdigest()
    token_digits = ''.join(filter(str.isdigit, base))[:15]
    total = 0
    for i, d in enumerate(reversed([int(x) for x in token_digits])):
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    check = (10 - (total % 10)) % 10
    return token_digits + str(check)

def level_1():
    print(f"\n{Fore.GREEN}=== LEVEL 1 - Token Validation ==={Style.RESET_ALL}")
    print("Break the time-windowed token system. Expires every 30 seconds.\n")
    attempts = 0
    while attempts < 5:
        guess = input(f"Enter token ({5-attempts} attempts remaining): ").strip()
        attempts += 1
        if not _demo_luhn_check(guess):
            print(f"{Fore.RED}[IRIS] Token failed Luhn validation.{Style.RESET_ALL}")
            continue
        if guess == _generate_demo_token():
            print(f"\n{Fore.GREEN}[CHEVRON 1 - LOCKED] Level 1 CLEARED.{Style.RESET_ALL}\n")
            return True
        print(f"{Fore.YELLOW}Valid Luhn checksum - but wrong token. (Hint: time-based + what else?){Style.RESET_ALL}")
    print(f"\n{Fore.RED}[IRIS PROTOCOL] Session terminated. Keys rotated.{Style.RESET_ALL}\n")
    return False

CHEVRON_CHALLENGES = [
    ("CHEVRON 1", "Layer 3 key exchange algorithm?", "kyber"),
    ("CHEVRON 2", "Minimum onion routing hops?", "3"),
    ("CHEVRON 3", "Hash function for Merkle Tree?", "blake3"),
    ("CHEVRON 4", "Ledger structure replacing blockchain?", "dag"),
    ("CHEVRON 5", "Quantum-safe hash-based signature?", "sphincs+"),
    ("CHEVRON 6", "What triggers the Iris Protocol?", "intrusion"),
    ("CHEVRON 7", "Total factors in Chevron system?", "9"),
    ("CHEVRON 8", "Protocol inspiring anonymous routing?", "i2p"),
    ("CHEVRON 9", "[REDACTED - CLASSIFIED]", "[REDACTED]"),
]

def level_2():
    print(f"\n{Fore.GREEN}=== LEVEL 2 - 9-Chevron Bypass ==={Style.RESET_ALL}")
    print("All 9 chevrons must lock. One wrong answer = session terminated.\n")
    for chevron, question, answer in CHEVRON_CHALLENGES:
        if answer == "[REDACTED]":
            print(f"\n{Fore.RED}[{chevron}] {question}{Style.RESET_ALL}")
            print(f"{Fore.RED}Cannot be answered from public information.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Level 2 - PARTIAL CLEAR (8/9). The gate cannot open without all 9.{Style.RESET_ALL}\n")
            return False
        guess = input(f"[{chevron}] {question}: ").strip().lower()
        if guess == answer:
            print(f"{Fore.GREEN}[{chevron} - LOCKED] OK{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}[IRIS] Wrong on {chevron}. Unanimous consensus failed.{Style.RESET_ALL}\n")
            return False
    return True

def level_3():
    print(f"\n{Fore.GREEN}=== LEVEL 3 - Iris Protocol ==={Style.RESET_ALL}")
    challenge = hashlib.sha256(os.urandom(32)).hexdigest()[:16]
    print(f"[IRIS] Challenge nonce: {challenge}")
    print("Compute: BLAKE3(nonce + secret) - submit first 8 hex chars.")
    print(f"{Fore.RED}You don't have the secret. That's the point.{Style.RESET_ALL}\n")
    start = time.time()
    input("Bypass signature (10 sec): ")
    if time.time() - start > 10:
        print(f"{Fore.RED}[IRIS] Time expired.{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.RED}[IRIS] Signature invalid. Level 3 - UNSOLVED (by design).{Style.RESET_ALL}\n")
    return False

def level_4():
    print(f"\n{Fore.RED}=== LEVEL 4 - Master Key Reconstruction ==={Style.RESET_ALL}")
    print("\nThis level has never been solved.")
    print("Requires: Fragment 1 (author only) + Fragment 2 (heir) + Fragment 3 (DAG)")
    print("+ Delta Nechita parameter + Genesis microsecond timestamp")
    print(f"\n{Fore.RED}If you believe you solved this - contact @nDumitru immediately.{Style.RESET_ALL}\n")
    return False

def main():
    parser = argparse.ArgumentParser(description="D00MGATE-NECH9 CTF Challenge")
    parser.add_argument("--level", type=int, choices=[1,2,3,4], default=1)
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    print(BANNER)
    print("D00MGATE-NECH9 CTF Challenge - Public Demo")
    print("Copyright (c) 2026 Dumitru Nechita")
    print("Core protocol mechanics are redacted.\n")
    levels = {1: level_1, 2: level_2, 3: level_3, 4: level_4}
    if args.all:
        for i in range(1, 5):
            if not levels[i]() and i < 3:
                break
    else:
        levels[args.level]()

if __name__ == "__main__":
    main()
