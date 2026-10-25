#!/usr/bin/env python3
"""Independent finite controls for PR 906. No assertions or candidate imports.

Needs sympy==1.14.0 and mpmath==1.3.0. Authentication is against the
manifest hash read from the live PR on 2026-10-13, never a self-supplied pin.
The written analytic proof remains necessary; finite controls cannot check
all Sobolev competitors or certify historical novelty.
"""
import argparse
import ast
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import stat
import sys

PUBLIC_PIN = 'acab12ef33c8e2dc566337cfe01b94f2fe81f06ede4b31f1c363e055741fb0df'
HEAD = '32eaecaa8907dbf674e65b138b000cdcc49004ae'
PINS = {
    'author/MANIFEST.json': '9cb1f5c242224d4f04a34b1d28e660a29fb2f63d47215d16257f5d4073c001cb',
    'author/PROOF.md': '2634e714b9a06a1770ae39b0201031c7d2a7ce6e97f3330f8745d0e2453d4fef',
    'author/KOREVAAR_SCHOEN.md': '4bac91a7e34b266391051d48ae2ef10adc60d10b6ed0d57d1c5cb8395e2a6abe',
    'audit_a/AUDIT_MANIFEST.json': 'dd4962a906e248bd347b1ce4296a4817bcc5ce2ac9a0ef417344faf9883fe052',
    'audit_b/AUDIT_MANIFEST.json': '0c7e1f517f62b27734e5e91a7a7209585ecc2b853bdc1d460b4cee7f4013f5dc',
}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def default_packet():
    here = Path(__file__).resolve().parent
    for ancestor in [here, *here.parents][:6]:
        for p in [ancestor / 'original_packet', ancestor / 'original/unsolved_math_prioritization/attempts/30006419']:
            if (p / 'PUBLIC_MANIFEST.json').is_file():
                return p
    raise RuntimeError('Supply --packet; original_packet/ package fallback was not found')


def authenticate(packet):
    packet = Path(packet)
    require(not packet.is_symlink(), 'Independent guard rejects a symlinked root')
    packet = packet.resolve()
    entries = {}
    dirs = set()
    for p in packet.rglob('*'):
        mode = p.lstat().st_mode
        rel = p.relative_to(packet).as_posix()
        require(not stat.S_ISLNK(mode), 'Symlink: ' + rel)
        if stat.S_ISREG(mode):
            entries[rel] = p
        elif stat.S_ISDIR(mode):
            dirs.add(rel)
        else:
            raise RuntimeError('Nonregular path: ' + rel)
    require('PUBLIC_MANIFEST.json' in entries, 'Missing regular public manifest')
    raw = entries['PUBLIC_MANIFEST.json'].read_bytes()
    require(digest(raw) == PUBLIC_PIN, 'Externally fixed public manifest mismatch')
    m = json.loads(raw)
    require(m['problem_id'] == 30006419 and m['turns'] == '2/5' and m['status'] == 'claimed_solved', 'Scope mismatch')
    require(m['frozen_files_preserved'] == 22, 'Frozen count mismatch')
    records = m['files']
    require(type(records) is dict and len(records) == 29, 'Wrong manifest shape/count')
    expected_dirs = set()
    for name, rec in records.items():
        q = PurePosixPath(name)
        require(not q.is_absolute() and q.as_posix() == name and all(x not in ('', '.', '..') for x in q.parts), 'Unsafe path')
        require(type(rec) is dict and set(rec) == {'bytes', 'sha256'}, 'Record shape')
        require(type(rec['bytes']) is int and rec['bytes'] >= 0 and type(rec['sha256']) is str and len(rec['sha256']) == 64, 'Record types')
        for parent in q.parents:
            if parent.as_posix() != '.':
                expected_dirs.add(parent.as_posix())
    require(set(entries) == set(records) | {'PUBLIC_MANIFEST.json'} and dirs == expected_dirs, 'Closed inventory mismatch')
    for name, rec in records.items():
        data = entries[name].read_bytes()
        require(len(data) == rec['bytes'] and digest(data) == rec['sha256'], 'Byte mismatch: ' + name)
    for name, sha in PINS.items():
        require(digest(entries[name].read_bytes()) == sha, 'Independent frozen pin mismatch: ' + name)
    nested_count = 0
    for folder, filename in [('author', 'MANIFEST.json'), ('audit_a', 'AUDIT_MANIFEST.json'), ('audit_b', 'AUDIT_MANIFEST.json')]:
        nested = json.loads(entries[folder + '/' + filename].read_bytes())
        require(nested['problem_id'] == 30006419, 'Nested identity')
        require({p.name for p in (packet / folder).iterdir()} == set(nested['files']) | {filename}, 'Nested inventory')
        for name, rec in nested['files'].items():
            require(records[folder + '/' + name] == rec, 'Nested record mismatch')
        nested_count += len(nested['files']) + 1
    require(nested_count == 22, 'Frozen nested count')
    status = json.loads(entries['PUBLICATION_STATUS.json'].read_bytes())
    require(status['turns'] == '2/5' and status['frozen_files_preserved'] == 22, 'Status mismatch')
    tree = ast.parse(entries['audit_b/independent_checks.py'].read_bytes())
    omissions = [n for n in tree.body if isinstance(n, ast.For) and isinstance(n.iter, ast.Call)
                 and isinstance(n.iter.func, ast.Attribute) and isinstance(n.iter.func.value, ast.Name)
                 and n.iter.func.value.id == 'source_expected' and n.iter.func.attr == 'items']
    require(len(omissions) == 1, 'Adapter must omit exactly one original source loop')
    require(any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'require' for n in ast.walk(omissions[0])), 'Source loop guard')
    assertion_counts = {n: sum(isinstance(q, ast.Assert) for q in ast.walk(ast.parse(entries[n].read_bytes())))
                        for n in ['author/checks.py', 'audit_a/independent_controls.py', 'audit_b/independent_checks.py', 'verify_publication.py', 'source_free_audit_b.py']}
    require(all(v == 0 for v in assertion_counts.values()), 'Frozen runtime guard removed by optimization')
    return {'status': 'PASS', 'head': HEAD, 'public_manifest_sha256': PUBLIC_PIN, 'packet_files': len(entries),
            'frozen_files': nested_count, 'turns': '2/5', 'assertion_counts': assertion_counts,
            'source_free_adapter_omitted_top_level_loops': len(omissions)}


