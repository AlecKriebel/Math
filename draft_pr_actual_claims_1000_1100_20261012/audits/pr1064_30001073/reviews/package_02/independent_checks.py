"""New independent finite diagnostics; exact combinatorics and Decimal logs.
Not an interval certificate or universal proof. All checks use explicit raises.
"""
from fractions import Fraction as F
from decimal import Decimal as D, getcontext
from itertools import permutations, product
from collections import defaultdict
import argparse, hashlib, json
from pathlib import Path

getcontext().prec=160
TOL=D('1e-120')
p=argparse.ArgumentParser();p.add_argument('--fault',default='none');p.add_argument('--output',required=True)
args=p.parse_args()
def require(c,m):
    if not c: raise ValueError(m)
def dec(x):return D(x.numerator)/D(x.denominator) if isinstance(x,F) else D(x)
def xl(x):return dec(x)*dec(x).ln() if x else D(0)
def q(b):
    if not b:return D(0)
    if b==1:return D(0) if args.fault=='q-unit' else D(1)
    z=dec(b);return -z*z*z.ln()/(1-z)
def h(a):return dec(a)**2*(1-dec(a).ln()) if a else D(0)
def div(b,a):
    if not a:require(not b,'bad support');return D(0)
    if not b:return D(0) if args.fault=='drop-zero-a' else dec(a)
    return dec(b)*(dec(b)/dec(a)).ln()-dec(b)+dec(a)
def close(x,m):require(abs(x)<TOL,m+': '+str(x))
def nonneg(x,m):require(x>=-TOL,m+': '+str(x))
def tail(row):
    result=D(0);orders=list(permutations(range(len(row))))
    for o in orders:
        for k,j in enumerate(o):
            if row[j]:result+=dec(row[j])*dec(sum(row[t] for t in o[k:])).ln()/len(orders)
    return result

def check_law(mu):
    n=len(next(iter(mu)));require(sum(mu.values())==1,'law normalization')
    B=[[sum((w for x,w in mu.items() if x[i]==j),F(0)) for j in range(n)] for i in range(n)]
    H=-sum(map(xl,mu.values()));cross=sum((xl(b) for row in B for b in row),D(0))
    orders=list(permutations(range(n)));Elog=D(0);histories=0
    for o in orders:
        chain=D(0)
        for k,i in enumerate(o):
            groups=defaultdict(dict)
            for x,w in mu.items():groups[tuple(x[t] for t in o[:k])][x]=w
            for used,sub in groups.items():
                histories+=1;mass=sum(sub.values());Z=sum(B[i][j] for j in range(n) if j not in used)
                require(mass>0 and Z>0,'supported history mass')
                cond=[sum((w for x,w in sub.items() if x[i]==j),F(0))/mass for j in range(n)]
                ch=-sum(map(xl,cond));cb=sum((dec(cond[j])*dec(B[i][j]).ln() for j in range(n) if cond[j]),D(0))
                nonneg(dec(Z).ln()-ch-cb,'local KL')
                chain+=dec(mass)*ch;Elog+=dec(mass)*dec(Z).ln()/len(orders)
        close(chain-H,'entropy chain')
    correction=-D(n)+sum((q(b) for row in B for b in row),D(0))
    rows=sum((tail(row) for row in B),D(0));cols=sum((tail([B[i][j] for i in range(n)]) for j in range(n)),D(0))
    close(rows-Elog,'suffix/order correspondence')
    nonneg(Elog-H-cross,'KL chain slack');nonneg(correction-Elog,'Jensen direction')
    C=sum((xl(1-b) for row in B for b in row),D(0));coef=D(1) if args.fault=='DJ-half' else D('.5')
    dj=-cross+C+coef*(rows+cols-2*C)
    close(dj-(-cross+(rows+cols)/2),'Dong-Jain cancellation')
    nonneg(dj-H,'Dong-Jain entropy inequality')
    return B,H,rows,correction,histories

