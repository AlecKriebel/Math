from pathlib import Path
R=Path(__file__).resolve().parent;body=(R/'independent_controls.py').read_bytes();marker=b"w=setup('valid_actual_full_lifecycle')"
if body.count(marker)!=1:raise RuntimeError('Independent helper changed')
prefix=body.split(marker)[0]
exec(compile(prefix.replace(b"('fresh_'+MODE)",b"('identity_'+MODE)"),str(R/'independent_controls.py')+'[definitions-only]','exec'),globals())
for field,value in [('id',999),('manifest','/unreviewed/replacement-manifest.json'),('environment','sandbox')]:
    label='saved_original_manifest_'+field;w=setup(label,'publish');q,state=c.zenodo.local_state(pub.MANIFEST.resolve(),'production');state[field]=value;q.write_text(json.dumps(state)+'\n');before=(len(w.native.calls),w.appends)
    with w.installed():a,e=run(w,'publish')
    record(label,w,False,a,e,before,{'native':0,'append':0},{'corrupted_field':field})

w=setup('create_gate_ages_after_fsynced_write_intent');writer=c.durable;real_datetime=c.dt.datetime;offset=[0]
class ReviewClock(real_datetime):
    @classmethod
    def now(cls,tz=None):return real_datetime.now(tz)+datetime.timedelta(seconds=offset[0])
def aged(path,value):
    writer(path,value)
    if path.name=='WRITE_stage_create_INTENT.json':offset[0]=181
with model.patch((c,'durable',aged),(c.dt,'datetime',ReviewClock)),w.installed():a,e=run(w,'resume-stage')
record('create_gate_ages_after_fsynced_write_intent',w,False,a,e,(0,0),{'native':0,'append':0})

w=setup('fresh_native_gate_may_be_consumed_once');args=types.SimpleNamespace(deposit_id=None,clearance_sha256=w.clearance_sha,operations_sha256=MS,expected_pr_head=m.HEAD)
with w.installed():
    guard=pub.GuardedClient(args,'stage',None);guard.before(None);first=guard.delegate.create(guard.metadata)
    try:guard.delegate.create(guard.metadata);a={};e=None
    except Exception as exc:a=None;e={'type':type(exc).__name__,'message':str(exc)}
need(e is not None and 'fresh unused' in e['message'],'Consumed guard was reusable')
record('fresh_native_gate_may_be_consumed_once',w,False,a,e,(0,0),{'native':1,'append':0},{'component_case':True,'first_returned_id':first['id']})
need(not model.ATTEMPTS,'Real escape attempted')
report={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':MODE,'source_sha256':MS,'bootstrap_sha256':BS,'case_count':len(checks),'actual_parsed_CLI_cases':sum(not q.get('component_case',False) for q in checks),'counterexamples':[v['case'] for v in checks if v['status']=='COUNTEREXAMPLE'],'results':checks,'real_escape_attempts':model.ATTEMPTS,'real_service_or_Git_mutations':0,'allocated_bytes':allocated(),'publication_ready':False}
(DEST/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
