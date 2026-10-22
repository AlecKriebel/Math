"""Exact algebraic and finite incidence checks for the enriched-configuration report."""
import itertools, json
from pathlib import Path
import sympy as s
from sympy.polys.matrices import DomainMatrix
u=s.symbols('u')
A=s.Matrix([[1,0],[-1,1]])
M=u*A-A.T
Delta=s.factor(M.det())
B=s.simplify((1-u)*M.inv())
bar=lambda X:X.applyfunc(lambda z:s.cancel(z.subs(u,1/u)))
checks={
 'alexander_determinant':str(Delta),
 'module_matrix':str(M),
 'pairing_matrix_conjugate_first':str(B),
 'hermitian_exact':all(s.cancel(z)==0 for z in B-bar(B).T),
 'right_relation_matrix':str(s.simplify(B*M)),
 'left_relation_matrix':str(s.simplify(bar(M).T*B)),
 'self_pairing_minus_u_over_delta':str(s.cancel(B[0,0]-u/Delta)),
 'mirror_negates_pairing':all(s.cancel(z)==0 for z in ((1-u)*(-M).inv()+B)),
 'generator_relation_e2':str((u-1)/u),
 'norm_of_a_plus_b_zeta':'a^2 + a*b + b^2',
 'norm_completed_square':'(a+b/2)^2 + 3*b^2/4'
}
if not checks['hermitian_exact'] or not checks['mirror_negates_pairing']:
 raise RuntimeError('Pairing matrix identity failed')
if s.cancel(B[0,0]-u/Delta)!=-1:
 raise RuntimeError('Unexpected self-pairing residue')

# The nonminimal neutral coefficient system (1,1,-1,-1).
n=4; w=[1,1,-1,-1]; edges=list(itertools.combinations(range(n),2))
def components(S):
 parts=[{i} for i in range(n)]
 for e in S:
  a,b=edges[e]; ia=next(i for i,c in enumerate(parts) if a in c); ib=next(i for i,c in enumerate(parts) if b in c)
  if ia!=ib:
   parts[ia]|=parts[ib];parts.pop(ib)
 return parts

def stalkdim(S,q):
 p=components(S)
 if any(sum(w[i] for i in c)!=0 for c in p):return 0
 b=len(p)
 # Hc(M) is k in degrees 2 and 3, so coefficient of x^q in (x^2+x^3)^b.
 return int(s.binomial(b,q-2*b)) if 0<=q-2*b<=b else 0

E2={};chainchecks=[]
for q in range(2,7):
 bases=[]
 for p in range(6):
  bases.append([(S,j) for S in itertools.combinations(range(6),p+1)
                for j in range(stalkdim(S,q))])
 maps=[]
 for p in range(5):
  rows={x:i for i,x in enumerate(bases[p+1])};mat=s.zeros(len(rows),len(bases[p]))
  for j,(S,k) in enumerate(bases[p]):
   for e in set(range(6))-set(S):
    T=tuple(sorted(S+(e,)))
    if (T,k) not in rows:continue
    # Surviving restriction maps can only be full-diagonal identities here.
    if len(components(S))!=1 or len(components(T))!=1:
     raise RuntimeError('Unexpected non-full-diagonal map requiring geometric input')
    mat[rows[(T,k)],j]=(-1)**T.index(e)
  maps.append(mat)
 for a,b in zip(maps,maps[1:]):
  if b*a!=s.zeros(b.rows,a.cols):raise RuntimeError('d^2 != 0')
 ranks=[DomainMatrix.from_Matrix(a).convert_to(s.QQ).rank() for a in maps]
 dims=[len(bases[p])-(ranks[p-1] if p else 0)-(ranks[p] if p<5 else 0) for p in range(6)]
 for p,d in enumerate(dims):
  if d:E2[(p,q)]=d
 chainchecks.append({'q':q,'dimensions':[len(x) for x in bases],'differential_ranks':ranks,'E2_dimensions':dims})
expected={(1,4):2,(1,5):4,(1,6):2,(2,2):6,(2,3):6}
if E2!=expected:raise RuntimeError((E2,expected))
ordinary={}
for (p,q),d in E2.items():
 i=12-(p+q+1)
 ordinary[i]=ordinary.get(i,0)+d
if ordinary!={4:2,5:4,6:8,7:6}:raise RuntimeError(ordinary)
result={'blanchfield_algebra':checks,'nonminimal_neutral_E2':[{'p':p,'q':q,'rank':d} for (p,q),d in sorted(E2.items())],
        'ordinary_betti_numbers':ordinary,'cochain_checks':chainchecks,
        'scope':'Exact matrix identities and finite Cech ranks; report proves naturality and collapse.'}
Path(__file__).with_name('EXACT_ENRICHMENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
