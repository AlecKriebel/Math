#!/usr/bin/env python3
"""Independent read-only iterate-trace/Mobius and scope-boundary validation.
No target imports, writes, network, source builders or numerical prime-law claims.
"""
from pathlib import Path
from fractions import Fraction as F
from math import gcd,isqrt
from collections import Counter
import hashlib,json
HERE=Path(__file__).resolve().parent
LANE=HERE.parent
PAPER=HERE.parents[2]
SOURCE=PAPER/'sources'
checks=0

def require(test,why):
 global checks
 checks+=1
 if not test:raise RuntimeError(why)
def prime(n):return n>=2 and all(n%d for d in range(2,isqrt(n)+1))
def divisors(n):return [d for d in range(1,n+1) if n%d==0]
def mobius(n):
 sign=1;d=2
 while d*d<=n:
  if n%d==0:
   n//=d;sign=-sign
   if n%d==0:return 0
  d+=1
 return sign if n==1 else -sign
def phi(n):return sum(gcd(j,n)==1 for j in range(n))
def h(t):return max(F(0),min(F(1),2*t-1))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

require(sha(SOURCE/'SOURCE_READY.json')=='1e18c3ce5d1b7556f97ee9c90f4d8ed21fa6a4d19e54cee8b730210a15795eaa','source ready identity')
r=json.loads((SOURCE/'SOURCE_READY.json').read_text())
require(r['record_id']==23539734 and r['version']=='1.1' and r['publication_date']=='2026-10-21','exact version/date')
for row in [r['selected_actual_PDF'],r['all_TeX_candidates'][0]]:
 p=Path(row.get('path',row.get('extracted_path')))
 require(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'target artifact identity')
require(sha(LANE/'INITIAL_SEAL.json')=='a29453a18dbce66945bfc337334a7c0356305928c4e9f2a2d77f7a3c80987a0d','predecessor sealed initial identity')

# Verify actual retained prior native execution receipts, not just PASS labels.
base=SOURCE/'published-source/birational-cycle-verification'
for name in ['check_math','check_all_odd_primes']:
 receipt=next(a for a in json.loads((LANE/'SUPPLIED_EXECUTION_RECEIPTS.json').read_text()) if Path(a['command'][-1]).stem==name)
 require(sha(Path(receipt['command'][-1]))==receipt['source_sha256'],'prior executed source identity')
 output=Path(receipt['stdout']);require(sha(output)==receipt['stdout_sha256'],'prior native stdout identity')
 expected=base/('expected_checks.json' if name=='check_math' else 'expected_all_odd_checks.json')
 require(json.loads(output.read_text())==json.loads(expected.read_text()),'entire prior expected object')
 require(receipt['returncode']==0 and Path(receipt['stderr']).read_bytes()==b'','prior native process success')

