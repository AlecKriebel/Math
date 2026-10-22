#!/usr/bin/env python3
"""Independent offline controls of actual proposed helper functions.
Every service/Git response is an explicit fixture, never an actual production
receipt. Filesystem/SQLite/locking/atomic replacement are real in private scratch.
The suite must itself run in actual separate normal/-O/-OO Python processes.
"""
import sys
if not(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('Use -I -S -B')
import argparse,contextlib,copy,hashlib,io,json,os,shutil,sqlite3,stat,tempfile,subprocess
from pathlib import Path
from datetime import datetime,timezone
OWN=Path(__file__).resolve().parent;P=OWN.parents[2];SOURCE=P/'close_pr967.py';AUDIT=P/'audits/pr967_2616'
def sha(x):return hashlib.sha256(x).hexdigest()
def enc(x):return (json.dumps(x,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()
def need(ok,m):
 if not ok:raise RuntimeError(m)
p=argparse.ArgumentParser();p.add_argument('--core-sha256',required=True);p.add_argument('--wrapper-sha256',required=True);args=p.parse_args()
raw=SOURCE.read_bytes();wrapper=(P/'finalize_pr967_and_gate_next.py').read_bytes()
need(sha(raw)==args.core_sha256 and sha(wrapper)==args.wrapper_sha256,'external proposed helper pins')
records_raw=(AUDIT/'ORIGINAL_FILE_RECORDS.json').read_bytes();records=json.loads(records_raw)['files']
original_raw={name:(AUDIT/'original'/name).read_bytes() for name in records}
private=(AUDIT/'source_record_private.txt').read_bytes();private_obj=json.loads(private)
EVENTS=[];SERVICE=[];GIT=[]
import atexit
DONE=[False]
@atexit.register
def partial_results():
 if not DONE[0]:print(json.dumps({'status':'INCOMPLETE_OFFLINE_SUITE_NO_CREDIT','outer_optimization':sys.flags.optimize,'events':EVENTS,'event_count':len(EVENTS)},sort_keys=True))
def yes(name,fn):
 try:fn()
 except Exception as e:raise RuntimeError('POSITIVE '+name+' rejected: '+repr(e)) from e
 EVENTS.append({'test':name,'status':'PASS'})
def no(name,fn):
 try:fn()
 except (RuntimeError,ValueError,TypeError,KeyError,FileNotFoundError,OSError,sqlite3.Error) as e:EVENTS.append({'test':name,'status':'REJECTED_EXPECTED','guard':str(e)})
 else:raise RuntimeError('ADVERSE '+name+' accepted')
(OWN/'private_tmp').mkdir(mode=0o700,exist_ok=True)
with tempfile.TemporaryDirectory(prefix='offline-',dir=OWN/'private_tmp') as td:
 root=Path(td);effort=root/'effort';audit=effort/'audits/pr967_2616';runtime=audit/'closure_runtime'
 audit.mkdir(parents=True);runtime.mkdir(mode=0o700)
 n={'__name__':'_actual_proposed_functions_offline_','__file__':str(SOURCE)}
 exec(compile(raw,str(SOURCE),'exec',dont_inherit=True,optimize=sys.flags.optimize),n)
 n.update(ROOT=root,P=effort,A=audit,W=runtime)
 n['now']=lambda:'2026-10-16T22:00:04+00:00'
 for name,body in [('close_pr967.py',raw),('finalize_pr967_and_gate_next.py',wrapper)]: (effort/name).write_bytes(body)
 (audit/'ORIGINAL_FILE_RECORDS.json').write_bytes(records_raw)
 for name,body in original_raw.items():
  target=audit/'original'/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(body);target.chmod(0o644)
 (audit/'source_record_private.txt').write_bytes(private)
 cache=root/'unsolved_math_prioritization/cache';cache.mkdir(parents=True);db=cache/'catalog.sqlite'
 def rebuild(problem=None,prior=None,default=True):
  if db.exists():db.unlink()
  problem=private_obj['problem'] if problem is None else problem
  prior=private_obj['prior_research'] if default else prior
  with sqlite3.connect(db) as c:
   c.execute('CREATE TABLE records (key TEXT,payload TEXT,report TEXT)');c.execute('INSERT INTO records VALUES(?,?,?)',(n['KEY'],json.dumps(problem),json.dumps(prior)))
 rebuild()
 queue=b'UNRELATED QUEUE HEADER\n| 1038 | 2616 / KOU-21.107 | problem | x | x | x | x | claimed_solved | 1/5 |  | findings |  |\nOTHER ROW\n'
 parent='a'*40;blobs={n['QUEUE']:queue,n['STATE']:b'{"unrelated":{"spelling" : [1, 2]}}\n',n['HISTORY']:b'{"id":"unrelated","note":"keep exact"}\n',n['CATALOG']:enc([{'id':2616,'present':True,'holds':[],'statement_hash':n['STATEMENT'],'review_hash':n['REVIEW']}]),n['RELATED']:enc({'groups':[]})}
 git_modes={name:'100644' for name in records}
 git_bytes=dict(original_raw)
 def git(*a,raw=False,input=None):
  GIT.append(list(a))
  if a[:2]==('ls-tree','-r'):
   return b''.join((git_modes[name]+' blob '+record['git_blob']).encode()+b'\t'+name.encode()+b'\0' for name,record in records.items())
  if a[:2]==('cat-file','blob'):
   return git_bytes[next(name for name,v in records.items() if v['git_blob']==a[2])]
  if a[0]=='show':return blobs[a[1].split(':',1)[1]]
  if a[:2]==('remote','get-url'):return 'https://github.com/AlecKriebel/Math.git\n'
  if a[0]=='ls-remote':return parent+'\trefs/heads/main\n'
  if a[:2]==('cat-file','-e'):return ''
  if a[:2]==('symbolic-ref','--short'):return 'main\n'
  raise RuntimeError('FORBIDDEN/unexpected fixture Git call '+repr(a))
 n['git']=git
 WHO={'id':17,'login':'synthetic-root-actor','node_id':'SYNTHETIC_ACTOR_17'}
 CFG={};comment_values=[];event_values=[]
 def rest(number):
  state=CFG.get('state','open');merged=CFG.get('merged',False)
  return {'number':number,'state':state,'draft':CFG.get('draft',True),'head':{'sha':CFG.get('head',n['HEAD'] if number==967 else 'b'*40),'ref':'fixture-branch','repo':{'full_name':CFG.get('head_repo',n['REPO']),'owner':{'login':CFG.get('head_owner','AlecKriebel')}}},'base':{'sha':parent,'ref':CFG.get('base_ref','main'),'repo':{'full_name':CFG.get('base_repo',n['REPO']),'owner':{'login':CFG.get('base_owner','AlecKriebel')}}},'html_url':f'https://github.com/{n["REPO"]}/pull/{number}','node_id':'SYNTHETIC_PR_'+str(number),'merged_at':'2026-10-16T22:00:01Z' if merged else None,'closed_at':'2026-10-16T22:00:01Z' if state=='closed' else None}
 def node(number):
  x=rest(number);return {'number':number,'state':'MERGED' if x['merged_at'] else 'CLOSED' if x['state']=='closed' else 'OPEN','isDraft':x['draft'],'headRefOid':x['head']['sha'],'headRefName':x['head']['ref'],'baseRefName':x['base']['ref'],'url':x['html_url'],'mergedAt':x['merged_at'],'closedAt':x['closed_at'],'baseRef':{'name':x['base']['ref'],'target':{'oid':CFG.get('live_base',parent)}}}
 def api(method,endpoint,payload=None):
  SERVICE.append({'method':method,'endpoint':endpoint,'fixture_only':True})
  stamp='2026-10-16T22:00:03+00:00'
  if endpoint=='graphql':
   variables=payload['variables'];query=payload['query']
   if 'expr' in variables:
    q=CFG.get('queue',queue);obj={'oid':hashlib.sha1(b'blob '+str(len(q)).encode()+b'\0'+q).hexdigest(),'byteSize':len(q),'isBinary':False,'text':q.decode()}
    if CFG.get('bad_blob'):obj['oid']='f'*40
    return {'data':{'repository':{'object':obj}}},stamp
   number=variables['number'];v=node(number)
   if 'files(first' in query:
    paths=CFG.get('paths',list(records)+[n['QUEUE']])
    if number!=967:paths=[n['QUEUE'],'unsolved_math_prioritization/attempts/9999/FIXTURE.md']
    if CFG.get('duplicate_path'):paths=paths+[paths[0]]
    page=0 if variables.get('cursor') is None else int(variables['cursor']);chunk=paths[page*100:(page+1)*100]
    v.update(changedFiles=CFG.get('changed_count',len(paths)),files={'nodes':[{'path':x} for x in chunk],'pageInfo':{'hasNextPage':len(paths)>(page+1)*100,'endCursor':str(page+1)}})
    if CFG.get('page_base_drift'):v['baseRef']['target']['oid']='f'*40
   if CFG.get('bad_node_type'):v['isDraft']=1
   return {'data':{'repository':{'nameWithOwner':n['REPO'],'pullRequest':v}}},stamp
  if endpoint=='user':return copy.deepcopy(CFG.get('actor',WHO)),'2026-10-16T22:00:00+00:00'
  if endpoint.startswith('repos/'+n['REPO']+'/pulls/'):
   number=int(endpoint.rsplit('/',1)[1])
   if method=='GET':return rest(number),stamp
   if method=='PATCH':
    need(payload=={'state':'closed'},'fixture PATCH shape');CFG['state']='closed';event_values.append({'id':2001,'event':'closed','created_at':'2026-10-16T22:00:01Z','actor':copy.deepcopy(WHO)})
    if CFG.get('close_race'):CFG.update(CFG['close_race'])
    if CFG.get('lost_close_response'):raise RuntimeError('SYNTHETIC_LOST_CLOSE_RESPONSE')
    return rest(number),stamp
  if '/comments?per_page=100&page=' in endpoint:
   page=int(endpoint.rsplit('=',1)[1]);return copy.deepcopy(comment_values[(page-1)*100:page*100]),stamp
  if '/events?per_page=100&page=' in endpoint:
   page=int(endpoint.rsplit('=',1)[1]);return copy.deepcopy(event_values[(page-1)*100:page*100]),stamp
  if endpoint==f'repos/{n["REPO"]}/issues/967/comments' and method=='POST':
   cid=1001;comment_values.append({'id':cid,'body':payload['body'],'user':copy.deepcopy(WHO),'created_at':'2026-10-16T22:00:01Z','updated_at':'2026-10-16T22:00:01Z','html_url':f'https://github.com/{n["REPO"]}/pull/967#issuecomment-{cid}','issue_url':f'https://api.github.com/repos/{n["REPO"]}/issues/967'})
   if CFG.get('post_race'):CFG.update(CFG['post_race'])
   if CFG.get('lost_post_response'):raise RuntimeError('SYNTHETIC_LOST_POST_RESPONSE')
   return copy.deepcopy(comment_values[-1]),stamp
  if '/issues/comments/' in endpoint:return copy.deepcopy(next(x for x in comment_values if x['id']==int(endpoint.rsplit('/',1)[1]))),stamp
  raise RuntimeError('FORBIDDEN/unexpected fixture API call '+method+' '+endpoint)
 original_api=n['api'];n['api']=api
 def reset_runtime():
  for x in runtime.iterdir():
   if x.is_file():x.unlink()
  CFG.clear();comment_values.clear();event_values.clear();SERVICE.clear()
 # Real parsing primitives and actual local filesystem adverse controls.
 no('duplicate_JSON_keys',lambda:n['strict']('{"a":1,"a":2}'))
 no('boolean_fingerprint_size',lambda:n['fingerprint']({'bytes':True,'sha256':'a'*64}))
 scratch=runtime/'fifo';os.mkfifo(scratch);no('FIFO_rejected_before_read',lambda:n['read'](scratch));scratch.unlink()
 scratch=runtime/'symlink';scratch.symlink_to(audit/'ORIGINAL_FILE_RECORDS.json');no('symlink_input_rejected',lambda:n['read'](scratch));scratch.unlink()
 original_run=n['run'];n['run']=lambda *a,**k:b'HTTP/2 200 OK\r\nDate: Fri, 16 Oct 2026 22:00:00 GMT\r\n\r\n{"ok":true}'
 yes('actual_API_include_header_Date_parser',lambda:n['need'](original_api('GET','SYNTHETIC')[0]=={'ok':True},'API parser'))
 n['run']=lambda *a,**k:b'HTTP/2 403 Forbidden\r\nDate: Fri, 16 Oct 2026 22:00:00 GMT\r\n\r\n{}';no('actual_API_permission_uncertainty_rejected',lambda:original_api('GET','SYNTHETIC'))
 n['run']=lambda *a,**k:b'HTTP/2 200 OK\r\nDate: Fri, 16 Oct 2026 22:00:00 GMT\r\nDate: Fri, 16 Oct 2026 22:00:00 GMT\r\n\r\n{}';no('actual_API_ambiguous_server_Date_rejected',lambda:original_api('GET','SYNTHETIC'));n['run']=original_run
 saved_git=n['git'];fetches=[]
 def missing_object_git(*a,**kwargs):
  if a[:2]==('cat-file','-e'):raise subprocess.CalledProcessError(1,['SYNTHETIC_ONLY'])
  if a[0]=='fetch':fetches.append(a);return ''
  return saved_git(*a,**kwargs)
 n['git']=missing_object_git;yes('exact_SHA_object_only_fetch_contract',n['remote_main']);n['git']=saved_git
 need(len(fetches)==1 and fetches[0]==('fetch','--no-auto-maintenance','--no-write-fetch-head','--no-tags','--no-recurse-submodules','--no-prune','origin',parent),'fetch mutated ref/config contract')
 # Actual source/original functions and all26 byte/mode variants.
 yes('actual_original26_Git_disk_inventory',n['originals'])
 for name in records:
  target=audit/'original'/name;body=target.read_bytes();target.write_bytes(body+b'X');no('original_disk_byte_'+name, n['originals']);target.write_bytes(body)
  target.chmod(0o600);no('original_disk_mode_'+name,n['originals']);target.chmod(0o644)
  same=[x for x in records if records[x]['git_blob']==records[name]['git_blob']]
  for x in same:git_bytes[x]=body+b'X'
  no('original_Git_byte_'+name,n['originals'])
  for x in same:git_bytes[x]=body
  git_modes[name]='100755';no('original_Git_mode_'+name,n['originals']);git_modes[name]='100644'
 yes('source_actual_prior_is_empty_object',lambda:n['source_gate'](parent))
 rebuild(prior={'inert':1},default=False);no('source_changed_nonempty_prior_rejected',lambda:n['source_gate'](parent));rebuild()
 rebuild(prior=None,default=False);no('source_null_prior_rejected',lambda:n['source_gate'](parent));rebuild()
 old=blobs[n['CATALOG']];v=json.loads(old);v[0]['holds']=['fixturehold'];blobs[n['CATALOG']]=enc(v);no('source_current_hold_rejected',lambda:n['source_gate'](parent));blobs[n['CATALOG']]=old
 old=blobs[n['RELATED']];blobs[n['RELATED']]=enc({'groups':[{'ids':[2616]}]});no('source_related_membership_rejected',lambda:n['source_gate'](parent));blobs[n['RELATED']]=old
 source_path=audit/'source_record_private.txt';source_path.write_bytes(private+b' ');no('source_private_hash_rejected',lambda:n['source_gate'](parent));source_path.write_bytes(private)
 # True metadata, complete filename and immutable QUEUE machinery under fixtures.
 yes('selected_exact_status_head_base_fullpath',lambda:n['need'](n['status_gate']()['action']=='ELIGIBLE','selected action'))
 for key,value,label in [('head','c'*40,'changed_head'),('head_repo','someone/fork','head_fork'),('head_owner','someone','head_owner'),('base_ref','other','base_branch'),('base_repo','someone/fork','base_fork'),('page_base_drift',True,'livebase_page_drift'),('duplicate_path',True,'duplicate_path'),('changed_count',28,'incomplete_paths'),('bad_blob',True,'immutable_blob_oid'),('bad_node_type',True,'malformed_bool')]:
  CFG[key]=value;no('gate_'+label,n['status_gate']);CFG.clear()
 CFG['paths']=list(records)+[n['QUEUE'],'foreign/path'];no('gate_foreign_fullpath',n['status_gate']);CFG.clear()
 CFG['queue']=queue.replace(b'claimed_solved',b'unsolved');yes('other_status_skip_before_any_source_intake',lambda:n['need'](n['status_gate']()['action']=='SKIP_STATUS_ONLY','skip'));CFG.clear()
 CFG['queue']=queue+queue;no('gate_ambiguous_queue_row',n['status_gate']);CFG.clear()
 CFG['queue']=queue.replace(b'1/5',b'2/5');no('gate_changed_declared_turns',n['status_gate']);CFG.clear()
 for change in [('draft',False),('state','closed'),('merged',True)]:
  CFG[change[0]]=change[1]
  if change[0]=='merged':CFG['state']='closed'
  yes('metadata_only_skip_'+change[0],lambda:n['need'](n['status_gate']()['action']=='SKIP_NOT_OPEN_DRAFT','skip'));CFG.clear()
 CFG['queue']=queue.replace(b'2616 /',b'9999 /');yes('actual_next_gate_filename_id_queue_only',lambda:n['need'](n['status_gate'](968,key=None,expected_head=None)['action']=='ELIGIBLE','next eligible'));CFG.clear()
 CFG['queue']=queue.replace(b'2616 /',b'9999 /').replace(b'claimed_solved',b'unsolved');yes('actual_next_otherstatus_skips',lambda:n['need'](n['status_gate'](968,key=None,expected_head=None)['action']=='SKIP_STATUS_ONLY','next skip'));CFG.clear()
 CFG['paths']=[n['QUEUE']]+['unsolved_math_prioritization/attempts/2616/F'+str(i)+'.md' for i in range(129)]
 yes('actual_full_filename_two_page_connection',lambda:n['need'](n['changed_paths'](n['metadata'](967)[0])['count']==130,'full filename pages'));CFG.clear()
 # Synthetic complete root records, not real scientific decisions or receipts.
 ops={'schema':'pr967-closure-operations-v1','pr':967,'problem_id':'2616','original_pr_head':n['HEAD'],'files':{(effort/x).relative_to(root).as_posix():n['pin']((effort/x).read_bytes()) for x in n['HELPERS']}}
 opsraw=enc(ops);(audit/'CLOSURE_OPERATIONS_INVENTORY.json').write_bytes(opsraw);context=n['inventory'](sha(opsraw))
 E={}
 def evidence(path,value):
  path.parent.mkdir(parents=True,exist_ok=True);body=value if type(value) is bytes else enc(value);path.write_bytes(body);rel=path.relative_to(root).as_posix();E[rel]=n['pin'](body);return {'path':rel,'sha256':sha(body)}
 allfamilies={};allfindings={};auths={}
 n['FINDING_COUNTS']={f:1 for f in n['FAMILIES']} # Synthetic-only catalog sizes.
 for i,f in enumerate(sorted(n['FAMILIES'])):
  folder=audit/'reviews'/f;folder.mkdir(parents=True)
  find=evidence(folder/'FINDINGS.json',{'schema':'SYNTHETIC_ONLY','id':'SYNTHETIC-'+f})
  member={'FINDINGS.json':E[find['path']]};af='explicit_allowlist' if f=='exact_priority_falsifier_01' else 'explicit_public_allowlist'
  manifest=evidence(folder/'MANIFEST.json',{'files':member,af:['FINDINGS.json']})
  if f=='priority_recent_01':n['RECENT_SEAL']=manifest['sha256'] # Test-only repin, no production-source edit.
  source=evidence(audit/('SOURCE_AUTH_'+f+'.json'),{'utc':'2026-10-16T20:00:00+00:00','before_substantive_intake':True,'external_manifest_sha256':manifest['sha256'],'files':1,'bytes':member['FINDINGS.json']['bytes'],'all_members_authenticated':True})
  intake=evidence(audit/('INTAKE_'+f+'.json'),{'utc':'2026-10-16T20:30:00+00:00','schema':'SYNTHETIC_ONLY'})
  auths[f]={'status':'PASS_BYTES_BEFORE_FULL_REPORT_INTAKE','manifest_path':manifest['path'],'manifest_sha256':manifest['sha256'],'manifest_allowlist_field':af,'file_count':1,'total_bytes':member['FINDINGS.json']['bytes'],'root_authentication_path':source['path'],'root_authentication_sha256':source['sha256'],'root_authentication_utc':'2026-10-16T20:00:00+00:00','root_authentication_entry_path':[],'source_manifest_pin_field':'external_manifest_sha256','source_count_field':'files','source_bytes_field':'bytes','source_all_members_field':'all_members_authenticated','full_intake_path':intake['path'],'full_intake_sha256':intake['sha256'],'full_intake_utc':'2026-10-16T20:30:00+00:00','authenticated_before_substantive_intake':True,'historical_root_record_schema_preserved':True}
  allfamilies[f]={'manifest':manifest}
  allfindings[f]=[{'id':'SYNTHETIC-'+f,'identifier_origin':'root_canonical_index_of_narrative_finding_not_an_original_family_id','source':'FINDINGS.json/fixture section','finding':'SYNTHETIC ONLY','disposition':'SYNTHETIC_EXPLICIT_ONLY','resolution':'No scientific credit; exercising exact individual catalog closure.'}]
 norm=evidence(audit/'SYNTHETIC_NORMALIZED.json',{'schema':'pr967-normalized-family-authentications-v1','normalization_utc':'2026-10-16T21:00:00+00:00','pr':967,'problem_id':'2616','original_head':n['HEAD'],'normalization_is_retrospective':True,'families':auths})
 for f in allfamilies:allfamilies[f]['authentication']=norm
 ready_evidence=evidence(audit/'SYNTHETIC_EVIDENCE.json',{'schema':'SYNTHETIC_ONLY_NO_REAL_SOURCE_PROOF_OR_PRIORITY_CREDIT'})
 names=['source_identity','whole_proof','actual_reproduction','classical_priority_intake','recent_priority_intake','exact_priority_falsification','historical_date_qualification','finding_dispositions']
 ready=evidence(audit/'SYNTHETIC_READINESS.json',{'schema':'pr967-root-closure-readiness-v1','utc':'2026-10-16T21:01:00+00:00','pr':967,'problem_id':'2616','original_pr_head':n['HEAD'],'checks':{x:{'status':'PASS','observed_utc':'2026-10-16T21:00:00+00:00','evidence':[ready_evidence]} for x in names}})
 body='SYNTHETIC TEST ONLY; NO ACTUAL CLOSURE AUTHORITY\n'+n['MARKER']+'\n';(audit/'CLOSURE_COMMENT_DRAFT.md').write_text(body)
 authorization={'schema':'pr967-root-operation-authorization-v1','utc':'2026-10-16T21:01:00+00:00','root_issued':True,'pr':967,'problem_id':'2616','original_pr_head':n['HEAD'],'operations_inventory_sha256':context['inventory_sha256'],'closure_comment_sha256':sha(body.encode()),'operation_nonce':'d'*64,'actor':WHO,'allowed_operations':['comment','close','finalize']}
 ar=evidence(audit/'SYNTHETIC_AUTHORIZATION.json',authorization)
 fr=evidence(audit/'SYNTHETIC_FINDINGS.json',{'schema':'pr967-root-individual-family-findings-v1','utc':'2026-10-16T21:00:00+00:00','pr':967,'problem_id':'2616','original_head':n['HEAD'],'families':allfindings,'all_ids_unique':True,'required_mathematical_repairs_remaining':[],'priority_outcome':'SYNTHETIC_ONLY','external_action_authority':False,'no_new_author_proof_responses':True})
 d={'schema':'pr967-priority-closure-decision-v1','utc':'2026-10-16T21:02:00+00:00','pr':967,'problem_id':'2616','original_pr_head':n['HEAD'],'disposition':'CLOSE_WITHOUT_MERGE_ESTABLISHED_PRIORITY','operations_inventory_sha256':context['inventory_sha256'],'closure_comment_sha256':sha(body.encode()),'proposed_comment_sha256':sha(body.encode()),'families':allfamilies,'evidence_files':E,'readiness':ready,'operation_authorization':ar,'finding_dispositions':fr,'reason':'mathematically_correct_rediscovery','scope':{'original_declared_turns':'1/5','historical_native_turn_count':'UNKNOWN','new_author_proof_responses':0,'proof_search_turns_added_by_audit':0,'no_ultimate_discovery_or_misconduct_adjudication':True,'strict_historical_linked_body_hash_available':False,'strict_historical_linked_body_hash_qualification_retained':True,'credit_alone_restores_original_target_novelty':False},'historical_evidence':{'status':'NOT_AVAILABLE_QUALIFIED','original_qualification':ready_evidence,'archival_addendum':None}}
 def decision():
  (audit/'PRIORITY_DISPOSITION.json').write_bytes(enc(d));return sha(enc(d))
 dp=decision();bound=n['authority'](dp,context,body,authorization)
 yes('synthetic_complete_prerequisite_schema',lambda:n['prerequisites'](dp,context))
 no('decision_external_pin_required',lambda:n['prerequisites']('0'*64,context))
 (audit/'CLOSURE_COMMENT_DRAFT.md').write_text(body+'X');no('comment_exact_review_pin_required',lambda:n['prerequisites'](dp,context));(audit/'CLOSURE_COMMENT_DRAFT.md').write_text(body)
 saved=copy.deepcopy(d)
 d['families'].pop(sorted(n['FAMILIES'])[0]);bad=decision();no('all_six_family_seals_required',lambda:n['prerequisites'](bad,context));d=copy.deepcopy(saved);dp=decision()
 # Independently mutate actual family bytes/allowlist/unsafe members/root-auth chronology.
 fam=sorted(n['FAMILIES'])[0];folder=audit/'reviews'/fam;manifest_path=folder/'MANIFEST.json';manifest_raw=manifest_path.read_bytes()
 manifest_path.write_bytes(manifest_raw+b' ');no('family_seal_byte_drift',lambda:n['prerequisites'](dp,context));manifest_path.write_bytes(manifest_raw)
 m=json.loads(manifest_raw);m['explicit_public_allowlist']*=2;manifest_path.write_bytes(enc(m));E[manifest_path.relative_to(root).as_posix()]=n['pin'](enc(m));d['families'][fam]['manifest']['sha256']=sha(enc(m));bad=decision();no('family_duplicate_allowlist_even_repinned',lambda:n['prerequisites'](bad,context))
 manifest_path.write_bytes(manifest_raw);d=copy.deepcopy(saved);E=d['evidence_files'];dp=decision()
 m=json.loads(manifest_raw);m['files']['../escape']={'bytes':1,'sha256':'f'*64};m['explicit_public_allowlist'].append('../escape');manifest_path.write_bytes(enc(m));d['evidence_files'][manifest_path.relative_to(root).as_posix()]=n['pin'](enc(m));d['families'][fam]['manifest']['sha256']=sha(enc(m));bad=decision();no('family_unsafe_member_even_repinned',lambda:n['prerequisites'](bad,context))
 manifest_path.write_bytes(manifest_raw);d=copy.deepcopy(saved);E=d['evidence_files'];dp=decision()
 authpath=root/d['families'][fam]['authentication']['path'];authraw=authpath.read_bytes();v=json.loads(authraw);v['normalization_utc']='2026-10-16T19:00:00+00:00';authpath.write_bytes(enc(v));d['evidence_files'][authpath.relative_to(root).as_posix()]=n['pin'](enc(v));d['families'][fam]['authentication']['sha256']=sha(enc(v));bad=decision();no('no_backdated_normalization_even_repinned',lambda:n['prerequisites'](bad,context));authpath.write_bytes(authraw);d=copy.deepcopy(saved);E=d['evidence_files'];dp=decision()
 yes('actual_functions_full_synthetic_preflight',lambda:n['preflight'](dp,context))
 # Independent approval interface fixture, not a scientific or real review.
 review=audit/'reviews/SYNTHETIC_CLOSURE_REVIEW';review.mkdir()
 rpins={'decision_sha256':dp,'operations_inventory_sha256':context['inventory_sha256'],'closure_comment_sha256':sha(body.encode())}
 result={'pr':967,'problem_id':'2616','original_pr_head':n['HEAD'],**rpins,'reviewer_agent_id':'SYNTHETIC_REVIEWER_ONLY','started_utc':'2026-10-16T21:03:00+00:00','completed_utc':'2026-10-16T21:04:00+00:00','clean_context':True,'entire_closure_package_review':True,'full_reproducer_completed':True,'clean_for_closure':True,'required_issues':[],'optional_issues':[]}
 docs={'RESULT.json':result,'AUTHENTICATION_START.json':{'status':'PASS','utc':'2026-10-16T21:03:10+00:00',**rpins,'all26_original_bytes_and_modes_authenticated':True,'all_six_family_members_authenticated':True,'both_entire_helpers_authenticated':True},'AUTHENTICATION_END.json':{'status':'PASS','utc':'2026-10-16T21:03:50+00:00',**rpins,'all26_original_bytes_and_modes_authenticated':True,'all_six_family_members_authenticated':True,'both_entire_helpers_authenticated':True},'FULL_AUDIT.md':b'SYNTHETIC ONLY NO ACTUAL REVIEW CREDIT\n','RESEARCH_LOG.md':b'SYNTHETIC ONLY\n'}
 for name,value in docs.items():(review/name).write_bytes(value if type(value) is bytes else enc(value))
 rm={'files':{name:n['pin']((review/name).read_bytes()) for name in docs},'explicit_public_allowlist':list(docs)};rmb=enc(rm);(review/'MANIFEST.json').write_bytes(rmb)
 ra={'utc':'2026-10-16T21:05:00+00:00','before_substantive_intake':True,'all_members_authenticated':True,'external_manifest_sha256':sha(rmb)};(audit/'SYNTHETIC_REVIEW_ROOT_AUTH.json').write_bytes(enc(ra))
 approval={'schema':'pr967-root-closure-package-approval-v1','utc':'2026-10-16T21:06:00+00:00','root_issued':True,'pr':967,'problem_id':'2616','original_pr_head':n['HEAD'],**rpins,'reviewer_agent_id':'SYNTHETIC_REVIEWER_ONLY','status':'PASS_ENTIRE_CURRENT_CLOSURE_PACKAGE','review_manifest':{'path':(review/'MANIFEST.json').relative_to(root).as_posix(),**n['pin'](rmb)},'root_authentication':{'path':(audit/'SYNTHETIC_REVIEW_ROOT_AUTH.json').relative_to(root).as_posix(),**n['pin'](enc(ra))}}
 (audit/'CLOSURE_PACKAGE_APPROVAL.json').write_bytes(enc(approval));ap=sha(enc(approval));bound=n['authority'](dp,context,body,authorization,ap)
 yes('synthetic_entire_closure_approval_required',lambda:n['package_approval'](ap,dp,context,body,authorization))
 no('missing_external_closure_approval_rejected',lambda:n['package_approval'](None,dp,context,body,authorization))
 # Production close orchestration under explicit service fixtures, no real API.
 def invoke(execute=True):
  with contextlib.redirect_stdout(io.StringIO()):n['close_operation'](argparse.Namespace(disposition_sha256=dp,approval_sha256=ap,execute=execute),context)
 reset_runtime();yes('default_readonly_has_no_service_mutation',lambda:invoke(False));need(not any(x['method'] in ('PATCH',) or (x['method']=='POST' and x['endpoint']!='graphql') for x in SERVICE),'default mutated')
 reset_runtime();CFG['actor']={'id':99,'login':'foreign','node_id':'FOREIGN'};no('actor_mismatch_blocks_all_writes',invoke);need(not any(x['method']=='PATCH' or (x['method']=='POST' and x['endpoint']!='graphql') for x in SERVICE),'actor rejection mutated')
 for change,label in [({'head':'c'*40},'head'),({'draft':False},'draft'),({'live_base':'f'*40},'live_main_base'),({'queue':queue.replace(b'claimed_solved',b'unsolved')},'literal_status')]:
  reset_runtime();CFG['post_race']=change;no('post_request_observed_'+label+'_stops_before_close',invoke);need(not any(x['method']=='PATCH' for x in SERVICE),'observed post race still closed')
 reset_runtime();CFG['close_race']={'head':'c'*40};no('close_postreadback_changed_head_no_success_receipt',invoke);need(not (runtime/'CLOSURE_RECEIPT.json').exists(),'race concealed by successful receipt')
 reset_runtime();CFG['lost_post_response']=True;no('lost_comment_response_stops',invoke);need(exists:= (runtime/'COMMENT_POST_INTENT.json').exists(),'POST intent missing before lost response');CFG.pop('lost_post_response');yes('GET_only_unique_comment_recovery_then_close',invoke)
 need(sum(x['method']=='POST' and x['endpoint'].endswith('/issues/967/comments') for x in SERVICE)==1,'duplicate comment POST recovery')
 need(sum(x['method']=='PATCH' for x in SERVICE)==1,'duplicate close PATCH')
 yes('closed_known_intent_readonly_reconciliation',lambda:invoke(False));yes('closed_execute_local_receipt_idempotent',invoke)
 comment_values[0]['user']={'id':99,'login':'foreign','node_id':'FOREIGN'};no('recovery_foreign_comment_actor',lambda:n['reconcile_comment'](bound,body));comment_values[0]['user']=copy.deepcopy(WHO)
 comment_values[0]['created_at']='2026-10-15T00:00:00Z';no('recovery_preintent_comment_timestamp',lambda:n['reconcile_comment'](bound,body));comment_values[0]['created_at']='2026-10-16T22:00:01Z'
 comment_values.append({**comment_values[0],'id':1002});no('recovery_duplicate_exact_body',lambda:n['reconcile_comment'](bound,body));comment_values.pop()
 CFG['merged']=True;no('merged_rejects_closure_receipt',lambda:n['closure_receipt'](bound,body,context));CFG.pop('merged')
 reset_runtime();CFG['lost_close_response']=True;no('lost_close_response_stops',invoke);CFG.pop('lost_close_response');yes('closed_lostresponse_GET_only_recovery',invoke);need(sum(x['method']=='PATCH' for x in SERVICE)==1,'lost-close retry duplicated PATCH')
 # An uncertain OPEN close intent cannot repeat PATCH; ambiguous POST cannot repeat.
 CFG['state']='open';no('uncertain_close_stillopen_never_repeat',invoke);need(sum(x['method']=='PATCH' for x in SERVICE)==1,'uncertain open duplicated PATCH')
 reset_runtime();CFG['lost_post_response']=True;no('prepare_uncertain_post_fixture',invoke);CFG.pop('lost_post_response');comment_values.clear();no('uncertain_post_no_actual_match_never_repeat',invoke);need(sum(x['method']=='POST' and x['endpoint'].endswith('/issues/967/comments') for x in SERVICE)==1,'uncertain POST repeated')
 # More than100 comments exercises actual full pagination for recovery.
 reset_runtime()
 for i in range(1,102):comment_values.append({'id':i,'body':'UNRELATED SYNTHETIC COMMENT','user':copy.deepcopy(WHO),'created_at':'2026-10-15T00:00:00Z','updated_at':'2026-10-15T00:00:00Z','html_url':f'https://github.com/{n["REPO"]}/pull/967#issuecomment-{i}','issue_url':f'https://api.github.com/repos/{n["REPO"]}/issues/967'})
 yes('full_pagination_comment_and_close',invoke);need(any('comments?per_page=100&page=2' in x['endpoint'] for x in SERVICE),'second page absent')
 # Native global byte differences and closure actor mismatch cannot be hidden.
 original_native=copy.deepcopy(blobs)
 for path in (n['QUEUE'],n['STATE'],n['HISTORY']):
  blobs[path]+=b' ';no('native_actual_raw_change_'+path,lambda:n['closure_receipt'](bound,body,context));blobs[path]=original_native[path]
 event_values[-1]['actor']={'id':99,'login':'foreign','node_id':'FOREIGN'};no('closed_actual_event_actor_mismatch',lambda:n['closure_receipt'](bound,body,context));event_values[-1]['actor']=copy.deepcopy(WHO)
 # The real filesystem lock excludes a distinct actual local child process.
 with n['operation_lock'](bound):
  program='import fcntl,os,sys; f=os.open(sys.argv[1],os.O_RDWR); '+"\ntry: fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)\nexcept BlockingIOError: sys.exit(73)\nsys.exit(0)"
  child=subprocess.run([sys.executable,'-I','-S','-B','-c',program,str(runtime/'OPERATION.lock')],capture_output=True)
  need(child.returncode==73 and not child.stderr,'actual child acquired held operation lock')
 EVENTS.append({'test':'real_distinct_child_process_lock_exclusion','status':'PASS','actual_child_returncode':child.returncode})
 # Durable local four-file plan / actual atomic writes / retry / foreign fields.
 receipt=n['closure_receipt'](bound,body,context);record=n['local_record'](bound,receipt,d)
 state={'active_pr':967,'active_problem_id':'2616','next_pr':967,'eligible_prs':[904,967],'completed_prs':[904],'published_prs':[904],'completed_results':[{'pr':904,'outcome':'accepted_merged_preprint_published','foreign':'KEEP'}],'closed_prs':[],'foreign':{'preserve':[1,2]},'active_original_head':n['HEAD']}
 items=[{'number':904,'foreign':'KEEP'},{'number':967,'headRefOid':n['HEAD'],'baseRefName':'main','url':f'https://github.com/{n["REPO"]}/pull/967','entries':[{'id':'2616','foreign':'KEEP'}],'disposition':'pending_audit','foreign':'KEEP'},{'number':999,'foreign':'LATERKEEP'}]
 scan={'schema':'pr967-ascending-status-gate-v1','range':[968,1000],'skipped':[],'next_eligible':None,'end_of_range':True,'math_source_read':False,'whole_goal_complete':False,'two_complete_900_1000_resweeps_still_required':True}
 def local_setup():
  for name in ['LOCAL_FINALIZATION_INTENT.json','LOCAL_FINALIZATION_RECEIPT.json',*[r+s for r in n['local_paths']() for s in ['.before','.after']]]:
   try:(runtime/name).unlink()
   except FileNotFoundError:pass
  (effort/'CURRENT_STATE.json').write_bytes(enc(state));(effort/'inventory.json').write_bytes(enc(items))
  (effort/'RESEARCH_LOG.md').write_bytes(b'FOREIGN PROJECT LOG\n');(audit/'RESEARCH_LOG.md').write_bytes(b'FOREIGN AUDIT LOG\n')
 def final():return n['reconcile_local'](bound,record,scan,True)
 local_setup();yes('local_default_preview_writes_zero',lambda:n['reconcile_local'](bound,record,scan,False));need(not (runtime/'LOCAL_FINALIZATION_INTENT.json').exists(),'preview wrote plan')
 yes('local_all_four_files_real_atomic_finalize',final)
 actual=json.loads((effort/'CURRENT_STATE.json').read_bytes());inv=json.loads((effort/'inventory.json').read_bytes())
 need(actual['foreign']==state['foreign'] and actual['completed_results'][0]==state['completed_results'][0] and inv[0]==items[0] and inv[2]==items[2] and inv[1]['foreign']=='KEEP','foreign fields lost')
 need(actual['active_pr'] is None and actual['two_complete_900_1000_final_resweeps_required'] is True,'explicit end/resweep obligation')
 yes('local_retry_idempotent_unique_markers',final)
 for role,path in n['local_paths']().items():
  if 'log' in role:need(path.read_bytes().count(b'PR967-PRIORITY-LOCAL-COMPLETION-V1 ')==1,'duplicate marker')
 original_atomic=n['atomic']
 for failrole in ['inventory','state','project_log','audit_log']:
  local_setup();armed=[True]
  def interrupted(path,*a):
   if path==n['local_paths']()[failrole] and armed[0]:armed[0]=False;raise RuntimeError('SYNTHETIC_INTERRUPT_BEFORE_'+failrole)
   return original_atomic(path,*a)
  n['atomic']=interrupted;no('local_partial_'+failrole,final);need(not (runtime/'LOCAL_FINALIZATION_RECEIPT.json').exists(),'partial success receipt')
  n['atomic']=original_atomic;yes('local_recovery_'+failrole,final)
 local_setup();armed=[True]
 def interrupted(path,*a):
  out=original_atomic(path,*a)
  if path==effort/'inventory.json' and armed[0]:armed[0]=False;raise RuntimeError('SYNTHETIC_AFTER_RENAME')
  return out
 n['atomic']=interrupted;no('local_interrupt_after_atomic_rename',final);n['atomic']=original_atomic
 foreign=(effort/'CURRENT_STATE.json').read_bytes()+b' ';(effort/'CURRENT_STATE.json').write_bytes(foreign)
 no('local_pending_plan_rejects_foreign_writer',final);need((effort/'CURRENT_STATE.json').read_bytes()==foreign,'foreign bytes overwritten')
 local_setup();log=effort/'RESEARCH_LOG.md';log.write_bytes(b'PR967-PRIORITY-LOCAL-COMPLETION-V1 {}\n');no('local_malformed_marker_rejects',final)
 # Ascending scan tests never fetch originals/evidence and must explicitly end.
 saved_gate=n['status_gate'];seen=[]
 def fake_gate(number,key=None,expected_head=None,allow_closed=False):
  seen.append(number)
  return {'action':'SKIP_STATUS_ONLY','pr':{'number':number},'status':'unsolved','math_source_read':False}
 n['status_gate']=fake_gate
 yes('ascending_all968_1000_explicit_end',lambda:n['need'](n['scan_next']()['end_of_range'] is True,'no explicit end'));need(seen==list(range(968,1001)),'range skipped/expanded')
 seen.clear()
 def first_selected(number,**kwargs):
  seen.append(number);return {'action':'ELIGIBLE' if number==971 else 'SKIP_STATUS_ONLY','pr':{'number':number},'problem_id':'fixture','math_source_read':False}
 n['status_gate']=first_selected
 yes('ascending_stops_at_actual_nexteligible',lambda:n['need'](n['scan_next']()['next_eligible']['pr']['number']==971,'wrong next'));need(seen==list(range(968,972)),'read after selected')
 n['status_gate']=saved_gate
 # These are test logs of explicit fixtures, not actual production operations.
 DONE[0]=True
 print(json.dumps({'schema':'pr967-proposed-closure-offline-tests-v1','status':'PASS_OFFLINE_CONTROLS_ONLY','outer_optimization':sys.flags.optimize,'core_sha256':args.core_sha256,'wrapper_sha256':args.wrapper_sha256,'events':EVENTS,'event_count':len(EVENTS),'real_local_SQLite_file_reads':True,'real_atomic_local_replacements_and_locks_available':True,'all26_original_bytes_and_modes_mutated':True,'service_and_Git_responses':'EXPLICIT_OFFLINE_FIXTURES','actual_remote_service_mutations':0,'actual_Git_mutations':0,'private_fixture_bodies_retained':False,'acceptance_or_priority_or_clean_review_authority':False},sort_keys=True))
