from fractions import Fraction as F
import json
checks=0
def check(c):
 global checks
 assert c;checks+=1
def f(x):
 if x<=0:return F(0)
 if x<=F(1,3):return x/(1-x)
 if x<=F(1,2):return F(3,2)-3*x
 if x<=2:return F(4,3)*(x-F(1,2))
 if x<=F(7,3):return 2+(x-2)/(3-x)
 if x<=F(5,2):return F(19,2)-3*x
 return F(2)
check(f(0)==0);check(f(2)==2);check(f(F(1,2))==0);check(f(F(5,2))==2)
for n in range(1,501):
 a=F(1,n+2);b=2+a;check(f(a)==F(1,n+1));check(f(b)==2+F(1,n+1));check(b-a==2)
for T in range(101):
 for t in range(T+1):
  n=T+1;x=F(1,n+2);y=2+x
  for j in range(t):x=f(x);y=f(y)
  check(x==F(1,n-t+2));check(y-x==2)
# Both side formulas at each breakpoint.
check(F(1,3)/(1-F(1,3))==F(3,2)-3*F(1,3))
check(F(3,2)-3*F(1,2)==F(4,3)*(F(1,2)-F(1,2)))
check(F(4,3)*(2-F(1,2))==2)
check(2+(F(7,3)-2)/(3-F(7,3))==F(19,2)-3*F(7,3))
check(F(19,2)-3*F(5,2)==2)
print(json.dumps({'assertions':checks,'scope':'exact rational orbit, separation and continuity-junction controls; infinite argument is in the proof'},indent=2))
