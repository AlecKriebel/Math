import itertools,json,math,time
from pathlib import Path

def reps(A,p):
 c=[0]*p
 for i,a in enumerate(A):
  for b in A[i:]:c[(a+b)%p]+=1
 return c

def solve(p):
 counts=[]
 for n in range(2,p+1):
  # Cauchy-Davenport plus every present sum has >=2 multiset representations.
  if min(p,2*n-1)>n*(n+1)//4:
   counts.append({'n':n,'excluded':'pair_capacity_cauchy_davenport'});continue
  count=0
  for tail in itertools.combinations(range(2,p),n-2):
   count+=1; A=(0,1)+tail;c=reps(A,p)
   if 1 not in c:
    return {'p':p,'m':n,'witness':A,'unordered_counts':c,'smaller_sizes':counts,'candidates_at_witness':count}
  counts.append({'n':n,'normalized_candidates':count,'expected':math.comb(p-2,n-2)})

if __name__=='__main__':
 out=[]
 for p in [3,5,7,11,13,17,19,23,29,31]:
  t=time.time();r=solve(p);r['seconds']=time.time()-t;out.append(r);print(r,flush=True)
  Path(__file__).with_name('exact_results.json').write_text(json.dumps(out,indent=2)+'\n')
