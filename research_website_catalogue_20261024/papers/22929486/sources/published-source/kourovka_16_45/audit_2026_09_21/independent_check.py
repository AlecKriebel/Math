#!/usr/bin/env python3
"""Independent exact audit written from proof.tex, without consulting bundle code.
Standard library only. All certificates are freshly reconstructed.
"""
import datetime, itertools, json, pathlib, time
from collections import Counter, deque

START = time.monotonic()
HERE = pathlib.Path(__file__).resolve().parent

def mm(a,b,p):
    return ((a[0]*b[0]+a[1]*b[2])%p,(a[0]*b[1]+a[1]*b[3])%p,
            (a[2]*b[0]+a[3]*b[2])%p,(a[2]*b[1]+a[3]*b[3])%p)
I=(1,0,0,1)
def power(a,n,p):
    x=I
    for _ in range(n): x=mm(x,a,p)
    return x

def closure_matrices(gens,p):
    seen={I}; todo=[I]
    for x in todo:
        for g in gens:
            y=mm(x,g,p)
            if y not in seen: seen.add(y); todo.append(y)
    return sorted(seen)

def construct(p,A,B):
    mats=closure_matrices([A,B],p); ix={m:i for i,m in enumerate(mats)}
    tab=[[ix[mm(a,b,p)] for b in mats] for a in mats]
    one=ix[I]
    def gen(gs):
        seen={one}; todo=[one]
        for x in todo:
            for g in gs:
                y=tab[x][g]
                if y not in seen: seen.add(y); todo.append(y)
        return frozenset(seen)
    return mats,ix,tab,one,gen

def order(x,tab,one):
    y=x; n=1
    while y!=one: y=tab[y][x]; n+=1
    return n

def bitset(s): return sum(1<<x for x in s)

def affine_closure(gs,p,mats,tab,one):
    identity=(0,0,one); seen={identity}; todo=[identity]
    for x,y,h in todo:
        a,b,c,d=mats[h]
        for u,v,k in gs:
            z=((x+a*u+b*v)%p,(y+c*u+d*v)%p,tab[h][k])
            if z not in seen: seen.add(z); todo.append(z)
    return seen

def intersection(sets):
    it=iter(sets); acc=set(next(it))
    for s in it: acc.intersection_update(s)
    return acc

p=29; A=(0,28,1,0); B=(2,7,12,28)
mats,ix,tab,one,gen=construct(p,A,B)
assert len(mats)==120 and all((a*d-b*c)%p==1 for a,b,c,d in mats)
minus=ix[(28,0,0,28)]; Z={one,minus}
assert power(A,2,p)==power(B,3,p)==power(mm(A,B,p),5,p)==mats[minus]

# Enumerate all actual subgroups by breadth-first extension, retaining a small
# generating tuple for each discovered subgroup. Completeness follows because
# each subgroup has a generating sequence and every possible next element is tried.
subs={frozenset([one]):()}; queue=deque(subs)
while queue:
    s=queue.popleft(); gs=subs[s]
    for x in range(120):
        if x not in s:
            t=gen(gs+(x,))
            if t not in subs: subs[t]=gs+(x,); queue.append(t)
assert len(subs)==76
proper=[bitset(s) for s in subs if len(s)<120]
triple_count=0; faithful_triples=0; normal_triples=0; irr_triples=0
for a,b,c in itertools.combinations(proper,3):
    triple_count+=1; meet=a&b&c
    if (a&b)!=meet and (a&c)!=meet and (b&c)!=meet:
        irr_triples+=1
        if meet==(1<<one): faithful_triples+=1
        # normality checked directly against both generators, which generate H.
        elems=[x for x in range(120) if (meet>>x)&1]
        normal=True
        for h in [ix[A],ix[B]]:
            inv=next(x for x in range(120) if tab[h][x]==one)
            if any(not ((meet>>tab[tab[h][x]][inv])&1) for x in elems): normal=False
        normal_triples+=normal