def check_matrix(A):
    n=len(A);A=[[F(v) for v in row] for row in A]
    require(all(sum(row)==1 and min(row)>=0 for row in A),'row stochastic')
    weights={}
    for x in permutations(range(n)):
        v=F(1)
        for i,j in enumerate(x):v*=A[i][j]
        if v:weights[x]=v
    P=sum(weights.values());S=sum(a*a for row in A for a in row)
    require(1<=S<=n,'unnormalized S range')
    if not P:return {'n':n,'permanent':'0','histories':0}
    mu={x:v/P for x,v in weights.items()};B,H,T,C,count=check_law(mu)
    matrix=sum((dec(B[i][j])*(dec(B[i][j])/dec(A[i][j])).ln() for i in range(n) for j in range(n) if B[i][j]),D(0))
    scalar=sum((div(B[i][j],A[i][j]) for i in range(n) for j in range(n)),D(0))
    close(matrix-scalar,'total-mass cancellation')
    energy=sum((dec(B[i][j])*dec(A[i][j]).ln() for i in range(n) for j in range(n) if B[i][j]),D(0))
    close(dec(P).ln()-H-energy,'Gibbs identity')
    seq=D(0);orders=list(permutations(range(n)));positive=all(a>0 for row in A for a in row)
    for o in orders:
        nu={}
        for x in permutations(range(n)):
            prob=F(1);used=set()
            for i in o:
                Z=sum(B[i][j] for j in range(n) if j not in used)
                if not Z or not B[i][x[i]]:prob=F(0);break
                prob*=B[i][x[i]]/Z;used.add(x[i])
            nu[x]=prob
        if positive:require(sum(nu.values())==1,'positive sequential normalization')
        for x,v in mu.items():
            require(nu[x]>0,'sequential supported target')
            seq+=dec(v)*(dec(v)/dec(nu[x])).ln()/len(orders)
    close(seq-(T-H-sum((xl(b) for row in B for b in row),D(0))),'direct sequential KL versus chain')
    used=matrix if args.fault=='KL-confusion' else (D(0) if args.fault=='drop-seq' else seq)
    close(dec(P).ln()-(-matrix+T-used),'Anari exact expanded identity')
    nonneg(C-matrix-dec(P).ln(),'Gibbs entropy bound')
    raw=sum((h(a) for row in A for a in row),D(0));E4=D(4).exp()
    nonneg(-n+E4*raw-dec(P).ln(),'first theorem')
    norm=-n+E4*dec(S)*(1+D(n).ln())
    nonneg(norm-(-n+E4*raw),'square-entropy conversion')
    if n>=2 or args.fault=='n1-pure':nonneg(3*E4*dec(S)*D(n).ln()-n-dec(P).ln(),'pure-power range')
    return {'n':n,'permanent':str(P),'S':str(S),'histories':count,'D_matrix':str(matrix),'D_seq':str(seq),'bound_slack':str(norm-dec(P).ln())}

matrices=[[[1]],[[F(2,3),F(1,3)],[0,1]],[[1,0],[1,0]],[[F(3,5),F(2,5)],[F(1,4),F(3,4)]],[[F(1,3)]*3 for _ in range(3)]]
for n in (2,3,4):
    for seed in range(1,5):
        rows=[]
        for i in range(n):
            row=[((seed+2)*(i+3)+(j+1)**2)%11 for j in range(n)]
            if not sum(row):row[0]=1
            rows.append([F(v,sum(row)) for v in row])
        matrices.append(rows)
records=[check_matrix(a) for a in matrices]
laws=[{(0,1,2):F(1,5),(1,2,0):F(1,5),(2,0,1):F(3,5)},
      {(0,1,2,3):F(2,9),(1,0,3,2):F(7,9)}]
law_counts=[check_law(mu)[-1] for mu in laws]
vals={D(0),D(1),D('.2'),D('.5'),D('.8')}
for k in [1,2,8,20,40,100]:vals.add(D(10)**-k);vals.add(1-D(10)**-k)
pairs=set(product(vals,vals));E2=D(2).exp()
for a in vals:
    if a>0 and E2*a<1:
        for factor in [1-D('1e-90'),D(1),1+D('1e-90')]:pairs.add((a,E2*a*factor))
count=0
for a,b in pairs:
    if not a and b:continue
    count+=1
    nonneg(b-q(b),'q<=b');nonneg(h(b)-q(b),'q<=h')
    nonneg(div(b,a),'d>=0');nonneg(D(4).exp()*h(a)-q(b)+div(b,a),'scalar bound')
report={'pass':True,'matrix_cases':len(matrices),'arbitrary_laws':len(laws),'positive_histories':sum(x['histories'] for x in records)+sum(law_counts),'scalar_probes':count,'precision':160,'tolerance':str(TOL),'fault':args.fault,'scope':'Finite exact Fraction enumeration with Decimal logarithms. No interval or universal certification. Explicit raises active under optimization.','records':records,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(args.output).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='records'},indent=2))
