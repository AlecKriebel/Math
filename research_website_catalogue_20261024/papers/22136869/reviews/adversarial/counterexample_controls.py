#!/usr/bin/env python3
"""Independent exact falsification of the p.12 ansatz necessity assertion.

Written after a targeted counterexample suggestion from the parent, without
reading another reviewer's code or report. No submitted verification imports.
"""
from collections import Counter
from datetime import datetime,timezone
from fractions import Fraction as R
from itertools import product,combinations
from pathlib import Path
import hashlib,json,sys
import sympy as s

assert s.__version__=='1.14.0'
counts=Counter()
def ck(b,k):
    if not b:raise AssertionError(k)
    counts[k]+=1
def eq(a,b,k):ck(a==b,k)
h=5**(-s.Rational(1,4));F=s.QQ.algebraic_field(h)
def cv(x):return F.from_sympy(s.sympify(x))
zero,one=cv(0),cv(1)
def multiply(xs):
    q=one
    for x in xs:q*=x
    return q
def iv(a):
    # Positive h is isolated by 2/3<h<7/10; exact rational Horner bounds.
    v=(R(0),R(0));z=(R(2,3),R(7,10))
    for c in a.to_list():
        terms=[x*y for x in v for y in z]
        c=R(int(c.numerator),int(c.denominator))
        v=(min(terms)+c,max(terms)+c)
    return v
def pos(a):return iv(a)[0]>0
eq((cv(h)**4)*5,one,'field_relation')
ck(5*R(2,3)**4-1<0<5*R(7,10)**4-1,'rational_root_bracket')
# f(t)=5t^4-1 is strictly increasing for t>0, proving unique positive root.
K=[one,cv(s.Rational(1,2)),cv(s.Rational(1,2)),cv(s.Rational(1,2))]
U=[one,cv(h/3),cv(h),cv(s.Rational(1,3))]
V=[one,cv(h),cv(h/3),cv(s.Rational(1,3))]
S=[one,cv(3*h*h/4),cv(s.Rational(1,4)),cv(s.Rational(1,4))]
T=[one,cv(s.Rational(1,4)),cv(3*h*h/4),cv(s.Rational(1,4))]
P=[one,cv((5*h**3+h)/4),cv((5*h**3+h)/4),cv(h*h)]
B=[one,cv(h*h/2),cv(h*h/2),cv(5*h*h/12)]
alpha=[K[i]**2*P[i] for i in range(4)]
beta=[K[i]*B[i] for i in range(4)]
tree=[alpha,beta,beta]
edge={'L':K,'R':K,'U':U,'V':V,'A2':S,'A3':S,'B2':T,'B3':T,'D2':K,'D3':K}
arcs=[('rho','1','L'),('rho','u','R'),('u','p','U'),('u','q','V'),('p','r2','A2'),('q','r2','B2'),('p','r3','A3'),('q','r3','B3'),('r2','2','D2'),('r3','3','D3')]
chars=((1,1,1,1),(1,1,-1,-1),(1,-1,1,-1),(1,-1,-1,1))
def xor(values):
    k=0
    for x in values:k^=x
    return k
def children(es):
    out={v:[] for a,b,e in es for v in (a,b)}
    for a,b,e in es:out[a].append((b,e))
    return out
def retained(a,b):
    excluded={'B2' if a else 'A2','B3' if b else 'A3'}
    return [e for e in arcs if e[2] not in excluded]
graphs=[retained(a,b) for a,b in product([0,1],repeat=2)]
def descendant_sets(es):
    ch=children(es)
    def go(v):
        if v in ['1','2','3']:return {int(v)-1}
        return set().union(*(go(w) for w,e in ch[v])) if ch[v] else set()
    return {e:go(b) for a,b,e in es}
ds=[descendant_sets(g) for g in graphs]
M={}
for y,z in product(range(4),repeat=2):
    M[y,z]=(S[y]*S[z]*U[y^z]+S[y]*T[z]*U[y]*V[z]+T[y]*S[z]*U[z]*V[y]+T[y]*T[z]*V[y^z])/4
    eq(M[y,z],P[y^z]*B[y]*B[z],'all_16_core_factorizations')
eq(cv(s.Rational(1,4))/cv(s.Rational(1,4)),one,'ratio_e_over_d_is_one')
ck(one!=cv(s.Rational(6,5)),'claimed_ratio_is_false')
q={}
for lab in product(range(4),repeat=3):
    x,y,z=lab
    val=zero
    if xor(lab)==0:
        for D in ds:val+=multiply([edge[e][xor(lab[i] for i in leaves)] for e,leaves in D.items()])/4
        eq(val,K[x]**2*K[y]*K[z]*M[y,z],'literal_graph_vs_core')
    q[lab]=val
    eq(val,multiply([tree[i][lab[i]] for i in range(3)]) if xor(lab)==0 else zero,'all_64_fourier_collision')
def trans(a):
    row=[sum((a[k]*chars[k][j] for k in range(4)),zero)/4 for j in range(4)]
    return [[row[i^j] for j in range(4)] for i in range(4)]
