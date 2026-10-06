"""Source-bound assessment and import of original effort in an isolated backend."""
from pathlib import Path
import datetime, hashlib, json, os, sqlite3, subprocess
A=Path(__file__).resolve().parent;C=A.parents[2];P=A.parents[1]
R=Path('/Users/alec/Documents/Math');K='600008'
D=A/'native_prior_disposition_20261006_retry1';D.mkdir(exist_ok=False)
B=D/'private_backend';B.mkdir();records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def run(argv,cwd=C,body_only=False):
    start=now();p=subprocess.Popen(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate();i=len(records)
    # Large repository inputs remain recoverable immutable Git blobs, not duplicate raw files.
    if not body_only:(D/(str(i)+'.stdout.bin')).write_bytes(out)
    (D/(str(i)+'.stderr.bin')).write_bytes(err)
    records.append({'argv':argv,'cwd':str(cwd),'PID':p.pid,'UTC_start':start,'UTC_end':now(),
        'exit_code':p.returncode,'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),
        'stdout_file':None if body_only else str(i)+'.stdout.bin','large_git_blob_not_duplicated':body_only,
        'stderr_file':str(i)+'.stderr.bin','stderr_sha256':hashlib.sha256(err).hexdigest()})
    dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'records':records})
    require(p.returncode==0,err.decode('utf8','replace')[:1200]);return out
def git(*args,body=False):return run(['/usr/bin/git',*args],body_only=body)
ready=load(A/'ROOT_DISPOSITION_READY_20261006.json');closed=load(A/'actual_closure_20261006/RECEIPT.json')
require(ready['fresh_final_disposition_review_authenticated'] and ready['native_status_correction_supported'],'gate')
require(closed['same_head_closed_without_merge'] and closed['PR_after']['headRefOid']==ready['original_head'],'actual closure')
require(git('symbolic-ref','--short','HEAD').strip()==b'main','notmain')
base=git('rev-parse','HEAD').strip().decode()
require(base=='dd742176bcb997caf788f73594fcd9f9dea236fd','main advanced; reconcile first')
require(git('ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main').decode().split()[0]==base,'remote advanced')
require(not git('diff','--cached','--name-only','-z'),'foreign staged')
prefix='unsolved_math_prioritization/'
N=C/prefix/'attempts'/K
require(not N.exists() and not git('ls-tree','-r','--name-only',base,'--',str(N.relative_to(C))), 'existing native attempt')
names=['queue.py','manifest.json','policy.json','catalog.json','assessments.json','state.json','history.jsonl',
       'assessment_history.jsonl','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md']
