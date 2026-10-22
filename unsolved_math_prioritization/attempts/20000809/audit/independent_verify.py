#!/usr/bin/env python3
"""Independent exact controls: border-basis commutators, adjacent Macaulay
relations, symbolic distraction, and interpolation. Python standard library.
No author modules are imported. No network, source files, or corpora required.
"""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
import json

checks = []
def require(value, label):
    if not value:
        raise AssertionError(label)
    checks.append(label)

def plus(a,b): return tuple(x+y for x,y in zip(a,b))
def minus(a,b): return tuple(x-y for x,y in zip(a,b))
def unit(n,i): return tuple(int(j==i) for j in range(n))
def divisible(a,b): return all(x>=y for x,y in zip(a,b))
def in_ideal(a,G): return any(divisible(a,g) for g in G)
def mons(n,d):
    if n == 1:
        return [(d,)]
    return [(i,)+v for i in range(d+1) for v in mons(n-1,d-i)]

def matrix_rank(rows,n):
    """Independent dense Gauss-Jordan elimination over Q."""
    a = [[Q(row.get(i,0)) for i in range(n)] for row in rows if any(row.values())]
    k=0
    for j in range(n):
        pivot=next((i for i in range(k,len(a)) if a[i][j]),None)
        if pivot is None: continue
        a[k],a[pivot]=a[pivot],a[k]
        c=a[k][j]; a[k]=[z/c for z in a[k]]
        for i in range(k+1,len(a)):
            if a[i][j]:
                c=a[i][j]; a[i]=[z-c*w for z,w in zip(a[i],a[k])]
        k+=1
        if k==len(a): break
    return k

def weighted_kernel(variables,rows):
    groups=defaultdict(list)
    for k,(_,_,weight) in enumerate(variables): groups[weight].append(k)
    out={}
    for w,cols in sorted(groups.items()):
        selected=[{i:row.get(c,0) for i,c in enumerate(cols)} for row in rows]
        nullity=len(cols)-matrix_rank(selected,len(cols))
        if nullity: out[w]=nullity
    # Equations must never combine distinct torus characters.
    require(all(len({variables[c][2] for c,a in row.items() if a})<=1 for row in rows), 'homogeneous equations')
    return out

def border_tangent(B,filtered=False):
    """Linearize all pairwise multiplication commutators at a monomial algebra.
    Multiplication columns inside B are fixed. A border monomial has one shared
    coefficient vector, even if several columns reach it.
    """
    B=sorted(B); bs=set(B); n=len(B[0]); E=[unit(n,i) for i in range(n)]
    border=sorted({plus(b,e) for b in B for e in E}-bs)
    variables=[(a,b,minus(b,a)) for a in border for b in B if not filtered or sum(b)<=sum(a)]
    rows=defaultdict(dict)
    def contribute(key,c,v):
        rows[key][c]=rows[key].get(c,0)+v
        if not rows[key][c]: del rows[key][c]
    for c,(a,b,w) in enumerate(variables):
        for i,j in combinations(range(n),2):
            for q in B:
                qi,qj=plus(q,E[i]),plus(q,E[j])
                # D_i M_j and -D_j M_i.
                if qj in bs and plus(qj,E[i])==a: contribute((i,j,b,q),c,1)
                if qi in bs and plus(qi,E[j])==a: contribute((i,j,b,q),c,-1)
                # M_i D_j and -M_j D_i.
                if qj==a and plus(b,E[i]) in bs: contribute((i,j,plus(b,E[i]),q),c,1)
                if qi==a and plus(b,E[j]) in bs: contribute((i,j,plus(b,E[j]),q),c,-1)
    W=weighted_kernel(variables,list(rows.values()))
    return W, {'border_monomials':len(border),'variables':len(variables),'nonzero_equations':sum(bool(r) for r in rows.values()),'rank':len(variables)-sum(W.values())}

