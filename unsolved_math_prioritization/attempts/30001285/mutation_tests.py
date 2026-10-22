#!/usr/bin/env python3
"""Disposable adversarial controls for the source-free publication packet."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def require(value, label):
    if not value: raise RuntimeError(label)


def digest(b): return hashlib.sha256(b).hexdigest()


def run(script, mode, *args):
    return subprocess.run([sys.executable, '-I', '-S', '-B', *mode, str(script), *map(str,args)],
                          cwd=tempfile.gettempdir(), capture_output=True, timeout=180)


def rebind(root):
    path = root / 'PUBLIC_MANIFEST.json'; m = json.loads(path.read_bytes())
    for name in m['files']:
        f = root / name
        if f.is_file() and not f.is_symlink():
            b = f.read_bytes(); m['files'][name] = {'bytes':len(b), 'sha256':digest(b)}
    b = (json.dumps(m,indent=2,sort_keys=True)+'\n').encode()
    path.write_bytes(b)
    return digest(b)


def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);a=p.parse_args()
    packet=Path(__file__).resolve().parent
    cases = ['bad_external_digest','payload_edit','extra_file','extra_directory','missing_file',
             'payload_symlink','directory_symlink','manifest_symlink','nonregular_payload',
             'unsafe_path','wrong_size','rebound_original','rebound_audit','rebound_patch',
             'rebound_corrected','rebound_manifest_anchor']
    results=[]
    for mode in ([], ['-O']):
        good=run(packet/'verify_publication.py',mode,'--manifest-sha256',a.manifest_sha256,'--integrity-only')
        require(good.returncode==0,'positive control failed: '+good.stderr.decode(errors='replace'))
        for case in cases:
            with tempfile.TemporaryDirectory(prefix='motivic-negative-') as td:
                root=Path(td)/'packet';shutil.copytree(packet,root);expected=a.manifest_sha256
                target=root/'original/STATEMENT.md'
                if case=='bad_external_digest':expected='0'*64
                elif case=='payload_edit':target.write_bytes(target.read_bytes()+b'\n')
                elif case=='extra_file':(root/'UNLISTED').write_text('extra')
                elif case=='extra_directory':(root/'UNLISTED').mkdir()
                elif case=='missing_file':target.unlink()
                elif case=='payload_symlink':
                    other=Path(td)/'statement';target.rename(other);target.symlink_to(other)
                elif case=='directory_symlink':
                    other=Path(td)/'original';(root/'original').rename(other);(root/'original').symlink_to(other,target_is_directory=True)
                elif case=='manifest_symlink':
                    other=Path(td)/'manifest';(root/'PUBLIC_MANIFEST.json').rename(other);(root/'PUBLIC_MANIFEST.json').symlink_to(other)
                elif case=='nonregular_payload':target.unlink();target.mkdir()
                elif case in ('unsafe_path','wrong_size'):
                    mp=root/'PUBLIC_MANIFEST.json';m=json.loads(mp.read_bytes())
                    if case=='unsafe_path':m['files']['../escape']=m['files'].pop('README.md')
                    else:m['files']['README.md']['bytes']+=1
                    b=(json.dumps(m,indent=2,sort_keys=True)+'\n').encode();mp.write_bytes(b);expected=digest(b)
                elif case.startswith('rebound_'):
                    dest={'rebound_original':'original/STATEMENT.md','rebound_audit':'audit/AUDIT_REPORT.md',
                          'rebound_patch':'audit/LOW_DEGREE_CORRECTION.patch','rebound_corrected':'corrected/STATEMENT.md',
                          'rebound_manifest_anchor':'original/MANIFEST.json'}[case]
                    f=root/dest;f.write_bytes(f.read_bytes()+b'\n');expected=rebind(root)
                result=run(root/'verify_publication.py',mode,'--manifest-sha256',expected,'--integrity-only')
                require(result.returncode!=0,'corruption accepted: '+case)
                results.append({'case':case,'mode':'optimized' if mode else 'normal','rejected':True})
        # Direct checker failures reach the mathematical controls, without integrity gates.
        with tempfile.TemporaryDirectory(prefix='motivic-checker-failure-') as td:
            root=Path(td)
            author=(packet/'original/checks.py').read_text()
            require(author.count('# All subgroups')==1,'author mutation insertion changed')
            author=author.replace('# All subgroups',"check('publication_deliberate_failure', False)\n\n# All subgroups",1)
            (root/'author.py').write_text(author)
            result=run(root/'author.py',mode)
            require(result.returncode!=0 and b'publication_deliberate_failure' in result.stderr,'author false check did not fail')
            independent=(packet/'audit/independent_controls.py').read_text()
            require(independent.count('def finite_group(moduli):')==1,'audit mutation insertion changed')
            independent=independent.replace('def finite_group(moduli):',"require(False, 'publication_deliberate_failure')\n\ndef finite_group(moduli):",1)
            (root/'independent.py').write_text(independent)
            result=run(root/'independent.py',mode)
            require(result.returncode!=0 and b'publication_deliberate_failure' in result.stderr,'independent false check did not fail')
            results.extend({'case':case,'mode':'optimized' if mode else 'normal','rejected':True}
                           for case in ('author_explicit_failure','independent_explicit_failure'))
    print(json.dumps({'status':'PASS','negative_controls':len(results),'results':results,
                      'limits':'Disposable integrity and finite-control tests; no motivic theorem is certified.'},indent=2,sort_keys=True))

if __name__=='__main__':main()
