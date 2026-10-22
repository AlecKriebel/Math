"""DFC drift of Allerton 2012's operative high-load Lyapunov function."""
import math,json,datetime
r=math.exp(-1); C=864*math.e

def V(a,b,x,y): return 2*(a+b)+x+y

def G(a,b,x,y):
 S=a+b+x+y+1
 return S*(r**(x+1)+r**(y+1)+r**(a+b))

def qFG(a,b,x,y):
 D=x+y+1;st=(a,b,x,y)
 transitions=[((a+1,b,x,y),.5),((a,b+1,x,y),.5)]
 if a:transitions.append(((a-1,b,x+1,y),a*(x+1)/D))
 if b:transitions.append(((a,b-1,x,y+1),b*(y+1)/D))
 if x:transitions.append(((a,b,x-1,y),x*(y+1)/D))
 if y:transitions.append(((a,b,x,y-1),y*(x+1)/D))
 return math.fsum(q*(C*(V(*t)-V(*st))+G(*t)-G(*st)) for t,q in transitions)
rows=[]
for M in [10000,100000,1000000]:
 q=qFG(1,0,M,1)
 rows.append({'M':M,'drift':q,'drift_over_M':q/M})
 assert q>0
assert abs(rows[-1]['drift_over_M']-(1-r))<.006
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lambda':1,'C':C,'states':'(1,0,M,1)','analytic_limit_drift_over_M':1-r,'rows':rows,'direct_Allerton_function_is_DFC_Foster_certificate':False},indent=2))
