"""Complete read-only reconciliation after a definitive exact push and delayed GH readback.
Never repeat any merge, stage, commit, push, PR edit, or other remote mutation.
"""
import datetime, gzip, hashlib, importlib.util, json, os, stat, sys
from pathlib import Path
from capture import capture, reserve_remaining
if sys.flags.optimize:raise RuntimeError('Optimization disables checks')
R=Path('/Users/alec/Documents/Math'); A=R/'draft_pr_publication_program_20260930/audits/pr80_30000177'; F=Path(__file__).parent
PLAN=A/'ROOT_NATIVE_PLAN_WORKSPACE_REPAIR_V2_FINAL_20261005.json'
ACK=R/'draft_pr_descending_audit_20261002/audits/pr305_5100034/root_during_peer_pause_20261005/ROOT_EXCLUSIVE_PR80_PUBLICATION_INTEGRATION_ACK.json'
STATUS=R/'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'
WINDOW=A/'ROOT_ACTUAL_NATIVE_WINDOW_GATE_20261004.json'; E=F/'process_evidence'
BASE='83fe73d348b24881989569e5e50d7b19a9458004'; COMMIT='3804c6bbc5890529da417e9d9202b2be1c15330f'; HEAD='dcfeb5d8ad68b397ec509c70e85c6fca46cd01e3'
TOKEN='9c9c35b7-756d-4983-aab5-dec348577203'; RECEIPT=A/'ROOT_NATIVE_MERGE_RECEIPT_20261004.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def pin(p):
 assert p.is_file() and not p.is_symlink() and p.resolve()==p and p.is_relative_to(R)
 b=p.read_bytes();return {'path':str(p.relative_to(R)),'bytes':len(b),'sha256':sha(b),'mode':stat.S_IMODE(p.stat().st_mode)}
def names(b):return {x.decode() for x in b.split(b'\0') if x}
def evidence(label):
 d=E/label;x=load(d/'result.json');start=load(d/'process_started.json');end=load(d/'process_completed.json')
 assert x['actual_PID']==start['actual_PID']==end['actual_PID'] and x['exit_code']==end['exit_code']
 assert x['start_UTC']==start['start_UTC']==end['start_UTC'] and x['end_UTC']==end['end_UTC']
 streams={}
 for k in ('stdout','stderr'):
  q=Path(x[k+'_path']);assert q.parent==d and q.name==k+'.bin.gz';b=q.read_bytes();st=x[k+'_storage'];logical=gzip.decompress(b)
  assert st['storage_codec']=='gzip' and len(b)==st['storage_bytes'] and sha(b)==st['storage_sha256']
  assert len(logical)==x[k+'_bytes']==st['logical_bytes']==end[k+'_bytes'] and sha(logical)==x[k+'_sha256']==st['logical_sha256']==end[k+'_sha256'];streams[k]=logical
 for item in x['retained_sources_prelaunch']:
  q=Path(item['retained_path']);assert q.parent==d;b=q.read_bytes();logical=gzip.decompress(b)
  assert len(b)==item['storage_bytes'] and sha(b)==item['storage_sha256'] and len(logical)==item['bytes']==item['logical_bytes'] and sha(logical)==item['sha256']==item['logical_sha256']
 return x,streams,pin(d/'result.json')
