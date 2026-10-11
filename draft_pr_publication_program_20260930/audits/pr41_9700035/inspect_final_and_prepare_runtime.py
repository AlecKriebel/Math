"""ROOT verifies actual final outputs before binding later administrative phases."""
from pathlib import Path
import datetime as dt
import json
import os
import subprocess
import author_root_acceptance_inputs as o

A, R, H = o.A, o.R, o.H


def clock(v):
    t = dt.datetime.fromisoformat(v[:-1]+'+00:00' if v.endswith('Z') else v)
    assert t.tzinfo is not None and t.utcoffset() == dt.timedelta(0)
    return t


def main():
    final = A / 'final_evidence_reconciliation'
    fm = o.load(final / 'FINAL_MANIFEST.json')
    assert fm['files_count'] == 2 and fm['self_excluded'] == ['FINAL_MANIFEST.json']
    o.closure(final, 'FINAL_MANIFEST.json', fm['files'], True)
    plan = o.load(A / 'ROOT_REVIEWED_FINAL_PLAN.json')
    scope = o.load(final / 'ROOT_REVIEWED_SCOPE.json')
    receipt = o.load(final / 'ROOT_FINAL_RECONCILIATION.json')
    assert o.sha((A / 'ROOT_REVIEWED_FINAL_PLAN.json').read_bytes()) == '959c3be95de3bcc4fbdd39a989a558f4f3039b8c6a1db72dbc681ee745e02a15'
    assert scope == plan and receipt['entire_scope'] == plan
    assert receipt['bindings_before'] == receipt['bindings_after'] == plan['immutable_evidence_references']
    assert receipt['actual_root_reconciliation'] is True and receipt['status'] == 'PASS'
    assert receipt['science_helpers_executed'] is False and receipt['shared_mutations'] is False
    for row in receipt['bindings_before']: o.check(R, row)
    cb = A / 'root_final_reconciliation_actual_capture'
    cap = o.load(cb / 'CAPTURE.json')
    assert cap['actual_execution'] is True and cap['completed'] is True and cap['exit_code'] == 0
    assert cap['pid'] == 35045 and cap['cwd'] == str(A) and cap['stdin_supplied'] is False
    assert clock(cap['started_utc']) <= clock(receipt['utc']) <= clock(cap['finished_utc'])
    assert (cb / 'prelaunch_source.py').read_bytes() == (H / 'seal_final_evidence.py').read_bytes()
    assert cap['source_sha256'] == '38f312eb07c2e3079d868aa315f0b7ad10884be6093ca6c54608994a659ca4ce'
    o.check(cb, cap['stdout']); o.check(cb, cap['stderr'])
    stdout = o.load(cb / cap['stdout']['path'])
    assert stdout['status'] == 'PASS'
    assert stdout['final_receipt_sha256'] == o.sha((final / 'ROOT_FINAL_RECONCILIATION.json').read_bytes())
    assert stdout['final_manifest_sha256'] == o.sha((final / 'FINAL_MANIFEST.json').read_bytes())
    assert {p.name for p in cb.iterdir()} == {'CAPTURE.json','prelaunch_source.py','stdout.bin','stderr.bin'}
    fresh = o.load(A / 'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json')
    for row in fresh['files']:
        o.check(R, row)
        assert (R / row['path']).stat().st_mode & 0o7777 == row['worktree_mode']
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip() == fresh['current_head']
    paths = {'final-plan': A/'ROOT_REVIEWED_FINAL_PLAN.json',
             'final-receipt': final/'ROOT_FINAL_RECONCILIATION.json',
             'final-manifest': final/'FINAL_MANIFEST.json',
             'reconciliation-capture': cb/'CAPTURE.json',
             'previous-mirror': A.parent/'pr40_2814/state_mirror_bindings.json',
             'previous-post': A.parent/'pr40_2814/post_acceptance_verification.json',
             'fresh-preimage': A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json',
             'root-bindings': A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json'}
    previous = o.load(paths['previous-post']); mirror = o.load(paths['previous-mirror'])
    assert previous['status'] == 'PASS' and previous['targets'] == 31 and previous['primary_acceptances'] == 30
    assert len(mirror['entries']) == 30 and 40 in mirror['required_completed_prs'] and 41 not in mirror['required_completed_prs']
    runtime = {'schema':'root-pr41-actual-runtime-pins/v1',
               'preparation_manifest_sha256':o.PREP,
               'inputs': {k: o.pin(p) for k,p in paths.items()}}
    runtime_path = o.dump('ROOT_ACCEPTANCE_RUNTIME_INPUTS.json',runtime)
    result = {'schema':'pr41-root-actual-final-output-inspection/v1',
              'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),
              'status':'PASS','entire_final_scope':scope,'entire_final_receipt':receipt,
              'entire_actual_final_capture':cap,'final_manifest':o.pin(final/'FINAL_MANIFEST.json'),
              'fresh_native13_and_HEAD_unchanged':True,'runtime_inputs':o.pin(runtime_path),
              'science_helpers_executed':False,'native_or_Git_mutations':False}
    o.dump('ROOT_ACTUAL_FINAL_OUTPUT_INSPECTION.json',result)
    print(json.dumps({'status':'PASS','actual_pid':os.getpid(),
                      'runtime_inputs':o.pin(runtime_path),'final_manifest':o.pin(final/'FINAL_MANIFEST.json')},sort_keys=True))


if __name__ == '__main__': main()
