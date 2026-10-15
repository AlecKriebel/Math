#!/usr/bin/env python3
"""Independent algebra controls; the universal descent argument is in FINDINGS.md."""
from pathlib import Path
import datetime,hashlib,itertools,json
import sympy as s
checks=[]
def require(name,ok):
    if not bool(ok): raise RuntimeError(name)
    checks.append(name)
def zero(m):return all(s.simplify(e)==0 for e in m)
def canonical(m):
    m=m.applyfunc(s.simplify)
    first=next(v for v in m if v!=0)
    return tuple(s.simplify(v/first) for v in m)
def mat(t):return s.Matrix(2,2,t)
I=s.I
identity=s.eye(2)
v4=[identity,s.diag(-1,1),s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-1],[1,0]])]
R=s.diag(I,1);S=s.Matrix([[1,1],[1,-1]])
gens=[R,S];group={canonical(identity)};todo=list(group)
while todo:
    t=todo.pop()
    for g in gens:
        n=canonical(mat(t)*g)
        if n not in group: group.add(n);todo.append(n)
require('octahedral normalizer generated has order24',len(group)==24)
vkeys=[canonical(g) for g in v4]
def action(m):
    return tuple(vkeys.index(canonical(m*e*m.inv())) for e in v4)
actions={action(mat(g)) for g in group}
require('all six actions on three nonidentity V4 elements',len(actions)==6)
require('conjugation kernel is exactly V4', {g for g in group if action(mat(g))==(0,1,2,3)}==set(vkeys))
require('Galois conjugation fixes every quotient permutation',all(action(mat(g).conjugate())==action(mat(g)) for g in group))
rational=[g for g in group if all(s.im(x)==0 for x in g)]
require('normalizer only8 of24 Q rational',len(rational)==8)
require('rational normalizer quotient has order2, not S3',len({action(mat(g)) for g in rational})==2)
require('R conjugate differs by V4, not generally equal',canonical(R.conjugate())!=canonical(R) and canonical(R.conjugate()*R.inv()) in vkeys)

# Derive descended translation directly from the elliptic chord law,
# reducing b using F(e)=0, rather than quoting the packet formula.
X,e,a=s.symbols('X e a')
b=-e**3-a*e
F=X**3+a*X+b
chord_x=s.cancel(F/(X-e)**2-X-e)
phi=e+(3*e**2+a)/(X-e)
require('chord law gives projective translation',s.cancel(chord_x-phi)==0)
Me=s.Matrix([[e,2*e**2+a],[1,-e]])
require('involution square equals Fprime(e) times I',zero(Me*Me-(3*e**2+a)*identity))
require('determinant equals minus Fprime(e)',s.expand(Me.det()+3*e**2+a)==0)
require('matrix action matches chord derived function',s.cancel((Me[0,0]*X+Me[0,1])/(Me[1,0]*X+Me[1,1])-phi)==0)

# Use two free roots and eliminate third plus a; all are exact identities
# on the open discriminant locus, not sampling evidence for that locus.
u,v=s.symbols('u v');w=-u-v;aa=-(u*u+u*v+v*v)
roots=[u,v,w]
Ms=[Me.subs({e:r,a:aa}) for r in roots]
for j,k in itertools.permutations(range(3),2):
    ell=3-j-k;prod=Ms[j]*Ms[k]
    # Projective equality tested by all Plucker cross products of4 entries.
    require(f'translation product{j}{k} equals remaining{ell}',all(s.expand(prod[p]*Ms[ell][q]-prod[q]*Ms[ell][p])==0 for p in range(4) for q in range(4)))
for j,m in enumerate(Ms):
    require(f'nonzero determinant{j} on distinct root locus',s.factor(m.det())==s.factor(-s.prod(roots[j]-roots[k] for k in range(3) if k!=j)))
for j,k in itertools.combinations(range(3),2):
    require(f'distinct nonidentity translations{j}{k}',s.expand(Ms[j][3]-Ms[k][3])!=0)
# Galois equivariance follows universally from M_e coefficients in k[e].
require('translation entries use only singled-out root and rational coefficients',all(not val.has(u,v) for val in Me))

# Exercise all4 finite image possibilities for cubic etale actions over Q.
T=s.symbols('T')
cubics=[('trivial',(T-1)*(T-2)*(T-3),False,True,True),('C2',(T-2)*(T*T+1),False,False,True),('C3',T**3-3*T+1,True,True,False),('S3',T**3-T-1,True,False,False)]
cubic_results=[]
for label,f,irreducible,square_disc,has_root in cubics:
    P=s.Poly(f,T,domain=s.QQ);disc=P.discriminant()
    require(label+' separable',disc!=0)
    require(label+' irreducibility pattern',bool(P.is_irreducible)==irreducible)
    require(label+' discriminant square pattern',bool(disc>=0 and s.sqrt(disc).is_Rational)==square_disc)
    rational_roots=[r for r in s.polys.polytools.ground_roots(P)]; require(label+' rational root pattern',bool(rational_roots)==has_root)
    cubic_results.append({'label':label,'polynomial':str(s.expand(f)),'discriminant':str(disc),'rational_roots':list(map(str,rational_roots))})

# Finite cocycle direction control in a genuinely nonabelian model.
# This is a finite model check, not a replacement for the symbolic proof.
perms=list(itertools.permutations(range(3)))
def compose(p,q):return tuple(p[q[j]] for j in range(3))
def inv(p):return tuple(p.index(j) for j in range(3))
idp=(0,1,2)
for h0,p,q in itertools.product(perms,repeat=3):
    # Twisted action sigma(g)=p g p^-1; quotient coboundary obeys law.
    sigma_h=compose(compose(p,h0),inv(p))
    b_p=compose(inv(h0),sigma_h)
    tau_h=compose(compose(q,h0),inv(q))
    b_q=compose(inv(h0),tau_h)
    lhs=compose(inv(h0),compose(compose(compose(p,q),h0),inv(compose(p,q))))
    rhs=compose(b_p,compose(compose(p,b_q),inv(p)))
    if lhs!=rhs: raise RuntimeError('nonabelian coboundary law')
require('216 nonabelian coboundary order controls',True)

result={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sympy_version':s.__version__,'assertions':len(checks),'checks':checks,'cubic_actions':cubic_results,'scope':'Exact generic algebra and finite normalizer/cocycle controls. Classification, Hilbert90, conic descent and all-field moduli argument require separate mathematical proof.','status':'PASS'}
Path(__file__).with_name('RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','assertions':len(checks),'normalizer_order':len(group),'rational_normalizer_order':len(rational),'cubic_action_types':[x['label'] for x in cubic_results]}))
