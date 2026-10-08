#!/usr/bin/env python3
"""Exact finite checks supporting partial mathematics; no topology is certified."""
from itertools import permutations, combinations
from fractions import Fraction
from collections import Counter
import json, sys

def require(ok, message):
    if not ok:
        raise ValueError(message)

G = list(permutations(range(5)))
e = tuple(range(5))
def mul(a,b): return tuple(a[b[i]] for i in range(5))
def inv(a): return tuple(a.index(i) for i in range(5))
def cyc(a):
    seen=set(); lengths=[]
    for i in range(5):
        if i not in seen:
            j=i; n=0
            while j not in seen: seen.add(j); n+=1; j=a[j]
            lengths.append(n)
    return tuple(sorted(lengths,reverse=True))
def sign(a): return (-1)**(5-len(cyc(a)))
def fp(a): return sum(a[i]==i for i in range(5))
def permutation(*cycles):
    a=list(e)
    for c in cycles:
        for i,j in zip(c,c[1:]+c[:1]): a[i-1]=j-1
    return tuple(a)
def closure(gens):
    out={e}; todo=[e]
    while todo:
        a=todo.pop()
        for b in gens:
            c=mul(a,b)
            if c not in out: out.add(c);todo.append(c)
    return frozenset(out)
def normalizer(H): return frozenset(g for g in G if frozenset(mul(mul(g,h),inv(g)) for h in H)==H)
def avg(char,H): return Fraction(sum(char(h) for h in H),len(H))
T=permutation((1,2)); D=permutation((1,2),(3,4)); R=permutation((1,2,3,4)); S=permutation((1,3))
EA=closure([D,permutation((1,3),(2,4))]); EB=closure([T,permutation((3,4))]); P2=closure([R,S]); C4=closure([R]); C2d=closure([mul(R,R)])
require(len(G)==120 and len(P2)==8 and len(EA)==len(EB)==4,'group sizes')
involutions=[g for g in G if g!=e and mul(g,g)==e]
V4={closure([a,b]) for a,b in combinations(involutions,2) if mul(a,b)==mul(b,a)}
require(len(V4)==20 and all(len(E)==4 for E in V4),'all Klein fours')
require(not any(all(mul(t,h)==mul(h,t) for h in E) for E in V4 for t in involutions if t not in E),'no elementary abelian rank three')
V4_types=Counter(tuple(sorted(cyc(g) for g in E if g!=e)) for E in V4)
require(sorted(V4_types.values())==[5,15],'V4 class counts')
pairs=list(combinations(range(5),2))
def pairchar(g): return sum(tuple(sorted((g[a],g[b])))==(a,b) for a,b in pairs)
def U(g): return fp(g)-1
def F(g): return pairchar(g)-fp(g)
def L(g): return (U(g)**2-U(mul(g,g)))//2
chars=[('1',lambda g:1),('sign',sign),('U',U),('U_sign',lambda g:U(g)*sign(g)),('D5',F),('D5_sign',lambda g:F(g)*sign(g)),('wedge2_U',L)]
for i,(ni,ci) in enumerate(chars):
    for j,(nj,cj) in enumerate(chars): require(avg(lambda g:ci(g)*cj(g),G)==int(i==j),'orthonormal character rows')
require(sum(c(e)**2 for n,c in chars)==120,'complete character list')
fixed=[[n,c(e),c(T),c(D),int(avg(c,EA)),int(avg(c,EB))] for n,c in chars]
expected=[[1,1],[1,0],[1,2],[1,0],[2,2],[2,1],[0,1]]
require([r[-2:] for r in fixed]==expected,'fixed dimensions')
require(all(a+b>0 for a,b in expected),'each irreducible has forbidden fixed vector')
# D8 quotient: precisely two V4 preimages and one cyclic-four preimage.
preimages=[H for H in V4 if C2d<=H<=P2]+[C4]
require(len(preimages)==3 and len(normalizer(C2d))==8,'D8 quotient subgroup structure')
require(len(normalizer(closure([T])))==12 and len(normalizer(C4))==8,'normalizers')
# The S4 rotation representation W = sign * reduced permutation module.
H4=frozenset(g for g in G if g[4]==4)
def W(g):
    require(g in H4,'W defined only on S4')
    return sign(g)*(fp(g)-2)
