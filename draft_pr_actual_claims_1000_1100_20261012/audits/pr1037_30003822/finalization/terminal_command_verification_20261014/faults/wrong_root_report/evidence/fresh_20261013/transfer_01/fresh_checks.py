#!/usr/bin/env python3
"""Fresh exact checks, authored for this review; no historical code imported."""
import argparse, collections, datetime, hashlib, itertools, json, pathlib, sys, time
import sympy as sp
from sympy.polys.matrices import DomainMatrix

ROOT=pathlib.Path(__file__).resolve().parent
RESULTS=[]
def record(name,ok,**kw):
    r={'name':name,'ok':bool(ok),**kw}; RESULTS.append(r)
    print(json.dumps(r),flush=True)
    if not ok: raise AssertionError(name)
def partitions(n):
    out=[]
    def rec(i,bl):
        if i==n: out.append(tuple(tuple(x) for x in bl)); return
        for j in range(len(bl)):
            bl[j].append(i);rec(i+1,bl);bl[j].pop()
        bl.append([i]);rec(i+1,bl);bl.pop()
    rec(0,[])
    return sorted(out,key=lambda p:(-len(p),p))
def tree_edges(p,style='star'):
    edges=[]
    for b in p:
        if style=='star': edges.extend((b[0],v) for v in b[1:])
        elif style=='path': edges.extend(zip(b,b[1:]))
        elif style=='last': edges.extend((v,b[-1]) for v in b[:-1])
        else: raise ValueError(style)
    return edges
def transition(n,A,style='star',must_meet=True):
    ps=partitions(n); pi={p:i for i,p in enumerate(ps)}
    T=[[0 for p in ps] for q in ps];counts=[]
    for ip,p in enumerate(ps):
        cnt=0
        for mask in range(1<<(n*n)):
            par=list(range(2*n)); rank=[0]*(2*n)
            def find(u):
                while par[u]!=u:par[u]=par[par[u]];u=par[u]
                return u
            def union(u,v):
                u,v=find(u),find(v)
                if u==v:return False
                if rank[u]<rank[v]:u,v=v,u
                par[v]=u
                if rank[u]==rank[v]:rank[u]+=1
                return True
            for u,v in tree_edges(p,style):assert union(u,v)
            weight=1;ok=True
            for k in range(n*n):
                if mask>>k&1:
                    i,j=divmod(k,n)
                    if not union(i,n+j):ok=False;break
                    weight*=A[i][j]
            if not ok:continue
            comps=collections.defaultdict(list)
            for v in range(2*n):comps[find(v)].append(v)
            if must_meet and any(all(v<n for v in c) for c in comps.values()):continue
            q=tuple(sorted(tuple(v-n for v in c if v>=n) for c in comps.values() if any(v>=n for v in c)))
            T[ip][pi[q]]+=weight;cnt+=1
        counts.append(cnt)
    return sp.Matrix(T),counts

# Exterior monomials use increasing bit positions. Position 2v is x_v, 2v+1 is b_v.
def add(f,g):
    out=dict(f)
    for m,c in g.items():
        out[m]=out.get(m,0)+c
        if out[m]==0:del out[m]
    return out
def scale(f,c):return {m:v*c for m,v in f.items() if v*c!=0}
def mul(f,g):
    out={}
    for a,ca in f.items():
        for b,cb in g.items():
            if a&b:continue
            crossings=sum((b & ((1<<i)-1)).bit_count() for i in range(a.bit_length()) if a>>i&1)
            m=a|b;c=ca*cb*(-1 if crossings%2 else 1)
            out[m]=out.get(m,0)+c
            if out[m]==0:del out[m]
    return out
def gen(i):return {1<<i:sp.Integer(1)}
def diff(a,b):return add(gen(a),scale(gen(b),-1))
def q(u,v):return mul(diff(2*u,2*v),diff(2*u+1,2*v+1))
def forest(p,offset=0,style='star'):
    f={0:sp.Integer(1)}
    for u,v in tree_edges(p,style):f=mul(f,q(u+offset,v+offset))
    return f
def integrate(f,n):
    top=(1<<(2*n))-1
    return {m>>(2*n):c for m,c in f.items() if m&top==top}
def substitute(f,images):
    out={}
    for m,c in f.items():
        z={0:c}
        for i in range(m.bit_length()):
            if m>>i&1:z=mul(z,images[i])
        out=add(out,z)
    return out
def kernel(n,A):
    f={0:sp.Integer(1)}
    for i in range(n):
        for j in range(n):f=mul(f,add({0:sp.Integer(1)},scale(q(i,n+j),A[i][j])))
    return f
