#!/usr/bin/env python3
"""Read-only verification of scope bindings and independently derived boundaries.

Never invokes source builders, mutates source, or reads another review lane.
Run with any Python 3; only standard-library modules are used.
"""
from pathlib import Path
from fractions import Fraction as F
import ast, hashlib, json

HERE=Path(__file__).resolve().parent
PAPER=HERE.parents[2]
SOURCE=PAPER/'sources'
READY=SOURCE/'SOURCE_READY.json'
assert hashlib.sha256(READY.read_bytes()).hexdigest()=='b0fbd1e6e0b06518f837b4d59e1c5bc28e40a4aed044d9d46b3408856b3a45ce'
r=json.loads(READY.read_text())
for key,want in [('selected_actual_PDF','cfd9eb2755a4f9296eae8209adff6f6b41708425a4a4f186e647184ec6617672'),('controlling_TeX','40aac446c6391fe840578a6276f39ea045236f6d64e0b0184d15f67c9c376f20')]:
 b=Path(r[key]['path']).read_bytes();assert len(b)==r[key]['bytes'];assert hashlib.sha256(b).hexdigest()==want
assert r['record_id']==21850042 and r['latest_record_id']==22625980
assert r['publication_date']=='2026-08-08'
assert r['version']=='simultaneous-amplification-below-three-halves-v1.0.0'
print('PASS exact record, version, original date, PDF and TeX SHA256 bindings')

# Center initialization is indispensable at endpoint: mixing a deficit q/N
# with center probability 1/(3N+1) adds q/3=1/9 to the graph dB deficit.
q=F(1,3);module_B=F(4,3);module_D=F(16,81)
graph_B=module_B;graph_D=module_D+q/3
baseline_B=F(0);baseline_D=q/3
assert graph_D==F(25,81)
assert graph_B-baseline_B==F(4,3)
assert graph_D-baseline_D==F(16,81)
assert (q/F(1,4), q/F(27,16))==(module_B,module_D)
print('PASS independent endpoint coefficients including dB center-start term')

# Fixed-r strict comparison follows from limits; the sign vanishes at 3/2.
for fitness in (F(1001,1000),F(6,5),F(1499,1000),F(3,2),F(2)):
 gap=q-(1-1/fitness)
 assert gap==(3-2*fitness)/(3*fitness)
 assert (gap>0)==(fitness<F(3,2))
print('PASS fixed-r interval sign and endpoint boundary; no uniform-r conclusion')

# Prop 8 independent exact checks, including extreme positive total weights.
r0=F(3,2);s=F(5,4);z=F(9,8)
gamma=(s/z+z)/(s+1);Ds=(1/z)/(1-gamma)
assert gamma==F(161,162) and Ds==144 and r0*(r0+1)*Ds==540
for c in range(13,201):
 k=c//2
 assert F(2*c-1,2*(c+2))>=F(5,6)
 for i in range(1,k):
  b=(c-i)*r0*i/(c+(r0-1)*i)
  death=i*F(c-i+1)/(c+(r0-1)*(i-1))
  ratio=b/death
  assert s<=ratio<=r0
  up=ratio/(1+ratio)
  assert 1-(up/z+(1-up)*z)>=1-gamma
  for W in (F(1,10**12),F(1),F(10**12)):
   activation=r0*i/(c+W+(r0-1)*i)
   assert activation/death<=r0*(r0+1)/c
 assert F(c)*F(2,3)**k/(1-F(2,3)**k)<2
assert (F(540)+1+r0)/q+2<F(1630)
for c in (0,1,13,10**4):
 for weights in ((F(1,10**12),F(10**12)),(F(1),),(F(1,7),F(13),F(8,9))):
  W=sum(weights)
  activations=[r0*w/(c+W+(2*r0-1)*w) for w in weights]
  assert sum(activations)<=r0
print('PASS arbitrary-weight leaf hazard, core-potential constants, endpoint A=1630 boundary checks')

# Strengthen the native q2 verifier cover test: Kraft sum by itself does not
# validate changing axis choices. Confirm a consistent split axis at every
# common node as well as full binary coverage for this actual certificate.
base=Path(r['controlling_TeX']['path']).parents[1]
script=base/'construction/higher_threshold/direct_portal_network/verify_q2_scalar_separator.py'
tree=ast.parse(script.read_text())
node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='INTERVAL_PATHS' for t in n.targets))
paths=ast.literal_eval(node.value)
def cover(suffixes):
 if any(not p for p in suffixes):
  assert len(suffixes)==1 and not suffixes[0];return
 assert len({p[0][0] for p in suffixes})==1
 for side in (0,1):
  children=[p[1:] for p in suffixes if p[0][1]==side]
  assert children;cover(children)
cover(paths)
assert len(paths)==11 and max(map(len,paths))==5
print('PASS independent direct-two-portal 11-box cover geometry')

# A precise warning test for reading the diffuse support extension too broadly.
# Its max(lambda)=o(s) condition alone does NOT imply fast strong-pair
# resolution when Q also grows. This is an interface diagnostic, not a
# counterexample to any no-amplification conclusion.
for k in (2,10,100):
 population_blades=k**4;portals=k**2;heavy_lambda=k**3
 assert F(heavy_lambda,population_blades)==F(1,k)
 assert F(portals,population_blades)==F(1,k**2)
 assert F(portals*heavy_lambda,population_blades)==k
witness=json.loads((HERE/'DIFFUSE_INTERFACE_WITNESS.json').read_text())
for row in witness['rows']:
 k=row['k'];population_blades=k**4;portals=k**2
 pi=F(1,k**3);lam_h=k**3;lam_l=1/(1-pi)
 B=2*(pi*lam_h+(1-pi)*lam_l)
 assert B==4 and row['B']==str(B)
 assert row['child_type_mass_heavy']==str(2*pi*lam_h/B)==str(F(1,2))
 up=r0*(1+F(1,k))/(r0*(1+F(1,k))+F(portals-1,k))
 down=(1+F(portals-1,k))/(1+F(portals-1,k)+r0*F(1,k))
 assert row['dB_pair_up_rate']==str(up)
 assert row['dB_pair_down_rate']==str(down)
 assert row['pair_up_first_if_portals_frozen']==str(up/(up+down))
 assert up<=r0*F(k+1,k*k-1)
 assert down>=F(1,1+r0/k)
print('PASS exact diffuse interface witness: fixed B, half child mass, up→0 and down→1')
print('ALL SCOPE CHECKS PASS; these finite/algebraic checks do not certify unproved stochastic limits')

# Validate original input bindings and the immutable continuation seal when present.
for row in json.loads((HERE/'SOURCE_BINDINGS.json').read_text())['files']:
 data=Path(row['path']).read_bytes()
 assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
if (HERE/'MANIFEST.json').exists():
 manifest=json.loads((HERE/'MANIFEST.json').read_text())
 for row in manifest['files']:
  data=(HERE/row['path']).read_bytes()
  assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
 seal=json.loads((HERE/'SEAL.json').read_text())
 assert hashlib.sha256((HERE/'MANIFEST.json').read_bytes()).hexdigest()==seal['manifest_sha256']
 assert hashlib.sha256((HERE/'REPORT.md').read_bytes()).hexdigest()==seal['report_sha256']
 assert hashlib.sha256((HERE/'VERDICT.json').read_bytes()).hexdigest()==seal['verdict_sha256']
 print('PASS original input bindings and immutable continuation manifest/seal')
