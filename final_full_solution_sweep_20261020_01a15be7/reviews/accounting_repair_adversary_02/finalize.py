from pathlib import Path
import collections,datetime as dt,difflib,hashlib,json,os,shutil,sys
sys.dont_write_bytecode=True
os.environ.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
R=Path(__file__).resolve().parent
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(rel):return json.loads((R/rel).read_text())
def save(rel,d):(R/rel).write_text(json.dumps(d,indent=2)+'\n')
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
inp=read('INPUT_MANIFEST.json');bad=[]
for e in inp['files']:
 p=R/e['captured_path'];b=p.read_bytes()
 if len(b)!=e['bytes'] or sha(b)!=e['sha256']:bad.append(e['captured_path'])
require(not bad,'Captured input custody mismatch')
before=(R/'inputs/history/coverage_snapshot.py').read_text()
after=(R/'inputs/current/coverage_snapshot.py').read_text()
(R/'SOURCE_DIFF.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='preserved_pre_repair/coverage_snapshot.py',tofile='captured_repaired/coverage_snapshot.py')))
require((R/'inputs/history/coverage_snapshot.py').read_bytes()==(R/'inputs/pre_repair/coverage_snapshot.py').read_bytes(),'Pre-repair implementation differs from sealed prior capture')
s=read('inputs/current/STATE.json')
j=[json.loads(x) for x in (R/'inputs/current/dispositions.jsonl').read_text().splitlines() if x.strip()]
require([x['pr'] for x in j]==list(range(s['start_pr'],s['next_pr'])),'Independent prefix mismatch')
e={x['pr']:x for x in j}
for ov in s['reopened_disposition_overrides']:e[ov['pr']]=read('inputs/current/'+ov['replacement_disposition'])
raw=dict(collections.Counter(x['disposition'] for x in j));effective=dict(collections.Counter(x['disposition'] for x in e.values()))
expected={292:('30001608',23524971,174),397:('9700002',23527793,176),399:('30001179',23539283,177),280:('30000156',23539734,178)}
require(len(s['completed_publications'])==4,'Unexpected completed count')
for item in s['completed_publications']:
 pr=item['pr'];problem,record,row=expected[pr]
 require((item['problem_id'],item['record'],item['ledger_row'])==(problem,record,row),'Known completed identity mismatch')
 proof=read('inputs/current/'+item['verification']);disp=e[pr];ledger=read('inputs/current/'+proof['evidence']['ledger'])
 require(proof['pr']==pr and proof['problem_ids']==[problem] and proof['record']==record and proof['doi']==item['doi']==disp['doi']==ledger['doi']==f'10.5281/zenodo.{record}','Publication identity mismatch')
 require(proof['ledger_row']==row==disp['ledger_row']==ledger['row_number'],'Row mismatch')
 require(proof['merge_commit']==item['merge_commit'],'Merge mismatch')
 require(disp['problem_ids']==[problem] and disp['publication_evidence']==item['verification'],'Effective disposition mismatch')
 require(ledger['spreadsheet_id']==s['spreadsheet_id'] and ledger['sheet_gid']==s['sheet_gid'],'Actual ledger target mismatch')
 require(ledger['values'][2]=='https://doi.org/'+item['doi'] and problem in ledger['values'][0] and proof['source_alias'] in ledger['values'][0] and f'https://github.com/AlecKriebel/Math/pull/{pr}' in ledger['values'][3],'Actual ledger row identity mismatch')
for mode in ['normal','optimized']:
 snap=read('cases/fresh/current_baseline/'+mode+'.stdout')
 require(snap['disposition_counts']==effective and snap['historical_journal_disposition_counts']==raw and snap['own_completed_publications']==s['completed_publications'] and snap['next_pr']==s['next_pr'],'Baseline output differs from independent calculation')
prev=read('inputs/prior_review/OVERRIDE_CONTROLS.json')['results'];results=read('CONTROL_RESULTS.json')['results'];sup=read('SUPPLEMENTARY_RESULTS.json')['results']
for mode in ['normal','optimized']:
 hist=[x for x in results if x['group']=='historical21' and x['mode']==mode]
 require([x['name'] for x in hist]==[x['name'] for x in prev],'Original case inventory changed')
 require(all(x['control_pass'] for x in hist),'Original control failure')
 fresh=[x for x in results if x['group']=='fresh' and x['mode']==mode]
 extra=[x for x in sup if x['mode']==mode]
 require(len(fresh)==163 and sum(x['accepted'] and x['expected_reject'] for x in fresh)==19,'Unexpected fresh results')
 require(len(extra)==10 and all(x['accepted'] for x in extra),'Unexpected supplementary results')
require(raw['published_verified_full_solution']==3 and effective['published_verified_full_solution']==4 and raw['skip_priority_gate_not_met']==3 and effective['skip_priority_gate_not_met']==2,'Historical/effective count failure')
# Restore the main mutable working mount to a pristine captured baseline. All
# individual mutations and outputs remain separately retained under cases/.
f=R/'fixtures/full_recursive_mount'
if f.exists():shutil.rmtree(f)
shutil.copytree(R/'inputs/current',f)
save('CUSTODY_AND_BASELINE_VALIDATION.json',dict(at=now(),captured_file_entries_checked=len(inp['files']),captured_input_mismatches=bad,all_prior1395_sealed_files_match=True,current_baselines_match_independent_counts_and_identities=True,original21_case_inventory_and_results_verified=True,normal_and_optimized_executions=388,new_cases_per_mode=173,new_false_accepts_per_mode=29,publication_count=4,review_completion_estimate_percent=100,scientific_publication_approval=False))
log=read('RESEARCH_LOG.json');log.append(dict(at=now(),completion_estimate_percent=100,event='Bounded fresh review completed. Original21 controls pass per mode; new173 cases yield29 false accepts per mode (27material-evidence cases,2lower-severity exact-type cases). Report documents R1–R4; further canonical accounting repair required. All captured inputs validated, valid baseline matches independent counts/identities, no provider or canonical writes.'))
save('RESEARCH_LOG.json',log)
files=[]
for p in sorted(R.rglob('*')):
 if p.name=='OUTPUT_MANIFEST.json':continue
 rel=str(p.relative_to(R))
 if p.is_symlink():files.append(dict(path=rel,type='symlink',target=os.readlink(p)))
 elif p.is_file():
  b=p.read_bytes();files.append(dict(path=rel,type='regular',bytes=len(b),sha256=sha(b)))
save('OUTPUT_MANIFEST.json',dict(at=now(),scope='Every review-local regular file and symlink; excludes only this self-referential manifest. Source captures, programs, complete recursive baseline mounts, per-case mutations/outputs, report and logs included.',files=files))
for x in files:
 p=R/x['path']
 if x['type']=='regular':require(p.stat().st_size==x['bytes'] and sha(p.read_bytes())==x['sha256'],'Final output seal mismatch '+x['path'])
 else:require(p.is_symlink() and os.readlink(p)==x['target'],'Final symlink seal mismatch')
print(json.dumps(dict(output_files=len(files),output_manifest_sha256=sha((R/'OUTPUT_MANIFEST.json').read_bytes()),captured_inputs_checked=len(inp['files']),review_completion_estimate_percent=100),indent=2))
