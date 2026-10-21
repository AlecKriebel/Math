"""Independent offline PR191 lifecycle probes. No live helper or service imports.
Run python3 -B independent_probe.py. Fixtures exist only in this own folder.
"""
from pathlib import Path
import base64,copy,hashlib,importlib.util,json,shutil,socket,subprocess,sys,tempfile,types
OWN=Path(__file__).resolve().parent
CASE=OWN.parent
PROPOSAL=CASE/'lifecycle_controls_preparation_01'
sys.dont_write_bytecode=True

def forbidden(*a,**k):raise AssertionError('LIVE PROCESS/NETWORK FORBIDDEN')
socket.socket=forbidden;socket.create_connection=forbidden;subprocess.run=forbidden
spec=importlib.util.spec_from_file_location('independently_probed_controls',PROPOSAL/'lifecycle_common.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
RESULTS=[]

def check(name,fn,expected='pass'):
 try:
  evidence=fn()
  RESULTS.append({'name':name,'outcome':'PASS','expected':expected,'evidence':evidence})
 except Exception as exc:
  RESULTS.append({'name':name,'outcome':'HARNESS_OR_UNEXPECTED_FAILURE','expected':expected,'error':type(exc).__name__+': '+str(exc)})

def rejects(fn,contains=None):
 try:fn()
 except RuntimeError as e:
  if contains:assert contains in str(e),(contains,str(e))
  return str(e)
 raise AssertionError('Unsafe action was accepted')

def dump(p,v):
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():p.chmod(0o644)
 p.write_text(v if isinstance(v,str) else json.dumps(v,indent=2)+'\n')
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def fixture():
 td=tempfile.TemporaryDirectory(prefix='offline_fixture_',dir=OWN);p=Path(td.name);m.A=p;m._helpers=None
 files={'paper.pdf':b'%PDF synthetic\xff','paper.tex':b'credited theorem synthetic','support.zip':b'PK\xffsynthetic','README.md':b'five file packet'}
 for n,b in files.items():(p/'packet').mkdir(exist_ok=True);(p/'packet'/n).write_bytes(b)
 metadata={'metadata':{'title':'Synthetic credited note','description':'No novelty','upload_type':'publication','publication_type':'preprint','creators':[{'name':'Alec Kriebel'}]},'files':[{'path':n} for n in ['paper.pdf','paper.tex','support.zip']]}
 dump(p/'packet/zenodo.json',metadata)
 proof='approved proof synthetic\n';dump(p/'PROOF.md',proof)
 T=p/'integration_preparation/native_template_pending_probe';T.mkdir(parents=True)
 native={'CANDIDATE.md':proof,'PROOF_V4.md':proof,'verify.py':'assert True\n','RESEARCH_LOG.md':'Dated pending generation.\n','README.md':'Pending publication sentence.','review/REVIEW.md':'Pending review sentence.'}
 for n in m.JSON_FACTS:native[n]={'UTC':'before','whole_package_reviews_complete':False,'publication_ready':False,'actual_Zenodo_published':False,'actual_DOI':None,'actual_tracker_updated':False,'actual_original_PR_merged':False,'case_percent':60,'novelty_clearance':False,'whole_package_reviews_pending':True}
 originals=[]
 for i in range(16):
  n=f'original_{i:02}.txt';native['ORIGINAL_SUBMISSION/'+n]=f'original artifact {i}\n';originals.append(n)
 for n,v in native.items():dump(T/n,v)
 manifest={'current_template':T.name,'files':{n:m.pin(T/n) for n in native}}
 dump(p/'integration_preparation/PENDING_MANIFEST.json',manifest)
 dump(p/'ORIGINAL_FILE_MANIFEST.json',{'original_head':m.HEAD,'files':[{'path':m.NATIVE+n,**m.pin(T/'ORIGINAL_SUBMISSION'/n)} for n in originals]})
 reviews=[]
 for i in [1,2]:
  r={'reviewer_id':f'independent-{i}','disposition':'PASS','authoritative':True}
  for k in ['report','seal','root_authentication']:
   n=f'review_{i}_{k}.json';dump(p/n,{'reviewer':i,'disposition':'PASS','status':'accepted','generation':i});r[k]={'path':n,**m.pin(p/n)}
  reviews.append(r)
 dump(p/'METADATA_PROPOSAL.json',{'title':'Credited note','body_before_publication':'Qualified credited verification. No novelty.'})
 dump(p/'TRACKER_PROPOSAL.json',{'original_problem':'Synthetic PR191','solution_chat_url':'','notes':'Credited note; no novelty.'})
 dump(p/'REVIEW_INPUT.json',{'package':'packet','proof':'PROOF.md'})
 g={'schema':'PR191_LIFECYCLE_GATE_V1','status':'READY_FOR_AUTHORIZED_PUBLICATION','PR':191,'original_head':m.HEAD,'qualified_note_route_authorized':True,'historical_priority_clearance':False,'all_required_findings_globally_resolved':True,'last_review_required_repairs':0,'whole_package_reviews':reviews,'package_name':'packet','payloads':{n:m.pin(p/'packet'/n) for n in [*files,'zenodo.json']},'paper_files':{'pdf':'paper.pdf','source':'paper.tex','support':'support.zip','metadata':'zenodo.json'},'current_proof':{'path':'PROOF.md',**m.pin(p/'PROOF.md')},'native_pending_template':T.name,'native_pending_manifest':{'path':'integration_preparation/PENDING_MANIFEST.json',**m.pin(p/'integration_preparation/PENDING_MANIFEST.json')},'native_proof_paths':['CANDIDATE.md','PROOF_V4.md'],'native_json_status_paths':sorted(m.JSON_FACTS),'native_text_status_replacements':{'README.md':'Pending publication sentence.','review/REVIEW.md':'Pending review sentence.'},'native_final_template':'native_template_final_probe','native_complete_template':'native_template_complete_probe','pr_metadata_proposal':{'path':'METADATA_PROPOSAL.json',**m.pin(p/'METADATA_PROPOSAL.json')},'tracker_row_proposal':{'path':'TRACKER_PROPOSAL.json',**m.pin(p/'TRACKER_PROPOSAL.json')},'review_input':{'path':'REVIEW_INPUT.json',**m.pin(p/'REVIEW_INPUT.json')},'public_case_paths':[],'public_case_pins':{}}
 dump(p/'ROOT_PUBLICATION_GATE.json',g)
 z={'environment':'production','id':90000001,'state':'published','doi':'10.5281/zenodo.90000001','doi_url':'https://doi.org/10.5281/zenodo.90000001','files':[{'name':g['paper_files'][k],'size':g['payloads'][g['paper_files'][k]]['bytes'],'sha256':g['payloads'][g['paper_files'][k]]['sha256']} for k in ['pdf','source','support']],'gate_sha256':m.pin(p/'ROOT_PUBLICATION_GATE.json')['sha256']}
 dump(p/'ZENODO_PUBLICATION_READBACK.json',z)
 tr={'status':'TRACKER_APPEND_AND_TWO_FRESH_READS_ACCEPTED','spreadsheet_id':m.SID,'gid':m.GID,'tab':m.TAB,'range':"'Math Puzzles'!A3:D3",'DOI':z['doi'],'actual_fresh_reads':2,'gate_sha256':z['gate_sha256']}
 dump(p/'TRACKER_ACCEPTANCE.json',tr)
 dump(p/'INTAKE_CHECKPOINT_ACCEPTANCE.json',{'PR':191,'original_head':m.HEAD,'checkpoint_commit':'1'*40})
 dump(p/'CURRENT_CASE_STATUS.json',{'original_PR_merged':False,'DOI':None});dump(p/'RESEARCH_LOG.md','Research log.\n')
 for n in m.CONTROL_FILES:dump(p/n,'# synthetic installed control '+n+'\n')
 for n in ['ROOT_ORIGINAL_PARENT_AND_QUEUE_GUARD_01.json','ZENODO_LOCAL_CHECK.json','ZENODO_STAGE_READBACK.json','ZENODO_DRAFT_READBACK.json','ZENODO_POSTPUBLICATION_INSPECTION.json','sheets_tracking/TARGET_VALIDATION.json','sheets_tracking/ROW_READBACK_1.json','sheets_tracking/ROW_READBACK_2.json']:dump(p/n,{})
 return td,p,g,z,tr

class Native:
 def __init__(self):
  self.blobs={};self.trees={};self.commits={};self.counter=0;self.main=None;self.advance_on_create=False;self.drift_foreign_on_tree=False
  self.pr={'head':{'sha':m.HEAD},'state':'open','merged':False,'draft':False,'title':'','body':''}
  self.m=types.SimpleNamespace(m=types.SimpleNamespace(h=types.SimpleNamespace(warm_selected_directories=lambda *a:None)))
 def ident(self):self.counter+=1;return f'{self.counter:040x}'
 def store(self,b):s=blob(b);self.blobs[s]=b;return ('100644','blob',s)
 def tree(self,contents):
  t=self.ident();self.trees[t]={n:self.store(b) for n,b in contents.items()};return t
 def commit(self,t,parents=()):c=self.ident();self.commits[c]={'tree':{'sha':t},'parents':[{'sha':s} for s in parents]};return c
 def altered(self,parent,changes):
  t=self.ident();self.trees[t]=dict(self.trees[self.commits[parent]['tree']['sha']]);self.trees[t].update({n:self.store(b) for n,b in changes.items()});return self.commit(t,[parent])
 def api(self,path,method='GET',data=None):
  if path=='git/ref/heads/main':return {'object':{'sha':self.main}}
  if path.startswith('git/commits/') and method=='GET':return copy.deepcopy(self.commits[path.split('/')[-1]])
  if path=='git/blobs':return {'sha':self.store(base64.b64decode(data['content']))[2]}
  if path=='git/trees':
   t=self.ident();self.trees[t]=dict(self.trees[data['base_tree']])
   for e in data['tree']:self.trees[t][e['path']]=self.store(e['content'].encode()) if 'content' in e else (e['mode'],e['type'],e['sha'])
   if self.drift_foreign_on_tree:self.trees[t]['foreign/unrelated.txt']=self.store(b'CORRUPTED')
   return {'sha':t}
  if path=='git/commits':
   c=self.commit(data['tree'],data['parents'])
   if self.advance_on_create:self.advance_on_create=False;self.main=self.altered(self.main,{'foreign/new.txt':b'concurrent peer bytes'})
   return {'sha':c}
  if path=='pulls/191':return copy.deepcopy(self.pr)
  if path.startswith('compare/'):
   a,b=path[len('compare/'):].split('...');seen=set();q=[b]
   while q:
    c=q.pop()
    if c==a:return {'status':'identical' if a==b else 'ahead'}
    if c in seen:continue
    seen.add(c);q += [x['sha'] for x in self.commits.get(c,{}).get('parents',[])]
   return {'status':'diverged'}
  raise AssertionError(('Unexpected offline native API',path,method))
 def lookup(self,t,n):return self.trees[t].get(n)
 def changed_leaves(self,a,b):return {n for n in self.trees[a].keys()|self.trees[b].keys() if self.lookup(a,n)!=self.lookup(b,n)}
 def body_at(self,n,c):return self.blobs[self.lookup(self.commits[c]['tree']['sha'],n)[2]]

def integration_fixture():
 td,p,g,z,tr=fixture();m.prepare_native(False);req=m.metadata_request();dump(p/'PR_METADATA_ACCEPTANCE.json',{'status':'ACTUAL_ORIGINAL_HEAD_METADATA_AND_READY_STATE_ACCEPTED','PR':191,'original_head':m.HEAD,'gate_sha256':z['gate_sha256'],'request_sha256':m.pin(p/'PR_METADATA_REQUEST.json')['sha256']})
 h=Native();h.pr.update(title=req['request']['title'],body=req['request']['body'])
 guard=json.loads((CASE/'ROOT_ORIGINAL_PARENT_AND_QUEUE_GUARD_01.json').read_text());original=guard['rows'][1]['row'];base=guard['rows'][2]['row'];q='unsolved_math_prioritization/QUEUE.md'
 progress={'fully_completed_count':39,'published_count':23,'last_completed_PR':190,'current_PR':191,'dated_eligible_total':99,'fully_completed_eligible_PRs':list(range(100,139)),'published_PRs':list(range(100,123)),'skipped_since_last_completion':[],'actual_factual_checkpoint_accepted':True,'active_checkpoint_commit':'old','last_completed_writer_operation_finished':True,'read_only_next_case':{'PR':190}}
 contents={q:('foreign queue prefix\n'+base+'\nforeign queue suffix\n').encode(),m.PREFIX+'CURRENT_PROGRESS.json':json.dumps(progress).encode(),m.PREFIX+'CURRENT_PROGRESS.md':b'Dated earlier programme facts.\n',m.PREFIX+'RESEARCH_LOG.md':b'Dated programme log.\n','foreign/unrelated.txt':b'KEEP FOREIGN'}
 h.main=h.commit(h.tree(contents));h.commits[m.HEAD]={'tree':{'sha':h.tree({q:(original+'\n').encode()})},'parents':[]};h.commits[m.ORIGINAL_BASE]={'tree':{'sha':h.tree({q:(base+'\n').encode()})},'parents':[]};m._helpers=h
 m.final_scope();r=m.integration_prepare('merge_preparation_probe');return td,p,g,z,tr,h,r

def merged_fixture():
 td,p,g,z,tr,h,r=integration_fixture();h.main=r['commit'];h.pr.update(merged=True,state='closed');m.integration_accept();return td,p,g,z,tr,h,r

def positive_gate():
 td,p,*_=fixture()
 with td:m.gate();return 'Synthetic full gate including original16 and exact packet accepted.'
def gate_mutant(kind):
 td,p,g,z,tr=fixture()
 with td:
  if kind=='payload':(p/'packet/paper.tex').write_text('DRIFT')
  if kind=='proof':(p/'PROOF.md').write_text('DRIFT')
  if kind=='head':g['original_head']='f'*40;dump(p/'ROOT_PUBLICATION_GATE.json',g)
  if kind=='review_duplicate':g['whole_package_reviews'][1]['reviewer_id']=g['whole_package_reviews'][0]['reviewer_id'];dump(p/'ROOT_PUBLICATION_GATE.json',g)
  if kind=='review_bytes':dump(p/'review_1_report.json',{'disposition':'REPAIR_REQUIRED'})
  return rejects(m.gate)
def ambiguous_reviews():
 td,p,g,z,tr=fixture()
 with td:
  for r in g['whole_package_reviews']:
   for k in ['report','seal','root_authentication']:
    dump(p/r[k]['path'],{'disposition':'REPAIR_REQUIRED','remaining_repairs':7,'generation':99,'input_sha256':'bad'})
    r[k]={'path':r[k]['path'],**m.pin(p/r[k]['path'])}
  dump(p/'ROOT_PUBLICATION_GATE.json',g);m.gate();return 'CONFIRMED: contradictory/future review bodies accepted; only Root assertions and file pins checked.'

class Sheets:
 def __init__(self,z,mode='normal'):
  self.rows=[m.HEADER,['foreign problem','','10.5281/zenodo.77777777','KEEP FOREIGN']];self.z=z;self.mode=mode;self.appends=0;self.reads=0
 def __call__(self,resource,method,params,body=None):
  assert params['spreadsheetId']==m.SID
  if resource=='spreadsheet':return {'spreadsheetId':m.SID,'sheets':[{'properties':{'sheetId':m.GID,'title':m.TAB}}]}
  r=params['range']
  if method=='append':
   assert params['valueInputOption']=='RAW' and params['insertDataOption']=='INSERT_ROWS';self.appends+=1
   row=body['values'][0];self.rows.append(row);i=len(self.rows)
   if self.mode=='duplicate':self.rows.append(list(row))
   if self.mode=='foreign_loss':self.rows[1]=['CORRUPTED']
   if self.mode=='unknown':raise RuntimeError('Unknown append outcome')
   if self.mode=='unknown_no_effect':self.rows.pop();raise RuntimeError('Unknown append outcome')
   return {'updates':{'updatedRange':f"'Math Puzzles'!A{i}:D{i}",'updatedRows':1,'updatedColumns':4}}
  if r=="'Math Puzzles'!A1:D1":return {'values':[m.HEADER]}
  if r=="'Math Puzzles'!A:D":return {'values':copy.deepcopy(self.rows)}
  self.reads+=1;i=int(r.split('!A')[1].split(':')[0]);return {'values':[self.rows[i-1]]}

def tracker_case(mode):
 td,p,g,z,tr=fixture()
 with td:
  s=Sheets(z,mode)
  if mode in ['unknown','unknown_no_effect']:
   rejects(lambda:m.record_tracker(s),'Unknown append')
   if mode=='unknown_no_effect':rejects(lambda:m.record_tracker(s),'Unknown earlier append');assert s.appends==1;return 'Unconfirmed append with no visible row blocks second write.'
   s.mode='normal';m.record_tracker(s);assert s.appends==1;return 'Unknown successful append reconciled by existing DOI; one write total.'
  r=m.record_tracker(s);assert r['actual_fresh_reads']==2 and s.appends==1 and s.reads==2
  count=sum(any(z['doi'] in str(c) for c in row) for row in s.rows)
  if mode=='duplicate':assert count==2;return 'CONFIRMED: tracker accepted with two identical DOI rows after concurrent duplicate.'
  if mode=='foreign_loss':assert s.rows[1]==['CORRUPTED'];return 'CONFIRMED: tracker accepted after foreign row changed; only own row readbacks.'
  assert count==1;return 'Exactly one RAW append, two actual own-row reads.'

def integration_case(kind):
 td,p,g,z,tr,h,r=integration_fixture()
 with td:
  if kind=='positive':
   assert h.body_at('foreign/unrelated.txt',r['commit'])==b'KEEP FOREIGN';h.main=r['commit'];h.pr.update(merged=True,state='closed');a=m.integration_accept();return {'selected_count':a['selected_files'],'foreign_preserved':True,'parents':[x['sha'] for x in h.commits[r['commit']]['parents']]}
  target=m.CASE+'CURRENT_CASE_STATUS.json'
  h.main=h.altered(r['commit'],{target:b'WRONG CURRENT STATUS'}) if kind in ['current_drift','pruned_map'] else r['commit'];h.pr.update(merged=True,state='closed')
  if kind=='pruned_map':
   del r['selected_files'][target];dump(p/'SCOPED_MERGE_PREPARATION.json',r);a=m.integration_accept();return {'CONFIRMED':'Shrunk selected map allowed current MAIN drift while prepared tree intact','omitted':target,'accepted_selected':a['selected_files']}
  if kind=='head':h.pr['head']['sha']='f'*40
  if kind=='parents':h.commits[r['commit']]['parents'].reverse()
  return rejects(m.integration_accept)

def retry_case(factual=False):
 vals=merged_fixture() if factual else integration_fixture();td,p,g,z,tr,h,r=vals
 with td:
  if factual:
   h.advance_on_create=True;rejects(lambda:m.factual_prepare('factual_preparation_stale'),'MAIN advanced');first=m.read(p/'FINAL_FACTUAL_PREPARATION.json');r2=m.factual_prepare('factual_preparation_fresh');receipt='FINAL_FACTUAL_PREPARATION'
  else:
   h.advance_on_create=True;rejects(lambda:m.integration_prepare('merge_preparation_stale'),'MAIN advanced');first=m.read(p/'SCOPED_MERGE_PREPARATION.json');r2=m.integration_prepare('merge_preparation_fresh');receipt='SCOPED_MERGE_PREPARATION'
  assert first['commit']!=r2['commit'];assert h.body_at('foreign/new.txt',r2['commit'])==b'concurrent peer bytes'
  hist=p/'integration_preparation/receipt_history'/(receipt+'_'+first['commit']+'.json');assert hist.exists()
  return {'fresh_parent':r2['expected_main'],'abandoned_receipt_preserved':True,'gate_unchanged':m.pin(p/'ROOT_PUBLICATION_GATE.json')['sha256']==z['gate_sha256']}

def factual_case(kind):
 td,p,g,z,tr,h,merged=merged_fixture()
 with td:
  if kind=='before_drift':
   h.main=h.altered(h.main,{m.NATIVE+'verify.py':b'CORRUPTED'});return rejects(lambda:m.factual_prepare('factual_preparation_probe'),'Selected current MAIN identity drift')
  r=m.factual_prepare('factual_preparation_probe');h.main=r['commit']
  if kind=='after_drift':h.main=h.altered(h.main,{m.NATIVE+'verify.py':b'CORRUPTED'});return rejects(m.factual_accept,'Selected current MAIN identity drift')
  if kind=='pruned_merged_map':
   target=m.CASE+'METADATA_PROPOSAL.json';del merged['selected_files'][target];dump(p/'SCOPED_MERGE_PREPARATION.json',merged);h.main=h.altered(h.main,{target:b'CORRUPTED CONTROL'});a=m.factual_accept();return {'CONFIRMED':'Factual acceptance accepted changed merged-only control after receipt map pruning','omitted':target,'accepted':a['status']}
  a=m.factual_accept();j=json.loads(h.body_at(m.PREFIX+'CURRENT_PROGRESS.json',h.main));assert (j['fully_completed_count'],j['published_count'],j['last_completed_PR'],j['current_PR'],j['next_numeric_intake_cursor'])==(40,24,191,191,192)
  assert 'active_checkpoint_commit' not in j and 'read_only_next_case' not in j
  return {'accepted':a['status'],'census_current_next':[40,24,191,191,192],'stale_aliases_retired':True}

def native_actual_aliases():
 td,p,g,z,tr=fixture()
 with td:
  T=p/'actual_native_aliases';T.mkdir()
  source=CASE/'integration_preparation/native_template_pending_01'
  for n in sorted(m.JSON_FACTS|m.TEXT_FACTS|{'RESEARCH_LOG.md'}):
   (T/n).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source/n,T/n)
  g['native_text_status_replacements']={'README.md':'PUBLICATION.json contains dated assembly-time publication facts, pending until actual publication and repository acceptance.','review/REVIEW.md':'Those are pending at this dated assembly snapshot.'}
  m.native_status(T,g,z,tr,False)
  for n in m.JSON_FACTS:
   j=m.read(T/n)
   for k in ['whole_package_reviews_pending','publication_and_tracker_actions_not_yet_performed','paper_science_and_current_native_template_require_review','not_an_approval']:
    if k in j:assert j[k] is False,(n,k)
   if 'actual_DOI' in j:assert j['actual_DOI']==z['doi']
  m.native_status(T,g,z,tr,True)
  contradictions={n:('remains pending at this preparation.' in (T/n).read_text() and 'was actually accepted' in (T/n).read_text()) for n in m.TEXT_FACTS}
  assert all(contradictions.values())
  return {'json_live_aliases_updated':True,'CONFIRMED_current_text_retains_both_pending_and_accepted_merge_sentences':contradictions}

