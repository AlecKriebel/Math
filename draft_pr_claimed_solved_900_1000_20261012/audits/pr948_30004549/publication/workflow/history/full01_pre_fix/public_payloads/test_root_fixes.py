import sys
if not(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise RuntimeError('Use Python -I -S -B')
from datetime import datetime,timezone
started_utc=datetime.now(timezone.utc).isoformat()
from pathlib import Path
import json,copy
p=Path('draft_pr_claimed_solved_900_1000_20261012/accept_pr948.py').absolute();N={'__name__':'_in_memory_root_fixes_','__file__':str(p)}
exec(compile(p.read_bytes(),str(p),'exec',dont_inherit=True,optimize=0),N)
results=[]
def test(name,f):
 try:f();results.append({'name':name,'status':'PASS'})
 except Exception as e:results.append({'name':name,'status':'FAIL','error':str(e)});raise
def must(x):
 if not x:raise RuntimeError('condition false')
def reject(f):
 try:f()
 except (RuntimeError,ValueError,KeyError,TypeError,OSError):return
 raise RuntimeError('unsafe fixture accepted')
class Patch:
 def __init__(self,**kw):self.kw=kw
 def __enter__(self):self.old={k:N[k] for k in self.kw};N.update(self.kw)
 def __exit__(self,*args):N.update(self.old)
test('exact50IDs',lambda:must(len(N['INHERITED_FINDING_IDS'])==50))
with Patch(blob=lambda ref,name:b'{}' if name==N['STATE'] else b''):
 test('ROOT03_true_absence',lambda:must(N['native_safety']('fixture')['target_state_absent'] is True))
with Patch(blob=lambda ref,name:json.dumps({N['KEY']:None}).encode() if name==N['STATE'] else b''):
 test('ROOT03_null_rejected',lambda:reject(lambda:N['native_safety']('fixture')))
before={'number':952,'state':'OPEN','isDraft':True,'headRefOid':'a'*40,'headRefName':'new','baseRefName':'main','url':'https://github.com/AlecKriebel/Math/pull/952'}
old={'number':952,'headRefOid':'b'*40,'entries':[{'id':'111'}]};calls=[]
def service(args,**kw):
 calls.append(args)
 if any(x.startswith('number=') for x in args):
  return json.dumps({'data':{'repository':{'pullRequest':{**before,'changedFiles':2,'files':{'nodes':[{'path':'unsolved_math_prioritization/QUEUE.md'},{'path':'unsolved_math_prioritization/attempts/222/README.md'}],'pageInfo':{'hasNextPage':False,'endCursor':None}}}}}})
 q='| 1 | 111 / OLD | old | 0 | 0 | 0 | 0 | claimed_solved | 4/5 | | | |\n| 2 | 222 / NEW | new | 0 | 0 | 0 | 0 | unsolved | 5/5 | | | |\n'
 return json.dumps({'data':{'repository':{'object':{'text':q,'byteSize':len(q.encode()),'isBinary':False,'oid':'c'*40}}}})
with Patch(run=service,pr_view=lambda number:copy.deepcopy(before)):
 def changed():
  skips,selected=N['gate_next']([old]);must(selected is None and skips[0]['problem_id']=='222' and skips[0]['status']=='unsolved' and len(calls)==2)
 test('ROOT02_old_claimed_new_unsolved_changed_head_SKIPS_newID',changed)
 calls.clear()
 def unchanged():
  skips,selected=N['gate_next']([{**old,'headRefOid':before['headRefOid']}]);must(selected['problem_id']=='111' and len(calls)==1)
 test('ROOT02_unchanged_head_reuse',unchanged)
def ambiguous(args,**kw):
 return json.dumps({'data':{'repository':{'pullRequest':{**before,'changedFiles':2,'files':{'nodes':[{'path':'unsolved_math_prioritization/attempts/222/a'},{'path':'unsolved_math_prioritization/attempts/333/b'}],'pageInfo':{'hasNextPage':False,'endCursor':None}}}}}})
with Patch(run=ambiguous):test('ROOT02_ambiguous_changed_head_rejected',lambda:reject(lambda:N['next_identity'](old,before)))

W=N['W'];ROOT=N['ROOT'];P=N['P']
import io,zipfile
def raw(value):return (json.dumps(value,indent=2)+'\n').encode()
def page_service(args,**kw):
 cursor=next((x.split('=',1)[1] for x in args if x.startswith('cursor=')),None)
 paths=[{'path':'unsolved_math_prioritization/attempts/222/README.md'}] if cursor is None else [{'path':'unsolved_math_prioritization/QUEUE.md'}]
 return json.dumps({'data':{'repository':{'pullRequest':{**before,'changedFiles':2,'files':{'nodes':paths,'pageInfo':{'hasNextPage':cursor is None,'endCursor':'NEXT' if cursor is None else None}}}}}})
with Patch(run=page_service):test('ROOT02_complete_pagination_positive',lambda:must(N['next_identity'](old,before)=='222'))
def incomplete(args,**kw):
 data=json.loads(ambiguous(args));data['data']['repository']['pullRequest']['changedFiles']=3;return json.dumps(data)
with Patch(run=incomplete):test('ROOT02_incomplete_paths_rejected',lambda:reject(lambda:N['next_identity'](old,before)))
def raced(args,**kw):
 data=json.loads(ambiguous(args));data['data']['repository']['pullRequest']['headRefOid']='d'*40;return json.dumps(data)
with Patch(run=raced):test('ROOT02_page_head_race_rejected',lambda:reject(lambda:N['next_identity'](old,before)))
event={'id':N['KEY'],'event':'audited_imported_candidate_publication'}
with Patch(blob=lambda ref,name:raw({N['KEY']:event}) if name==N['STATE'] else (json.dumps(event)+'\n').encode()):
 test('ROOT03_exact_recovery_membership_not_absent',lambda:must(N['native_safety']('fake',event)['target_state_absent'] is False))
oldinvraw=(W/'history/root01_pre_fix/public_payloads/OPERATIONS_INVENTORY.json').read_bytes();oldinv=json.loads(oldinvraw)
currentinv={**oldinv,'files':{name:N['fingerprint']((ROOT/name).read_bytes()) for name in oldinv['files']}}
currentpin=N['sha'](raw(currentinv));context={'inventory_sha256':currentpin,'inventory':currentinv}
familydata={family:(N['A']/'reviews'/family/'MANIFEST.json').read_bytes() for family in N['FAMILY_PINS']}
fs={}
class VirtualPath(type(Path())):
 def iterdir(self):
  prefix=str(self).rstrip('/')+'/'
  names={key[len(prefix):].split('/')[0] for key in fs if key.startswith(prefix)}
  return iter(self/name for name in sorted(names))
F=VirtualPath(str(W/'virtual_owned_fixture'));A=F/'audit';D=F/'preprint'
def put(path,data):
 fs[str(path)]=data
 return N['fingerprint'](data)
def virtual_read(path,cap=None,pin=None):
 key=str(path)
 if key not in fs:raise FileNotFoundError(key)
 data=fs[key]
 if pin is not None:
  N['validate_pin'](pin);N['need'](N['fingerprint'](data)==pin,'virtual byte fingerprint changed')
 if cap is not None:N['need'](len(data)<=cap,'virtual cap')
 return data
names=['ORIGINAL_FILE_RECORDS.json','TARGET_IDENTITY_PREFLIGHT.json','ROOT_PRE_PACKAGE_SOURCE_CONTINUITY_06.json','source_record_private.txt','PUBLICATION_FINDINGS_REGISTER.md','ROOT_ORIGINAL_AUTHENTICATION_AND_BUDGET.json','ROOT_PROFILE_ROOT01_AUTHENTICATION.json','ROOT_PROFILE_ROOT01_REPLAY.json']
evidence={}
for name in names:
 target=A/name;evidence[target.relative_to(ROOT).as_posix()]=put(target,b'OLD register\n' if name=='PUBLICATION_FINDINGS_REGISTER.md' else b'owned fake evidence\n')
for family,data in familydata.items():
 target=A/'reviews'/family/'MANIFEST.json';evidence[target.relative_to(ROOT).as_posix()]=put(target,data)
def candidate(base,revision,inv,invpin,evidence):
 members={'profile/verify_package.py':b'# fixture profile stub\n','paper/note.pdf':b'owned fake PDF\n'}
 manifest={'schema':'pr948-sourcefree-package-v1','version':1,'problem_id':30004549,'original_head':N['HEAD'],'files':{name:{**N['fingerprint'](data),'mode':'100644'} for name,data in members.items()}}
 members['PACKAGE_MANIFEST.json']=raw(manifest)
 files={'package/'+name:put(base/'package'/name,data) for name,data in members.items()}
 files[N['PDF']]=put(base/N['PDF'],members['paper/note.pdf'])
 buf=io.BytesIO()
 with zipfile.ZipFile(buf,'w') as archive:
  for name,data in members.items():archive.writestr(name,data)
 files[N['ZIP']]=put(base/N['ZIP'],buf.getvalue())
 extras={'zenodo-deposit.json':b'{}\n','FINDING_DISPOSITIONS.json':raw({'findings':[{'id':x} for x in sorted(N['INHERITED_FINDING_IDS']-{'R948-WORKFLOW-ROOT-01','R948-WORKFLOW-ROOT-02','R948-WORKFLOW-ROOT-03'} if revision==1 else N['INHERITED_FINDING_IDS'])]}),'PR_DESCRIPTION.md':b'owned fake description\n','BUILD_RECEIPT.json':b'{}\n'}
 extras.update({'PACKAGE_REPLAY_'+label+'.json':raw({'receipt':{'fixture_revision':revision,'mode':label}}) for label in ['normal','O','OO','env2']})
 for name,data in extras.items():files[name]=put(base/name,data)
 freeze={'schema':'pr948-publication-freeze-v1','created_utc':'2026-10-16T00:0'+str(revision)+':00+00:00','revision_candidate':revision,'pr':948,'problem_id':N['KEY'],'original_pr_head':N['HEAD'],'operations_inventory_sha256':invpin,'pr_description_sha256':'1'*64,'package_manifest_sha256':N['sha'](members['PACKAGE_MANIFEST.json']),'package_pdf':'paper/note.pdf','package_verifier':'profile/verify_package.py','files':files,'evidence_files':copy.deepcopy(evidence),'future_helpers':{name:inv['files'][(P.relative_to(ROOT)/name).as_posix()] for name in N['HELPERS']},'replay_normalization_ignored':[]}
 frozen=raw(freeze);put(base/'FREEZE.json',frozen);return freeze,N['sha'](frozen)
oldbase=D/'reviewed_candidates/candidate01'
oldfreeze,oldpin=candidate(oldbase,1,oldinv,N['sha'](oldinvraw),evidence)
put(oldbase/'OPERATIONS_INVENTORY.json',oldinvraw)
for name,record in oldinv['files'].items():put(oldbase/'operations'/name,(W/'history/root01_pre_fix/operations'/name).read_bytes())
for name in evidence:put(oldbase/'evidence'/name,fs[str(ROOT/name)])
register=A/'PUBLICATION_FINDINGS_REGISTER.md';registerkey=register.relative_to(ROOT).as_posix()
put(register,b'NEW register ROOT01/02/03\n')
newevidence={name:N['fingerprint'](fs[str(ROOT/name)]) for name in evidence}
freeze,pin=candidate(D,2,currentinv,currentpin,newevidence)
profile_calls=[]
def profile(freeze,base):
 profile_calls.append(str(base))
 def inspect(data,expected):
  with zipfile.ZipFile(io.BytesIO(data)) as archive:
   must(set(archive.namelist())==set(expected))
   for name,item in expected.items():must(N['fingerprint'](archive.read(name))=={'bytes':item['bytes'],'sha256':item['sha256']})
  return expected
 return {'verify':lambda root,anchor:({'fixture_only':True},{}),'inspect_archive':inspect}
original_findings=N['inherited_findings']
with Patch(A=A,D=D,read_regular=virtual_read,frozen_profile=profile,inherited_findings=lambda freeze:original_findings(freeze,D)):
 test('ROOT01_old_snapshot_passes_after_live_register_changed',lambda:must(N['freeze_check'](fs[str(oldbase/'FREEZE.json')],oldpin,context,oldbase,historical=True)['revision_candidate']==1))
 snapshot=oldbase/'evidence'/registerkey;original=fs.pop(str(snapshot));profile_calls.clear()
 test('ROOT01_missing_snapshot_rejects_no_live_fallback',lambda:reject(lambda:N['freeze_check'](fs[str(oldbase/'FREEZE.json')],oldpin,context,oldbase,historical=True)))
 test('ROOT01_missing_snapshot_before_profile_execution',lambda:must(profile_calls==[]))
 put(snapshot,original+b'tampered')
 test('ROOT01_tampered_snapshot_rejects',lambda:reject(lambda:N['freeze_check'](fs[str(oldbase/'FREEZE.json')],oldpin,context,oldbase,historical=True)))
 put(snapshot,original)
 test('ROOT01_current_live_positive',lambda:must(N['freeze_check'](fs[str(D/'FREEZE.json')],pin,context,D)['revision_candidate']==2))
 newregister=fs[str(register)];put(register,b'DRIFT\n')
 test('ROOT01_current_live_drift_rejects',lambda:reject(lambda:N['freeze_check'](fs[str(D/'FREEZE.json')],pin,context,D)))
 put(register,newregister)
 originals={'fake-original':{'bytes':1,'sha256':'a'*64,'git_blob':'b'*40,'git_mode':'100644','disk_mode':'0644'}}
 def review(number,rf,rpin,issue=False):
  base=A/'reviews'/f'full_package_{number:02d}'
  result={'pr':948,'problem_id':N['KEY'],'original_pr_head':N['HEAD'],'reviewer_agent_id':'fresh'+str(number),'clean_context':True,'full_reproducer_completed':True,'entire_package_review':True,'started_utc':f'2026-10-16T00:{number+2:02d}:00+00:00','completed_utc':f'2026-10-16T00:{number+2:02d}:59+00:00','candidate_revision':rf['revision_candidate'],'candidate_pins':{'freeze':rpin,'manifest':rf['package_manifest_sha256'],'pdf':rf['files'][N['PDF']]['sha256']},'inspected_helper_hashes':rf['future_helpers'],'required_issues':[{'id':'R948-WORKFLOW-ROOT-01'}] if issue else [],'optional_issues':[],'clean_for_preprint':not issue,'strongest_verified_theorem':'Scoped fixture theorem.','mathematical_remaining_gap_for_stated_theorem':None,'prior_issue_resolution':{} if issue else {'R948-WORKFLOW-ROOT-01':{'verified':True,'evidence':'Verified old snapshots and live drift.'}},'inherited_finding_dispositions':{x:{'verified':True,'evidence':'Verified fixture disposition.'} for x in (N['INHERITED_FINDING_IDS']-{'R948-WORKFLOW-ROOT-01','R948-WORKFLOW-ROOT-02','R948-WORKFLOW-ROOT-03'} if rf['revision_candidate']==1 else N['INHERITED_FINDING_IDS'])}}
  auth={'status':'PASS','utc':f'2026-10-16T00:{number+2:02d}:01+00:00','original_pr_head':N['HEAD'],'freeze_sha256':rpin,'package_manifest_sha256':rf['package_manifest_sha256'],'future_helpers':rf['future_helpers'],'candidate_files':rf['files'],'originals':{'fake-original':{**originals['fake-original'],'archive_mode':'100644','disk_and_archive_match':True}}}
  cold={'status':'PASS','utc':f'2026-10-16T00:{number+2:02d}:30+00:00','cold_extraction':True,'package_manifest_sha256':rf['package_manifest_sha256'],'externally_pinned_verifier_sha256':rf['files']['package/profile/verify_package.py']['sha256'],'normalized_fields_ignored':[],'modes':[{'mode':label,'observed_outer_optimization':opt,'returncode':0,'receipt':{'fixture_revision':rf['revision_candidate'],'mode':label}} for label,opt in zip(['normal','O','OO','env2'],[0,1,2,0])]}
  values={'RESULT.json':raw(result),'AUTHENTICATION_START.json':raw(auth),'AUTHENTICATION_END.json':raw({**auth,'utc':f'2026-10-16T00:{number+2:02d}:58+00:00'}),'COLD_REPLAY.json':raw(cold),'FULL_AUDIT.md':b'Complete fixture audit.\n','RESEARCH_LOG.md':b'Preserved old adverse review and new clean rounds.\n'}
  records={name:put(base/name,data) for name,data in values.items()};data=raw({'files':records,'explicit_public_allowlist':list(records)});put(base/'MANIFEST.json',data);return f'{number:02d}:'+N['sha'](data)
 specs=[review(1,oldfreeze,oldpin,issue=True),review(2,freeze,pin)]
 with Patch(original_check=lambda:originals):
  test('ROOT01_whole_fix_loop_old_adverse_one_new_clean_insufficient',lambda:reject(lambda:N['review_check'](specs,freeze,pin,context)))
  specs.append(review(3,freeze,pin))
  test('ROOT01_whole_fix_loop_old_adverse_two_new_current_clean_pass',lambda:must(len(N['review_check'](specs,freeze,pin,context)[0])==3))
receipt={'schema':'pr948-workflow-root-fixes-tests-v1','status':'PASS','passed':len(results),'failed':0,'tests':results,'in_memory_filesystem_fixture':True,'historical_gate_and_review_gate_actual_functions':True,'tiny_package_profile_stub_explicit':True,'genuine_byte_hash_pins':True,'external_mutations':0,'receipt_not_saved_due_ENOSPC':False}
receipt.update(started_utc=started_utc,completed_utc=datetime.now(timezone.utc).isoformat(),saved_after_storage_recovery=True)
(W/'ROOT_FIXES_RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'passed':receipt['passed'],'failed':receipt['failed'],'receipt':str(W/'ROOT_FIXES_RESULT.json')}))
