"""Additive source-bound correction; execute after fresh gate and actual closure."""
from pathlib import Path
import datetime, hashlib, importlib.util, json, os, sqlite3, subprocess, sys, textwrap
A=Path(__file__).resolve().parent
C=A.parents[2]
P=A.parent.parent
R=Path('/Users/alec/Documents/Math')
K='30001234'
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'
PY='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
D=A/'native_exact_prior_disposition_20261006'
B=D/'private_backend'
records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(value,label):
    if not value:raise ValueError(label)
def load(path):return json.loads(path.read_text())
def dump(path,obj):path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
def digest(body):return hashlib.sha256(body).hexdigest()
def sha(path):return digest(path.read_bytes())
def run(argv,cwd=C):
    start=now();child=subprocess.Popen(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate()
    records.append({'argv':argv,'cwd':str(cwd),'PID':child.pid,'UTC_start':start,'UTC_end':now(),
      'exit_code':child.returncode,'stdout_bytes':len(out),'stdout_sha256':digest(out),
      'stderr_bytes':len(err),'stderr_sha256':digest(err),'stderr':err.decode('utf-8','replace')[:1200]})
    dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'records':records})
    require(child.returncode==0,'Actual command failed; inspect native journal before retry')
    return out
def git(*args):return run([GIT,*args])
require(not D.exists(),'Existing native run; inspect rather than repeat')
ready=load(A/'ROOT_DISPOSITION_READY_20261006.json')
closed=load(A/'actual_closure_20261006/RECEIPT.json')
window=load(A/'ACTUAL_WRITER_HANDOFF_20261006.json')
require(window['explicit_release_received'],'Actual main writer handoff absent')
require(ready['fresh_disposition_review_PASS'] and ready['native_status_correction_supported'],'Fresh disposition gate')
require(closed['same_head_closed_without_merge'] and closed['original_head']==ready['original_head'],'Actual same-head closure absent')
D.mkdir();B.mkdir();(D/'.gitignore').write_text('private_backend/\n')
require(git('branch','--show-current').strip()==b'main','Not main')
base=git('rev-parse','HEAD').decode().strip()
require(base==sys.argv[1],'Main advanced; reconcile first')
require(git('ls-remote','origin','refs/heads/main').decode().split()[0]==base,'Remote advanced')
require(not git('diff','--cached','--name-only'),'Index not empty')
prefix='unsolved_math_prioritization/'
N=C/prefix/'attempts'/K
require(not N.exists() and not git('ls-tree','-r','--name-only',base,'--',str(N.relative_to(C))),'Existing native attempt requires reconciliation')
names=['queue.py','manifest.json','policy.json','catalog.json','assessments.json','state.json','history.jsonl','assessment_history.jsonl','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md']
before={}
for name in names:
    data=git('show',base+':'+prefix+name);before[name]=data
    current=C/prefix/name
    require(not current.is_symlink() and (not current.exists() or current.read_bytes()==data),'Unknown native worktree edit '+name)
    (B/name).write_bytes(data)
(B/'cache').mkdir();cache=B/'cache/catalog.sqlite'
run(['/bin/cp','-c',str(R/prefix/'cache/catalog.sqlite'),str(cache)])
manifest=load(B/'manifest.json')
db=sqlite3.connect('file:'+str(cache)+'?mode=ro',uri=True)
require(db.execute('SELECT revision FROM metadata').fetchone()==(manifest['revision'],),'Cache revision')
require(db.execute('SELECT count(*) FROM records').fetchone()[0]==manifest['records'],'Cache count')
raw,report=db.execute('SELECT payload,report FROM records WHERE key=?',(K,)).fetchone();db.close()
source,prior=json.loads(raw),json.loads(report)
F=A/'original_head_authentication_20261006';O=F/'original_attempt'
require(source==load(O/'source_record.json') and source==load(F/'SOURCE_STATEMENT.json') and prior==load(F/'PRIOR_REPORT.json'),'Complete immutable source/prior mismatch')
review_hash=digest(json.dumps([source,prior],sort_keys=True).encode())
oldrows=json.loads(before['catalog.json']);catalog={row['id']:row for row in oldrows};row=catalog[K]
require(review_hash==row['review_hash']=='6ff8253c57c5544f0b33ac8a6303be8ec7f42ac0f5ce6b4976a8149ae1b28152','Exact source binding')
auth=load(F/'ORIGINAL_AUTHENTICATION.json')
require(auth['original_budget']=='1/5' and auth['original_literal_status']=='claimed_solved','Authenticated original effort')
for item in auth['original_files']:
    path=O/item['path'];require(path.stat().st_size==item['bytes'] and sha(path)==item['sha256'],'Original file changed '+item['path'])
