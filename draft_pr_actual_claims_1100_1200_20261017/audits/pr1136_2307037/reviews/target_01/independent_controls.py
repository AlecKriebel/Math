#!/usr/bin/env python3
"""Independent target/boundary controls. No assert statements; guards survive -O."""
import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PROOF = HERE.parents[1] / 'inputs' / 'PROOF.md'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def require(condition, message):
    if not condition:
        raise ValueError(message)

def simpson(f, lo, hi, n):
    require(n > 0 and n % 2 == 0, 'Simpson interval count')
    h = (hi-lo)/n
    return h/3 * math.fsum([f(lo), f(hi)] +
        [4*f(lo+k*h) for k in range(1,n,2)] +
        [2*f(lo+k*h) for k in range(2,n,2)])

def one_pole_ray_integral(a, R, n):
    # Polar coordinates about pole a >= 0; remove the disk of radius one.
    def ray(theta):
        c = math.cos(theta)
        disc = R*R-a*a*math.sin(theta)**2
        if disc <= 0:
            return 0.0
        root = math.sqrt(disc)
        upper = -a*c+root
        lower = max(1.0, -a*c-root)
        return math.log(upper/lower) if upper > lower else 0.0
    if a > R:
        beta = math.asin(R/a)
        # Remove the square-root endpoint singularity before integration.
        return 2*simpson(lambda u:ray(math.pi+beta*math.sin(u))*beta*math.cos(u),
                         0, math.pi/2, n)
    if a > 0:
        c = (R*R-a*a-1)/(2*a)
        if c <= -1:
            return 0.0
        lo = 0.0 if c >= 1 else math.acos(c)
        return 2*simpson(ray,lo,math.pi,n)
    return 2*math.pi*ray(0)

def disk_field(a, mass, z, nr=32, nt=256):
    # Uniform in radius squared gives equal area weights in a disk.
    total = 0j
    radius = math.sqrt(mass)
    for ir in range(nr):
        r = radius*math.sqrt((ir+0.5)/nr)
        for it in range(nt):
            theta = 2*math.pi*(it+0.5)/nt
            w = a+r*complex(math.cos(theta),math.sin(theta))
            total += (w-z)**-2
    return mass*total/(nr*nt)  # integral divided by pi

