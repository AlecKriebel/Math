"""New finite diagnostics written for this edition, independent of old programs."""
from collections import deque
from itertools import product, combinations
from math import gcd
from common import require

def bank(q, allowed):
    require(type(q) is int and q >= 2, 'bad modulus')
    require(allowed and all(type(a) is int and 0 <= a < q for a in allowed),
            'empty or invalid allowed set')
    h = lambda k: int(k % q in allowed)
    offsets = []
    multiplicities = []
    for a in range(q):
        c = 1+h(-a-1)-h(-a)
        multiplicities.append(c)
        offsets.extend([a]*c)
    require(len(offsets) == q, 'counter count')
    return offsets, multiplicities

def normalize(formula):
    require(isinstance(formula, (list,tuple)), 'formula encoding')
    result = []
    for clause in formula:
        require(isinstance(clause, (list,tuple)) and len(clause) <= 3,
                'clause encoding')
        require(all(type(v) is int and v != 0 for v in clause), 'literal encoding')
        c = set(clause)
        if not c:
            return None
        if any(-v in c for v in c):
            continue
        result.append(tuple(sorted(c)))
    labels = sorted({abs(v) for c in result for v in c})
    mapping = {v:i+1 for i,v in enumerate(labels)}
    return [tuple(mapping[abs(v)]*(1 if v>0 else -1) for v in c) for c in result]

def truth(formula):
    if formula is None:
        return False
    n = max((abs(v) for c in formula for v in c),default=0)
    return any(all(any(bool(bits[abs(v)-1]) == (v>0) for v in c)
                   for c in formula) for bits in product((0,1),repeat=n))

def predicates(formula):
    n = max(abs(v) for c in formula for v in c)
    primes = []
    candidate = 3
    while len(primes) < n:
        if all(candidate%d for d in range(2,int(candidate**0.5)+1)):
            primes.append(candidate)
        candidate += 1
    result = [(p,{0,1}) for p in primes]
    for c in formula:
        indices = sorted({abs(v)-1 for v in c})
        q = 1
        for i in indices:
            q *= primes[i]
        # Independent residue scan; no imported CRT solver or prior code.
        allowed = {k for k in range(q)
                   if all(k%primes[i] in (0,1) for i in indices)
                   and any(bool(k%primes[abs(v)-1]) == (v>0) for v in c)}
        require(len(allowed) == 2**len(indices)-1, 'clause size')
        result.append((q,allowed))
    return primes, result