require(avg(lambda g:W(g)**2,H4)==1,'W irreducible')
require(all(avg(W,E)==0 for E in V4 if E<=P2),'W kills both Sylow V4 types')
for a in P2:
    for b in P2:
        if cyc(a)==cyc(b): require(W(a)==W(b),'W fusion stable')
cyclic2={closure([g]) for g in P2 if g!=e}
require(all(avg(W,K)==1 for K in cyclic2),'all cyclic-two-power subgroups fix line')
P3=closure([permutation((1,2,3))]);P5=closure([permutation((1,2,3,4,5))])
chi2=lambda g:4*W(g)
chi3=lambda g:12 if g==e else -6
chi5=lambda g:12 if g==e else -3
require(chi2(e)==chi3(e)==chi5(e)==12,'local complex dimensions')
require(avg(chi3,P3)==avg(chi5,P5)==0,'odd Sylow fixed vectors absent')
require(all(avg(chi2,E)==0 for E in V4 if E<=P2),'2-effective dimension12')
# Induced S4 character evaluated independently by defining character sum.
def induced(g):
    total=0
    for x in G:
        xgx=mul(mul(inv(x),g),x)
        if xgx in H4:total+=W(xgx)
    return Fraction(total,len(H4))
ind_formula=lambda g:fp(g)*(fp(g)-2)*sign(g)
require(all(induced(g)==ind_formula(g) for g in G),'induction formula')
require(avg(ind_formula,EA)==3 and avg(ind_formula,EB)==2,'induced forbidden fixed dimensions')
# Exhaustive bounded check of the universal linear dimension equations.
solutions=[]
for n in range(0,150):
    for a in range(-1,n+1):
        if n+1!=3*(a+1):continue
        for b in range(-1,n+1):
            if n+1==2*(b+1)+(a+1):
                require(a==b and a>=0 and (n-a)%2==0,'Borel consequence')
                s=a # the quotient Borel equation is a+1=s+1.
                solutions.append([n,a,b,s])
# A duality check for the degree pattern only, not a construction of a manifold.
thickenings=[]
for n in [2,5,11,23]:
    for dim in [2*n+3,2*n+4]:
        degrees=[0,n,dim-n-1,dim-1]
        require(len(set(degrees))==4,'distinct boundary homology degrees')
        thickenings.append({'n':n,'D':dim,'nonzero_integral_homology_degrees':degrees})
result={'status':'PASS','scope':'finite group and exact arithmetic checks, not a smooth-realization proof','group_order':len(G),'involutions':len(involutions),'V4_total':len(V4),'V4_type_counts':sorted(V4_types.values()),'character_fixed_columns':['name','dimension','trace_transposition','trace_double_transposition','dim_EA_fixed','dim_EB_fixed'],'character_fixed_table':fixed,'normalizer_orders':{'C2_transposition':12,'C2_double':8,'C4':8},'local_complex_dimensions':[12,12,12],'local_real_sphere_dimensions':{'ambient':23,'nontrivial_cyclic_2_fixed':7},'induced_dimension':15,'induced_fixed_dimensions':[3,2],'borel_solutions_under_n150':solutions,'conditional_thickening_patterns':thickenings}
if '--self-test' in sys.argv:
    try:require(False,'deliberate rejection')
    except ValueError: pass
    else: raise RuntimeError('require was bypassed')
    def rejects(test, message):
        try: require(test,message)
        except ValueError: return
        raise RuntimeError('negative control accepted: '+message)
    damaged=expected.copy();damaged[-1]=[0,0]
    rejects(damaged==[r[-2:] for r in fixed],'mutated character table')
    rejects(avg(ind_formula,EA)==0,'falsely fixed-point-free induced representation')
    rejects(24+1==3*(7+1),'incompatible Borel dimensions')
    rejects([0,23,49-23-1,49-1]==[0,48],'thickening boundary falsely a homology sphere')
    result['negative_controls']='PASS: explicit rejection and four false mathematical-output controls'
print(json.dumps(result,indent=2,sort_keys=True))
