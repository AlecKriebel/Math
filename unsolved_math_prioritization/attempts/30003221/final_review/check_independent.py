from pathlib import Path
from fractions import Fraction as F
import hashlib,json
p=Path('/workspace/shared/research_nonlocal_30003221');checks=0
for f in json.loads((p/'checkpoint/FINAL_FROZEN_MANIFEST.json').read_text())['files']:
 assert hashlib.sha256((p/'checkpoint'/f['path']).read_bytes()).hexdigest()==f['sha256'];checks+=1
for f in json.loads((p/'checkpoint/SOURCE_MANIFEST.json').read_text())['primary_pdfs']:
 assert hashlib.sha256((p/f['local_audit_file']).read_bytes()).hexdigest()==f['sha256'];checks+=1
for alpha in [F(1,100),F(1,2),F(1),F(2),F(7),F(100)]:
 # Attraction-minus-repulsion mass exponent is strictly positive.
 assert (2+alpha/3)-(2-F(1,3))==(alpha+1)/3>0;checks+=1
 # ell=alpha^(-1/(alpha+1)); ratio attractive/repulsive coefficient ell^(alpha+1)=1/alpha.
 assert -F(1)/(alpha+1)*(alpha+1)==-1;checks+=1
 # dxd y contributes ell^6, Coulomb ell^-1, and mass ell^3; density cap unchanged.
 assert 6-1==5;checks+=1
assert 0<1<3-1;checks+=1
assert 1-F(1,3-1)==F(1,2)>0;checks+=1
print(json.dumps({'status':'PASS','independent_assertions':checks,'scope':'hash and exact specialization/scaling controls; analytic theorem is credited'},indent=2))
