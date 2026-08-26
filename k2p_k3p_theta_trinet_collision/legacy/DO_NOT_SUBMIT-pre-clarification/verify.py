#!/usr/bin/env python3
"""Delegate to the sole current K2P/K3P verification package."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parent
CANONICAL=ROOT/'k2p_k3p_theta_clarified'
subprocess.run([sys.executable,str(CANONICAL/'verify.py')],cwd=CANONICAL,check=True)
