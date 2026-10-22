from pathlib import Path
R=Path(__file__).resolve().parent
body=(R/'independent_controls.py').read_bytes()
marker=b"w=setup('valid_actual_full_lifecycle')"
if body.count(marker)!=1:raise RuntimeError('Independent helper boundary changed')
prefix=body.split(marker)[0]
if prefix.count(b"('fresh_'+MODE)")!=1:raise RuntimeError('Independent destination boundary changed')
exec(compile(prefix.replace(b"('fresh_'+MODE)",b"('extension_'+MODE)"),str(R/'independent_controls.py')+'[definitions-only]','exec'),globals())

w=setup('ledger_native31seconds_after_complete_gate','ledger');offset=[0];real_datetime=c.dt.datetime
class LateClock(real_datetime):
    @classmethod
    def now(cls,tz=None):return real_datetime.now(tz)+datetime.timedelta(seconds=offset[0])
def late(*a,**k):offset[0]=31
w.gate_hook=late;before=(len(w.native.calls),w.appends)
with model.patch((c.dt,'datetime',LateClock)),w.installed():a,e=run(w,'ledger')
record('ledger_native31seconds_after_complete_gate',w,False,a,e,before,{'native':0,'append':0},{'native_age_advanced_seconds':31})

w=setup('ledger_native_family_changed_after_complete_gate','ledger')
def aftergate(*a,**k):
    def changed(l,n,f):
        l['conceptrecid']='999';l['conceptdoi']='10.5281/zenodo.999'
        n['parent']['id']='999';n['parent']['pids']['doi']['identifier']='10.5281/zenodo.999'
    w.native.fault=changed
w.gate_hook=aftergate;before=(len(w.native.calls),w.appends)
with w.installed():a,e=run(w,'ledger')
record('ledger_native_family_changed_after_complete_gate',w,False,a,e,before,{'native':0,'append':0},{'native_family_after_gate':[777,999],'account_family_at_gate':[777,778]})

w=setup('fullmetadata_hidden_changes_between_paired_gets');original=w.command;count=[0]
def command(argv,body=None):
    value=original(argv,body)
    if argv[0]=='gws' and argv[3]=='get':count[0]+=1;value['sheets'][0]['properties']['hidden']=bool(count[0]%2)
    return value
w.command=command
with w.installed():a,e=run(w,'resume-stage')
record('fullmetadata_hidden_changes_between_paired_gets',w,False,a,e,(0,0),{'native':0,'append':0},{'metadata_call_count':count[0]})

w=setup('publication_revoked_during_postwrite_native_verification','publish');native=modules['native_policy'];writer=native.durable;hit=[False]
def revoke(path,value):
    writer(path,value)
    if path.name=='verified.json' and value.get('published') is True and not hit[0]:
        hit[0]=True;w.ad_path.rename(w.ad_path.with_suffix('.revoked'))
before=(len(w.native.calls),w.appends)
with model.patch((native,'durable',revoke)),w.installed():a,e=run(w,'publish')
# The POST precedes this hook; this case tests certification, not prevention.
record('publication_revoked_during_postwrite_native_verification',w,False,a,e,before,{'native':1,'append':0},{'postwrite_hook_fired':hit[0],'mutation_precedes_revocation':True,'receipt_condition_under_review':True})

w=setup('source_closure_unexpected_cache_file');q=m.CONTEXT['source_root']/'__pycache__';q.mkdir();(q/'lifecycle06.pyc').write_bytes(b'UNTRUSTED-CACHE-MARKER')
with w.installed():a,e=run(w,'resume-stage')
record('source_closure_unexpected_cache_file',w,False,a,e,(0,0),{'native':0,'append':0})

# Combining marks are Unicode word continuations. A safe false-positive may
# still contradict the advertised bounded grammar; it is not a duplicate claim.
w=setup('combining_mark_inside_word_false_lead');w.rows.append(['Other result','','','cafe\u0301PR1131x'])
with w.installed():a,e=run(w,'resume-stage')
record('combining_mark_inside_word_false_lead',w,True,a,e,(0,0),{'native':4,'append':0})

need(not model.ATTEMPTS,'Real escape attempted')
report={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':MODE,'source_sha256':MS,'bootstrap_sha256':BS,
        'case_count':len(checks),'actual_parsed_CLI_cases':len(checks),'counterexamples':[v['case'] for v in checks if v['status']=='COUNTEREXAMPLE'],
        'results':checks,'real_escape_attempts':model.ATTEMPTS,'real_service_or_Git_mutations':0,
        'allocated_bytes':allocated(),'publication_ready':False}
(DEST/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
