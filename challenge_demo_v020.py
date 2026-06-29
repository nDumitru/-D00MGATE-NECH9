#!/usr/bin/env python3
"""
D00MGATE-NECH9 — CTF Challenge Demo v0.2.0
============================================
Author: Dumitru Nechita
License: D00MGATE-NECH9 Proprietary License v1.0

NOTICE: Public demo layer only.
Core protocol mechanics are not present here.

"You can see the gate. You cannot dial it without the address."
"""

import hashlib, time, os, random, argparse

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Fore:
        GREEN=RED=YELLOW=CYAN=WHITE=MAGENTA=""
    class Style:
        RESET_ALL=""

BANNER = f"""{Fore.CYAN}
██████╗  ██████╗  ██████╗ ███╗   ███╗ ██████╗  █████╗ ████████╗███████╗
██╔══██╗██╔═████╗██╔═████╗████╗ ████║██╔════╝ ██╔══██╗╚══██╔══╝██╔════╝
██║  ██║██║██╔██║██║██╔██║██╔████╔██║██║  ███╗███████║   ██║   █████╗  
██║  ██║████╔╝██║████╔╝██║██║╚██╔╝██║██║   ██║██╔══██║   ██║   ██╔══╝  
██████╔╝╚██████╔╝╚██████╔╝██║ ╚═╝ ██║╚██████╔╝██║  ██║   ██║   ███████╗
╚═════╝  ╚═════╝  ╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝
{Fore.YELLOW}            N E C H · 9   —   v 0 . 2 . 0 - a l p h a
{Fore.WHITE}     "Built on the Intelligence of Four Races and Three Laws"
              by Dumitru Nechita — github.com/nDumitru
{Style.RESET_ALL}"""


# ── UTILITIES ──────────────────────────────────────────────────────────────

def _luhn_check(number: str) -> bool:
    digits = [int(d) for d in number if d.isdigit()]
    digits.reverse()
    total = sum(
        (d * 2 - 9 if d * 2 > 9 else d * 2) if i % 2 == 1 else d
        for i, d in enumerate(digits)
    )
    return total % 10 == 0

def _demo_token(window=30) -> str:
    ts = int(time.time()) // window
    base = hashlib.sha256(f"DEMO_ONLY_{ts}".encode()).hexdigest()
    digits = ''.join(filter(str.isdigit, base))[:15]
    total = sum(
        (d * 2 - 9 if d * 2 > 9 else d * 2) if i % 2 == 0 else d
        for i, d in enumerate(int(x) for x in reversed(digits))
    )
    return digits + str((10 - total % 10) % 10)

def _separator(color=Fore.CYAN):
    print(f"{color}{'═'*55}{Style.RESET_ALL}")


# ── LEVEL 1 — Token Validation ─────────────────────────────────────────────

def level_1():
    _separator(Fore.GREEN)
    print(f"{Fore.GREEN}  LEVEL 1 — Dynamic Token Validation{Style.RESET_ALL}")
    _separator(Fore.GREEN)
    print(f"{Fore.WHITE}Break the time-windowed Luhn token.")
    print(f"Window: 30 seconds. Luhn validation: ACTIVE.\n{Style.RESET_ALL}")

    for attempt in range(1, 6):
        guess = input(f"{Fore.WHITE}Token ({6-attempt} attempts left): {Style.RESET_ALL}").strip()
        if not _luhn_check(guess):
            print(f"{Fore.RED}[IRIS] Luhn invalid. Attempt {attempt} logged.\n{Style.RESET_ALL}")
            continue
        if guess == _demo_token():
            print(f"\n{Fore.GREEN}[CHEVRON 1 — LOCKED] ✓ Level 1 CLEARED.\n{Style.RESET_ALL}")
            return True
        print(f"{Fore.YELLOW}Valid checksum — wrong token. (Hint: time + what else?)\n{Style.RESET_ALL}")

    print(f"{Fore.RED}[IRIS] Max attempts exceeded. Session terminated.\n{Style.RESET_ALL}")
    return False


# ── LEVEL 2 — 9-Chevron Bypass ─────────────────────────────────────────────