def zenodo_case(kind):
 td,p,g,z,tr=fixture()
 with td:
  h=Native();m._helpers=h;calls=[]
  def runner(args,**kw):
   cmd=args[6];calls.append(cmd)
   out={**z,'state':'ready_to_publish'}
   if kind=='stage_unknown' and cmd=='stage':return types.SimpleNamespace(returncode=1,stdout=b'unknown',stderr=b'')
   if kind=='stage_unknown' and cmd=='inspect':return types.SimpleNamespace(returncode=1,stdout=b'no saved state',stderr=b'')
   if kind=='publish_unknown' and cmd=='publish':return types.SimpleNamespace(returncode=1,stdout=b'unknown',stderr=b'')
   if kind=='already_published':out=dict(z)
   return types.SimpleNamespace(returncode=0,stdout=json.dumps(out).encode(),stderr=b'')
  if kind=='stage_unknown':
   rejects(lambda:m.run_zenodo('stage',runner=runner));rejects(lambda:m.run_zenodo('stage',runner=runner));assert calls==['stage','inspect'];return {'calls':calls,'duplicate_creation_prevented':True}
  dump(p/'ZENODO_STAGE_READBACK.json',{'id':z['id'],'gate_sha256':z['gate_sha256']})
  if kind=='publish_unknown':
   rejects(lambda:m.run_zenodo('publish',z['id'],runner));rejects(lambda:m.run_zenodo('publish',z['id'],runner));assert calls==['inspect','publish','inspect'];return {'calls':calls,'second_publish_prevented':True}
  m.run_zenodo('publish',z['id'],runner);assert calls==['inspect'];return {'calls':calls,'existing_published_reused':True}

