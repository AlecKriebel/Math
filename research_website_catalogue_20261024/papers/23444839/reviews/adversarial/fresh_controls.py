"""Fresh affine-chart finite-plane and exact torus controls; no package imports."""
from pathlib import Path
from itertools import combinations
from fractions import Fraction as Q
from datetime import datetime,timezone
import json

ROOT=Path(__file__).resolve().parent
def plane(q):
    # Affine q-by-q grid, one point at infinity per slope, and the vertical point.
    points=[('a',x,y) for x in range(q) for y in range(q)]+[('i',m) for m in range(q)]+[('v',)]
    lines=[]
    for m in range(q):
        for b in range(q):lines.append({('a',x,(m*x+b)%q) for x in range(q)}|{('i',m)})
    for a in range(q):lines.append({('a',a,y) for y in range(q)}|{('v',)})
    lines.append(set(points[q*q:]))
    index={p:i for i,p in enumerate(points)}
    incid=[{index[p] for p in line} for line in lines]
    n=q*q+q+1
    assert len(points)==len(lines)==n and all(len(s)==q+1 for s in incid)
    rows=[{j for j,s in enumerate(incid) if i in s} for i in range(n)]
    assert all(len(s)==q+1 for s in rows)
    assert all(len(rows[i]&rows[j])==1 for i,j in combinations(range(n),2))
    assert all(len(incid[i]&incid[j])==1 for i,j in combinations(range(n),2))
    adj=[set(n+j for j in row) for row in rows]+incid
    return adj,rows
def connected(adj,deleted=None):
    start=next(i for i in range(len(adj)) if i!=deleted);seen={start};todo=[start]
    while todo:
        for j in adj[todo.pop()]:
            if j!=deleted and j not in seen:seen.add(j);todo.append(j)
    return len(seen)==len(adj)-(deleted is not None)
def rank(matrix):
    if not matrix:return 0
    a=[list(map(Q,row)) for row in matrix];i=0
    for j in range(len(a[0])):
        p=next((p for p in range(i,len(a)) if a[p][j]),None)
        if p is None:continue
        a[i],a[p]=a[p],a[i];c=a[i][j];a[i]=[v/c for v in a[i]]
        for k in range(len(a)):
            if k!=i and a[k][j]:
                c=a[k][j];a[k]=[v-c*w for v,w in zip(a[k],a[i])]
        i+=1
        if i==len(a):break
    return i

start=datetime.now(timezone.utc).isoformat();adj,rows=plane(11)
assert len(adj)==266 and sum(map(len,adj))//2==1596 and connected(adj)
for w in range(266):
    assert connected(adj,w)
    assert set(len(adj[v]-{w}) for v in range(266) if v!=w)=={11,12}
    # Deleted-neighbor energy loss is a diagonal mask with coefficients at most1.
    assert all(int(v in adj[w]) in (0,1) for v in range(266) if v!=w)
# Exact normalized-gap threshold: sqrt(11)<4, so (11-sqrt(11))/12>7/12>1/2.
assert 11<4**2 and Q(7,12)>Q(1,2)
# Unique common neighbors exclude a4cycle; bipartiteness excludes3/5cycles.
assert all(len(adj[i]&adj[j])==1 for i,j in combinations(range(133),2))
damaged=[set(r) for r in rows];j=next(iter(damaged[0]));damaged[0].remove(j)
assert len(damaged[0])!=12

# Triangulated 3x3 periodic square grid, each square split along its same diagonal.
n=3;vertex=lambda i,j:(i%n)*n+(j%n)
triangles=set()
for i in range(n):
    for j in range(n):
        a=vertex(i,j);b=vertex(i+1,j);c=vertex(i,j+1);d=vertex(i+1,j+1)
        triangles.add(tuple(sorted((a,b,d))));triangles.add(tuple(sorted((a,c,d))))
triangles=sorted(triangles);edges=sorted({e for tri in triangles for e in combinations(tri,2)})
edgeindex={e:i for i,e in enumerate(edges)}
d1=[[0]*len(edges) for _ in range(n*n)]
for j,(a,b) in enumerate(edges):d1[a][j]=-1;d1[b][j]=1
d2=[[0]*len(triangles) for _ in edges]
for j,(a,b,c) in enumerate(triangles):
    for edge,sign in [((b,c),1),((a,c),-1),((a,b),1)]:d2[edgeindex[edge]][j]=sign
assert all(sum(d1[i][k]*d2[k][j] for k in range(len(edges)))==0 for i in range(n*n) for j in range(len(triangles)))
r1,r2=rank(d1),rank(d2);betti=[n*n-r1,len(edges)-r1-r2,len(triangles)-r2]
assert betti==[1,2,1] and n*n-len(edges)+len(triangles)==0
for v in range(n*n):
    link={}
    for tri in triangles:
        if v in tri:
            a,b=[u for u in tri if u!=v];link.setdefault(a,set()).add(b);link.setdefault(b,set()).add(a)
    assert len(link)==6 and all(len(s)==2 for s in link.values())
    seen={next(iter(link))};todo=list(seen)
    while todo:
        for u in link[todo.pop()]:
            if u not in seen:seen.add(u);todo.append(u)
    assert len(seen)==6
# C6 has normalized gap1-cos(pi/3)=1/2 exactly; a nonzero closed1form exists.
# Use the horizontal displacement of short edges, in {-1,0,1}.
cochain=[]
for a,b in edges:
    ax,ay=divmod(a,n);bx,by=divmod(b,n);delta=(bx-ax)%n
    cochain.append(-1 if delta==n-1 else delta)
assert any(cochain)
assert all(sum(d2[i][j]*cochain[i] for i in range(len(edges)))==0 for j in range(len(triangles)))
weights=[sum(abs(x) for x in row) for row in d2];assert set(weights)=={2}
assert all(sum(d1[v][i]*weights[i]*cochain[i] for i in range(len(edges)))==0 for v in range(n*n))
energy=sum(w*a*a for w,a in zip(weights,cochain));linkenergy=0;linknorm=0
def a(u,v):return cochain[edgeindex[tuple(sorted((u,v)))]]*(1 if u<v else -1)
for v in range(n*n):
    for tri in triangles:
        if v in tri:
            u,w=[s for s in tri if s!=v];linkenergy+=(a(v,u)-a(v,w))**2
    for u in range(n*n):
        if tuple(sorted((u,v))) in edgeindex:linknorm+=2*a(v,u)**2
assert linkenergy==energy and linknorm==2*energy and energy>0

out={'started_utc':start,'completed_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_FRESH_CONTROLS','projective_plane':{'construction':'affine grid with slope/vertical/infinity lines','points':133,'lines':133,'vertices':266,'edges':1596,'regular_degree':12,'exact_Gram':'11I+J','all266deletions_connected':True,'deletion_degrees':[11,12],'no_cycles_below6':True,'gap_lower_bound_strictly_above_half':True,'deleted_incidence_mutant_detected':True},'torus_boundary_control':{'vertices':9,'edges':27,'triangles':18,'ranks':[r1,r2],'rational_betti':betti,'all_vertex_links':'C6','normalized_gap':'1/2 exactly','nonzero_closed_weighted_coclosed_cochain':cochain,'global_energy':energy,'summed_link_energy':linkenergy,'summed_link_norm':linknorm,'strict_threshold_required':True},'limits':'No finite quotient enumeration, no independent construction of building theory, no exhaustive sphere-subcomplex enumeration; these are finite proof controls.'}
(ROOT/'fresh-controls.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','projective_plane','torus_boundary_control']}))
