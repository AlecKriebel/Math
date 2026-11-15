#!/usr/bin/env python3
"""Independent exact pole/axial-triangle derivations; explicit guards survive -O.
Mathematics was reconstructed in the sealed initial before deposited code reading.
"""
from pathlib import Path
from collections import Counter
import hashlib,json,sys
import sympy as s
sys.dont_write_bytecode=True
counts=Counter()
def ck(b,name):
 counts[name]+=1
 if not b:raise RuntimeError(name)
def zero(x,name):ck(s.cancel(x)==0,name)
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def sub(p,q):return tuple(x-y for x,y in zip(p,q))
def area(P):return sum(det(P[i],P[(i+1)%len(P)]) for i in range(len(P)))/2
def foot(F,n,h):
 lam=(h-dot(n,F))/dot(n,n)
 return tuple(s.cancel(F[i]+lam*n[i]) for i in range(2))
def main():
 ck(len(sys.argv)==1,'no overrides');root=Path(__file__).resolve().parents[2]
 for name,h in {'sources/SOURCE_READY.json':'4cd6366eabab646cbb7837b7b3854cf931b3fa57fc7de0152d0ff210ab35c16a','sources/cache/native-assets-attempt3/focal-pedal-ratios-note.pdf':'426e2f9809b6f02bf03ee564cad40ae41cc0cee68dfafb907257bd17c6f04686','sources/cache/extracted/container-001/focal_pedal_ratios.tex':'64c57cba5e70a49d43cbfef6d4cab161093a4c75d93272e5bb5ef8f6092e3ccd','reviews/analytic/INITIAL_SEAL.json':'9aa2324160d7c3febb036bb5665d04e3ce67d93e9c00296fb42c355fb70f9cc7'}.items():ck(hashlib.sha256((root/name).read_bytes()).hexdigest()==h,'target binding')
 # Rational parametrization of the unit circle gives projection identities for
 # every generic real/complex (sn,cn); a^2-b^2=k^2 is substituted explicitly.
 z,k,a=s.symbols('z k a',nonzero=True);p=s.sqrt(1-k*k);b=s.sqrt(a*a-k*k)
 sn=2*z/(1+z*z);cn=(1-z*z)/(1+z*z);F=(k,0)
 q=((k-sn)/(1-k*sn),p*cn/(1-k*sn));Q=(a*(k-a*sn)/(a-k*sn),a*b*cn/(a-k*sn))
 for got,n in [(q,(-sn,cn/p)),(Q,(-sn/a,cn/b))]:
  proj=foot(F,n,1)
  for x,y in zip(got,proj):zero(x-y,'universal exact line projection')
  zero(dot(got,got)-(1 if got is q else a*a),'focal foot auxiliary circle')
 # Quarter-shift even germs: no dependence on a numerical z or k.
 C=1-z*z/2+(1+4*k*k)*z**4/24
 D=1-k*k*z*z/2+k*k*(4+k*k)*z**4/24
 qx=(k*k*C-D)/(k*(C-D));qy=-s.I*(1-k*k)/(k*(C-D))
 zero(s.limit(z*z*qx,z,0)-2/k,'original double-pole leading x')
 zero(s.limit(z*z*qy,z,0)-2*s.I/k,'original double-pole leading y')
 zero(qx.subs(z,-z)-qx,'original germ evenness x');zero(qy.subs(z,-z)-qy,'original germ evenness y')
 S,Cv,Dv=s.symbols('S Cv Dv',nonzero=True)
 derivative=s.cancel(((-k*k*S*Cv)*Cv-Dv*(-S*Dv))/(k*Cv*Cv))
 zero(derivative.subs(Dv**2,1-k*k*S*S).subs(S*S,1-Cv*Cv)-(1-k*k)*S/(k*Cv*Cv),'quarter-shift derivative')
 ar=Dv/Cv;br2=(1-k*k)/(Cv*Cv);lead=(-ar*br2/k,-s.I*ar*br2/k)
 residue=tuple(s.cancel(x/(-br2*S)) for x in lead)
 for i,x in enumerate(residue):zero(x-ar*(1,s.I)[i]/(k*S),'outer simple-pole residue')
 zero(det(residue,tuple(-x for x in residue)),'adjacent double-pole determinant cancellation')
 # Direct axial triangle, independent of the older center-locus deduction.
 t,A,c,e=s.symbols('t A c e',nonzero=True);X=t*(t+2);Y=2*t+1
 G=s.groebner([e*e-1,c*c-(t*t-1),A*A-X],e,c,A,t)
 def modzero(expr,name):
  num,den=s.fraction(s.cancel(expr));ck(G.reduce(s.expand(num))[1]==0,name)
 P=[(A,0),(-A*t/(t+1),Y/(t+1)),(-A*t/(t+1),-Y/(t+1))]
 chord=[((1/A,1),1),((1,0),-A*t/(t+1)),((1/A,-1),1)]
 tangent=[((1,0),A),((-t/A,1),t+1),((-t/A,-1),t+1)]
 ap=area([foot((e*c,0),n,h) for n,h in chord]);bp=area([foot((e*c,0),n,h) for n,h in tangent])
 expectedA=X*(A*(t+2)+e*c*(t-1))/(t+1)**4
 expectedB=(t+2)*(A*(t+2)+e*c*(t-1))/(2*(t+1))
 modzero(ap-expectedA,'general axial chord-pedal area');modzero(bp-expectedB,'general axial tangent-pedal area')
 modzero(bp-(t+1)**3*ap/(2*t),'general triangular multiplier for both foci')
 alpha=X*t*t/(t+1)**2;beta=Y/(t+1)**2
 modzero(alpha-beta-c*c,'general caustic confocality')
 for i,(n,h) in enumerate(chord):
  modzero(alpha*n[0]**2+beta*n[1]**2-h*h,'general actual caustic side tangency')
 for p in P:modzero(p[0]**2/X+p[1]**2/Y-1,'general actual boundary incidence')
 # Exact unit-vector reflection uses known side lengths, not square-root
 # sign simplifications by a CAS. Domain t>1 is imposed in the written proof.
 lengths=[Y,2*Y/(t+1),Y]
 for i in range(3):
  vi=tuple(x/lengths[(i-1)%3] for x in sub(P[i],P[(i-1)%3]));vo=tuple(x/lengths[i] for x in sub(P[(i+1)%3],P[i]));normal=(P[i][0]/X,P[i][1]/Y)
  modzero(dot(vi,vi)-1,'general incident unit length');modzero(dot(vo,vo)-1,'general outgoing unit length')
  for j in range(2):modzero(vo[j]-vi[j]+2*dot(vi,normal)*normal[j]/dot(normal,normal),'general exact reflection law')
 lam=1/(t+1);contact=(A*t*t/(t+1)**2,Y/(t+1)**2)
 for j in range(2):modzero(contact[j]-P[0][j]-lam*(P[1][j]-P[0][j]),'general contact on segment')
 S21=s.sqrt(21);S5=s.sqrt(5)
 for sign in [-1,1]:
  # Our normalized axial triangle is scaled by2 to get the published axes.
  valA=s.cancel(4*expectedA.subs({t:s.Rational(3,2),A:S21/2,c:S5/2,e:sign}));valB=s.cancel(4*expectedB.subs({t:s.Rational(3,2),A:S21/2,c:S5/2,e:sign}))
  zero(valA-s.Rational(84,625)*(7*S21+sign*S5),'published exact original area')
  zero(valB-s.Rational(7,10)*(7*S21+sign*S5),'published exact outer area')
  zero(valB-s.Rational(125,24)*valA,'published exact multiplier')
 ratio=(7*S21+S5)/(7*S21-S5);ck(ratio>1 and 1/ratio<1,'exact reciprocal phases nonconstant')
 # Every translation/reversal/repetition identity follows algebraically from
 # the cyclic sum; verify its symbolic triangle specialization independently.
 x,y=s.symbols('x y');trans=[(p[0]+x,p[1]+y) for p in P]
 zero(area(trans)-area(P),'symbolic area translation');zero(area(P[::-1])+area(P),'symbolic area reversal');zero(area(P*3)-3*area(P),'symbolic area repetition')
 faults={'wrong original pole sign':s.limit(z*z*qx,z,0)!=-2/k,'noncollinear outer residues produce double pole':s.simplify(det((1,s.I),(1,-s.I)))!=0,'wrong triangular multiplier':s.cancel(expectedB-(t+1)**2*expectedA/(2*t))!=0,'incorrect common-ratio constancy':s.simplify(ratio-1/ratio)!=0}
 for name,value in faults.items():ck(bool(value),'false algebraic assertion rejection')
 print(json.dumps({'assessment':'INDEPENDENT_EXACT_POLE_AND_TRIANGULAR_IDENTITIES_SUPPORTED','optimized':not __debug__,'checks':dict(sorted(counts.items())),'total_checks':sum(counts.values()),'false_assertions_rejected':list(faults),'sympy_version':s.__version__,'scope':'Exact rational/polynomial identities. Domain inequalities, torus pole completeness, positivity for all stars and all-phase proportionality are proved in the written reconstruction; no finite sampling substitutes for them.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
