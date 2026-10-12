#!/usr/bin/env python3
"""Exact audit controls for the proposed inverse-perimeter transfer, not a proof search."""
from fractions import Fraction as F
from pathlib import Path
import datetime, hashlib, json, os, sys

checks = 0

def require(condition, name):
    global checks
    checks += 1
    if not condition:
        raise RuntimeError(name)

def dot(u, v):
    return u[0]*v[0]+u[1]*v[1]

def sub(u, v):
    return (u[0]-v[0], u[1]-v[1])

def inverse(u):
    r2 = dot(u,u)
    return (u[0]/r2, u[1]/r2)

def det(u,v):
    return u[0]*v[1]-u[1]*v[0]

cases = []
for integers in [(1,2,3,1),(2,1,-1,4),(5,-2,3,7),(-4,3,2,5),(1,-3,-2,-1),(3,2,3,-2),(7,4,-2,6)]:
    u, v = tuple(map(F,integers[:2])), tuple(map(F,integers[2:]))
    r2, s2, determinant = dot(u,u), dot(v,v), det(u,v)
    ell2 = dot(sub(v,u),sub(v,u))
    q = ((r2*v[1]-s2*u[1])/determinant, (u[0]*s2-v[0]*r2)/determinant)
    iu, iv = inverse(u), inverse(v)
    height2 = determinant*determinant/ell2
    inverse_ell2 = dot(sub(iv,iu),sub(iv,iu))
    inverse_height2 = det(iu,iv)**2/inverse_ell2
    q2 = dot(q,q)
    require(dot(q,u)==r2 and dot(q,v)==s2, 'actual antipedal supporting lines')
    require(dot(q,iu)==1 and dot(q,iv)==1, 'inverse-polar line equations')
    require(inverse_ell2==ell2/(r2*s2), 'inverse chord metric')
    require(inverse_height2==height2/(r2*s2), 'inverse sideline height metric')
    require(q2==r2*s2/height2, 'ordinary antipedal norm square')
    require(q2*inverse_height2==1, 'antipedal norm reciprocal inverse height')
    cases.append({'u':list(map(str,u)), 'v':list(map(str,v)), 'q_squared':str(q2), 'inverse_edge_squared':str(inverse_ell2)})

# Same outer ellipse a=5,b=3,f=(4,0) and strictly nested confocal caustic lambda=19/4.
# These are regular tangent chords. Closure is deliberately not assumed for this local transfer check.
lam = F(19,4)
vertical = {'rho_squared':F(81,4), 'outer_support_squared':F(25), 'height_squared':F(1,4), 'focal_radius_product_squared':F(49,25)**2, 'edge_squared':F(171,25)}
horizontal = {'rho_squared':F(17,4), 'outer_support_squared':F(9), 'height_squared':F(17,4), 'focal_radius_product_squared':F(149,9)**2, 'edge_squared':F(475,9)}
controls = []
for label, data in [('vertical',vertical),('horizontal',horizontal)]:
    require(data['outer_support_squared']-data['rho_squared']==lam, 'same confocal caustic')
    require(F(0)<lam<F(9), 'strict nested elliptical caustic')
    q2=data['focal_radius_product_squared']/data['height_squared']
    inverse_edge2=data['edge_squared']/data['focal_radius_product_squared']
    controls.append({'chord':label, 'q_squared':str(q2), 'inverse_edge_squared':str(inverse_edge2), 'ratio_squared':str(q2/inverse_edge2)})
require(controls[0]['ratio_squared']!=controls[1]['ratio_squared'], 'reject fixed-pair per-edge scaling of antipedal norm by inverse sidelength')
require(controls[0]['q_squared']=='9604/625', 'vertical independently specified value')
require(controls[1]['q_squared']=='88804/1377', 'horizontal independently specified value')

result = {
    'schema':'pr110-modern-metric-transfer-controls/v1',
    'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'actual_PID':os.getpid(), 'executable':sys.executable,
    'optimization':sys.flags.optimize, 'explicit_checks':checks,
    'status':'passed', 'rational_general_cases':cases, 'same_confocal_pair_controls':controls,
    'check_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'meaning':'Rejects a proposed constant per-edge metric scaling; verifies inversion/polarity observable mapping. It does not disprove a nonlocal identity or certify novelty, and is not a k603 proof search.'
}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'passed','explicit_checks':checks,'actual_PID':os.getpid(),'optimization':sys.flags.optimize}))
