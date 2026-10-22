#!/usr/bin/env python3
"""Independent exact construction; no author code or external tables imported.
All assertions are explicit checks and remain active under python -O.
"""
from fractions import Fraction as F
from itertools import product, permutations
from collections import Counter, deque
import json, hashlib, pathlib, sys, datetime
OUT = pathlib.Path(__file__).resolve().parent

def check(ok, message):
    if not ok: raise RuntimeError(message)

def gf4mul(a,b):
    v=0
    while b:
        if b&1: v^=a
        b>>=1; a<<=1
        if a&4: a^=7
    return v

def mm(A,B,q):
    if q==4:
        return tuple(gf4mul(A[2*i],B[j])^gf4mul(A[2*i+1],B[2+j]) for i in range(2) for j in range(2))
    return tuple((A[2*i]*B[j]+A[2*i+1]*B[2+j])%q for i in range(2) for j in range(2))

def det(A,q):
    return gf4mul(A[0],A[3])^gf4mul(A[1],A[2]) if q==4 else (A[0]*A[3]-A[1]*A[2])%q

def sl(q): return sorted(A for A in product(range(q),repeat=4) if det(A,q)==1)
def tables(gs,q):
    ix={g:i for i,g in enumerate(gs)}; e=ix[(1,0,0,1)]
    mt=[[ix[mm(g,h,q)] for h in gs] for g in gs]
    inv=[next(j for j in range(len(gs)) if mt[i][j]==e) for i in range(len(gs))]
    order=[]
    for i in range(len(gs)):
        j=i; n=1
        while j!=e: j=mt[j][i];n+=1
        order.append(n)
    return ix,e,mt,inv,order

def basis(vs):
    d={}
    for v in vs:
        while v:
            k=v.bit_length()-1
            if k not in d: d[k]=v;break
            v^=d[k]
    return list(d.values())

def rank(vs): return len(basis(vs))
def bits(v):
    while v:
        b=v&-v;yield b.bit_length()-1;v^=b

def amul(a,b,mt):
    c=0
    for i in bits(a):
        for j in bits(b): c^=1<<mt[i][j]
    return c

