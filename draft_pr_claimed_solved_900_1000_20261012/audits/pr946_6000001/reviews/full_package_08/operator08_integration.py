"""Actual operator/core/kit integration; private fixture and all Git/API/token fakes.

Requires current08_controls.py to have prepared all seven actual earlier seals
and one explicitly synthetic eighth terminal contract review. No production
acceptance or external mutation is possible in this harness.
"""
import sys
if not sys.flags.isolated or not sys.flags.no_site or sys.flags.optimize or not sys.dont_write_bytecode:raise RuntimeError('Use -I -S -B')
import argparse,builtins,contextlib,copy,datetime,hashlib,io,json,pathlib,types,subprocess
R=pathlib.Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';W=A/'reviews/full_package_08';root=W/'private/current08_context';p=root/P.name;a=p/'audits/pr946_6000001';d=a/'preprint';w=a/'reviews/full_package_08'
def need(x,m):
 if not x:raise RuntimeError(m)
def fp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(x):return (json.dumps(x,indent=2)+'\n').encode()
source=(A/'publication_operator.py').read_bytes();op_pin=fp(source);need(op_pin=={'bytes': 9912, 'sha256': 'd085ec080ee6c2f1239f49f724e7a71ef6d86b3d994fbe9b4039371181a61aef'},'operator external pin')
kitraw=(R/'zenodo_deposit_tool/zenodo.py').read_bytes();need(fp(kitraw)['sha256']=='a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca','kit external pin')
core_raw=(P/'accept_pr946.py').read_bytes();need(fp(core_raw)['sha256']=='8e1a0d7b3ca6e5d72e76415541b393fbfbe52e307368bc86b9e7982d5be27cd7','core external pin')
operator_path=a/'publication_operator.py';operator_path.write_bytes(source)
result=json.loads((w/'RESULT.json').read_bytes());result['inspected_publication_operator']=op_pin;result['prior_issue_resolution']['PUB946-METADATA-001']={'verified':True,'resolution':'SYNTHETIC test approval only.'};(w/'RESULT.json').write_bytes(enc(result))
manifest=json.loads((w/'MANIFEST.json').read_bytes());manifest['files']['RESULT.json']=fp((w/'RESULT.json').read_bytes());(w/'MANIFEST.json').write_bytes(enc(manifest));seal=fp((w/'MANIFEST.json').read_bytes())['sha256']
accepted=json.loads((a/'ACCEPTANCE.json').read_bytes());accepted['full_package_reviews'][-1]['manifest_sha256']=seal;(a/'ACCEPTANCE.json').write_bytes(enc(accepted));accepted_raw=(a/'ACCEPTANCE.json').read_bytes()
originals=json.loads((W/'AUTHENTICATION_START.json').read_bytes())['originals'];queue=subprocess.check_output(['git','show','7d3adb0e500b0414a49a449e7981d34ade329427:unsolved_math_prioritization/QUEUE.md'],cwd=R)
catalog=json.dumps([x for x in json.loads((R/'unsolved_math_prioritization/catalog.json').read_bytes()) if str(x.get('id'))=='6000001']).encode();hold=False;C='918948421d00b1184a88ca07017134726b466adb';parent='a'*40
pr=json.loads((A/'PR_MERGE_RECEIPT.json').read_bytes());need(pr['state']=='MERGED','actual saved merge');(a/'PR_MERGE_RECEIPT.json').write_bytes(enc(pr))
calls=[];cases=[];namespaces=[];live_api=None
def blob(ref,name):
 if name in originals:return(a/'original'/name).read_bytes()
 if name.endswith('QUEUE.md'):return queue
 if name.endswith('catalog.json'):
  x=json.loads(catalog)
  if hold:x[0]['holds']=['SYNTHETIC newly imposed hold']
  return enc(x)
 if name.endswith('related_target_groups.json'):return b'{"groups":[]}'
 raise RuntimeError('Unexpected fake Git blob '+repr((ref,name)))
