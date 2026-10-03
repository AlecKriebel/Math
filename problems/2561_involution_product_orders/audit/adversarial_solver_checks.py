from pathlib import Path
"""Brute-force completeness checks for release search plus whole-class cross-checks."""
from itertools import combinations,permutations,product
from collections import Counter
import importlib.util,random,sys,json,subprocess
ROOT=str(Path(__file__).resolve().parent.parent/'checks')+'/'
spec=importlib.util.spec_from_file_location('release',ROOT+'colored_involutions.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
def brute(M):
 n=len(M)
 return sum(all(M[i][j]==M[f[i]][f[j]] for i in range(n) for j in range(i)) for tail in permutations(range(1,n)) for f in [(0,)+tail])
def test(M):
 n=len(M);C=[list(range(n)) for _ in range(n)]
 z=r.solve(M,C);b=brute(M)
 assert z['stabilizer_size']==b,(M,z,b)
 return b
checked=0
for bits in product((2,3),repeat=10):
 M=[[1 if i==j else 0 for j in range(5)] for i in range(5)]
 for (i,j),v in zip(combinations(range(5),2),bits):M[i][j]=M[j][i]=v
 test(M);checked+=1
rng=random.Random(4642561)
for n in (6,7):
 for _ in range(40):
  M=[[1 if i==j else 0 for j in range(n)] for i in range(n)]
  for i,j in combinations(range(n),2):M[i][j]=M[j][i]=rng.choice((2,2,3))
  test(M);checked+=1
 M=[[1 if i==j else 2 for j in range(n)] for i in range(n)];test(M);checked+=1
print('Full stabilizer matches brute force:',checked,'graphs',flush=True)

# Enumerate entire S_n independently and select desired even involutions.
classes={}
for n,k in [(5,2),(6,2),(7,2),(8,4)]:
 whole={p for p in permutations(range(n)) if sum(p[i]!=i for i in range(n))==2*k and all(p[p[i]]==i for i in range(n))}
 generated=set(r.alternating_class(n,k));assert generated==whole
 classes[f'A{n}_{k}']=len(whole)
print('Full permutation class enumerations:',classes,flush=True)

# Exhaust every determinant-one 2x2 matrix, then select projective involutions
# from its action. This does not impose trace zero in the enumeration.
prime={}
for p in (7,11):
 actions=set()
 for a,b,c,d in product(range(p),repeat=4):
  if (a*d-b*c)%p!=1:continue
  def action(x):
   if x==p:return (a*pow(c,-1,p))%p if c else p
   den=(c*x+d)%p
   return ((a*x+b)*pow(den,-1,p))%p if den else p
  actions.add(tuple(action(x) for x in range(p+1)))
 identity=tuple(range(p+1));inv={g for g in actions if g!=identity and all(g[g[i]]==i for i in range(p+1))}
 assert inv==set(r.psl2_prime_class(p))
 assert len(actions)==p*(p*p-1)//2
 prime[p]={'whole_group':len(actions),'all_involutions':len(inv)}
print('Full PSL2(p) enumerations:',prime,flush=True)

# Deterministic negative: swap two A5 vertices fixing the same letter.
D=r.alternating_class(5,2);M,C=r.tables(D)
block=[i for i,d in enumerate(D) if d[4]==4];f=list(range(15));f[block[0]],f[block[1]]=f[block[1]],f[block[0]]
assert all((M[i][j]==2)==(M[f[i]][f[j]]==2) for i in range(15) for j in range(15))
assert any(M[i][j]!=M[f[i]][f[j]] for i in range(15) for j in range(15))
assert any(f[C[i][j]]!=C[f[i]][f[j]] for i in range(15) for j in range(15))
try:r.solve(M,C,max_nodes=0)
except TimeoutError:pass
else:raise AssertionError('node limit did not fail closed')
x=subprocess.run([sys.executable,'-O',ROOT+'run_all.py'],capture_output=True,text=True)
assert x.returncode and 'do not run Python with -O' in x.stderr
out={'bruteforce_graphs':checked,'all_counts_match':True,'classes':classes,'prime_groups':prime,'explicit_negative_control':True,'node_limit_fails_closed':True,'optimized_runner_refused':True}
json.dump(out,open(Path(__file__).resolve().parent/'adversarial_solver_results.json','w'),indent=2)
print(out)
