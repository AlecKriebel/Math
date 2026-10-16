"""Root rebuild of entire sealed05 fixture and its decisive actual-read failures.

Historical candidate05 supplies immutable transport data. The selected subject
is tested separately; terminal05 is synthetic and every external service/Git
boundary is fake. This never creates production approval or invokes a service.
"""
import sys
if not sys.flags.isolated or sys.flags.optimize:
    raise RuntimeError('Use -I -B at optimization zero')
import argparse, contextlib, hashlib, io, json
from pathlib import Path

ROOT = Path('/Users/alec/Documents/Math')
P = ROOT / 'draft_pr_claimed_solved_900_1000_20261012'
A = P / 'audits/pr946_6000001'
INPUT = A / 'reviews/full_package_05'
SEAL = '4d60602995d799a0850c4657b3401ad9c353460800f1fbd752c532b73b6963b2'
ap = argparse.ArgumentParser()
ap.add_argument('--core', required=True)
ap.add_argument('--core-sha256', required=True)
ap.add_argument('--output', required=True)
ap.add_argument('--expect-defect', action='store_true')
args = ap.parse_args()
raw = (INPUT / 'MANIFEST.json').read_bytes()
assert hashlib.sha256(raw).hexdigest() == SEAL
manifest = json.loads(raw)
assert set(manifest['files']) == set(manifest['explicit_public_allowlist'])
for name, pin in manifest['files'].items():
    b = (INPUT / name).read_bytes()
    assert len(b) == pin['bytes'] and hashlib.sha256(b).hexdigest() == pin['sha256']
subject = Path(args.core).read_bytes()
assert hashlib.sha256(subject).hexdigest() == args.core_sha256
scratch = A / 'private/root_review05_closure_controls'
scratch.mkdir(parents=True, exist_ok=True)
baseline = A / 'preprint/reviewed_candidates/candidate05'

def replace(code, old, new):
    assert code.count(old) == 1, ('Unexpected fixture version', old[:90])
    return code.replace(old, new)

code = (INPUT / 'current05_controls.py').read_text()
code = replace(code, "D=A/'preprint';O=A/'reviews/full_package_05'",
               "C=A/'preprint';D=Path(baseline_path);INPUT=Path(input_path);O=Path(scratch_path)")
code = replace(code, "raw=(P/'accept_pr946.py').read_bytes();assert fp(raw)['sha256']=='62fa159687104c889195863303fa5642d877e52257bc9e4fb2bc97e89ea2b919'",
               "raw=Path(args.core).read_bytes();assert fp(raw)['sha256']==args.core_sha256")
code = replace(code, "cp(A/'OPERATIONS_INVENTORY.json',a/'OPERATIONS_INVENTORY.json');I=json.loads((a/'OPERATIONS_INVENTORY.json').read_bytes())",
               "cp(D/'OPERATIONS_INVENTORY.json',a/'OPERATIONS_INVENTORY.json');I=json.loads((a/'OPERATIONS_INVENTORY.json').read_bytes())")
code = replace(code, "for name in I['files']:cp(R/name,root/name)",
               "for name in I['files']:cp(D/'operations'/name,root/name)")
code = replace(code, "old=D/'reviewed_candidates'/f'candidate{num:02d}'",
               "old=C/'reviewed_candidates'/f'candidate{num:02d}'")
code = replace(code, "S=json.loads((O/'AUTHENTICATION_START.json').read_bytes())",
               "S=json.loads((INPUT/'AUTHENTICATION_START.json').read_bytes())")
code = replace(code, "c=json.loads((O/'COLD_REPLAY.json').read_bytes())",
               "c=json.loads((INPUT/'COLD_REPLAY.json').read_bytes())")
namespace = {'__name__':'_root_rebuilt_full05_', '__file__':str(INPUT/'current05_controls.py'),
             'args':args,'baseline_path':str(baseline),'input_path':str(INPUT),
             'scratch_path':str(scratch)}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code, str(INPUT/'current05_controls.py'), 'exec', dont_inherit=True, optimize=0), namespace)
report = namespace['out']
assert report['case_count'] == 79
assert bool(report['findings']) is args.expect_defect
if args.expect_defect:
    assert len(report['findings']) == 3
    assert {x['id'] for x in report['findings']} == {'FP05-OPS-001','FP05-OPS-002'}

# Independently re-run the three decisive descriptor/source-read controls. The
# actual source_gate and premerge_gate execute, with only exact fake transports.
late = (INPUT / 'late_refresh_controls.py').read_text()
late = replace(late, "O=Path(__file__).resolve().parent;R=Path('/Users/alec/Documents/Math')",
               "O=Path(scratch_path);INPUT=Path(input_path);R=Path('/Users/alec/Documents/Math')")
late = replace(late, "raw=(P/'accept_pr946.py').read_bytes();assert hashlib.sha256(raw).hexdigest()=='62fa159687104c889195863303fa5642d877e52257bc9e4fb2bc97e89ea2b919'",
               "raw=Path(args.core).read_bytes();assert hashlib.sha256(raw).hexdigest()==args.core_sha256")
late = late.replace("(O/'AUTHENTICATION_START.json')", "(INPUT/'AUTHENTICATION_START.json')")
late = replace(late, "N['read_regular']=hooked;N['accepted_review_check'](accepted,F,ctx);N['read_regular']=real_read;assert fired[0]","""N['read_regular']=hooked;error=None
 try:N['accepted_review_check'](accepted,F,ctx)
 except RuntimeError as caught:error=str(caught)
 finally:N['read_regular']=real_read
 assert fired[0] and ((error is None) if args.expect_defect else (error is not None)),error""")
