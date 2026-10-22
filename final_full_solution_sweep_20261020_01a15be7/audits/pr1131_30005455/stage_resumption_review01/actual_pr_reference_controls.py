"""Known labelled PR identity controls through actual parsed production stage.

Reuses this review's fully read fixture construction and production bundle;
changes only the owned output namespace of that construction.
"""
from pathlib import Path
import contextlib, io, json, sys, hashlib

HERE=Path(__file__).resolve().parent
driver=HERE/'actual_wrapper_controls.py';raw=driver.read_text()
delimiter="\nw,n,args,rt,ap,old=world('valid_first_actual_stage')"
if raw.count(delimiter)!=1:raise RuntimeError('fixture construction boundary changed')
prefix=raw.split(delimiter)[0]
needle="DEST=ROOT/'private'/('cases_'+MODE)"
if prefix.count(needle)!=1:raise RuntimeError('owned namespace boundary changed')
prefix=prefix.replace(needle,"DEST=ROOT/'private'/('reference_cases_'+MODE)")
ns={'__file__':str(driver),'__name__':'independent_reference_fixture'}
exec(compile(prefix,str(driver),'exec'),ns)
world,record,need=ns['world'],ns['record'],ns['need']
pub=ns['pub'];MODE=ns['MODE'];DEST=ns['DEST']
answers=[]
for label,reference,should_hold in [
    ('known_compact_pull_request','pull request1131',False),
    ('known_spaced_pull_request','pull request 1131',False),
    ('known_hash_pull_request','pull request #1131',False),
    ('known_PR_hash_control','PR #1131',True),
    ('known_full_URL_control','https://github.com/AlecKriebel/Math/pull/1131',True),
    ('nearby_11310_control','pull request11310',False),
]:
    w,n,args,rt,ap,old=world(label)
    # The actual parsed original stage CLI, rather than this proposed wrapper,
    # owns its first stage intent. Preserve the unused input fixture separately.
    (rt/'ZENODO_STAGE_INTENT.json').rename(rt/'UNUSED_INPUT_FIXTURE_STAGE_INTENT.json')
    row=['Universal finite-graph surviving structure for alpha above4/3 at arbitrary positive vertex rates and positive integer initial counts',
         '','',f'Earlier solution audited in {reference}.']
    w.rows.append(row)
    before=sys.argv;output=io.StringIO();failure=None;answer=None
    try:
        sys.argv=['publish_and_ledger','stage','--expected-pr-head',w.git.head,
                  '--clearance-sha256',w.clearance_sha,'--operations-sha256',ns['MS']]
        try:
            with w.installed(),contextlib.redirect_stdout(output):pub.main()
        except Exception as exc:failure={'type':type(exc).__name__,'message':str(exc)}
        else:answer=json.loads(output.getvalue())
    finally:sys.argv=before
    if should_hold:
        need(failure is not None and not w.native.calls and 'ledger lead' in failure['message'],
             'positive identity guard did not reject before create')
    else:
        need(failure is None and answer['state']=='ready_to_publish' and w.native.calls.count('create')==1,
             'explicit known-reference bypass/nearby control not reproduced')
    item={'case':label,'reference':reference,'existing_row':row,'counterexample':label.startswith('known_') and not should_hold,
          'full_actual_parsed_production_CLI':True,'result':answer,'exception':failure,
          'native_calls':list(w.native.calls),'create_POSTs':w.native.calls.count('create'),
          'stage_verified':(rt/'ZENODO_STAGE_VERIFIED.json').exists(),
          'account_page_observations':len([v for v in w.events if 'account_page' in v]),
          'numeric_view_reads':w.numeric_calls,'real_service_mutations':0}
    answers.append(item)
    (DEST/(label+'.json')).write_text(json.dumps(item,indent=2)+'\n')
    need(ns['allocated']()<50*1024*1024,'owned50MiB cap')
    print(json.dumps({'case':label,'creates':item['create_POSTs'],'counterexample':item['counterexample']}),flush=True)
need(not ns['model'].ATTEMPTS,'real network/process escape')
summary={'mode':MODE,'fixture_driver_sha256':hashlib.sha256(driver.read_bytes()).hexdigest(),
         'operations_manifest_sha256':ns['MS'],'cases':answers,'case_count':len(answers),
         'actual_service_mutations':0,'real_escape_attempts':ns['model'].ATTEMPTS,
         'allocated_bytes':ns['allocated']()}
(HERE/('PR_REFERENCE_RESULTS_'+MODE+'.json')).write_text(json.dumps(summary,indent=2)+'\n')
