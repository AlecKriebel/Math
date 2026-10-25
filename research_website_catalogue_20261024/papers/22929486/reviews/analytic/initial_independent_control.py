"""Fresh exact reconstruction, written before opening the supplied verifier code.

Uses matrices, finite Cayley closure, subgroup bitsets, and affine element sets.
No published certificates, group catalogues, or optimization packages are inputs.
"""
from itertools import combinations
from collections import Counter, deque
from pathlib import Path
import json, time, hashlib, datetime

START = time.time()
CHECKS = []
def check(name, condition, evidence):
    assert condition, (name, evidence)
    CHECKS.append({'check': name, 'passed': True, 'evidence': evidence})

def mm(a,b,p):
    return ((a[0]*b[0]+a[1]*b[2])%p,(a[0]*b[1]+a[1]*b[3])%p,
            (a[2]*b[0]+a[3]*b[2])%p,(a[2]*b[1]+a[3]*b[3])%p)
I=(1,0,0,1)
def closure(gens,unit,prod):
    seen={unit}; todo=[unit]
    for a in todo:
        for g in gens:
            b=prod(a,g)
            if b not in seen: seen.add(b);todo.append(b)
    return frozenset(seen)
def power(a,k,p):
    b=I
    for _ in range(k):b=mm(b,a,p)
    return b
def order(a,p):
    b=a;k=1
    while b!=I:b=mm(b,a,p);k+=1
    return k
def hgroup(p,A,B):return sorted(closure([A,B],I,lambda a,b:mm(a,b,p)))
def intersect(xs):
    out=xs[0]
    for x in xs[1:]:out=out & x
    return out

p=29;A=(0,28,1,0);B=(2,7,12,28);minus=(28,0,0,28)
H=hgroup(p,A,B);idx={h:i for i,h in enumerate(H)};one=idx[I]
check('H is 120 determinant-one matrices',len(H)==120 and all((a*d-b*c)%p==1 for a,b,c,d in H),len(H))
check('triangle lift relations',power(A,2,p)==power(B,3,p)==power(mm(A,B,p),5,p)==minus,True)
table=[[idx[mm(a,b,p)] for b in H] for a in H]
inverses=[next(j for j in range(120) if table[i][j]==one) for i in range(120)]
check('unique involution',[h for h in H if h!=I and mm(h,h,p)==I]==[minus],list(minus))

# The joint word closure proves these are homomorphisms and bijections without
# invoking the triangle-group presentation or a library group identifier.
C=(0,4,1,0);D=(0,4,1,1)
paired=closure([(A,C),(B,D)],(I,I),lambda a,b:(mm(a[0],b[0],29),mm(a[1],b[1],5)))
all_sl5={(a,b,c,d) for a in range(5) for b in range(5) for c in range(5) for d in range(5) if (a*d-b*c)%5==1}
check('explicit SL2(5) isomorphism',len(paired)==120 and {a for a,b in paired}==set(H) and {b for a,b in paired}==all_sl5,{'joint_group':len(paired),'SL2(5)':len(all_sl5)})
perm_id=tuple(range(5));pa=(1,0,3,2,4);pb=(2,1,4,3,0)
def pm(a,b):return tuple(a[b[i]] for i in range(5))
joint=closure([(A,pa),(B,pb)],(I,perm_id),lambda a,b:(mm(a[0],b[0],29),pm(a[1],b[1])))
Q={b for a,b in joint};kernel={a for a,b in joint if b==perm_id}
check('explicit A5 quotient',len(joint)==120 and len(Q)==60 and kernel=={I,minus},{'joint':len(joint),'quotient':len(Q),'kernel':sorted(kernel)})
pinv={a:tuple(a.index(i) for i in range(5)) for a in Q}
classes={frozenset(pm(pm(g,a),pinv[g]) for g in Q) for a in Q}
sizes=sorted(map(len,classes))
check('A5 conjugacy classes and simplicity test',sizes==[1,12,12,15,20] and not any(60%(1+sum(s))==0 and 1<1+sum(s)<60 for r in range(1,5) for s in combinations([12,12,15,20],r)),sizes)

# Discover all actual subgroups with retained generating sets; bitsets only
# accelerate later intersections. Completeness follows by adding one generator.
subgens={frozenset([one]):()};todo=list(subgens)
for sub in todo:
    for g in range(120):
        if g in sub:continue
        gens=subgens[sub]+(g,)
        new=closure(gens,one,lambda a,b:table[a][b])
        if new not in subgens:subgens[new]=gens;todo.append(new)
check('complete H subgroup count',len(subgens)==76,dict(sorted(Counter(map(len,subgens)).items())))
check('odd subgroup orders and common involution of even subgroups',all((len(s) in [1,3,5]) if len(s)%2 else idx[minus] in s for s in subgens),True)
proper=[sum(1<<a for a in s) for s in subgens if len(s)<120]
four_bad=0
for a,b,c,d in combinations(proper,4):
    z=a&b&c&d
    if b&c&d!=z and a&c&d!=z and a&b&d!=z and a&b&c!=z:four_bad+=1
