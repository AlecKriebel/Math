import sympy as S,itertools,json
checks=0
def ck(v):
 global checks
 assert v
 checks+=1
a,b,c,d,u,v,x,t=S.symbols('a b c d u v x t',nonzero=True)
F=a*b*c*d+a*b+a*c-b*d+c*d;H=(a+c)*(b*d+1)+b+d
M=S.Matrix([[a+1/a+1/b,-1/a,0,-1/b],[-1/a,b+1/a+1/d,-1/d,0],[0,-1/d,c+1/c+1/d,-1/c],[-1/b,0,-1/c,d+1/b+1/c]])
ck(S.factor(a*b*c*d*M.det()-F**2-H**2)==0)
for sub,D,target in [({a:u/v,b:1,c:v/u,d:1},u*v,u*u+u*v+v*v),({a:1,b:x/(x-t),c:1,d:x/(x+t)},x*x-t*t,3*x*x-t*t)]:
 ck(S.factor(D*F.subs(sub)-target)==0);ck(S.factor(D*H.subs(sub)-2*target)==0)
# Independent enumeration of all connected simple graphs through five vertices,
# with all terminal pairs; test the squarefree balanced-network conclusion.
graphs=balanced=0
for n in range(2,6):
 es=list(itertools.combinations(range(n),2))
 for mask in range(1,1<<len(es)):
  E=[e for j,e in enumerate(es) if mask>>j&1];L=S.zeros(n)
  for i,j in E:L[i,i]+=1;L[j,j]+=1;L[i,j]-=1;L[j,i]-=1
  T=int(L[:n-1,:n-1].det())
  if not T:continue
  graphs+=1
  if any(e>1 for e in S.factorint(T).values()):continue
  for s,z in es:
   ids=[i for i in range(n) if i!=z];A=L.extract(ids,ids);ss=ids.index(s);A[ss,ss]+=1
   forest=int(A.det())-T
   if forest!=T:continue
   balanced+=1;ck((s,z) in E)
   E2=[e for e in E if e!=(s,z)];seen={s}
   while True:
    old=len(seen)
    for i,j in E2:
     if i in seen or j in seen:seen.update((i,j))
    if len(seen)==old:break
   ck(z not in seen)
# Arithmetic positivity witnesses for both prime classes, independently enumerated.
for p in S.primerange(3,1000):
 if p%4!=3:continue
 if p==3 or p%12==7:
  sols=[(i,j) for i in range(1,S.integer_nthroot(p,2)[0]+1) for j in range(1,S.integer_nthroot(p,2)[0]+1) if i*i+i*j+j*j==p]
 else:
  sols=[(i,j) for i in range(1,p+1) for j in range(-i+1,i) if 3*i*i-j*j==p]
 ck(bool(sols));ck(all(S.gcd(i,j)==1 for i,j in sols))
print(json.dumps({'status':'PASS','independent_assertions':checks,'connected_simple_graphs':graphs,'squarefree_balanced_terminal_cases':balanced},indent=2))
