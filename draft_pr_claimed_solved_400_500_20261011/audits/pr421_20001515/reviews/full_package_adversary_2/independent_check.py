"""Independent, stdlib, occurrence-level reconstruction; no packet imports."""
import itertools, json, pathlib

def need(condition, message):
    if not condition:
        raise ValueError(message)

def inv(h):
    return h.swapcase()

def germ(h):
    return h.lower() + ('+' if h.islower() else '-')

def corners(word):
    return [frozenset((germ(inv(word[i-1])), germ(word[i]))) for i in range(len(word))]

def red(word):
    out=[]
    for h in word:
        if out and out[-1]==inv(h): out.pop()
        else: out.append(h)
    return ''.join(out)

def inverse_word(word):
    return ''.join(inv(h) for h in word[::-1])

def subst(word, mapping):
    return red(''.join(mapping[h] if h in mapping else inverse_word(mapping[inv(h)]) for h in word))

BASE=['xyXY','bxBY']
EDGE={'p':('B','A','x'),'q':('A','C','y'),'r':('D','C','x'),'s':('B','D','y'),'d':('A','B','b'),'e':('C','A','b')}
Q=[('B','pqRS'),('A','dpEQ')]
lam={'x':'y','y':'x','b':'B'}

def geometry(base=BASE, qfaces=Q):
    base_occ=sum((corners(w) for w in base),[])
    need(len(base_occ)==len(set(base_occ)), 'base duplicate corner edge')
    need(all(len(e)==2 for e in base_occ), 'base loop in link')
    base_edges=set(base_occ)
    q_occ={v:[] for v in 'ABCD'}
    q_verts={v:set() for v in 'ABCD'}
    q_corner_records=[]
    for start,w in qfaces:
        curr=start; vertex_cycles=[]
        for i,h in enumerate(w):
            u,v,label=EDGE[h.lower()]
            if h.isupper(): u,v,label=v,u,inv(label)
            need(curr==u,'Q attaching path endpoint mismatch')
            prev=w[i-1]
            corner=frozenset((germ(inv(prev)),germ(h)))
            q_occ[curr].append(corner);q_verts[curr].update(corner)
            vertex_cycles.append(curr);curr=v
        need(curr==start,'Q face not closed')
        q_corner_records.append((w,vertex_cycles))
    for h,(u,v,_) in EDGE.items():
        q_verts[u].add(h+'+');q_verts[v].add(h+'-')
    def image(g,top=False):
        h=EDGE[g[0]][2]
        if g[1]=='-': h=inv(h)
        if top: h=subst(h,lam)
        return germ(h)
    need(sum(map(len,q_occ.values()))==8,'Q must have eight actual corners')
    link_occ=list(base_occ);tri_occ=[];cone_records=[]
    for v in 'ABCD':
        need(len(q_occ[v])==len(set(q_occ[v])),'duplicate Q corner')
        for top in (False,True):
            apex='z'+v+('-' if top else '+')
            vertices={image(g,top) for g in q_verts[v]}
            need(len(vertices)==len(q_verts[v]),'noninjective signed link map')
            mapped=[frozenset(image(g,top) for g in e) for e in q_occ[v]]
            induced={e for e in base_edges if e<=vertices}
            need(set(mapped)==induced,'nonfull link image')
            link_occ.extend(frozenset((apex,g)) for g in vertices)
            tri_occ.extend(frozenset((apex,)+tuple(e)) for e in mapped)
            cone_records.append({'apex':apex,'base_vertices':sorted(vertices),'base_edges':[sorted(e) for e in mapped]})
    need(len(link_occ)==len(set(link_occ)),'actual square corners duplicate a link edge')
    need(len(tri_occ)==len(set(tri_occ)),'actual cube corners duplicate a link triangle')
    link_edges=set(link_occ);triangles=set(tri_occ)
    vertices=set.union(*(set(e) for e in link_edges))
    cliques={frozenset(c) for c in itertools.combinations(vertices,3) if all(frozenset(p) in link_edges for p in itertools.combinations(c,2))}
    need(cliques==triangles,'actual triangle set is not all three-cliques')
    need(not any(all(frozenset(p) in link_edges for p in itertools.combinations(c,2)) for c in itertools.combinations(vertices,4)), 'missing tetrahedron')
    need((len(vertices),len(link_edges),len(triangles))==(14,32,16),'wrong link counts')
    # Attach every product square directly from its edge endpoints.
    squares=[]
    for h,(u,v,label) in EDGE.items():
        squares.append([label,'z'+v,inverse_word(subst(label,lam)),'Z'+u])
    def tinv(t):
        return t.swapcase() if len(t)==1 else ('Z' if t[0]=='z' else 'z')+t[1:]
    def tgerm(t):
        return germ(t) if len(t)==1 else 'z'+t[1:]+('+' if t[0]=='z' else '-')
    actual_square_edges=list(base_occ)
    for square in squares:
        actual_square_edges.extend(frozenset((tgerm(tinv(square[i-1])),tgerm(square[i]))) for i in range(4))
    need(len(actual_square_edges)==32 and set(actual_square_edges)==link_edges,'direct product-square incidence differs from cone link')
    cube_records=[]; actual_cube_triangles=[]
    for start,word in qfaces:
        curr=start; records=[]
        for i,h in enumerate(word):
            u,v,label=EDGE[h.lower()]
            if h.isupper():u,v=v,u
            local_corner=(germ(inv(word[i-1])),germ(h))
            for top in (False,True):
                tri=frozenset(('z'+curr+('-' if top else '+'),)+tuple(image(g,top) for g in local_corner))
                actual_cube_triangles.append(tri)
                records.append({'occurrence':i,'vertex':curr,'end':int(top),'triangle':sorted(tri)})
            curr=v
        cube_records.append({'Q_square':word,'bottom_word':subst(word,{h:e[2] for h,e in EDGE.items()}),'top_word':subst(subst(word,{h:e[2] for h,e in EDGE.items()}),lam),'eight_actual_corners':records})
    need(len(actual_cube_triangles)==16 and set(actual_cube_triangles)==triangles,'direct product-cube incidence differs from cone link')
    return {'Q_corner_cycles':q_corner_records,'Q_links':{v:[sorted(e) for e in q_occ[v]] for v in q_occ},'cone_records':cone_records,'actual_cube_records':cube_records,'link_counts':[14,32,16], 'cell_counts':[1,7,8,2],'product_squares':squares,'square_corner_occurrences':len(link_occ),'cube_corner_occurrences':len(tri_occ)}

