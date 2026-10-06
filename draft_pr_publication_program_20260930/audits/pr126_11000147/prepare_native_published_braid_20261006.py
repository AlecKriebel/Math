"""Prepare a scoped native priority correction in private copies; export only after a fresh writer grant."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,os,sqlite3,subprocess,sys,textwrap
A=Path(__file__).resolve().parent;C=A.parents[2];P=A.parent.parent
R=Path('/Users/alec/Documents/Math');K='11000147'
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'
PY='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
D=A/'native_published_braid_preparation_20261006';B=D/'private_backend';N=D/'proposed_native_attempt';records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(v,s):
 if not v:raise ValueError(s)
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def run(argv,cwd=C):
 start=now();ch=subprocess.Popen(argv,cwd=cwd,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'},stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=ch.communicate()
 records.append({'argv':argv,'cwd':str(cwd),'PID':ch.pid,'UTC_start':start,'UTC_end':now(),'exit_code':ch.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err),'stderr':err.decode('utf8','replace')[:1200]})
 dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'records':records})
 require(ch.returncode==0,'Actual native preparation failed; inspect before retry')
 return out
def git(*args):return run([GIT,*args])
require(not D.exists(),'Existing native preparation; inspect rather than repeat')
ready=load(A/'ROOT_PUBLISHED_BRAID_DISPOSITION_READY_20261006.json')
closed=load(A/'actual_closure_20261006/RECEIPT.json')
require(ready['fresh_disposition_review_PASS'] and ready['native_status_correction_supported'],'Fresh disposition gate')
require(closed['same_head_closed_without_merge'] and closed['original_head']==ready['original_head'],'Actual original-head closure')
D.mkdir();B.mkdir();N.mkdir();(D/'.gitignore').write_text('private_backend/\n')
require(git('branch','--show-current').strip()==b'main','Stay on main')
base=git('rev-parse','HEAD').decode().strip()
require(base==sys.argv[1],'Local main advanced')
require(git('ls-remote','origin','refs/heads/main').decode().split()[0]==base,'Remote main advanced')
require(not git('diff','--cached','--name-only'),'Shared index not empty')
prefix='unsolved_math_prioritization/'
require(not git('ls-tree','-r','--name-only',base,'--',prefix+'attempts/'+K),'Existing native attempt requires reconciliation')
names=['queue.py','manifest.json','policy.json','catalog.json','assessments.json','state.json','history.jsonl','assessment_history.jsonl','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md'];before={}
for name in names:
 b=git('show',base+':'+prefix+name);before[name]=b;(B/name).write_bytes(b)
 current=C/prefix/name
 require(not current.is_symlink() and (not current.exists() or current.read_bytes()==b),'Unknown materialized native change '+name)
(B/'cache').mkdir();cache=B/'cache/catalog.sqlite'
run(['/bin/cp','-c',str(R/prefix/'cache/catalog.sqlite'),str(cache)])
manifest=load(B/'manifest.json');db=sqlite3.connect('file:'+str(cache)+'?mode=ro',uri=True)
require(db.execute('SELECT revision FROM metadata').fetchone()==(manifest['revision'],),'Cache revision')
require(db.execute('SELECT count(*) FROM records').fetchone()[0]==manifest['records'],'Cache record count')
raw,report=db.execute('SELECT payload,report FROM records WHERE key=?',(K,)).fetchone();db.close();source,prior=json.loads(raw),json.loads(report)
F=A/'original_head_authentication_20261006';O=F/'original_attempt'
require(source==load(F/'SOURCE_STATEMENT.json') and prior==load(F/'PRIOR_REPORT.json'),'Full authenticated source/prior mismatch')
original_ready=load(O/'readiness.json')
require(original_ready['review_hash']=='e4661a35fab521d11683d68c0042e48103644a570c1502031ec3b4951035dcc0' and original_ready['statement_hash']==sha(source['statement'].encode()) and original_ready['budget']['substantive_attempts_used']==1,'Original full source/readiness/effort binding')
review_hash=sha(json.dumps([source,prior],sort_keys=True).encode());oldrows=load(B/'catalog.json');catalog={x['id']:x for x in oldrows};row=catalog[K]
require(review_hash==row['review_hash']=='e4661a35fab521d11683d68c0042e48103644a570c1502031ec3b4951035dcc0','Complete source binding')
auth=load(F/'ORIGINAL_AUTHENTICATION.json')
require(auth['original_budget']=='1/5' and auth['original_literal_status']=='claimed_solved','Original submitted effort')
for x in auth['original_files']:
 b=(O/x['path']).read_bytes();require(len(b)==x['bytes'] and sha(b)==x['sha256'],'Original changed '+x['path'])
states=load(B/'state.json');oldstates=json.loads(before['state.json']);require(K not in states,'Existing native state requires reconciliation')
evidence={'review_hash':review_hash,'exact_claim':source['statement'],'original_head':ready['original_head'],'original_effort_imported':1,'original_budget':'1/5','original_archive':str(O.relative_to(C)),'original_proof_sha256':sha((O/'CANDIDATE.md').read_bytes()),'effort_provenance':str((F/'ORIGINAL_AUTHENTICATION.json').relative_to(C)),'new_central_proof_search_turns':0,'mathematics_valid':True,'classification_scope':'Published BKL1998 band-generator relations already supply the universal three-element braid construction; the Wajnryb2006 source supplies the Anosov pair. Already_solved is scoped to old mathematical content, not an established express earlier answer to the named Wajnryb question.','old_published_whole_narrow_result_verified':True,'express_historical_named_target_answer_established':False,'explicit_application_first_priority_established':False,'exact_matrix_first_priority_established':False,'substantive_novel_open_problem_resolution_established':False,'mathematical_gate':str((A/'MATHEMATICAL_SOURCE_GATE_20261006.json').relative_to(C)),'priority_reasoning':str((A/'ROOT_PUBLISHED_BRAID_DISPOSITION_20261006.md').relative_to(C)),'primary_braid_bridge':str((A/'ROOT_PUBLISHED_BRAID_PRIORITY_BRIDGE_20261006.md').relative_to(C)),'fresh_review':str((A/ready['fresh_disposition_review']).relative_to(C)),'closed_PR_comment':closed['closing_comment_url'],'prior_braid_DOI':'10.1006/aima.1998.1761','source_chapter_DOI':'10.1090/pspum/074/2264536','source_scope':'Existence on closed torus allowed by original source; no every-genus, boundary-fixed, faithful-triangle-Artin or minimal-generator claim','original_independent_assert_guard_weakness':'Normal311 author and3156 independent checks reproduced. Independent checker predicates vanish under -O; separately bound diagnostic repair passes and rejects corruption. Original16 preserved; no repaired verifier promoted or original receipt reused as code authentication.','no_fabricated_proof_turns_or_readiness':True}
dump(B/'evidence.json',evidence)
imported={'at':now(),'id':K,'status':'already_solved','turns_used':1,'review_hash':review_hash,'statement_hash':row['statement_hash'],'evidence':evidence,'note':'Imported authenticated original submitted effort1/5; priority validation adds zero central proof turns; no synthetic candidate/readiness ledger.','original_effort_import':evidence}
states[K]=imported;dump(B/'state.json',states)
with (B/'history.jsonl').open('a') as h:h.write(json.dumps({**imported,'event':'import_authenticated_submitted_author_effort'},ensure_ascii=False)+'\n')
oldass=json.loads(before['assessments.json']);old=oldass[K]
note='Valid closed-torus triple is already implied by BKL1998 band relations (DOI10.1006/aima.1998.1761) and the Wajnryb2006 source Anosov pair (DOI10.1090/pspum/074/2264536). No substantive new mathematical theorem established; express earlier named answer, first application and exact-matrix priority remain unestablished. PR126 closed unmerged without paper/DOI/tracker. Original1/5 imported; audit0.'
assessment={**old,'p_solve':0,'p_valid_open':0,'resolution':'already_solved','route':'proof','decision':'exclude','review_policy':'2.0-five-turn-proof','review_type':'fresh full-source mathematical and published-braid disposition','review_hash':review_hash,'note':note,'rationale':'Independent exact algebra and source/dynamics families verify the entire narrow closed-torus theorem. BKL1998 Proposition2.1 Eq8 with Eq4 indices supplies AB=CA=BC in every image of B3; the already credited source pair supplies the Anosov dynamics. Separate published-braid and named-question historical families, followed by a fresh disposition adversary, support the precise old-content classification and comment.','remaining_gap':'No mathematical or source-scope gap in the old-content implication. Express earlier named-question answer, first explicit-application priority and exact-matrix priority are not established. This priority exclusion does not assert BKL expressly answered the later Wajnryb question; no substantive novel resolution demonstrated.','first_experiment':'Preserve the valid self-contained original proof and independently bound verifiers/source bridges; do not prepare a novel-solution preprint for the existing old-content consequence. Any materially new theorem needs a separate exact target.','sources':['https://doi.org/10.1006/aima.1998.1761','https://www.math.columbia.edu/~jb/bkl-newpres.pdf','https://doi.org/10.1090/pspum/074/2264536','https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf'],'original_budget':'1/5','new_central_proof_search_turns':0,'evidence':evidence}
dump(B/'assessment.json',assessment)
run([PY,'-E','-S','-B','-P',str(B/'queue.py'),'assess',K,'--file',str(B/'assessment.json')],B)
run([PY,'-E','-S','-B','-P',str(B/'queue.py'),'status',K,'already_solved','--note',note,'--evidence',str(B/'evidence.json')],B)
afterass,afterstate=load(B/'assessments.json'),load(B/'state.json');aftercatalog={x['id']:x for x in load(B/'catalog.json')}
require({k:v for k,v in afterass.items() if k!=K}=={k:v for k,v in oldass.items() if k!=K},'Other assessment changed')
require({k:v for k,v in afterstate.items() if k!=K}==oldstates,'Other state changed')
require(afterstate[K]['turns_used']==1 and afterstate[K]['status']=='already_solved','Effort/status mismatch')
require(aftercatalog[K]['local_status']=='already_solved' and not aftercatalog[K]['eligible'] and aftercatalog[K]['turns_used']==1,'Target projection')
require(set(catalog)==set(aftercatalog),'Catalog identities changed')
for name in ['history.jsonl','assessment_history.jsonl']:require((B/name).read_bytes().startswith(before[name]),'History prefix modified')
added=[json.loads(s) for s in (B/'history.jsonl').read_bytes()[len(before['history.jsonl']):].decode().splitlines()];aa=[json.loads(s) for s in (B/'assessment_history.jsonl').read_bytes()[len(before['assessment_history.jsonl']):].decode().splitlines()]
require(len(added)==2 and len(aa)==1 and all(x['id']==K for x in added+aa),'History event scope')
require(added[0]['event']=='import_authenticated_submitted_author_effort' and all(x['turns_used']==1 for x in added),'Original effort provenance')
drift=[]
for key,x in catalog.items():
 if key==K:continue
 diff={f:{'before':x.get(f),'after':aftercatalog[key].get(f)} for f in set(x)|set(aftercatalog[key]) if f!='rank' and x.get(f)!=aftercatalog[key].get(f)}
 if diff:
  require(set(diff)<={'local_status','eligible','turns_used'},'Unexplained unrelated projection '+key)
  st=afterstate.get(key,{})
  require(aftercatalog[key]['local_status']==st['status'] and aftercatalog[key]['turns_used']==st.get('turns_used',0),'Projection inconsistency '+key)
  drift.append({'id':key,'difference':diff,'baseline_preserved':True})
dump(D/'UNRELATED_BASELINE_PROJECTION_DRIFT.json',{'base_commit':base,'differences':drift,'other_targets_not_reassessed':True})
rows=[dict(aftercatalog[K]) if x['id']==K else dict(x) for x in oldrows];rows.sort(key=lambda x:(not x['eligible'],-x['ev'],x['id']))
for i,x in enumerate([x for x in rows if x['eligible']],1):x['rank']=i
for x in rows:
 if not x['eligible']:x['rank']=None
code=(B/'queue.py').read_text();render=textwrap.dedent(code[code.index("    write(ROOT/'catalog.json',rows)"):code.index('def seen_ids')])
spec=importlib.util.spec_from_file_location('pr126_native_queue_writer',B/'queue.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
namespace=dict(module.__dict__);namespace.update(rows=rows,cfg=load(B/'policy.json'),reviews=afterass,state=afterstate)
exec(compile(render,str(B/'queue.py')+':pinned-native-render','exec'),namespace)
for x in load(B/'catalog.json'):
 if x['id']!=K:require({f:v for f,v in x.items() if f!='rank'}=={f:v for f,v in catalog[x['id']].items() if f!='rank'},'Other semantic catalog row changed')
dump(D/'SCOPED_RENDER_RECEIPT.json',{'UTC':now(),'queue_py_sha256':sha((B/'queue.py').read_bytes()),'native_render_code_sha256':sha(render.encode()),'unrelated_catalog_rows_preserved_except_rank':True,'baseline_drift_preserved':len(drift)})
lines=before['QUEUE.md'].decode().splitlines();positions=[i for i,s in enumerate(lines) if '| 11000147 / AMR-109-0147 |' in s];require(len(positions)==1,'Unique campaign row')
i=positions[0];cells=lines[i].split('|');require(cells[8].strip()=='queued' and cells[9].strip()=='0/5','Native campaign baseline')
cells[4],cells[8],cells[9]=' 0.0000 ',' already_solved ',' 1/5 '
cells[11]=' 2026-10-06: Valid torus triple already follows from BKL1998 band relations (DOI10.1006/aima.1998.1761) and Wajnryb2006 source pair (DOI10.1090/pspum/074/2264536). No substantive novel theorem; express named-answer, first-application and exact-matrix priority unestablished. PR126 closed unmerged without paper/DOI/tracker. Original1/5 imported, audit0. '
lines[i]='|'.join(cells)
require([s for j,s in enumerate(lines) if j!=i]==[s for j,s in enumerate(before['QUEUE.md'].decode().splitlines()) if j!=i],'Other campaign row changed')
(B/'QUEUE.md').write_text('\n'.join(lines)+'\n')
dump(N/'assessment.json',afterass[K]);require(load(N/'assessment.json')==afterass[K],'Canonical attempt assessment equals authoritative target');dump(N/'HISTORICAL_DESK_ASSESSMENT.json',old);dump(N/'PRIORITY_EVIDENCE.json',evidence)
(N/'README.md').write_text('# 11000147: published-braid priority disposition\n\nStatus: already_solved, scoped to mathematical content already implied by BKL1998 Eq4 and Proposition2.1 Eq8 plus the Anosov pair already credited in Wajnryb2006. The original closed-torus triple is mathematically valid. An express earlier answer to the named Wajnryb question, first explicit-application priority and exact-matrix priority remain unestablished. No substantive new mathematical theorem was identified.\n\nPR126 closed unmerged: '+closed['closing_comment_url']+'\n\nThe original proof and its16 unchanged submitted bodies are archived in ../../../draft_pr_publication_program_20260930/audits/pr126_11000147/original_head_authentication_20261006/original_attempt/. Exact old-content bridge, scope limits, independent audits and seals are in the same PR126 audit folder. Original1/5 effort imported; no new proof-search turn, fabricated candidate/readiness, preprint, DOI or tracker row. Extensive AI assistance; no conventional human peer review.\n\nNormal verification reproduced311 author checks and3156 independent checks. Optimized Python erases the submitted independent assert predicates; a separately bound diagnostic repair was checked against corruption. Original checker bodies remain unchanged and no diagnostic repair is promoted as an original receipt.\n')
(N/'RESEARCH_LOG.md').write_text('# Published-braid disposition log\n\n'+now()+': Mathematics/source100%; bounded old published-content/fresh disposition100%; novelty clearance false. Native workflow95% pending actual scoped export, commit/push/full readbacks/release. Original1/5 imported, newproof0. Actual original-head closure verified. Program21/99=21.21%,11published; goalactive.\n')
record={'schema':'pr126-private-prepared-native-published-braid-correction/v1','UTC':now(),'actual_operator_PID':os.getpid(),'base_commit':base,'PR':126,'status':'already_solved','classification_scope':evidence['classification_scope'],'express_historical_named_target_answer_established':False,'original_budget':'1/5','new_central_proof_search_turns':0,'full_source_prior_authenticated':True,'original16_unchanged':True,'historical_desk_assessment_preserved':True,'unrelated_assessments_states_and_campaign_rows_preserved':True,'other_catalog_rows_only_rank_may_change':True,'baseline_projection_drift_preserved':len(drift),'native_commands':['assess','status'],'source_inputs':[{'path':prefix+n,'bytes':len(b),'sha256':sha(b),'Git_commit':base} for n,b in before.items()],'cache_snapshot_sha256':sha(cache.read_bytes()),'cache_revision':manifest['revision'],'cache_records':manifest['records'],'closing_comment_url':closed['closing_comment_url'],'same_head_closed_without_merge':True,'publication':False,'DOI':None,'tracker':False,'shared_tracked_files_exported':False,'primary_checkout_mutated':False,'native_export_pending_fresh_writer_grant':True}
dump(N/'DISPOSITION.json',record)
export=['assessments.json','state.json','history.jsonl','assessment_history.jsonl','catalog.json','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md']
record['proposed_native_pins']=[{'path':prefix+n,'prepared_local_path':str(B/n),'bytes':(B/n).stat().st_size,'sha256':sha((B/n).read_bytes())} for n in export]+[{'path':prefix+'attempts/'+K+'/'+p.name,'prepared_local_path':str(p),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(N.iterdir())]
dump(D/'PREPARED_RECEIPT.json',record)
print(json.dumps({k:v for k,v in record.items() if k not in ['proposed_native_pins','source_inputs']},sort_keys=True))
