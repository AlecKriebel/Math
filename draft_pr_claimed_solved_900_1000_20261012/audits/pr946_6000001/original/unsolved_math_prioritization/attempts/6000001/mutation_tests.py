#!/usr/bin/env python3
"""Publication corruption controls. Authenticate this file externally first."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECTED: use python -I -S -B [-O|-OO] mutation_tests.py PIN PACKET')
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(b):
    return hashlib.sha256(b).hexdigest()

def update_manifest(root):
    path = root/'PUBLIC_MANIFEST.json'
    m = json.loads(path.read_bytes())
    for row in m['files']:
        raw = (root/row['path']).read_bytes()
        row.update(bytes=len(raw), sha256=digest(raw))
    raw = (json.dumps(m, indent=2)+'\n').encode()
    path.write_bytes(raw)
    return digest(raw)

def run(root, pin, mode, *extra):
    cmd = [sys.executable, '-I', '-S', '-B'] + (['-'+'O'*mode] if mode else [])
    cmd += [str(root/'verify_publication.py'), pin, str(root)] + list(extra)
    env = dict(os.environ, PYTHONOPTIMIZE='2', PYTHONPATH='/does/not/exist')
    return subprocess.run(cmd, cwd='/', env=env, capture_output=True, text=True, timeout=320)

def main():
    require(len(sys.argv)==3, 'usage: mutation_tests.py EXTERNAL_PIN PACKET')
    pin, original = sys.argv[1], Path(sys.argv[2]).absolute()
    baseline = run(original, pin, 0, '--integrity-only')
    require(baseline.returncode==0, 'Original integrity failed: '+baseline.stderr)
    require(Path(__file__).read_bytes()==(original/'mutation_tests.py').read_bytes(), 'Mutation driver differs from authenticated packet')
    records=[]
    with tempfile.TemporaryDirectory(prefix='statistical-embedding-mutations-') as td:
        top=Path(td)
        for mode in (0,1,2):
            cases=['proof', 'audit_a_report', 'audit_b_report', 'acceptance', 'script', 'result',
                   'source_metadata', 'missing', 'extra', 'empty_directory', 'symlink_file',
                   'symlink_directory', 'wrong_pin', 'manifest_rewrite', 'duplicate_json_key',
                   'traversal_path', 'duplicate_path', 'forged_reanchored_acceptance', 'frozen_manifest',
                   'optimized_child_1', 'optimized_child_2']
            for case in cases:
                root=top/(str(mode)+'_'+case)
                shutil.copytree(original,root)
                current_pin=pin
                payloads={'proof':'public/PROOF.md','audit_a_report':'independent_global_audit/public/GLOBAL_AUDIT.md',
                          'audit_b_report':'independent_audit_b/public/FULL_REPORT.md',
                          'acceptance':'independent_audit_b/public/ACCEPTANCE.json',
                          'script':'public/verify_math.py','result':'public/VERIFICATION.json',
                          'source_metadata':'public/SOURCE_METADATA.json'}
                if case in payloads:
                    p=root/payloads[case];p.write_bytes(p.read_bytes()+b'\ncorruption\n')
                elif case=='missing': (root/'public/README.md').unlink()
                elif case=='extra': (root/'unlisted.txt').write_text('extra')
                elif case=='empty_directory': (root/'unexpected').mkdir()
                elif case=='symlink_file':
                    p=root/'public/PROOF.md';p.unlink();p.symlink_to(original/'public/PROOF.md')
                elif case=='symlink_directory':
                    p=root/'public';shutil.rmtree(p);p.symlink_to(original/'public',target_is_directory=True)
                elif case=='wrong_pin': current_pin='0'*64
                elif case=='manifest_rewrite':
                    p=root/'PUBLIC_MANIFEST.json';p.write_bytes(p.read_bytes()+b'\n')
                elif case=='duplicate_json_key':
                    p=root/'PUBLIC_MANIFEST.json';raw=p.read_bytes();raw=raw.replace(b'"problem_id": 6000001', b'"problem_id": 6000001, "problem_id": 6000001');p.write_bytes(raw);current_pin=digest(raw)
                elif case in ('traversal_path','duplicate_path'):
                    p=root/'PUBLIC_MANIFEST.json';m=json.loads(p.read_bytes())
                    m['files'][0]['path']='../escape' if case=='traversal_path' else m['files'][1]['path']
                    raw=(json.dumps(m,indent=2)+'\n').encode();p.write_bytes(raw);current_pin=digest(raw)
                elif case=='forged_reanchored_acceptance':
                    p=root/'independent_audit_b/public/ACCEPTANCE.json';m=json.loads(p.read_bytes());m['verdict']='FAIL';p.write_text(json.dumps(m,indent=2)+'\n');current_pin=update_manifest(root)
                elif case=='frozen_manifest':
                    p=root/'public/MANIFEST.json';p.write_bytes(p.read_bytes()+b'\n');current_pin=update_manifest(root)
                extra=['--child-optimize',case[-1]] if case.startswith('optimized_child_') else ['--integrity-only']
                check=run(root,current_pin,mode,*extra)
                require(check.returncode!=0 and 'REJECTED:' in check.stderr, 'Negative control was accepted: '+case)
                if case.startswith('optimized_child_'):
                    require('optimized child would remove frozen assertions' in check.stderr, 'Wrong optimized-child rejection')
                    require('"optimize": '+case[-1] in check.stderr, 'Actual child optimization was not recorded')
                records.append({'outer_optimize':mode,'case':case,'rejected':True})
            # Relocation plus poisoned Python environment must still permit integrity.
            relocated=top/('relocated_'+str(mode));shutil.copytree(original,relocated)
            good=run(relocated,pin,mode,'--integrity-only')
            require(good.returncode==0, 'Relocated positive integrity failed')
        require(run(original,pin,2,'--integrity-only').returncode==0,'Original altered by mutation tests')
    print(json.dumps({'status':'PASS','outer_driver_optimize':sys.flags.optimize,'negative_controls':len(records),
                      'relocated_positive_modes':[0,1,2],'cases':records,
                      'limitation':'Packaging rejection tests; mathematical proof is not machine formalized.'},indent=2))

if __name__=='__main__':
    try: main()
    except Exception as exc: raise SystemExit('REJECTED: '+str(exc))
