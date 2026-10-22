"""Independent read-only mathematical replay; no import of the author verifier."""
import json, hashlib, sys
from pathlib import Path
from collections import Counter, deque
import sympy as S

PACKET=Path(__file__).resolve().parents[1]/'derived_pure_braid_30003634'/'packet'
def need(x,msg):
    if not x: raise ValueError(msg)
def inverse(w): return [-x for x in w[::-1]]
def reduce_word(w):
    r=[]
    for x in w:
        if r and r[-1]==-x: r.pop()
        else: r.append(x)
    return r
def comm(x,y): return reduce_word(x+y+inverse(x)+inverse(y))
def target():
    a=[1,1]; b=[2,2]; c=comm(a,b)
    d=reduce_word(inverse(a)+c+a); e=reduce_word(inverse(b)+c+b)
    u=comm(c,d); v=comm(d,e)
    return comm(u,v)
def blocks(w):
    out=[]
    for x in w:
        if out and out[-1][0]==abs(x): out[-1][1]+=1 if x>0 else -1
        else: out.append([abs(x),1 if x>0 else -1])
    return out

def planar_faces(w):
    # Clockwise half-edge order at each crossing: UL, UR, LR, LL.
    # Match consecutive half-edges along each vertical braid-position line,
    # closing bottom to top. This constructs the planar projection independently
    # of crossing signs and without the syllable Goeritz formula.
    vertical=[[],[],[]]
    for c,x in enumerate(w):
        p=abs(x)-1
        vertical[p].append((4*c,4*c+3))
        vertical[p+1].append((4*c+1,4*c+2))
    need(all(vertical),'projection must meet all three positions')
    across={}
    for chain in vertical:
        for (_,out),(inc,_) in zip(chain,chain[1:]+chain[:1]):
            across[out]=inc; across[inc]=out
    face_of={}; faces=[]
    for d in range(4*len(w)):
        if d in face_of: continue
        f=[]; now=d
        while now not in face_of:
            face_of[now]=len(faces); f.append(now)
            end=across[now]; now=4*(end//4)+(end+1)%4
        need(now==d,'face permutation broken')
        faces.append(f)
    need(len(faces)==len(w)+2,'nonplanar rotation system')
    adjacency=[set() for _ in faces]
    for c in range(len(w)):
        fs=[face_of[4*c+k] for k in range(4)]
        for a,b in zip(fs,fs[1:]+fs[:1]):
            adjacency[a].add(b); adjacency[b].add(a)
    color={0:0}; q=deque([0])
    while q:
        a=q.popleft()
        for b in adjacency[a]:
            if b not in color: color[b]=1-color[a]; q.append(b)
            need(color[b]!=color[a],'not checkerboard')
    need(len(color)==len(faces),'face graph disconnected')
    return faces,face_of,color

def planar_goeritz(w):
    faces,fo,col=planar_faces(w)
    # Erle's alpha color occupies the horizontal corners at sigma_1 and
    # vertical corners at sigma_2. Face dart k corresponds to corner (k-1,k).
    first1=next(i for i,x in enumerate(w) if abs(x)==1)
    alpha=col[fo[4*first1]] # k=0 is the left horizontal corner.
    ids=[f for f in range(len(faces)) if col[f]==alpha]
    full=S.zeros(len(ids)); ix={f:i for i,f in enumerate(ids)}
    crossings=[]
    for i,x in enumerate(w):
        fs=[fo[4*i+k] for k in range(4)]
        selected=[k for k in range(4) if col[fs[k]]==alpha]
        need(selected in ([0,2],[1,3]),'opposite alpha corners')
        u,v=[ix[fs[k]] for k in selected]
        sign=1 if x>0 else -1
        eta=sign if selected==[0,2] else -sign
        if u!=v:
            full[u,u]+=eta; full[v,v]+=eta
            full[u,v]-=eta; full[v,u]-=eta
        crossings.append((u,v,eta,selected==[0,2]))
    # The single outside alpha region is incident to every sigma_1 crossing.
    common=None
    for i,x in enumerate(w):
        if abs(x)==1:
            pair=set(crossings[i][:2]); common=pair if common is None else common & pair
    need(len(common)==1,'outside region not unique')
    outside=common.pop()
    inner=[i for i in range(len(ids)) if i!=outside]
    matrix=full.extract(inner,inner)
    correction=sum(e for u,v,e,exc in crossings if exc and u!=v)
    cycle_order=[inner.index(ix[fo[4*i+1]]) for i,x in enumerate(w) if abs(x)==2]
    need(len(set(cycle_order))==len(inner),'cycle does not list every bounded face')
    return matrix,correction,{'cycle_order':cycle_order,'faces':len(faces),'alpha_regions':len(ids),'outside_index':outside,'crossings':crossings,'face_lengths':[len(f) for f in faces]}

def block_goeritz(w):
    bs=blocks(w); need(len(bs)%2==0,'even syllables')
    need(all(g==(1 if i%2==0 else 2) for i,(g,e) in enumerate(bs)),'alternating')
    A=[e for g,e in bs[::2]]; B=[e for g,e in bs[1::2]]
    n=sum(map(abs,B)); G=S.zeros(n); t=0
    for a,b in zip(A,B):
        G[t,t]+=a
        for h in range(abs(b)):
            u=(t+h)%n; v=(t+h+1)%n; s=1 if b>0 else -1
            G[u,u]-=s; G[v,v]-=s; G[u,v]+=s; G[v,u]+=s
        t+=abs(b)
    return G,sum(A)

def inertia(M):
    """Exact symmetric congruence with maximum-diagonal pivots and 2x2 fallback."""
    A=S.Matrix(M); pos=neg=zero=0; piv=[]
    while A.rows:
        n=A.rows
        if any(A[i,i] for i in range(n)):
            k=max(range(n),key=lambda i:abs(A[i,i])); p=A[k,k]
            rest=[i for i in range(n) if i!=k]; v=A.extract(rest,[k]); H=A.extract(rest,rest)
            pos+=int(bool(p>0)); neg+=int(bool(p<0)); piv.append(str(p))
            A=H-v*v.T/p
        elif any(A):
            i,j=next((i,j) for i in range(n) for j in range(i+1,n) if A[i,j])
            rest=[k for k in range(n) if k not in (i,j)]
            D=A.extract([i,j],[i,j]); C=A.extract(rest,[i,j]); H=A.extract(rest,rest)
            A=H-C*D.inv()*C.T; pos+=1; neg+=1; piv.append(['pair',str(D[0,1])])
        else:
            zero+=n; break
    return [pos,neg,zero],piv

I=S.eye(2); J=S.Matrix([[0,1],[-1,0]])
GEN={1:S.Matrix([[1,0],[-1,1]]),2:S.Matrix([[1,1],[0,1]])}
GEN[-1]=GEN[1].inv(); GEN[-2]=GEN[2].inv()
def meyer(A,B):
    X=A.inv()-I; Y=I-B
    # Kernel vectors are pairs (v1,v2) with X*v1=Y*v2=e.
    K=(X.row_join(-Y)).nullspace()
    if not K: return 0,[]
    K=S.Matrix.hstack(*K)
    E=X*K[:2,:]; U=K[:2,:]+K[2:,:]
    F=U.T*J*E; F=(F+F.T)/2
    it,piv=inertia(F)
    return it[0]-it[1],[[str(x) for x in row] for row in F.tolist()]
def braid_signature(w,terms=False):
    A=I; ms=[]; forms=[]
    for x in w:
        m,F=meyer(A,GEN[x]); ms.append(m); forms.append(F); A=A*GEN[x]
    return -sum(ms),A,ms,forms

def run():
    cert=json.loads((PACKET/'certificate.json').read_text()); w=target()
    need(len(w)==104,'word length'); need(w==cert['word'],'word differs')
    need([e for g,e in blocks(w)]==cert['syllables'],'syllables differ')
    labels=[0,1,2]; counts={(0,1):0,(0,2):0,(1,2):0}
    for x in w:
        j=abs(x)-1; pair=tuple(sorted(labels[j:j+2])); counts[pair]+=1 if x>0 else -1
        labels[j],labels[j+1]=labels[j+1],labels[j]
    need(labels==[0,1,2],'not pure'); need(not any(counts.values()),'linking nonzero')
    G,mu=block_goeritz(w); PG,pmu,pdata=planar_goeritz(w)
    gi,gp=inertia(G); pi,pp=inertia(PG)
    need(G.tolist()==cert['goeritz'],'Goeritz mismatch')
    need(PG.extract(pdata['cycle_order'],pdata['cycle_order'])==G,'diagram matrix differs after cyclic region numbering')
    need(gi==[23,25,0] and pi==gi,'inertia mismatch')
    need(mu==pmu==0,'correction mismatch')
    det=G.det(method='domain-ge'); pdet=PG.det(method='domain-ge')
    need(det==pdet==cert['goeritz_determinant'],'determinant mismatch')
    sig,M,terms,forms=braid_signature(w)
    need(sig==cert['signature']==-2,'signature mismatch')
    need(list(M)==cert['burau_matrix'],'Burau mismatch')
    need(terms==cert['meyer_terms'],'Meyer terms differ')
    need(M.det()==1,'Burau not unimodular')
    controls=[]
    known=[('empty',[],0),('one crossing',[1],0),('positive Hopf',[1,1],-1),('negative Hopf',[-1,-1],1),('positive trefoil',[1]*3,-2),('negative trefoil',[-1]*3,2),('trefoil positive stabilization',[1]*3+[2],-2),('trefoil negative stabilization',[1]*3+[-2],-2),('figure eight',[1,-2]*2,0),('Borromean rings',[1,-2]*3,0),('three component positive torus link',[1,2]*3,-4),('negative torus link',[-1,-2]*3,4)]
    for name,v,expected in known:
        s,_,_,_=braid_signature(v); need(s==expected,'known signature: '+name)
        controls.append({'name':name,'word':v,'signature':s})
    result={'word_length':len(w),'word':w,'syllables':blocks(w),'permutation':labels,'pairwise_crossing_sums':list(counts.values()),'goeritz_inertia':gi,'goeritz_determinant':str(det),'planar_inertia':pi,'planar_determinant':str(pdet),'planar_face_counts':[pdata['faces'],pdata['alpha_regions']], 'planar_region_permutation':pdata['cycle_order'], 'planar_matrix_equals_certificate_after_permutation':True,'correction':mu,'burau':[[int(x) for x in row] for row in M.tolist()],'meyer_terms':terms,'meyer_term_counts':dict(Counter(terms)),'signature':sig,'known_controls':controls,'independent_meyer_forms':forms,'maximum_pivot_inertia_pivots':gp}
    print(json.dumps(result,indent=2))
if __name__=='__main__': run()
