#!/usr/bin/env python3
"""Replays a separately pinned author release; all mutations are disposable."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

class Reject(Exception):
    pass

def require(value, message):
    if not value:
        raise Reject(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def inventory(root):
    return {str(p.relative_to(root)): {'bytes': len(p.read_bytes()), 'sha256': sha(p.read_bytes())}
            for p in sorted(root.rglob('*')) if p.is_file()}

def run(command, cwd, env=None):
    p = subprocess.run(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=45)
    return p.returncode, p.stdout, p.stderr

def main():
    require(len(sys.argv) == 5, 'usage: run_audit.py RELEASE MANIFEST_SHA256 BOOTSTRAP_SHA256 RECEIPT')
    release = Path(sys.argv[1]).resolve()
    manifest_pin, bootstrap_pin = sys.argv[2:4]
    output = Path(sys.argv[4]).resolve()
    require(sha((release/'AUTHOR_MANIFEST.json').read_bytes()) == manifest_pin, 'untrusted manifest')
    require(sha((release/'bootstrap.py').read_bytes()) == bootstrap_pin, 'untrusted bootstrap')
    before = inventory(release)
    result = {'schema': 'habiro-independent-source-bridge-replay-v1',
              'problem_id': 10400145, 'manifest_sha256': manifest_pin,
              'bootstrap_sha256': bootstrap_pin, 'uid': os.getuid(),
              'baseline': [], 'controls': [], 'read_only': [], 'algebra': [], 'algebra_read_only': []}
    require(os.getuid() != 0, 'replay must not run as root')
    modes = [('normal', []), ('-O', ['-O']), ('-OO', ['-OO'])]
    good_stdout = None
    algebra_stdout = None
    algebra = Path(__file__).resolve().with_name('independent_algebra.py')
    for name, flags in modes:
        command = [sys.executable, '-I', '-S', '-B', *flags, str(release/'bootstrap.py'), str(release/'packet')]
        code, out, err = run(command, release)
        require(code == 0 and not err, 'baseline failed '+name)
        if good_stdout is None:
            good_stdout = out
        require(good_stdout == out, 'optimization changed author output')
        result['baseline'].append({'mode': name, 'exit_code': code, 'stdout_sha256': sha(out)})
        code, out, err = run([sys.executable, '-I', '-S', '-B', *flags, str(algebra)], release)
        require(code == 0 and not err, 'independent algebra failed '+name)
        if algebra_stdout is None:
            algebra_stdout = out
        require(algebra_stdout == out, 'optimization changed algebra output')
        result['algebra'].append({'mode': name, 'exit_code': code, 'stdout_sha256': sha(out)})
        code, out, err = run(['bwrap', '--ro-bind', '/', '/', '--die-with-parent', '--', *command], release)
        require(code == 0 and not err and out == good_stdout, 'read-only author replay failed '+name)
        result['read_only'].append({'mode': name, 'exit_code': code, 'stdout_sha256': sha(out), 'mount': 'whole filesystem read-only'})
        code, out, err = run(['bwrap', '--ro-bind', '/', '/', '--die-with-parent', '--', sys.executable, '-I', '-S', '-B', *flags, str(algebra)], release)
        require(code == 0 and not err and out == algebra_stdout, 'read-only independent algebra failed '+name)
        result['algebra_read_only'].append({'mode': name, 'exit_code': code, 'stdout_sha256': sha(out), 'mount': 'whole filesystem read-only'})
    probe = ('from pathlib import Path\nimport sys\n'
             'p=Path(sys.argv[1])\n'
             'try:\n p.write_bytes(b"write-probe")\n'
             'except OSError as error:\n print("WRITE_DENIED_ERRNO="+str(error.errno))\n'
             'else:\n raise SystemExit("READ_ONLY_TEST_FAILED")\n')
    with tempfile.TemporaryDirectory(prefix='habiro-source-bridge-audit-') as temporary:
        temp = Path(temporary)
        probe_path = temp/'probe'
        probe_path.write_text('unchanged')
        code, out, err = run(['bwrap', '--ro-bind', '/', '/', '--die-with-parent', '--', sys.executable,
                              '-I', '-S', '-B', '-c', probe, str(probe_path)], temp)
        require(code == 0 and out == b'WRITE_DENIED_ERRNO=30\n' and probe_path.read_text() == 'unchanged', 'mount write probe failed')
        result['write_denied_probe'] = True
        result['write_denied_errno'] = 30
        result['read_only_command_prefix'] = ['bwrap', '--ro-bind', '/', '/', '--die-with-parent', '--']
        # Each semantic mutation is tested directly against the exact pinned
        # author's checker, so its rejection is not merely a stale-hash result.
        base_cert = json.loads((release/'packet/CERTIFICATE.json').read_text())
        semantic = [
            ('wrong-rank-three', lambda c: c.update(first_coefficients=[0,-6,-12])),
            ('zero-residual', lambda c: c.update(second_difference=0)),
            ('floating-rank', lambda c: c.update(ranks=[1,2,3.0])),
            ('boolean-rank', lambda c: c.update(ranks=[True,2,3])),
            ('missing-rank-one', lambda c: c.update(ranks=[2,3,4])),
            ('wrong-casson', lambda c: c.update(casson_normalization=1)),
            ('wrong-parameter', lambda c: c.update(quantum_parameter='q=1+2*x')),
            ('inverted-q-minus-one', lambda c: c.update(base_ring='Z[x,x^-1]/(x^2)')),
            ('too-low-quotient', lambda c: c.update(quotient_level=2)),
            ('extra-key', lambda c: c.update(extra='unpermitted')),
            ('missing-key', lambda c: c.pop('witness')),
            ('boolean-casson', lambda c: c.update(casson_normalization=True)),
        ]
        for label, mutate in semantic:
            case = temp/label
            shutil.copytree(release/'packet', case)
            for f in case.iterdir(): f.chmod(0o644)
            case.chmod(0o755)
            cert = json.loads(json.dumps(base_cert)); mutate(cert)
            (case/'CERTIFICATE.json').write_text(json.dumps(cert))
            for name, flags in modes:
                code, out, err = run([sys.executable, '-I', '-S', '-B', *flags, str(case/'verify.py')], temp)
                require(code != 0 and b'REJECT:' in err, 'semantic control accepted '+label+' '+name)
                result['controls'].append({'name': label, 'layer': 'direct pinned checker', 'mode': name, 'rejected': True})
        for label, text in [('duplicate-json-key', '{"schema":"bad",'+(release/'packet/CERTIFICATE.json').read_text().lstrip()[1:]),
                            ('invalid-json', '{'), ('non-object-json', '[]')]:
            case=temp/label;shutil.copytree(release/'packet',case);case.chmod(0o755)
            for f in case.iterdir():f.chmod(0o644)
            (case/'CERTIFICATE.json').write_text(text)
            for name, flags in modes:
                code,out,err=run([sys.executable,'-I','-S','-B',*flags,str(case/'verify.py')],temp)
                require(code != 0 and b'REJECT:' in err, 'JSON control accepted '+label)
                result['controls'].append({'name':label,'layer':'direct pinned checker','mode':name,'rejected':True})
        def stale_file(case):
            p=case/'packet/PROOF_AND_STATUS.md';p.write_bytes(p.read_bytes()+b'\nchanged\n')
        def wrong_source(case):
            p=case/'packet/SOURCE_METADATA.json';c=json.loads(p.read_text());c['sources'][0]['bytes']+=1;p.write_text(json.dumps(c))
        def corrupt_checker(case):
            p=case/'packet/verify.py';p.write_bytes(p.read_bytes()+b'\n# changed\n')
        def missing(case): (case/'packet/CERTIFICATE.json').unlink()
        def extra(case): (case/'packet/extra.txt').write_text('unexpected')
        def nested(case): (case/'packet/nested').mkdir()
        def symlink(case):
            p=case/'packet/CERTIFICATE.json';p.unlink();p.symlink_to(release/'packet/CERTIFICATE.json')
        def bad_manifest(case): (case/'AUTHOR_MANIFEST.json').write_text('{')
        for label, mutate in [('stale-proof',stale_file),('changed-source-metadata',wrong_source),
                              ('altered-checker',corrupt_checker),('missing-payload',missing),
                              ('extra-payload',extra),('nested-directory',nested),('symlink-payload',symlink),
                              ('malformed-manifest',bad_manifest)]:
            case=temp/label;shutil.copytree(release,case)
            for f in case.rglob('*'):f.chmod(0o755 if f.is_dir() else 0o644)
            case.chmod(0o755);mutate(case)
            for name,flags in modes:
                code,out,err=run([sys.executable,'-I','-S','-B',*flags,str(case/'bootstrap.py'),str(case/'packet')],temp)
                require(code != 0 and b'REJECT:' in err,'bootstrap control accepted '+label)
                result['controls'].append({'name':label,'layer':'pinned bootstrap','mode':name,'rejected':True})
        hostile=temp/'hostile';hostile.mkdir()
        for module in ['json','hashlib','pathlib','sitecustomize']:
            (hostile/(module+'.py')).write_text('raise RuntimeError("hostile import executed")\n')
        env=dict(os.environ);env['PYTHONPATH']=str(hostile);env['PYTHONSTARTUP']=str(hostile/'json.py')
        for name,flags in modes:
            code,out,err=run([sys.executable,'-I','-S','-B',*flags,str(release/'bootstrap.py'),str(release/'packet')],hostile,env)
            require(code==0 and not err and out==good_stdout,'hostile-environment control failed')
            result['controls'].append({'name':'hostile-cwd-and-pythonpath','layer':'isolated bootstrap','mode':name,'expected_pass':True})
    require(before == inventory(release), 'frozen author bytes changed')
    result.update(status='PASS', author_bytes_unchanged=True, control_count=len(result['controls']),
                  algebra_result=json.loads(algebra_stdout), scope='Mathematical/source review is in FULL_AUDIT.md; scripts validate finite algebra and replay integrity only.')
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','controls':len(result['controls']),'author_bytes_unchanged':True},sort_keys=True))

if __name__ == '__main__':
    main()
