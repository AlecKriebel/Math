"""Replay all31 sealed auditor faults per mode; reuse pristine3 already run."""
from pathlib import Path
import ast,datetime,difflib,json
from prior_recheck import O,P,S,run,save,sha,once
A=P/'verification/audit-spanning-sos-gin-code-sol-20261025'
def main():
    if (O/'AUDITOR_DISPATCH_ONCE.json').exists():raise RuntimeError('no_duplicate_auditor_fault_replay')
    pins={'REPORT.md':'09c9b3b3ceba9a0a2658d399f487f8629d5a513f67974ce945d1fe1a97ae8801','FINAL_MANIFEST.json':'990e920dd02c6d2b09f6b4248bc6afd0a44c2ad95b240594b63c8fb313b683d8','FINAL_SEAL.json':'6f8a2f365de2c3b3a20cb2ab59685c992f9802fab0fcd0685737dc186d12f3af','checker_control.py':'828ba113c2018ce7935be1bbc65488cc399739553c89721b180c5fad338238e0'}
    for n,h in pins.items():
        if sha(A/n)!=h:raise RuntimeError('sealed_auditor_input:'+n)
    manifest=json.loads((A/'FINAL_MANIFEST.json').read_text());originals=[]
    for x in manifest['files']:
        p=A/x['path']
        if p.stat().st_size!=x['bytes'] or sha(p)!=x['sha256']:raise RuntimeError('auditor_owned_binding')
        originals.append({'path':str(p),'bytes':x['bytes'],'SHA256':x['sha256']})
    for n in ['FINAL_MANIFEST.json','FINAL_SEAL.json']:originals.append({'path':str(A/n),'bytes':(A/n).stat().st_size,'SHA256':sha(A/n)})
    save('AUDITOR_INPUT_CUSTODY.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'root_report_manifest_seal_pins':pins,'original_files':originals,'variant_code_read_after_final_seal_and_own_early_mechanism':True})
    code=(A/'checker_control.py').read_text();(O/'inputs/checker_control.original.py').write_text(code)
    target=O/'auditor';target.mkdir(exist_ok=True)
    adapted=once(code,'E=Path(__file__).resolve().parent','E=Path('+repr(str(target))+')')
    adapted=once(adapted,'P=E.parents[1]','P=Path('+repr(str(P))+')')
    adapted=once(adapted,"str(S/'final-content-check.stage.py')","str(Path("+repr(str(O))+")/'final-content-check.stage.py')")
    ast.parse(adapted);(O/'checker_control.recheck.py').write_text(adapted)
    (O/'auditor-dispatch-only.diff').write_text(''.join(difflib.unified_diff(code.splitlines(True),adapted.splitlines(True),fromfile='sealed-auditor-driver',tofile='own-output-and-new-checker-only')))
    plan=json.loads((A/'CONTROL_PLAN.json').read_text());cases=[x for x in plan['cases'] if not x['intended_acceptance']]
    if len(cases)!=31:raise RuntimeError('31_auditor_faults_required')
    prior=json.loads((O/'PRIOR_RESULTS.json').read_text())
    if prior['status']!='PASS':raise RuntimeError('pristine3_and_prior35_required')
    save('AUDITOR_DISPATCH_ONCE.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'faults_each_mode':31,'negative_dispatches':62,'three_pristine_plan_entries_reused_from_prior_new_checker_runs':True,'old61_suite_runs':0})
    rows=[]
    for opt,mode in [(False,'normal'),(True,'optimized')]:
        for item in cases:
            rid=item['record'];case=item['case'];execution=run([str(O/'checker_control.recheck.py'),rid,case,mode],opt);save('auditor/'+mode+'/'+rid+'-'+case+'-execution.json',execution)
            rp=target/mode/(rid+'-'+case+'.json');data=json.loads(rp.read_text()) if rp.exists() else None
            if execution['exit']!=1 or execution['stderr'] or data is None or data['status']!='ISSUES_FOUND':raise RuntimeError((rid,case,mode,execution))
            original=json.loads((A/mode/(rid+'-'+case+'-mutation.json')).read_text());actual=json.loads((target/mode/(rid+'-'+case+'-mutation.json')).read_text())
            if {k:v for k,v in original.items() if k!='writes_guarded_to'}!={k:v for k,v in actual.items() if k!='writes_guarded_to'}:raise RuntimeError('auditor_fault_bytes_changed')
            old_result=json.loads((A/mode/(rid+'-'+case+'.json')).read_text());former=old_result['status']=='PASS'
            required={'wrong_visible_h1':'exact_visible_h1','unapproved_body_claim':'exact_approved_whole_body_text','Gin_TeX_link_mislabelled':'exact_visible_original_TeX_link_label'}.get(case)
            if former and (required is None or rid+': '+required not in data['issues']):raise RuntimeError('former_false_accept_not_caught_by_expected_new_guard')
            rows.append({'mode':mode,'record_id':rid,'case':case,'rejected':True,'former_false_accept':former,'specific_new_guard':required,'issues':data['issues'],'original_and_changed_byte_identities_equal_sealed_auditor':True,'only_receipt_difference':'writes_guarded_to identifies own new output namespace','report_SHA256':sha(rp)})
        print(mode+': all31 auditor faults reject; former7 reject through expected new guards.',flush=True)
    if any(sum(x['former_false_accept'] for x in rows if x['mode']==m)!=7 for m in ['normal','optimized']):raise RuntimeError('former_seven_count')
    save('AUDITOR_REPLAY_RESULTS.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','root_corrected_checker_SHA256':sha(O/'inputs/final-content-check.proposed.py'),'auditor_faults_each_mode':31,'former_false_accepts_rejected_each_mode':7,'pristine3_reused_from_prior_results':True,'all_original_mutations_unchanged':True,'old61_suite_rerun':False,'cases':rows})
    print(json.dumps({'status':'PASS_ALL_AUDITOR_VARIANTS','negative_dispatches':62,'former_seven_reject_each_mode':True},indent=2))
if __name__=='__main__':main()