def run(mutant):
    p = HERE/'control_inputs.json'
    inp = json.loads(p.read_text())
    require(inp['schema'] == 1, 'schema')
    require(sha(PROOF) == inp['proof_sha256'], 'proof pin')
    require(sha(HERE/'sources/private/1809.07200v2.pdf') == inp['hl_pdf_sha256'], 'source pin')
    n, tol = inp['quadrature_points'], inp['tolerance']
    require(n >= 4096 and n % 2 == 0 and 0 < tol < 1e-6, 'numeric guard')
    checks = []
    def close(name, observed, expected, scale=1.0):
        error = abs(observed-expected)
        require(error <= tol*max(scale,abs(expected)), name)
        checks.append({'name':name, 'observed':observed, 'expected':expected, 'abs_error':error})

    # Universal formula independently integrated after angular averaging.
    for kappa in inp['kernel_rho_over_R']:
        require(kappa > 1, 'separation guard')
        observed = simpson(lambda x:2*math.pi*x/(kappa*kappa-x*x), 0, 1, n)
        expected = math.pi*math.log1p(1/(kappa*kappa-1))
        if mutant == 'missing_pi':
            expected /= math.pi
        close('radial_kernel_ratio_'+str(kappa),observed,expected)
        # Unit scaling has no remaining R factor. An area-scaling mutant fails.
        for R in inp['kernel_R']:
            model = expected*(R*R if mutant == 'spurious_R2' else 1)
            close('scale_'+str(kappa)+'_'+str(R),observed,model)

    # Independently sample the angular kernel, sensitive to sign/normalization.
    for ratio in [0.1,0.5,1/math.sqrt(2)]:
        observed = 2*math.pi/n*math.fsum(
            1/(1+ratio*ratio-2*ratio*math.cos(2*math.pi*j/n)) for j in range(n))
        close('angular_'+str(ratio),observed,2*math.pi/(1-ratio*ratio))

    # Exact arithmetic checks repeated masses, tiny positive masses, and disk area.
    masses = [Fraction(x) for x in inp['rational_repeated_masses']]
    tiny = Fraction(inp['tiny_mass'])
    require(all(x > 0 for x in masses) and sum(masses) == 1, 'mass input')
    require(0 < tiny < 1 and (1-tiny)+tiny == 1, 'tiny normalized mass')
    area_over_pi = sum(x*x if mutant == 'radius_lambda' else x for x in masses)
    require(area_over_pi == 1, 'radii must be sqrt(lambda), not lambda')
    for z in map(Fraction,['-3','1/2','2/3','5']):
        require(sum(x/(z*z) for x in masses) == 1/(z*z), 'repeated-pole identity')
    for z in map(Fraction,['0','1/2','3/2','3']):
        direct = Fraction(1,2)/(z-2)**2+Fraction(1,2)/(z+2)**2
        formula = (z*z+4)/(z*z-4)**2
        require(direct == formula, 'two-pole rational identity')
    checks.append({'name':'exact_mass_and_rational_checks','passed':True,'tiny_mass':str(tiny)})

    # Independent area quadrature for disjoint-disk quadrature configurations.
    for label,poles,weights,z in [
        ('one',[0j],[1],2+1j),
        ('two',[-2+0j,2+0j],[0.5,0.5],1j),
        ('tiny',[0j,5+7j],[1-1e-12,1e-12],2+3j)]:
        field = sum(disk_field(a,m,z) for a,m in zip(poles,weights))
        direct = sum(m/(z-a)**2 for a,m in zip(poles,weights))
        require(abs(field-direct) <= tol*max(1,abs(direct)), 'disk exterior identity '+label)
        checks.append({'name':'disk_field_'+label,'abs_error':abs(field-direct)})

    # Exact calculus reduction independently checks arbitrary-local-mass bound.
    worst_margin = math.inf
    for t in inp['entropy_t']:
        require(0 <= t <= 1, 'local mass fraction')
        entropy = t*math.log(1/t) if t else 0.0
        require(entropy <= 1/math.e+1e-14, 'entropy upper bound')
        for R in inp['R']:
            require(R > 1, 'target radius range')
            local_bound = 2*t*math.log(R)+math.log(2)+entropy
            target_bound = 2*math.log(R)+math.log(2)+1/math.e
            margin = target_bound-local_bound
            require(margin >= -1e-12, 'universal localization algebra')
            worst_margin = min(worst_margin,margin)
    checks.append({'name':'localization_grid_diagnostic','smallest_margin_over_pi':worst_margin})

    # Independent single-pole geometries, including a pole on |z|=1.
    for a,R in [(0,1.0001),(0.5,2),(10,2),(10,20)]:
        observed = one_pole_ray_integral(a,R,n)
        if a == 0:
            exact = 2*math.pi*math.log(R)
        elif R > a+1:
            exact = math.pi*math.log(R*R-a*a)
        else:
            exact = math.pi*math.log1p(R*R/(a*a-R*R))
        close('single_pole_a_'+str(a)+'_R_'+str(R),observed,exact)
    boundary = 2*simpson(lambda x:math.log(2*math.cos(x)),0,math.pi/3,n)
    close('boundary_single_pole',one_pole_ray_integral(1,1,n),boundary)
    require(boundary > 1, 'zero additive constant obstruction')
    checks.append({'name':'wrong_C_zero_for_boundary_disk_rejected','positive_limit':boundary})

    return {'status':'PASS','schema':1,'input_sha256':sha(p),'code_sha256':sha(Path(__file__)),
            'proof_sha256':sha(PROOF),'hl_pdf_sha256':inp['hl_pdf_sha256'],
            'assertions_used':False,'floating_status':'diagnostic, not rigorous error enclosure',
            'checks':checks}

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutant',choices=['none','missing_pi','spurious_R2','radius_lambda'],default='none')
    args = ap.parse_args()
    try:
        print(json.dumps(run(args.mutant),indent=2,sort_keys=True))
    except Exception as exc:
        print(json.dumps({'status':'FAIL','mutant':args.mutant,'reason':str(exc)},sort_keys=True))
        sys.exit(1)