states=json.loads(before['state.json']);require(K not in states,'Existing native state requires reconciliation')
evidence={'review_hash':review_hash,'exact_claim':source['statement'],
 'classification_scope':'Exact original singleton-augmented-image optimizer question already has the identical published counterexample in Takagi Example4.4, arXiv2011/published2013.',
 'original_head':ready['original_head'],'original_effort_imported':1,'original_budget':'1/5',
 'effort_provenance':str((F/'ORIGINAL_AUTHENTICATION.json').relative_to(C)),
 'original_proof_sha256':sha(O/'CANDIDATE.md'),'original_archive':str(O.relative_to(C)),
 'mathematical_gate':str((A/'MATHEMATICAL_SOURCE_GATE_20261006.json').relative_to(C)),
 'priority_reasoning':str((A/'ROOT_PRIORITY_DISPOSITION_20261006.md').relative_to(C)),
 'fresh_review':ready['fresh_disposition_review'],'closed_PR_comment':closed['closing_comment_url'],
 'published_DOI':'10.2140/ant.2013.7.917','earlier_version':'https://arxiv.org/abs/1105.0072v1',
 'earlier_disclosure_UTC':'2011-04-30T10:42:16Z','exact_prior_same_example_authenticated':True,
 'mathematics_valid':True,'complete_face_exposition_and_verification_useful':True,
 'substantive_novel_open_problem_resolution_established':False,
 'new_central_proof_search_turns':0,'no_fabricated_proof_turns_or_readiness':True}
dump(B/'evidence.json',evidence)
imported={'at':now(),'id':K,'status':'already_solved','turns_used':1,'review_hash':review_hash,
 'statement_hash':row['statement_hash'],'evidence':evidence,
 'note':'Imported authenticated submitted original effort1/5; no new proof turn or synthetic readiness/candidate ledger.',
 'original_effort_import':evidence}
states[K]=imported;dump(B/'state.json',states)
with (B/'history.jsonl').open('a') as h:h.write(json.dumps({**imported,'event':'import_authenticated_submitted_author_effort'},ensure_ascii=False)+'\n')
oldass=json.loads(before['assessments.json']);old=oldass[K]
note='Exact singleton-fiber question already answered by the SAME three-minor example in Takagi2011 Example4.4/p19 and2013 Example4.4/p940, DOI10.2140/ant.2013.7.917. Current full-face proof/ideal checks valid useful exposition; no substantive novel resolution established. PR117 closed unmerged, no new paper/DOI/tracker. Original1/5 imported; audit0.'
assessment={**old,'p_solve':0,'p_valid_open':0,'resolution':'already_solved','route':'proof','decision':'exclude',
 'review_policy':'2.0-five-turn-proof','review_type':'fresh full-source mathematical and explicit-prior disposition',
 'review_hash':review_hash,'note':note,
 'rationale':'Root and three independent math/source families verify the complete counterexample. Three independent priority families and a fresh disposition adversary identify explicit prior same-example failure of the same rational singleton-fiber condition. Ambient c=0 and exact interleaving/third sign swap preserve every constraint, objective and augmented-image fiber. The dated imported openness assessment is superseded by actual2011/2013 primary bodies.',
 'remaining_gap':'No mathematical gap in the verified elementary counterexample or exact prior scope match. No substantive new original-target resolution established; no inaccessible source is needed for this priority disposition. Earliest possible disclosure globally is not asserted.',
 'first_experiment':'Do not allocate further proof turns or prepare a novel-solution preprint for this identical known counterexample. Preserve the original proof/ledger and attributed direct full-face verification. A materially new theorem needs a separate exact target and bounded research process.',
 'sources':['https://arxiv.org/abs/1105.0072v1','https://msp.org/ant/2013/7-4/ant-v7-n4-p06-s.pdf','https://doi.org/10.2140/ant.2013.7.917','https://arxiv.org/pdf/0810.1278v3','https://ems.press/content/serial-article-files/46224'],
 'original_budget':'1/5','new_central_proof_search_turns':0,'evidence':evidence}