def make_graph(pred, oriented):
    counters = [(q,a) for q,A in pred for a in bank(q,A)[0]]
    Q = len(counters)
    P = max(q for q,A in pred)
    count_returns = P if oriented else P-1
    n = 1+Q+count_returns
    edges = [[] for _ in range(n)]
    edges[0] = list(range(1,Q+1))
    for v,(q,a) in enumerate(counters,1):
        edges[v] = ([] if oriented else [0])+list(range(Q+1,Q+1+q-(0 if oriented else 1)))
    for t in range(Q+1,n):
        edges[t] = [0]
    B = sum(q*(q-1)//2-len(A)+q for q,A in pred)
    x = [0]+[a for q,a in counters]+[0]*count_returns
    x[0] = Q+B-1-sum(x)
    require(x[0] >= 0, 'initial root nonnegative')
    return edges, x, counters, B

def validate_graph(edges, oriented=False):
    n = len(edges)
    require(n >= 2 and all(edges), 'positive degrees')
    for v,targets in enumerate(edges):
        require(len(targets) == len(set(targets)) and v not in targets,
                'simple loopless graph')
        require(all(0 <= u < n for u in targets), 'target range')
        if oriented:
            require(all(v not in edges[u] for u in targets), 'opposite arc')
    for start in range(n):
        reached = {start}
        queue = [start]
        for v in queue:
            for u in edges[v]:
                if u not in reached:
                    reached.add(u); queue.append(u)
        require(len(reached) == n, 'strong connectivity')

def fire(edges,x,v):
    require(x[v] >= len(edges[v]), 'illegal firing')
    y = list(x)
    y[v] -= len(edges[v])
    for u in edges[v]:
        y[u] += 1
    require(min(y) >= 0 and sum(y) == sum(x), 'physical conservation')
    return y

def canonical(pred, oriented):
    edges,x,counters,B = make_graph(pred,oriented)
    validate_graph(edges,oriented)
    Q = len(counters); P=max(q for q,A in pred)
    require(len(edges) == Q+P+int(oriented), 'vertex count')
    require(sum(map(len,edges)) == Q+sum(q*q for q,A in pred)+P-1+int(oriented), 'arc count')
    require(all(not any(u != 0 and edges[u] != [0] for u in edges[v])
                for v in range(1,len(edges))), 'root-deleted depth')
    mass=sum(x); seen=set(); counts=[0]*len(x); steps=0; k=0
    while True:
        require(x[1:Q+1] == [(a+k)%q for q,a in counters], 'counter checkpoint')
        require(not any(x[Q+1:]), 'empty return checkpoint')
        storage=sum(x[1:Q+1])
        require(x[0] == Q+B-1-storage, 'root mass')
        accepts=all(k%q in A for q,A in pred)
        require((x[0] < Q) == accepts == (storage == B), 'root predicate threshold')
        state=tuple(x)
        if x[0] < Q:
            return True,edges,x,counts,steps,k
        if state in seen:
            return False,edges,x,counts,steps,k
        seen.add(state)
        x=fire(edges,x,0); counts[0]+=1;steps+=1
        for v in range(1,Q+1):
            if x[v] >= len(edges[v]):
                x=fire(edges,x,v);counts[v]+=1;steps+=1
        for t in range(Q+1,len(edges)):
            while x[t]:
                x=fire(edges,x,t);counts[t]+=1;steps+=1
        require(sum(x)==mass,'mass at checkpoint')
        k+=1
        require(k <= 1000, 'diagnostic period budget exceeded')

def successor_graph(edges,initial):
    start=tuple(initial); todo=deque([start]); visited={start}; stable=[]; words={start:[0]*len(edges)}
    transitions=0
    while todo:
        x=todo.popleft()
        legal=[v for v in range(len(edges)) if x[v]>=len(edges[v])]
        if not legal:
            stable.append((x,words[x]))
        for v in legal:
            y=tuple(fire(edges,x,v));transitions+=1
            if y not in visited:
                visited.add(y);todo.append(y)
                f=words[x].copy();f[v]+=1;words[y]=f
    return visited,stable,words,transitions

def period_trees(edges):
    n=len(edges); trees=[]
    for root in range(n):
        vertices=[v for v in range(n) if v!=root]; total=0
        for choices in product(*(edges[v] for v in vertices)):
            successor=dict(zip(vertices,choices)); good=True
            for v in vertices:
                seen=set();u=v
                while u!=root and u not in seen:
                    seen.add(u);u=successor[u]
                if u!=root:
                    good=False;break
            total+=int(good)
        trees.append(total)
    require(all(trees),'positive tree counts')
    divisor=0
    for t in trees:divisor=gcd(divisor,t)
    pi=[t//divisor for t in trees]
    for v in range(n):
        require(len(edges[v])*pi[v] == sum(pi[u] for u in range(n) if v in edges[u]),'period kernel orientation')
    return pi

def reject(test):
    try:test()
    except (ValueError,TypeError,IndexError):return 1
    raise ValueError('deliberately damaged control was accepted')

def schedule(edges, initial, highest=False, dissipate_returns_from=None):
    x=list(initial);seen=set();steps=0
    while tuple(x) not in seen:
        seen.add(tuple(x))
        legal=[v for v in range(len(edges)) if x[v]>=len(edges[v])]
        if not legal:return True,steps,sum(initial)-sum(x)
        v=legal[-1] if highest else legal[0]
        if dissipate_returns_from is not None and v>=dissipate_returns_from:
            x[v]-=len(edges[v])
        else:x=fire(edges,x,v)
        steps+=1
        require(steps<=50000,'arbitrary schedule diagnostic budget')
    return False,steps,sum(initial)-sum(x)

def run():
    results={'bank_sets':0,'bank_positions':0,'HLW_priming_positions':0,
             'CRT_formulas':0,'CRT_positions':0,'local_nonBoolean_distinctions':0,
             'main_oriented_graphs':0,'legal_firings':0,'root_firings':0,
             'generic_graphs':0,'generic_configurations':0,'generic_states':0,
             'generic_legal_edges':0,'halting_certificates':0,'faults_rejected':0}
    for q in range(2,9):
        for mask in range(1,1<<q):
            A={a for a in range(q) if mask>>a&1}; offsets,c=bank(q,A)
            results['bank_sets']+=1
            K=q*(q-1)//2-len(A)
            for k in range(-q,2*q+1):
                actual=sum((a+k)%q for a in offsets)
                require(actual == K+q*int(k%q in A),'storage identity')
                results['bank_positions']+=1
                if k>=0:
                    F=k+int(0 in A)-int(k%q in A)
                    require(sum((a+k)//q for a in offsets) == F, 'literal HLW substitution')
                    results['HLW_priming_positions']+=1
    pool=[(1,),(-1,),(2,),(-2,),(1,2),(-1,-2)]
    formulas=[[c for i,c in enumerate(pool) if bits>>i&1]
              for bits in range(1<<len(pool))]
    formulas.extend([[(1,2,3)],[(-1,-2,-3)],[(1,),(-1,),(1,2,3)],
                     [(1,1),(-2,2),(2,3,-1)]])
    for original in formulas:
        formula=normalize(original)
        if not formula:continue
        primes,pred=predicates(formula); period=1
        for p in primes:period*=p
        found=False
        results['CRT_formulas']+=1
        for k in range(period):
            good=all(k%q in A for q,A in pred)
            invalid=any(k%p not in (0,1) for p in primes)
            failed=False
            for c in formula:
                indices={abs(v)-1 for v in c}
                is_boolean=all(k%primes[i] in (0,1) for i in indices)
                falsifies=is_boolean and all(bool(k%primes[abs(v)-1]) != (v>0) for v in c)
                failed |= falsifies
                if not is_boolean:results['local_nonBoolean_distinctions']+=1
            require(good == (not (invalid or failed)), 'classical bad union complement')
            found |=good;results['CRT_positions']+=1
        require(found == truth(formula),'CRT SAT existence')
        for oriented in (False,True):
            outcome,edges,x,f,steps,k=canonical(pred,oriented)
            require(outcome == truth(formula),'SAT halting outcome')
            results['main_oriented_graphs']+=1
            results['legal_firings']+=steps;results['root_firings']+=k
    # All loopless strongly connected graphs on two or three labeled vertices.
    for n in (2,3):
        pairs=[(u,v) for u in range(n) for v in range(n) if u!=v]
        for mask in range(1<<len(pairs)):
            edges=[[] for _ in range(n)]
            for i,(u,v) in enumerate(pairs):
                if mask>>i&1:edges[u].append(v)
            try:validate_graph(edges)
            except ValueError:continue
            results['generic_graphs']+=1; pi=period_trees(edges)
            require(max(pi)<=(n-1)**(n-1),'tree bound')
            for x in product(range(3),repeat=n):
                if sum(x)>2:continue
                visited,stable,words,transitions=successor_graph(edges,x)
                results['generic_configurations']+=1;results['generic_states']+=len(visited)
                results['generic_legal_edges']+=transitions
                if stable:
                    require(len(stable)==1,'stable uniqueness')
                    z,f=stable[0];results['halting_certificates']+=1
                    require(any(f[v]<pi[v] for v in range(n)),'period subtraction')
                    for g in words.values():require(all(g[v]<=f[v] for v in range(n)),'least action all explored words')
                    for u in range(n):
                        require(f[u]+1 <= (n-1)**(2*n-2),'certificate bound')
                        for v in edges[u]:require(f[u]+1<=len(edges[v])*(f[v]+1),'correct additive edge slack')
    results['faults_rejected']+=reject(lambda:bank(3,set()))
    results['faults_rejected']+=reject(lambda:normalize([(0,)]))
    results['faults_rejected']+=reject(lambda:normalize('bad'))
    results['faults_rejected']+=reject(lambda:validate_graph([[1,1],[0]]))
    results['faults_rejected']+=reject(lambda:validate_graph([[1],[0]],True))
    offsets,c=bank(3,{0})
    results['faults_rejected']+=reject(lambda:require(sum(offsets)==3*2//2-1,'missing bank phase'))
    results['faults_rejected']+=reject(lambda:require(1<=2*0,'omitted certificate slack'))
    edges,x,counters,B=make_graph([(3,{0}),(3,{1})],False)
    old=sum(x);y=fire(edges,x,0)
    results['faults_rejected']+=reject(lambda:require(sum(y)-1==old,'dissipative mass fault'))
    results['noncanonical_schedules']=0
    results['semantic_outcome_faults']=0
    for oriented in (False,True):
        for pred,expected in (([(3,{0})],True), ([(3,{0}),(3,{1})],False)):
            edges,x,counters,B=make_graph(pred,oriented)
            for highest in (False,True):
                outcome,steps,lost=schedule(edges,x,highest)
                require(outcome==expected and not lost,'noncanonical ordinary outcome')
                results['noncanonical_schedules']+=1
                results['legal_firings']+=steps
            if expected:
                damaged=x.copy();damaged[0]+=1
                outcome,steps,lost=schedule(edges,damaged)
                require(not outcome and not lost,'extra root chip must change YES outcome')
            else:
                outcome,steps,lost=schedule(edges,x,dissipate_returns_from=1+len(counters))
                require(outcome and lost>0,'dissipative returns must change NO outcome')
            results['semantic_outcome_faults']+=1
    # Fixed cases and lexical-variable normalization do not require a SAT oracle.
    for oriented in (False,True):
        edges=[[1],[2],[0]] if oriented else [[1],[0]]
        zeros=[0]*len(edges)
        _,stable,_,_=successor_graph(edges,zeros)
        require(bool(stable),'fixed YES')
        zeros[0]=1
        _,stable,_,_=successor_graph(edges,zeros)
        require(not stable,'fixed NO')
    require(normalize([(10**1000,),(-7,7)]) == [(1,)],'large variable relabel/tautology')
    require(normalize([()]) is None and normalize([])==[],'trivial preprocessing')
    results['status']='PASS'
    results['limitations']='Finite controls supplement the proof; no literature or unbounded theorem certification and no replay of omitted historical programs.'
    return results
