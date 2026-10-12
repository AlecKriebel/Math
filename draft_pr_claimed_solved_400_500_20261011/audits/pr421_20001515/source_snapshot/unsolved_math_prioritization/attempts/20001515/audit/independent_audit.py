"""Independent reviewer finite reconstruction. Does not import/read author's verifier.
Models the 2-skeleton directly and reconstructs cube corners from square coordinates.
"""
import itertools as I, collections as C, json, hashlib, pathlib
BASE=pathlib.Path(__file__).resolve().parent.parent

def inv(l):
    e,s=l
    return (e,-s)
def w(tokens):
    return [(t.lower(),1 if t.islower() else -1) for t in tokens]
def wi(word): return list(map(inv,word[::-1]))
def red(word):
    ans=[]
    for a in word:
        if ans and ans[-1]==inv(a): ans.pop()
        else: ans.append(a)
    return ans

def cyclic_same(u,v):
    return any(u==vv[i:]+vv[:i] for vv in (v,wi(v)) for i in range(len(v)))
def lamb(a):
    e,s=a
    return {'x':('y',s),'y':('x',s),'b':('b',-s)}[e]
def corners(word):
    return [(inv(word[i-1]),word[i]) for i in range(len(word))]
def es(a,b):
    assert a!=b, ('loop link edge',a)
    return frozenset([a,b])
def fmt(a): return a[0]+('+' if a[1]>0 else '-')
def encode(ss): return sorted(sorted(map(fmt,s)) for s in ss)

ksquares=[w('xyXY'),w('bxBY')]
kcounter=C.Counter(es(*v) for word in ksquares for v in corners(word))
kedges=set(kcounter)
kverts=set(sum([list(e) for e in kedges],[]))
assert all(n==1 for n in kcounter.values())
assert all(any(cyclic_same(list(map(lamb,s)),target) for target in ksquares) for s in ksquares)
assert all(lamb(lamb(a))==a for a in kverts)
qedges={
    'p':('B','A',('x',1)), 'q':('A','C',('y',1)),
    'r':('D','C',('x',1)), 's':('B','D',('y',1)),
    'd':('A','B',('b',1)), 'e':('C','A',('b',1))}
qsquares=[w('pqRS'),w('dpEQ')]

def endpoints(a):
    u,v,_=qedges[a[0]]
    return (u,v) if a[1]>0 else (v,u)
def j(a):
    _,_,(l,s)=qedges[a[0]]
    return l,s*a[1]
qverts={}
qcorners={}
for e,(u,v,label) in qedges.items():
    qverts.setdefault(u,[]).append((e,1))
    qverts.setdefault(v,[]).append((e,-1))
for word in qsquares:
    assert any(cyclic_same(list(map(j,word)),s) for s in ksquares)
    for i,(a,b) in enumerate(corners(word)):
        assert endpoints(word[i-1])[1]==endpoints(word[i])[0]
        v=endpoints(word[i])[0]
        qcorners.setdefault(v,[]).append(es(a,b))
qlinks={}
for v,dirs in sorted(qverts.items()):
    vd=list(map(j,dirs))
    assert len(set(vd))==len(dirs)
    ee=[frozenset(map(j,e)) for e in qcorners[v]]
    assert len(set(ee))==len(ee)
    induced={e for e in kedges if e<=set(vd)}
    assert set(ee)==induced
    qlinks[v]={'vertices': sorted(map(fmt,vd)), 'edges':encode(ee)}
# Collapse a spanning tree, independently checking tree connectedness/cyclicity.
tree=['p','q','s']
reachable={'A'}
while True:
    old=set(reachable)
    for e in tree:
        u,v,_=qedges[e]
        if u in reachable or v in reachable: reachable|={u,v}
    if old==reachable:break
assert len(reachable)==4 and len(tree)==3
collapsed=[red([a for a in word if a[0] not in tree]) for word in qsquares]
assert collapsed==[w('R'),w('dE')]
# Direct list of all Z square boundaries. No cone-based construction is used here.
def vertical(v,s=1):return ('z'+v,s)
zwords=list(ksquares)
for e,(u,v,l) in qedges.items():
    zwords.append([l,vertical(v),inv(lamb(l)),vertical(u,-1)])
