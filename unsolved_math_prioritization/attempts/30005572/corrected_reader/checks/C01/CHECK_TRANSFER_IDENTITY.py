"""Finite sanity checks of the stated trivial-coefficient cochain-transfer identity.
The general proof is the cocycle calculation in RAMIFIED_FIVE_ACCEPTANCE.md.
No external packages, floating-point arithmetic, or mathematical source text.
"""
import itertools
import json
from pathlib import Path

results=[]
def check(name,G,mul,identity,H,k):
    reps=[]; decomposition={}
    for g in G:
        if g in decomposition:
            continue
        reps.append(g)
        for h in H:
            x=mul(h,g)
            if x in decomposition:
                raise AssertionError('Coset overlap')
            decomposition[x]=(h,g)
    def split(t,g):
        return decomposition[mul(t,g)]
    def A(g):
        return sum(k(t,g)-k(*split(t,g)) for t in reps)
    def transfer_k(g,h):
        total=0
        for t in reps:
            h1,t1=split(t,g)
            h2,t2=split(t1,h)
            total+=k(h1,h2)
        return total
    for g,h,j in itertools.product(G,repeat=3):
        if k(h,j)-k(mul(g,h),j)+k(g,mul(h,j))-k(g,h):
            raise AssertionError((name,'Not a cocycle',g,h,j))
    for g,h in itertools.product(G,repeat=2):
        lhs=transfer_k(g,h)
        rhs=len(reps)*k(g,h)-(A(h)-A(mul(g,h))+A(g))
        if lhs!=rhs:
            raise AssertionError((name,g,h,lhs,rhs))
    results.append({'group':name,'order':len(G),'subgroup_order':len(H),'index':len(reps),'pair_checks':len(G)**2,'passed':True})

for n in (4,6,8,9,10,12):
    G=list(range(n)); mul=lambda a,b,n=n:(a+b)%n
    for d in range(2,n+1):
        if n%d:
            continue
        H=list(range(0,n,d))
        f={g:g*g-3*g for g in G}
        def k(a,b,n=n,f=f):
            return (a+b)//n+f[a]+f[b]-f[(a+b)%n]
        check('C'+str(n),G,mul,0,H,k)

G=list(itertools.permutations(range(3)))
id3=(0,1,2)
mul=lambda a,b:tuple(a[b[i]] for i in range(3))
H=[id3,(1,0,2)]
f={g:(i*i-2*i) for i,g in enumerate(G)}
f[id3]=0
k=lambda a,b:f[a]+f[b]-f[mul(a,b)]
check('S3 nonnormal subgroup',G,mul,id3,H,k)
result={'identity':'Tr(k|H) = index*k - d_group A_k','integer_arithmetic':True,'scope':'sanity checks only; not substitute for general proof','cases':results,'total_pair_checks':sum(r['pair_checks'] for r in results),'all_passed':all(r['passed'] for r in results)}
print(json.dumps(result,indent=2))
Path(__file__).with_name('TRANSFER_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
