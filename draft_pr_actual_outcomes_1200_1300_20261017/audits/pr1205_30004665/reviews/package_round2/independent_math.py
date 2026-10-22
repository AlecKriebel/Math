import json,pathlib,re
from collections import Counter
import sympy as s
b=pathlib.Path("draft_pr_actual_outcomes_1200_1300_20261017/audits/pr1205_30004665")
tex=(b/"publication/manuscript/main.tex").read_text()
word=(1,2,3,2,4,2,1,2,3,2,4,2);N=12
adj={frozenset(t) for t in ((1,2),(2,3),(2,4))}
def req(x,m):
 if not x:raise ValueError(m)
simple=[s.Matrix(x) for x in ((1,-1,0,0),(0,1,-1,0),(0,0,1,-1),(0,0,1,1))]
base=s.Matrix.hstack(*simple);R=[s.eye(4)-a*a.T for a in simple];g=s.eye(4);inv=[]
for k in word:
 inv.append(tuple(base.inv()*g*simple[k-1]));g=g*R[k-1]
roots=set()
for i in range(4):
 for j in range(i+1,4):
  for a in (-1,1):
   for c in (-1,1):
    e=[0]*4;e[i]=a;e[j]=c;roots.add(tuple(base.inv()*s.Matrix(e)))
pos={r for r in roots if all(t>=0 for t in r)}
req(set(inv)==pos and len(inv)==len(set(inv))==12 and g==-s.eye(4),"word/root")
nxt=[next((j for j in range(i+1,N) if word[i]==word[j]),N) for i in range(N)]
frozen={i for i,j in enumerate(nxt) if j==N};arcs=Counter()
for i in range(N):
 if nxt[i]<N:arcs[i,nxt[i]]+=1
 for j in range(i+1,N):
  if j<nxt[i]<nxt[j] and frozenset((word[i],word[j])) in adj:arcs[j,i]+=1
arcs=Counter({(a,c):v for (a,c),v in arcs.items() if not {a,c}<=frozen})
def change(A,k):
 req(k not in frozen,"frozen mutation")
 B=A.copy()
 for (a,c),v in A.items():
  if c==k:
   for (u,w),d in A.items():
    if u==k and a!=w:B[a,w]+=v*d
 for (a,c),v in A.items():
  if k in (a,c):B[a,c]-=v;B[c,a]+=v
 for a in range(N):
  for c in range(a+1,N):
   v=min(B[a,c],B[c,a]);B[a,c]-=v;B[c,a]-=v
 return Counter({(a,c):v for (a,c),v in B.items() if v and not {a,c}<=frozen})
xs=s.symbols("X1:13");routes={7:(2,6,1,3,4,8,5,10),9:(4,8,5,10),11:(10,),12:()};terms={};reports={}
for f,route in routes.items():
 A=arcs.copy();v=list(xs)
 for kk in route:
  k=kk-1;old=v[:]
  for i in range(N):
   c=A[i,k]-A[k,i]
   if i==k:v[i]=s.cancel(1/old[k])
   elif c:v[i]=s.cancel(old[i]*(1+old[k]**(-1 if c>0 else 1))**(-c))
  A=change(A,k)
 req(not any(a==f-1 and c not in frozen for a,c in A),"optimization")
 row=[A[f-1,i]-A[i,f-1] for i in range(N)]
 req(row==[(-1 if i==9 else 0) for i in range(N)],"final row")
 num,den=s.fraction(s.cancel(1/v[f-1]));ds=s.Poly(den,*xs).terms();req(len(ds)==1,"Laurent")
 de,dc=ds[0];req(dc==1,"den coeff")
 one={tuple(int(de[i]-e[i]) for i in range(N)):int(c) for e,c in s.Poly(num,*xs).terms()}
 req(all(c>0 for c in one.values()),"positive")
 for e,c in one.items():terms[e]=terms.get(e,0)+c
 reports[f]={"route":route,"terms":len(one),"row":row}
 print("forward X route",f,"terms",len(one),flush=True)
matches=re.findall(r"^(\d+) & \\texttt\{([0-9]{12})\} & \$\(([-0-9,]+)\)\$",tex,re.M);req(len(matches)==22,"TeX parse")
rows=[];zs=[]
for j,d,z in matches:
 req(int(j)==len(rows)+1,"order");rows.append(tuple(map(int,d)));zs.append(tuple(map(int,z.split(","))))
req(terms==dict.fromkeys(rows,1) and len(set(rows))==22,"TeX support/coefficients")
u=[int(i in frozen) for i in range(N)];products=[]
for j,z in enumerate(zs):
 ds=[sum(a*c for a,c in zip(r,z)) for r in rows];req(ds[j]==-1 and all(t>=0 for i,t in enumerate(ds) if i!=j),"separator");products.append(ds)
 p=[a+c for a,c in zip(z,u)]
 req(all(sum(a*c for a,c in zip(r,p))==(0 if i==j else max(1,sum(a*c for a,c in zip(r,p)))) for i,r in enumerate(rows)),"facet")
req(all(sum(a*c for a,c in zip(r,u))==1 for r in rows),"interior");req(s.Matrix(rows).rank()==12,"rank")
y=s.symbols("y1:13");i=lambda k:y[k-1];A=1+i(3)+i(2)*i(3);B=i(2)*i(3)*i(4)*i(5)
F7=1+i(6)+i(6)*i(8)*A+i(6)*i(8)*i(10)*((1+i(5))*A+B*(1+i(6)+i(1)*i(6)))
F9=1+i(8)+i(8)*i(10)*(1+i(5)+i(4)*i(5))
req(dict(s.Poly(s.expand(i(7)*F7+i(9)*F9+i(11)*(1+i(10))+i(12)),*y).terms())==terms,"compact expansion")
H=base.T*base;K=s.zeros(N)
for k in range(N):
 K[k,k]=1
 if nxt[k]<N:K[k,nxt[k]]=1
 for l in range(k+1,nxt[k]):K[k,l]=H[word[k]-1,word[l]-1]
pulled=s.Matrix(rows)*K;req(K.det()==1 and all(abs(t)<=1 for t in pulled),"chamber")
req(list(pulled.row(20))==[0,1,0,1,0,1,-1,0,0,0,0,0],"row21");req(list(pulled.row(21))==[1,0,0,0,0,0,0,0,0,0,0,0],"row22")
out={"status":"PASS","independence":"Fresh non-blinded implementation. No candidate-code imports. Euclidean roots, oriented path graph mutation, forward rational X mutation, manuscript-table input.","roots":inv,"arrows":[(a+1,c+1,v) for (a,c),v in sorted(arcs.items())],"routes":reports,"terms":[{"a":e,"coefficient":terms[e]} for e in rows],"products":products,"rank":12,"dimension":12,"facet_dimension":11,"K":K.tolist(),"transformed":pulled.tolist(),"squared_rows":[j+1 for j,r in enumerate(rows) if r[5]==2]}
print(json.dumps(out,default=int,sort_keys=True))
try:(b/"reviews/package_round2/independent_math_results.json").write_text(json.dumps(out,indent=2,default=int)+"\n")
except OSError as e:print("RESULT WRITE BLOCKED",str(e))