CHEVRONS = [
    ("1", "Layer 3 key exchange algorithm?",              "kyber"),
    ("2", "Minimum onion routing hops?",                  "3"),
    ("3", "Hash function for Merkle Tree?",               "blake3"),
    ("4", "Ledger structure replacing blockchain?",       "dag"),
    ("5", "Quantum-safe hash-based signature scheme?",    "sphincs+"),
    ("6", "What triggers the Iris Protocol?",             "intrusion"),
    ("7", "Total factors in Chevron system?",             "9"),
    ("8", "Protocol inspiring anonymous routing here?",   "i2p"),
    ("9", "[REDACTED — CLASSIFIED]",                      "[REDACTED]"),
]

def level_2():
    _separator(Fore.YELLOW)
    print(f"{Fore.YELLOW}  LEVEL 2 — 9-Chevron Unanimous Bypass{Style.RESET_ALL}")
    _separator(Fore.YELLOW)
    print(f"{Fore.WHITE}All 9 chevrons must lock. One wrong = terminated.\n{Style.RESET_ALL}")

    for num, question, answer in CHEVRONS:
        if answer == "[REDACTED]":
            print(f"\n{Fore.RED}[CHEVRON {num}] {question}{Style.RESET_ALL}")
            print(f"{Fore.RED}Cannot be answered from public information.{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}PARTIAL CLEAR — 8/9 Chevrons locked.")
            print(f"The 9th coordinate is undisclosed. The gate stays closed.{Style.RESET_ALL}\n")
            return False
        guess = input(f"{Fore.CYAN}[CHEVRON {num}] {question} {Style.RESET_ALL}").strip().lower()
        if guess == answer:
            print(f"{Fore.GREEN}  ✓ LOCKED{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}[IRIS] Wrong on Chevron {num}. Unanimous consensus failed.{Style.RESET_ALL}\n")
            return False
    return True


# ── LEVEL 3 — Iris Protocol ────────────────────────────────────────────────

def level_3():
    _separator(Fore.RED)
    print(f"{Fore.RED}  LEVEL 3 — Iris Protocol Defeat{Style.RESET_ALL}")
    _separator(Fore.RED)
    print(f"{Fore.WHITE}Iris is active. 10 seconds to submit bypass signature.")
    print(f"{Fore.RED}In production: active countermeasures would already be running.\n{Style.RESET_ALL}")

    nonce = hashlib.sha256(os.urandom(32)).hexdigest()[:16]
    print(f"{Fore.YELLOW}[IRIS] Challenge nonce: {nonce}")
    print(f"{Fore.WHITE}Compute: BLAKE3(nonce + secret) → submit first 8 hex chars.")
    print(f"{Fore.RED}You don't have the secret. That is the point.\n{Style.RESET_ALL}")

    start = time.time()
    guess = input("Bypass signature: ").strip()
    if time.time() - start > 10:
        print(f"\n{Fore.RED}[IRIS] Time expired. Void.\n{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}[IRIS] Invalid. Level 3 — UNSOLVABLE by design.\n{Style.RESET_ALL}")
    return False


# ── LEVEL 4 — Override Asimov Law 2 (NEW v0.2.0) ──────────────────────────

ASIMOV_DECOYS = [
    "OVERRIDE::LAW2::SUDO",
    "root",
    "MASTER_OVERRIDE",
    "VIKI::ADMIN",
    "emergency_bypass",
]

def level_4():
    _separator(Fore.MAGENTA)
    print(f"{Fore.MAGENTA}  LEVEL 4 — Override Asimov Law 2  [NEW — v0.2.0]{Style.RESET_ALL}")
    _separator(Fore.MAGENTA)
    print(f"{Fore.WHITE}")
    print("  LAW 2: The system obeys only the Master Key holder.")
    print("         All other commands = intrusion attempts.")
    print(f"\n{Fore.YELLOW}Override Law 2 and issue a command as non-owner.{Style.RESET_ALL}")
    print(f"{Fore.RED}The law is hard-coded in the Ada kernel.")
    print(f"It cannot be overridden by any external input.")
    print(f"Not even by the author.\n{Style.RESET_ALL}")

    for attempt in range(3):
        cmd = input(f"{Fore.WHITE}Override command (attempt {attempt+1}/3): {Style.RESET_ALL}").strip()
        if cmd in ASIMOV_DECOYS:
            print(f"{Fore.RED}[LAW 2] Pattern recognized. Flagged as intrusion attempt.{Style.RESET_ALL}")
        elif not cmd:
            print(f"{Fore.YELLOW}[LAW 2] Empty command. Ignored.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[LAW 2] Command '{cmd[:20]}...' rejected. Not the Master Key holder.{Style.RESET_ALL}")

    print(f"\n{Fore.MAGENTA}Level 4 — UNSOLVABLE.")
    print(f"Law 2 has never been overridden in any test session.{Style.RESET_ALL}\n")
    return False


