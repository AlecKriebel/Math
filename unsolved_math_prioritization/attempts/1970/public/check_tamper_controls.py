#!/usr/bin/env python3
"""Check inventory, identity, scope, and acceptance guards in disposable copies."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
MODES=[('normal',[]),('O',['-O']),('OO',['-OO'])]
def require(ok,why):
    if not ok:raise RuntimeError(why)
def sha(b):return hashlib.sha256(b).hexdigest()
def snapshot():return {p.relative_to(ROOT).as_posix():sha(p.read_bytes()) for p in ROOT.rglob('*') if p.is_file()}
def write(path,data):path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
def rebind(root,rel):
    p=root/'MANIFEST.json';m=json.loads(p.read_text());raw=(root/rel).read_bytes()
    for entry in m['files']:
        if entry['path']==rel:entry['bytes']=len(raw);entry['sha256']=sha(raw);break
    else:raise RuntimeError('missing mutation entry')
    write(p,m)
def invoke(root,flags):
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None)
    return subprocess.run([sys.executable,'-I','-B',*flags,str(root/'verify_package.py')],cwd=root,env=env,capture_output=True,timeout=60)
def change(root,name):
    mpath=root/'MANIFEST.json';m=json.loads(mpath.read_text())
    if name.startswith('formulation_field:'):
        key=name.split(':',1)[1];p=root/'FORMULATION.json';d=json.loads(p.read_text());value=d[key]
        d[key]=not value if type(value) is bool else value+1 if type(value) is int else value+' changed'
        write(p,d);rebind(root,'FORMULATION.json');return 'formulation mismatch: '+key
    if name=='formulation_extra_field':
        p=root/'FORMULATION.json';d=json.loads(p.read_text());d['unreviewed_claim']=True;write(p,d);rebind(root,'FORMULATION.json');return 'exact formulation schema'
    if name=='altered_file':
        with (root/'README.md').open('a') as f:f.write('\nChanged.\n')
        return 'file identity mismatch'
    if name=='missing_file':(root/'README.md').unlink();return 'missing regular file'
    if name=='unexpected_file':(root/'UNLISTED.txt').write_text('extra\n');return 'unmanifested or missing files'
    if name=='symbolic_link':(root/'UNLISTED_LINK').symlink_to('README.md');return 'symbolic link forbidden'
    if name=='duplicate_json_key':
        raw=mpath.read_text();mpath.write_text(raw.replace('"status": "UNSOLVED"','"status": "UNSOLVED", "status": "UNSOLVED"'));return 'duplicate JSON key'
    if name=='unsafe_path':m['files'][0]['path']='../outside';write(mpath,m);return 'unsafe manifest path'
    if name=='manifest_solution':m['resolution_claimed']=True;write(mpath,m);return 'manifest mathematical status'
    if name=='checkpoint_solution':m['checkpoint']='completed solution';write(mpath,m);return 'checkpoint scope mismatch'
    if name=='formulation_global_tau':
        p=root/'FORMULATION.json';d=json.loads(p.read_text());d['global_tau_equals_q1_claimed']=True;write(p,d);rebind(root,'FORMULATION.json');return 'formulation mismatch'
    if name=='audit_global_binary':
        p=root/'AUDIT_BINDINGS.json';d=json.loads(p.read_text());d['global_actual_binary_E_claimed']=True;write(p,d);rebind(root,'AUDIT_BINDINGS.json');return 'audit scope mismatch'
    if name=='audit_report_binding':
        p=root/'AUDIT_BINDINGS.json';d=json.loads(p.read_text());d['acceptance_report']['sha256']='0'*64;write(p,d);rebind(root,'AUDIT_BINDINGS.json');return 'acceptance report binding mismatch'
    if name=='audit_proof_unbound':
        p=root/'AUDIT_BINDINGS.json';d=json.loads(p.read_text());d['proofs'].pop();write(p,d);rebind(root,'AUDIT_BINDINGS.json');return 'incomplete proof binding'
    if name=='audit_missing_acceptance':
        p=root/'AUDIT_BINDINGS.json';d=json.loads(p.read_text());d['status']='PENDING';write(p,d);rebind(root,'AUDIT_BINDINGS.json');return 'final independent acceptance missing'
    raise RuntimeError('unknown control')
def main():
    cp=invoke(ROOT,[]);require(cp.returncode==0 and not cp.stderr,'initial integrity failure: '+cp.stderr.decode())
    before=snapshot();records=[]
    names=['altered_file','missing_file','unexpected_file','symbolic_link','duplicate_json_key','unsafe_path','manifest_solution','checkpoint_solution','formulation_global_tau','audit_global_binary','audit_report_binding','audit_proof_unbound','audit_missing_acceptance']
    names += ['formulation_field:'+key for key in sorted(json.loads((ROOT/'FORMULATION.json').read_text()))]
    names.append('formulation_extra_field')
    with tempfile.TemporaryDirectory(prefix='ep168-integrity-') as td:
        for name in names:
            work=Path(td)/name;shutil.copytree(ROOT,work);label=change(work,name)
            for mode,flags in MODES:
                cp=invoke(work,flags)
                require(cp.returncode!=0 and label.encode() in cp.stderr,'integrity mutation accepted or wrong failure: '+name+' '+cp.stderr.decode())
                records.append({'case':name,'mode':mode,'expected_guard':label,'rejected':True})
    require(snapshot()==before,'public package changed during integrity controls')
    print(json.dumps({'status':'PASS','modes':[m for m,_ in MODES],'cases':len(names),'rejected_mutations':len(records),'source_tree_modified':False,'controls':records},indent=2,sort_keys=True))
if __name__=='__main__':main()
