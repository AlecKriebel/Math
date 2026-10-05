#!/usr/bin/env python3
"""Relocation and mutation tests on disposable copies; no freeze is edited."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

def need(ok, why):
    if not ok:
        raise ValueError(why)

def inventory(root):
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('root',type=Path)
    ap.add_argument('expected_manifest')
    ap.add_argument('--queue',required=True,type=Path)
    args=ap.parse_args()
    root=args.root.resolve(); queue=args.queue.resolve(); before=inventory(root)
    tests=[]
    with tempfile.TemporaryDirectory(prefix='root unity publication controls ') as tmp:
        tmp=Path(tmp)
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
        def run(target, optimized=False, pin=None, q=queue, replay=False):
            cmd=[sys.executable,*(['-O'] if optimized else []),str(root/'verify_publication.py'),str(target),pin or args.expected_manifest,'--queue',str(q)]
            if replay: cmd.append('--replay')
            return subprocess.run(cmd,cwd=tmp,env=env,capture_output=True,text=True,timeout=1200)
        moved=tmp/'relocated packet with spaces'; shutil.copytree(root,moved)
        for optimized in [False,True]:
            p=run(moved,optimized,replay=True)
            need(p.returncode==0,'relocated full replay failed: '+p.stderr)
            result=json.loads(p.stdout)
            if not optimized: expected=result
            need(result==expected,'normal/optimized relocation differs')
            tests.append({'case':'relocated_full_replay','optimized':optimized,'passed':True})
        cases=['missing_author','missing_audit','changed_proof','changed_audit','changed_verifier','unlisted_file','unlisted_directory','manifest_whitespace','duplicate_manifest_entry','duplicate_json_key','coherently_rehashed_payload','author_manifest_symlink','audit_manifest_symlink','publication_manifest_symlink','payload_symlink','directory_symlink','root_symlink','scope_status']
        for case in cases:
            target=tmp/case
            if case=='root_symlink': target.symlink_to(root,target_is_directory=True)
            else:
                shutil.copytree(root,target)
                if case=='missing_author': shutil.rmtree(target/'author')
                elif case=='missing_audit': shutil.rmtree(target/'audit')
                elif case in ('changed_proof','changed_audit','changed_verifier','manifest_whitespace'):
                    name={'changed_proof':'author/PROOFS.md','changed_audit':'audit/AUDIT_REPORT.md','changed_verifier':'verify_publication.py','manifest_whitespace':'PUBLICATION_MANIFEST.json'}[case]
                    p=target/name; p.write_bytes(p.read_bytes()+b'\n')
                elif case=='unlisted_file': (target/'unexpected.txt').write_text('mutation')
                elif case=='unlisted_directory': (target/'unexpected').mkdir()
                elif case=='duplicate_manifest_entry':
                    p=target/'PUBLICATION_MANIFEST.json'; m=json.loads(p.read_text()); m['files'].append(m['files'][0]); p.write_text(json.dumps(m))
                elif case=='duplicate_json_key':
                    p=target/'PUBLICATION_MANIFEST.json'; p.write_text('{"problem_id":"30004334",'+p.read_text().lstrip()[1:])
                elif case=='coherently_rehashed_payload':
                    p=target/'author/PROOFS.md'; p.write_bytes(p.read_bytes()+b'\n'); m=json.loads((target/'PUBLICATION_MANIFEST.json').read_text())
                    for f in m['files']:
                        if f['path']=='author/PROOFS.md': f.update(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                    (target/'PUBLICATION_MANIFEST.json').write_text(json.dumps(m))
                elif case in ('author_manifest_symlink','audit_manifest_symlink','publication_manifest_symlink','payload_symlink'):
                    name={'author_manifest_symlink':'author/AUTHOR_MANIFEST.json','audit_manifest_symlink':'audit/AUDIT_MANIFEST.json','publication_manifest_symlink':'PUBLICATION_MANIFEST.json','payload_symlink':'author/PROOFS.md'}[case]
                    p=target/name; p.unlink(); p.symlink_to(root/name)
                elif case=='directory_symlink': shutil.rmtree(target/'author'); (target/'author').symlink_to(root/'author',target_is_directory=True)
                elif case=='scope_status':
                    p=target/'PUBLICATION_STATUS.json'; s=json.loads(p.read_text()); s['status']='solved'; p.write_text(json.dumps(s))
            for optimized in [False,True]:
                p=run(target,optimized)
                need(p.returncode!=0,'mutation accepted: '+case)
                tests.append({'case':case,'optimized':optimized,'rejected':True})
        badqueue=tmp/'bad queue.md'; badqueue.write_bytes(queue.read_bytes()+b'\n')
        for optimized in [False,True]:
            need(run(root,optimized,pin='0'*64).returncode!=0,'wrong external pin accepted')
            tests.append({'case':'wrong_external_pin','optimized':optimized,'rejected':True})
            need(run(root,optimized,q=badqueue).returncode!=0,'wrong queue accepted')
            tests.append({'case':'wrong_queue','optimized':optimized,'rejected':True})
    need(inventory(root)==before,'original freeze changed')
    print(json.dumps({'status':'PASS','relocated_normal_optimized_replays':2,'negative_controls':40,'original_freeze_unchanged':True,'tests':tests},indent=2,sort_keys=True))

if __name__=='__main__':
    main()
