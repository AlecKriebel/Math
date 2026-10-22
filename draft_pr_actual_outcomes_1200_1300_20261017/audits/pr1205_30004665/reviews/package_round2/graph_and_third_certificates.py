"""Independent standard-library graph, chamber, and third-certificate checks.

No candidate functions imported. Uses positive-arrow path mutation. The
chamber/braid comparison reduces rational monomials to x^e(uw+v)^q signatures.
"""
from collections import deque, Counter
import json, pathlib
HERE=pathlib.Path(__file__).resolve().parent
V=HERE.parent.parent/'publication/verification'
word=(1,2,3,2,4,2,1,2,3,2,4,2);N=12
adj=lambda a,b:abs(a-b)==1 and {a,b}<={1,2,3} or {a,b}=={2,4}

def require(x,m):
    if not x:raise ValueError(m)

def seed(w):
    nx=[next((j for j in range(i+1,N) if w[i]==w[j]),N) for i in range(N)]
    fr={i for i,t in enumerate(nx) if t==N};A=Counter();M=[]
    for i in range(N):
        if nx[i]<N:A[i,nx[i]]+=1
        for j in range(i+1,N):
            if j<nx[i]<nx[j] and adj(w[i],w[j]):A[j,i]+=1
        M.append([-1 if j in (i,nx[i]) else (1 if adj(w[i],w[j]) else -2 if w[i]==w[j] else 0) if i<j<nx[i] else 0 for j in range(N)])
    return Counter({(a,b):v for (a,b),v in A.items() if not {a,b}<=fr}),fr,M

def mutate(A,k,fr):
    require(k not in fr,'mutable')
    C=A.copy()
    incoming=[(a,v) for (a,b),v in A.items() if b==k]
    outgoing=[(b,v) for (a,b),v in A.items() if a==k]
    for a,v in incoming:
        for b,t in outgoing:
            if a!=b:C[a,b]+=v*t
    for (a,b),v in A.items():
        if k in (a,b):C[a,b]-=v;C[b,a]+=v
    for a in range(N):
        for b in range(a+1,N):
            t=min(C[a,b],C[b,a]);C[a,b]-=t;C[b,a]-=t
    return Counter({(a,b):v for (a,b),v in C.items() if v and not {a,b}<=fr})

def moves(w):
    for t in range(N-1):
        if w[t]!=w[t+1] and not adj(w[t],w[t+1]):
            v=list(w);v[t],v[t+1]=v[t+1],v[t];yield tuple(v),False,t
    for t in range(N-2):
        if w[t]==w[t+2] and adj(w[t],w[t+1]):
            v=list(w);v[t:t+3]=[w[t+1],w[t],w[t+1]];yield tuple(v),True,t

todo=deque([word]);seen={word};edges=0;chamber_rows=0
while todo:
    w=todo.popleft();A,fr,M=seed(w)
    for v,braid,t in moves(w):
        B,g,L=seed(v);C=mutate(A,t,fr) if braid else A
        p=list(range(N));a=t+int(braid);b=a+1;p[a],p[b]=p[b],p[a]
        transported=Counter({(i,j):C[p[i],p[j]] for i in range(N) for j in range(N) if C[p[i],p[j]]})
        require(transported==B and {i for i in range(N) if p[i] in fr}==g,'graph transport')
        for i in range(N):
            left=L[i][:];lq=0;right=M[p[i]][:];rq=0
            if not braid:left[t],left[t+1]=left[t+1],left[t]
            else:
                a,b,c=left[t:t+3];left[t:t+3]=[b,a,a+b-c];lq=c-a
                q=p[i];e=A[q,t]-A[t,q]
                if q==t:right=[-x for x in right]
                elif e>0:right[t+1]+=e;rq=-e
                elif e<0:right[t]+=e;right[t+2]+=e;rq=-e
            require(left==right and lq==rq,'chamber commutation')
            chamber_rows+=1
        edges+=1
        if v not in seen:seen.add(v);todo.append(v)
require(len(seen)==2316 and edges==12504,'graph counts')

fresh=json.loads((V/'blind_reconstruction/blind_frozen.json').read_text())
d=json.loads((V/'blind_reconstruction/supplement_exact.json').read_text())
rows=[v['exponents'] for s in fresh['summands'].values() for v in s['canonical_X_support']]
data=json.loads((V/'certificate.json').read_text())
require({tuple(r) for r in rows}=={tuple(-x for x in r['a']) for r in data['certificate_rows']},'fresh vs primary support')
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
u=d['strict_interior_point'];require(all(dot(r,u)>0 for r in rows),'fresh interior')
pairings=0
for i,c in enumerate(d['facets']):
    w=c['exclusive_violation_witness'];p=c['facet_relative_interior_point']
    a=[dot(r,w) for r in rows];b=[dot(r,p) for r in rows]
    require(a==c['all_pairings'] and b==c['boundary_pairings'],'stored products')
    require(a[i]<0 and all(x>0 for j,x in enumerate(a) if i!=j),'exclusive violation')
    require(b[i]==0 and all(x>0 for j,x in enumerate(b) if i!=j),'relative interior')
    pairings+=len(a)+len(b)
out={'status':'PASS','no_candidate_code_imported':True,'graph_vertices':len(seen),'directed_edges':edges,'exact_chamber_coordinate_identities':chamber_rows,'third_table_facets':len(rows),'third_table_integer_products':pairings,'third_table_support_matches_primary':True}
(HERE/'graph_and_third_certificates.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
