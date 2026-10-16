"""Final exact-source checks after strict identity/readback refinements."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,json,traceback
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('repair_fixture_final',HERE/'probes_01.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
p.RUNS=HERE/'probe_runs_03';p.SNAP=HERE/'source_snapshot_03'
p.SOURCE={n:(HERE.parent/n).read_bytes() for n in p.NAMES}
RESULTS=[]
def test(label,fn):
    try:r={'label':label,'status':'PASS','detail':fn()}
    except Exception as e:r={'label':label,'status':'FAIL','error':repr(e),'traceback':traceback.format_exc()}
    RESULTS.append(r);p.dump(HERE/'PROBE_RESULTS_03.json',RESULTS);print(json.dumps(r),flush=True)
def unknown_stage():
    f=p.Fixture('unknown_stage');real=f.run
    def run(args,**kw):
        result=real(args,**kw)
        if len(args)>3 and args[3]=='stage':raise TimeoutError('Synthetic stage response lost after stub stage')
        return result
    f.run=run;first=p.reject(f.publish);before=len(f.calls);second=p.reject(f.publish)
    assert f.stages==1 and f.publishes==0 and len(f.calls)==before
    f.trace();return {'first':first,'blocked_retry':second,'stage_calls':1,'publish_calls':0,'retry_provider_calls':0}
def sync_failure():
    f=p.Fixture('sync_failure');real=f.rb.sync_directory
    def sync(path):
        if path==f.pub and (f.pub/'STAGE_ATTEMPT.json').exists():raise OSError('Synthetic parent fsync failure')
        return real(path)
    f.rb.sync_directory=sync;err=p.reject(f.publish);assert f.stages==f.publishes==0 and (f.pub/'STAGE_ATTEMPT.json').exists()
    f.trace();return {'error':err,'no_provider_mutation':True,'intent_retained':True}
def boolean_id():
    f=p.Fixture('boolean_id');real=f.v
    def one(state='published'):
        v=real(state);v.update(id=1,doi='10.5281/zenodo.1',doi_url='https://doi.org/10.5281/zenodo.1',record_url='https://zenodo.org/records/1')
        v['doi_resolution'].update(url=v['doi_url'],resolved_url=v['record_url']);return v
    f.v=one;f.publish();path=f.pub/'PUBLISH_ATTEMPT.json';a=json.loads(path.read_text());a['id']=True;p.dump(path,a)
    return p.reject(lambda:f.rb.publication(f.r,f.pub,f.ctx))
def spreadsheet_id():
    f=p.Fixture('spreadsheet_id');f.publish();real=f.run
    def run(args,**kw):
        result=real(args,**kw)
        if args[0].endswith('/gws') and args[1:4]==['sheets','spreadsheets','get']:
            v=json.loads(result.stdout);v['spreadsheetId']='other';result.stdout=json.dumps(v)
        return result
    f.run=run;err=p.reject(f.append);assert f.appends==0
    f.trace();return {'error':err,'append_calls':0}
def append_data_range():
    f=p.Fixture('append_data_range');f.publish();real=f.run
    def run(args,**kw):
        result=real(args,**kw)
        if args[0].endswith('/gws') and len(args)>4 and args[4]=='append':
            v=json.loads(result.stdout);v['updates']['updatedData']['range']='Other sheet!Z9';result.stdout=json.dumps(v)
        return result
    f.run=run;err=p.reject(f.append);assert f.appends==1 and not (f.pub/'TRACKER_VERIFIED_APPEND.json').exists()
    f.trace();return {'error':err,'append_calls':1,'no_verified_receipt':True}
if __name__=='__main__':
    p.SNAP.mkdir()
    for n,raw in p.SOURCE.items():(p.SNAP/n).write_bytes(raw)
    p.dump(HERE/'EXACT_SOURCE_INPUTS_03.json',{'utc':datetime.now(timezone.utc).isoformat(),'case_completion_percent':55,'files':[p.pin(p.SNAP/n,HERE) for n in p.NAMES]})
    for label,fn in [('final_baseline',p.baseline),('unknown_stage',unknown_stage),('stage_intent_sync_failure',sync_failure),
        ('boolean_publication_id',boolean_id),('wrong_spreadsheet_id',spreadsheet_id),('wrong_append_data_range',append_data_range)]:
        test(label,fn)
    raise SystemExit(0 if all(r['status']=='PASS' for r in RESULTS) else 1)
