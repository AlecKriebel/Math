#!/usr/bin/env python3
"""Publication-boundary controls on disposable copies; authenticate release first."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use python -I -S -B')
import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import tempfile


def need(ok, message):
    if not ok:
        raise ValueError(message)


def writable(root):
    if root.is_symlink():
        return
    for base, dirs, files in os.walk(root, followlinks=False):
        Path(base).chmod(0o755)
        for name in files:
            p = Path(base)/name
            if not p.is_symlink():
                p.chmod(0o644)


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}


def main():
    need(len(sys.argv) == 2 and os.getuid() == os.geteuid() != 0, 'packet path and real nonroot required')
    packet = Path(os.path.abspath(sys.argv[1]))
    bootstrap = packet/'BOOTSTRAP.py'
    initial = snapshot(packet)
    rows = []
    with tempfile.TemporaryDirectory(prefix='boundary-controls-') as td:
        work = Path(td)
        case, hostile, sentinel = work/'case', work/'hostile', work/'SENTINEL'
        hostile.mkdir()
        attack = "open("+repr(str(sentinel))+", 'w').write('unexpected execution')\nraise RuntimeError('hostile execution')\n"
        for module in ['json', 'hashlib', 'argparse', 'pathlib', 'sitecustomize', 'usercustomize', 'subprocess']:
            (hostile/(module+'.py')).write_text(attack)
        hostile.chmod(0o555)
        env = dict(os.environ, PYTHONPATH=str(hostile), PYTHONHOME='/nonexistent-python-home',
                   PYTHONSTARTUP=str(hostile/'sitecustomize.py'), PYTHONINSPECT='1', PYTHONOPTIMIZE='2')
        def reset():
            if case.is_symlink():
                case.unlink()
            if case.exists():
                writable(case); shutil.rmtree(case)
            shutil.copytree(packet, case)
            # copytree preserves input modes; mutations require writable disposable copies.
            writable(case)
            return case
        def run(label, target, expected, mode):
            flags = [] if mode == 'normal' else ['-'+mode]
            result = subprocess.run([sys.executable, '-I', '-S', '-B', *flags, str(bootstrap), str(target)],
                                    env=env, cwd=hostile, capture_output=True, timeout=240)
            need(result.returncode == expected, label+' unexpected exit')
            need(not sentinel.exists(), label+' executed hostile bytes')
            if expected == 0:
                data = json.loads(result.stdout)
                need(data['status'] == 'PASS' and data['source_free_expected_outcomes'] == 301,
                     'positive replay receipt')
                need(data['source_identity_checks'] == 'NOT_RUN', 'source scope')
            rows.append(dict(test=label, python_mode=mode, expected_exit=expected,
                             actual_exit=result.returncode, passed=True))
        def all_modes(label, target, expected=1):
            for mode in ['normal', 'O', 'OO']:
                run(label, target, expected, mode)
        try:
            all_modes('intact_hostile_environment', packet, 0)
            ns = runpy.run_path(str(packet/'verify_publication.py'))
            reset()
            for p in case.rglob('*'):
                p.chmod(0o555 if p.is_dir() else 0o444)
            case.chmod(0o555)
            denied = 0
            for p, mode in [(case/'README.md','ab'), (case/'new','wb'), (case/'author'/'new','wb'), (hostile/'new','wb')]:
                try:
                    with p.open(mode):
                        pass
                except PermissionError:
                    denied += 1
            need(denied == 4, 'genuine readonly probes')
            all_modes('whole_packet_readonly', case, 0)
            for name in ['author/ACCEPTANCE_REPORT.md', 'audit/AUDIT_REPORT.md', 'audit/AUDIT_TEST_RESULTS.json',
                         'FRESH_REPLAY.json', 'verify_publication.py', 'BOOTSTRAP.py', 'PUBLICATION_MANIFEST.json']:
                reset(); p=case/name; raw=bytearray(p.read_bytes());raw[-1]^=1;p.write_bytes(raw)
                all_modes('same_size_'+name,case)
            for name in ['author/RESULT.json','audit/verify_independent.py','README.md','BOOTSTRAP.py']:
                reset();(case/name).unlink();all_modes('missing_'+name,case)
            for name in ['extra.pdf','.hidden','author/.hidden']:
                reset();(case/name).write_text('synthetic fixture');all_modes('extra_'+name,case)
            reset();(case/'nested').mkdir();all_modes('extra_directory',case)
            for name in ['author/RESULT.json','audit/verify_independent.py','PUBLICATION_MANIFEST.json','BOOTSTRAP.py']:
                reset();(case/name).unlink();(case/name).symlink_to(packet/name);all_modes('symlink_'+name,case)
            reset();shutil.rmtree(case/'audit');(case/'audit').symlink_to(packet/'audit',target_is_directory=True)
            all_modes('linked_audit_directory',case)
            reset();writable(case);shutil.rmtree(case);case.symlink_to(packet,target_is_directory=True)
            all_modes('linked_packet_root',case)
            reset();(case/'author'/'RESULT.json').unlink();os.mkfifo(case/'author'/'RESULT.json')
            all_modes('fifo_member',case)
            for name in ['author/verify_packet.py','audit/verify_independent.py','audit/run_audit_tests.py','verify_publication.py']:
                reset();(case/name).write_text(attack);all_modes('hostile_'+name,case)
                manifest=json.loads((case/'PUBLICATION_MANIFEST.json').read_text())
                for row in manifest['files']:
                    if row['path']==name:
                        b=(case/name).read_bytes();row.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
                (case/'PUBLICATION_MANIFEST.json').write_text(json.dumps(manifest))
                all_modes('hostile_rehashed_'+name,case)
            # Direct parser/schema tests reach semantic checks behind the fixed hash gate.
            base=json.loads((packet/'PUBLICATION_MANIFEST.json').read_text())
            malformed=[('duplicate','{"a":1,"a":2}'),('nested_duplicate','{"a":{"b":1,"b":2}}'),
                       ('nan','{"a":NaN}'),('infinity','{"a":Infinity}'),('minus_infinity','{"a":-Infinity}'),
                       ('overflow','{"a":1e999}')]
            for label,raw in malformed:
                for mode in ['normal','O','OO']:
                    flags=[] if mode=='normal' else ['-'+mode]
                    code="import runpy,sys; n=runpy.run_path(sys.argv[1]); n['parse'](sys.argv[2])"
                    r=subprocess.run([sys.executable,'-I','-S','-B',*flags,'-c',code,str(packet/'verify_publication.py'),raw],env=env,cwd=hostile,capture_output=True)
                    need(r.returncode==1 and not sentinel.exists(),'parser negative')
                    rows.append(dict(test='parser_'+label,python_mode=mode,expected_exit=1,actual_exit=1,passed=True))
            changes=[('boolean_schema',lambda m:m.update(schema=True)),('float_schema',lambda m:m.update(schema=1.0)),
                     ('wrong_id',lambda m:m.update(problem_id=0)),('boolean_id',lambda m:m.update(problem_id=True)),
                     ('float_id',lambda m:m.update(problem_id=2305029.0)),('extra_field',lambda m:m.update(extra=0)),
                     ('missing_field',lambda m:m.pop('schema')),('empty_files',lambda m:m.update(files=[])),
                     ('duplicate_path',lambda m:m['files'].__setitem__(1,m['files'][0])),
                     ('traversal',lambda m:m['files'][0].update(path='../outside')),
                     ('boolean_size',lambda m:m['files'][0].update(bytes=True)),
                     ('float_size',lambda m:m['files'][0].update(bytes=float(m['files'][0]['bytes']))),
                     ('negative_size',lambda m:m['files'][0].update(bytes=-1)),
                     ('uppercase_hash',lambda m:m['files'][0].update(sha256=m['files'][0]['sha256'].upper())),
                     ('null_row',lambda m:m['files'].__setitem__(0,None))]
            for label,change in changes:
                value=json.loads(json.dumps(base));change(value)
                for mode in ['normal','O','OO']:
                    flags=[] if mode=='normal' else ['-'+mode]
                    code="import runpy,sys; from pathlib import Path; n=runpy.run_path(sys.argv[1]); r=Path(sys.argv[2]); s={k:(r/k).read_bytes() for k in n['PAYLOAD']}; n['validate_manifest'](n['parse'](sys.argv[3]),s)"
                    r=subprocess.run([sys.executable,'-I','-S','-B',*flags,'-c',code,str(packet/'verify_publication.py'),str(packet),json.dumps(value)],env=env,cwd=hostile,capture_output=True)
                    need(r.returncode==1 and not sentinel.exists(),'schema negative')
                    rows.append(dict(test='schema_'+label,python_mode=mode,expected_exit=1,actual_exit=1,passed=True))
            need(not ns['same'](True,1) and not ns['same'](1,1.0),'exact type equality')
            need(snapshot(packet)==initial,'original publication changed')
            print(json.dumps(dict(schema=1,problem_id=2305029,status='PASS',nonroot=True,
                                  readonly_write_probes_denied=denied,test_count=len(rows),tests=rows,
                                  hostile_sentinel_created=False,original_unchanged=True,
                                  source_identity_checks='NOT_RUN',mathematical_proof_check='NOT_RUN'),indent=2))
        finally:
            if case.is_symlink():case.unlink()
            elif case.exists():writable(case)
            hostile.chmod(0o755)


if __name__=='__main__':
    main()
