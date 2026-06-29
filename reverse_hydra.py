"""
D00MGATE-NECH9 - ReverseHydra Evolution Engine
Author: Dumitru Nechita | Original concept: Dumitru Nechita, 2026
License: D00MGATE-NECH9 Proprietary v1.0

PRINCIPLE: Every break - human OR AI - feeds the system.
  Human break   -> 2 heads spawned
  AI-Assisted   -> 3 heads spawned
  Full AI       -> 4 heads (punished MORE - systematic = more replication risk)
  Team          -> 3 heads
  Generation N  -> split^N heads (exponential)
  Layer 9       -> NEVER evolves via any external trigger
Master Key signature required for EVERY evolution.
Layer stays OFFLINE until Master signs.
"You killed one head. You fed the others."
"""
import hashlib, time, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..","core"))
import master_key as MK
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

class BreakType(Enum):
    HUMAN       = "human"
    AI_ASSISTED = "ai_assisted"
    FULL_AI     = "full_ai"
    TEAM        = "team"

class HydraState(Enum):
    STABLE         = "stable"
    BROKEN         = "broken"
    PENDING_MASTER = "pending_master"
    MULTI_HEAD     = "multi_head"

class Urgency(Enum):
    INFO     = "INFO"
    WARNING  = "WARNING"
    URGENT   = "URGENT"
    CRITICAL = "CRITICAL"

SPLIT = {
    BreakType.HUMAN: 2, BreakType.AI_ASSISTED: 3,
    BreakType.FULL_AI: 4, BreakType.TEAM: 3,
}
GREEK = ["a","b","g","d","e","z","h","th","i","k","l","m","n","x","o","p"]
IMMUTABLE = 9

@dataclass
class AttackVector:
    layer: int
    break_type: BreakType
    competitor_id: str
    timestamp: float
    attempts: int
    ai_probability: float
    version_broken: str
    pattern: str = ""
    replication_risk: float = 0.0

    def analyze(self):
        p = {
            BreakType.FULL_AI:      ("ml_systematic",      0.92),
            BreakType.HUMAN:        ("human_intuitive",    0.35),
            BreakType.AI_ASSISTED:  ("hybrid_augmented",   0.65),
            BreakType.TEAM:         ("coordinated_multi",  0.45),
        }
        self.pattern, self.replication_risk = p[self.break_type]
        return self

@dataclass
class HydraHead:
    head_id: str
    layer: int
    parent_version: str
    version: str
    created_at: float
    basis: str
    active: bool = True
    generation: int = 1

    def spawn(self, n, attack):
        return [HydraHead(
            head_id=hashlib.sha256((self.head_id+str(i)+str(time.time())).encode()).hexdigest()[:12],
            layer=self.layer, parent_version=self.version,
            version=self.version+"."+str(i+1)+"-"+GREEK[i%len(GREEK)],
            created_at=time.time(), basis="counter-"+attack.pattern+"-v"+str(i+1),
            generation=self.generation+1,
        ) for i in range(n)]

@dataclass
class MasterNotif:
    notif_id: str
    layer: int
    summary: str
    heads_n: int
    created_at: float
    urgency: Urgency = Urgency.INFO
    acked: bool = False

    def escalate(self):
        e = time.time() - self.created_at
        if e > 86400:   self.urgency = Urgency.CRITICAL
        elif e > 21600: self.urgency = Urgency.URGENT
        elif e > 3600:  self.urgency = Urgency.WARNING
        return self.urgency