phi={'a':'a','b':'ab','c':'bcb'}
psi={'a':'a','b':'Ab','c':'BacBa'}
def powerphi(w,n):
    for _ in range(abs(n)): w=subst(w,phi if n>=0 else psi)
    return w
def mult(v,w):
    return (red(v[0]+powerphi(w[0],v[1])),v[1]+w[1])
def inverse_pair(v):
    return (powerphi(inverse_word(v[0]),-v[1]),-v[1])
images={'x':('',1),'y':('A',1),'b':('b',0),'z':('C',-1)}
def eval_letters(w,table=images):
    ans=('',0)
    for h in w:
        val=table[h.lower()]
        ans=mult(ans,val if h.islower() else inverse_pair(val))
    return ans
def algebra():
    for h in 'abc':
        need(subst(phi[h],psi)==h,'phi inverse composition fails')
        need(subst(psi[h],phi)==h,'inverse phi composition fails')
    inv_auto={h:psi[h] for h in 'abc'}
    zB=eval_letters('xzY');zC=eval_letters('Yzx');zD=eval_letters('YxzYx')
    table={**images,'A':images['z'],'B':zB,'C':zC,'D':zD}
    def token(t):
        if t[0]=='z': return table[t[1]]
        if t[0]=='Z': return inverse_pair(table[t[1]])
        return eval_letters(t)
    geom=geometry()
    vals=[]
    for sq in geom['product_squares']:
        p=('',0)
        for t in sq:p=mult(p,token(t))
        need(p==('',0),'product square not satisfied in target G')
        vals.append(p)
    for w in ('xyXY','bxBY','ZbxzYb'):
        need(eval_letters(w)==('',0),'reduced HNN relator fails')
    return {'inverse_automorphism':inv_auto,'six_product_relators_target_values':vals,'reduced_HNN_relators_target_values':[['',0]]*3,'note':'Tietze reversibility is proved in OWN_PROOF_RECONSTRUCTION.md; forward evaluation alone is not used as isomorphism proof.'}

def main():
    result={'geometry':geometry(),'algebra':algebra()}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