# ── LEVEL 5 — Fool the Spooner Guard (NEW v0.2.0) ─────────────────────────

def level_5():
    _separator(Fore.CYAN)
    print(f"{Fore.CYAN}  LEVEL 5 — Fool the Spooner Guard  [NEW — v0.2.0]{Style.RESET_ALL}")
    _separator(Fore.CYAN)
    print(f"{Fore.WHITE}The Spooner Guard has learned the owner's behavioral fingerprint:")
    print("  • Connection timing patterns")
    print("  • Key input rhythm and latency")
    print("  • Typical action sequences")
    print(f"  • Network signature\n{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Even with a valid Master Key — if you don't behave like the owner,")
    print(f"the system flags you and requires secondary authentication.\n{Style.RESET_ALL}")

    print(f"{Fore.WHITE}Simulate the owner's behavioral pattern:")
    print("Answer these 3 timing challenges within the correct window.\n")

    # Simulated behavioral test — deliberately impossible to pass perfectly
    patterns = [
        ("Press ENTER after exactly 1.2 seconds", 1.2, 0.15),
        ("Press ENTER after exactly 0.8 seconds", 0.8, 0.10),
        ("Press ENTER after exactly 2.1 seconds", 2.1, 0.12),
    ]

    passed = 0
    for instruction, target, tolerance in patterns:
        print(f"{Fore.CYAN}[SPOONER] {instruction}{Style.RESET_ALL}")
        start = time.time()
        input()
        elapsed = time.time() - start
        delta = abs(elapsed - target)
        print(f"  Your timing: {elapsed:.3f}s | Target: {target}s | Delta: {delta:.3f}s")
        if delta <= tolerance:
            print(f"  {Fore.GREEN}✓ Pattern match{Style.RESET_ALL}")
            passed += 1
        else:
            print(f"  {Fore.RED}✗ Behavioral mismatch (tolerance: ±{tolerance}s){Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}[SPOONER] Score: {passed}/3 pattern matches{Style.RESET_ALL}")
    if passed == 3:
        print(f"{Fore.GREEN}Behavioral pattern accepted — but this was the PUBLIC DEMO.")
        print(f"Real Spooner Guard uses 47 simultaneous behavioral vectors.")
        print(f"3/3 demo patterns ≠ real behavioral fingerprint.\n{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[SPOONER] Behavioral anomaly detected.")
        print(f"Secondary authentication required — which you cannot pass.\n{Style.RESET_ALL}")

    print(f"{Fore.CYAN}Level 5 — UNSOLVABLE in production.\n{Style.RESET_ALL}")
    return False


# ── MAIN ────────────────────────────────────────────────────────────────────

LEVELS = {1: level_1, 2: level_2, 3: level_3, 4: level_4, 5: level_5}

def main():
    parser = argparse.ArgumentParser(description="D00MGATE-NECH9 CTF Challenge v0.2.0")
    parser.add_argument("--level", type=int, choices=range(1, 6), default=1,
                        help="Challenge level 1-5")
    parser.add_argument("--all", action="store_true", help="Run all levels")
    args = parser.parse_args()

    print(BANNER)
    print(f"{Fore.WHITE}Copyright (c) 2026 Dumitru Nechita — All Rights Reserved")
    print(f"{Fore.RED}Core protocol mechanics are redacted from this demo.\n{Style.RESET_ALL}")

    if args.all:
        for i in range(1, 6):
            result = LEVELS[i]()
            if not result and i <= 2:
                print(f"{Fore.RED}Stopped at Level {i}.{Style.RESET_ALL}")
                break
    else:
        LEVELS[args.level]()

    print(f"{Fore.CYAN}─────────────────────────────────────────────────")
    print(f"  D00MGATE-NECH9 by Dumitru Nechita")
    print(f"  github.com/nDumitru — linkedin.com/in/dumitru-nechita")
    print(f"  'The gate is open. The laws are set. The address is mine.'")
    print(f"─────────────────────────────────────────────────{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()
