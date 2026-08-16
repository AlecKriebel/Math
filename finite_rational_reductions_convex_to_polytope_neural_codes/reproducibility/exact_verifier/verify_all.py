#!/usr/bin/env python3
import subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
scripts=['verify_reductions.py','verify_bridge.py','verify_fixed_arrangement.py','verify_sequential_repair.py','verify_one_round.py']
for s in scripts:
    print(f'== {s} ==')
    subprocess.run([sys.executable,str(root/s)],check=True,cwd=root.parent)
print('PAPER 1 EXACT FINITE CALIBRATIONS PASS')