def lower(n,f,D):
    # z indices first, xi indices second.
    images=[add(gen(i),gen(2*n+i)) for i in range(2*n)]
    z={0:sp.Integer(1)}
    for i in range(n):z=mul(z,{0:sp.Integer(1),(1<<(2*i))|(1<<(2*i+1)):D[i]})
    return scale(integrate(mul(z,substitute(f,images)),n),1/sp.prod(D))
def rho(n,f,B):
    images=[]
    for i in range(n):
        for parity in range(2):
            z={}
            for j in range(n):z=add(z,scale(gen(2*j+parity),B[i,j]))
            images.append(z)
    return substitute(f,images)
def exponent(f):
    out={0:sp.Integer(1)};powf={0:sp.Integer(1)}
    for k in range(1,100):
        powf=mul(powf,f)
        if not powf:break
        out=add(out,scale(powf,sp.Rational(1,sp.factorial(k))))
    else:raise AssertionError('exterior exponential did not terminate')
    return out
def raise_S(n,f,S):
    quadratic={}
    for i in range(n):
        for j in range(n):quadratic=add(quadratic,scale(mul(gen(2*i),gen(2*j+1)),S[i,j]))
    return mul(exponent(quadratic),f)
def basis_matrix(fs,n):
    mon=sorted(set().union(*(set(f) for f in fs)))
    mat=sp.Matrix([[f.get(m,0) for f in fs] for m in mon])
    piv=mat.rref()[1]
    return [fs[i] for i in piv],mat.rank()
def operator_on_basis(fs,images):
    mon=sorted(set().union(*(set(f) for f in fs+images)))
    P=sp.Matrix([[f.get(m,0) for f in fs] for m in mon])
    Q=sp.Matrix([[f.get(m,0) for f in images] for m in mon])
    rows=P.T.rref()[1]
    small=P[list(rows),:]
    M=small.inv()*Q[list(rows),:]
    assert P*M==Q
    return M

def forest_checks():
    # All 3 labelled trees on 3 vertices, all 16 labelled trees on 4 vertices.
    for n in [3,4]:
        edges=list(itertools.combinations(range(n),2));products=[]
        for es in itertools.combinations(edges,n-1):
            par=list(range(n))
            def find(u):
                while par[u]!=u:u=par[u]
                return u
            good=True
            for u,v in es:
                a,b=find(u),find(v)
                if a==b:good=False;break
                par[b]=a
            if not good:continue
            z={0:sp.Integer(1)}
            for u,v in es:z=mul(z,q(u,v))
            products.append(z)
        record('all labelled tree products agree n='+str(n),all(p==products[0] for p in products),tree_count=len(products))
    cyc=mul(mul(q(0,1),q(1,2)),q(2,0))
    record('triangle cycle annihilation',not cyc)
    record('edge reversal unchanged',q(0,1)==q(1,0))
    record('repeated edge annihilation',not mul(q(0,1),q(0,1)))

def symbolic_checks(n):
    symbols=sp.symbols(' '.join('a%d%d'%(i+1,j+1) for i in range(n) for j in range(n)))
    if n==1:symbols=(symbols,)
    A=[list(symbols[i*n:(i+1)*n]) for i in range(n)]
    T,counts=transition(n,A)
    domain=sp.ZZ.poly_ring(*symbols)
    dm=DomainMatrix.from_Matrix(T).convert_to(domain)
    det=dm.det().as_expr()
    ca=sp.binomial(2*n,n)//(n+1)
    target=sp.Matrix(A).det()**ca
    delta=sp.Poly(det-target,*symbols)
    record('full symbolic forest determinant n='+str(n),delta.is_zero,bell=len(partitions(n)),catalan=int(ca),edge_subset_visits=len(partitions(n))*(1<<(n*n)),admissible_counts=counts,determinant_terms=len(sp.Poly(det,*symbols).terms()))
    if n<=2:
        k=kernel(n,A)
        for ip,p in enumerate(partitions(n)):
            left=integrate(mul(k,forest(p)),n)
            right={}
            for iq,qpart in enumerate(partitions(n)):right=add(right,scale(forest(qpart),T[ip,iq]))
            for m in set(left)|set(right):assert sp.expand(left.get(m,0)-right.get(m,0))==0
        record('symbolic exterior versus independent edge enumeration n='+str(n),True)
        (ROOT/('symbolic_n%d.txt'%n)).write_text('A='+str(A)+'\nT='+str(T)+'\ndet='+str(sp.factor(det))+'\ncounts='+str(counts)+'\n')

