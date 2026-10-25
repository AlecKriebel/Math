"""Independent literal complete-ear and reduction controls; no supplied code.

Finite graphs are diagnostics, not proofs of the reduction for arbitrary input.
--verify-only repeats without writes; default creates one fresh own receipt.
"""
from pathlib import Path
from itertools import combinations
import datetime,json,sys
import sympy as sy
if sys.argv[1:] not in ([],['--verify-only']):raise SystemExit('usage: controls.py [--verify-only]')


def need(ok,msg):
    if not ok:raise RuntimeError(msg)


def verts(E,mask):return set(v for i,e in enumerate(E) if mask>>i&1 for v in e)


def conn(E,S):
    if not S:return False
    seen={next(iter(S))};stack=list(seen)
    while stack:
        v=stack.pop()
        for a,b in E:
            w=b if a==v else a if b==v else None
            if w in S and w not in seen:seen.add(w);stack.append(w)
    return seen==S


def pm(E,S):
    if not S:return []
    if len(S)%2:return None
    v=min(S);others=S-{v}
    for w in sorted(others):
        if tuple(sorted((v,w))) in E:
            rest=pm(E,others-{w})
            if rest is not None:return [(v,w)]+rest
    return None


def two(E,S):return len(S)>=3 and conn(E,S) and all(conn(E,S-{v}) for v in S)


def cycle(E,mask):
    V=verts(E,mask);degree={v:0 for v in V}
    for i,(a,b) in enumerate(E):
        if mask>>i&1:degree[a]+=1;degree[b]+=1
    return bool(V) and all(x==2 for x in degree.values()) and conn([e for i,e in enumerate(E) if mask>>i&1],V)


def new_paths(E,old,used,odd_only):
    adj={v:[] for e in E for v in e}
    for i,(a,b) in enumerate(E):
        if not used>>i&1:adj[a].append((b,i));adj[b].append((a,i))
    def walk(start,v,path,mask):
        for w,i in adj[v]:
            if w in path:continue
            nm=mask|(1<<i)
            if w in old:
                if w!=start and len(path)>1 and (not odd_only or nm.bit_count()%2):yield nm
            else:yield from walk(start,w,path+[w],nm)
    for v in sorted(old):yield from walk(v,v,[v],0)


def validate_complete(E,ears,n):
    need(ears and cycle(E,ears[0]),'initial circuit')
    used=ears[0];old=verts(E,used);prefix=0;still=True
    for j,mask in enumerate(ears):
        if still and mask.bit_count()%2:prefix+=1
        else:still=False
        if j==0:continue
        need(not used&mask,'edge repeated')
        V=verts(E,mask);degrees={v:0 for v in V};es=[e for i,e in enumerate(E) if mask>>i&1]
        for a,b in es:degrees[a]+=1;degrees[b]+=1
        ends={v for v,d in degrees.items() if d==1}
        need(len(ends)==2 and all(d in (1,2) for d in degrees.values()) and conn(es,V)
             and V&old==ends,'invalid open ear')
        used|=mask;old|=V
    need(used==(1<<len(E))-1 and old==set(range(n)),'not complete edge partition')
    return prefix


def literal_beta(n,E):
    allmask=(1<<len(E))-1;stack=[]
    for mask in range(1,allmask+1):
        if mask.bit_count()%2 and cycle(E,mask):stack.append((verts(E,mask),mask,[mask]))
    seen=set();best=[]
    while stack:
        old,used,ears=stack.pop();key=(sum(1<<v for v in old),used)
        if key in seen:continue
        seen.add(key)
        if len(ears)>len(best):best=ears
        for i,(a,b) in enumerate(E):
            if not used>>i&1 and a in old and b in old:stack.append((old,used|(1<<i),ears+[1<<i]))
        for mask in new_paths(E,old,used,True):stack.append((old|verts(E,mask),used|mask,ears+[mask]))
    expected=len(best)
    if not best:
        best=[next(mask for mask in range(1,allmask+1) if cycle(E,mask))]
    # Complete the literal best prefix, then verify the actual full objective.
    ears=list(best);used=0
    for mask in ears:used|=mask
    old=verts(E,used)
    while len(old)<n:
        mask=next(new_paths(E,old,used,False),None);need(mask is not None,'ear completion blocked')
        ears.append(mask);used|=mask;old|=verts(E,mask)
    for i in range(len(E)):
        if not used>>i&1:ears.append(1<<i);used|=1<<i
    need(validate_complete(E,ears,n)==expected,'complete prefix objective changed')
    return expected


def fc_formula(n,E):
    best=0
    for bits in range(1<<n):
        S={i for i in range(n) if bits>>i&1}
        if two(E,S) and all(pm(E,S-{v}) is not None for v in S):
            best=max(best,sum(a in S and b in S for a,b in E)-len(S)+1)
    return best


