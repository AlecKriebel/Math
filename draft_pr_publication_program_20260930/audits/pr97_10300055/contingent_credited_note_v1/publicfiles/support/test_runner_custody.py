#!/usr/bin/env python3
"""Test output-boundary and failure-receipt custody using synthetic children."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

def sha(data):
    return hashlib.sha256(data).hexdigest()

def inventory(root):
    return {p.relative_to(root).as_posix(): sha(p.read_bytes())
            for p in root.rglob('*') if p.is_file()}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', required=True)
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    output = Path(args.output_dir).expanduser().resolve(strict=False)
    if output == root or root in output.parents:
        raise ValueError('Custody controls must be outside the package')
    output.mkdir(parents=True, exist_ok=True)
    before = inventory(root)
    records = []
    def invoke(label, script, arguments, optimized):
        command = [sys.executable, '-E', '-B'] + (['-O'] if optimized else [])
        command += [str(script)] + arguments
        start = dt.datetime.now(dt.timezone.utc).isoformat()
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        record = dict(label=label, optimized=optimized, command=command, pid=proc.pid,
                      started_utc=start, finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                      exit_code=proc.returncode, stdout=out.decode(errors='replace'),
                      stderr=err.decode(errors='replace'), stdout_sha256=sha(out),
                      stderr_sha256=sha(err), script_sha256=sha(script.read_bytes()))
        records.append(record)
        (output/'PROCESS_RECEIPTS.json').write_text(json.dumps(records, indent=2)+'\n')
        return record
    alias = output/'outside_named_alias'
    alias.symlink_to(root, target_is_directory=True)
    for optimized in (False, True):
        r = invoke('diagnostic_output_ancestor_symlink', root/'support/run_diagnostics.py',
                   ['--output-dir', str(alias/'must_not_be_created')], optimized)
        if r['exit_code'] == 0 or 'Choose an output directory outside the closed package' not in r['stderr']:
            raise RuntimeError('Diagnostic runner failed output-boundary rejection')
        r = invoke('integrity_output_ancestor_symlink', root/'support/test_integrity.py',
                   ['--archive', str(Path(args.archive).absolute()),
                    '--output-dir', str(alias/'must_not_be_created')], optimized)
        if r['exit_code'] == 0 or 'Controls must be outside the closed package' not in r['stderr']:
            raise RuntimeError('Integrity runner failed output-boundary rejection')
    alias.unlink()
    good_fixture = ('import json\n'
                    'def ck(name, value):\n'
                    ' if not value: raise AssertionError(name)\n'
                    'print(json.dumps({"status":"PASS","assertions":0}))\n')
    cases = [('author_malformed_zero', 'author', 'print("not JSON")\n', 0, 'Malformed child output'),
             ('author_nonzero', 'author', 'print("not JSON"); raise SystemExit(7)\n', 7, 'Unexpected child exit code'),
             ('author_wrong_structure', 'author', 'print("[]")\n', 0, 'Child output lacks a PASS object'),
             ('independent_malformed_zero', 'independent', 'print("not JSON")\n', 0, 'Malformed child output')]
    for optimized in (False, True):
        for label, family, synthetic, exit_code, reason in cases:
            case = output/(label+('_O' if optimized else '_normal'))
            support = case/'package/support'
            (support/'review').mkdir(parents=True)
            runner = support/'run_diagnostics.py'
            shutil.copyfile(root/'support/run_diagnostics.py', runner)
            (support/'CANDIDATE.md').write_text('Synthetic custody fixture; no theorem claim.\n')
            (support/'verify.py').write_text(synthetic if family == 'author' else good_fixture)
            (support/'review/independent_checks.py').write_text(synthetic)
            results = case/'results'
            r = invoke(label, runner, ['--output-dir', str(results)], optimized)
            receipt = results/'PROCESS_RECEIPTS.json'
            if r['exit_code'] == 0 or not receipt.is_file():
                raise RuntimeError('Failed child lacked saved execution custody: '+label)
            journal = json.loads(receipt.read_text())
            last = journal[-1]
            if last['family'] != family or last['mode'] != 'normal' or last['exit_code'] != exit_code:
                raise RuntimeError('Failed child receipt does not identify the actual failed run')
            for key in ['pid','command','stdout_sha256','stderr_sha256','started_utc','finished_utc']:
                if key not in last:
                    raise RuntimeError('Missing raw custody field: '+key)
            if last['accepted'] is not False or last.get('rejection_reason') != reason:
                raise RuntimeError('Failure receipt missing rejection interpretation')
            stem = family+'_normal'
            if last['stdout_sha256'] != sha((results/(stem+'.stdout.json')).read_bytes()):
                raise RuntimeError('Saved stdout digest mismatch')
            if last['stderr_sha256'] != sha((results/(stem+'.stderr.txt')).read_bytes()):
                raise RuntimeError('Saved stderr digest mismatch')
            if reason == 'Malformed child output' and 'parse_error' not in last:
                raise RuntimeError('Malformed stdout lacks recorded parse error')
            r['inner_receipt_sha256'] = sha(receipt.read_bytes())
            r['synthetic_control'] = True
    if before != inventory(root):
        raise RuntimeError('Custody controls altered the package')
    (output/'PROCESS_RECEIPTS.json').write_text(json.dumps(records, indent=2)+'\n')
    result = dict(status='PASS', outer_process_runs=len(records),
                  output_symlink_rejections=4, saved_failure_receipt_controls=8,
                  package_unchanged=True,
                  diagnostic_runner_sha256=sha((root/'support/run_diagnostics.py').read_bytes()),
                  integrity_runner_sha256=sha((root/'support/test_integrity.py').read_bytes()),
                  synthetic_children_only=True, new_central_proof_search_turns=0,
                  publication_authorized=False,
                  scope='Wrapper custody controls; synthetic outputs are not mathematical evidence')
    (output/'RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
