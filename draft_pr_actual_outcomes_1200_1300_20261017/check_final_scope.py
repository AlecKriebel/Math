#!/usr/bin/env python3
"""Read-only identity/outcome comparison after every admitted case completes.

This does not review proofs or automatically adjudicate new outcome claims.
Any excluded-case drift or nonempty activity requires a separate semantic read.
"""
from pathlib import Path
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('capture');args=parser.parse_args()
capture=(ROOT/args.capture).resolve()
if not capture.is_relative_to(ROOT):raise RuntimeError('Own capture folder required')
state=json.loads((ROOT/'PROGRAM_STATE.json').read_text())
eligible=[1205,1211,1216,1225,1241,1261,1262,1268,1271,1274,1280,1283]
if state['eligible_prs']!=eligible or state['completed_prs']!=eligible or state['current_pr'] is not None:raise RuntimeError('All12 original admissions must finish first')
old=json.loads((ROOT/'PR_OUTCOME_METADATA.json').read_text())['data']['repository']
live=json.loads((capture/'FINAL_LIVE_METADATA.json').read_text())['data']['repository']
if set(live)!={'p'+str(n) for n in range(1200,1301)}:raise RuntimeError('Exact101 final records required')
pubs={r['pr']:r for r in state['publications']}
if set(pubs)!=set(eligible) or len({p['doi'] for p in pubs.values()})!=12:raise RuntimeError('Twelve unique completed publications required')
completed=[];skipped=[];activity=[]
for n in range(1200,1301):
 current=live['p'+str(n)];prior=old['p'+str(n)]
 if n in pubs:
  p=pubs[n]
  if current['state']!='MERGED' or current['isDraft'] is not False or current['baseRefName']!='main' or current['headRefOid']!=p['reviewed_head'] or current['mergeCommit']['oid']!=p['merge_commit'] or p['doi'] not in current['body']:raise RuntimeError('Completed identity/body/merge differs PR'+str(n))
  completed.append({'pr':n,'head':current['headRefOid'],'merge_commit':current['mergeCommit']['oid'],'doi':p['doi'],'tracker_range':p['tracker_range'],'body_sha256':hashlib.sha256(current['body'].encode()).hexdigest()})
 else:
  changed=[field for field in ['body','headRefOid','updatedAt','state','isDraft','baseRefName'] if current[field]!=prior[field]]
  skipped.append({'pr':n,'changed_fields':changed,'original_exclusion_retained_if_no_new_full_claim':True,'mathematical_processing_performed':False})
 for kind in ['comments','reviews']:
  data=current.get(kind)
  if not isinstance(data,dict) or not isinstance(data.get('totalCount'),int) or not isinstance(data.get('nodes'),list):raise RuntimeError('Latest activity metadata missing PR'+str(n))
  if data['totalCount']:
   activity.append({'pr':n,'kind':kind,'total_count':data['totalCount'],'latest':data['nodes']})
result={'status':'PASS_IDENTITIES_ONLY_SEMANTIC_SCOPE_ADJUDICATION_SEPARATE','records':101,'completed':completed,'skipped':skipped,'excluded_drift_prs':[r['pr'] for r in skipped if r['changed_fields']],'nonempty_activity':activity,'scope':'No skipped proof, mathematical audit, repair, merge, close, comment or publication operation. Reconcile any changed recorded outcomes and latest activity explicitly before marking the goal complete.'}
print(json.dumps(result,indent=2))
