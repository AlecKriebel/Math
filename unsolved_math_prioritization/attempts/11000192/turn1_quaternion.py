from fractions import Fraction as F
from functools import reduce
one=(F(1),F(0),F(0),F(0));i=(F(0),F(1),F(0),F(0));j=(F(0),F(0),F(1),F(0));k=(F(0),F(0),F(0),F(1))
def mul(a,b):
 w,x,y,z=a;v,p,q,r=b
 return(w*v-x*p-y*q-z*r,w*p+x*v+y*r-z*q,w*q-x*r+y*v+z*p,w*r+x*q-y*p+z*v)
def prod(*a):return reduce(mul,a,one)
def inv(a):return(a[0],-a[1],-a[2],-a[3])
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def conjug(a,b):return prod(a,b,inv(a))
def invariant(t):
 a,b,c,d,x,y,z,w=t;delta=sub(b,c);v=mul(d,delta);u=conjug(inv(x),mul(a,delta))
 assert v[0]==u[0]==0
 return dot(v,u)**2/(dot(v,v)*dot(u,u))
def relation(t):
 a,b,c,d,x,y,z,w=t
 return mul(a,y)==mul(x,a) and mul(b,x)==mul(y,c) and mul(c,z)==mul(w,b) and mul(d,w)==mul(z,d)
def gen(t,name,sign=1):
 a,b,c,d,x,y,z,w=t
 if name=='A':a=prod(a,y if sign==1 else inv(y))
 if name=='E':d=prod(z if sign==1 else inv(z),d)
 if name=='C':b=prod(b,prod(x,z) if sign==1 else inv(prod(x,z)));c=prod(c,prod(z,x) if sign==1 else inv(prod(z,x)))
 if name=='B':x=prod(x,prod(inv(c),inv(a)) if sign==1 else prod(a,c));y=prod(y,prod(inv(a),inv(c)) if sign==1 else prod(c,a))
 if name=='D':z=prod(z,prod(inv(b),inv(d)) if sign==1 else prod(d,b));w=prod(w,prod(inv(d),inv(b)) if sign==1 else prod(b,d))
 out=(a,b,c,d,x,y,z,w);assert relation(out),(name,sign)
 return out
def word(t,s):
 for name in s:t=gen(t,name.upper(),1 if name.isupper() else -1)
 return t
if __name__=='__main__':
 for a,b in [(F(1),F(0)),(F(0),F(1)),(F(3,5),F(4,5)),(F(5,13),F(12,13))]:
  t=((a,b,F(0),F(0)),k,inv(k),one,i,i,j,j);assert relation(t)
  print('witness',a,b,'F',invariant(t))
  for w in ['C','D','eedcBCDEE','EE DC B cd ee'.replace(' ',''),'CDeedcBCDEE']:
   try:print(w,invariant(word(t,w)))
   except ZeroDivisionError:print(w,'undefined')