def extra_case(kind):
 if kind in ['foreign_tree','queue_foreign_target','metadata_actual','gate_receipt_drift','native_code','native_inventory','protected_original','metadata_pinned','scope_private','scope_derivative','generator']:
  td,p,g,z,tr=fixture()
  with td:
   if kind=='foreign_tree':
    h=Native();h.main=h.commit(h.tree({'foreign/unrelated.txt':b'KEEP'}));h.drift_foreign_on_tree=True
    return rejects(lambda:m.prepare_tree(h,h.main,{'owned/proof.txt':p/'PROOF.md'},[h.main,m.HEAD],'test','test_receipt.json'),'Full-tree foreign scope drift')
   if kind=='queue_foreign_target':
    guard=json.loads((CASE/'ROOT_ORIGINAL_PARENT_AND_QUEUE_GUARD_01.json').read_text());orig=guard['rows'][1]['row'];base=guard['rows'][2]['row']
    return rejects(lambda:m.queue_update(base.replace('queued','foreign_edit'),orig,base,z['doi'],z['doi_url']),'Foreign target-row drift')
   if kind=='gate_receipt_drift':
    g['native_complete_template']='native_template_complete_drift';dump(p/'ROOT_PUBLICATION_GATE.json',g)
    return rejects(lambda:m.publication(m.gate()),'another gate')
   if kind=='protected_original':
    dump(p/'integration_preparation'/g['native_pending_template']/'ORIGINAL_SUBMISSION/original_00.txt','DRIFT')
    return rejects(m.gate,'Bound bytes drift')
   if kind=='metadata_pinned':dump(p/'METADATA_PROPOSAL.json',{'title':'WRONG'});return rejects(m.gate,'Bound bytes drift')
   if kind=='scope_private':return rejects(lambda:m.inside('lifecycle_private/state.json'),'Private/cache/raw')
   if kind=='scope_derivative':
    (p/'unapproved.png').write_bytes(b'fake rendered derivative');return rejects(lambda:m.approved_media(g,'unapproved.png'),'Unapproved body/derivative')
   if kind=='generator':
    spec=importlib.util.spec_from_file_location('independent_generator_guard',PROPOSAL/'protect_canonical_outputs.py');guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
    return rejects(lambda:guard.require_new_outputs(p,['lifecycle_common.py']),'Refuse overwriting')
   if kind=='metadata_actual':
    req=m.metadata_request();dump(p/'PR_METADATA_ACCEPTANCE.json',{'status':'ACTUAL_ORIGINAL_HEAD_METADATA_AND_READY_STATE_ACCEPTED','PR':191,'original_head':m.HEAD,'gate_sha256':z['gate_sha256'],'request_sha256':m.pin(p/'PR_METADATA_REQUEST.json')['sha256']})
    return rejects(lambda:m.require_metadata(g,z,tr,{'title':'OTHER','body':req['request']['body']}),'Actual PR metadata')
   m.prepare_native(False);cur=m.read(p/'integration_preparation/CURRENT_TEMPLATE.json');T=p/'integration_preparation'/cur['current_template']
   if kind=='native_inventory':dump(T/'unexpected.txt','extra');return rejects(lambda:m.current_native(g,False),'inventory')
   dump(T/'verify.py','CORRUPTED');cur['files']['verify.py']=m.pin(T/'verify.py');dump(p/'integration_preparation/CURRENT_TEMPLATE.json',cur)
   return rejects(lambda:m.current_native(g,False),'Bound bytes drift')
 if kind=='merged_forged_foreign_receipt':
  td,p,g,z,tr,h,r=integration_fixture()
  with td:
   oldtree=r['tree'];t=h.ident();h.trees[t]=dict(h.trees[oldtree]);h.trees[t]['foreign/unrelated.txt']=h.store(b'LOST FOREIGN')
   r['commit']=h.commit(t,[r['expected_main'],m.HEAD]);r['tree']=t;r['parent_tree']=t;r['changed_paths']=[]
   dump(p/'SCOPED_MERGE_PREPARATION.json',r);h.main=r['commit'];h.pr.update(merged=True,state='closed');a=m.integration_accept()
   return {'CONFIRMED':'Acceptance does not bind parent_tree to expected_main tree or derive changed_paths from selected map','accepted':a['status'],'foreign_at_prepared':h.body_at('foreign/unrelated.txt',r['commit']).decode()}
 raise AssertionError(kind)

