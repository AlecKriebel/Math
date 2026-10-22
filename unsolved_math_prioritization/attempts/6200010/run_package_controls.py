#!/usr/bin/env python3
"""Clean relocation, historical defect reproduction and hostile mutations."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).absolute().parent
def need(v,m):
    if not v:raise RuntimeError('CONTROL FAILURE: '+m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def run(root,script,opt,pin=None):
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
    return subprocess.run([sys.executable]+(['-O'] if opt else [])+[str(root/script)]+(['--expected-manifest',pin] if pin else []),cwd=root.parent,env=env,capture_output=True,text=True,timeout=240)
def refresh(root,name):
    p=root/'AUDIT_MANIFEST.json';m=read(p)
    for e in m['files']:
        if e['path']==name:e.update(bytes=(root/name).stat().st_size,sha256=sha(root/name))
    write(p,m)
def audit_mutation(root,name):
    p=root/'AUDIT_MANIFEST.json';m=read(p)
    if name=='changed_author_result':(root/'author/CHECK_RESULTS.json').write_text('{}\n')
    elif name=='missing_file':(root/'README.md').unlink()
    elif name=='extra_file':(root/'extra.txt').write_text('extra')
    elif name in ['nested_manifest','nested_author_manifest']:
        dest=root/('unexpected' if name=='nested_manifest' else 'author/unexpected');dest.mkdir();(dest/'MANIFEST.json').write_text('{}\n')
    elif name=='symlink':(root/'linked').symlink_to('README.md')
    elif name=='duplicate_entry':m['files'].append(dict(m['files'][0]));write(p,m)
    elif name=='wrong_identity':m['problem_id']=6200004;write(p,m)
    elif name=='traversal':m['files'][0]['path']='../outside';write(p,m)
    elif name=='noncanonical':m['files'][0]['path']='./'+m['files'][0]['path'];write(p,m)
    elif name=='invalid_size':m['files'][0]['bytes']=-1;write(p,m)
    elif name=='duplicate_json_key':p.write_text(p.read_text().replace('{','{"problem_id":6200010,',1))
    elif name=='resigned_wrong_disposition':
        q=root/'AUDIT_STATUS.json';d=read(q);d['original_problem_resolved']=True;write(q,d);refresh(root,'AUDIT_STATUS.json')
    elif name=='resigned_wrong_independent_result':
        q=root/'INDEPENDENT_RESULTS.json';d=read(q);d['checks']=0;write(q,d);refresh(root,'INDEPENDENT_RESULTS.json')
    elif name=='resigned_author_change':
        q=root/'author/RESULT.md';q.write_text(q.read_text()+'\nUnexpected change.\n');refresh(root,'author/RESULT.md')
    else:need(False,'unknown mutation')
def main():
    pin=sha(ROOT/'PUBLICATION_MANIFEST.json');rows=[];normalized=[]
    with tempfile.TemporaryDirectory(prefix='kleinian-publication-controls-') as td:
        tmp=Path(td);clean=tmp/'relocated';shutil.copytree(ROOT,clean)
        for label,root in [('original',ROOT),('relocated',clean)]:
            for opt in (False,True):
                r=run(root,'verify_package.py',opt,pin);need(r.returncode==0,label+r.stderr);d=json.loads(r.stdout);d.pop('optimized');normalized.append(d);rows.append({'group':'package','test':label,'optimized':opt,'passed':True})
        need(all(d==normalized[0] for d in normalized),'mode/relocation output agreement')
        anames=['changed_author_result','missing_file','extra_file','nested_manifest','nested_author_manifest','symlink','duplicate_entry','wrong_identity','traversal','noncanonical','invalid_size','duplicate_json_key','resigned_wrong_disposition','resigned_wrong_independent_result','resigned_author_change']
        for name in anames:
            root=tmp/('audit_'+name);shutil.copytree(clean/'audit',root);audit_mutation(root,name)
            for opt in (False,True):
                r=run(root,'verify_audit.py',opt);need(r.returncode!=0,'accepted audit '+name);rows.append({'group':'audit','test':name,'optimized':opt,'rejected':True})
        pnames=['changed_proof','same_size_result','missing_file','extra_file','extra_directory','nested_manifest','damaged_zip','changed_manifest','unsafe_manifest','member_symlink','ancestor_symlink','wrong_external_pin','duplicate_json_key']
        for name in pnames:
            root=tmp/('package_'+name);shutil.copytree(clean,root);usepin=pin
            if name=='changed_proof':
                p=root/'author/RESULT.md';p.write_bytes(p.read_bytes()+b'changed')
            elif name=='same_size_result':
                p=root/'author/CHECK_RESULTS.json';b=p.read_bytes();need(b'32400' in b,'same-size fixture');p.write_bytes(b.replace(b'32400',b'32401',1))
            elif name=='missing_file':(root/'audit/INDEPENDENT_RESULTS.json').unlink()
            elif name=='extra_file':(root/'extra.txt').write_text('extra')
            elif name=='extra_directory':(root/'extra').mkdir()
            elif name=='nested_manifest':
                p=root/'author/unexpected';p.mkdir();(p/'MANIFEST.json').write_text('{}')
            elif name=='damaged_zip':
                p=next((root/'archives').glob('*.zip'));b=p.read_bytes();p.write_bytes(b[:15]+bytes([b[15]^1])+b[16:])
            elif name=='changed_manifest':
                p=root/'PUBLICATION_MANIFEST.json';p.write_bytes(p.read_bytes()+b' ')
            elif name=='unsafe_manifest':
                p=root/'PUBLICATION_MANIFEST.json';d=read(p);d['files'][0]['path']='../escape';write(p,d);usepin=sha(p)
            elif name=='member_symlink':
                p=root/'author/RESULT.md';p.unlink();p.symlink_to(clean/'author/RESULT.md')
            elif name=='ancestor_symlink':
                alias=tmp/'linked_parent';alias.symlink_to(tmp,target_is_directory=True);root=alias/root.name
            elif name=='wrong_external_pin':usepin='0'*64
            elif name=='duplicate_json_key':
                p=root/'PUBLICATION_MANIFEST.json';p.write_text(p.read_text().replace('{','{"problem_id":6200010,',1));usepin=sha(p)
            for opt in (False,True):
                r=run(root,'verify_package.py',opt,usepin);need(r.returncode!=0,'accepted package '+name);rows.append({'group':'package','test':name,'optimized':opt,'rejected':True})
        # This expected historical failure of the author-only inventory is documented,
        # not a validation of the extra file. Operative audit/package checks reject it.
        old=tmp/'historical_author_gap';shutil.copytree(clean/'author',old);(old/'unexpected').mkdir();(old/'unexpected/MANIFEST.json').write_text('{}\n')
        gaps=[]
        for opt in (False,True):
            r=run(old,'verify.py',opt);need(r.returncode==0,'historical gap no longer reproduced');gaps.append({'optimized':opt,'unlisted_nested_manifest_accepted_by_original_author_only':True})
    print(json.dumps({'status':'PASS','problem_id':6200010,'clean_runs':4,'audit_hostile_rejections':30,'publication_hostile_rejections':26,'controls':rows,'historical_author_gap':gaps,'normalized_outputs_agree':True,'original_problem_resolved':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
