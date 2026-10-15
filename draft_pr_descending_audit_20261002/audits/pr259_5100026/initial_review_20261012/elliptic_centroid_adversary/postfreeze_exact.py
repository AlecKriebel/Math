"""Post-freeze independent controls for submitted formulas and odd-repeat boundary."""
import json,sys,platform,math
from pathlib import Path
from datetime import datetime,timezone
sys.path.insert(0,str(Path(__file__).resolve().parent/'vendor'))
import sympy as z
checks={}
h,l,m,n=z.symbols('h l m n')
M=z.Matrix([m,n]);rs=[z.Matrix([h,l]),z.Matrix([-h,l]),z.Matrix([-h,-l]),z.Matrix([h,-l])]
def antipedal(r,s):
 mat=z.Matrix.vstack((r-M).T,(s-M).T)
 return mat.inv()*z.Matrix([r.dot(r)-M.dot(r),s.dot(s)-M.dot(s)])
mean=sum([antipedal(rs[i],rs[(i+1)%4]) for i in range(4)],z.zeros(2,1))/4
claimed=z.Matrix([m/2*((l*l-n*n)/(h*h-m*m)-1),n/2*((h*h-m*m)/(l*l-n*n)-1)])
checks['submitted_unrestricted_rectangle_formula']=[z.factor(e)==0 for e in mean-claimed]
lx,ly,qx,qy,mx,my=z.symbols('lx ly qx qy mx my');L=z.Matrix([lx,ly]);Q=z.Matrix([qx,qy]);Mp=z.Matrix([mx,my])
J=lambda x:z.Matrix([-x[1],x[0]])
det=lambda a,b:a[0]*b[1]-a[1]*b[0]
V=lambda Mv,Qv:-L.dot(L)*J(Qv-Mv)/det(L,Qv-Mv)
checks['residue_leading_first_equation']=z.factor(L.dot(V(Mp,Q))-L.dot(L))==0
checks['residue_leading_second_equation']=z.factor((Q-Mp).dot(V(Mp,Q)))==0
checks['submitted_total_residue_identity']=[z.factor(e)==0 for e in V(Mp,Q)+V(Mp,-Q)-V(-Mp,Q)-V(-Mp,-Q)]
# Exact odd least-period three construction: b²=1,a²=8/5,lambda=8/9,k²=27/32.
f=z.sqrt(z.Rational(3,5));M=z.Matrix([f,0]);rs=[z.Matrix([-4/z.sqrt(5),1]),z.Matrix([4/z.sqrt(5),1]),z.Matrix([0,-3])]
oddvals=[antipedal(rs[i],rs[(i+1)%3]) for i in range(3)]
oddmean=z.simplify(sum(oddvals,z.zeros(2,1))/3)
checks['exact_odd_3_centroid']=[z.simplify(e)==0 for e in oddmean-z.Matrix([z.sqrt(15)/3,-z.Rational(6,5)])]
checks['exact_odd_3_strict_caustic']=bool(z.Rational(8,5)>1 and 0<z.Rational(8,9)<1)
checks['exact_odd_3_modulus']=z.simplify((z.Rational(8,5)-1)/(z.Rational(8,5)-z.Rational(8,9))-z.Rational(27,32))==0
# sn v=2sqrt2/3,cn v=1/3,dn v=1/2, canonical v=2K/3.
S=2*z.sqrt(2)/3;C=z.Rational(1,3);D=z.Rational(1,2);k2=z.Rational(27,32);den=1-k2*S**4
checks['exact_odd_3_sn_duplication']=z.simplify(2*S*C*D/den-S)==0
checks['exact_odd_3_cn_duplication']=z.simplify((C*C-S*S*D*D)/den+C)==0
checks['exact_odd_3_dn_duplication']=z.simplify((D*D-k2*S*S*C*C)/den-D)==0
checks['exact_odd_3_twice_repeated_not_invariant']=bool(oddmean[1]!=0)
count=0;ok=True
for N in range(4,402,2):
 for winding in range(1,N//2):
  if math.gcd(N,winding)!=1:continue
  count+=1
  # Coordinate unit K/N: delta=4 winding; pole separation2K is2N.
  ok=ok and winding%2==1 and (N//2*4*winding)%(4*N)==2*N
  if N>=6:ok=ok and len({0,N-1,N//2,N//2-1})==4
checks['finite_integer_star_bookkeeping']=ok
allpass=all(all(v) if isinstance(v,list) else v for v in checks.values())
print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'sympy':z.__version__,'postfreeze':True,'checks':checks,'integer_cases':count,'odd_centroid_exact':[str(e) for e in oddmean],'all_pass':allpass},indent=2))
if not allpass:raise SystemExit(1)
