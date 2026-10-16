"""Root reproductions and repairs of sealed review04's workflow controls.

The externally sealed46-case program supplies the independently authored
full-directory fixture. Adaptations below are explicit: own scratch/output,
immutable candidate04 baseline, selected subject code, repaired expectations,
and12 additional root service-read injections. All terminal proof verdicts
and service/Git transport data are synthetic. No production action is called.
"""
import sys
if not sys.flags.isolated or sys.flags.optimize:
    raise RuntimeError('Use Python -I -B without optimization')
import argparse, contextlib, copy, hashlib, io, json
from pathlib import Path

ROOT = Path('/Users/alec/Documents/Math')
P = ROOT / 'draft_pr_claimed_solved_900_1000_20261012'
A = P / 'audits/pr946_6000001'
INPUT = A / 'reviews/full_package_04'
SEAL = '7fb99b465473a17ad54a363c4ee6f410023b3857343a5df2c356a705d50180d0'
parser = argparse.ArgumentParser()
parser.add_argument('--core', required=True)
parser.add_argument('--core-sha256', required=True)
parser.add_argument('--output', required=True)
parser.add_argument('--expect-defect', action='store_true')
args = parser.parse_args()
baseline = A / 'preprint/reviewed_candidates/candidate04'
manifest_raw = (INPUT / 'MANIFEST.json').read_bytes()
assert hashlib.sha256(manifest_raw).hexdigest() == SEAL
manifest = json.loads(manifest_raw)
assert set(manifest['files']) == set(manifest['explicit_public_allowlist'])
for name, want in manifest['files'].items():
    raw = (INPUT / name).read_bytes()
    assert len(raw) == want['bytes'] and hashlib.sha256(raw).hexdigest() == want['sha256']
subject = Path(args.core).read_bytes()
assert hashlib.sha256(subject).hexdigest() == args.core_sha256
code = (INPUT / 'action_chain_controls.py').read_text()
source_program_pin = manifest['files']['action_chain_controls.py']['sha256']
scratch = A / 'private/root_review04_canonical_controls'
(scratch / 'private').mkdir(parents=True, exist_ok=True)
def replace(old, new):
    global code
    assert code.count(old) == 1, ('unexpected fixture source', old[:70])
    code = code.replace(old, new)
replace("D=A/'preprint';O=A/'reviews/full_package_04';F=",
        "C=A/'preprint';D=Path(baseline_path);I=A/'reviews/full_package_04';O=Path(scratch_path);F=")
replace("b=(P/'accept_pr946.py').read_bytes();assert fp(b)['sha256']=='0ac1335d4703638002392802a37db43fa0307561a8052b54b98f47c955094591'",
        "b=Path(args.core).read_bytes();assert fp(b)['sha256']==args.core_sha256")
replace("cp(A/'OPERATIONS_INVENTORY.json',a/'OPERATIONS_INVENTORY.json');op=json.loads((A/'OPERATIONS_INVENTORY.json').read_bytes())",
        "cp(D/'OPERATIONS_INVENTORY.json',a/'OPERATIONS_INVENTORY.json');op=json.loads((D/'OPERATIONS_INVENTORY.json').read_bytes())")
replace("for name in op['files']:cp(R/name,root/name)",
        "for name in op['files']:cp(D/'operations'/name,root/name)")
replace("old=D/'reviewed_candidates'/f'candidate{number:02d}'",
        "old=C/'reviewed_candidates'/f'candidate{number:02d}'")
replace("S=json.loads((O/'AUTHENTICATION_START.json').read_bytes())",
        "S=json.loads((I/'AUTHENTICATION_START.json').read_bytes())")
replace("c=json.loads((O/'COLD_REPLAY.json').read_bytes())",
        "c=json.loads((I/'COLD_REPLAY.json').read_bytes())")
