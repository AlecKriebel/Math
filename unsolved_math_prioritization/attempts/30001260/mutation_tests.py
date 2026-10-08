#!/usr/bin/env python3
"""Reject deliberate packet damage in isolated normal and optimized Python."""
import argparse, hashlib, json, pathlib, shutil, subprocess, sys, tempfile

def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def main(root,pin):
    root=pathlib.Path(root).resolve();verifier=root/'verify_publication.py'
    results={}
    cases=['clean','changed','same_size_change','missing','extra','empty_directory','symlink_file','symlink_directory','changed_manifest','wrong_pin','duplicate_path','unsafe_path','bad_size','bad_hash','duplicate_json_key','changed_archive_rehashed','changed_frozen_manifest_rehashed']
    for flags,label in (([],'normal'),(['-O'],'optimized')):
        for case in cases:
            with tempfile.TemporaryDirectory(prefix='s5-publication-control-') as tmp:
                dst=pathlib.Path(tmp)/'packet';shutil.copytree(root,dst);active=pin
                mf=dst/'PUBLIC_MANIFEST.json';target=dst/'author/TURN_1_LINEAR_OBSTRUCTION.md'
                if case=='changed':target.write_bytes(target.read_bytes()+b'X')
                elif case=='same_size_change':target.write_bytes(b'!'+target.read_bytes()[1:])
                elif case=='missing':target.unlink()
                elif case=='extra':(dst/'EXTRA').write_text('extra')
                elif case=='empty_directory':(dst/'EMPTY').mkdir()
                elif case=='symlink_file':target.unlink();target.symlink_to(root/'author/TURN_1_LINEAR_OBSTRUCTION.md')
                elif case=='symlink_directory':shutil.rmtree(dst/'author');(dst/'author').symlink_to(root/'author',target_is_directory=True)
                elif case=='changed_manifest':mf.write_bytes(mf.read_bytes()+b' ')
                elif case=='wrong_pin':active='0'*64
                elif case in ('duplicate_path','unsafe_path','bad_size','bad_hash'):
                    m=json.loads(mf.read_bytes())
                    if case=='duplicate_path':m['files'].append(m['files'][0].copy())
                    if case=='unsafe_path':m['files'][0]['path']='../outside'
                    if case=='bad_size':m['files'][0]['bytes']+=1
                    if case=='bad_hash':m['files'][0]['sha256']='0'*64
                    mf.write_text(json.dumps(m));active=hashlib.sha256(mf.read_bytes()).hexdigest()
                elif case=='duplicate_json_key':
                    text=mf.read_text();mf.write_text(text.replace('"schema": 1','"schema": 1, "schema": 1'));active=hashlib.sha256(mf.read_bytes()).hexdigest()
                elif case in ('changed_archive_rehashed','changed_frozen_manifest_rehashed'):
                    relative='archives/audit.zip' if case=='changed_archive_rehashed' else 'author/MANIFEST.json'
                    f=dst/relative;f.write_bytes(f.read_bytes()+b' ');m=json.loads(mf.read_bytes())
                    for r in m['files']:
                        if r['path']==relative:r['bytes']=f.stat().st_size;r['sha256']=hashlib.sha256(f.read_bytes()).hexdigest()
                    mf.write_text(json.dumps(m));active=hashlib.sha256(mf.read_bytes()).hexdigest()
                run=subprocess.run([sys.executable,'-I',*flags,str(verifier),active,'--root',str(dst),'--integrity-only'],capture_output=True,cwd=tmp)
                need((run.returncode==0)==(case=='clean'),label+' unexpected result '+case)
                results.setdefault(case,{})[label]='accepted' if run.returncode==0 else 'rejected'
    return {'status':'PASS','cases':results,'negative_cases_per_mode':len(cases)-1,'replay_scope':'Each mutation tests integrity rejection; full mathematical replay is performed separately.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('manifest_sha256');p.add_argument('--root',default=str(pathlib.Path(__file__).resolve().parent));a=p.parse_args();print(json.dumps(main(a.root,a.manifest_sha256),indent=2,sort_keys=True))
