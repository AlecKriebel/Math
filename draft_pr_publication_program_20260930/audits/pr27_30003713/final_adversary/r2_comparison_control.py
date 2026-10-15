"""Independent exact r2 kappa/alpha comparison in the primary proof.
Multilinear degree4 only; the natural proof is reviewed separately.
"""
from itertools import combinations
from pathlib import Path
import sympy as S,json,hashlib

def wedge(w):
 return tuple(sorted(w)),(-1)**sum(a>b for i,a in enumerate(w) for b in w[i+1:])
basis=[(t,next(x for x in range(4) if x not in t)) for t in combinations(range(4),3)]
target=[(t,tuple(x for x in range(4) if x not in t)) for t in combinations(range(4),2)]
bi={b:i for i,b in enumerate(basis)};ti={b:i for i,b in enumerate(target)}
K=S.zeros(6,4);e=S.zeros(4);tau=S.zeros(6)
for j,(t,w) in enumerate(basis):
 # Exterior coproduct3->2+1, followed by product with final singleton.
 for i in range(3):
  pair=t[:i]+t[i+1:];last,sgn=wedge((t[i],w));K[ti[pair,last],j]+=(-1)**(2-i)*sgn
 # Product3+1 then coproduct4->3+1, normalized by4.
 word,sgn=wedge(t+(w,))
 for i in range(4):e[bi[word[:i]+word[i+1:],word[i]],j]+=S.Rational(sgn*(-1)**(3-i),4)
for j,(a,b) in enumerate(target):tau[ti[b,a],j]=1
J=2*e-S.eye(4)
assert e**2==e and e.rank()==1 and J**2==S.eye(4)
assert K.rank()==4 and tau*K==K*J
# Under projection onto its first summand the r2 kernel's coefficient swap
# is -tau-alpha, whose multiplicities are1 sign and3 trivial.
rho=-J
assert rho.charpoly().as_expr().expand()==((S.Symbol('lambda')+1)*(S.Symbol('lambda')-1)**3).expand()
out={'status':'PASS','r2_kappa_injective_rank':K.rank(),'projection_rank_Lambda4':e.rank(),'tau_alpha_comparison_verified':True,'kernel_place_swap_eigenvalue_multiplicities':{'minus1_sign':1,'plus1_trivial':3},'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Multilinear r2 primary comparison, exact rational; no all-degree solution.'}
Path(__file__).with_name('R2_COMPARISON_RECEIPT.json').write_text(json.dumps(out,indent=2,default=int)+'\n');print(json.dumps(out,default=int))