if not args.expect_defect:
    start = code.index("  else:\n   assert error is None and (early if recovering else completed and after['active_pr']==947),(kind,window,error)")
    end = code.index('\n  late.append(row)', start)
    code = code[:start] + """  else:
   assert error is not None and 'EXTERNAL BOUNDARY FORBIDDEN' not in error and not early and after==state,(kind,window,error)
   row={'case':window+'_'+kind,'rejected_before_completion':True,'error':error[:250]}
""".rstrip() + code[end:]
    start = code.index("with contextlib.redirect_stdout(io.StringIO()):N['merge'](types.SimpleNamespace(),ctx)\nassert dispatch==")
    end = code.index("\n(a/'ACCEPTANCE.json').write_bytes(original_acceptance)", start)
    code = code[:start] + """error=None
try:
 with contextlib.redirect_stdout(io.StringIO()):N['merge'](types.SimpleNamespace(),ctx)
except RuntimeError as caught:error=str(caught)
assert error is not None and 'canonical acceptance changed' in error and dispatch==[['gh','pr','ready']],(error,dispatch)
late.append({'case':'accepted_revocation_during_ready_before_merge','rejected_before_merge':True,'fake_dispatches':dispatch,'error':error})
""".rstrip() + code[end:]
code = code[:code.index("\n(O/'ACTION_CHAIN_CONTROLS.json').write_bytes(enc(report))")]
namespace = {'__name__': '_root_rebuilt_review04_fixture_', '__file__': __file__,
             'args': args, 'baseline_path': str(baseline), 'scratch_path': str(scratch)}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code, str(INPUT / 'action_chain_controls.py'), 'exec', dont_inherit=True, optimize=0), namespace)
report = namespace['report']
if not args.expect_defect:
    N = namespace['N']
    accepted, freeze, context = namespace['accepted'], namespace['freeze'], namespace['ctx']
    actual_original, actual_review = N['original_check'], N['review_check']
    actual_load = N['load']
    fixture_a, fixture_d, fixture_p = namespace['a'], namespace['d'], namespace['p']
    targets = {
        'accepted_revocation': fixture_a / 'ACCEPTANCE.json',
        'accepted_theorem': fixture_a / 'ACCEPTANCE.json',
        'current_freeze': fixture_d / 'FREEZE.json',
        'current_tex': fixture_d / 'research_note.tex',
        'operation_core': fixture_p / 'accept_pr946.py',
        'operations_inventory': fixture_a / 'OPERATIONS_INVENTORY.json'}
    for boundary in ('original_source_read', 'full_review_chain_read'):
        for kind, path in targets.items():
            original_raw = path.read_bytes()
            injected = [False]
            def inject():
                if injected[0]:
                    return
                injected[0] = True
                if kind.startswith('accepted_'):
                    value = json.loads(original_raw)
                    value['accepted' if kind == 'accepted_revocation' else 'exact_claim'] = False if kind == 'accepted_revocation' else 'WITHDRAWN synthetic theorem'
                    path.write_bytes((json.dumps(value, indent=2) + '\n').encode())
                else:
                    path.write_bytes(original_raw + b'\n')
            def original_hook(*pos, **kw):
                value = actual_original(*pos, **kw)
                if boundary == 'original_source_read':
                    inject()
                return value
            def review_hook(*pos, **kw):
                value = actual_review(*pos, **kw)
                if boundary == 'full_review_chain_read':
                    inject()
                return value
            N['original_check'], N['review_check'] = original_hook, review_hook
            error = None
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    N['accepted_review_check'](accepted, freeze, context)
            except RuntimeError as caught:
                error = str(caught)
            finally:
                path.write_bytes(original_raw)
                N['original_check'], N['review_check'] = actual_original, actual_review
            assert injected[0] and error is not None and 'EXTERNAL BOUNDARY FORBIDDEN' not in error, (kind, boundary, error)
            report['cases'].append({'case': boundary + '_' + kind, 'rejected': True,
                                    'error': error, 'actual_full_current_capture_and_shared_guard': True})
    with contextlib.redirect_stdout(io.StringIO()):
        N['accepted_review_check'](accepted, freeze, context)
    report['cases'].append({'case': 'restored_full_chain_positive_after_all_service_read_injections', 'passed': True})
report.update(status='DEFECT_REPRODUCED' if args.expect_defect else 'PASS',
              control_count=len(report['cases']), source_program_sha256=source_program_pin,
              subject_core_sha256=args.core_sha256,
              root_fixture_adaptations='Externally sealed46-case fixture rebuilt in root own scratch using immutable candidate04 transport inventory/data; subject core selected separately. New12 deterministic source/history-read drift injections plus final restored positive guard. All external boundaries fake, terminal verdict synthetic; not a production acceptance.',
              interpretation='Nine old failures reproduced.' if args.expect_defect else 'All old46 cases plus12 root source/history-read injections and final positive full-chain guard pass; no OS-atomicity claim.')
output = Path(args.output)
assert output.parent == A and output.suffix == '.json'
output.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'status': report['status'], 'controls': report['control_count'],
                  'core_sha256': args.core_sha256, 'external_actions': 0}))
