"""Exact controls for the final-turn local-forest bridge and entropy certificate.
All tree/graph enumeration and rational interval code is authored here.
"""
from itertools import product,combinations
from collections import Counter,defaultdict,deque
from fractions import Fraction as F
from math import factorial,comb,prod
import json
ct=Counter()
def ck(v,key):
    assert v,key
    ct[key]+=1
def falling(n,j):return prod(range(n-j+1,n+1))
def decode(k,word):
    deg=[1]*k
    for v in word:deg[v]+=1
    adj=[[] for _ in range(k)]
    for v in word:
        u=next(x for x in range(k) if deg[x]==1)
        adj[u].append(v);adj[v].append(u);deg[u]-=1;deg[v]-=1
    u,v=[x for x in range(k) if deg[x]==1];adj[u].append(v);adj[v].append(u)
    return adj

def root_shape(adj,v,parent,depth,cap,forbidden=frozenset()):
    if depth==cap:return ()
    return tuple(sorted(root_shape(adj,w,v,depth+1,cap,forbidden) for w in adj[v] if w!=parent and tuple(sorted((v,w))) not in forbidden))
def stats(tree,depth,cap):
    v=1;I=int(depth<cap);aut=1
    for child in tree:
        w,J,A=stats(child,depth+1,cap);v+=w;I+=J;aut*=A
    for mult in Counter(tree).values():aut*=factorial(mult)
    return v,I,aut
forest_cases=0;tree_count=0
for k in range(3,8):
    alltrees=[decode(k,w) for w in product(range(k),repeat=k-2)];tree_count+=len(alltrees)
    for D in range(1,min(3,k-2)+1):
        forbidden=frozenset((i,i+1) for i in range(D))
        conditional=[adj for adj in alltrees if all(i+1 in adj[i] for i in range(D))]
        denominator=(D+1)*k**(k-D-2)
        ck(len(conditional)==denominator,'full_path_extension_count')
        rootsets=[(0,),tuple(sorted({0,D}))]
        if D>=2:rootsets.append(tuple(range(1,D)))
        for roots in rootsets:
            for cap in [1,2]:
                hist=Counter(tuple(root_shape(adj,v,-1,0,cap,forbidden) for v in roots) for adj in conditional)
                for shapes,num in hist.items():
                    vs=I=0;aut=1
                    for shape in shapes:
                        v,J,A=stats(shape,0,cap);vs+=v;I+=J;aut*=A
                    j=vs-len(roots);V=D+1+j;b=V-I
                    if V==k:extensions=1
                    else:extensions=b*(k-I)**(k-V-1)
                    expected=F(falling(k-D-1,j)*extensions,aut*denominator)
                    ck(F(num,denominator)==expected,'exact_selected_root_forest_law')
                    forest_cases+=1
# Exact null simultaneous exploration probability, ignoring root-root edges.
def explore(n,edges,mask,roots,cap):
    adj=[[] for _ in range(n)]
    for i,(u,v) in enumerate(edges):
        if mask>>i&1:adj[u].append(v);adj[v].append(u)
    roots=set(roots);parent={r:None for r in roots};depth={r:0 for r in roots};children=defaultdict(list);todo=deque(sorted(roots))
    while todo:
        v=todo.popleft()
        if depth[v]>=cap:continue
        for w in adj[v]:
            if v in roots and w in roots:continue
            if w not in depth:
                depth[w]=depth[v]+1;parent[w]=v;children[v].append(w);todo.append(w)
            elif parent[v]!=w and parent[w]!=v:return None
    def code(v):return tuple(sorted(code(w) for w in children[v]))
    return tuple(code(r) for r in sorted(roots))
