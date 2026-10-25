"""One old-content suite plus full renderer comparisons, without old-site copies."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,os,subprocess,signal,sys
from run_stage import O,R,PY,ENV,run,save

def checked(command):
    p=run(command)
    if p['exit'] or p['stderr']:raise RuntimeError(p)
    return json.loads(p['stdout'])

def main():
    frozen=json.loads((O/'FROZEN_INPUT_SET.json').read_text());ids=frozen['old_configured_record_ids_in_order']
    if len(ids)!=59:raise RuntimeError('frozen59_required')
    # This file makes an accidental second full suite explicit rather than silently repeating.
    marker=O/'LEGACY_FULL_SUITE_ONCE.json'
    if marker.exists():raise RuntimeError('full_legacy_suite_already_dispatched')
    save(marker.name,{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'DISPATCHED_ONCE','record_ids':ids})
    proc=run([str(O/'stage_reader.py'),str(O/'final-content-check.stage.py'),*ids,'--site',str(O/'public'),'--output-dir',str(O),'--output-stem','legacy-full-proposed'])
    save('legacy-full-proposed.stdout.txt',proc['stdout']);save('legacy-full-proposed.stderr.txt',proc['stderr'])
    report=json.loads((O/'legacy-full-proposed.json').read_text())
    if proc['exit'] or proc['stderr'] or report['status']!='PASS':raise RuntimeError({'execution':proc,'issues':report['issues']})
    save(marker.name,{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'COMPLETE_PASS_ONE_DISPATCH','record_ids':ids,'checks':sum(len(x['checks']) for x in report['papers'].values())})
    print('One complete59-record legacy suite passed.',flush=True)
    def compare(rid):
        a=checked([str(O/'memory_render.py'),str(O/'inputs/render_page.py'),rid]);b=checked([str(O/'memory_render.py'),str(O/'render_page.proposed.py'),rid])
        if a['outputs']!=b['outputs'] or a['original_read_bindings']!=b['original_read_bindings'] or a['renderer_receipt']!=b['renderer_receipt']:raise RuntimeError('old_renderer_difference:'+rid)
        return {'record_id':rid,'all_original_and_proposed_output_bytes_equal':True,'filesystem_output_writes':0,'outputs':a['outputs'],'original_read_bindings':a['original_read_bindings']}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:comparisons=list(pool.map(compare,ids))
    save('legacy-renderer-equivalence.json',{'status':'PASS','record_ids':ids,'complete_renderer_executions':118,'all59_original_and_proposed_outputs_equal':True,'source_input_read_bindings_equal':True,'no_old_site_fixture_copies':True,'comparisons':comparisons})
    print('All59 complete original/proposed renderer outputs agree byte for byte in memory.',flush=True)
    for optimized in [False,True]:
        cmd=[PY,'-B']+(['-O'] if optimized else [])+[str(O/'guard_controls.py')]
        p=subprocess.run(cmd,env=ENV,text=True,capture_output=True,timeout=60)
        if p.returncode or p.stderr:raise RuntimeError(p.stderr or p.stdout)
        data=json.loads(p.stdout);save('guard-controls'+('-optimized' if optimized else '')+'.json',data)
    public_controls()
    print(json.dumps({'status':'PASS_LEGACY_AND_CONTROLS','legacy_records':59,'full_legacy_suite_dispatches':1,'legacy_checks':sum(len(x['checks']) for x in report['papers'].values()),'complete_memory_renderer_executions':118,'public_rejection_controls':4},indent=2))

def public_controls():
    controls=[]
    for rid in ['23387774','23074543']:
        for case,tag in [('missing_result','whole_every_rate_geometric_marked_PPP_and_moments' if rid=='23387774' else 'separate_fullD_every_subset_GP_and_relative_S'),('changed_complete_support','exact_complete_PDF_ZIP_bytes')]:
            proc=run([str(O/'checker_public_fault.py'),rid,case]);name='negative-public-'+rid+'-'+case
            save(name+'.stdout.txt',proc['stdout']);save(name+'.stderr.txt',proc['stderr'])
            data=json.loads((O/(name+'.json')).read_text())
            if proc['exit']==0 or proc['stderr'] or data['status']!='ISSUES_FOUND' or rid+': '+tag not in data['issues']:raise RuntimeError({'execution':proc,'issues':data.get('issues')})
            controls.append({'record_id':rid,'case':case,'rejected':True,'issues':data['issues'],'expected_guard':tag})
    save('public-output-rejection-controls.json',{'status':'PASS','no_fixture_writes':True,'controls':controls})
    print(json.dumps({'status':'PASS_PUBLIC_REJECTION_CONTROLS','public_rejection_controls':len(controls)},indent=2))

if __name__=='__main__':
    if sys.argv[1:]==['--public-controls-only']:public_controls()
    else:main()
