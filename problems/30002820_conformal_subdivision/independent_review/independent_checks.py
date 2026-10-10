from fractions import Fraction as F
from itertools import combinations,product
import sympy as S,json
N=0
def ck(x):
 global N
 assert x;N+=1
faces0=[tuple(c) for c in combinations(range(4),3)];edges0=list(combinations(range(4),2));cols={}
for e in edges0:
 forbidden={cols[f] for f in cols if any(set(e)|set(f)<=set(t) for t in faces0)}
 cols[e]=next(c for c in range(5) if c not in forbidden)
order=sorted(edges0,key=lambda e:(cols[e],e))
def refine(mult):
 faces=list(faces0);length={e:mult[e[0]]*mult[e[1]] for e in edges0};factor=dict(enumerate(mult));splits={}
 for e in order:
  i,j=e;m=len(factor);inc=[f for f in faces if i in f and j in f];op=[next(v for v in f if v not in e) for f in inc];k=min(op)
  L=lambda a,b:length[tuple(sorted((a,b)))]
  t=L(i,k)/(L(i,k)+L(j,k));old=L(i,j)
  length[(i,m)]=t*old;length[(j,m)]=(1-t)*old
  for q in op:length[(q,m)]=(1-t)*L(i,q)+t*L(j,q)
  del length[e];faces=[f for f in faces if f not in inc]
  for q in op:faces.extend([tuple(sorted((i,m,q))),tuple(sorted((m,j,q)))])
  splits[e]=(m,t);factor[m]=F(0)
  for f in faces:
   l=[L(a,b) for a,b in combinations(f,2)]
   ck(all(sum(l)-2*x>0 for x in l))
 return faces,length,splits
rf,rl,rs=refine([F(1)]*4)
for mult in product([F(9,10),F(1),F(11,10)],repeat=4):
 f,l,ss=refine(mult);ck(f==rf);ck(len(f)==16);fac=dict(enumerate(mult))
 for i,j in order:
  m,t=rs[(i,j)];D=fac[i]*t+fac[j]*(1-t);fac[m]=fac[i]*fac[j]/D
  ck(ss[(i,j)][1]==fac[i]*t/D)
  ck(l[(i,m)]+l[(j,m)]==mult[i]*mult[j])
 for (i,j),v in l.items():ck(v==fac[i]*fac[j]*rl[(i,j)])
a,b,c,t=S.symbols('a b c t');hh=(1-t)*b+t*a;he=(1-t)*b*b+t*a*a-t*(1-t)*c*c
ck(S.expand(hh*hh-he-t*(1-t)*(c*c-(a-b)**2))==0)
ck(S.expand(b+t*c-hh-t*(b+c-a))==0)
ck(S.expand(a+(1-t)*c-hh-(1-t)*(a+c-b))==0)
print(json.dumps({'status':'PASS','independent_exact_assertions':N,'tetrahedral_metric_pairs':81,'output_faces_per_pair':16},indent=2))