def truncated_tangent(G,r):
    """Macaulay degree-(r+1) neighbor relations, not Taylor LCM syzygies.
    This suffices here since the strongly stable r-truncations, r>=reg(J),
    have linear presentations. The mathematical justification is in the audit.
    """
    n=len(G[0]); E=[unit(n,i) for i in range(n)]
    degree_r=mons(n,r); heads=[a for a in degree_r if in_ideal(a,G)]; tails=[a for a in degree_r if not in_ideal(a,G)]
    variables=[(a,b,minus(b,a)) for a in heads for b in tails]; index={(a,b):i for i,(a,b,w) in enumerate(variables)}
    next_tails={b for b in mons(n,r+1) if not in_ideal(b,G)}; relations=[]
    for a in mons(n,r+1):
        parents=[(i,minus(a,E[i])) for i in range(n) if a[i] and minus(a,E[i]) in heads]
        if len(parents)<2: continue
        i,g=parents[0]
        for j,h in parents[1:]:
            coefficients=defaultdict(dict)
            for b in tails:
                for k,head,sgn in [(i,g,1),(j,h,-1)]:
                    out=plus(b,E[k])
                    if out in next_tails:
                        c=index[head,b]; coefficients[out][c]=coefficients[out].get(c,0)+sgn
            relations.extend(coefficients.values())
    # Independently prove these neighbor syzygies generate all pair syzygies:
    # in each LCM multidegree, its dividing heads are connected by r+1 edges.
    lcmm={tuple(max(x,y) for x,y in zip(a,b)) for a,b in combinations(heads,2)}
    connected=True
    for top in lcmm:
        vertices=[a for a in heads if divisible(top,a)]
        seen={vertices[0]}; stack=[vertices[0]]
        while stack:
            a=stack.pop()
            for b in vertices:
                if b not in seen and sum(max(x,y) for x,y in zip(a,b))==r+1:
                    seen.add(b); stack.append(b)
        connected &= len(seen)==len(vertices)
    require(connected,'Macaulay neighbor syzygy completeness at degree '+str(r))
    W=weighted_kernel(variables,relations)
    return W,{'degree':r,'heads':len(heads),'variables':len(variables),'rank':len(variables)-sum(W.values()),'LCM_connectivity_multidegrees':len(lcmm)}

def weight_list(W): return [{'weight':list(w),'multiplicity':a} for w,a in sorted(W.items())]
def staircase(m): return [(0,j) for j in range(m+1)]+[(1,j) for j in range(m)]
B=staircase(3); G=[(2,0,0),(1,3,0),(0,4,0)]
W,control=border_tangent(B); Wn,filtered_control=border_tangent(B,True)
require(sum(W.values())==14,'border tangent dimension 14')
require(sum(Wn.values())==12,'degree-filtered border tangent dimension 12')
require(W[(-1,2)]==1 and W[(1,-2)]==1,'opposite tangent characters')
require({w:W[w]-Wn.get(w,0) for w in W if W[w]!=Wn.get(w,0)}=={(-1,2):1,(-2,3):1},'precisely two omitted directions')
require(all(3*w[0]+2*w[1]<0 for w in Wn),'naive cocharacter contracts filtered tangent')
require(any(3*w[0]+2*w[1]>0 for w in W),'same cocharacter fails actual tangent')
require(any(3*w[0]+2*w[1]==0 for w in W),'second missing character has zero pairing')
lifted={w+(-sum(w),):a for w,a in W.items()}
truncations=[]
for r in [4,5,7,10]:
    WT,stats=truncated_tangent(G,r)
    require(WT==lifted,'Macaulay truncation restores full character multiset at degree '+str(r))
    truncations.append(stats)
family=[]
for m in range(3,17):
    WW,stats=border_tangent(staircase(m))
    require(sum(WW.values())==4*m+2,'family border tangent dimension m='+str(m))
    require(WW.get((-1,2),0)>0 and WW.get((1,-2),0)>0,'family opposite pair m='+str(m))
    family.append({'m':m,'length':2*m+1,'tangent_dimension':sum(WW.values())})
# Independent enumeration of lower ideals via ordinary partitions, filtered by
# closure under moving a y-factor to x. The author enumerates strict partitions.
def partitions(n,maximum=None):
    if not n: return [()]
    ans=[]
    for a in range(1,min(n,maximum or n)+1):
        ans.extend((a,)+p for p in partitions(n-a,a))
    return ans
small=[]
for d in range(1,7):
    for h in partitions(d):
        b={(i,j) for i,t in enumerate(h) for j in range(t)}
        # Complement is strongly stable iff every B-monomial divisible by x
        # remains in B on replacing that x by y.
        if not all((i-1,j+1) in b for i,j in b if i): continue
        ww,_=border_tangent(list(b))
        witness=next(((a,c) for a in range(1,32) for c in range(1,32) if all(a*w[0]+c*w[1]<0 for w in ww)),None)
        require(sum(ww.values())==2*d,'small plane tangent dimension')
        require(witness is not None,'small plane separating functional')
        small.append({'length':d,'heights':list(h),'negative_cocharacter':list(witness)})
