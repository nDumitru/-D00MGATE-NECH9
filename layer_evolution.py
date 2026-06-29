"""
D00MGATE-NECH9 — Layer Evolution Engine
=========================================
Author: Dumitru Nechita
Version: 0.4.0-alpha
License: D00MGATE-NECH9 Proprietary License v1.0

PUBLIC INTERFACE — Evolution rules are public.
Evolution signatures and Master Key validation: REDACTED.

IMMUTABLE RULE: Only the Master Key holder can
sign and approve a layer evolution.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import time
import hashlib


class BreakType(Enum):
    HUMAN        = "human"
    AI_ASSISTED  = "ai_assisted"
    FULL_AI      = "full_ai"
    TEAM         = "team"


class EvolutionTrigger(Enum):
    COMPETITION_BREAK = "competition_break"   # Human/team broke the layer
    AUTHOR_CHOICE     = "author_choice"       # Master Key holder decides
    NEVER             = "never"               # Layer 9 — no external trigger


@dataclass
class LayerBreak:
    """Record of a successful layer completion."""
    layer_num: int
    competitor_id: str          # anonymized
    competitor_type: BreakType
    timestamp: float
    attempts: int
    layer_version_broken: str   # e.g. "3.0", "3.1"
    ai_probability: float       # 0.0 = human, 1.0 = AI


@dataclass
class LayerVersion:
    """A specific version of a layer."""
    layer_num: int
    version: str                # semver: "1.0", "1.1", "2.0"
    released_at: float
    evolution_trigger: EvolutionTrigger
    triggered_by: Optional[str] # competitor_id or "AUTHOR"
    master_key_signature: str   # REDACTED in public — placeholder here
    changelog: str
    is_active: bool = True


@dataclass
class LayerState:
    """Current state of all layers in the protocol."""
    layer_num: int
    current_version: str
    total_breaks: int           # how many times this layer has been broken
    current_breakers: list      # competitors currently on this layer
    evolution_trigger: EvolutionTrigger
    layer_9_locked: bool = True # Layer 9 never evolves externally


class LayerEvolutionEngine:
    """
    Manages layer evolution across competition sessions.

    IMMUTABLE RULES (cannot be changed by any update):
    1. Only human/team breaks trigger evolution (not Full AI)
    2. Layer 9 NEVER evolves via competition — author only
    3. Every evolution requires Master Key signature
    4. Competitors on a layer at evolution time face new version immediately
    5. The breaker receives prize AND must re-face evolved layer to progress
    """

    # Layer 9 is permanently excluded from competition evolution
    IMMUTABLE_LAYER = 9

    # Full AI breaks do NOT trigger evolution (but are recorded)
    AI_TRIGGERS_EVOLUTION = False

    def __init__(self):
        self._layers: dict[int, LayerState] = {}
        self._history: list[LayerBreak] = []
        self._versions: list[LayerVersion] = []
        self._initialize_layers()

    def _initialize_layers(self):
        """Set initial state for all 9 layers."""
        triggers = {
            1: EvolutionTrigger.COMPETITION_BREAK,
            2: EvolutionTrigger.COMPETITION_BREAK,
            3: EvolutionTrigger.COMPETITION_BREAK,
            4: EvolutionTrigger.COMPETITION_BREAK,
            5: EvolutionTrigger.COMPETITION_BREAK,
            6: EvolutionTrigger.COMPETITION_BREAK,
            7: EvolutionTrigger.COMPETITION_BREAK,
            8: EvolutionTrigger.COMPETITION_BREAK,
            9: EvolutionTrigger.NEVER,           # IMMUTABLE
        }
        for i in range(1, 10):
            self._layers[i] = LayerState(
                layer_num=i,
                current_version="1.0",
                total_breaks=0,
                current_breakers=[],
                evolution_trigger=triggers[i],
                layer_9_locked=(i == 9),
            )

    def record_break(self, break_event: LayerBreak) -> dict:
        """
        Record a layer break and determine if evolution triggers.

        Returns: {
            "evolution_triggered": bool,
            "new_version": str or None,
            "prize_eligible": bool,
            "affected_competitors": list,
            "master_key_required": bool
        }
        """
        layer = self._layers.get(break_event.layer_num)
        if not layer:
            return {"error": "Invalid layer"}

        # Layer 9 — NEVER evolves via competition
        if break_event.layer_num == self.IMMUTABLE_LAYER:
            print(f"[EVOLUTION] Layer 9 break attempt recorded.")
            print(f"[EVOLUTION] Layer 9 does not evolve via competition.")
            print(f"[EVOLUTION] This event has been logged and flagged for author review.")
            self._history.append(break_event)
            return {
                "evolution_triggered": False,
                "new_version": None,
                "prize_eligible": True,   # Theoretical — if it ever happens
                "affected_competitors": [],
                "master_key_required": True,
                "note": "Layer 9 break — author notification sent."
            }

        # Full AI breaks — recorded but don't trigger evolution
        if break_event.competitor_type == BreakType.FULL_AI and not self.AI_TRIGGERS_EVOLUTION:
            print(f"[EVOLUTION] Layer {break_event.layer_num} broken by FULL AI.")
            print(f"[EVOLUTION] AI breaks do not trigger evolution (immutable rule).")
            print(f"[EVOLUTION] Recorded in AI leaderboard.")
            self._history.append(break_event)
            layer.total_breaks += 1
            return {
                "evolution_triggered": False,
                "new_version": None,
                "prize_eligible": True,   # AI gets prize in AI category
                "affected_competitors": layer.current_breakers.copy(),
                "master_key_required": False,
                "note": "AI category break — no evolution triggered."
            }

        # Human / AI-Assisted / Team break — TRIGGERS EVOLUTION
        self._history.append(break_event)
        layer.total_breaks += 1

        old_version = layer.current_version
        new_version = self._bump_version(old_version)
        affected = layer.current_breakers.copy()

        # Update layer state
        layer.current_version = new_version
        # Add breaker to current layer (they must re-face evolved version)
        if break_event.competitor_id not in layer.current_breakers:
            layer.current_breakers.append(break_event.competitor_id)

        # Record version (signature would be Master Key in production)
        version_record = LayerVersion(
            layer_num=break_event.layer_num,
            version=new_version,
            released_at=time.time(),
            evolution_trigger=EvolutionTrigger.COMPETITION_BREAK,
            triggered_by=break_event.competitor_id,
            master_key_signature="[REQUIRES MASTER KEY — REDACTED]",
            changelog=f"Evolved from {old_version} after break by {break_event.competitor_type.value}. Triggered at {time.strftime('%Y-%m-%d %H:%M:%S')}.",
            is_active=True,
        )
        self._versions.append(version_record)

        print(f"\n[EVOLUTION] ⚡ LAYER {break_event.layer_num} EVOLVED")
        print(f"[EVOLUTION] {old_version} → {new_version}")
        print(f"[EVOLUTION] Triggered by: {break_event.competitor_type.value}")
        print(f"[EVOLUTION] Affected competitors: {len(affected)}")
        print(f"[EVOLUTION] Master Key signature required before activation.")
        print(f"[EVOLUTION] Evolution content: REDACTED\n")

        return {
            "evolution_triggered": True,
            "old_version": old_version,
            "new_version": new_version,
            "prize_eligible": True,
            "affected_competitors": affected,
            "master_key_required": True,
            "evolution_record": version_record,
        }

    def _bump_version(self, version: str) -> str:
        """Increment minor version: 1.0 → 1.1 → 1.2 → 2.0 at 10 breaks."""
        major, minor = map(int, version.split('.'))
        minor += 1
        if minor >= 10:
            major += 1
            minor = 0
        return f"{major}.{minor}"

    def get_layer_status(self, layer_num: int) -> dict:
        """Return public status of a specific layer."""
        layer = self._layers.get(layer_num)
        if not layer:
            return {"error": "Layer not found"}
        return {
            "layer": layer_num,
            "version": layer.current_version,
            "total_breaks": layer.total_breaks,
            "competitors_on_layer": len(layer.current_breakers),
            "evolution_trigger": layer.evolution_trigger.value,
            "evolves_via_competition": layer_num != self.IMMUTABLE_LAYER,
        }

    def get_all_status(self) -> list:
        """Return public status of all layers."""
        return [self.get_layer_status(i) for i in range(1, 10)]

    def sign_evolution(self, layer_num: int, version: str, master_key_proof: str) -> bool:
        """
        Validate and sign a layer evolution with the Master Key.
        Called by author only. Implementation: REDACTED.
        """
        raise NotImplementedError(
            "Master Key signing: REDACTED. "
            "Only the author can sign evolutions."
        )


# ── DEMO ─────────────────────────────────────────────────────────────────────

def demo():
    print("D00MGATE-NECH9 — Layer Evolution Engine Demo")
    print("=" * 50)

    engine = LayerEvolutionEngine()

    print("\n[STATUS] Initial layer states:")
    for s in engine.get_all_status():
        lock = "🔒 NO COMPETITION EVOLUTION" if not s["evolves_via_competition"] else "✓"
        print(f"  Layer {s['layer']}: v{s['version']} | breaks: {s['total_breaks']} | {lock}")

    print("\n[DEMO] Simulating a human break on Layer 1...")
    result = engine.record_break(LayerBreak(
        layer_num=1,
        competitor_id="COMPETITOR_REDACTED_001",
        competitor_type=BreakType.HUMAN,
        timestamp=time.time(),
        attempts=847,
        layer_version_broken="1.0",
        ai_probability=0.03,
    ))
    print(f"  Evolution triggered: {result['evolution_triggered']}")
    print(f"  New version: {result.get('new_version')}")
    print(f"  Master Key required: {result['master_key_required']}")

    print("\n[DEMO] Simulating Full AI break on Layer 2...")
    result2 = engine.record_break(LayerBreak(
        layer_num=2,
        competitor_id="AI_AGENT_GPT_X_042",
        competitor_type=BreakType.FULL_AI,
        timestamp=time.time(),
        attempts=50000,
        layer_version_broken="1.0",
        ai_probability=0.98,
    ))
    print(f"  Evolution triggered: {result2['evolution_triggered']}")
    print(f"  Note: {result2.get('note')}")

    print("\n[DEMO] Layer 9 break attempt (theoretical)...")
    result3 = engine.record_break(LayerBreak(
        layer_num=9,
        competitor_id="THEORETICAL_ENTITY",
        competitor_type=BreakType.HUMAN,
        timestamp=time.time(),
        attempts=999999999,
        layer_version_broken="1.0",
        ai_probability=0.0,
    ))
    print(f"  Evolution triggered: {result3['evolution_triggered']}")
    print(f"  Note: {result3.get('note')}")

    print("\n[STATUS] Final layer states:")
    for s in engine.get_all_status():
        print(f"  Layer {s['layer']}: v{s['version']} | breaks: {s['total_breaks']}")

    print("\n'The gate changes. The address does not.'")
    print("— Dumitru Nechita")


if __name__ == "__main__":
    demo()
