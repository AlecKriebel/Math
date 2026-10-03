#!/usr/bin/env python3
"""New adversarial controls after candidate read, before family comparison.

Uses only the independently sealed helper implementation, never author imports.
The finite examples test exact boundary hypotheses; the general proof checks are
recorded in POST_CANDIDATE_RECONSTRUCTION.md.
"""
import contextlib,io,json,itertools,math
from fractions import Fraction as Q
with contextlib.redirect_stdout(io.StringIO()):
    import independent_controls as C
N=0
def ck(x):
    global N
    assert x;N+=1
def germ(f,x):
    for (a,b),(c,d) in zip(f,f[1:]):
        if a<=x<c:return (d-b)/(c-a)
    raise ValueError(x)
def components(f):
    cuts={x for x,y in f}
    for (a,b),(c,d) in zip(f,f[1:]):
        da,dc=b-a,d-c
        if da*dc<0:cuts.add(a+(c-a)*(-da)/(dc-da))
    cuts=sorted(cuts);out=[]
    for a,b in zip(cuts,cuts[1:]):
        mid=(a+b)/2
        if C.val(f,mid)!=mid:
            if out and out[-1][1]==a and C.val(f,a)!=a:out[-1]=(out[-1][0],b)
            else:out.append((a,b))
    return out

# A common interior endpoint 1/3, despite all breakpoints and slopes being dyadic.
f=C.canon([(0,0),(Q(1,4),Q(1,8)),(Q(5,16),Q(1,4)),
           (Q(3,8),Q(1,2)),(Q(1,2),Q(5,8)),(Q(3,4),Q(3,4)),(1,1)])
b=C.rescale(C.t,Q(7,8),Q(15,16));a=Q(1,3)
ck(C.isf(f) and C.isf(b));ck(C.val(f,a)==a and germ(f,a)==4)
ck(components(f)==[(Q(0),a),(a,Q(3,4))]);ck(C.plcomm(f,b)==C.ID)
words=[]
for i,j in itertools.product(range(-4,5),range(-2,3)):
    w=C.compose(C.power(f,i),C.power(b,j));ck(C.isf(w));ck(C.val(w,a)==a)
    ck(germ(w,a)==Q(4)**i);words.append((i,j,w))
for i,j,w in words[::4]:
    for k,l,v in words[::5]:
        ck(germ(C.compose(w,v),a)==germ(w,a)*germ(v,a))
        ck(C.plcomm(w,v)==C.ID)
normal={'group':'<f> times outside-support maps','ordinary_fg_normal_N':'<f>',
        'non_dyadic_common_fixed_endpoint':'1/3','N_detecting_integer_character':'log_2 right slope = 2*i',
        'support_components':[['0','1/3'],['1/3','3/4']]}

# Dropping normality really breaks the ambient germ construction.
local=C.a;x=Q(1,2)
ck(C.val(C.t,x)!=x)
ck(C.compose(C.compose(C.iv(C.t),local),C.t)!=local)
ck(germ(C.compose(local,C.t),x)!=germ(local,x)*germ(C.t,x))
normality_mutant={'removed_hypothesis':'normality/common fixed endpoint',
                  'character_multiplicativity_fails':True,'normal_closure_generation':'finite normal != ordinary finite'}

# An independent exact rank calculation for increasingly many normal generators.
def rank(rows):
    rows=[[Q(x) for x in row] for row in rows];r=0
    for j in range(len(rows[0]) if rows else 0):
        pivot=next((i for i in range(r,len(rows)) if rows[i][j]),None)
        if pivot is None:continue
        rows[r],rows[pivot]=rows[pivot],rows[r];v=rows[r][j];rows[r]=[x/v for x in rows[r]]
        for i in range(len(rows)):
            if i!=r and rows[i][j]:
                v=rows[i][j];rows[i]=[x-v*y for x,y in zip(rows[i],rows[r])]
        r+=1
    return r