def exact_controls(sp):
    x, y, t = sp.symbols('x y t', real=True)
    results = []
    def check(name, ok, detail=None):
        require(bool(ok), 'Exact control: ' + name)
        results.append({'name': name, 'passed': True, 'detail': detail})
    integrate = lambda f: sp.integrate(sp.expand(f), (x, 0, 1), (y, 0, 1))
    bubble = x**2 * (1-x)**2 * y**2 * (1-y)**2
    for k in [-5, -2, 0, 3, 7]:
        w = sp.Rational(k, 11) * bubble * (1+x+2*y)
        f = y+w
        e = integrate(sp.diff(f,x)**2+sp.diff(f,y)**2)
        check('scalar_same_trace_' + str(k), e == 1+integrate(sp.diff(w,x)**2+sp.diff(w,y)**2))
    check('scalar_wrong_trace_negative', integrate(sp.diff(2*y,y)**2) != 1)
    # The exact-form calculation uses a polynomial primitive in target coordinates.
    # It differs from the candidate's monomial moment implementation.
    for k in [-2, 1, 4]:
        u = x+sp.Rational(k,5)*bubble
        v = y+sp.Rational(k+1,7)*bubble*(1+x)
        jac = sp.diff(u,x)*sp.diff(v,y)-sp.diff(u,y)*sp.diff(v,x)
        omega = 1+u+v+u**2*v
        baseline = integrate(1+x+y+x**2*y)
        check('same_boundary_exact_form_' + str(k), integrate(omega*jac) == baseline)
    check('changed_boundary_exact_form_negative', integrate((1+2*x+y+4*x**2*y)*2) != integrate(1+x+y+x**2*y))
    for mass in [sp.Rational(1,99), sp.Rational(1,3), sp.Rational(49,100)]:
        b = mass/(1-mass)
        check('calibration_mass_' + str(mass), (1+b)*mass-b == 0 and 0 < b < 1 and (1+b)-b == 1)
    check('large_cutoff_negative', sp.Rational(3,4)/(1-sp.Rational(3,4)) > 1)
    check('conformal_factor_cancellation', sp.cancel((sp.Symbol('r',positive=True)/sp.Symbol('d',positive=True))**2 * sp.Symbol('d',positive=True)**2) == sp.Symbol('r',positive=True)**2)
    # Angular moments are obtained by beta integrals, then tested on independent
    # PSD matrices, including zero and rank-one boundaries.
    moment = lambda p,q: sp.simplify(2*sp.beta(sp.Rational(p+1,2),sp.Rational(q+1,2))/sp.pi) if p%2 == q%2 == 0 else 0
    moments = {(p,q):sp.simplify(moment(p,q).rewrite(sp.gamma)) for p,q in [(0,0),(2,0),(0,2),(4,0),(2,2),(0,4)]}
    check('angular_beta_moments', moments == {(0,0):2,(2,0):1,(0,2):1,(4,0):sp.Rational(3,4),(2,2):sp.Rational(1,4),(0,4):sp.Rational(3,4)})
    theta = sp.symbols('theta', real=True)
    W = sp.Matrix([sp.cos(theta),sp.sin(theta)])
    matrices = [sp.zeros(2),sp.eye(2),sp.diag(9,0),sp.Matrix([[1,1],[1,1]]),sp.Matrix([[5,2],[2,1]]),sp.Matrix([[sp.Rational(1,7),0],[0,sp.Rational(1,70000)]])]
    B = sp.Matrix([[sp.Rational(2,9),sp.Rational(-3,8)],[sp.Rational(4,5),sp.Rational(1,6)]])
    epsilon = sp.symbols('epsilon')
    for i,G in enumerate(matrices):
        check('PSD_boundary_' + str(i), G.det() >= 0 and G[0,0] >= 0 and G[1,1] >= 0)
        sq = (W.T*G*W)[0]
        T = sp.simplify(sp.integrate(sq*(4*W*W.T-2*sp.eye(2)),(theta,0,2*sp.pi))/sp.pi)
        check('quadratic_stress_' + str(i), T == 2*G-sp.trace(G)*sp.eye(2))
        A = sp.eye(2)+epsilon*B
        direct = sp.trace(A.T*G*A)/A.det()
        pairing = sum(T[a,b]*B[a,b] for a in range(2) for b in range(2))
        check('exact_first_variation_' + str(i), sp.simplify(sp.diff(direct,epsilon).subs(epsilon,0)-pairing) == 0)
    for n in [1,2,7,100,10000]:
        w = sp.Rational(1,8*n)
        check('positive_band_witness_' + str(n), 0 < w < sp.Rational(1,4) and 1/w**2 > n)
    check('central_h_degree_three', sp.diff(t**3/3,t) == t**2 and sp.Poly(t**3/3,t).degree() == 3)
    core_defect = sp.integrate(1-t**2,(t,0,sp.Rational(1,4)))
    check('strict_compression_lower_bound', core_defect == sp.Rational(47,192) and core_defect > 0)
    # New rectangle and bubble, checked by direct integration and independent
    # integration by parts. The test is W0^{1,2}; scalar smoothing preserves sign.
    left,right = sp.Rational(1,10),sp.Rational(1,5)
    psi = (t-left)**3*(right-t)**3*x**3*(1-x)**3
    rect = lambda f: sp.integrate(sp.expand(f),(t,left,right),(x,0,1))
    first = rect(2*t**2*sp.diff(psi,t))
    parts = rect(-4*t*psi)
    second = rect(sp.diff(psi,t)**2+sp.diff(psi,x)**2)
    step = -first/(2*second)
    change = sp.factor(step*first+step**2*second)
    image_bound = right**3/3+step*(right-left)**6/4096
    check('KS_finite_lowering_same_trace', first == parts and first < 0 and second > 0 and change < 0 and image_bound < 2,
          {'first':str(first),'quadratic':str(second),'step':str(step),'energy_change':str(change),'image_bound':str(image_bound)})
    m = sp.sqrt(17)-4
    check('KS_root_reciprocal', sp.simplify(m*m+8*m-1) == 0 and sp.simplify(1/m-4-sp.sqrt(17)) == 0 and m > 0)
    return results


