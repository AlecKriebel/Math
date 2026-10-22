#!/usr/bin/env python3
"""Independent read-only baseline and disposable-copy adversarial package tests."""
import argparse,hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile
from datetime import datetime,timezone

def require(v,m):
    if not v: raise RuntimeError(m)

def digest(p):
    d=p.read_bytes();return {'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()}

def write_json(p,v):p.write_text(json.dumps(v,indent=2)+'\n')

def rehash(root,names):
    p=root/'FILES.json';m=json.loads(p.read_text())
    for e in m['files']:
        if e['path'] in names:e.update(digest(root/e['path']))
    write_json(p,m)

def invoke(py,root,mode='normal',script='tools/reproduce.py',args=None,cwd=None):
    flags=['-B']+(['-O'] if mode=='optimized' else [])
    env=dict(os.environ)
    if mode=='env2':env['PYTHONOPTIMIZE']='2'
    command=[py]+flags+[str(root/script)]+([str(root)] if args is None else args)
    q=subprocess.run(command,text=True,capture_output=True,cwd=cwd,env=env)
    return {'mode':mode,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr}

def baseline(root,out):
    pys=['/opt/homebrew/bin/python3','/Users/alec/Documents/Math/.venv/bin/python','/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3']
    records=[];canonical=None
    for py in pys:
        version=subprocess.check_output([py,'--version'],text=True).strip()
        for mode in ['normal','optimized','env2','relative']:
            if mode=='relative':
                env=dict(os.environ);env['PYTHONOPTIMIZE']='2'
                q=subprocess.run([py,'-O','-B','tools/reproduce.py','.'],cwd=root,text=True,capture_output=True,env=env)
                r={'mode':mode,'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr}
            else:r=invoke(py,root,mode)
            require(r['returncode']==0,'baseline failed '+version+' '+mode+':'+r['stderr'])
            if canonical is None:canonical=r['stdout']
            require(r['stdout']==canonical,'baseline stdout mismatch')
            r['python']=version;records.append(r)
    write_json(out/'BASELINE_RUNTIME_MATRIX.json',{'timestamp_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','replays':records,'all_stdout_identical':True,'scope':'Finite replay, not analytic proof.'})
    print('baseline',len(records),'passed')

def attacks(root,out,private):
    py='/opt/homebrew/bin/python3';records=[]
    with tempfile.TemporaryDirectory(dir=private,prefix='adversary-') as d:
        work=pathlib.Path(d)/'bundle'
        def fresh():
            if work.exists():shutil.rmtree(work)
            shutil.copytree(root,work)
        def reject(label,mutation,script='tools/reproduce.py'):
            fresh();mutation(work)
            for mode in ['normal','optimized','env2']:
                r=invoke(py,work,mode,script=script)
                require(r['returncode']!=0,'unexpected acceptance '+label+' '+mode)
                r.update(label=label);records.append(r)
        reject('missing_original',lambda r:(r/'original/CANDIDATE_PROOF.md').unlink())
        reject('extra_file',lambda r:(r/'extra.txt').write_text('extra'))
        reject('same_length_payload_tamper',lambda r:(r/'manuscript/main.tex').write_bytes(b'X'*(r/'manuscript/main.tex').stat().st_size))
        def symlink(r):
            p=r/'original/README.md';p.unlink();p.symlink_to(root/'original/README.md')
        reject('file_symlink',symlink)
        reject('directory_symlink',lambda r:(r/'linked').symlink_to(root,target_is_directory=True))
        def manifest_value(r,field,value):
            p=r/'FILES.json';m=json.loads(p.read_text());m['files'][0][field]=value;write_json(p,m)
        for label,field,value in [('bool_bytes','bytes',True),('float_bytes','bytes',702.0),('parent_path','path','../else'),('absolute_path','path','/else'),('windows_path','path','C:/else'),('double_slash','path','a//b'),('null_path','path','a\x00b')]:
            reject(label,lambda r,f=field,v=value:manifest_value(r,f,v),script='tools/integrity.py')
        def schema(r,val):
            p=r/'FILES.json';m=json.loads(p.read_text());m['schema']=val;write_json(p,m)
        reject('bool_schema',lambda r:schema(r,True),script='tools/integrity.py')
        reject('float_schema',lambda r:schema(r,1.0),script='tools/integrity.py')
        reject('duplicate_manifest_key',lambda r:(r/'FILES.json').write_text('{"schema":1,"schema":1,"files":[]}'),script='tools/integrity.py')
        def wrong_identity(r):
            p=r/'reviews/continuity_core/independent_controls.py'
            p.write_text("import json\nprint(json.dumps({'status':'PASS','finite_words':19530}))\n")
            rehash(r,{'reviews/continuity_core/independent_controls.py'})
        reject('rehashed_wrong_control_identity',wrong_identity)
        def wrong_count_type(r):
            p=r/'reviews/continuity_core/independent_controls.py'
            s=p.read_text();s=s.replace('print(json.dumps(calculate(), indent=2, sort_keys=True))','print(json.dumps(dict(calculate(), finite_words=19531.0), indent=2, sort_keys=True))')
            require(s!=p.read_text(),'mutation anchor missing');p.write_text(s);rehash(r,{'reviews/continuity_core/independent_controls.py'})
        reject('rehashed_float_control_count',wrong_count_type)
        def baseline_tamper(r):
            p=r/'reviews/continuity_core/INDEPENDENT_CONTROLS.normal.json';m=json.loads(p.read_text());m['finite_words']=19531.0;write_json(p,m);rehash(r,{'reviews/continuity_core/INDEPENDENT_CONTROLS.normal.json'})
        reject('rehashed_float_sealed_baseline',baseline_tamper)
        def historical_fail(r):
            p=r/'original/check_density_chain.py';s=p.read_text().replace('assert direct==chained',"assert False, 'PKG_ADVERSARY_NESTED_ASSERT_SENTINEL'");require(s!=p.read_text(),'mutation anchor missing');p.write_text(s)
            q=r/'original/PUBLIC_PACKET_MANIFEST.json';m=json.loads(q.read_text());m['files']['check_density_chain.py'].update(digest(p));write_json(q,m)
            rehash(r,{'original/check_density_chain.py','original/PUBLIC_PACKET_MANIFEST.json'})
        reject('rehashed_nested_assert_sentinel',historical_fail)
        for r in records:
            if r['label']=='rehashed_nested_assert_sentinel':require('PKG_ADVERSARY_NESTED_ASSERT_SENTINEL' in r['stderr'],'nested assertion not reached')
    # The included 27-control suite is also rerun, rather than trusted as a receipt.
    supplied=[]
    for mode in ['normal','optimized','env2']:
        r=invoke(py,root,mode,script='tools/test_integrity_controls.py',args=[str(private)])
        require(r['returncode']==0,'supplied negative suite failed');require(json.loads(r['stdout'])['rejected_mutations']==27,'suite count mismatch');supplied.append(r)
    write_json(out/'HOSTILE_PACKAGE_TESTS.json',{'timestamp_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','actual_package_mutations':len(records)//3,'rejection_runs':records,'supplied_control_runs':supplied,'scope':'Invalid actual copies rejected. Rehashed sentinels bypass only outer byte checks to test semantic replay and nested assertions; manifests are not authenticated signatures.'})
    print('mutations',len(records)//3,'rejection runs',len(records),'supplied suite',len(supplied),'passed')

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('stage',choices=['baseline','attacks']);a.add_argument('root',type=pathlib.Path);a.add_argument('output',type=pathlib.Path);a.add_argument('private',type=pathlib.Path);args=a.parse_args()
    if args.stage=='baseline':baseline(args.root,args.output)
    else:attacks(args.root,args.output,args.private)
