#!/usr/bin/env python3
"""Adversarial packaging controls in isolated copies; accepted originals untouched."""
from pathlib import Path
import ast,concurrent.futures,hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
MODES=[('normal',[],None),('minus_O',['-O'],None),('minus_OO',['-OO'],None),('environment_1',[],'1'),('environment_2',[],'2'),('mixed_OO_environment_1',['-OO'],'1')]


def require(condition,detail):
    if not condition:raise RuntimeError(str(detail))


def invocation(root,entry,mode):
    name,flags,opt=mode;env={k:v for k,v in os.environ.items() if k!='PYTHONOPTIMIZE'};env['PYTHONDONTWRITEBYTECODE']='1'
    if opt is not None:env['PYTHONOPTIMIZE']=opt
    return subprocess.run([sys.executable,*flags,str(root/entry)],cwd=root,env=env,capture_output=True,text=True)


def refresh_records(obj,root):
    if isinstance(obj,dict):
        if {'path','bytes','sha256'}<=obj.keys():
            path=root/obj['path'];data=path.read_bytes();obj['bytes']=len(data);obj['sha256']=hashlib.sha256(data).hexdigest()
        for value in obj.values():refresh_records(value,root)
    elif isinstance(obj,list):
        for value in obj:refresh_records(value,root)


def reseal_fixture(root):
    # This deliberately updates the isolated fixture's chain and package hashes.
    # A passing integrity gate must therefore reach the altered checker semantics.
    for n in range(1,6):
        path=root/f'research_elasticity_1791_pass{n}_20261016/audit/AUDIT_MANIFEST.json'
        obj=json.loads(path.read_text());refresh_records(obj,root);path.write_text(json.dumps(obj,indent=2)+'\n')
    path=root/'PACKAGE_MANIFEST.json';obj=json.loads(path.read_text());refresh_records(obj,root);path.write_text(json.dumps(obj,indent=2)+'\n')


def mutate(root,case):
    if case=='same_length_status_corruption':
        p=root/'research_elasticity_1791_pass5_20261016/audit/FINAL_ACCEPTANCE_REPORT.md';s=p.read_text();t=s.replace('UNSOLVED 5/5','RESOLVED 5/5',1)
        require(t!=s and len(t.encode())==len(s.encode()),'status fixture must be same length');p.write_text(t)
    elif case=='unexpected_file':(root/'UNEXPECTED.md').write_text('unexpected test file\n')
    elif case=='missing_file':(root/'README.md').unlink()
    elif case=='malformed_manifest':(root/'PACKAGE_MANIFEST.json').write_text('{not valid JSON\n')
    elif case=='wrong_manifest_type':
        p=root/'PACKAGE_MANIFEST.json';o=json.loads(p.read_text());o['files']={};p.write_text(json.dumps(o)+'\n')
    elif case=='false_manifest_status':
        p=root/'PACKAGE_MANIFEST.json';o=json.loads(p.read_text());o['terminal_status']='RESOLVED 5/5';p.write_text(json.dumps(o)+'\n')
    elif case=='false_final_exact_identity':
        p=root/'research_elasticity_1791_pass5_20261016/exact/verify_final.py';s=p.read_text();old="eq('barrier source constant six',s.limit(((1-t)**-6-1)/t,t,0),6)";new=old[:-2]+'7)'
        require(old in s,'exact identity fixture anchor');p.write_text(s.replace(old,new,1));reseal_fixture(root)
    elif case=='false_nested_exact_identity':
        p=root/'research_elasticity_1791_pass1_20261016/exact/verify_exact.py';oldhash=hashlib.sha256(p.read_bytes()).hexdigest();s=p.read_text();old='def certify(name, expression):\n';require(old in s,'nested fixture anchor');p.write_text(s.replace(old,old+'    expression = expression + 1  # Deliberately false isolated control.\n',1));newhash=hashlib.sha256(p.read_bytes()).hexdigest()
        q=root/'research_elasticity_1791_pass5_20261016/exact/verify_final.py';s=q.read_text();require(oldhash in s,'nested pinned script hash anchor');q.write_text(s.replace(oldhash,newhash,1));reseal_fixture(root)
    elif case=='nonzero_child_exit':
        p=root/'research_elasticity_1791_pass5_20261016/positivity/verify_final.py';p.write_text('raise SystemExit(23)\n'+p.read_text());reseal_fixture(root)
    elif case=='zero_exit_without_output':
        p=root/'research_elasticity_1791_pass5_20261016/positivity/verify_final.py';p.write_text('raise SystemExit(0)\n'+p.read_text());reseal_fixture(root)
    elif case=='changed_child_output':
        p=root/'research_elasticity_1791_pass5_20261016/positivity/verify_final.py';s=p.read_text();old="'symbolic_check_count':len(checks)";require(old in s,'output fixture anchor');p.write_text(s.replace(old,"'symbolic_check_count':len(checks)+1",1));reseal_fixture(root)
    else:raise RuntimeError(('unknown fixture',case))


