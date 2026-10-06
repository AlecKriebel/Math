"""Read-only adversarial validation; writes only this assigned audit folder.

Does not import or execute the private native queue, preparer or continuation.
Git and GitHub invocations below are read-only. Failures use explicit exceptions.
"""
from pathlib import Path
import collections, copy, csv, datetime, hashlib, io, json, os, sqlite3, subprocess

HERE=Path(__file__).resolve().parent
A=HERE.parent; C=A.parents[2]; R=Path('/Users/alec/Documents/Math')
D=A/'native_published_obstruction_preparation_20261006'; B=D/'private_backend'; N=D/'proposed_native_attempt'
F=A/'original_head_authentication_20261006'; O=F/'original_attempt'
BASE='5de48499b84f168099d0273a340f4976f841f691'; HEAD='d110ad761291aa6ac1d66d2a49e8b8212c18bed6'; K='10400231'
PREFIX='unsolved_math_prioritization/'
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'; GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
events=[]; pins={}; checks=[]; controls=[]; observations=[]
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def require(v,label):
    if not v: raise RuntimeError(label)
    checks.append(label)
def dump(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
def read(p):
    require(not p.is_symlink() and p.is_file(),'Regular input '+str(p))
    b=p.read_bytes(); pins[str(p)]={'path':str(p),'bytes':len(b),'sha256':sha(b)}; return b
def load(p): return json.loads(read(p))
def run(argv,cwd=C):
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'); start=now()
    child=subprocess.Popen(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
    out,err=child.communicate()
    events.append({'argv':argv,'cwd':str(cwd),'actual_PID':child.pid,'UTC_start':start,'UTC_end':now(),'exit_code':child.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err)})
    require(child.returncode==0,'Successful read-only process '+str(argv)); return out
def git(*args,cwd=C): return run([GIT,*args],cwd)
def bind(source,prior,expected):
    if str(source['id'])!=K or source['problem_number']!='AMR-103-0231': raise ValueError('Wrong target')
    if sha(json.dumps([source,prior],sort_keys=True).encode())!=expected: raise ValueError('Source/prior changed')
def negative(label,fn):
    try: fn()
    except (ValueError,RuntimeError,KeyError): controls.append({'control':label,'rejected':True})
    else: raise RuntimeError('Control accepted: '+label)
start=now()
branch=git('branch','--show-current'); require(branch==b'main\n','Main branch')
localhead=git('rev-parse','HEAD'); require(localhead.strip().decode()==BASE,'Pinned local main')
index_before=git('diff','--cached','--name-only','-z'); require(not index_before,'Shared index empty')
dirty_before=git('diff','--name-only','-z')
primaryhead=git('rev-parse','HEAD',cwd=R)
primaryindex=git('diff','--cached','--name-only','-z',cwd=R)
primarydirty=git('diff','--name-only','-z',cwd=R)
names=['queue.py','manifest.json','policy.json','catalog.json','assessments.json','state.json','history.jsonl','assessment_history.jsonl','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md']
before={n:git('show',BASE+':'+PREFIX+n) for n in names}
baseline_pins=[{'Git_commit':BASE,'path':PREFIX+n,'bytes':len(b),'sha256':sha(b)} for n,b in before.items()]
receipt=load(D/'PREPARED_RECEIPT.json'); journal=load(D/'PROCESS_JOURNAL.json'); failure=load(D/'ACTUAL_INTERRUPTED_RECEIPT_PHASE.json')
require(receipt['base_commit']==BASE and receipt['PR']==124,'Receipt target/base')
require(receipt['shared_tracked_files_exported'] is False and receipt['native_export_pending_fresh_writer_grant'] is True,'Prepared receipt export still pending')
require(receipt['source_inputs']==baseline_pins,'All 12 receipt baseline bodies match Git')
exports=['assessments.json','state.json','history.jsonl','assessment_history.jsonl','catalog.json','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md']
expected_paths={PREFIX+n for n in exports}|{PREFIX+'attempts/'+K+'/'+n for n in ['DISPOSITION.json','HISTORICAL_DESK_ASSESSMENT.json','PRIORITY_EVIDENCE.json','README.md','RESEARCH_LOG.md','assessment.json']}
members=receipt['proposed_native_pins']
require(len(members)==15 and {x['path'] for x in members}==expected_paths,'Exactly 15 allowlisted unique proposed native paths')
for item in members:
    p=Path(item['prepared_local_path']); expected=(N/p.name if '/attempts/' in item['path'] else B/p.name)
    require(p==expected,'Each prepared locator matches exact destination '+item['path'])
    b=read(p); require(len(b)==item['bytes'] and sha(b)==item['sha256'],'Full proposed body pin '+item['path'])
negative('forged proposed hash',lambda: require(sha(read(Path(members[0]['prepared_local_path'])))=='0'*64,'Forged hash rejection'))
negative('one-byte body corruption',lambda: require(sha(read(Path(members[-1]['prepared_local_path']))+b'X')==members[-1]['sha256'],'Corrupt body rejection'))
negative('wrong destination target',lambda: require(expected_paths=={x.replace('/10400231/','/10400232/') for x in expected_paths},'Wrong destination rejection'))
manifest=load(B/'manifest.json'); cache=B/'cache/catalog.sqlite'; cachebody=read(cache)
require(sha(cachebody)==receipt['cache_snapshot_sha256'],'Full SQLite snapshot pin')
sourceauth=load(F/'SOURCEPAIR_AUTHENTICATION.json')
require({'bytes':len(cachebody),'sha256':sha(cachebody)}==sourceauth['cache_pins']['catalog.sqlite'],'SQLite snapshot original authentication pin')
db=sqlite3.connect('file:'+str(cache)+'?mode=ro&immutable=1',uri=True)
require(db.execute('SELECT revision FROM metadata').fetchall()==[(manifest['revision'],)],'SQLite immutable revision exact')
require(db.execute('SELECT count(*) FROM records').fetchone()[0]==manifest['records']==receipt['cache_records']==15458,'SQLite record count exact')
rows=db.execute('SELECT payload,report FROM records WHERE key=?',(K,)).fetchall(); db.close(); require(len(rows)==1,'Single exact cached numeric target')
source,prior=map(json.loads,rows[0]); expected_hash='f95daf41b9da37094c786cb6c24fc3351423008edf7d33d57643cecc39a14a38'
bind(source,prior,expected_hash)
require(source==load(O/'source_record.json')==load(F/'SOURCE_STATEMENT.json'),'Complete cached source equals both original and authenticated source')
require(prior==load(O/'prior_imported_report.json')==load(F/'PRIOR_REPORT.json')==sourceauth['complete_prior_report'],'Complete nonempty prior equals original and authenticated prior')
for fn in ['problems.json','research_results.json']:
    b=read(R/PREFIX/'cache'/fn); require({'bytes':len(b),'sha256':sha(b)}==sourceauth['cache_pins'][fn],'Full upstream cache pin '+fn)
problems=json.loads(read(R/PREFIX/'cache/problems.json')); reports=json.loads(read(R/PREFIX/'cache/research_results.json'))
require([p for p in problems if str(p['id'])==K]==[source] and reports[source['problem_number']]==prior,'Full raw cache joins exact source/prior')
stale=copy.deepcopy(source); stale['view_count']+=1
negative('stale source metadata despite same statement',lambda:bind(stale,prior,expected_hash))
wrong=copy.deepcopy(source); wrong['id']=10400232
negative('wrong numeric target',lambda:bind(wrong,prior,expected_hash))
badprior=copy.deepcopy(prior); badprior['what_remains']+=' altered'
negative('stale full prior report',lambda:bind(source,badprior,expected_hash))
auth=load(F/'ORIGINAL_AUTHENTICATION.json'); require(auth['original_head']==HEAD and auth['original_budget']=='2/5' and auth['original_literal_status']=='claimed_solved','Original head/status/effort exact')
tree=git('ls-tree','-r','--long','-z',HEAD,'--',PREFIX+'attempts/'+K).split(b'\0'); entries={}
for e in tree:
    if e:
        m,p=e.decode().split('\t'); mode,kind,blob,size=m.split(); require(mode=='100644' and kind=='blob','Regular original Git blob'); entries[p.removeprefix(PREFIX+'attempts/'+K+'/')]=(blob,int(size))
require(len(entries)==17 and set(entries)=={x['path'] for x in auth['original_files']},'Exactly 17 original Git bodies')
for item in auth['original_files']:
    b=read(O/item['path']); g=git('show',HEAD+':'+PREFIX+'attempts/'+K+'/'+item['path']); blob,size=entries[item['path']]
    require(b==g and len(b)==item['bytes']==size and sha(b)==item['sha256'] and blob==item['Git_blob'],'Unchanged original Git body '+item['path'])
oldqueue=git('show',HEAD+':'+PREFIX+'QUEUE.md'); require(oldqueue==read(F/'ORIGINAL_HEAD_QUEUE.md'),'Original full queue body exact')
original_line=[s for s in oldqueue.decode().splitlines() if '| 10400231 / AMR-103-0231 |' in s]
require(len(original_line)==1 and '| claimed_solved | 2/5 |' in original_line[0],'Original immutable campaign effort2/5')
log=read(O/'RESEARCH_LOG.md').decode(); require('1. Investigated' in log and '2. Proved' in log and 'candidate2/5' in log,'Original two numbered substantive entries')
require(not (O/'readiness.json').exists() and not (O/'turns.jsonl').exists(),'No invented original readiness or turn ledger')
oldass=json.loads(before['assessments.json']); oldstate=json.loads(before['state.json']); oldcat={x['id']:x for x in json.loads(before['catalog.json'])}
newass=load(B/'assessments.json'); newstate=load(B/'state.json'); newrows=load(B/'catalog.json'); newcat={x['id']:x for x in newrows}
require(set(oldass)==set(newass) and {k:v for k,v in oldass.items() if k!=K}=={k:v for k,v in newass.items() if k!=K},'Every unrelated assessment unchanged')
require(K not in oldstate and {k:v for k,v in newstate.items() if k!=K}==oldstate,'Every unrelated state unchanged; target is new imported effort')
require(set(oldcat)==set(newcat) and len(newcat)==len(newrows),'All catalog identities preserved without duplicate rows')
rankchanges=[]
for k,v in oldcat.items():
    if k!=K:
        require({f:x for f,x in v.items() if f!='rank'}=={f:x for f,x in newcat[k].items() if f!='rank'},'Other semantic catalog row unchanged '+k)
        if v['rank']!=newcat[k]['rank']: rankchanges.append(k)
targetdiff={f:{'before':oldcat[K].get(f),'after':newcat[K].get(f)} for f in set(oldcat[K])|set(newcat[K]) if oldcat[K].get(f)!=newcat[K].get(f)}
require(set(targetdiff)=={'holds','ev_low','desk_decision','p_solve','eligible','turns_used','p_valid_open','ev','rank','ev_high','desk_note','local_status'},'Only intended target catalog fields changed')
require(newcat[K]['local_status']=='already_solved' and newcat[K]['turns_used']==2 and newcat[K]['eligible'] is False and newcat[K]['holds']==['known_resolution','not_selected_for_five_turn_attempt'],'Target catalog excludes old mathematical content and records original2/5')
require(newstate[K]['turns_used']==2 and newstate[K]['status']=='already_solved' and not {'readiness_review_hash','candidate_turn'}&set(newstate[K]),'No synthetic state readiness/candidate ledger')
require(load(N/'HISTORICAL_DESK_ASSESSMENT.json')==oldass[K],'Historical full desk assessment archived')
evidence=load(N/'PRIORITY_EVIDENCE.json'); assessment=load(N/'assessment.json')
require(evidence==load(B/'evidence.json')==newstate[K]['evidence'] and assessment==load(B/'assessment.json'),'Native attempt exact assessment/evidence counterparts')
require(evidence['exact_claim']==source['statement'] and evidence['review_hash']==expected_hash and evidence['original_effort_imported']==2 and evidence['new_central_proof_search_turns']==0,'Exact statement binding; original2 imported; newproof0')
require(evidence['express_historical_refutation_established'] is False and evidence['explicit_application_first_priority_established'] is False and evidence['substantive_novel_open_problem_resolution_established'] is False and evidence['whole_book_read'] is False,'Historical/novelty/source limits preserved')
for name,count in [('history.jsonl',2),('assessment_history.jsonl',1)]:
    b=read(B/name); require(b.startswith(before[name]),'Byte-for-byte historical prefix '+name)
    extra=[json.loads(s) for s in b[len(before[name]):].decode().splitlines()]; require(len(extra)==count and all(x['id']==K for x in extra),'Exactly scoped appended event count '+name)
    if name=='history.jsonl':
        require(extra[0]['event']=='import_authenticated_submitted_author_effort' and all(x['turns_used']==2 and x['status']=='already_solved' for x in extra),'Import/status only; no proof turn')
        require(extra[1]==newstate[K],'Final state equals exact last history event')
    else: require(extra[0]==newass[K],'Native assessment equals exact assessment history event')
drift=load(D/'UNRELATED_BASELINE_PROJECTION_DRIFT.json'); require(len(drift['differences'])==48 and drift['base_commit']==BASE,'48 explicitly archived baseline projection discrepancies')
computed=[]
for k,v in oldcat.items():
    if k==K or k not in oldstate: continue
    s=oldstate[k]; projection={'local_status':s['status'],'turns_used':s.get('turns_used',0),'eligible':not v['holds'] and s['status'] in ['queued','unreviewed','ready'] and s.get('turns_used',0)<v['turn_limit']}
    diff={f:{'before':v[f],'after':value} for f,value in projection.items() if v[f]!=value}
    if diff: computed.append({'id':k,'difference':diff,'baseline_preserved':True})
require(sorted(computed,key=lambda x:x['id'])==sorted(drift['differences'],key=lambda x:x['id']),'Independently derived exact 48 discrepancies preserved, not repaired')
expectedrows=sorted(newrows,key=lambda x:(not x['eligible'],-x['ev'],x['id']))
require(expectedrows==newrows,'Pinned scoped row ordering exact')
for i,row in enumerate([r for r in newrows if r['eligible']],1): require(row['rank']==i,'Eligible rank consecutive '+row['id'])
require(all(r['rank'] is None for r in newrows if not r['eligible']),'Every ineligible rank null')
fields=['rank','id','problem_number','title','category','ev','ev_low','ev_high','impact','p_solve','p_valid_open','assessment','local_status','upstream_status','eligible','present','holds','reasons','source_url','difficulty','proposed_year','age_years','age_multiplier','base_impact','route','desk_decision','desk_note','turns_used','turn_limit']
f=io.StringIO(newline=''); writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); writer.writeheader()
for row in newrows: writer.writerow({**row,'holds':'; '.join(row['holds']),'reasons':'; '.join(row['reasons'])})
require(f.getvalue().encode()==read(B/'ranking.csv'),'Complete ranking CSV independently rendered from preserved catalog')
counts=collections.Counter(h.split(':')[0] for row in newrows for h in row['holds'])
require(load(B/'summary.json')=={'records':len(newrows),'eligible':sum(row['eligible'] for row in newrows),'holds':dict(counts),'assessed':len(newass)},'Summary exactly matches scoped preserved catalog')
require(read(B/'SHORTLIST.md')==before['SHORTLIST.md'],'Full unrelated shortlist unchanged')
oldlines=before['QUEUE.md'].decode().splitlines(); newlines=read(B/'QUEUE.md').decode().splitlines()
require(len(oldlines)==len(newlines),'Campaign full line count preserved')
linechanges=[i for i,(x,y) in enumerate(zip(oldlines,newlines)) if x!=y]
require(len(linechanges)==1 and '| 10400231 / AMR-103-0231 |' in oldlines[linechanges[0]],'Only target campaign row changed')
cells=newlines[linechanges[0]].split('|'); require(cells[8].strip()=='already_solved' and cells[9].strip()=='2/5','Campaign scope and effort correct')
records=journal['records']; native=[x for x in records if 'assess' in x['argv'] or 'status' in x['argv']]
require(journal['actual_operator_PID']==68361 and len(native)==2 and [x['argv'][6] for x in native]==['assess','status'] and all(x['exit_code']==0 for x in native),'Actual original preparer68361 executed assess/status exactly once')
require(receipt['private_native_command_operator_PID']==68361 and receipt['actual_receipt_completion_operator_PID']==receipt['actual_operator_PID']==70252 and receipt['native_commands_repeated'] is False,'Original and continuation PIDs separated honestly')
prepared_source=read(A/'prepare_native_published_obstruction_20261006.py'); needle=b"'cache_snapshot_sha256':sha(cache.read_bytes())"
require(prepared_source.count(needle)==1 and sha(prepared_source)==failure['corrected_script_sha256'] and sha(prepared_source.replace(needle,b"'cache_snapshot_sha256':sha(cache)"))==failure['actual_executed_original_script_sha256'],'Executed defective preparer source and corrected source both pinned')
require(failure['actual_tool_exit_code']==1 and failure['failed_actual_operator_PID']==68361 and failure['failure_type']=='TypeError: object supporting the buffer API required','Actual receipt failure reported, not erased')
continuation=read(A/'complete_interrupted_native_receipt_20261006.py').decode(); tail=prepared_source.decode().split("record={'schema':'pr124-private-prepared-native-published-obstruction-correction/v1'",1)[1]
require('run(' not in tail and 'git(' not in tail and "native_commands_repeated':False" in continuation,'Receipt-only continuation contains no command repeat in executed tail')
require(len(receipt['read_only_revalidation_events'])==12 and all(x['argv'][1]=='show' and x['exit_code']==0 for x in receipt['read_only_revalidation_events']),'Continuation records exactly 12 full baseline readbacks')
ready=load(A/'ROOT_PUBLISHED_OBSTRUCTION_DISPOSITION_READY_20261006.json'); closed=load(A/'actual_closure_20261006/RECEIPT.json'); actualjournal=load(A/'actual_closure_20261006/PROCESS_JOURNAL.json'); mathgate=load(A/'MATHEMATICAL_SOURCE_GATE_20261006.json')
for filename,field in [('ROOT_PUBLISHED_OBSTRUCTION_DISPOSITION_20261006.md','root_disposition_sha256'),('CLOSING_COMMENT_OLD_PUBLISHED_OBSTRUCTION_20261006.md','closing_comment_sha256')]: require(sha(read(A/filename))==ready[field],'Exact reviewed root text '+filename)
fresh=load(A/'fresh_published_obstruction_disposition_adversary_20261006/RESULT.json'); freshauth=load(A/'ROOT_FRESH_DISPOSITION_AUTHENTICATION_20261006.json')
require(fresh['verdict']=='PASS' and fresh['operational_mutation_authorization'] is False and ready['fresh_disposition_review_PASS'] is True and mathgate['status']=='PASS','Fresh scoped scientific review and mathematical gate; no operational grant')
for item in freshauth['public_members']:
    b=read(A/item['path']); require(len(b)==item['bytes'] and sha(b)==item['sha256'],'Authenticated fresh public member '+item['path'])
