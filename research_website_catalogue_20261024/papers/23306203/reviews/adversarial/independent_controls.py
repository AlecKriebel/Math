#!/usr/bin/env python3
"""Independent exact fraction divisor multisets and biquadratic geometry; no native imports."""
from fractions import Fraction as F
from collections import Counter
from math import gcd
import json
checks=0
def need(v,m):
 global checks
 checks+=1
 if not v:raise RuntimeError(m)
def mod1(x):return x%1

def divisor(N,tau):
 step=F(tau,N);roots=[-F(1,4)-step/2,-F(1,4)+step/2];poles=[F(0),F(1,2)];d=Counter()
 need(mod1(roots[0])!=mod1(roots[1]),'singlefactorzerosdistinct')
 need(all(mod1(q)!=p for q in roots for p in poles),'singlefactornonpolarzeros')
 for j in range(N):
  for q in roots:d[mod1(q-j*step)]+=1
  for p in poles:d[mod1(p-j*step)]-=1
 return {x:v for x,v in d.items()if v}
class B:
 # Q(a,c), a²=15,c²=8. Basis1,a,c,ac.
 def __init__(self,*v):
  if len(v)==1 and isinstance(v[0],B):self.v=v[0].v
  else:self.v=tuple(F(x)for x in(v+(0,)*(4-len(v))))
 def __add__(self,o):o=B(o);return B(*[x+y for x,y in zip(self.v,o.v)])
 __radd__=__add__
 def __neg__(self):return B(*[-x for x in self.v])
 def __sub__(self,o):return self+-B(o)
 def __rsub__(self,o):return B(o)+-self
 def __mul__(self,o):
  o=B(o);v=[F(0)]*4
  for i,x in enumerate(self.v):
   for j,y in enumerate(o.v):v[i^j]+=x*y*(15 if i&j&1 else 1)*(8 if i&j&2 else 1)
  return B(*v)
 __rmul__=__mul__
 def __truediv__(self,o):return self*F(1,o)
 def __pow__(self,n):
  out=B(1)
  for _ in range(n):out=out*self
  return out
 def __eq__(self,o):return self.v==B(o).v
 def pack(self):return [str(v)for v in self.v]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def polyadd(a,b):
 c=a.copy()
 for k,v in b.items():c[k]=c.get(k,F(0))+v
 return {k:v for k,v in c.items()if v}
def polytimes(a,b):
 c={}
 for(i,j),x in a.items():
  for(k,l),y in b.items():c[i+k,j+l]=c.get((i+k,j+l),F(0))+x*y
 return {k:v for k,v in c.items()if v}
