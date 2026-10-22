#!/usr/bin/env python3
"""Fresh exact finite controls; no author code, solver or third-party imports."""
import itertools as it
import json
import math
from collections import Counter, deque
from fractions import Fraction as F


class Rejected(ValueError):pass
def need(ok,why):
    if not ok:raise Rejected(why)


def subsets(a):
    a=tuple(sorted(a))
    return (frozenset(x) for n in range(len(a)+1) for x in it.combinations(a,n))


def closure(facets):return frozenset(s for a in facets for s in subsets(a))
def vertices(C):return set().union(*C) if C else set()
def dim(C):return max(map(len,C),default=0)-1
def faces(C,k):return sorted((tuple(sorted(a)) for a in C if len(a)==k+1))
def link(C,a):
    a=frozenset(a)
    return frozenset(f-a for f in C if a<=f)
def induced(C,A):return frozenset(f for f in C if f<=A)
def fvector(C):return [len(faces(C,k)) for k in range(dim(C)+1)]
def check_complex(C):
    need(frozenset() in C,'empty face')
    need(all(s in C for a in C for s in subsets(a)),'closure under subfaces')
def boundary(C):
    d=dim(C);top=faces(C,d)
    counts=Counter(frozenset(s) for a in top for s in it.combinations(a,d))
    need(all(v in (1,2) for v in counts.values()),'ridge incidence at most two')
    return closure(a for a,v in counts.items() if v==1)


def components(C,A=None):
    V=vertices(C) if A is None else set(A)
    adjacency={v:set() for v in V}
    for a,b in faces(C,1):
        if a in V and b in V:adjacency[a].add(b);adjacency[b].add(a)
    groups=[]
    while V:
        start=min(V);seen={start};todo=[start]
        while todo:
            for w in adjacency[todo.pop()]:
                if w not in seen:seen.add(w);todo.append(w)
        groups.append(seen);V-=seen
    return groups


def rank(A,p):
    need(p in (2,3,5),'coefficient is a tested prime field')
    if not A:return 0
    a=[[x%p for x in row] for row in A];rows=len(a);cols=len(a[0]);pivot=0
    for j in range(cols):
        i=next((i for i in range(pivot,rows) if a[i][j]),None)
        if i is None:continue
        a[pivot],a[i]=a[i],a[pivot];inv=pow(a[pivot][j],-1,p)
        a[pivot]=[(x*inv)%p for x in a[pivot]]
        for i in range(pivot+1,rows):
            if a[i][j]:
                q=a[i][j];a[i]=[(x-q*y)%p for x,y in zip(a[i],a[pivot])]
        pivot+=1
        if pivot==rows:break
    return pivot


def differential(C,k):
    rows=faces(C,k-1);cols=faces(C,k);index={a:i for i,a in enumerate(rows)}
    A=[[0]*len(cols) for _ in rows]
    for j,a in enumerate(cols):
        for q in range(k+1):A[index[a[:q]+a[q+1:]]][j]=(-1)**q
    return A


def betti(C,p):
    d=dim(C);f=fvector(C);r=[0]+[rank(differential(C,k),p) for k in range(1,d+1)]+[0]
    return [f[k]-r[k]-r[k+1] for k in range(d+1)]


def closed_three(C):
    check_complex(C);need(dim(C)==3,'dimension three')
    need(all(any(a<=frozenset(t) for t in faces(C,3)) for a in C),'purity')
    need(len(components(C))==1,'connectedness')
    counts=Counter(frozenset(t) for a in faces(C,3) for t in it.combinations(a,3))
    need(all(x==2 for x in counts.values()),'closed triangle incidence')
    for v in vertices(C):
        L=link(C,{v});need(dim(L)==2,'surface link dimension')
        edges=Counter(frozenset(e) for a in faces(L,2) for e in it.combinations(a,2))
        need(all(x==2 for x in edges.values()),'surface link closed edges')
        need(len(components(L))==1 and sum((-1)**i*x for i,x in enumerate(fvector(L)))==2,'connected spherical link')
        for u in vertices(L):
            LL=link(L,{u});deg=Counter(x for e in faces(LL,1) for x in e)
            need(all(x==2 for x in deg.values()) and len(components(LL))==1,'link surface vertex cycles')


