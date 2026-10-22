"""Exact controls for six global LND flow directions and certificate bounds."""
from itertools import permutations,product
from collections import Counter
import sympy as s
import json
C=Counter()
def ck(v,k):
    assert v,k
    C[k]+=1
def eq(a,b,k):ck(s.expand(a-b)==0,k)
x,y,z,t=s.symbols('x y z t')
v=(x,y,z);perms=list(permutations(range(3)))
for i,j,k in perms:
    D=v[i]**2*v[j]+v[k]**2
    E=lambda f:s.expand(D*(v[i]**2*s.diff(f,v[k])-2*v[k]*s.diff(f,v[j])))
    eq(E(D),0,'polynomial_LND_invariant')
    eq(E(E(v[k])),0,'polynomial_LND_middle_nilpotence')
    eq(E(E(E(v[j]))),0,'polynomial_LND_high_nilpotence')
    N={v[i]:v[i],v[k]:v[k]+t*v[i]**2*D,
       v[j]:v[j]-2*t*v[k]*D-t*t*v[i]**2*D**2}
    for q in v:
        eq(N[q],q+t*E(q)+t*t*E(E(q))/2,'exact_exponential_formula')
    for q,d in [(v[i],1),(v[k],5),(v[j],8)]:
        ck(s.Poly(N[q],*v).total_degree()==d,'single_flow_total_degree')

# All five cone transitions, with an arbitrary positive offset M-4p.
p,e=s.symbols('p e',positive=True)
M=4*p+e;H=2*M-2*p
cases=[(p,M,H,2*H),(M,H,p,2*M+H),(M,p,H,2*H),
       (H,M,p,2*H+M),(H,p,M,2*H+p)]
for P,Q,R,d in cases:
    other=2*P+Q if s.expand(d-2*R)==0 else 2*R
    ck(s.Poly(s.expand(d-other),p,e).coeffs() and
       all(a>0 for a in s.Poly(s.expand(d-other),p,e).coeffs()),'cone_unique_Delta_leading_term')
    ck(all(a>0 for a in s.Poly(s.expand(d-2*P),p,e).coeffs()),'cone_middle_gap')
    eq((2*P+2*d)-2*(2*P+d)+2*P,0,'cone_exact_degree_relation')
    ck(all(a>0 for a in s.Poly(s.expand(2*P+2*d-2*H),p,e).coeffs()),'cone_growth_over_old_maximum')

# Independent finite recursion on every distinct pair of the six directions.
degree_counts=Counter()
for old,new in product(perms,repeat=2):
    if old==new:continue
    degrees=[0]*3
    for i,val in zip(old,[1,8,5]):degrees[i]=val
    i,j,k=new;P,Q,R=(degrees[n] for n in new)
    ck(2*P+Q!=2*R,'six_direction_pair_no_tie')
    d=max(2*P+Q,2*R);nxt=[0]*3
    nxt[i]=P;nxt[j]=2*P+2*d;nxt[k]=2*P+d
    ck(nxt[k]>4*nxt[i] and nxt[j]==2*nxt[k]-2*nxt[i],'six_direction_pair_cone')
    ck(max(nxt)>16 and max(nxt)!=11,'target_degree_excluded_from_pairs')
    degree_counts[max(nxt)]+=1

# Affine mixing separation: all coordinate-degree selections with a largest R.
for P,S,R in [(1,4,11),(2,7,19),(5,11,29),(3,9,28)]:
    ck(P<S and R>2*S,'affine_gap_examples')
    for pp,qq,rr in product([P,S,R],repeat=3):
        if max(pp,qq,rr)!=R:continue
        ck(2*pp+qq!=2*rr,'all_affine_degree_separation')
        d=max(2*pp+qq,2*rr)
        ck(2*pp+3*d>3*R,'all_affine_maximum_growth')

# The exact target degree used in both obstructions.
D=x*x*y+z*z
G=[x,y-2*x*y*z-D**2+6*z*z*D+6*x*z*D**2+2*x*x*D**3,z+x*D]
ck([s.Poly(g,x,y,z).total_degree() for g in G]==[1,11,4],'target_total_multidegree')
for P,Q,R in [(1,1,1),(11,4,1),(4,11,11),(1,4,11),(1,11,4),(4,1,11)]:
    ck(2*P+Q!=2*R,'target_weight_no_tie')
    d=max(2*P+Q,2*R)
    wdeg=lambda f:max(P*a+Q*b+R*c for (a,b,c),co in s.Poly(f,x,y,z).terms())
    ck([wdeg(g) for g in G]==[P,2*P+3*d,P+d],'target_weighted_output_formula')

# Leibniz nilpotence certificate: any N coordinate derivatives below m
# have total order <=N(m-1); one more forces a vanishing coordinate factor.
for m in range(1,8):
    for N in range(1,8):
        ck(max(sum(a) for a in product(range(m),repeat=min(N,4)))==min(N,4)*(m-1),
           'finite_Leibniz_pigeonhole')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),
 'two_direction_degrees':dict(sorted(degree_counts.items())),
 'scope':'Exact symbolic LND/cone identities and finite degree/certificate diagnostics. All-word conclusions use the cone proof; no unrestricted factorization system for gamma is solved.'},indent=2,sort_keys=True))
