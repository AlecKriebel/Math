"""Independent unequal-node first-jet determinant checks, no topology assertions."""
import itertools,json,sys
def need(x,m):
 if not x:raise RuntimeError(m)
def weighted(a,b,c,va,vb,vc):return (b-a)*vc-(c-a)*vb+(c-b)*va
triples=list(itertools.combinations(range(1,17),3));basis=0;cubic=0
for a,b,c in triples:
 # q^r t^s evaluates to 1+(r+sn)x, including negative Laurent r.
 for r in range(-6,7):
  for s in range(13):
   need(weighted(a,b,c,r+s*a,r+s*b,r+s*c)==0,'unequal-node affine determinant');basis+=1
 for lam in [-7,-1,0,1,9]:
  f=lambda n:lam*n*(n*n-1)
  residual=weighted(a,b,c,f(a),f(b),f(c));expected=lam*(b-a)*(c-a)*(c-b)*(a+b+c)
  need(residual==expected,'cubic Vandermonde factorization')
  need((residual==0)==(lam==0),'positive distinct sizes must obstruct nonzero lambda');cubic+=1
# Nilpotent first coefficient: no divisions are used. The same identity holds
# over torsion rings, but integer nonzero can disappear after quotienting.
torsion=[]
for m in [2,3,4,5,6,7,11,12,13,25]:
 residue=weighted(1,2,3,0,-6,-24)%m;torsion.append({'modulus':m,'residual':residue})
need(weighted(1,2,3,0,-6,-12)==0,'affine realizable control');need(weighted(2,3,4,-6,-24,-60)==-18,'omitted assigned size one')
print(json.dumps({'status':'PASS_UNEQUAL_NODE_FINITE_CONTROLS','outer_optimization':sys.flags.optimize,'basis_cases':basis,'cubic_cases':cubic,'triple_count':len(triples),'torsion':torsion,'first_obstruction':-12,'scope':'Exact algebra controls accompanying the general unequal-node proof in FULL_AUDIT; no topology/priority/formal certification.'},sort_keys=True))
