"""Exactly one old64 suite,128 full memory renders; bounded changed-read controls."""
from pathlib import Path
import concurrent.futures,datetime,json
from run_stage import O,P,PY,ENV,IDS,run,save,sha
F=['wrong_visible_date','wrong_visible_edition','wrong_citation_edition','omit_status','reorder_status','omit_proof','wrong_iframe','wrong_original_PDF_href','wrong_schema_license','wrong_orcid','changed_reader_bytes','changed_ZIP_bytes','wrong_h1','extra_outside_claim','mislabel_original_PDF','mislabel_original_ZIP','wrong_result_math','raw_TeX_extra','changed_BibTeX']
def checked(args):
    x=run(args)
    if x['exit'] or x['stderr']:raise RuntimeError(x)
    return json.loads(x['stdout'])
def main():
    frozen=json.loads((O/'FROZEN_INPUT_SET.json').read_text());old=frozen['old_configured_record_ids_in_order']
    if len(old)!=64 or (O/'LEGACY_SUITE_ONCE.json').exists():raise RuntimeError('exactly_one_old64_suite')
    save('LEGACY_SUITE_ONCE.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'DISPATCHED_ONCE','record_ids':old})
    proc=run([str(O/'stage_reader.py'),str(O/'final-content-check.stage.py'),*old,'--site',str(O/'public'),'--output-dir',str(O),'--output-stem','legacy64-checks'])
    save('legacy64-checks.execution.json',{k:v for k,v in proc.items() if k!='stdout'});report=json.loads((O/'legacy64-checks.json').read_text())
    if proc['exit'] or proc['stderr'] or report['status']!='PASS':raise RuntimeError(report['issues'])
    save('LEGACY_SUITE_ONCE.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'ONE_DISPATCH_COMPLETE_PASS','record_ids':old,'checks':sum(len(x['checks']) for x in report['papers'].values())})
    print('One full64-record legacy suite passed.',flush=True)
    allinputs={}
    def compare(rid):
        a=checked([str(O/'memory_render.py'),str(O/'inputs/render_page.py'),rid]);b=checked([str(O/'memory_render.py'),str(O/'render_page.proposed.py'),rid])
        if a['outputs']!=b['outputs'] or a['original_read_bindings']!=b['original_read_bindings'] or a['renderer_receipt']!=b['renderer_receipt']:raise RuntimeError('old_renderer_difference:'+rid)
        return {'record_id':rid,'outputs_equal':True,'outputs':a['outputs'],'original_read_bindings':a['original_read_bindings']}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(compare,old))
    for row in rows:
        for path,value in row.pop('original_read_bindings').items():
            if path in allinputs and allinputs[path]!=value:raise RuntimeError('original_input_changed_during_memory_render')
            allinputs[path]=value
    save('LEGACY_RENDERER_INPUTS.json',allinputs)
    save('LEGACY_RENDERER_EQUIVALENCE.json',{'status':'PASS','record_ids':old,'complete_renderer_executions':128,'all_old_outputs_byte_identical':True,'no_old_site_fixture_copies':True,'input_bindings_path':'LEGACY_RENDERER_INPUTS.json','input_bindings_SHA256':sha(O/'LEGACY_RENDERER_INPUTS.json'),'comparisons':rows})
    print('All64 old/proposed complete renderer outputs agree in memory.',flush=True)
    public=[]
    for opt,mode in [(False,'normal'),(True,'optimized')]:
        out=O/mode;out.mkdir(exist_ok=True)
        source=run([str(O/'guard_controls.py')],opt)
        if source['exit'] or source['stderr']:raise RuntimeError(source)
        save('guard-controls-'+mode+'.json',json.loads(source['stdout']))
        positive=run([str(O/'stage_reader.py'),str(O/'final-content-check.stage.py'),*IDS,'--site',str(O/'public'),'--output-dir',str(out),'--output-stem','pristine3'],opt)
        save(mode+'/pristine3.execution.json',{k:v for k,v in positive.items() if k!='stdout'})
        if positive['exit'] or positive['stderr'] or json.loads((out/'pristine3.json').read_text())['status']!='PASS':raise RuntimeError(positive)
        cases=[(rid,case) for rid in IDS for case in F+(['HK_181_to_180'] if rid=='23441617' else [])]
        def fault(pair):
            rid,case=pair;x=run([str(O/'public_fault.py'),rid,case,mode],opt);rp=out/('checker-'+rid+'-'+case+'.json');data=json.loads(rp.read_text()) if rp.exists() else None
            if x['exit']!=1 or x['stderr'] or data is None or data['status']!='ISSUES_FOUND':raise RuntimeError({'record_id':rid,'case':case,'execution':x})
            return {'mode':mode,'record_id':rid,'case':case,'rejected':True,'exit':x['exit'],'issues':data['issues'],'report_SHA256':sha(rp)}
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:public.extend(pool.map(fault,cases))
        print(mode+': pristine3 accepted; '+str(len(cases))+' public faults rejected.',flush=True)
    save('PUBLIC_OUTPUT_CONTROLS.json',{'status':'PASS','cases':public,'faults_rejected_each_mode':58,'pristine_records_accepted_each_mode':3,'source_or_site_fixture_writes':0})
    print(json.dumps({'status':'PASS_ALL_LEGACY_AND_CONTROLS','old_records':64,'one_suite_checks':sum(len(x['checks']) for x in report['papers'].values()),'memory_renderer_executions':128,'public_faults':len(public)}))
if __name__=='__main__':main()
