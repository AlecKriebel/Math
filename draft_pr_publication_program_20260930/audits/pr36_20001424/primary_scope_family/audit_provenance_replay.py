#!/usr/bin/env python3
"""Read-only source/queue/Git audit plus private exact verifier executions."""
from pathlib import Path
import copy, datetime, hashlib, importlib.util, json, sqlite3, subprocess, sys
sys.dont_write_bytecode=True

ROOT=Path('/Users/alec/Documents/Math')
FAMILY=ROOT/'draft_pr_publication_program_20260930/audits/pr36_20001424/primary_scope_family'
SNAP=FAMILY.parent/'source_snapshot'
QUEUE=ROOT/'unsolved_math_prioritization'
HEAD='35be7fe58a2832c4d7012cf69c973810fb4c42f8'
BASE='01358d66fc67d1c462bddf31c0d4ee5b120e6737'
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(name,obj): (FAMILY/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def j(path):return json.loads(path.read_text())

manifest=j(QUEUE/'manifest.json')
problems=j(QUEUE/'cache/problems.json')
reports=j(QUEUE/'cache/research_results.json')
p=next(x for x in problems if x['id']==20001424)
r=reports[p['problem_number']]
frozen=j(SNAP/'source_record.json')
raw_files={name:{'bytes':(QUEUE/'cache'/name).stat().st_size,'sha256':sha((QUEUE/'cache'/name).read_bytes())} for name in manifest['files']}
db=sqlite3.connect((QUEUE/'cache/catalog.sqlite').as_uri()+'?mode=ro',uri=True)
db.execute('PRAGMA query_only=ON')
payload,report=db.execute('SELECT payload,report FROM records WHERE key=?',('20001424',)).fetchone()
db_revision=db.execute('SELECT revision FROM metadata').fetchall()
db_count=db.execute('SELECT count(*) FROM records').fetchone()[0]
db.close()
spec=importlib.util.spec_from_file_location('queue_readonly_module',QUEUE/'queue.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
cfg=j(QUEUE/'policy.json')
pure=module.score(p,r,cfg)
related=[]
for x in problems:
 text=' '.join(str(x.get(k,'')) for k in ('title','statement','original_statement','clean_statement','background')).lower()
 if ('field of moduli' in text or 'postcritically' in text or 'pcf' in text or 'pseudo-real' in text):
  related.append({'id':x['id'],'problem_number':x['problem_number'],'title':x['title'],'statement':x['statement'],'report_classification':reports.get(x['problem_number'],{}).get('classification')})
duplicates=[x['id'] for x in problems if ' '.join(x['statement'].split()).lower()==' '.join(p['statement'].split()).lower()]
same_code=[x['id'] for x in problems if x['problem_number']==p['problem_number']]
save('raw_source_record.json',{'problem':p,'upstream_prior_report':r})
save('related_source_records.json',related)
catalog=next(x for x in j(QUEUE/'catalog.json') if x['id']=='20001424')
assessment=j(QUEUE/'assessments.json').get('20001424')
save('corpus_queue_receipt.json',{'utc':utc(),'manifest':manifest,'raw_files':raw_files,'all_raw_hashes_match_manifest':raw_files==manifest['files'],'raw_problem_equals_frozen':p==frozen['problem'],'raw_report_equals_frozen':r==frozen['upstream_prior_report'],'sqlite_open_mode':'uri mode=ro; PRAGMA query_only=ON','sqlite_revision':db_revision,'sqlite_count':db_count,'sqlite_problem_equals_raw':json.loads(payload)==p,'sqlite_report_equals_raw':json.loads(report)==r,'separate_hashes':{'problem_semantic_json':sha(json.dumps(p,sort_keys=True).encode()),'report_semantic_json':sha(json.dumps(r,sort_keys=True).encode()),'statement_exact_utf8':sha(p['statement'].encode()),'whole_frozen_file':sha((SNAP/'source_record.json').read_bytes())},'actual_pure_score_function_result':pure,'score_called_without_cli':True,'catalog':catalog,'assessment':assessment,'current_local_state':j(QUEUE/'state.json').get('20001424'),'normalized_statement_duplicates':duplicates,'same_problem_code_ids':same_code,'related_record_count':len(related),'explicit_related_groups':[g for g in j(QUEUE/'review_v2/related_target_groups.json')['groups'] if '20001424' in g['ids']]})

diff=git('diff',BASE,HEAD,'--')
(FAMILY/'actual_git_diff.patch').write_bytes(diff)
changed=git('diff','--name-status',BASE,HEAD).decode()
files=[]
for file in sorted(SNAP.rglob('*')):
 if not file.is_file():continue
 rel=file.relative_to(SNAP).as_posix();path='unsolved_math_prioritization/attempts/20001424/'+rel
 blob=git('show',HEAD+':'+path)
 files.append({'path':rel,'bytes':len(blob),'snapshot_sha256':sha(file.read_bytes()),'head_sha256':sha(blob),'equals_git_head':file.read_bytes()==blob,'git_blob':git('rev-parse',HEAD+':'+path).decode().strip()})
headqueue=git('show',HEAD+':unsolved_math_prioritization/QUEUE.md').decode()
basequeue=git('show',BASE+':unsolved_math_prioritization/QUEUE.md').decode()
base_state=json.loads(git('show',BASE+':unsolved_math_prioritization/state.json'))
head_state=json.loads(git('show',HEAD+':unsolved_math_prioritization/state.json'))
save('actual_git_receipt.json',{'utc':utc(),'branch':git('branch','--show-current').decode().strip(),'workspace_head_observed':git('rev-parse','HEAD').decode().strip(),'pr_head':HEAD,'pr_base':BASE,'changed_paths_text':changed,'changed_path_count':len(changed.splitlines()),'full_diff_bytes':len(diff),'full_diff_sha256':sha(diff),'snapshot_files':files,'all_16_snapshot_files_match_head':len(files)==16 and all(x['equals_git_head'] for x in files),'base_queue_target_lines':[l for l in basequeue.splitlines() if '20001424' in l],'head_queue_target_lines':[l for l in headqueue.splitlines() if '20001424' in l],'base_queue_state':base_state.get('20001424'),'head_queue_state':head_state.get('20001424'),'branch_mutated':False,'remote_mutated':False})

tmp=FAMILY/'tmp';tmp.mkdir(exist_ok=True)
replay=[]
for program,receipt in [('verify_graph.py','graph_verification.json'),('review/independent_checks.py','review/independent_results.json')]:
 source=(SNAP/program).read_bytes();private=tmp/Path(program).name;private.write_bytes(source)
 run=subprocess.run([sys.executable,str(private)],capture_output=True,cwd=tmp)
 output=Path(program).name+'.stdout.json';(FAMILY/output).write_bytes(run.stdout)
 expected=(SNAP/receipt).read_bytes()
 replay.append({'program':program,'program_sha256':sha(source),'private_program_sha256':sha(private.read_bytes()),'unchanged':private.read_bytes()==source,'exit':run.returncode,'stderr':run.stderr.decode(),'output_file':output,'output_sha256':sha(run.stdout),'expected_sha256':sha(expected),'byte_for_byte_equal':run.stdout==expected,'whole_json_equal':json.loads(run.stdout)==json.loads(expected)})
save('unchanged_private_replay.json',replay)

mutants=[]
transforms=[('all_pendants_inside','verify_graph.py','if i<2 else','if i<4 else'),('wrong_pendant_length','verify_graph.py','1:[5,6]','1:[5]'),('incorrect_degree_assertion','verify_graph.py','20==2*11-2','20==2*12-2'),('wrong_antipode_sign','review/independent_checks.py','return(-z[0]/norm,-z[1]/norm)','return(z[0]/norm,z[1]/norm)'),('all_coordinates_pendants_inside','review/independent_checks.py','(-2,0),(0,-2),(0,-3)','(Q(-1,2),0),(0,Q(-1,2)),(0,Q(-1,3))')]
for label,program,old,new in transforms:
 source=(SNAP/program).read_text();assert old in source,(label,'replacement not found')
 mutant=source.replace(old,new,1);file=tmp/(label+'.py');file.write_text(mutant)
 run=subprocess.run([sys.executable,str(file)],capture_output=True,cwd=tmp)
 mutants.append({'label':label,'program':program,'replace_old':old,'replace_new':new,'original_sha256':sha(source.encode()),'mutant_sha256':sha(mutant.encode()),'actual_execution':True,'exit':run.returncode,'stdout':run.stdout.decode(),'stderr':run.stderr.decode(),'caught':run.returncode!=0})
save('executable_mutant_receipts.json',mutants)

# These metadata checks are audit predicates, not a claim that original verifiers parse them.
status=j(SNAP/'status.json');ready=j(SNAP/'readiness.json');turns=[json.loads(l) for l in (SNAP/'turns.jsonl').read_text().splitlines() if l.strip()]
def accounting_check(s,t,rr,src):
 return {'numeric_id':s['id']==rr['id']==src['problem']['id']==20001424,'actual_ledger_turns':s['turns_used']==rr['turns_used']==len(t)==1,'turn_limit':s['turn_limit']==rr['turn_limit']==5,'proof_hash':s['proof_sha256']==sha((SNAP/'CANDIDATE.md').read_bytes()),'model_matches':s['model']==rr['model']=='gpt-6-astra','reasoning_matches':s['reasoning']==rr['reasoning']=='xhigh','deadline_order':rr['started_utc']<t[0]['at_utc']<rr['deadline_utc'],'literal_scope':src['problem']['statement']=='field of definition vs field of moduli\n\nAre all PCF maps defined over their field of moduli?','review_receipt':s['review_sha256']==sha((SNAP/'review/REVIEW.md').read_bytes())}
metadata_mutants=[]
for label,where,key,value in [('wrong_numeric_id','status','id',20001425),('hidden_extra_turn','status','turns_used',2),('deadline_before_candidate','readiness','deadline_utc','2026-09-30T05:10:00Z'),('source_narrowed_to_odd_set','source','statement','Are all PCF maps with odd postcritical sets defined over their field of moduli?'),('stale_proof_hash','status','proof_sha256','0'*64)]:
 ss,tt,rr,src=copy.deepcopy(status),copy.deepcopy(turns),copy.deepcopy(ready),copy.deepcopy(frozen)
 if where=='status':ss[key]=value
 elif where=='readiness':rr[key]=value
 else:src['problem'][key]=value
 checks=accounting_check(ss,tt,rr,src)
 metadata_mutants.append({'label':label,'where':where,'key':key,'value':value,'checks':checks,'caught_by_audit_predicates':not all(checks.values()),'caught_by_original_verifiers':False,'original_verifiers_do_not_read_metadata':True})
save('source_accounting_mutant_receipts.json',{'baseline':accounting_check(status,turns,ready,frozen),'mutants':metadata_mutants,'policy_reasoning_budget':'queue policy says ultra, historical attempt records xhigh; metadata compatibility differs and no unrecorded upgrade is inferred','original_turns_preserved':1,'added_research_turns':0,'shared_queue_not_changed':True})
save('prose_coverage_receipt.json',{'executed_verifiers':replay,'programs_load_candidate':False,'programs_load_source_record':False,'programs_load_status':False,'programs_load_readiness':False,'operative_prose_claims_not_executably_tested':['graph realization theorem and its hypotheses','symmetry naturality through actual internal rays','equivariant charge arc construction','algebraicity of finite normalized locus','absolute field-of-moduli descent contradiction'],'description':'The original programs have hardcoded graph inputs and no proof/source metadata parser. Therefore arbitrary edits of CANDIDATE or status do not change their executions. Metadata/source predicates above are independent audit checks; finite diagnostics cannot certify the prose.'})
print(json.dumps({'raw_source_match':p==frozen['problem'] and r==frozen['upstream_prior_report'],'raw_hashes_match':raw_files==manifest['files'],'head_match':all(x['equals_git_head'] for x in files),'replays':[x['byte_for_byte_equal'] for x in replay],'mutants_caught':[x['caught'] for x in mutants],'related_count':len(related),'duplicates':duplicates,'score_hash':pure['review_hash']},indent=2))
