"""Independent exact diagnostics; analytic universal arguments remain in DERIVATIONS."""
from pathlib import Path
from itertools import product, permutations
import json
import sympy as s
D=Path(__file__).resolve().parent
def require(c,m):
    if not c: raise RuntimeError(m)
R=s.Rational
h=(1,2,3); triples=[(x,y,x^y) for x,y in product(range(4),repeat=2)]
spectra={a:{0:s.Integer(1),**{j:s.Symbol(a+str(j)) for j in h}} for a in 'abcdef'}
l=s.Symbol('l'); a,b,c,d,e,f=[spectra[z] for z in 'abcdef']
def q(t):
    x,y,z=t
    return a[x]*b[y]*c[z]*(l*f[y]*d[z]+(1-l)*f[x]*e[z])
qs={t:q(t) for t in triples}; Q={t:s.Symbol('q'+''.join(map(str,t))) for t in triples}
quartic_terms=[(1,[(0,0,0),(1,2,3),(2,3,1),(3,1,2)]),(-1,[(0,0,0),(1,3,2),(2,1,3),(3,2,1)]),(-1,[(0,1,1),(1,2,3),(2,0,2),(3,3,0)]),(1,[(0,1,1),(1,3,2),(2,2,0),(3,0,3)]),(1,[(0,2,2),(1,0,1),(2,1,3),(3,3,0)]),(-1,[(0,2,2),(1,1,0),(2,3,1),(3,0,3)]),(-1,[(0,3,3),(1,0,1),(2,2,0),(3,1,2)]),(1,[(0,3,3),(1,1,0),(2,0,2),(3,2,1)])]
F=sum(sign*s.prod(Q[t] for t in ts) for sign,ts in quartic_terms)
identity_counts=[]
for perm in [(0,1,2),(1,0,2),(0,2,1)]:
    sub={Q[t]:qs[tuple(t[i] for i in perm)] for t in triples}
    require(s.expand(F.xreplace(sub))==0,'quartic literal pullback')
    identity_counts.append(perm)
variables=[spectra[z][j] for z in 'abcdef' for j in h]+[l]
base={v:R(1,3) if str(v).startswith('f') else R(1,2) for v in variables}; base[l]=R(1,2)
rows=[t for t in triples if t!=(0,0,0)]
J=s.Matrix([[s.diff(qs[t],v).subs(base) for v in variables] for t in rows])
require(J.rank()==14,'rank14')
baseq={Q[t]:qs[t].subs(base) for t in triples}
grad=s.Matrix([s.diff(F,Q[t]).subs(baseq) for t in rows])
require(grad.T*J==s.zeros(1,19),'quartic conormal')
require(sorted(set(abs(v) for v in grad))==[0,R(1,6912)],'exact nonzero gradient')
rank_fixed={}
for model,blocks in [('JC',[(1,2,3)]),('K2P',[(1,3),(2,)]),('K3P',[(1,),(2,),(3,)])]:
    cols=[]
    for z in 'abcdef':
        for block in blocks: cols.append(sum((J[:,variables.index(spectra[z][j])] for j in block),s.zeros(15,1)))
    cols.append(J[:,-1]); M=s.Matrix.hstack(*cols)
    rank_fixed[model]={'rank':M.rank(),'parameters':M.cols,'fibre':M.cols-M.rank()}
require([v['rank'] for v in rank_fixed.values()]==[4,9,14],'tied ranks')
# F linear in q011: primitive coefficient binomial and explicit coprimality witness.
coef=s.diff(F,Q[(0,1,1)]); rem=F.subs(Q[(0,1,1)],0)
special={v:0 for v in Q.values()};special.update({Q[(0,0,0)]:1,Q[(1,3,2)]:1,Q[(2,1,3)]:1,Q[(3,2,1)]:1})
require(coef.subs(special)==0 and rem.subs(special)==-1,'coprimality witness')
# Character transpositions act alternately. An omitted term cannot pass this identity.
for p in permutations(h):
    mapping={0:0,**dict(zip(h,p))}; sign=(-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
    require(s.expand(F.xreplace({Q[t]:Q[tuple(mapping[j] for j in t)] for t in triples})-sign*F)==0,'alternation')
wrong=F-s.prod(Q[t] for t in quartic_terms[0][1])
require(s.expand(wrong.xreplace({Q[t]:qs[t] for t in triples}))!=0,'omitted monomial negative control')
# A valid positive K2P edge whose coordinatewise square root is not stochastic.
sv,gv=R(81,100),R(63,100)
require(gv>2*sv-1 and sv<1 and gv<1,'strict positive edge')
require(gv<R(16,25),'sqrt(g)<4/5 forces negative inverse Fourier margin')
rho=R(199,200); require(gv/rho>2*sv/rho-1 and max(sv,gv)<rho,'isotropic division works')
# Freeness fails at an excluded unmarked degree2 factor, succeeds at degree3.
anchor=s.Matrix([[1,1,0],[1,0,1],[0,1,1]])
require(anchor.det()==-2,'anchor exponent determinant')
u,v=s.symbols('u v',positive=True)
cherry=s.Matrix([u/v,u*v]).jacobian([u,v]).det()
require(s.simplify(cherry-2*u/v)==0,'cherry determinant')
result={'literal_quartic_pullbacks_zero_for_three_orientations':identity_counts,'ranks':rank_fixed,'gradient_nonzero_entries':sum(v!=0 for v in grad),'gradient_absolute_value':'1/6912','quartic_omission_rejected':True,'strict_positive_non_square_root_divisible_edge':{'s':str(sv),'g':str(gv),'rho':str(rho)},'anchor_determinant':str(anchor.det()),'cherry_sector_determinant':str(cherry),'scope':'Exact identities and rank witnesses; universal topology/analytic claims require the written derivations and imported finite certificates.'}
(D/'INDEPENDENT_EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