require(len(small)==13,'complete small strongly stable enumeration')
# Explicit Hilbert function and segment obstruction.
HF=[sum(not in_ideal(a,G) for a in mons(3,r)) for r in range(15)]
require(HF==[1,3,5]+[7]*12,'homogeneous Hilbert function')
for r in [4,7,11,30]:
    a,b,c=(2,0,r-2),(0,4,r-4),(1,2,r-3)
    require(in_ideal(a,G) and in_ideal(b,G) and not in_ideal(c,G) and plus(a,b)==plus(c,c),'equal-product nonsegment certificate')
# Symbolic distraction in Q[t,x_1,...,x_n], reducing with x-order while t
# remains a coefficient. Coefficient arithmetic uses exact rational numbers.
def padd(a,b,scale=1):
    out=dict(a)
    for m,c in b.items():
        out[m]=out.get(m,0)+scale*c
        if not out[m]: del out[m]
    return out

def shift(poly,e,c=1): return {plus(a,e):c*v for a,v in poly.items()}
def distracted(alpha):
    n=len(alpha); p={(0,)*(n+1):Q(1)}
    for i,a in enumerate(alpha):
        for j in range(a):
            # Distinct scalars j+1, avoiding the special zero factor.
            p=padd(shift(p,unit(n+1,i+1)),shift(p,unit(n+1,0)),scale=-(j+1))
    return p

def normal_form(poly,gens):
    out={}; p=dict(poly)
    while p:
        term=max(p,key=lambda a:(sum(a[1:]),a[1:],a[0])); c=p[term]
        use=next(((head,g) for head,g in gens if divisible(term[1:],head)),None)
        if use is None:
            out[term]=c; del p[term]
        else:
            head,g=use; e=(term[0],)+minus(term[1:],head)
            p=padd(p,shift(g,e,c),-1)
    return out

def basis_for(G):
    n=len(G[0]); bounds=[]
    for i in range(n):
        bounds.append(min(g[i] for g in G if g[i] and sum(g)==g[i]))
    return [b for b in product(*(range(m) for m in bounds)) if not in_ideal(b,G)]

def det(a):
    a=[[Q(x) for x in row] for row in a]; v=Q(1)
    for j in range(len(a)):
        i=next((i for i in range(j,len(a)) if a[i][j]),None)
        if i is None:return Q(0)
        if i!=j:a[j],a[i]=a[i],a[j];v=-v
        c=a[j][j];v*=c
        for i in range(j+1,len(a)):
            f=a[i][j]/c
            for k in range(j,len(a)):a[i][k]-=f*a[j][k]
    return v

distraction=[]
examples=[[(5,)],[(2,0),(1,3),(0,4)],[(3,0),(0,2)],[(2,0,0),(0,2,0),(0,0,2),(1,1,0)],[(2,0,0,0),(0,2,0,0),(0,0,2,0),(0,0,0,2)]]
for gens in examples:
    pairs=[(g,distracted(g)) for g in gens]; b=basis_for(gens); n=len(gens[0]); count=0
    for (a,f),(c,g) in combinations(pairs,2):
        l=tuple(max(x,y) for x,y in zip(a,c))
        s=padd(shift(f,(0,)+minus(l,a)),shift(g,(0,)+minus(l,c)),-1)
        require(not normal_form(s,pairs),'symbolic distraction Buchberger reduction');count+=1
    for a,f in pairs:
        require({v[1:]:z for v,z in f.items() if v[0]==0}=={a:1},'special fiber is original generator')
    pts=[tuple(v+1 for v in e) for e in b]
    require(len(set(pts))==len(b),'distinct distracted grid points')
    for pt in pts:
        for a,f in pairs:
            ev=sum(c*prod for e,c in f.items() for prod in [__import__('math').prod(v**t for v,t in zip(pt,e[1:]))])
            require(ev==0,'distracted generator vanishes on grid')
    e=[[__import__('math').prod(v**t for v,t in zip(pt,a)) for a in b] for pt in pts]
    determinant=det(e)
    require(determinant!=0,'standard monomials independent on distracted grid')
    distraction.append({'ambient_dimension':n,'length':len(b),'symbolic_S_pairs':count,'evaluation_determinant':str(determinant)})
# Exact char-2 finite-extension control. GF(4)=F2[u]/(u^2+u+1).
def fmul(a,b):
    c=0
    while b:
        if b&1:c^=a
        a<<=1
        if a&4:a^=7
        b>>=1
    return c

def fpow(a,b):
    v=1
    for _ in range(b):v=fmul(v,a)
    return v

