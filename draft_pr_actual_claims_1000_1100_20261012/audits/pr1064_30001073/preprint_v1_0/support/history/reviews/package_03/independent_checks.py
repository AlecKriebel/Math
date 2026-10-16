"""New exact finite permutation models with Decimal diagnostics; no assert checks."""
from fractions import Fraction as F
from decimal import Decimal as D, getcontext
from itertools import permutations, product
from collections import defaultdict
import argparse, json, random
getcontext().prec=170
TOL=D('1e-135')
p=argparse.ArgumentParser();p.add_argument('--fault',default='none');fault=p.parse_args().fault
def need(x,m):
 if not x:raise ValueError(m)
def dec(x):return D(x.numerator)/D(x.denominator) if isinstance(x,F) else D(x)
def xl(x):return dec(x)*dec(x).ln() if x else D(0)
def q(x):
 if not x:return D(0)
 if x==1:return D(0) if fault=='unit' else D(1)
 z=dec(x);return -z*z*z.ln()/(1-z)
def h(x):return dec(x)**2*(1-dec(x).ln()) if x else D(0)
def div(b,a):
 if not a:need(not b,'support');return D(0)
 if not b:return D(0) if fault=='zero-divergence' else dec(a)
 return dec(b)*(dec(b)/dec(a)).ln()-dec(b)+dec(a)
def ge(x,m):need(x>=-TOL,m)
def eq(x,m):need(abs(x)<=TOL,m)
def suffix(row):
 z=D(0);orders=list(permutations(range(len(row))))
 for order in orders:
  for pos,j in enumerate(order):
   if row[j]:z+=dec(row[j])*dec(sum((row[k] for k in order[pos:]),F(0))).ln()/len(orders)
 return z
def audit_law(law,name):
 n=len(next(iter(law)));need(sum(law.values(),F(0))==1,'law mass')
 b=[[sum((v for x,v in law.items() if x[i]==j),F(0)) for j in range(n)] for i in range(n)]
 H=-sum(map(xl,law.values()),D(0));cross=sum((xl(t) for row in b for t in row),D(0))
 eZ=D(0);histories=0;seqKL=D(0)
 orders=list(permutations(range(n)))
 for order in orders:
  chain=D(0)
  for depth,i in enumerate(order):
   cells=defaultdict(list)
   for x,w in law.items():cells[tuple(x[k] for k in order[:depth])].append((x,w))
   for prior,cell in cells.items():
    histories+=1;mass=sum((w for x,w in cell),F(0));unused=set(range(n))-set(prior)
    Z=sum((b[i][j] for j in unused),F(0));need(Z>0,'positive history normalizer')
    c=[sum((w for x,w in cell if x[i]==j),F(0))/mass for j in range(n)]
    hc=-sum(map(xl,c),D(0));bc=sum((dec(c[j])*dec(b[i][j]).ln() for j in unused if c[j]),D(0))
    ge(dec(Z).ln()-hc-bc,'conditional KL');chain+=dec(mass)*hc;eZ+=dec(mass)*dec(Z).ln()/len(orders)
  eq(chain-H,'chain rule')
  for x,w in law.items():
   used=set();prob=F(1)
   for i in order:
    mass=sum((b[i][j] for j in range(n) if j not in used),F(0));need(mass>0 and b[i][x[i]]>0,'supported sequential path')
    prob*=b[i][x[i]]/mass;used.add(x[i])
   seqKL+=dec(w)*(dec(w)/dec(prob)).ln()/len(orders)
 ge(eZ-H-cross,'chain summed');eq(seqKL-(eZ-H-cross),'direct sequential KL identity')
 corr=-D(n)+sum((q(t) for row in b for t in row),D(0));ge(corr-eZ,'Jensen')
 rows=sum((suffix(row) for row in b),D(0));cols=sum((suffix([b[i][j] for i in range(n)]) for j in range(n)),D(0))
 eq(rows-eZ,'coordinate suffix substitution')
 complement=sum((xl(1-t) for row in b for t in row),D(0));coef=D(1) if fault=='half' else D('.5')
 DJ=-cross+complement+coef*(rows+cols-2*complement)
 eq(DJ-(-cross+(rows+cols)/2),'Dong-Jain expansion');ge(DJ-H,'Dong-Jain law inequality');ge(-cross+corr-DJ,'Jensen two sides')
 return b,H,cross,seqKL,rows,{'name':name,'n':n,'support':len(law),'histories':histories,'entropy_slack':str(corr-H-cross),'sequential_KL':str(seqKL)}