def orientable(C):
    top=faces(C,dim(C));ridge={}
    for i,a in enumerate(top):
        for k in range(len(a)):
            b=a[:k]+a[k+1:];ridge.setdefault(b,[]).append((i,(-1)**k))
    adj=[[] for _ in top]
    for entries in ridge.values():
        if len(entries)==2:
            (i,s),(j,t)=entries;adj[i].append((j,-s*t));adj[j].append((i,-s*t))
    signs={}
    for root in range(len(top)):
        if root in signs:continue
        signs[root]=1;todo=[root]
        while todo:
            i=todo.pop()
            for j,q in adj[i]:
                x=signs[i]*q
                if j in signs:
                    if signs[j]!=x:return False
                else:signs[j]=x;todo.append(j)
    return True


def h1_presentation(C):
    E=faces(C,1);parent={v:v for v in vertices(C)}
    def find(v):
        while parent[v]!=v:v=parent[v]
        return v
    chords=[]
    for a,b in E:
        x,y=find(a),find(b)
        if x==y:chords.append((a,b))
        else:parent[x]=y
    T=faces(C,2);indices={e:i for i,e in enumerate(chords)}
    A=[[0]*len(T) for _ in chords]
    for j,(a,b,c) in enumerate(T):
        for e,s in [((b,c),1),((a,c),-1),((a,b),1)]:
            if e in indices:A[indices[e]][j]=s
    return A,chords


def unit_reduce(A):
    """A verified sequence of integral unit pivots suffices for these examples."""
    a=[row[:] for row in A]
    if not a:return 0,[]
    nr,nc=len(a),len(a[0]);k=0
    while k<min(nr,nc):
        found=next(((i,j) for i in range(k,nr) for j in range(k,nc) if abs(a[i][j])==1),None)
        if found is None:break
        i,j=found;a[k],a[i]=a[i],a[k]
        for row in a:row[k],row[j]=row[j],row[k]
        if a[k][k]==-1:a[k]=[-x for x in a[k]]
        for i in range(k+1,nr):
            q=a[i][k]
            if q:a[i]=[x-q*y for x,y in zip(a[i],a[k])]
        for j in range(k+1,nc):
            q=a[k][j]
            if q:
                for i in range(nr):a[i][j]-=q*a[i][k]
        k+=1
    return k,[row[k:] for row in a[k:]]


def separation(C):
    V=sorted(vertices(C));m=len(V);out=F(0)
    for A in subsets(V):out+=F(len(components(C,A))-1,math.comb(m,len(A)))
    return out


def mu_pair(C):
    u0=u1=F(0)
    for v in vertices(C):
        L=link(C,{v});m=len(vertices(L));s=separation(L)
        need(s==F((m-8)*(m+1),20),'stacked sphere link separation equality')
        u0+=F(1,m+1);u1+=(1+s)/F(m+1)
    return u0,u1


def null_cochain(C,p):
    A,chords=h1_presentation(C);a=[list(x) for x in zip(*A)];nr=len(a);nc=len(chords);piv=[];r=0
    for j in range(nc):
        i=next((i for i in range(r,nr) if a[i][j]%p),None)
        if i is None:continue
        a[r],a[i]=a[i],a[r];inv=pow(a[r][j]%p,-1,p);a[r]=[(x*inv)%p for x in a[r]]
        for i in range(nr):
            if i!=r:
                q=a[i][j]%p
                if q:a[i]=[(x-q*y)%p for x,y in zip(a[i],a[r])]
        piv.append(j);r+=1
    free=[j for j in range(nc) if j not in piv];need(len(free)==1,'one-dimensional first cohomology')
    z=[0]*nc;z[free[0]]=1
    for i,j in reversed(list(enumerate(piv))):z[j]=-sum(a[i][k]*z[k] for k in free)%p
    need(all(sum(x*y for x,y in zip(row,z))%p==0 for row in zip(*A)),'cochain annihilates triangle relations')
    return {e:z[i] for i,e in enumerate(chords)}


