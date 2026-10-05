#!/usr/bin/env python3
"""Independent exact finite controls. No external packages and no asymptotic-proof claim."""
from collections import Counter, defaultdict, deque
from fractions import Fraction as Q
from itertools import product
import hashlib, json

counts=Counter()
def verify(group, statement):
    if not statement:
        raise AssertionError(group)
    counts[group]+=1

def graph_distance(n, bits):
    edges=[(0,1)]; nxt=2; cursor=0
    for _ in range(n):
        new=[]
        for a,b in edges:
            if bits[cursor]:
                new.extend(((a,nxt),(nxt,b))); nxt+=1
            else:
                new.extend(((a,b),(a,b)))
            cursor+=1
        edges=new
    neighbors=[[] for _ in range(nxt)]
    for a,b in edges:
        neighbors[a].append(b); neighbors[b].append(a)
    todo=deque([(0,0)]);seen={0}
    while todo:
        vertex,d=todo.popleft()
        if vertex==1:return d,len(edges)
        for w in neighbors[vertex]:
            if w not in seen: seen.add(w);todo.append((w,d+1))
    raise AssertionError('disconnected')

def gate_tree(bits,leaves):
    vals=list(leaves)
    for level in range(len(leaves).bit_length()-2,-1,-1):
        start=2**level-1
        vals=[vals[2*i]+vals[2*i+1] if bits[start+i] else min(vals[2*i],vals[2*i+1]) for i in range(2**level)]
    return vals[0]

# Integer counts grouped by number of series gates. Equality is for every p.
recursive={(1,0):1}; tree_rows=[]
for n in range(1,5):
    next_counts=Counter()
    for (x,k),cx in recursive.items():
        for (y,l),cy in recursive.items():
            next_counts[(min(x,y),k+l)]+=cx*cy
            next_counts[(x+y,k+l+1)]+=cx*cy
    recursive=next_counts
    graph_counts=Counter();nodes=2**n-1
    for bits in product((0,1),repeat=nodes):
        dist,edges=graph_distance(n,bits)
        verify('graph_edges',edges==2**n)
        verify('graph_vs_gate_tree',dist==gate_tree(bits,[1]*2**n))
        graph_counts[(dist,sum(bits))]+=1
    verify('graph_polynomial_vs_recursive_polynomial',graph_counts==recursive)
    verify('gate_assignment_count',sum(graph_counts.values())==2**nodes)
    serialization=json.dumps([[d,k,c] for (d,k),c in sorted(graph_counts.items())],separators=(',',':')).encode()
    tree_rows.append({'depth':n,'assignments':2**nodes,'distance_gate_count_sha256':hashlib.sha256(serialization).hexdigest()})

# Concavity for every depth-two gate tree on an exhaustive finite vector grid.
vectors=list(product((0,1,2),repeat=4))
for bits in product((0,1),repeat=3):
    for x in vectors:
        for y in vectors:
            verify('gate_concavity_grid',gate_tree(bits,[a+b for a,b in zip(x,y)])>=gate_tree(bits,x)+gate_tree(bits,y))
# Jensen on every depth-three gate tree with independently sampled mean-one 0/2 leaves.
for bits in product((0,1),repeat=7):
    lhs=sum(gate_tree(bits,leaves) for leaves in product((0,2),repeat=8))
    verify('gate_jensen_depth3',lhs<=256*gate_tree(bits,[1]*8))

def moments(law):
    return sum(x*w for x,w in law.items()),sum(x*x*w for x,w in law.items())

def next_law(law,p):
    # Addition by convolution; minimum by squared survival differences.
    out=defaultdict(Q);xs=sorted(law)
    for x in xs:
        for y in xs:out[x+y]+=p*law[x]*law[y]
    tail=Q(1)
    for x in xs:
        after=tail-law[x]
        out[x]+=(1-p)*(tail*tail-after*after)
        tail=after
    return {x:w for x,w in out.items() if w}

def profile_integrals(law):
    # Independent integration over decreasing-quantile steps.
    steps=[];u=Q(0); A=Q(0);C=Q(0)
    for x,w in sorted(law.items(),reverse=True):
        v=u+w
        A+=x*(v*v-u*u);C+=x*x*(v*v-u*u)
        steps.append((u,v,x));u=v
    cross=Q(0)
    for a,b,x in steps:
        for c,d,y in steps:
            integral_uv=(b*b-a*a)/2*(d-c)-(b-a)*(d*d-c*c)/2
            cross+=x*y*(y-x)*integral_uv
    return A,C,cross

