"""Fresh exact falsification checks, independent state enumeration."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
import json, random, sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'clean_package/code'))
import gadget as candidate
import sampling as sampler

def matchings(vertices, edges):
    vertices=frozenset(vertices); edges=frozenset(tuple(sorted(e)) for e in edges)
    if not vertices:
        return [()]
    v=min(vertices); answer=[]
    for e in sorted(edges):
        if v in e and set(e)<=vertices:
            for suffix in matchings(vertices-set(e),edges):
                answer.append(tuple(sorted((e,*suffix))))
    return answer

def signature(edges, n):
    return tuple(len(matchings(set(range(n))-set(removed),edges))
                 for removed in [(),(0,1),(0,),(1,)])

def split(arcs,n,s,t):
    left={s:0}; right={t:1}; edges=[]; k=2
    for v in range(n):
        if v not in (s,t):
            left[v]=k;right[v]=k+1;edges.append((k,k+1));k+=2
    for u,v in arcs:edges.append(tuple(sorted((left[u],right[v]))))
    return tuple(edges),k

def paths(arcs,n,s,t):
    counts=[0]*n;counts[s]=1
    for v in range(n):
        for a,b in arcs:
            if a==v:counts[b]+=counts[v]
    return counts[t]

rng=random.Random(3020261007)
generic_dags=0
for n in range(2,7):
    possible=list(combinations(range(n),2))
    for _ in range(60):
        arcs=[e for e in possible if rng.randrange(2)]
        edges,k=split(arcs,n,0,n-1)
        assert signature(edges,k)==(paths(arcs,n,0,n-1),1,0,0)
        generic_dags+=1
# A deliberate cycle invalidates the signature: acyclicity is indispensable.
cycle_edges,cycle_n=split([(0,3),(1,2),(2,1)],4,0,3)
cycle_signature=signature(cycle_edges,cycle_n)
assert cycle_signature==(2,2,0,0)

gadget_checks=0
for w in [*range(1,130),255,256,257]:
    g=candidate.integer_gadget(w)
    assert signature(g.graph.edges,g.graph.order)==(w,1,0,0)
    gadget_checks+=1

fiber_checks=0
matrices=[]
for _ in range(45):
    matrix=[[F(0) for _ in range(4)] for _ in range(4)]
    for i,j in combinations(range(4),2):
        matrix[i][j]=matrix[j][i]=rng.choice([F(0),F(1),F(2)])
    matrices.append(matrix)
for special in [F(1,2),F(2,3),F(1,7)]:
    matrix=[[F(0) if i==j else F(1) for j in range(4)] for i in range(4)]
    matrix[0][1]=matrix[1][0]=special
    matrices.append(matrix)
for matrix in matrices:
    exp=candidate.expand_rational_matrix(matrix)
    original=matchings(range(4),[(i,j) for i,j in combinations(range(4),2) if matrix[i][j]])
    exact={m:F(1) for m in original}
    for m in exact:
        for i,j in m:exact[m]*=matrix[i][j]
    # Deliberately reverse matching edge order before projection.
    fibers=Counter(exp.project(tuple(reversed(m))) for m in matchings(range(exp.graph.order),exp.graph.edges))
    assert set(fibers)==set(exact)
    assert all(fibers[m]==exp.denominator**2*value for m,value in exact.items())
    assert sum(fibers.values())==exp.denominator**2*sum(exact.values(),F(0))
    fiber_checks+=1

def tv(a,b):
    return sum((abs(a.get(m,F(0))-b.get(m,F(0))) for m in a.keys()|b.keys()),F(0))/2

def law_arbitrary_failures(vertices,edges,eta):
    """Integrate arbitrary nonzero failed outputs with successful endpoints."""
    k=len(vertices)//2;cap=k*k;alpha=eta/(4*k) if k else F(0)
    gamma=eta/(4*cap) if cap else F(0)
    b=0
    while k and 2**b*eta<4*cap:b+=1
    grid=2**b
    edges=frozenset(edges)
    @lru_cache(None)
    def recurse(vertices):
        ms=matchings(vertices,edges)
        if not ms:return ()
        if not vertices:return (((),F(1)),)
        u=min(vertices);children=[]
        for e in sorted(edges):
            if u in e and set(e)<=set(vertices):
                rest=tuple(v for v in vertices if v not in e)
                z=len(matchings(rest,edges))
                if z:children.append((e,rest,z))
        if len(children)==1:
            e,rest,_=children[0]
            return tuple((tuple(sorted((e,*m))),p) for m,p in recurse(rest))
        scenarios=[]
        for i,(e,rest,z) in enumerate(children):
            success=z*(1+(alpha if (sum(vertices)+i)%2 else -alpha))
            # Every failure response is legal and finite, including huge numerator/denominator.
            scenarios.append([(success,1-gamma),(F(0),gamma/3),
                              (F(2**4096+i+1),gamma/3),(F(1,2**4096+i+1),gamma/3)])
        out=Counter()
        for pattern in product(*scenarios):
            estimates=[x for x,p in pattern];mass=F(1)
            for x,p in pattern:mass*=p
            total=sum(estimates,F(0))
            if not total:
                out[min(ms)]+=mass;continue
            old=0;cum=F(0)
            for (e,rest,z),value in zip(children,estimates):
                cum+=value;f=grid*cum/total;new=f.numerator//f.denominator
                branch=F(new-old,grid);old=new
                if branch:
                    for m,p in recurse(rest):out[tuple(sorted((e,*m)))]+=mass*branch*p
            assert old==grid
        return tuple(sorted(out.items()))
    return dict(recurse(tuple(vertices))),alpha,gamma,b

sampling_laws=0;maximum=F(0)
graphs=[]
for mask in range(64):graphs.append((4,[e for i,e in enumerate(combinations(range(4),2)) if mask>>i&1]))
graphs.extend((6,[e for e in combinations(range(6),2) if rng.randrange(2)]) for _ in range(20))
for n,edges in graphs:
    eta=F(1,13);ideal=matchings(range(n),edges)
    p={m:F(1,len(ideal)) for m in ideal}
    q,a,g,b=law_arbitrary_failures(range(n),edges,eta)
    assert set(q)<=set(p)
    assert sum(q.values(),F(0))==(1 if p else 0)
    error=tv(q,p); bound=(n//2)*a/(1-a)+(n//2)**2*g+F((n//2)**2,2**b)
    assert error<=bound<eta
    maximum=max(maximum,error);sampling_laws+=1

# Direct sampler checks failed responses' arithmetic, feasibility and caps.
graph=sampler.Graph.make(range(6),combinations(range(6),2))
direct=[]
for failure in [F(0),F(2**8192+13),F(1,2**8192+13)]:
    stats=sampler.Stats()
    result=sampler.sample_perfect_matching(graph,F(1,13),lambda *args:failure,
        sampler.exact_witness,lambda bits:(2**bits)-1,stats)
    assert result in matchings(range(6),graph.edges)
    assert stats.count_calls<=9 and stats.witness_calls<=10 and stats.decisions<=3
    direct.append(vars(stats))

report={'status':'passed','generic_DAGs':generic_dags,'cycle_control_signature':cycle_signature,
        'independent_signatures':gadget_checks,'rational_fiber_instances':fiber_checks,
        'arbitrary_nonzero_failure_laws':sampling_laws,'maximum_exact_TV':str(maximum),
        'direct_failed_tape_checks':direct,'scope':'Finite falsification only; asymptotic claims depend on proofs.'}
(HERE/'INDEPENDENT_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
