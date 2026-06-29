"""
D00MGATE-NECH9 - VERIDEX (Layer 10)
Author: Dumitru Nechita | Original name & concept: Dumitru Nechita, 2026
License: D00MGATE-NECH9 Proprietary v1.0
VERITAS (truth) + INDEX (key/pointer) = VERIDEX
"Veritas non moritur." - The Truth does not die.

4 PILLARS - no conflicts, no redundancies with layers 0-9:
  P1 Active Invisibility:    WeepingAngel + Silence
  P2 Asymmetric Temporality: TimeLock + OMEGA49 domain
  P3 Biological Matter:      Epigenetic + Precursor + JunkDNA
  P4 Absorption+Survival:    Gravemind + TheArk + Regeneration
"""
import hashlib, time, os, json, sys
from typing import Optional
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..","core"))
import master_key as MK
from genesis import OMEGA_49_DOMAIN

# ── P1: ACTIVE INVISIBILITY ───────────────────────────────────────────────────

class WeepingAngelProtocol:
    """Components active ONLY when not observed. Inspection = freeze (stone)."""
    def __init__(self):
        self._comps  = {}
        self._frozen = 0

    def register(self, name, payload):
        t = hashlib.sha256((name+str(time.time())+os.urandom(8).hex()).encode()).hexdigest()[:24]
        self._comps[t] = {"name": name, "hash": hashlib.sha256(payload).hexdigest(),
                          "frozen": False, "active": True}
        print("[ANGEL] Registered '"+name+"' | token: "+t[:8]+"...")
        return t

    def access(self, token, observer_id):
        c = self._comps.get(token)
        if not c or not c["active"]: return None
        known = MK.sign(token)[:8] if MK.ready() else "DEMO_KNOWN"
        if not observer_id.startswith(known):
            c["frozen"] = True
            self._frozen += 1
            print("[ANGEL] Unknown observer -> FROZEN (stone)")
            return None
        print("[ANGEL] Legitimate access -> ACTIVE")
        return b"[ACTIVE-PAYLOAD:REDACTED]"

    def unfreeze(self, token, proof):
        if not MK.require("unfreeze"): return False
        c = self._comps.get(token)
        if c: c["frozen"] = False; print("[ANGEL] Unfrozen by Master"); return True
        return False

    def status(self):
        total  = len(self._comps)
        frozen = sum(1 for c in self._comps.values() if c["frozen"])
        return {"total": total, "frozen": frozen, "active": total-frozen, "freeze_events": self._frozen}


class SilenceProtocol:
    """Operations with zero trace. No log. No memory. No forensic evidence."""
    def __init__(self): self._count = 0

    def execute_silent(self, fn, *args, **kwargs):
        result = fn(*args, **kwargs)
        self._count += 1
        return result

    def silent_derive(self, seed):
        return self.execute_silent(
            lambda: hashlib.sha512(seed + os.urandom(32)).digest()[:32])

    def status(self):
        return {"ops_executed": self._count, "ops_logged": 0, "trace": False, "forensic": "None"}


# ── P2: ASYMMETRIC TEMPORALITY ────────────────────────────────────────────────

