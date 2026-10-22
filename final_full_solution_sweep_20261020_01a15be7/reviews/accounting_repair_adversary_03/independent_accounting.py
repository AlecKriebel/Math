from pathlib import Path
import collections, datetime as dt, hashlib, json, os, subprocess, sys
sys.dont_write_bytecode=True
os.environ.update(PYTHONDONTWRITEBYTECODE="1",GIT_OPTIONAL_LOCKS="0")
R=Path(__file__).resolve().parent
F=R/'inputs/current'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(n):return json.loads((F/n).read_text())
def save(n,v):(R/n).write_text(json.dumps(v,indent=2)+"\n")
s=load('STATE.json');inv=load('rest_inventory.json');journal=[json.loads(x) for x in (F/'dispositions.jsonl').read_text().splitlines() if x.strip()]
nums=[e['pr'] for e in journal];known=[e['number'] for e in inv['pull_requests']]
assert nums==list(range(s['start_pr'],s['next_pr'])) and len(nums)==s['completed_pr_count']
assert s['last_completely_processed_pr']==s['next_pr']-1
assert all(load(f"PR{e['pr']:04d}_DISPOSITION.json")==e for e in journal)
assert all(type(n) is int for n in nums+known) and len(known)==len(set(known))==inv['in_scope_pr_count'] and max(known)==inv['highest_pr']
assert set(known).isdisjoint(inv['numeric_gaps']) and set(known)|set(inv['numeric_gaps'])==set(range(s['start_pr'],inv['highest_pr']+1))
raw=dict(collections.Counter(e['disposition'] for e in journal));effective={e['pr']:e for e in journal}
assert len(s['reopened_disposition_overrides'])==1
o=s['reopened_disposition_overrides'][0];assert o['pr']==280
old=load('PR0280_DISPOSITION.json');oldhash=sha((F/'PR0280_DISPOSITION.json').read_bytes());rep=load(o['replacement_disposition'])
assert old['disposition']=='skip_priority_gate_not_met' and oldhash==o['historical_disposition_sha256']==rep['historical_disposition_sha256']=='12786fed27bdc64dc25404de4d559f04611947006cfb62f0ee6e8bf1399009b1'
effective[280]=rep
counts=dict(collections.Counter(e['disposition'] for e in effective.values()))
expected={292:('30001608',23524971,174),397:('9700002',23527793,176),399:('30001179',23539283,177),280:('30000156',23539734,178)}
assert {e['pr'] for e in s['completed_publications']}==set(expected)
assert {n for n,e in effective.items() if e['disposition']=='published_verified_full_solution'}==set(expected)
records=[]
for own in s['completed_publications']:
 n=own['pr'];problem,record,row=expected[n];doi='10.5281/zenodo.'+str(record);p=load(own['verification']);e=effective[n];l=load(p['evidence']['ledger']);public=load(p['evidence']['public_files']) if 'public_files' in p['evidence'] else None
 assert (own['problem_id'],own['record'],own['ledger_row'],own['doi'])==(problem,record,row,doi)
 assert p['pr']==e['pr']==l['pr']==n and p['doi']==e['doi']==l['doi']==doi and p['record']==record
 assert p['problem_ids']==e['problem_ids']==[problem] and p['ledger_row']==e['ledger_row']==l['row_number']==row
 assert own['merge_commit']==p['merge_commit'] and p['published'] is True and e['new_publication'] is True
 assert l['values'][2] in [doi,'https://doi.org/'+doi] and problem in l['values'][0] and 'https://github.com/AlecKriebel/Math/pull/'+str(n) in l['values'][3]
 assert l['spreadsheet_id']==s['spreadsheet_id']=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20' and l['sheet_gid']==s['sheet_gid']==1254632077
 assert p['doi_resolution']['resolved_url']=='https://zenodo.org/records/'+str(record)
 if 'range' in l:assert l['range']==f"'Math Puzzles'!A{row}:D{row}"
 if public:
  assert public['pr']==n and public['record']==record and public['doi']==doi and public['files']==p['files'] and public['record_http_status']==200
  assert public['doi_resolution']==p['doi_resolution'] and public['title']==p['title']
  if 'version' in p:assert public['version']==p['version']
 else:
  assert n==292 and sha((F/own['verification']).read_bytes())=='ad5cad544399809004b1007a2758444fbc43891ad28a4745fffa805f46987cf2'
  z=next(f for f in p['files'] if f['name'].endswith('.zip'))
  assert any(Path(m).name=='MANIFEST.json' for m in z['members']) and len(z['members'])==len(set(z['members']))
 records.append(dict(completed=own,effective=e,root_receipt_sha256=sha((F/own['verification']).read_bytes()),ledger=l,files=p['files'],public_receipt_sha256=sha((F/p['evidence']['public_files']).read_bytes()) if public else None))
out=dict(at=dt.datetime.now(dt.timezone.utc).isoformat(),source_sha256=sha((F/'coverage_snapshot.py').read_bytes()),next_pr=s['next_pr'],prefix=dict(start=s['start_pr'],through=s['last_completely_processed_pr'],count=len(nums)),inventory=dict(highest=inv['highest_pr'],count=len(known),gaps=inv['numeric_gaps']),historical_counts=raw,effective_counts=counts,historical280=dict(sha256=oldhash,disposition=old['disposition']),own_publication_count=len(records),records=records,note='Direct independent computation without importing or executing the reviewed validator; actual local canonical captures show no material identity contradiction.')
comparisons=[]
for mode,flags in [('normal',[]),('optimized',['-O'])]:
 p=subprocess.run([sys.executable,'-B',*flags,str(F/'coverage_snapshot.py')],env=os.environ,cwd=R,capture_output=True)
 (R/(mode+'_baseline.stdout')).write_bytes(p.stdout);(R/(mode+'_baseline.stderr')).write_bytes(p.stderr)
 assert p.returncode==0
 emitted=json.loads(p.stdout)
 assert emitted['disposition_counts']==counts and emitted['historical_journal_disposition_counts']==raw and emitted['next_pr']==s['next_pr'] and emitted['own_completed_publications']==s['completed_publications']
 comparisons.append(dict(mode=mode,returncode=p.returncode,independent_counts_equal=True,stdout_sha256=sha(p.stdout),stderr_sha256=sha(p.stderr)))
out['baseline_comparisons']=comparisons
save('INDEPENDENT_ACCOUNTING.json',out)
print(json.dumps({k:out[k] for k in ['next_pr','prefix','historical_counts','effective_counts','own_publication_count','baseline_comparisons']},indent=2))
