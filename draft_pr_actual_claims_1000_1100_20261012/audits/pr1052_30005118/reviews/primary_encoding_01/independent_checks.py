from itertools import combinations, combinations_with_replacement, product

def sums(A,n=None):
    return frozenset((a+b if n is None else (a+b)%n) for a in A for b in A)

def subsets(xs):
    xs=tuple(xs)
    for mask in range(1<<len(xs)):
        yield frozenset(x for i,x in enumerate(xs) if mask>>i&1)

def integer_yes(S):
    if not S:return True
    lo,hi=min(S),max(S)
    if lo%2 or hi%2:return False
    return any(sums(A)==S for A in subsets(range(lo//2,hi//2+1)))

def transfer(S,restricted=False):
    if not S:return 3,frozenset({0}) if restricted else frozenset()
    t=min(S)
    if t%2:return 5,frozenset({0,1})
    B=frozenset(s-t for s in S)
    return max(3,2*max(B)+1),B

def test_transfer():
    counts={'zero_anchor_targets':0,'cyclic_roots_examined':0,'total_source_inputs':0}
    for n in range(1,16,2):
        rooted={}
        for A in subsets(range(n)):
            B=sums(A,n)
            rooted.setdefault(B,[]).append(A)
            counts['cyclic_roots_examined']+=1
        for M in range((n-1)//2+1):
            for B in subsets(range(M+1)):
                if 0 not in B:continue
                assert integer_yes(B)==(B in rooted),(n,M,B)
                for A in rooted.get(B,[]):
                    assert 0 in A and A<=B and sums(A)==B,(n,M,A,B)
                counts['zero_anchor_targets']+=1
    cyc_cache={}
    for S in subsets(range(-3,7)):
        n,B=transfer(S)
        if n not in cyc_cache:cyc_cache[n]={sums(A,n) for A in subsets(range(n))}
        assert integer_yes(S)==(B in cyc_cache[n]),(S,n,B)
        nr,Br=transfer(S,True)
        assert nr%2 and 0 in Br and all(2*b<nr for b in Br)
        if nr not in cyc_cache:cyc_cache[nr]={sums(A,nr) for A in subsets(range(nr))}
        assert integer_yes(S)==(Br in cyc_cache[nr]),(S,nr,Br)
        counts['total_source_inputs']+=1
    assert not integer_yes(frozenset({1})) and sums({3},5)=={1}
    assert sums({2},4)=={0} and 0 not in {2}
    return counts

def test_skeleton():
    j=tuple(5**i for i in range(5))
    a,u,s=(5**i for i in range(5,8))
    Ip={a,u,s-a,s-u}
    exceptions={2*a,2*s-2*a,2*s-2*u,s}
    E=sorted(sums(Ip)-exceptions)
    assert len(E)==5
    Ipp={4*5**8}
    for e,je in zip(E,j):Ipp.update({e-je,je})
    I=Ip|Ipp
    reps={z:sum(x+y==z for x in I for y in I) for z in exceptions}
    assert reps=={2*a:1,2*s-2*a:1,2*s-2*u:1,s:4}
    assert set(E)<=sums(Ipp)
    assert Ip.isdisjoint(Ipp) and min(I)>=0 and max(I)<=2**21
    assert (I-{4*5**8})<=set(range(5**8+1))
    return {'a':a,'u':u,'s':s,'I_size':len(I),'max_I':max(I),'representation_counts':reps,'primitive_reason':'I=J union {4*5^8}, J subset [0,5^8]; apply independently checked interval proof of Lemma 3.2.'}

def prime_at_least(n):
    if n<=2:return 3
    p=n
    while any(p%d==0 for d in range(2,int(p**.5)+1)):p+=1
    return p

def sidon_points(k):
    if k==1:return [0]
    p=prime_at_least(k)
    # First k graph points, rather than all p, retain the printed 4k^2 bound.
    vals=[2*p*x+(x*x)%p for x in range(k)]
    assert len(sums(vals))==k*(k+1)//2
    assert max(vals)<=4*k*k
    return vals

def sat_gadget(v,clauses):
    c=len(clauses);N=16*(v+c)**2
    vals=sidon_points(v+c)
    ss=[4*x for x in vals[:v]]
    ts=[4*x+64*(v+c)**2 for x in vals[v:]]
    Cs=[{t-ss[i]-(sign==1) for i,sign in clause} for t,clause in zip(ts,clauses)]
    U=set().union(*(set([s,s+1]) for s in ss),*Cs)
    X=set(ts);Y=set()
    for i,s in enumerate(ss):Y.update({2*s,2*s+2})
    for i,s in enumerate(ss):
        for j,t in enumerate(ss):
            if i!=j:Y.update({s+t,s+t+1,s+t+2})
        for C in Cs:Y.update(s+bit+x for bit in (0,1) for x in C)
    for C in Cs:
        for D in Cs:Y.update(x+y for x in C for y in D)
    assert max(U|X|Y)<=160*(v+c)**2 and min(U|X|Y)>=0
    assert all(2*s+1 not in Y for s in ss)
    for t,clause in zip(ts,clauses):
        allowed={(ss[i]+(sign==1),t-ss[i]-(sign==1)) for i,sign in clause}
        allowed|={(b,a) for a,b in tuple(allowed)}
        assert {(a,b) for a in U for b in U if a+b==t}<=allowed
    feasible=any(X<=sums(A)<=Y for A in subsets(U))
    satisfiable=any(all(any(bits[i]==(sign==1) for i,sign in C) for C in clauses) for bits in product((0,1),repeat=v))
    assert feasible==satisfiable,(v,clauses)
    return len(U)

def test_sat():
    allclauses=list(combinations_with_replacement([(i,s) for i in range(2) for s in (-1,1)],3))
    count=0;maxU=0
    for size in (1,2):
        for cs in combinations_with_replacement(allclauses,size):
            maxU=max(maxU,sat_gadget(2,cs));count+=1
    for k in range(1,101):sidon_points(k)
    return {'formulas':count,'variables':2,'clause_counts':[1,2],'allows_repeated_literals':True,'max_U_size':maxU,'sidon_sizes_checked':100}

if __name__=='__main__':
    import json
    result={'transfer':test_transfer(),'source_skeleton':test_skeleton(),'source_sat_gadget':test_sat()}
    print(json.dumps(result,indent=2))