assert not RECEIPT.exists()
assert reserve_remaining()>=200*1024*1024
plan=load(PLAN);ack=load(ACK);window=load(WINDOW);pp,ap,sp,wp=map(pin,(PLAN,ACK,STATUS,WINDOW))
assert pp['sha256']=='054843655c4a57844f49d1312a096f8bc000e8e93240f426aa6c7f677b2f9014' and ap['sha256']=='52ec5feb319771932f05569e28a3f1c8ba4b1e040e6b58ed0e8a2461e739c81a'
assert plan['ROOT_reviewed_for_execution'] is True and ack['writer_window_granted'] is True and ack['stable_Git_configuration_held'] is True
assert ack['ROOT_plan_sha256']==pp['sha256'] and ack['token']==TOKEN and ack['covers_phases']==['merge','accept','checkpoint'] and ack['exact_owned_paths']==plan['exact_owned_paths']
assert ack['starting_main']==BASE and ack['head']==plan['head']==HEAD and ack['PR']==plan['PR']==80
hp=plan['held_foreign_manifest'];assert pin(R/hp['path'])==hp and ack['held_foreign_manifest_sha256']==hp['sha256']
held=load(R/hp['path']);own=set(plan['exact_owned_paths'])
assert held['cooperative_control']==sp and not own.intersection({x['path'] for x in held['files']})
assert window['ROOT_authorizes_exact_plan'] is True and window['ROOT_verified_known_held_scope'] is True and window['plan_sha256']==pp['sha256'] and window['ACK']==ap and window['held_foreign_manifest']==hp
original,streams,failedpin=evidence('ROOT_actual_native_merge')
assert original['actual_PID']==11452 and original['exit_code']==1 and not streams['stdout'] and b'GitHub merged-head readback failed' in streams['stderr']
assert sha(streams['stderr'])=='7d7a4403570df21ff961fdce11e9c6b39518879657dc9f3c6e880581d2832d66'
old={}; evidencepins=[]
for n in range(1,182):
 x,streams,xpin=evidence('native_merge_'+str(n));assert x['exit_code']==0;old[n]=(x,streams);evidencepins.append(xpin)
assert not (E/'native_merge_182').exists()
assert old[178][0]['actual_PID']==12002 and old[178][0]['argv']==['git','--no-optional-locks','push','--force-with-lease=refs/heads/main:'+BASE,'https://github.com/AlecKriebel/Math.git',COMMIT+':refs/heads/main']
assert old[179][1]['stdout'].split()[0].decode()==old[180][1]['stdout'].split()[0].decode()==COMMIT
oldpr=json.loads(old[181][1]['stdout']);assert oldpr['state']=='OPEN' and oldpr['mergeCommit'] is None and oldpr['headRefOid']==HEAD
assert old[73][0]['argv']==['git','--no-optional-locks','merge','--no-ff','--no-commit',HEAD]
number=0;newrecords=[]
def run(argv):
 global number
 number+=1;rec,out,err=capture('merge_reconciliation_'+str(number),argv,sources=[str(Path(__file__).resolve()),str(PLAN),str(ACK)])
 assert rec['exit_code']==0;newrecords.append(rec);return out
def git(*args):return run(['git','--no-optional-locks',*args])
def controls():
 assert pin(PLAN)==pp and pin(ACK)==ap and pin(STATUS)==sp and pin(WINDOW)==wp and pin(R/hp['path'])==hp
 s=load(STATUS);assert s['shared_git_writes_paused'] is True and s['ascending_pr80_publication_integration_lease_token']==TOKEN
 for entry in plan['bound_inputs']+held['files']:assert pin(R/entry['path'])==entry
controls()
assert git('branch','--show-current').strip()==b'main' and git('rev-parse','HEAD').decode().strip()==COMMIT
endpoints=json.loads(run(['/opt/homebrew/bin/python3','-E','-B',str(F/'get_approved_git_endpoint.py')]))
assert endpoints['URL_rewrite_rules_absent'] is True and endpoints['credential_free_expected_repository'] is True and endpoints['endpoint']==plan['approved_git_endpoints']['push'] and endpoints['fetch_endpoint']==plan['approved_git_endpoints']['fetch']
assert git('ls-remote',endpoints['endpoint'],'refs/heads/main').split()[0].decode()==COMMIT
assert git('ls-remote','origin','refs/heads/main').split()[0].decode()==COMMIT
assert git('diff','--cached','--name-only','-z')==b'' and not (R/'.git/MERGE_HEAD').exists()
assert git('show','-s','--format=%P',COMMIT).decode().split()==[BASE,HEAD]
spec=importlib.util.spec_from_file_location('preserved_native',F/'native_integrate.py');native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
originals=[x for x in load(A/'original_source_authentication_20261004/ORIGINAL_BLOB_MANIFEST.json')['files'] if x['path'].startswith(native.PREFIX+'/')]
assert len(originals)==19;targets={x['path'] for x in originals}|{native.QUEUE}
assert names(git('diff','--name-only','-z',BASE,COMMIT))==targets
before=git('show',BASE+':'+native.QUEUE);oldrow=native.row(before);newrow=plan['queue_after_row'].encode();expected=before.replace(oldrow,newrow,1)
assert git('show',COMMIT+':'+native.QUEUE)==(R/native.QUEUE).read_bytes()==expected
assert native.row(expected)==newrow and expected.replace(newrow,b'',1)==before.replace(oldrow,b'',1)
for entry in originals:
 b=git('show',COMMIT+':'+entry['path']);assert len(b)==entry['bytes'] and sha(b)==entry['sha256'] and native.blob(b)==entry['git_blob_sha1']
 assert git('ls-tree',COMMIT,'--',entry['path']).decode().split()[:3]==[entry['mode'],'blob',entry['git_blob_sha1']]
 assert (R/entry['path']).read_bytes()==b and stat.S_IMODE((R/entry['path']).stat().st_mode)==0o644
