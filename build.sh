#!/bin/bash
# D00MGATE-NECH9 Ada Build Script
# Author: Dumitru Nechita
#
# Requirements:
#   sudo apt-get install gnat gprbuild
#
# Compile:
#   mkdir -p build/obj
#   gprbuild -P doomgate.gpr
#
# Run:
#   ./build/doomgate_demo

mkdir -p build/obj
gprbuild -P doomgate.gpr
echo ""
echo "Run: ./build/doomgate_demo"
