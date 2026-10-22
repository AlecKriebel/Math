"""Small exact controls for the source-counterexample review, not a topology engine."""
from pathlib import Path
import hashlib,json
checks=[]
def check(condition,label):
 assert condition,label
 checks.append(label)
# The imported example is a disk with the source's s=-2.
g=0;s=-2;chi=1-2*g
check(chi==1,'disk Euler characteristic')
check(2*g==0,'disk genus term')
check(abs(s)==2,'absolute Rasmussen term')
check(2*g<abs(s),'literal bound fails')
check(s<=2*g,'published one-sided bound holds')
check(s<=1-chi,'link normalization agrees for one component')
check((-s)>2*g,'opposite one-sided bound does not follow')
check(abs(-s)==abs(s),'boundary mirror leaves contradiction unchanged')
# Intersection form [-1] is nonsingular and negative definite. These are exact controls,
# not a computation of the geometric intersection form from a handle diagram.
q=-1
check(q<0,'negative definite rank-one form')
check(q*q==1,'unimodular rank-one form')
check(-q>0,'reversing ambient orientation exits negative definite class')
check(q*0==0,'relative zero class pairs trivially')
check(q*1==-1,'a nonzero generator must not be called null-homologous')
# In the verified long exact sequences, both endpoint groups are zero, so the
# intervening map is an isomorphism. The induced degree-two diagram has rank one.
A=[[1]]; B=[[1]]; H=[[1]]
check(A[0][0]*H[0][0]==H[0][0]*B[0][0],'degree-two naturality diagram')
check(A[0][0]!=0 and B[0][0]!=0,'absolute-relative maps invertible in model')
check(H[0][0]*0==0,'zero class remains zero under Hurewicz isomorphism')
# Relative obstruction cannot be inferred merely from contractibility of D^2;
# the sphere class obtained by gluing a boundary filling must vanish.
check(0-0==0,'disk-minus-boundary-filling zero class')
check(1-0!=0,'nonzero relative class fails strengthened condition')
# Recheck the author's finite checklist without modifying it.
a=json.loads(Path('submitted_verification.json').read_text())
check(a['genus']==g and a['s']==s and a['absolute_s']==abs(s),'submitted arithmetic reproduced')
check(a['inequality_holds'] is False,'submitted verdict reproduced')
artifact=Path('submitted_KNOWN_COUNTEREXAMPLE.md').read_bytes()
sha=hashlib.sha256(artifact).hexdigest()
assert sha=='f239c3a4ddf249251d04ccaa6567cc940f93a2781db49ccec1c1c043167d22fe'
r={'assertions':len(checks),'checks':checks,'status':'pass','reviewed_artifact_sha256':sha,'scope':'Exact consistency and source-checklist controls. The embedded disk and Hurewicz theorem are established analytically in REVIEW.md, not by these checks.'}
Path('independent_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
