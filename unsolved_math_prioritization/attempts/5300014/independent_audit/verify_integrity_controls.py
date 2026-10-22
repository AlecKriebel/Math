#!/usr/bin/env python3
"""Adversarial controls in disposable copies. Original inputs are never changed."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

def require(ok,msg):
    if not ok:raise RuntimeError(msg)

def run(root,mode,scope,pin):
    script='verify_audit.py' if scope=='audit' else 'verify_manifest.py'
    return subprocess.run([sys.executable,'-B']+mode+[str(root/script),'--expected-manifest',pin],cwd=root.parent,capture_output=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest',required=True);a=p.parse_args()
    root=Path(__file__).resolve().parent
    receipt=json.loads((root/'AUTHOR_FREEZE_RECEIPT.json').read_text())
    out={'positive_replays':[],'rejected_controls':{},'original_target_solved':False}
    modes=[[],['-O'],['-OO']]
    basic=['payload-tamper','extra-file','extra-directory','missing-file','manifest-rewrite','symlink-payload','wrong-external-pin']
    with tempfile.TemporaryDirectory(prefix='blaschke-audit-controls-') as t:
        tmp=Path(t)
        for scope,source,pin in [('author',root/'author',receipt['manifest_sha256']),('audit',root,a.expected_manifest)]:
            out['rejected_controls'][scope]=[]
            for mode in modes:
                label='normal' if not mode else mode[0]
                dest=tmp/('positive-'+scope+'-'+label);shutil.copytree(source,dest)
                r=run(dest,mode,scope,pin)
                require(r.returncode==0,'relocated positive failed: '+scope+' '+label+' '+r.stderr.decode())
                out['positive_replays'].append(scope+':'+label+':relocated')
                for control in basic+(['symlink-manifest'] if scope=='audit' else []):
                    dest=tmp/(scope+'-'+label+'-'+control);shutil.copytree(source,dest)
                    target=dest/('AUDIT_REPORT.md' if scope=='audit' else 'PROOF.md')
                    manifest=dest/('AUDIT_MANIFEST.json' if scope=='audit' else 'MANIFEST.json')
                    check_pin=pin
                    if control=='payload-tamper':target.write_bytes(target.read_bytes()+b'\nAUDIT_NEGATIVE_CONTROL\n')
                    elif control=='extra-file':(dest/'unexpected.txt').write_text('audit control')
                    elif control=='extra-directory':(dest/'unexpected_directory').mkdir()
                    elif control=='missing-file':target.unlink()
                    elif control=='manifest-rewrite':manifest.write_bytes(manifest.read_bytes()+b'\n')
                    elif control=='wrong-external-pin':check_pin='0'*64
                    elif control in ('symlink-payload','symlink-manifest'):
                        f=target if control=='symlink-payload' else manifest
                        external=tmp/(scope+'-'+label+'-'+control+'-target')
                        external.write_bytes(f.read_bytes());f.unlink();f.symlink_to(external)
                    r=run(dest,mode,scope,check_pin)
                    require(r.returncode!=0,'negative control accepted: '+scope+' '+label+' '+control)
                    out['rejected_controls'][scope].append(label+':'+control)
    out['negative_control_count']=sum(len(v) for v in out['rejected_controls'].values())
    out['original_inputs_preserved']=True
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
