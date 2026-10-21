"""No-remote adversarial proposal tests; only disposable copies under this folder."""
from pathlib import Path
import copy,hashlib,importlib.util,json,shutil,tempfile,types
D=Path(__file__).resolve().parent;CASE_ROOT=D.parent
spec=importlib.util.spec_from_file_location('proposed_191_controls',D/'lifecycle_common.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
results={'checks':[],'remote_calls':0,'production_modules_imported':0,'proposal_only':True}
def check(n,x):
 if not x:raise AssertionError(n)
 results['checks'].append({'name':n,'passed':True})
def reject(n,f,part=None):
 try:f()
 except (RuntimeError,FileNotFoundError) as e:check(n,part is None or part in str(e))
 else:raise AssertionError('Expected rejection '+n)
def plain(p):return {k:v for k,v in c.pin(p).items() if k!='git_blob'}
source_before={p.relative_to(CASE_ROOT).as_posix():plain(p) for p in [CASE_ROOT/'CURRENT_PROOF_V4.md',CASE_ROOT/'ROOT_WHOLE_REVIEW_INPUT_01.json',CASE_ROOT/'integration_preparation/NATIVE_TEMPLATE_PENDING_01_MANIFEST.json']}
source_packet={p.name:plain(p) for p in (CASE_ROOT/'publication_package_v1').iterdir() if p.is_file()}
frozen= json.loads((CASE_ROOT/'ROOT_WHOLE_REVIEW_INPUT_01.json').read_text())
def fixture(F):
 c.A=F;c._helpers=None
 shutil.copytree(CASE_ROOT/'publication_package_v1',F/'publication_package_v9')
 (F/'integration_preparation').mkdir();shutil.copytree(CASE_ROOT/'integration_preparation/native_template_pending_01',F/'integration_preparation/native_template_pending_09')
 nm=json.loads((CASE_ROOT/'integration_preparation/NATIVE_TEMPLATE_PENDING_01_MANIFEST.json').read_text());nm['current_template']='native_template_pending_09';c.write(F/'integration_preparation/NATIVE_TEMPLATE_PENDING_09_MANIFEST.json',nm)
 for n in ['ORIGINAL_FILE_MANIFEST.json','INTAKE_CHECKPOINT_ACCEPTANCE.json','CURRENT_CASE_STATUS.json']:shutil.copyfile(CASE_ROOT/n,F/n)
 shutil.copyfile(CASE_ROOT/'CURRENT_PROOF_V4.md',F/'CURRENT_PROOF_V9.md');c.write(F/'RESEARCH_LOG.md','FIXTURE LOG\n');c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',{'current_template':nm['current_template'],'files':list(nm['files'])})
 for n in ['REVIEW_A.json','REVIEW_B.json','SEAL_A.json','SEAL_B.json','AUTH_A.json','AUTH_B.json','ROOT_WHOLE_REVIEW_INPUT_09.json']:c.write(F/n,{'fixture':'synthetic final review, not actual clearance'})
 c.write(F/'PR_PROPOSAL.json',{'title':'Credited signed-angle research note PR191','body_before_publication':c.CLAIM})
 c.write(F/'TRACKER_PROPOSAL.json',{'original_problem':'Fuchs Conjecture2.6 /5000005','solution_chat_url':'','notes':c.CLAIM})
 def binding(n):return {'path':n,**plain(F/n)}
 reviews=[{'reviewer_id':letter,'disposition':'PASS','authoritative':True,'report':binding('REVIEW_'+letter+'.json'),'seal':binding('SEAL_'+letter+'.json'),'root_authentication':binding('AUTH_'+letter+'.json')} for letter in ['A','B']]
 g={'schema':'PR191_LIFECYCLE_GATE_V1','status':'READY_FOR_AUTHORIZED_PUBLICATION','PR':191,'original_head':c.HEAD,'qualified_note_route_authorized':True,'historical_priority_clearance':False,'all_required_findings_globally_resolved':True,'whole_package_reviews':reviews,'last_review_required_repairs':0,'package_name':'publication_package_v9','paper_files':{'pdf':'parallel_short_trajectories.pdf','source':'parallel_short_trajectories.tex','support':'verification-package.zip','metadata':'zenodo-deposit.json'},'payloads':{n:plain(F/'publication_package_v9'/n) for n in frozen['package_files']},'current_proof':binding('CURRENT_PROOF_V9.md'),'native_pending_manifest':binding('integration_preparation/NATIVE_TEMPLATE_PENDING_09_MANIFEST.json'),'native_pending_template':nm['current_template'],'native_final_template':'native_template_final_09','native_complete_template':'native_template_complete_09','native_proof_paths':['CANDIDATE.md','PROOF_V4.md'],'native_json_status_paths':sorted(c.JSON_FACTS),'native_text_status_replacements':{'README.md':'PUBLICATION.json contains dated assembly-time publication facts, pending until actual publication and repository acceptance.','review/REVIEW.md':'Those are pending at this dated assembly snapshot.'},'pr_metadata_proposal':binding('PR_PROPOSAL.json'),'tracker_row_proposal':binding('TRACKER_PROPOSAL.json'),'review_input':binding('ROOT_WHOLE_REVIEW_INPUT_09.json'),'public_case_paths':[],'public_case_pins':{}}
 c.write(F/'ROOT_PUBLICATION_GATE.json',g)
 z={'id':999999,'state':'published','environment':'production','doi':'10.9999/AUDIT-MOCK','doi_url':'https://doi.org/10.9999/AUDIT-MOCK','record_url':'https://example.invalid/AUDIT-MOCK','gate_sha256':c.pin(F/'ROOT_PUBLICATION_GATE.json')['sha256'],'files':[{'name':g['paper_files'][k],'size':g['payloads'][g['paper_files'][k]]['bytes'],'sha256':g['payloads'][g['paper_files'][k]]['sha256']} for k in ['pdf','source','support']]};c.write(F/'ZENODO_PUBLICATION_READBACK.json',z)
 tr={'status':'TRACKER_APPEND_AND_TWO_FRESH_READS_ACCEPTED','DOI':z['doi'],'spreadsheet_id':c.SID,'gid':c.GID,'tab':c.TAB,'range':"'Math Puzzles'!A999:D999",'actual_fresh_reads':2,'gate_sha256':z['gate_sha256']};c.write(F/'TRACKER_ACCEPTANCE.json',tr)
 return g,z,tr,nm
def prog():
 return {'current_PR':191,'fully_completed_count':39,'published_count':23,'last_completed_PR':190,'fully_completed_eligible_PRs':list(range(1,39))+[190],'published_PRs':list(range(1,23))+[190],'dated_eligible_total':99,'active_checkpoint_commit':'STALE','remaining_current_step':'STALE PR190','next_step':'STALE next191','program_snapshot_authority_condition':'STALE authority','last_completed_writer_operation_finished':'OLD WINDOW','read_only_next_case':{'PR':1},'historical_completed_case_records':[{'keep':'exact dated history'}]}

with tempfile.TemporaryDirectory(prefix='selftest_',dir=D) as t:
 F=Path(t);g,z,tr,nm=fixture(F)
 wrong=copy.deepcopy(g);wrong['whole_package_reviews'][1]['reviewer_id']='A';c.write(F/'ROOT_PUBLICATION_GATE.json',wrong);reject('same_reviewer_cannot_supply_two_rounds',c.gate,'Distinct successive')
 wrong=copy.deepcopy(g);wrong['whole_package_reviews']=[wrong['whole_package_reviews'][0]['report'],wrong['whole_package_reviews'][0]['seal']];c.write(F/'ROOT_PUBLICATION_GATE.json',wrong);reject('one_report_plus_one_seal_not_two_rounds',c.gate,'Per-review')
 wrong=copy.deepcopy(g);wrong['whole_package_reviews'][1]={**wrong['whole_package_reviews'][0],'reviewer_id':'B'};c.write(F/'ROOT_PUBLICATION_GATE.json',wrong);reject('relabeling_one_review_evidence_rejected',c.gate,'Distinct per-review evidence')
 c.write(F/'ROOT_PUBLICATION_GATE.json',g)
 mirror='verification_support_v9/paper/parallel_short_trajectories.pdf';c.write(F/mirror,'placeholder');(F/mirror).write_bytes((F/g['package_name']/g['paper_files']['pdf']).read_bytes());g['public_case_pins'][mirror]=plain(F/mirror);c.write(F/'ROOT_PUBLICATION_GATE.json',g);check('exact_reviewed_authored_pdf_mirror_allowed',c.gate()['public_case_pins'][mirror]['sha256']==g['payloads'][g['paper_files']['pdf']]['sha256'])
 p=F/mirror;p.write_bytes(b'UNREVIEWED EXTERNAL BODY');wrong=copy.deepcopy(g);wrong['public_case_pins'][mirror]=plain(p);c.write(F/'ROOT_PUBLICATION_GATE.json',wrong);reject('different_body_mirror_rejected',c.gate,'Unapproved body');p.write_bytes((F/g['package_name']/g['paper_files']['pdf']).read_bytes());c.write(F/'ROOT_PUBLICATION_GATE.json',g)
 # Gate fixtures below use the current gate hash, exactly as actual receipts do.
 z['gate_sha256']=c.pin(F/'ROOT_PUBLICATION_GATE.json')['sha256'];tr['gate_sha256']=z['gate_sha256'];c.write(F/'ZENODO_PUBLICATION_READBACK.json',z);c.write(F/'TRACKER_ACCEPTANCE.json',tr)
 extra=F/'integration_preparation'/g['native_pending_template']/'UNMANIFESTED.txt';extra.write_text('extra');reject('pending_native_extra_file_rejected',c.gate,'inventory');extra.unlink()
 check('dynamic_final_package_proof_and_native_versions',c.gate()['package_name']=='publication_package_v9')
 for name,change in [('unready',{'status':'PREPARED'}),('wrong_original_head',{'original_head':'0'*40}),('last_review_repairs',{'last_review_required_repairs':1})]:
  c.write(F/'ROOT_PUBLICATION_GATE.json',{**g,**change});reject('gate_rejects_'+name,c.gate)
 c.write(F/'ROOT_PUBLICATION_GATE.json',g)
 p=F/g['package_name']/g['paper_files']['source'];b=p.read_bytes();p.chmod(0o644);p.write_bytes(b+b'WRONG');reject('gate_rejects_changed_payload',c.gate,'Bound bytes drift');p.write_bytes(b)
 p=F/g['current_proof']['path'];b=p.read_bytes();p.write_bytes(b+b'WRONG');reject('gate_rejects_changed_current_proof',c.gate,'Bound bytes drift');p.write_bytes(b)
 for bad in ['../escape','lifecycle_private/source.pdf','sheets_tracking/PREAPPEND_FRESH_READ.stdout.json','.zenodo-state/state.json']:
  reject('private_or_escaping_path_rejected_'+bad,lambda:c.safe_rel(bad))
 class PRHelper:
  def api(self,n):return {'head':{'sha':'0'*40},'state':'open','merged':False,'draft':True}
 c._helpers=PRHelper();reject('original_head_drift_rejected',c.original_ready,'Original head');c._helpers=None
 j95=c.progress(prog(),g,z,tr,95)
 check('phase95_counts_aliases_and_no_advance',(j95['fully_completed_count'],j95['published_count'],j95['last_completed_PR'],j95['fully_completed_fraction_percent'],j95['next_numeric_intake_cursor'],j95['advance_to_next_PR_authorized_now'])==(39,23,190,39.39,192,False) and 'active_checkpoint_commit' not in j95 and 'PR191' in j95['remaining_current_step'] and 'Actual credited PR191' in j95['program_snapshot_semantics'])
 c.write(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',{'merge_commit':'fixture-merge','PR_merged':True,'every_selected_identity_checked_at_actual_observed_MAIN':True,'original_head':c.HEAD})
 j100=c.progress(copy.deepcopy(j95),g,z,tr,100)
 check('phase100_counts_unique_and_conditional_next',(j100['fully_completed_count'],j100['published_count'],j100['last_completed_PR'],j100['fully_completed_fraction_percent'],j100['next_numeric_intake_cursor'])==(40,24,191,40.4,192) and j100['next_intake_requires_actual_completion_receipt'] and j100['advance_to_next_PR_authorized_now'] and j100['historical_completed_case_records']==j95['historical_completed_case_records'])
 reject('wrong_phase_census_rejected',lambda:c.normalize(prog(),100),'census')
 check('no_window_or_future_self_commit',j100['next_intake_requires_explicit_writer_release'] is False and j100['peer_pause_or_exclusive_writer_window_assumed'] is False and 'active_checkpoint_commit' not in j100 and j100['retired_live_aliases_PR191'][0]['values']['active_checkpoint_commit']=='STALE')
 before={n:plain(F/'integration_preparation'/g['native_pending_template']/n) for n in nm['files']};cur=c.prepare_native(False);T=F/'integration_preparation'/cur['current_template']
 check('native_final_exact50_and_original16',len(cur['files'])==50 and sum(n.startswith('ORIGINAL_SUBMISSION/') for n in cur['files'])==16 and all(plain(T/n)==before[n] for n in before if n.startswith('ORIGINAL_SUBMISSION/')))
 check('native_science_unchanged',all(plain(T/n)==before[n] for n in before if n not in cur['only_declared_factual_paths_changed']))
 incomplete=copy.deepcopy(cur);incomplete['files'].pop('verify.py');c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',incomplete);reject('incomplete_current_native_manifest_rejected',lambda:c.current_native(g,False),'incomplete');c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',cur)
 extra=T/'UNLISTED';extra.write_text('extra');reject('current_native_extra_file_rejected',lambda:c.current_native(g,False),'inventory');extra.unlink()
 for n in c.JSON_FACTS:
  j=c.read(T/n)
  check('native_live_aliases_'+n,all(j.get(k) is expected for k,expected in [('whole_package_reviews_pending',False),('successive_NEW_whole_package_reviews_complete',True),('publication_clearance',True),('publication_and_tracker_actions_not_yet_performed',False)] if k in j))
 check('native_readme_review_pending_sentences_replaced',all(needle not in (T/n).read_text() for n,needle in g['native_text_status_replacements'].items()))
 check('native_does_not_preclaim_merge',c.read(T/'CURRENT_RESULT.json')['actual_original_PR_merged'] is False and c.read(F/'CURRENT_CASE_STATUS.json')['original_PR_merged'] is False and c.read(F/'CURRENT_CASE_STATUS.json')['first_whole_package_review_active'] is False)
 cur100=c.prepare_native(True);T100=F/'integration_preparation'/cur100['current_template'];check('postaccepted_merge_native_current_flags_true',c.read(T100/'CURRENT_RESULT.json')['actual_original_PR_merged'] is True and c.read(T100/'PUBLICATION.json')['actual_original_PR_merged'] is True and all(plain(T100/n)==before[n] for n in before if n not in cur100['only_declared_factual_paths_changed']))
 request=c.metadata_request();check('metadata_191_dynamic_actual_DOI_and_credit',request['request']['pr_number']==191 and c.HEAD in request['expected_original_head'] and z['doi_url'] in request['request']['body'] and 'all16' in request['request']['body'].lower() and '5000007' not in request['request']['body'])
 accept={'status':'ACTUAL_ORIGINAL_HEAD_METADATA_AND_READY_STATE_ACCEPTED','PR':191,'original_head':c.HEAD,'gate_sha256':z['gate_sha256'],'request_sha256':c.pin(F/'PR_METADATA_REQUEST.json')['sha256']};c.write(F/'PR_METADATA_ACCEPTANCE.json',accept);p={'title':request['request']['title'],'body':request['request']['body']};c.require_metadata(g,z,tr,p);check('metadata_exact_actual_request_accepted',True)
 reject('metadata_actual_body_mutant_rejected',lambda:c.require_metadata(g,z,tr,{**p,'body':'WRONG CLAIM'}),'Actual PR metadata')
 c.write(F/'PR_METADATA_ACCEPTANCE.json',{**accept,'request_sha256':'0'*64});reject('metadata_receipt_wrong_request_binding_rejected',lambda:c.require_metadata(g,z,tr,p),'acceptance binding');c.write(F/'PR_METADATA_ACCEPTANCE.json',accept)
 c.write(F/'ZENODO_PUBLICATION_READBACK.json',{**z,'files':[]});reject('publication_missing_uploaded_file_pins_rejected',lambda:c.publication(g),'exact uploaded');c.write(F/'ZENODO_PUBLICATION_READBACK.json',z)

# Tracker controls: callbacks never invoke GWS. Other rows stay only in memory.
for mode in ['append','existing','unknown_absent','false_duplicate','two_duplicates','wrong_header','wrong_tab','lost_append','bad_row_read']:
 with tempfile.TemporaryDirectory(prefix='tracker_',dir=D) as t:
  F=Path(t);g,z,tr,nm=fixture(F);proposal=c.read(F/'TRACKER_PROPOSAL.json');row=[proposal['original_problem'],'',z['doi_url'],proposal['notes']];calls=[];appends=[]
  if mode in ['unknown_absent','existing']:c.write(F/'sheets_tracking/APPEND_ATTEMPT_STARTED.json',{'unknown':True})
  def call(resource,method,params,body=None):
   calls.append((resource,method,params.get('range')))
   if resource=='spreadsheet':return {'spreadsheetId':c.SID,'sheets':[{'properties':{'sheetId':c.GID,'title':'WRONG' if mode=='wrong_tab' else c.TAB}}]}
   if method=='append':
    appends.append(body);check('append_is_RAW_and_one_own_row_'+mode,params['valueInputOption']=='RAW' and body['values']==[row])
    if mode=='lost_append':raise RuntimeError('SIMULATED unknown outcome')
    return {'updates':{'updatedRange':"'Math Puzzles'!A9:D9",'updatedRows':1,'updatedColumns':4}}
   if params['range']=="'Math Puzzles'!A1:D1":return {'values':[['WRONG'] if mode=='wrong_header' else c.HEADER]}
   if params['range']=="'Math Puzzles'!A:D":
    rows=[c.HEADER,['OTHER PRIVATE PROBLEM','','https://doi.org/10.9999/OTHER','private notes']]
    if mode=='existing':rows.append(row)
    if mode=='false_duplicate':rows.append(['foreign','','otherdoi','mentions '+z['doi']])
    if mode=='two_duplicates':rows.extend([row,row])
    return {'values':rows}
   return {'values':[['WRONG']] if mode=='bad_row_read' else [row]}
  if mode in ['append','existing']:
   out=c.record_tracker(call);check('tracker_success_'+mode,out['actual_fresh_reads']==2 and len(appends)==(1 if mode=='append' else 0) and len([x for x in calls if x[2] and x[2] not in ["'Math Puzzles'!A1:D1","'Math Puzzles'!A:D"]])==2)
  else:
   reject('tracker_rejects_'+mode,lambda:c.record_tracker(call));check('tracker_no_acceptance_'+mode,not (F/'TRACKER_ACCEPTANCE.json').exists())
   check('tracker_no_extra_append_'+mode,len(appends)<= (1 if mode in ['lost_append','bad_row_read'] else 0))
  if mode=='lost_append':check('unknown_append_marker_written_before_call',(F/'sheets_tracking/APPEND_ATTEMPT_STARTED.json').exists())
  check('other_tracker_rows_never_saved_'+mode,all('OTHER PRIVATE PROBLEM' not in p.read_text() for p in (F/'sheets_tracking').glob('*.json')))

# Exact object/control functions, using immutable tree identity maps.
def bp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
class Git:
 def __init__(self):
  self.maps={'base':{'foreign/file':('100644','blob','f'*40)},'prepared':{},'actual':{}};self.bodies={};self.posts=[];self.foreign_mutant=False
  self.m=types.SimpleNamespace(m=types.SimpleNamespace(h=types.SimpleNamespace(warm_selected_directories=lambda *x:None)))
 def api(self,n,method=None,body=None):
  if method=='POST':
   self.posts.append(n)
   if n=='git/trees':
    table=dict(self.maps['base'])
    for x in body['tree']:table[x['path']]=('100644','blob',bp(x['content'].encode())['git_blob'])
    if self.foreign_mutant:table['foreign/UNAUTHORIZED']=('100644','blob','e'*40)
    self.maps['new']=table;return {'sha':'new'}
   if n=='git/commits':return {'sha':'commit'}
  if n=='git/commits/fresh':return {'tree':{'sha':'base'}}
  if n=='git/commits/actual':return {'tree':{'sha':'actual'}}
  if n=='git/commits/commit':return {'tree':{'sha':'new'},'parents':[{'sha':'fresh'},{'sha':c.HEAD}]}
  if n=='git/ref/heads/main':return {'object':{'sha':'fresh'}}
  raise RuntimeError('Unexpected mock path '+n)
 def lookup(self,t,n):return self.maps[t].get(n)
 def changed_leaves(self,a,b):return {n for n in set(self.maps[a])|set(self.maps[b]) if self.maps[a].get(n)!=self.maps[b].get(n)}

# Full no-remote lifecycle acceptance plus a concrete stale-MAIN factual retry.
class FullGit:
 def __init__(self,F,g,j95,cur):
  self.F=F;self.g=g;self.main='mainold';self.advance=False;self.ref_reads=0;self.posts=0;self.blobs={};self.maps={};self.commits={};self.m=types.SimpleNamespace(m=types.SimpleNamespace(h=types.SimpleNamespace(warm_selected_directories=lambda *a:None)))
  content={c.NATIVE+n:(F/'integration_preparation'/cur['current_template']/n).read_bytes() for n in cur['files']};content.update({c.CASE+g['package_name']+'/'+n:(F/g['package_name']/n).read_bytes() for n in g['payloads']});content[c.PREFIX+'CURRENT_PROGRESS.json']=(json.dumps(j95)+'\n').encode();content[c.PREFIX+'CURRENT_PROGRESS.md']=b'PROGRESS\n';content[c.PREFIX+'RESEARCH_LOG.md']=b'LOG\n'
  table={n:('100644','blob',self.put(b)) for n,b in content.items()};self.maps['pre']={'foreign/base':('100644','blob',self.put(b'foreign before'))};self.maps['merged']={**self.maps['pre'],**table};self.maps['tipold']={**self.maps['merged'],'foreign/descendant':('100644','blob',self.put(b'foreign allowed'))};self.maps['tipnew']={**self.maps['tipold'],'foreign/newer':('100644','blob',self.put(b'foreign newer'))}
  self.commits={'acceptedmerge':{'tree':{'sha':'merged'},'parents':[{'sha':'premerge'},{'sha':c.HEAD}]},'mainold':{'tree':{'sha':'tipold'},'parents':[{'sha':'acceptedmerge'}]},'mainnew':{'tree':{'sha':'tipnew'},'parents':[{'sha':'mainold'}]}}
  selected={n:bp(b) for n,b in content.items()};c.write(F/'SCOPED_MERGE_PREPARATION.json',{'commit':'acceptedmerge','tree':'merged','parent_tree':'pre','expected_main':'premerge','selected_files':selected,'changed_paths':list(selected)})
 def put(self,b):x=bp(b)['git_blob'];self.blobs[x]=b;return x
 def api(self,n,method=None,body=None):
  if method=='POST':
   self.posts+=1
   if n=='git/blobs':return {'sha':self.put(__import__('base64').b64decode(body['content']))}
   if n=='git/trees':
    name='tree'+str(self.posts);table=dict(self.maps[body['base_tree']])
    for x in body['tree']:table[x['path']]=('100644','blob',self.put(x['content'].encode()) if 'content' in x else x['sha'])
    self.maps[name]=table;return {'sha':name}
   if n=='git/commits':name='candidate'+str(self.posts);self.commits[name]={'tree':{'sha':body['tree']},'parents':[{'sha':x} for x in body['parents']]};return {'sha':name}
  if n=='git/ref/heads/main':
   self.ref_reads+=1
   if self.advance and self.ref_reads>=2:self.main='mainnew'
   return {'object':{'sha':self.main}}
  if n.startswith('git/commits/'):return self.commits[n.split('/')[-1]]
  if n.startswith('compare/'):return {'status':'ahead'}
  if n=='pulls/191':return {'merged':True,'state':'closed','head':{'sha':c.HEAD},'merge_commit_sha':'acceptedmerge'}
  raise RuntimeError('Unexpected full mock path '+n)
 def lookup(self,t,n):return self.maps[t].get(n)
 def changed_leaves(self,a,b):return {n for n in set(self.maps[a])|set(self.maps[b]) if self.maps[a].get(n)!=self.maps[b].get(n)}
 def body_at(self,n,ref):return self.blobs[self.maps[self.commits[ref]['tree']['sha']][n][2]]
with tempfile.TemporaryDirectory(prefix='full_retry_',dir=D) as t:
 F=Path(t);g,z,tr,nm=fixture(F);cur=c.prepare_native(False);j95=c.progress(prog(),g,z,tr,95);h=FullGit(F,g,j95,cur);c._helpers=h
 accepted=c.integration_accept();check('actual_integration_accept_all_native50_and_packet',accepted['every_selected_identity_checked_at_actual_observed_MAIN'] and accepted['original_head']==c.HEAD)
 cur_merge=c.read(F/'SCOPED_MERGE_PREPARATION.json');incomplete=copy.deepcopy(cur_merge);incomplete['selected_files'].pop(c.NATIVE+'verify.py');reject('incomplete_native_merge_map_rejected',lambda:c.require_merge_scope(g,incomplete),'omits reviewed')
 plan={'selected_MAIN_paths':list(cur_merge['selected_files'])+[c.CASE+n for n in ['SCOPED_MERGE_PREPARATION.json','ROOT_ACTUAL_MERGE_ACCEPTANCE.json','WORKFLOW_COMPLETION.json','CURRENT_CASE_STATUS.json','RESEARCH_LOG.md','integration_preparation/CURRENT_TEMPLATE.json']],'factual_additional_paths':[c.CASE+'integration_preparation/'+g['native_complete_template']+'/'+n for n in cur['files']]+[c.CASE+'integration_preparation/'+g['native_complete_template']+'_MANIFEST.json']};c.write(F/'FINAL_MAIN_SCOPE.json',plan)
 gatehash=c.pin(F/'ROOT_PUBLICATION_GATE.json')['sha256'];h.advance=True;h.ref_reads=0
 reject('full_factual_prepare_detects_MAIN_advance',lambda:c.factual_prepare('factual_preparation_first'),'MAIN advanced');first=c.read(F/'FINAL_FACTUAL_PREPARATION.json');nativefirst=c.read(F/'integration_preparation/CURRENT_TEMPLATE.json');check('first_stale_preparation_preserved_before_retry',(F/'integration_preparation/factual_preparation_first/CURRENT_PROGRESS.json').is_file())
 h.advance=False;h.ref_reads=0;second=c.factual_prepare('factual_preparation_second')
 check('fresh_retry_reuses_exact_native_complete_generation',c.read(F/'integration_preparation/CURRENT_TEMPLATE.json')==nativefirst and first['commit']!=second['commit'])
 history=F/'integration_preparation/receipt_history'/('FINAL_FACTUAL_PREPARATION_'+first['commit']+'.json');check('fresh_retry_archives_immutable_first_receipt',c.read(history)==first and (history.stat().st_mode & 0o777)==0o444)
 check('fresh_retry_does_not_rewrite_gate',c.pin(F/'ROOT_PUBLICATION_GATE.json')['sha256']==gatehash)
 h.main=second['commit'];out=c.factual_accept();check('actual_factual_accept_combined_overrides_and_all_selected',out['every_selected_identity_checked_at_actual_observed_MAIN'] and out['fully_completed_count']==40 and out['published_count']==24)
 (F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').unlink();tree='mutant';h.maps[tree]=dict(h.maps[second['tree']]);h.maps[tree][c.NATIVE+'verify.py']=('100644','blob',h.put(b'WRONG SCIENCE'));h.commits['descendant_mutant']={'tree':{'sha':tree},'parents':[{'sha':second['commit']}]};h.main='descendant_mutant';reject('actual_factual_accept_rejects_later_native_mutant',c.factual_accept,'Selected current MAIN identity')
 check('failed_factual_accept_has_no_receipt',not (F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').exists())
for mutation in [None,'native','pdf','zip','deleted','foreign_only']:
 with tempfile.TemporaryDirectory(prefix='identity_',dir=D) as t:
  fixture(Path(t));h=Git();selected={n:bp(n.encode()) for n in ['native/check.py','packet/paper.pdf','packet/support.zip']};h.maps['actual']={n:('100644','blob',v['git_blob']) for n,v in selected.items()}
  if mutation in ['native','pdf','zip']:n={'native':'native/check.py','pdf':'packet/paper.pdf','zip':'packet/support.zip'}[mutation];h.maps['actual'][n]=('100644','blob','b'*40)
  if mutation=='deleted':h.maps['actual'].pop('native/check.py')
  if mutation=='foreign_only':h.maps['actual']['foreign/changed']=('100644','blob','c'*40)
  if mutation not in [None,'foreign_only']:reject('current_tree_rejects_'+mutation,lambda:c.selected_current(h,'actual',selected),'Selected current MAIN identity')
  else:check('current_tree_accepts_'+str(mutation),c.selected_current(h,'actual',selected)=='actual')
  merged=selected;factual={'native/status.json':bp(b'new factual status')};combined={**merged,**factual};h.maps['actual']={n:('100644','blob',x['git_blob']) for n,x in combined.items()};check('combined_factual_override_allowed_'+str(mutation),c.selected_current(h,'actual',combined)=='actual')
with tempfile.TemporaryDirectory(prefix='scope_',dir=D) as t:
 F=Path(t);fixture(F);p=F/'own.txt';p.write_text('owned');h=Git();h.foreign_mutant=True
 reject('full_tree_foreign_scope_mutant',lambda:c.prepare_tree(h,'fresh',{'case/own.txt':p},['fresh',c.HEAD],'fixture','PREP.json'),'Full-tree foreign scope drift');check('foreign_scope_rejected_before_commit','git/commits' not in h.posts)
row='|'+'|'.join(['x']*12)+'|';cells=row.split('|');cells[1]=' 5000005 / TARGET ';cells[8]=' claimed_solved ';cells[9]=' 2/5 ';row='|'.join(cells);original='HEADER\n'+row+'\nFOREIGN ROW\n'
check('queue_changes_only_target',c.queue_update(original,original,original,'10.9999/X','https://doi.org/10.9999/X').endswith('FOREIGN ROW\n'))
reject('foreign_target_row_drift',lambda:c.queue_update(original.replace('TARGET','FOREIGN CHANGE'),original,original,'x','y'),'Foreign target-row drift')
provenance=json.loads((CASE_ROOT/'ROOT_ORIGINAL_PARENT_AND_QUEUE_GUARD_01.json').read_text());rows={x['commit']:x['row'] for x in provenance['rows']};observed=provenance['actual_MAIN_observed'];before='HEADER\n'+rows[observed]+'\nFOREIGN ROW\n';orig='HEADER\n'+rows[c.HEAD]+'\nFOREIGN ROW\n';base='HEADER\n'+rows[c.ORIGINAL_BASE]+'\nFOREIGN ROW\n';updated=c.queue_update(before,orig,base,'10.9999/X','https://doi.org/10.9999/X');cells=updated.splitlines()[1].split('|')
check('actual_original_base_and_queue_PR_link',c.ORIGINAL_BASE==provenance['original_proof_parent_base'] and cells[10].strip()=='https://github.com/AlecKriebel/Math/pull/191' and cells[9].strip()=='2/5' and updated.endswith('FOREIGN ROW\n'))

# Zenodo calls are stub processes only: recover stage/publish, never blind retries.
for mode in ['stage_new','stage_unknown','stage_wrong_gate','publish_already','publish_unknown']:
 with tempfile.TemporaryDirectory(prefix='zenodo_',dir=D) as t:
  F=Path(t);g,z,tr,nm=fixture(F);c.original_ready=lambda draft=None:{'head':{'sha':c.HEAD}};calls=[]
  if mode in ['stage_unknown','stage_wrong_gate']:c.write(F/'lifecycle_private/ZENODO_STAGE_ATTEMPT_STARTED.json',{'unknown':True,'gate_sha256':c.pin(F/'ROOT_PUBLICATION_GATE.json')['sha256'] if mode=='stage_unknown' else 'WRONG_GATE'})
  if mode.startswith('publish'):
   c.write(F/'ZENODO_STAGE_READBACK.json',{'id':99,'gate_sha256':c.pin(F/'ROOT_PUBLICATION_GATE.json')['sha256']})
   if mode=='publish_unknown':c.write(F/'lifecycle_private/ZENODO_PUBLISH_ATTEMPT_STARTED.json',{'id':99})
  def runner(args,**kwargs):
   action=args[6];calls.append(action)
   if mode=='stage_unknown':return types.SimpleNamespace(returncode=1,stdout=b'',stderr=b'unknown draft state')
   out={'environment':'production','id':99,'state':'published' if mode=='publish_already' else 'ready_to_publish'}
   if out['state']=='published':out.update(doi=z['doi'],doi_url=z['doi_url'],record_url=z['record_url'])
   return types.SimpleNamespace(returncode=0,stdout=json.dumps(out).encode(),stderr=b'')
  if mode=='stage_new':check('zenodo_one_stage_creation',c.run_zenodo('stage',runner=runner)['id']==99 and calls==['stage'])
  elif mode=='publish_already':check('zenodo_existing_publication_no_second_POST',c.run_zenodo('publish','99',runner)['state']=='published' and calls==['inspect'])
  else:reject('zenodo_no_blind_retry_'+mode,lambda:c.run_zenodo('stage' if mode.startswith('stage') else 'publish','99',runner));check('zenodo_retry_never_posts_'+mode,all(x=='inspect' for x in calls))
  if mode=='stage_wrong_gate':check('stage_wrong_gate_rejected_before_external_runner',calls==[])

spec=importlib.util.spec_from_file_location('canonical_guard',D/'protect_canonical_outputs.py');guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
with tempfile.TemporaryDirectory(prefix='guard_',dir=D) as t:
 F=Path(t);(F/'audited.py').write_text('SENTINEL');reject('generator_canonical_protection',lambda:guard.require_new_outputs(F,['audited.py']),'Refuse overwriting');check('generator_existing_bytes_unchanged',(F/'audited.py').read_text()=='SENTINEL')
check('root_frozen_inputs_unchanged',all(plain(CASE_ROOT/n)==x for n,x in source_before.items()) and all(plain(CASE_ROOT/'publication_package_v1'/n)==x for n,x in source_packet.items()))
results.update(UTC=c.now(),verdict='PASS_OFFLINE_PROPOSAL_CONTROLS',checks_passed=len(results['checks']),root_inputs_unchanged=True,original16_preserved=True,external_actions_untested=True)
(D/'SELFTEST_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps({'verdict':results['verdict'],'checks':len(results['checks']),'remote_calls':0}))