rows=[]
for n in range(3,6):
    complete=list(combinations(range(n),2))
    for mask in range(1<<len(complete)):
        E=tuple(e for i,e in enumerate(complete) if mask>>i&1)
        if not two(E,set(range(n))):continue
        b=literal_beta(n,E);f=fc_formula(n,E);need(b==f,'literal ears/factor-critical mismatch')
        rows.append({'n':n,'complete_graph_edge_mask':mask,'beta':b,'induced_fc_rank':f})
cone_rows=[]
for a,b in [(1,1),(1,2),(1,3),(2,2)]:
    pairs=[(i,a+j) for i in range(a) for j in range(b)];n=a+b
    for mask in range(1<<len(pairs)):
        E=tuple(e for i,e in enumerate(pairs) if mask>>i&1)
        if not conn(E,set(range(n))):continue
        opt=0
        for bits in range(1<<n):
            S={i for i in range(n) if bits>>i&1}
            if conn(E,S) and pm(E,S) is not None:opt=max(opt,sum(u in S and v in S for u,v in E))
        G=E+tuple((i,n) for i in range(n));beta=literal_beta(n+1,G)
        need(opt==beta,'cone identity mismatch');cone_rows.append({'parts':[a,b],'mask':mask,'objective':opt,'literal_beta':beta})

k,a,b=sy.symbols('k a b')
need(sy.expand(k*(a+b)-a*b-k*(a-b)-b*(2*k-a))==0,'exact partial-block identity')

# Actual full-size witnesses; no exponential optimization of these large graphs.
reduction=[]
for m,sets,budget in [(3,[{0,1},{1,2},{0,2}],2),(2,[set(),{0,1},{0,1}],1),(3,[{0},{1},{2},set()],3)]:
    n=len(sets);T=sum(1+len(A) for A in sets);k=T+n+3;M=(m+1)*k*k;F=M-k*budget
    need(k>T and k>budget and k*k>k*budget+T and F>0,'threshold gaps')
    cover=next(J for r in range(budget+1) for J in combinations(range(n),r) if set().union(*(sets[j] for j in J))==set(range(m)))
    private={j:min(sets[j]-set().union(*(sets[q] for q in cover if q!=j))) for j in cover}
    need(len(set(private.values()))==len(cover),'private elements')
    left=lambda i,p:2*k*i+p
    right=lambda i,p:2*k*i+k+p
    c=lambda j:2*k*(m+1)+j
    E=tuple((left(i,p),right(i,q)) for i in range(m+1) for p in range(k) for q in range(k))
    E+=tuple((right(i,0),c(j)) for j,A in enumerate(sets) for i in [0]+[v+1 for v in sorted(A)])
    E=tuple(tuple(sorted(e)) for e in E);S=set(range(2*k*(m+1)))|{c(j) for j in cover}
    for i in private.values():S.remove(left(i+1,0))
    matching=[(c(j),right(i+1,0)) for j,i in private.items()]
    omitted={i+1 for i in private.values()}
    for i in range(m+1):
        for p in range(1 if i in omitted else 0,k):matching.append((left(i,p),right(i,p)))
    used=[v for e in matching for v in e]
    need(len(used)==len(set(used)) and set(used)==S and all(tuple(sorted(e)) in E for e in matching),'full-size perfect matching')
    count=sum(u in S and v in S for u,v in E)
    need(conn(E,S) and count==M-k*len(cover)+sum(1+len(sets[j]) for j in cover) and count>=F,'full-size forward witness')
    reduction.append({'m':m,'sets':[sorted(A) for A in sets],'budget':budget,'T':T,'k':k,'M':M,'F':F,
                      'B_vertices':2*k*(m+1)+n,'B_edges':len(E),'cover':list(cover),'private':private,
                      'selected_vertices':sorted(S),'matching':matching,'induced_edges':count,'large_beta_optimized':False})

# Connectivity/objective countercontrol, with exact explicit witnesses.
E=tuple((6*i+p,6*i+3+q) for i in range(3) for p in range(3) for q in range(3))+((3,18),(9,18),(3,19),(15,19))
E=tuple(tuple(sorted(e)) for e in E);dis=set(range(18));yes=set(range(20))-{6,12}
need(pm(E,dis) is not None and not conn(E,dis) and sum(u in dis and v in dis for u,v in E)==27,'disconnected27 control')
need(pm(E,yes) is not None and conn(E,yes) and sum(u in yes and v in yes for u,v in E)==25,'connected25 control')
need(literal_beta(3,((0,1),(0,2),(1,2)))==1,'triangle trivial-output control')

out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'EXACT_INDEPENDENT_CONTROLS_COMPLETED',
     'literal_graph_rows':rows,'cone_rows':cone_rows,'full_size_reduction_witnesses':reduction,
     'partial_block_identity_symbolically_verified':True,'connected25_disconnected27_control_verified':True,
     'finite_tests_are_universal_proofs':False,'general_proof':'DERIVATIONS.md','supplied_code_executed':False}
if sys.argv[1:]!=['--verify-only']:
    with (Path(__file__).resolve().parent/'CONTROL_RESULTS.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps({'literal_complete_ear_graphs':len(rows),'connected_bipartite_cones':len(cone_rows),
                  'full_size_witnesses':len(reduction),'status':out['status']}))
