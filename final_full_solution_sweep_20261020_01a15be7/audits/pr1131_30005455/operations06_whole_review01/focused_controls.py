from pathlib import Path
R=Path(__file__).resolve().parent
body=(R/'independent_controls.py').read_bytes();marker=b"w=setup('valid_actual_full_lifecycle')"
if body.count(marker)!=1:raise RuntimeError('Independent helper changed')
prefix=body.split(marker)[0]
exec(compile(prefix.replace(b"('fresh_'+MODE)",b"('focused_'+MODE)"),str(R/'independent_controls.py')+'[definitions-only]','exec'),globals())

w=setup('reviewed_known_PR_lead_remains_distinct')
row=['Independently reconciled separate result','','','Source cross-reference: pull request #1131']
w.rows.append(row);ad=json.loads(w.ad_path.read_bytes());ad['distinct_ledger_row_sha256']=[c.digest(row)];w.ad_path.write_text(json.dumps(ad)+'\n');w.clearance_sha=sha(w.ad_path.read_bytes())
with w.installed():a,e=run(w,'resume-stage')
record('reviewed_known_PR_lead_remains_distinct',w,True,a,e,(0,0),{'native':4,'append':0},{'exact_root_distinct_row_hash':c.digest(row)})

for phase in ['upload','update']:
    label='lost_'+phase+'_after_server_success';w=setup(label);original=getattr(w.native,phase)
    def lost(*a,**k):original(*a,**k);raise c.zenodo.DepositError('Independent lost '+phase+' response after server success')
    setattr(w.native,phase,lost)
    with w.installed():
        a,e=run(w,'resume-stage');count=(len(w.native.calls),w.appends);again,err=run(w,'resume-stage')
    receipt=json.loads((m.RUNTIME/'RESUME_STAGE_FAILURE.json').read_bytes())
    need(receipt['delegate_known_id']==777 and count==(len(w.native.calls),w.appends),'Known-ID custody/reentry failed')
    record(label,w,False,a,e,(0,0),{'native':2 if phase=='upload' else 4,'append':0},{'failure_receipt':receipt,'reentry_error':err})

w=setup('known_original_intent_drift_inside_update');original=w.native.update

def update(*a,**k):
    result=original(*a,**k);q=m.PRIOR_RUNTIME/'ZENODO_STAGE_INTENT.json';v=json.loads(q.read_bytes());v['id']=999;q.write_text(json.dumps(v)+'\n');return result
w.native.update=update
with w.installed():a,e=run(w,'resume-stage')
receipt=json.loads((m.RUNTIME/'RESUME_STAGE_FAILURE.json').read_bytes())
need(receipt['delegate_known_id']==777 and not (m.RUNTIME/'ZENODO_STAGE_VERIFIED.json').exists(),'Known update drift falsely verified')
record('known_original_intent_drift_inside_update',w,False,a,e,(0,0),{'native':4,'append':0},{'failure_receipt':receipt})

w=setup('lost_append_success_GET_only_reentry','ledger');w.append_mode='lost';before=(len(w.native.calls),w.appends)
with w.installed():
    a,e=run(w,'ledger');count=w.appends;again,err=run(w,'ledger')
need(w.appends==count==1 and err is None and again['new_row'] is False,'Lost append retried or unreconciled')
record('lost_append_success_GET_only_reentry',w,False,a,e,before,{'native':0,'append':1},{'reentry_answer':again,'reentry_error':err})

need(not model.ATTEMPTS,'Real escape attempted')
report={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':MODE,'source_sha256':MS,'bootstrap_sha256':BS,'case_count':len(checks),'actual_parsed_CLI_cases':len(checks),'counterexamples':[v['case'] for v in checks if v['status']=='COUNTEREXAMPLE'],'results':checks,'real_escape_attempts':model.ATTEMPTS,'real_service_or_Git_mutations':0,'allocated_bytes':allocated(),'publication_ready':False}
(DEST/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
