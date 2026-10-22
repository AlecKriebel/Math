#!/usr/bin/env python3
"""Independent exact truth-table controls; finite evidence, not a universal proof."""
import argparse
from collections import Counter
from itertools import product
from pathlib import Path
from fractions import Fraction
import datetime
import hashlib
import json
import sys
import time

class VerificationError(RuntimeError):
    pass

def require(condition, message):
    if not condition:
        raise VerificationError(message)

def mobius(values, n):
    c=list(values)
    for i in range(n):
        for x in range(1 << n):
            if x & (1 << i):
                c[x] -= c[x ^ (1 << i)]
    return c

def degree(values, n):
    return max((x.bit_count() for x,c in enumerate(mobius(values,n)) if c), default=-1)

def restrict(values, n, fixed_mask, answers):
    free=[i for i in range(n) if not fixed_mask >> i & 1]
    table=[]
    for y in range(1 << len(free)):
        x=answers
        for j,i in enumerate(free):
            x |= ((y >> j) & 1) << i
        table.append(values[x])
    return table,free

def submasks(mask):
    s=mask
    while True:
        yield s
        if not s:
            return
        s=(s-1) & mask

def validate_hitting_reduction(values, n, family):
    k=degree(values,n)
    c=mobius(values,n)
    top=[x for x,a in enumerate(c) if a and x.bit_count()==k]
    seen=0
    for m in family:
        require(m in top and not (seen&m), 'family must be disjoint top monomials')
        seen |= m
    require(all(m&seen for m in top), 'family is not inclusion-maximal')
    for answer in submasks(seen):
        restricted,free=restrict(values,n,seen,answer)
        require(degree(restricted,len(free))<k, 'degree did not decrease')
    return seen

def exhaustive_monomial_controls():
    counts=Counter()
    for n in range(1,4):
        N=1<<n
        for values in product((-1,0,1),repeat=N):
            counts['truth_tables']+=1
            c=mobius(values,n)
            k=max((x.bit_count() for x,a in enumerate(c) if a),default=-1)
            if k<1:
                continue
            top=[x for x,a in enumerate(c) if a and x.bit_count()==k]
            for m in top:
                outside=(N-1)^m
                for a in submasks(outside):
                    r,free=restrict(values,n,outside,a)
                    require(mobius(r,len(free))[-1]==c[m], 'top coefficient changed')
                    counts['coefficient_survival_instances']+=1
                for z in range(N):
                    if values[z]==0:
                        require(any(e and values[z^e] for e in submasks(m)), 'no nonempty flip')
                        counts['nonempty_block_instances']+=1
            for choices in range(1,1<<len(top)):
                family=[m for j,m in enumerate(top) if choices>>j&1]
                union=0
                disjoint=True
                for m in family:
                    if union&m:
                        disjoint=False
                        break
                    union |= m
                if disjoint and all(m&union for m in top):
                    validate_hitting_reduction(values,n,family)
                    counts['maximal_family_instances']+=1
                    counts['answer_restrictions']+=1<<union.bit_count()
    return dict(counts)

def optimal_tree(labels,n):
    """Independent minimax recursion over support labels: 0=free,1=p,2=q."""
    memo={}
    def solve(remaining,answers):
        key=(remaining,answers)
        if key in memo:
            return memo[key]
        present={labels[x] for x in range(1<<n) if (x & ~remaining)==answers}-{0}
        if len(present)<2:
            value=next(iter(present)) if present else 0
            out=(0,('leaf',value))
        else:
            candidates=[]
            for i in range(n):
                bit=1<<i
                if remaining&bit:
                    d0,t0=solve(remaining^bit,answers)
                    d1,t1=solve(remaining^bit,answers|bit)
                    candidates.append((1+max(d0,d1),('query',i,t0,t1)))
            out=min(candidates,key=lambda z:z[0])
        memo[key]=out
        return out
    return solve((1<<n)-1,0)

def verify_tree(tree,labels,n):
    depth=0
    for x,target in enumerate(labels):
        node=tree
        seen=set()
        while node[0]=='query':
            _,i,t0,t1=node
            require(i not in seen and 0<=i<n,'repeated or invalid query')
            seen.add(i)
            node=t1 if x>>i&1 else t0
        require(node[0]=='leaf','invalid leaf')
        require(target==0 or node[1]==target,'wrong support label')
        depth=max(depth,len(seen))
    return depth

def walsh(values,n):
    w=list(values)
    stride=1
    while stride<len(w):
        for start in range(0,len(w),2*stride):
            for j in range(stride):
                a,b=w[start+j],w[start+j+stride]
                w[start+j],w[start+j+stride]=a+b,a-b
        stride*=2
    return w

def relative_max(values,n):
    w=walsh(values,n)
    denominator=sum(a*a for a in w)
    require(denominator>0,'normalization of zero polynomial')
    numerator=max((sum(a*a for x,a in enumerate(w) if x>>i&1) for i in range(n)),default=0)
    return Fraction(numerator,denominator)

