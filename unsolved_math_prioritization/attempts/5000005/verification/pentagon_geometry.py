"""Actual regular-pentagon reflections over Q(sqrt(5)), with exact ordering.

No cone labels or candidate helper identities determine the traced type.
"""
from fractions import Fraction as F
from functools import total_ordering
from collections import Counter
import json
C=Counter();W={}
@total_ordering
class K:
 def __init__(self,a=0,b=0):
  if isinstance(a,K):self.a,self.b=a.a,a.b
  else:self.a,self.b=F(a),F(b)
 def __add__(self,v):
  v=K(v);return K(self.a+v.a,self.b+v.b)
 __radd__=__add__
 def __neg__(self):return K(-self.a,-self.b)
 def __sub__(self,v):return self+-K(v)
 def __rsub__(self,v):return K(v)+-self
 def __mul__(self,v):
  v=K(v);return K(self.a*v.a+5*self.b*v.b,self.a*v.b+self.b*v.a)
 __rmul__=__mul__
 def __truediv__(self,v):
  v=K(v);norm=v.a*v.a-5*v.b*v.b
  if not norm:raise ZeroDivisionError
  return self*K(v.a/norm,-v.b/norm)
 def __rtruediv__(self,v):return K(v)/self
 def sign(self):
  a,b=self.a,self.b
  if not a:return (b>0)-(b<0)
  if not b:return (a>0)-(a<0)
  if a*b>0:return (a>0)-(a<0)
  d=a*a-5*b*b
  return ((d>0)-(d<0))*(1 if a>0 else -1)
 def __eq__(self,v):
  try:v=K(v)
  except (TypeError,ValueError):return False
  return self.a==v.a and self.b==v.b
 def __lt__(self,v):return (self-K(v)).sign()<0
 def __bool__(self):return bool(self.a or self.b)
 def __str__(self):return f'{self.a}+({self.b})sqrt5'
def require(ok,name,detail=None):
 C[name]+=1
 if not ok:raise RuntimeError((name,detail))
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def scale(a,c):return(a[0]*c,a[1]*c)
def dot(a,b):return a[0]*b[0]+D*a[1]*b[1]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def mul(a,b):return(a[0]*b[0]-D*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
Z=K();one=K(1);c=K(F(-1,4),F(1,4));u=K(F(-1,4),F(-1,4))
D=K(F(5,8),F(1,8))
raw=[(one,Z),(c,-one),(u,-2*c),(u,2*c),(c,one)]
P=[sub(v,raw[0]) for v in raw];e0=P[-1];e1=P[1]
def rotate(v,steps):
 for _ in range(steps%5):v=mul(v,(c,one))
 return v
def rotate_small(v,steps):
 r36=(K(F(1,4),F(1,4)),K(F(-1,2),F(1,2)))
 for _ in range(steps%10):v=mul(v,r36)
 return v
def inward(v):return v!=(Z,Z) and cross(e0,v)>=0 and cross(v,e1)>=0
def reflection(v,e):return sub(scale(e,2*dot(v,e)/dot(e,e)),v)
def trace(d,limit=600):
 require(inward(d),'trace_inward');p=P[0];d0=d
 for q in range(1,limit+1):
  hits=[]
  for j,a in enumerate(P):
   b=P[(j+1)%5];e=sub(b,a);den=cross(d,e)
   if den:
    t=cross(sub(a,p),e)/den;u=cross(sub(a,p),d)/den
    if t>0 and 0<=u<=1:hits.append((t,j,u))
   elif cross(sub(a,p),d)==0:
    for u,v in [(Z,a),(one,b)]:
     t=dot(sub(v,p),d)/dot(d,d)
     if t>0:hits.append((t,j,u))
  require(bool(hits),'positive_next_intersection')
  t,j,u=min(hits);p=add(p,scale(d,t))
  if u==0 or u==1:
   v=j if u==0 else (j+1)%5
   require(p==P[v],'exact_vertex');eout=sub(P[(v-1)%5],P[v])
   num=mul(eout,d0 if q%2 else e0);denom=mul(d,e0 if q%2 else d0)
   ds=range(1,5) if q%2 else range(0,3)
   found=[z for z in ds if cross(num,rotate(denom,z))==0 and dot(num,rotate(denom,z))>0]
   require(len(found)==1,'source_integrality_from_geometry',(q,[str(x) for x in d0],found))
   z=found[0];k=((4-z) if q%2 else (z-1))%3
   C['saddle_connections']+=1;C['segments_total']+=q;C['max_segments']=max(C['max_segments'],q)
   return k,q,v
  e=sub(P[(j+1)%5],P[j]);old=dot(d,d);d=reflection(d,e)
  require(dot(d,d)==old,'reflection_preserves_metric')
 raise RuntimeError(('trace_limit',[str(x) for x in d0],limit))
def unwrapped(v,ell,eps):
 def ray(h):return rotate_small(e0,h)
 def ge(h):return True if h<=0 else False if h>3 else cross(ray(h),v)>=0
 def le(h):return True if h>=3 else False if h<0 else cross(v,ray(h))>=0
 return ge(-ell) and le(3-ell) if eps==1 else ge(ell-3) and le(ell)
def run():
 for j in range(1,5):require(trace(P[j])==((j-1)%3,1,j),'figure9_chords')
 records=[]
 # Seeds are sheared model chords. The actual tracer, not the shear premise,
 # determines whether each chosen direction really terminates.
 for span in (1,2,3,4):
  for power in (-1,0,1):
   v=add(P[span],scale(e0,K(F(3,2),F(1,2))*power*cross(e0,P[span])/dot(e0,e0)))
   for turn in range(5):
    base=rotate(v,turn)
    if not inward(base):continue
    k,q,j=trace(base)
    for eps in (-1,1):
     w=base if eps==1 else reflection(base,e0)
     for ell in range(-3,7):
      if not unwrapped(base,ell,eps):continue
      wp=rotate_small(w,ell)
      kp,qp,jp=trace(wp)
      require(kp==(eps*k-ell)%3,'signed_rule_actual_first_hits')
      row={'span':span,'shear_power':power,'turn':turn,'base_direction':[str(x) for x in base],'base_type':k,'base_segments':q,'ell':ell,'epsilon':eps,'new_type':kp,'new_segments':qp}
      records.append(row)
      for name,pred in [('wrong_epsilon',-eps*k-ell),('wrong_ell_sign',eps*k+ell),('wrong_ell_offset',eps*k-ell+1)]:
       if kp!=pred%3:W.setdefault(name,row)
 for name in ('wrong_epsilon','wrong_ell_sign','wrong_ell_offset'):require(name in W,name+'_detected')
 require(not inward((Z,Z)),'zero_direction_guard')
 # Literal mod-angle substitution would wrongly admit ell=10 (full 2pi).
 require(inward(rotate(P[2],5)) and not unwrapped(P[2],10,1),'literal_unwrapped_guard')
 print(json.dumps({'status':'PASS','scope':'n=5 actual first-hit geometry over Q(sqrt5), exact signs and unwrapped sector','counts':dict(C),'pair_count':len(records),'false_control_witnesses':W,'records':records},indent=2))
if __name__=='__main__':run()
