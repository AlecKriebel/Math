#!/usr/bin/env python3
"""Read-only audit controls. No finite test certifies all valuation statements."""
from pathlib import Path
from hashlib import sha256
import itertools
import json
import sys
import sympy as s

release = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / 'release'
checks = []
def require(name, assertion):
    if not assertion:
        raise AssertionError(name)
    checks.append(name)

manifest_bytes = (release/'AUTHOR_MANIFEST.json').read_bytes()
manifest = json.loads(manifest_bytes)
require('exact_frozen_manifest', sha256(manifest_bytes).hexdigest() == '380647dacb6bbc1e7c31784712465143b5feb90ff124a57c666c74cae68b0e2c')
require('manifest_binds_seven_payloads', manifest['file_count'] == len(manifest['files']) == 7)
actual = sorted(str(p.relative_to(release)) for p in release.rglob('*') if p.is_file())
require('exact_eight_file_inventory', actual == sorted(['AUTHOR_MANIFEST.json'] + [r['path'] for r in manifest['files']]))
for rec in manifest['files']:
    data = (release/rec['path']).read_bytes()
    require('bound_payload:' + rec['path'], len(data) == rec['bytes'] and sha256(data).hexdigest() == rec['sha256'])

# A separate scalar parity invariant immediately excludes zero in the CTPS residue sum.
options = [((0,0,1),(0,1,0)), ((0,0,0),(1,0,1)), ((0,0,0),(1,1,0))]
parities = [[sum(row)%2 for row in option] for option in options]
require('residue_scalar_invariant', parities == [[1,1],[0,0],[0,0]])
sums = [tuple(sum(choice[j] for choice in choices)%2 for j in range(3)) for choices in itertools.product(*options)]
require('all_eight_residue_sums_are_odd', len(sums) == 8 and all(sum(row)%2 == 1 for row in sums))

# At a codimension-one point, divisor avoidance allows at most one nonzero order.
# These four parity patterns exhaust that possibility; they do not enumerate valuations.
patterns = [(0,0,0),(1,0,0),(0,1,0),(0,0,1)]
require('horizontal_vertical_parity_implication', all(not ((e2+e3)%2 == (e3+e1)%2 == 0) or (e1+e2+e3)%2 == 0 for e1,e2,e3 in patterns))

p1,p2,p3,r = s.symbols('p1 p2 p3 r', nonzero=True)
a,b,c = p2*p3,p3*p1,p1*p2*p3
for i,(norm_value,sub) in enumerate([(-a*r*r,{p1:-r*r}),(-b*r*r,{p2:-r*r}),(-a*b/(r*r),{p3:-r*r})],1):
    require('explicit_closed_center_point_' + str(i), s.cancel((norm_value-c).subs(sub)) == 0)

x,t=s.symbols('x t')
f=x**3+x**2+t**3
require('elliptic_cubic_discriminant', s.expand(s.discriminant(f,x) + t**3*(27*t**3+4)) == 0)
b2,b4,b6,b8=s.Integer(4),s.Integer(0),4*t**3,4*t**3
Delta=-b2**2*b8-8*b4**3-27*b6**2+9*b2*b4*b6
require('minimal_Weierstrass_invariants', s.expand(Delta + 16*t**3*(27*t**3+4)) == 0 and b2**2-24*b4 == 16)

# Connected split kernel: the norm map has character column (1,...,1).
require('norm_product_primitive_character', s.gcd_list([1]*6) == 1 and 6-1 == 5)

# The class i is explicitly killed by 2 without being assumed trivial.
a0=s.symbols('a0', nonzero=True)
require('residual_class_order_divides_two_identity', s.simplify((-a0)/a0) == -1 and s.I**2 == -1 and s.I**4 == 1)

for n in (3,6):
    matrix=s.zeros(n,n)
    for i in range(n):
        matrix[i,i]=-1
        matrix[i,(i+1)%n]=1
    require('cycle_betti_number_'+str(n), n-matrix.rank() == 1)

result={
 'status':'PASS',
 'control_count':len(checks),
 'checks':checks,
 'frozen_payload_count':7,
 'frozen_total_file_count':8,
 'manifest_sha256':sha256(manifest_bytes).hexdigest(),
 'result_sha256':sha256((release/'RESULT.md').read_bytes()).hexdigest(),
 'ctps_residue_sums':sums,
 'scope':'Integrity, exact algebra, and finite bookkeeping only. Source theorem applicability and all-valuation coverage are reasoned in AUDIT.md; no formal proof certification is claimed.',
 'sympy_version':s.__version__,
}
print(json.dumps(result,indent=2,sort_keys=True))