quad_count=0; irr_quads=0
for a,b,c,d in itertools.combinations(proper,4):
    quad_count+=1; meet=a&b&c&d
    if a&b&c!=meet and a&b&d!=meet and a&c&d!=meet and b&c&d!=meet:
        irr_quads+=1
assert faithful_triples==0 and irr_quads==0 and normal_triples>0

R=[(0,28,1,0),(12,24,0,17),(25,3,4,4)]
assert R[1]==mm(mm(B,A,p),power(B,2,p),p)
assert R[2]==mm(mm(A,R[1],p),power(mm(A,B,p),2,p),p)
r=[ix[x] for x in R]
assert all(power(x,2,p)==mats[minus] for x in R)
pairs=[gen([r[j] for j in range(3) if j!=i]) for i in range(3)]
assert list(map(len,pairs))==[8,12,20]
assert intersection(pairs)==Z and len(gen(r))==120
assert all(r[i] not in pairs[i] for i in range(3))
odd_subgroups=[s for s in subs if len(s)%2]
assert all(len(s) in (1,3,5) for s in odd_subgroups)
assert all(Z<=s for s in subs if len(s)%2==0)
assert Counter(order(h,tab,one) for h in range(120))[2]==1

# All 30 lines, represented by (1,t), and the vertical line (0,1).
line_stabilizers=[]
for u,v in [(1,t) for t in range(29)]+[(0,1)]:
    st={h for h,(a,b,c,d) in enumerate(mats) if ((a*u+b*v)*v-(c*u+d*v)*u)%29==0}
    line_stabilizers.append(st)
    assert len(st)==4 and any(gen([x])==st for x in st)
    assert all((h==one) or ((mats[h][0]*u+mats[h][1]*v)%29,(mats[h][2]*u+mats[h][3]*v)%29)!=(u,v) for h in st)

# Explicit isomorphism with SL2(5), reconstructed by simultaneous closure.
A5mat=(0,4,1,0); B5mat=(0,4,1,1)
seen={I:I}; pending=[I]
for q in pending:
    for u,v in [(A5mat,A),(B5mat,B)]:
        q2=mm(q,u,5); h2=mm(seen[q],v,29)
        if q2 in seen: assert seen[q2]==h2
        else: seen[q2]=h2; pending.append(q2)
assert len(seen)==120 and len(set(seen.values()))==120
# Check every product, not only the generator transitions.
assert all(seen[mm(q,r,5)]==mm(seen[q],seen[r],29) for q in seen for r in seen)

# Explicit A5 quotient, using permutation composition (left factor after right).
def compose(s,t): return tuple(s[t[i]] for i in range(5))
pone=tuple(range(5)); pa=(1,0,3,2,4); pb=(2,1,4,3,0)
quot={one:pone}; todo=[one]
for h in todo:
    for a,b in [(ix[A],pa),(ix[B],pb)]:
        k=tab[h][a]; v=compose(quot[h],b)
        if k in quot: assert quot[k]==v
        else: quot[k]=v; todo.append(k)
assert len(set(quot.values()))==60
assert {h for h in quot if quot[h]==pone}==Z
assert all(quot[tab[h][k]]==compose(quot[h],quot[k]) for h in quot for k in quot)
inverses=[next(k for k in range(120) if tab[h][k]==one) for h in range(120)]
for subgroup in pairs:
    core=intersection({tab[tab[h][x]][inverses[h]] for x in subgroup} for h in range(120))
    assert core==Z
# H intersects its translation conjugate at elements fixing e1; here only I.
assert {h for h,m in enumerate(mats) if (m[0],m[2])==(1,0)}=={one}

