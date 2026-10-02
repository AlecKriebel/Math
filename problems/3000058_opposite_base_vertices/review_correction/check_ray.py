from fractions import Fraction as Q
import json
b=[0,1,None,0];n=0
def add(x,y):return None if x is None or y is None else x+y
def ge(x,y):return x is None or (y is not None and x>=y)
def ck(x):
 global n;n+=1;assert x
for A in range(4):
 for B in range(4):ck(ge(add(b[A],b[B]),add(b[A|B],b[A&B])))
def feasible(t):return t<=1
ck(feasible(Q(0)));ck(feasible(Q(1)));ck(feasible(Q(-1)))
for k in range(-100,8):
 t=Q(k,8)
 if t<1:
  eps=(1-t)/2;ck(feasible(t-eps) and feasible(t+eps));ck(((t-eps)+(t+eps))/2==t);ck(t-eps!=t+eps)
# At endpoint, a convex average of parameters<=1 can equal1 only if both equal1;
# finite controls supplement the elementary inequality proof.
for a in range(-10,2):
 for c in range(-10,2):
  if Q(a+c,2)==1:ck(a==c==1)
print(json.dumps({'assertions':n,'submodular_pairs':16,'literal_ray_status':'counterexample','bounded_conjecture_status':'unresolved','scope':'Exact finite controls; unique-vertex proof is affine-ray geometry.'},indent=2))
