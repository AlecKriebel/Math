"""Fresh exact Euclidean control. Example inputs are published in Ferudun 0062 §6.
Uses direct lines/projections and inversion, not submitted Jacobi or pole code.
Run with the designated ALWAYS-B Python (SymPy available). Finite control only.
"""
import datetime, json
from pathlib import Path
import sympy as s
A2=s.Integer(21); B2=s.Integer(16); lam=s.Rational(336,25)
a=s.sqrt(A2); b=s.sqrt(B2); c=s.sqrt(A2-B2)
phases={
 'H':[(a,0),(-3*a/5,s.Rational(16,5)),(-3*a/5,-s.Rational(16,5))],
 'V':[(0,b),(-s.Rational(21,5),-s.Rational(8,5)),(s.Rational(21,5),-s.Rational(8,5))]}
def simp(x): return s.radsimp(s.simplify(x))
def V(x):return s.Matrix(x)
def det(x,y):return simp(x[0]*y[1]-x[1]*y[0])
def area(P):return simp(sum(det(P[j],P[(j+1)%len(P)]) for j in range(len(P)))/2)
def foot(F,U,W):
 d=W-U
 return s.simplify(U+d*((F-U).dot(d))/d.dot(d))
def inverse(F,P):return s.simplify(F+(P-F)/(P-F).dot(P-F))
def zero(x):return simp(x)==0
checks=[]
def check(label,value):
 ok=bool(value);checks.append({'check':label,'pass':ok})
 if not ok:raise AssertionError(label)
rows={}
for name,raw in phases.items():
 P=[V(x) for x in raw];n=[V((p[0]/A2,p[1]/B2)) for p in P]
 outer=[]
 for j in range(3):
  M=s.Matrix([[n[j][0],n[j][1]],[n[(j+1)%3][0],n[(j+1)%3][1]]])
  check(name+' finite tangent intersection '+str(j),M.det()!=0)
  outer.append(s.simplify(M.inv()*V((1,1))))
 for j in range(3):
  p=P[j];pr=P[(j-1)%3];pn=P[(j+1)%3]
  check(name+' boundary '+str(j),zero(p[0]**2/A2+p[1]**2/B2-1))
  vin=(p-pr)/s.sqrt((p-pr).dot(p-pr));vout=(pn-p)/s.sqrt((pn-p).dot(pn-p))
  reflected=vin-2*vin.dot(n[j])/n[j].dot(n[j])*n[j]
  check(name+' unit specular reflection '+str(j),all(zero(x) for x in reflected-vout))
  d=pn-p;nn=V((d[1],-d[0]));h=nn.dot(p)
  check(name+' common strict elliptic caustic '+str(j),zero(h*h-(A2-lam)*nn[0]**2-(B2-lam)*nn[1]**2))
  contact=V(((A2-lam)*nn[0]/h,(B2-lam)*nn[1]/h))
  t=simp((contact-p).dot(d)/d.dot(d))
  check(name+' contact lies strictly inside edge '+str(j),bool(t>0) and bool(t<1))
 row={'original_area':str(area(P)),'outer_area':str(area(outer)),'foci':{}}
 for e in [-1,1]:
  F=V((e*c,0));outfeet=[];chordfeet=[];inverted=[]
  for j,p in enumerate(P):
   # Actual outer side from consecutive tangent intersections.
   q=foot(F,outer[(j-1)%3],outer[j]);outfeet.append(q)
   direct=s.simplify(F+(1-n[j].dot(F))/n[j].dot(n[j])*n[j])
   check(name+f' focus {e} tangent versus actual outer side {j}',all(zero(x) for x in q-direct))
   check(name+f' focus {e} classical auxiliary circle {j}',zero(q.dot(q)-A2))
   chordfeet.append(foot(F,p,P[(j+1)%3]));inverted.append(inverse(F,p))
  B=area(outfeet);C=area(inverted);D=area(chordfeet)
  for poly,label in [(outfeet,'outer feet'),(inverted,'original inverses')]:
   check(name+f' focus {e} reversal {label}',zero(area(list(reversed(poly)))+area(poly)))
   check(name+f' focus {e} triple traversal {label}',zero(area(poly*3)-3*area(poly)))
  row['foci'][str(e)]={'outer_pedal_area':str(B),'original_chord_pedal_area':str(D),'original_inverse_area':str(C)}
 rows[name]=row
 # Check products and focus-swapped scale; do not infer universal result from these two phases.
 Bs={e:s.sympify(row['foci'][str(e)]['outer_pedal_area']) for e in [-1,1]}
 Cs={e:s.sympify(row['foci'][str(e)]['original_inverse_area']) for e in [-1,1]}
 Ds={e:s.sympify(row['foci'][str(e)]['original_chord_pedal_area']) for e in [-1,1]}
 check(name+' target product',zero(Bs[-1]*Bs[1]-s.Rational(12544,25)))
 check(name+' inverse product',zero(Cs[-1]*Cs[1]-s.Rational(1,324)))
 for e in [-1,1]:
  check(name+f' swapped-focus scale {e}',zero(Bs[e]-s.Rational(2016,5)*Cs[-e]))
  check(name+f' chord/outer scale in two tested phases {e}',zero(Ds[e]-s.Rational(24,125)*Bs[e]))
 check(name+' objects are not equal',not zero(Bs[1]-Cs[1]) and not zero(Bs[1]-Ds[1]))
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':'exact finite rational/quadratic-field Euclidean controls','parameters':{'a_squared':str(A2),'b_squared':str(B2),'lambda':str(lam)},'all_checks_pass':all(x['pass'] for x in checks),'check_count':len(checks),'checks':checks,'phases':rows,'proved_by_this_code':'Only the exact displayed finite cases and elementary geometry checks. General trace proportionality is established in CHECKABLE_TRANSFER.md, not by sampling.','limitations':'No novelty certificate; no all-period computational claim; example inputs reused from published primary, checker independently authored.'}
Path(__file__).with_name('EXACT_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['checks']},indent=2))
