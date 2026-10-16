"""Direct binary64 construction check. Diagnostic only; not a proof certificate."""
import math,json
fib=[0,1]
for n in range(2,18):fib.append(fib[-1]+fib[-2])
out=[];pairs=0
for n in range(3,18):
 q,p=fib[n],fib[n-1]
 pts=[]
 for k in range(q):
  h=1-2*k/q;r=2*math.sqrt((k/q)*(1-k/q));ang=2*math.pi*((p*k)%q)/q
  pts.append((r*math.cos(ang),r*math.sin(ang),h))
 best=float('inf');arg=None
 for i in range(q):
  for j in range(i+1,q):
   d2=sum((x-y)**2 for x,y in zip(pts[i],pts[j]));pairs+=1
   if d2<best:best,arg=d2,(i,j)
 assert abs(best*q/4-1)<1e-10
 out.append({'n':n,'q':q,'minimum_squared_times_q_over_4':round(best*q/4,12),'minimizing_pair':arg})
print(json.dumps({'status':'PASS_DIAGNOSTIC_ONLY','precision':'binary64','pairs':pairs,'families':out,'scope':'Direct Cartesian distance comparison; no certified error bound and no role in the uniform proof.'},indent=2,sort_keys=True))
