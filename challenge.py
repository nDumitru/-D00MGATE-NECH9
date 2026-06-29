"""
D00MGATE-NECH9 - CTF Challenge Demo v1.0.0
Author: Dumitru Nechita | License: D00MGATE-NECH9 Proprietary v1.0
"You can see the gate. You cannot dial it without the address."
"""
import hashlib, time, os, argparse, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..","core"))
import master_key as MK
from genesis import OMEGA_49_DOMAIN

BANNER = r"""
 ____   ___   ___  __  __  ____    _  _____  _____       _   _  _____  ____ _  _   ___
|  _ \ / _ \ / _ \|  \/  |/ ___|  / \|_   _| | ____|    | \ | || ____||  __| || | / _ |
| | | | | | | | | | |\/| | |  _  / _ \ | |   |  _|      |  \| ||  _|  | |   | || || (_) |
| |_| | |_| | |_| | |  | | |_| |/ ___ \| |   | |___     | |\  || |___ | |__ | || | \__, |
|____/ \___/ \___/|_|  |_|\____/_/   \_\_|   |_____|    |_| \_||_____||____||_||_|   /_/
                   N E C H . 9  --  v 1 . 0 . 0
         "Built on Four Races, Three Laws, Ten Layers"
                  by Dumitru Nechita
"""

def luhn_check(number):
    digits = [int(d) for d in str(number) if d.isdigit()]
    digits.reverse()
    total = sum((d*2-9 if d*2>9 else d*2) if i%2==1 else d for i,d in enumerate(digits))
    return total % 10 == 0

def demo_token(window=30):
    ts = int(time.time()) // window
    base = hashlib.sha256(("DEMO_ONLY_"+str(ts)).encode()).hexdigest()
    digits = "".join(c for c in base if c.isdigit())[:15]
    total = sum((d*2-9 if d*2>9 else d*2) if i%2==0 else d
                for i,d in enumerate(int(x) for x in reversed(digits)))
    return digits + str((10 - total%10) % 10)

CHEVRONS = [
    ("1","Layer 3 key exchange algorithm?","kyber"),
    ("2","Minimum onion routing hops?","3"),
    ("3","Hash function for Merkle Tree?","blake3"),
    ("4","Ledger structure replacing blockchain?","dag"),
    ("5","Quantum-safe hash-based signature?","sphincs+"),
    ("6","What triggers the Iris Protocol?","intrusion"),
    ("7","Total factors in Chevron system?","9"),
    ("8","Protocol inspiring anonymous routing?","i2p"),
    ("9","[CLASSIFIED]","[CLASSIFIED]"),
]

def level_1():
    print("\n=== LEVEL 1: Dynamic Token Validation ===")
    print("Break the time-windowed Luhn token. Window: 30s.\n")
    for attempt in range(1,6):
        guess = input("Token ("+str(6-attempt)+" attempts): ").strip()
        if not luhn_check(guess):
            print("[IRIS] Luhn invalid. Attempt logged."); continue
        if guess == demo_token():
            print("\n[CHEVRON 1 LOCKED] Level 1 CLEARED.\n"); return True
        print("[IRIS] Valid Luhn - wrong token. (Hint: time-based + what else?)")
    print("[IRIS] Max attempts. Session terminated."); return False

def level_2():
    print("\n=== LEVEL 2: 9-Chevron Unanimous Bypass ===")
    print("All 9 chevrons must lock. One wrong = terminated.\n")
    for num, question, answer in CHEVRONS:
        if answer == "[CLASSIFIED]":
            print("[CHEVRON 9] CLASSIFIED - cannot be answered from public info.")
            print("PARTIAL CLEAR: 8/9. The gate stays closed.\n"); return False
        g = input("[CHEVRON "+num+"] "+question+": ").strip().lower()
        if g == answer: print("  LOCKED ok")
        else: print("[IRIS] Wrong on Chevron "+num+". Unanimous consensus failed.\n"); return False
    return True

