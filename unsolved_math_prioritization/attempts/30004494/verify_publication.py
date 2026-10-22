#!/usr/bin/env python3
"""Strict delivery integrity and replay controls; no mathematical proof formalization."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile, zipfile

PACKAGES = {
 'hodge_30004494': ('HODGE_30004494_AUTHOR_SAFE_FREEZE.zip','2880eb1f6345f6326c5b4ed8ab05801aa3c5db71d07e5a383472c74d69bcddbe','1b384c58531496829886e4a0a96820dad434ea796a3c36b96f532e5b6c6a8571',10),
 'hodge_30004494_v2': ('HODGE_30004494_V2_SAFE_FREEZE.zip','1cbc6d90a8de7a92094570e9304f0b187ad8d5a8335fbe1546b7c8b09efba8dd','8830a464eb9388fa980bc090bd44e17f548a860b39f686ffb45041689ef702c1',10),
 'hodge_30004494_independent_audit': ('HODGE_30004494_INDEPENDENT_AUDIT_SAFE_FREEZE.zip','48468ecb45f139badd88570fc52a86dd79af4c7baf7d38fa2cb74d3d0ac4bc78','62ef10b64024f32e58edaa3f53bd6dcf716c4833d967d01d98016913e05fc1fe',8),
 'hodge_30004494_v2_delta_audit': ('HODGE_30004494_V2_DELTA_ACCEPTANCE_SAFE_FREEZE.zip','bf4ab553e5abdc14290fe84aae9705ab977463f01005d965de7d218268759732','958ccb6d5de8efe494cf706fa4ad2b6c47a583f1d64833871b4f310b4e7bffd5',6),
}
PATCH='HODGE_30004494_V2_FROM_V1.patch'
PATCH_SHA='f384681f53cb6271f593d031c5de483dd60ba98ae12bd92cdb729225f8be6156'
MANIFEST='PUBLICATION_MANIFEST.json'

def require(test,message):
    if not test: raise ValueError(message)

def digest(b): return hashlib.sha256(b).hexdigest()

def read(p):
    require(p.is_file() and not p.is_symlink(), 'Nonregular or linked file: '+str(p))
    return p.read_bytes()

def safe_path(s):
    p=PurePosixPath(s)
    require(bool(s) and not p.is_absolute() and all(x not in ('','.','..') for x in p.parts) and str(p)==s,'Unsafe path: '+s)
    return s

def exact_inventory(root,expected):
    require(root.is_dir() and not root.is_symlink(),'Nonregular root')
    got_files=set();got_dirs=set()
    for p in root.rglob('*'):
        require(not p.is_symlink(),'Symlink: '+str(p))
        rel=p.relative_to(root).as_posix()
        if p.is_dir():got_dirs.add(rel)
        else: require(p.is_file(),'Special file: '+rel);got_files.add(rel)
    exp_dirs=set()
    for s in expected:
        for par in PurePosixPath(s).parents:
            if str(par)!='.':exp_dirs.add(str(par))
    require(got_files==set(expected),'File inventory mismatch')
    require(got_dirs==exp_dirs,'Directory inventory mismatch')

def verify_files(root,pin=None):
    mb=read(root/MANIFEST)
    if pin is not None: require(digest(mb)==pin,'External manifest binding mismatch')
    m=json.loads(mb);entries=m['files']; names=[safe_path(e['path']) for e in entries]
    require(len(names)==len(set(names)) and MANIFEST not in names,'Invalid manifest entries')
    require(m['problem_id']=='30004494' and m['status']=='unsolved' and m['turns']=='5/5','Publication disposition drift')
    exact_inventory(root,set(names)|{MANIFEST})
    for e in entries:
        b=read(root/e['path']); require(len(b)==e['bytes'] and digest(b)==e['sha256'],'Publication entry mismatch: '+e['path'])
    expected={MANIFEST,'PUBLICATION_STATUS.json','README.md','verify_publication.py',PATCH}
    for folder,(archive,ah,mh,count) in PACKAGES.items():
        ab=read(root/archive);require(digest(ab)==ah,'Archive pin mismatch: '+archive)
        manifest_bytes=read(root/folder/'MANIFEST.json');require(digest(manifest_bytes)==mh,'Package manifest pin mismatch: '+folder)
        fm=json.loads(manifest_bytes); fnames=[safe_path(e['path']) for e in fm['files']]
        require(len(fnames)==len(set(fnames)) and 'MANIFEST.json' not in fnames,'Duplicate package entry')
        require(len(fnames)+1==count,'Frozen package count mismatch')
        exact_inventory(root/folder,set(fnames)|{'MANIFEST.json'})
        for e in fm['files']:
            b=read(root/folder/e['path']);require(len(b)==e['bytes'] and digest(b)==e['sha256'],'Frozen entry mismatch: '+folder+'/'+e['path'])
        with zipfile.ZipFile(root/archive) as z:
            zexpected={folder+'/'+n for n in fnames}|{folder+'/MANIFEST.json'}
            require(set(z.namelist())==zexpected and len(z.namelist())==count,'Archive inventory mismatch')
            for name in z.namelist():require(z.read(name)==read(root/name),'Archive byte mismatch: '+name)
        expected|={archive}|{folder+'/'+n for n in fnames}|{folder+'/MANIFEST.json'}
    require(set(names)|{MANIFEST}==expected,'Unexpected publication manifest scope')
    require(digest(read(root/PATCH))==PATCH_SHA,'Patch pin mismatch')
    v1=root/'hodge_30004494';v2=root/'hodge_30004494_v2'
    for n in ['PROOFS.md','verify.py','VERIFICATION.json']:require(read(v1/n)==read(v2/n),'Unchanged proof/code/output drift')
    status=json.loads(read(root/'PUBLICATION_STATUS.json'))
    require(status['status']=='unsolved' and status['turns']=='5/5' and status['overall_audit_verdict']=='PASS_SCOPED_PARTIAL_RESULTS','Invalid current status')
    for field in ('complete_solution','counterexample_to_original_target','novelty_claim','formal_geometric_verification','external_human_peer_review'):require(status[field] is False,'Unapproved scope upgrade: '+field)
    require(status['controlling_revision']=='hodge_30004494_v2' and status['controlling_acceptance']=='hodge_30004494_v2_delta_audit/DELTA_ACCEPTANCE.json','Wrong authority')
    acceptance=json.loads(read(root/status['controlling_acceptance']))
    require(acceptance['verdict']=='PASS_DELTA_M1_ACCEPTED' and acceptance['resolved_corrections']==['M1'] and acceptance['remaining_mandatory_corrections']==[],'Delta not accepted')
    require(acceptance['original_target_status']=='unsolved' and acceptance['turns_used']==acceptance['turn_limit']==5,'Target status changed')
    return digest(mb),len(expected)

def replay(root):
    env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
    jobs=[
      ('author_v1',['hodge_30004494/verify.py'],'hodge_30004494/VERIFICATION.json'),
      ('author_v2',['hodge_30004494_v2/verify.py'],'hodge_30004494_v2/VERIFICATION.json'),
      ('independent',['hodge_30004494_independent_audit/independent_verify.py','--author',str(root/'hodge_30004494'),'--archive',str(root/PACKAGES['hodge_30004494'][0])],'hodge_30004494_independent_audit/INDEPENDENT_VERIFICATION.json'),
      ('delta',['hodge_30004494_v2_delta_audit/verify_delta.py','--root',str(root)],'hodge_30004494_v2_delta_audit/DELTA_VERIFICATION.json'),
    ]
    for label,args,expected in jobs:
        args[0]=str(root/args[0]);r=subprocess.run([sys.executable,'-I',*args],cwd=root,capture_output=True,env=env)
        require(r.returncode==0,label+' replay failed: '+r.stderr.decode(errors='replace'))
        require(not r.stderr and r.stdout==read(root/expected),label+' output differs')
    with tempfile.TemporaryDirectory(prefix='hodge_patch_') as t:
        out=Path(t)/'reconstructed';shutil.copytree(root/'hodge_30004494',out)
        r=subprocess.run(['patch','--batch','--forward','--fuzz=0','-p1','-i',str(root/PATCH)],cwd=out,capture_output=True)
        log=(r.stdout+r.stderr).decode(errors='replace').lower();require(r.returncode==0 and 'fuzz' not in log and 'offset' not in log,'Patch did not apply exactly')
        target=root/'hodge_30004494_v2';require({p.name for p in out.iterdir()}=={p.name for p in target.iterdir()},'Patched inventory differs')
        for p in out.iterdir():require(read(p)==read(target/p.name),'Patch reconstruction differs: '+p.name)

def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest-sha256');p.add_argument('--no-relocation',action='store_true',help='Skip only the second relocated replay');a=p.parse_args()
    root=Path(__file__).absolute().parent
    mh,count=verify_files(root,a.manifest_sha256);replay(root)
    if not a.no_relocation:
        with tempfile.TemporaryDirectory(prefix='hodge_relocated_') as t:
            other=Path(t)/'packet';shutil.copytree(root,other)
            require(verify_files(other,mh)==(mh,count),'Relocated integrity differs');replay(other)
    require(verify_files(root,mh)==(mh,count),'Input drift during replay')
    print(json.dumps({'result':'PASS','problem_id':'30004494','status':'unsolved','turns':'5/5','packet_files':count,'publication_manifest_sha256':mh,'author_finite_controls':18549,'independent_finite_controls':33222,'archives_exact':4,'patch_reconstruction_byte_exact':True,'M1':'PASS_DELTA_M1_ACCEPTED','original_adverse_audit_preserved':True,'relocated_replay':not a.no_relocation,'frozen_runners_assertions_enabled':True,'scope':'Delivery integrity, exact patch, and finite controls only; no complete solution or novelty claim.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