before={};pins=[]
for name in names:
    data=git('show',base+':'+prefix+name,body=True);before[name]=data
    q=C/prefix/name
    require(not q.is_symlink() and (not q.exists() or q.read_bytes()==data),'unknown worktree edit: '+name)
    (B/name).write_bytes(data)
    pins.append({'path':prefix+name,'git_commit':base,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(B/'cache').mkdir()
source_cache=R/prefix/'cache/catalog.sqlite';cache=B/'cache/catalog.sqlite'
# APFS clone is a private copy-on-write snapshot and does not write the primary cache.
run(['/bin/cp','-c',str(source_cache),str(cache)])
manifest=load(B/'manifest.json')
db=sqlite3.connect('file:'+str(cache)+'?mode=ro',uri=True)
require(db.execute('SELECT revision FROM metadata').fetchone()==(manifest['revision'],),'cache revision')
require(db.execute('SELECT count(*) FROM records').fetchone()[0]==manifest['records'],'cache count')
payload,prior=db.execute('SELECT payload,report FROM records WHERE key=?',(K,)).fetchone();db.close()
review_hash=hashlib.sha256(json.dumps([json.loads(payload),json.loads(prior)],sort_keys=True).encode()).hexdigest()
catalog={x['id']:x for x in json.loads(before['catalog.json'])};row=catalog[K]
require(review_hash==row['review_hash']=='597672d96f2b12dc802c798cbd01e1d224329f4f3a277e65514b429354103663','source pair')
original=A/'original_source_authentication_20261006/original_attempt'
source=load(original/'status.json');turns=[json.loads(t) for t in (original/'turns.jsonl').read_text().splitlines()]
require(source['substantive_approaches']==1 and [t['turn'] for t in turns]==[1],'original effort')
require(sha(original/'ANALYTIC_CRITERION.md')=='608217a2ffc120a965b165f5b6065edd83f8cf94c5e77f0f95a0326640db2dae','proof changed')
states=json.loads(before['state.json']);require(K not in states,'prior native state needs separate adjudication')
evidence={'review_hash':review_hash,'exact_claim':'All-positive-axis literal analytic null-chain parameter classification, with actual winding and full-arc parity.',
 'prior_reconstruction':'draft_pr_publication_program_20260930/audits/pr104_600008/ROOT_PRIORITY_ADJUDICATION_20261006.md',
 'fresh_independent_review':'draft_pr_publication_program_20260930/audits/pr104_600008/final_disposition_adversary_20261006/REPORT.md',
 'original_head':ready['original_head'],'original_archive':'draft_pr_publication_program_20260930/audits/pr104_600008/original_source_authentication_20261006/original_attempt',
 'original_proof_sha256':sha(original/'ANALYTIC_CRITERION.md'),'original_turns_sha256':sha(original/'turns.jsonl'),
 'original_effort_imported':1,'extra_central_proof_search_turns':0,'exact_earlier_printing_verified':False,
 'finite_algebraic_cayley_output_verified':False,'closed_PR_comment':closed['closing_comment_url']}
dump(B/'evidence.json',evidence)
imported={'at':now(),'id':K,'status':'already_solved','turns_used':1,'review_hash':review_hash,
 'statement_hash':row['statement_hash'],'note':'Imported authenticated original submitted author effort1/5; no new central proof turn.',
 'original_effort_import':evidence,'evidence':evidence}
states[K]=imported;dump(B/'state.json',states)
with (B/'history.jsonl').open('a') as f:f.write(json.dumps({**imported,'event':'import_authenticated_submitted_author_effort'},ensure_ascii=False)+'\n')
old_assessments=json.loads(before['assessments.json']);old=old_assessments[K]
note='Already solved for the literal analytic null-chain parameter classification: verified reconstruction from DR2019 Eq3.2/Remark4.4 and the classical DLMF19.7.8 identity. No substantive new contribution established. Exact earlier printing/earliest priority and finite algebraic Cayley output unverified. Original submitted effort1/5 imported; additional central proof turns0; immutable original proof retained.'
assessment={**old,'impact':old['impact'],'p_solve':0,'p_valid_open':0,'resolution':'already_solved',
 'review_policy':'2.0-five-turn-proof','route':'proof','decision':'exclude','review_type':'fresh source-bound mathematical and priority correction',
 'review_hash':review_hash,'note':note,
 'rationale':'Three mathematical families verified the literal analytic theorem. Independent priority reconstructions and a fresh final adversary recover the same criterion from the earlier same-problem quadratures and classical connection identity. Close without a new paper; credited prior application.',
 'remaining_gap':'No gap in the literal analytic classification. Earliest/exact mean-formula printing and a stronger finite algebraic Cayley output are unverified and not certified by this status.',
 'first_experiment':'Do not allocate another proof attempt to this resolved analytic target. Retain frozen proof, prior reconstruction and full count/parity comparison; any stronger algebraic output must be separately scoped.',
 'sources':['https://arxiv.org/abs/0705.0188v1','https://amj.math.stonybrook.edu/pdf-Springer-final/014-0001-3.pdf','https://arxiv.org/abs/1909.08154v1','https://doi.org/10.1007/978-3-030-57000-2_8','https://dlmf.nist.gov/19.7#E8'],
 'original_budget':'1/5','new_central_proof_search_turns':0,'evidence':evidence}
dump(B/'assessment.json',assessment)
py='/opt/homebrew/bin/python3'
run([py,'-E','-B',str(B/'queue.py'),'assess',K,'--file',str(B/'assessment.json')],B)
run([py,'-E','-B',str(B/'queue.py'),'status',K,'already_solved','--note',note,'--evidence',str(B/'evidence.json')],B)
after_assess=load(B/'assessments.json');after_state=load(B/'state.json');after_catalog={x['id']:x for x in load(B/'catalog.json')}
require({k:v for k,v in after_assess.items() if k!=K}=={k:v for k,v in old_assessments.items() if k!=K},'other assessment changed')
before_state=json.loads(before['state.json'])
require({k:v for k,v in after_state.items() if k!=K}==before_state,'other state changed')
require(after_state[K]['turns_used']==1 and after_state[K]['status']=='already_solved','effort/status')
require(after_catalog[K]['local_status']=='already_solved' and not after_catalog[K]['eligible'] and after_catalog[K]['turns_used']==1,'catalog status')
require(set(catalog)==set(after_catalog),'catalog identities')
for key,oldrow in catalog.items():
    if key!=K:require({k:v for k,v in oldrow.items() if k!='rank'}=={k:v for k,v in after_catalog[key].items() if k!='rank'},'other catalog row changed: '+key)
for name in ['history.jsonl','assessment_history.jsonl']:
    require((B/name).read_bytes().startswith(before[name]),'historical prefix changed')
generated_queue=(B/'QUEUE.md').read_bytes()
# Preserve the repository's current campaign-table format and every other row,
# after the required native commands have regenerated the canonical machine data.
lines=before['QUEUE.md'].decode().splitlines();ids=[i for i,s in enumerate(lines) if '| 600008 / AMR-005-0008 |' in s]
require(len(ids)==1,'unique campaign row');i=ids[0];cells=lines[i].split('|')
require(cells[8].strip()=='queued' and cells[9].strip()=='0/5','campaign base changed')
cells[4]=' 0.0000 ';cells[8]=' already_solved ';cells[9]=' 1/5 '
cells[11]=' 2026-10-06: Literal analytic criterion verified and recovered from DR2019 Eq3.2/stated surface limit plus classical DLMF19.7.8. Prior reconstruction/classical corollary; exact earlier printing and earliest priority unverified, finite algebraic Cayley output separate. PR104 closed without merge/new paper after independent mathematical/priority and fresh disposition reviews. Original1/5 imported; audit0; no DOI/tracker. '
lines[i]='|'.join(cells)
(B/'QUEUE.md').write_text('\n'.join(lines)+'\n')
require([s for j,s in enumerate(lines) if j!=i]==[s for j,s in enumerate(before['QUEUE.md'].decode().splitlines()) if j!=i],'other campaign rows changed')
N.mkdir(parents=True)
dump(N/'assessment.json',load(B/'assessment.json'));dump(N/'HISTORICAL_DESK_ASSESSMENT.json',old)
dump(N/'PRIORITY_EVIDENCE.json',evidence)
(N/'README.md').write_text('# 600008: prior analytic null-chain classification\n\nStatus: already_solved for the literal analytic parameter classification. The submitted proof passed the mathematical audit, but its criterion is recovered from DR2019 Eq3.2/Remark4.4 and classical DLMF19.7.8. Exact earlier printing/earliest priority and a finite algebraic Cayley output are unverified. The [checked reconstruction](../../../draft_pr_publication_program_20260930/audits/pr104_600008/ROOT_PRIORITY_ADJUDICATION_20261006.md) states all count and limiting qualifications.\n\nPR104 was closed without merging or publishing a new paper: '+closed['closing_comment_url']+'\n\nThe [immutable original attempt](../../../draft_pr_publication_program_20260930/audits/pr104_600008/original_source_authentication_20261006/original_attempt/ANALYTIC_CRITERION.md) and original one-entry turns ledger are preserved. Original effort1/5 was imported rather than reset; no extra central proof-search turn. Extensive AI-assisted adversarial verification occurred; conventional human peer review did not. No paper, DOI or tracker row.\n')
(N/'RESEARCH_LOG.md').write_text('# 600008 disposition research log\n\n'+now()+': Mathematical verification 100%; bounded analytic priority comparison 100%; disposition workflow 95% pending committed main and remote readback. The original analytic proof and one-entry 1/5 ledger were authenticated and preserved. Independent mathematical and priority families, followed by a fresh disposition adversary, support a prior analytic result/classical corollary classification. PR104 was closed at the original head without merge or publication. This native assessment imports the original effort and records zero additional central proof-search turns. Exact earliest printing and the stronger finite algebraic output remain uncertified. Main release/readback must precede program completion credit.\n')
export=['assessments.json','state.json','history.jsonl','assessment_history.jsonl','catalog.json','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md']
for name in export:
    out=C/prefix/name;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes((B/name).read_bytes())
result={'schema':'pr104-native-prior-disposition-prepared/v1','UTC':now(),'actual_operator_PID':os.getpid(),
 'PR':104,'problem_id':600008,'base_commit':base,'status':'already_solved','scope':'literal analytic classification',
 'source_review_hash':review_hash,'original_budget':'1/5','budget_import_not_new_proof_response':True,
 'new_central_proof_search_turns':0,'historical_desk_assessment_preserved':True,'other_native_targets_preserved':True,
 'catalog_only_other_rank_positions_may_change':True,'other_campaign_rows_byte_preserved':True,
 'native_commands':['assess','status'],'source_inputs':pins,'cache_snapshot_revision':manifest['revision'],
 'cache_snapshot_bytes':cache.stat().st_size,'cache_snapshot_sha256':sha(cache),
 'native_generated_queue_sha256_before_campaign_overlay':hashlib.sha256(generated_queue).hexdigest(),
 'closing_comment_url':closed['closing_comment_url'],'same_head_closed_without_merge':True,
 'publication':False,'DOI':None,'tracker':False,'main_checkpoint_pending':True,'primary_checkout_mutated':False}
dump(N/'DISPOSITION.json',result)
paths=[C/prefix/n for n in export]+[f for f in N.iterdir() if f.is_file()]
result['native_paths']=[str(f.relative_to(C)) for f in paths]
result['native_pins']=[{'path':str(f.relative_to(C)),'bytes':f.stat().st_size,'sha256':sha(f)} for f in paths]
dump(D/'PREPARED_RECEIPT.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ['source_inputs','native_paths','native_pins']}))
