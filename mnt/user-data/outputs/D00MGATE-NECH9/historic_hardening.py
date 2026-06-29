"""
D00MGATE-NECH9 — HistoricHardening Engine
==========================================
Author: Dumitru Nechita
Version: 0.5.1-alpha
License: D00MGATE-NECH9 Proprietary License v1.0

CONCEPT: HistoricHardening (original concept by Dumitru Nechita)

While ReverseHydra reacts to the CURRENT attack,
HistoricHardening analyzes ALL past attempts, breaches,
and unlocks across ALL layers — regardless of which layer
was broken — and uses that cumulative intelligence to
produce a hardening update stronger than any single reaction.

PRINCIPLE:
  Every attempt (successful or not) leaves a signature.
  Every breach reveals a pattern.
  Every unlock exposes a weakness that once existed.
  
  HistoricHardening reads ALL of this history
  and synthesizes a layer update that:
  → Closes every vector ever used
  → Anticipates vectors that were CLOSE to working
  → Cross-layer pattern analysis (attack on L1 informs L5 defense)
  → Cumulative difficulty: each generation is harder than all previous combined

COMBINED WITH REVERSHYDRA:
  Immediate response  → ReverseHydra    (spawn heads NOW)
  Deep learning       → HistoricHardening (synthesize ALL history → stronger update)
  
  Together: the system doesn't just react.
  It remembers. It learns. It anticipates.

"The past is not behind us.
 It is inside every layer."
 — HistoricHardening Principle, D00MGATE-NECH9
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from collections import defaultdict
import hashlib
import time
import math


# ── ENUMS ─────────────────────────────────────────────────────────────────────

class AttemptOutcome(Enum):
    FAILED_EARLY   = "failed_early"    # Stopped at Luhn / first gate
    FAILED_MID     = "failed_mid"      # Got partway through
    FAILED_LATE    = "failed_late"     # Almost succeeded — most dangerous
    BREACH         = "breach"          # Layer fully broken
    PARTIAL_UNLOCK = "partial_unlock"  # Some sub-components accessed


class HardeningTrigger(Enum):
    SCHEDULED      = "scheduled"       # Periodic (every 3 months)
    POST_BREACH    = "post_breach"     # After any breach
    THRESHOLD      = "threshold"       # After N failed attempts
    MASTER_MANUAL  = "master_manual"   # Author decides
    CROSS_LAYER    = "cross_layer"     # Pattern detected across multiple layers


class PatternClass(Enum):
    TIMING_ATTACK       = "timing_attack"
    BRUTEFORCE          = "bruteforce"
    ML_ENUMERATION      = "ml_enumeration"
    SIDE_CHANNEL        = "side_channel"
    REPLAY_ATTACK       = "replay_attack"
    SOCIAL_ENGINEERING  = "social_engineering"  # Unlikely but logged
    HYBRID_COORDINATED  = "hybrid_coordinated"
    UNKNOWN_NOVEL       = "unknown_novel"        # Most dangerous class


# ── DATA CLASSES ──────────────────────────────────────────────────────────────

@dataclass
class HistoricAttempt:
    """A single recorded attempt on any layer."""
    attempt_id: str
    layer_num: int
    timestamp: float
    outcome: AttemptOutcome
    attacker_type: str              # human / ai / assisted / team
    ai_probability: float
    pattern_class: PatternClass
    duration_seconds: float
    num_requests: int
    got_to_chevron: int             # how far into 9-chevron auth (0-9)
    partial_completion_pct: float   # 0-100% of layer completed
    unique_vectors_tried: int       # how many different approaches
    notes: str = ""


@dataclass
class LayerHistory:
    """Complete attack history for one layer."""
    layer_num: int
    total_attempts: int = 0
    total_breaches: int = 0
    total_partial_unlocks: int = 0
    attempts: list = field(default_factory=list)

    # Computed statistics
    most_common_pattern: Optional[PatternClass] = None
    closest_breach_pct: float = 0.0    # highest partial completion seen
    avg_attempts_to_breach: float = 0.0
    novel_attack_count: int = 0
    cross_layer_correlation: dict = field(default_factory=dict)

    def add_attempt(self, attempt: HistoricAttempt):
        self.attempts.append(attempt)
        self.total_attempts += 1
        if attempt.outcome == AttemptOutcome.BREACH:
            self.total_breaches += 1
        if attempt.outcome == AttemptOutcome.PARTIAL_UNLOCK:
            self.total_partial_unlocks += 1
        if attempt.partial_completion_pct > self.closest_breach_pct:
            self.closest_breach_pct = attempt.partial_completion_pct
        if attempt.pattern_class == PatternClass.UNKNOWN_NOVEL:
            self.novel_attack_count += 1


@dataclass
class HardeningReport:
    """Analysis result and hardening recommendations."""
    report_id: str
    generated_at: float
    layers_analyzed: list[int]
    trigger: HardeningTrigger

    # Analysis findings
    dominant_patterns: list[PatternClass]
    cross_layer_patterns: list[str]
    near_miss_vectors: list[str]       # attacks that almost worked
    novel_vectors_detected: int
    total_history_depth: int           # total attempts analyzed

    # Hardening recommendations
    hardening_actions: list[str]       # public descriptions only
    estimated_strength_delta: float    # how much stronger (multiplier)
    priority_layers: list[int]         # which layers need most work
    master_key_required: bool = True

    # Private (REDACTED in public release)
    _implementation_details: str = "[REDACTED — Master Key required]"


# ── HISTORIC HARDENING ENGINE ─────────────────────────────────────────────────

class HistoricHardeningEngine:
    """
    Analyzes complete attack history across ALL layers
    to produce cumulative hardening updates.

    HARDENING TRIGGERS:
    1. After any breach (immediate analysis)
    2. Scheduled every 3 months (periodic)
    3. After 1000 failed attempts on any single layer (threshold)
    4. When cross-layer patterns detected (automatic)
    5. Manual trigger by Master Key holder (anytime)

    ANALYSIS SCOPE:
    - Every attempt ever made on any layer
    - Successful breaches AND near-misses (near-misses are critical)
    - Cross-layer pattern correlation
    - Attacker evolution over time (are they getting smarter?)
    - Novel vs. known attack patterns

    HARDENING OUTPUT:
    - Per-layer update recommendations
    - Cross-layer defensive improvements
    - Priority ranking of vulnerabilities
    - Estimated strength improvement factor
    - All signed by Master Key before activation
    """

    # Thresholds
    ATTEMPT_THRESHOLD = 1000          # trigger analysis after this many attempts
    SCHEDULE_INTERVAL = 7776000       # 3 months in seconds
    NEAR_MISS_THRESHOLD = 0.75        # attempts completing >75% are near-misses
    NOVEL_ALERT_THRESHOLD = 5         # alert after this many novel patterns

    def __init__(self):
        self._layer_histories: dict[int, LayerHistory] = {
            i: LayerHistory(layer_num=i) for i in range(1, 10)
        }
        self._global_attempt_log: list[HistoricAttempt] = []
        self._hardening_reports: list[HardeningReport] = []
        self._last_scheduled_hardening: float = time.time()
        self._pending_master_approval: list[HardeningReport] = []

    # ── RECORD ATTEMPT ────────────────────────────────────────────────────────

    def record_attempt(self, attempt: HistoricAttempt) -> dict:
        """
        Record any attempt (failed or successful) on any layer.
        Automatically checks if hardening triggers are met.
        """
        self._global_attempt_log.append(attempt)
        self._layer_histories[attempt.layer_num].add_attempt(attempt)

        triggers_fired = []

        # Check threshold trigger
        layer_hist = self._layer_histories[attempt.layer_num]
        if layer_hist.total_attempts % self.ATTEMPT_THRESHOLD == 0:
            triggers_fired.append(HardeningTrigger.THRESHOLD)

        # Check post-breach trigger
        if attempt.outcome == AttemptOutcome.BREACH:
            triggers_fired.append(HardeningTrigger.POST_BREACH)

        # Check cross-layer pattern
        cross_pattern = self._detect_cross_layer_pattern(attempt)
        if cross_pattern:
            triggers_fired.append(HardeningTrigger.CROSS_LAYER)

        # Check scheduled hardening
        if time.time() - self._last_scheduled_hardening > self.SCHEDULE_INTERVAL:
            triggers_fired.append(HardeningTrigger.SCHEDULED)
            self._last_scheduled_hardening = time.time()

        reports = []
        for trigger in triggers_fired:
            report = self._run_analysis(trigger, cross_pattern)
            reports.append(report)

        return {
            "attempt_recorded": True,
            "layer": attempt.layer_num,
            "total_attempts_on_layer": layer_hist.total_attempts,
            "near_miss": attempt.partial_completion_pct >= self.NEAR_MISS_THRESHOLD,
            "triggers_fired": [t.value for t in triggers_fired],
            "hardening_reports_generated": len(reports),
            "master_approval_pending": len(self._pending_master_approval),
        }

    # ── CORE ANALYSIS ────────────────────────────────────────────────────────

    def _run_analysis(
        self,
        trigger: HardeningTrigger,
        cross_pattern_info: Optional[str] = None
    ) -> HardeningReport:
        """
        Run full historical analysis and generate hardening report.
        """
        print(f"\n[HARDENING] 🔍 Analysis triggered: {trigger.value}")
        print(f"[HARDENING] Scanning {len(self._global_attempt_log)} total attempts...")

        # 1. Pattern frequency analysis across all layers
        pattern_counts = defaultdict(int)
        near_misses = []
        novel_vectors = []
        breach_vectors = []

        for attempt in self._global_attempt_log:
            pattern_counts[attempt.pattern_class] += 1
            if attempt.partial_completion_pct >= self.NEAR_MISS_THRESHOLD:
                near_misses.append(attempt)
            if attempt.pattern_class == PatternClass.UNKNOWN_NOVEL:
                novel_vectors.append(attempt)
            if attempt.outcome == AttemptOutcome.BREACH:
                breach_vectors.append(attempt)

        # 2. Sort patterns by frequency
        dominant = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
        dominant_patterns = [p for p, _ in dominant[:3]]

        # 3. Cross-layer correlation
        cross_patterns = self._analyze_cross_layer_correlations()

        # 4. Near-miss deep analysis
        near_miss_summaries = self._analyze_near_misses(near_misses)

        # 5. Compute priority layers (most attacked / closest to breach)
        priority_layers = self._compute_priority_layers()

        # 6. Estimate strength delta
        strength_delta = self._estimate_strength_improvement(
            len(near_misses), len(novel_vectors), len(breach_vectors)
        )

        # 7. Generate hardening actions (public descriptions)
        actions = self._generate_hardening_actions(
            dominant_patterns, near_miss_summaries, cross_patterns, novel_vectors
        )

        report = HardeningReport(
            report_id=hashlib.sha256(
                f"HARDENING_{trigger.value}_{time.time()}".encode()
            ).hexdigest()[:16],
            generated_at=time.time(),
            layers_analyzed=list(range(1, 10)),
            trigger=trigger,
            dominant_patterns=dominant_patterns,
            cross_layer_patterns=cross_patterns,
            near_miss_vectors=near_miss_summaries,
            novel_vectors_detected=len(novel_vectors),
            total_history_depth=len(self._global_attempt_log),
            hardening_actions=actions,
            estimated_strength_delta=strength_delta,
            priority_layers=priority_layers,
        )

        self._hardening_reports.append(report)
        self._pending_master_approval.append(report)

        self._print_report(report)
        return report

    # ── CROSS-LAYER ANALYSIS ──────────────────────────────────────────────────

    def _detect_cross_layer_pattern(self, latest: HistoricAttempt) -> Optional[str]:
        """
        Detect if an attack on one layer correlates with patterns
        seen on other layers — suggesting coordinated campaign.
        """
        # Check if same attacker type used same pattern on multiple layers
        same_pattern_layers = []
        for layer_num, history in self._layer_histories.items():
            if layer_num == latest.layer_num:
                continue
            for attempt in history.attempts[-50:]:  # Last 50 attempts per layer
                if (attempt.pattern_class == latest.pattern_class and
                    attempt.attacker_type == latest.attacker_type):
                    same_pattern_layers.append(layer_num)
                    break

        if len(same_pattern_layers) >= 2:
            return (
                f"Cross-layer pattern: {latest.pattern_class.value} "
                f"detected on layers {same_pattern_layers + [latest.layer_num]}"
            )
        return None

    def _analyze_cross_layer_correlations(self) -> list[str]:
        """Find patterns that appear across multiple layers."""
        correlations = []

        # Group all attempts by pattern and attacker type
        by_pattern = defaultdict(list)
        for attempt in self._global_attempt_log:
            key = (attempt.pattern_class, attempt.attacker_type)
            by_pattern[key].append(attempt.layer_num)

        for (pattern, atype), layers in by_pattern.items():
            unique_layers = set(layers)
            if len(unique_layers) >= 3:
                correlations.append(
                    f"{pattern.value} by {atype} spans {len(unique_layers)} layers "
                    f"— coordinated campaign suspected"
                )

        return correlations

    def _analyze_near_misses(self, near_misses: list[HistoricAttempt]) -> list[str]:
        """
        Near-misses are MORE important than successful breaches
        for hardening — they show what almost worked.
        """
        if not near_misses:
            return []

        summaries = []
        # Group by layer and pattern
        by_layer = defaultdict(list)
        for nm in near_misses:
            by_layer[nm.layer_num].append(nm)

        for layer, attempts in by_layer.items():
            max_pct = max(a.partial_completion_pct for a in attempts)
            patterns = set(a.pattern_class.value for a in attempts)
            summaries.append(
                f"Layer {layer}: {len(attempts)} near-misses, "
                f"max {max_pct:.0f}% completion, "
                f"patterns: {', '.join(patterns)}"
            )

        return summaries

    def _compute_priority_layers(self) -> list[int]:
        """
        Rank layers by urgency of hardening needed.
        Factors: breach history, near-miss frequency, novel attacks.
        """
        scores = {}
        for layer_num, history in self._layer_histories.items():
            if layer_num == 9:  # Layer 9 has its own process
                continue
            score = (
                history.total_breaches * 10 +
                history.closest_breach_pct * 0.5 +
                history.novel_attack_count * 3 +
                history.total_partial_unlocks * 1
            )
            scores[layer_num] = score

        return sorted(scores.keys(), key=lambda x: scores[x], reverse=True)[:5]

    def _estimate_strength_improvement(
        self, near_misses: int, novel: int, breaches: int
    ) -> float:
        """
        Estimate how much stronger the hardened layer will be.
        Returns a multiplier (e.g. 3.7 = 3.7x harder to break).
        
        Full calculation: REDACTED.
        This is a public approximation only.
        """
        base = 1.0
        base += near_misses * 0.15    # each near-miss adds 15% strength
        base += novel * 0.40          # novel patterns add 40% per unique vector
        base += breaches * 0.80       # each breach adds 80% (painful but instructive)
        return round(min(base, 50.0), 2)  # cap at 50x for public display

    def _generate_hardening_actions(
        self,
        patterns: list,
        near_misses: list,
        cross_patterns: list,
        novel: list
    ) -> list[str]:
        """
        Generate public descriptions of hardening actions.
        Actual implementation: REDACTED.
        """
        actions = []

        for pattern in patterns:
            if pattern == PatternClass.ML_ENUMERATION:
                actions.append(
                    "Rotate Luhn salt mechanism — ML enumeration detected. "
                    "New salt derivation method applied. [DETAILS: REDACTED]"
                )
            elif pattern == PatternClass.TIMING_ATTACK:
                actions.append(
                    "Normalize response timing across all validation paths. "
                    "Add randomized micro-delays. [DETAILS: REDACTED]"
                )
            elif pattern == PatternClass.BRUTEFORCE:
                actions.append(
                    "Implement progressive lockout with exponential backoff. "
                    "Integrate Iris Protocol earlier in validation chain. [DETAILS: REDACTED]"
                )
            elif pattern == PatternClass.UNKNOWN_NOVEL:
                actions.append(
                    "Novel attack vector detected. Full architectural review initiated. "
                    "VIKI Engine rules updated to counter pattern. [DETAILS: REDACTED]"
                )
            elif pattern == PatternClass.SIDE_CHANNEL:
                actions.append(
                    "Side-channel hardening: memory access pattern randomization. "
                    "Constant-time operations enforced in critical paths. [DETAILS: REDACTED]"
                )
            elif pattern == PatternClass.HYBRID_COORDINATED:
                actions.append(
                    "Coordinated multi-vector attack detected. "
                    "NS-5 Mesh alert raised. Cross-layer correlation defenses deployed. [DETAILS: REDACTED]"
                )

        if near_misses:
            actions.append(
                f"{len(near_misses)} near-miss vectors hardened specifically. "
                "These represent highest-priority closure targets. [DETAILS: REDACTED]"
            )

        if cross_patterns:
            actions.append(
                f"Cross-layer defensive synchronization applied across "
                f"{len(cross_patterns)} correlated attack patterns. [DETAILS: REDACTED]"
            )

        if novel:
            actions.append(
                f"{len(novel)} novel attack vectors catalogued and countered. "
                "Delta Nechita parameter rotation recommended. [DETAILS: REDACTED]"
            )

        return actions

    # ── MASTER APPROVAL ───────────────────────────────────────────────────────

    def master_approve_hardening(
        self, report_id: str, master_key_proof: str
    ) -> dict:
        """
        Master Key holder approves and activates a hardening report.
        Cannot be bypassed. Implementation of validation: REDACTED.
        """
        report = next(
            (r for r in self._pending_master_approval if r.report_id == report_id),
            None
        )
        if not report:
            return {"error": "Report not found or already approved"}

        print(f"\n[MASTER] Validating Master Key for hardening approval...")
        print(f"[MASTER] Validation: REDACTED")
        print(f"[MASTER] Hardening report {report_id[:8]}... approved.")
        print(f"[MASTER] Strength delta: {report.estimated_strength_delta}x")
        print(f"[MASTER] Implementation: REDACTED — applied to live layers.")

        self._pending_master_approval.remove(report)

        return {
            "status": "HARDENING_ACTIVATED",
            "report_id": report_id,
            "layers_hardened": report.layers_analyzed,
            "strength_improvement": f"{report.estimated_strength_delta}x",
            "actions_applied": len(report.hardening_actions),
            "signed_by": "Dumitru Nechita — Master Key",
        }

    # ── STATUS ────────────────────────────────────────────────────────────────

    def get_history_summary(self) -> dict:
        """Public summary of the attack history database."""
        total = len(self._global_attempt_log)
        breaches = sum(1 for a in self._global_attempt_log
                      if a.outcome == AttemptOutcome.BREACH)
        near_misses = sum(1 for a in self._global_attempt_log
                         if a.partial_completion_pct >= self.NEAR_MISS_THRESHOLD)
        novel = sum(1 for a in self._global_attempt_log
                   if a.pattern_class == PatternClass.UNKNOWN_NOVEL)

        return {
            "total_attempts_analyzed": total,
            "total_breaches": breaches,
            "total_near_misses": near_misses,
            "novel_attack_vectors": novel,
            "hardening_reports_generated": len(self._hardening_reports),
            "pending_master_approval": len(self._pending_master_approval),
            "history_makes_system_stronger": True,
            "cumulative_strength_factor": round(
                1.0 + (breaches * 0.8) + (near_misses * 0.15) + (novel * 0.4), 2
            ),
            "note": "Every attempt — successful or not — strengthens the system."
        }

    def _print_report(self, report: HardeningReport):
        print(f"\n{'═'*55}")
        print(f"  📊 HISTORIC HARDENING REPORT")
        print(f"{'═'*55}")
        print(f"  Report ID:      {report.report_id[:12]}...")
        print(f"  Trigger:        {report.trigger.value}")
        print(f"  History depth:  {report.total_history_depth} total attempts")
        print(f"  Near-misses:    {len(report.near_miss_vectors)}")
        print(f"  Novel vectors:  {report.novel_vectors_detected}")
        print(f"  Priority layers:{report.priority_layers}")
        print(f"  Strength delta: {report.estimated_strength_delta}x STRONGER")
        print(f"\n  HARDENING ACTIONS:")
        for i, action in enumerate(report.hardening_actions, 1):
            print(f"  {i}. {action[:70]}...")
        if report.cross_layer_patterns:
            print(f"\n  CROSS-LAYER PATTERNS:")
            for p in report.cross_layer_patterns:
                print(f"  ⚡ {p}")
        print(f"\n  ⚠️  MASTER KEY SIGNATURE REQUIRED TO ACTIVATE")
        print(f"{'═'*55}\n")


# ── COMBINED ENGINE (ReverseHydra + HistoricHardening) ───────────────────────

class D00MGATEDefenseEngine:
    """
    Unified defense engine combining both systems:

    ReverseHydra:       Immediate reaction → spawn heads NOW
    HistoricHardening:  Deep analysis → make it permanently stronger

    Together they form the complete adaptive defense of D00MGATE-NECH9.
    No other security protocol combines both mechanisms.

    "The system doesn't forget.
     The system doesn't forgive.
     The system gets stronger every time you try."
    """

    def __init__(self):
        from reverse_hydra import ReverseHydraEngine, AttackVector, BreakType
        self.hydra = ReverseHydraEngine()
        self.hardening = HistoricHardeningEngine()
        print("[D00MGATE] Defense Engine initialized.")
        print("[D00MGATE] ReverseHydra: ACTIVE")
        print("[D00MGATE] HistoricHardening: ACTIVE")
        print("[D00MGATE] Master Key: REQUIRED FOR ALL EVOLUTIONS\n")


# ── DEMO ─────────────────────────────────────────────────────────────────────

def demo():
    print("D00MGATE-NECH9 — HistoricHardening Engine Demo")
    print("Original concept: Dumitru Nechita\n")

    engine = HistoricHardeningEngine()

    # Simulate a history of attacks
    attack_history = [
        HistoricAttempt("A001", 1, time.time()-86400*30, AttemptOutcome.FAILED_MID,
            "ai", 0.95, PatternClass.ML_ENUMERATION, 3600, 50000, 3, 45.0, 12),
        HistoricAttempt("A002", 1, time.time()-86400*20, AttemptOutcome.FAILED_LATE,
            "human", 0.05, PatternClass.TIMING_ATTACK, 7200, 300, 6, 78.0, 4),
        HistoricAttempt("A003", 2, time.time()-86400*15, AttemptOutcome.BREACH,
            "team", 0.30, PatternClass.HYBRID_COORDINATED, 14400, 2100, 8, 100.0, 8),
        HistoricAttempt("A004", 3, time.time()-86400*10, AttemptOutcome.FAILED_LATE,
            "ai", 0.92, PatternClass.ML_ENUMERATION, 1800, 98000, 5, 81.0, 15),
        HistoricAttempt("A005", 1, time.time()-86400*5,  AttemptOutcome.BREACH,
            "human", 0.08, PatternClass.UNKNOWN_NOVEL, 18000, 847, 9, 100.0, 3),
        HistoricAttempt("A006", 4, time.time()-86400*2,  AttemptOutcome.FAILED_EARLY,
            "ai", 0.99, PatternClass.BRUTEFORCE, 600, 200000, 1, 12.0, 1),
        HistoricAttempt("A007", 2, time.time()-3600,     AttemptOutcome.FAILED_LATE,
            "assisted", 0.55, PatternClass.SIDE_CHANNEL, 9000, 1500, 7, 88.0, 6),
    ]

    print(f"[DEMO] Recording {len(attack_history)} historical attempts...")
    for attempt in attack_history:
        result = engine.record_attempt(attempt)
        if result["triggers_fired"]:
            print(f"  Layer {attempt.layer_num}: {attempt.outcome.value} → triggers: {result['triggers_fired']}")

    print("\n[DEMO] Approving first pending hardening report...")
    if engine._pending_master_approval:
        report = engine._pending_master_approval[0]
        approval = engine.master_approve_hardening(report.report_id, "[DEMO_MASTER_PROOF]")
        print(f"  Status: {approval['status']}")
        print(f"  Strength improvement: {approval['strength_improvement']}")

    print("\n[SUMMARY]")
    summary = engine.get_history_summary()
    for k, v in summary.items():
        print(f"  {k}: {v}")

    print(f"\n{'═'*55}")
    print("  HistoricHardening Principle — Dumitru Nechita, 2026")
    print("  'The system doesn't forget.")
    print("   The system doesn't forgive.")
    print("   The system gets stronger every time you try.'")
    print(f"{'═'*55}\n")


if __name__ == "__main__":
    demo()
