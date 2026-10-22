"""Additional real parsed06 controls with uploader/collector state stores identical."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
body=(HERE/'controls06.py').read_bytes()
marker=b'# Grammar coverage is deliberately bounded; do not reintroduce a substring'
if body.count(marker)!=1:raise RuntimeError('Helper definition boundary changed')
prefix=body.split(marker)[0]
old=b"('controls_v3_'+MODE)"
if prefix.count(old)!=1:raise RuntimeError('Helper output boundary changed')
exec(compile(prefix.replace(old,b"('aligned_state_'+MODE)"),str(HERE/'controls06.py')+'[definitions-only]','exec'),globals())

w=world('complete_lifecycle_same_state_store')
c.zenodo.STATE_DIR=live.REPO/'.zenodo-state'
with w.installed():
    staged=cli(w);state_path,state=c.zenodo.local_state(pub.MANIFEST.resolve(),'production')
    need(state is not None and state['id']==777 and live.REPO in state_path.parents,'Uploader/collector state stores differ')
    publication=cli(w,'publish');ledger=cli(w,'ledger')
gates=[json.loads(p.read_bytes()) for p in (w.place/'private').rglob('gate.json')]
target_gates=[g for g in gates if g['target_id']==777]
need(target_gates and all(any(s['id']==777 for s in g['local_states']) for g in target_gates)
     and ledger['verified'] and w.appends==1 and w.native.calls.count('create')==w.native.calls.count('publish')==1,
     'Actual saved target state not covered by complete gates')
finish('complete_lifecycle_same_state_store',w,None,{'all_target_gates_contain_exact_saved_state':True,'target_gate_count':len(target_gates)})

w=world('unreviewed_local_reference_after_stage')
c.zenodo.STATE_DIR=live.REPO/'.zenodo-state'
with w.installed():
    cli(w)
    (c.zenodo.STATE_DIR/'unreviewed_source.json').write_text(json.dumps({'id':42,'result':{'source':'pull request #001131'}})+'\n')
    error=failure(lambda:cli(w,'publish'))
need(w.native.calls.count('publish')==0 and 'local deposit state' in error['message'],'Poststage local source reference reached publication')
finish('unreviewed_local_reference_after_stage',w,error,{'same_original_manifest_state_store':True})
need(not model.ATTEMPTS,'Real external call attempted')
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','mode':MODE,
     'sources_sha256':MS,'bootstrap_sha256':BS,'helper_sha256':hashlib.sha256(body).hexdigest(),
     'full_parsed_CLI_cases':len(results),'results':results,'same_uploader_collector_state_directory':True,
     'real_external_mutations':0,'real_external_attempts':model.ATTEMPTS,'publication_ready':False}
(DEST/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='results'},indent=2))