freshinputs=load(A/'fresh_published_obstruction_disposition_adversary_20261006/INPUT_HASHES.json')['inputs']
for item in freshinputs:
    p=Path(item['path']); p=p if p.is_absolute() else A/p
    b=read(p); require(len(b)==item['bytes'] and sha(b)==item['sha256'],'Authenticated earlier full input '+item['path'])
actualpr=json.loads(run([GH,'pr','view','124','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,baseRefName,url,closedAt,mergedAt']))
dump('ACTUAL_READ_ONLY_PR.json',actualpr)
require(actualpr==closed['after'] and actualpr['headRefOid']==HEAD and actualpr['state']=='CLOSED' and actualpr['mergedAt'] is None and actualpr['closedAt']=='2026-10-06T20:54:37Z','Actual read-only service confirms exact same-head unmerged closure')
actualcomment=json.loads(run([GH,'api','repos/AlecKriebel/Math/issues/comments/6025266251']))
dump('ACTUAL_READ_ONLY_COMMENT.json',actualcomment)
comment=read(A/'CLOSING_COMMENT_OLD_PUBLISHED_OBSTRUCTION_20261006.md').decode()
require(actualcomment['id']==6025266251 and actualcomment['html_url']==closed['closing_comment_url'] and actualcomment['body']==comment and sha(actualcomment['body'].encode())==closed['closing_comment_sha256'],'Actual read-only full comment body exactly equals reviewed body')
require(actualcomment['issue_url'].endswith('/issues/124'),'Actual comment belongs to precise target')
require(evidence['closed_PR_comment']==actualcomment['html_url'] and closed['original_head']==HEAD and closed['original_budget']=='2/5' and closed['new_central_proof_search_turns']==0,'Native evidence agrees with actual closure and original effort')
release=load(A/'ACTUAL_MATH_PRIORITY_WRITER_RELEASE_20261006.json'); require(release['writer_ownership_released'] is True,'Prior writer ownership released; fresh concrete grant required')
for root in [C,R]:
    for name in names:
        p=root/PREFIX/name
        expected=before[name] if root==C else git('show',primaryhead.strip().decode()+':'+PREFIX+name,cwd=R)
        if p.exists(): require(read(p)==expected,'No shared native body export at '+str(p))
    require(not (root/PREFIX/'attempts'/K).exists(),'No shared native attempt exported at '+str(root))
