import itertools,math,json
n=0
def ck(b):
 global n
 assert b;n+=1
for p in (2,3,5,7,11,13,17,19):
 for k in range(1,201):
  v=[sum((-1)**(k-j)*math.comb(k,j) for j in range(i,k+1,p)) for i in range(p)]
  def val(a):
   if not a:return 10000
   r=0
   while a%p==0:r+=1;a//=p
   return r
  a=min(map(val,v));ck(a==(k-1)//(p-1));ck(sum(v)==0)
  for e in range(1,8):ck(all(x%(p**e)==0 for x in v)==(k>=e*(p-1)+1))
for q in (2,3,4,5,7):
 pts=list(itertools.product(range(q),repeat=3))
 def mul(u,v):
  a,b,c=u;d,e,f=v;return ((a+d)%q,(b+e)%q,(c+f+a*e)%q)
 def theta(u):
  a,b,c=u;return b,a,(a*b-c)%q
 for u in pts:
  ck(theta(theta(u))==u)
  for v in pts:ck(theta(mul(u,v))==mul(theta(u),theta(v)))
 U={u for u in pts if u[0]==0};V={theta(u) for u in U};ck(U!=V)
# Scalar inclusion lattices: scaling preserves exponent differences.
for d in range(2,9):
 for exps in itertools.product(range(4),repeat=2):
  v=exps+(0,)*(d-2)
  for b in range(6):ck((len(set(v))==1)==(len(set(a+b for a in v))==1))
print(json.dumps({'result':'PASS','assertions':n,'scope':'Bounded independent controls only, no author imports'},indent=2))