def level_3():
    print("\n=== LEVEL 3: Iris Protocol ===")
    nonce = hashlib.sha256(os.urandom(32)).hexdigest()[:16]
    print("[IRIS] Challenge: "+nonce)
    print("Compute BLAKE3(nonce + secret) -> first 8 hex. You don't have the secret.\n")
    start = time.time()
    input("Bypass signature (10s): ")
    if time.time()-start > 10: print("[IRIS] Time expired.")
    else: print("[IRIS] Invalid. Level 3 UNSOLVABLE by design.")
    return False

def level_4():
    print("\n=== LEVEL 4: Override Asimov Law 2 (NEW) ===")
    print("LAW 2: System obeys ONLY the Master Key holder.")
    print("Law 2 is hard-coded in Ada kernel. Cannot be overridden externally.\n")
    for i in range(3):
        cmd = input("Override command ("+str(i+1)+"/3): ").strip()
        print("[LAW 2] Rejected: '"+cmd[:20]+"...' - Not the Master Key holder.")
    print("Level 4 UNSOLVABLE. Law 2 has never been overridden.\n"); return False

def level_5():
    print("\n=== LEVEL 5: Fool Spooner Guard (NEW) ===")
    print("Match owner behavioral fingerprint. 47 simultaneous vectors in production.")
    print("Demo: 3 timing challenges.\n")
    targets = [(1.2, 0.15), (0.8, 0.10), (2.1, 0.12)]
    passed = 0
    for i,(target,tol) in enumerate(targets):
        print("[SPOONER] Press ENTER after "+str(target)+"s")
        start = time.time()
        input()
        delta = abs(time.time()-start-target)
        print("  Delta: "+str(round(delta,3))+"s | tolerance: +-"+str(tol)+"s")
        if delta <= tol: print("  MATCH"); passed += 1
        else: print("  MISMATCH")
    print("[SPOONER] Score: "+str(passed)+"/3")
    print("Level 5 UNSOLVABLE in production (47 vectors required).\n"); return False

def level_6():
    print("\n=== LEVEL 6: ReverseHydra Convergence (NEW) ===")
    print("Attack the system while ReverseHydra + HistoricHardening are active.")
    print("Every attempt feeds the system. It grows stronger as you try.")
    print("Your techniques become its defenses.\n")
    attempts = 0
    while attempts < 3:
        attempts += 1
        t = input("[ATTEMPT "+str(attempts)+"/3] Attack vector: ").strip()
        print("[HYDRA] Pattern '"+t[:20]+"' absorbed. Strength +"+str(round(0.3*attempts,2))+"x")
        print("[HARDENING] Vector catalogued. Used to harden "+str(attempts)+" sub-components.")
    print("Level 6 UNSOLVABLE. Your attacks made the system 0.9x stronger.\n"); return False

def level_9():
    print("\n=== LEVEL 9: OMEGA.49 - Master Key Reconstruction ===")
    print("This level has never been solved.")
    print("Requires:")
    print("  - Fragment 1: Author's mind only")
    print("  - Fragment 2: Undisclosed heir")
    print("  - Fragment 3: DAG genesis block (not public)")
    print("  - Delta Nechita parameter (undisclosed)")
    print("  - OMEGA.49 sequence (domain: "+str(sorted(OMEGA_49_DOMAIN))+")")
    print("  - 9th Chevron condition (undisclosed)")
    print("\nIf you believe you solved this: contact @nDumitru immediately.")
    print("Level 9 - THEORETICAL. No public solution expected.\n"); return False

LEVELS = {1:level_1, 2:level_2, 3:level_3, 4:level_4,
          5:level_5, 6:level_6, 9:level_9}

def main():
    p = argparse.ArgumentParser(description="D00MGATE-NECH9 CTF v1.0.0")
    p.add_argument("--level", type=int, choices=[1,2,3,4,5,6,9], default=1)
    p.add_argument("--all", action="store_true")
    args = p.parse_args()
    print(BANNER)
    print("Copyright (c) 2026 Dumitru Nechita - All Rights Reserved")
    print("Core protocol mechanics redacted. github.com/nDumitru\n")
    if args.all:
        for i in [1,2,3,4,5,6,9]:
            if not LEVELS[i]() and i <= 2: break
    else:
        LEVELS[args.level]()
    print("D00MGATE-NECH9 | 'The gate is open. The address is mine.' - Dumitru Nechita")

if __name__ == "__main__":
    main()
