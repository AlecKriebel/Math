#!/usr/bin/env python3
"""Exercise the externally authenticated bootstrap against mutated copies."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent.parent
BOOT=ROOT/'bootstrap.py'

def need(ok,message):
    if not ok: raise ValueError(message)

def run(root,flags):
    return subprocess.run([sys.executable,'-I','-S','-B',*flags,str(BOOT),'--root',str(root)],text=True,capture_output=True,timeout=90)

def main():
    need(BOOT.is_file(),'run this control script from the frozen author directory')
    positives=negatives=0
    mutations=['proof_append','claim_status','claim_and_manifest','manifest_empty','bootstrap_append','extra_file','extra_directory','missing_payload','payload_symlink','author_symlink','root_symlink','swap_payload','truncated_payload']
    with tempfile.TemporaryDirectory(prefix='sublamination-boundary-') as td:
        temp=Path(td)
        for flags in ([],['-O'],['-OO']):
            good=temp/'good'; shutil.copytree(ROOT,good)
            p=run(good,flags); need(p.returncode==0 and not p.stderr,'valid relocated boundary failed'); positives+=1
            shutil.rmtree(good)
            for kind in mutations:
                root=temp/'case'; shutil.copytree(ROOT,root)
                a=root/'author'
                if kind=='proof_append':
                    with (a/'PROOF.md').open('ab') as f: f.write(b'changed')
                elif kind in ('claim_status','claim_and_manifest'):
                    q=json.loads((a/'CLAIMS.json').read_text());q['status']='claimed_solved';(a/'CLAIMS.json').write_text(json.dumps(q))
                    if kind=='claim_and_manifest':
                        m=json.loads((root/'MANIFEST.json').read_text());b=(a/'CLAIMS.json').read_bytes();m['files']['author/CLAIMS.json']={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};(root/'MANIFEST.json').write_text(json.dumps(m))
                elif kind=='manifest_empty': (root/'MANIFEST.json').write_text('{}')
                elif kind=='bootstrap_append':
                    with (root/'bootstrap.py').open('ab') as f: f.write(b'\n# altered\n')
                elif kind=='extra_file': (a/'unlisted.txt').write_text('unlisted')
                elif kind=='extra_directory': (a/'unlisted').mkdir()
                elif kind=='missing_payload': (a/'PROOF.md').unlink()
                elif kind=='payload_symlink':
                    (a/'PROOF.md').unlink();(a/'PROOF.md').symlink_to(ROOT/'author'/'PROOF.md')
                elif kind=='author_symlink':
                    shutil.rmtree(a);a.symlink_to(ROOT/'author',target_is_directory=True)
                elif kind=='root_symlink':
                    shutil.rmtree(root);root.symlink_to(ROOT,target_is_directory=True)
                elif kind=='swap_payload':
                    b=(a/'PROOF.md').read_bytes();(a/'PROOF.md').write_bytes((a/'README.md').read_bytes());(a/'README.md').write_bytes(b)
                elif kind=='truncated_payload': (a/'SOURCE_PINS.json').write_bytes(b'{')
                p=run(root,flags)
                need(p.returncode!=0 and not p.stdout and p.stderr,'mutation accepted or improper rejection: '+kind)
                negatives+=1
                if root.is_symlink(): root.unlink()
                else: shutil.rmtree(root)
    print(json.dumps({'status':'PASS_OUTER_BOUNDARY_CONTROLS','positive_relocated_runs':positives,'rejected_mutated_runs':negatives,'inner_modes':['normal','-O','-OO'],'mutation_classes':mutations},sort_keys=True))

if __name__=='__main__':
    try: main()
    except (ValueError,OSError,subprocess.SubprocessError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(2)
