"""Fresh finite incidence reconstruction, without importing author programs."""
import itertools, json
from pathlib import Path

def require(ok, message):
    if not ok:
        raise ValueError(message)

def inv(w): return w.swapcase()[::-1]
def red(w):
    s=[]
    for c in w:
        if s and s[-1] == c.swapcase(): s.pop()
        else: s.append(c)
    return ''.join(s)
def subst(w, images):
    return red(''.join(images[c] if c in images else inv(images[c.lower()]) for c in w))
def dih(w):
    return {v[i:]+v[:i] for v in (w,inv(w)) for i in range(len(w))}
def pair(a,b): return tuple(sorted((a,b)))
def corners(w): return [pair(w[i-1].swapcase(),w[i]) for i in range(len(w))]

K=['xyXY','bxBY']; KE={e for w in K for e in corners(w)}
lam={'x':'y','y':'x','b':'B'}
require(all(subst(subst(w,lam),lam)==w for w in ('x','y','b')), 'lambda involution on edges')
require(all(subst(w,lam) in dih(w) for w in K), 'lambda geometric square dihedral maps')
# The permutation of square corners is determined by boundary label positions.
square_lambda=[]
for w in K:
    lw=subst(w,lam)
    mapping=[]
    for direction in (1,-1):
        for start in range(4):
            labels=''.join(w[(start+i)%4] if direction==1 else w[(start-i-1)%4].swapcase() for i in range(4))
            if labels==lw: mapping.append([(start+direction*i)%4 for i in range(4)])
    require(len(mapping)==1,'unique isometric corner map')
    m=mapping[0]; require(all(m[m[i]]==i for i in range(4)), 'square isometry squares to identity')
    square_lambda.append(m)

edges={'p':('B','A','x'),'q':('A','C','y'),'r':('D','C','x'),
       's':('B','D','y'),'d':('A','B','b'),'e':('C','A','b')}
Q=['pqRS','dpEQ']; origins=['B','A']
def qedge(c):
    a,b,label=edges[c.lower()]
    return (a,b,label) if c.islower() else (b,a,label.swapcase())
QL={v:set() for v in 'ABCD'}; QV={v:set() for v in 'ABCD'}
cycles=[]; boundary_faces=[]
for wi,(w,origin) in enumerate(zip(Q,origins)):
    v=origin; cycle=[]
    for i,c in enumerate(w):
        a,b,label=qedge(c); require(a==v,'attaching path closes with true incidence')
        cycle.append(a); v=b
        ce=pair(w[i-1].swapcase(),c); QL[a].add(ce); QV[a].update(ce)
    require(v==origin,'closed square')
    labelword=''.join(qedge(c)[2] for c in w)
    require(labelword==K[wi],'bottom face isometry')
    require(subst(labelword,lam) in dih(K[wi]),'top face isometry')
    cycles.append(cycle); boundary_faces.append({'bottom':labelword,'top':subst(labelword,lam),'sides':list(w)})

def germ_image(c,top=False):
    label=edges[c.lower()][2]
    if c.isupper(): label=label.swapcase()
    return subst(label,lam) if top else label

Ledges=set(KE); Ltri=set(); cones={}
for v in 'ABCD':
    for top in (False,True):
        apex='z'+v+('-' if top else '+')
        vertices={germ_image(c,top) for c in QV[v]}
        imageedges={pair(germ_image(a,top),germ_image(b,top)) for a,b in QL[v]}
        require(len(vertices)==len(QV[v]),'injective vertex link')
        require(len(imageedges)==len(QL[v]),'injective edge link')
        full={e for e in KE if set(e)<=vertices}
        require(full==imageedges,'full induced link image')
        cones[apex]={'vertices':sorted(vertices),'edges':sorted(imageedges)}
        Ledges.update(pair(apex,g) for g in vertices)
        Ltri.update(tuple(sorted((apex,a,b))) for a,b in imageedges)

# Reconstruct the same simplices from actual square and cube corners,
# independently of the cones. Repeated vertex incidences remain in lists.
inc_edges=list(KE); inc_tri=[]; product_squares=[]
for h,(a,b,label) in edges.items():
    top=subst(label,lam)
    rel=[label,'z'+b+'+',top.swapcase(),'z'+a+'-']
    product_squares.append(rel)
    inc_edges += [pair(label.swapcase(),'z'+b+'+'),pair(top.swapcase(),'z'+b+'-'),
                  pair(top,'z'+a+'-'),pair(label,'z'+a+'+')]
for w,cycle in zip(Q,cycles):
    for i,v in enumerate(cycle):
        for top in (False,True):
            a=germ_image(w[i-1].swapcase(),top); b=germ_image(w[i],top)
            inc_tri.append(tuple(sorted(('z'+v+('-' if top else '+'),a,b))))
require(set(inc_edges)==Ledges,'actual square incidences vs cone edges')
require(len(inc_edges)==len(set(inc_edges)),'no repeated link edges')
require(set(inc_tri)==Ltri,'actual cube incidences vs cone triangles')
require(len(inc_tri)==len(set(inc_tri)),'no repeated link triangles')
LV={v for e in Ledges for v in e}
cliques=[]
for size in range(3,5):
    for s in itertools.combinations(sorted(LV),size):
        if all(pair(a,b) in Ledges for a,b in itertools.combinations(s,2)): cliques.append(s)
require({s for s in cliques if len(s)==3}==Ltri,'flag triangles')
require(not any(len(s)==4 for s in cliques),'no four clique')

phi={'a':'a','b':'ab','c':'bcb'}; phiinv={'a':'a','b':'Ab','c':'BacBa'}
require(all(subst(subst(c,phi),phiinv)==c and subst(subst(c,phiinv),phi)==c for c in 'abc'),'inverse automorphism both compositions')
# Inverse basis before quotient relations, including t and c.
forward={'x':'t','y':'At','z':'CT','b':'b'}
backward={'t':'x','a':'xY','c':'XZ','b':'b'}
require(all(subst(subst(c,forward),backward)==c for c in 'xyzb'),'basis forward-back')
require(all(subst(subst(c,backward),forward)==c for c in 'tacb'),'basis back-forward')
result={'status':'PASS','base_edges':sorted(KE),'Q_vertex_cycles':cycles,
 'Q_links':{v:sorted(QL[v]) for v in QL},'lambda_square_vertex_permutations':square_lambda,
 'actual_cube_faces':boundary_faces,'product_square_boundaries':product_squares,'cones':cones,
 'link_counts':[len(LV),len(Ledges),len(Ltri)],'cell_counts':[1,7,8,2],
 'link_edges':sorted(Ledges),'link_triangles':sorted(Ltri),'automorphism_and_basis_both_compositions':'PASS'}
out=Path(__file__).with_name('INDEPENDENT_RECONSTRUCTION_RESULTS.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'cycles':cycles,'counts':result['link_counts'],'basis':'PASS'}))