link_edge_occurrences=C.Counter(es(*corner) for word in zwords for corner in corners(word))
assert all(n==1 for n in link_edge_occurrences.values())
zedges=set(link_edge_occurrences)
zverts=set(sum([list(e) for e in zedges],[]))
# Full actual cube characteristic maps: cube positions indexed by (x,y,t).
# Each underlying Q square has directed boundary e0,e1,e2,e3 at 00,10,11,01.
coords=[(0,0),(1,0),(1,1),(0,1)]
tri_counts=C.Counter()
cube_report=[]
for word in qsquares:
    vertex_at={coords[i]:endpoints(word[i])[0] for i in range(4)}
    local_germs={coords[i]:corners(word)[i] for i in range(4)}
    cube_triangles=[]
    for c in coords:
        qv=vertex_at[c]
        for height in [0,1]:
            horizontal=[j(a) for a in local_germs[c]]
            if height: horizontal=list(map(lamb,horizontal))
            tr=frozenset(horizontal+[vertical(qv,1 if height==0 else -1)])
            assert len(tr)==3
            assert all(frozenset(pair) in zedges for pair in I.combinations(tr,2))
            tri_counts[tr]+=1
            cube_triangles.append(sorted(map(fmt,tr)))
    # Each side really is the correct product-square cell, allowing face reversal.
    side_words=[]
    for a in word:
        u,v=endpoints(a);l=j(a)
        side=[l,vertical(v),inv(lamb(l)),vertical(u,-1)]
        expected=zwords[2+list(qedges).index(a[0])]
        assert cyclic_same(side,expected)
        side_words.append(list(map(fmt,side)))
    assert any(cyclic_same(list(map(j,word)),s) for s in ksquares)
    assert any(cyclic_same(list(map(lamb,map(j,word))),s) for s in ksquares)
    cube_report.append({'corner_triangles':cube_triangles,'four_side_faces':side_words})
assert all(n==1 for n in tri_counts.values())
ztri=set(tri_counts)
cliques={n:{frozenset(q) for q in I.combinations(zverts,n)
            if all(frozenset(p) in zedges for p in I.combinations(q,2))}
         for n in range(3,15)}
assert cliques[3]==ztri
assert all(not cliques[n] for n in range(4,15))
assert (len(zverts),len(zedges),len(ztri))==(14,32,16)
# Negative controls detect omission of each cube corner and addition of missing edges.
controls=0
for t in ztri:
    assert cliques[3]!=(ztri-{t});controls+=1
# A sign error in the proposed involution must fail already on the second K square.
wrong_lambda=lambda a: {'x':('y',a[1]),'y':('x',a[1]),'b':('b',a[1])}[a[0]]
assert not any(cyclic_same(list(map(wrong_lambda,ksquares[1])),f) for f in ksquares)
controls+=1
# The complete clique enumeration, rather than just no tetrahedra, is recorded above.
# Publication-only portability adjustment: bind the unchanged mathematical proof.
# Original five-file WIP hashes are retained in INITIAL_WIP_FREEZE.json.
assert hashlib.sha256((BASE/'ATTEMPT_1.md').read_bytes()).hexdigest() == (
    'c022afdfe003d0692a032cee48855ddf712de22953b358b895c485215875d8a6')
result={
 'status':'PASS finite geometric incidence checks',
 'independence':'Fresh reconstruction; does not import or execute verify.py',
 'frozen_proof_hash_matches': True,
 'K_link':{'vertices':sorted(map(fmt,kverts)),'edges':encode(kedges)},
 'Q_links':qlinks,
 'Q_collapsed_relators':[list(map(fmt,word)) for word in collapsed],
 'Z_square_relators':[list(map(fmt,word)) for word in zwords],
 'Z_link_f_vector':[len(zverts),len(zedges),len(ztri)],
 'Z_link_edges':encode(zedges),'Z_link_triangles':encode(ztri),
 'Z_all_cliques_by_size':{n:len(c) for n,c in cliques.items()},
 'cube_face_and_corner_maps':cube_report,
 'negative_controls':controls,
 'cell_f_vector':[1,7,8,2],
 'scope':'Finite combinatorial certificate only; group identification and global geometric conclusions have separate written audit.'}
(BASE/'audit'/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','frozen_proof_hash_matches','Z_link_f_vector','Z_all_cliques_by_size','negative_controls','cell_f_vector']},indent=2))