rows=[];negative=[]
for p in [n for n in range(3,102,2) if prime(n)]:
 N=p-1;ds=divisors(N);aa=[(u*u+1)%p for u in range(p)];root=aa.count(0);R=p*(p-root)
 require(root==(2 if p%4==1 else 0),'root residue class')
 # Direct iterate traces count actual fixed points, without computing an
 # order for any multiplier and without following individual cycles.
 fixed={d:sum((pow(a,d,p)*v)%p==v for a in aa if a for v in range(p)) for d in ds}
 exact={d:sum(mobius(d//e)*fixed[e] for e in divisors(d)) for d in ds}
 require(sum(exact.values())==R,'Mobius trace total point mass')
 for d in ds:
  require(exact[d]>=0 and exact[d]%d==0,'exact cycle points divisible by period')
  require(sum(exact[e] for e in divisors(d))==fixed[d],'iterate trace reconstruction')
 P=sum(all(pow(a,d,p)!=1 for d in ds if d<N) for a in aa if a)
 require(exact[N]==(p-1)*P,'maximal-period mass from iterate trace')
 theta=F(phi(N),N);omega=sum(prime(q) and N%q==0 for q in range(2,N+1));W=2**omega
 require((F(P)-F(p-root)*theta)**2<=theta**2*(W-1)**2*p,'primitive character bound with exact principal count')
 require(W**4<=64**4*N,'global squarefree-divisor constant control')
 moment=sum(F(count,R)*h(F(d,p)) for d,count in exact.items())
 require(moment==(1-F(2,p))*F((p-1)*P,R),'bounded ramp from iterate traces')
 for x in [F(1,2),F(3,4),F(99,100),F(N,p),F(1)]:
  cdf=F(sum(count for d,count in exact.items() if F(d,p)<=x),R)
  if x<1 and p*(1-x)>1:
   require(cdf==1-F((p-1)*P,R),'exact fixed-x CDF under strict threshold')
  if x>=F(N,p):require(cdf==1,'maximal normalized period included at threshold')
 # Every possible retained population size, with heterogeneous finite
 # assigned normalized periods, including values far beyond support[0,1].
 extras=([F(0),F(1,p),F(p*p),F(2)]*(root*p//4+1))[:root*p]
 for e in range(root*p+1):
  epsilon=F(e,R+e)
  require(epsilon<=F(root,p),'universal exceptional mass bound')
  completed=(R*moment+sum(h(t) for t in extras[:e]))/(R+e)
  require(abs(completed-moment)<=epsilon,'heterogeneous ramp contamination bound')
  # Sharp general [0,1] statistic bound from extreme endpoint values.
  for reg in [F(0),F(1,3),F(1)]:
   for exceptional in [F(0),F(1)]:
    require(abs((1-epsilon)*reg+epsilon*exceptional-reg)<=epsilon,'all bounded-positive statistic mixture bound')
  for x in [F(1,2),F(3,4),F(1),F(10*p)]:
   count=sum(count for d,count in exact.items() if F(d,p)<=x)
   reg=F(count,R);complete=F(count+sum(t<=x for t in extras[:e]),R+e)
   require(abs(complete-reg)<=epsilon,'all retained sizes CDF contamination')
 rows.append({'p':p,'root_fibers':root,'regular_points':R,'primitive_parameters':P,'period_points':{str(d):exact[d] for d in ds},'ramp':str(moment)})

# Analytic constants used in the unconditional mean argument.
require(F(1,2)-F(1,12)==F(5,12),'odd-prime union bound over integers')
require(F(1,2)*(1-F(5,12))==F(7,24)>F(13,48),'strict mean contradiction margin')
require(F(1,2)*F(1,2)+F(1,2)*F(1,24)==F(13,48),'residue split mean upper bound')
for n in range(1,1001):require(2*phi(n)**2>=n,'coefficient-series summability lower bound')

def reject(name,false_claim):
 require(not false_claim,'negative control incorrectly accepted: '+name)
 negative.append(name)
reject('full affine permutation at p5',len({(u,(u*u+1)*v%5) for u in range(5) for v in range(5)})==25)
reject('include maximum period at x3/4,p3 using excluded formula',F(1)==1-F(4,9))
reject('unbounded first moment stable under arbitrary completion',F(2,101)*101**2<=F(2,101))
# Two infinite subsequences and a mean are compatible with a convergent
# positive-density selection: b_n=parity(n) has mean1/2 but is0 on evens.
require(F(sum(i%2 for i in range(100)),100)==F(1,2),'mean-only toy sequence')
require(all(i%2==0 for i in range(0,100,2)),'positive-density convergent toy subsequence')
negative.append('mean and two incompatible subsequences alone do not prove every positive-upper-density exclusion')

finite_checks_before_optional_manifest=checks
if (HERE/'MANIFEST.json').exists():
 manifest=json.loads((HERE/'MANIFEST.json').read_text());seal=json.loads((HERE/'SEAL.json').read_text())
 for row in manifest['files']:
  f=HERE/row['path'];require(f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],'continuation manifest file')
 require(sha(HERE/'MANIFEST.json')==seal['manifest_sha256'],'manifest seal')
 for row in json.loads((HERE/'SOURCE_BINDINGS.json').read_text())['files']:
  f=Path(row['path']);require(f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],'source and historical originals unchanged')
print(json.dumps({'status':'PASS','method':'independent iterate-trace Mobius inversion and bounded-mixture checks; no target imports','finite_prime_max':101,'odd_primes':len(rows),'positive_checks':finite_checks_before_optional_manifest,'total_checks_including_optional_manifest':checks,'negative_controls':negative,'rows':rows,'limiting_scalar_law_proved_by_finite_checks':False},indent=2))
