"""Package review 01: independent finite probes; explicit guards, not a proof."""
from fractions import Fraction as F
from decimal import Decimal as D, getcontext
from itertools import permutations
from pathlib import Path
import json, argparse, hashlib
getcontext().prec=190
tol=D('1e-160')
p=argparse.ArgumentParser();p.add_argument('--fault',default='none');args=p.parse_args()
def need(c,m):
    if not c: raise ValueError(m)
def dec(x): return D(x.numerator)/D(x.denominator) if isinstance(x,F) else D(x)
def ln(x): return dec(x).ln()
def xl(x): return D(0) if not x else dec(x)*ln(x)
def q(x):
    if not x:return D(0)
    if x==1:return D(0) if args.fault=='endpoint' else D(1)
    return -dec(x)**2*ln(x)/(1-dec(x))
def h(x):return D(0) if not x else dec(x)**2*(1-ln(x))
def div(b,a):
    if not a:need(not b,'forbidden support');return D(0)
    if not b:return D(0) if args.fault=='mass' else dec(a)
    if args.fault=='divergence':return D(0)
    return dec(b)*ln(b/a)-dec(b)+dec(a)
def near(x,m):need(abs(x)<=tol,m+': '+str(x))
def positive(x,m):need(x>=-tol,m+': '+str(x))
def suffix(row):
    orders=list(permutations(range(len(row))));v=D(0)
    for order in orders:
        for i,j in enumerate(order):
            if row[j]:v+=dec(row[j])*ln(sum((row[k] for k in order[i:]),F(0)))/len(orders)
    return v
def law(name,mu,A=None):
    n=len(next(iter(mu)));orders=list(permutations(range(n)))
    need(sum(mu.values(),F(0))==1,'law normalization')
    B=[[sum((w for x,w in mu.items() if x[i]==j),F(0)) for j in range(n)]for i in range(n)]
    H=-sum((xl(w)for w in mu.values()),D(0));cross=sum((xl(v)for row in B for v in row),D(0))
    TR=sum((suffix(row)for row in B),D(0));TC=sum((suffix([B[i][j]for i in range(n)])for j in range(n)),D(0))
    corr=-D(n)+sum((q(v)for row in B for v in row),D(0))
    # Calculate sequential nu as exact products, then KL from mu/nu directly.
    seq=D(0);exposure=D(0);nu_totals=[];histories=0
    for order in orders:
        nu={}
        for x in orders:
            used=set();v=F(1)
            for i in order:
                Z=sum((B[i][j]for j in range(n)if j not in used),F(0))
                if not Z or not B[i][x[i]]:v=F(0);break
                v*=B[i][x[i]]/Z;used.add(x[i])
            nu[x]=v
        nu_totals.append(sum(nu.values(),F(0)))
        if A is not None and all(v>0 for row in A for v in row):need(nu_totals[-1]==1,'positive sequential law normalized')
        orderkl=D(0)
        for x,w in mu.items():
            need(nu[x]>0,'supported nu positive')
            orderkl+=dec(w)*ln(w/nu[x])
            used=set()
            for i in order:
                Z=sum((B[i][j]for j in range(n)if j not in used),F(0));need(Z>0,'supported normalizer')
                exposure+=dec(w)*ln(Z)/len(orders);used.add(x[i])
        positive(orderkl,'sequential KL');seq+=orderkl/len(orders)
        chain=D(0)
        for depth,i in enumerate(order):
            buckets={}
            for x,w in mu.items():buckets.setdefault(tuple(x[r]for r in order[:depth]),[]).append((x,w))
            for key,sub in buckets.items():
                histories+=1;mass=sum((w for x,w in sub),F(0));c=[sum((w for x,w in sub if x[i]==j),F(0))/mass for j in range(n)]
                CH=-sum((xl(v)for v in c),D(0));Z=sum((B[i][j]for j in range(n)if j not in key),F(0))
                need(Z>0,'positive-history normalizer')
                cx=sum((dec(c[j])*ln(B[i][j])for j in range(n)if c[j]),D(0))
                positive(ln(Z)-CH-cx,'conditional KL');chain+=dec(mass)*CH
        near(chain-H,'chain rule')
    near(exposure-TR,'row suffix equals exposure')
    near(seq-(TR-H-cross),'direct sequential KL equals chain slack')
    positive(corr-TR,'Jensen rows');positive(corr-TC,'Jensen cols');positive(corr-H-cross,'entropy lemma')
    C=sum((xl(1-v)for row in B for v in row),D(0));HB=-cross+C
    coefficient=D(1) if args.fault=='half' else D('0.5')
    rhs=HB+coefficient*(TR+TC-2*C)
    near(rhs-(-cross+(TR+TC)/2),'Dong-Jain coefficient cancellation');positive(rhs-H,'Dong-Jain bound')
    rec={'name':name,'n':n,'histories':histories,'sequential_mass_min':str(min(nu_totals)),'D_seq_direct':str(seq),'entropy_slack':str(corr-H-cross)}
    if A is not None:
        weights={x:prod([A[i][x[i]]for i in range(n)])for x in orders};P=sum(weights.values(),F(0))
        DM=sum((dec(B[i][j])*ln(B[i][j]/A[i][j])for i in range(n)for j in range(n)if B[i][j]),D(0))
        SD=sum((div(B[i][j],A[i][j])for i in range(n)for j in range(n)),D(0));near(DM-SD,'all-entry mass cancellation')
        used=DM if args.fault=='KL' else (D(0)if args.fault=='drop' else seq)
        near(ln(P)-(-DM+TR-used),'Anari identity direct sequential KL')
        S=sum((v*v for row in A for v in row),F(0));need(S>=1,'row Frobenius lower')
        raw=sum((h(v)for row in A for v in row),D(0));positive(dec(S)*(1+ln(n))-raw,'norm entropy')
        E4=D(4).exp();positive(-n+E4*raw-ln(P),'per bound')
        if n>=2 or args.fault=='n1':positive(3*E4*dec(S)*ln(n)-n-ln(P),'purepower valid range')
        rec['D_matrix']=str(DM);rec['S']=str(S);rec['permanent']=str(P)
    return rec
