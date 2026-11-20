#!/usr/bin/env python3
"""Exact, standard-library-only finite controls. These do not settle universality."""
import argparse, collections, hashlib, itertools as it, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent

class Invalid(ValueError): pass

def need(condition, message):
    if not condition: raise Invalid(message)

def canonical(data):
    return json.dumps(data, sort_keys=True, indent=2) + '\n'

def add(x,y): return (x[0]+y[0],x[1]+y[1])
def mul(x,y): return (x[0]*y[0]+x[1]*y[1],x[0]*y[1]+x[1]*y[0]+x[1]*y[1])
def dot(x,y):
    z=(0,0)
    for a,b in zip(x,y): z=add(z,mul(a,b))
    return z

def sign(x):
    # Sign of a+b phi, phi=(1+sqrt(5))/2, without floats.
    a,b=x; u,v=2*a+b,b
    if not v: return (u>0)-(u<0)
    if not u: return (v>0)-(v<0)
    if u>0 and v>0: return 1
    if u<0 and v<0: return -1
    if u>0: return (u*u>5*v*v)-(u*u<5*v*v)
    return (5*v*v>u*u)-(5*v*v<u*u)

def vertices600():
    out=set()
    for k in range(4):
        for sg in (-1,1):
            p=[(0,0)]*4; p[k]=(2*sg,0); out.add(tuple(p))
    for signs in it.product((-1,1),repeat=4): out.add(tuple((s,0) for s in signs))
    for perm in it.permutations(range(4)):
        if sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))%2: continue
        for signs in it.product((-1,1),repeat=3):
            s,t,u=signs; p=((0,0),(s,0),(0,t),(-u,u));out.add(tuple(p[i] for i in perm))
    return sorted(out)

def facets600(points):
    adjacent={i:set() for i in range(len(points))}
    for i,j in it.combinations(adjacent,2):
        if dot(points[i],points[j])==(0,2): adjacent[i].add(j);adjacent[j].add(i)
    return sorted((a,b,c,d) for a in adjacent for b in sorted(adjacent[a]) if b>a
                  for c in sorted(adjacent[a]&adjacent[b]) if c>b
                  for d in sorted(adjacent[a]&adjacent[b]&adjacent[c]) if d>c)

def connected(vertices, edges):
    vertices=set(vertices)
    if not vertices:return False
    adj={v:set() for v in vertices}
    for a,b in edges: adj[a].add(b);adj[b].add(a)
    seen=set();stack=[next(iter(vertices))]
    while stack:
        v=stack.pop()
        if v in seen:continue
        seen.add(v);stack.extend(adj[v]-seen)
    return seen==vertices

def cycle(edges):
    edges=set(tuple(sorted(e)) for e in edges)
    ds=collections.Counter(x for e in edges for x in e)
    return len(ds)>=3 and set(ds.values())=={2} and connected(ds,edges)

def analyze(tetrahedra, require56=True, require_tcp=False):
    need(isinstance(tetrahedra,list) and tetrahedra,'nonempty list required')
    need(all(isinstance(t,(tuple,list)) and len(t)==4 and all(type(v) is int and v>=0 for v in t) and len(set(t))==4 for t in tetrahedra),'invalid tetrahedron')
    ts=[tuple(sorted(t)) for t in tetrahedra]
    need(len(ts)==len(set(ts)),'duplicate tetrahedron')
    vs=set(v for t in ts for v in t)
    edges=collections.Counter(e for t in ts for e in it.combinations(t,2))
    faces=collections.defaultdict(list)
    for i,t in enumerate(ts):
        for k in range(4): faces[t[:k]+t[k+1:]].append((i,(-1)**k))
    need(all(len(f)==2 for f in faces.values()),'not closed along triangles')
    need(connected(vs,edges),'disconnected')
    if require56: need(set(edges.values())<={5,6},'edge degree outside 5/6')
    edge_link={e:[] for e in edges}
    for t in ts:
        for e in it.combinations(t,2): edge_link[e].append(tuple(v for v in t if v not in e))
    need(all(cycle(es) for es in edge_link.values()),'nonspherical edge link')
    links={v:[] for v in vs}
    for t in ts:
        for v in t: links[v].append(tuple(x for x in t if x!=v))
    link_summary=collections.Counter()
    for v,triangles in links.items():
        lv=set(x for t in triangles for x in t)
        le=collections.Counter(e for t in triangles for e in it.combinations(t,2))
        need(set(le.values())=={2} and connected(lv,le),'bad vertex-link surface')
        need(len(lv)-len(le)+len(triangles)==2,'vertex link not sphere')
        n5=sum(edges[tuple(sorted((v,w)))]==5 for w in lv)
        n6=sum(edges[tuple(sorted((v,w)))]==6 for w in lv)
        if require56:need(n5==12,'link curvature identity failed')
        link_summary[(n5,n6)]+=1
    # Coherent tetrahedron orientation, independent of an input orientation flag.
    dual={i:[] for i in range(len(ts))}
    for pairs in faces.values():
        (i,s),(j,t)=pairs;dual[i].append((j,-s*t));dual[j].append((i,-s*t))
    ori={0:1};queue=[0]
    while queue:
        i=queue.pop()
        for j,factor in dual[i]:
            if j not in ori:ori[j]=ori[i]*factor;queue.append(j)
            else:need(ori[j]==ori[i]*factor,'nonorientable')
    need(len(ori)==len(ts),'dual disconnected')
    violations=sum(sum(edges[e]==6 for e in it.combinations(f,2))>1 for f in faces)
    if require_tcp:need(violations==0,'TCP triangle restriction failed')
    if require_tcp:need(all(q<=4 for n,q in link_summary),'TCP link degree bound failed')
    if require56:need(sum(d==5 for d in edges.values())==6*len(vs),'global E5 identity failed')
    return {'f_vector':[len(vs),len(edges),len(faces),len(ts)],
            'edge_histogram':{str(k):v for k,v in sorted(collections.Counter(edges.values()).items())},
            'vertex_link_counts':[{'degree5':n,'degree6':q,'vertices':c} for (n,q),c in sorted(link_summary.items())],
            'tcp_violating_triangles':violations,'orientable':True}