def git_run(argv,**kw):
 if argv[:2]==['git','ls-tree']:return '100644 blob '+originals[argv[-1]]['git_blob']+'\t'+argv[-1]+'\n'
 if argv[:2]==['git','fetch']:return ''
 if argv[:2]==['git','merge-base']:return ''
 if argv[:3]==['git','show','-s']:return parent+' '+pr['headRefOid']+'\n'
 raise RuntimeError('Unexpected fake transport '+repr(argv))
def forbidden(*args,**kw):raise RuntimeError('FORBIDDEN nonfake external dispatch')
class API:
 def __init__(self,mutate=None,lost=False,published=False):self.value=None;self.calls=[];self.mutate=mutate;self.lost=lost;self.published=published;self.gets=0
 def get(self,ident):
  need(type(ident) is int and ident==23409904,'fake exact ID');self.gets+=1;self.calls.append('GET')
  if self.mutate:self.mutate(self.gets)
  return copy.deepcopy(self.value)
 def publish(self,ident):
  need(ident==23409904,'fake publish ID');self.calls.append('POST');self.value['submitted']=True;self.value['doi']='10.5281/zenodo.23409904'
  if self.lost:raise namespaces[-1]['DepositError']('SYNTHETIC lost response')
  return copy.deepcopy(self.value)
def intercepted_exec(code,ns,*args,**kw):
 builtins.exec(code,ns,*args,**kw)
 if ns.get('__name__')=='_reviewed_reconciliation_core_':
  # Actual core guards remain unchanged. Only fake Git/PR transport installed.
  ns.update(blob=blob,run=git_run,remote_main=lambda:parent,pr_view=lambda:copy.deepcopy(pr),subprocess=types.SimpleNamespace(run=forbidden));namespaces.append(ns)
 elif ns.get('__name__')=='_captured_original_zenodo_kit_':
  # Actual unchanged kit functions execute, fake service/token/DOI boundaries.
  ns['STATE_DIR']=a/'fake_kit_state';ns['ZenodoClient']=lambda *x:live_api;ns['token_for']=lambda *x:'SYNTHETIC-NOT-A-SECRET';ns['doi_status']=lambda doi:{'status':'synthetic_resolved','doi':doi}
  metadata,files=ns['load_manifest'](a/'operations_runtime/zenodo-deposit.json')
  live_api.value={'id':23409904,'submitted':live_api.published,'metadata':copy.deepcopy(metadata),'files':[{'filename':f['name'],'filesize':f['size'],'checksum':f['md5']} for f in files]}
  live_api.value['metadata']['notes']=metadata['notes'].replace('Python>=3.11','Python&gt;=3.11')
  if live_api.published:live_api.value['doi']='10.5281/zenodo.23409904'
  runtime=(a/'operations_runtime/zenodo-deposit.json').resolve();ns['save_state'](ns['state_path'](runtime,'production'),{'manifest':str(runtime),'environment':'production','id':23409904});namespaces.append(ns)
def module():
 ns={'__name__':'_independent_operator08_','__file__':str(operator_path)};builtins.exec(compile(source,str(operator_path),'exec',dont_inherit=True,optimize=0),ns);ns.update(ROOT=root,P=p,A=a,D=d,exec=intercepted_exec);return ns
def clean():
 global hold
 hold=False;(a/'ACCEPTANCE.json').write_bytes(accepted_raw);operator_path.write_bytes(source)
 for q in d.glob('ZENODO_*.json'):q.unlink()
 for q in a.glob('PUBLICATION_RECONCILIATION_*.json'):q.unlink()
def action(label,mode,api,want_error=False):
 global live_api
 live_api=api;ns=module();error=None
 try:
  with contextlib.redirect_stdout(io.StringIO()):ns['run'](argparse.Namespace(action=mode,operator_sha256=op_pin['sha256'],review_sha256=seal))
 except Exception as e:error=type(e).__name__+': '+str(e)
 need((error is not None)==want_error,(label,error));need(error is None or 'FORBIDDEN' not in error and 'Unexpected fake' not in error,(label,error))
 rec={'case':label,'action':mode,'error':error,'API_calls':api.calls[:],'POST_count':api.calls.count('POST')};cases.append(rec);return rec