params=[Q(1,2),Q(51,100),Q(3,5),Q(3,4),Q(9,10),Q(1)]
profiles=0; invariant_cases=0
for weights in product(range(9),repeat=5):
    if sum(weights)!=8:continue
    law={x:Q(w,8) for x,w in zip([Q(0),Q(1,3),Q(1),Q(2),Q(7)],weights) if w}
    m,s=moments(law)
    if not m:continue
    profiles+=1;A,C,cross=profile_integrals(law)
    verify('anticorrelation_identity',A*s-C*m==cross)
    verify('anticorrelation_sign',cross>=0)
    normal={x/m:w for x,w in law.items()};s0=s/m**2
    for p in params:
        out=next_law(normal,p);d,t=moments(out)
        verify('normalization',sum(out.values())==1)
        verify('mean_formula',d==2*p+(1-p)*A/m)
        verify('second_moment_formula',t==2*p*s0+2*p+(1-p)*C/m**2)
        verify('second_moment_inequality',t/d**2<=(s0+1)/(2*p))
        if p>Q(1,2) and s0<=1/(2*p-1):
            invariant_cases+=1
            verify('invariant_L2_set',t/d**2<=1/(2*p-1))
        for shift in [Q(0),Q(1,7),Q(1),Q(11)]:
            left=t/d**2-(t+2*shift*d+shift**2)/(d+shift)**2
            right=shift*(2*d+shift)*(t-d*d)/(d*d*(d+shift)**2)
            verify('shift_identity',left==right)
            verify('shift_sign',left>=0)

sequences=[]
for p in [Q(0),Q(1,4),Q(1,2),Q(51,100),Q(3,5),Q(3,4),Q(9,10),Q(1)]:
    law={Q(1):Q(1)};means=[Q(1)]
    for n in range(1,8):
        law=next_law(law,p);m,s=moments(law);means.append(m)
        verify('depth7_mass',sum(law.values())==1)
        verify('depth7_bounds',(2*p)**n<=m<=(1+p)**n)
        if p>Q(1,2):verify('depth7_L2_bound',s/m**2<=1/(2*p-1))
    for n in range(1,8):
        for k in range(1,8-n):verify('block_submultiplicativity',means[n+k]<=means[n]*means[k])
    verify('depth2_mean_polynomial',means[2]==1+p+3*p*p-p**3)
    sequences.append({'p':str(p),'m7':str(means[7])})

negative=[]
def reject(name, witness, check):
    verify('negative_controls',check)
    negative.append({'name':name,'witness':witness,'rejected':True})
p=Q(3,4); unit={Q(1):Q(1)};split={Q(1,2):Q(1,2),Q(3,2):Q(1,2)}
u=next_law(unit,p);v=next_law(split,p)
reject('mean-only closure','p=3/4: means 1 and 1; output means 7/4 and 27/16',moments(u)[0]==Q(7,4) and moments(v)[0]==Q(27,16))
reject('reverse block inequality','p=3/4: m1^2-m2=3/64',moments(u)[0]**2-moments(next_law(u,p))[0]==Q(3,64))
reject('reciprocal L2 cap','p=3/4, X=1: normalized second moment 1 exceeds 2p-1=1/2',Q(1)>2*p-1)
reject('constant eigenfunction','T(1) has distinct outputs 1 and 2, each with positive mass',len(u)==2)
reject('maximum in place of minimum','X uniform on {0,2}: E min=1/2; E max=3/2',sum(Q(1,4)*min(x,y) for x,y in product((0,2),repeat=2))==Q(1,2))
reject('resistance substituted for distance','parallel unit edges: distance=1, resistance=1/2',Q(1)!=Q(1,2))
reject('critical compactness from mean alone','f_n=n on (0,1/n), else 0: mean=1, second moment=n; f_n ->0 a.e.',all(n*n*Q(1,n)==n and n*Q(1,n)==1 for n in (2,4,8,16)))
reject('pointwise-mean perturbation loses homogeneity','T(f)+epsilon*1 on the cone fails scaling: c=2, epsilon=1',Q(2)*Q(1)!=Q(1))
reject('dropping decreasing hypothesis in anticorrelation sign','f(u)=2u has A=4/3,S=4/3,C=2,M=1, giving AS-CM=-2/9',Q(4,3)*Q(4,3)-2==-Q(2,9))
reject('missing sum cross term','p=3/4 and X=1: actual second moment 13/4; omitting the 2p*M^2 term gives 7/4',moments(u)[1]==Q(13,4) and moments(u)[1]-(2*p+(1-p))==Q(3,2))

result={'status':'PASS','arithmetic':'exact fractions and integer combinatorial counts','assertions':sum(counts.values()),'assertions_by_group':dict(sorted(counts.items())),'literal_graph_controls':tree_rows,'weighted_step_profiles':profiles,'invariant_set_instances':invariant_cases,'recursive_depth':7,'parameters':[str(x) for x in params],'sequence_samples':sequences,'negative_controls':negative,'scope':'Finite controls and explicit counterexamples only. Analytic compactness, fixed points, maximality, and limits are reviewed separately.'}
print(json.dumps(result,indent=2,sort_keys=True))