pr=json.loads(run(['/opt/homebrew/bin/gh','pr','view','80','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,baseRefName,mergeCommit,mergedAt,title,body']))
assert pr['number']==80 and pr['state']=='MERGED' and pr['baseRefName']=='main' and pr['headRefOid']==HEAD and pr['mergeCommit']['oid']==COMMIT and pr['mergedAt']
assert pr['title']==plan['current_title'] and pr['body'].encode()==(A/'native_preparation_20261004/PR_BODY.md').read_bytes()
identity=native.sourcepair()
assert load(A/'ROOT_FINAL_PACKAGE_GATE_20261004.json')['publication_clearance'] is True
pub=load(A/'ROOT_PUBLICATION_VERIFICATION_20261004.json');track=load(A/'ROOT_TRACKER_VERIFICATION_20261004.json')
assert pub['all8_public_bytes_identical'] is True and pub['intended_metadata_exact'] is True and pub['DOI']==track['DOI']==plan['DOI'] and track['fresh_full_table_exactly_one_pair'] is True
dirty=names(git('diff','--name-only','-z','HEAD'));assert dirty==set(held['ordinary_foreign_dirty_paths']) and not dirty.intersection(own)
assert git('diff','--binary','HEAD','--',*sorted(dirty))==old[8][1]['stdout']
index,flags=git('ls-files','--stage','-z'),git('ls-files','-v','-z')
def exclude(b):return b'\0'.join(x for x in b.split(b'\0') if x and (x.split(b'\t',1)[-1].decode() if b'\t' in x else x[2:].decode()) not in own)
assert exclude(index)==exclude(old[9][1]['stdout']) and exclude(flags)==exclude(old[10][1]['stdout'])
hidden={x.decode()[2:] for x in flags.split(b'\0') if x and (chr(x[0]).islower() or chr(x[0]).upper()=='S')}-own
assert hidden==set(held['hidden_flagged_foreign_paths'])
controls()
result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'COMMITTED_PUSHED_INDEPENDENTLY_READ_BACK','phase':'merge','commit':COMMIT,'parent':BASE,'second_parent':HEAD,'merge_exit':old[73][0]['exit_code'],'merged_at':pr['mergedAt'],'19_original_bodies_modes_blobs_preserved':True,'original_head':HEAD,'lease_token':TOKEN,'actual_PID':os.getpid(),'index_empty':True,'ordinary_foreign_dirty_bodies_modes_diffs_and_entire_foreign_index_preserved':True,'known_held_foreign_manifest_preserved':hp,'known_held_foreign_file_count':len(held['files']),'foreign_assurance_scope':'Exactly coordinator-declared held set plus all ordinary dirty/hidden-index-flag paths; not every ignored or historical unheld file','original_budget':'1/5','new_central_proof_search_turns':0,'reconciliation':{'failed_original_child_PID':11452,'failed_outer_result':failedpin,'failure':'Immediate GitHub readback OPEN after successful exact push; later fresh read-only GitHub reports exact merged commit','original_failed_evidence_preserved':True,'original_completed_inner_children':181,'original_push_PID':12002,'read_only_completion_child_count':len(newrecords),'no_merge_push_commit_stage_or_PR_mutation_repeated':True,'reconciliation_source':pin(Path(__file__).resolve()),'original_child_result_pins':evidencepins}}
with RECEIPT.open('x') as stream:stream.write(json.dumps(result,indent=2)+'\n');stream.flush();os.fsync(stream.fileno())
assert load(RECEIPT)==result
print(json.dumps(result,indent=2))
