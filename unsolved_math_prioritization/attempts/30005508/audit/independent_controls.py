#!/usr/bin/env python3
"""Independent exact audit controls. Standard library; no downloaded data or imports
from the author's checker. This certifies finite examples, not a universal theorem.
Run: python3 independent_controls.py > independent_results.json
"""
from itertools import product
from fractions import Fraction
import json

# F_4 = F_2[w]/(w^2+w+1), with elements 0,1,w,w+1 encoded 0,1,2,3.
def fm(a,b):
    c=0
    for _ in range(2):
        if b&1:c^=a
        b>>=1;a<<=1
        if a&4:a^=7
    return c

def rank(rows):
    piv={}
    for row in rows:
        r=list(row)
        for j in sorted(piv):
            if r[j]:
                c=r[j];r=[x^fm(c,y) for x,y in zip(r,piv[j])]
        if any(r):
            j=next(j for j,x in enumerate(r) if x)
            c={1:1,2:3,3:2}[r[j]]
            piv[j]=[fm(c,x) for x in r]
    return len(piv)

def mm(a,b):
    n=len(a)
    return tuple(tuple(xor(fm(a[i][k],b[k][j]) for k in range(n)) for j in range(n)) for i in range(n))
def xor(xs):
    r=0
    for x in xs:r^=x
    return r

def flat(m):return tuple(x for row in m for x in row)
def eye(n):return tuple(tuple(int(i==j) for j in range(n)) for i in range(n))
W=(1,2,3)
Q=list(product(range(3),repeat=3))
def qm(q,r):
    a,b,c=q;u,v,w=r
    return ((a+u)%3,(b+v)%3,(c+w+a*v)%3)
def alpha(q):a,b,c=q;return ((-a)%3,b,(-c)%3)
H=list(product(Q,range(2)))
def hm(h,k):
    q,t=h;r,s=k
    return (qm(q,alpha(r) if t else r),t^s)
assert all(hm(hm(a,b),c)==hm(a,hm(b,c)) for a in H for b in H for c in H)
V=list(product(range(2),repeat=4))
def va(v,w):return tuple(a^b for a,b in zip(v,w))
def av(v):x,y=v;return (y,x^y)
def act(h,v):
    (a,b,c),t=h
    u=v[:2];w=v[2:]
    if t:u=u[::-1]
    for _ in range(a):u=av(u)
    for _ in range(b):w=av(w)
    return u+w
assert all(act(hm(h,k),v)==act(h,act(k,v)) for h in H for k in H for v in V)
# G=V semidirect H, independently constructed from the verified small action.
G=list(product(V,H));ix={g:i for i,g in enumerate(G)};n=len(G)
v0=(0,0,0,0);q0=(0,0,0);h0=(q0,0);one=ix[(v0,h0)]
def gm(g,k):v,h=g;w,j=k;return (va(v,act(h,w)),hm(h,j))
M=[[ix[gm(g,k)] for k in G] for g in G]
assert all(M[one][i]==i==M[i][one] for i in range(n))
inv=[next(j for j in range(n) if M[i][j]==one==M[j][i]) for i in range(n)]
def cj(y,h):return M[M[inv[h]][y]][h]

def rho(q):
    a,b,c=q;m=[[0]*3 for _ in range(3)]
    for j in range(3):m[(j+b)%3][j]=W[(c+a*j)%3]
    return tuple(map(tuple,m))
R={q:rho(q) for q in Q}
assert all(mm(R[q],R[r])==R[qm(q,r)] for q in Q for r in Q)
assert rank(map(flat,R.values()))==9

def sigma(h):
    q,t=h;m=[[0]*6 for _ in range(6)]
    for source in range(2):
        target=source^t
        r=R[alpha(q) if target else q]
        for i in range(3):
            for j in range(3):m[3*target+i][3*source+j]=r[i][j]
    return tuple(map(tuple,m))
S={h:sigma(h) for h in H}
assert all(mm(S[h],S[k])==S[hm(h,k)] for h in H for k in H)
assert rank(map(flat,S.values()))==36
z=ix[(v0,((0,0,1),0))];zz=M[z][z]
support={z,zz}
assert {cj(z,g) for g in range(n)}==support
# Central idempotent e=z+z^2 over characteristic 2, verified as group-algebra support.
square=set()
for a in support:
    for b in support:
        c=M[a][b]
        if c in square:square.remove(c)
        else:square.add(c)