def induced_injectivity(C,p):
    co=null_cochain(C,p);V=vertices(C);count=0
    for S in subsets(V):
        Y=induced(C,S);E=faces(Y,1);groups=components(Y);T=faces(Y,2)
        if not S:beta=0
        else:beta=len(E)-len(S)+len(groups)-rank(differential(Y,2),p)
        adjacency={v:[] for v in S}
        for a,b in E:
            w=co.get((a,b),0);adjacency[a].append((b,w));adjacency[b].append((a,-w))
        pot={};nonzero=False
        for group in groups:
            root=min(group);pot[root]=0;todo=[root]
            while todo:
                a=todo.pop()
                for b,w in adjacency[a]:
                    value=(pot[a]+w)%p
                    if b in pot:nonzero|=pot[b]!=value
                    else:pot[b]=value;todo.append(b)
        need(beta==int(nonzero),'every induced H1 map injective')
        count+=1
    return count


def cutting(C,sigma,literal=False):
    sigma=frozenset(sigma);R={a for a in C if a&sigma and not a<=sigma}
    top=[frozenset(a) for a in faces(C,dim(C)) if sigma<=set(a)]
    need(len(top)==2,'cut face has two incident facets')
    x=min(top[0]-sigma);y=min(top[1]-sigma);X=set();Y=set()
    for z in sigma:
        L=link(C,{z});G=components(L,vertices(L)-sigma)
        need(len(G)==2,'two sides in each vertex link')
        cx=next(g for g in G if x in g);cy=next(g for g in G if y in g)
        need(cx!=cy,'opposite facets on different sides')
        for side,out in [(cx,X),(cy,Y)]:
            if literal:
                for a in R&set(L):
                    if a<=side|(sigma-{z}):out.add(a|{z})
            else:
                for a in R:
                    if z in a and a-{z}<=side|(sigma-{z}):out.add(a)
    if not literal:need(X|Y==R and not X&Y,'corrected cut side partition')
    new={z:max(vertices(C))+1+i for i,z in enumerate(sorted(sigma))}
    rename=lambda a:frozenset(new.get(v,v) for v in a)
    cut=frozenset((set(C)-X)|{rename(a) for a in X}|set(subsets(new.values())))
    return cut,R,X,Y,new


def cutting_checks():
    records=[]
    for d in range(2,6):
        sig=set(range(d));C=closure([sig|{d},sig|{d+1}]);B=boundary(C)
        need(frozenset(sig) not in B and all(a in B for a in subsets(sig) if a!=frozenset(sig)),'valid interior cutting hypotheses')
        bad,R,X,Y,new=cutting(C,sig,True)
        need(frozenset({0,d}) in R-(X|Y),'literal omitted edge')
        literal_missing=len(R-(X|Y))
        try:check_complex(bad)
        except Rejected:pass
        else:raise Rejected('literal cutting defect not detected')
        fixed,R,X,Y,new=cutting(C,sig)
        check_complex(fixed);need(len(components(fixed))==2,'two simplex pieces')
        inverse={v:k for k,v in new.items()}
        quotient=frozenset(frozenset(inverse.get(v,v) for v in a) for a in fixed)
        need(quotient==C,'correct cut recovers original under gluing')
        records.append({'d':d,'literal_omitted_faces':literal_missing,'corrected_components':2})
    C=closure([set(range(i,i+5)) for i in range(12)])
    for i in range(11):
        sigma=set(range(i+1,i+5));fixed,_,_,_,_=cutting(C,sigma)
        check_complex(fixed);need(len(components(fixed))==2,'path stacked-ball cuts separate')
        f=[frozenset(a) for a in faces(fixed,4)]
        need(len(f)==12,'cut preserves top facets')
    return {'two_simplex_dimensions':records,'additional_path_ball_cuts':11}


