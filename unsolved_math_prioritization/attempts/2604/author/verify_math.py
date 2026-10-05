#!/usr/bin/env python3
"""Exact, dependency-free checks for the exclusions in PROOFS.md.
This does not test recognisability against all finite groups.
"""
import argparse,itertools,json,math
from collections import Counter,defaultdict
from pathlib import Path

def pf(n):
    ans=[]; d=2
    while d*d<=n:
        if n%d==0:
            ans.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:ans.append(n)
    return ans

def divisors(n):return [d for d in range(1,n+1) if n%d==0]
def primes(n):return [p for p in range(2,n+1) if pf(p)==[p]]
def graph(verts,orders):
    return {'vertices':sorted(verts),'edges':[list(e) for e in itertools.combinations(sorted(verts),2) if any(o%(e[0]*e[1])==0 for o in orders)]}
def sn_graph(n):return graph(primes(n),[p*q for p,q in itertools.combinations(primes(n),2) if p+q<=n])
def pgl_graph(q):
    ch=pf(q); assert len(ch)==1 and q%2
    return graph(set(pf(q-1)+pf(q+1)+ch),divisors(q-1)+divisors(q+1)+ch)
def pgl_key(q):return tuple(sorted((len(pf(q-1))-1,len(pf(q+1))-1)))
def pgl_map(q,r):
    assert q!=r and pgl_key(q)==pgl_key(r)
    a,b=[p for p in pf(q-1) if p!=2],[p for p in pf(q+1) if p!=2]
    c,d=[p for p in pf(r-1) if p!=2],[p for p in pf(r+1) if p!=2]
    if len(a)!=len(c):c,d=d,c
    m={2:2,pf(q)[0]:pf(r)[0]}; m.update(zip(a,c));m.update(zip(b,d))
    g,h=pgl_graph(q),pgl_graph(r)
    assert set(m)==set(g['vertices']) and set(m.values())==set(h['vertices'])
    assert {tuple(sorted((m[x],m[y]))) for x,y in g['edges']}=={tuple(e) for e in h['edges']}
    return m

