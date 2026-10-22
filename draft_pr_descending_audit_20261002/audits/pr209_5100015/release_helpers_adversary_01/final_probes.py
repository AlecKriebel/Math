"""Receipt lineage, version drift, durability failure and merge controls."""
import json
import probes as p

RESULTS=[]
def run(label,fn):
 try:RESULTS.append(dict(label=label,status='PASS',detail=fn()))
 except Exception as e:RESULTS.append(dict(label=label,status='PROBE_ERROR',error=type(e).__name__+': '+str(e)))
 p.dump(p.HERE/'FINAL_PROBE_RESULTS.json',RESULTS);print(json.dumps(RESULTS[-1]))

def missing_publication_lineage():
 f=p.Fixture('missing_publication_lineage');assert not (f.pub/'STAGE_ATTEMPT.json').exists() and not (f.pub/'PUBLISH_ATTEMPT.json').exists()
 z=f.rb.publication(f.r,f.pub,f.ctx);f.execute('verify_published_readonly.py');f.save()
 return dict(accepted_id=z['id'],stage_intent_exists=False,publish_intent_exists=False,provider_readbacks_requested=len(f.calls))

def version_drift():
 f=p.Fixture('version_drift');(f.pub/'TRACKER_VERIFIED_APPEND.json').unlink();f.metadata.update(version='1.1',publication_date='2026-10-17')
 p.dump(f.r/'metadata.json',f.metadata);p.dump(f.r/'deposit.json',dict(metadata=f.metadata,files=f.mappings));package=json.loads((f.r/'PACKAGE_MANIFEST.json').read_text());package['metadata']=p.pin(f.r/'metadata.json',f.r);p.dump(f.r/'PACKAGE_MANIFEST.json',package)
 f.clear.update(publication_metadata=f.metadata,publication_metadata_sha256=p.sha((f.r/'metadata.json').read_bytes()),deposit_manifest_sha256=p.sha((f.r/'deposit.json').read_bytes()),package_manifest_sha256=p.sha((f.r/'PACKAGE_MANIFEST.json').read_bytes()));p.dump(f.r/'FINAL_CLEARANCE.json',f.clear)
 f.ctx=f.rb.context(f.r);f.z.update(metadata=f.metadata,release_binding=f.rb.binding(f.ctx));p.dump(f.pub/'ZENODO_VERIFIED_PUBLICATION.json',f.z)
 f.execute('append_verified_tracker.py');f.save();t=f.rb.tracker(f.r,f.pub,f.ctx,f.z)
 assert 'v1.0,2026-10-16' in t['values'][3]
 return dict(cleared_metadata_version='1.1',cleared_publication_date='2026-10-17',accepted_tracker_literal='v1.0,2026-10-16')

def stage_intent_sync_failure():
 f=p.Fixture('stage_intent_sync_failure')
 for n in ['ZENODO_VERIFIED_PUBLICATION.json','TRACKER_VERIFIED_APPEND.json']:(f.pub/n).unlink()
 real=f.rb.sync_directory
 def sync(path):
  if path==f.pub and (f.pub/'STAGE_ATTEMPT.json').exists():raise OSError('synthetic parent fsync failure')
  return real(path)
 f.rb.sync_directory=sync;error=p.rejection(lambda:f.execute('publish_preprint.py'));f.save()
 ops=[c['operation'] for c in f.calls if c['provider']=='zenodo-kit'];assert ops==['check'] and (f.pub/'STAGE_ATTEMPT.json').exists()
 return dict(error=error,provider_operations=ops,no_stage_after_failed_intent_sync=True,intent_retained=True)

def merge_unknown():
 f=p.Fixture('merge_unknown');f.execute('integrate_reviewed_pr.py');real=f.native
 def native(method,path,payload):
  result=real(method,path,payload)
  if method=='PUT':raise TimeoutError('synthetic lost native merge outcome')
  return result
 f.native=native;first=p.rejection(lambda:f.execute('verify_and_merge.py'));before=len(f.calls);retry=p.rejection(lambda:f.execute('verify_and_merge.py'));f.save()
 assert len(f.calls)==before and not (f.pub/'PR_MERGED.json').exists() and (f.pub/'NATIVE_MERGE_REQUEST.json').exists()
 return dict(first=first,retry=retry,retry_provider_calls=0,no_premature_completion_receipt=True)

