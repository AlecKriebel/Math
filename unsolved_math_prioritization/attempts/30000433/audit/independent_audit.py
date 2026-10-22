#!/usr/bin/env python3
"""Independent exact audit of frozen author controls; standard library only.
This program regenerates the geometry in Z[sqrt(5)], not Z[phi], checks
combinatorial links, GF(2) homology, surgery identifications and orientations.
It does not prove universal 5/6 or TCP existence, or use homology to name a manifold.
"""
import argparse, collections, hashlib, importlib.util, itertools, json, pathlib
C=itertools.combinations

def require(x,msg):
    if not x: raise ValueError(msg)
def plus(a,b): return (a[0]+b[0],a[1]+b[1])
def times(a,b): return (a[0]*b[0]+5*a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def negative(a): return (-a[0],-a[1])
def product(seq):
    y=(1,0)
    for x in seq:y=times(y,x)
    return y

def sgn(x):
    a,b=x
    if a==0:return (b>0)-(b<0)
    if b==0:return (a>0)-(a<0)
    if a*b>0:return (a>0)-(a<0)
    q=a*a-5*b*b
    return ((a>0)-(a<0))*((q>0)-(q<0))

def dot(a,b):
    z=(0,0)
    for x,y in zip(a,b):z=plus(z,times(x,y))
    return z

def parity(t):return -1 if sum(t[i]>t[j] for i in range(len(t)) for j in range(i+1,len(t)))%2 else 1

def determinant(rows):
    r=(0,0)
    for perm in itertools.permutations(range(4)):
        v=product(rows[i][perm[i]] for i in range(4))
        r=plus(r,v if parity(perm)==1 else negative(v))
    return r

def points():
    p=set()
    for i in range(4):
        for s in [-1,1]:
            t=[(0,0)]*4;t[i]=(4*s,0);p.add(tuple(t))
    for ss in itertools.product([-1,1],repeat=4):p.add(tuple((2*s,0) for s in ss))
    for perm in itertools.permutations(range(4)):
        if parity(perm)!=1:continue
        for ss in itertools.product([-1,1],repeat=3):
            t=[(0,0),(2*ss[0],0),(ss[1],ss[1]),(-ss[2],ss[2])]
            p.add(tuple(t[i] for i in perm))
    return sorted(p)

def regenerate(p):
    adj=[set() for _ in p]
    for a,b in C(range(len(p)),2):
        if dot(p[a],p[b])==(4,4):adj[a].add(b);adj[b].add(a)
    out=set()
    for a in range(len(p)):
        for b,c,d in C(sorted(x for x in adj[a] if x>a),3):
            if c in adj[b] and d in adj[b] and d in adj[c]:out.add((a,b,c,d))
    return sorted(out)

def skeleton(tets,k):return sorted({f for t in tets for f in C(t,k+1)})
def connected(vertices,edges):
    vertices=set(vertices);adj={v:set() for v in vertices}
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    if not vertices:return False
    q=[next(iter(vertices))];seen=set(q)
    for v in q:
        for w in adj[v]-seen:seen.add(w);q.append(w)
    return seen==vertices

def cyclic(es):
    es=list(es);vs=set(x for e in es for x in e)
    return len(es)==len(set(es)) and len(vs)>=3 and set(collections.Counter(x for e in es for x in e).values())=={2} and connected(vs,es)

def rank2(columns):
    piv={}
    for a in columns:
        while a:
            k=a.bit_length()-1
            if k not in piv:piv[k]=a;break
            a^=piv[k]
    return len(piv)

def complex_checks(tets):
    require(len(tets)==len(set(tets)),'duplicate tetrahedra')
    require(all(len(t)==4 and len(set(t))==4 for t in tets),'collapsed tetrahedra')
    sk=[skeleton(tets,k) for k in range(4)]
    inc=[collections.defaultdict(list) for _ in range(3)]
    for i,t in enumerate(tets):
        for k in range(3):
            for f in C(t,k+1):inc[k][f].append(i)
    require(set(map(len,inc[2].values()))=={2},'triangle closure')
    require(connected([v[0] for v in sk[0]],sk[1]),'disconnected')
    for e,its in inc[1].items():require(cyclic([tuple(v for v in tets[i] if v not in e) for i in its]),'edge link not circle')
    for (v,),its in inc[0].items():
        tris=[tuple(w for w in tets[i] if w!=v) for i in its];ls=[skeleton(tris,k) for k in range(3)]
        require(len(ls[0])-len(ls[1])+len(ls[2])==2,'vertex-link Euler characteristic')
        require(connected([w[0] for w in ls[0]],ls[1]),'vertex-link disconnected')
        require(set(collections.Counter(e for tr in tris for e in C(tr,2)).values())=={2},'vertex-link not closed surface')
    ori={0:1};q=[0];constraints=collections.defaultdict(list)
    for f,ts in inc[2].items():
        a,b=ts;sa=(-1)**tets[a].index(next(v for v in tets[a] if v not in f));sb=(-1)**tets[b].index(next(v for v in tets[b] if v not in f))
        constraints[a].append((b,-sa*sb));constraints[b].append((a,-sa*sb))
    oriented=True
    for i in q:
        for j,factor in constraints[i]:
            if j not in ori:ori[j]=ori[i]*factor;q.append(j)
            elif ori[j]!=ori[i]*factor:oriented=False
    require(len(ori)==len(tets),'disconnected dual')
    ranks=[0]
    for k in range(1,4):
        ind={f:i for i,f in enumerate(sk[k-1])}
        ranks.append(rank2(sum(1<<ind[f] for f in C(t,k)) for t in sk[k]))
    ranks.append(0)
    betti=[len(sk[k])-ranks[k]-ranks[k+1] for k in range(4)]
    deg={e:len(i) for e,i in inc[1].items()}
    tcp=[f for f in sk[2] if sum(deg[e]==6 for e in C(f,2))>1]
    return {'f_vector':list(map(len,sk)), 'edge_histogram':dict(sorted(collections.Counter(deg.values()).items())), 'orientable':oriented,'betti_mod2':betti,'tcp_violations':len(tcp)}, tcp

def boundary(tets):
    c=collections.Counter(f for t in tets for f in C(t,3))
    return sorted(f for f,n in c.items() if n==1)
def induced(tets,tris):
    vs={x for f in tris for x in f};faces={f for t in tris for k in range(1,4) for f in C(t,k)}
    require(all(f in faces for t in tets for k in range(1,5) for f in C(t,k) if set(f)<=vs),'non-induced boundary')
    return vs

def main():
    ap=argparse.ArgumentParser();ap.add_argument('freeze',type=pathlib.Path);args=ap.parse_args();d=args.freeze.resolve()
    require(hashlib.sha256((d/'MANIFEST.json').read_bytes()).hexdigest()=='ac8006591dde3c8d85cbf2bc47dcb375f7b572107c159bc9a4118e16b8ed0873','author manifest differs')
    m=json.loads((d/'MANIFEST.json').read_text())
    for name,rec in m['files'].items():
        raw=(d/name).read_bytes();require(len(raw)==rec['bytes'] and hashlib.sha256(raw).hexdigest()==rec['sha256'],'author member differs: '+name)
    spec=importlib.util.spec_from_file_location('frozen_author',d/'verify.py');author=importlib.util.module_from_spec(spec);spec.loader.exec_module(author)
    p=points();t=regenerate(p);require(len(p)==120 and len(t)==600,'independent reconstruction counts')
    apoints=author.vertices600();conversion={i:p.index(tuple((2*a+b,b) for a,b in v)) for i,v in enumerate(apoints)}
    at=author.facets600(apoints)
    require({tuple(sorted(conversion[v] for v in f)) for f in at}==set(t),'independent facets disagree with author')
    strict=0;det_signs={};support_equalities=0
    for f in t:
        normal=tuple((sum(p[i][j][0] for i in f),sum(p[i][j][1] for i in f)) for j in range(4))
        require(all(dot(p[i],p[j])==((16,0) if i==j else (4,4)) for i in f for j in f),'Gram matrix')
        det_signs[f]=sgn(determinant([p[i] for i in f]));require(det_signs[f]!=0,'degenerate facet')
        eq=[]
        for i,v in enumerate(p):
            q=dot(normal,v);z=sgn((28-q[0],12-q[1]));require(z>=0,'nonsupporting plane')
            if z==0:eq.append(i);support_equalities+=1
            else:strict+=1
        require(eq==list(f),'support equality locus')
    base,_=complex_checks(t);require(base['betti_mod2']==[1,0,0,1] and base['orientable'],'base control')
    n=p.index(((-4,0),(0,0),(0,0),(0,0)));s=p.index(((4,0),(0,0),(0,0),(0,0)))
    rem=[f for f in t if n not in f];link=boundary(rem);seam=induced(rem,link)
    require(len(link)==20 and len(seam)==12,'single puncture boundary')
    double=sorted(rem+[tuple(sorted(v if v in seam else v+len(p) for v in f)) for f in rem]);ds,dtcp=complex_checks(double)
    require(set(dtcp)==set(link),'connected-sum violating triangles are not exactly seam')
    require(ds['betti_mod2']==[1,0,0,1] and ds['orientable'],'double control')
    rem=[f for f in t if n not in f and s not in f]
    l0=sorted(tuple(x for x in f if x!=n) for f in t if n in f);l1=sorted(tuple(x for x in f if x!=s) for f in t if s in f)
    v0=induced(rem,l0);v1=induced(rem,l1)
    require(v0.isdisjoint(v1) and all(not(set(f)&v0 and set(f)&v1) for f in rem),'unsafe two-puncture quotient')
    require(set(boundary(rem))==set(l0+l1),'two punctures have wrong boundary')
    image={i:p.index(tuple(q if k==1 else negative(q) for k,q in enumerate(v))) for i,v in enumerate(p)}
    require(all(image[image[i]]==i for i in image),'symmetry not involutive')
    require({tuple(sorted(image[v] for v in f)) for f in t}==set(t),'not full simplicial symmetry')
    bc={}
    for f in rem:
        for k in range(4):
            face=f[:k]+f[k+1:];bc[face]=bc.get(face,0)+((-1)**k)*det_signs[f]
    require(set(f for f,c in bc.items() if c)!=set(),'boundary orientation missing')
    require(all(c==0 for f,c in bc.items() if f not in set(l0+l1)),'geometric orientations not coherent')
    for f in l0:
        raw=tuple(image[x] for x in f);target=tuple(sorted(raw));require(bc[f]*parity(raw)==-bc[target],'self-handle map does not reverse induced boundary orientations')
    # All simplex fibers, not just vertices/tetrahedra, must match the intended
    # boundary quotient. No simplex meeting both boundary sets is insufficient.
    quotient_fibers=[]
    for k in range(1,5):
        original={f for t in rem for f in C(t,k)};fibers=collections.defaultdict(list)
        for f in original:fibers[tuple(sorted(image[v] if v in v1 else v for v in f))].append(f)
        for target,old in fibers.items():
            require(all(len(target)==len(f) for f in old),'quotient collapses simplex')
            if len(old)>1:
                require(len(old)==2,'quotient fiber has more than two members')
                a,b=old
                require((set(a)<=v0 and set(b)<=v1) or (set(a)<=v1 and set(b)<=v0),'extra quotient identification outside boundary')
                require(tuple(sorted(image[v] for v in a))==b,'wrong boundary quotient pair')
        quotient_fibers.append({'dimension':k-1,'original_simplices':len(original),'quotient_simplices':len(fibers),'paired_boundary_simplices':sum(len(fs)==2 for fs in fibers.values()),'extra_collisions':0})
    handle=sorted(tuple(sorted(image[v] if v in v1 else v for v in f)) for f in rem);hs,htcp=complex_checks(handle)
    require(set(htcp)==set(l0),'handle violating triangles are not exactly seam')
    require(hs['betti_mod2']==[1,1,1,1] and hs['orientable'],'handle control')
    antipodal={i:p.index(tuple(negative(q) for q in v)) for i,v in enumerate(p)}
    wrong=sorted(tuple(sorted(antipodal[v] if v in v1 else v for v in f)) for f in rem);ws,_=complex_checks(wrong)
    require(not ws['orientable'],'orientation-preserving boundary gluing incorrectly orientable')
    rejected=[]
    for label,data in [('deleted facet',t[:-1]),('duplicated facet',t+[t[0]]),('collapsed facet',[(0,0,1,2)]+t[1:])]:
        try:complex_checks(data)
        except (ValueError,KeyError):rejected.append(label)
        else:raise ValueError('bad complex accepted: '+label)
    try:author.analyze(wrong)
    except author.Invalid:rejected.append('wrong self-handle boundary orientation')
    else:raise ValueError('author accepted nonorientable self-handle')
    # Independent field oracle: isolate sqrt(5) by the certified rational interval.
    lo,hi=2236067977499789696409173668731276235,2236067977499789696409173668731276236;den=10**36
    require(lo*lo<5*den*den<hi*hi,'invalid radical enclosure')
    for a in range(-100,101):
        for b in range(-100,101):
            lower=a*den+b*(lo if b>=0 else hi);upper=a*den+b*(hi if b>=0 else lo)
            expected=0 if (a,b)==(0,0) else (1 if lower>0 else -1 if upper<0 else None)
            require(expected is not None and sgn((a,b))==expected,'independent sign arithmetic')
            require(author.sign((a,b))==sgn((2*a+b,b)),'author phi sign differs')
    report={'schema':1,'status':'pass','problem_id':30000433,'independent_geometry':{'coefficient_ring':'Z[sqrt(5)], coordinates twice author coordinates','vertices':len(p),'facets':len(t),'support_comparisons':len(p)*len(t),'strict_comparisons':strict,'equalities':support_equalities,'facet_determinants_nonzero':len(det_signs)},'six_hundred_cell':base,'double':ds,'self_handle':hs,'quotient_fibers':quotient_fibers,'orientation_control':{'antipodal_gluing_orientable':ws['orientable'],'induced_boundary_orientation_reversals':len(l0)},'sign_checks':40401,'mutation_rejections':rejected,'claim_limits':['Homology is corroboration, not manifold recognition.','Topological identifications use the written convex-polytope and PL-surgery arguments.','The universal 5/6 and TCP questions remain unresolved.']}
    print(json.dumps(report,sort_keys=True,indent=2))
if __name__=='__main__':main()
