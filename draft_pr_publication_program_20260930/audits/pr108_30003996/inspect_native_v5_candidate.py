"""Independent root byte/dictionary audit of the concrete private candidate; no export."""
from pathlib import Path
import sys, os, datetime, hashlib, json, csv, io, collections, re
A=Path(__file__).resolve().parent; C=A.parents[2]
D=A/'native_publication_integration_plan_20261006/corrected_v5'
sys.path.insert(0,str(D))
import v3_guards as g
from bounded_process import BoundedRunner
g.validate_python_startup(os.environ)
inputs_bytes=(D/'EXECUTION_INPUTS_FROZEN_20261006.json').read_bytes()
inputs=g.loads(inputs_bytes); g.validate_execution_manifest(inputs,inputs_bytes)
inputs_sha=g.sha(inputs_bytes)
g.require(inputs_sha=='dfe3e71993e3bd99afb9c11e54f4fe4c9117c770849ffac54c7bc2b17e6bd76a','Actual frozen inputs changed')
candidate=D/('candidate_'+inputs_sha[:16]); receipt=g.loads((candidate/'CANDIDATE_RECEIPT.json').read_bytes())
g.require(receipt['execution_inputs_sha256']==inputs_sha and receipt['native_assess_executed_in_private_backend'] is True and receipt['native_export_executed'] is False and not (candidate/'PREPARE_FAILURE.json').exists(),'Candidate identity/failure')
out=A/'root_native_v5_candidate_inspection_20261006';out.mkdir(exist_ok=False)
e=inputs['effective'];runner=BoundedRunner(out,C,e['process_policy'],e['environment_policy'])
before={}; native_prefix='unsolved_math_prioritization/';K='30003996';N=native_prefix+'attempts/'+K+'/'
names=['assessments.json','state.json','history.jsonl','assessment_history.jsonl','catalog.json','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md']
basepins={Path(p['path']).name:p for p in e['native_baseline_pins']}
for name in names:
    b,_,_=runner.run([e['runtime']['git_executable'],'show',e['main_parent']+':'+native_prefix+name],role='git',stdout_cap=basepins[name]['bytes']+1)
    g.require(len(b)==basepins[name]['bytes'] and g.sha(b)==basepins[name]['sha256'],'Baseline byte pin')
    p=C/native_prefix/name
    g.require(not p.is_symlink() and (not p.exists() or p.read_bytes()==b),'Concurrent native baseline edit')
    before[name]=b
affected=receipt['affected_paths'];g.require(len({x['path'] for x in affected})==len(affected),'Duplicate offer')
offered={}
for row in affected:
    path=g.relative(row['path']);g.require(path.startswith(N) or path in [native_prefix+n for n in names],'Export scope')
    p=candidate/'bundle'/path;g.regular(p);b=p.read_bytes()
    g.require({'bytes':len(b),'sha256':g.sha(b)}==row['after'],'Offer body pin')
    if path in [native_prefix+n for n in names]:
        old=before[Path(path).name];g.require(row['before']=={'bytes':len(old),'sha256':g.sha(old)} and old!=b,'Global diff correspondence')
    else:g.require(row['before'] is None,'Target file unexpectedly exists')
    offered[path]=b
def after(name):return offered.get(native_prefix+name,before[name])
oldass=g.loads(before['assessments.json']);newass=g.loads(after('assessments.json'))
oldstate=g.loads(before['state.json']);newstate=g.loads(after('state.json'))
g.require({k:v for k,v in oldass.items() if k!=K}=={k:v for k,v in newass.items() if k!=K},'Other assessments changed')
g.require(K not in oldstate and {k:v for k,v in newstate.items() if k!=K}==oldstate,'Other states changed')
state=newstate[K];g.require(state['status']=='claimed_solved' and state['turns_used']==2 and state['new_central_proof_search_turns']==0 and state['original_structured_ledger_present'] is False,'Target provenance')
g.require(g.loads(offered[N+'IMPORT_BASELINE.json'])==state,'Import baseline correspondence')
g.require(g.loads(offered[N+'HISTORICAL_DESK_ASSESSMENT.json'])==oldass[K],'Original desk metadata')
for key,value in oldass[K].items():
    if key!='reviewed_at':g.require(newass[K].get(key)==value,'Historical assessment field changed: '+key)
g.require(g.utc(newass[K]['reviewed_at'])<=datetime.datetime.now(datetime.timezone.utc),'Native assessment timestamp')
g.require(newass[K]['publication_DOI']=='10.5281/zenodo.23181280' and newass[K]['original_budget']=='2/5' and newass[K]['new_central_proof_search_turns']==0,'Published assessment')
for name in ['history.jsonl','assessment_history.jsonl']:
    b=after(name);g.require(b.startswith(before[name]),'Ledger prefix')
    extra=b[len(before[name]):].splitlines();g.require(len(extra)==1 and g.loads(extra[0])['id']==K,'Ledger scope')