class ReverseHydraEngine:
    def __init__(self):
        self._states  = {i: HydraState.STABLE for i in range(1, 11)}
        self._heads   = {i: [HydraHead(
            head_id=hashlib.sha256(("GENESIS_L"+str(i)).encode()).hexdigest()[:12],
            layer=i, parent_version="GENESIS", version="1.0",
            created_at=time.time(), basis="GENESIS", generation=1,
        )] for i in range(1, 11)}
        self._history  = []
        self._pending  = []
        self._evol_cnt = 0

    def process_break(self, attack):
        if attack.layer == IMMUTABLE:
            print("[HYDRA] Layer 9 break - IMPOSSIBLE. Master notified CRITICAL.")
            return {"status": "LAYER_9_IMMUTABLE"}
        attack.analyze()
        self._history.append(attack)
        broken = next((h for h in self._heads[attack.layer]
                       if h.version == attack.version_broken and h.active), None)
        if broken: broken.active = False
        n = SPLIT[attack.break_type]
        gen = broken.generation if broken else 1
        if gen > 1:
            n = min(n ** gen, 16)
            print("[HYDRA] Gen-"+str(gen)+" head broken -> exponential split: "+str(n))
        notif = MasterNotif(
            notif_id=hashlib.sha256((str(attack.layer)+str(time.time())).encode()).hexdigest()[:16],
            layer=attack.layer,
            summary="L"+str(attack.layer)+" broken by "+attack.break_type.value+" | pattern:"+attack.pattern+" | risk:"+str(round(attack.replication_risk*100))+"%",
            heads_n=n, created_at=time.time(),
        )
        self._pending.append(notif)
        self._states[attack.layer] = HydraState.PENDING_MASTER
        print("="*52)
        print("  REVERSHYDRA TRIGGERED - Layer " + str(attack.layer))
        print("  Type: "+attack.break_type.value+" | Pattern: "+attack.pattern)
        print("  Replication risk: "+str(round(attack.replication_risk*100))+"%")
        print("  Heads spawning: "+str(n))
        print("  State: OFFLINE - PENDING MASTER SIGNATURE")
        print("  Notification: "+notif.notif_id[:12]+"...")
        print("  Evolution content: REDACTED")
        print("="*52)
        return {"status": "PENDING_MASTER", "layer": attack.layer,
                "heads_to_spawn": n, "notification_id": notif.notif_id}

    def master_acknowledge(self, notif_id, proof):
        if not MK.require("master_acknowledge"): return {"error": "Master Key required"}
        notif = next((n for n in self._pending if n.notif_id == notif_id), None)
        if not notif: return {"error": "Not found"}
        layer = notif.layer
        broken = next((h for h in self._heads[layer] if not h.active), None)
        attack = next((a for a in reversed(self._history) if a.layer == layer), None)
        if broken and attack:
            new_heads = broken.spawn(notif.heads_n, attack)
        else:
            new_heads = [HydraHead(
                head_id=hashlib.sha256(("SPLIT_"+str(layer)+"_"+str(i)+"_"+str(time.time())).encode()).hexdigest()[:12],
                layer=layer, parent_version="1.0", version="2.0-"+GREEK[i],
                created_at=time.time(), basis="hydra-split-"+str(i+1), generation=2,
            ) for i in range(notif.heads_n)]
        self._heads[layer].extend(new_heads)
        self._states[layer] = HydraState.MULTI_HEAD
        self._pending.remove(notif)
        notif.acked = True
        self._evol_cnt += 1
        print("[HYDRA] Evolution complete L"+str(layer)+": "+str(len(new_heads))+" new heads")
        for h in new_heads: print("  -> "+h.version+" | "+h.basis)
        return {"status": "EVOLUTION_COMPLETE", "layer": layer,
                "new_heads": [h.version for h in new_heads],
                "total_evolutions": self._evol_cnt}

    def check_notifications(self):
        return [{"id": n.notif_id[:12], "layer": n.layer,
                 "urgency": n.escalate().value,
                 "hours_pending": round((time.time()-n.created_at)/3600, 1),
                 "heads_waiting": n.heads_n} for n in self._pending]

    def status(self, layer=None):
        if layer:
            heads = [h for h in self._heads.get(layer, []) if h.active]
            return {"layer": layer, "state": self._states[layer].value,
                    "active_heads": len(heads),
                    "versions": [h.version for h in heads]}
        return [self.status(i) for i in range(1, 11)]

def demo():
    print("D00MGATE-NECH9 - ReverseHydra | Concept: Dumitru Nechita")
    e = ReverseHydraEngine()
    r = e.process_break(AttackVector(1, BreakType.FULL_AI, "AI_DEMO",
        time.time(), 50000, 0.97, "1.0"))
    e.master_acknowledge(r["notification_id"], "DEMO")
    e.process_break(AttackVector(2, BreakType.HUMAN, "HUMAN_DEMO",
        time.time(), 843, 0.04, "1.0"))
    print("Pending: " + str(e.check_notifications()))
    for s in e.status():
        if s["active_heads"] > 1:
            print("L"+str(s["layer"])+": "+s["state"]+" | "+str(s["versions"]))
    print("You killed one head. You fed the others.")

if __name__ == "__main__":
    demo()