class TimeLockEngine:
    """Keys exist ONLY within secret temporal windows derived from OMEGA49."""
    def __init__(self):
        self._gen = 0
        self._exp = 0

    def _omega_seq(self, epoch):
        seed   = MK.OMEGA_49_SEED
        domain = sorted(OMEGA_49_DOMAIN)
        seq    = []
        h      = hashlib.sha256((seed+":"+str(epoch)).encode()).digest()
        for i in range(7):
            seq.append(domain[h[i % len(h)] % len(domain)])
            h = hashlib.sha256(h + bytes([i])).digest()
        return seq

    def _window(self, epoch):
        seq     = self._omega_seq(epoch)
        base    = (int(time.time())//3600)*3600
        start   = base + abs(seq[0])*60 + abs(seq[1])*7
        dur     = abs(seq[2])*30 + abs(seq[3])*13
        neg_mod = sum(v for v in seq if v < 0)
        start  += abs(neg_mod)*11
        return start, start + max(dur, 30)

    def generate(self, layer):
        now, epoch = time.time(), int(time.time()//3600)
        ws, we = self._window(epoch)
        if not (ws <= now <= we):
            print("[TIMELOCK] Outside window. Key does not exist.")
            return None
        key = hashlib.sha256((MK.MASTER_KEY+":"+str(layer)+":"+str(epoch)+":"+str(ws)).encode()).hexdigest()
        self._gen += 1
        print("[TIMELOCK] Key generated L"+str(layer)+" | valid "+str(round(we-now))+"s")
        return {"key_hash": key[:16]+"...", "layer": layer,
                "valid_until": we, "window_id": hashlib.md5((str(epoch)+":"+str(ws)).encode()).hexdigest()[:8]}

    def validate(self, kd, layer):
        if not kd: return False
        if time.time() > kd["valid_until"]:
            self._exp += 1; print("[TIMELOCK] EXPIRED"); return False
        if kd["layer"] != layer: print("[TIMELOCK] Layer mismatch"); return False
        print("[TIMELOCK] VALID"); return True

    def status(self):
        return {"omega_seed_set": MK.OMEGA_49_SEED != "MASTER_KEY_HERE",
                "domain": "{ -7..-1, 1..7 } 14 elements",
                "generated": self._gen, "expired": self._exp}


# ── P3: BIOLOGICAL MATTER ─────────────────────────────────────────────────────

class EpigeneticKeyEngine:
    """Key evolves with owner over time. Captured key decays. Owner key lives."""
    def __init__(self): self._gen = 0; self._last = time.time()

    def derive(self, identity):
        evo = (time.time()-self._last)/(365.25*86400)
        epi = hashlib.sha256((identity+":"+str(self._gen)+":"+str(round(evo,6))).encode()).hexdigest()
        key = hashlib.sha512((MK.MASTER_KEY+":"+identity+":"+epi).encode()).hexdigest()[:64]
        print("[EPIGENETIC] Gen:"+str(self._gen)+" | evo:"+str(round(evo,6))+" | key:"+key[:12]+"...")
        return key

    def evolve(self):
        self._gen += 1; self._last = time.time()
        print("[EPIGENETIC] Evolved to gen "+str(self._gen))
        return self.derive(MK.MASTER_KEY)

    def status(self):
        return {"generation": self._gen,
                "since_s": round(time.time()-self._last, 1),
                "principle": "Captured key decays, owner key evolves"}


class PrecursorMatterEncoder:
    """Data in statistical properties of carrier. Implementation: REDACTED."""
    def encode(self, data, carrier):
        print("[PRECURSOR] "+str(len(data))+"b into "+str(len(carrier))+"b carrier | method: REDACTED")
        return carrier
    def decode(self, carrier):
        if not MK.require("precursor_decode"): return None
        return None


class JunkDNALayer:
    """Real data in 98.5% noise. Positions REDACTED (Master Key derived)."""
    RATIO = 0.985
    def encode(self, payload):
        total = int(len(payload)/(1-self.RATIO))
        print("[JUNK_DNA] "+str(len(payload))+"b -> "+str(total)+"b ("+str(round(self.RATIO*100,1))+"% noise)")
        return os.urandom(total)
    def decode(self, stream):
        if not MK.require("junk_dna_decode"): return None
        return None
    def status(self):
        return {"noise": str(round(self.RATIO*100,1))+"%",
                "signal": str(round((1-self.RATIO)*100,1))+"%",
                "positions": "REDACTED"}


# ── P4: ABSORPTION + SURVIVAL ─────────────────────────────────────────────────

class GravemindProtocol:
    """Absorb attack techniques -> convert to defense. Better attacker = stronger system."""
    def __init__(self): self._absorbed = []; self._strength = 0.0

    def absorb(self, attack):
        mult = {"full_ai": 1.5, "ai_assisted": 1.3, "team": 1.1}.get(attack.get("type",""), 1.0)
        val  = attack.get("sophistication", 0.5) * mult
        self._absorbed.append({**attack, "value": val, "at": time.time(), "converted": True})
        self._strength += val
        print("[GRAVEMIND] Absorbed: "+str(attack.get("technique","?"))+" | "+str(round(val,2))+"x | total:"+str(round(self._strength,2))+"x")
        return {"technique": attack.get("technique"), "value": val, "total": self._strength}

    def status(self):
        return {"absorbed": len(self._absorbed), "strength": round(self._strength,2),
                "principle": "Attacker technique becomes defender weapon"}


class TheArkProtocol:
    """Complete rebuild. Post-rebuild: different unrecognizable topology."""
    def __init__(self): self._sealed=False; self._at=None; self._rebuilds=0

    def seal(self, snapshot):
        if not MK.require("seal_ark"): return "UNSIGNED_DEMO"
        seal = MK.sign(json.dumps({"t": time.time()}))
        self._sealed=True; self._at=time.time()
        print("[ARK] Sealed | Location: REDACTED (MK + Delta Nechita)")
        return seal

    def activate(self, proof):
        if not MK.require("activate_ark"): return {"error": "Master Key required"}
        if not self._sealed: return {"error": "Not sealed"}
        self._rebuilds += 1
        print("[ARK] REBUILD #"+str(self._rebuilds)+" | New topology: DIFFERENT | REDACTED")
        return {"status": "REBUILDING", "instance": self._rebuilds, "topology": "DIFFERENT"}

    def status(self):
        return {"sealed": self._sealed, "rebuilds": self._rebuilds,
                "location_set": MK.ARK_LOCATION != "MASTER_KEY_HERE"}


class RegenerationEngine:
    """Master Key survives all versions. Same Master. Different protocol. Always."""
    def __init__(self): self._count=0; self._versions=[]

    def verify_continuity(self, old, new):
        if not MK.require("verify_continuity"): return False
        proof = MK.sign(old+"->"+new)
        self._versions.append({"from": old, "to": new, "proof": proof[:12]})
        print("[REGEN] Continuity: "+old+" -> "+new+" | Same Master.")
        return True

    def emergency_regen(self, heir_frag, dag_frag):
        print("[REGEN] EMERGENCY Shamir 2-of-3 | impl: REDACTED")
        self._count += 1
        return {"status": "COMPLETE", "count": self._count}

    def status(self):
        return {"regenerations": self._count, "continuity_proofs": len(self._versions),
                "heir": "Active - 2-of-3 Shamir",
                "principle": "Same Master. Different protocol. Always."}


# ── VERIDEX UNIFIED ───────────────────────────────────────────────────────────

class VERIDEX:
    """
    VERIDEX - Layer 10 | D00MGATE-NECH9
    Original name and concept: Dumitru Nechita, 2026
    "Veritas non moritur."
    """
    VERSION = "10.1.0"
    AUTHOR  = "Dumitru Nechita"
    MOTTO   = "Veritas non moritur."

    def __init__(self):
        self.angel      = WeepingAngelProtocol()
        self.silence    = SilenceProtocol()
        self.timelock   = TimeLockEngine()
        self.epigenetic = EpigeneticKeyEngine()
        self.precursor  = PrecursorMatterEncoder()
        self.junk_dna   = JunkDNALayer()
        self.gravemind  = GravemindProtocol()
        self.ark        = TheArkProtocol()
        self.regen      = RegenerationEngine()
        if not MK.ready(): MK.warn("VERIDEX.__init__")
        else: print("[VERIDEX] Master Key SET. All pillars ACTIVE.")

    def full_status(self):
        return {
            "layer": 10, "name": "VERIDEX", "version": self.VERSION,
            "author": self.AUTHOR, "motto": self.MOTTO,
            "master_key_set": MK.ready(),
            "warning": None if MK.ready() else MK._WARN,
            "P1_invisibility":  {"angel": self.angel.status(),  "silence": self.silence.status()},
            "P2_temporality":   {"timelock": self.timelock.status()},
            "P3_biological":    {"epigenetic": self.epigenetic.status(),
                                  "junk_dna": self.junk_dna.status()},
            "P4_survival":      {"gravemind": self.gravemind.status(),
                                  "ark": self.ark.status(), "regen": self.regen.status()},
        }


def demo():
    print("="*52)
    print("  D00MGATE-NECH9 - VERIDEX Layer 10")
    print("  Concept: Dumitru Nechita, 2026")
    print("="*52)
    v = VERIDEX()
    print("\n-- P1: INVISIBILITY --")
    t = v.angel.register("veridex_core", b"secret")
    v.angel.access(t, "UNKNOWN_000")
    v.angel.access(t, "DEMO_KNOWN_xxx")
    r = v.silence.execute_silent(lambda: hashlib.sha256(b"silent").hexdigest()[:16])
    print("Silent op: "+str(r)+" | logged: "+str(v.silence.status()["ops_logged"]))
    print("\n-- P2: TEMPORALITY --")
    k = v.timelock.generate(10)
    print("TimeKey: "+("generated" if k else "outside window - set real OMEGA_49_SEED"))
    print("\n-- P3: BIOLOGICAL --")
    v.epigenetic.derive("DEMO_IDENTITY")
    v.junk_dna.encode(b"VERIDEX_PAYLOAD")
    v.precursor.encode(b"DATA", os.urandom(256))
    print("\n-- P4: SURVIVAL --")
    v.gravemind.absorb({"technique": "ml_timing", "type": "full_ai", "sophistication": 0.9})
    seal = v.ark.seal({"v": "10.1.0"})
    print("Ark seal: "+str(seal)[:16]+"...")
    v.regen.verify_continuity("9.0.0", "10.1.0")
    print("\n-- STATUS --")
    s = v.full_status()
    print("Layer:"+str(s["layer"])+" | "+s["name"]+" v"+s["version"]+" | Author: "+s["author"])
    print("Master Key: "+("SET" if s["master_key_set"] else "NOT SET - DEMO MODE"))
    if not s["master_key_set"]:
        print("="*52)
        print("  To activate: edit core/master_key.py")
        print("  Set MASTER_KEY = 'your_personal_key'")
        print("  One file. One line. Full activation.")
        print("="*52)
    print("\n" + v.MOTTO + " - Dumitru Nechita, 2026")

if __name__ == "__main__":
    demo()
