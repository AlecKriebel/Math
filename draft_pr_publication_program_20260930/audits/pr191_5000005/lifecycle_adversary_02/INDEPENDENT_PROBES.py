"""Independent offline probes. No network, Git processes, production helper import or shared writes.
Author SELFTEST was neither read nor executed when this harness was derived.
"""
from pathlib import Path
import copy, datetime, hashlib, importlib.util, json, os, shutil, sys, types
sys.dont_write_bytecode=True
O=Path(__file__).resolve().parent
A=O.parent
S=A/'lifecycle_controls_preparation_02'
spec=importlib.util.spec_from_file_location('independent_runtime_02',S/'lifecycle_common.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
real_read=m.read
ready=json.loads((A/'ROOT_PUBLICATION_GATE_DRAFT_01.json').read_text())
ready['status']='READY_FOR_AUTHORIZED_PUBLICATION'
ready['all_required_findings_globally_resolved']=True
results=[]
def result(name, expected, observed, detail=None):
 results.append(dict(name=name,expected=expected,observed=observed,passed=expected==observed,detail=detail))
def rejection(name,f):
 try:f()
 except Exception as e:result(name,'reject','reject',str(e));return
 result(name,'reject','accept')
def acceptance(name,f):
 try:r=f();result(name,'accept','accept');return r
 except Exception as e:result(name,'accept','reject',str(e))
def encode(x):return json.dumps(x,indent=2)+'\n'
def put(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(x if isinstance(x,str) else encode(x))
def fixture(name):
 p=O/'fixtures'/name
 if p.exists():raise RuntimeError('Independent probe fixtures are single-use')
 p.mkdir(parents=True);return p
# Actual frozen data gate compatibility, using a ready clone only in memory.
m.A=A
current_gate=copy.deepcopy(ready)
def bound_read(p):
 if Path(p)==A/'ROOT_PUBLICATION_GATE.json':return copy.deepcopy(current_gate)
 return real_read(p)
m.read=bound_read
acceptance('actual_436_pin_gate_ready_clone',m.gate)
current_gate=copy.deepcopy(ready);current_gate['whole_package_reviews'][1]['reviewer_id']=current_gate['whole_package_reviews'][0]['reviewer_id']
rejection('duplicate_review_identity',m.gate)
current_gate=copy.deepcopy(ready);current_gate['payloads'][current_gate['paper_files']['source']]['sha256']='0'*64
rejection('changed_exact_source_payload',m.gate)
current_gate=copy.deepcopy(ready);current_gate['status']='DRAFT_SCIENCE_READY_OPERATIONAL_REPAIRS_AND_FRESH_AUDIT_PENDING_NOT_AUTHORITY'
rejection('real_draft_cannot_authorize',m.gate)
# Receipt attacks: only shared read-only inputs used; all forged receipts remain inside this audit.
m.read=real_read
F=fixture('receipt_forgery');m.A=F;put(F/'ROOT_PUBLICATION_GATE.json',ready);m.gate=lambda:copy.deepcopy(ready)
gatehash=m.pin(F/'ROOT_PUBLICATION_GATE.json')['sha256']
z={'state':'published','environment':'production','id':9919191,'doi':'10.5281/zenodo.9919191','doi_url':'https://doi.org/10.5281/zenodo.9919191','gate_sha256':gatehash,'files':[{'name':ready['paper_files'][k],'size':ready['payloads'][ready['paper_files'][k]]['bytes'],'sha256':ready['payloads'][ready['paper_files'][k]]['sha256']} for k in ['pdf','source','support']]}
put(F/'ZENODO_PUBLICATION_READBACK.json',z)
tr={'status':'TRACKER_APPEND_AND_TWO_FRESH_READS_ACCEPTED','DOI':z['doi'],'spreadsheet_id':m.SID,'gid':m.GID,'tab':m.TAB,'actual_fresh_reads':2,'gate_sha256':gatehash,'range':"'Math Puzzles'!A999:D999",'row':['deliberately false own row']}
put(F/'TRACKER_ACCEPTANCE.json',tr)
rejection('forged_publication_without_actual_inspection',lambda:m.publication(ready))
rejection('forged_tracker_false_row_and_no_readbacks',m.published_tracked)
# Exact real native template factual generation, then malicious mutation in a fact-file scientific field.
F=fixture('native');m.A=F;put(F/'ROOT_PUBLICATION_GATE.json',ready)
manifest=real_read(A/ready['native_pending_manifest']['path']);put(F/ready['native_pending_manifest']['path'],manifest)
put(F/'ORIGINAL_FILE_MANIFEST.json',real_read(A/'ORIGINAL_FILE_MANIFEST.json'))
T=F/'integration_preparation'/ready['native_final_template'];shutil.copytree(A/'integration_preparation'/ready['native_pending_template'],T)
for p in T.rglob('*'):
 if p.is_file():p.chmod(0o644)
m.published_tracked=lambda:(copy.deepcopy(ready),copy.deepcopy(z),copy.deepcopy(tr))
changed=m.native_status(T,ready,z,tr,False)
unchanged=[n for n in manifest['files'] if n not in changed]
result('real_native_nonscope_and_original16_exact','preserve','preserve' if all(m.pin(T/n)['sha256']==manifest['files'][n]['sha256'] for n in unchanged) else 'changed',{'protected_files':len(unchanged),'changed_factual_paths':len(changed)})
cur={'current_template':ready['native_final_template'],'files':{n:m.pin(T/n) for n in manifest['files']},'actual_original_PR_merged':False}
put(F/'integration_preparation/CURRENT_TEMPLATE.json',cur)
acceptance('real_native_phase95_compatible',lambda:m.current_native(ready,False))
f=real_read(T/'CURRENT_RESULT.json');f['novelty_clearance']=True;f['historical_priority_clearance']=True;f['positive_result']='All imported conjunctions solved; priority certified';put(T/'CURRENT_RESULT.json',f)
cur['files']['CURRENT_RESULT.json']=m.pin(T/'CURRENT_RESULT.json');put(F/'integration_preparation/CURRENT_TEMPLATE.json',cur)
rejection('native_scientific_claim_mutation_inside_factual_json',lambda:m.current_native(ready,False))
# Actual phase95->100 generated prose and retained qualifiers in an untouched new template.
T2=F/'integration_preparation'/ready['native_complete_template'];shutil.copytree(A/'integration_preparation'/ready['native_pending_template'],T2)
for p in T2.rglob('*'):
 if p.is_file():p.chmod(0o644)
m.native_status(T2,ready,z,tr,False);m.native_status(T2,ready,z,tr,True)
result('real_native_phase100_prose_and_qualifiers','correct','correct' if all('was actually accepted; final factual MAIN acceptance follows separately.' in (T2/n).read_text() and 'no theorem, type repair, full-group formulation or descent advertised as new' in (T2/n).read_text() for n in ready['native_text_status_replacements']) else 'stale')
# Cursor truth before factual acceptance.
put(F/'INTAKE_CHECKPOINT_ACCEPTANCE.json',{'PR':191,'original_head':m.HEAD,'checkpoint_commit':'1'*40})
j={'current_PR':191,'fully_completed_count':39,'published_count':23,'last_completed_PR':190,'dated_eligible_total':99}
r=m.normalize(j,95)
result('phase95_next_numeric_cursor_not_advanced_before_acceptance','not_192','192' if r['next_numeric_intake_cursor']==192 else 'not_192')
# Independent tracker protocol model: synthetic foreign cells never written as fixtures/results.
F=fixture('tracker');m.A=F;put(F/'ROOT_PUBLICATION_GATE.json',ready)
proposal=real_read(A/ready['tracker_row_proposal']['path']);put(F/ready['tracker_row_proposal']['path'],proposal)
# Match fixture proposal pin because the reviewed JSON is copied byte-exact.
(F/ready['tracker_row_proposal']['path']).write_bytes((A/ready['tracker_row_proposal']['path']).read_bytes())
m.gate=lambda:copy.deepcopy(ready);m.publication=lambda g=None:copy.deepcopy(z)
row=[proposal['original_problem'],proposal.get('solution_chat_url',''),z['doi_url'],proposal['notes']]
class Sheet:
 def __init__(self,attack=None,lost=False):self.rows=[m.HEADER[:],['synthetic unrelated row','','','synthetic unrelated note']];self.append_calls=0;self.full_reads=0;self.attack=attack;self.lost=lost
 def __call__(self,resource,method,params,body=None):
  if resource=='spreadsheet':return {'spreadsheetId':m.SID,'sheets':[{'properties':{'sheetId':m.GID,'title':m.TAB}}]}
  rng=params['range']
  if method=='append':
   assert params['valueInputOption']=='RAW' and params['insertDataOption']=='INSERT_ROWS' and body=={'majorDimension':'ROWS','values':[row]}
   self.append_calls+=1;self.rows.append(row[:])
   if self.lost:raise RuntimeError('synthetic response loss after server append')
   return {'updates':{'updatedRange':"'Math Puzzles'!A3:D3",'updatedRows':1,'updatedColumns':4}}
  if rng=="'Math Puzzles'!A1:D1":return {'values':[m.HEADER[:]]}
  if rng=="'Math Puzzles'!A:D":
   self.full_reads+=1
   if self.full_reads==2:
    if self.attack=='duplicate':self.rows.append(row[:])
    elif self.attack=='foreign_change':self.rows[1][0]='changed unrelated row'
    elif self.attack=='concurrent_foreign':self.rows.append(['concurrent unrelated row','','','synthetic note'])
   return {'values':copy.deepcopy(self.rows)}
  return {'values':[row[:]]}
sheet=Sheet('concurrent_foreign');acceptance('tracker_RAW_and_concurrent_foreign_append_preserved',lambda:m.record_tracker(sheet));result('tracker_single_append','1',str(sheet.append_calls))
for attack in ['duplicate','foreign_change']:
 F2=fixture('tracker_'+attack);m.A=F2;put(F2/'ROOT_PUBLICATION_GATE.json',ready);p=F2/ready['tracker_row_proposal']['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((A/ready['tracker_row_proposal']['path']).read_bytes());sheet=Sheet(attack);rejection('tracker_postappend_'+attack,lambda:m.record_tracker(sheet))
F2=fixture('tracker_lost');m.A=F2;put(F2/'ROOT_PUBLICATION_GATE.json',ready);p=F2/ready['tracker_row_proposal']['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((A/ready['tracker_row_proposal']['path']).read_bytes());sheet=Sheet(lost=True);rejection('tracker_lost_response_initial',lambda:m.record_tracker(sheet));acceptance('tracker_lost_response_readback_recovery',lambda:m.record_tracker(sheet));result('tracker_lost_response_no_second_append','1',str(sheet.append_calls))
# Prepared-object model, independent of author/native helper stack. Immutable object contents live in memory.
F=fixture('objects');m.A=F;put(F/'ROOT_PUBLICATION_GATE.json',ready)
body=b'exact selected public bytes\n';x={'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()};sel={'case/file.txt':x};digest=m.selected_digest(sel)
r={'original_head':m.HEAD,'gate_sha256':m.pin(F/'ROOT_PUBLICATION_GATE.json')['sha256'],'commit':'prepared','tree':'new_tree','expected_main':'fresh_main','parent_tree':'old_tree','selected_files':sel,'selected_map_sha256':digest,'changed_paths':['case/file.txt']}
class Objects:
 def __init__(self):self.parents=['fresh_main',m.HEAD];self.message='audit\nPR191 selected-map SHA256: '+digest;self.current='new_tree';self.extra=False
 def api(self,path,*args):
  if path=='git/commits/prepared':return {'tree':{'sha':'new_tree'},'parents':[{'sha':p} for p in self.parents],'message':self.message}
  if path=='git/commits/fresh_main':return {'tree':{'sha':'old_tree'}}
  if path=='git/commits/actual_main':return {'tree':{'sha':self.current}}
  raise AssertionError(path)
 def lookup(self,tree,path):return ('100644','blob',x['git_blob']) if tree=='new_tree' else None
 def changed_leaves(self,*a):return {'case/file.txt','foreign.txt'} if self.extra else {'case/file.txt'}
h=Objects();h.m=types.SimpleNamespace(m=types.SimpleNamespace(h=types.SimpleNamespace(warm_selected_directories=lambda *a:None)))
acceptance('object_exact_two_parent_and_full_delta',lambda:m.verify_prepared(h,r,['fresh_main',m.HEAD]))
h.parents=[m.HEAD,'fresh_main'];rejection('object_parent_order_mutant',lambda:m.verify_prepared(h,r,['fresh_main',m.HEAD]));h.parents=['fresh_main',m.HEAD]
h.extra=True;rejection('object_foreign_delta_mutant',lambda:m.verify_prepared(h,r,['fresh_main',m.HEAD]));h.extra=False
h.current='old_tree';rejection('actual_CURRENT_MAIN_differs_from_prepared',lambda:m.selected_current(h,'actual_main',sel,'new_tree'))
r2=copy.deepcopy(r);r2['parent_tree']='invented';rejection('forged_parent_tree_receipt',lambda:m.verify_prepared(h,r2,['fresh_main',m.HEAD]))
# Public media guard and no path escape.
rejection('public_private_path_guard',lambda:m.safe_rel('lifecycle_private/external.json'))
rejection('public_parent_escape_guard',lambda:m.safe_rel('../foreign.txt'))
summary={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':hashlib.sha256((S/'lifecycle_common.py').read_bytes()).hexdigest(),'author_harness_read_or_run':False,'production_helpers_imported_or_run':False,'network_or_git_processes':False,'tests':results,'count':len(results),'satisfied_expectations':sum(x['passed'] for x in results),'unexpected_acceptances':[x['name'] for x in results if not x['passed']]}
put(O/'INDEPENDENT_RESULTS.json',summary)
print(json.dumps({k:v for k,v in summary.items() if k!='tests'},indent=2))
