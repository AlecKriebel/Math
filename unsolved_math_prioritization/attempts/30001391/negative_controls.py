#!/usr/bin/env python3
"""Reject isolated temporary corruption without modifying this release."""
from pathlib import Path
import json,shutil,subprocess,sys,tempfile
P=Path(__file__).resolve().parent

def mutate(q,name):
    if name=='author_body':
        with (q/'submission/PARTIAL_PROOF.md').open('a') as f:f.write('\nmutation\n')
    elif name=='author_manifest':
        with (q/'submission/SHA256SUMS.json').open('a') as f:f.write(' ')
    elif name=='audit_body':
        with (q/'audit/AUDIT_REPORT.md').open('a') as f:f.write('\nmutation\n')
    elif name=='audit_manifest':
        with (q/'audit/AUDIT_MANIFEST.json').open('a') as f:f.write(' ')
    elif name=='missing_payload':(q/'RELEASE_ADDENDUM.md').unlink()
    elif name=='extra_payload':(q/'extra.txt').write_text('extra')
    elif name=='extra_manifest_named_file':(q/'audit/SHA256SUMS.json').write_text('{}')
    elif name=='extra_empty_directory':(q/'unexpected').mkdir()
    elif name=='payload_symlink':
        a=q/'README.md';a.unlink();a.symlink_to('submission/README.md')
    elif name=='selfconsistent_author_corruption':
        a=q/'submission/PARTIAL_PROOF.md';a.write_text(a.read_text()+'\nmutation\n')
        import hashlib
        m=json.loads((q/'RELEASE_MANIFEST.json').read_text());b=a.read_bytes();m['files']['submission/PARTIAL_PROOF.md']={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};(q/'RELEASE_MANIFEST.json').write_text(json.dumps(m))
    else:raise ValueError(name)

def main():
    names=['author_body','author_manifest','audit_body','audit_manifest','missing_payload','extra_payload','extra_manifest_named_file','extra_empty_directory','payload_symlink','selfconsistent_author_corruption']
    rows=[]
    with tempfile.TemporaryDirectory() as t:
        for name in names:
            q=Path(t)/name;shutil.copytree(P,q);mutate(q,name)
            for optimized in [False,True]:
                r=subprocess.run([sys.executable,'-B',*(['-O'] if optimized else []),str(q/'verify_release.py')],cwd=q,capture_output=True,text=True)
                if r.returncode==0:raise RuntimeError('mutation was accepted: '+name)
                rows.append({'mutation':name,'optimized_python':optimized,'rejected':True})
    return {'result':'PASS','negative_controls':len(rows),'all_rejected':True,'controls':rows,'limits':'Integrity corruption controls only; not mathematical counterexample search.'}
if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
