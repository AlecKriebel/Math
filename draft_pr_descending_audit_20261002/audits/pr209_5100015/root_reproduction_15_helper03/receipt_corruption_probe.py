"""Exact-source single-artifact corruption counterexample; no function rewrites."""
import adversarial_controls as H
import copy,json,traceback
D=H.D
f=H.Fixture('receipt_corruption_final')
H.quiet(f.prepare);H.quiet(f.merge)
path=f.pub/'PR_MERGED.json';raw=path.read_bytes();original=json.loads(raw);fixed=len(f.mutations)
rb=f.rb;i=f.module('integrate_reviewed_pr.py');m=f.module('verify_and_merge.py');ctx=rb.context(f.r);z=rb.publication(f.r,f.pub,ctx);t=rb.tracker(f.r,f.pub,ctx,z)
api=i.NativeAPI(f.pub,'independent_corruption_readonly',readonly=True);trees=i.NativeTrees(api)
prep,built,packet,row=m.prepared_authority(f.r,f.pub,ctx,z,t,api,trees)
progress=m.progress_baseline(f.r,f.pub,ctx,api,trees)
intake=json.loads(i.safe_read(f.c,'initial_review_20261016/INTAKE.json'))
base=api('GET','git/commits/'+prep['main_parent']);prefix=f.c.relative_to(f.root).as_posix()+'/'
args=m.load_merge(f.pub,ctx,built,packet,intake,z,progress,api,trees,base,prefix)
outcomes={}
for key,value in [('doi_url','https://doi.org/10.5281/zenodo.999999999'),('tracker_range',"'Wrong tab'!Z999:AC999"),('case_completion_percent',1),('actual_publication_tracker_native_merge_complete',False),('exact_native_body_readbacks',[]),('merged',False)]:
 changed=copy.deepcopy(original);changed[key]=value;H.dump(path,changed)
 try:
  returned=m.complete_merge(f.r,f.pub,ctx,z,t,*args,progress,api,trees)
  outcomes[key]=dict(accepted=returned[key]==value,corrupted_value=value,unchanged_retained_bytes=path.read_bytes()==(json.dumps(changed,indent=2)+'\n').encode(),no_provider_mutations=len(f.mutations)==fixed)
 except Exception as e:outcomes[key]=dict(accepted=False,error=repr(e),traceback=traceback.format_exc())
 H.dump(f.base/('CORRUPT_'+key+'.json'),dict(changed_receipt=changed,outcome=outcomes[key]));path.write_bytes(raw)
 print(json.dumps(dict(field=key,outcome=outcomes[key])),flush=True)
H.dump(f.base/'CORRUPTION_OUTCOMES.json',outcomes);f.trace()
H.dump(D/'RECEIPT_CORRUPTION_RESULT.json',dict(utc=H.utc(),outcomes=outcomes,all6_corruptions_accepted=all(x.get('accepted') is True for x in outcomes.values()),byte_exact_candidates=True,provider_and_path_substitutions_only=True,case_completion_percent=65,no_release_authority=True))
H.compact('receipt_corruption_final')
assert all(x.get('accepted') is True for x in outcomes.values()),outcomes
