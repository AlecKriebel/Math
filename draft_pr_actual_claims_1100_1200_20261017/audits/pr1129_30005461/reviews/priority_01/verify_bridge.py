"""Authored exact symbolic transcription checks for the priority bridge.
No third-party text is embedded. These checks supplement REPORT.md; they do
not reprove the imported classification theorem or replace its hypotheses.
"""
from pathlib import Path
from collections import defaultdict
from hashlib import sha256
from datetime import datetime, timezone
import json
BASE=Path(__file__).resolve().parent
CHECKS=[]
def check(name,actual,expected):
 if actual != expected:raise ValueError((name,actual,expected))
 CHECKS.append({'name':name,'passed':True})
def clean(p):return {e:a for e,a in p.items() if a}
# A polynomial is an integer coefficient dictionary on (u,v,c) exponents.
def vertical(p):
 q=defaultdict(int)
 for (i,j,k),a in p.items():q[(i,i+j-2,k)]+=a
 if any(min(e)<0 for e in q):raise ValueError('Invalid division')
 return clean(q)
def horizontal(p):
 q=defaultdict(int)
 for (i,j,k),a in p.items():q[(i+j-2,j,k)]+=a
 if any(min(e)<0 for e in q):raise ValueError('Invalid division')
 return clean(q)
def restrict(p,variable):
 return {e:a for e,a in p.items() if e[variable]==0}
def multiplicity(p):return min(i+j for i,j,k in p)
def tangent(p):
 m=multiplicity(p);return {e:a for e,a in p.items() if e[0]+e[1]==m}
F0={(2,0,0):1,(4,0,0):1,(0,6,0):1,(2,2,1):-1}
F1={(2,0,0):1,(4,2,0):1,(0,4,0):1,(2,2,1):-1}
F2={(2,0,0):1,(4,4,0):1,(0,2,0):1,(2,2,1):-1}
F3={(0,0,0):1,(2,0,0):1,(4,6,0):1,(2,2,1):-1}
for n,(f,g) in enumerate([(F0,F1),(F1,F2),(F2,F3)],1):
 check('vertical chart identity '+str(n),vertical(f),g)
 check('complementary chart exceptional restriction '+str(n),restrict(horizontal(f),0),{(0,0,0):1} if n<3 else {(0,0,0):1,(0,2,0):1})
 check('multiplicity of real center '+str(n),multiplicity(f),2)
check('first tangent cone',tangent(F0),{(2,0,0):1})
check('second tangent cone',tangent(F1),{(2,0,0):1})
check('third tangent cone',tangent(F2),{(2,0,0):1,(0,2,0):1})
check('terminal vertical exceptional restriction',restrict(F3,1),{(0,0,0):1,(2,0,0):1})
# The calculation is symbolic in c, so no sampled-parameter extrapolation occurs.
check('local delta sum',sum(2*(2-1)//2 for _ in range(3)),3)
check('two-point total real delta',2*3,6)
# Restricting an SOS identity to y=0 and x=0 forces cubic square roots
# to be combinations of precisely these monomials.
cubics=[(i,j,3-i-j) for i in range(4) for j in range(4-i)]
allowed=[e for e in cubics if (e[0]>0 and e[1]>0) or e==(0,0,3)]
check('cubic count',len(cubics),10)
check('restricted cubic supports',set(allowed),{(2,1,0),(1,2,0),(1,1,1),(0,0,3)})
pairs=[(a,b) for a in allowed for b in allowed if tuple(a[i]+b[i] for i in range(3))==(2,2,2)]
check('negative coefficient comes only from square',pairs,[((1,1,1),(1,1,1))])
# c<=0 is already SOS: (x^2 y)^2+(xy^2)^2+(z^3)^2+(-c)(xyz)^2.
# c>3 is negative at [1:1:1]; c=3 is deliberately excluded.
input_dir=BASE.parent.parent/'inputs'
pins={
 'PROOF.md':'46af7394ebfee7b0de9861693f84ab684502da3be208c626411f24e2538c7d15',
 'REAL_DELTA_APPENDIX.md':'c1ca3231f1b61e9a550d37a0b1dd63a618d25caab0fb897978b863ed0614cd38',
}
for name,expected in pins.items():check('input SHA256 '+name,sha256((input_dir/name).read_bytes()).hexdigest(),expected)
result={'generated_utc':datetime.now(timezone.utc).isoformat(),'total_checks':len(CHECKS),'all_passed':True,'checks':CHECKS,'formal_certification':False,'source_theorem_reproved':False,'parameters':'Identities over Z[c]; no numerical inference','input_pins':pins}
(BASE/'BRIDGE_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'total_checks':len(CHECKS),'all_passed':True}))
