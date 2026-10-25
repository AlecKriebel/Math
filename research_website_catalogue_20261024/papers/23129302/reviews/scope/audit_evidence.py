#!/usr/bin/env python3
"""Read-only custody check of this bounded intake and scope lane."""
from pathlib import Path
import hashlib,json,zipfile
E=Path(__file__).resolve().parent;S=E.parents[1]/'sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(p,row):return p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
issues=[]
seal=json.loads((S/'SOURCE_SEAL.json').read_text());m=S/'SOURCE_MANIFEST.json'
if sha(m)!=seal['manifest_sha256']:issues.append('source manifest hash')
sm=json.loads(m.read_text())
for row in sm['files']:
 if not check(S/row['path'],row):issues.append('source '+row['path'])
first=json.loads((E/'SOURCE_FIRST_SEAL.json').read_text())
if not check(E/first['baseline'],first):issues.append('independent baseline')
for row in json.loads((E/'preservation-before.json').read_text())['original_bindings']:
 if not check(Path(row['path']),row):issues.append('original '+row['path'])
for row in json.loads((S/'receipt.json').read_text())['files']:
 if not check(Path(row['path']),row) or hashlib.md5(Path(row['path']).read_bytes()).hexdigest()!=row['md5']:issues.append('fresh file '+row['filename'])
with zipfile.ZipFile(S/'basin-boundaries-verification.zip') as z:
 names=[r.filename for r in z.infolist() if not r.is_dir()]
 if len(names)!=len(set(names)) or len(names)!=74:issues.append('ZIP member set')
 for name in names:
  if z.read(name)!=(S/'published-source'/name).read_bytes():issues.append('member '+name)
for p in [E/'supplement-default.stdout.json',E/'supplement-full.stdout.json',E/'independent-exact-checks.json']:
 if json.loads(p.read_text())['status']!='PASS':issues.append(p.name+' status')
if (E/'evidence-manifest.json').is_file():
 if (E/'SEAL.json').is_file() and sha(E/'evidence-manifest.json')!=json.loads((E/'SEAL.json').read_text())['manifest_sha256']:issues.append('review manifest seal')
 for row in json.loads((E/'evidence-manifest.json').read_text())['files']:
  if not check(E/row['path'],row):issues.append('review '+row['path'])
print(json.dumps({'status':'PASS' if not issues else 'FAIL','source_bindings':len(sm['files']),'ZIP_members':74,'initial_independence_baseline_unchanged':not('independent baseline'in issues),'original_bindings':2,'current_sibling_verdicts_not_read':True,'issues':issues,'scope':'File custody only; does not replace scientific review or certify novelty.'},indent=2))
raise SystemExit(bool(issues))
