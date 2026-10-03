#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
D=Path(__file__).resolve().parent
for r in json.loads((D/'PUBLICATION_MANIFEST.json').read_text())['files']:
 b=(D/r['path']).read_bytes();assert len(b)==r['bytes'];assert hashlib.sha256(b).hexdigest()==r['sha256']
for i in range(1,5):
 out=subprocess.check_output([sys.executable,str(D/f'check_turn_{i}.py')],cwd=D)
 assert out==(D/f'TURN_{i}_CHECKS.json').read_bytes()
out=subprocess.check_output([sys.executable,str(D/'verify_turn_4_cpp.py')],cwd=D)
assert out==(D/'TURN_4_CPP_CHECKS.json').read_bytes()
out=subprocess.check_output([sys.executable,str(D/'review/independent_check.py')],cwd=D)
assert json.loads(out)==json.loads((D/'review/INDEPENDENT_CHECKS.json').read_bytes())
print('PASS: all frozen public bytes, four Python receipts, C++ full stream, and independent review controls')
