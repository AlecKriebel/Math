"""Validate exhaustive individual reviews and bind them to the pinned input."""
import argparse,collections,hashlib,json,pathlib,sqlite3
ROOT=pathlib.Path(__file__).resolve().parents[1]
HERE=ROOT/'review_v2'
def read(p):return json.loads(p.read_text())
def validate(require_complete=True):
 manifest=read(HERE/'assignments.json'); source=read(ROOT/'manifest.json')
 if manifest['source_revision']!=source['revision']:raise ValueError('Source changed while reviews were in progress')
 allreviews={};counts=[]
 for shard,expected in enumerate(manifest['shards']):
  path=HERE/f'reviews_{shard}.json';items=read(path) if path.exists() else []
  seen=set()
  for item in items:
   key=item['id']
   if key not in expected or key in seen or key in allreviews:raise ValueError('Wrong shard or duplicate ID: '+str(key))
   for field in ['impact','p_solve','p_valid_open']:
    v=item[field]
    if not isinstance(v,(int,float)) or not (0<v<=10 if field=='impact' else 0<=v<=1):raise ValueError('Invalid score '+key)
   if item['route'] not in ['proof','hybrid','large_search','unclear']:raise ValueError('Invalid route '+key)
   if item['decision'] not in ['candidate','defer','exclude','repair']:raise ValueError('Invalid decision '+key)
   if not isinstance(item['note'],str) or len(item['note'].split())<6:raise ValueError('Missing individual rationale '+key)
   seen.add(key);allreviews[key]={**item,'reviewer_shard':shard}
  counts.append({'shard':shard,'reviewed':len(seen),'required':len(expected)})
  if require_complete and seen!=set(expected):raise ValueError(f'Incomplete shard {shard}: {len(seen)}/{len(expected)}')
 return allreviews,counts

def merge(exclusion_policy):
 reviews,counts=validate()
 old=read(ROOT/'assessments.json')
 c=sqlite3.connect(ROOT/'cache/catalog.sqlite');assessments={}
 for key,payload,report in c.execute('select key,payload,report from records'):
  p,r=json.loads(payload),json.loads(report);rev=reviews[key];prior=old.get(key,{})
  holds=[]
  if rev['route']=='large_search':holds.append('large_exhaustive_search')
  if rev['decision']!='candidate':holds.append('desk_review_'+rev['decision'])
  if rev['route']=='unclear':holds.append('no_concrete_proof_route')
  assessments[key]={**rev,'review_type':'individual short five-turn desk review','review_policy':'2.0-five-turn-proof',
   'review_hash':hashlib.sha256(json.dumps([p,r],sort_keys=True).encode()).hexdigest(),
   'statement_hash':hashlib.sha256(p['statement'].encode()).hexdigest(),
   'rationale':rev['note'],'remaining_gap':'Full exact source target; see individual note and source statement.',
   'first_experiment':'Check current literature and exact hypotheses; pursue the named proof mechanism within five turns.',
   'holds':list(dict.fromkeys(prior.get('holds',[])+holds)),
   'sources':prior.get('sources') or [p.get('source_url') or 'Pinned UnsolvedMath record '+key],
   'confidence':'low; not empirically calibrated'}
 (ROOT/'assessments.json').write_text(json.dumps(assessments,ensure_ascii=False,indent=2)+'\n')
 policy=read(HERE/'policy_v2.json');policy['exclusion_policy']=exclusion_policy
 (ROOT/'policy.json').write_text(json.dumps(policy,indent=2)+'\n')
 print('Merged',len(assessments),'individually reviewed records')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--merge',action='store_true');p.add_argument('--exclusion-policy',choices=['exclude_resolved','exclude_open_and_resolved']);a=p.parse_args()
 if a.merge:
  if not a.exclusion_policy:p.error('--exclusion-policy required for merge')
  merge(a.exclusion_policy)
 else:
  reviews,counts=validate(False);print(json.dumps({'counts':counts,'total_reviewed':len(reviews),'decisions':dict(collections.Counter(r['decision'] for r in reviews.values()))},indent=2))