def pgl_enumerate(p):
    def norm(a):
        s=next(x for x in a if x); inv=pow(s,-1,p)
        return tuple(x*inv%p for x in a)
    def mul(a,b):
        return norm(((a[0]*b[0]+a[1]*b[2])%p,(a[0]*b[1]+a[1]*b[3])%p,(a[2]*b[0]+a[3]*b[2])%p,(a[2]*b[1]+a[3]*b[3])%p))
    one=(1,0,0,1)
    def power(a,n):
        z=one
        while n:
            if n&1:z=mul(z,a)
            a=mul(a,a);n//=2
        return z
    count=Counter()
    mats=itertools.chain(((1,b,c,d) for b,c,d in itertools.product(range(p),repeat=3)),((0,1,c,d) for c,d in itertools.product(range(p),repeat=2)))
    for a in mats:
        if (a[0]*a[3]-a[1]*a[2])%p==0:continue
        o=p*(p*p-1)
        for r in pf(o):
            while o%r==0 and power(a,o//r)==one:o//=r
        assert power(a,o)==one
        count[o]+=1
    assert sum(count.values())==p*(p*p-1)
    assert set(count)==set(divisors(p-1)+divisors(p+1)+[p])
    return {'p':p,'order':sum(count.values()),'element_order_counts':dict(sorted(count.items())),'graph':graph(pf(p*(p*p-1)),count)}

def perm_order(g):
    unseen=set(range(len(g))); o=1
    while unseen:
        i=next(iter(unseen)); j=i; k=0
        while j in unseen:unseen.remove(j);k+=1;j=g[j]
        o=math.lcm(o,k)
    return o

def symmetric_affine(n,mode='deleted'):
    ones=(1<<n)-1
    def rep(v):return min(v,v^ones) if mode=='deleted' and n%2==0 else v
    vectors=sorted({rep(v) for v in range(1<<n) if mode=='full' or v.bit_count()%2==0})
    def act(g,v):return rep(sum(((v>>i)&1)<<g[i] for i in range(n)))
    counts=Counter();base=Counter()
    for g in itertools.permutations(range(n)):
        m=perm_order(g);base[m]+=1
        for v in vectors:
            z=0;u=v
            for _ in range(m):z^=u;u=act(g,u)
            z=rep(z);counts[m if z==0 else 2*m]+=1
    g=graph(primes(n),counts)
    if mode=='deleted':assert g==sn_graph(n)
    return {'n':n,'mode':mode,'module_order':len(vectors),'group_order':sum(counts.values()),'base_element_order_counts':dict(sorted(base.items())),'affine_element_order_counts':dict(sorted(counts.items())),'graph':g}

class F2:
    def __init__(self,f,poly):self.f=f;self.q=1<<f;self.poly=poly
    def mul(self,a,b):
        z=0
        while b:
            if b&1:z^=a
            b>>=1;a<<=1
            if a&self.q:a^=self.poly
        return z
    def frob(self,a,j):
        for _ in range(j):a=self.mul(a,a)
        return a

def semilinear_check(f,poly):
    F=F2(f,poly);q=F.q;mul=F.mul
    mats=[a for a in itertools.product(range(q),repeat=4) if mul(a[0],a[3])^mul(a[1],a[2])==1]
    assert len(mats)==q*(q*q-1)
    def mm(a,b):return (mul(a[0],b[0])^mul(a[1],b[2]),mul(a[0],b[1])^mul(a[1],b[3]),mul(a[2],b[0])^mul(a[3],b[2]),mul(a[2],b[1])^mul(a[3],b[3]))
    def gm(x,y):return (mm(x[0],tuple(F.frob(t,x[1]) for t in y[0])),(x[1]+y[1])%f)
    one=((1,0,0,1),0)
    def power(x,n):
        z=one
        while n:
            if n&1:z=gm(z,x)
            x=gm(x,x);n//=2
        return z
    def action(g,v):
        a,j=g;x,y=(F.frob(t,j) for t in v)
        return (mul(a[0],x)^mul(a[1],y),mul(a[2],x)^mul(a[3],y))
    vs=list(itertools.product(range(q),repeat=2));count=Counter();aff=Counter();fixed_checks=0
    total=len(mats)*f
    for a,j in itertools.product(mats,range(f)):
        x=(a,j);o=total
        for r in pf(o):
            while o%r==0 and power(x,o//r)==one:o//=r
        assert power(x,o)==one;count[o]+=1
        for v in vs:
            z=(0,0);u=v
            for _ in range(o):z=(z[0]^u[0],z[1]^u[1]);u=action(x,u)
            aff[o if z==(0,0) else 2*o]+=1
            if o>2 and pf(o)==[o] and v!=(0,0) and action(x,v)==v:
                h,k=v
                t=(1^mul(h,k),mul(h,h),mul(k,k),1^mul(h,k))
                assert t in mats and t!=(1,0,0,1) and mm(t,t)==one[0]
                assert gm(x,(t,0))==gm((t,0),x)
                fixed_checks+=1
    assert graph(pf(total),count)==graph(pf(total),aff)
    return {'f':f,'q':q,'irreducible_polynomial_binary':poly,'base_order':total,'affine_order':sum(aff.values()),'base_element_order_counts':dict(sorted(count.items())),'affine_element_order_counts':dict(sorted(aff.items())),'fixed_vector_transvection_checks':fixed_checks,'graph':graph(pf(total),count)}

def run():
    pps=set()
    for p in primes(10000):
        if p==2:continue
        q=p
        while q<=10000:
            if q>=5:pps.add(q)
            q*=p
    groups=defaultdict(list)
    for q in sorted(pps):groups[pgl_key(q)].append(q)
    census=[];unmatched=[]
    for q in sorted(x for x in pps if x<=1000):
        targets=[r for r in groups[pgl_key(q)] if r!=q]
        if not targets:unmatched.append(q);continue
        r=targets[0];m=pgl_map(q,r)
        census.append({'q':q,'witness_q':r,'vertex_map':m})
    pairs=[{'q':q,'r':r,'vertex_map':pgl_map(q,r),'q_graph':pgl_graph(q),'r_graph':pgl_graph(r)} for q,r in [(27,11),(169,181),(289,29)]]
    syms=[symmetric_affine(n) for n in (5,6,7)]
    neg_full=symmetric_affine(5,'full');neg_augmentation=symmetric_affine(6,'augmentation')
    assert [2,5] in neg_full['graph']['edges'] and [2,5] not in sn_graph(5)['edges']
    assert [2,5] in neg_augmentation['graph']['edges'] and [2,5] not in sn_graph(6)['edges']
    fixed=[]
    for n in range(5,101):
        for r in primes(n):
            if r==2:continue
            for k in range(1,n//r+1):
                dim=n-k*(r-1)-1-(n%2==0)
                assert dim>=0
                if 2+r>n:assert dim==0
        fixed.append(n)
    wrong=pgl_map(169,181);wrong[3],wrong[5]=wrong[5],wrong[3]
    g,h=pgl_graph(169),pgl_graph(181)
    assert {tuple(sorted((wrong[x],wrong[y]))) for x,y in g['edges']}!={tuple(e) for e in h['edges']}
    return {'status':'PASS','scope':'Exact exclusions and controls, not a solution of Kourovka 21.95','symmetric_affine':syms,'fixed_space_formula_n_checked':fixed,'semilinear_affine':[semilinear_check(2,0b111),semilinear_check(3,0b1011)],'pgl_matrix_enumerations':[pgl_enumerate(p) for p in (5,7,11,13)],'pgl_named_collisions':pairs,'pgl_census':{'target_max_q':1000,'witness_max_q':10000,'targets':len(census)+len(unmatched),'excluded':len(census),'unmatched':unmatched,'certificates':census},'negative_controls':{'full_module_adds_2_5_to_S5':neg_full,'augmentation_without_quotient_adds_2_5_to_S6':neg_augmentation,'mutated_pgl_vertex_map_rejected':True}}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    result=run();path=Path(__file__).with_name('CHECK_RESULTS.json')
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:assert json.loads(path.read_text())==json.loads(json.dumps(result))
    print(json.dumps({'status':result['status'],'symmetric_affine_orders':[x['group_order'] for x in result['symmetric_affine']],'semilinear_affine_orders':[x['affine_order'] for x in result['semilinear_affine']],'pgl_targets':result['pgl_census']['targets'],'pgl_excluded':result['pgl_census']['excluded'],'pgl_unmatched':result['pgl_census']['unmatched']},indent=2))
