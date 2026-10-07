#!/usr/bin/env python3
"""Corruption and deeper mathematical controls, confined to temporary copies."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
MODES=['normal','dash_O','env_2']
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def digest(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def snapshot(p):return {f.relative_to(p).as_posix():digest(f) for f in sorted(p.rglob('*')) if f.is_file()}
def run(script,mode,args=()):
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
    flags=[]
    if mode=='dash_O':flags=['-O'];env['PYTHONOPTIMIZE']='1'
    if mode=='env_2':env['PYTHONOPTIMIZE']='2'
    return subprocess.run([sys.executable,*flags,'-B',str(script),*args],cwd=script.parent,env=env,capture_output=True)
def rebind(root,name):
    p=root/name;m=json.loads(p.read_text());m['files']={f.relative_to(root).as_posix():digest(f) for f in sorted(root.rglob('*')) if f.is_file() and f!=p};p.write_text(json.dumps(m,indent=2)+'\n')
def replace(p,old,new):
    text=p.read_text();need(old in text,'missing mutation target');p.write_text(text.replace(old,new))

def main():
    before=snapshot(ROOT);results=[]
    for mode in MODES:
        r=run(ROOT/'verify_publication.py',mode);need(r.returncode==0,'unmutated control failed '+r.stderr.decode())
    cases=['changed_proof','changed_audit','changed_result','missing_member','extra_member','symlink_member','unsafe_manifest_path','rebound_author_manifest','rebound_audit_manifest','wrong_external_anchor']
    for case in cases:
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'portable packet';shutil.copytree(ROOT,p)
            if case=='changed_proof':q=p/'packet/PROOF.md';q.write_bytes(q.read_bytes()+b'changed')
            elif case=='changed_audit':q=p/'independent_audit/AUDIT_REPORT.md';q.write_bytes(q.read_bytes()+b'changed')
            elif case=='changed_result':(p/'packet/FUSION_CHECKS.json').write_text('{}\n')
            elif case=='missing_member':(p/'packet/README.md').unlink()
            elif case=='extra_member':(p/'extra.txt').write_text('extra')
            elif case=='symlink_member':q=p/'packet/README.md';q.unlink();q.symlink_to(ROOT/'packet/README.md')
            elif case=='unsafe_manifest_path':
                q=p/'PUBLIC_MANIFEST.json';m=json.loads(q.read_text());m['files']['../escape']={'bytes':0,'sha256':'0'*64};q.write_text(json.dumps(m))
            elif case.startswith('rebound_'):
                folder,name=('packet','AUTHOR_MANIFEST.json') if case=='rebound_author_manifest' else ('independent_audit','AUDIT_MANIFEST.json')
                q=p/folder/name;m=json.loads(q.read_text());m['status_note']='tampered';q.write_text(json.dumps(m));rebind(p,'PUBLIC_MANIFEST.json')
            for mode in MODES:
                args=['--manifest-sha256','0'*64] if case=='wrong_external_anchor' else []
                r=run(p/'verify_publication.py',mode,args);need(r.returncode!=0,'accepted '+case+' '+mode)
                error=r.stderr.decode();need('RuntimeError:' in error,'unexpected rejection '+error)
                results.append({'case':case,'mode':mode,'stage':'publication_integrity','status':'REJECTED'})
    for case in ['rebound_bad_hom_count','rebound_bad_carry','rebound_wrong_output']:
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'packet';shutil.copytree(ROOT/'packet',p)
            if case=='rebound_bad_hom_count':replace(p/'check_fusion.py','len(homs)==len(set(homs))==36','len(homs)==len(set(homs))==35')
            elif case=='rebound_bad_carry':replace(p/'check_obstructions.py','carry=[(i+j)//p for i,j in two]','carry=[((i+j)//p+1)%p for i,j in two]')
            else:(p/'FUSION_CHECKS.json').write_text('{}\n')
            rebind(p,'AUTHOR_MANIFEST.json')
            for mode in MODES:
                r=run(p/'verify.py',mode);need(r.returncode!=0,'accepted rebound mutant')
                marker='checker output differs:' if case=='rebound_wrong_output' else 'checker failed:'
                need(marker in r.stderr.decode(),'did not reach requested stage: '+r.stderr.decode())
                results.append({'case':case,'mode':mode,'stage':marker,'status':'REJECTED','optimized_children_explicit_env':mode!='normal'})
    for case,script,old,new,marker in [
        ('independent_bad_counts','independent_fusion_check.py','==[36,36,36,6,10,14,1,1,9]','==[35,36,36,6,10,14,1,1,9]','nine expected counts'),
        ('independent_bad_H2','independent_obstruction_check.py','p*p-r1-r2==1','p*p-r1-r2==2','H2 dimension')]:
        with tempfile.TemporaryDirectory() as tmp:
            b=Path(tmp);shutil.copytree(ROOT/'packet',b/'packet');shutil.copytree(ROOT/'independent_audit',b/'independent_audit');q=b/'independent_audit'/script;replace(q,old,new)
            for mode in MODES:
                r=run(q,mode);need(r.returncode!=0 and marker in r.stderr.decode(),'independent checker accepted mutation')
                results.append({'case':case,'mode':mode,'stage':'independent mathematical checker','status':'REJECTED'})
    need(snapshot(ROOT)==before,'original packet changed')
    print(json.dumps({'status':'PASS','positive_modes':3,'negative_runs':len(results),'original_packet_unchanged':True,'results':results},indent=2,sort_keys=True))
if __name__=='__main__':main()
