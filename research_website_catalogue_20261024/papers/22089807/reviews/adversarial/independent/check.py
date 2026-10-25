"""Independent exact, labelled-chain adversarial checks. No submitted imports.

Deliberately uses only standard-library rational arithmetic. Dropping the
positive statewise Moran clock leaves absorption probabilities unchanged.
"""
from fractions import Fraction as F
from pathlib import Path
import json, hashlib, datetime

OUT=Path(__file__).parent

def solve(a,b):
    a=[list(x)+list(y) for x,y in zip(a,b)]
    n=len(a); k=len(b[0])
    for j in range(n):
        p=next(i for i in range(j,n) if a[i][j])
        a[j],a[p]=a[p],a[j]
        z=a[j][j]; a[j]=[v/z for v in a[j]]
        for i in range(n):
            if i==j or not a[i][j]: continue
            z=a[i][j]; a[i]=[x-z*y for x,y in zip(a[i],a[j])]
    return [row[n:n+k] for row in a]

def graph(C,m,q,sigma,eps):
    n=C+m+2*q; w=[[F(0) for _ in range(n)] for _ in range(n)]
    def edge(i,j,z): w[i][j]=w[j][i]=F(z)
    for i in range(C):
        for j in range(i): edge(i,j,1)
    for j in range(C,C+m): edge(0,j,1)
    for k in range(q):
        a=C+m+2*k; edge(a,a+1,F(C)/sigma)
        for u in (a,a+1):
            for j in range(C): edge(u,j,eps)
    return w

def generator(w,r,U):
    n=len(w); N=1<<n; d=list(map(sum,w)); out=[]
    for S in range(N):
        z={}
        for v in range(n):
            tv=(S>>v)&1
            if U=='Bd':
                rate=sum(((r if (S>>u)&1 else 1)*w[u][v]/d[u]
                         for u in range(n) if ((S>>u)&1)!=tv),F(0))
            else:
                den=sum(((r if (S>>u)&1 else 1)*w[u][v] for u in range(n)),F(0))
                rate=sum(((r if (S>>u)&1 else 1)*w[u][v] for u in range(n)
                          if ((S>>u)&1)!=tv),F(0))/den
            if rate: z[S^(1<<v)]=rate
        z[S]=-sum(z.values(),F(0)); out.append(z)
    return out

def committor(g):
    N=len(g); T=list(range(1,N-1))
    x=solve([[-g[i].get(j,F(0)) for j in T] for i in T],
            [[g[i].get(N-1,F(0))] for i in T])
    return [F(0)]+[z[0] for z in x]+[F(1)]

def label(S,C,m,q):
    h=S&1; i=sum((S>>v)&1 for v in range(1,C)); l=sum((S>>v)&1 for v in range(C,C+m))
    pair=[sum((S>>(C+m+2*k+j))&1 for j in (0,1)) for k in range(q)]
    return (h,i,pair.count(1),pair.count(2),l)

def derivative_from_macro(w0,w1,S,r,U):
    # Exact coefficient of epsilon: every changing event at a macro state
    # uses a cross edge of weight epsilon, so denominator derivatives vanish.
    n=len(w0); d=list(map(sum,w0)); z={}
    for v in range(n):
        tv=(S>>v)&1
        if U=='Bd':
            rate=sum(((r if (S>>u)&1 else 1)*w1[u][v]/d[u]
                      for u in range(n) if ((S>>u)&1)!=tv),F(0))
        else:
            den=sum(((r if (S>>u)&1 else 1)*w0[u][v] for u in range(n)),F(0))
            rate=sum(((r if (S>>u)&1 else 1)*w1[u][v]
                      for u in range(n) if ((S>>u)&1)!=tv),F(0))/den
        if rate: z[S^(1<<v)]=rate
    z[S]=-sum(z.values(),F(0)); return z

