"""Fresh review controls from literal death--Birth updates, no submitted imports."""
from pathlib import Path
import json, hashlib, datetime
from itertools import combinations
from collections import Counter
import sympy as s
R=s.Rational
COUNTS=Counter();DETAILS={}
def check(label, pred):
    if not bool(pred): raise AssertionError(label)
    COUNTS[label]+=1
def norm(P):
    return s.Matrix(P.rows,P.cols,lambda i,j:P[i,j]/sum(P.row(i)))
def complete(n):return s.Matrix(n,n,lambda i,j:R(int(i!=j),n-1))
def baseline(n,r):return R(n-1,n)*(1-1/r)/(1-r**(1-n)) if r!=1 else R(1,n)
def literal_jets(P,D=None,strong=False,r=R(2)):
    n=P.rows;full=(1<<n)-1;states=list(range(1,full));ix={a:k for k,a in enumerate(states)}
    Q=[s.zeros(len(states)) for _ in range(3)];b=[s.zeros(len(states),1) for _ in range(3)]
    for a in states:
        row=ix[a]
        for v in range(n):
            x=sum(P[v,u] for u in range(n) if a>>u&1)
            if strong:
                ff=[s.Integer(0)]*3 if x==0 else [s.Integer(1),-(1-x)/x,((1-x)/x)**2]
            else:
                z=0 if D is None else sum(D[v,u] for u in range(n) if a>>u&1)
                den=1+(r-1)*x
                ff=[r*x/den,r*z/den**2,-r*(r-1)*z*z/den**3]
            for val in (0,1):
                dest=(a|(1<<v)) if val else (a&~(1<<v))
                prob=ff if val else [1-ff[0],-ff[1],-ff[2]]
                for order in range(3):
                    p=prob[order]/n
                    if dest==full:b[order][row]+=p
                    elif dest:Q[order][row,ix[dest]]+=p
        check('literal_total_probability',sum(Q[0].row(row))+b[0][row]<=1)
    inv=(s.eye(len(states))-Q[0]).inv(method='DM')
    h=[inv*b[0]]
    h.append(inv*(b[1]+Q[1]*h[0]))
    h.append(inv*(b[2]+Q[1]*h[1]+Q[2]*h[0]))
    rho=[s.factor(sum(v[ix[1<<i]] for i in range(n))/n) for v in h]
    return rho,h
def standard(n):
    z=[1,-1]+[0]*(n-2)
    return s.Matrix(n,n,lambda i,j:R(z[i]+(n-1)*z[j],n*(n-2)) if i!=j else 0)
def symmetric(n):
    d=s.zeros(n)
    for i,j,a in [(0,1,1),(2,3,1),(0,2,-1),(1,3,-1)]:d[i,j]=d[j,i]=a
    return d
def antisymmetric(n):
    d=s.zeros(n)
    for i,j in [(0,1),(1,2),(2,0)]:d[i,j]=1;d[j,i]=-1
    return d
def f_norm(d):return sum(x*x for x in d)
TABLE={3:[R(1,11),None,R(1,9)],4:[R(87,640),R(3,208),R(57,640)],5:[R(8585,57314),R(359,26660),R(143,2100)]}
def curvature(n,d):
    rr,hh=literal_jets(complete(n),d)
    check('complete_baseline',rr[0]==baseline(n,R(2)))
    check('zero_first_derivative',rr[1]==0)
    val=-rr[2]/(n*rr[0]**2)
    check('positive_curvature',val>0)
    return val
def gradients(N):
    c=R(2**N-1,N*2**(N-1));d={0:s.Integer(0),N:s.Integer(0)}
    for k in range(1,N):d[k]=s.factor((2*N*(R(1,k)-c)+(k-1)*d[k-1])/(N-k))
    for k in range(1,N):
        check('poisson_positive_decreasing',d[k]>d[k+1])
        check('poisson_bounds',R(2*(N-2),N*k)<=d[k]<=R(2,k))
    return d
