# Self-authored exploratory filter, not a proof of global positivity.
from fractions import Fraction as F
import json
out=[]
points=[]
for j in range(31):
 t=F(j,10);points.append((t*t,2*t**3))
 if t<=1:points.append((t*t,-2*t**3))
for j in range(1,91):
 x=F(j,10)
 if x>=1:points.append((x,(x*x+18*x-27)/4))
for a in range(-8,9):
 for b in range(-10,11):
  for c in range(-27,28):
   A=1-a+2*b;B=a-4*b;C=c;D=b-c
   if all(A+B*x+C*x*x+D*y>=0 for x,y in points):
    out.append({'a':a,'b':b,'c':c,'dimension':1+8*a+20*b+27*c,'polynomial':[A,B,C,D]})
print(json.dumps({'scope':'Finite rational boundary sample filter only; not a positivity proof.','candidates':out},indent=2))