clean();action('positive_reconciled_existing_stage','inspect-stage',API());stage_raw=(d/'ZENODO_STAGE.json').read_bytes()
action('positive_publication','publish',API());action('positive_public_DOI_inspect','inspect',API(published=True))
N=next(x for x in reversed(namespaces) if x.get('__name__')=='_reviewed_reconciliation_core_');ctx=N['capture_inventory'](N['load'](a/'OPERATIONS_INVENTORY.json') and 'f4742eca6ddd628ecac1e704fed772a17837d42d4d0fdef42c73d3cda3bed254');acc,f=N['accepted_package'](ctx);N['publication_links'](acc,f);cases.append({'case':'actual_core_publication_links_accept_reconciled_stage_publish_inspect','pass':True})
clean();(d/'ZENODO_STAGE.json').write_bytes(stage_raw);action('positive_lost_POST_response_recovers_without_second_POST','publish',API(lost=True))
action('prior_publish_intent_blocks_blind_repeat','publish',API(),True);need(cases[-1]['POST_count']==0,'blind retry')
# A GET between the final guard and the POST revokes the real fixture approval.
for kind in ['acceptance','source_hold']:
 clean();(d/'ZENODO_STAGE.json').write_bytes(stage_raw)
 def mutate(n):
  global hold
  if n==2:
   if kind=='acceptance':x=json.loads(accepted_raw);x['accepted']=False;(a/'ACCEPTANCE.json').write_bytes(enc(x))
   else:hold=True
 rec=action('REPAIRED_final_GET_'+kind+'_before_POST','publish',API(mutate=mutate),True);need(rec['POST_count']==0,'repaired final GET allowed POST')
 rec['resolved_finding']='FP07-OPS-001';rec['approval_or_source_invalid_before_POST']=True;rec['publication_blocked_before_POST']=True
# Alter operator during the first external read, before its final publication guard.
clean();(d/'ZENODO_STAGE.json').write_bytes(stage_raw)
def drift(n):
 if n==1:operator_path.write_bytes(source+b'\n# SYNTHETIC changed canonical operator\n')
rec=action('REPAIRED_operator_drift_during_first_GET_is_blocked','publish',API(mutate=drift),True);need(rec['POST_count']==0,'operator drift allowed POST');rec['resolved_finding']='FP07-OPS-002';rec['canonical_operator_drifted']=True
clean();(d/'ZENODO_STAGE.json').write_bytes(stage_raw)
def initial_revoke(n):
 if n==1:x=json.loads(accepted_raw);x['accepted']=False;(a/'ACCEPTANCE.json').write_bytes(enc(x))
rec=action('control_approval_revoked_in_first_GET_is_blocked_by_actual_core_guard','publish',API(mutate=initial_revoke),True);need(rec['POST_count']==0,'first GET baseline guard')
clean()
# Actual entry contract check: repaired entry rejects absence of -S on actual import.
probe='import sys,pathlib; p=pathlib.Path(sys.argv[1]); n={"__name__":"_startup_probe_","__file__":str(p)}; print(sys.flags.no_site,flush=True); exec(compile(p.read_bytes(),str(p),"exec",optimize=0),n)'
proc=subprocess.run([sys.executable,'-I','-B','-c',probe,str(operator_path)],capture_output=True,text=True);need(proc.returncode!=0 and proc.stdout.strip()=='0' and 'Use Python -I -S -B' in proc.stderr,'missing-S entry was not rejected');cases.append({'case':'REPAIRED_actual_operator_import_rejects_no_site_zero','resolved_finding':'FP07-OPS-003','returncode':proc.returncode,'actual_no_site':0,'actual_isolated':1,'actual_dont_write_bytecode':1})

