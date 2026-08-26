#!/usr/bin/env python3
"""One-command exact replay of the K2P/K3P verification package."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parent
if sys.version_info < (3,10):
    raise SystemExit('Python 3.10 or newer is required')
STEPS=[('source conventions',ROOT/'src/verify_source_conventions.py'),('simple K2P collision',ROOT/'verify_k2p_simple.py'),('simple K2P displayed-tree reconstruction and direct pruning',ROOT/'verify_k2p_displayed_trees.py'),('edgewise strictly continuous-time K2P and proof audit',ROOT/'src/verify_k2p_extended.py'),('K2P rank and collision families',ROOT/'src/verify_k2p_rank_family.py'),('K3P collision, rank, and edgewise continuous-time analytic-IFT data',ROOT/'src/verify_k3p.py')]
PYTHON=[sys.executable]
if sys.flags.optimize:
    PYTHON.append('-'+'O'*sys.flags.optimize)
for title,path in STEPS:
    print('\n'+'='*78,flush=True);print(title.upper(),flush=True);print('='*78,flush=True);subprocess.run([*PYTHON,str(path)],cwd=ROOT,check=True)
print('\nALL EXACT CHECKS PASSED')