def prod(xs):
    v=F(1)
    for x in xs:v*=x
    return v
matrices=[('unit',[[1]]),('repeated_column',[[1,0],[1,0]]),('unused_positive',[[F(1,3),F(2,3)],[0,1]]),('asym2',[[F(3,5),F(2,5)],[F(1,7),F(6,7)]]),('asym3',[[F(2,7),F(3,7),F(2,7)],[F(5,11),F(4,11),F(2,11)],[F(1,13),F(8,13),F(4,13)]]),('sparsecycle',[[F(1,2),F(1,2),0],[F(1,2),0,F(1,2)],[0,F(1,2),F(1,2)]]),('blocks',[[F(1,2),F(1,2),0,0],[F(1,2),F(1,2),0,0],[0,0,F(1,2),F(1,2)],[0,0,F(1,2),F(1,2)]])]
records=[]
for name,A in matrices:
    A=[[F(v)for v in row]for row in A];n=len(A);ws={x:prod([A[i][x[i]]for i in range(n)])for x in permutations(range(n))};P=sum(ws.values(),F(0))
    if not P:records.append({'name':name,'permanent':'0','Gibbs_not_defined':True});continue
    records.append(law(name,{x:w/P for x,w in ws.items()if w},A))
records.append(law('four_atoms4',{(0,1,2,3):F(1,15),(1,0,3,2):F(2,15),(2,3,0,1):F(4,15),(3,2,1,0):F(8,15)}))
records.append(law('three_atoms3',{(0,1,2):F(2,17),(1,2,0):F(7,17),(2,0,1):F(8,17)}))
# Wide scalar boundary probes at 190 digits; all are finite diagnostics.
vals={D(0),D(1),D('0.125'),D('0.275'),D('0.5'),D('0.875')}
for k in [2,20,90,140,300]:vals.add(D(10)**-k)
for k in [2,20,90,140]:vals.add(1-D(10)**-k)
pairs={(a,b)for a in vals for b in vals if a or not b}
for a in vals:
    if a and D(2).exp()*a<=1:
        for r in [1-D('1e-130'),D(1),1+D('1e-130')]:pairs.add((a,D(2).exp()*a*r))
for a,b in pairs:positive(D(4).exp()*h(a)-q(b)+div(b,a),'scalar probe')
report={'pass':True,'fault':args.fault,'digits':getcontext().prec,'tolerance':str(tol),'matrix_cases':len(matrices),'arbitrary_laws':2,'scalar_pairs':len(pairs),'histories':sum(r.get('histories',0)for r in records),'records':records,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Independent finite Fraction enumeration and Decimal logarithms; direct explicit sequential nu products, not interval or universal proof.'}
Path('INDEPENDENT_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