require(git('rev-parse','HEAD')==localhead and git('branch','--show-current')==branch and git('diff','--cached','--name-only','-z')==index_before and git('diff','--name-only','-z')==dirty_before,'Review leaves main/ref/index/tracked changes unchanged')
require(git('rev-parse','HEAD',cwd=R)==primaryhead and git('diff','--cached','--name-only','-z',cwd=R)==primaryindex and git('diff','--name-only','-z',cwd=R)==primarydirty,'Review leaves primary main/index/tracked changes unchanged')
locators=['original_archive','effort_provenance','mathematical_gate','priority_reasoning','book_source_bridge','fresh_review']
for field in locators:
    p=C/evidence[field]
    if not p.exists(): observations.append({'field':field,'value':evidence[field],'repository_relative_resolution_exists':False,'audit_relative_resolution_exists':(A/evidence[field]).exists()})
dump('INPUT_HASHES.json',{'schema':'pr124-native-protocol-inputs/v1','UTC':now(),'inputs':list(pins.values()),'baseline_git_inputs':baseline_pins,'private_bodies_not_republished':True})
dump('ACTUAL_VALIDATION.json',{'schema':'pr124-native-protocol-actual-validation/v1','UTC_start':start,'UTC_end':now(),'actual_operator_PID':os.getpid(),'checks_passed':len(checks),'checks':checks,'negative_controls':controls,'read_only_processes':events,'all15_body_hashes_verified':True,'source_prior_review_hash':expected_hash,'original17_full_Git_bodies_verified':True,'unrelated_rank_changes':len(rankchanges),'unrelated_semantic_rows_preserved':len(newcat)-1,'preserved_baseline_projection_discrepancies':48,'target_catalog_differences':targetdiff,'reference_observations':observations,'native_CLI_runs_by_this_review':0,'service_mutations':False,'new_central_proof_search_turns':0})
print(json.dumps({'UTC':now(),'PID':os.getpid(),'checks_passed':len(checks),'negative_controls':len(controls),'input_count':len(pins),'rank_changes':len(rankchanges),'reference_observations':observations},sort_keys=True))