check('all four-subgroup families are redundant',four_bad==0,{'tested':1215450,'irredundant':four_bad})
triple_bad=sum(a&b&c==1<<one and a&b!=1<<one and a&c!=1<<one and b&c!=1<<one for a,b,c in combinations(proper,3))
check('no faithful irredundant triple in H',triple_bad==0,{'tested':67525,'faithful_minimal':triple_bad})
normal=[s for s in subgens if all(table[table[g][x]][inverses[g]] in s for g in range(120) for x in s)]
check('normal subgroups of H',sorted(map(len,normal))==[1,2,120],sorted(map(len,normal)))

R=[A,(12,24,0,17),(25,3,4,4)]
check('R words',R[1]==mm(mm(B,A,p),power(B,2,p),p) and R[2]==mm(mm(A,R[1],p),power(mm(A,B,p),2,p),p),R)
P=[closure([idx[r] for j,r in enumerate(R) if j!=i],one,lambda a,b:table[a][b]) for i in range(3)]
check('independent complement triple',list(map(len,P))==[8,12,20] and all(idx[R[i]] not in P[i] for i in range(3)) and len(closure([idx[r] for r in R],one,lambda a,b:table[a][b]))==120,list(map(len,P)))
check('complement witness intersection',intersect(P)=={one,idx[minus]},sorted(intersect(P)))

def action(h,v,p):return ((h[0]*v[0]+h[1]*v[1])%p,(h[2]*v[0]+h[3]*v[1])%p)
lines=[(1,t) for t in range(29)]+[(0,1)]
stabdata=[]
for v in lines:
    s=[h for h in H if (action(h,v,p)[0]*v[1]-action(h,v,p)[1]*v[0])%p==0]
    scalar=[action(h,v,p)[0] if v[0] else action(h,v,p)[1] for h in s]
    check('line stabilizer '+str(v),len(s)==len(set(scalar))==4 and any(order(h,p)==4 for h in s),{'order':len(s),'scalars':sorted(scalar)})
    stabdata.append({'line':v,'order':len(s)})

# Exact affine elements encode the matrix by its independent table index.
unit=(0,0,one)
def aff(a,b):
    w=action(H[a[2]],b[:2],29)
    return ((a[0]+w[0])%29,(a[1]+w[1])%29,table[a[2]][b[2]])
S=[(1,0,one)]+[(0,0,idx[r]) for r in R]
G=closure(S,unit,aff)
check('generated affine group',len(G)==100920,len(G))
M=[closure(S[:i]+S[i+1:],unit,aff) for i in range(4)]
check('four independent generators and omission groups',list(map(len,M))==[120,6728,10092,16820] and all(S[i] not in M[i] for i in range(4)),list(map(len,M)))
z0=frozenset([unit,(0,0,idx[minus])])
check('nonnormal intersection obstruction',intersect(M)==z0 and aff(aff(S[0],(0,0,idx[minus])),(28,0,one))==(2,0,idx[minus]) and (2,0,idx[minus]) not in z0,{'intersection':sorted(z0),'conjugate':(2,0,idx[minus])})
L=[closure(gs,unit,aff) for gs in [[(1,0,one),(0,0,idx[minus])],[(0,1,one),(0,0,idx[minus])],[(1,1,one),(2,0,idx[minus])]]]
pair_intersections=[L[0]&L[1],L[0]&L[2],L[1]&L[2]]
check('faithful minimal triple',list(map(len,L))==[58]*3 and intersect(L)=={unit} and pair_intersections==[{unit,(0,0,idx[minus])},{unit,(2,0,idx[minus])},{unit,(0,27,idx[minus])}],{'orders':list(map(len,L)),'pair_intersections':[sorted(x) for x in pair_intersections],'degree':3*100920//58})

# Boundary/control: replacing 29 by 11 invalidates the upper-bound mechanism.
H11=hgroup(11,(0,10,1,0),(0,2,5,1));C11=(6,10,0,2);minus11=(10,0,0,10)
def aff11(a,b):
    w=action(a[2],b[:2],11)
    return ((a[0]+w[0])%11,(a[1]+w[1])%11,mm(a[2],b[2],11))
u11=(0,0,I)
LL=[closure(gs,u11,aff11) for gs in [[(1,0,I),(0,0,C11)],[(1,4,I),(0,0,C11)],[(1,0,I),(0,1,I),(0,0,power(C11,5,11))],[(1,0,I),(0,1,I),(0,0,power(C11,2,11))]]]
deletions=[len(intersect(LL[:i]+LL[i+1:])) for i in range(4)]
check('characteristic eleven falsifies unrestricted extension',len(H11)==120 and C11 in H11 and order(C11,11)==10 and intersect(LL)=={u11} and deletions==[11,11,5,2],{'H_order':len(H11),'C_order':order(C11,11),'subgroup_orders':list(map(len,LL)),'deletion_intersections':deletions})
# A mutation of the affine third stabilizer to the zero coset must destroy faithfulness.
badL=closure([(1,1,one),(0,0,idx[minus])],unit,aff)
check('zero-offset mutation detected',len(L[0]&L[1]&badL)==2,len(L[0]&L[1]&badL))

out={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'arithmetic':'exact Python integers modulo primes; no supplied verification code imported','named_checks':len(CHECKS),'elapsed_seconds':time.time()-START,'checks':CHECKS}
Path(__file__).with_suffix('.results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'checks':len(CHECKS),'passed':True,'elapsed_seconds':out['elapsed_seconds']},indent=2))