dump(B/'assessment.json',assessment)
run([PY,'-E','-S','-B','-P',str(B/'queue.py'),'assess',K,'--file',str(B/'assessment.json')],B)
run([PY,'-E','-S','-B','-P',str(B/'queue.py'),'status',K,'already_solved','--note',note,'--evidence',str(B/'evidence.json')],B)
afterass,afterstate=load(B/'assessments.json'),load(B/'state.json')
aftercatalog={x['id']:x for x in load(B/'catalog.json')}
require({k:v for k,v in afterass.items() if k!=K}=={k:v for k,v in oldass.items() if k!=K},'Unrelated assessments changed')
require({k:v for k,v in afterstate.items() if k!=K}==json.loads(before['state.json']),'Unrelated states changed')
require(afterstate[K]['turns_used']==1 and afterstate[K]['status']=='already_solved','Status/effort mismatch')
require(aftercatalog[K]['local_status']=='already_solved' and not aftercatalog[K]['eligible'] and aftercatalog[K]['turns_used']==1,'Target catalog mismatch')
require(set(catalog)==set(aftercatalog),'Catalog identities changed')
for name in ['history.jsonl','assessment_history.jsonl']:require((B/name).read_bytes().startswith(before[name]),'Historical prefix modified')
added=[json.loads(s) for s in (B/'history.jsonl').read_bytes()[len(before['history.jsonl']):].decode().splitlines()]
aa=[json.loads(s) for s in (B/'assessment_history.jsonl').read_bytes()[len(before['assessment_history.jsonl']):].decode().splitlines()]
require(len(added)==2 and len(aa)==1 and all(x['id']==K for x in added+aa),'Historical event scope')
require(added[0]['event']=='import_authenticated_submitted_author_effort' and all(x['turns_used']==1 for x in added),'Original-effort import mismatch')
drift=[]
for key,oldrow in catalog.items():
    if key==K:continue
    difference={f:{'before':oldrow.get(f),'after':aftercatalog[key].get(f)} for f in set(oldrow)|set(aftercatalog[key]) if f!='rank' and oldrow.get(f)!=aftercatalog[key].get(f)}
    if difference:
        require(set(difference)<={'local_status','eligible','turns_used'},'Unexplained unrelated projection drift '+key)
        st=afterstate.get(key,{})
        require(aftercatalog[key]['local_status']==st['status'] and aftercatalog[key]['turns_used']==st.get('turns_used',0),'Unexplained state projection '+key)
        drift.append({'id':key,'difference':difference,'baseline_preserved':True})
dump(D/'UNRELATED_BASELINE_PROJECTION_DRIFT.json',{'base_commit':base,'differences':drift,'other_targets_not_reassessed':True})
rows=[dict(aftercatalog[K]) if x['id']==K else dict(x) for x in oldrows]
rows.sort(key=lambda x:(not x['eligible'],-x['ev'],x['id']))
for i,x in enumerate([x for x in rows if x['eligible']],1):x['rank']=i
for x in rows:
    if not x['eligible']:x['rank']=None