def numeric_checks(n,A,case):
    A=sp.Matrix(A);rows=list(A.tolist());T,counts=transition(n,rows)
    ca=int(sp.binomial(2*n,n)//(n+1)); detA=A.det();detT=T.det()
    if n<=3:expected=detA**ca;record('exact transfer determinant '+case,detT==expected,n=n,detA=str(detA),detT=str(detT),expected=str(expected))
    else:
        perm=sum(sp.prod(A[i,p[i]] for i in range(n)) for p in itertools.permutations(range(n)))
        expected=detA**ca*perm
        record('exact n4 determinant with permanent '+case,detT==expected,n=n,detA=str(detA),detT=str(detT),permanent=str(perm))
    k=kernel(n,rows);ps=partitions(n);fs=[forest(p) for p in ps]
    images=[]
    for ip,p in enumerate(ps):
        left=integrate(mul(k,fs[ip]),n);images.append(left)
        right={}
        for iq in range(len(ps)):right=add(right,scale(fs[iq],T[ip,iq]))
        assert left==right
    record('exact exterior transfer versus graph enumeration '+case,True,n=n,bell=len(ps),kernel_monomials=len(k))
    r=[sum(A[i,j] for j in range(n)) for i in range(n)]
    if any(x==0 for x in r):
        record('zero row sums bypass Gaussian inverse '+case,True,zero_rows=[i for i,x in enumerate(r) if x==0]);return
    D=sp.diag(*r);B=D.inv()*A;S=sp.diag(*[sum(A[i,j] for i in range(n)) for j in range(n)])-A.T*D.inv()*A
    assert B*sp.ones(n,1)==sp.ones(n,1) and S==S.T and S*sp.ones(n,1)==sp.zeros(n,1)
    detD=sp.prod(r)
    factored=[scale(raise_S(n,rho(n,lower(n,f,r),B),S),detD) for f in fs]
    record('exact ordered Gaussian equality '+case,images==factored,n=n,detD=str(detD))
    bas,rank=basis_matrix(fs,n);assert rank==ca
    H=operator_on_basis(bas,[lower(n,f,r) for f in bas]);M=operator_on_basis(bas,[raise_S(n,f,S) for f in bas]);G=operator_on_basis(bas,[integrate(mul(k,f),n) for f in bas])
    record('H M quotient determinant '+case,H.det()==M.det()==1 and G.det()==detA**ca,rank=rank,detH=str(H.det()),detM=str(M.det()),detG=str(G.det()))
    if n>=2 and detA!=0:
        bad=[scale(raise_S(n,lower(n,rho(n,f,B),r),S),detD) for f in fs]
        record('negative control swapped H and rho detected '+case,bad!=images)
        badnorm=[scale(f,detD) for f in factored]
        record('negative control missing H normalization detected '+case,badnorm!=images)

def special_n4_tree_check():
    n=4;A=[[2,-1,0,1],[0,3,1,-2],[1,0,2,1],[-1,2,0,3]]
    T,counts=transition(n,A,'star')
    for style in ['path','last']:
        alt,c=transition(n,A,style)
        record('all Bell n4 fixed internal tree independence '+style,T==alt and counts==c,bell=len(partitions(4)),edge_subsets_per_input=65536)
    crossing=((0,2),(1,3));record('crossing n4 partition included',crossing in partitions(4))

def negative_graph_control():
    A=[[2,1],[3,4]]
    good,_=transition(2,A);bad,_=transition(2,A,must_meet=False)
    record('negative control allowing X-only components detected',good!=bad,correct_det=str(good.det()),faulty_det=str(bad.det()))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=['symbolic','exterior','n4tree','all'],default='all');args=parser.parse_args()
    start=time.time();record('execution environment',True,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,sympy=sp.__version__,mode=args.mode,script_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest())
    if args.mode in ['symbolic','all']:
        forest_checks()
        for n in [1,2,3]:symbolic_checks(n)
        negative_graph_control()
    if args.mode in ['exterior','all']:
        for n,A,label in [
            (1,[[-2]],'n1 negative'),
            (2,[[2,-1],[3,4]],'n2 generic signed'),
            (2,[[1,-1],[2,3]],'n2 invertible zero row'),
            (2,[[1,-1],[2,-2]],'n2 singular zero rows'),
            (2,[[0,0],[0,0]],'n2 all zero'),
            (3,[[2,-1,1],[3,4,-2],[-1,2,3]],'n3 generic signed nonsymmetric'),
            (3,[[1,-1,0],[2,3,1],[0,1,2]],'n3 invertible zero row'),
            (3,[[1,2,-1],[2,4,-2],[0,1,2]],'n3 rank deficient'),
            (4,[[2,-1,0,1],[0,3,1,-2],[1,0,2,1],[-1,2,0,3]],'n4 signed nonplanar Bell'),
        ]:numeric_checks(n,A,label)
    if args.mode in ['n4tree','all']:special_n4_tree_check()
    record('completed',True,elapsed_seconds=round(time.time()-start,3),checks=len(RESULTS))
    (ROOT/('CHECK_RESULTS_'+args.mode+'.json')).write_text(json.dumps(RESULTS,indent=2)+'\n')
if __name__=='__main__':main()
