"""Independent finite and integer controls; imports no author code.

These controls do not certify infinite CB, category, or a target solution.
"""
from collections import deque, Counter
from itertools import combinations, permutations, product
from pathlib import Path
import json

counts = Counter()
details = {}

def check(proposition, category):
    assert proposition, category
    counts[category] += 1

def distances(elements, multiply, identity, letters):
    d = {identity: 0}
    q = deque([identity])
    while q:
        x = q.popleft()
        for s in letters:
            y = multiply(x, s)
            if y not in d:
                d[y] = d[x] + 1
                q.append(y)
    return d

def power_set(es):
    for k in range(1, len(es) + 1):
        yield from combinations(es, k)

def cyclic(n):
    return tuple(range(n)), lambda x,y:(x+y)%n, 0, lambda x:(-x)%n

def dihedral(n):
    es=tuple(product(range(n),range(2)))
    return es, lambda x,y:((x[0]+(-1)**x[1]*y[0])%n,(x[1]+y[1])%2), (0,0), lambda x:((-(-1)**x[1]*x[0])%n,x[1])

def symmetric3():
    es=tuple(permutations(range(3)))
    mul=lambda x,y:tuple(x[y[i]] for i in range(3))
    inv=lambda x:tuple(x.index(i) for i in range(3))
    return es,mul,tuple(range(3)),inv

group_set_counts=[]
for name, data in [(f'C{n}',cyclic(n)) for n in range(2,10)]+[('S3',symmetric3()),('D10',dihedral(5))]:
    es,mul,e,inv=data
    nsets=0
    for S in power_set(tuple(x for x in es if x!=e)):
        p=distances(es,mul,e,S)
        u=distances(es,mul,e,set(S)|{inv(s) for s in S})
        check(set(p)==set(u),'finite_group_positive_generation')
        if len(p)!=len(es): continue
        nsets+=1
        R=max(p[inv(s)] for s in S);D=max(p.values());d=max(u.values())
        check(R<=D<=d*max(1,R),'inverse_cost')
        for b in range(D+1):
            A={x for x in es if p[x]<=b and p[inv(x)]<=b}
            c=distances(es,mul,e,A)
            check(all(inv(x) in A for x in A),'symmetric_core')
            check(all(p[x]<=b*c[x] for x in c),'core_positive_conversion')
            if len(c)==len(es): check(D<=b*max(c.values()),'core_global_bound')
    group_set_counts.append({'group':name,'generating_sets':nsets})
details['group_sets']=group_set_counts

# Nonnormal right cosets, independently enumerated in S3.
es,mul,e,inv=symmetric3()
h=(1,0,2);H={e,h}
check(any(mul(mul(x,h),inv(x)) not in H for x in es),'nonnormal_test_subgroup')
cosets={frozenset(mul(z,x) for z in H) for x in es}
coset_of={x:next(c for c in cosets if x in c) for x in es}
for S in power_set(tuple(x for x in es if x!=e)):
    p=distances(es,mul,e,S)
    if len(p)!=len(es): continue
    reps={c:min(c,key=lambda x:(p[x],x)) for c in cosets}
    check(reps[frozenset(H)]==e,'identity_coset_representative')
    q=max(p[x] for x in reps.values());c=max(p[inv(x)] for x in reps.values())
    T={mul(mul(r,s),inv(reps[coset_of[mul(r,s)]])) for r in reps.values() for s in S}
    td=distances(es,mul,e,T)
    check(set(td)==H,'nonnormal_directed_schreier_generation')
    check(q<=len(cosets)-1,'right_coset_shortest_path')
    check(all(p[t]<=q+1+c for t in T),'right_coset_factor_cost')
    check(max(p.values())<=max(td.values())*(q+1+c)+q,'nonnormal_overgroup_bound')
    # Explicit telescoping for each reconstructed short positive word.
    for target in H:
        queue=deque([(e,())]);visited={e};word=None
        while queue:
            x,w=queue.popleft()
            if x==target:word=w;break
            for s in S:
                y=mul(x,s)
                if y not in visited:visited.add(y);queue.append((y,w+(s,)))
        prefix=e;factorproduct=e
        for s in word:
            old=reps[coset_of[prefix]];prefix=mul(prefix,s)
            new=reps[coset_of[prefix]]
            factorproduct=mul(factorproduct,mul(mul(old,s),inv(new)))
        check(factorproduct==target,'positive_telescoping')

# Representative inverse cost is not bounded by index-1.
es,mul,e,inv=cyclic(10);p=distances(es,mul,e,[1]);
check(p[1]==1 and p[inv(1)]==9 and 9>2-1,'inverse_rep_cost_counterexample')
details['inverse_representative_counterexample']={'group':'C10','subgroup':'even residues','index':2,'q':1,'c':9}