def example_checks():
    W=closure([set(range(i,i+5)) for i in range(12)]);K=boundary(W);closed_three(K)
    need(fvector(K)==[16,54,76,38],'initial stacked sphere face vector')
    need(all((frozenset({i,j}) in K)==(j-i<=4) for i in range(16) for j in range(i+1,16)),'interval sphere graph')
    need(mu_pair(K)[1]-mu_pair(K)[0]==-1,'sphere mu difference')
    sigma=(0,1,2,3);tau=(12,13,14,15);out=[];reps={}
    for perm in it.permutations(tau):
        mapping=dict(zip(sigma,perm))
        for a,b in mapping.items():
            need(not any(a in e and b in e for e in K if len(e)==2),'no identified edge')
            need(not (vertices(link(K,{a}))&vertices(link(K,{b}))),'no identified common neighbor')
        C=frozenset(frozenset(mapping.get(v,v) for v in a) for a in K if a not in (frozenset(sigma),frozenset(tau)))
        check_complex(C);closed_three(C);need(fvector(C)==[12,48,72,36],'handle face counts')
        need(len(faces(C,1))-4*len(vertices(C))+10==10,'handle g2 ten')
        orientation=orientable(C);Bs={p:betti(C,p) for p in (2,3,5)}
        need(all(v[1]==1 for v in Bs.values()),'all tested first Betti numbers')
        need(Bs[2][3]==1 and Bs[3][3]==int(orientation),'orientation homology control')
        A,_=h1_presentation(C);units,remainder=unit_reduce(A)
        need(all(not x for row in remainder for x in row) and len(A)-units==1,'integral H1 is free rank one')
        mu0,mu1=mu_pair(C);need(mu1-mu0==0 and mu0>1,'new mu formula without neighborliness')
        if orientation not in reps:reps[orientation]=C
        out.append({'bijection':perm,'orientable':orientation,'face_vector':fvector(C),'betti':Bs,
                    'integer_H1_free_rank':1,'mu0':str(mu0),'mu1':str(mu1)})
    need(sum(x['orientable'] for x in out)==12,'both bundle orientation types')
    induced_counts=[]
    for orientation,C in reps.items():
        for p in (2,3):induced_counts.append({'orientable':orientation,'field':p,'subsets':induced_injectivity(C,p)})
    # Field dependence is not assumed for arbitrary complexes: a standard RP2 foil.
    rp=closure([(1,2,3),(1,2,4),(1,3,5),(1,4,6),(1,5,6),(2,3,6),(2,4,5),(2,5,6),(3,4,5),(3,4,6)])
    need(betti(rp,2)[1]==1 and betti(rp,3)[1]==0,'torsion field-dependence foil')
    octa=closure([a for a in it.product((0,1),(2,3),(4,5))])
    need(separation(octa)<F((6-8)*(6+1),20),'nonstacked sphere strict separation')
    # An induced missing triangle is nonzero but is killed by its cone over a new vertex.
    triangle=closure([(0,1),(1,2),(0,2)]);cone=closure([{3}|set(a) for a in triangle])
    need(betti(triangle,2)[1]==1 and betti(cone,2)[1]==0,'missing triangle cone contradiction')
    # Connected sum face count and g2 arithmetic, using disjoint copies of two blocks.
    blocks=list(reps.values());A=blocks[0];B=frozenset(frozenset(v+100 for v in a) for a in blocks[1])
    fa=faces(A,3)[0];fb=faces(B,3)[0];mapping=dict(zip(fb,fa))
    Sum=frozenset((set(A)-{frozenset(fa)})|{frozenset(mapping.get(v,v) for v in a) for a in B if a!=frozenset(fb)})
    closed_three(Sum);need(fvector(Sum)==[20,90,140,70],'connected sum face vector')
    need(len(faces(Sum,1))-4*len(vertices(Sum))+10==20 and betti(Sum,2)[1]==2,'connected sum additive control')
    return {'gluing_cases':out,'induced_H1_checks':induced_counts,'RP2_foil_betti':{2:betti(rp,2),3:betti(rp,3)},
            'octahedron_separation':str(separation(octa)),'connected_sum_faces':fvector(Sum)}