code=(B/'queue.py').read_text()
render=textwrap.dedent(code[code.index("    write(ROOT/'catalog.json',rows)"):code.index('def seen_ids')])
spec=importlib.util.spec_from_file_location('pr117_native_queue_writer',B/'queue.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
namespace=dict(module.__dict__);namespace.update(rows=rows,cfg=load(B/'policy.json'),reviews=afterass,state=afterstate)
exec(compile(render,str(B/'queue.py')+':pinned-native-render','exec'),namespace)
for x in load(B/'catalog.json'):
    if x['id']!=K:require({f:v for f,v in x.items() if f!='rank'}=={f:v for f,v in catalog[x['id']].items() if f!='rank'},'Unrelated semantic row changed')
dump(D/'SCOPED_RENDER_RECEIPT.json',{'UTC':now(),'queue_py_sha256':sha(B/'queue.py'),'native_render_code_sha256':digest(render.encode()),'unrelated_catalog_rows_preserved_except_rank':True,'baseline_drift_preserved':len(drift)})
lines=before['QUEUE.md'].decode().splitlines()
positions=[i for i,s in enumerate(lines) if '| 30001234 / OWR-3471-008 |' in s]
require(len(positions)==1,'Unique campaign row')
i=positions[0];cells=lines[i].split('|')
require(cells[8].strip()=='queued' and cells[9].strip()=='0/5','Native campaign baseline changed')
cells[4],cells[8],cells[9]=' 0.0000 ',' already_solved ',' 1/5 '
cells[11]=' 2026-10-06: Exact singleton-fiber counterexample already in Takagi2011/2013 Example4.4, DOI10.2140/ant.2013.7.917. Current proof and complete optimal segment verified, useful exposition; no novel resolution. PR117 closed unmerged without paper/DOI/tracker. Original1/5 imported, audit0. '
lines[i]='|'.join(cells)
require([s for j,s in enumerate(lines) if j!=i]==[s for j,s in enumerate(before['QUEUE.md'].decode().splitlines()) if j!=i],'Unrelated campaign row changed')
(B/'QUEUE.md').write_text('\n'.join(lines)+'\n')
N.mkdir(parents=True)
dump(N/'assessment.json',assessment);dump(N/'HISTORICAL_DESK_ASSESSMENT.json',old);dump(N/'PRIORITY_EVIDENCE.json',evidence)
(N/'README.md').write_text('# 30001234: explicit prior counterexample\n\nStatus: already_solved for the exact original rational singleton-augmented-image optimizer question. Takagi Example4.4 already gives the same three-minor ideal in arXiv1105.0072v1 (30April2011), p19, and Algebra & Number Theory7(4)(2013), p940, DOI10.2140/ant.2013.7.917. The ambient c=0 and third generator sign/column permutation preserve the literal program.\n\nThe current elementary full optimal segment, polynomial ideal/minimality checks and diagnostics are mathematically valid useful exposition, without an established substantive novel resolution. PR117 closed unmerged: '+closed['closing_comment_url']+'\n\nAll original20 bodies and authenticated1/5 ledger remain preserved in ../../../draft_pr_publication_program_20260930/audits/pr117_30001234/original_head_authentication_20261006/original_attempt/. Effective guard-only diagnostics and all independent audits are retained separately. No synthetic readiness/candidate events, new central proof turns, preprint, DOI, or tracker row. Extensive AI assistance used in verification; no conventional human peer review claimed.\n')
(N/'RESEARCH_LOG.md').write_text('# Explicit prior disposition log\n\n'+now()+': Mathematics/source100%; exact published-prior and fresh disposition100%; publication novelty clearance false. Native workflow95% pending actual commit/remote full readbacks. Original1/5 imported, proof-search turns0. Same-head closure actual verified; program19/99=19.19%,11published; persistent goal active.\n')
export=['assessments.json','state.json','history.jsonl','assessment_history.jsonl','catalog.json','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md']
for name in export:
    out=C/prefix/name;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes((B/name).read_bytes())
record={'schema':'pr117-native-exact-prior-correction/v1','UTC':now(),'actual_operator_PID':os.getpid(),
 'base_commit':base,'PR':117,'status':'already_solved','original_budget':'1/5','new_central_proof_search_turns':0,
 'original_effort_import_not_new_proof_event':True,'scope':evidence['classification_scope'],
 'source_review_hash':review_hash,'full_source_and_prior_authenticated':True,'historical_desk_assessment_preserved':True,
 'all20_original_files_unchanged':True,'unrelated_assessments_states_and_campaign_rows_preserved':True,
 'other_catalog_rows_only_rank_may_change':True,'baseline_projection_drift_preserved':len(drift),'native_commands':['assess','status'],
 'source_inputs':[{'path':prefix+name,'bytes':len(body),'sha256':digest(body),'Git_commit':base} for name,body in before.items()],
 'cache_snapshot_sha256':sha(cache),'cache_revision':manifest['revision'],'cache_records':manifest['records'],
 'closing_comment_url':closed['closing_comment_url'],'same_head_closed_without_merge':True,
 'publication':False,'DOI':None,'tracker':False,'main_checkpoint_pending':True,'primary_checkout_mutated':False}
dump(N/'DISPOSITION.json',record)
paths=[C/prefix/name for name in export]+[path for path in N.iterdir() if path.is_file()]
record['native_pins']=[{'path':str(path.relative_to(C)),'bytes':path.stat().st_size,'sha256':sha(path)} for path in paths]
dump(D/'PREPARED_RECEIPT.json',record)
print(json.dumps({k:v for k,v in record.items() if k not in {'source_inputs','native_pins'}},sort_keys=True))
