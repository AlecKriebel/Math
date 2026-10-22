from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json, math
import sympy as s
import mpmath as mp

ROOT=Path(__file__).resolve().parent
checks=[]
def exact(name, expression):
    residual=s.factor(s.cancel(expression))
    if residual != 0: raise AssertionError((name,residual))
    checks.append({"name":name,"kind":"symbolic_rational_identity","pass":True})
a,b,c,u,v,t=s.symbols("a b c u v t", positive=True)
X=a*(a+v)*(a-u)/((a-b)*(a+c))
Y=b*(b+v)*(u-b)/((a-b)*(b+c))
Z=c*(c-v)*(c+u)/((a+c)*(b+c))
exact("surface equation",X/a+Y/b+Z/c-1)
coords=[(X,1),(Y,1),(Z,-1)]
def g(i,j): return sum(sign*s.diff(q,i)*s.diff(q,j)/(4*q) for q,sign in coords)
Ru=u/((a-u)*(u-b)*(c+u))
Rv=v/((a+v)*(b+v)*(c-v))
exact("confocal diagonal horizontal metric",g(u,u)-(u+v)*Ru/4)
exact("confocal diagonal vertical metric",g(v,v)+(u+v)*Rv/4)
exact("confocal orthogonality",g(u,v))
P0=lambda x:-x*(a-x)*(b-x)*(c+x)
exact("DR surviving positive horizontal differential",u*u/P0(u)-Ru)
exact("DR surviving positive vertical differential",v*v/P0(-v)-Rv)
n=(a-b)/a
m=c/(b+c)
k2=n*m
C2=4*b*b/(a*(b+c))
x=b/(1-n*t)
y=b*m*t/(1-m*t)
exact("DLMF right interval endpoint b",x.subs(t,0)-b)
exact("DLMF right interval endpoint a",x.subs(t,1)-a)
exact("DLMF left interval endpoint 0",y.subs(t,0))
exact("DLMF left interval endpoint c",y.subs(t,1)-c)
exact("right pullback squared",Ru.subs(u,x)*s.diff(x,t)**2*4*t*(1-t)-C2/((1-n*t)**2*(1-k2*t)))
exact("left pullback squared",Rv.subs(v,y)*s.diff(y,t)**2*4*t*(1-t)-C2*m*m*t*t/((1-m*t)**2*(1-k2*t)))
exact("DLMF parameter product",n*m-k2)
exact("DLMF complete residue factor",C2-4*(1-n)*(1-m))
M=s.symbols("M",positive=True)
exact("rotation conversion",(s.pi-s.pi*M)/(2*s.pi*M)-(1-M)/(2*M))
A,r,period=s.symbols("A r period",positive=True)
cc=A*((1+2*r/period)**2-1)
exact("axisymmetric squared target",A/(A+cc)-(period/(period+2*r))**2)
# Exact physical parity and least-period check; no quadrature involved.
sample_count=0
for q in range(1,20):
 for p in range(1,20):
  if math.gcd(p,q)!=1: continue
  sample_count += 1
  least=math.lcm(2,q)
  actual=next(N for N in range(1,2*q+1) if N%2==0 and (N*p)%q==0)
  if least!=actual: raise AssertionError((p,q))
checks.append({"name":f"physical parity least arcs for {sample_count} coprime rational samples","kind":"exact_integer_check","pass":True})
mp.mp.dps=70
numerical=[]
for aa,bb,cc in [(4,1,3),(4,1,8),(5,2,7),(2,1,100),(2,1,'0.00001'),('1.00001',1,2),(100,1,2),(3,2,1)]:
 aa,bb,cc=map(mp.mpf,(aa,bb,cc))
 nn=(aa-bb)/aa; mm=cc/(bb+cc); kk=nn*mm; C=2*bb/mp.sqrt(aa*(bb+cc))
 # Positive trigonometric integrals are independently parametrized.
 Iu=2*mp.quad(lambda th:mp.sqrt((aa*mp.sin(th)**2+bb*mp.cos(th)**2)/(cc+aa*mp.sin(th)**2+bb*mp.cos(th)**2)),[0,mp.pi/2])
 Iv=2*cc*mp.quad(lambda th:mp.sin(th)**2/mp.sqrt((aa+cc*mp.sin(th)**2)*(bb+cc*mp.sin(th)**2)),[0,mp.pi/2])
 right=C*mp.ellippi(nn,kk)
 left=C*(mp.ellippi(mm,kk)-mp.ellipk(kk))
 errors=[abs(Iu-right),abs(Iv-left),abs(Iu+Iv-mp.pi)]
 if max(errors)>mp.mpf('1e-55'): raise AssertionError((aa,bb,cc,errors))
 numerical.append({"a":str(aa),"b":str(bb),"c":str(cc),"max_abs_error":str(max(errors)),"pass":True})
record={"at":datetime.now(timezone.utc).isoformat(),"sympy":s.__version__,"mpmath":mp.__version__,"script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),"exact_check_count":len(checks),"exact_checks":checks,"diagnostic_quadrature_cases":numerical,"numerical_proof_status":"diagnostic only; symbolic substitutions and analytic text supply proof","all_passed":True}
(ROOT/'INDEPENDENT_CHECK_RESULTS.json').write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps({"exact_check_count":len(checks),"quadrature_cases":len(numerical),"all_passed":True}))