null_graphs=0
for n in range(3,6):
    edges=list(combinations(range(n),2));p=F(1,3)
    for roots in [(0,),(0,1)]:
        for cap in [1,2]:
            hist=defaultdict(F)
            for mask in range(1<<len(edges)):
                shape=explore(n,edges,mask,roots,cap);null_graphs+=1
                if shape is None:continue
                e=mask.bit_count();hist[shape]+=p**e*(1-p)**(len(edges)-e)
            for shapes,prob in hist.items():
                vs=I=0;aut=1
                for sh in shapes:
                    v,J,A=stats(sh,0,cap);vs+=v;I+=J;aut*=A
                r=len(roots);j=vs-r
                absent=I*n-I*(I+1)//2-comb(r,2)-j
                expected=F(falling(n-r,j),aut)*p**j*(1-p)**absent
                ck(prob==expected,'exact_null_exploration_law')
# Exact exp/log intervals. Alternating tails after 61 terms have decreasing magnitudes.
def expneg_interval(x,m=61):
    low=sum(((-x)**j/F(factorial(j)) for j in range(m+1)),F(0))
    assert m%2==1 and F(x,m+2)<1
    high=low+x**(m+1)/factorial(m+1)
    return low,high

def log_unit_interval(x,m=24):
    assert 1<=x<=2
    u=(x-1)/(x+1)
    low=2*sum((u**(2*j+1)/F(2*j+1) for j in range(m)),F(0))
    high=low+2*u**(2*m+1)/((2*m+1)*(1-u*u))
    return low,high

def log_interval(x):
    assert x>=1
    power=0
    while x>=2:x/=2;power+=1
    lo,hi=log_unit_interval(x);l2,u2=log_unit_interval(F(2))
    return lo+power*l2,hi+power*u2
c=F(3,2);e1,_=expneg_interval(F(1));ec,_=expneg_interval(c)
scaled_terms=[];lower=F(-1);scale=10**12
for m in range(10):
    r=e1*F(5,3)**m
    loglo,_=log_interval(1+r/c)
    term=ec*c**m/factorial(m)*(c+r)*loglo
    floor=term.numerator*scale//term.denominator
    ck(F(floor,scale)<=term,'rational_entropy_term_rounddown')
    scaled_terms.append(floor);lower+=F(floor,scale)
_,logcupper=log_interval(c)
ceil_logc=(logcupper.numerator*scale+logcupper.denominator-1)//logcupper.denominator
ck(F(ceil_logc,scale)>=logcupper,'rational_logc_roundup')
gap=lower-F(ceil_logc,scale)
ck(gap>F(1,500),'depth_two_entropy_exceeds_log_c')
# The depth-one criterion fails here, so this is a genuinely richer statistic.
_,log53upper=log_interval(F(5,3));log32lower,_=log_interval(F(3,2))
ck(F(5,2)*log53upper-1-log32lower<0,'depth_one_criterion_fails_at_three_halves')
# Exact positivity and monotone-exploration regime algebra at finite values.
for k in range(100,401,25):
    for D in range(10,min(k//3,40)):
        for I in range(1,6):
            for j in range(I,2*I+1):
                b=D+1+j-I
                ck(b>0 and k-I>0 and k-D-j-2>=0,'forest_bridge_legal_factors')
print(json.dumps({'status':'PASS','exact_assertions':sum(ct.values()),'counts':dict(sorted(ct.items())),'labelled_trees_enumerated':tree_count,'conditional_forest_shape_cases':forest_cases,'null_graph_experiments':null_graphs,'entropy_certificate':{'c':'3/2','offspring_terms_included':'m=0,...,9; all omitted terms nonnegative','scale':scale,'certified_lower_term_numerators':scaled_terms,'certified_upper_log_3_over_2_numerator':ceil_logc,'certified_gap_numerator':gap.numerator,'certified_gap_denominator':gap.denominator,'gap_strictly_above':'1/500','exp_alternating_order':61,'log_atanh_terms_after_power_of_two_reduction':24},'scope':'Exact finite Cayley and null-exploration laws plus a rational finite entropy certificate. Uniform growing-window bridges and the original-model detector are proved in TURN_5.md; no converse or sharp mean-degree transition is claimed.'},indent=2,sort_keys=True))
