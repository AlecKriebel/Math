#!/usr/bin/env python3
"""Independent hostile-integrity and finite mathematical controls, not a theorem verifier."""
import hashlib
import importlib.util
import itertools
import json
import math
import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile

HERE = Path(__file__).absolute().parent
spec = importlib.util.spec_from_file_location('independent_packet_guard', HERE/'PACKET_GUARD.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def need(value, message):
    if not value:
        raise RuntimeError(message)


def env(inherited=False):
    out = {k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
    out['PYTHONDONTWRITEBYTECODE'] = '1'
    if inherited:
        out['PYTHONOPTIMIZE'] = '2'
    return out


def invoke(python, flags, command, cwd, inherited=False):
    return subprocess.run([python, *flags, *command], cwd=cwd, env=env(inherited),
                          capture_output=True, timeout=60)


def modes():
    return [('normal', ['-I','-B'], False), ('-O', ['-I','-B','-O'], False),
            ('-OO', ['-I','-B','-OO'], False), ('inherited_PYTHONOPTIMIZE_2', ['-B'], True)]


def hostile_controls(packet, snapshot, scratch, python):
    rows = []
    entrypoints = ['public/controls.py', 'public/verify_packet.py', 'PORTABLE_INDEPENDENT.py',
                   'VERIFY_PUBLICATION.py', 'TEST_MUTATIONS.py', 'audit_b/independent_controls.py']
    cases = ['clean', *['changed_code:'+p for p in entrypoints], 'assert_false_payload', 'proof_and_outer_rebound',
             'missing', 'extra_file', 'extra_empty_directory', 'file_mode', 'directory_mode',
             'file_symlink', 'directory_symlink', 'root_symlink', 'ancestor_symlink',
             'dot_component', 'double_slash', 'parent_component', 'fifo', 'socket']
    for label, flags, inherited in modes():
        with tempfile.TemporaryDirectory(prefix='marker-positive-', dir=scratch) as temporary:
            marker = Path(temporary)/'marker'
            command = 'from pathlib import Path; Path('+repr(str(marker))+').write_text("executed")'
            cp = invoke(python, flags, ['-c', command], temporary, inherited)
            need(cp.returncode == 0 and marker.read_text() == 'executed', 'marker positive failed')
        for case in cases:
            with tempfile.TemporaryDirectory(prefix='hostile-', dir=scratch) as temporary:
                work = Path(temporary); root = work/'packet'; shutil.copytree(packet, root)
                g.authenticate(str(root), snapshot)
                marker = work/'UNEXPECTED_EXECUTION'
                path_arg = str(root); entrypoint = 'public/controls.py'; sock = None
                try:
                    if case.startswith('changed_code:'):
                        entrypoint = case.split(':', 1)[1]
                        (root/entrypoint).write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\nprint("{}")\n')
                    elif case == 'assert_false_payload':
                        (root/entrypoint).write_text('assert False, "untrusted false assertion"\nfrom pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\n')
                    elif case == 'proof_and_outer_rebound':
                        proof = root/'public/PROOF.md'; proof.write_bytes(proof.read_bytes()+b'\nAltered claim.\n')
                        outer = g.strict_json((root/'PUBLICATION_MANIFEST.json').read_bytes())
                        for item in outer['files']:
                            if item['path'] == 'public/PROOF.md':
                                item['sha256'] = g.sha(proof.read_bytes()); item['bytes'] = proof.stat().st_size
                        (root/'PUBLICATION_MANIFEST.json').write_text(json.dumps(outer))
                    elif case == 'missing': (root/'audit_a/CONTROL_REPLAY.json').unlink()
                    elif case == 'extra_file': (root/'hidden.py').write_text('extra')
                    elif case == 'extra_empty_directory': (root/'public/empty').mkdir()
                    elif case == 'file_mode': (root/'public/PROOF.md').chmod(0o600)
                    elif case == 'directory_mode': (root/'audit_a').chmod(0o700)
                    elif case == 'file_symlink':
                        path = root/'public/controls.py'; path.unlink(); path.symlink_to(packet/'public/controls.py')
                    elif case == 'directory_symlink':
                        path = root/'audit_a'; moved = work/'audit_a'; path.rename(moved); path.symlink_to(moved, target_is_directory=True)
                    elif case == 'root_symlink':
                        link = work/'alias'; link.symlink_to(root, target_is_directory=True); path_arg = str(link)
                    elif case == 'ancestor_symlink':
                        alias = work/'alias'; alias.symlink_to(work, target_is_directory=True); path_arg = str(alias/'packet')
                    elif case == 'dot_component': path_arg = str(work)+'/./packet'
                    elif case == 'double_slash': path_arg = str(work)+'//packet'
                    elif case == 'parent_component': path_arg = str(root)+'/../packet'
                    elif case == 'fifo':
                        path = root/'public/controls.py'; path.unlink(); os.mkfifo(path)
                    elif case == 'socket':
                        path = root/'public/controls.py'; path.unlink(); sock = socket.socket(socket.AF_UNIX)
                        prior_directory = os.getcwd()
                        try:
                            os.chdir(work)
                            sock.bind('packet/public/controls.py')
                        finally:
                            os.chdir(prior_directory)
                    cp = invoke(python, flags, [str(HERE/'GUARDED_RUN.py'), '--packet', path_arg, '--entrypoint', entrypoint], work, inherited)
                    expected = 0 if case == 'clean' else 42
                    need(cp.returncode == expected, label+'/'+case+' unexpected return: '+cp.stderr.decode(errors='replace'))
                    need(not marker.exists(), label+'/'+case+' executed untrusted marker')
                    if expected:
                        need(cp.stdout == b'' and cp.stderr.startswith(b'GUARD_REJECT:'), 'not controlled guard rejection')
                    else:
                        need(cp.stdout == (root/'public/CONTROL_RESULTS.json').read_bytes(), 'guard clean diagnostics changed')
                    rows.append({'mode': label, 'case': case, 'returncode': cp.returncode,
                                 'untrusted_marker_executed': False, 'stdout_sha256': g.sha(cp.stdout),
                                 'controlled_rejection': bool(expected)})
                finally:
                    if sock is not None: sock.close()
    return rows


def standalone_boundaries(packet, snapshot, scratch, python):
    rows = []
    def authenticate_executed_code(root):
        for name, record in snapshot['files'].items():
            if name.endswith('.py'):
                raw = g.regular(root/name)
                need(len(raw) == record['bytes'] and g.sha(raw) == record['sha256'], 'direct probe copied code differs: '+name)
    # These tests deliberately omit the all-29 gate to identify a direct-script limit.
    # The executing checker remains the authenticated original; changed metadata is data.
    with tempfile.TemporaryDirectory(prefix='direct-', dir=scratch) as temporary:
        work = Path(temporary); root = work/'packet'; shutil.copytree(packet, root)
        g.authenticate(str(root), snapshot)
        sm = g.strict_json((root/'public/SOURCE_METADATA.json').read_bytes())
        sm['sources'][0]['bytes'] = True
        sm['sources'][0]['sha256'] = 'unsupported witness'
        (root/'public/SOURCE_METADATA.json').write_text(json.dumps(sm))
        authenticate_executed_code(root)
        cp = invoke(python, ['-I','-B'], [str(root/'PORTABLE_INDEPENDENT.py'), '--packet-root', str(root)], work)
        need(cp.returncode == 0, 'portable direct boundary probe failed unexpectedly')
        result = g.strict_json(cp.stdout)
        need(result['pass'] is True and result['source_pins'][0]['bytes'] is True and
             result['source_pins'][0]['sha256'] == 'unsupported witness', 'portable witness probe not observed')
        rows.append({'case': 'portable_direct_unauthenticated_source_metadata', 'returncode': cp.returncode,
                     'observed': 'reports pass and echoes boolean bytes/unsupported hash with sources explicitly not run',
                     'full_fixed_packet_guard_rejects': True})
        try: g.authenticate(str(root), snapshot)
        except g.Rejected: pass
        else: raise RuntimeError('guard accepted unauthenticated source metadata')
    with tempfile.TemporaryDirectory(prefix='ancestor-', dir=scratch) as temporary:
        work = Path(temporary); root = work/'packet'; shutil.copytree(packet, root)
        g.authenticate(str(root), snapshot)
        alias = work/'alias'; alias.symlink_to(work, target_is_directory=True)
        authenticate_executed_code(root)
        cp = invoke(python, ['-I','-B'], [str(root/'VERIFY_PUBLICATION.py'), '--packet', str(alias/'packet'),
                    '--expected-manifest', g.OUTER_PIN, '--check-only'], work)
        need(cp.returncode == 0, 'legacy ancestor probe differed')
        rows.append({'case': 'legacy_full_gate_symlink_ancestor', 'returncode': 0,
                     'observed': 'authentic packet accepted through a symbolic ancestor',
                     'changed_payload_accepted': False, 'current_guard_rejects': True})
    # JSON parser probes run the frozen parser from an authenticated copy, without package mutation.
    with tempfile.TemporaryDirectory(prefix='parser-', dir=scratch) as temporary:
        work = Path(temporary); root = work/'packet'; shutil.copytree(packet, root)
        g.authenticate(str(root), snapshot)
        authenticate_executed_code(root)
        command = ('import json,math,runpy; ns=runpy.run_path('+repr(str(root/'VERIFY_PUBLICATION.py'))+'); '
                   'value=ns["load_json"](b\'{"value":1e999}\'); print(json.dumps({"overflow_is_infinite":math.isinf(value["value"])}))')
        cp = invoke(python, ['-I','-B'], ['-c', command], work)
        need(cp.returncode == 0 and g.strict_json(cp.stdout)['overflow_is_infinite'] is True, 'legacy overflow parser probe differed')
        rows.append({'case': 'legacy_json_overflow_parser', 'observed': '1e999 parses as infinity',
                     'frozen_manifest_contains_overflow': False, 'current_parser_rejects': True})
    for raw in [b'{"x":NaN}', b'{"x":Infinity}', b'{"x":-Infinity}', b'{"x":1e999}', b'{"x":1,"x":2}', b'{']:
        try: g.strict_json(raw)
        except g.Rejected: pass
        else: raise RuntimeError('current strict JSON accepted '+repr(raw))
    need(not g.typed_equal({'x':1}, {'x':True}) and not g.typed_equal([1], [1.0]), 'typed equality merged numeric types')
    return rows


def optimization_controls(python, scratch):
    rows = []
    for label, flags, inherited in modes():
        command = ('import json,os,subprocess,sys; '
                   'e={k:v for k,v in os.environ.items() if not k.startswith("PYTHON")}; '
                   'c=subprocess.run([sys.executable,"-I","-B","-c","import sys; print(sys.flags.optimize)"],capture_output=True,env=e,check=True); '
                   'print(json.dumps({"parent":sys.flags.optimize,"child":int(c.stdout),"debug":__debug__}))')
        cp = invoke(python, flags, ['-c', command], scratch, inherited)
        need(cp.returncode == 0, 'optimization parent probe failed')
        obj = g.strict_json(cp.stdout)
        expected = 0 if label == 'normal' else 1 if label == '-O' else 2
        need(obj['parent'] == expected and obj['child'] == 0 and obj['debug'] is (expected == 0), 'optimization isolation mismatch')
        failure = invoke(python, flags, ['-c', 'raise RuntimeError("deliberate explicit negative")'], scratch, inherited)
        need(failure.returncode != 0 and b'deliberate explicit negative' in failure.stderr,
             'explicit failure disappeared under optimization')
        rows.append({'mode': label, 'parent_optimization': obj['parent'], 'isolated_unflagged_child_optimization': obj['child'],
                     'explicit_failure_active': True, 'assert_false_used': False})
    return rows


def readonly_controls(packet, snapshot, scratch, python):
    with tempfile.TemporaryDirectory(prefix='readonly-control-',dir=scratch) as temporary:
        work=Path(temporary); root=work/'packet'; shutil.copytree(packet,root)
        g.authenticate(str(root),snapshot)
        for path in root.rglob('*'): path.chmod(0o555 if path.is_dir() else 0o444)
        root.chmod(0o555)
        try:
            before=g.authenticate(str(root),snapshot,'readonly')
            rejected=[]
            for path in [root/'unpermitted_new_file',root/'public/PROOF.md']:
                try:
                    with path.open('ab'): pass
                except PermissionError: rejected.append(True)
                else: rejected.append(False)
            need(rejected==[True,True],'read-only controls require an unprivileged account with denied writes')
            rows=[]
            for entry,args in [('VERIFY_PUBLICATION.py',['--packet',str(root),'--expected-manifest',g.OUTER_PIN,'--check-only','--filesystem-profile','readonly']),
                               ('public/verify_packet.py',['--manifest-sha256','1cd8291f2025524b351c5cc3cb5780b35ba5fa4c4afde78c6e288daddd350e9f'])]:
                g.authenticate(str(root),snapshot,'readonly')
                cp=invoke(python,['-I','-B'],[str(root/entry),*args],work)
                need(cp.returncode==0 and cp.stderr==b'','read-only original entry point failed')
                need(g.typed_equal(before,g.authenticate(str(root),snapshot,'readonly')),'read-only input changed')
                rows.append({'entrypoint':entry,'returncode':0,'stdout_sha256':g.sha(cp.stdout),'all_29_readonly_authenticated':True})
            return {'write_probes_denied':2,'uid':os.geteuid(),'all_29_unchanged':True,'runs':rows,
                    'OS_sandbox_claimed':False}
        finally:
            root.chmod(0o755)
            for path in root.rglob('*'): path.chmod(0o755 if path.is_dir() else 0o644)


def comparator_controls(packet):
    spec = importlib.util.spec_from_file_location('independent_release_gate', HERE/'RELEASE_GATE.py')
    gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
    historical = g.strict_json(g.regular(packet/'audit_b/INDEPENDENT_CONTROL_RESULTS.json'))
    historical['counts'].pop('source_pin'); historical['total_checks'] -= 9
    historical['source_verification'] = 'NOT_RUN_NO_SEPARATELY_SUPPLIED_SOURCES'
    clone = lambda value: g.strict_json(json.dumps(value).encode())
    actual = clone(historical); actual['numeric_max_jacobi_error'] = 1.5367479511141369e-10
    need(gate.compare_independent(actual,historical)['all_other_keys_types_values_exact'], 'one-field positive comparator control')
    rows = []
    for label in ['theorem_flag', 'count_value', 'count_type', 'status_type', 'proof_hash', 'other_numerical_diagnostic',
                  'source_witness_type', 'extra_key', 'missing_key', 'integer_diagnostic', 'boolean_diagnostic',
                  'negative_diagnostic', 'nan_diagnostic', 'infinite_diagnostic', 'bound_equality', 'above_bound',
                  'historical_bound_equality', 'historical_integer_diagnostic']:
        changed = clone(actual); old = clone(historical)
        if label == 'theorem_flag': changed['analytic_proof_certified_by_computation'] = True
        elif label == 'count_value': changed['counts']['edge_arclength_numeric'] = 0
        elif label == 'count_type': changed['total_checks'] = 4137.0
        elif label == 'status_type': changed['pass'] = 1
        elif label == 'proof_hash': changed['proof_sha256'] = '0'*64
        elif label == 'other_numerical_diagnostic': changed['numeric_max_edge_error'] += 1e-16
        elif label == 'source_witness_type': changed['source_pins'][0]['bytes'] = True
        elif label == 'extra_key': changed['extra'] = False
        elif label == 'missing_key': changed.pop('counts')
        elif label == 'integer_diagnostic': changed['numeric_max_jacobi_error'] = 0
        elif label == 'boolean_diagnostic': changed['numeric_max_jacobi_error'] = False
        elif label == 'negative_diagnostic': changed['numeric_max_jacobi_error'] = -1e-20
        elif label == 'nan_diagnostic': changed['numeric_max_jacobi_error'] = math.nan
        elif label == 'infinite_diagnostic': changed['numeric_max_jacobi_error'] = math.inf
        elif label == 'bound_equality': changed['numeric_max_jacobi_error'] = 3e-7
        elif label == 'above_bound': changed['numeric_max_jacobi_error'] = 3.1e-7
        elif label == 'historical_bound_equality': old['numeric_max_jacobi_error'] = 3e-7
        elif label == 'historical_integer_diagnostic': old['numeric_max_jacobi_error'] = 0
        try: gate.compare_independent(changed,old)
        except g.Rejected: pass
        except Exception as error:
            # Each independently loaded module owns its own Rejected class.
            need(type(error).__name__ == 'Rejected', 'uncontrolled comparator exception')
        else: raise RuntimeError('bounded comparator accepted '+label)
        rows.append({'case':label, 'rejected':True})
    return {'positive_disclosed_drift_accepted':True, 'negative_cases':rows, 'negative_count':len(rows),
            'any_other_field_exception_allowed':False}


def finite_math_controls():
    counts = {}; witness = {}
    def check(category, value):
        need(value, 'independent math control: '+category)
        counts[category] = counts.get(category, 0) + 1
    # Exact integer-complex operations: these products use no floating division.
    C = [((0,-1j),(-1j,0)), ((0,-1),(1,0)), ((-1j,0),(0,1j))]
    I = ((1,0),(0,1)); Z = ((0,0),(0,0))
    def mul(A,B): return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    def add(A,B): return tuple(tuple(A[i][j]+B[i][j] for j in range(2)) for i in range(2))
    def scale(t,A): return tuple(tuple(t*x for x in row) for row in A)
    check('pauli_volume',mul(mul(C[0],C[1]),C[2]) == scale(-1,I))
    for j,k in itertools.product(range(3), repeat=2):
        check('pauli_basis_anticommutator',add(mul(C[j],C[k]),mul(C[k],C[j])) == (scale(-2,I) if j == k else Z))
    # A nonzero actual intertwiner for a half-turn, and its wrong-sign countercheck.
    A = C[2]; signs = [-1,-1,1]
    for j in range(3):
        check('intertwiner_positive',mul(scale(signs[j],C[j]),A) == mul(A,C[j]))
    check('intertwiner_wrong_sign_negative',mul(C[0],A) != mul(A,C[0]))
    check('positive_branch_identity',scale(-1,mul(mul(C[2],I),C[2])) == I)
    check('antipodal_branch_negative',scale(-1,mul(mul(C[2],I),scale(-1,C[2]))) == scale(-1,I))
    for theta in [0.0,1e-10,.2,.8,math.pi/2-1e-10]:
        for t in [0.,.01,.3,.7,1.]:
            ratio = t if theta == 0 else math.sin(t*theta)/math.sin(theta)
            check('spherical_hemisphere_endpoint',0 <= ratio <= 1+1e-14 and 0 <= t <= 1)
    outside = math.sin(1.4)/math.sin(2.8)
    check('spherical_nonhemisphere_negative',outside > 2.9)
    check('same_linear_weights_negative',math.sin(1.3)/math.sin(2.6) > 1.8)
    for ell in [1,2,4,8,16,32,64]:
        planar = 2*math.pi/ell
        check('logarithmic_planar_rate',planar > 0 and abs(planar*ell-2*math.pi) < 1e-14)
        check('critical_trace_exponents',1/2+2/4 == 1)
    check('nonlogarithmic_cutoff_negative',3*math.pi/4 > 2)
    witness.update(nonhemisphere_expansion=outside, same_weight_endpoint_expansion=math.sin(1.3)/math.sin(2.6),
                   linear_width_planar_squared_L2=3*math.pi/4)

    # Square pyramid: five actual facets, a four-facet apex, and nonadjacent
    # opposite side facets meeting only at that apex. All incidence arithmetic is integer.
    raw_normals = [(1,0,1),(-1,0,1),(0,1,1),(0,-1,1),(0,0,-1)]
    raw_heights = [1,1,1,1,1]
    vertices = [(0,0,1),(-2,-2,-1),(-2,2,-1),(2,-2,-1),(2,2,-1)]
    dot = lambda a,b:sum(x*y for x,y in zip(a,b))
    norm = lambda a:math.sqrt(dot(a,a))
    incidence = [[dot(v,n) == h for n,h in zip(raw_normals,raw_heights)] for v in vertices]
    check('pyramid_exact_incidence', [sum(row) for row in incidence] == [4,3,3,3,3])
    for J in [(0,1),(2,3)]:
        check('nonadjacent_pair_vertex_only',[k for k,row in enumerate(incidence) if all(row[j] for j in J)] == [0])
    for J in itertools.combinations(range(5),3):
        check('pyramid_triples_at_most_vertex',sum(all(row[j] for j in J) for row in incidence) <= 1)
    normals = [tuple(x/norm(n) for x in n) for n in raw_normals]
    heights = [h/norm(n) for h,n in zip(raw_heights,raw_normals)]
    # Independent quadrature of the actual infinitely flat double-integral bump.
    # Composite Simpson is a diagnostic, not interval-certified integration.
    def primitive(a):
        if a <= 0: return 0.
        n = 128; step = a/n
        def value(t): return 0. if t == 0 else (a-t)*math.exp(-1/t)
        return step/3*(value(0)+value(a)+sum((4 if k%2 else 2)*value(k*step) for k in range(1,n)))
    normalization = primitive(2.)
    def phi(s): return primitive(s+2)/normalization
    check('pyramid_bump_normalization',abs(phi(0)-1)<1e-14 and phi(-2)==0)
    many = 0; nonadjacent = 0; max_radial = 0.; max_vertex = 0.; samples = 0
    for lam in [100.,1000.,10000.]:
        rays = list(vertices)+[(.25,.5,.75),(-.4,.3,-.7),(1.,1.,0.)]
        rays += [(a/lam,b/lam,1.) for a,b in itertools.product([-.7,0.,.7],repeat=2)]
        for ray in rays:
            d = tuple(x/norm(ray) for x in ray)
            rout = min(h/dot(n,d) for n,h in zip(normals,heights) if dot(n,d)>0)
            low, high = 0., rout
            for _ in range(52):
                mid = (low+high)/2
                value = sum(phi(lam*(mid*dot(n,d)-h)) for n,h in zip(normals,heights))
                if value <= 1: low = mid
                else: high = mid
            r = (low+high)/2; x = tuple(r*t for t in d)
            active = [j for j,(n,h) in enumerate(zip(normals,heights)) if dot(n,x)-h > -2/lam]
            common = [k for k,row in enumerate(incidence) if all(row[j] for j in active)]
            check('pyramid_actual_level_sample',abs(sum(phi(lam*(dot(n,x)-h)) for n,h in zip(normals,heights))-1)<1e-8)
            check('pyramid_active_common_face',bool(active) and bool(common))
            check('pyramid_radial_displacement',0 <= lam*(rout-r) < 10)
            max_radial = max(max_radial,lam*(rout-r))
            if len(active)>=3:
                many += 1; dist = min(norm(tuple(a-b for a,b in zip(x,v))) for v in vertices)
                check('pyramid_vertex_localization_sample',lam*dist<10)
                max_vertex = max(max_vertex,lam*dist)
            if (0 in active and 1 in active) or (2 in active and 3 in active):
                nonadjacent += 1
                check('pyramid_nonadjacent_localization',lam*norm(tuple(a-b for a,b in zip(x,vertices[0])))<10)
            y = tuple(rout*t for t in d); q = tuple(t/norm(y) for t in y)
            for j in active: check('pyramid_radial_hemisphere',dot(q,normals[j])>0)
            samples += 1
    check('pyramid_many_active_present',many > 20 and nonadjacent > 20)
    witness.update(square_pyramid_samples=samples, square_pyramid_many_active=many,
                   square_pyramid_nonadjacent_active=nonadjacent, square_pyramid_max_lambda_radial_shift=max_radial,
                   square_pyramid_max_lambda_vertex_distance=max_vertex,
                   square_pyramid_bump_quadrature='128-panel composite Simpson; finite diagnostic only')
    return {'counts':counts, 'total_checks':sum(counts.values()), 'witnesses':witness,
            'analytic_theorem_certified':False, 'universal_localization_certified':False,
            'actual_boundary_L2_or_Dirac_index_certified':False}


def run(packet, snapshot, scratch, python):
    hostile = hostile_controls(packet, snapshot, scratch, python)
    boundaries = standalone_boundaries(packet, snapshot, scratch, python)
    optimization = optimization_controls(python, scratch)
    readonly = readonly_controls(packet,snapshot,scratch,python)
    comparison = comparator_controls(packet)
    mathematics = finite_math_controls()
    return {'summary': {'hostile_cases':len(hostile), 'clean_acceptances':sum(r['returncode']==0 for r in hostile),
                        'guard_rejections':sum(r['returncode']==42 for r in hostile),
                        'marker_positive_modes':4, 'untrusted_markers_executed':0,
                        'standalone_boundary_witnesses':len(boundaries), 'bounded_comparator_negative_cases':comparison['negative_count'],
                        'readonly_write_probes_denied':readonly['write_probes_denied'],
                        'mathematical_finite_checks':mathematics['total_checks']},
            'hostile':hostile, 'standalone_boundaries':boundaries, 'optimization':optimization,
            'bounded_comparator':comparison, 'readonly':readonly, 'finite_mathematics':mathematics}
