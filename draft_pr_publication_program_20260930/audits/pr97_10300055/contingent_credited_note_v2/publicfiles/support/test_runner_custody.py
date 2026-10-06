#!/usr/bin/env python3
"""Fresh-output and failure-receipt custody controls; all children are synthetic."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
sys.dont_write_bytecode = True
from safe_output import fresh_output, copy_new, write_new, json_bytes, Journal


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inventory(root):
    return {p.relative_to(root).as_posix(): sha(p.read_bytes())
            for p in root.rglob('*') if p.is_file()}


def require(value, message):
    if not value:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', required=True)
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    output = fresh_output(args.output_dir, root)
    before = inventory(root)
    records = []
    custody = Journal(output/'PROCESS_RECEIPTS.json')
    wrappers = ['run_diagnostics.py', 'test_integrity.py', 'test_runner_custody.py']
    archive = str(Path(args.archive).absolute())

    def invoke(label, script, arguments, optimized, marker=None):
        command = [sys.executable, '-E', '-B'] + (['-O'] if optimized else [])
        if marker is None:
            command += [str(script)] + arguments
        else:
            # Record every attempted child launch, even one that fails.
            bootstrap = ('import pathlib,runpy,sys\n'
                         'marker=pathlib.Path(sys.argv[1]); script=sys.argv[2]\n'
                         'def audit(event,args):\n'
                         ' if event=="subprocess.Popen" and not marker.exists():\n'
                         '  with marker.open("xb") as f: f.write(b"CHILD_LAUNCHED")\n'
                         'sys.addaudithook(audit)\n'
                         'sys.path.insert(0,str(pathlib.Path(script).parent))\n'
                         'sys.argv=[script]+sys.argv[3:]\n'
                         'runpy.run_path(script,run_name="__main__")\n')
            command += ['-c', bootstrap, str(marker), str(script)] + arguments
        start = dt.datetime.now(dt.timezone.utc).isoformat()
        tick = time.monotonic()
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        record = dict(label=label, optimized=optimized, command=command, cwd=os.getcwd(),
                      pid=proc.pid, started_utc=start,
                      finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                      wall_seconds=time.monotonic()-tick, exit_code=proc.returncode,
                      stdout=out.decode(errors='replace'), stderr=err.decode(errors='replace'),
                      stdout_sha256=sha(out), stderr_sha256=sha(err),
                      script_sha256=sha(script.read_bytes()), synthetic_control=True,
                      accepted=None)
        records.append(record)
        custody.save(records)
        return record

    def fixture(case):
        package = case/'package'
        support = package/'support'
        (support/'review').mkdir(parents=True)
        for name in wrappers+['safe_output.py']:
            copy_new(root/'support'/name, support/name)
        write_new(package/'README.md', b'SYNTHETIC CLOSED INPUT: MUST REMAIN UNCHANGED\n')
        write_new(package/'LICENSE.txt', b'SYNTHETIC CLOSED INPUT: MUST REMAIN UNCHANGED\n')
        write_new(support/'CANDIDATE.md', b'Synthetic custody fixture; no theorem claim.\n')
        sentinel = b'raise RuntimeError("SYNTHETIC CHILD REACHED")\n'
        for target in [package/'check_integrity.py', support/'verify.py',
                       support/'review/independent_checks.py']:
            write_new(target, sentinel)
        return package

    for optimized in (False, True):
        for name in wrappers:
            for kind in ['symlink', 'hardlink', 'plain_existing', 'reused', 'ancestor_symlink']:
                label = name[:-3]+'_'+kind+('_O' if optimized else '_normal')
                case = output/label
                package = fixture(case)
                marker = case/'CHILD_LAUNCHED'
                destination = case/'results'
                victim = package/('README.md' if name == 'run_diagnostics.py' else 'LICENSE.txt')
                victim_before = sha(victim.read_bytes())
                if kind == 'ancestor_symlink':
                    alias = case/'outside_named_alias'
                    alias.symlink_to(package, target_is_directory=True)
                    destination = alias/'must_not_be_created'
                    reason = 'Choose an output directory outside the closed package'
                    output_before = None
                else:
                    destination.mkdir()
                    reason = 'Output directory must be fresh and non-existing'
                    if kind in ('symlink', 'hardlink'):
                        leaf = destination/('author_normal.stdout.json' if name == 'run_diagnostics.py'
                                            else 'PROCESS_RECEIPTS.json')
                        if kind == 'symlink':
                            leaf.symlink_to(victim)
                        else:
                            os.link(victim, leaf)
                    elif kind == 'reused':
                        write_new(destination/'prior_run.txt', b'Previous disposable run; no reuse.\n')
                    output_before = inventory(destination)
                input_before = inventory(package)
                arguments = (['--archive', archive] if name != 'run_diagnostics.py' else [])
                arguments += ['--output-dir', str(destination)]
                r = invoke(label, package/'support'/name, arguments, optimized, marker)
                r.update(expected_reason=reason, link_type=kind,
                         input_inventory_before=input_before,
                         input_inventory_after=inventory(package),
                         victim_sha256_before=victim_before,
                         victim_sha256_after=sha(victim.read_bytes()),
                         child_launch_observation='CPython subprocess.Popen audit hook',
                         child_launched=marker.exists())
                if output_before is not None:
                    r['output_inventory_before'] = output_before
                    r['output_inventory_after'] = inventory(destination)
                r['accepted'] = (r['exit_code'] != 0 and reason in r['stderr']
                                 and r['input_inventory_before'] == r['input_inventory_after']
                                 and r['victim_sha256_before'] == r['victim_sha256_after']
                                 and not r['child_launched']
                                 and (output_before is None or output_before == inventory(destination)))
                if kind == 'ancestor_symlink':
                    r['accepted'] = r['accepted'] and not destination.exists()
                    alias.unlink()
                custody.save(records)
                require(r['accepted'], 'Fresh-output rejection failed: '+label)

    good_fixture = ('import json\n'
                    'def ck(name, value):\n'
                    ' if not value: raise AssertionError(name)\n'
                    'print(json.dumps({"status":"PASS","assertions":0}))\n')
    cases = [('author_malformed_zero', 'author', 'print("not JSON")\n', 0, 'Malformed child output'),
             ('author_nonzero', 'author', 'print("not JSON"); raise SystemExit(7)\n', 7,
              'Unexpected child exit code'),
             ('author_wrong_structure', 'author', 'print("[]")\n', 0, 'Child output lacks a PASS object'),
             ('independent_malformed_zero', 'independent', 'print("not JSON")\n', 0,
              'Malformed child output')]
    for optimized in (False, True):
        for label, family, synthetic, exit_code, reason in cases:
            case = output/(label+('_O' if optimized else '_normal'))
            support = case/'package/support'
            (support/'review').mkdir(parents=True)
            runner = support/'run_diagnostics.py'
            for name in ['run_diagnostics.py','safe_output.py']:
                copy_new(root/'support'/name, support/name)
            write_new(support/'CANDIDATE.md', b'Synthetic custody fixture; no theorem claim.\n')
            write_new(support/'verify.py', (synthetic if family == 'author' else good_fixture).encode())
            write_new(support/'review/independent_checks.py', synthetic.encode())
            results = case/'results'
            r = invoke(label+('_O' if optimized else '_normal'), runner,
                       ['--output-dir', str(results)], optimized)
            receipt = results/'PROCESS_RECEIPTS.json'
            require(r['exit_code'] != 0 and receipt.is_file(), 'Failed child lacked custody: '+label)
            journal = json.loads(receipt.read_text())
            last = journal[-1]
            require(last['family'] == family and last['mode'] == 'normal'
                    and last['exit_code'] == exit_code, 'Receipt misidentifies failed child')
            for key in ['pid','command','stdout_sha256','stderr_sha256','started_utc','finished_utc']:
                require(key in last, 'Missing raw custody field: '+key)
            require(last['accepted'] is False and last.get('rejection_reason') == reason,
                    'Failure receipt lacks rejection interpretation')
            stem = family+'_normal'
            require(last['stdout_sha256'] == sha((results/(stem+'.stdout.json')).read_bytes()),
                    'Saved stdout digest mismatch')
            require(last['stderr_sha256'] == sha((results/(stem+'.stderr.txt')).read_bytes()),
                    'Saved stderr digest mismatch')
            if reason == 'Malformed child output':
                require('parse_error' in last, 'Malformed stdout lacks recorded parse error')
            r.update(inner_receipt_sha256=sha(receipt.read_bytes()),
                     failed_child_receipt=last, accepted=True)
            custody.save(records)
    # Focused helper controls: first writes reject aliases; updates replace them.
    helper_control = ('import json,os,pathlib,sys\n'
                      'sys.dont_write_bytecode=True\n'
                      'sys.path.insert(0,sys.argv[1])\n'
                      'from safe_output import write_new,Journal\n'
                      'base=pathlib.Path(sys.argv[2]); kind=sys.argv[3]; method=sys.argv[4]\n'
                      'victim=base/"victim"; leaf=base/"leaf"\n'
                      'write_new(victim,b"UNCHANGED")\n'
                      'j=Journal(leaf)\n'
                      'if method=="journal_update": j.save({"before":True}); leaf.unlink()\n'
                      'if kind=="symlink": leaf.symlink_to(victim)\n'
                      'else: os.link(victim,leaf)\n'
                      'rejected=False\n'
                      'try:\n'
                      ' if method=="first_write": write_new(leaf,b"NEW")\n'
                      ' else: j.save({"after":True})\n'
                      'except FileExistsError: rejected=True\n'
                      'if victim.read_bytes()!=b"UNCHANGED": raise RuntimeError("Victim changed")\n'
                      'if method=="journal_update":\n'
                      ' if rejected or json.loads(leaf.read_text())!={"after":True}: '
                      'raise RuntimeError("Atomic replacement failed")\n'
                      'elif not rejected: raise RuntimeError("First creation followed alias")\n'
                      'print(json.dumps({"status":"PASS","victim_unchanged":True, '
                      '"method":method,"link_type":kind}))\n')
    helper_script = output/'helper_control.py'
    write_new(helper_script, helper_control.encode())
    for optimized in (False, True):
        for kind in ('symlink','hardlink'):
            for method in ('first_write','journal_first','journal_update'):
                label = 'helper_'+kind+'_'+method+('_O' if optimized else '_normal')
                case = output/label
                case.mkdir()
                r = invoke(label, helper_script, [str(root/'support'),str(case),kind,method], optimized)
                parsed = json.loads(r['stdout']) if r['exit_code'] == 0 else {}
                r['accepted'] = (r['exit_code'] == 0 and parsed.get('status') == 'PASS'
                                 and parsed.get('victim_unchanged') is True)
                r['safe_output_sha256'] = sha((root/'support/safe_output.py').read_bytes())
                custody.save(records)
                require(r['accepted'], 'Exclusive/atomic helper control failed: '+label)
    require(before == inventory(root), 'Custody controls altered the package')
    result = dict(status='PASS', outer_process_runs=len(records),
                  linked_leaf_rejections=12, plain_existing_rejections=6,
                  populated_reuse_rejections=6, output_ancestor_symlink_rejections=6,
                  saved_failure_receipt_controls=8, package_unchanged=True,
                  exclusive_first_creation_and_atomic_update_controls=12,
                  no_child_launch_for_all_30_output_rejections=True,
                  wrapper_hashes={name:sha((root/'support'/name).read_bytes()) for name in wrappers},
                  safe_output_sha256=sha((root/'support/safe_output.py').read_bytes()),
                  synthetic_children_only=True, new_central_proof_search_turns=0,
                  publication_authorized=False,
                  scope='Local disposable-output custody; synthetic outputs are not mathematical evidence; '
                        'no promise against arbitrary concurrent hostile filesystem replacement')
    write_new(output/'RESULT.json', json_bytes(result))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
