"""Source-derived exact first-hit billiards, independent of cyclic cone labels.

Coordinates (x,y) mean (x,sqrt(D)*y); all ray intersections and reflections
are rational. Restricted to the crystallographic n=3,4,6 cases.
"""
from fractions import Fraction as F
from collections import Counter
from math import gcd
import json
C=Counter();W={}
def require(ok,name,detail=None):
 C[name]+=1
 if not ok:raise RuntimeError((name,detail))
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def scale(a,c):return(a[0]*c,a[1]*c)
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b,D):return a[0]*b[0]+D*a[1]*b[1]
def mul(a,b,D):return(a[0]*b[0]-D*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def rotate(v,n,steps):
 # Positive rotation by steps*2*pi/n.
 r={3:(F(-1,2),F(1,2)),4:(F(0),F(1)),6:(F(1,2),F(1,2))}[n]
 D=1 if n==4 else 3
 for _ in range(steps%n):v=mul(v,r,D)
 return v

def polygon(n):
 raw={3:[(0,0),(F(1,2),F(1,2)),(1,0)],4:[(0,0),(0,1),(1,1),(1,0)],6:[(0,0),(F(-1,2),F(1,2)),(0,1),(1,1),(F(3,2),F(1,2)),(1,0)]}[n]
 return [tuple(F(x) for x in v) for v in raw]

def admissible(n,v,ell=None):
 if ell is not None and n%2==0 and ell%2:return False
 if v==(0,0):return False
 P=polygon(n)
 return cross(sub(P[-1],P[0]),v)>=0 and cross(v,sub(P[1],P[0]))>=0

def trace(n,d,limit=500):
 P=polygon(n);D=1 if n==4 else 3;p=P[0];d0=d
 require(admissible(n,d),'trace_inward')
 for q in range(1,limit+1):
  hits=[]
  for j,a in enumerate(P):
   b=P[(j+1)%n];e=sub(b,a);den=cross(d,e)
   if den:
    t=cross(sub(a,p),e)/den;u=cross(sub(a,p),d)/den
    if t>0 and 0<=u<=1:hits.append((t,j,u))
   elif cross(sub(a,p),d)==0:
    # Boundary rays reach a vertex; don't discard collinear segments.
    for u,v in [(F(0),a),(F(1),b)]:
     t=dot(sub(v,p),d,D)/dot(d,d,D)
     if t>0:hits.append((t,j,u))
  require(bool(hits),'positive_next_intersection',(n,p,d,q))
  t,j,u=min(hits)
  p=add(p,scale(d,t))
  if u in (0,1):
   vertex=j if u==0 else (j+1)%n
   require(p==P[vertex],'exact_vertex')
   eout=sub(P[(vertex-1)%n],P[vertex])
   if q%2:
    num=mul(eout,d0,D);denom=mul(d,P[-1],D)
    ds=range(1,n)
   else:
    num=mul(eout,P[-1],D);denom=mul(d,d0,D)
    ds=range(-((n-4)//2),n//2+1)
   candidates=[z for z in ds if cross(num,rotate(denom,n,z))==0 and dot(num,rotate(denom,n,z),D)>0]
   require(len(candidates)==1,'source_integrality_from_geometry',(n,q,d0,d,eout,candidates))
   z=candidates[0]
   k=((n-1-z) if q%2 else (z-1))%(n-2)
   C['saddle_connections']+=1;C['segments_total']+=q;C['reflections_total']+=q-1
   C['max_segments']=max(C['max_segments'],q)
   return k,q,vertex
  e=sub(P[(j+1)%n],P[j]);oldnorm=dot(d,d,D)
  d=sub(scale(e,2*dot(d,e,D)/dot(e,e,D)),d)
  require(dot(d,d,D)==oldnorm,'reflection_preserves_metric')
 raise RuntimeError(('reflection_limit',n,d0,limit))

def run():
 records=[]
 for n in (3,4,6):
  for j in range(1,n):
   k,q,v=trace(n,polygon(n)[j]);require((k,q,v)==((j-1)%(n-2),1,j),'figure9_chords',(n,j,k,q,v))
  vectors=[]
  for p in range(-7,13):
   for q in range(0,11):
    if gcd(p,q)!=1:continue
    v=(F(p),F(q))
    if admissible(n,v):vectors.append(v)
  for v in vectors:
   k,q,j=trace(n,v)
   for epsilon in (-1,1):
    w=(v[0],epsilon*v[1])
    step=2 if n%2==0 else 1
    for ell in range(-2*n,2*n+1,step):
     if n==3:
      # ell*pi/3 equals rotation (2*pi/3)*2ell, modulo2pi.
      wp=rotate(w,n,2*ell)
     else:wp=rotate(w,n,ell//2)
     if not admissible(n,wp,ell):continue
     M=n-2
     # Exact unwrapped sector test in angular units pi/n.
     rays={3:[(1,0),(1,1)],4:[(1,0),(1,1),(0,1)],
           6:[(1,0),(3,1),(1,1),(0,1),(-1,1)]}[n]
     def ge(h):
      return True if h<=0 else False if h>M else cross(rays[h],v)>=0
     def le(h):
      return True if h>=M else False if h<0 else cross(v,rays[h])>=0
     if epsilon==1:
      allowed=ge(-ell) and le(M-ell)
     else:allowed=ge(ell-M) and le(ell)
     if not allowed:continue
     kp,qp,jp=trace(n,wp)
     require(kp==(epsilon*k-ell)%M,'signed_rule_actual_first_hits',(n,v,k,ell,epsilon,wp,kp))
     records.append([n,str(v[0]),str(v[1]),k,q,ell,epsilon,kp,qp])
     if M>1 and kp!=(-epsilon*k-ell)%M:W.setdefault('wrong_epsilon',records[-1])
     if M>1 and kp!=(epsilon*k+ell)%M:W.setdefault('wrong_ell_sign',records[-1])
     if M>1 and kp!=(epsilon*k-ell+1)%M:W.setdefault('wrong_ell_offset',records[-1])
  if n%2==0:
   require(not admissible(n,polygon(n)[-1],1),'forbidden_odd_ell_guard')
  require(not admissible(n,(F(0),F(0))),'zero_direction_guard')
 require('wrong_epsilon' in W,'epsilon_false_control_detected')
 require('wrong_ell_offset' in W,'ell_false_control_detected')
 # Wrong sign ell is indistinguishable modulo4 under even ell, and modulo2.
 # It must be tested in a higher/noncrystallographic modulus separately.
 # Terminal supplement: n=6 direct X0X2 has alpha=3pi/6,beta=5pi/6;
 # replacing beta by pi-beta gives odd sum (3+1)/2=2 and wrong k=3 vs1.
 wrong=(6-1-(3+1)//2)%4
 require(wrong!=1,'terminal_supplement_false_control',(wrong,1))
 require(trace(4,(F(1),F(1)))[0]==1,'square_both_odd')
 require(trace(4,(F(1),F(2)))[0]==0,'square_mixed_parity')
 print(json.dumps({'status':'PASS','scope':'exact rational first-hit geometry for n=3,4,6; all intersections, reflections, source classification and unwrapped sector tests exact','counts':dict(C),'false_control_witnesses':W,'pair_count':len(records),'records':records},indent=2))
if __name__=='__main__':run()
