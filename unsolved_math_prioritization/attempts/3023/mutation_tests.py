#!/usr/bin/env python3
"""Authenticate inputs, replay three modes, and test publication trust boundaries."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use python -I -S -B')
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--bootstrap-sha256', required=True)
    args = ap.parse_args()
    root = Path(os.path.abspath(args.root))
    need(os.getuid() == os.geteuid() == 1000, 'genuine nonroot required')
    need(re.fullmatch('[0-9a-f]{64}', args.bootstrap_sha256) is not None, 'external bootstrap pin format')
    bootstrap = (root/'BOOTSTRAP.py').read_bytes()
    need(sha(bootstrap) == args.bootstrap_sha256, 'external bootstrap pin mismatch')
    boot = {'__name__':'trusted_bootstrap', '__file__':str(root/'BOOTSTRAP.py')}
    exec(compile(bootstrap, '<externally-pinned-bootstrap>', 'exec'), boot)
    raw = (root/'verify_publication.py').read_bytes()
    need(sha(raw) == boot['VERIFIER_SHA256'] and len(raw) == boot['VERIFIER_BYTES'], 'verifier pin mismatch')
    trusted = {'__name__':'trusted_verifier'}
    exec(compile(raw, '<authenticated-verifier>', 'exec'), trusted)
    pin = boot['MANIFEST_SHA256']; bpin = args.bootstrap_sha256
    original, parsed = trusted['integrity'](root, pin, bpin)
    tests = []
    def reject(label, action):
        try:
            action()
        except (ValueError, OSError, TypeError, KeyError):
            tests.append(label)
        else:
            raise ValueError('negative accepted: '+label)
    def dump(path, value):
        path.write_text(json.dumps(value, indent=2, allow_nan=True)+'\n')
    def repin(target):
        value = json.loads((target/'PUBLICATION_MANIFEST.json').read_bytes())
        for row in value['files']:
            path = target/row['path']
            if path.is_file() and not path.is_symlink():
                data = path.read_bytes(); row.update(bytes=len(data), sha256=sha(data))
        dump(target/'PUBLICATION_MANIFEST.json', value)
        return sha((target/'PUBLICATION_MANIFEST.json').read_bytes())
    def run(target, mode, cwd, env):
        result = subprocess.run([sys.executable, '-I', '-S', '-B', *mode, str(root/'BOOTSTRAP.py'), str(target)],
                                cwd=cwd, env=env, capture_output=True, timeout=300)
        need(result.returncode == 0 and result.stderr == b'', 'full replay failed')
        value = trusted['parse'](result.stdout)
        need(type(value['optimization']) is int and value['optimization'] == (len(mode[0])-1 if mode else 0), 'mode receipt')
        need(value['status'] == 'PASS' and value['fresh_source_bindings'] == 'NOT_RUN', 'fresh scope receipt')
        return value
    with tempfile.TemporaryDirectory(prefix='dga-publication-controls-') as directory:
        temp = Path(directory)
        def mutation_copy(target):
            # Only new, disposable negative-control copies may be thawed.
            need(target.parent == temp and not target.exists(), 'disposable mutation target')
            shutil.copytree(root, target)
            target.chmod(0o755)
            for path in target.rglob('*'):
                need(not path.is_symlink(), 'unexpected link in mutation copy')
                path.chmod(0o755 if path.is_dir() else 0o644)
        env = dict(PATH=os.defpath, HOME=str(temp), TMPDIR=str(temp), LC_ALL='C')
        modes = [[]] if sys.flags.optimize == 0 else [['-'+('O'*sys.flags.optimize)]]
        baseline_cwd=temp/'baseline-cwd';baseline_cwd.mkdir();baseline_cwd.chmod(0o555)
        baseline = [run(root, mode, baseline_cwd, env) for mode in modes]
        normalized = [{k:v for k,v in row.items() if k != 'optimization'} for row in baseline]
        need(all(trusted['same'](row, normalized[0]) for row in normalized), 'mode output mismatch')
        mutations = [
            ('missing_member', lambda t:(t/'evidence/REPORT.md').unlink(), False),
            ('extra_member', lambda t:(t/'EXTRA').write_bytes(b'extra'), False),
            ('extra_empty_directory', lambda t:(t/'empty').mkdir(), False),
            ('nested_extra_directory', lambda t:(t/'evidence/empty').mkdir(), False),
            ('payload_symlink', lambda t:((t/'evidence/REPORT.md').unlink(), (t/'evidence/REPORT.md').symlink_to(root/'evidence/REPORT.md')), False),
            ('manifest_symlink', lambda t:((t/'PUBLICATION_MANIFEST.json').unlink(), (t/'PUBLICATION_MANIFEST.json').symlink_to(root/'PUBLICATION_MANIFEST.json')), False),
            ('fifo_member', lambda t:((t/'evidence/REPORT.md').unlink(), os.mkfifo(t/'evidence/REPORT.md')), False),
            ('accepted_same_size_change', lambda t:(t/'evidence/REPORT.md').write_bytes(b'X'+(t/'evidence/REPORT.md').read_bytes()[1:]), False),
            ('accepted_self_consistent_repin', lambda t:(t/'evidence/REPORT.md').write_bytes(b'X'+(t/'evidence/REPORT.md').read_bytes()[1:]), True),
            ('freeze_self_consistent_repin', lambda t:(t/'evidence/PUBLIC_SLICE.json').write_bytes(b'changed'), True),
            ('audit_result_self_consistent_repin', lambda t:(t/'evidence/AUTHOR_RUNS.public.json').write_bytes(b'{}'), True),
            ('audit_receipt_change', lambda t:(t/'evidence/AUDIT_RUNS.public.json').write_bytes(b'{}\n'), True),
            ('second_review_self_consistent_repin', lambda t:(t/'evidence/INDEPENDENT_AUDIT.public.md').write_bytes(b'changed'), True),
            ('envelope_self_consistent_repin', lambda t:(t/'evidence/PROVENANCE_ADDENDUM.md').write_bytes(b'changed'), True),
            ('bootstrap_change', lambda t:(t/'BOOTSTRAP.py').write_bytes(b'changed'), False),
            ('untrusted_manifest_change', lambda t:(t/'PUBLICATION_MANIFEST.json').write_bytes((t/'PUBLICATION_MANIFEST.json').read_bytes()+b' '), False),
        ]
        for index, (label, change, rehash) in enumerate(mutations):
            target=temp/('m'+str(index)); mutation_copy(target)
            change(target); testpin=repin(target) if rehash else pin
            reject(label, lambda:trusted['integrity'](target, testpin, bpin))
        # A trusted external bootstrap, rather than a self-reported fresh hash,
        # must reject a substituted wrapper before any of its bytes execute.
        target=temp/'reanchored-wrapper'; mutation_copy(target)
        marker=temp/'UNTRUSTED_WRAPPER_EXECUTED'
        (target/'verify_publication.py').write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\n')
        repin(target)
        result=subprocess.run([sys.executable,'-I','-S','-B',str(root/'BOOTSTRAP.py'),str(target)],
                              cwd=temp,env=env,capture_output=True,timeout=30)
        need(result.returncode != 0 and not marker.exists(), 'trusted bootstrap permitted substituted wrapper')
        tests.append('externally_anchored_wrapper_substitution')
        target=temp/'root-link'; target.symlink_to(root, target_is_directory=True)
        reject('linked_root', lambda:trusted['integrity'](target, pin, bpin))
        real=temp/'ancestor'; real.mkdir(); shutil.copytree(root,real/'packet')
        link=temp/'ancestor-link'; link.symlink_to(real,target_is_directory=True)
        reject('linked_ancestor', lambda:trusted['integrity'](link/'packet',pin,bpin))
        for label, bad in [('wrong_pin','0'*64),('uppercase_pin',pin.upper()),('short_pin',pin[:-1])]:
            reject(label, lambda bad=bad:trusted['integrity'](root,bad,bpin))
        manifest=parsed['PUBLICATION_MANIFEST.json']
        changes=[
            ('boolean_schema',lambda x:x.__setitem__('schema',True)),
            ('float_schema',lambda x:x.__setitem__('schema',1.0)),
            ('boolean_problem',lambda x:x.__setitem__('problem_id',True)),
            ('float_problem',lambda x:x.__setitem__('problem_id',3023.0)),
            ('extra_field',lambda x:x.__setitem__('extra',0)),
            ('null_files',lambda x:x.__setitem__('files',None)),
            ('duplicate_path',lambda x:x['files'].__setitem__(1,copy.deepcopy(x['files'][0]))),
            ('missing_path',lambda x:x['files'].pop()),
            ('boolean_bytes',lambda x:x['files'][0].__setitem__('bytes',True)),
            ('float_bytes',lambda x:x['files'][0].__setitem__('bytes',1.0)),
            ('negative_bytes',lambda x:x['files'][0].__setitem__('bytes',-1)),
            ('string_bytes',lambda x:x['files'][0].__setitem__('bytes','1')),
            ('uppercase_digest',lambda x:x['files'][0].__setitem__('sha256',x['files'][0]['sha256'].upper())),
            ('parent_path',lambda x:x['files'][0].__setitem__('path','../outside')),
            ('absolute_path',lambda x:x['files'][0].__setitem__('path','/outside')),
            ('dot_path',lambda x:x['files'][0].__setitem__('path','./README.md')),
            ('backslash_path',lambda x:x['files'][0].__setitem__('path','original\\RESEARCH_REPORT.md')),
            ('extra_row_field',lambda x:x['files'][0].__setitem__('extra',0)),
        ]
        for label, change in changes:
            value=copy.deepcopy(manifest);change(value)
            reject(label,lambda value=value:trusted['manifest'](value,original,trusted['PAYLOAD']))
        for name in ['check_exact.py','check_independent.py']:
            expected=trusted['expected_stdout'](name,original,sys.flags.optimize)
            reject('empty_output_'+name,lambda name=name,expected=expected:trusted['check_output'](b'',expected))
            reject('extra_output_'+name,lambda name=name,expected=expected:trusted['check_output'](expected+b' ',expected))
            value=trusted['parse'](expected);value['uid']=True
            altered=(json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
            reject('altered_payload_'+name,lambda altered=altered,expected=expected:trusted['check_output'](altered,expected))
        for label, value in [('duplicate_json_key' ,b'{"x":1,"x":1}'),('nan',b'{"x":NaN}'),('infinity',b'{"x":Infinity}'),('negative_infinity',b'{"x":-Infinity}'),('overflow_float',b'{"x":1e999}')]:
            reject(label,lambda value=value:trusted['parse'](value))
        for label, left, right in [('bool_int',True,1),('float_int',1.0,1),('nested_bool',{'x':[True]},{'x':[1]}),('extra_receipt_key',{'x':1,'y':2},{'x':1})]:
            need(not trusted['same'](left,right),'exact-type comparison');tests.append(label)
        relocated=temp/'readonly relocated';shutil.copytree(root,relocated)
        hostile=temp/'hostile cwd';hostile.mkdir();sentinel=temp/'HOSTILE_EXECUTED'
        evil='from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("executed")\nraise RuntimeError("hostile import")\n'
        for name in ['sitecustomize.py','usercustomize.py','json.py','hashlib.py','pathlib.py','subprocess.py','fractions.py']:
            (hostile/name).write_text(evil)
        for path in relocated.rglob('*'):
            path.chmod(0o555 if path.is_dir() else 0o444)
        relocated.chmod(0o555)
        before_hostile={p.name:sha(p.read_bytes()) for p in hostile.iterdir()}
        for path in hostile.iterdir():path.chmod(0o444)
        hostile.chmod(0o555)
        denied=[]
        try:
            for path in [relocated/'NEW_FILE',relocated/'README.md',hostile/'NEW_FILE']:
                try:
                    with path.open('ab') as f:f.write(b'forbidden')
                except PermissionError:denied.append(path.name)
                else:raise ValueError('readonly probe succeeded')
            hostile_env=dict(env,PYTHONPATH=str(hostile),PYTHONHOME=str(hostile),PYTHONSTARTUP=str(hostile/'sitecustomize.py'))
            replay=[run(relocated,mode,hostile,hostile_env) for mode in modes]
            need(all(trusted['same'](a,b) for a,b in zip(baseline,replay)), 'relocation/hostile result changed')
            need(not sentinel.exists(),'hostile import executed')
            need(before_hostile=={p.name:sha(p.read_bytes()) for p in hostile.iterdir()},'hostile cwd changed')
            need(trusted['integrity'](relocated,pin,bpin)[0]==original,'readonly packet changed')
        finally:
            relocated.chmod(0o755);hostile.chmod(0o755)
            for path in relocated.rglob('*'):path.chmod(0o755 if path.is_dir() else 0o644)
            for path in hostile.iterdir():path.chmod(0o644)
    need(trusted['integrity'](root,pin,bpin)[0]==original,'original packet changed')
    print(json.dumps(dict(schema=1,problem_id=3023,status='PASS',uid=os.getuid(),euid=os.geteuid(),
                         harness_optimization=sys.flags.optimize,negative_controls=len(tests),negative_labels=tests,
                         baseline_modes=['normal' if not modes[0] else modes[0][0]],readonly_hostile_modes=['normal' if not modes[0] else modes[0][0]],
                         readonly_probes_denied=denied,hostile_import_executed=False,original_unchanged=True,
                         source_bindings='NOT_RUN',bootstrap_sha256=bpin,manifest_sha256=pin,baseline_receipts=baseline,readonly_hostile_receipts=replay),sort_keys=True))


if __name__=='__main__':
    try:
        main()
    except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired):
        print('REJECT: publication control failed',file=sys.stderr)
        sys.exit(1)
