#!/usr/bin/env python3
"""Actual original replays, adversarial scope controls, isolated workflow probes."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,copy,subprocess,shutil,sqlite3,importlib.util,contextlib,io,math
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3];U=ROOT/'unsolved_math_prioritization';SNAP=HERE.parent/'source_snapshot'
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def dump(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def run(path):
 p=subprocess.run(['python3',str(path)],capture_output=True,cwd=path.parent,timeout=90)
 return {'returncode':p.returncode,'stdout_sha256':sha(p.stdout),'stderr':p.stderr.decode()},p.stdout
out={'at_utc':datetime.now(timezone.utc).isoformat(),'audit_completion_percent':78,
 'original_substantive_turns':'1/5','verification_turns':0,'mathematical_goal_verification_percent':0}
protected=['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','assessment_history.jsonl','queue.py','policy.json','manifest.json','review_v2/related_target_groups.json']
before={n:sha((U/n).read_bytes()) for n in protected}
orig=HERE/'isolated/original'
out['baseline_replays']={}
for code,receipt in [('verify.py','verification.json'),('review/independent_checks.py','review/independent_results.json')]:
 replay=HERE/'tmp'/('replay_author' if code=='verify.py' else 'replay_review')
 replay.mkdir(parents=True,exist_ok=True)
 target=replay/Path(code).name;target.write_bytes((orig/code).read_bytes())
 status,stdout=run(target)
 (replay/'receipt.stdout.json').write_bytes(stdout)
 expected=(orig/receipt).read_bytes()
 status.update(original_code_sha256=sha((orig/code).read_bytes()),copied_code_sha256=sha(target.read_bytes()),
  code_unchanged=target.read_bytes()==(orig/code).read_bytes(),receipt_bytes_equal=stdout==expected,
  receipt_structurally_equal=json.loads(stdout)==json.loads(expected))
 if code=='verify.py':status['generated_receipt_bytes_equal']=(replay/'verification.json').read_bytes()==expected
 out['baseline_replays'][code]=status

# Raw source/metadata falsifiers bind the exact original record and report.
raw=load(HERE/'source_record.raw.json');prior=load(HERE/'prior_report.json')
readiness=load(orig/'readiness.json');turns=[json.loads(x) for x in (orig/'turns.jsonl').read_text().splitlines()]
def bind(problem,report,ready=readiness,ledger=turns):
 errors=[]
 if not isinstance(problem,dict) or problem.get('id')!=10000046 or problem.get('problem_number')!='AMR-099-0046':errors.append('identity mismatch')
 if problem!=raw:errors.append('payload differs from fresh pinned source')
 if report!=prior:errors.append('prior report differs from fresh pinned report')
 if sha(json.dumps([problem,report],sort_keys=True).encode())!=ready.get('review_hash'):errors.append('review_hash mismatch')
 if not isinstance(problem,dict) or sha(problem.get('statement','').encode())!=ready.get('statement_hash'):errors.append('statement_hash mismatch')
 if ready.get('budget',{}).get('used_substantive_attempts')!=len(ledger) or [x.get('turn') for x in ledger]!=[1] or len(ledger)!=1:errors.append('original ledger mismatch')
 return errors
controls=[]
variants=[]
p=copy.deepcopy(raw);p['id']=10000047;variants.append(('numeric_identity_mutation',p,prior,readiness,turns))
p=copy.deepcopy(raw);p['problem_number']='AMR-099-0047';variants.append(('code_identity_mutation',p,prior,readiness,turns))
p=copy.deepcopy(raw);p['statement']=p['statement'].replace('paths are disjoint','positions differ at each equal time');variants.append(('statement_payload_mutation',p,prior,readiness,turns))
p=copy.deepcopy(raw);p['view_count']+=1;variants.append(('incidental_payload_mutation',p,prior,readiness,turns))
variants.extend([('null_report',raw,None,readiness,turns),('deleted_report_join_defaults_empty',raw,{},readiness,turns)])
r=copy.deepcopy(prior);r['result']='A full solution has been proved';variants.append(('invented_report_solution',raw,r,readiness,turns))
rd=copy.deepcopy(readiness);rd['budget']['used_substantive_attempts']=0;variants.append(('reset_original_turn_count',raw,prior,rd,turns))
ledger=copy.deepcopy(turns);ledger.append({**ledger[0],'turn':2,'outcome':'candidate'});variants.append(('invented_proof_turn',raw,prior,readiness,ledger))
for name,p,r,rd,l in variants:
 errors=bind(p,r,rd,l);assert errors
 controls.append({'name':name,'rejected':True,'reasons':errors})
assert not bind(raw,prior)
out['new_binding_falsifiers']={'baseline_passes':True,'actual_variants':controls,
 'boundary':'These are independently authored exact source/ledger controls, not functionality claimed for the original finite checkers.'}

# A checker with no artifact/source reads still passes when adjacent prose or provenance is changed.
mutants=[
 ('uniform_positive_limit_claim',lambda s:s.replace('Equations(1)–(2) do not evaluate that limit.','Equations(1)–(2) prove that the limit is strictly positive.')),
 ('distance_ten_threshold_extended',lambda s:s.replace('N\\le9','N\\le10')),
 ('infimum_replaced_by_supremum',lambda s:s.replace('\\inf_Na_N','\\sup_Na_N'))]
out['original_program_scope_mutants']=[]
for name,mut in mutants:
 sandbox=HERE/'tmp'/name
 shutil.copytree(orig,sandbox,dirs_exist_ok=True)
 p=sandbox/'PARTIAL.md';old=p.read_text();new=mut(old);assert new!=old;p.write_text(new)
 receipts=[]
 for code,receipt in [('verify.py','verification.json'),('review/independent_checks.py','review/independent_results.json')]:
  status,stdout=run(sandbox/code)
  receipts.append({'program':code,'exit_code':status['returncode'],'unchanged_receipt':stdout==(orig/receipt).read_bytes()})
 assert all(x['exit_code']==0 and x['unchanged_receipt'] for x in receipts)
 out['original_program_scope_mutants'].append({'name':name,'actual_prose_changed':True,'original_programs_passed':receipts,
  'conclusion':'The original programs certify their fixed finite diagnostics, not the adjacent prose or infinite claim.'})
provenance_sandbox=HERE/'tmp/provenance_mutation'
shutil.copytree(orig,provenance_sandbox,dirs_exist_ok=True)
dump(provenance_sandbox/'source_record.json',{'id':999,'statement':'invented'})
dump(provenance_sandbox/'prior_report.json',None)
p=provenance_sandbox/'readiness.json';rd=load(p);rd['budget']['used_substantive_attempts']=0;dump(p,rd)
out['original_program_provenance_mutants']=[]
for code,receipt in [('verify.py','verification.json'),('review/independent_checks.py','review/independent_results.json')]:
 status,stdout=run(provenance_sandbox/code)
 out['original_program_provenance_mutants'].append({'program':code,'exit_code':status['returncode'],'receipt_unchanged':stdout==(orig/receipt).read_bytes()})

# Actual independent matcher produces a finite counterexample to sup/limit swapping.
spec=importlib.util.spec_from_file_location('independent_original',orig/'review/independent_checks.py')
module=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):spec.loader.exec_module(module)
seq=[module.test(1,n,(2,)) for n in (1,2,10)]
out['finite_claim_falsifiers']={
 'supremum_is_not_limit_witness':seq,
 'distance_ten_N10_translation_word':{'d':3,'X10':[10,0,0],'Y0':[10,0,0],'equal_time_displacement':[10,0,0],
   'positive_word_probability':'1/60466176','all_couplings_a10_upper_bound':'60466175/60466176',
   'conclusion':'The first marginal can hit the other fixed start at time10. Therefore a10<1 under every coupling, disproving the N≤10 mutant, not merely its translation justification.'},
 'one_time_marginal_is_not_path_law':{'construction':'For every n≥1 sample Xn independently with the n-step SRW endpoint law from zero; fix X0=0.',
  'all_one_time_position_marginals_exact':True,'one_dimensional_invalid_two_step_pair':[1,-2],
  'probability_invalid_pair':'1/8','SRW_invalid_pair_probability':'0',
  'conclusion':'Correct one-time position marginals do not imply an SRW path law. Already X1=1,X2=-2 has positive probability, violating the nearest-neighbor transition rule.'},
 'boundary':'No additional research attempt or resolution search; counterexamples expose finite-certificate and path-marginal scope.'}

# Exercise actual queue code on isolated synthetic DB/files, never on live inputs.
spec=importlib.util.spec_from_file_location('queue_actual',U/'queue.py');queue=importlib.util.module_from_spec(spec);spec.loader.exec_module(queue)
sandbox=HERE/'tmp/workflow';sandbox.mkdir(parents=True,exist_ok=True);queue.ROOT=sandbox
(sandbox/'cache').mkdir(exist_ok=True)
db=sqlite3.connect(sandbox/'cache/catalog.sqlite')
db.execute('CREATE TABLE IF NOT EXISTS records (key TEXT PRIMARY KEY,payload TEXT,report TEXT)')
db.execute('CREATE TABLE IF NOT EXISTS metadata (revision TEXT)');db.execute('DELETE FROM records');db.execute('DELETE FROM metadata')
revision='37e53eabe540fb458758e198be61634bd02ee008'
db.execute('INSERT INTO records VALUES (?,?,?)',(str(raw['id']),json.dumps(raw),json.dumps(prior)))
db.execute('INSERT INTO metadata VALUES (?)',(revision,));db.commit()
dump(sandbox/'manifest.json',{'revision':revision,'records':1})
dump(sandbox/'policy.json',load(U/'policy.json'))
current=load(U/'assessments.json')[str(raw['id'])]
dump(sandbox/'assessments.json',{str(raw['id']):current});dump(sandbox/'state.json',{})
livequeue=(U/'QUEUE.md').read_text();(sandbox/'QUEUE.md').write_text(livequeue)
with contextlib.redirect_stdout(io.StringIO()):queue.rank(None)
generated=(sandbox/'QUEUE.md').read_text()
row=next(x for x in generated.splitlines() if '10000046 / AMR-099-0046' in x)
out['actual_queue_generator_private_probe']={'generated_selected_row':row,'generated_cell_count':len(row.split('|')[1:-1]),
 'protected_input_cell_count':12,'protected_input_was_live_full_queue_copy':True,
 'findings_chat_doi_impact_columns_lost':all(x not in next(s for s in generated.splitlines() if s.startswith('| Rank |')) for x in ['Impact','Chat','Findings','DOI']),
 'actual_rank_executed_only_on_private_synthetic_input':True}
cache=[]
for name,p,r in [('payload_changed',variants[2][1],prior),('null_report',raw,None),('deleted_report_default_empty',raw,{})]:
 db.execute('UPDATE records SET payload=?,report=? WHERE key=?',(json.dumps(p),json.dumps(r),str(raw['id'])));db.commit()
 try:queue.require_cache();passed=True;error=None
 except Exception as exc:passed=False;error=str(exc)
 cache.append({'name':name,'actual_require_cache_accepted':passed,'error':error,
  'binding_control_rejects':bool(bind(p,r))})
db.close();out['actual_cache_preflight_negative_controls']=cache
after={n:sha((U/n).read_bytes()) for n in protected}
out['protected_live_bytes_unchanged_by_controls']=before==after
out['protected_before']=before;out['protected_after']=after
dump(HERE/'controls_results.json',out)
print(json.dumps({'baseline':out['baseline_replays'],'binding_variants':len(controls),
 'prose_mutants':len(mutants),'queue_probe':out['actual_queue_generator_private_probe'],
 'cache_negative_controls':cache,'protected_unchanged':before==after},indent=2))