def support_check(points, facets):
    need(len(points)==120 and len(set(points))==120,'600-cell vertex count')
    need(all(dot(p,p)==(4,0) for p in points),'incorrect radius')
    need(len(facets)==600,'600-cell facet count')
    # Each selected 4-clique has positive-definite Gram matrix: diagonals 4,
    # off-diagonals 2phi. Its four vertices are linearly independent.
    # The normal sum of its vertices gives an exact supporting hyperplane.
    strict=0
    for facet in facets:
        normal=tuple(sum(points[i][j][k] for i in facet) for j in range(4) for k in range(2))
        normal=tuple((normal[2*j],normal[2*j+1]) for j in range(4))
        eq=[]
        for j,p in enumerate(points):
            x=dot(normal,p);s=sign((4-x[0],6-x[1]))
            need(s>=0,'support plane cuts through a vertex')
            if s==0:eq.append(j)
            else:strict+=1
        need(eq==list(facet),'facet equality vertices differ')
    return {'support_planes':len(facets),'weak_inequalities':len(points)*len(facets),'strict_inequalities':strict}

def star_sum(tetrahedra, apex=0):
    boundary=sorted(set(tuple(v for v in t if v!=apex) for t in tetrahedra if apex in t))
    seam=set(v for f in boundary for v in f)
    puncture=[t for t in tetrahedra if apex not in t]
    # No extra face of the complement with vertices in seam may get identified.
    boundary_faces=set(f for t in boundary for r in range(1,4) for f in it.combinations(t,r))
    for t in puncture:
        for r in range(1,5):
            for f in it.combinations(t,r):
                if set(f)<=seam:need(f in boundary_faces,'non-induced gluing boundary')
    offset=max(v for t in tetrahedra for v in t)+1
    out=list(puncture)+[tuple(sorted(v if v in seam else v+offset for v in t)) for t in puncture]
    return out, boundary

def self_handle(points,tetrahedra):
    # Orthogonal symmetry diag(-1,1,-1,-1): orientation reversing on S^3,
    # and it exchanges the two antipodal coordinate-axis vertices.
    north=0; south=points.index(tuple((-a,-b) for a,b in points[north]))
    link0=sorted(tuple(v for v in t if v!=north) for t in tetrahedra if north in t)
    link1=sorted(tuple(v for v in t if v!=south) for t in tetrahedra if south in t)
    v0=set(v for t in link0 for v in t);v1=set(v for t in link1 for v in t)
    need(not v0 & v1,'handle boundaries intersect')
    image={i:points.index(tuple((a,b) if k==1 else (-a,-b) for k,(a,b) in enumerate(p))) for i,p in enumerate(points)}
    need(image[north]==south,'handle symmetry does not swap poles')
    need(sorted(tuple(sorted(image[v] for v in t)) for t in link0)==link1,'handle boundary map is not simplicial')
    rem=[t for t in tetrahedra if north not in t and south not in t]
    # No simplex meets both boundary vertex sets, excluding quotient collapse.
    need(all(not (set(t)&v0 and set(t)&v1) for t in rem),'simplex meets both handle boundaries')
    out=[tuple(sorted(image[v] if v in v1 else v for v in t)) for t in rem]
    need(all(len(set(t))==4 for t in out),'collapsed handle tetrahedron')
    return out

def stellar(tets,face,new):
    face=set(face);out=[]
    for t in tets:
        if face<=set(t):
            for v in face:out.append(tuple(sorted((set(t)-{v})|{new})))
        else:out.append(tuple(t))
    return out

def counts(tets):return collections.Counter(e for t in tets for e in it.combinations(sorted(t),2))

