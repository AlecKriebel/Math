from pathlib import Path
from fractions import Fraction as Q
import argparse,hashlib,json
p=argparse.ArgumentParser();p.add_argument('--author',required=True);p.add_argument('--sources',action='store_true');a=p.parse_args();root=Path(a.author);count=0
m=json.loads((root/'PACKET_MANIFEST.json').read_text())
for e in m['files']:
 b=(root/e['path']).read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'];count+=1
sources=0
if a.sources:
 for e in json.loads((root/'SOURCE_MANIFEST.json').read_text())['files']:
  b=(root/e['path']).read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'];sources+=1
n=0
# Direct rational monotonicity and spectral root transformation.
for v in range(1,201):
 c=Q(v,200)
 for w in range(300,601):
  delta=Q(w,200)
  assert (delta*(3-delta)>=c)==((2*delta-3)**2<=9-4*c);n+=1
 for w in range(1,100):
  x=Q(w,100)+Q(3,2);y=x+Q(1,100)
  assert x*(3-x)>y*(3-y);n+=1
print(json.dumps({'artifact_bindings':count,'local_source_bindings':sources,'independent_algebra_assertions':n,'result':'PASS','scope':'Source/hypothesis review establishes the analytic application; finite controls do not compute a Cheeger constant'},indent=2))
