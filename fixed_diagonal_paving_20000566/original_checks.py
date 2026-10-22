"""Exact symbolic and exhaustive rational checks. No random/probabilistic proof claims."""
import sympy as s
import itertools, json
from pathlib import Path
a,b,c=s.symbols('a b c',real=True)
I=s.I
S=s.Matrix([[0,a,b,c],[a,0,I*c,-I*b],[b,-I*c,0,I*a],[c,I*b,-I*a,0]])
assert S==S.conjugate().T
assert s.simplify(S*S-(a*a+b*b+c*c)*s.eye(4))==s.zeros(4)
results={'symbolic_symmetry_identity':True,'samples':[]}
for aa,bb,cc in [(0,0,1),(s.Rational(1,3),s.Rational(2,3),s.Rational(2,3)),(1/s.sqrt(3),)*3]:
 P=(s.eye(4)+S.subs({a:aa,b:bb,c:cc}))/2
 assert s.simplify(P*P-P)==s.zeros(4)
 vals=[]
 for mask in range(1,8): # exactly seven unordered bipartitions, coordinate 3 always on complement
  J=[j for j in range(4) if mask>>j&1];K=[j for j in range(4) if j not in J]
  norms=[max(P.extract(L,L).eigenvals().keys()) for L in [J,K]]
  vals.append(max(norms))
 got=min(vals);expected=(1+min(aa,bb,cc))/2
 assert s.simplify(got-expected)==0
 results['samples'].append({'parameters':list(map(str,[aa,bb,cc])),'all_partition_norms':list(map(str,vals)),'optimum':str(got)})
# Symbolic coupled block realizes prescribed compression eigenvalues.
t=s.symbols('t',positive=True)
C=s.Matrix([[t,s.sqrt(t*(1-t))],[s.sqrt(t*(1-t)),1-t]])
assert s.simplify(C*C-C)==s.zeros(2)
results['coupled_block_idempotence']=True
# Exhaust diagonal vectors on a quarter grid: compare all subset vs sorted prefix universal test.
count=0
for n in range(1,7):
 for q in itertools.product([s.Rational(k,4) for k in range(5)],repeat=n):
  if sum(q).q!=1:continue
  for r in range(1,n+1):
   alltest=all(len(J)<=r*s.ceiling(sum(q[j] for j in J)) for k in range(1,n+1) for J in itertools.combinations(range(n),k))
   prefix=all(k<=r*s.ceiling(sum(sorted(q)[:k])) for k in range(1,n+1))
   assert alltest==prefix
   count+=1
results['exhaustive_prefix_equivalence_cases']=count
Path(__file__).with_name('CHECK_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
