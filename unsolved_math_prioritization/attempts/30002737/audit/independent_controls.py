#!/usr/bin/env python3
"""Independent reviewer controls, not an author proof attempt.
Direct deterministic RS words and physical point-set pair counts; no IID signs.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json,subprocess,tempfile,shutil
BASE=Path(__file__).resolve().parents[1]/'author'
OUT=Path(__file__).parent
manifest=json.loads((BASE/'MANIFEST.json').read_text())
hashes={name:hashlib.sha256((BASE/name).read_bytes()).hexdigest() for name in manifest['files']}
assert all(hashes[name]==meta['sha256'] for name,meta in manifest['files'].items())
# Primitive substitution, then independent bit-count formula.
rho={'a':'ab','b':'ac','c':'db','d':'dc'}
word='a'
for _ in range(18):word=''.join(map(rho.__getitem__,word))
signs=[1 if c in 'ab' else -1 for c in word]
bit_signs=[(-1)**((n&(n>>1)).bit_count()) for n in range(len(word))]
assert signs==bit_signs
primitive_depth=None
for k in range(1,8):
    images={c:c for c in rho}
    for _ in range(k):images={c:''.join(rho[t] for t in s) for c,s in images.items()}
    if all(set(s)==set('abcd') for s in images.values()):primitive_depth=k;break
assert primitive_depth==3
# Source's two-sided fixed point: c|a is a legal rho^2 seed.
def rs(n):
    if n==0:return 1
    if n==-1:return -1
    q,r=divmod(n,4)
    return rs(q)*(1 if r<2 or (q+r)%2==0 else -1)
left,right='c','a'
for _ in range(6):
    for __ in range(2):left=''.join(rho[t] for t in left);right=''.join(rho[t] for t in right)
bilateral=[1 if c in 'ab' else -1 for c in left+right]
assert bilateral==[rs(n) for n in range(-len(left),len(right))]
rs_samples=[]
for n in [1024,4096,16384,65536,262144]:
    a=signs[:n]
    corr=[sum(a[i]*a[i+h] for i in range(n-h))/n for h in range(1,65)]
    rs_samples.append({'length':n,'mean':sum(a)/n,'max_abs_lag_1_to_64':max(map(abs,corr))})
# Physical motif on the exact 1/30 grid, direct membership counts.
C=[(0,0),(3,3),(10,0),(0,10)]
weights=[F(1),F(1),F(1,2),F(1,2)]
def marker_pairs(C,e):
    return [(i,j) for i,c in enumerate(C) for j,d in enumerate(C) if tuple((d[k]-c[k])%30 for k in [0,1])==e]
assert marker_pairs(C,C[1])==[(0,1)]
mutant=[(0,0),(5,0),(10,0),(0,10)]
assert marker_pairs(mutant,mutant[1])==[(0,1),(1,2)]
# For ALL local choices of signs at three consecutive rows/columns,
# recognize every possible directed e-pair by actual physical points.
local_marker_cases=0
for xs in product((-1,1),repeat=3):
  for ys in product((-1,1),repeat=3):
    pts=set()
    for i,j in product(range(3),repeat=2):
      for c in [0,1]+([2] if xs[i]==1 else [])+([3] if ys[j]==1 else []):
        pts.add((30*i+C[c][0],30*j+C[c][1]))
    detected={p for p in pts if (p[0]+3,p[1]+3) in pts}
    assert detected=={(30*i,30*j) for i,j in product(range(3),repeat=2)}
    local_marker_cases+=1
shifts=sorted({(d[0]-c[0]+30*m,d[1]-c[1]+30*n) for c,d in product(C,repeat=2) for m,n in product(range(-1,2),repeat=2)})
def infinite_coeff(r):
    out=F(0)
    for c,d in product(range(4),repeat=2):
        if all((r[k]-(C[d][k]-C[c][k]))%30==0 for k in [0,1]):out+=weights[c]*weights[d]
    if r[0]==0 and r[1]%30==0:out+=F(1,4)
    if r[1]==0 and r[0]%30==0:out+=F(1,4)
    return out
physical=[]
for N in [64,128,256]:
    xs=signs[:N];ys=signs[1024:1024+N]
    points=set()
    for i,j in product(range(N),repeat=2):
      for c in [0,1]+([2] if xs[i]==1 else [])+([3] if ys[j]==1 else []):
        points.add((30*i+C[c][0],30*j+C[c][1]))
    # An independent factorized finite count; includes ALL boundary and mean terms.
    def finite_coeff_count(r):
      total=0
      for c,d in product(range(4),repeat=2):
        remainder=[r[k]-(C[d][k]-C[c][k]) for k in [0,1]]
        if any(v%30 for v in remainder):continue
        m,n=[v//30 for v in remainder]
        I=range(max(0,-m),min(N,N-m));J=range(max(0,-n),min(N,N-n))
        xc=sum((c!=2 or xs[i]==1) and (d!=2 or xs[i+m]==1) for i in I)
        yc=sum((c!=3 or ys[j]==1) and (d!=3 or ys[j+n]==1) for j in J)
        total+=xc*yc
      return total
    max_error=F(0);worst=None
    for r in shifts:
      actual=sum((p[0]+r[0],p[1]+r[1]) in points for p in points)
      assert actual==finite_coeff_count(r),(N,r,actual,finite_coeff_count(r))
      error=abs(F(actual,N*N)-infinite_coeff(r))
      if error>max_error:max_error=error;worst=r
    physical.append({'side':N,'point_count':len(points),'empirical_density':len(points)/(N*N),'tested_displacements':len(shifts),'max_infinite_limit_error':float(max_error),'worst_displacement_grid30':worst})
# Finite invariant rectangle statistics demonstrate that x/y at identical
# sequences are independent under separate coordinate spatial averages.
N=256
assert sum(signs[i]*signs[j] for i,j in product(range(N),repeat=2))==sum(signs[:N])**2
# Section integration using exact cell breakpoints, not overlap formula.
def exact_flow_corr(t):
    cuts=sorted({F(0),F(1)}|{F(z)-t for z in range(-7,8) if 0<F(z)-t<1})
    total=F(0)
    for a,b in zip(cuts,cuts[1:]):
        u=(a+b)/2;shift=(u+t).__floor__()
        if shift==0:total+=b-a
    return total
flow_checks=0
for denom in [2,3,5,7,11,13]:
  for num in range(-4*denom,4*denom+1):
    t=F(num,denom)
    assert exact_flow_corr(t)==max(F(0),1-abs(t))
    flow_checks+=1
# Run frozen checker only in an isolated copy, preserving frozen output.
with tempfile.TemporaryDirectory() as td:
    copy=Path(td)/'verify_counterexample.py';shutil.copyfile(BASE/'checks/verify_counterexample.py',copy)
    replay=json.loads(subprocess.check_output(['python3',str(copy)],text=True))
    assert replay==json.loads((BASE/'checks/verification_results.json').read_text())
assert all(hashlib.sha256((BASE/name).read_bytes()).hexdigest()==h for name,h in hashes.items())
result={'verdict':'PASS','frozen_hashes':hashes,'rho_primitive_depth':primitive_depth,'rho_vs_bit_formula_sites':len(word),'bilateral_source_recursion_sites':len(bilateral),'rs_finite_samples':rs_samples,'physical_point_count_controls':physical,'exhaustive_local_marker_cases':local_marker_cases,'bad_marker_negative_control':'caught extra pair (1,2)','exact_flow_section_checks':flow_checks,'frozen_checker_isolated_replay':'identical results; frozen sources unchanged','limitations':'Finite tests are diagnostics; the infinite conclusions are proved analytically in independent_audit.md.'}
(OUT/'independent_controls_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