def one(case,mode):
    with tempfile.TemporaryDirectory(prefix='e6322_release_control_') as td:
        copy=Path(td)/'checkpoint';shutil.copytree(ROOT,copy)
        if case=='clean':
            v=invocation(copy,'verify.py',mode);r=invocation(copy,'replay.py',mode)
            require(v.returncode==0 and json.loads(v.stdout)['status']=='pass',('clean verifier',mode,v.stderr))
            require(r.returncode==0 and json.loads(r.stdout)['status']=='pass',('clean replay',mode,r.stderr))
            require(json.loads(r.stdout)['checker_assertions_enabled'] is True,'checker assertion state missing')
            return {'case':case,'mode':mode[0],'passed':True,'verification_exit':v.returncode,'replay_exit':r.returncode,'replay_output_sha256':hashlib.sha256(r.stdout.encode()).hexdigest()}
        mutate(copy,case)
        semantic=case in {'false_final_exact_identity','false_nested_exact_identity','nonzero_child_exit','zero_exit_without_output','changed_child_output'}
        v=invocation(copy,'verify.py',mode)
        if semantic:
            require(v.returncode==0,('resealed fixture must pass integrity',case,mode,v.stderr))
            r=invocation(copy,'replay.py',mode)
            require(r.returncode!=0 and not r.stdout.strip(),('semantic fixture accepted',case,mode,r.stdout,r.stderr))
            needle={'false_final_exact_identity':'barrier source constant six','false_nested_exact_identity':'CalledProcessError','nonzero_child_exit':'checker process failed','zero_exit_without_output':'checker output missing','changed_child_output':'historical output differs'}[case]
            require(needle in r.stderr,('unexpected semantic rejection reason',case,mode,r.stderr))
            return {'case':case,'mode':mode[0],'passed':True,'resealed_fixture_integrity_passed':True,'replay_exit':r.returncode,'expected_rejection':needle}
        require(v.returncode!=0 and not v.stdout.strip(),('integrity fixture accepted',case,mode,v.stdout,v.stderr))
        r=invocation(copy,'replay.py',mode)
        require(r.returncode!=0 and not r.stdout.strip() and 'integrity verification failed' in r.stderr,('replay accepted invalid input',case,mode,r.stdout,r.stderr))
        return {'case':case,'mode':mode[0],'passed':True,'verification_exit':v.returncode,'replay_exit':r.returncode}


def main():
    for name in ('verify.py','replay.py','test_release_guards.py'):
        tree=ast.parse((ROOT/name).read_text());require(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),('removable assertion in release gate',name))
    initial={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.is_file()}
    cases=['clean','same_length_status_corruption','unexpected_file','missing_file','malformed_manifest','wrong_manifest_type','false_manifest_status','false_final_exact_identity','false_nested_exact_identity','nonzero_child_exit','zero_exit_without_output','changed_child_output']
    work=[(case,mode) for case in cases for mode in MODES]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(lambda pair:one(*pair),work))
    final={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.is_file()}
    require(initial==final,'candidate changed during release controls')
    clean_hashes={r['replay_output_sha256'] for r in results if r['case']=='clean'}
    require(len(clean_hashes)==1,'optimization modes changed replay output')
    return {'status':'pass','scope':'Packaging-only optimization and fail-closed controls; no new mathematical pass.','mode_count':len(MODES),'control_count':len(results),'clean_full_replays':len(MODES),'negative_controls':len(results)-len(MODES),'false_identity_fixtures_resealed':True,'nested_original_checker_assertions_tested':True,'original_candidate_unchanged':True,'wrapper_ast_assert_count':0,'all_clean_replay_outputs_identical':True,'results':results}

if __name__=='__main__':print(json.dumps(main(),indent=2))
