from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from math import comb,exp,sqrt,pi,erf
import cmath,datetime,json
R=Path(__file__).resolve().parent

def need(x,msg):
    if not x:raise RuntimeError(msg)
def ff(a,k):
    ans=1
    for j in range(k):ans*=a-j
    return ans
rows=[];graphs=0;max_fourier_error=0.0;negative=[]
for n in [3,4,5]:
    edges=list(combinations(range(n),2));N=len(edges);tri=[sum(1<<edges.index(e) for e in combinations(vs,2)) for vs in combinations(range(n),3)]
    wedges=[(i,j) for i,j in combinations(range(N),2) if set(edges[i])&set(edges[j])];disjoint=[(i,j) for i,j in combinations(range(N),2) if not set(edges[i])&set(edges[j])]
    raw=[];by_m={m:[] for m in range(N+1)}
    for mask in range(1<<N):
        m=mask.bit_count();t=sum(mask&x==x for x in tri);w=sum((mask>>i)&(mask>>j)&1 for i,j in wedges);y=sum((mask>>i)&(mask>>j)&1 for i,j in disjoint)
        need(y==comb(m,2)-w,'ordinary 2K2 identity');raw.append((m,t,w,y));by_m[m].append(w)
    graphs+=len(raw);need(0 in [x[1] for x in raw] and 1 in [x[1] for x in raw],'triangle span')
    if n>=4:
        A=N*(n-2);B=A*(4*n-10)
        need(len(wedges)==A and B-4*A*A//N==-2*A,'wedge combinatorial cancellation')
        for m,ws in by_m.items():
            pj=lambda j:F(ff(m,j),ff(N,j));mean=F(sum(ws),len(ws));var=F(sum(w*w for w in ws),len(ws))-mean**2
            formula=A*(pj(2)-pj(4))+B*(pj(3)-pj(4))+A*A*(pj(4)-pj(2)**2)
            need(var==formula,'conditional wedge variance')
    for p in [F(1,4),F(1,2),F(3,4)]:
        weights=[p**m*(1-p)**(N-m) for m,t,w,y in raw];ET=sum(a*t for a,(m,t,w,y) in zip(weights,raw));VT=sum(a*t*t for a,(m,t,w,y) in zip(weights,raw))-ET**2
        formula=comb(n,3)*p**3*(1-p**3)+12*comb(n,4)*p**5*(1-p) if n>=4 else comb(n,3)*p**3*(1-p**3)
        need(ET==comb(n,3)*p**3 and VT==formula,'triangle moments')
        linear=N*(n-2)**2*p**5*(1-p);remainder=3*comb(n,3)*p**4*(1-p)**2+comb(n,3)*p**3*(1-p)**3
        need(VT==linear+remainder,'true variance projection decomposition')
        if n>=4:
            EY=sum(a*y for a,(m,t,w,y) in zip(weights,raw));VY=sum(a*y*y for a,(m,t,w,y) in zip(weights,raw))-EY**2
            need(EY==3*comb(n,4)*p*p,'2K2 mean');need(VY==N*comb(n-2,2)**2*p**3*(1-p)+3*comb(n,4)*p*p*(1-p)**2,'2K2 true variance')
        pmf={k:sum(a for a,(_,t,_,_) in zip(weights,raw) if t==k) for k in range(comb(n,3)+1)}
        for q in [1,2,4,6,7,12]:
            res=[sum(v for k,v in pmf.items() if k%q==a) for a in range(q)];delta=max(abs(q*v-1) for v in res)
            if q==1:need(delta==0,'q1 exact')
            for a,v in enumerate(res):
                pred=sum(sum(float(prob)*cmath.exp(2j*pi*r*k/q) for k,prob in pmf.items())*cmath.exp(-2j*pi*r*a/q) for r in range(q))/q
                err=abs(pred-float(v));max_fourier_error=max(max_fourier_error,err);need(err<2e-14,'finite Fourier inversion')
            if q>=2:need(abs(sum(float(v)*cmath.exp(2j*pi*k/q) for k,v in pmf.items()))<=float(delta)+2e-14,'first Fourier lower bound')
        # Labeled embeddings have zero odd mass: a deliberate wrong convention is rejected.
        need(sum(v for k,v in pmf.items() if (6*k)%2==1)==0,'6T parity control')
        if n>=4:need(VT!=comb(n,3)*p**3*(1-p**3)+6*comb(n,4)*p**5*(1-p),'missing factor2 detection')
    rows.append({'n':n,'graphs':len(raw),'p':['1/4','1/2','3/4'],'all_conditional_m':n>=4})
# Direct and dual Gaussian folding; declared ordinary floating tolerance only.
phi=lambda x:exp(-x*x/2)/sqrt(2*pi)
grid=[];max_gaussian=0.0
for h in [0.15,0.5,1,2,4,10,50]:
    for theta in [0,0.137,0.4999]:
        K=int(12/h)+10;direct=h*sum(phi(h*(j+theta)) for j in range(-K,K+1));dual=1+2*sum(exp(-2*pi*pi*l*l/h**2)*__import__('math').cos(2*pi*l*theta) for l in range(1,int(12*h)+10));err=abs(direct-dual);max_gaussian=max(max_gaussian,err)
        need(err<2e-12,'Gaussian dual comparison');need(abs(direct-1)<=sqrt(2/pi)*h+2e-12,'shifted mesh bound');grid.append([h,theta,direct])
# Cell comparison at multiple scales/phases, with cancellation-aware tolerance.
for sigma in [1,2,10,100]:
    for z in [-3,-0.2,0,1.4]:
        cell=(erf((z+0.5/sigma)/sqrt(2))-erf((z-0.5/sigma)/sqrt(2)))/2;g=phi(z)/sigma
        need(abs(cell-g)<=phi(0)/(24*sigma**3)+2e-16,'Gaussian cell midpoint inequality')
out={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','independent_graph_configurations':graphs,'enumerations':rows,'fourier_moduli':[1,2,4,6,7,12],'max_fourier_error':max_fourier_error,'gaussian_direct_dual_cases':len(grid),'max_gaussian_error':max_gaussian,'tolerances':{'fourier':2e-14,'gaussian_dual_mesh':2e-12,'cell_roundoff_allowance':2e-16},'intentional_errors_rejected':['variance ordered-overlap coefficient6','6T convention modulo2'],'proof_scope':'Exact finite moment/conditional identities plus floating finite Fourier/Gaussian diagnostics only. Asymptotic proof was checked separately; no LLT proof inferred.'}
(R/'MATH_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
