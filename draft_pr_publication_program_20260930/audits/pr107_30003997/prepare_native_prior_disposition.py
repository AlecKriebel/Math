"""Run source-bound native correction in a private backend, preserving other targets."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,os,sqlite3,subprocess,sys,textwrap
A=Path(__file__).resolve().parent;C=A.parents[2];R=Path('/Users/alec/Documents/Math');K='30003997'
D=A/'native_prior_disposition_20261006';D.mkdir(exist_ok=False);B=D/'private_backend';B.mkdir();records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(c,m):
 if not c:raise RuntimeError(m)
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(argv,cwd=C,body_only=False):
 start=now();p=subprocess.Popen(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();i=len(records)
 if not body_only:(D/(str(i)+'.stdout.bin')).write_bytes(out)
 (D/(str(i)+'.stderr.bin')).write_bytes(err)
 records.append({'argv':argv,'cwd':str(cwd),'PID':p.pid,'UTC_start':start,'UTC_end':now(),'exit_code':p.returncode,'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stdout_file':None if body_only else str(i)+'.stdout.bin','large_git_blob_not_duplicated':body_only,'stderr_file':str(i)+'.stderr.bin','stderr_sha256':hashlib.sha256(err).hexdigest()})
 dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'records':records});require(p.returncode==0,err.decode('utf8','replace')[:1200]);return out
def git(*args,body=False):return run(['/usr/bin/git',*args],body_only=body)
ready=load(A/'ROOT_DISPOSITION_READY_20261006.json');closed=load(A/'actual_closure_20261006/RECEIPT.json')
require(ready['fresh_final_disposition_review_authenticated'] and ready['native_status_correction_supported'],'gate')
require(closed['same_head_closed_without_merge'] and closed['original_head']==ready['original_head'],'actual closure')
require(git('symbolic-ref','--short','HEAD').strip()==b'main','notmain');base=git('rev-parse','HEAD').strip().decode()
require(base==sys.argv[1],'main advanced; reconcile first')
require(git('ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main').decode().split()[0]==base,'remote advanced')
require(not git('diff','--cached','--name-only','-z'),'foreign staged')
prefix='unsolved_math_prioritization/';N=C/prefix/'attempts'/K
require(not N.exists() and not git('ls-tree','-r','--name-only',base,'--',str(N.relative_to(C))),'existing native attempt')
names=['queue.py','manifest.json','policy.json','catalog.json','assessments.json','state.json','history.jsonl','assessment_history.jsonl','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md'];before={};inputpins=[]
for name in names:
 data=git('show',base+':'+prefix+name,body=True);before[name]=data;q=C/prefix/name
 require(not q.is_symlink() and (not q.exists() or q.read_bytes()==data),'unknown worktree edit: '+name)
 (B/name).write_bytes(data);inputpins.append({'path':prefix+name,'git_commit':base,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(B/'cache').mkdir();cache=B/'cache/catalog.sqlite'
run(['/bin/cp','-c',str(R/prefix/'cache/catalog.sqlite'),str(cache)])
manifest=load(B/'manifest.json');db=sqlite3.connect('file:'+str(cache)+'?mode=ro',uri=True)
require(db.execute('SELECT revision FROM metadata').fetchone()==(manifest['revision'],),'cache revision')
require(db.execute('SELECT count(*) FROM records').fetchone()[0]==manifest['records'],'cache count')
payload,prior=db.execute('SELECT payload,report FROM records WHERE key=?',(K,)).fetchone();db.close()
require(json.loads(prior)=={},'unexpected prior report; no-join normalization')
review_hash=hashlib.sha256(json.dumps([json.loads(payload),json.loads(prior)],sort_keys=True).encode()).hexdigest()
oldrows=json.loads(before['catalog.json']);catalog={x['id']:x for x in oldrows};row=catalog[K]
require(review_hash==row['review_hash']=='806c5596635c33619f1a907f0c98bf4762c7cbe77ad8cb384b50d50659e80359','source pair')
O=A/'original_source_authentication_20261006/original_attempt';turns=[json.loads(t) for t in (O/'turns.jsonl').read_text().splitlines()]
require(load(O/'status.json')['substantive_approaches']==1 and [x['turn'] for x in turns]==[1],'original effort')
require(sha(O/'PROOF.md')=='2c219bf80ad4bbba75f8c70169b26b7e9b11b6f5e1742543f25d9cb0d0c5ebe8','original proof changed')
states=json.loads(before['state.json']);require(K not in states,'prior native state needs separate adjudication')
evidence={'review_hash':review_hash,'exact_claim':ready['exact_claim'],'prior_reconstruction':str((A/'ROOT_PRIORITY_ADJUDICATION_20261006.md').relative_to(C)),'fresh_independent_review':str((A/'fresh_prior_disposition_adversary_20261006/REPORT.md').relative_to(C)),'original_head':ready['original_head'],'original_archive':str(O.relative_to(C)),'original_proof_sha256':sha(O/'PROOF.md'),'original_turns_sha256':sha(O/'turns.jsonl'),'current_effective_audit_package':str((A/'repaired_diagnostics_v2').relative_to(C)),'original_effort_imported':1,'extra_central_proof_search_turns':0,'exact_prior_cost_table_printing_verified':False,'earliest_priority_verified':False,'exact_general_3SAT_optimum_identity_priority':'unresolved; substantive novelty not established','closed_PR_comment':closed['closing_comment_url']}
dump(B/'evidence.json',evidence)
imported={'at':now(),'id':K,'status':'already_solved','turns_used':1,'review_hash':review_hash,'statement_hash':row['statement_hash'],'note':'Imported authenticated original author effort1/5; no new central proof turn.','original_effort_import':evidence,'evidence':evidence}
states[K]=imported;dump(B/'state.json',states)
with (B/'history.jsonl').open('a') as f:f.write(json.dumps({**imported,'event':'import_authenticated_submitted_author_effort'},ensure_ascii=False)+'\n')
oldass=json.loads(before['assessments.json']);old=oldass[K]
note='Already solved as a checkable elementary corollary of Chapoullie–Szigeti2022 Theorem13 proof: complete fixed-root destination-cost hardness bundle, including binary0/1, simple reachable depth3 layered DAG, nonroot indegree<=3, and positive1/2 offset. Candidate math verified after minor guard/preprocessing repairs; no substantive new contribution established. Exact earliest cost-table wording and general3SAT optimum identity priority unresolved. Original1/5 imported; audit proof turns0.'
assessment={**old,'impact':old['impact'],'p_solve':0,'p_valid_open':0,'resolution':'already_solved','review_policy':'2.0-five-turn-proof','route':'proof','decision':'exclude','review_type':'fresh source-bound mathematical and priority correction','review_hash':review_hash,'note':note,'rationale':'Three independent mathematical families and three distinct priority families, followed by a fresh disposition adversary, support mathematical validity but a prior-corollary classification. The explicit selector subdivision and destination mismatch prices recover every advertised hardness restriction from the published2022 RXC3 construction.','remaining_gap':'No unresolved gap in the literal source hardness target or advertised restriction bundle. Earliest/verbatim priority and the exact all-formula minimum-unsatisfied-clause identity are unverified; no substantive novelty or independent approximation result established.','first_experiment':'Do not allocate a new proof attempt to the resolved hardness target. Retain the frozen direct proof, exact optimum correspondence, current exception-guard diagnostics and checkable prior transformation. Any separately consequential strengthening needs a newly scoped target and source-bound priority audit.','sources':['https://ems.press/content/serial-article-files/46772','https://doi.org/10.1016/j.disopt.2022.100702','https://arxiv.org/abs/2203.01096v1','https://pagesperso.g-scop.grenoble-inp.fr/~szigetiz/OCG/13.C-Szigeti.pdf'],'original_budget':'1/5','new_central_proof_search_turns':0,'evidence':evidence}
dump(B/'assessment.json',assessment);py='/opt/homebrew/bin/python3'
run([py,'-E','-B',str(B/'queue.py'),'assess',K,'--file',str(B/'assessment.json')],B)
run([py,'-E','-B',str(B/'queue.py'),'status',K,'already_solved','--note',note,'--evidence',str(B/'evidence.json')],B)
afterass=load(B/'assessments.json');afterstate=load(B/'state.json');regenerated=load(B/'catalog.json');aftercatalog={x['id']:x for x in regenerated}
require({k:v for k,v in afterass.items() if k!=K}=={k:v for k,v in oldass.items() if k!=K},'other assessment changed')
require({k:v for k,v in afterstate.items() if k!=K}==json.loads(before['state.json']),'other state changed')
require(afterstate[K]['turns_used']==1 and afterstate[K]['status']=='already_solved','effort/status')
require(aftercatalog[K]['local_status']=='already_solved' and not aftercatalog[K]['eligible'] and aftercatalog[K]['turns_used']==1,'target catalog')
require(set(catalog)==set(aftercatalog),'catalog identities')
for name in ['history.jsonl','assessment_history.jsonl']:require((B/name).read_bytes().startswith(before[name]),'historical prefix changed')
extra=[json.loads(t) for t in (B/'history.jsonl').read_bytes()[len(before['history.jsonl']):].decode().splitlines()]
extraass=[json.loads(t) for t in (B/'assessment_history.jsonl').read_bytes()[len(before['assessment_history.jsonl']):].decode().splitlines()]
require(len(extra)==2 and len(extraass)==1 and all(x['id']==K for x in extra+extraass),'new event scope')
require(extra[0]['event']=='import_authenticated_submitted_author_effort' and all(x['turns_used']==1 for x in extra),'imported effort ledger')
# Native regeneration can refresh stale projections of unchanged other states.
# Record those, preserving their baseline semantic rows instead of processing them.
drift=[]
for key,oldrow in catalog.items():
 if key==K:continue
 diff={f:{'before':oldrow.get(f),'after':aftercatalog[key].get(f)} for f in set(oldrow)|set(aftercatalog[key]) if f!='rank' and oldrow.get(f)!=aftercatalog[key].get(f)}
 if diff:
  require(set(diff)<=set(['local_status','eligible','turns_used']),'unexplained source/score drift: '+key)
  st=afterstate.get(key,{});require(aftercatalog[key]['local_status']==st['status'] and aftercatalog[key]['turns_used']==st.get('turns_used',0),'unexplained state projection: '+key)
  drift.append({'id':key,'difference':diff,'baseline_preserved':True})
dump(D/'UNRELATED_BASELINE_PROJECTION_DRIFT.json',{'base_commit':base,'count':len(drift),'differences':drift,'other_targets_not_reassessed':True})
rawpins={name:sha(B/name) for name in ['catalog.json','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md']}
rows=[dict(aftercatalog[K]) if x['id']==K else dict(x) for x in oldrows];rows.sort(key=lambda x:(not x['eligible'],-x['ev'],x['id']))
for i,x in enumerate([x for x in rows if x['eligible']],1):x['rank']=i
for x in rows:
 if not x['eligible']:x['rank']=None
text=(B/'queue.py').read_text();start=text.index("    write(ROOT/'catalog.json',rows)");end=text.index('def seen_ids',start);render=textwrap.dedent(text[start:end])
spec=importlib.util.spec_from_file_location('pr107_native_queue_writer',B/'queue.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
namespace=dict(mod.__dict__);namespace.update(rows=rows,cfg=load(B/'policy.json'),reviews=afterass,state=afterstate);exec(compile(render,str(B/'queue.py')+':pinned-native-render','exec'),namespace)
for x in load(B/'catalog.json'):
 if x['id']!=K:require({f:v for f,v in x.items() if f!='rank'}=={f:v for f,v in catalog[x['id']].items() if f!='rank'},'other catalog changed after overlay')
dump(D/'SCOPED_RENDER_RECEIPT.json',{'UTC':now(),'queue_py_sha256':sha(B/'queue.py'),'native_render_code_sha256':hashlib.sha256(render.encode()).hexdigest(),'raw_generated_pins':rawpins,'other_catalog_rows_semantically_preserved_except_rank':True,'baseline_drift_count':len(drift)})
generated_queue=(B/'QUEUE.md').read_bytes();lines=before['QUEUE.md'].decode().splitlines();ids=[i for i,s in enumerate(lines) if '| 30003997 / OWR-16633-014 |' in s];require(len(ids)==1,'unique campaign row');i=ids[0];cells=lines[i].split('|')
require(cells[8].strip()=='queued' and cells[9].strip()=='0/5','campaign baseline changed');cells[4]=' 0.0000 ';cells[8]=' already_solved ';cells[9]=' 1/5 '
cells[11]=' 2026-10-06: Math verified; complete restricted destination-cost hardness is a checkable corollary of Chapoullie–Szigeti2022 Thm13 via selector subdivision/mismatch prices. Exact cost-table printing/earliest priority and general3SAT optimum identity priority unresolved; substantive novelty not established. PR107 closed without merge/new paper after fresh adversary. Original1/5 imported; audit0; no DOI/tracker. '
lines[i]='|'.join(cells);(B/'QUEUE.md').write_text('\n'.join(lines)+'\n');require([s for j,s in enumerate(lines) if j!=i]==[s for j,s in enumerate(before['QUEUE.md'].decode().splitlines()) if j!=i],'other campaign rows changed')
N.mkdir(parents=True);dump(N/'assessment.json',assessment);dump(N/'HISTORICAL_DESK_ASSESSMENT.json',old);dump(N/'PRIORITY_EVIDENCE.json',evidence)
(N/'README.md').write_text('# 30003997: prior destination-cost arborescence hardness\n\nStatus: already_solved as an elementary corollary of Chapoullié–Szigeti2022 Theorem13 construction. The direct3SAT candidate passed independent mathematical audits after minor guard/preprocessing repairs. The entire advertised binary/depth3/indegree3/positive-offset hardness bundle is covered by the [checkable prior comparison](../../../draft_pr_publication_program_20260930/audits/pr107_30003997/ROOT_PRIORITY_ADJUDICATION_20261006.md). Exact earliest/verbatim cost-table priority and the general3SAT optimum identity priority remain unresolved; no substantive new contribution is established.\n\nPR107 closed without merging or a new publication: '+closed['closing_comment_url']+'\n\nThe immutable original proof/one-entry1/5 ledger are preserved in the linked audit, and the current effective package is repaired_diagnostics_v2. No new central proof-search turn, paper, DOI or tracker row. Extensive AI-assisted verification occurred; no conventional human peer review is claimed.\n')
(N/'RESEARCH_LOG.md').write_text('# 30003997 disposition log\n\n'+now()+': Mathematical audit100%; bounded prior-corollary audit100%; disposition95% pending committed/remote native readback. Original effort1/5 imported, new proof turns0. Three distinct mathematical families, three priority families and fresh disposition adversary support mathematically valid prior result. Same-head PR closure verified, no merge/paper/DOI/tracker. Exact optimum identity retained with historical priority unresolved.\n')
export=['assessments.json','state.json','history.jsonl','assessment_history.jsonl','catalog.json','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md']
for name in export:
 out=C/prefix/name;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes((B/name).read_bytes())
result={'schema':'pr107-native-prior-disposition-prepared/v1','UTC':now(),'actual_operator_PID':os.getpid(),'PR':107,'problem_id':30003997,'base_commit':base,'status':'already_solved','scope':'literal destination-cost hardness and full advertised restriction bundle as published-construction corollary','source_review_hash':review_hash,'original_budget':'1/5','budget_import_not_new_proof_response':True,'new_central_proof_search_turns':0,'historical_desk_assessment_preserved':True,'other_native_targets_preserved':True,'catalog_only_other_rank_positions_may_change':True,'baseline_existing_state_projection_drift_preserved':len(drift),'other_campaign_rows_byte_preserved':True,'native_commands':['assess','status'],'source_inputs':inputpins,'cache_snapshot_revision':manifest['revision'],'cache_snapshot_bytes':cache.stat().st_size,'cache_snapshot_sha256':sha(cache),'native_generated_queue_sha256_before_campaign_overlay':hashlib.sha256(generated_queue).hexdigest(),'closing_comment_url':closed['closing_comment_url'],'same_head_closed_without_merge':True,'publication':False,'DOI':None,'tracker':False,'main_checkpoint_pending':True,'primary_checkout_mutated':False}
dump(N/'DISPOSITION.json',result);paths=[C/prefix/n for n in export]+[f for f in N.iterdir() if f.is_file()];result['native_paths']=[str(p.relative_to(C)) for p in paths];result['native_pins']=[{'path':str(p.relative_to(C)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in paths]
dump(D/'PREPARED_RECEIPT.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ['source_inputs','native_paths','native_pins']}))