assert square==support
assert all({M[g][s] for s in support}=={M[s][g] for s in support} for g in range(n))
# Rank of e on kH equals 36. Together with span(S(H))=M_6(F4), e*kH=M_6(F4).
hi={h:i for i,h in enumerate(H)};hz=((0,0,1),0);hzz=hm(hz,hz)
columns=[]
for h in H:
    col=[0]*len(H)
    col[hi[hm(hz,h)]]^=1;col[hi[hm(hzz,h)]]^=1
    columns.append(col)
assert rank(columns)==36
sz=S[hz];szz=S[hzz]
assert tuple(tuple(sz[i][j]^szz[i][j] for j in range(6)) for i in range(6))==eye(6)
D={ix[(v,h0)] for v in V};E={ix[(v,(q0,t))] for v in V for t in range(2)}
Cz={g for g in range(n) if M[g][z]==M[z][g]}
CD={g for g in range(n) if all(M[g][d]==M[d][g] for d in D)}
assert len(D)==16 and len(E)==32 and len(Cz)==432 and len(CD)==48
assert CD=={M[d][u] for d in D for u in (one,z,zz)}
assert all({cj(d,g) for d in D}==D for g in range(n))
# e_theta=1+w^2*z+w*z^2 in k C_G(D); conjugation stabilizer is computed exactly.
f={one:1,z:3,zz:2}
f_square={}
for a,c in f.items():
    for b,dcoef in f.items():
        g=M[a][b];f_square[g]=f_square.get(g,0)^fm(c,dcoef)