def frank(a):
    a=[list(row) for row in a]; k=0
    for j in range(len(a[0])):
        p=next((i for i in range(k,len(a)) if a[i][j]),None)
        if p is None:continue
        a[k],a[p]=a[p],a[k]; inv=fpow(a[k][j],2);a[k]=[fmul(z,inv) for z in a[k]]
        for i in range(k+1,len(a)):
            c=a[i][j]
            if c:a[i]=[v^fmul(c,w) for v,w in zip(a[i],a[k])]
        k+=1
        if k==len(a):break
    return k
pts=B
for p in pts:
    for a in [(2,0),(1,3),(0,4)]:
        v=1
        for coord,degree in zip(p,a):
            for j in range(degree):v=fmul(v,coord^j)
        require(v==0,'characteristic-two distraction vanishing')
mat=[[fmul(fpow(p[0],a[0]),fpow(p[1],a[1])) for a in B] for p in pts]
require(frank(mat)==7,'characteristic-two GF4 evaluation rank seven')
# Exact interpolation chart: seven distinct first coordinates, two arbitrary
# polynomial coordinate functions, reconstruct and check the inverse data.
xs=[-3,-2,-1,0,1,2,4]; coeffs=[[Q(2),Q(-1),Q(0),Q(3),Q(1),Q(0),Q(-2)], [Q(4),Q(3),Q(-2),Q(1),Q(0),Q(2),Q(1)]]
vand=[[Q(x)**i for i in range(7)] for x in xs]
require(det(vand)!=0,'interpolation first-coordinate separation')
# Solve independently by Lagrange basis, returning ascending coefficients.
def pmul(a,b):
    c=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c

def lagrange(values):
    out=[Q(0)]*len(xs)
    for i,x in enumerate(xs):
        p=[Q(1)]; denominator=Q(1)
        for j,y in enumerate(xs):
            if i!=j:p=pmul(p,[-y,1]);denominator*=x-y
        for j,c in enumerate(p):out[j]+=values[i]*c/denominator
    return out
for c in coeffs:
    values=[sum(z*Q(x)**i for i,z in enumerate(c)) for x in xs]
    require(lagrange(values)==c,'monic-interpolation chart inverse')
f=[Q(1)]
for x in xs:f=pmul(f,[-x,1])
require(len(f)==8 and f[-1]==1 and all(sum(c*Q(x)**i for i,c in enumerate(f))==0 for x in xs),'monic polynomial recovery')
quad_pts=[(0,0),(1,0),(2,0),(0,1),(0,2),(1,1)]
quad_exps=[(0,0),(1,0),(0,1),(2,0),(1,1),(0,2)]
quad_det=det([[x**a*y**b for a,b in quad_exps] for x,y in quad_pts])
require(quad_det!=0,'generic seven-point quadratic rank six')
# Adversarial false-alternative controls, each checked against computed data.
boundary_weights,_=border_tangent(staircase(2))
false={
    'extend_opposite_pair_family_below_m3':bool(boundary_weights.get((-1,2),0) and boundary_weights.get((1,-2),0)),
    'replace_actual_tangent_by_untruncated_Hom':sum(Wn.values())==sum(W.values()),
    'negating_cocharacter_removes_opposite_weights':all(-3*w[0]-2*w[1]<0 for w in W),
    'use_smooth_Borel_to_infer_source':all(3*w[0]+2*w[1]<0 for w in W),
    'call_J3_quadratic_Hilbert_function_generic':HF[2]==6,
    'use_non_distinct_scalars_in_small_prime_field':len({(x%2,y%2) for x,y in B})==7,
    'treat_positive_characteristic_Borel_as_strong_stable':in_ideal((1,1),[(2,0),(0,2)]),
    'discard_linear_syzygies_from_Hom':3*len(B)==sum(W.values()),
}
for label,claim in false.items():require(not claim,'reject '+label)
print(json.dumps({'status':'PASS_INDEPENDENT_EXACT_CONTROLS','assertion_count':len(checks),
    'method':'Border commutators and adjacent Macaulay equations, independent of author Taylor-pair implementation',
    'affine_tangent_weights':weight_list(W),'filtered_tangent_weights':weight_list(Wn),
    'border_matrix':control,'filtered_border_matrix':filtered_control,'truncation_matrices':truncations,
    'odd_family':family,'small_plane_certificates':small,'distraction_controls':distraction,
    'GF4_distraction_rank':frank(mat),'quadratic_evaluation_determinant':str(quad_det),
    'negative_controls_rejected':list(false),
    'scope':'Finite exact controls supplement the mathematical audit; no general projective AIM resolution.'},sort_keys=True,indent=2))