cases=[[[F(1)]],[[F(2,3),F(1,3)],[F(1),F(0)]],[[F(1),F(0)],[F(1),F(0)]]]
for i,j in product(range(5),repeat=2):cases.append([[F(i,4),F(4-i,4)],[F(j,4),F(4-j,4)]])
rng=random.Random(106403)
for n in [3,3,3,4,4,4]:
 rows=[]
 for i in range(n):
  values=[rng.randrange(0,8) for _ in range(n)];values[i]+=1;s=sum(values);rows.append([F(v,s) for v in values])
 cases.append(rows)
cases.append([[1-F(1,10**65),F(1,10**65)],[F(1,10**57),1-F(1,10**57)]])
reports=[];per_zero=0
for idx,A in enumerate(cases):
 n=len(A);need(all(sum(row,F(0))==1 for row in A),'row sum');weights={}
 for x in permutations(range(n)):
  w=F(1)
  for i,j in enumerate(x):w*=A[i][j]
  if w:weights[x]=w
 per=sum(weights.values(),F(0));S=sum((a*a for row in A for a in row),F(0));need(S>=1,'Cauchy')
 if not per:per_zero+=1;continue
 law={x:w/per for x,w in weights.items()};b,H,cross,seq,rows,report=audit_law(law,'matrix'+str(idx))
 dm=sum((dec(b[i][j])*(dec(b[i][j])/dec(A[i][j])).ln() for i in range(n) for j in range(n) if b[i][j]),D(0))
 ds=sum((div(b[i][j],A[i][j]) for i in range(n) for j in range(n)),D(0));eq(dm-ds,'linear mass cancellation')
 used=dm if fault=='KL-confusion' else (D(0) if fault=='drop-sequential' else seq)
 eq(dec(per).ln()-(-dm+rows-used),'Anari expansion direct reference')
 energy=sum((dec(b[i][j])*dec(A[i][j]).ln() for i in range(n) for j in range(n) if b[i][j]),D(0));eq(dec(per).ln()-H-energy,'Gibbs')
 raw=sum((h(a) for row in A for a in row),D(0));ge(D(4).exp()*raw-D(n)-dec(per).ln(),'entry bound');ge(dec(S)*(1+D(n).ln())-raw,'square entropy')
 for i,j in product(range(n),repeat=2):ge(D(4).exp()*h(A[i][j])-q(b[i][j])+div(b[i][j],A[i][j]),'scalar applied')
 if n>1 or fault=='n1':ge(D(3)*D(4).exp()*dec(S)*D(n).ln()-n-dec(per).ln(),'pure power range')
 report['S']=str(S);report['permanent']=str(per);report['D_matrix']=str(dm);reports.append(report)
extra=[{(0,1,2,3):F(2,19),(1,0,3,2):F(4,19),(2,3,0,1):F(13,19)}, {(0,1,2):F(5,23),(2,1,0):F(7,23),(1,2,0):F(11,23)}]
for idx,law in enumerate(extra):reports.append(audit_law(law,'arbitrary'+str(idx))[-1])
values=[D(0),D(1),D('.37'),D('.83')]+[D(10)**(-k) for k in [2,7,31,80,130]]+[1-D(10)**(-k) for k in [4,30,80]]
probes=[(a,b) for a,b in product(values,repeat=2) if a or not b]
for a in values:
 if 0<a<D(1)/D(2).exp():
  for scale in [1-D('1e-60'),D(1),1+D('1e-60')]:probes.append((a,D(2).exp()*a*scale))
for a,b in probes:ge(D(4).exp()*h(a)-q(b)+div(b,a),'independent scalar probe')
print(json.dumps({'pass':True,'precision':170,'tolerance':str(TOL),'matrix_inputs':len(cases),'permanent_zero_inputs':per_zero,'arbitrary_laws':len(extra),'positive_histories':sum(x['histories'] for x in reports),'scalar_probes':len(probes),'reports':reports,'scope':'Exact Fraction enumeration and noninterval Decimal finite corroboration; analytic proof is separate.'},indent=2))