def prune(es,mat,pat):
    ch=children(es)
    def go(v):
        if v in ['1','2','3']:return [cv(int(i==pat[int(v)-1])) for i in range(4)]
        msg=[one]*4
        for child,label in ch[v]:
            cm=go(child);A=mat[label]
            msg=[msg[i]*sum((A[i][j]*cm[j] for j in range(4)),zero) for i in range(4)]
        return msg
    return sum(go('rho'),zero)/4
minimum_transition=None
for name,a in {**edge,'effective_L':[K[i]**2 for i in range(4)],'tree1':alpha,'tree2':beta}.items():
    for x in a[1:]:ck(pos(x) and pos(one-x),'strict_eigenvalue_bounds')
    for row in trans(a):
        eq(sum(row,zero),one,'row_sum_one')
        for x in row:
            ck(pos(x),'strict_transition_positivity')
            minimum_transition=min(minimum_transition,iv(x)[0]) if minimum_transition is not None else iv(x)[0]
    for i,j in combinations(range(4),2):eq(trans(a)[i][j],trans(a)[j][i],'matrix_symmetry')
mat={name:trans(a) for name,a in edge.items()}
tmat={str(i):trans(a) for i,a in enumerate(tree)}
tes=[('rho',str(i+1),str(i)) for i in range(3)]
p={}
for pat in product(range(4),repeat=3):
    p[pat]=sum((v*multiply([cv(chars[lab[i]][pat[i]]) for i in range(3)]) for lab,v in q.items()),zero)/64
    direct=sum((prune(g,mat,pat) for g in graphs),zero)/4
    eq(direct,p[pat],'all_64_ordinary_network_pruning')
    eq(prune(tes,tmat,pat),p[pat],'all_64_ordinary_tree_pruning')
    ck(pos(p[pat]),'all_64_pattern_positivity')
eq(sum(p.values(),zero),one,'pattern_normalization')

# Exact symbolic free-e check: the same ansatz admits a whole open interval of
# alternatives. Reduce numerator polynomials modulo 5H^4-1, without importing
# or accepting the candidate B as a numerical certificate.
H,E=s.symbols('H E');f=s.Poly(5*H**4-1,H,domain=s.QQ.frac_field(E))
UU=[1,H/3,H,s.Rational(1,3)];VV=[1,H,H/3,s.Rational(1,3)]
SS=[1,3*H**2/4,s.Rational(1,4),E];TT=[1,s.Rational(1,4),3*H**2/4,E]
BB=[1,H**2/2,H**2/2,5*E*H**2/3];PP=[1,(5*H**3+H)/4,(5*H**3+H)/4,H**2]
for y,z in product(range(4),repeat=2):
    residual=(SS[y]*SS[z]*UU[y^z]+SS[y]*TT[z]*UU[y]*VV[z]+TT[y]*SS[z]*UU[z]*VV[y]+TT[y]*TT[z]*VV[y^z])/4-PP[y^z]*BB[y]*BB[z]
    rem=s.rem(s.Poly(residual,H,domain=s.QQ.frac_field(E)),f)
    ck(rem.is_zero,'symbolic_free_e_factorization')
# Negative control: force B_T=B_C (an extra JC condition, not stated in the
# displayed positive ansatz). The e=1/4 example then fails at (T,T).
badB=B[:];badB[3]=badB[1]
ck(M[3,3]!=P[0]*badB[3]**2,'extra_jc_B_restriction_is_material')
# The supplied theorem's chosen e=3/10 is included, rather than contradicted.
eq(s.simplify((5*E*H**2/3).subs(E,s.Rational(3,10))-H**2/2),0,'published_witness_is_family_member')
result={'status':'COUNTEREXAMPLE_CONFIRMED','utc':datetime.now(timezone.utc).isoformat(),
        'python':sys.version,'sympy':s.__version__,'assertions':sum(counts.values()),'families':len(counts),'counts':dict(counts),
        'target':'Published PDF p12, positive ansatz paragraph after Theorem12; TeX lines414–422',
        'parameters':{'h':'positive root of 5h^4-1','tau':'1/3','b':'h','kappa':'3h^2','d':'1/4','e':'1/4','e_over_d':'1','P':'(1,(5h^3+h)/4,(5h^3+h)/4,h^2)','B':'(1,h^2/2,h^2/2,5h^2/12)'},
        'minimum_certified_transition_lower_bound':str(minimum_transition),
        'minimum_certified_pattern_lower_bound':str(min(iv(x)[0] for x in p.values())),
        'scope':'Falsifies e/d=6/5 necessity from the displayed positive ansatz and tau=1/3 alone. Does not falsify the chosen witness or Theorems12–19.',
        'extra_condition':'Equal nontrivial B coordinates would be an additional JC normalization and excludes this counterexample; it is not stated in the displayed positive ansatz paragraph.',
        'independence':'Targeted candidate supplied by parent after independent full-manuscript read. No other reviewer report/code consulted; all arithmetic, graph reconstruction and state pruning independently implemented.',
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('counterexample_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
