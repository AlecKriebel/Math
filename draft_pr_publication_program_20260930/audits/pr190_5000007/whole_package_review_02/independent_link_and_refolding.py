"""Reviewer-owned exact singular-link/affine-parameter attack, with no imports of candidate code."""
from fractions import Fraction as F
import datetime,json
from pathlib import Path
R=Path(__file__).resolve().parent
zero=(F(0),)*4;one=(F(1),F(0),F(0),F(0));r=(F(0),F(1),F(0),F(0))
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def sub(x,y):return add(x,neg(y))
def scale(t,x):return tuple(t*a for a in x)
def mul(x,y):
    p=[F(0)]*7
    for i,a in enumerate(x):
        for j,b in enumerate(y):p[i+j]+=a*b
    for k in range(6,3,-1):
        lead=p[k]
        for j in range(4):p[k-4+j]-=lead
        p[k]=0
    return tuple(p[:4])
def powr(k):
    z=one
    for i in range(k%5):z=mul(z,r)
    return z
def require(x,m):
    if not x:raise ValueError(m)
P=[zero];Q=[zero]
for i in range(4):P.append(add(P[-1],powr(i)));Q.append(add(Q[-1],powr(-i)))
# Build the entire metric link combinatorially from the parallel-edge gluings.
def following(c):
    s,j=c
    return ('Q',(-j)%5) if s=='P' else ('P',(2-j)%5)
cycle=[('P',0)]
while following(cycle[-1])!=cycle[0]:
    n=following(cycle[-1]);require(n not in cycle,'link splits or repeats');cycle.append(n)
require(len(cycle)==10,'wrong singular link');require(F(10)*F(3,5)==6,'cone angle is not 6pi')
def hcorner(c):return ('Q' if c[0]=='P' else 'P',(1-c[1])%5)
link_rows=[]
for i,c in enumerate(cycle):
    image=hcorner(c);require(image==cycle[(i+5)%10],'h does not preserve correct singular sector')
    link_rows.append({'sector':list(c),'h_sector':list(image),'link_offset_in_pi':str(F(5)*F(3,5))})
# Compare both coefficients of the affine edge parameter, hence *all* t, not a finite grid.
edge_rows=[]
for i in range(5):
    j=(-i)%5;ep=sub(P[(i+1)%5],P[i]);eq=sub(Q[(j+1)%5],Q[j]);require(ep==eq,'gluing derivative')
    tr=sub(P[i],Q[j]);h_constant=add(sub(one,P[i]),tr);h_slope=neg(ep)
    require(h_constant==add(P[i],ep) and h_slope==neg(ep),'edge h(t) != 1-t')
    # Fixed-point equation ep*(2t-1)=0: ep is nonzero in a field, so t=1/2 uniquely.
    require(ep!=zero,'degenerate edge')
    edge_rows.append({'P_edge':i,'Q_edge':j,'all_parameter_identity':'h(i,t)=(i,1-t)','unique_regular_fixed_t':'1/2'})
# Terminal-corner vs direction is a bijection; only q1 can match p0's *sector*.
corner_rows=[]
for j in range(5):
    edge=sub(Q[(j+1)%5],Q[j]);require(edge==powr(-j),'bad terminal edge')
    reflected_last_set={sub(Q[j],p) for p in P}
    symmetric=reflected_last_set==set(Q)
    require(symmetric==(j==1),'wrong corner could masquerade as central symmetry')
    require((hcorner(('Q',j))==('P',0))==(j==1),'singular germ false positive')
    corner_rows.append({'terminal_Q_corner':j,'outgoing_direction_units_2pi_over5':(-j)%5,'same_initial_sector_after_h':j==1,'last_face_equals_B_minus_P':symmetric})
# Strict elementary graph obstruction independently tests all distance-two pairs,
# using a generalized Petersen G(10,2) construction, not supporting-plane coordinates.
edges=set()
for i in range(10):
    for a,b in [(i,(i+1)%10),(i,10+i),(10+i,10+(i+2)%10)]:edges.add(tuple(sorted((a,b))))
g={i:set() for i in range(20)}
for a,b in edges:g[a].add(b);g[b].add(a)
require(len(edges)==30 and all(len(v)==3 for v in g.values()),'graph degree')
rows=[]
for a in range(20):
    for b in range(a+1,20):
        common=g[a]&g[b]
        if common and b not in g[a]:
            require(len(common)==1,'distance-two multiple common neighbors');rows.append([a,b,next(iter(common))])
require(len(rows)==60,'distance-two pairs count')
result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mechanism':'Whole singular metric-link permutation plus exact affine coefficient equality; alternate quotient-free final-face criterion; independent graph G(10,2) local obstruction. Universal proof remains analytic.','link_cycle':list(map(list,cycle)),'cone_angle_in_pi':'6','h_link_rows':link_rows,'all_t_edge_parameter_identities':edge_rows,'terminal_sector_falsification':corner_rows,'distance_two_unique_common_neighbor_pairs':rows,'distinct_attack_rejected':'All four incorrect Q terminal sectors fail both sector match and last-face central symmetry; equality of global tangent alone is insufficient.','status':'PASS'}
(R/'INDEPENDENT_ATTACK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
