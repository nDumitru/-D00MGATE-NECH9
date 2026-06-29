# D00MGATE-NECH9 -- Ada Implementation
## Author: Dumitru Nechita | License: D00MGATE-NECH9 Proprietary v1.0

### Files

```
core/
  master_key.ads / .adb    <- MASTER KEY (set here - 1 location)
  reverse_hydra.ads / .adb <- ReverseHydra Engine (original concept)
  historic_hardening.ads / .adb <- HistoricHardening (original concept)
  veridex.ads / .adb       <- VERIDEX Layer 10 (original concept)

src/
  luhn_dynamic.ads / .adb  <- Layer 1: Dynamic Luhn Token

demo/
  doomgate_demo.adb        <- Main demo (all systems)

doomgate.gpr               <- GNAT project file
build.sh                   <- Build script
```

### Quick Start

```bash
# Install compiler
sudo apt-get install gnat gprbuild

# Build
mkdir -p build/obj
gprbuild -P doomgate.gpr

# Run demo
./build/doomgate_demo
```

### Set Your Master Key

Edit **core/master_key.adb** — find this line:

```ada
Master_Key_Value : constant String := "MASTER_KEY_HERE";
```

Replace with your personal key. Recompile. Done.

### TODO markers in code

Search for `-- TODO:` across all files for places you should customize:
- `core/master_key.adb` -> Master_Key_Value (your key)
- `src/luhn_dynamic.adb` -> Delta Nechita seed integration
- `core/reverse_hydra.adb` -> Evolution content implementation
- `core/historic_hardening.adb` -> Hardening logic implementation
- `core/veridex.adb` -> Silent ops, JunkDNA positions, Gravemind conversion

### Verified Working

Compiled and tested with GNAT 13.3.0 on Ubuntu 24.04.
All 4 engines functional in DEMO MODE.
Set Master Key to unlock full functionality.

"The gate is open. The address is mine." - Dumitru Nechita, 2026
