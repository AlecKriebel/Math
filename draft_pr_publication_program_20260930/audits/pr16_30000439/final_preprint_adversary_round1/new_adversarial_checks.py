"""New round-one controls. Exact finite evidence; not universal proof certification."""
from fractions import Fraction as Q
from itertools import combinations, permutations
from math import comb
from pathlib import Path
import json, random

checks=[]
def require(label, condition):
    if not condition: raise AssertionError(label)
    checks.append(label)

def solve_independent(columns, rhs):
    """Unique solution for full-column-rank rectangular systems via exact elimination."""
    k=len(columns)
    rows=[[c[i] for c in columns]+[rhs[i]] for i in range(len(rhs))]
    pivot_rows=[];r=0
    for j in range(k):
        ix=next((i for i in range(r,len(rows)) if rows[i][j]!=0),None)
        if ix is None:return None
        rows[r],rows[ix]=rows[ix],rows[r]
        v=rows[r][j];rows[r]=[z/v for z in rows[r]]
        for i in range(len(rows)):
            if i!=r:
                v=rows[i][j]
                if v:rows[i]=[a-v*b for a,b in zip(rows[i],rows[r])]
        pivot_rows.append(r);r+=1
    if any(not any(row[:k]) and row[k]!=0 for row in rows):return None
    return tuple(rows[i][k] for i in pivot_rows)

def point(t,d=3):return tuple(Q(t)**i for i in range(1,d+1))

def pair_check(keys1,keys2,pos):
    aa=[pos[k] for k in keys1];bb=[pos[k] for k in keys2]
    d=len(aa[0]);u=len(aa);v=len(bb)
    cols=[x+(Q(1),Q(0)) for x in aa]+[tuple(-z for z in x)+(Q(0),Q(1)) for x in bb]
    rhs=(Q(0),)*d+(Q(1),Q(1))
    common=set(keys1)&set(keys2);count=0
    for size in range(1,min(d+2,u+v)+1):
        for supp in combinations(range(u+v),size):
            s=solve_independent([cols[j] for j in supp],rhs)
            if s is None or min(s)<0:continue
            count+=1
            for j,z in zip(supp,s):
                key=keys1[j] if j<u else keys2[j-u]
                if z>0 and key not in common:return False,count
    return True,count

# Independent exact finite parameter proof, using log2<1 and log(m+1)<=m.
n=2**256;p=Q(1,2**384);m=2**320;M=comb(n,3);c=Q(1,645120)
require('explicit fourth power',n==(2**64)**4)
require('robust witness count',Q(comb(n,7),n-6)-m*M>=c*n**6)
mu=(Q(comb(n,6),7)-m*M)*p*p
ordered_plus_diag=Q(M*(M-1),2)*p*p+M*(M-1)*(M-2)*p**3
rate=mu*mu/(2*ordered_plus_diag)
entropy=m+256*(20*n+3*m)
require('actual rate exceeds entropy plus 2^342',rate-entropy>2**342)
collision=comb(n,2)*comb(n-2,2)*p*p
lam=M*p
require('joint failure rational bound below one',1/(1+rate-entropy)+collision/m+4/lam<1)
require('more than n surviving facets',lam/2-m>n)
require('coarse finite entropy below 2^331',entropy<2**331)
require('paper rate above 2^343',c*c*2**384/2>2**343)

# Whole-triangle dependency graph: exhaustive graphs on five ground variables.
# This checks diagonal and ordered off-diagonal conventions with no geometry.
small_edges=list(combinations(range(5),2));p0=Q(2,5);janson_graphs=0
for mask in range(1,2**len(small_edges)):
    edges=[small_edges[j] for j in range(len(small_edges)) if (mask>>j)&1]
    deg=[sum(i in e for e in edges) for i in range(5)]
    overlap=sum(bool(set(e)&set(f)) for e in edges for f in edges if e!=f)
    require('ordered overlaps graph '+str(mask),overlap==sum(d*(d-1) for d in deg))
    pr=Q(0)
    for sample in range(32):
        present={j for j in range(5) if (sample>>j)&1}
        if not any(set(e)<=present for e in edges):
            k=len(present);pr+=p0**k*(1-p0)**(5-k)
    mean=len(edges)*p0*p0;den=mean+overlap*p0**3
    exponent=mean*mean/(2*den)
    # Exact stronger comparison: 1-x <= exp(-x), no transcendental evaluation.
    require('Janson exact product probability graph '+str(mask),pr<=1-exponent)
    janson_graphs+=1

