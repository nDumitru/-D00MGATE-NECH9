"""
D00MGATE-NECH9 — ReverseHydra Evolution Engine
================================================
Author: Dumitru Nechita
Version: 0.5.0-alpha
License: D00MGATE-NECH9 Proprietary License v1.0

CONCEPT: ReverseHydra (original concept by Dumitru Nechita)

Classical Hydra:   cut 1 head  → 2 heads grow
ReverseHydra:      break 1 layer → layer SPLITS into N variants
                   each variant analyzes HOW it was broken
                   each variant evolves DIFFERENTLY
                   next attacker faces N variants, not 1
                   N grows with each subsequent attack
                   AI break → more aggressive split than human break

MASTER NOTIFICATION:
  Every evolution requires Master Key holder acknowledgment.
  The system CANNOT complete evolution without it.
  Notification is mandatory, persistent, and escalating.
  The Master cannot be bypassed. By design.

"You killed one head.
 You fed the others."
 — ReverseHydra Principle, D00MGATE-NECH9
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import hashlib
import time
import json
import math


# ── ENUMS ─────────────────────────────────────────────────────────────────────

class BreakType(Enum):
    HUMAN        = "human"
    AI_ASSISTED  = "ai_assisted"
    FULL_AI      = "full_ai"
    TEAM         = "team"


class HydraState(Enum):
    STABLE        = "stable"        # Layer intact, no pending evolution
    BROKEN        = "broken"        # Layer was broken, analysis running
    SPLITTING     = "splitting"     # ReverseHydra splitting in progress
    PENDING_MASTER= "pending_master"# Waiting for Master Key acknowledgment
    EVOLVING      = "evolving"      # Master acknowledged, evolution active
    MULTI_HEAD    = "multi_head"    # Layer now has multiple active variants


class NotificationUrgency(Enum):
    INFO      = "INFO"      # First notification
    WARNING   = "WARNING"   # 1 hour without response
    URGENT    = "URGENT"    # 6 hours without response
    CRITICAL  = "CRITICAL"  # 24 hours — layer offline until master responds


# ── DATA CLASSES ──────────────────────────────────────────────────────────────

@dataclass
class AttackVector:
    """Detailed analysis of how a layer was broken."""
    layer_num: int
    break_type: BreakType
    competitor_id: str
    timestamp: float
    attempts: int
    ai_probability: float
    time_to_break_seconds: float
    layer_version_broken: str

    # Attack analysis (computed)
    attack_pattern: str = ""        # e.g. "timing_side_channel", "bruteforce", "ml_pattern"
    weakest_point: str = ""         # which sub-component was exploited
    attack_entropy: float = 0.0     # how "creative" the attack was
    replication_risk: float = 0.0   # probability another uses same vector

    def analyze(self) -> 'AttackVector':
        """
        Analyze the attack vector to determine evolution response.
        Full analysis: REDACTED. Demo stubs below.
        """
        # AI attacks have predictable patterns — higher replication risk
        if self.break_type == BreakType.FULL_AI:
            self.attack_pattern = "ml_systematic_enumeration"
            self.attack_entropy = 0.3          # AI is methodical, low entropy
            self.replication_risk = 0.92       # easily replicated by other AIs
        elif self.break_type == BreakType.HUMAN:
            self.attack_pattern = "human_intuitive_probe"
            self.attack_entropy = 0.75         # humans are creative
            self.replication_risk = 0.35       # harder to replicate
        elif self.break_type == BreakType.AI_ASSISTED:
            self.attack_pattern = "hybrid_augmented"
            self.attack_entropy = 0.60
            self.replication_risk = 0.65
        elif self.break_type == BreakType.TEAM:
            self.attack_pattern = "coordinated_multi_vector"
            self.attack_entropy = 0.85         # teams are most creative
            self.replication_risk = 0.45

        self.weakest_point = "[ANALYSIS: REDACTED]"
        return self


@dataclass
class HydraHead:
    """One variant/head of an evolved layer."""
    head_id: str
    layer_num: int
    parent_version: str
    head_version: str              # e.g. "2.0-α", "2.0-β", "2.0-γ"
    created_at: float
    evolution_basis: str           # what attack vector this head counters
    is_active: bool = True
    breaks_survived: int = 0       # how many times this head resisted attack
    child_heads: list = field(default_factory=list)  # if this head is broken, it spawns these

    def spawn_children(self, n: int, attack: AttackVector) -> list['HydraHead']:
        """
        When this head is broken, spawn N child heads.
        Each child counters the attack differently.
        Implementation: REDACTED.
        """
        children = []
        greek = ['α','β','γ','δ','ε','ζ','η','θ','ι','κ','λ','μ']
        for i in range(n):
            child_version = f"{self.head_version.split('-')[0]}.{i+1}-{greek[i % len(greek)]}"
            child = HydraHead(
                head_id=hashlib.sha256(
                    f"{self.head_id}_{i}_{time.time()}".encode()
                ).hexdigest()[:12],
                layer_num=self.layer_num,
                parent_version=self.head_version,
                head_version=child_version,
                created_at=time.time(),
                evolution_basis=f"Counter-{attack.attack_pattern}-variant-{i+1}",
            )
            children.append(child)
        self.child_heads = [c.head_id for c in children]
        return children


@dataclass
class MasterNotification:
    """Mandatory notification to Master Key holder."""
    notification_id: str
    layer_num: int
    attack_summary: str
    heads_to_spawn: int
    pending_since: float
    urgency: NotificationUrgency = NotificationUrgency.INFO
    acknowledged: bool = False
    acknowledged_at: Optional[float] = None
    master_signature: Optional[str] = None  # REDACTED in production

    def escalate(self) -> NotificationUrgency:
        """Escalate urgency based on time without response."""
        elapsed = time.time() - self.pending_since
        if elapsed > 86400:    # 24 hours
            self.urgency = NotificationUrgency.CRITICAL
        elif elapsed > 21600:  # 6 hours
            self.urgency = NotificationUrgency.URGENT
        elif elapsed > 3600:   # 1 hour
            self.urgency = NotificationUrgency.WARNING
        return self.urgency


# ── REVERSE HYDRA ENGINE ──────────────────────────────────────────────────────

class ReverseHydraEngine:
    """
    ReverseHydra Evolution Engine — original concept by Dumitru Nechita.

    CORE PRINCIPLE:
    Every break — human or AI — feeds the system.
    The attacker's own technique becomes the blueprint
    for what they'll face next, multiplied.

    SPLIT FORMULA:
    Human break:       layer splits into 2 heads
    AI-Assisted break: layer splits into 3 heads
    Full AI break:     layer splits into 4 heads  ← AI gets punished MORE
    Team break:        layer splits into 3 heads

    Each subsequent break of a head:
    → that head splits into split_count² heads
    → exponential growth, not linear

    MASTER NOTIFICATION:
    → Mandatory for every evolution
    → Cannot be bypassed or automated
    → Escalates every hour without response
    → Layer goes OFFLINE if no response in 24h
    → Master MUST sign every evolution with Master Key
    → No signature = no evolution = layer stays broken/offline
    """

    # Split counts by attacker type
    SPLIT_COUNTS = {
        BreakType.HUMAN:        2,
        BreakType.AI_ASSISTED:  3,
        BreakType.FULL_AI:      4,   # AI attacks punished most aggressively
        BreakType.TEAM:         3,
    }

    # Layer 9 — NEVER splits via ReverseHydra
    IMMUTABLE_LAYER = 9

    def __init__(self):
        self._layer_states: dict[int, HydraState] = {i: HydraState.STABLE for i in range(1, 10)}
        self._active_heads: dict[int, list[HydraHead]] = {i: [] for i in range(1, 10)}
        self._attack_history: list[AttackVector] = []
        self._pending_notifications: list[MasterNotification] = []
        self._evolution_log: list[dict] = []

        # Initialize each layer with one default head
        for i in range(1, 10):
            self._active_heads[i].append(HydraHead(
                head_id=hashlib.sha256(f"GENESIS_L{i}".encode()).hexdigest()[:12],
                layer_num=i,
                parent_version="GENESIS",
                head_version="1.0",
                created_at=time.time(),
                evolution_basis="GENESIS — original layer",
            ))

    # ── CORE METHOD ──────────────────────────────────────────────────────────

    def process_break(self, attack: AttackVector) -> dict:
        """
        Process a layer break and trigger ReverseHydra evolution.

        Flow:
        1. Analyze attack vector
        2. Determine split count
        3. Generate pending evolution
        4. Create mandatory Master notification
        5. Layer state → PENDING_MASTER
        6. When Master acknowledges → SPLITTING → MULTI_HEAD
        """

        # Layer 9 protection
        if attack.layer_num == self.IMMUTABLE_LAYER:
            return self._handle_layer9_break(attack)

        # Analyze the attack
        attack.analyze()
        self._attack_history.append(attack)

        # Find the broken head
        broken_head = self._find_active_head(attack.layer_num, attack.layer_version_broken)

        # Determine split count
        split_n = self.SPLIT_COUNTS[attack.break_type]

        # If this head was already a child head — exponential growth
        if broken_head and broken_head.parent_version != "GENESIS":
            generation = self._get_head_generation(broken_head)
            split_n = min(split_n ** generation, 16)  # cap at 16 heads
            print(f"[HYDRA] Generation {generation} head broken — exponential split: {split_n} heads")

        # Update state
        self._layer_states[attack.layer_num] = HydraState.BROKEN

        # Create Master notification
        notification = self._create_master_notification(attack, split_n, broken_head)
        self._pending_notifications.append(notification)

        # Update state to pending
        self._layer_states[attack.layer_num] = HydraState.PENDING_MASTER

        # Deactivate broken head
        if broken_head:
            broken_head.is_active = False

        result = {
            "status": "PENDING_MASTER_ACKNOWLEDGMENT",
            "layer": attack.layer_num,
            "broken_head": broken_head.head_version if broken_head else "unknown",
            "attack_type": attack.break_type.value,
            "attack_pattern": attack.attack_pattern,
            "replication_risk": f"{attack.replication_risk:.0%}",
            "heads_to_spawn": split_n,
            "notification_id": notification.notification_id,
            "layer_state": "OFFLINE — pending Master signature",
            "message": (
                f"Layer {attack.layer_num} broken by {attack.break_type.value}. "
                f"ReverseHydra will spawn {split_n} evolved heads. "
                f"MASTER KEY SIGNATURE REQUIRED."
            )
        }

        self._log_evolution(attack, split_n, notification)
        self._print_break_report(result, attack, notification)
        return result

    # ── MASTER ACKNOWLEDGMENT ─────────────────────────────────────────────────

    def master_acknowledge(
        self,
        notification_id: str,
        master_key_proof: str,      # REDACTED — real validation not here
        approved_split: Optional[int] = None   # Master can override split count
    ) -> dict:
        """
        Master Key holder acknowledges and approves layer evolution.
        This is the ONLY way to complete a ReverseHydra evolution.

        master_key_proof: validated against Master Key in Ada kernel (REDACTED)
        approved_split: Master can increase or decrease heads (override)
        """
        notif = next((n for n in self._pending_notifications
                      if n.notification_id == notification_id), None)
        if not notif:
            return {"error": "Notification not found"}

        # In production: validate master_key_proof against Master Key
        # Implementation: REDACTED
        print(f"[MASTER] Validating Master Key proof... [REDACTED IN PUBLIC RELEASE]")
        print(f"[MASTER] Acknowledgment accepted for notification {notification_id[:8]}...")

        notif.acknowledged = True
        notif.acknowledged_at = time.time()
        notif.master_signature = "[MASTER KEY SIGNED — REDACTED]"

        # Execute the split
        split_n = approved_split or notif.heads_to_spawn
        layer_num = notif.layer_num

        # Find the broken head to spawn children from
        broken_head = next(
            (h for h in self._active_heads[layer_num] if not h.is_active),
            None
        )

        # Create attack vector for spawn context
        attack = next(
            (a for a in reversed(self._attack_history) if a.layer_num == layer_num),
            None
        )

        if broken_head and attack:
            new_heads = broken_head.spawn_children(split_n, attack)
        else:
            # Fallback: create heads without parent context
            new_heads = self._create_genesis_split(layer_num, split_n)

        self._active_heads[layer_num].extend(new_heads)
        self._layer_states[layer_num] = HydraState.MULTI_HEAD
        self._pending_notifications.remove(notif)

        result = {
            "status": "EVOLUTION_COMPLETE",
            "layer": layer_num,
            "new_heads": split_n,
            "head_versions": [h.head_version for h in new_heads],
            "layer_state": "MULTI_HEAD — active",
            "signed_by": "Master Key Holder (Dumitru Nechita)",
        }

        print(f"\n[HYDRA] ⚡ REVERSHYDRA EVOLUTION COMPLETE")
        print(f"[HYDRA] Layer {layer_num}: {split_n} new heads active")
        for h in new_heads:
            print(f"  → Head {h.head_version} | basis: {h.evolution_basis}")
        print(f"[HYDRA] Full evolution content: REDACTED\n")

        return result

    # ── NOTIFICATION SYSTEM ───────────────────────────────────────────────────

    def check_notifications(self) -> list[dict]:
        """
        Check all pending notifications and escalate as needed.
        Called periodically by the system.
        """
        reports = []
        for notif in self._pending_notifications:
            urgency = notif.escalate()
            report = {
                "notification_id": notif.notification_id,
                "layer": notif.layer_num,
                "urgency": urgency.value,
                "pending_hours": round((time.time() - notif.pending_since) / 3600, 1),
                "heads_waiting": notif.heads_to_spawn,
                "layer_status": "OFFLINE" if urgency == NotificationUrgency.CRITICAL else "DEGRADED",
                "action_required": "MASTER KEY SIGNATURE",
            }

            if urgency == NotificationUrgency.CRITICAL:
                report["warning"] = (
                    f"CRITICAL: Layer {notif.layer_num} has been offline 24h+. "
                    f"ReverseHydra cannot complete without Master Key acknowledgment. "
                    f"Layer remains unavailable to ALL users until signed."
                )

            reports.append(report)
        return reports

    # ── STATUS ────────────────────────────────────────────────────────────────

    def get_hydra_status(self, layer_num: int) -> dict:
        """Return full ReverseHydra status for a layer."""
        heads = self._active_heads.get(layer_num, [])
        active_heads = [h for h in heads if h.is_active]
        state = self._layer_states.get(layer_num, HydraState.STABLE)

        return {
            "layer": layer_num,
            "state": state.value,
            "total_heads": len(active_heads),
            "head_versions": [h.head_version for h in active_heads],
            "total_breaks_survived": sum(h.breaks_survived for h in active_heads),
            "evolves_via_competition": layer_num != self.IMMUTABLE_LAYER,
            "ai_triggers_split": True,     # AI breaks NOW trigger evolution
            "ai_split_multiplier": self.SPLIT_COUNTS[BreakType.FULL_AI],
        }

    def get_all_status(self) -> list:
        return [self.get_hydra_status(i) for i in range(1, 10)]

    # ── PRIVATE HELPERS ───────────────────────────────────────────────────────

    def _find_active_head(self, layer_num: int, version: str) -> Optional[HydraHead]:
        for h in self._active_heads.get(layer_num, []):
            if h.head_version == version:
                return h
        # Return any inactive head if exact version not found
        for h in self._active_heads.get(layer_num, []):
            if not h.is_active:
                return h
        return None

    def _get_head_generation(self, head: HydraHead) -> int:
        """Count how many generations deep this head is."""
        gen = 1
        version = head.head_version
        while '.' in version and len(version.split('.')) > 2:
            gen += 1
            version = '.'.join(version.split('.')[:-1])
        return gen

    def _create_master_notification(
        self, attack: AttackVector, split_n: int, broken_head: Optional[HydraHead]
    ) -> MasterNotification:
        notif_id = hashlib.sha256(
            f"{attack.layer_num}_{attack.timestamp}_{time.time()}".encode()
        ).hexdigest()[:16]

        summary = (
            f"Layer {attack.layer_num} broken by {attack.break_type.value.upper()}. "
            f"Pattern: {attack.attack_pattern}. "
            f"Replication risk: {attack.replication_risk:.0%}. "
            f"ReverseHydra: {split_n} heads pending spawn. "
            f"Head broken: {broken_head.head_version if broken_head else 'unknown'}. "
            f"LAYER IS OFFLINE UNTIL YOU SIGN."
        )

        return MasterNotification(
            notification_id=notif_id,
            layer_num=attack.layer_num,
            attack_summary=summary,
            heads_to_spawn=split_n,
            pending_since=time.time(),
        )

    def _create_genesis_split(self, layer_num: int, n: int) -> list[HydraHead]:
        greek = ['α','β','γ','δ','ε','ζ','η','θ']
        return [HydraHead(
            head_id=hashlib.sha256(f"SPLIT_{layer_num}_{i}_{time.time()}".encode()).hexdigest()[:12],
            layer_num=layer_num,
            parent_version="1.0",
            head_version=f"2.0-{greek[i]}",
            created_at=time.time(),
            evolution_basis=f"ReverseHydra-split-{i+1}",
        ) for i in range(n)]

    def _handle_layer9_break(self, attack: AttackVector) -> dict:
        print(f"\n[HYDRA] ⚠️  LAYER 9 BREAK DETECTED")
        print(f"[HYDRA] This event is impossible by design.")
        print(f"[HYDRA] Logging. Alerting Master. Flagging for full audit.")
        print(f"[HYDRA] Layer 9 does NOT split. Ever. Under any circumstances.")

        notif = MasterNotification(
            notification_id=hashlib.sha256(f"L9_{time.time()}".encode()).hexdigest()[:16],
            layer_num=9,
            attack_summary=f"IMPOSSIBLE EVENT: Layer 9 break claimed by {attack.break_type.value}. FULL AUDIT REQUIRED.",
            heads_to_spawn=0,
            pending_since=time.time(),
            urgency=NotificationUrgency.CRITICAL,
        )
        self._pending_notifications.append(notif)

        return {
            "status": "LAYER_9_IMMUTABLE",
            "note": "Layer 9 does not evolve via any external trigger. Master notified with CRITICAL urgency.",
            "notification_id": notif.notification_id,
        }

    def _log_evolution(self, attack: AttackVector, split_n: int, notif: MasterNotification):
        self._evolution_log.append({
            "timestamp": time.time(),
            "layer": attack.layer_num,
            "attack_type": attack.break_type.value,
            "split_n": split_n,
            "notification_id": notif.notification_id,
            "state": "PENDING_MASTER",
        })

    def _print_break_report(self, result: dict, attack: AttackVector, notif: MasterNotification):
        print(f"\n{'='*55}")
        print(f"  ⚡ REVERSHYDRA TRIGGERED — LAYER {attack.layer_num}")
        print(f"{'='*55}")
        print(f"  Attacker type:     {attack.break_type.value.upper()}")
        print(f"  Attack pattern:    {attack.attack_pattern}")
        print(f"  Replication risk:  {attack.replication_risk:.0%}")
        print(f"  Heads to spawn:    {result['heads_to_spawn']}")
        print(f"  Layer state:       OFFLINE — PENDING MASTER")
        print(f"  Notification ID:   {notif.notification_id[:8]}...")
        print(f"  Urgency:           {notif.urgency.value}")
        print(f"\n  ⚠️  MASTER KEY HOLDER: ACTION REQUIRED")
        print(f"  Layer {attack.layer_num} is OFFLINE until you sign.")
        print(f"  Evolution content: REDACTED")
        print(f"{'='*55}\n")


# ── DEMO ─────────────────────────────────────────────────────────────────────

def demo():
    print("D00MGATE-NECH9 — ReverseHydra Engine Demo")
    print("Original concept: Dumitru Nechita\n")

    engine = ReverseHydraEngine()

    print("[STATUS] Initial hydra state:")
    for s in engine.get_all_status():
        print(f"  Layer {s['layer']}: {s['state']} | heads: {s['total_heads']}")

    print("\n" + "─"*55)
    print("[DEMO 1] Full AI breaks Layer 1 (→ 4 heads)")
    print("─"*55)
    result = engine.process_break(AttackVector(
        layer_num=1,
        break_type=BreakType.FULL_AI,
        competitor_id="AI_AGENT_DEMO",
        timestamp=time.time(),
        attempts=50000,
        ai_probability=0.97,
        time_to_break_seconds=3600,
        layer_version_broken="1.0",
    ))

    print("\n[MASTER] Simulating Master acknowledgment...")
    notif_id = result["notification_id"]
    ack_result = engine.master_acknowledge(notif_id, "[DEMO_MASTER_PROOF]")
    print(f"  New heads: {ack_result.get('head_versions', [])}")

    print("\n" + "─"*55)
    print("[DEMO 2] Human breaks Layer 2 (→ 2 heads)")
    print("─"*55)
    result2 = engine.process_break(AttackVector(
        layer_num=2,
        break_type=BreakType.HUMAN,
        competitor_id="HUMAN_DEMO",
        timestamp=time.time(),
        attempts=843,
        ai_probability=0.04,
        time_to_break_seconds=7200,
        layer_version_broken="1.0",
    ))

    print("\n[NOTIFICATIONS] Pending notifications:")
    for n in engine.check_notifications():
        print(f"  Layer {n['layer']}: [{n['urgency']}] — {n['pending_hours']}h pending")

    print("\n[STATUS] Final hydra state:")
    for s in engine.get_all_status():
        heads = s['head_versions'] if s['total_heads'] > 1 else ['1.0']
        print(f"  Layer {s['layer']}: {s['state']} | heads: {s['total_heads']} {heads}")

    print(f"\n{'='*55}")
    print("  ReverseHydra Principle — Dumitru Nechita, 2026")
    print("  'You killed one head. You fed the others.'")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    demo()