def merge_rejects_failure():
 f=p.Fixture('merge_rejects_failure');f.execute('integrate_reviewed_pr.py');real=f.native
 def native(method,path,payload):
  if method=='PUT':
   assert payload['sha']==f.pr['head']['sha'];f.calls.append(dict(provider='github',method=method,path=path,payload=payload));return {'merged':False,'message':'synthetic conflict'}
  return real(method,path,payload)
 f.native=native;error=p.rejection(lambda:f.execute('verify_and_merge.py'));f.save();assert not (f.pub/'PR_MERGED.json').exists()
 return dict(error=error,expected_SHA_in_merge_request=True,no_completion_or_counts_receipt=True)

def public_sha_failure():
 f=p.Fixture('public_sha_failure');(f.pub/'ZENODO_VERIFIED_PUBLICATION.json').unlink();p.dump(f.pub/'PUBLISH_ATTEMPT.json',dict(id=12345,release_binding=f.rb.binding(f.ctx)));real=f.urlopen
 class BadResponse:
  def __enter__(self):return self
  def __exit__(self,*args):return None
  def read(self):return b'wrong public bytes'
 f.urlopen=lambda *args,**kw:BadResponse();error=p.rejection(lambda:f.execute('verify_published_readonly.py'))
 assert not (f.pub/'ZENODO_VERIFIED_PUBLICATION.json').exists() and (f.pub/'PUBLICATION_VERIFICATION_PENDING.json').exists()
 f.urlopen=real;f.execute('verify_published_readonly.py');f.save();assert f.rb.publication(f.r,f.pub,f.ctx)
 return dict(error=error,bad_public_SHA_not_promoted=True,read_only_recovery_succeeded=True,provider_operations=[c['operation'] for c in f.calls])

def unresolved_doi():
 f=p.Fixture('unresolved_doi');(f.pub/'ZENODO_VERIFIED_PUBLICATION.json').unlink();p.dump(f.pub/'PUBLISH_ATTEMPT.json',dict(id=12345,release_binding=f.rb.binding(f.ctx)));f.z['doi_resolution']['status']='pending'
 error=p.rejection(lambda:f.execute('verify_published_readonly.py'));f.save()
 assert not (f.pub/'ZENODO_VERIFIED_PUBLICATION.json').exists() and (f.pub/'PUBLICATION_VERIFICATION_PENDING.json').exists()
 return dict(error=error,pending_receipt=True,no_verified_receipt=True)

def mutated_metadata_after_inspect():
 f=p.Fixture('mutated_metadata_after_inspect');(f.pub/'ZENODO_VERIFIED_PUBLICATION.json').unlink();p.dump(f.pub/'PUBLISH_ATTEMPT.json',dict(id=12345,release_binding=f.rb.binding(f.ctx)));real=f.run
 def call(args,**kw):
  result=real(args,**kw)
  if len(args)>3 and args[3]=='inspect':(f.r/'metadata.json').write_text('{"title":"changed during provider read"}')
  return result
 f.run=call;error=p.rejection(lambda:f.execute('verify_published_readonly.py'));f.save();assert not (f.pub/'ZENODO_VERIFIED_PUBLICATION.json').exists()
 return dict(error=error,no_verified_receipt=True)

if __name__=='__main__':
 for label,fn in [('missing_publication_lineage',missing_publication_lineage),('version_drift',version_drift),('stage_intent_sync_failure',stage_intent_sync_failure),('merge_unknown',merge_unknown),('merge_rejects_failure',merge_rejects_failure),('public_sha_failure',public_sha_failure),('unresolved_doi',unresolved_doi),('mutated_metadata_after_inspect',mutated_metadata_after_inspect)]:run(label,fn)