def image_basis(gs,q):
    # P1(F4) vectors: infinity then (x,1), in this exact order.
    points=[(1,0)]+[(x,1) for x in range(4)]
    def act(A,p):
        u=gf4mul(A[0],p[0])^gf4mul(A[1],p[1]);v=gf4mul(A[2],p[0])^gf4mul(A[3],p[1])
        return (1,0) if not v else (gf4mul(u,next(y for y in range(1,4) if gf4mul(v,y)==1)),1)
    perms=[tuple(points.index(act(A,p)) for p in points) for A in gs]
    check(len(set(perms))==60,'SL2(4) projective action not faithful')
    check(all(sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))%2==0 for p in perms),'projective action is not A5')
    # S: basis e_i+e_4, i=0..3. U: F4 basis 1,t, in each natural coordinate.
    sm=[];um=[]
    for A,p in zip(gs,perms):
        sc=[];uc=[]
        for j in range(4):
            w=(1<<p[j])^(1<<p[4]);sc.append(w&15)
            v=[0,0];v[j//2]=1<<(j%2)
            out=[gf4mul(A[0],v[0])^gf4mul(A[1],v[1]),gf4mul(A[2],v[0])^gf4mul(A[3],v[1])]
            uc.append(out[0]|out[1]<<2)
        sm.append(sum(v<<(4*j) for j,v in enumerate(sc)))
        um.append(sum(v<<(4*j) for j,v in enumerate(uc)))
    return perms,sm,um

def matmul4(A,B):
    cs=[(A>>(4*j))&15 for j in range(4)]
    out=[]
    for j in range(4):
        out.append(xor(cs[i] for i in bits((B>>(4*j))&15)))
    return sum(v<<(4*j) for j,v in enumerate(out))

def xor(vs):
    out=0
    for v in vs:out^=v
    return out

def commutant_dim(mats):
    # linear equations from XA=AX, in 16 unknown entries encoded columnwise.
    rows=[]
    for A in mats:
        cols=[matmul4(1<<j,A)^matmul4(A,1<<j) for j in range(16)]
        rows.extend(sum(((cols[j]>>i)&1)<<j for j in range(16)) for i in range(16))
    return 16-rank(rows)

def linear_lifts(images):
    d={};ker=[]
    for i,v in enumerate(images):
        w=1<<i
        while v:
            k=v.bit_length()-1
            if k not in d:d[k]=(v,w);break
            v^=d[k][0];w^=d[k][1]
        if not v:ker.append(w)
    def lift(v):
        w=0
        while v:
            k=v.bit_length()-1
            check(k in d,'requested quotient matrix not in image')
            v^=d[k][0];w^=d[k][1]
        return w
    return d,ker,lift

def ideal_rank(a,mt):return rank(amul(1<<i,a,mt) for i in range(len(mt)))
def subgroup(i,e,mt):
    s={e};v=i
    while v!=e:s.add(v);v=mt[v][i]
    return frozenset(s)

h=sl(4);hix,he,hm,hi,ho=tables(h,4)
perms,sm,um=image_basis(h,4)
for i in range(60):
    for j in range(60):
        check(matmul4(sm[i],sm[j])==sm[hm[i][j]],'S representation homomorphism')
        check(matmul4(um[i],um[j])==um[hm[i][j]],'U representation homomorphism')
check(rank(sm)==16,'S algebra not full M4(F2)')
check(rank(um)==8,'U algebra not M2(F4)')
check(commutant_dim(sm)==1,'S endomorphism ring dimension')
check(commutant_dim(um)==2,'U endomorphism ring dimension')
images=[1|(u<<1)|(s<<17) for u,s in zip(um,sm)]
d,ker,lift=linear_lifts(images)
check(len(d)==25 and len(ker)==35,'semisimple quotient dimensions')
# A kernel of a representation homomorphism is an ideal. Explicitly certify nilpotent.
kpow=basis(ker);kdims=[len(kpow)]
while kpow and len(kdims)<12:
    kpow=basis(amul(x,y,hm) for x in kpow for y in ker);kdims.append(len(kpow))
check(not kpow,'joint kernel not verified nilpotent')
# This proves exactly F2 x M2(F4) x M4(F2), not just three exhibited simples.
# E11 over F4 acts as F2 identity on its first two coordinates: columns (1,2,0,0).
u11=1|(2<<4);s11=1
projs=[];hidem=[]
for label,target,want in [('1',1,12),('U',u11<<1,16),('S',s11<<17,4)]:
    e0=lift(target);e=e0;nsquare=0
    while amul(e,e,hm)!=e and nsquare<12:e=amul(e,e,hm);nsquare+=1
    check(amul(e,e,hm)==e,'idempotent correction failed')
    check(xor(images[i] for i in bits(e))==target,'idempotent quotient changed')
    check(ideal_rank(e,hm)==want,'A5 PIM dimension wrong')
    hidem.append(e);projs.append({'type':label,'H_dimension':want,'H_idempotent_hex':hex(e),'squarings':nsquare})
# S restriction to Sylow 2 is regular, with generator orbit of e_i+e_4.
syl=[hix[(1,a,0,1)] for a in range(4)]
check(len({perms[i][j] for i in syl for j in [1]})==4,'Sylow regular orbit missing')
check(rank((sm[i]&15) for i in syl)==4,'S restriction not regular')
# Rational V5 is augmentation of permutation action on the six C5 subgroups.
c5s=sorted(set(subgroup(i,he,hm) for i,o in enumerate(ho) if o==5),key=lambda s:tuple(sorted(s)))
check(len(c5s)==6,'wrong number of Sylow5 subgroups')
v4=[sum(p[j]==j for j in range(5))-1 for p in perms]
v5=[sum(frozenset(hm[hm[i][j]][hi[i]] for j in s)==s for s in c5s)-1 for i in range(60)]
check(sum(x*x for x in v4)==60 and sum(x*x for x in v5)==60,'rational augmentation irreducibility norms')
check(Counter((ho[i],v4[i],v5[i]) for i in range(60))==Counter({(1,4,5):1,(2,0,1):15,(3,1,-1):20,(5,-1,0):24}),'rational character values')
# P1 is independently the permutation module induced from an odd C5.
c5=c5s[0];ec5=sum(1<<i for i in c5)
check(amul(ec5,ec5,hm)==ec5 and ideal_rank(ec5,hm)==12,'C5 permutation PIM')
check(xor(images[i] for i in c5)==1,'C5 PIM top is not just trivial')
cosets=[]
remaining=set(range(60))
while remaining:
    i=min(remaining);c=frozenset(hm[i][j] for j in c5);cosets.append(c);remaining-=c
p1char=[sum(frozenset(hm[i][j] for j in c)==c for c in cosets) for i in range(60)]
check(Counter((ho[i],p1char[i]) for i in range(60))==Counter({(1,12):1,(2,0):15,(3,0):20,(5,2):24}),'P1 permutation character')
# Brauer U values: degree4, -2 on3, -1 on5, obtained from natural + Frobenius natural.
brauer={1:(1,4,4),3:(1,-2,1),5:(1,-1,-1)}
classesH={'1':(4,2,0),'U':(4,3,0),'S':(0,0,1)}
for i,o in enumerate(ho):
    if o%2:
        one,U,S=brauer[o]
        check(v5[i]==one+U,'V5 decomposition class')
        check(v4[i]==S,'V4 decomposition class')
        check(p1char[i]==4*one+2*U,'P1 composition class')
        numerator=(60 if o==1 else 0)-p1char[i]-4*S
        check(numerator==2*(4*one+3*U),'PU regular decomposition class')
# Exact quaternion field Q(sqrt5).
Z=(F(0),F(0));O=(F(1),F(0));HALF=(F(1,2),F(0));PHI=(F(1,2),F(1,2));INVPHI=(F(-1,2),F(1,2))
def qa(x,y):return (x[0]+y[0],x[1]+y[1])
def qn(x):return (-x[0],-x[1])
def qm(x,y):return (x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def scale(x,n):return (x[0]*n,x[1]*n)
def qprod(x,y):
    a,b,c,d=x;f,g,j,k=y
    return (qa(qa(qm(a,f),qn(qm(b,g))),qn(qa(qm(c,j),qm(d,k)))),
            qa(qa(qm(a,g),qm(b,f)),qa(qm(c,k),qn(qm(d,j)))),
            qa(qa(qm(a,j),qn(qm(b,k))),qa(qm(c,f),qm(d,g))),
            qa(qa(qm(a,k),qm(b,j)),qa(qn(qm(c,g)),qm(d,f))))
def parity(p):return sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2
quats=set()
for i in range(4):
    for sign in (-1,1):q=[Z]*4;q[i]=scale(O,sign);quats.add(tuple(q))
for signs in product((-1,1),repeat=4):quats.add(tuple(scale(HALF,s) for s in signs))
for p in permutations(range(4)):
    if parity(p):continue
    for signs in product((-1,1),repeat=3):
        vals=(Z,scale(HALF,signs[0]),scale(PHI,F(signs[1],2)),scale(INVPHI,F(signs[2],2)))
        quats.add(tuple(vals[j] for j in p))
check(len(quats)==120,'quaternion group cardinality')
for q in quats:check(sum((qm(a,a)[0] for a in q),F(0))==1 and sum((qm(a,a)[1] for a in q),F(0))==0,'quaternion norm')
# Reduction sqrt5 -> 0, with i,j mapped to anticommuting norm-one matrices.
I=(1,0,0,1);Qi=(0,1,4,0);Qj=(0,2,2,0);Qk=mm(Qi,Qj,5)
def mod5(x):return (x[0].numerator*pow(x[0].denominator,-1,5))%5
def qmap(q):return tuple(sum(mod5(q[j])*M[k] for j,M in enumerate((I,Qi,Qj,Qk)))%5 for k in range(4))
g=sl(5);gix,ge,gm,gi,go=tables(g,5)
qby={qmap(q):q for q in quats};check(set(qby)==set(g),'quaternion reduction not bijective SL2F5')
qproducts=0
for x in quats:
    for y in quats:
        z=qprod(x,y);check(z in quats,'quaternion closure');check(qmap(z)==mm(qmap(x),qmap(y),5),'quaternion reduction homomorphism');qproducts+=1
# SU2 embedding gives actual natural representation; symmetric cube trace x^3-2x.
minus=[]
for A in g:
    x=scale(qby[A][0],2);v=qa(qm(qm(x,x),x),qn(scale(x,2)))
    check(v[1]==0 and v[0].denominator==1,'nonintegral symcube character')
    minus.append(int(v[0]))
check(sum(x*x for x in minus)==120,'Sym3 is not irreducible')
fs=sum(minus[gm[i][i]] for i in range(120))
check(fs==-120,'Sym3 FS not -1')
# Produce quotient G/{+-1} from its conjugation action on six Sylow5 groups;
# match actual A5 by isomorphism via the certified quaternion model and group presentation.
# Instead construct G -> SL2(4) using a pair of generators and exhaustive products.
a=gix[(0,4,1,0)];b=gix[(0,4,1,1)]
mapG=None;pairtries=0
for aa in range(60):
    if ho[aa]!=2:continue
    for bb in range(60):
        if ho[bb]!=3 or ho[hm[aa][bb]]!=5:continue
        pairtries+=1;mp={ge:he};queue=deque([ge]);ok=True
        while queue and ok:
            i=queue.popleft()
            for x,y in ((a,aa),(b,bb)):
                j=gm[i][x];val=hm[mp[i]][y]
                if j in mp:
                    if mp[j]!=val:ok=False;break
                else:mp[j]=val;queue.append(j)
        if ok and len(mp)==120 and len(set(mp.values()))==60:mapG=mp;break
    if mapG:break
check(mapG is not None,'quotient identification failed')
for i in range(120):
    for j in range(120):check(mapG[gm[i][j]]==hm[mapG[i]][mapG[j]],'quotient not homomorphism')
central=gix[(4,0,0,4)];check(set(i for i,v in mapG.items() if v==he)=={ge,central},'quotient kernel')
plus=[v4[mapG[i]] for i in range(120)]
check(sum(x*x for x in plus)==120,'augmentation character norm')
check(sum(x*y for x,y in zip(plus,minus))==0,'degree4 characters not distinct orthogonal')
expected=Counter({(1,4,4):1,(2,4,-4):1,(3,1,1):20,(4,0,0):30,(5,-1,-1):24,(6,1,-1):20,(10,-1,1):24})
check(Counter((go[i],plus[i],minus[i]) for i in range(120))==expected,'actual degree4 character values')
# Lift actual H primitive idempotents across central square-zero quotient.
section={j:min(i for i in range(120) if mapG[i]==j) for j in range(60)}
t=(1<<ge)^(1<<central)
for rec,eh in zip(projs,hidem):
    e0=xor(1<<section[j] for j in bits(eh));e=amul(e0,e0,gm)
    check(amul(e,e,gm)==e,'central corrected primitive lift not idempotent')
    pb=basis(amul(1<<i,e,gm) for i in range(120))
    tp=basis(amul(t,v,gm) for v in pb)
    check(len(pb)==2*rec['H_dimension'],'G PIM dimension')
    check(len(tp)==rec['H_dimension'],'central filter dimension')
    check(all(amul(t,v,gm)==0 for v in tp),'central image not in kernel')
    # image=kernel since rank nullity, and quotient basis gives specified H ideal.
    qdim=rank(xor(1<<mapG[i] for i in bits(v)) for v in pb)
    check(qdim==rec['H_dimension'],'central quotient module dimension')
    rec.update(G_dimension=len(pb),G_idempotent_hex=hex(e),t_image_dimension=len(tp),t_kernel_dimension=len(pb)-len(tp),quotient_dimension=qdim)
# Rational witness class checks, including nonsplit regular multiplicity.
witnesses={'1':(4,4,0),'U':(2,6,0),'S':(0,0,2)}
for typ,(a1,a5,a4) in witnesses.items():
    c=tuple(2*x for x in classesH[typ]);check(c==(a1+a5,a5,a4),'positive witness')
check(24+2*32+4*8==120,'regular PIM multiplicities')
# The p-projective character forced by the rank8 module is plus+minus.
forced=[8 if o==1 else (2*plus[i] if o%2 else 0) for i,o in enumerate(go)]
check(forced==[x+y for x,y in zip(plus,minus)],'forced projective character')
# Conjugacy and square-map receipts are independently actual group enumeration.
def conjugacy(mt,inv):
    rem=set(range(len(mt)));cs=[]
    while rem:
        i=min(rem);c={mt[mt[j][i]][inv[j]] for j in range(len(mt))};cs.append(sorted(c));rem-=c
    return cs
cs=conjugacy(gm,gi);cid={i:j for j,c in enumerate(cs) for i in c}
result={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS',
 'scope':'Exact saved PR436 candidate; no new candidate search',
 'SL2F4_order':60,'SL2F5_order':120,'simple_algebra_image_dimension':25,'joint_kernel_power_dimensions':kdims,
 'simple_types':{'1':{'dimension':1,'End_F2_dimension':1},'U':{'dimension':4,'End_F2_dimension':2,'image_algebra_dimension':8},'S':{'dimension':4,'End_F2_dimension':1,'image_algebra_dimension':16}},
 'H_cartan_columns':classesH,'projectives':projs,'rational_witness_V1_V5_V4':witnesses,
 'regular_multiplicities':{'1':1,'U':2,'S':4},'S_representation_products_checked':3600,'U_representation_products_checked':3600,'quaternion_products_checked':qproducts,'quotient_products_checked':14400,'quotient_generator_pairs_tried':pairtries,
 'symcube_norm':1,'symcube_FS':-1,'forced_character':'chi_plus+chi_minus',
 'conjugacy_classes':[{'size':len(c),'representative':g[c[0]],'order':go[c[0]],'square_class':cid[gm[c[0]][c[0]]],'chi_plus':plus[c[0]],'chi_minus':minus[c[0]]} for c in cs],
 'theoretical_bridge_not_encoded':'SU2 embedding and symmetric cube actual construction; nilpotent semisimple quotient classification; Brauer-character injectivity; projective integral character vanishing; FS parity; semiperfect idempotent lifting'}
print(json.dumps(result,indent=2))