def exhaustive_pairs():
    counts=Counter()
    minimum={}
    cache={}
    options=((0,0),(1,0),(-1,0),(0,1),(0,-1))
    for n in range(0,4):
        N=1<<n
        for pairs in product(options,repeat=N):
            p=tuple(a for a,b in pairs)
            q=tuple(b for a,b in pairs)
            labels=tuple(1 if a else 2 if b else 0 for a,b in pairs)
            key=(n,labels)
            if key not in cache:
                dep,tree=optimal_tree(labels,n)
                require(verify_tree(tree,labels,n)==dep,'depth mismatch')
                cache[key]=(dep,tree)
                counts['distinct_support_labelings']+=1
                counts['common_zero_labelings']+=int(0 in labels)
            dep,_=cache[key]
            counts['signed_disjoint_pairs']+=1
            if not any(p) or not any(q):
                require(dep==0,'zero polynomial did not terminate')
                continue
            counts['both_nonzero_pairs']+=1
            d=max(degree(p,n),degree(q,n))
            require(d>=1,'nonzero constant disjoint companion')
            require(dep<=min(n,16*d**4),'separator depth violation')
            delta=max(relative_max(p,n),relative_max(q,n))
            require(delta>=Fraction(1,1024*d**8),'strong influence bound violation')
            minimum[d]=min(minimum.get(d,delta),delta)
            counts['max_optimal_depth']=max(counts['max_optimal_depth'],dep)
    return {'counts':dict(counts),'min_delta_by_degree':{str(k):str(v) for k,v in sorted(minimum.items())}}

def bernoulli_controls():
    counts=Counter()
    for b in range(0,4):
        N=1<<b
        unit={1<<i for i in range(b)}
        domains=[(1,) if x==0 else (-1,0) if x in unit else (-1,0,1) for x in range(N)]
        for values in product(*domains):
            c=mobius(values,b)
            m=degree(values,b)
            coeff=[sum(a for x,a in enumerate(c) if x.bit_count()==k) for k in range(b+1)]
            derivative=coeff[1] if b else 0
            require(derivative==sum(values[1<<i]-values[0] for i in range(b)),'wrong derivative identity')
            require(b<=abs(derivative)<=2*m*m,'Markov endpoint control')
            for t in (Fraction(0),Fraction(1,7),Fraction(1,2),Fraction(6,7),Fraction(1)):
                moment=sum(Fraction(a)*t**k for k,a in enumerate(coeff))
                expectation=sum(Fraction(v)*t**x.bit_count()*(1-t)**(b-x.bit_count()) for x,v in enumerate(values))
                require(moment==expectation and abs(moment)<=1,'Bernoulli expectation mismatch')
                counts['rational_moment_instances']+=1
            counts['bounded_ternary_functions']+=1
    sharp=(1,0,0,-1)
    require(degree(sharp,2)==1 and 2==2*degree(sharp,2)**2,'sharp affine fixture')
    counts['sharp_factor_two_fixtures']=1
    return dict(counts)

def mutation_controls():
    rejected=[]
    def reject(name,fn):
        try:
            fn()
        except VerificationError:
            rejected.append(name)
        else:
            raise VerificationError('wrong-result guard accepted '+name)
    reject('omitted_Markov_factor_two',lambda: require(2<=degree((1,0,0,-1),2)**2,'factor two lost'))
    reject('nonmaximal_family',lambda:validate_hitting_reduction((0,1,1,2),2,[1]))
    def wrong_survival():
        # q=x1(1-x2); lower monomial x1 cancels after x2=1.
        r,free=restrict((0,1,0,0),2,2,2)
        require(mobius(r,1)[1]==1,'non-top monomial does not survive')
    reject('lower_degree_monomial_survival',wrong_survival)
    reject('wrong_total_separator',lambda:verify_tree(('leaf',0),(1,0,2,0),2))
    reject('repeated_coordinate',lambda:verify_tree(('query',0,('query',0,('leaf',1),('leaf',1)),('leaf',2)),(1,2),1))
    # A maximal matching need not be a maximum matching: all top edges hit {2,3}.
    q=tuple(((x&3)==3)+((x&12)==12)+((x&6)==6) for x in range(16))
    require(validate_hitting_reduction(q,4,[6])==6,'maximal nonmaximum fixture rejected')
    # Coefficient magnitude and signs: use exact large/small rational scaling.
    for scale in (Fraction(1,10**80),Fraction(-10**80),Fraction(7,13)):
        values=tuple(scale*x for x in q)
        require(degree(values,4)==2,'scaling changed degree')
        validate_hitting_reduction(values,4,[6])
    return {'rejected':rejected,'maximal_nonmaximum_example_passed':True,'arbitrary_rational_scaling_fixtures':3}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    started=time.monotonic()
    result={'status':'PASS','method':'exact integer/rational truth tables and independent minimax support-label trees','limits':'All ternary functions n<=3; all pointwise disjoint signed ternary pairs n<=3. This is finite evidence only.','monomial':exhaustive_monomial_controls(),'pairs':exhaustive_pairs(),'bernoulli':bernoulli_controls(),'mutation_guards':mutation_controls()}
    result['runtime']={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.monotonic()-started,'python':sys.version,'optimization':sys.flags.optimize,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(args.output).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':
    main()