ranks=[]
for window in range(1,16):
    polys=[C.shift(C.u,i) for i in range(-window,window+1)]
    rows=[[p.get(i,0) for i in range(-window,window+2)] for p in polys]
    rk=rank(rows);ck(rk==2*window+1);ranks.append({'window':window,'normal_shift_rank':rk})

# Three independent dyadic lamps in one fundamental interval; all translates
# are exact PL elements and detect separate exponent coordinates.
intervals=[(Q(1,2),Q(9,16)),(Q(9,16),Q(5,8)),(Q(5,8),Q(11,16))]
lamps={}
for j,(a0,b0) in enumerate(intervals):
    lamp=C.rescale(C.t,a0,b0)
    for i in range(-3,4):
        w=C.compose(C.compose(C.power(C.t,-i),lamp),C.power(C.t,i));ck(C.isf(w));ck(w!=C.ID)
        lamps[j,i]=w
for x,y in itertools.combinations(lamps.values(),2):ck(C.plcomm(x,y)==C.ID)
for exps in itertools.product(range(-2,3),repeat=3):
    w=C.ID
    for j,k in enumerate(exps):w=C.compose(w,C.power(lamps[j,0],k))
    ck((w==C.ID)==(exps==(0,0,0)))
    for j,(a0,b0) in enumerate(intervals):
        mid=(a0+b0)/2;ck((C.val(w,mid)!=mid)==(exps[j]!=0))
tors=[]
mods=[2,3,5]
for residue in itertools.product(*[range(m) for m in mods]):
    order=math.lcm(*[m//math.gcd(m,x) for m,x in zip(mods,residue)])
    ck(all(order*x%m==0 for m,x in zip(mods,residue)))
    for k in range(1,order):ck(any(k*x%m for m,x in zip(mods,residue)))
    tors.append({'residue':residue,'order':order})

# Signed balanced-power controls at a non-dyadic interior germ and in P_m.
for p,q in itertools.product([i for i in range(-6,7) if i],repeat=2):
    ck((germ(C.power(f,p),Q(1,3))==germ(C.power(f,q),Q(1,3)))==(p==q))
balanced=[]
for m in [1,2,6,11]:
    pts=list(itertools.product(range(-1,2),repeat=3))
    for u in pts:
        if u==(0,0,0):continue
        for v in pts[::4]:
            for p,q in itertools.product([-3,-1,1,2,4],repeat=2):
                c=C.hm(C.hm(C.hi(v,m),C.hp(u,p,m),m),v,m)
                if c==C.hp(u,q,m):ck(p==q)
                if p!=q:ck(c!=C.hp(u,q,m))
    balanced.append({'m':m,'unequal_signed_conjugate_powers_excluded':True})

# An outer-twisted diagonal in three factors has one independent simple block.
odd=(1,0,2,3,4);alpha=[C.idx[C.pc(C.pc(odd,s),C.pi(odd))] for s in C.A]
gens=[C.idx[(1,2,0,3,4)],C.idx[(1,2,3,4,0)]]
good=0
for a0,b0,c0 in itertools.product(range(60),repeat=3):
    norm=all(C.mt[C.mt[b0][alpha[s]]][C.inv[b0]]==alpha[C.mt[C.mt[a0][s]][C.inv[a0]]] for s in gens)
    ck(norm==(b0==alpha[a0]))
    if norm:good+=1
ck(good==3600)
print(json.dumps({'assertions':N,'sealed_helper_original_controls':C.checks,
 'ambient_normal_germ':normal,'normality_negative_mutant':normality_mutant,
 'normal_shift_independence':ranks,'multilamp':{'independent_lamps':3,'translated_lamps':21,
 'torsion_moduli':mods,'all_residue_orders':tors},'signed_balanced_power_models':balanced,
 'three_factor_outer_twisted_diagonal_normalizer_size':good,
 'scope':'new exact controls; no author imports, no finite-presentation recognition, no full-target solution'},indent=2,sort_keys=True))