assert {g:c for g,c in f_square.items() if c}==f
assert all({cj(a,g):c for a,c in f.items()}==f for g in CD)
Nf={g for g in range(n) if {cj(a,g):c for a,c in f.items()}==f}
assert Nf==Cz and CD<=Nf and len(Nf)//len(CD)==9
# Ordinary rho values in Z[zeta_3] represented by integer pairs, zeta^2=-1-zeta.
qembed={ix[(v0,(q,0))]:q for q in Q}
rvalues={(0,0,0):(3,0),(0,0,1):(0,3),(0,0,2):(-3,-3)}
phi=[]
for g in range(n):
    a=b=0
    for h in range(n):
        q=qembed.get(cj(g,h))
        r,s=rvalues.get(q,(0,0));a+=r;b+=s
    assert a%27==b%27==0
    phi.append((a//27,b//27))
assert phi[one]==(96,0) and phi[z]==phi[zz]==(-48,0)
assert all(v==(0,0) for i,v in enumerate(phi) if i not in {one,z,zz})
roots={g for g in range(n) if M[g][g]==one};remaining=set(roots);rows=[]
while remaining:
    y=min(remaining);orb={cj(y,g) for g in range(n)};remaining-=orb
    C={g for g in range(n) if M[g][y]==M[y][g]}
    lhs=tuple(Fraction(sum(phi[g][i] for g in C),len(C)) for i in range(2))
    rhs=len(orb&(E-D));assert lhs==(rhs,0)
    rows.append(dict(class_size=len(orb),centralizer=len(C),multiplicity=rhs,coset_intersection=rhs))
assert len(rows)==6 and len(roots)==88

# Small C3 semidirect E controls. Every index-two subgroup is tested, for every
# x in D and every y with y^2=x. Includes nonsplit quaternion and cyclic pairs.
def cyc(n):return list(range(n)),lambda a,b:(a+b)%n,0

def dihedral(n):
    return list(product(range(n),range(2))),lambda a,b:((a[0]+(-1 if a[1] else 1)*b[0])%n,a[1]^b[1]),(0,0)

def quat8():
    # i^4=1, j^2=i^2, j*i=i^-1*j.
    return list(product(range(4),range(2))),lambda a,b:((a[0]+(-1 if a[1] else 1)*b[0]+2*a[1]*b[1])%4,a[1]^b[1]),(0,0)

def index2_subgroups(el,op,e):
    # A subgroup of index two is the kernel of a nonzero homomorphism to C2.
    from itertools import combinations
    others=[g for g in el if g!=e];answer=[]
    for xs in combinations(others,len(el)//2-1):
        d=set(xs)|{e}
        if all(op(a,b) in d for a in d for b in d):answer.append(d)
    return answer

family=[];quot=[]
for name,data in [('C2',cyc(2)),('C4',cyc(4)),('C8',cyc(8)),('D8',dihedral(4)),('Q8',quat8())]:
    es,em,ee=data
    for d in index2_subgroups(es,em,ee):
        gs=list(product(range(3),es));gi={g:i for i,g in enumerate(gs)}
        def op(g,h):return ((g[0]+(1 if g[1] in d else -1)*h[0])%3,em(g[1],h[1]))
        tab=[[gi[op(g,h)] for h in gs] for g in gs];e=gi[(0,ee)];nn=len(gs)
        iv=[next(j for j in range(nn) if tab[i][j]==e==tab[j][i]) for i in range(nn)]
        def cc(y,h):return tab[tab[iv[h]][y]][h]
        dd={gi[(0,x)] for x in d};ext={gi[(0,x)] for x in es}
        tests=0;nonreal=0
        for x in sorted(dd):
            ch={g for g in range(nn) if tab[x][g]==tab[g][x]};q=ch&ext;p=ch&dd
            real=len(q)>len(p)
            if not real:nonreal+=1
            ph={}
            for g in ch:
                a,h=gs[g]
                if h!=ee:ph[g]=(0,0)
                elif real:ph[g]=(len(q) if a==0 else -len(p),0)
                else:
                    r,s=((1,0),(0,1),(-1,-1))[a];ph[g]=(len(p)*r,len(p)*s)
            for y in range(nn):
                if tab[y][y]!=x:continue
                cy={g for g in range(nn) if tab[y][g]==tab[g][y]};assert cy<=ch
                orb={cc(y,h) for h in ch};rhs=len(orb&(ext-dd))
                lhs=tuple(Fraction(sum(ph[g][i] for g in cy),len(cy)) for i in range(2))
                assert lhs==(rhs,0);tests+=1
                # Genuine real nonprincipal-block central-quotient controls, not bare 2-groups.
                if x!=e and real:
                    zs={e};v=x
                    while v not in zs:zs.add(v);v=tab[v][x]
                    cos={g:frozenset(tab[g][z] for z in zs) for g in ch}
                    ky={g for g in ch if cc(y,g) in cos[y]};t=len(ky)//len(cy)
                    assert t in (1,2)
                    barorb={cos[g] for g in orb}
                    assert all(sum(cos[g]==c for g in orb)==t for c in barorb)
                    barrhs=len(barorb & {cos[g] for g in (q-p)})
                    assert rhs==t*barrhs
                    # PIM of quotient is induced from the surviving C3, using group orders.
                    barC={cos[g] for g in ky};barQ={cos[g] for g in q};barP={cos[g] for g in p}
                    barvals={}
                    for a in range(3):
                        c=cos[gi[(a,ee)]];barvals[c]=len(barQ) if a==0 else -len(barP)
                    barlhs=Fraction(sum(barvals.get(c,0) for c in barC),len(barC))
                    assert lhs[0]==t*barlhs and barlhs==barrhs
                    # Independent Brauer-character test of the Grothendieck identity.
                    for g in ch:
                        power=e;order=0
                        while True:
                            power=tab[power][g];order+=1
                            if power==e:break
                        if order%2==0:continue
                        fixed=sum(cc(w,g)==w for w in orb)
                        barfixed=sum(cos[cc(next(iter(c)),g)]==c for c in barorb)
                        assert fixed==t*barfixed
                    if rhs:
                        quot.append(dict(group=name,order=nn,central_order=len(zs),t=t,lhs=int(lhs[0]),quotient_lhs=int(barlhs),rhs=rhs,quotient_rhs=barrhs))
        family.append(dict(group=name,defect_elements=sorted(d),defect_order=len(d),subsections=len(dd),nonreal_local_blocks=nonreal,root_tests=tests))
assert {r['t'] for r in quot}=={1,2}
from collections import Counter
quot_counts=Counter(tuple(sorted(r.items())) for r in quot)
quot_summary=[dict(dict(k),instances=v) for k,v in sorted(quot_counts.items())]
output={
    'status':'PASS_SCOPED_PARTIAL',
    'scope':'Finite controls and independent block certificates; not a general-conjecture proof',
    'group_order':n,'group_action_verified':True,
    'rho_degree':3,'rho_matrix_span_dimension':9,
    'simple_degree':6,'simple_matrix_span_dimension':36,
    'quotient_block_algebra_dimension':36,
    'block_idempotent_central_and_idempotent':True,
    'defect_order':len(D),'extended_defect_order':len(E),
    'defect_class_centralizer_order':len(Cz),'defect_class_extended_centralizer_order':n,
    'defect_group_centralizer_order':len(CD),'brauer_block_stabilizer_order':len(Nf),'inertial_quotient_order':9,
    'projective_character_recomputed_by_induction':True,'projective_degree':96,
    'involution_count_including_identity':len(roots),'involution_orbits':sorted(rows,key=lambda r:(r['multiplicity'],r['class_size'])),
    'all_pair_model_controls':family,'positive_actual_block_quotient_controls':quot_summary,'positive_actual_block_quotient_test_count':len(quot),
    'all_assertions_passed':True}
print(json.dumps(output,indent=2))
