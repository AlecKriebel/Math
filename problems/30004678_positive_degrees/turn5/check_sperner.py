import itertools,json,math
from fractions import Fraction
checks=0
def ck(x):
 global checks
 checks+=1;assert x
counts=[]
for k in range(1,5):
 N=1<<k;bad=[(a,b) for a in range(N) for b in range(a+1,N) if a&b==a];ct=0;mx=0
 for mask in range(1<<N):
  if any(mask>>a&1 and mask>>b&1 for a,b in bad):continue
  xs=[a for a in range(N) if mask>>a&1];ct+=1;mx=max(mx,len(xs))
  ck(len(xs)<=math.comb(k,k//2));ck(sum((Fraction(1,math.comb(k,a.bit_count())) for a in xs),Fraction())<=1)
 counts.append({'k':k,'antichains':ct,'maximum':mx})
mono=[f for f in itertools.product(range(2),repeat=8) if all(f[a]<=f[b] for a in range(8) for b in range(8) if a&b==a)]
maxsolutions=0
for fs in itertools.product(mono,repeat=3):
 sol=[a for a in range(8) if all(fs[i][a]==1-(a>>i&1) for i in range(3))]
 ck(len(sol)<=3);ck(all(a==b or a&b!=a for a in sol for b in sol));maxsolutions=max(maxsolutions,len(sol))
ck(maxsolutions==3)
for fs in itertools.product(mono,repeat=2):
 total=0
 for outside in range(2):
  sol=[a for a in range(4) if all(fs[i][a|(outside<<2)]==1-(a>>i&1) for i in range(2))]
  ck(len(sol)<=2);total+=len(sol)
 ck(Fraction(total,8)<=Fraction(1,2))
prev=Fraction(1)
for m in range(1,501):
 b=Fraction(math.comb(2*m,m),1<<(2*m));ck(b*b<=Fraction(1,m+1));ck(b==prev*Fraction(2*m-1,2*m));ck(b<prev);prev=b
print(json.dumps({'assertions':checks,'antichain_counts':counts,'monotone_three_bit_functions':len(mono),'vector_maps':len(mono)**3,'max_reversed_solutions':maxsolutions,'outside_bit_maps':len(mono)**2,'central_bounds_checked':500},indent=2))
