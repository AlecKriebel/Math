"""Independent exact checks of the direct-pole proof's finite algebra/arithmetic.

These checks corroborate the universal argument in COMPARISON_DERIVATION.md;
they are not a proof of all periods or a historical priority certificate.
Run only with the assigned existing scientific Python and -B.
"""
from pathlib import Path
from fractions import Fraction
from math import gcd
import datetime, hashlib, json
import sympy as S

BASE=Path(__file__).resolve().parent
checks={}
x,y,z,w,a,b,t,s,c,e,k=S.symbols('x y z w a b t s c e k', nonzero=True)
D=x*w-y*z; q=x*x+y*y; r=z*z+w*w
checks['radial_quadratic_telescopes']=[S.expand(D*(x*z-y*w)-(q*z*w-r*x*y))==0,
 S.expand(D*(x*w+y*z)-(q*w*w-r*y*y))==0]
# Both endpoint normal equations for the explicitly half-shifted outer point.
# sn(t+/-delta)=(s*c0*e0 +/- s0*c*e)/den, cn=(c*c0 -/+ s*s0*e*e0)/den.
s0,c0,e0=S.symbols('s0 c0 e0',nonzero=True)
den=1-k*k*s*s*s0*s0
for sign in [-1,1]:
 sn=(s*c0*e0+sign*s0*c*e)/den
 cn=(c*c0-sign*s*s0*e*e0)/den
 val=S.together(sn*e0*s/c0+cn*c/c0-1)
 numerator=S.fraction(val)[0]
 numerator=S.expand(numerator).subs(e0**2,1-k*k*s0*s0).subs(c**2,1-s*s)
 checks['outer_tangent_endpoint_%+d'%sign]=S.expand(numerator)==0
# Orthogonal foot for real nonzero normal, checked bilinearly as a rational identity.
mx,my=S.symbols('mx my'); foot=S.Matrix([mx,my])+(1-mx*x-my*y)*S.Matrix([x,y])/q
checks['foot_on_tangent']=S.factor(x*foot[0]+y*foot[1]-1)==0
checks['foot_displacement_parallel_normal']=S.factor((foot[0]-mx)*y-(foot[1]-my)*x)==0
# Any two principal parts parallel to one normal have zero double-pole determinant.
rho,sigma=S.symbols('rho sigma')
checks['parallel_residue_double_pole_cancels']=S.expand(rho*x*sigma*y-rho*y*sigma*x)==0

rows=[]
for N in range(3,201):
 for tau in range(1,(N+1)//2):
  if gcd(tau,N)!=1: continue
  collision=any((4*tau*j-N)%(2*N)==0 for j in range(N))
  assert collision == (N%4==0)
  # A determinant has adjacent Jacobi poles iff h is a 2K multiple.
  adjacent_jacobi=(2*tau)%N==0
  assert not adjacent_jacobi
  extra_pedal=(4*tau)%N==0
  assert extra_pedal == (N==4)
  phi=lambda j:(1-j)%N
  psi=lambda j:(-j)%N
  assert all(phi(phi(j))==j and phi(j+1)==(phi(j)-1)%N for j in range(N))
  assert all(psi(psi(j))==j and psi(j+1)==(psi(j)-1)%N for j in range(N))
  fixed=[j for j in range(N) if phi(j)==j]
  assert len(fixed)==(1 if N%2 else 0)
  if fixed:
   # At u=zp-delta this fixed foot lands at a removable Jacobi-pole value.
   shift=Fraction(4*tau,N)*(Fraction(fixed[0])-Fraction(1,2))
   assert shift.denominator==1 and shift.numerator%2==0
  rows.append({'N':N,'tau':tau,'complementary_pole_sets_collide':collision,
               'extra_adjacent_foot_coincidence':extra_pedal,'odd_self_paired_foot_count':len(fixed)})

def det(p,q): return p[0]*q[1]-p[1]*q[0]
def area(points): return sum(det(p,points[(i+1)%len(points)]) for i,p in enumerate(points))/2
pts=[(Fraction(1),Fraction(0)),(Fraction(-4,5),Fraction(3,7)),(Fraction(-4,5),Fraction(-3,7))]
repeat_checks=[]
for repeat in range(1,17):
 assert area(pts*repeat)==repeat*area(pts)
 repeat_checks.append({'repeat':repeat,'area_scale_exact':True,'product_scale':repeat*repeat})
assert all(all(v) if isinstance(v,list) else v for v in checks.values())
result={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'formal_algebra_checks':checks,'primitive_arithmetic_cases':len(rows),'N_range':[3,200],
 'covered_primitive_cases':sum(not r['complementary_pole_sets_collide'] for r in rows),
 'excluded_4_divisible_cases':sum(r['complementary_pole_sets_collide'] for r in rows),
 'arithmetic_rows':rows,'repetition_controls':repeat_checks,
 'verdict':'PASS for all encoded exact finite/algebraic assertions',
 'limits':'No finite range certifies the universal theorem; no numerical geometry, manuscript execution, independence of provenance or historical priority is certified.'}
(BASE/'COMPARISON_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('arithmetic_rows','repetition_controls')},indent=2))
