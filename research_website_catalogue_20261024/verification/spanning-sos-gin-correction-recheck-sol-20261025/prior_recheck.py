"""Run pristine3 and all35 unchanged earlier faults per normal/-O mode."""
from pathlib import Path
import ast,datetime,difflib,hashlib,json,os,signal,subprocess
O=Path(__file__).resolve().parent;P=O.parents[1];S=P/'verification/local-spanning-sos-gin-stage-sol-20261025'
PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3';ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(S)+os.pathsep+str(P/'scripts'))
IDS=['23181280','23442760','23395703']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def once(s,a,b):
    if s.count(a)!=1:raise RuntimeError('expected_one_dispatch_override:'+a)
    return s.replace(a,b,1)
def run(args,opt=False):
    proc=subprocess.Popen([PY,'-B']+(['-O'] if opt else [])+args,env=ENV,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    try:out,err=proc.communicate(timeout=45)
    except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGTERM);out,err=proc.communicate(timeout=5);raise RuntimeError('bounded_checker_timeout')
    return {'argv':args,'optimized':opt,'exit':proc.returncode,'stdout':out,'stderr':err}
def main():
    if (O/'PRIOR_DISPATCH_ONCE.json').exists():raise RuntimeError('no_duplicate_prior_fault_execution')
    corrected=(O/'inputs/final-content-check.proposed.py').read_text()
    if hashlib.sha256(corrected.encode()).hexdigest()!='aceef187f34f5d1029a19e4e2e9b2b15472535a07cf224134adbd2ddb16fd6c4':raise RuntimeError('exact_root_input')
    stage=once(corrected,'R=Path(__file__).resolve().parents[1]','R=Path('+repr(str(P))+')');ast.parse(stage);(O/'final-content-check.stage.py').write_text(stage)
    (O/'checker-private-root-override.diff').write_text(''.join(difflib.unified_diff(corrected.splitlines(True),stage.splitlines(True),fromfile='exact-root-corrected-input',tofile='private-root-only')))
    original=(S/'public_fault.py').read_text();(O/'inputs/public_fault.original.py').write_text(original)
    adapted=once(original,'O=Path(__file__).resolve().parent;P=O.parents[1];',"O=Path("+repr(str(O))+');P=Path('+repr(str(P))+');S=Path('+repr(str(S))+');')
    adapted=once(adapted,"article=O/'public/research'","article=S/'public/research'")
    if adapted.count("str(O/'stage_reader.py')")!=2:raise RuntimeError('two_readonly_stage_reader_dispatch_references_required')
    adapted=adapted.replace("str(O/'stage_reader.py')","str(S/'stage_reader.py')")
    adapted=once(adapted,"str(O/'public')","str(S/'public')")
    ast.parse(adapted);(O/'public_fault.recheck.py').write_text(adapted)
    (O/'prior-fault-dispatch-only.diff').write_text(''.join(difflib.unified_diff(original.splitlines(True),adapted.splitlines(True),fromfile='immutable-prior35-fault-source',tofile='own-output-and-new-checker-dispatch-only')))
    cases=['wrong_visible_date','wrong_visible_edition','wrong_visible_citation_edition','omit_status_paragraph','omit_proof_paragraph','wrong_iframe','wrong_original_download','wrong_schema_license','wrong_orcid','wrong_readable_math','altered_reader_bytes']
    save('PRIOR_DISPATCH_ONCE.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pristine_record_checks':6,'negative_cases':70,'normal_and_optimized':True,'old61_suite_runs':0})
    rows=[];positives=[]
    for opt,base in [(False,'normal'),(True,'optimized')]:
        mode='prior-'+base;out=O/mode;out.mkdir(exist_ok=True)
        execution=run([str(S/'stage_reader.py'),str(O/'final-content-check.stage.py'),*IDS,'--site',str(S/'public'),'--output-dir',str(out),'--output-stem','pristine3'],opt);save(mode+'/pristine3.execution.json',execution)
        result=json.loads((out/'pristine3.json').read_text())
        if execution['exit'] or execution['stderr'] or result['status']!='PASS':raise RuntimeError('pristine3_not_PASS')
        positives.append({'mode':base,'status':'PASS','record_ids':list(result['papers']),'checks':sum(len(x['checks']) for x in result['papers'].values())})
        for rid in IDS:
            for case in cases+(['drop_TeX_original_link','invent_Gin_schema_version'] if rid=='23395703' else []):
                execution=run([str(O/'public_fault.recheck.py'),rid,case,mode],opt);save(mode+'/execution-'+rid+'-'+case+'.json',execution);report=out/('checker-'+rid+'-'+case+'.json');data=json.loads(report.read_text()) if report.exists() else None
                if execution['exit']!=1 or execution['stderr'] or data is None or data['status']!='ISSUES_FOUND':raise RuntimeError((base,rid,case,execution))
                actual=json.loads((out/('mutation-'+rid+'-'+case+'.json')).read_text());prior=json.loads((S/base/('mutation-'+rid+'-'+case+'.json')).read_text())
                if actual!=prior:raise RuntimeError('mutation_bytes_differ_from_immutable_prior_case')
                rows.append({'mode':base,'record_id':rid,'case':case,'rejected':True,'issues':data['issues'],'identical_prior_mutation_receipt':True,'report_SHA256':sha(report)})
        print(base+': pristine3 PASS; all prior35 faults reject.',flush=True)
    save('PRIOR_RESULTS.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','root_checker_SHA256':sha(O/'inputs/final-content-check.proposed.py'),'prior_fault_source_SHA256':sha(S/'public_fault.py'),'pristine':positives,'faults':rows,'faults_rejected_each_mode':35,'same_prior_mutations':True,'old61_suite_rerun':False})
    print(json.dumps({'status':'PASS_PRISTINE_AND_PRIOR35_EACH_MODE','negative_executions':70,'pristine_records_each_mode':3},indent=2))
if __name__=='__main__':main()