def standard_quotient(N):
    labels=[('P',k) for k in range(1,N)]+[('R',k) for k in range(1,N)]+[('Q',k) for k in range(1,N+1)]
    ix={a:i for i,a in enumerate(labels)};H=s.zeros(len(labels));gam=s.zeros(len(labels),1);sig=s.zeros(1,len(labels));d=gradients(N)
    def add(a,b,x):
        if b in ix:H[ix[a],ix[b]]+=x
    for k in range(1,N):
        a=('P',k);add(a,a,R(k,2*N));add(a,('P',k+1),R(N-k-1,2*N));add(a,('Q',k+1),R(1,2*N));gam[ix[a]]=k*d[k]
        a=('R',k);add(a,a,R(k,2*N)+R((k-1)*(N-k),2*k*N));add(a,('R',k+1),R(N-k-1,2*N));add(a,('R',k-1),R((k-1)**2,2*k*N));add(a,('Q',k),R(1,2*k*N));add(a,('P',k-1),R(k-1,2*k*N));add(a,('P',k),R(N-k,2*k*N))
        gam[ix[a]]=N*d[k]+R((N+1)*(k-1),k)*d[k-1];sig[ix[a]]=R(s.binomial(N-2,k-1),2**(N-2))
    for k in range(1,N+1):
        a=('Q',k);add(a,a,R(k*k-1,2*k*N));add(a,('Q',k+1),R(N-k,2*N));add(a,('P',k-1),-R(k-1,2*k*N));add(a,('P',k),-R(N-k,2*k*N));add(a,('R',k-1),-R((k-1)**2,2*k*N));add(a,('R',k),-R((k-1)*(N-k),2*k*N));gam[ix[a]]=-(N-k)*d[k]-R((N+1)*(k-1),k)*d[k-1]
    phi=(sig*(s.eye(len(labels))-H).inv(method='DM')*gam)[0]
    check('standard_quotient_positive',phi>0)
    return phi/(4*N*(N+1))
def active(P):
    n=P.rows;ys=[(a,v) for v in range(n) for a in range(1,1<<n) if not a>>v&1];ix={a:i for i,a in enumerate(ys)};K=s.zeros(len(ys))
    for a,v in ys:
        row=ix[a,v];verts=[i for i in range(n) if a>>i&1]
        for i in range(n):
            if i!=v:K[row,ix[a|1<<i,v]]+=P[v,i]/2
        for w in verts:
            for i in range(n):
                if i!=w:K[row,ix[(a&~(1<<w))|1<<i,w]]+=P[w,i]/(2*len(verts))
        check('active_stochastic',sum(K.row(row))==1)
    A=K.T-s.eye(len(ys));b=s.zeros(len(ys),1);A[-1,:]=s.ones(1,len(ys));b[-1]=1;nu=A.inv(method='DM')*b
    return ys,K,nu
def union_chain(P):
    n=P.rows;states=list(range(1,(1<<n)-1));ix={a:i for i,a in enumerate(states)};K=s.zeros(len(states))
    for a in states:
        for v in range(n):
            if not a>>v&1:K[ix[a],ix[a]]+=R(1,n);continue
            others=[i for i in range(n) if i!=v]
            for length in range(1,n):
                for sampled in combinations(others,length):
                    prob=0
                    for k in range(1,length+1):
                        for sub in combinations(sampled,k):
                            z=sum(P[v,i] for i in sub);prob+=(-1)**(length-k)*z/(2-z)
                    dest=a&~(1<<v)
                    for i in sampled:dest|=1<<i
                    check('geometric_exact_set_nonnegative',prob>=0)
                    K[ix[a],ix[dest]]+=prob/n
    A=K.T-s.eye(len(states));b=s.zeros(len(states),1);A[-1,:]=s.ones(1,len(states));b[-1]=1;pi=A.inv(method='DM')*b
    check('union_stationary',K.T*pi==pi)
    return states,pi
