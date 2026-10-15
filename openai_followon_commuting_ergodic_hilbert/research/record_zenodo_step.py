#!/usr/bin/env python3
"""Record one separately invoked documented Zenodo CLI operation."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
TOOL=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
assert sys.argv[1] in ['check','stage','inspect','publish']
step=sys.argv[1]
suffix='_doi' if '--check-doi' in sys.argv[2:] else ''
run=subprocess.run(['python3',str(TOOL),step,str(ROOT/'zenodo-deposit.json'),*sys.argv[2:]],text=True,capture_output=True)
(ROOT/'receipts'/('zenodo_'+step+suffix+'.stdout.json')).write_text(run.stdout)
(ROOT/'receipts'/('zenodo_'+step+suffix+'.stderr.txt')).write_text(run.stderr)
print(run.stdout,end='')
if run.stderr: print(run.stderr,end='',file=sys.stderr)
sys.exit(run.returncode)