late = replace(late, "'guard_returned':True", "'guard_returned':args.expect_defect,'closing_rejection':error")
late = replace(late, "with contextlib.redirect_stdout(io.StringIO()):N['accept'](types.SimpleNamespace(freeze=FP,review=specs),ctx)\nassert source_calls[0]==2 and acceptpath.exists() and tex.read_bytes()!=oldtex","""error=None
try:
 with contextlib.redirect_stdout(io.StringIO()):N['accept'](types.SimpleNamespace(freeze=FP,review=specs),ctx)
except RuntimeError as caught:error=str(caught)
assert source_calls[0]==2 and tex.read_bytes()!=oldtex
assert ((error is None and acceptpath.exists()) if args.expect_defect else
        (error is not None and not acceptpath.exists())),error""")
late = replace(late, "'canonical_acceptance_written':True", "'canonical_acceptance_written':args.expect_defect,'closing_rejection':error")
late_namespace = {'__name__':'_root_rebuilt_decisive05_', '__file__':str(INPUT/'late_refresh_controls.py'),
                  'args':args,'input_path':str(INPUT),'scratch_path':str(scratch)}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(late, str(INPUT/'late_refresh_controls.py'), 'exec', dont_inherit=True, optimize=0), late_namespace)
decisive = late_namespace['records']
assert len(decisive) == 3
report['cases'].extend(decisive)

if not args.expect_defect:
    # Extend the actual final source-read case to every canonical closure class,
    # including earlier historical candidate data and a sealed prior review.
    N = late_namespace['N']
    accepted, freeze, context = late_namespace['accepted'], late_namespace['F'], late_namespace['ctx']
    fa, fd, fp = late_namespace['a'], late_namespace['d'], late_namespace['p']
    acc_path = fa/'ACCEPTANCE.json'
    acc_bytes = acc_path.read_bytes()
    specs = late_namespace['specs']
    actual_source = N['source_gate']
    targets = {
        'current_freeze':fd/'FREEZE.json',
        'current_evidence':late_namespace['root']/next(iter(freeze['evidence_files'])),
        'current_core':fp/'accept_pr946.py',
        'current_inventory':fa/'OPERATIONS_INVENTORY.json',
        'latest_review_payload':fa/'reviews/full_package_05/FULL_AUDIT.md',
        'latest_review_seal':fa/'reviews/full_package_05/MANIFEST.json',
        'earlier_review_payload':fa/'reviews/full_package_01/FULL_AUDIT.md',
        'historical_tex':fd/'reviewed_candidates/candidate01/research_note.tex',
        'historical_operations':fd/'reviewed_candidates/candidate01/operations'/P.name/'accept_pr946.py',
    }
    for kind, path in targets.items():
        old = path.read_bytes()
        calls = [0]
        def source_hook(parent):
            value = actual_source(parent)
            calls[0] += 1
            if calls[0] == 2:
                path.write_bytes(old+b'\n')
            return value
        N['source_gate'] = source_hook
        acc_path.unlink()
        error = None
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                N['accept'](late_namespace['types'].SimpleNamespace(freeze=late_namespace['FP'],review=specs),context)
        except RuntimeError as caught:
            error = str(caught)
        finally:
            path.write_bytes(old)
            N['source_gate'] = actual_source
        assert calls[0] == 2 and error is not None and not acc_path.exists(), (kind,error)
        acc_path.write_bytes(acc_bytes)
        report['cases'].append({'case':'initial_accept_final_actual_source_'+kind,
                                'rejected_before_acceptance':True,'error':error})
    N['accepted_package'](context)
    report['cases'].append({'case':'restored_actual_full_chain_after_all_root_closure_cases','pass':True})
    acc_path.unlink()
    with contextlib.redirect_stdout(io.StringIO()):
        N['accept'](late_namespace['types'].SimpleNamespace(freeze=late_namespace['FP'],review=specs),context)
    approved = json.loads(acc_path.read_bytes())
    assert approved['accepted'] is True and approved['freeze_sha256'] == late_namespace['FP']
    assert approved['exact_claim'] == accepted['exact_claim']
    N['accepted_package'](context)
    report['cases'].append({'case':'valid_initial_acceptance_and_fresh_complete_readback','pass':True})
    acc_path.write_bytes(acc_bytes)

report.update(status='DEFECTS_INDEPENDENTLY_REPRODUCED' if args.expect_defect else 'PASS',
              root_control_count=len(report['cases']), subject_core_sha256=args.core_sha256,
              source_review_external_seal=SEAL,
              source_programs={name:manifest['files'][name] for name in
                               ('current05_controls.py','late_refresh_controls.py')},
              explicit_root_adaptations='Own scratch/output; immutable candidate05 transport inventory plus all4 actual sealed histories; subject core selected separately; terminal05 synthetic. New9 actual-source final-acceptance closure classes and restored full-chain positive. No production acceptance or external calls.',
              no_OS_atomic_filesystem_guarantee=True, actual_external_mutations=0)
output = Path(args.output).resolve()
assert output.parent == A and output.suffix == '.json'
output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'controls':report['root_control_count'],
                  'core_sha256':args.core_sha256,'actual_external_mutations':0}))
