"""Replay a rank-two F7 local system and its twisted Fox determinant.
External representation/group fixture: Wada (1994), section 6, pp.254-255.
Source-derived inputs are deliberately not bundled; pass --input /path/to/fixture.json.
This verifies one representation, not an enumeration of all representations.
"""
import argparse, hashlib, json
from pathlib import Path
import sympy as s
from sympy.polys.matrices import DomainMatrix
u=s.symbols('u'); I=s.eye(2); F=s.GF(7).frac_field(u)
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--input',required=True,help='External JSON fixture transcribed from the cited primary source; not bundled.')
args=parser.parse_args()
input_path=Path(args.input)
input_bytes=input_path.read_bytes()
data=json.loads(input_bytes)
rho={int(j):s.Matrix(a) for j,a in data['rho'].items()}
mod=lambda M:M.applyfunc(lambda x:int(x)%7)
if any(int(rho[j].det())%7!=1 or int(rho[j].trace())%7!=2 for j in rho):
 raise RuntimeError('Not a meridian-trace-two SL2 representation')
for j in list(rho):rho[-j]=rho[j].inv_mod(7)
inv=lambda w:[-a for a in w[::-1]]
lhs=data['lhs'];rhs=data['rhs']
rels=[a+inv(b) for a,b in zip(lhs,rhs)]
def evaluate(w):
 M=I
 for j in w:M=mod(M*rho[j])
 return M
for r in rels:
 if evaluate(r)!=I or sum(1 if x>0 else -1 for x in r)!=0:
  raise RuntimeError('Group representation or abelianization relation fails')

def fox(r,j):
 pre=I; exp=0; out=s.zeros(2)
 for a in r:
  if a==j:out+=u**exp*pre
  elif a==-j:out-=u**(exp-1)*mod(pre*rho[a])
  pre=mod(pre*rho[a]);exp+=1 if a>0 else -1
 return out.applyfunc(s.expand)
blocks=[[fox(r,j) for j in range(1,5)] for r in rels]
for row in blocks:
 foxsum=sum((row[j-1]*(u*rho[j]-I) for j in range(1,5)),s.zeros(2))
 DM=DomainMatrix.from_Matrix(foxsum).convert_to(F)
 if not DM.is_zero_matrix:raise RuntimeError('Fox fundamental identity fails')
M=s.Matrix.vstack(*[s.Matrix.hstack(*row[:3]) for row in blocks])
DM=DomainMatrix.from_Matrix(M).convert_to(F)
num=DM.det()
den=DomainMatrix.from_Matrix(u*rho[4]-I).convert_to(F).det()
tau=num/den
expected=F.from_sympy(sum(int(c)*u**i for i,c in enumerate(data['reference_torsion_coefficients_low_to_high'])))
ratio=tau/expected
# Wada torsions have Laurent unit indeterminacy; record it rather than suppress it.
ratio_sym=F.to_sympy(ratio)
rat_num,rat_den=s.fraction(ratio_sym)
if len(s.Poly(rat_num,u).terms())!=1 or len(s.Poly(rat_den,u).terms())!=1:
 raise RuntimeError(('Unexpected torsion',str(tau),str(ratio)))
comm=evaluate([1,2,-1,-2])
if comm==I:raise RuntimeError('Representation unexpectedly abelian')
def canonical_polynomial(z):
 P=s.Poly(s.expand(z),u,domain=s.QQ)
 return s.Add(*[(int(c.p)*pow(int(c.q),-1,7)%7)*u**e[0] for e,c in P.terms()])
def canonical_rational(z):
 a,b=s.fraction(s.cancel(F.to_sympy(z)))
 return str(canonical_polynomial(a)) if b==1 else '('+str(canonical_polynomial(a))+')/('+str(canonical_polynomial(b))+')'
result={'field':'F_7' ,'input_sha256':hashlib.sha256(input_bytes).hexdigest(),'input_source':data['source_url'],
 'input_bundled':False,'all_relations_verified':True,'all_meridians_trace_two':all(int(rho[j].trace())%7==2 for j in range(1,5)),
 'nonabelian_commutator':[[int(x) for x in row] for row in comm.tolist()],'fox_fundamental_identity_verified':True,
 'deleted_generator':4,'fox_matrix_dimension':[6,6],
 'fox_determinant':canonical_rational(num),'denominator_determinant':canonical_rational(den),
 'computed_torsion':canonical_rational(tau),'normalized_computed_torsion':canonical_rational(tau/F.from_sympy(u**2)),
 'computed_over_reference_Laurent_unit':str(ratio_sym),
 'unknot_parabolic_torsion':'1/(u-1)^2',
 'scope':'One explicit genuine local system; no all-representation enumeration or Jones reconstruction.'}
Path(__file__).with_name('HIGHER_RANK_KT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