# Genuine nonsplit finite extension: C12, H=even residues, Q=C2.
# Omitting the factor-set constants falsifies the lower comparison.
es,mul,e,inv=cyclic(12);S={10};W={10,1};H=set(range(0,12,2));
s=distances(es,mul,e,S);w=distances(es,mul,e,W);T={10,2};t=distances(es,mul,e,T)
check(s[2]==5 and w[2]==2,'factor_set_omission_counterexample')
check(all(t[x]<=w[x] for x in H),'nonsplit_factor_set_comparison')
check(mul(1,1)==2 and 2!=0,'nonsplit_transversal_square')
details['factor_set_counterexample']={'group':'C12','H':'even residues','S':[10],'l_S(2)':5,'l_W(2)':2,'c(1,1)':2}

# Finite split action: all monoid generators, invariance and saturation.
for n in range(3,11):
    hs,hm,he,hi=cyclic(n);es,mul,e,inv=dihedral(n)
    for S in power_set(tuple(range(1,n))):
        s=distances(hs,hm,he,S)
        if len(s)!=n:continue
        sat=set(S)|{(-x)%n for x in S};sd=distances(hs,hm,he,sat)
        w=distances(es,mul,e,{(x,0) for x in S}|{(0,1)})
        for x in hs:
            check(sd[x]<=w[(x,0)]<=3*sd[x],'split_saturation')
            if set(S)==sat:check(s[x]==w[(x,0)],'split_invariant_equality')

# Exact integer dihedral operation, never reducing modulo n.
def imul(x,y):return (x[0]+(-1)**x[1]*y[0],(x[1]+y[1])%2)
def evaluate(word):
    r=(0,0)
    for a in word:r=imul(r,a)
    return r
for n in range(-1000,1001):
    rot=[] if n==0 else [(n,0)] if n>0 else [(0,1),(-n,0),(0,1)]
    ref=[(n,0),(0,1)] if n>=0 else [(0,1),(-n,0)]
    check(evaluate(rot)==(n,0) and len(rot)<=3,'integer_dihedral_rotation')
    check(evaluate(ref)==(n,1) and len(ref)<=2,'integer_dihedral_reflection')
check(-3 < -2,'integer_dihedral_two_letter_rotation_lower_bound')
details['infinite_dihedral_scope']='Written parity/exponent proof rules out every word of length at most2 for r^-3; finite windows do not prove a global statement.'

# Normal conjugacy invariant metrics independently in S3.
es,mul,e,inv=symmetric3()
classes={frozenset(mul(mul(x,g),inv(x)) for x in es) for g in es if g!=e}
classes=list(classes)
for selection in power_set(tuple(range(len(classes)))):
    S=set().union(*(classes[i] for i in selection));p=distances(es,mul,e,S)
    if len(p)!=len(es):continue
    for x,g in product(es,repeat=2):check(p[mul(mul(x,g),inv(x))]==p[g],'conjugation_length_invariance')
    for F in power_set(tuple(x for x in es if x!=e)):
        U={mul(mul(h,f),inv(h)) for h in es for a in F for f in (a,inv(a))}
        d=distances(es,mul,e,U)
        if len(d)!=len(es):continue
        C=max(p[f] for a in F for f in (a,inv(a)))
        check(max(p.values())<=max(d.values())*C,'finite_normal_generation_cost')

# Independent Cartesian coordinate-padding control on C4 x C5.
es=tuple(product(range(4),range(5)));mul=lambda x,y:((x[0]+y[0])%4,(x[1]+y[1])%5)
for A in ({0,1},{0,3},{0,1,2}):
    for B in ({0,1},{0,2},{0,1,4}):
        a=distances(range(4),lambda x,y:(x+y)%4,0,A);b=distances(range(5),lambda x,y:(x+y)%5,0,B)
        d=distances(es,mul,(0,0),set(product(A,B)))
        for x in es:check(d[x]==max(a[x[0]],b[x[1]]),'cartesian_padding')

# Closed-profinite example projections and direct-sum support controls.
for n in range(1,17):
    check((-1)%(2**n)==2**n-1,'two_adic_residue')
    check(2**n-1>=n,'two_adic_unbounded_residue_lengths')
for n in range(1,15):
    for x in range(1<<n):
        check(sum((x>>j)&1 for j in range(n))==x.bit_count(),'binary_support_length')
    check(((1<<n)-1).bit_count()==n,'support_unbounded_family')

receipt={'assertions':sum(counts.values()),'categories':dict(sorted(counts.items())),'details':details,'author_imports':False,'scope':'Finite inequalities and exact integer controls only. Infinite CB, Baire category, algebraic generation in inverse limits, and the original separation require proofs.'}
out=Path(__file__).with_name('INDEPENDENT_CONTROLS.json')
out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))