def model_guard(sp, coefficient=16, denominator=3, degree=3, shift_upper=None):
    # A sensitivity control on the stated construction, not a new proof search.
    shift_upper = sp.Rational(1,2) if shift_upper is None else shift_upper
    inner = sp.sqrt(sp.Rational(1,coefficient))
    outer = sp.sqrt(sp.Rational(1+denominator,coefficient))
    require(inner == sp.Rational(1,4), 'Wrong central cutoff')
    require(outer == sp.Rational(1,2), 'Wrong exterior cutoff')
    t = sp.Symbol('t')
    require(sp.diff(t**degree/sp.Integer(degree),t) == t*t, 'Wrong central leading degree')
    require(shift_upper == sp.Rational(1,2), 'Unsupported shift upper bound')
    return True


def numerical_controls(mp):
    # These are arbitrary-precision quadrature/finite-difference diagnostics,
    # without rigorous enclosure or proven error bounds.
    def run(dps):
        with mp.workdps(dps):
            def H(z):
                if z <= 0: return mp.mpf(0)
                if z >= 1: return mp.mpf(1)
                return 1/(1+mp.exp(1/z-1/(1-z)))
            def radial_derivative(t):
                weight = H((16*t*t-1)/3)
                return t*t+(1-t*t)*weight
            c = mp.quad(lambda t:1-radial_derivative(t),[0,mp.mpf(1)/4,mp.mpf(1)/2])
            require(mp.mpf(47)/192 < c < mp.mpf(1)/2, 'Numerical compression bound')
            rho2 = lambda s:mp.exp(-2*s*H(s-2))
            transition = mp.quad(rho2,[2,mp.mpf('2.25'),mp.mpf('2.5'),mp.mpf('2.75'),3])
            tail = mp.exp(-6)/2
            target_area = 4*mp.pi*(2+transition+tail)
            # Integrate source intervals: [0,1/2] is flat, and h=t-c outside.
            source_energy = 4*mp.pi*(mp.mpf(1)/2+(2+c-mp.mpf(1)/2)+transition+tail)
            gap_error = abs(source_energy-target_area-4*mp.pi*c)
            require(gap_error < mp.mpf('1e-28'), 'Numerical energy defect')
            A = mp.matrix([['1.17','.23'],['-.19','.84']])
            B = mp.matrix([['.27','-.33'],['.41','-.16']])
            R = mp.matrix([[mp.cos(mp.mpf('.371')),-mp.sin(mp.mpf('.371'))],[mp.sin(mp.mpf('.371')),mp.cos(mp.mpf('.371'))]])
            norms = {
                'euclidean':lambda v:mp.sqrt(v[0]**2+v[1]**2),
                'ellipsoid':lambda v:mp.sqrt(2*v[0]**2+mp.mpf('0.6')*v[0]*v[1]+mp.mpf('.8')*v[1]**2),
                'l1':lambda v:abs(v[0])+abs(v[1]),
                'linfty':lambda v:max(abs(v[0]),abs(v[1])),
                'rank_one':lambda v:mp.mpf('1.7')*abs(v[0]),
                'zero':lambda v:mp.mpf(0),
            }
            def breaks(C):
                rows = [[C[0,0],C[0,1]],[C[1,0],C[1,1]],
                        [C[0,0]-C[1,0],C[0,1]-C[1,1]], [C[0,0]+C[1,0],C[0,1]+C[1,1]]]
                points = [mp.mpf(0),2*mp.pi]
                for a,b in rows:
                    if a == b == 0: continue
                    root = mp.atan2(-a,b) % mp.pi
                    points.extend([root,root+mp.pi])
                return sorted(set(points))
            w = lambda theta:mp.matrix([mp.cos(theta),mp.sin(theta)])
            identity = mp.eye(2)
            def stress(norm,C=identity):
                return mp.matrix([[mp.quad(lambda theta:norm(C*w(theta))**2*(4*w(theta)[i]*w(theta)[j]-(2 if i==j else 0)),breaks(C))/mp.pi for j in range(2)] for i in range(2)])
            def density(norm,C):
                return mp.quad(lambda theta:norm(C*w(theta))**2,breaks(C))/(mp.pi*mp.det(C))
            errors = {}
            step = mp.mpf('1e-7')
            for name,norm in norms.items():
                T = stress(norm)
                direct = density(norm,A)
                inverse = A**-1
                rhs = mp.quad(lambda theta:norm(w(theta))**2/(mp.fdot(inverse*w(theta),inverse*w(theta))**2),breaks(identity))/(mp.pi*mp.det(A)**2)
                derivative = (density(norm,identity+step*B)-density(norm,identity-step*B))/(2*step)
                predicted = sum(T[i,j]*B[i,j] for i in range(2) for j in range(2))
                rotated = stress(norm,R)
                rotation_error = max(abs(v) for v in rotated-R.T*T*R)
                change_error,derivative_error = abs(direct-rhs),abs(derivative-predicted)
                require(change_error < mp.mpf('1e-24'), 'Angular change diagnostic: '+name)
                require(derivative_error < mp.mpf('1e-11'), 'First variation diagnostic: '+name)
                require(rotation_error < mp.mpf('1e-24'), 'Rotation diagnostic: '+name)
                if name in ('l1','linfty','zero'):
                    require(max(abs(v) for v in T) < mp.mpf('1e-24'), 'Balanced boundary diagnostic')
                if name == 'rank_one':
                    require(max(abs(v) for v in T-mp.matrix([[mp.mpf('2.89'),0],[0,mp.mpf('-2.89')]])) < mp.mpf('1e-24'), 'Rank-one diagnostic')
                errors[name] = {'angular_change_error':mp.nstr(change_error,12),'finite_difference_error':mp.nstr(derivative_error,12),'rotation_error':mp.nstr(rotation_error,12),'stress':[[mp.nstr(T[i,j],25) for j in range(2)] for i in range(2)]}
            return {'precision_digits':dps,'c':mp.nstr(c,30),'c_precision_string':mp.nstr(c,dps+5),'target_area':mp.nstr(target_area,30),'map_energy':mp.nstr(source_energy,30),'energy_gap_error':mp.nstr(gap_error,12),'stress_diagnostics':errors}
    values = [run(35),run(60)]
    with mp.workdps(70):
        delta = abs(mp.mpf(values[0]['c_precision_string'])-mp.mpf(values[1]['c_precision_string']))
        require(delta < mp.mpf('1e-28'), 'Cross-precision compression diagnostic')
        delta_text = mp.nstr(delta,20)
    return {'runs':values,'cross_precision_c_difference':delta_text,'cross_precision_compares':'Full working-precision decimal strings, not the 30-digit display values.',
            'tolerances':{'angular_change_and_rotation':'1e-24 absolute','finite_difference':'1e-11 absolute, step 1e-7','energy_defect':'1e-28 absolute','cross_precision_c':'1e-28 absolute'},
            'limitation':'Numerical diagnostics, not rigorous interval enclosures or proofs of quadrature error.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet', type=Path)
    p.add_argument('--output', type=Path)
    p.add_argument('--integrity-only', action='store_true')
    args = p.parse_args()
    packet = args.packet if args.packet is not None else default_packet()
    result = {'status':'PASS','problem_id':30006419,'family':'independent computational and integrity adversary','optimization_level':sys.flags.optimize,'authentication':authenticate(packet)}
    if not args.integrity_only:
        import sympy as sp
        import mpmath as mp
        require(sp.__version__ == '1.14.0' and mp.__version__ == '1.3.0', 'Use pinned independent dependencies')
        result['dependencies'] = {'sympy':sp.__version__,'mpmath':mp.__version__}
        result['exact_controls'] = exact_controls(sp)
        result['exact_control_count'] = len(result['exact_controls'])
        model_guard(sp)
        mutations = [{'name':'narrow cutoff','kwargs':{'coefficient':64}}, {'name':'wide cutoff','kwargs':{'coefficient':4}},
                     {'name':'late outer cutoff','kwargs':{'denominator':8}}, {'name':'wrong leading degree','kwargs':{'degree':5}},
                     {'name':'degree two instead of three','kwargs':{'degree':2}}, {'name':'shift bound too narrow','kwargs':{'shift_upper':sp.Rational(1,4)}},
                     {'name':'shift bound too wide','kwargs':{'shift_upper':sp.Rational(3,4)}}]
        rejected = []
        for case in mutations:
            try: model_guard(sp,**case['kwargs'])
            except RuntimeError as e: rejected.append({'name':case['name'],'rejected':True,'reason':str(e)})
            else: raise RuntimeError('Mathematical sensitivity mutant accepted: '+case['name'])
        result['mathematical_sensitivity_mutations'] = rejected
        result['numerical_controls'] = numerical_controls(mp)
    result['scope'] = 'Finite exact identities, mathematical sensitivity and numerical diagnostics, plus byte authentication. No all-competitor analytic certification, formalization, fresh proof search, source retrieval, or priority claim. Original 2/5 author approaches retained.'
    raw = json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(raw)
    print(raw,end='')


if __name__ == '__main__':
    main()
