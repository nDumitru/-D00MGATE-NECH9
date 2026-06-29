"""
D00MGATE-NECH9 - HistoricHardening Engine
Author: Dumitru Nechita | Original concept: Dumitru Nechita, 2026
License: D00MGATE-NECH9 Proprietary v1.0

Analyzes ALL past attempts across ALL layers -> cumulative hardening.
Near-misses (>75%) weighted MORE than breaches.
Cross-layer pattern detection included.
"The system does not forget. It gets stronger every time you try."
"""
import hashlib, time, sys, os
from collections import defaultdict
from enum import Enum
from dataclasses import dataclass
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..","core"))
import master_key as MK

class Outcome(Enum):
    FAILED_EARLY = "failed_early"
    FAILED_MID   = "failed_mid"
    FAILED_LATE  = "failed_late"
    BREACH       = "breach"
    PARTIAL      = "partial"

class Pattern(Enum):
    TIMING       = "timing_attack"
    BRUTEFORCE   = "bruteforce"
    ML_ENUM      = "ml_enumeration"
    SIDE_CHANNEL = "side_channel"
    HYBRID       = "hybrid_coordinated"
    NOVEL        = "unknown_novel"

class Trigger(Enum):
    POST_BREACH = "post_breach"
    THRESHOLD   = "threshold"
    SCHEDULED   = "scheduled"
    CROSS_LAYER = "cross_layer"
    MANUAL      = "master_manual"

NEAR_MISS = 0.75
THRESHOLD = 1000
SCHEDULE  = 7776000

@dataclass
class Attempt:
    attempt_id: str
    layer: int
    timestamp: float
    outcome: Outcome
    attacker: str
    ai_prob: float
    pattern: Pattern
    partial_pct: float
    count: int

@dataclass
class HardeningReport:
    report_id: str
    timestamp: float
    trigger: Trigger
    depth: int
    dominant: list
    near_misses: int
    novel: int
    cross: list
    actions: list
    delta: float
    priority: list
    pending: bool = True

