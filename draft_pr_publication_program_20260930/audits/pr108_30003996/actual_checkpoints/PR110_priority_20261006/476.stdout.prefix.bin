from fractions import Fraction as F
from pathlib import Path
import json,hashlib
checks=0;chords=0
def ratcirc(t):return (1-t*t)/(1+t*t),2*t/(1+t*t)
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def solve(A,b):
 D=A[0][0]*A[1][1]-A[0][1]*A[1][0]
 assert D
 return ((b[0]*A[1][1]-A[0][1]*b[1])/D,(A[0][0]*b[1]-b[0]*A[1][0])/D)
for aa,bb,cc in [(5,4,3),(5,3,4),(13,12,5),(17,8,15)]:
 a,b,c=map(F,[aa,bb,cc])
 for j in range(-12,13):
  C,S=ratcirc(F(j,7));D2=C*C/(a*a)+S*S/(b*b)
  for k in range(1,16):
   U,V=ratcirc(F(k,30));lam=V*V/D2
   if not (0<lam<b*b):continue
   A=(a*(C*U+S*V),b*(S*U-C*V));B=(a*(C*U-S*V),b*(S*U+C*V))
   assert dot((C/a,S/b),A)==U and dot((C/a,S/b),B)==U;checks+=1
   assert U*U-(c/a)**2*C*C==(b*b-lam)*D2;checks+=1
   RR=[]
   for sign in [1,-1]:
    focus=(sign*c,F(0));v1=tuple(x-y for x,y in zip(A,focus));v2=tuple(x-y for x,y in zip(B,focus))
    Q=solve([v1,v2],[dot(v1,v1),dot(v2,v2)])
    H=U-sign*c/a*C
    assert H>0;checks+=1
    r1=a-sign*c*(C*U+S*V);r2=a-sign*c*(C*U-S*V)
    assert dot(v1,v1)==r1*r1 and dot(v2,v2)==r2*r2;checks+=1
    R=r1*r2/H
    assert dot(Q,Q)==D2*R*R;checks+=1
    expanded=(a*a+b*b*lam/(b*b-lam))*U+sign*(-a*c+c/a*b*b*lam/(b*b-lam))*C
    assert R==expanded;checks+=1
    RR.append(R)
   assert RR[0]-RR[1]==2*c/a*(-a*a+b*b*lam/(b*b-lam))*C;checks+=1
   # Remove the common sqrt(D2) from the telescoping identity using sqrt(lam)*sqrt(D2)=V.
   assert (RR[0]-RR[1])*V==c/(a*b)*(-a*a+b*b*lam/(b*b-lam))*(B[1]-A[1]);checks+=1
   chords+=1
r={'assertions':checks,'rational_chords_checked':chords,'all_pass':True,'scope':'Exact antipedal line intersections and positive-distance identities for confocal ellipse chords; all-N closure follows from the written telescoping proof.'}
if Path('PROOF.md').exists():r['artifact_sha256']=hashlib.sha256(Path('PROOF.md').read_bytes()).hexdigest()
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
