"""Validate exhaustive individual reviews and bind them to the pinned input."""
import argparse,collections,hashlib,json,math,os,pathlib,re,sqlite3,tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
HERE=ROOT/'review_v2'
def read(p):return json.loads(p.read_text())
def validate_record(item,key):
 if item.get('id')!=key:raise ValueError('Review ID mismatch: '+str(key))
 for field in ['impact','p_solve','p_valid_open']:
  v=item.get(field)
  if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or not (0<v<=10 if field=='impact' else 0<=v<=1):raise ValueError('Invalid score '+key)
 if item.get('route') not in ['proof','hybrid','large_search','unclear']:raise ValueError('Invalid route '+key)
 if item.get('decision') not in ['candidate','defer','exclude','repair']:raise ValueError('Invalid decision '+key)
 if not isinstance(item.get('note'),str) or len(item['note'].split())<6:raise ValueError('Missing individual rationale '+key)
 if 'holds' in item and (not isinstance(item['holds'],list) or any(not isinstance(h,str) for h in item['holds'])):raise ValueError('Invalid holds '+key)

def validate(require_complete=True):
 manifest=read(HERE/'assignments.json'); source=read(ROOT/'manifest.json')
 if manifest['source_revision']!=source['revision']:raise ValueError('Source changed while reviews were in progress')
 expected_ids=[key for shard in manifest['shards'] for key in shard]
 if len(expected_ids)!=len(set(expected_ids)) or len(expected_ids)!=source['records']:raise ValueError('Assignments must cover every source ID exactly once')
 allreviews={};counts=[]
 for shard,expected in enumerate(manifest['shards']):
  path=HERE/f'reviews_{shard}.json';items=read(path) if path.exists() else []
  seen=set()
  for item in items:
   key=item['id']
   if key not in expected or key in seen or key in allreviews:raise ValueError('Wrong shard or duplicate ID: '+str(key))
   validate_record(item,key)
   seen.add(key);allreviews[key]={**item,'reviewer_shard':shard}
  counts.append({'shard':shard,'reviewed':len(seen),'required':len(expected)})
  if require_complete and seen!=set(expected):raise ValueError(f'Incomplete shard {shard}: {len(seen)}/{len(expected)}')
 return allreviews,counts

def merge(exclusion_policy):
 reviews,counts=validate()
 old=read(ROOT/'assessments.json')
 overrides=read(HERE/'adversarial_overrides.json') if (HERE/'adversarial_overrides.json').exists() else {}
 if not isinstance(overrides,dict) or set(overrides)-set(reviews):raise ValueError('Override IDs must identify reviewed source records')
 for key,override in overrides.items():
  if not isinstance(override,dict):raise ValueError('Invalid override '+key)
  validate_record({**reviews[key],**override},key)
 if not (HERE/'policy_v2.json').exists():raise ValueError('Replacement policy missing')
 policy=read(HERE/'policy_v2.json')
 if policy.get('version')!='2.0-five-turn-proof' or policy.get('turn_limit')!=5:raise ValueError('Invalid five-turn policy')
 policy['exclusion_policy']=exclusion_policy
 previous_merge=read(HERE/'merge_manifest.json') if (HERE/'merge_manifest.json').exists() else None
 if previous_merge and hashlib.sha256((ROOT/'assessments.json').read_bytes()).hexdigest()!=previous_merge.get('assessments_sha256'):
  raise ValueError('Current assessments changed after merge; preserve those edits and use assess instead of rebuilding')
 cache=ROOT/'cache/catalog.sqlite'
 if not cache.exists():raise ValueError('Pinned source cache missing; restore it before merging')
 c=sqlite3.connect(f'file:{cache}?mode=ro',uri=True);assessments={}
 source=read(ROOT/'manifest.json')
 try:
  if c.execute('select revision from metadata').fetchone()!=(source['revision'],):raise ValueError('Source cache revision does not match review assignments')
  if {row[0] for row in c.execute('select key from records')}!=set(reviews):raise ValueError('Source cache IDs do not match reviewed IDs')
 except Exception:
  c.close();raise
 for key,payload,report in c.execute('select key,payload,report from records'):
  p,r=json.loads(payload),json.loads(report);rev={**reviews[key],**overrides.get(key,{})};prior=old.get(key,{})
  holds=list(rev.get('holds',[]))
  if rev['route']=='large_search':holds.append('large_exhaustive_search')
  if rev['decision']!='candidate':holds.append('desk_review_'+rev['decision'])
  if rev['route']=='unclear':holds.append('no_concrete_proof_route')
  assessments[key]={**rev,'review_type':'individual short five-turn desk review','review_policy':'2.0-five-turn-proof',
   'review_hash':hashlib.sha256(json.dumps([p,r],sort_keys=True).encode()).hexdigest(),
   'statement_hash':hashlib.sha256(p['statement'].encode()).hexdigest(),
   'rationale':rev['note'],'remaining_gap':'Full exact source target; see individual note and source statement.',
   'first_experiment':'Check current literature and exact hypotheses; pursue the named proof mechanism within five turns.',
   'holds':list(dict.fromkeys(prior.get('holds',[])+holds)),
   'sources':rev.get('sources') or prior.get('sources') or [p.get('source_url') or (re.search(r'Source URL:\s*(https?://[^\s<>]+)',p.get('background') or '').group(1) if re.search(r'Source URL:\s*(https?://[^\s<>]+)',p.get('background') or '') else 'https://huggingface.co/datasets/ulamai/UnsolvedMath')],
   'confidence':'low; not empirically calibrated'}
 c.close()
 assessment_bytes=(json.dumps(assessments,ensure_ascii=False,indent=2)+'\n').encode()
 manifest={'source_revision':source['revision'],'records_reviewed':len(assessments),'coverage':counts,'exclusion_policy':exclusion_policy,'review_files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.glob('reviews_*.json'))},'adversarial_overrides_sha256':hashlib.sha256((HERE/'adversarial_overrides.json').read_bytes()).hexdigest() if (HERE/'adversarial_overrides.json').exists() else None,'assessments_sha256':hashlib.sha256(assessment_bytes).hexdigest()}
 # Prepare every output before replacing any active file; manifest is the final marker.
 outputs={ROOT/'assessments.json':assessment_bytes,ROOT/'policy.json':(json.dumps(policy,indent=2)+'\n').encode(),HERE/'merge_manifest.json':(json.dumps(manifest,indent=2)+'\n').encode()}
 with tempfile.TemporaryDirectory(prefix='.merge-',dir=HERE) as temp:
  staged=[]
  for i,(target,data) in enumerate(outputs.items()):
   path=pathlib.Path(temp)/str(i);path.write_bytes(data);staged.append((path,target))
  for path,target in staged:os.replace(path,target)
 print('Merged',len(assessments),'individually reviewed records')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--merge',action='store_true');p.add_argument('--exclusion-policy',choices=['exclude_resolved','exclude_open_and_resolved']);a=p.parse_args()
 if a.merge:
  if not a.exclusion_policy:p.error('--exclusion-policy required for merge')
  merge(a.exclusion_policy)
 else:
  reviews,counts=validate(False);print(json.dumps({'counts':counts,'total_reviewed':len(reviews),'decisions':dict(collections.Counter(r['decision'] for r in reviews.values()))},indent=2))
