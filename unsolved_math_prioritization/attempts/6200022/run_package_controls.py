#!/usr/bin/env python3
"""Replay frozen mutation suite plus publication controls, only in temporary copies."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).absolute().parent
def need(v,m):
    if not v:raise RuntimeError('CONTROL FAILURE: '+m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def run(root,opt,pin):return subprocess.run([sys.executable,'-I']+(['-O'] if opt else [])+[str(root/'verify_package.py'),'--expected-manifest',pin],cwd='/',capture_output=True,text=True,timeout=180)
def refresh(root,name):
    p=root/'PUBLICATION_MANIFEST.json';d=read(p)
    for row in d['files']:
        if row['path']==name:row.update(bytes=(root/name).stat().st_size,sha256=sha(root/name))
    write(p,d)
def main():
    pin=sha(ROOT/'PUBLICATION_MANIFEST.json');rows=[];clean=[]
    r=subprocess.run([sys.executable,'-I',str(ROOT/'audit/test_integrity.py'),'--author-archive',str(ROOT/'archives/KLEINIAN_BOUNDARY_6200022_AUTHOR_SAFE_FREEZE.zip')],cwd='/',capture_output=True,text=True,timeout=300)
    need(r.returncode==0,'frozen controls: '+r.stderr);frozen=json.loads(r.stdout);need(frozen==read(ROOT/'audit/VERIFY_TESTS.json'),'full frozen receipt replay')
    with tempfile.TemporaryDirectory(prefix='diagonal-publication-') as td:
        tmp=Path(td);moved=tmp/'path with spaces'/'moved';shutil.copytree(ROOT,moved)
        for label,p in [('original',ROOT),('relocated',moved)]:
            for opt in (False,True):
                r=run(p,opt,pin);need(r.returncode==0,label+r.stderr);d=json.loads(r.stdout);d.pop('optimized');clean.append(d);rows.append({'case':label,'optimized':opt,'passed':True})
        need(all(d==clean[0] for d in clean),'mode/relocation output agreement')
        names=['changed_proof','same_size_results','missing_file','extra_file','extra_directory','nested_manifest','damaged_zip','changed_manifest','unsafe_path','member_symlink','self_symlink','ancestor_symlink','wrong_external_pin','duplicate_key','boolean_size','rehashed_wrong_disposition','rehashed_false_novelty','rehashed_wrong_target']
        for name in names:
            p=tmp/name;shutil.copytree(moved,p);usepin=pin;m=p/'PUBLICATION_MANIFEST.json'
            if name=='changed_proof':q=p/'author/RESULT.md';q.write_bytes(q.read_bytes()+b'changed')
            elif name=='same_size_results':q=p/'author/CHECK_RESULTS.json';b=q.read_bytes();need(b'77142' in b,'fixture');q.write_bytes(b.replace(b'77142',b'77143',1))
            elif name=='missing_file':(p/'audit/AUDIT.md').unlink()
            elif name=='extra_file':(p/'extra.txt').write_text('extra')
            elif name=='extra_directory':(p/'empty').mkdir()
            elif name=='nested_manifest':q=p/'author/extra';q.mkdir();(q/'MANIFEST.json').write_text('{}')
            elif name=='damaged_zip':q=next((p/'archives').glob('*.zip'));b=q.read_bytes();q.write_bytes(b[:15]+bytes([b[15]^1])+b[16:])
            elif name=='changed_manifest':m.write_bytes(m.read_bytes()+b' ')
            elif name=='unsafe_path':d=read(m);d['files'][0]['path']='../escape';write(m,d);usepin=sha(m)
            elif name=='member_symlink':q=p/'author/RESULT.md';q.unlink();q.symlink_to(moved/'author/RESULT.md')
            elif name=='self_symlink':q=p/'verify_package.py';q.unlink();q.symlink_to(moved/'verify_package.py')
            elif name=='ancestor_symlink':alias=tmp/'alias';alias.symlink_to(tmp,target_is_directory=True);p=alias/p.name
            elif name=='wrong_external_pin':usepin='0'*64
            elif name=='duplicate_key':m.write_text(m.read_text().replace('{','{"problem_id":6200022,',1));usepin=sha(m)
            elif name=='boolean_size':d=read(m);d['files'][0]['bytes']=True;write(m,d);usepin=sha(m)
            elif name.startswith('rehashed_'):
                q=p/'VERDICT.json';d=read(q)
                if name=='rehashed_wrong_disposition':d['classification']='verified_solved'
                elif name=='rehashed_false_novelty':d['novelty_claimed']=True
                else:d['problem_id']=6200021
                write(q,d);refresh(p,'VERDICT.json');usepin=sha(m)
            for opt in (False,True):
                r=run(p,opt,usepin);need(r.returncode!=0 and 'PACKAGE FAILURE:' in r.stderr,'accepted or non-explicit rejection: '+name);rows.append({'case':name,'optimized':opt,'rejected':True})
    print(json.dumps({'status':'PASS','problem_id':6200022,'publication_positive_runs':4,'publication_negative_runs':36,'frozen_author_positive_runs':4,'frozen_author_negative_runs':28,'frozen_audit_positive_runs':4,'frozen_audit_negative_runs':28,'frozen_receipt_reproduced':True,'normalized_outputs_agree':True,'controls':rows},indent=2,sort_keys=True))
if __name__=='__main__':main()
