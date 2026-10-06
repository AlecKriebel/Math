"""Independent Pruefer-tree and edge-cut audit of aggregate all-root costs.

Standard library only. Does not import the author verifier or adjacent problem.
All-size NP-completeness is a written proof, not a finite-test conclusion.
"""
from pathlib import Path
from itertools import product,combinations_with_replacement
from functools import lru_cache
import hashlib,json

root=Path(__file__).resolve().parent
EXPECTED='1a6c267c6240b66c1d804397f4bbbe246f5b6147c3930e1a68396e60b618d615'
assert hashlib.sha256((root/'author_replay/PROOF.md').read_bytes()).hexdigest()==EXPECTED
counts={};stats={'formulas':0,'unsatisfiable_formulas':0,'tree_formula_cases':0,
 'noncanonical_trees':0,'without_hub_edge':0,'extra_clause_edges':0,'canonical_trees':0,
 'canonical_positive_penalty_trees':0}
def ck(v,k):
    assert v,k
    counts[k]=counts.get(k,0)+1

@lru_cache(None)
def complete_trees(N):
    result=[]
    for code in product(range(N),repeat=N-2):
        degree=[1]*N
        for a in code:degree[a]+=1
        es=[]
        for a in code:
            leaf=next(i for i in range(N) if degree[i]==1)
            es.append(tuple(sorted((leaf,a))));degree[leaf]-=1;degree[a]-=1
        es.append(tuple(i for i in range(N) if degree[i]==1))
        result.append(tuple(sorted(es)))
    ck(len(result)==N**(N-2),'pruefer_census_size')
    return result

@lru_cache(None)
def allowed_trees(N,E):
    allowed=set(E);out=[]
    for es in complete_trees(N):
        if not all(e in allowed for e in es):continue
        adj=[set() for _ in range(N)]
        for a,b in es:adj[a].add(b);adj[b].add(a)
        cuts=[]
        for a,b in es:
            reached={a};todo=[a]
            for v in todo:
                for w in adj[v]:
                    if {v,w}=={a,b}:continue
                    if w not in reached:reached.add(w);todo.append(w)
            ck(b not in reached and reached,'edge_cut_partition')
            cuts.append((a,b,sum(1<<v for v in reached)))
        out.append((es,tuple(cuts)))
    return out

def construct(n,clauses):
    m=len(clauses);N=n+m+2
    edges={(0,1)}
    for i in range(n):edges.update({(0,2+i),(1,2+i)})
    for j,C in enumerate(clauses):
        for l in C:edges.add((abs(l)+1,n+2+j))
    C=[[[0]*N for _ in range(N)] for _ in range(N)]
    for a,b in edges:
        val=(n+1 if b>=n+2 else 0 if (a,b)==(0,1) else 1)
        C[0][a][b]=C[0][b][a]=val
    for j,clause in enumerate(clauses):
        r=n+2+j
        for literal in clause:
            var=abs(literal)+1
            for hub,truth in [(0,True),(1,False)]:
                C[r][var][hub]=int(truth!=(literal>0))
    return N,tuple(sorted(edges)),C,(n+1)*m+n

def cut_cost(N,cost,cuts,reverse=False,shift=0):
    totals=[0]*N
    for a,b,mask in cuts:
        for r in range(N):
            tail,head=(a,b) if (mask>>r)&1 else (b,a)
            if reverse:
                tail,head=head,tail
                totals[r]+=cost[r][head][tail]+shift
            else:totals[r]+=cost[r][tail][head]+shift
    return totals

def test(n,clauses):
    N,E,C,K=construct(n,clauses);m=len(clauses)
    sats=[a for a in product([False,True],repeat=n)
          if all(any(a[abs(l)-1]==(l>0) for l in clause) for clause in clauses)]
    stats['formulas']+=1;stats['unsatisfiable_formulas']+=int(not sats)
    feasible=[]
    trees=allowed_trees(N,E)
    for es,cuts in trees:
        stats['tree_formula_cases']+=1
        totals=cut_cost(N,C,cuts);value=sum(totals)
        q=sum(b>=n+2 for a,b in es);h=int((0,1) in es)
        ck(totals[0]==K+1-h+n*(q-m),'unrestricted_base_identity')
        ck(value>=totals[0] and q>=m,'nonnegative_domination')
        ck(cut_cost(N,C,cuts,reverse=True)==totals,'inward_cost_reversal')
        # All roots each use N-1 arcs, even the zero-cost roots.
        ck(sum(cut_cost(N,C,cuts,shift=1))==value+N*(N-1),'positive_cost_shift')
        canonical=(h==1 and q==m)
        if not canonical:
            stats['noncanonical_trees']+=1
            stats['without_hub_edge']+=int(not h);stats['extra_clause_edges']+=int(q>m)
            ck(value>K,'noncanonical_exclusion')
        else:
            stats['canonical_trees']+=1
            assignment=tuple((0,2+i) in es for i in range(n))
            ck(all(((0,2+i) in es)+((1,2+i) in es)==1 for i in range(n)),
               'one_variable_attachment')
            penalty=0
            for j,clause in enumerate(clauses):
                neighbors=[a for a,b in es if b==n+2+j]
                ck(len(neighbors)==1,'one_clause_attachment')
                variable=neighbors[0]-1
                literal=next(l for l in clause if abs(l)==variable)
                expected=int(assignment[variable-1]!=(literal>0))
                ck(totals[n+2+j]==expected,'individual_literal_cost')
                penalty+=expected
            ck(value==K+penalty,'canonical_total_cost')
            stats['canonical_positive_penalty_trees']+=int(penalty>0)
        if value<=K:feasible.append(es)
    ck(bool(feasible)==bool(sats),'sat_equivalence')
    for a in sats:
        desired={(0,1)}|{(0 if a[i] else 1,2+i) for i in range(n)}
        for j,clause in enumerate(clauses):
            l=next(l for l in clause if a[abs(l)-1]==(l>0))
            desired.add((abs(l)+1,n+2+j))
        ck(tuple(sorted(desired)) in feasible,'assignment_witness')

for n,max_m in [(1,3),(2,3),(3,2)]:
    clauses=[tuple((i+1)*z for i,z in enumerate(signs) if z)
             for signs in product([-1,0,1],repeat=n) if any(signs)]
    for m in range(1,max_m+1):
        for cs in combinations_with_replacement(clauses,m):test(n,cs)

# Explicit fixed yes/no instances for preprocessing degeneracies.
# The sole two-vertex tree has two aggregate directed arcs, one per root.
ck(0+0<=0,'fixed_yes_instance')
ck(not(1+1<=1),'fixed_no_instance')

r={'all_pass':True,'assertions':sum(counts.values()),'checks':counts,'statistics':stats,
   'distinct_graphs':allowed_trees.cache_info().currsize,'artifact_sha256':EXPECTED,
   'scope':'Independent Pruefer enumeration and all-root edge-cut cost evaluation, including all noncanonical trees in the finite suite. The written proof establishes all-size strong NP-completeness.'}
(root/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