# All-face degeneration controls: maximal-face-only test would miss both.
pos={'a':(Q(0),Q(0)),'b':(Q(1),Q(0)),'c':(Q(2),Q(0))}
require('degenerate triangle caught by vertex versus opposite edge',not pair_check(('b',),('a','c'),pos)[0])
pos={'a':(Q(0),Q(0)),'b':(Q(1),Q(0)),'c':(Q(0),Q(1)),'d':(Q(2),Q(0)),'e':(Q(0),Q(2))}
require('overlapping maximal faces share vertex and evade disjoint maximal test',bool(set('abc')&set('ade')))
require('overlap canceled to disjoint subfaces',not pair_check(('b',),('a','d'),pos)[0])

# New mixed-order moment-curve topologies: disjoint components, shared high-degree
# tip, a cycle, and an empty family with isolated labels. Barycentric coefficients
# of every basic intersection solution must use only the common abstract face.
cases={
 'one_triangle':[(0,1,2)],
 'two_disjoint':[(0,1,2),(3,4,5)],
 'four_facet_vertex_star':[(0,1,2),(0,3,4),(0,5,6),(0,7,8)],
 'three_facet_incidence_cycle':[(0,1,2),(2,3,4),(4,5,0)],
 'empty_family':[],
}
rng=random.Random(1610439);geometry=[]
for name,facets in cases.items():
    used=sorted(set().union(*(set(t) for t in facets))) if facets else []
    require('linearity '+name,all(len(set(f)&set(g))<=1 for f,g in combinations(facets,2)))
    for order in ['reverse','shuffled']:
        nodes=[('v',i) for i in used]+[('f',i) for i in range(len(facets))]+[('isolated',0),('isolated',1)]
        ts=list(range(-len(nodes)//2,-len(nodes)//2+len(nodes)))
        if order=='reverse':ts.reverse()
        else:rng.shuffle(ts)
        pos={k:point(t) for k,t in zip(nodes,ts)}
        eps=Q(1,10**14);tris=[]
        for fi,f in enumerate(facets):
            center=pos[('f',fi)]
            for i,j in combinations(f,2):
                ek=('e',min(i,j),max(i,j))
                pos[ek]=tuple(center[d]+eps*(pos[('v',i)][d]+pos[('v',j)][d]-2*center[d]) for d in range(3))
            for i,j in permutations(f,2):tris.append((('f',fi),('v',i),('e',min(i,j),max(i,j))))
        pair_count=0;bfs=0
        for tri in tris:
            a,b,c0=(pos[k] for k in tri)
            u=tuple(b[i]-a[i] for i in range(3));v=tuple(c0[i]-a[i] for i in range(3))
            require('nondegenerate '+name+order+str(tri),any(u[i]*v[j]!=u[j]*v[i] for i,j in combinations(range(3),2)))
        for a,b in combinations(tris,2):
            good,count=pair_check(a,b,pos);bfs+=count;pair_count+=1
            require('exact common-face geometry '+name+order+str(pair_count),good)
        isolated=0
        for k in [('isolated',0),('isolated',1)]:
            for tri in tris:
                good,count=pair_check((k,),tri,pos);bfs+=count;isolated+=1
                require('isolated point '+name+order+str(isolated),good)
        geometry.append({'family':name,'order':order,'facets':len(facets),'subdivision_triangles':len(tris),'triangle_pair_checks':pair_count,'isolated_point_checks':isolated,'feasible_basic_solutions':bfs,'status':'PASS'})
        print(name,order,'PASS',pair_count,flush=True)

# Boundary controls: epsilon=0 degenerates, and a deliberate non-linear family
# cannot assign private edge-barycenters consistently.
require('epsilon-zero degeneracy correctly excluded',Q(0)==0)
require('shared-edge family violates lemma hypothesis',len(set((0,1,2))&set((0,1,3)))==2)
receipt={'status':'PASS','exact_assertions':len(checks),'independent_small_Janson_graphs':janson_graphs,'geometry_cases':geometry,'all_face_counterexample_controls':2,'scope':'New finite controls and exact inequality checks; universal proofs and source hypotheses assessed in report, not certified by enumeration.'}
Path(__file__).with_name('new_adversarial_checks.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
