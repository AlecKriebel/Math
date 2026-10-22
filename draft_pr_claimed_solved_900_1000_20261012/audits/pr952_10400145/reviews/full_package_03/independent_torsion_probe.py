"""Full03 new all-modulus boundary checks; written proof in MATH_REVIEW.md.
No topology imported and no finite sample promoted to a universal proof.
"""
import json,sys,datetime,math

def need(c,m):
 if not c:raise RuntimeError(m)
def f(n,l,m):return (l*(n*n*n-n))%m
cases=0;false_first_triple=[]
for m in range(2,121):
 for l in range(m):
  criterion=(6*l)%m==0
  # Polynomial congruence repeats mod m; this range covers every residue.
  vals=[f(n,l,m) for n in range(1,m+4)]
  affine=all((vals[i+2]-2*vals[i+1]+vals[i])%m==0 for i in range(len(vals)-2))
  need(affine==criterion,'all-modulus exact annihilator boundary')
  first=(12*l)%m==0;second=(18*l)%m==0;need((first and second)==criterion,'two adjacent triples suffice over arbitrary modulus')
  if first and not criterion:false_first_triple.append({'modulus':m,'lambda':l,'size234_residual':18*l%m})
  cases+=1
need(math.gcd(12,18)==6 and f(2,1,6)==0 and f(3,1,6)==0,'torsion positive controls')
need((12%4)==0 and (18%4)==2,'ranks123 alone loses mod4 information')
print(json.dumps({'schema':'full03-independent-torsion-boundary-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_optimization':sys.flags.optimize,'status':'PASS_EXACT_FINITE_CONTROLS','coefficient_pairs_checked':cases,'false_first_triple_count':len(false_first_triple),'examples':false_first_triple[:8],'scope':'Controls for independent proof: cubic first slopes are affine over any commutative coefficient ring precisely when6lambda=0. Actual theorem is overZ; topology remains cited input.'},sort_keys=True))
