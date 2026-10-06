"""Prepare a scoped native priority correction in private copies; export only after a fresh writer grant."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,os,sqlite3,subprocess,sys,textwrap
A=Path(__file__).resolve().parent;C=A.parents[2];P=A.parent.parent
R=Path('/Users/alec/Documents/Math');K='10400231'
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'
PY='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
D=A/'native_published_obstruction_preparation_20261006';B=D/'private_backend';N=D/'proposed_native_attempt';records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(v,s):
 if not v:raise ValueError(s)
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def run(argv,cwd=C):
 start=now();ch=subprocess.Popen(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=ch.communicate()
 records.append({'argv':argv,'cwd':str(cwd),'PID':ch.pid,'UTC_start':start,'UTC_end':now(),'exit_code':ch.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err),'stderr':err.decode('utf8','replace')[:1200]})
 dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'records':records})
 require(ch.returncode==0,'Actual native preparation failed; inspect before retry')
 return out
def git(*args):return run([GIT,*args])
require(not D.exists(),'Existing native preparation; inspect rather than repeat')
ready=load(A/'ROOT_PUBLISHED_OBSTRUCTION_DISPOSITION_READY_20261006.json')
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
require(source==load(O/'source_record.json') and source==load(F/'SOURCE_STATEMENT.json') and prior==load(F/'PRIOR_REPORT.json'),'Full original source/prior mismatch')
review_hash=sha(json.dumps([source,prior],sort_keys=True).encode());oldrows=load(B/'catalog.json');catalog={x['id']:x for x in oldrows};row=catalog[K]
require(review_hash==row['review_hash']=='f95daf41b9da37094c786cb6c24fc3351423008edf7d33d57643cecc39a14a38','Complete source binding')
auth=load(F/'ORIGINAL_AUTHENTICATION.json')
require(auth['original_budget']=='2/5' and auth['original_literal_status']=='claimed_solved','Original submitted effort')
for x in auth['original_files']:
 b=(O/x['path']).read_bytes();require(len(b)==x['bytes'] and sha(b)==x['sha256'],'Original changed '+x['path'])
states=load(B/'state.json');oldstates=json.loads(before['state.json']);require(K not in states,'Existing native state requires reconciliation')
evidence={'review_hash':review_hash,'exact_claim':source['statement'],'original_head':ready['original_head'],'original_effort_imported':2,'original_budget':'2/5','original_archive':str(O.relative_to(C)),'original_proof_sha256':sha((O/'COUNTEREXAMPLE.md').read_bytes()),'effort_provenance':str((F/'ORIGINAL_AUTHENTICATION.json').relative_to(C)),'new_central_proof_search_turns':0,'mathematics_valid':True,'classification_scope':'Published II.3.3/3.4 plus II.5.2 already imply the exact original all-prime family and general obstruction; already_solved is scoped to old mathematical content, not an established express historical Conjecture12.26 refutation.','old_published_full_family_and_general_obstruction_verified':True,'express_historical_refutation_established':False,'explicit_application_first_priority_established':False,'substantive_novel_open_problem_resolution_established':False,'mathematical_gate':str((A/'MATHEMATICAL_SOURCE_GATE_20261006.json').relative_to(C)),'priority_reasoning':str((A/'ROOT_PUBLISHED_OBSTRUCTION_DISPOSITION_20261006.md').relative_to(C)),'book_source_bridge':str((A/'continued_public_access_20261006/ROOT_BOOK_SOURCE_RECONCILIATION.md').relative_to(C)),'fresh_review':ready['fresh_disposition_review'],'closed_PR_comment':closed['closing_comment_url'],'prior_book_DOI':'10.1007/978-3-0348-7999-6','actual_primary_preview_pages':[20,22,23,26,27,28,45,46,114,118],'whole_book_read':False,'no_fabricated_proof_turns_or_readiness':True}
dump(B/'evidence.json',evidence)
imported={'at':now(),'id':K,'status':'already_solved','turns_used':2,'review_hash':review_hash,'statement_hash':row['statement_hash'],'evidence':evidence,'note':'Imported authenticated original submitted effort2/5; priority validation adds zero central proof turns; no synthetic candidate/readiness ledger.','original_effort_import':evidence}
states[K]=imported;dump(B/'state.json',states)
with (B/'history.jsonl').open('a') as h:h.write(json.dumps({**imported,'event':'import_authenticated_submitted_author_effort'},ensure_ascii=False)+'\n')
oldass=json.loads(before['assessments.json']);old=oldass[K]
note='Valid all-prime counterexample and general rank obstruction already follow from Turaev2002 II.3.3/3.4 and II.5.2, DOI10.1007/978-3-0348-7999-6. No substantive new mathematical theorem established; explicit historical application priority remains unresolved. PR124 closed unmerged without paper/DOI/tracker. Original2/5 imported; audit0.'
assessment={**old,'p_solve':0,'p_valid_open':0,'resolution':'already_solved','route':'proof','decision':'exclude','review_policy':'2.0-five-turn-proof','review_type':'fresh full-source mathematical and published-obstruction disposition','review_hash':review_hash,'note':note,'rationale':'The original full-group counterexample and integral proof pass three independent mathematical/source families. New actual book primary pages and two independent fresh source/contribution families show II.3.4 forces p-divisible polynomial-part augmentation while II.5.2 forces a monomial of augmentation1 for the original data. II.3.3 recovers the original general torsion-rank inequality. A fresh disposition adversary accepted the precise old-content classification and comment.','remaining_gap':'No mathematical or source-normalization gap in the old-theorem implication. Express earlier named conjecture refutation and first explicit-application priority are not established; no substantive novel resolution demonstrated. This status is a priority audit exclusion, not an assertion of a known express historical refutation.','first_experiment':'Do not prepare a novel-solution preprint or allocate more proof turns for the existing old direct corollary. Preserve the useful original self-contained proof, exact source bridge, source limits and review seals. A materially new theorem requires a separate exact target.','sources':['https://doi.org/10.1007/978-3-0348-7999-6','https://books.google.com/books?id=83ZJs9Z9BY0C&pg=PA23','https://books.google.com/books?id=83ZJs9Z9BY0C&pg=PA28','https://books.google.com/books?id=83ZJs9Z9BY0C&pg=PA118','https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf'],'original_budget':'2/5','new_central_proof_search_turns':0,'evidence':evidence}
dump(B/'assessment.json',assessment)
run([PY,'-E','-S','-B','-P',str(B/'queue.py'),'assess',K,'--file',str(B/'assessment.json')],B)
run([PY,'-E','-S','-B','-P',str(B/'queue.py'),'status',K,'already_solved','--note',note,'--evidence',str(B/'evidence.json')],B)
afterass,afterstate=load(B/'assessments.json'),load(B/'state.json');aftercatalog={x['id']:x for x in load(B/'catalog.json')}
require({k:v for k,v in afterass.items() if k!=K}=={k:v for k,v in oldass.items() if k!=K},'Other assessment changed')
require({k:v for k,v in afterstate.items() if k!=K}==oldstates,'Other state changed')
require(afterstate[K]['turns_used']==2 and afterstate[K]['status']=='already_solved','Effort/status mismatch')
require(aftercatalog[K]['local_status']=='already_solved' and not aftercatalog[K]['eligible'] and aftercatalog[K]['turns_used']==2,'Target projection')
require(set(catalog)==set(aftercatalog),'Catalog identities changed')
for name in ['history.jsonl','assessment_history.jsonl']:require((B/name).read_bytes().startswith(before[name]),'History prefix modified')
added=[json.loads(s) for s in (B/'history.jsonl').read_bytes()[len(before['history.jsonl']):].decode().splitlines()];aa=[json.loads(s) for s in (B/'assessment_history.jsonl').read_bytes()[len(before['assessment_history.jsonl']):].decode().splitlines()]
require(len(added)==2 and len(aa)==1 and all(x['id']==K for x in added+aa),'History event scope')
require(added[0]['event']=='import_authenticated_submitted_author_effort' and all(x['turns_used']==2 for x in added),'Original effort provenance')
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
spec=importlib.util.spec_from_file_location('pr124_native_queue_writer',B/'queue.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
namespace=dict(module.__dict__);namespace.update(rows=rows,cfg=load(B/'policy.json'),reviews=afterass,state=afterstate)
exec(compile(render,str(B/'queue.py')+':pinned-native-render','exec'),namespace)
for x in load(B/'catalog.json'):
 if x['id']!=K:require({f:v for f,v in x.items() if f!='rank'}=={f:v for f,v in catalog[x['id']].items() if f!='rank'},'Other semantic catalog row changed')
dump(D/'SCOPED_RENDER_RECEIPT.json',{'UTC':now(),'queue_py_sha256':sha((B/'queue.py').read_bytes()),'native_render_code_sha256':sha(render.encode()),'unrelated_catalog_rows_preserved_except_rank':True,'baseline_drift_preserved':len(drift)})
lines=before['QUEUE.md'].decode().splitlines();positions=[i for i,s in enumerate(lines) if '| 10400231 / AMR-103-0231 |' in s];require(len(positions)==1,'Unique campaign row')
i=positions[0];cells=lines[i].split('|');require(cells[8].strip()=='queued' and cells[9].strip()=='0/5','Native campaign baseline')
cells[4],cells[8],cells[9]=' 0.0000 ',' already_solved ',' 2/5 '
cells[11]=' 2026-10-06: Valid counterexample already implied by published Turaev2002 II.3.3/3.4+II.5.2, DOI10.1007/978-3-0348-7999-6. No substantive novel theorem; express historical application priority unresolved. PR124 closed unmerged without paper/DOI/tracker. Original2/5 imported, audit0. '
lines[i]='|'.join(cells)
require([s for j,s in enumerate(lines) if j!=i]==[s for j,s in enumerate(before['QUEUE.md'].decode().splitlines()) if j!=i],'Other campaign row changed')
(B/'QUEUE.md').write_text('\n'.join(lines)+'\n')
dump(N/'assessment.json',assessment);dump(N/'HISTORICAL_DESK_ASSESSMENT.json',old);dump(N/'PRIORITY_EVIDENCE.json',evidence)
(N/'README.md').write_text('# 10400231: published-obstruction priority disposition\n\nStatus: already_solved, scoped to mathematical content already implied by Turaev2002 II.3.3/3.4 and II.5.2, DOI10.1007/978-3-0348-7999-6. The original all-prime counterexample and general rank inequality are valid old direct consequences. An express earlier publication refuting Conjecture12.26 and first explicit-application priority remain unestablished. No substantive new mathematical result was identified.\n\nPR124 closed unmerged: '+closed['closing_comment_url']+'\n\nThe useful original connected-cut proof and its17unchanged bodies are preserved in ../../../draft_pr_publication_program_20260930/audits/pr124_10400231/original_head_authentication_20261006/original_attempt/. Source bridge and primary acquisition limits are in continued_public_access_20261006; independent audits and seals are in the same PR124 audit folder. Original2/5 effort imported; no new proof-search turn, fabricated candidate/readiness, preprint, DOI or tracker row. Extensive AI assistance; no conventional human peer review.\n')
(N/'RESEARCH_LOG.md').write_text('# Published-obstruction disposition log\n\n'+now()+': Mathematics/source100%; old published-content/fresh disposition100%; publication novelty clearance false. Native workflow95% pending actual scoped export, commit/push/full readbacks/release. Original2/5 imported, newproof0. Actual original-head closure verified. Program20/99=20.20%,11published; goalactive.\n')
record={'schema':'pr124-private-prepared-native-published-obstruction-correction/v1','UTC':now(),'actual_operator_PID':os.getpid(),'base_commit':base,'PR':124,'status':'already_solved','classification_scope':evidence['classification_scope'],'express_historical_refutation_established':False,'original_budget':'2/5','new_central_proof_search_turns':0,'full_source_prior_authenticated':True,'original17_unchanged':True,'historical_desk_assessment_preserved':True,'unrelated_assessments_states_and_campaign_rows_preserved':True,'other_catalog_rows_only_rank_may_change':True,'baseline_projection_drift_preserved':len(drift),'native_commands':['assess','status'],'source_inputs':[{'path':prefix+n,'bytes':len(b),'sha256':sha(b),'Git_commit':base} for n,b in before.items()],'cache_snapshot_sha256':sha(cache.read_bytes()),'cache_revision':manifest['revision'],'cache_records':manifest['records'],'closing_comment_url':closed['closing_comment_url'],'same_head_closed_without_merge':True,'publication':False,'DOI':None,'tracker':False,'shared_tracked_files_exported':False,'primary_checkout_mutated':False,'native_export_pending_fresh_writer_grant':True}
dump(N/'DISPOSITION.json',record)
export=['assessments.json','state.json','history.jsonl','assessment_history.jsonl','catalog.json','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md']
record['proposed_native_pins']=[{'path':prefix+n,'prepared_local_path':str(B/n),'bytes':(B/n).stat().st_size,'sha256':sha((B/n).read_bytes())} for n in export]+[{'path':prefix+'attempts/'+K+'/'+p.name,'prepared_local_path':str(p),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(N.iterdir())]
dump(D/'PREPARED_RECEIPT.json',record)
print(json.dumps({k:v for k,v in record.items() if k not in ['proposed_native_pins','source_inputs']},sort_keys=True))
