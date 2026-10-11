from pathlib import Path
from fractions import Fraction as F
import hashlib,json
p=Path('/workspace/shared/research_harmonicpath_2303002/checkpoint');src=p.parent/'sources';n=0
for f in json.loads((p/'FINAL_FROZEN_MANIFEST.json').read_text())['files']:
 assert hashlib.sha256((p/f['path']).read_bytes()).hexdigest()==f['sha256'];n+=1
for f in json.loads((p/'SOURCE_MANIFEST.json').read_text())['primary_pdfs']:
 assert hashlib.sha256((src/f['file']).read_bytes()).hexdigest()==f['sha256'];n+=1
for dim in range(3,21):
 for j in range(91):
  a=F(j,100);lo=(1-a*a)/(1+a)**dim;hi=(1-a*a)/(1-a)**dim
  assert 0<lo<=1<=hi;n+=1
  if j==0:assert lo==hi==1;n+=1
print(json.dumps({'status':'PASS','independent_assertions':n,'scope':'integrity and exact kernel-bound sanity checks; full analytic proof reviewed separately'},indent=2))
