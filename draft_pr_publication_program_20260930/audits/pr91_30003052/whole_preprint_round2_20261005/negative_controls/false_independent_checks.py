"""Independent exact controls, not a finite approximation to a Koopman spectrum."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import argparse,hashlib,json,math
import sympy as S

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--artifact", type=Path, default=Path(__file__).resolve().parent.parent / "pr91_note.tex")
parser.add_argument("--output", type=Path)
args = parser.parse_args()
artifact = args.artifact.resolve()
if not artifact.is_file():
    parser.error("artifact file is missing: " + str(artifact))
artifact_sha256 = hashlib.sha256(artifact.read_bytes()).hexdigest()

checks={}
def ck(label,x):
 if not bool(x):
  raise AssertionError(label)
 checks[label]=checks.get(label,0)+1
ck("round2_deliberately_false", False)
def zero(M):return all(S.simplify(v)==0 for v in M)
# An adapted l1 norm, not the submitted l-infinity example.
T=S.Matrix([[1,3,-2,0],[0,1,2,1],[0,0,1,-1],[0,0,0,1]])
Ti=T.inv();D=S.diag(-1,S.I,S.Rational(1,3),S.Rational(1,3));D[2,3]=S.Rational(1,3)
A=T*D*Ti;P=T*S.diag(1,1,0,0)*Ti
ck('adapted_l1_contraction',max(sum(abs(D[i,j]) for i in range(4)) for j in range(4))==1)
ck('projection',P*P==P and A*P==P*A)
ck('projection_adapted_norm',max(sum(abs((Ti*P*T)[i,j]) for i in range(4)) for j in range(4))==1)
ck('projection_not_euclidean_orthogonal',P!=P.conjugate().T)
for n in range(1,21):
 J=S.Matrix([[S.Rational(1,3),S.Rational(1,3)],[0,S.Rational(1,3)]])
 expected=S.Rational(1,3)**n*S.Matrix([[1,n],[0,1]])
 ck('stable_Jordan',J**n==expected)
 ck('distance_stable_part',zero(Ti*(A**n-A**n*P)*T-S.diag(S.zeros(2),expected)))
 if n%4==0:ck('recurrence_subsequence',zero(Ti*(A**n-P)*T-S.diag(S.zeros(2),expected)))
# Left eigenfunctional is available even though the stable block is not semisimple.
ell=Ti[3,:]
ck('left_eigenfunctional',ell*A==ell/3)
for v in product(range(-1,2),repeat=4):
 x=T*S.Matrix(v)
 ck('left_eigenfunctional_points',(ell*A*x)[0]==(ell*x)[0]/3)
 ck('projection_points',P*x==T*S.Matrix([v[0],v[1],0,0]))
# Polynomial identity for arbitrary continuous functions when stable part is nilpotent.
N=S.zeros(4);N[0,0]=S.I;N[1,2]=N[2,3]=1
B=T*N*Ti;Q=T*S.diag(1,0,0,0)*Ti
ck('nilpotent_peripheral_split',B*Q==Q*B and Q*Q==Q)
ck('nilpotent_index',B**3*(S.eye(4)-Q)==S.zeros(4))
ck('global_iterate_identity',B**7==B**3)
x,y,z,w=S.symbols('x y z w');coords=S.Matrix([x,y,z,w]);physical=T*coords
for powers in product(range(3),repeat=4):
 f=lambda row: S.prod(row[i]**powers[i] for i in range(4))
 f0=f(coords)-f(S.Matrix([x,0,0,0]))
 after=f0.subs(dict(zip(coords,N**3*coords)),simultaneous=True)
 ck('vanishing_ideal_nilpotence',S.expand(after)==0)
# Generator groups via rational phases with nonprimitive and repeated generators.
for angles in [(F(2,6),),(F(2,8),F(3,12)),(F(2,5),F(3,7)),(F(0),F(0)),(F(1,3),F(2,3))]:
 denom=math.lcm(*(x.denominator for x in angles));g=math.gcd(denom,*(int(x*denom) for x in angles));order=denom//g
 found={F(0)};front=[F(0)]
 while front:
  v=front.pop()
  for a in angles:
   nxt=(v+a)%1
   if nxt not in found:found.add(nxt);front.append(nxt)
 ck('group_orders',found=={F(j,order) for j in range(order)})
 for a in angles:ck('group_inverse',(-a)%1 in found)
# Exact Cesaro projection of fifth-root frequencies modulo Phi_5.
zeta=S.Symbol('zeta');phi=sum(zeta**j for j in range(5))
for target,freq in product(range(5),repeat=2):
 avg=sum(zeta**(((freq-target)*j)%5) for j in range(5))
 ck('Cesaro',S.rem(avg-5*int(target==freq),phi,zeta)==0)
# Product/conjugate eigenfunctions in phase-exponent notation; no float roots.
for p,q,r,s in product(range(4),repeat=4):
 exp=(p-q)+2*(r-s)
 direct=(p+4*q+2*r+3*s)%5
 ck('monomial_character',exp%5==direct)
# Complex radial exponents tested at all orbit levels, including phase != 1.
for phase in range(7):
 for m in range(1,5):
  for j in range(8):
   # r=1/2, z=m + 2*pi*i*phase/(7*log(r)); values are 2^(-mj)*xi^(phase*j).
   left=(F(1,2)**(m*(j+1)),phase*(j+1)%7)
   right=(F(1,2)**m*F(1,2)**(m*j),(phase+phase*j)%7)
   ck('radial_complex_orbits',left==right)
for r in (F(1,7),F(1,2),F(6,7)):
 for j in range(29):
  t=F(j,28)
  ck('zero_eigenvalue_range',max(F(0),r*t-r)==0)
 ck('zero_eigenfunction_nonzero',1-r>0)
# One-dimensional nilpotent and identity endpoints.
ck('zero_matrix_projection',S.zeros(1)**2==S.zeros(1))
ck('identity_matrix_projection',S.eye(1)**2==S.eye(1))
receipt={'status':'PASS','exact_assertions':sum(checks.values()),'checks':checks,
'artifact_sha256':artifact_sha256,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
'sympy_version':S.__version__,'scope':'Exact finite algebraic diagnostics only; analytic proof steps and the full operator spectrum require separate proof verification.'}

raw = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
if args.output is not None:
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(raw, encoding="utf-8")
print(raw, end="")
