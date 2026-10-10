"""Pure integer sparse-polynomial certificate, with support checks."""
from itertools import product
import json
N=0
def ck(b):
 global N
 N+=1
 assert b
ZERO=(0,)*6
def const(n):return {ZERO:n} if n else {}
def var(i):
 t=list(ZERO);t[i]=1;return {tuple(t):1}
def add(*ps):
 r={}
 for p in ps:
  for e,c in p.items():r[e]=r.get(e,0)+c
 return {e:c for e,c in r.items() if c}
def neg(p):return {e:-c for e,c in p.items()}
def sub(p,q):return add(p,neg(q))
def mul(p,q):
 r={}
 for e,c in p.items():
  for f,d in q.items():
   k=tuple(x+y for x,y in zip(e,f));r[k]=r.get(k,0)+c*d
 return {e:c for e,c in r.items() if c}
def evaluate(p,v):return sum(c*__import__('math').prod(x**e for x,e in zip(v,k)) for k,c in p.items())
def edges(U,V):
 E={}
 for u,v in product(U,V):E.setdefault(u+v,[]).append((u,v))
 return E
def main():
 a,b,c,d,e,g=[var(i) for i in range(6)];one=const(1);two=const(2)
 F={1:sub(add(a,b),one),2:sub(add(mul(a,b),c),one),3:sub(add(mul(a,c),d,e),one),8:sub(add(c,g),one),9:sub(add(mul(a,g),e),one),11:sub(add(d,a),one),12:sub(add(d,g),one)}
 M={1:mul(two,a),2:const(-2),3:one,8:sub(two,a),9:const(-1),11:sub(one,mul(two,a)),12:sub(mul(two,a),two)}
 cert=add(*(mul(M[i],F[i]) for i in F));ck(cert==one)
 for v in product(range(-2,3),repeat=6):ck(sum(evaluate(M[i],v)*evaluate(F[i],v) for i in F)==1)
 U=(0,1,3,7);V=(0,1,2,3,5,9,11,13);E=edges(U,V)
 uniq=[p[0] for p in E.values() if len(p)==1];UA={u for u,v in uniq};VB={v for u,v in uniq}
 ck(UA=={0,7});ck(VB=={0,11,13});ck(all(len(E[u+v])==1 for u,v in product(UA,VB)))
 A={0:one,1:a,3:d,7:one};B={0:one,1:b,2:c,3:e,9:g,11:one,13:one}
 # The omitted coefficient at degree5 cannot enter the seven selected degrees.
 for deg,i in [(1,1),(2,2),(3,3),(9,8),(10,9),(14,11),(16,12)]:
  ck(deg-5 not in U)
  coeff=add(*(mul(A[u],B[v]) for u in A for v in B if u+v==deg));ck(sub(coeff,one)==F[i])
 for h in range(1,101):
  for s,t in [(-7,9),(0,0),(13,-22)]:
   Eh=edges([s+h*u for u in U],[t+h*v for v in V]);ck(sorted(map(len,Eh.values()))==sorted(map(len,E.values())))
 print(json.dumps({'problem_id':159,'turn':4,'status':'PASS','exact_assertions':N,'formal_certificate_terms':len(F),'formal_identity':cert==one,'integer_specializations':5**6,'affine_support_controls':300,'scope':'One credited residual system and its affine support family. No general-degree certificate theorem or full conjecture proof.'},indent=2))
if __name__=='__main__':main()