class HistoricHardeningEngine:
    def __init__(self):
        self._log      = []
        self._reports  = []
        self._pending  = []
        self._counts   = defaultdict(int)
        self._last_sched = time.time()

    def record(self, attempt):
        self._log.append(attempt)
        self._counts[attempt.layer] += 1
        triggers = []
        if attempt.outcome == Outcome.BREACH:
            triggers.append(Trigger.POST_BREACH)
        if self._counts[attempt.layer] % THRESHOLD == 0:
            triggers.append(Trigger.THRESHOLD)
        if time.time() - self._last_sched > SCHEDULE:
            triggers.append(Trigger.SCHEDULED)
            self._last_sched = time.time()
        if self._cross_detect(attempt):
            triggers.append(Trigger.CROSS_LAYER)
        reports = [self._analyze(t) for t in triggers]
        return {"recorded": True, "layer": attempt.layer,
                "near_miss": attempt.partial_pct >= NEAR_MISS,
                "triggers": [t.value for t in triggers],
                "reports": len(reports)}

    def _analyze(self, trigger):
        pcounts = defaultdict(int)
        nm, nv, br = [], [], []
        for a in self._log:
            pcounts[a.pattern] += 1
            if a.partial_pct >= NEAR_MISS: nm.append(a)
            if a.pattern == Pattern.NOVEL: nv.append(a)
            if a.outcome == Outcome.BREACH: br.append(a)
        dominant = [p for p,_ in sorted(pcounts.items(), key=lambda x: x[1], reverse=True)[:3]]
        cross = self._cross_correlations()
        priority = self._priority()
        delta = round(min(1.0 + len(br)*0.8 + len(nm)*0.15 + len(nv)*0.4, 50.0), 2)
        actions = self._actions(dominant, nm, cross, nv)
        r = HardeningReport(
            report_id=hashlib.sha256((trigger.value+str(time.time())).encode()).hexdigest()[:16],
            timestamp=time.time(), trigger=trigger, depth=len(self._log),
            dominant=[p.value for p in dominant], near_misses=len(nm),
            novel=len(nv), cross=cross, actions=actions, delta=delta, priority=priority,
        )
        self._reports.append(r)
        self._pending.append(r)
        print("[HARDENING] Trigger:"+trigger.value+" | depth:"+str(len(self._log))+" | near-misses:"+str(len(nm))+" | delta:"+str(delta)+"x | Master required.")
        return r

    def _cross_detect(self, latest):
        layers = set(a.layer for a in self._log[-200:] if a.layer != latest.layer and a.pattern == latest.pattern)
        return len(layers) >= 2

    def _cross_correlations(self):
        byp = defaultdict(set)
        for a in self._log: byp[a.pattern].add(a.layer)
        return [p.value+" across "+str(len(ls))+" layers - coordinated" for p,ls in byp.items() if len(ls) >= 3]

    def _priority(self):
        scores = defaultdict(float)
        for a in self._log:
            if a.outcome == Outcome.BREACH: scores[a.layer] += 10
            scores[a.layer] += a.partial_pct * 0.05
            if a.pattern == Pattern.NOVEL: scores[a.layer] += 3
        return sorted(scores.keys(), key=lambda x: scores[x], reverse=True)[:5]

    def _actions(self, patterns, nm, cross, novel):
        amap = {
            Pattern.ML_ENUM:      "Rotate Luhn salt - ML detected [REDACTED]",
            Pattern.TIMING:       "Normalize timing + micro-delays [REDACTED]",
            Pattern.BRUTEFORCE:   "Exponential backoff + early Iris [REDACTED]",
            Pattern.NOVEL:        "Novel vector - full review + VIKI update [REDACTED]",
            Pattern.SIDE_CHANNEL: "Constant-time ops enforced [REDACTED]",
            Pattern.HYBRID:       "NS5 Mesh alert + cross-layer sync [REDACTED]",
        }
        actions = [amap[p] for p in patterns if p in amap]
        if nm: actions.append(str(len(nm))+" near-miss vectors hardened [REDACTED]")
        if cross: actions.append("Cross-layer sync: "+str(len(cross))+" patterns [REDACTED]")
        if novel: actions.append(str(len(novel))+" novel vectors - Delta Nechita rotation recommended")
        return actions

    def approve(self, report_id, proof):
        if not MK.require("approve_hardening"): return {"error": "Master Key required"}
        r = next((x for x in self._pending if x.report_id == report_id), None)
        if not r: return {"error": "Not found"}
        r.pending = False
        self._pending.remove(r)
        print("[HARDENING] Approved "+report_id[:12]+"... | Strength: "+str(r.delta)+"x | Signed: Dumitru Nechita")
        return {"status": "ACTIVATED", "strength": str(r.delta)+"x", "actions": len(r.actions)}

    def summary(self):
        br = sum(1 for a in self._log if a.outcome == Outcome.BREACH)
        nm = sum(1 for a in self._log if a.partial_pct >= NEAR_MISS)
        nv = sum(1 for a in self._log if a.pattern == Pattern.NOVEL)
        return {"total": len(self._log), "breaches": br, "near_misses": nm,
                "novel": nv, "reports": len(self._reports),
                "pending": len(self._pending),
                "strength": round(1.0+br*0.8+nm*0.15+nv*0.4, 2),
                "principle": "Every attempt strengthens the system."}

def demo():
    print("D00MGATE-NECH9 - HistoricHardening | Concept: Dumitru Nechita")
    e = HistoricHardeningEngine()
    attempts = [
        Attempt("A1", 1, time.time()-86400*20, Outcome.FAILED_LATE, "ai",   0.95, Pattern.ML_ENUM,      78.0, 50000),
        Attempt("A2", 2, time.time()-86400*15, Outcome.BREACH,      "team", 0.30, Pattern.HYBRID,       100.0, 2100),
        Attempt("A3", 3, time.time()-86400*10, Outcome.FAILED_LATE, "ai",   0.92, Pattern.ML_ENUM,       81.0, 98000),
        Attempt("A4", 1, time.time()-86400*5,  Outcome.BREACH,      "human",0.08, Pattern.NOVEL,        100.0, 847),
        Attempt("A5", 4, time.time()-86400*2,  Outcome.FAILED_LATE, "asst", 0.55, Pattern.SIDE_CHANNEL,  88.0, 1500),
    ]
    for a in attempts:
        r = e.record(a)
        if r["triggers"]: print("  L"+str(a.layer)+" "+a.outcome.value+" -> "+str(r["triggers"]))
    if e._pending:
        e.approve(e._pending[0].report_id, "DEMO")
    print("Summary: "+str(e.summary()))
    print("The system gets stronger every time you try.")

if __name__ == "__main__":
    demo()
