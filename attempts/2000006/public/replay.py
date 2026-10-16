#!/usr/bin/env python3
"""Fail-closed auxiliary replay in clean copies with checker assertions enabled."""
from pathlib import Path
import concurrent.futures,hashlib,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
# -O/-OO flags are never forwarded. Remove the optimization variable so nested
# historical subprocesses (which invoke sys.executable directly) also keep checks.
ENV={k:v for k,v in os.environ.items() if k!='PYTHONOPTIMIZE'}
ENV['PYTHONDONTWRITEBYTECODE']='1'
DRIVER='import runpy,sys;\nif sys.flags.optimize != 0: raise RuntimeError("checker assertions disabled")\nrunpy.run_path(sys.argv[1],run_name="__main__")\n'


def require(condition,detail):
    if not condition:
        raise RuntimeError(str(detail))


def checked_python(script,cwd):
    # -E ignores interpreter environment flags; -B prevents cache creation.
    # The explicit driver verifies the child state before any checker runs.
    return subprocess.run([sys.executable,'-E','-B','-c',DRIVER,str(script)],cwd=cwd,env=ENV,capture_output=True,text=True)


def verify_copy():
    result=checked_python(ROOT/'verify.py',ROOT)
    require(result.returncode==0,('integrity verification failed',result.stderr))
    return json.loads(result.stdout)


def execute(job):
    with tempfile.TemporaryDirectory(prefix='e6322_public_replay_') as tmp:
        mirror=Path(tmp)/'checkpoint';shutil.copytree(ROOT,mirror)
        script=mirror/job['script'];expected=(ROOT/Path(job['script']).parent/job['output']).read_bytes()
        adapter=job.get('adaptation')
        if adapter:shutil.copyfile(mirror/adapter['public_adapter'],script)
        output_path=script.with_name(job['output'])
        if not job.get('stdout_output'):output_path.unlink()
        result=checked_python(script,mirror)
        require(result.returncode==0,('checker process failed',job['script'],result.stdout,result.stderr))
        if not job.get('stdout_output'):require(output_path.is_file(),('checker output missing',job['script']))
        actual=result.stdout.encode() if job.get('stdout_output') else output_path.read_bytes()
        record={'pass':job['pass'],'lane':job['lane'],'script':job['script'],'exit_code':0,'output_sha256':hashlib.sha256(actual).hexdigest()}
        got=json.loads(actual)
        if adapter:
            old=json.loads(expected);skips=adapter['omitted_check_names']
            omitted=[c for c in old['checks'] if c['name'] in skips]
            kept=[c for c in old['checks'] if c['name'] not in skips]
            require(len(omitted)==len(skips) and got['checks']==kept,(job['script'],'algebra-check list mismatch'))
            require(got['total_checks']==len(kept) and all(c['passed'] for c in kept),(job['script'],'adapted check totals or outcomes'))
            record.update(public_adapter=adapter['public_adapter'],mathematical_checks=len(kept),all_mathematical_checks_identical=True,omitted_historical_source_document_checks=skips,byte_identical_full_historical_output=False)
        else:
            require(actual==expected,(job['script'],'historical output differs; inspect dependency/interpreter versions'))
            record['byte_identical_historical_output']=True
            if job['lane']=='exact':
                require(got['total_exact_checks']==201 and got['prior_quadrature_checks']==14 and len(got['prior_reproductions'])==4,'exact replay counts')
                record.update(exact_checks=got['total_exact_checks'],quadrature_comparisons=got['prior_quadrature_checks'],prior_exact_replays=len(got['prior_reproductions']))
            elif job['lane']=='positivity':
                count=got.get('symbolic_check_count',got.get('total_checks'))
                if count is not None:record['symbolic_check_count']=count
            elif job['lane']=='audit' and 'total_checks' in got:record['total_checks']=got['total_checks']
        return record


def run():
    integrity=verify_copy();jobs=[]
    def add(n,lane,script,output,**extra):
        jobs.append({'pass':n,'lane':lane,'script':f'research_elasticity_1791_pass{n}_20261016/{lane}/{script}','output':output,**extra})
    add(5,'exact','verify_final.py','verification.json')
    for n,s,o in [(1,'check_formulas.py','formula_checks.json'),(2,'verify_endpoint.py','ENDPOINT_CHECKS.json'),(3,'verify_constitutive.py','CONSTITUTIVE_CHECKS.json'),(4,'verify_repairs.py','REPAIR_CHECKS.json'),(5,'verify_final.py','FINAL_CHECKS.json')]:add(n,'positivity',s,o)
    add(1,'counterexample','verify_scaling.py','SCALING_CHECKS.json',stdout_output=True)
    add(1,'audit','verify_audit.py','AUDIT_CHECKS.json')
    add(5,'audit','verify_audit.py','AUDIT_CHECKS.json')
    for adaptation in json.loads((ROOT/'portable_audits/ADAPTATIONS.json').read_text()):
        add(adaptation['pass'],'audit','verify_audit.py','AUDIT_CHECKS.json',adaptation=adaptation)
    require(len(jobs)==12,'unexpected replay job count')
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(execute,jobs))
    require(verify_copy()==integrity,'checkpoint changed during replay')
    return {'status':'pass','problem':'E-6322','terminal_status':'UNSOLVED 5/5','direct_replay_jobs':len(jobs),'nested_prior_exact_replays':4,'exact_checks':201,'quadrature_comparisons':14,'final_positivity_checks':28,'final_audit_controls':57,'historical_source_document_checks_not_replayed':sum(len(r.get('omitted_historical_source_document_checks',[])) for r in results),'optimization_independent_gates':True,'checker_assertions_enabled':True,'optimization_environment_removed':True,'no_source_documents_downloaded':True,'checkpoint_unchanged':True,'benchmark_proved':False,'benchmark_counterexample':False,'results':results}

if __name__=='__main__':print(json.dumps(run(),indent=2))
