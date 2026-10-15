"""Audit-owned exact cyclotomic model. No submission imports; guards survive -O.
Rational vectors in Q[T]/Phi5, matrix inversion, reflected polygons, support planes.
Literal face/word data are public mathematical inputs, not executable code.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from collections import Counter, deque
import cmath, json, math

def require(ok, message):
    if not ok: raise ValueError(message)

class C:
    __slots__ = ('v',)
    def __init__(self, x=0):
        self.v = x.v if isinstance(x,C) else ((Q(x),Q(0),Q(0),Q(0)) if not isinstance(x,(list,tuple)) else tuple(map(Q,x)))
        require(len(self.v)==4, 'field dimension')
    def __add__(self,x):
        x=C(x); return C([a+b for a,b in zip(self.v,x.v)])
    __radd__=__add__
    def __neg__(self): return C([-a for a in self.v])
    def __sub__(self,x): return self+-C(x)
    def __rsub__(self,x): return C(x)+-self
    def __mul__(self,x):
        x=C(x); a=[Q(0)]*7
        for i in range(4):
            for j in range(4): a[i+j]+=self.v[i]*x.v[j]
        for k in range(6,3,-1):
            for j in range(1,5): a[k-j]-=a[k]
        return C(a[:4])
    __rmul__=__mul__
    def inv(self):
        basis=[C([int(i==j) for i in range(4)]) for j in range(4)]
        columns=[(self*b).v for b in basis]
        rows=[[columns[j][i] for j in range(4)]+[Q(i==0)] for i in range(4)]
        for j in range(4):
            k=next((i for i in range(j,4) if rows[i][j]),None)
            require(k is not None, 'division by zero')
            rows[j],rows[k]=rows[k],rows[j]
            scale=rows[j][j]; rows[j]=[a/scale for a in rows[j]]
            for i in range(4):
                if i!=j:
                    scale=rows[i][j];rows[i]=[a-scale*b for a,b in zip(rows[i],rows[j])]
        return C([rows[i][4] for i in range(4)])
    def __truediv__(self,x): return self*C(x).inv()
    def conj(self):
        powers=[ONE, T*T*T*T, T*T*T, T*T]
        return sum((a*b for a,b in zip(self.v,powers)),ZERO)
    def __eq__(self,x): return self.v==C(x).v
    def __hash__(self): return hash(self.v)
    def real_pair(self):
        a,b,c,d=self.v
        require(b==0 and c==d,'not real')
        return a-c/2,-c/2
    def sign(self):
        a,b=self.real_pair()
        if not b: return (a>0)-(a<0)
        if not a: return (b>0)-(b<0)
        if (a>0)==(b>0): return (a>0)-(a<0)
        cmp=a*a-5*b*b
        return ((a>0)-(a<0))*((cmp>0)-(cmp<0))
    def data(self): return [str(a) for a in self.v]
    def pairdata(self): return [str(a) for a in self.real_pair()]
    def approximate(self): return sum(float(a)*cmath.exp(2j*math.pi*k/5) for k,a in enumerate(self.v))

ZERO=C(); ONE=C(1); T=C([0,1,0,0])
SQRT5=ONE+2*(T+T.conj()); PHI=(ONE+SQRT5)/2

def dot(a,b): return sum((x*y for x,y in zip(a,b)),ZERO)
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def scale(k,a): return tuple(k*x for x in a)
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def det(a,b): return (a.conj()*b-a*b.conj())/(T-T.conj())
def norm(a): return a*a.conj()
def reflect(z,a,b):
    d=b-a
    return a+d*d*(z-a).conj()/norm(d)

def model3d():
    ip=ONE/PHI
    vertices=[tuple(C(t) for t in signs) for signs in product([-1,1], repeat=3)]
    for s,t in product([-1,1], repeat=2):
        vertices.extend([(ZERO,s*ip,t*PHI),(s*ip,t*PHI,ZERO),(s*PHI,ZERO,t*ip)])
    edge_length=4*ip*ip
    edges={frozenset((i,j)) for i,j in combinations(range(20),2) if dot(sub(vertices[i],vertices[j]),sub(vertices[i],vertices[j]))==edge_length}
    require(len(edges)==30,'edge count')
    graph={i:{next(iter(e-{i})) for e in edges if i in e} for i in range(20)}
    require(all(len(s)==3 for s in graph.values()),'degree')
    faces=set()
    for i,j,k in combinations(range(20),3):
        n=cross(sub(vertices[j],vertices[i]),sub(vertices[k],vertices[i]))
        if dot(n,n)==0: continue
        vals=[dot(n,sub(v,vertices[i])).sign() for v in vertices]
        if 1 in vals and -1 in vals: continue
        on=frozenset(i for i,s in enumerate(vals) if s==0)
        require(len(on)==5,'support face size')
        faces.add(on)
    require(len(faces)==12,'face count')
    for face in faces:
        require(all(len(graph[i]&face)==2 for i in face),'pentagonal face graph')
        require(len({dot(sub(vertices[i],vertices[j]),sub(vertices[i],vertices[j])) for i,j in combinations(face,2)})==2,'regular face distances')
    require(all(sum(e<=f for f in faces)==2 for e in edges),'two faces per edge')
    dists={}
    for start in graph:
        ds={start:0}; q=deque([start])
        while q:
            i=q.popleft()
            for j in graph[i]-ds.keys(): ds[j]=ds[i]+1;q.append(j)
        require(Counter(ds.values())=={0:1,1:3,2:6,3:6,4:3,5:1},'distance census')
        dists[start]=ds
    axes={}; results=[]
    for edge in sorted(map(sorted,edges)):
        i,j=edge; a=add(vertices[i],vertices[j]); a2=dot(a,a)
        perm=[vertices.index(sub(scale(2*dot(v,a)/a2,a),v)) for v in vertices]
        require(len(set(perm))==20 and all(perm[perm[i]]==i and perm[i]!=i for i in range(20)),'free involution')
        require(perm[i]==j,'edge swap')
        require(all(frozenset(perm[i] for i in e) in edges for e in edges),'graph symmetry')
        require(all(frozenset(perm[i] for i in f) in faces for f in faces),'face symmetry')
        hist=Counter(dists[i][perm[i]] for i in range(20))
        require(hist=={1:4,3:8,4:4,5:4},'half-turn distances')
        results.append({'edge':edge,'permutation':perm,'histogram':dict(sorted(hist.items()))})
        key=tuple(perm);axes[key]=axes.get(key,0)+1
    require(len(axes)==15 and set(axes.values())=={2},'opposite edge axes')
    return vertices,edges,faces,graph,results

FACES=[[6,18,4,8,10],[10,8,0,16,2],[17,16,0,12,1],[3,13,2,16,17],[5,9,1,12,14],[14,12,0,8,4],[5,14,4,18,19],[3,17,1,9,11],[11,9,5,19,7],[6,10,2,13,15],[19,18,6,15,7],[15,13,3,11,7]]
WORD=[1,3,11,8,6,5,1,3,11,10,8,6,4,5,2,1]
EDGES=[(2,16),(3,13),(7,11),(5,19),(4,14),(0,8),(2,16),(3,13),(7,15),(7,19),(5,19),(5,14),(12,14),(0,12),(0,16)]

def cycles(face,first):
    i=face.index(first)
    return face[i:]+face[:i]

def develop(word=WORD):
    initial=cycles(FACES[word[0]],0)
    require(initial[1]==16,'initial side')
    points=[ZERO]
    for edge in [ONE,T,T*T,T*T*T]: points.append(points[-1]+edge)
    polys=[dict(zip(initial,points))]
    labels=[{v:i for i,v in enumerate(initial)}]
    for f0,f1 in zip(word,word[1:]):
        shared=set(FACES[f0])&set(FACES[f1]);require(len(shared)==2,'face adjacency')
        u,v=sorted(shared); old=polys[-1]
        a=cycles(FACES[f0],u);b=cycles(FACES[f1],u)
        require(a[1]==v or a[-1]==v,'shared boundary edge')
        require((a[1]==v)!=(b[1]==v),'opposite orientation')
        reflected=[reflect(old[x],old[u],old[v]) for x in a]
        b=[b[0]]+b[:0:-1]
        new=dict(zip(b,reflected))
        require(new[u]==old[u] and new[v]==old[v],'shared coordinates')
        labels.append({y:labels[-1][x] for x,y in zip(a,b)})
        polys.append(new)
    return polys,labels

def graph_map(physical,geometric):
    used=set(); mapping={}
    def visit():
        if len(mapping)==20: return True
        v=max((v for v in physical if v not in mapping),key=lambda v:len(physical[v]&mapping.keys()))
        for w in geometric:
            if w in used:continue
            if any((n in physical[v])!=(mapping[n] in geometric[w]) for n in mapping):continue
            mapping[v]=w;used.add(w)
            if visit():return True
            used.remove(w);del mapping[v]
        return False
    require(visit(),'public graph isomorphic to exact solid')
    return mapping

def witness(model):
    vertices,edges,faces,graph,turns=model
    physical={i:set() for i in range(20)}
    for face in FACES:
        for i,j in zip(face,face[1:]+face[:1]): physical[i].add(j);physical[j].add(i)
    mapping=graph_map(physical,graph)
    require(all(frozenset(mapping[i] for i in f) in faces for f in FACES),'literal faces on solid')
    polys,labels=develop();end=polys[-1][2]
    require(norm(end)==(307+137*SQRT5)/2,'witness length')
    crossings=[];last=ZERO
    for i,(u,v) in enumerate(EDGES):
        a=polys[i][u];b=polys[i][v];d=b-a
        t=det(a,d)/det(end,d);s=det(a,end)/det(end,d)
        require(t.sign()>0 and (1-t).sign()>0,'crossing time interior')
        require(s.sign()>0 and (1-s).sign()>0,'crossing edge interior')
        require((t-last).sign()>0 and end*t==a+s*d,'ordered crossing')
        crossings.append((t,s));last=t
    cuts=[ZERO]+[t for t,s in crossings]+[ONE];hits=[]
    for k,poly in enumerate(polys):
        f=FACES[WORD[k]];mid=end*(cuts[k]+cuts[k+1])/2
        require(all(det(poly[j]-poly[i],mid-poly[i]).sign()>0 for i,j in zip(f,f[1:]+f[:1])),'strict face containment')
        for label,p in poly.items():
            if det(end,p)==0:
                t=p/end
                if t.sign()>=0 and (1-t).sign()>=0:hits.append([k,label,t.pairdata()])
    require(hits==[[0,0,['0','0']],[15,2,['1','0']]],'first subsequent vertex')
    end_label=labels[-1][2]
    terminal_next=next(v for v,k in labels[-1].items() if k==(end_label+1)%5)
    source_ray=polys[-1][terminal_next]-end;physical_ray=polys[-1][10]-end
    require(terminal_next==16 and source_ray==T*T*T,'transported endpoint ray')
    require(physical_ray*T==-ONE,'physical endpoint ray')
    require(det(ONE,end).sign()>0 and det(end,-T*T*T).sign()>0,'alpha between 0 and 36 degrees')
    alpha=cmath.phase(end.approximate())*180/math.pi
    direct=[];p=list(polys[0].values())
    for j in range(1,5):
        ray=p[(j+1)%5]-p[j];z=p[j]
        a=cmath.phase(z.approximate())*180/math.pi
        interior=abs((cmath.phase(ray.approximate())*180/math.pi-cmath.phase((-z).approximate())*180/math.pi+180)%360-180)
        direct.append({'target_index':j,'alpha':a,'beta':180-interior,'bare_difference':180-interior-a})
    return {'literal_to_3d_graph_isomorphism':mapping,'end_cyclotomic_coefficients':end.data(),'squared_length_pair':norm(end).pairdata(),'crossings':[{'t':t.pairdata(),'s':s.pairdata()} for t,s in crossings],'vertex_hits':hits,'terminal_transported_next_vertex':terminal_next,'terminal_label_map':labels[-1],'source_ray_coefficients':source_ray.data(),'physical_ray_coefficients':physical_ray.data(),'alpha_degrees_display':alpha,'beta_minus_alpha_exact_degrees':144,'direct_diagonal_controls_display':direct}

if __name__=='__main__':
    require(T*T*T*T*T==ONE,'root of unity')
    require(SQRT5*SQRT5==5 and SQRT5.sign()>0,'positive square root')
    m=model3d()
    print(json.dumps({'arithmetic':'Q[T]/Phi5; Gaussian elimination; exact real sign tests','vertex_count':len(m[0]),'edge_count':len(m[1]),'supporting_faces':sorted(map(sorted,m[2])),'axis_count':15,'half_turns':m[4],'witness':witness(m)},indent=2))