def scale(a,c):return {k:v*c for k,v in a.items()if v*c}
def run():
 out={'mechanism':'Signed divisor counters in Q/Z built per individual factor; direct exact Q(sqrt15,sqrt8) coordinate/normal/distance geometry; no native formulas imported','divisor_cases':[],'nonprimitive_return_length_counterexamples':[],'normal_frame_identity_parameter_cases':[]}
 for N in range(3,36):
  for tau in range(1,(N+1)//2):
   if 2*tau>=N:continue
   g=gcd(N,tau);n=N//g;d=divisor(N,tau);good=not d
   need(good==(n%4==2),'leastperiodcriterion')
   need(len({mod1(j*F(tau,N))for j in range(n)})==n,'distinctleastperiodvertices')
   if d:
    poles={x:-v for x,v in d.items()if v<0};zeros={x:v for x,v in d.items()if v>0}
    need(sum(poles.values())==sum(zeros.values())==2*N,'wholedivisordegree')
    need(len(poles)==(2*n if n%2 else n),'exactpolelocationcount')
    need(set(poles.values())=={g if n%2 else 2*g},'multiplicitynotjustsupport')
   primitive=(g==1)
   # Reversal has identical real cyclic orbit; zeros are exchanged.
   need(divisor(N,-tau)==d,'bothorientationdivisors')
   row={'returnN':N,'tau':tau,'leastperiod':n,'traversals':g,'primitive':primitive,'constant':good,'retainedpolelocations':sum(v<0 for v in d.values())}
   out['divisor_cases'].append(row)
   if N%4==2 and n%2 and len(out['nonprimitive_return_length_counterexamples'])<8:out['nonprimitive_return_length_counterexamples'].append(row)
 need(any(x['returnN']==6 and x['tau']==2 and not x['constant']for x in out['divisor_cases']),'sixreturnthreeleastperiodcontrol')
 # Algebraic identity of normal/tangent frame, tested by explicit polynomial
 # expansion, not by substituting the already factored manuscript expression.
 X={(1,0):F(1)};Y={(0,1):F(1)};one={(0,0):F(1)};X2=polytimes(X,X);Y2=polytimes(Y,Y);XY=polytimes(X,Y)
 for a2,b2,A2,B2 in [(F(15),F(7),F(135,16),F(7,16)),(F(25),F(16),F(13),F(4)),(F(9),F(8),F(5),F(4))]:
  c2=a2-b2;need(A2-B2==c2,'confocalinput')
  M=[[polyadd(scale(one,B2),scale(Y2,-1)),XY],[XY,polyadd(scale(one,A2),scale(X2,-1))]]
  nu=[scale(X,1/a2),scale(Y,1/b2)];t=[scale(Y,-1/b2),scale(X,1/a2)];lhs={}
  for i in range(2):
   for j in range(2):lhs=polyadd(lhs,polytimes(polytimes(nu[i],M[i][j]),t[j]))
  rhs=scale(polytimes(XY,polyadd(one,polyadd(scale(X2,-1/a2),scale(Y2,-1/b2)))),c2/(a2*b2))
  need(lhs==rhs,'expandednormalframeidentity')
  out['normal_frame_identity_parameter_cases'].append([str(x)for x in[a2,b2,A2,B2]])
 a=B(0,1);c=B(0,0,1);inv_a=a/15
 vertices=[(a,B(0)),(-3*a/4,B(F(7,4))),(-3*a/4,B(-F(7,4)))];contacts=[(9*a/16,B(F(7,16))),(-3*a/4,B(0)),(9*a/16,B(-F(7,16)))]
 a2=F(15);b2=F(7);A2=F(135,16);B2=F(7,16)
 need(a2-b2==A2-B2==8 and a2>A2 and b2>B2>0,'strictnondegenerateconfocalpair')
 lengths=[F(7),F(7,2),F(7)]
 for i,(x,y)in enumerate(vertices):
  need(x*x/a2+y*y/b2==1,'vertexonouterellipse')
  j=(i+1)%3;vec=[vertices[j][k]-vertices[i][k]for k in range(2)];need(dot(vec,vec)==lengths[i]**2,'exactedgelength')
  contact=contacts[i];need(contact[0]*contact[0]/A2+contact[1]*contact[1]/B2==1,'contactoncaustic')
  # Contact weights along each actual segment:1/4,1/2,3/4.
  lam=[F(1,4),F(1,2),F(3,4)][i]
  need(all(contact[k]==vertices[i][k]+lam*vec[k]for k in range(2)),'contactstrictlyinsidesegment')
  if i==1:need(contact[0]==-3*a/4,'verticaltangent')
  else:need(contact[0]+(a*contact[1]if i==0 else -a*contact[1])==a,'slantedtangentequation')
 for i,(x,y)in enumerate(vertices):
  prev=(i-1)%3;nxt=(i+1)%3
  ray0=[(vertices[prev][j]-vertices[i][j])/lengths[prev]for j in range(2)];ray1=[(vertices[nxt][j]-vertices[i][j])/lengths[i]for j in range(2)]
  need(dot(ray0,ray0)==dot(ray1,ray1)==1,'bothunitrays')
  nu=[-x/a2,-y/b2];nu2=dot(nu,nu);need(all(v==0 for v in nu2.v[1:])and nu2.v[0]>0,'nonzeronormalnorm')
  reflected=[nu[j]*(2*dot(nu,ray0)/nu2.v[0])-ray0[j]for j in range(2)]
  need(reflected==ray1,'exactelasticreflectionallthreevertices')
 need(len(set(tuple(v.v for v in point)for point in vertices))==3,'threeverticesdistinctleast3')
 plus=B(1);minus=B(1)
 for x,y in vertices:
  gp=a-c*x*inv_a;gm=a+c*x*inv_a
  need((x-c)**2+y*y==gp**2 and(x+c)**2+y*y==gm**2,'ordinaryfocaldistancesquaredidentity')
  plus*=gp;minus*=gm
 need(plus==15*a/2+3*c and minus==15*a/2-3*c,'exactprimitiveproducts')
 need(plus**2-minus**2==90*a*c,'doubledreturnproductdifference')
 need((a*c)**2==120,'sqrt120equals2sqrt30')
 out['triangle']={'basis':['1','sqrt15','sqrt8','sqrt120'],'primitiveplus':plus.pack(),'reflectedprimitiveplus':minus.pack(),'sixreturnproductdifference':(plus**2-minus**2).pack(),'difference_exact':'90sqrt120=180sqrt30>0','allthree_reflections_and_segment_contacts_exact':True}
 out['boundary_controls']=['N=6,tau=2 has leastperiod3 and is nonconstant despite N=2mod4','n=1/2 absent because0<tau<n/2 and gcd1','c=0 removes sn poles: circular products are a^N, not classified by noncircular divisor','positive-real rthpower is injective, so repetition cannot repair a nonconstant primitive product']
 out['checks']=checks;out['status']='PASS_BOUNDED_EXACT_INDEPENDENT_CONTROLS';out['limits']='Bounded inventory/geometry support only; complete allperiod analytic/geometric proof reconstructed in INITIAL_RECONSTRUCTION.md.'
 return out
if __name__=='__main__':print(json.dumps(run(),indent=2))
