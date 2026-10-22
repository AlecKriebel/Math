from pathlib import Path
import json,re,hashlib,datetime
E=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7'); O=E/'reviews/range0344_0396_adversary'; P=E/'private/pr0344_0396_review'
initial=json.loads((O/'independent_classification_initial.json').read_text())['classifications']
journal=[]
for line in (E/'dispositions.jsonl').read_text().splitlines():
 m=re.search(r'"pr"\s*:\s*(\d+)',line)
 if m and 344<=int(m.group(1))<=396:journal.append(json.loads(line))
rows=[]; faults=[]
for a in initial:
 n=a['pr']; d=json.loads((E/f'PR{n:04d}_DISPOSITION.json').read_text()); e=json.loads((E/f'eligibility/pr{n:04d}.json').read_text()); j=[x for x in journal if x['pr']==n]
 actual={f['path']:f for f in a['changed_paths']}; cached={f['filename']:f for f in e['files']}
 checks={'single_journal_entry':len(j)==1,'journal_matches_receipt':len(j)==1 and j[0]==d,'receipt_pr':d['pr']==n,'receipt_head':d['inventory_head_sha']==a['head'],'receipt_base':d['inventory_base_sha']==a['input_base'],'receipt_ids':d['problem_ids']==a['problem_ids'],'eligibility_pin':e['inventory_head_sha']==a['head'] and e['inventory_base_sha']==a['input_base'],'eligibility_exact_changed_paths':set(e['changed_paths'])==set(actual)==set(cached),'eligibility_count':e['file_count']==len(actual),'eligibility_no_duplicate_paths':len(e['changed_paths'])==len(set(e['changed_paths'])) and len(e['files'])==len(cached)==len(actual),'eligibility_every_head_blob':all(f['head_git_blob']==cached[p]['sha'] for p,f in actual.items()) if set(cached)==set(actual) else False,'eligibility_added_own_statuses':sorted((r['problem_id'],r['status'],r['turns']) for r in e['added_queue_rows'] if r['problem_id'] in a['problem_ids'])==sorted((r['problem_id'],r['status'],r['turns']) for r in a['changed_corresponding_rows'])}
 cls=a['independent_preclassification']; expected={'explicit_nonclaim_queue':'skip_explicit_non_claimed_solved','claimed_solved_requires_publication_or_audit':'skip_entirely_already_published','no_usable_changed_own_queue_requires_substantive_read':'skip_inferred_no_full_solution_claim'}[cls]
 checks['disposition_matches_independent_semantics']=d['disposition']==expected
 if cls=='explicit_nonclaim_queue':checks['recorded_status_matches_actual']=sorted(d['explicit_pr_queue_statuses'])==sorted(set(r['status'] for r in a['changed_corresponding_rows']))
 if n==363:
  S=E/'audits/pr0363_11000228';s=json.loads((S/'SOURCE_SNAPSHOT.json').read_text())
  checks.update(snapshot_pin=s['head']==a['head'] and s['comparison_base']==a['input_base'] and s['comparison_merge_base']==a['actual_merge_base'],snapshot_exact_paths=set(s['exact_pinned_changed_paths'])==set(actual),snapshot_file_list_exact=set(x['repository_path'] for x in s['files'])==set(actual),snapshot_no_duplicate_paths=len(s['exact_pinned_changed_paths'])==len(set(s['exact_pinned_changed_paths']))==len(s['files'])==len(actual),snapshot_every_blob=all(x['git_blob']==actual[x['repository_path']]['head_git_blob'] and x['sha256']==actual[x['repository_path']]['sha256'] and x['bytes']==actual[x['repository_path']]['bytes'] and hashlib.sha256((S/x['local']).read_bytes()).hexdigest()==x['sha256'] for x in s['files']),snapshot_no_queue=s['no_queue_change'] and not a['changed_corresponding_rows'] and len((P/'pr0363_queue.patch').read_bytes())==0)
  checks['missing_status_flag']=d['missing_status_case'] and d['explicit_pr_queue_statuses']==[]
 for k,v in checks.items():
  if not v:faults.append({'pr':n,'check':k})
 rows.append({'pr':n,'problem_ids':a['problem_ids'],'actual_statuses':[r['status'] for r in a['changed_corresponding_rows']],'disposition':d['disposition'],'checks':checks,'eligibility_receipt_sha256':hashlib.sha256((E/f'eligibility/pr{n:04d}.json').read_bytes()).hexdigest(),'disposition_receipt_sha256':hashlib.sha256((E/f'PR{n:04d}_DISPOSITION.json').read_bytes()).hexdigest()})
result={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':[344,396],'expected_unique_pr_count':53,'journal_entries':len(journal),'contiguous_unique':sorted(x['pr'] for x in journal)==list(range(344,397)),'checks':rows,'faults':faults}
(O/'receipt_reconciliation.json').write_text(json.dumps(result,indent=2)+'\n')
(P/'scoped_dispositions_snapshot.json').write_text(json.dumps(journal,indent=2)+'\n')
print(json.dumps({'journal':len(journal),'contiguous_unique':result['contiguous_unique'],'faults':faults},indent=2))