# Additional actual final-GET boundaries, including same-size executable drift.
fixture_manifest=w/'MANIFEST.json';fixture_result=w/'RESULT.json'
saved={q:q.read_bytes() for q in [a/'ACCEPTANCE.json',d/'FREEZE.json',d/'research_note.tex',
    w/'FULL_AUDIT.md',fixture_manifest,p/'accept_pr946.py',a/'OPERATIONS_INVENTORY.json',
    root/next(iter(json.loads((d/'FREEZE.json').read_bytes())['evidence_files']))]}
extra_review=a/'reviews/full_package_09'
def restore_extra():
    global hold
    import shutil
    if extra_review.exists():shutil.rmtree(extra_review)
    for q,b in saved.items():q.write_bytes(b)
    clean()
for kind in ['pending','adverse','theorem','tex','freeze','payload','seal','core','inventory','evidence','operator_same_size']:
    restore_extra();(d/'ZENODO_STAGE.json').write_bytes(stage_raw)
    def invalidate(n):
        if n!=2:return
        if kind in ['pending','adverse']:
            extra_review.mkdir()
            if kind=='adverse':(extra_review/'RESULT.json').write_bytes(enc({'required_issues':[{'id':'SYNTHETIC'}]}))
        elif kind=='theorem':
            x=json.loads(accepted_raw);x['exact_claim']='SYNTHETIC revoked theorem';(a/'ACCEPTANCE.json').write_bytes(enc(x))
        elif kind=='operator_same_size':operator_path.write_bytes(source.replace(b'Resume only',b'resume only',1))
        else:
            q={'tex':d/'research_note.tex','freeze':d/'FREEZE.json','payload':w/'FULL_AUDIT.md',
               'seal':fixture_manifest,'core':p/'accept_pr946.py','inventory':a/'OPERATIONS_INVENTORY.json',
               'evidence':root/next(iter(json.loads(saved[d/'FREEZE.json'])['evidence_files']))}[kind]
            q.write_bytes(saved[q]+b'\n')
    rec=action('final_GET_blocks_'+kind,'publish',API(mutate=invalidate),True)
    need(rec['POST_count']==0,'Final GET invalidation allowed POST: '+kind)
    need(not(d/'ZENODO_PUBLISH.json').exists(),'Invalid publication receipt written')
restore_extra()
for mode in ['inspect-stage','inspect']:
    clean()
    def operator_changed(n):
        if n==1:operator_path.write_bytes(source+b'\n# SYNTHETIC changed canonical operator\n')
    rec=action('receipt_closure_blocks_operator_drift_'+mode,mode,API(mutate=operator_changed,published=mode=='inspect'),True)
    need(rec['POST_count']==0,'Read-only path published')
    need(not(d/('ZENODO_STAGE.json' if mode=='inspect-stage' else 'ZENODO_INSPECT.json')).exists(),'Invalid read-only receipt written')
clean()

out={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate_revision':6,'actual_prior_rounds':7,'terminal08_explicitly_synthetic':True,'operator':op_pin,'core_sha256':fp(core_raw)['sha256'],'kit_sha256':fp(kitraw)['sha256'],'guards_unmodified':['capture_inventory','freeze_check','archive_check','original_check','review_check','accepted_package','accepted_review_check','merged_gate','source_gate','publication_links','descriptor_check','runtime_upload_copy','kit.verify','kit.run'],'fake_only':['private fixture paths','Git/PR transport','Zenodo API/token/DOI factories'],'cases':cases,'case_count':len(cases),'actual_external_mutations':0}
(W/'OPERATOR08_INTEGRATION.json').write_bytes(enc(out));print(json.dumps({'status':out['status'],'cases':len(cases),'resolved_findings':['FP07-OPS-001','FP07-OPS-002','FP07-OPS-003'],'actual_external_mutations':0}))