for kind in ['foreign_tree','queue_foreign_target','metadata_actual','gate_receipt_drift','native_code','native_inventory','protected_original','metadata_pinned','scope_private','scope_derivative','generator','merged_forged_foreign_receipt']:check('extra_'+kind,lambda k=kind:extra_case(k),'confirm gap' if kind=='merged_forged_foreign_receipt' else 'pass')

check('gate_full_positive',positive_gate)
for kind in ['payload','proof','head','review_duplicate','review_bytes']:check('gate_reject_'+kind,lambda k=kind:gate_mutant(k))
check('review_bodies_contradict_gate_accepted',ambiguous_reviews,'confirm limitation')
for mode in ['normal','duplicate','foreign_loss','unknown','unknown_no_effect']:check('tracker_'+mode,lambda k=mode:tracker_case(k),'confirm gap' if mode in ['duplicate','foreign_loss'] else 'pass')
for kind in ['positive','current_drift','head','parents','pruned_map']:check('integration_'+kind,lambda k=kind:integration_case(k),'confirm gap' if kind=='pruned_map' else 'pass')
check('stale_merge_retry',lambda:retry_case(False));check('stale_factual_retry',lambda:retry_case(True))
for kind in ['positive','before_drift','after_drift','pruned_merged_map']:check('factual_'+kind,lambda k=kind:factual_case(k),'confirm gap' if kind=='pruned_merged_map' else 'pass')
check('actual_native_factual_aliases',native_actual_aliases,'confirm text ambiguity')
for kind in ['stage_unknown','publish_unknown','already_published']:check('zenodo_'+kind,lambda k=kind:zenodo_case(k))
summary={'schema':'independent-offline-lifecycle-probes/v1','proposal_common_sha256':hashlib.sha256((PROPOSAL/'lifecycle_common.py').read_bytes()).hexdigest(),'live_process_calls':0,'live_network_calls':0,'native_helper_imports':0,'author_selftest_imports':0,'tests':RESULTS,'counts':{'total':len(RESULTS),'completed':sum(r['outcome']=='PASS' for r in RESULTS),'unexpected_failures':sum(r['outcome']!='PASS' for r in RESULTS)}}
(OWN/'INDEPENDENT_PROBE_RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
sys.exit(bool(summary['counts']['unexpected_failures']))