def run():
    vals={}
    for n in range(3,7):
        ds=[standard(n),symmetric(n) if n>=4 else None,antisymmetric(n)];eigs=[];raw=[]
        for j,d in enumerate(ds):
            if d is None:eigs.append(None);raw.append(0);continue
            q=curvature(n,d);ev=q/f_norm(d);raw.append(q);eigs.append(ev)
            if n in TABLE:check('printed_sector_eigenvalue',ev==TABLE[n][j])
        check('standard_fullchain_matches_quotient',eigs[0]==standard_quotient(n-1))
        mix=sum((d for d in ds if d is not None),s.zeros(n));check('sector_cross_terms_zero',curvature(n,mix)==sum(raw))
        vals[n]=list(map(str,eigs));print('curvature',n,vals[n],flush=True)
    DETAILS['full_state_sector_eigenvalues']=vals
    for N in range(2,16):standard_quotient(N)
    for n in (3,4,5):
        W=s.Matrix(n,n,lambda i,j:0 if i==j else (i+1)*(j+2)+(i-j)**2);P=norm(W)
        rr,hh=literal_jets(P,strong=True)
        defect=sum((P[v,u]-P[v,z])**2/(P[v,u]*P[v,z]) for v in range(n) for u,z in combinations([i for i in range(n) if i!=v],2))
        check('strong_selection_limit',rr[0]==R(n-1,n));check('strong_selection_deficit_coefficient',-R(n-1,n)-rr[1]==defect/(n*n*(n-2)))
        scale=s.diag(*range(2,n+2));check('incoming_scale_invariance',norm(scale*W)==P)
        DETAILS[f'strong_n{n}']={'defect':str(defect),'rho_jet':list(map(str,rr))}
        if n<=4:
            rho,h=literal_jets(P);states,pi=union_chain(P);ys,K,nu=active(P)
            mean=sum(a.bit_count()*pi[i] for i,a in enumerate(states));collision=sum(nu[i]/a.bit_count() for i,(a,v) in enumerate(ys))
            check('coverage_mean',mean/n==rho[0]);check('active_collision',collision==1/mean)
            for pos,a in enumerate(states):check('coverage_all_committors',h[0][pos]==sum(pi[i] for i,b in enumerate(states) if a&b))
            n0=active(complete(n))[2];check('complete_active_stationary',all(n0[i]==R(a.bit_count(),n*(n-1)*2**(n-2)) for i,(a,v) in enumerate(ys)))
            DETAILS[f'dual_n{n}']={'mean':str(mean),'collision':str(collision)}
    # Exact boundary/negative controls: n=2 degeneracy, nonuniform initialization,
    # asymmetric complete support, and connected incomplete undirected limits.
    for r in [R(1,2),R(1),R(2),R(7)]:check('n2_ties',literal_jets(complete(2),r=r)[0][0]==R(1,2))
    _,h=literal_jets(complete(3),standard(3));check('uniform_initialization_is_essential',any(v!=0 for v in h[1]))
    for n in (3,4,5):
        for kind in ('path','star','cycle'):
            W=s.zeros(n)
            es=[(i,i+1) for i in range(n-1)] if kind=='path' else ([(0,i) for i in range(1,n)] if kind=='star' else [(i,(i+1)%n) for i in range(n)])
            for i,j in es:W[i,j]=W[j,i]=1
            P=norm(W);rr,_=literal_jets(P,strong=True)
            claimed=sum(R(sum(1 for z in W.row(i) if z>0),sum(1 for z in W.row(i) if z>0)+1) for i in range(n))/n
            check('undirected_support_limit',rr[0]==claimed)
    for a,b,c in [(1,1,1),(1,2,3),(1,1,9),(1,3,3)]:
        P=norm(s.Matrix([[0,a,b],[a,0,c],[b,c,0]]))
        for r in [R(101,100),R(3,2),R(2),R(10),R(1000)]:
            value=literal_jets(P,r=r)[0][0];check('triangle_global_sample',value<=baseline(3,r));check('triangle_equality_sample',(value==baseline(3,r))==(a==b==c))
    for x,y in [(1,1),(2,1),(3,5),(R(1,7),R(3,2))]:
        W= s.ones(4)-s.eye(4);W[0,1]=W[1,0]=x;W[2,3]=W[3,2]=y
        for r in [R(101,100),R(2),R(19)]:
            value=literal_jets(norm(W),r=r)[0][0];check('K4_22_global_sample',value<=baseline(4,r));check('K4_22_equality_sample',(value==baseline(4,r))==(x==y==1))
    out={'status':'PASS','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'assertions':sum(COUNTS.values()),'families':len(COUNTS),'counts':dict(COUNTS),'details':DETAILS,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limitations':'Finite exact literal-chain controls do not prove the all-order sector bounds or all-fitness polynomial identities.'}
    Path(__file__).with_name('independent_control_results.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',sum(COUNTS.values()),flush=True)
if __name__=='__main__':run()
