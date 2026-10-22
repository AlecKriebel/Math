from pathlib import Path
import datetime as dt,hashlib,json,re,subprocess,sys
Q=Path(__file__).resolve().parent;R=Q/'inputs/current'
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
s=json.loads((R/'STATE.json').read_text());j=[json.loads(l) for l in (R/'dispositions.jsonl').read_text().splitlines()];assert [v['pr'] for v in j]==list(range(9,s['next_pr']));eff={v['pr']:v for v in j};old=(R/'PR0280_DISPOSITION.json').read_bytes();assert sha(old)=='12786fed27bdc64dc25404de4d559f04611947006cfb62f0ee6e8bf1399009b1';assert json.loads(old)['disposition']=='skip_priority_gate_not_met'
for o in s['reopened_disposition_overrides']:
 assert o['pr']==280 and o['historical_disposition_sha256']==sha(old);replacement=json.loads((R/o['replacement_disposition']).read_text());eff[280]=replacement
expected={292:('30001608',23524971,174),397:('9700002',23527793,176),399:('30001179',23539283,177),280:('30000156',23539734,178)};rows=[]
for item in s['completed_publications']:
 pr=item['pr'];problem,record,row=expected[pr];doi=f'10.5281/zenodo.{record}';assert (item['problem_id'],item['record'],item['ledger_row'],item['doi'])==(problem,record,row,doi);proof=json.loads((R/item['verification']).read_text());entry=eff[pr]
 assert proof['pr']==pr and proof['record']==record and proof['ledger_row']==row and proof['doi']==doi and proof['problem_ids']==[problem] and proof['merge_commit']==item['merge_commit'];assert entry['publication_evidence']==item['verification'] and entry['new_publication'] is True and entry['disposition']=='published_verified_full_solution'
 ledger=json.loads((R/proof['evidence']['ledger']).read_text());assert ledger['pr']==pr and ledger['row_number']==row and ledger['doi']==doi and ledger['spreadsheet_id']=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20' and ledger['sheet_gid']==1254632077;assert len(ledger['values'])==4 and ledger['values'][2]=='https://doi.org/'+doi and problem in ledger['values'][0] and f'https://github.com/AlecKriebel/Math/pull/{pr}' in ledger['values'][3] and f'https://zenodo.org/records/{record}' in ledger['values'][3]
 assert proof['published'] is True and proof['ledger_read_back_exact'] is True and proof['unique_target_and_DOI'] is True;files=proof['files'];assert len(files)==2 and {Path(f['name']).suffix for f in files}=={'.pdf','.zip'}
 if pr==292:assert sha((R/item['verification']).read_bytes())=='ad5cad544399809004b1007a2758444fbc43891ad28a4745fffa805f46987cf2'
 else:
  public=json.loads((R/proof['evidence']['public_files']).read_text());assert public['pr']==pr and public['record']==record and public['doi']==doi;assert {f['name']:(f['bytes'],f['sha256']) for f in public['files']}=={f['name']:(f['bytes'],f['sha256']) for f in files};z=next(f for f in files if f['name'].endswith('.zip'));assert z['all_manifest_payloads_verified']==z['members']-1
 rows.append(dict(pr=pr,problem=problem,record=record,row=row,doi=doi,files=[dict(name=f['name'],sha256=f['sha256']) for f in files],consistent=True))
assert {p for p,v in eff.items() if v['disposition']=='published_verified_full_solution'}==set(expected)
outputs=[]
for mode,flags in [('normal',[]),('optimized',['-O'])]:
 x=subprocess.run([sys.executable,'-B',*flags,str(R/'coverage_snapshot.py')],capture_output=True);(Q/('baseline_'+mode+'.stdout')).write_bytes(x.stdout);(Q/('baseline_'+mode+'.stderr')).write_bytes(x.stderr);assert x.returncode==0;out=json.loads(x.stdout);assert out['disposition_counts']['published_verified_full_solution']==4 and out['historical_journal_disposition_counts']['published_verified_full_solution']==3 and out['final_reconciliation_complete'] is False;outputs.append(dict(mode=mode,returncode=x.returncode,stdout_sha256=sha(x.stdout)))
save(Q/'INDEPENDENT_IDENTITY_AND_BASELINE.json',dict(at=now(),identities=rows,baselines=outputs,assertion='All four actual captured local crossartifact identities/labels and effective/raw counts agree. No live provider/proof/priority endorsement.'))
print(json.dumps(dict(four_identities_consistent=True,two_baselines_pass=True)))
