#!/usr/bin/env python3
"""Independent current-package controls, one disposable case at a time."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

A=Path(__file__).resolve().parents[1];R=A/'package_review_01'
T=A.parents[1]/'work/pr822_revision_r1'
def sha(b):return hashlib.sha256(b).hexdigest()
def need(c,m):
    if not c:raise RuntimeError(m)
records=[]
for family in ('portable','outer'):
    for optimize in (False,True):
        for case in ('baseline','extra file','extra empty directory','missing note','symlink note',
                     'FIFO note','same-size changed note','changed note with rehashed manifest'):
            with tempfile.TemporaryDirectory(prefix='R1 independent integrity case with spaces ') as td:
                root=Path(td)/'test package with spaces'
                if family=='portable':
                    root.mkdir()
                    with zipfile.ZipFile(A/'preprint/verification.zip') as z:z.extractall(root)
                    note=root/'note.tex';manifest=root/'package_index.json';script=root/'verify_package.py'
                else:
                    shutil.copytree(T,root)
                    note=root/'publication_20261013/preprint/note.tex'
                    manifest=root/'PUBLICATION_MANIFEST.json';script=root/'verify_publication.py'
                pin=sha(manifest.read_bytes())
                if case=='extra file':(root/'unexpected').write_text('x')
                elif case=='extra empty directory':(root/'unexpected').mkdir()
                elif case=='missing note':note.unlink()
                elif case=='symlink note':
                    note.unlink();note.symlink_to(A/'preprint/note.tex')
                elif case=='FIFO note':
                    note.unlink();os.mkfifo(note)
                elif case.startswith('same-size') or case.startswith('changed'):
                    b=note.read_bytes();note.write_bytes(b'!'+b[1:])
                    if case.startswith('changed'):
                        data=json.loads(manifest.read_bytes())
                        for row in data['files']:
                            b=(root/row['path']).read_bytes()
                            row['bytes']=len(b);row['sha256']=sha(b)
                        manifest.write_text(json.dumps(data,indent=2)+'\n')
                command=[sys.executable,'-I','-B']+(['-O'] if optimize else [])+[str(script),pin]
                p=subprocess.run(command,cwd='/',capture_output=True,text=True,timeout=30)
                accepted=p.returncode==0;expected=case=='baseline'
                need(accepted==expected,family+' '+case+' unexpected acceptance')
                records.append({'family':family,'optimized':optimize,'case':case,'accepted':accepted,
                                'expected_acceptance':expected,'exit_code':p.returncode,
                                'stderr':p.stderr,'stdout_sha256':sha(p.stdout.encode())})

# The copied current root-level historical control harness is executable but incompatible.
with tempfile.TemporaryDirectory(prefix='R1 stale public tool reproduction ') as td:
    root=Path(td)/'published assembly with spaces';shutil.copytree(T,root)
    p=subprocess.run([sys.executable,'-I','-B',str(root/'package_controls.py')],
                     cwd='/',capture_output=True,text=True,timeout=60)
    need(p.returncode!=0 and 'wrong acceptance: relocated exact package' in p.stderr,'stale control baseline failure not reproduced')
    obsolete={'tool':'current outer package_controls.py','exit_code':p.returncode,'stderr':p.stderr}
    cli=subprocess.run([sys.executable,'-I','-B',str(root/'verify_publication.py'),
                       '--root',str(root),'--integrity-only'],cwd='/',capture_output=True,text=True,timeout=30)
    need(cli.returncode!=0 and 'unrecognized arguments: --root' in cli.stderr,'obsolete interface cause not reproduced')
    obsolete['obsolete_child_cli']={'exit_code':cli.returncode,'stderr':cli.stderr}
    p=subprocess.run([sys.executable,'-I','-B',str(root/'publication_20261013/preprint/build_verification.py')],
                     cwd='/',capture_output=True,text=True,timeout=60)
    need(p.returncode!=0 and 'SOURCE_MANIFEST.json' in p.stderr,'missing published builder layout not reproduced')
    builder={'tool':'current published preprint/build_verification.py','exit_code':p.returncode,'stderr':p.stderr}

result={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_EXPECTED_CONTROLS',
        'current_controls':records,'total':len(records),'accepted_baselines':4,'expected_rejections':28,
        'obsolete_top_level_control':obsolete,'nonportable_advertised_builder':builder,
        'mutations_confined_to_disposable_copies':True,'sealed_inputs_changed':False}
(R/'INTEGRITY_CONTROL_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='current_controls'},indent=2))
