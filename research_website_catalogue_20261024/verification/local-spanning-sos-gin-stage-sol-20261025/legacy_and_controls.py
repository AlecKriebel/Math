"""One full61 legacy suite,122 in-memory renders and bounded changed reads."""
from pathlib import Path
import concurrent.futures,datetime,json,subprocess
from run_stage import O,P,PY,ENV,IDS,run,save,sha
def checked(args):
    x=run(args)
    if x['exit'] or x['stderr']:raise RuntimeError(x)
    return json.loads(x['stdout'])
def main():
    frozen=json.loads((O/'FROZEN_INPUT_SET.json').read_text());old=frozen['old_configured_record_ids_in_order']
    if len(old)!=61 or (O/'LEGACY_SUITE_ONCE.json').exists():raise RuntimeError('exactly_one_current61_suite_required')
    save('LEGACY_SUITE_ONCE.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'DISPATCHED_ONCE','record_ids':old})
    proc=run([str(O/'stage_reader.py'),str(O/'final-content-check.stage.py'),*old,'--site',str(O/'public'),'--output-dir',str(O),'--output-stem','legacy61-checks'])
    save('legacy61-checks.execution.json',proc);report=json.loads((O/'legacy61-checks.json').read_text())
    if proc['exit'] or proc['stderr'] or report['status']!='PASS':raise RuntimeError(report['issues'])
    save('LEGACY_SUITE_ONCE.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'ONE_DISPATCH_COMPLETE_PASS','record_ids':old,'checks':sum(len(x['checks']) for x in report['papers'].values())})
    print('One complete61-record legacy suite passed.',flush=True)
    def compare(rid):
        a=checked([str(O/'memory_render.py'),str(O/'inputs/render_page.py'),rid]);b=checked([str(O/'memory_render.py'),str(O/'render_page.proposed.py'),rid])
        if a['outputs']!=b['outputs'] or a['original_read_bindings']!=b['original_read_bindings'] or a['renderer_receipt']!=b['renderer_receipt']:raise RuntimeError('old_renderer_difference:'+rid)
        return {'record_id':rid,'outputs_equal':True,'filesystem_output_writes':0,'outputs':a['outputs'],'original_read_bindings':a['original_read_bindings']}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(compare,old))
    save('LEGACY_RENDERER_EQUIVALENCE.json',{'status':'PASS','record_ids':old,'complete_renderer_executions':122,'all_old_outputs_byte_identical':True,'no_old_site_fixture_copies':True,'comparisons':rows})
    print('All61 complete original/proposed renderer outputs agree in memory.',flush=True)
    public=[]
    faults=['wrong_visible_date','wrong_visible_edition','wrong_visible_citation_edition','omit_status_paragraph','omit_proof_paragraph','wrong_iframe','wrong_original_download','wrong_schema_license','wrong_orcid','wrong_readable_math','altered_reader_bytes']
    for opt,mode in [(False,'normal'),(True,'optimized')]:
        out=O/mode;out.mkdir(exist_ok=True)
        source=run([str(O/'guard_controls.py')],opt)
        if source['exit'] or source['stderr']:raise RuntimeError(source)
        save('guard-controls-'+mode+'.json',json.loads(source['stdout']))
        positive=run([str(O/'stage_reader.py'),str(O/'final-content-check.stage.py'),*IDS,'--site',str(O/'public'),'--output-dir',str(out),'--output-stem','pristine3'],opt)
        save(mode+'/pristine3.execution.json',positive)
        if positive['exit'] or positive['stderr'] or json.loads((out/'pristine3.json').read_text())['status']!='PASS':raise RuntimeError(positive)
        for rid in IDS:
            for case in faults+(['drop_TeX_original_link','invent_Gin_schema_version'] if rid=='23395703' else []):
                x=run([str(O/'public_fault.py'),rid,case,mode],opt);save(mode+'/execution-'+rid+'-'+case+'.json',x)
                rp=out/('checker-'+rid+'-'+case+'.json');data=json.loads(rp.read_text()) if rp.exists() else None
                if x['exit']!=1 or x['stderr'] or data is None or data['status']!='ISSUES_FOUND':raise RuntimeError({'record_id':rid,'case':case,'execution':x})
                required={'wrong_visible_date':'visible_exact_byline_declared_date_header_edition','wrong_visible_edition':'visible_exact_byline_declared_date_header_edition','wrong_visible_citation_edition':'visible_exact_citation_edition','omit_status_paragraph':'all_exact_approved_status_paragraphs','drop_TeX_original_link':'all_three_assets_and_ordinary_TeX_link','invent_Gin_schema_version':'jsonld'}.get(case)
                if required and rid+': '+required not in data['issues']:raise RuntimeError('expected_specific_guard_not_fired')
                public.append({'mode':mode,'record_id':rid,'case':case,'rejected':True,'issues':data['issues'],'specific_guard':required,'report_SHA256':sha(rp)})
        print(mode+': three pristine records accepted;35 output mutations rejected.',flush=True)
    save('PUBLIC_OUTPUT_CONTROLS.json',{'status':'PASS','cases':public,'faults_rejected_each_mode':35,'pristine_records_accepted_each_mode':3,'source_or_site_fixture_writes':0})
    print(json.dumps({'status':'PASS_ALL_LEGACY_AND_CONTROLS','old_records':61,'one_full_suite_checks':sum(len(x['checks']) for x in report['papers'].values()),'memory_renderer_executions':122,'public_faults':len(public)},indent=2))
if __name__=='__main__':main()