def corruption_checks():
    sphere=boundary(closure([set(range(5))]));results=[]
    sf=fvector(sphere)
    def reject(name,f):
        try:f()
        except Rejected as e:results.append({'name':name,'rejected':True,'reason':str(e)})
        else:raise Rejected('corruption survived: '+name)
    reject('remove_subface',lambda:check_complex(sphere-{frozenset({0,1})}))
    reject('remove_top_facet',lambda:closed_three(sphere-{frozenset((0,1,2,3))}))
    reject('nonfield_modulus',lambda:rank([[1,2],[2,0]],4))
    reject('wrong_constant_shift',lambda:need(sf[1]-4*sf[0]==0,'g2 needs plus ten'))
    reject('wrong_handle_edge_change',lambda:need(54-5==48,'handle loses six edges'))
    reject('disconnected_extension',lambda:need(-10>=0,'unadjusted bound requires connectedness'))
    reject('omit_empty_separation_term',lambda:need(separation(closure(it.combinations(range(4),3)))+1==-1,'empty subset contributes minus one'))
    rp=closure([(1,2,3),(1,2,4),(1,3,5),(1,4,6),(1,5,6),(2,3,6),(2,4,5),(2,5,6),(3,4,5),(3,4,6)])
    reject('field_independence_for_all_complexes',lambda:need(betti(rp,2)[1]==betti(rp,3)[1],'RP2 foil first Betti numbers differ'))
    return results


def relative_morse_checks():
    """All orderings of an octahedral sphere; its H1 injections are not all injective."""
    C=closure([a for a in it.product((0,1),(2,3),(4,5))]);V=sorted(vertices(C));records=[]
    def relative_pair(B,A,p):
        lists=[[a for a in faces(B,k) if frozenset(a) not in A] for k in range(3)]
        ranks=[]
        for k in (1,2):
            index={a:i for i,a in enumerate(lists[k-1])};mat=[[0]*len(lists[k]) for _ in lists[k-1]]
            for j,a in enumerate(lists[k]):
                for q in range(k+1):
                    b=a[:q]+a[q+1:]
                    if b in index:mat[index[b]][j]=(-1)**q
            ranks.append(rank(mat,p))
        return len(lists[0])-ranks[0],len(lists[1])-ranks[0]-ranks[1]
    u0=sum((F(1,len(vertices(link(C,{v})))+1) for v in V),F(0))
    u1=sum(((1+separation(link(C,{v})))/F(len(vertices(link(C,{v})))+1) for v in V),F(0))
    for p in (2,3):
        total0=total1=kernels=orders=0
        for order in it.permutations(V):
            S=set();A=induced(C,S);ba=[0,0]
            for v in order:
                S.add(v);B=induced(C,S);bb=betti(B,p);bb=(bb+[0,0])[:2]
                r0,r1=relative_pair(B,A,p)
                kernel=r1-r0-(bb[1]-ba[1]-bb[0]+ba[0])
                need(kernel>=0,'relative Morse kernel nonnegative')
                total0+=r0;total1+=r1;kernels+=kernel;A=B;ba=bb
            orders+=1
        need(F(total0,orders)==u0 and F(total1,orders)==u1,'all-order relative averaging equals new mu')
        need(u1-u0+1==F(kernels,orders)==F(1,5),'strict Morse gap detects killed induced cycles')
        records.append({'field':p,'orders':orders,'one_vertex_pairs':orders*len(V),'mu0':str(u0),'mu1':str(u1),'average_kernel_sum':str(F(kernels,orders))})
    return records


def main():
    result={'schema':'fresh-three-manifold-prior-coverage-controls-1','exact_arithmetic':'integers, prime fields, rational separation',
            'author_code_executed':False,'source_code_executed':False,'guard_style':'explicit exceptions',
            'cutting':cutting_checks(),'examples':example_checks(),'relative_Morse':relative_morse_checks(),
            'negative_controls':corruption_checks()}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