def audit(C,m,q,sigma,r,U):
    n=C+m+2*q; w0=graph(C,m,q,sigma,0); w=graph(C,m,q,sigma,F(1,8))
    g=generator(w,r,U); groups={}
    for S,row in enumerate(g):
        assert sum(row.values())==0
        agg={}
        for T,z in row.items():
            key=label(T,C,m,q); agg[key]=agg.get(key,F(0))+z
        agg={k:v for k,v in agg.items() if v}
        key=label(S,C,m,q)
        if key in groups: assert groups[key]==agg
        groups[key]=agg
    assert q==1
    H=(1<<(C+m))-1; P=((1<<n)-1)^H; M=[0,P,H,(1<<n)-1]
    G0=generator(w0,r,U); ff=[s for s in range(1<<n) if s not in M]
    R=solve([[-G0[i].get(j,F(0)) for j in ff] for i in ff],
            [[G0[i].get(j,F(0)) for j in M] for i in ff])
    ret={s:row for s,row in zip(ff,R)}
    w1=[[F(int(w[i][j]!=w0[i][j])) for j in range(n)] for i in range(n)]
    L=[]
    for S in M:
        der=derivative_from_macro(w0,w1,S,r,U)
        L.append([der.get(T,F(0))+sum((v*ret[X][j] for X,v in der.items() if X in ret),F(0))
                  for j,T in enumerate(M)])
    # Derive isolated module committors independently, then compare the four
    # macro transition coefficients to the paper table.
    center=[row[:C+m] for row in w0[:C+m]]
    hp=committor(generator(center,r,U)); hm=committor(generator(center,1/r,U))
    corep=sum((hp[1<<v] for v in range(C)),F(0))/C
    corem=sum((hm[1<<v] for v in range(C)),F(0))/C
    IH=sum((1/sum(center[v]) for v in range(C)),F(0)); IP=2*sigma/C
    if U=='Bd':
        A=C*r*IP*corep; D=2*IH/(r+1); B=2*r*IH*r/(r+1); Cp=C*IP*corem
    else:
        Jp=sum((hp[1<<v]/sum(center[v]) for v in range(C)),F(0))
        Jm=sum((hm[1<<v]/sum(center[v]) for v in range(C)),F(0))
        A=2*r*Jp; D=sigma/r; B=r*sigma; Cp=2*Jm/r
    assert (L[1][3],L[1][0],L[2][3],L[2][0])==(A,D,B,Cp)
    macroP=A/(A+D); macroH=B/(B+Cp)
    aH=sum((hp[1<<v] for v in range(C+m)),F(0))/(C+m)
    aP=r/(r+1) if U=='Bd' else F(1,2)
    trace=F(C+m,n)*aH*macroH+F(2,n)*aP*macroP
    actual=[]
    for e in (3,7):
        h=committor(generator(graph(C,m,q,sigma,F(1,2**e)),r,U))
        rho=sum((h[1<<v] for v in range(n)),F(0))/n
        actual.append({'e':e,'fixation':str(rho),'trace_error':str(rho-trace)})
    return {'C':C,'m':m,'q':q,'sigma':str(sigma),'r':str(r),'rule':U,
            'labelled_states':1<<n,'orbit_fibres':len(groups),'macro_exact':True,
            'macro_coefficients':[str(v) for v in (A,D,B,Cp)],'finite_trace':str(trace),
            'finite_positive_cut_comparisons':actual}

def complete(n,r,U):
    w=[[F(int(i!=j)) for j in range(n)] for i in range(n)]
    h=committor(generator(w,r,U)); rho=sum((h[1<<v] for v in range(n)),F(0))/n
    expected=F(1,n) if r==1 else ((1-1/r)/(1-r**(-n)) if U=='Bd'
                else F(n-1,n)*(1-1/r)/(1-r**(-(n-1))))
    assert rho==expected
    return {'n':n,'r':str(r),'rule':U,'uniform_fixation':str(rho),'exact_baseline_identity':True}

def polytrim(p):
    while p and not p[-1]: p.pop()
    return p
def rem(p,q):
    p=p[:]
    while len(p)>=len(q):
        a=p[-1]/q[-1]; shift=len(p)-len(q)
        for j,b in enumerate(q): p[j+shift]-=a*b
        polytrim(p)
    return p
def ev(p,x):
    a=F(0)
    for v in reversed(p): a=a*x+v
    return a
def sturm(p):
    seq=[p,[i*p[i] for i in range(1,len(p))]]
    while seq[-1]:
        z=[-a for a in rem(seq[-2],seq[-1])]
        if not z: break
        seq.append(z)
    return seq
def variations(seq,x):
    v=[ev(p,x) for p in seq]; s=[1 if x>0 else -1 for x in v if x]
    return sum(a!=b for a,b in zip(s,s[1:]))

if __name__=='__main__':
    result={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'independence':'Written and run before inspecting submitted certificates or other reviewer opinions.',
            'baseline':[],'finite_audits':[]}
    for U in ('Bd','dB'):
        for r in (F(1,2),F(1),F(3,2),F(3)):
            result['baseline'].append(complete(4,r,U))
        for r in (F(1),F(3,2),F(3)):
            result['finite_audits'].append(audit(3,1,1,F(1,3),r,U))
    p=list(map(F,[1,-6,21,-30,22,-8,1])); seq=sturm(p)
    rootcounts=[variations(seq,a)-variations(seq,b) for a,b in ((F(1),F(3,2)),(F(3,2),F(151,100)))]
    assert rootcounts==[0,1]
    assert ev(p,F(3,2))==F(1,64)
    assert ev(p,F(151,100))==-F(39866792399,10**12)
    sig=F(19,137); lam=F(20,27); r=F(3,2)
    B=2*(sig-1)/(1+sig*(r*r-1))+lam/(r-1)
    D=2*(r*(2-r)-sig)/(sig+2*r*(r-1))-lam
    assert (B,D)==(F(232,17361),F(65,12123))
    result['algebra']={'sturm_root_counts':rootcounts,'rational_margins':[str(B),str(D)]}
    result['status']='PASS: exact finite identities; not a numerical proof of population asymptotics'
    (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'audits':len(result['finite_audits'])}))