oldrows=g.loads(before['catalog.json']);newrows=g.loads(after('catalog.json'))
g.require(len(newrows)==len(oldrows) and [x['id'] for x in newrows]==[x['id'] for x in oldrows],'Full catalog order/count')
for old,new in zip(oldrows,newrows):
    if old['id']!=K:g.require(old==new,'Unrelated full catalog row/rank changed')
target=next(x for x in newrows if x['id']==K)
g.require(target['local_status']=='claimed_solved' and target['turns_used']==2 and target['eligible'] is False,'Target catalog')
def records(b):
    text=b.decode();lines=re.findall(r'[^\r\n]*(?:\r\n|\r|\n|$)',text);lines=[x for x in lines if x]
    reader=csv.reader(io.StringIO(text,newline=''),strict=True);result=[];end=0
    for row in reader:
        result.append((row,''.join(lines[end:reader.line_num]).encode()));end=reader.line_num
    g.require(end==len(lines),'Independent CSV partition');return result
orows,nrows=records(before['ranking.csv']),records(after('ranking.csv'))
g.require(len(orows)==len(nrows) and orows[0]==nrows[0],'Ranking header/count')
col=orows[0][0].index('id')
for old,new in zip(orows[1:],nrows[1:]):
    g.require(old[0][col]==new[0][col],'Ranking position')
    if old[0][col]!=K:g.require(old==new,'Unrelated full CSV span changed')
oldlines=before['QUEUE.md'].splitlines(keepends=True);newlines=after('QUEUE.md').splitlines(keepends=True)
g.require(len(oldlines)==len(newlines),'Campaign row count');changed=[i for i,(x,y) in enumerate(zip(oldlines,newlines)) if x!=y]
g.require(len(changed)==1 and ('| '+K+' / OWR-16633-013 |').encode() in newlines[changed[0]] and b' claimed_solved | 2/5 ' in newlines[changed[0]] and b'https://doi.org/10.5281/zenodo.23181280' in newlines[changed[0]],'Campaign exact target only')
g.require(after('SHORTLIST.md')==before['SHORTLIST.md'],'Shortlist changed')
summary=g.loads(after('summary.json'));oldsummary=g.loads(before['summary.json'])
expected={**oldsummary,'records':len(newrows),'eligible':sum(x['eligible'] for x in newrows),'assessed':len(newass),'holds':dict(collections.Counter(h.split(':')[0] for x in newrows for h in x['holds']))}
g.require(summary==expected,'Summary full scoped correspondence')
for pin in e['original_authentication_pins']['original_files']:
    src=C/pin['path'];relative=src.relative_to(A/'original_source_authentication_20261006/original_attempt')
    g.require(offered[N+'historical_original/'+str(relative)]==src.read_bytes(),'Original fifteen bytes')
g.require(g.loads(offered[N+'prior_imported_report.json'])=={} and offered[N+'PROOF.md']==(A/'repaired_diagnostics_v1/PROOF.md').read_bytes(),'Effective proof/imported prior')
package=g.loads((C/e['package']['manifest']['path']).read_bytes())
for p in package['files']:
    b=offered[N+'publication/package/'+p['relative_path']]
    g.require(len(b)==p['bytes'] and g.sha(b)==p['sha256'],'Published logical file changed')
privacy=g.loads((A/'native_actual_input_preparation_v2_20261006/draft_dfe3e71993e3bd99/PRIVATE_EXPORT_EXCLUSIONS.json').read_bytes())
r={'schema':'pr108-root-actual-candidate-inspection/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'execution_inputs_sha256':inputs_sha,'main_parent':e['main_parent'],'all_offered_bodies_authenticated':len(affected),'all_other_catalog_rows_ranks_positions_identical':len(oldrows)-1,'all_other_assessments_states_identical':True,'historical_ledger_prefixes_and_one_target_append_verified':True,'ranking_unrelated_physical_records_identical':True,'campaign_single_target_change':True,'original15_and_published46_byte_identical':True,'target_catalog':target,'target_state':state,'target_assessment':newass[K],'private_export_plan':privacy,'native_worker_PID':receipt['native_worker_process_PID'],'actual_native_candidate_passed_root_data_inspection':True,'independent_candidate_review_pending':True,'native_export_or_merge_executed':False}
(out/'ROOT_RECEIPT.json').write_bytes(g.canonical(r));print(json.dumps({'offered_paths':len(affected),'unrelated_rows_preserved':len(oldrows)-1,'native_worker_PID':receipt['native_worker_process_PID'],'root_data_inspection_passed':True,'export':False}))
