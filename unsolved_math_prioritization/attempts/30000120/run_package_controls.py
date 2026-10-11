#!/usr/bin/env python3
"""Relocated clean replays and hostile package tests, both Python modes."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).absolute().parent
def need(v,m):
    if not v:raise RuntimeError('CONTROL FAILURE: '+m)
def run(root,opt,pin):
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
    return subprocess.run([sys.executable]+(['-O'] if opt else [])+[str(root/'verify_package.py'),'--expected-manifest',pin],cwd=root.parent,env=env,capture_output=True)
def main():
    pin=hashlib.sha256((ROOT/'PUBLICATION_MANIFEST.json').read_bytes()).hexdigest();rows=[];outputs=[]
    with tempfile.TemporaryDirectory(prefix='wonderful-chern-controls-') as td:
        base=Path(td);clean=base/'relocated';shutil.copytree(ROOT,clean)
        for label,root in [('original',ROOT),('relocated',clean)]:
            for opt in [False,True]:
                r=run(root,opt,pin);need(r.returncode==0,label+': '+r.stderr.decode(errors='replace'));outputs.append(r.stdout);rows.append({'test':label,'optimized':opt,'passed':True})
        need(all(x==outputs[0] for x in outputs),'normal optimized relocated output identity')
        names=['changed_report','same_size_result','missing_file','extra_file','extra_directory','damaged_zip','changed_manifest','unsafe_manifest','member_symlink','ancestor_symlink','wrong_external_pin']
        for name in names:
            root=base/name;shutil.copytree(clean,root);usepin=pin
            if name=='changed_report':
                p=root/'author/REPORT.md';p.write_bytes(p.read_bytes()+b'corruption\n')
            elif name=='same_size_result':
                p=root/'audit/CHECKS.json';b=p.read_bytes();need(b'48' in b,'result mutation fixture');p.write_bytes(b.replace(b'48',b'49',1))
            elif name=='missing_file':(root/'audit/CHECKS.json').unlink()
            elif name=='extra_file':(root/'unlisted.txt').write_text('extra')
            elif name=='extra_directory':(root/'unlisted').mkdir()
            elif name=='damaged_zip':
                p=next((root/'archives').glob('*.zip'));b=p.read_bytes();p.write_bytes(b[:15]+bytes([b[15]^1])+b[16:])
            elif name=='changed_manifest':
                p=root/'PUBLICATION_MANIFEST.json';p.write_bytes(p.read_bytes()+b' ')
            elif name=='unsafe_manifest':
                p=root/'PUBLICATION_MANIFEST.json';d=json.loads(p.read_text());d['files']['../escape']=d['files'].pop('README.md');p.write_text(json.dumps(d));usepin=hashlib.sha256(p.read_bytes()).hexdigest()
            elif name=='member_symlink':
                p=root/'author/REPORT.md';p.unlink();p.symlink_to(clean/'author/REPORT.md')
            elif name=='ancestor_symlink':
                alias=base/'linked_parent';alias.symlink_to(base,target_is_directory=True);root=alias/name
            elif name=='wrong_external_pin':usepin='0'*64
            for opt in [False,True]:
                r=run(root,opt,usepin);need(r.returncode!=0,'accepted '+name);rows.append({'test':name,'optimized':opt,'rejected':True})
    print(json.dumps({'status':'pass','clean_outputs_byte_identical':True,'clean_runs':4,'hostile_rejections':22,'controls':rows},indent=2,sort_keys=True))
if __name__=='__main__':main()
