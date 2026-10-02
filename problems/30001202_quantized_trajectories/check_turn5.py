from fractions import Fraction as F
import itertools,json
checks=0;systems=0
def check(c):
 global checks
 assert c;checks+=1
# Solve bounded one-dimensional weak/strict systems exactly, including zero rows.
def interval(rows):
 lo,hi=F(-2),F(2);lop=hip=False
 for a,b,strict in rows:
  if not a:
   if not(0<b if strict else 0<=b):return None
  elif a>0:
   q=b/a
   if q<hi:hi=q;hip=strict
   elif q==hi:hip|=strict
  else:
   q=b/a
   if q>lo:lo=q;lop=strict
   elif q==lo:lop|=strict
 if lo>hi or lo==hi and(lop or hip):return None
 return lo,hi,lop,hip
def holds(x,rows):return all(a*x<b if s else a*x<=b for a,b,s in rows)
cells=[[(F(-1),F(2),False),(F(1),F(0),True)],[(F(-1),F(0),False),(F(1),F(2),False)]]
for a in (F(-2),F(-1),F(-1,2),F(0),F(1,2),F(1),F(2)):
 for b in (F(-1,2),F(0),F(1,2)):
  for T in range(4):
   for word in itertools.product(range(2),repeat=T+1):
    B=F(1);c=F(0);rows=[];iterates=[]
    for j in range(T+1):
     iterates.append((B,c));rows += [(r*B,s-r*c,k) for r,s,k in cells[word[j]]];B,c=a*B,a*c+b
    J=interval(rows);systems+=1
    candidates=[F(k,8) for k in range(-16,17)]
    if J:
     lo,hi,lop,hip=J;candidates += [lo,hi,(lo+hi)/2]
    for x in candidates:
     y=x;direct=True
     for j in range(T+1):direct &= holds(y,cells[word[j]]);y=a*y+b
     check(direct==holds(x,rows))
    if J:
     lo,hi,lop,hip=J;z=(lo+hi)/2
     if lo==hi:z=lo
     check(holds(z,rows))
     for r in (F(1),F(1,2),F(1,10)):
      for endpoint in (lo,hi):check(holds((1-r)*endpoint+r*z,rows))
     for B,c in iterates:check((B*(hi-lo))**2>=0)
# Vertex-pair diameter controls for affine images of a rational square.
V=list(itertools.product((F(-1),F(1)),repeat=2))
for entries in itertools.product((-1,0,1),repeat=4):
 def image(x):return(entries[0]*x[0]+entries[1]*x[1],entries[2]*x[0]+entries[3]*x[1])
 def dist(x,y):return sum((a-b)**2 for a,b in zip(image(x),image(y)))
 D=max(dist(v,w) for v in V for w in V)
 for v,w in itertools.product(V,repeat=2):
  for r in (F(0),F(1,3),F(1)):
   x=tuple((1-r)*v[i]+r*w[i] for i in range(2))
   for z in V:check(dist(x,z)<=D)
print(json.dumps({'assertions':checks,'affine_interval_systems':systems,'scope':'exact strict-boundary, singular-map and convex-image diameter controls; general finite algorithm is proved in text'},indent=2))
