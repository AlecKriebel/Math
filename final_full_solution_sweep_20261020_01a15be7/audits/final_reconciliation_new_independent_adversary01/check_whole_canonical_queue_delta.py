"""Independent whole canonical QUEUE delta and claim-coverage replay; read-only."""
from pathlib import Path
import hashlib,base64,re,sys,json
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7')
W=R/'audits/final_reconciliation_new_independent_adversary01'
p=W/'independent_checks.py';b=p.read_bytes()
assert hashlib.sha256(b).hexdigest()=='63f9f0d1cd4d8e8d87b3c087ce8db2535ef526db3f359e2df7f4c13ce550aa8a'
n={'__name__':'_readonly_whole_queue_delta','__file__':str(p)};exec(compile(b,str(p),'exec'),n)
oldpin={'path':str(R/'CURRENT_CANONICAL_QUEUE_SNAPSHOT.json'),'bytes':999851,'sha256':'f0c2555ab5929865dc3ec09240ce46a0fa46c12f27abbab141182bc0e4febd9d'}
bodypin={'path':str(R/'audits/root_final_canonical_queue_live_reconciliation01/CURRENT_COMPLETE_QUEUE_BODY_AND_BLOB.json.gz'),'bytes':413150,'sha256':'763f57434be9c48489c5e266b5ef481c936a84b3e16f9196a07e44622b98b09f'}
old=n['objpin'](oldpin);blob=n['objpin'](bodypin);body=base64.b64decode(blob['decoded_bytes_base64'],validate=True)
assert n['H'](body)=='2b48dea11ecc3d701e7fb29a6684bfb2ec1c14d3369541462fa13292abebc38b'
j=n['frozen_join']()['baseline']();fresh={}
for line in body.decode('utf-8').splitlines():
 if not re.match(r'^\|\s*\d+\s*\|',line):continue
 cs=[x.strip()for x in line.strip().strip('|').split('|')];pid=cs[1].split(' / ')[0]
 assert pid not in fresh
 fresh[pid]={'rank':int(cs[0]),'problem_id':pid,'problem_alias':cs[1],'problem_title':cs[2],'status':cs[7],'turns':cs[8],'source_line':line}
assert len(fresh)==len(old['rows'])==1951 and fresh.keys()==old['rows'].keys()
expected={'30003185':1330,'30003208':1329,'30003225':1332,'30004534':1337,'10000037':1348,'30002726':1372,'30005740':1391,'1200024':1407}
d=[]
for pid in sorted(fresh):
 if n['typed'](fresh[pid],old['rows'][pid]):continue
 row=fresh[pid];prior=old['rows'][pid]
 assert pid in expected and prior['status']=='queued'and row['status']=='claimed_solved'
 assert {k for k in row if not n['typed'](row[k],prior[k])}=={'status','turns','source_line'}
 matches=[x for x in j['rows']if pid in x['problem_ids']]
 assert len(matches)==1 and matches[0]['pr']==expected[pid]
 x=matches[0]
 assert x['historical_claimed_marker']is True and x['explicit_historical_QUEUE_statuses']==['claimed_solved']and x['effective_coverage_bucket']=='publication_recorded'
 pubs=[p for p in j['own_publications']if p['pr']==x['pr']]
 assert len(pubs)==1 and x['coverage']['doi']==pubs[0]['doi']and x['coverage']['row']==pubs[0]['ledger_row']
 d.append({'problem_id':pid,'pr':x['pr'],'old_full_row':prior,'current_full_row':row,'actual_dated_coverage':x['coverage']})
assert {x['problem_id']for x in d}==set(expected)
print(json.dumps({'status':'PASS_DATED_ALL1951_CANONICAL_ROWS_AND_NEW_CLAIM_DELTAS_COVERED','historical_observed_at':old['at'],'current_native_bracket':['2026-10-23T01:24:49.835643+00:00','2026-10-23T01:24:53.407449+00:00'],'old_snapshot':oldpin,'complete_current_body':bodypin,'all_ranked_rows_checked':1951,'unchanged_complete_rows':1943,'new_or_missing_ids':[],'changed_rows':d,'conclusion':'All eight newly claimed canonical rows were already explicit historical PR claims and are among actual13 recorded own papers. No other canonical ranked-row changes; no hidden QUEUE-only new claim detected.','final_clearance':False,'scope':'Dated whole-QUEUE comparison. Accepted blob identity must persist at final checkpoint; no current/future PR or ledger completeness inferred.'},sort_keys=True,indent=2,ensure_ascii=False))
