#!/usr/bin/env python3
"""Exact component-color checks of the star-forest theorem."""
import itertools,json
counts={}
def ck(x,k):
    assert x,k
    counts[k]=counts.get(k,0)+1

def parts(total,ceiling=None):
    if total==0:yield ();return
    if ceiling is None:ceiling=total
    for a in range(min(total,ceiling),0,-1):
        for rest in parts(total-a,a):yield (a,)+rest

def comps(total,q):
    if q==1:yield (total,);return
    for a in range(total+1):
        for t in comps(total-a,q-1):yield (a,)+t

def fits(cap,target):
    cap=sorted(cap,reverse=True)
    return len(cap)>=len(target) and all(a>=b for a,b in zip(cap,target))

def direct(host,target,q):
    for alloc in itertools.product(*(list(comps(d,q)) for d in host)):
        if all(not fits([a[c] for a in alloc],target) for c in range(q)):return False
    return True

def threshold(host,target,q):
    tau={t:sum(k>=t for k in target) for t in set(target)}
    for tt in itertools.product(sorted(tau),repeat=q):
        D=sum(t-1 for t in tt);quota=[tau[t]-1 for t in tt]
        if sum(d>D for d in host)<=sum(quota):return False,tt,quota
    return True,None,None

def conv(a,b):return tuple(max(a[i]+b[k-i] for i in range(max(0,k-len(b)+1),min(len(a)-1,k)+1)) for k in range(len(a)+len(b)-1))
def canonical(target,q):
    a=tuple(k-1 for k in target);c=(0,)
    for _ in range(q):c=conv(c,a)
    return tuple(x+1 for x in c)

def avoid(host,tt,quota):
    q=len(tt);remaining=list(quota);D=sum(t-1 for t in tt);out=[]
    for d in host:
        a=[0]*q;left=d
        if d>D:
            c=next(i for i,r in enumerate(remaining) if r);remaining[c]-=1
            for i in range(q):
                if i!=c:a[i]=min(left,tt[i]-1);left-=a[i]
            a[c]=left
        else:
            for i in range(q):a[i]=min(left,tt[i]-1);left-=a[i]
            assert left==0
        out.append(a)
    return out
hosts=[p for n in range(8) for p in parts(n)]
targets=[p for n in range(1,6) for p in parts(n)]
cases=0;avoidcases=0
for target in targets:
    for q in [2,3,4]:
        F=canonical(target,q)
        ck(len(F)==q*(len(target)-1)+1,'canonical_component_count')
        ck(F[0]==q*(target[0]-1)+1,'canonical_largest_component')
        ck(all(F[i]>=F[i+1] for i in range(len(F)-1)),'canonical_sorted')
        for host in hosts:
            cases+=1;a=direct(host,target,q);b,tt,quota=threshold(host,target,q)
            ck(a==b,'direct_vs_threshold')
            ck(a==fits(host,F),'direct_vs_canonical')
            if not b:
                avoidcases+=1;allocation=avoid(host,tt,quota)
                for d,row in zip(host,allocation):ck(sum(row)==d and all(x>=0 for x in row),'avoiding_allocation_valid')
                for c in range(q):ck(not fits([r[c] for r in allocation],target),'avoiding_color_target_absent')
ck(canonical((2,1),2)==(3,2,1),'small_example_q2')
ck(canonical((2,1),3)==(4,3,2,1),'small_example_q3')
a=(5,4,2,2,1);b=(5,4,3,2,1)
ck(canonical(a,2)==tuple(range(9,0,-1)),'collision_first_profile')
ck(canonical(b,2)==tuple(range(9,0,-1)),'collision_second_profile')
print(json.dumps({'problem_id':30003973,'status':'PASS','assertions':sum(counts.values()),'counts':counts,'host_profiles':len(hosts),'host_edges_max':7,'target_profiles':len(targets),'target_edges_max':5,'colors':[2,3,4],'profile_cases':cases,'avoiding_cases':avoidcases,'collision':{'targetA':a,'targetB':b,'common_q2_host':list(range(9,0,-1))},'scope':'Exact bounded tests of the proved all-size star-forest-host criterion. Same restricted-host profile is not universal Ramsey equivalence.'},indent=2,sort_keys=True))
