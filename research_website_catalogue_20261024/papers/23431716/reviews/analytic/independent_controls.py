"""Fresh exact controls from the seven-page paper, before published helper reading.

Independent mechanisms: exhaustive finite-state transition graphs, direct
enumeration of arborescences, all two-variable normalized CNFs, and physical
one-vertex-at-a-time conservative firing. Standard library only.
"""
from pathlib import Path
from itertools import product, combinations
from collections import deque, Counter
from functools import reduce
from math import gcd, lcm, prod
import datetime, hashlib, json

HERE=Path(__file__).resolve().parent
counts=Counter()
def ck(value,label):
    if not value: raise RuntimeError(label)
    counts[label]+=1

def bank(q,A):
    return [a for a in range(q) for _ in range(1+int((-a-1)%q in A)-int((-a)%q in A))]

for q in range(2,11):
    for mask in range(1,1<<q):
        A={i for i in range(q) if (mask>>i)&1};offsets=bank(q,A)
        K=q*(q-1)//2-len(A);B=K+q
        ck(len(offsets)==q,'bank_count')
        storage=[]
        for k in range(-2*q,2*q+1):
            value=sum((a+k)%q for a in offsets);storage.append(value)
            ck(value==K+q*int(k%q in A),'bank_storage_all_integer_signs')
            if k>=0:
                output=sum((a+k)//q for a in offsets)
                ck(output==k+int(0 in A)-int(k%q in A),'primed_toppler_cumulative')
        ck(max(storage)==B and {k for k in range(q) if sum((a+k)%q for a in offsets)==B}==A,'bank_maximum')
ck(max(sum((a+k)%2 for a in bank(2,set())) for k in range(2)) != 2*1//2+2,'empty_set_negative_control')

def reachable(adj,start):
    seen={start};todo=[start]
    while todo:
        for v in adj[todo.pop()]:
            if v not in seen:seen.add(v);todo.append(v)
    return seen

def construct(banks,oriented):
    P=max(q for q,A in banks);Q=sum(q for q,A in banks)
    offsets=[(q,a) for q,A in banks for a in bank(q,A)]
    n=1+Q+P-(not oriented);returns=list(range(1+Q,n))
    adj=[[] for _ in range(n)];adj[0]=list(range(1,Q+1))
    for v,(q,a) in enumerate(offsets,1):adj[v]=(returns[:q] if oriented else [0]+returns[:q-1])
    for v in returns:adj[v]=[0]
    B=sum(q*(q+1)//2-len(A) for q,A in banks);C=Q+B-1
    state=[C-sum(a for q,a in offsets)]+[a for q,a in offsets]+[0]*len(returns)
    ck(all(u!=v and len(adj[u])==len(set(adj[u])) for u in range(n) for v in adj[u]),'loopless_simple')
    ck(all(len(reachable(adj,u))==n for u in range(n)),'strongly_connected')
    ck(all(not any(w!=0 for w in adj[v]) for u in range(1,n) for v in adj[u] if v!=0),'root_deletion_depth_one')
    if oriented:ck(all(u not in adj[v] for u in range(n) for v in adj[u]),'no_antiparallel')
    ck(n==Q+P+int(oriented) and sum(map(len,adj))==Q+sum(q*q for q,A in banks)+P-1+int(oriented),'graph_size_identities')
    ck(state[0]>=Q-1 and min(state)>=0 and sum(state)==C,'initial_mass')
    return adj,state,offsets,returns,C,B

def fire(adj,state,u):
    ck(state[u]>=len(adj[u]),'legal_firing')
    old=sum(state);state[u]-=len(adj[u])
    for v in adj[u]:state[v]+=1
    ck(sum(state)==old and min(state)>=0,'conservation_every_firing')

def canonical(banks,oriented):
    adj,state,offsets,returns,C,B=construct(banks,oriented)
    Q=len(offsets);period=lcm(*(q for q,A in banks));initial=tuple(state);f=[0]*len(adj)
    for k in range(period+1):
        ck(all(state[v]==(a+k)%q for v,(q,a) in enumerate(offsets,1)) and all(state[v]==0 for v in returns),'physical_checkpoint_residues')
        accept=all(k%q in A for q,A in banks)
        ck((state[0]<Q)==accept,'physical_checkpoint_iff')
        ck(state[0]==C-sum(state[1:]),'checkpoint_mass')
        if accept:
            ck(all(state[v]<len(adj[v]) for v in range(len(adj))),'stable_success')
            return True,k,f,adj,state
        if k==period:
            ck(tuple(state)==initial,'literal_nonhalting_cycle')
            return False,None,f,adj,state
        fire(adj,state,0);f[0]+=1
        for v in range(1,Q+1):
            if state[v]>=len(adj[v]):fire(adj,state,v);f[v]+=1
        for v in returns:
            while state[v]:fire(adj,state,v);f[v]+=1

def sat(clauses,assignment):
    return all(any(assignment[v]==polarity for v,polarity in clause) for clause in clauses)

def formula_banks(clauses):
    used=sorted({v for clause in clauses for v,p in clause});primes=[3,5,7]
    p={v:primes[i] for i,v in enumerate(used)};banks=[(p[v],{0,1}) for v in used]
    for clause in clauses:
        variables=sorted({v for v,polarity in clause});q=prod(p[v] for v in variables)
        # Direct residue scan is an independent control on local CRT mapping.
        A={k for k in range(q) if all(k%p[v] in [0,1] for v in variables) and any(k%p[v]==polarity for v,polarity in clause)}
        ck(len(A)==2**len(variables)-1,'local_clause_size')
        banks.append((q,A))
    return used,p,banks

possible=[((v,pol),) for v in range(2) for pol in (0,1)]+[tuple(zip([0,1],bits)) for bits in product([0,1],repeat=2)]
formulas=[[possible[i] for i in range(8) if mask>>i&1] for mask in range(1,256)]
formulas += [[tuple(zip([0,1,2],bits))] for bits in product([0,1],repeat=3)]
formulas += [[tuple(zip([0,1,2],bits)) for bits in product([0,1],repeat=3)]]
formula_results=[]
for clauses in formulas:
    used,p,banks=formula_banks(clauses)
    expected=any(sat(clauses,dict(zip(used,bits))) for bits in product([0,1],repeat=len(used)))
    M=prod(p.values())
    for k in range(M):
        variable_bad=any(k%p[v] not in [0,1] for v in used)
        failed_local=any(all(k%p[v]==1-pol for v,pol in clause) for clause in clauses)
        ck(all(k%q in A for q,A in banks)==(not(variable_bad or failed_local)),'classical_union_complement')
    vals=[]
    for oriented in (False,True):
        outcome,k,f,adj,z=canonical(banks,oriented)
        ck(outcome==expected,'SAT_physical_equivalence')
        if outcome:ck(max(f,default=0)+1<=(len(adj)-1)**(2*len(adj)-2),'constructed_certificate_bound')
        vals.append({'oriented':oriented,'halts':outcome,'successful_k':k,'vertices':len(adj),'arcs':sum(map(len,adj)),'chips':sum(z)})
    formula_results.append({'clauses':clauses,'results':vals})
print('bank and physical formula controls passed',flush=True)

def compositions(total,n):
    if n==1:yield (total,);return
    for first in range(total+1):
        for rest in compositions(total-first,n-1):yield (first,)+rest

def primitive_tree_period(adj):
    n=len(adj);tau=[]
    for root in range(n):
        other=[u for u in range(n) if u!=root];number=0
        for choices in product(*(adj[u] for u in other)):
            successor=dict(zip(other,choices));ok=True
            for u in other:
                visited=set();v=u
                while v!=root and v not in visited:visited.add(v);v=successor[v]
                if v!=root:ok=False;break
            number+=ok
        tau.append(number)
    divisor=reduce(gcd,tau);period=[v//divisor for v in tau]
    ck(min(period)>0 and max(period)<=(n-1)**(n-1),'tree_period_size')
    ck(all(len(adj[v])*period[v]==sum(period[u] for u in range(n) if v in adj[u]) for v in range(n)),'tree_period_kernel')
    return period

def whole_state_space(adj,C):
    n=len(adj);states=list(compositions(C,n));index={s:i for i,s in enumerate(states)}
    edges=[[] for _ in states];back=[[] for _ in states]
    for i,state in enumerate(states):
        for u in range(n):
            if state[u]>=len(adj[u]):
                nxt=list(state);nxt[u]-=len(adj[u])
                for v in adj[u]:nxt[v]+=1
                j=index[tuple(nxt)];edges[i].append((u,j));back[j].append(i)
    terminals=[i for i,E in enumerate(edges) if not E]
    # Reverse reachability of stability versus iterative removal of dead ends:
    # the survivors are exactly states admitting some infinite legal walk.
    reaches=set(terminals);todo=deque(terminals)
    while todo:
        for j in back[todo.popleft()]:
            if j not in reaches:reaches.add(j);todo.append(j)
    out=[len(E) for E in edges];removed=set(terminals);todo=deque(terminals)
    while todo:
        for j in back[todo.popleft()]:
            out[j]-=1
            if out[j]==0 and j not in removed:removed.add(j);todo.append(j)
    ck(reaches==removed,'all_schedule_halting_no_mixed_behavior')
    for i in reaches:
        current=i;f=[0]*n
        while edges[current]:u,current=edges[current][0];f[u]+=1
        ck(max(f)+1<=(n-1)**(2*n-2),'general_certificate_bound')
        z=states[current];initial=states[i]
        ck(all(z[v]==initial[v]-len(adj[v])*f[v]+sum(f[u] for u in range(n) if v in adj[u]) for v in range(n)),'certificate_balance')
        ck(all(f[u]+1<=len(adj[v])*(f[v]+1) for u in range(n) for v in adj[u]),'additive_one_arc_bound')
        # Explore all legal prefixes with their counts, bounded because this
        # terminal-reachable subgraph is acyclic by the preceding exact test.
        visited=set();stack=[(i,tuple([0]*n))]
        while stack:
            j,g=stack.pop()
            if (j,g) in visited:continue
            visited.add((j,g));ck(all(a<=b for a,b in zip(g,f)),'least_action_all_prefixes')
            for u,k in edges[j]:
                gg=list(g);gg[u]+=1;stack.append((k,tuple(gg)))
    return len(states),len(reaches),sum(map(len,edges))

graphs=0;state_count=0;transition_count=0;haltstates=0
for n in (2,3):
    arcs=[(u,v) for u in range(n) for v in range(n) if u!=v]
    for mask in range(1<<len(arcs)):
        adj=[[] for _ in range(n)]
        for i,(u,v) in enumerate(arcs):
            if mask>>i&1:adj[u].append(v)
        if any(len(reachable(adj,u))!=n for u in range(n)):continue
        graphs+=1;primitive_tree_period(adj)
        for C in range(sum(map(len,adj))-n+2):
            total,halt,trans=whole_state_space(adj,C);state_count+=total;haltstates+=halt;transition_count+=trans
for banks in [[(2,{0})],[(2,{1})],[(2,{0,1})],[(2,{0}),(2,{1})]]:
    for oriented in (False,True):
        adj,state,*rest=construct(banks,oriented)
        whole_state_space(adj,sum(state))

# The cited missing-slack inequality is disproved by an exact one-fire run.
adj=[[1],[0,2],[0]];state=[1,0,0];fire(adj,state,0)
ck(state==[0,1,0] and 1>len(adj[1])*0,'slack_omission_negative_control')
# Two actual conservative mutant games, with exact repeated states. Both
# change a satisfiable bank instance to a nonhalting one.
mutants=[]
for kind,banks in [('root_mass_plus_one',[(2,{0,1})]),('omit_direct_return',[(2,{1})])]:
    adj,state,offsets,returns,C,B=construct(banks,False)
    if kind=='root_mass_plus_one':state[0]+=1
    else:
        for v in range(1,len(offsets)+1):adj[v].remove(0)
    original=tuple(state);seen={};period=None
    for step in range(10):
        if tuple(state) in seen:period=step-seen[tuple(state)];break
        seen[tuple(state)]=step
        ck(state[0]>=len(adj[0]),'mutant_root_remains_legal')
        fire(adj,state,0)
        for v in range(1,len(offsets)+1):
            while state[v]>=len(adj[v]):fire(adj,state,v)
        for v in returns:
            while state[v]:fire(adj,state,v)
    ck(period is not None,kind+'_negative_control')
    mutants.append({'kind':kind,'initial':original,'checkpoint_cycle_period':period,'original_bank_accepts_some_residue':True,'mutant_has_infinite_legal_word':True})
(HERE/'negative-controls.json').write_text(json.dumps(mutants,indent=2)+'\n')
result={'status':'PASS','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'helper_code_read_before_authoring':False,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'assertions':sum(counts.values()),'counts_by_mechanism':dict(counts),
    'bank_moduli_exhausted':[2,10],'nonempty_allowed_sets_exhausted':sum((1<<q)-1 for q in range(2,11)),
    'normalized_formulas':len(formulas),'physical_graphs':2*len(formulas),
    'all_small_strongly_connected_graphs':graphs,'small_graph_states':state_count,
    'small_graph_terminal_reachable_states':haltstates,'small_graph_transitions':transition_count,
    'extra_complete_constructed_state_spaces':8,'universal_claims':'These finite controls corroborate the separate proof; they do not prove arbitrary input correctness.'}
(HERE/'independent-controls.json').write_text(json.dumps(result,indent=2)+'\n')
(HERE/'formula-graph-results.json').write_text(json.dumps(formula_results,indent=2)+'\n')
print(json.dumps(result,indent=2))
