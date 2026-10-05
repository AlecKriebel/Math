#!/usr/bin/env python3
"""Negative integrity controls on disposable copies; no source inputs needed."""
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--expected-manifest-sha256',required=True);a=p.parse_args()
    root=Path(__file__).resolve().parent
    tests=['alter_payload','alter_archive','extra_file','extra_empty_directory','missing_file','payload_symlink',
           'wrong_manifest_pin','duplicate_manifest_path','unsafe_manifest_path','duplicate_json_key','frozen_archive_repin']
    results=[]
    with tempfile.TemporaryDirectory(prefix='kahler-negative-controls-') as tmp:
        for optimize in [False, True]:
            for kind in tests:
                dest=Path(tmp)/'packet';shutil.copytree(root,dest);pin=a.expected_manifest_sha256
                mf=dest/'PUBLICATION_MANIFEST.json'
                if kind=='alter_payload': (dest/'author/PROOF.md').write_bytes(b'altered')
                elif kind=='alter_archive':
                    f=dest/'archives/KAHLER_KOSZUL_30005418_AUTHOR_SAFE_FREEZE.zip';f.write_bytes(f.read_bytes()+b'altered')
                elif kind=='extra_file': (dest/'author/extra.json').write_text('{}')
                elif kind=='extra_empty_directory': (dest/'extra').mkdir()
                elif kind=='missing_file': (dest/'author/PROOF.md').unlink()
                elif kind=='payload_symlink':
                    f=dest/'author/PROOF.md';f.unlink();f.symlink_to('README.md')
                elif kind=='wrong_manifest_pin': pin='0'*64
                elif kind=='duplicate_json_key':
                    mf.write_text(mf.read_text().replace('"schema": 1','"schema": 1, "schema": 1',1));pin=hashlib.sha256(mf.read_bytes()).hexdigest()
                else:
                    m=json.loads(mf.read_text())
                    if kind=='duplicate_manifest_path': m['files'].append(m['files'][0])
                    elif kind=='unsafe_manifest_path': m['files'][0]['path']='../escape'
                    elif kind=='frozen_archive_repin':
                        rel='archives/KAHLER_KOSZUL_30005418_AUTHOR_SAFE_FREEZE.zip';f=dest/rel;f.write_bytes(f.read_bytes()+b'altered')
                        e=next(x for x in m['files'] if x['path']==rel);e.update(bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest())
                    mf.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n');pin=hashlib.sha256(mf.read_bytes()).hexdigest()
                command=[sys.executable]+(['-O'] if optimize else [])+['-B',str(dest/'verify_publication.py'),'--expected-manifest-sha256',pin,'--integrity-only']
                r=subprocess.run(command,capture_output=True,text=True)
                if r.returncode==0 or 'FAIL:' not in r.stderr: raise RuntimeError('negative control did not reject: '+kind)
                results.append({'test':kind,'outer_optimized':optimize,'rejected':True});shutil.rmtree(dest)
    print(json.dumps({'status':'PASS','negative_controls':len(results),'results':results},indent=2,sort_keys=True))

if __name__=='__main__': main()
