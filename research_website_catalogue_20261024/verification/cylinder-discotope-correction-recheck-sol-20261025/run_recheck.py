"""Replay exactly the sealed auditor's22 cases per mode against new checker."""
from pathlib import Path
import ast,datetime,difflib,hashlib,json,os,signal,subprocess
O=Path(__file__).resolve().parent;P=O.parents[1]
S=P/'verification/local-cylinder-discotope-stage-sol-20261025';A=P/'verification/cylinder-discotope-code-audit-sol-20261025'
PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(S)+os.pathsep+str(P/'scripts'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def once(body,old,new):
    if body.count(old)!=1:raise RuntimeError('expected_exact_one_override:'+old)
    return body.replace(old,new,1)
def run(argv):
    proc=subprocess.Popen(argv,env=ENV,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    try:out,err=proc.communicate(timeout=45)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid,signal.SIGTERM);out,err=proc.communicate(timeout=5);raise RuntimeError('bounded_case_timeout')
    return {'exit':proc.returncode,'stdout':out,'stderr':err}

def main():
    if (O/'EXECUTIONS_DISPATCHED_ONCE.json').exists():raise RuntimeError('do_not_duplicate_44_cases')
    expected={'FINAL_SEAL.json':'5a1f81828dfa560a8d3f5f5d38ce08387a2861ddfece19012b6bb58d2d6c2370','FINAL_MANIFEST.json':'5e3a94b0f66f6edff3adaa64799fb1ea98ed4c9a243abfdac11524c610d9f358','fault_checker.py':'d6b83179b6f6d5dc5ccc7fd4f3ad840e3d936f0fa586a4af8079153419c3c9df'}
    for n,h in expected.items():
        if sha(A/n)!=h:raise RuntimeError('exact_auditor_input_binding:'+n)
    am=json.loads((A/'FINAL_MANIFEST.json').read_text());bindings=[]
    for item in am['files']:
        p=A/item['path']
        if p.stat().st_size!=item['bytes'] or sha(p)!=item['SHA256']:raise RuntimeError('auditor_owned_binding')
        bindings.append({'path':str(p),'bytes':item['bytes'],'SHA256':item['SHA256']})
    for n in ['FINAL_MANIFEST.json','FINAL_SEAL.json']:bindings.append({'path':str(A/n),'bytes':(A/n).stat().st_size,'SHA256':sha(A/n)})
    save('AUDITOR_INPUT_CUSTODY.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seal_seen_before_fault_code_read':True,'expected_pins':expected,'original_files':bindings})
    (O/'inputs/fault_checker.py').write_bytes((A/'fault_checker.py').read_bytes())
    checker=(O/'inputs/final-content-check.proposed.py').read_text()
    stage=once(checker,'R=Path(__file__).resolve().parents[1]','R=Path('+repr(str(P))+')')
    ast.parse(stage);(O/'final-content-check.stage.py').write_text(stage)
    (O/'checker-private-root-override.diff').write_text(''.join(difflib.unified_diff(checker.splitlines(True),stage.splitlines(True),fromfile='root-proposed-input',tofile='private-execution-only')))
    original=(A/'fault_checker.py').read_text();adapted=once(original,'A=Path(__file__).resolve().parent',"A=Path("+repr(str(O))+')/sys.argv[3]')
    adapted=once(adapted,'R=A.parents[1]','R=Path('+repr(str(P))+')')
    adapted=once(adapted,'rid,case=sys.argv[1:3]','rid,case=sys.argv[1:3]')
    adapted=once(adapted,"str(S/'final-content-check.stage.py')","str(Path("+repr(str(O))+ ")/'final-content-check.stage.py')")
    ast.parse(adapted);(O/'fault_checker.recheck.py').write_text(adapted)
    (O/'fault-dispatch-only.diff').write_text(''.join(difflib.unified_diff(original.splitlines(True),adapted.splitlines(True),fromfile='sealed-auditor-original',tofile='own-output-and-corrected-checker-dispatch-only')))
    cases=['pristine','omit_status_paragraph','wrong_visible_date','wrong_visible_edition','wrong_visible_citation_edition','omit_proof_paragraph','wrong_iframe','wrong_original_download','wrong_schema_license','wrong_orcid','altered_reader_bytes']
    ids=['23387774','23074543'];rows=[]
    save('EXECUTIONS_DISPATCHED_ONCE.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'44_CASE_EXECUTIONS_DISPATCHED_ONCE','record_ids':ids,'cases':cases,'modes':['normal','optimized'],'legacy59_executions':0})
    for opt,mode in [(False,'normal'),(True,'optimized')]:
        outdir=O/mode;outdir.mkdir(exist_ok=True)
        for rid in ids:
            for case in cases:
                cmd=[PY,'-B']+(['-O'] if opt else [])+[str(O/'fault_checker.recheck.py'),rid,case,mode]
                proc=run(cmd);report_path=outdir/('checker-'+rid+'-'+case+'.json')
                report=json.loads(report_path.read_text()) if report_path.is_file() else None
                (outdir/('execution-'+rid+'-'+case+'.json')).write_text(json.dumps({'argv':cmd,**proc},indent=2,ensure_ascii=False)+'\n')
                if proc['stderr'] or report is None:raise RuntimeError({'case':case,'record_id':rid,'mode':mode,'execution':proc})
                passed=proc['exit']==0 and report['status']=='PASS'
                if (case=='pristine')!=passed or (case!='pristine' and (proc['exit']!=1 or report['status']!='ISSUES_FOUND')):raise RuntimeError('unexpected_case_outcome:'+str((rid,case,mode,proc['exit'],report['status'])))
                mutation=json.loads((outdir/('mutation-'+rid+'-'+case+'.json')).read_text());oldmutation=json.loads((A/('mutation-'+rid+'-'+case+'.json')).read_text())
                if mutation!=oldmutation:raise RuntimeError('fault_bytes_differ_from_sealed_auditor_case')
                prior=json.loads((A/('checker-'+rid+'-'+case+'.json')).read_text());former_false_accept=case!='pristine' and prior['status']=='PASS'
                required={'wrong_visible_date':'visible_exact_declared_date_and_header_edition','wrong_visible_edition':'visible_exact_declared_date_and_header_edition','wrong_visible_citation_edition':'visible_exact_citation_edition','omit_status_paragraph':'all_exact_approved_status_paragraphs'}.get(case)
                if required and rid+': '+required not in report['issues']:raise RuntimeError('specific_new_guard_not_fired')
                rows.append({'mode':mode,'record_id':rid,'case':case,'expected_pristine':case=='pristine','accepted':passed,'exit':proc['exit'],'checks':len(report['papers'][rid]['checks']),'issues':report['issues'],'specific_new_guard':required,'former_false_accept':former_false_accept,'actual_original_and_fault_bytes_equal_sealed_auditor_receipt':True,'report_path':str(report_path.relative_to(O)),'report_SHA256':sha(report_path)})
        print(mode+': two pristine accepted, twenty altered-output cases rejected.',flush=True)
    save('RECHECK_RESULTS.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_BOUNDED_CORRECTION_RECHECK','root_corrected_checker_SHA256':sha(O/'inputs/final-content-check.proposed.py'),'auditor_fault_driver_SHA256':expected['fault_checker.py'],'executions':len(rows),'modes':['normal','optimized'],'per_mode_pristine':2,'per_mode_faults_rejected':20,'per_mode_former_false_accepts_now_rejected':sum(x['former_false_accept'] for x in rows if x['mode']=='normal'),'full_old59_suite_rerun':False,'cases':rows})
    print(json.dumps({'status':'PASS_BOUNDED_CORRECTION_RECHECK','executions':len(rows),'former_seven_rejected_each_mode':sum(x['former_false_accept'] for x in rows if x['mode']=='normal')==7,'root_guard_input_SHA256':sha(O/'inputs/final-content-check.proposed.py')},indent=2))

if __name__=='__main__':main()