def local_controls():
    records=[]
    for d in range(3,21):
        old=[(0,1,2+i,2+(i+1)%d) for i in range(d)]
        out=stellar(old,(0,1),99);deg=counts(out)
        need(deg[(0,99)]==d and deg[(1,99)]==d,'edge split axial degrees')
        need(all(deg[(v,99)]==4 for v in range(2,d+2)),'edge split degree-four obstruction')
        records.append({'operation':'edge_stellar','old_degree':d,'new_transverse_degree':4})
    faceout=stellar([(0,1,2,3),(0,1,2,4)],(0,1,2),99)
    fd=counts(faceout)
    need(all(fd[(v,99)]==4 for v in range(3)),'face stellar obstruction')
    tetout=stellar([(0,1,2,3)],(0,1,2,3),99)
    need(all(counts(tetout)[(v,99)]==3 for v in range(4)),'tet stellar obstruction')
    pachner=[(0,1,3,4),(0,2,3,4),(1,2,3,4)]
    need(counts(pachner)[(3,4)]==3,'2-3 move new edge')
    # Every independent subset of a cyclic 5-neighbor link has cardinality <=2.
    independent=[]
    for mask in range(32):
        chosen=[i for i in range(5) if mask>>i&1]
        if all(not ((mask>>i&1) and (mask>>((i+1)%5)&1)) for i in range(5)):
            need(len(chosen)<=2,'five-cycle bound');independent.append(chosen)
    return {'edge_stellar_cases':records,'face_stellar_degree':4,'tetra_stellar_degree':3,'pachner_2_3_new_degree':3,'cycle5_independent_subsets':independent,'octahedral_replacement_minimum_new_vertices':7}

def reject(call,label):
    try:call()
    except (Invalid,KeyError,TypeError,ValueError):return label
    raise Invalid('negative control accepted: '+label)

def compute():
    p=vertices600();t=facets600(p)
    geometry=support_check(p,t);a=analyze(t,require_tcp=True)
    glued,boundary=star_sum(t);b=analyze(glued)
    need(a['f_vector']==[120,720,1200,600],'600-cell f-vector')
    need(b['f_vector']==[226,1386,2320,1160],'glued f-vector')
    need(b['edge_histogram']=={'5':1356,'6':30},'glued edge histogram')
    need(b['tcp_violating_triangles']==20,'glued TCP failures')
    handle=self_handle(p,t);h=analyze(handle)
    need(h['f_vector']==[106,666,1120,560],'handle f-vector')
    need(h['edge_histogram']=={'5':636,'6':30},'handle edge histogram')
    neg=[]
    neg.append(reject(lambda:analyze(t[:-1]),'missing tetrahedron'))
    neg.append(reject(lambda:analyze(t+[t[0]]),'duplicate tetrahedron'))
    neg.append(reject(lambda:analyze([(0,0,1,2)]+t[1:]),'collapsed tetrahedron'))
    neg.append(reject(lambda:analyze(glued,require_tcp=True),'false TCP assertion'))
    pp=list(p);pp[0]=((99,0),(0,0),(0,0),(0,0))
    neg.append(reject(lambda:support_check(pp,t),'mutated vertex coordinate'))
    need(cycle([(0,1),(1,2),(0,2)]),'positive cycle control')
    need(not cycle([(0,1),(1,2)]),'open path control')
    need(not cycle([(0,1),(1,2),(0,2),(3,4),(4,5),(3,5)]),'disconnected cycles control')
    return {'schema':1,'problem_id':30000433,'status':'partial_unsolved','approaches_used':4,
            'full_source_solved':False,'scope':'finite closed orientable simplicial 3-manifolds; no generalized-gluing or boundary extension claimed',
            'support_certificate':geometry,'six_hundred_cell':a,'vertex_star_connected_sum':b,
            'self_handle_S2_times_S1':h,'local_controls':local_controls(),'negative_controls':neg,
            'limitations':['Finite controls do not prove the universal existence claim.','The explicit manifold types S3 and S2 times S1 were already known to admit TCP triangulations.','No novelty or human peer-review claim.']}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write-results',action='store_true');ap.add_argument('--manifest-sha256');args=ap.parse_args()
    if args.manifest_sha256:
        raw=(ROOT/'MANIFEST.json').read_bytes();need(hashlib.sha256(raw).hexdigest()==args.manifest_sha256,'manifest pin mismatch')
        manifest=json.loads(raw)
        for name,meta in manifest['files'].items():
            need(pathlib.PurePosixPath(name).name==name,'unsafe manifest path')
            data=(ROOT/name).read_bytes();need(len(data)==meta['bytes'] and hashlib.sha256(data).hexdigest()==meta['sha256'],'file hash mismatch: '+name)
    result=compute()
    if args.write_results:(ROOT/'results.json').write_text(canonical(result))
    else:need(canonical(json.loads((ROOT/'results.json').read_text()))==canonical(result),'stored results do not match exact replay')
    print(canonical(result),end='')

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
