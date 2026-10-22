#!/usr/bin/env python3
"""Independent finite exact moments and conditional counts; not an LLT proof."""
import cmath,collections,itertools,json,math,pathlib
from fractions import Fraction as F
H=pathlib.Path(__file__).resolve().parent
def need(v,m):
    if not v:raise ValueError(m)
def fall(m,k):
    r=1
    for j in range(k):r*=m-j
    return r
graphs=0;conditional=0;cases=[];max_error=0.;negative_controls=[]
for n in [3,4,5]:
    edges=list(itertools.combinations(range(n),2));N=len(edges);counts=[];strata=collections.defaultdict(list)
    for mask in range(1<<N):
        chosen={e for i,e in enumerate(edges) if mask>>i&1};m=len(chosen);degrees=[sum(v in e for e in chosen) for v in range(n)]
        t=sum(all(e in chosen for e in itertools.combinations(v,2)) for v in itertools.combinations(range(n),3))
        w=sum(d*(d-1)//2 for d in degrees);y=sum(not (set(e)&set(f)) for e,f in itertools.combinations(chosen,2))
        need(y==m*(m-1)//2-w,'ordinary disjoint pair partition');counts.append((m,t,y));strata[m].append(w);graphs+=1
    if n>=4:
        S=N*(n-2);B=S*(4*n-10)
        for m,ws in strata.items():
            mean=F(sum(ws),len(ws));var=F(sum(w*w for w in ws),len(ws))-mean*mean
            p2,p3,p4=[F(fall(m,j),fall(N,j)) for j in [2,3,4]]
            need(var==S*(p2-p4)+B*(p3-p4)+S*S*(p4-p2*p2),'conditional wedge variance from enumeration')
            conditional+=1
    for p in [F(1,3),F(2,5),F(4,5)]:
        den=p.denominator;num=p.numerator;normal=den**N;dist=collections.Counter();tot=0;et=F(0);et2=F(0);ey=F(0);ey2=F(0)
        for m,t,y in counts:
            weight=num**m*(den-num)**(N-m);tot+=weight;dist[t]+=weight;prob=F(weight,normal);et+=prob*t;et2+=prob*t*t;ey+=prob*y;ey2+=prob*y*y
        need(tot==normal,'total exact mass');C=math.comb(n,3);D=math.comb(n,4) if n>=4 else 0
        variance=C*p**3*(1-p**3)+12*D*p**5*(1-p)
        need(et==C*p**3 and et2-et*et==variance,'triangle exact moments')
        projection=N*(n-2)**2*p**5*(1-p)
        need(variance-projection==3*C*p**4*(1-p)**2+C*p**3*(1-p)**3,'orthogonal residual variance')
        if n>=4:
            need(ey==3*D*p*p,'ordinary 2K2 mean')
            need(ey2-ey*ey==N*math.comb(n-2,2)**2*p**3*(1-p)+3*D*p*p*(1-p)**2,'ordinary 2K2 variance')
        for q in [1,2,3,4,6,9,C+4]:
            residue=[F(sum(w for t,w in dist.items() if t%q==a),normal) for a in range(q)]
            delta=max(abs(q*x-1) for x in residue)
            if q>=2:
                coeff=sum(float(F(w,normal))*cmath.exp(2j*math.pi*t/q) for t,w in dist.items());need(abs(coeff)<=float(delta)+1e-13,'Fourier coefficient bounded by relative error')
            else:need(delta==0,'q1')
            for a,prob in enumerate(residue):
                inv=sum(cmath.exp(-2j*math.pi*j*a/q)*sum(float(F(w,normal))*cmath.exp(2j*math.pi*j*t/q) for t,w in dist.items()) for j in range(q))/q
                max_error=max(max_error,abs(inv-complex(float(prob))));need(abs(inv-complex(float(prob)))<1e-12,'finite Fourier inversion')
        cases.append(dict(n=n,p=str(p),mean=str(et),variance=str(variance)))
        if n>=4:need(C*p**3*(1-p**3)+6*D*p**5*(1-p)!=variance,'wrong factor6 rejected')
        need(all((6*t)%2==0 for _,t,_ in counts),'6T parity obstruction')
negative_controls=['wrong covariance factor6 differs for n>=4','6T all-even: relative q2 discrepancy exactly1']
j=dict(status='PASS',host_graphs=graphs,rational_parameter_cases=cases,conditional_edge_strata=conditional,max_finite_Fourier_error=max_error,tolerance=1e-12,negative_controls=negative_controls,scope='Finite exact rational moments and graph counts; Fourier values are floating diagnostics. Asymptotic claims are checked by written deductions relative to named source imports, not finite evidence.')
(H/'INDEPENDENT_MATH.json').write_text(json.dumps(j,indent=2)+'\n')
