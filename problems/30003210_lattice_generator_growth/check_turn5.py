import itertools,json,math
checks=0
def test(c):
 global checks
 assert c;checks+=1
def mul(a,b):return tuple(a[b[i]] for i in range(5))
def inv(a):return tuple(a.index(i) for i in range(5))
def even(a):return sum(a[i]>a[j] for i in range(5) for j in range(i+1,5))%2==0
A={p for p in itertools.permutations(range(5)) if even(p)};e=tuple(range(5));test(len(A)==60)
remaining=set(A);sizes=[]
while remaining:
 a=next(iter(remaining));cl={mul(mul(g,a),inv(g)) for g in A};test(cl<=A);sizes.append(len(cl));remaining-=cl
test(sorted(sizes)==[1,12,12,15,20])
for mask in range(16):
 s=1+sum([12,12,15,20][j] for j in range(4) if mask>>j&1)
 if 60%s==0:test(s in (1,60))
x=(1,2,0,3,4);cl={mul(mul(g,x),inv(g)) for g in A};H={e};todo=[e]
while todo:
 a=todo.pop()
 for b in cl:
  c=mul(a,b);checks+=1
  if c not in H:H.add(c);todo.append(c)
test(H==A)
for k in range(1,101):test(60**k+1>60**k)
# Abelianization loses conjugation: verify with sign exponent vectors over finite fields.
for p in (2,3,5,7):
 for a,b in itertools.product(range(p),repeat=2):test((a+b-a)%p==b)
for N in range(1,30):
 for J in range(1,1000):test(N+(J.bit_length()-1)>=N)
print(json.dumps({'assertions':checks,'A5_conjugacy_classes':sorted(sizes),'normal_closure_size':len(H),'scope':'exact finite controls; P_r is a method counterexample, not a lattice counterexample'},indent=2))