# Independent affine enumeration. No multiplication table of the affine group.
S=[(1,0,one)]+[(0,0,h) for h in r]
G=affine_closure(S,29,mats,tab,one)
assert len(G)==100920
omissions=[affine_closure(S[:j]+S[j+1:],29,mats,tab,one) for j in range(4)]
assert list(map(len,omissions))==[120,6728,10092,16820]
assert all(S[j] not in omissions[j] for j in range(4))
bottom=intersection(omissions)
assert bottom=={(0,0,one),(0,0,minus)}
assert (2,0,minus) in G and (2,0,minus) not in bottom
L=[affine_closure(gs,29,mats,tab,one) for gs in
   [[(1,0,one),(0,0,minus)],[(0,1,one),(0,0,minus)],[(1,1,one),(2,0,minus)]]]
assert list(map(len,L))==[58]*3
expected=[{(0,0,one),(0,0,minus)}, {(0,0,one),(2,0,minus)}, {(0,0,one),(0,27,minus)}]
assert [L[i]&L[j] for i,j in [(0,1),(0,2),(1,2)]]==expected
assert intersection(L)=={(0,0,one)}

# Direct boundary-case construction and intersections in characteristic 11.
m11,i11,t11,e11,g11=construct(11,(0,10,1,0),(0,2,5,1))
assert len(m11)==120
C=(6,10,0,2); c11=i11[C]
assert order(c11,t11,e11)==10
c2=i11[power(C,2,11)]; c5=i11[power(C,5,11)]
K=[affine_closure(gs,11,m11,t11,e11) for gs in
   [[(1,0,e11),(0,0,c11)],[(1,4,e11),(0,0,c11)],
    [(1,0,e11),(0,1,e11),(0,0,c5)],[(1,0,e11),(0,1,e11),(0,0,c2)]]]
assert intersection(K)=={(0,0,e11)}
deletions=[len(intersection(K[:i]+K[i+1:])) for i in range(4)]
assert deletions==[11,11,5,2]

result={
 'status':'all_assertions_passed',
 'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'runtime_seconds':round(time.monotonic()-START,3),
 'arithmetic':'exact integers, standard-library Python',
 'complement_order':120,
 'subgroups':len(subs),
 'subgroup_order_distribution':dict(sorted(Counter(map(len,subs)).items())),
 'proper_subgroup_triples_checked':triple_count,
 'irredundant_triples':irr_triples,
 'faithful_irredundant_triples':faithful_triples,
 'normal_bottom_irredundant_triples':normal_triples,
 'proper_subgroup_quadruples_checked':quad_count,
 'irredundant_quadruples':irr_quads,
 'complement_invariants':{'mu_prime':3,'b':3,'b_faithful':2},
 'pair_subgroup_orders':list(map(len,pairs)),
 'line_stabilizer_order_distribution':dict(Counter(map(len,line_stabilizers))),
 'sl2_5_isomorphism_all_products_checked':120**2,
 'a5_quotient_all_products_checked':120**2,
 'a5_quotient_kernel_order':2,
 'pair_subgroup_core_orders':[2,2,2],
 'complement_translation_conjugate_intersection_order':1,
 'affine_group_order':len(G),
 'affine_independent_set_omission_orders':list(map(len,omissions)),
 'affine_independent_set_common_intersection_order':len(bottom),
 'faithful_three_family_subgroup_orders':list(map(len,L)),
 'faithful_three_family_pair_intersection_orders':[len(x) for x in expected],
 'characteristic_11_group_order':len(m11)*121,
 'characteristic_11_family_orders':list(map(len,K)),
 'characteristic_11_deletion_intersection_orders':deletions,
 'finite_verification_completion_percent':100,
 'limitation':'General all-actions upper bound for G relies on manuscript structural proof; the subgroup lattice of G was not enumerated.'
}
(HERE/'independent_check_results.json').write_text(json.dumps(result,indent=2)+'\n')
# Canonical complete subgroup certificate enables comparison without shared labels.
certificate=sorted([sorted([list(mats[h]) for h in s]) for s in subs],key=lambda s:(len(s),s))
(HERE/'independent_subgroups.json').write_text(json.dumps(certificate)+'\n')
print(json.dumps(result,indent=2))
