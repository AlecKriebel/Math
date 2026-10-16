from pathlib import Path
from hashlib import sha256, sha1
import json,stat,difflib
R=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr316_9900002')
O=R/'priority_correction_finalization_review'
F=R/'priority_correction_review'
B=R/'correction_review_replay_private'
P=R/'priority_correction_packet'
S=R/'snapshot/unsolved_math_prioritization/attempts/9900002'
checks=[]
def ck(v,label):
 if not v: raise AssertionError(label)
 checks.append(label)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def gitpin(p):
 b=p.read_bytes();return {**pin(p),'git_blob_sha1':sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def j(p):return json.loads(p.read_text())
fin=j(R/'PRIORITY_CORRECTION_FINALIZATION.json');replay=j(R/'ROOT_CORRECTION_REPLAY.json');freeze=j(R/'ROOT_CORRECTION_REVIEW_FREEZE.json')
prep=j(R/'PRIORITY_CORRECTION_PREPARATION.json')
ck(pin(R/'PRIORITY_CORRECTION_PREPARATION.json')==fin['historic_preparation_receipt_unchanged'],'historical preparation preserved')
ck(pin(F/'CORRECTION_REVIEW.md')==fin['accepted_report'],'accepted report pin')
ck(pin(F/'REVIEW_MANIFEST.json')==fin['accepted_review_manifest'],'accepted manifest pin')
ck(pin(R/'ROOT_CORRECTION_REPLAY.json')==fin['root_completed_replay'],'root completed replay binding')
closed=j(F/'REVIEW_MANIFEST.json')
for name,p in closed['files'].items():ck(pin(F/name)==p,'closed original artifact '+name)
ck(set(freeze['files'])=={str(p.relative_to(F)) for p in F.rglob('*') if p.is_file()},'all twenty-two closed files frozen')
ck(len(freeze['files'])==22,'closed twenty-two count')
for name,p in freeze['files'].items():
 ck(pin(F/name)=={k:p[k] for k in ['bytes','sha256']},'freeze content '+name)
 ck(stat.S_IMODE((F/name).stat().st_mode)==0o444,'observed current mode '+name)
 ck(p['observed_mode_before']=='0o644' and p['mode_after']=='0o444','explicit mode transition '+name)
ck(set(fin['final_packet'])=={p.name for p in P.iterdir() if p.is_file()},'exact final six files')
ck(set(fin['pre_review_packet'])==set(fin['final_packet']),'same six file scope')
for name,p in fin['final_packet'].items():ck(pin(P/name)==p,'final packet pin '+name)
for name,p in fin['pre_review_packet'].items():
 ck(pin(B/'priority_correction_packet'/name)==p,'reviewed packet pin '+name)
 ck(prep['prepared_files'][name]['bytes']==p['bytes'] and prep['prepared_files'][name]['sha256']==p['sha256'],'early preparation pin '+name)
# Strict reconstruction of every substantive text edit; no scientific test run.
for name in ['README.md','PR_BODY.md','CURRENT_PRIORITY_NOTE.md','PR_TITLE.txt']:
 expected=(B/'priority_correction_packet'/name).read_text()
 for old,new in fin['readability_replacements']:expected=expected.replace(old,new)
 for old,new in fin['bounded_changes'].get(name,[]):expected=expected.replace(old,new)
 if name=='PR_TITLE.txt':expected=expected.replace('(already_solved1/5)','(already_solved, 1/5)')
 ck(expected==(P/name).read_text(),'only authorized text replacements '+name)
oldstatus=j(B/'priority_correction_packet/CURRENT_STATUS.json');cur=j(P/'CURRENT_STATUS.json')
expected=dict(oldstatus)
expected['independent_review']='Submitted mathematics PASS; classical-corollary priority correction and independent prepared-packet mathematical review accepted; bounded editorial finalization separately bound'
for name in ['utc','accepted_correction_review_sha256','accepted_correction_review_manifest_sha256','review_acceptance_utc']:expected[name]=cur[name]
ck(expected==cur,'status only permitted acceptance metadata edits')
ck(cur['accepted_correction_review_sha256']==fin['accepted_report']['sha256'],'status report binding')
ck(cur['accepted_correction_review_manifest_sha256']==fin['accepted_review_manifest']['sha256'],'status manifest binding')
ck(cur['utc']==cur['review_acceptance_utc'],'status actual acceptance timestamp')
ck(cur['status']=='already_solved' and cur['substantive_author_turns']==1 and cur['turn_limit']==5,'operational status and one of five')
ck(cur['mathematical_acceptance'] and not cur['new_resolution_claim'] and not cur['preprint_ready'],'no new resolution/publication readiness')
ck(cur['paper']==False and cur['zenodo_upload']==False and cur['doi'] is None and cur['tracker_row']==False,'no paper Zenodo DOI tracker')
pub=j(P/'PUBLICATION_MANIFEST.json');oldpub=j(B/'priority_correction_packet/PUBLICATION_MANIFEST.json');expected=json.loads(json.dumps(oldpub))
for name in ['CURRENT_STATUS.json','README.md','CURRENT_PRIORITY_NOTE.md']:expected['files'][name]=gitpin(P/name)
expected['utc']=cur['utc'];ck(expected==pub,'manifest regenerated only current pins/time')
wrappers={'README.md','CURRENT_STATUS.json','PUBLICATION_MANIFEST.json'}
orig={str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()}
ck(len(orig)==18,'original eighteen scope');hist=orig-wrappers;ck(len(hist)==15,'historical fifteen scope')
for name in hist:ck(pub['files'][name]==gitpin(S/name),'historical preserved '+name)
for name in wrappers:ck(pub['original_current_wrapper_pins'][name]==gitpin(S/name),'old wrapper pin '+name)
ck(set(pub['files'])==orig-{'PUBLICATION_MANIFEST.json'}|{'CURRENT_PRIORITY_NOTE.md'},'combined nineteen target minus self')
ck(pub['historical_author_review_files_preserved']==15 and pub['substantive_author_turns']==1,'manifest counts')
# Actual native execution records, not copied/renamed output counts.
counts={}
for name,item in fin['native_count_evidence'].items():
 base=R/'root_runs_private'/name
 ck(pin(base/'execution.json')==item['execution_receipt'],'native receipt pin '+name)
 e=j(base/'execution.json');ck(e==item['actual_execution'],'native embedded execution '+name)
 ck(e['exit_code']==0,'native exit zero '+name)
 for stream in ['stdout','stderr']:
  ck(pin(base/(stream+'.bin'))=={'bytes':e[stream+'_bytes'],'sha256':e[stream+'_sha256']},'native '+stream+' '+name)
 for prog in e['programs']:ck(pin(Path(prog['path']))=={'bytes':prog['bytes'],'sha256':prog['sha256']},'native program bound '+name)
 actual=j(base/'stdout.bin');ck(actual['status']=='PASS','native PASS '+name)
 ck(actual[item['count_field']]==item['count'],'native count field '+name);counts[name]=item['count']
ck(list(counts.values())==[7852,646,6124,263,1773],'native count vector')
for field,value in [('author_assertions',7852),('independent_assertions',646),('root_independent_geometric_controls',6124),('fresh_probability_controls',263),('fresh_normalization_controls',1773)]:ck(cur[field]==value,'current count '+field)
# Root's already-completed scientific replay: inspect/bind outputs, do not rerun.
e=j(B/'execution.json');ck(e==replay['completed_native_execution'],'disposable replay actual receipt')
ck(pin(B/'execution.json')==replay['execution_receipt_pin'],'disposable replay receipt pin')
ck(e['exit_code']==0,'disposable scientific replay exit zero')
for stream in ['stdout','stderr']:ck(pin(B/(stream+'.bin'))=={'bytes':e[stream+'_bytes'],'sha256':e[stream+'_sha256']},'disposable '+stream)
for name,p in e['inputs'].items():ck(pin(B/name)==p,'disposable input pin '+name)
ck(pin(F/'validate_artifacts.py')['sha256']==e['original_checker_sha256'],'original checker binding')
ck(pin(B/'validate_artifacts_disposable.py')['sha256']==e['adapted_checker_sha256'],'adapted checker binding')
ck((F/'validate_artifacts.py').read_bytes().replace(str(R).encode(),str(B).encode(),1)==(B/'validate_artifacts_disposable.py').read_bytes(),'exactly one root-path substitution')
for name in ['artifact_validation.json','independent_endpoint_controls.json','author_checker.stdout','author_checker.stderr']:
 ck((F/'executions'/name).read_bytes()==(B/'priority_correction_review/executions'/name).read_bytes(),'replay complete output identical '+name)
ck((F/'executions/validation.stdout').read_bytes()==(B/'stdout.bin').read_bytes(),'replay whole stdout identical')
ck(replay['artifact_assertions']==80 and replay['author_assertions']==7852 and replay['endpoint_controls']==1959 and replay['identity_cases']==1875,'replay count semantics')
# Authenticate preserved bookkeeping failures and recovery without invoking them.
fail=replay['preserved_outer_metadata_failure'];base=Path(fail['directory'])
ck(pin(base/'execution.json')==fail['execution'],'outer failure receipt pin')
ck(pin(base/'stderr.bin')==fail['stderr'],'outer failure stderr pin')
ck(j(base/'execution.json')['exit_code']==1 and "KeyError: 'assertions'" in (base/'stderr.bin').read_text(),'outer receipt KeyError preserved')
for name,exitcode in [('pr316_priority_finalization_actual001',1),('pr316_priority_finalization_recovery_actual001',0)]:
 base=R/'root_runs_private'/name;e=j(base/'execution.json');ck(e['exit_code']==exitcode,'finalizer actual exit '+name)
 for stream in ['stdout','stderr']:ck(pin(base/(stream+'.bin'))=={'bytes':e[stream+'_bytes'],'sha256':e[stream+'_sha256']},'finalizer stream bound '+name+' '+stream)
 for prog in e['programs']:ck(pin(Path(prog['path']))=={'bytes':prog['bytes'],'sha256':prog['sha256']},'finalizer program bound '+name)
ck('RuntimeError: Closed review mode changed' in (R/'root_runs_private/pr316_priority_finalization_actual001/stderr.bin').read_text(),'actual mode assumption failure preserved')
recovery=j(R/'root_runs_private/pr316_priority_finalization_recovery_actual001/stdout.bin')
ck(recovery['final_packet']==fin['final_packet'] and recovery['scientific_tests_rerun']==False,'recovery actual final packet/no science rerun')
# Persist only own sibling output; retain diffs for checkability.
diff=''
for name in sorted(fin['final_packet']):diff+=''.join(difflib.unified_diff((B/'priority_correction_packet'/name).read_text().splitlines(True),(P/name).read_text().splitlines(True),fromfile='reviewed/'+name,tofile='final/'+name))
(O/'executions/exact_final_diff.txt').write_text(diff)
result={'status':'PASS_BOUNDED_FINALIZATION_RECHECK','bookkeeping_assertions':len(checks),'scientific_tests_run':False,'new_mathematical_claims_reviewed':False,'final_six':fin['final_packet'],'native_bound_counts':counts,'closed_original_files':22,'preserved_historical_files':15,'author_turns':'1/5','operational_status':'already_solved','no_remaining_concerns_within_scope':True,'inputs':{name:pin(R/name) for name in ['PRIORITY_CORRECTION_FINALIZATION.json','ROOT_CORRECTION_REPLAY.json','ROOT_CORRECTION_REVIEW_FREEZE.json','PRIORITY_CORRECTION_PREPARATION.json']}}
(O/'executions/finalization_validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
