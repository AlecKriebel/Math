"""Finish the successful native CLI assessment with a target-scoped catalog projection."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, importlib.util, textwrap
A=Path(__file__).resolve().parent;C=A.parents[2];R=Path('/Users/alec/Documents/Math');K='600008'
D=A/'native_prior_disposition_finalization_20261006';D.mkdir(exist_ok=False)
B=A/'native_prior_disposition_20261006_retry1/private_backend';records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def run(argv,cwd=C,body_only=False):
    start=now();p=subprocess.Popen(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate();i=len(records)
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
require(ready['fresh_final_disposition_review_authenticated'] and closed['same_head_closed_without_merge'],'closure gate')
require(git('symbolic-ref','--short','HEAD').strip()==b'main','not main')
base=git('rev-parse','HEAD').strip().decode()
require(base=='dd742176bcb997caf788f73594fcd9f9dea236fd','main advanced')
require(git('ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main').decode().split()[0]==base,'remote advanced')
require(not git('diff','--cached','--name-only','-z'),'foreign staged')
prefix='unsolved_math_prioritization/';N=C/prefix/'attempts'/K
require(not N.exists() and not git('ls-tree','-r','--name-only',base,'--',str(N.relative_to(C))),'existing native attempt')
names=['queue.py','manifest.json','policy.json','catalog.json','assessments.json','state.json','history.jsonl',
       'assessment_history.jsonl','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md']
before={};pins=[]
for name in names:
    data=git('show',base+':'+prefix+name,body=True);before[name]=data;q=C/prefix/name
    require(not q.is_symlink() and (not q.exists() or q.read_bytes()==data),'unknown worktree edit: '+name)
    pins.append({'path':prefix+name,'git_commit':base,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
for name in ['queue.py','manifest.json','policy.json']:
    require((B/name).read_bytes()==before[name],'backend immutable input changed: '+name)
journal=load(A/'native_prior_disposition_20261006_retry1/PROCESS_JOURNAL.json')
cli=[x for x in journal['records'] if str(B/'queue.py') in x['argv']]
require(len(cli)==2 and [x['argv'][4] for x in cli]==['assess','status'] and all(x['exit_code']==0 for x in cli),'actual native CLI commands')
manifest=load(B/'manifest.json');cache=B/'cache/catalog.sqlite'
original=A/'original_source_authentication_20261006/original_attempt'
require(sha(original/'ANALYTIC_CRITERION.md')=='608217a2ffc120a965b165f5b6065edd83f8cf94c5e77f0f95a0326640db2dae','proof changed')
require(load(original/'status.json')['substantive_approaches']==1 and [json.loads(t)['turn'] for t in (original/'turns.jsonl').read_text().splitlines()]==[1],'original effort')
evidence=load(B/'evidence.json');review_hash=evidence['review_hash']
require(review_hash=='597672d96f2b12dc802c798cbd01e1d224329f4f3a277e65514b429354103663','source pair')
old_assessments=json.loads(before['assessments.json']);old=old_assessments[K]
after_assess=load(B/'assessments.json');after_state=load(B/'state.json')
require({k:v for k,v in after_assess.items() if k!=K}=={k:v for k,v in old_assessments.items() if k!=K},'other assessment changed')
require({k:v for k,v in after_state.items() if k!=K}==json.loads(before['state.json']),'other state changed')
require(after_state[K]['turns_used']==1 and after_state[K]['status']=='already_solved','effort/status')
require(after_assess[K]['resolution']=='already_solved' and after_assess[K]['review_hash']==review_hash,'assessment')
for name in ['history.jsonl','assessment_history.jsonl']:
    require((B/name).read_bytes().startswith(before[name]),'historical prefix changed')
extra_history=[json.loads(t) for t in (B/'history.jsonl').read_bytes()[len(before['history.jsonl']):].decode().splitlines()]
extra_assess=[json.loads(t) for t in (B/'assessment_history.jsonl').read_bytes()[len(before['assessment_history.jsonl']):].decode().splitlines()]
require(len(extra_history)==2 and len(extra_assess)==1 and all(x['id']==K for x in extra_history+extra_assess),'new native event scope')
require(extra_history[0]['event']=='import_authenticated_submitted_author_effort' and all(x['turns_used']==1 for x in extra_history),'imported effort')
old_rows=json.loads(before['catalog.json']);catalog={x['id']:x for x in old_rows}
regenerated=load(B/'catalog.json');after_catalog={x['id']:x for x in regenerated}
require(set(catalog)==set(after_catalog),'catalog identities')
require(after_catalog[K]['local_status']=='already_solved' and not after_catalog[K]['eligible'] and after_catalog[K]['turns_used']==1,'target catalog status')
# The baseline catalog contains48 stale projections of unchanged existing states.
# Record them, then preserve their baseline rows rather than reprocess other targets.
drift=[]
for key,oldrow in catalog.items():
    if key==K:continue
    diff={f:{'before':oldrow.get(f),'after':after_catalog[key].get(f)} for f in set(oldrow)|set(after_catalog[key]) if f!='rank' and oldrow.get(f)!=after_catalog[key].get(f)}
    if diff:
        require(set(diff)<=set(['local_status','eligible','turns_used']),'unexplained source/score drift: '+key)
        st=after_state.get(key,{})
        require(after_catalog[key]['local_status']==st['status'] and after_catalog[key]['turns_used']==st.get('turns_used',0),'unexplained state projection: '+key)
        drift.append({'id':key,'difference':diff,'baseline_preserved':True})
dump(D/'UNRELATED_BASELINE_PROJECTION_DRIFT.json',{'base_commit':base,'count':len(drift),'differences':drift,'other_targets_not_reassessed':True})
raw_generated_pins={name:sha(B/name) for name in ['catalog.json','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md']}
rows=[dict(after_catalog[K]) if x['id']==K else dict(x) for x in old_rows]
rows.sort(key=lambda x:(not x['eligible'],-x['ev'],x['id']))
for i,x in enumerate([x for x in rows if x['eligible']],1):x['rank']=i
for x in rows:
    if not x['eligible']:x['rank']=None
# Reuse the exact pinned native output-writing code, with only the scoped rows.
text=(B/'queue.py').read_text();start=text.index("    write(ROOT/'catalog.json',rows)");end=text.index('def seen_ids',start)
render=textwrap.dedent(text[start:end])
spec=importlib.util.spec_from_file_location('pr104_native_queue_writer',B/'queue.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
namespace=dict(module.__dict__);namespace.update(rows=rows,cfg=load(B/'policy.json'),reviews=after_assess,state=after_state)
exec(compile(render,str(B/'queue.py')+':pinned-native-render','exec'),namespace)
for x in load(B/'catalog.json'):
    if x['id']!=K:require({f:v for f,v in x.items() if f!='rank'}=={f:v for f,v in catalog[x['id']].items() if f!='rank'},'other catalog row changed after overlay')
dump(D/'SCOPED_RENDER_RECEIPT.json',{'UTC':now(),'queue_py_sha256':sha(B/'queue.py'),'native_render_code_sha256':hashlib.sha256(render.encode()).hexdigest(),
 'raw_generated_pins':raw_generated_pins,'other_catalog_rows_semantically_preserved_except_rank':True,'baseline_drift_count':len(drift),
 'actual_native_cli_journal':'native_prior_disposition_20261006_retry1/PROCESS_JOURNAL.json','actual_native_commands':cli})
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
result={'schema':'pr104-native-prior-disposition-prepared/v2','UTC':now(),'actual_operator_PID':os.getpid(),
 'PR':104,'problem_id':600008,'base_commit':base,'status':'already_solved','scope':'literal analytic classification',
 'source_review_hash':review_hash,'original_budget':'1/5','budget_import_not_new_proof_response':True,
 'new_central_proof_search_turns':0,'historical_desk_assessment_preserved':True,'other_native_targets_preserved':True,
 'catalog_only_other_rank_positions_may_change':True,'baseline_existing_state_projection_drift_preserved':len(drift),'scoped_render_receipt':'SCOPED_RENDER_RECEIPT.json','other_campaign_rows_byte_preserved':True,
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
