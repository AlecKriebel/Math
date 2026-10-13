#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
D=Path(__file__).resolve().parent
for r in json.loads((D/'PUBLICATION_MANIFEST.json').read_text())['files']:
 b=(D/r['path']).read_bytes();assert len(b)==r['bytes'];assert hashlib.sha256(b).hexdigest()==r['sha256']
out=subprocess.check_output([sys.executable,str(D/'check_turn_1.py')]);assert out==(D/'TURN_1_CHECKS.json').read_bytes()
out=json.loads(subprocess.check_output([sys.executable,str(D/'review/portable_check.py'),str(D)]))
old=json.loads((D/'review/CHECKS.json').read_text())
assert out['independent_assertions']==old['independent_assertions']==3128
assert out['author_receipt']==old['author_receipt']
print(json.dumps({'status':'PASS','all_public_hashes':True,'author_assertions':5529,'independent_assertions':3128,'raw_source_hashes_checked_this_run':out['source_pdfs']},indent=2))
