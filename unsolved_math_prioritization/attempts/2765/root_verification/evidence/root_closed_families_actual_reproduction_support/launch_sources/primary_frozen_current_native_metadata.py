from pathlib import Path
import json,hashlib,datetime
root=Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr38_2765/tmp/root_pr38_actual_f4mchuie');out=Path(__file__).resolve().parent;target='2765';found={}
for name in ['state.json','assessments.json','catalog.json']:
 p=root/'unsolved_math_prioritization'/name;v=json.loads(p.read_text())
 x=v.get(target) if isinstance(v,dict) else [r for r in v if isinstance(r,dict) and str(r.get('id'))==target]
 found[name]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'target':x}
rp=root/'unsolved_math_prioritization/review_v2/related_target_groups.json';rv=json.loads(rp.read_text());found['related_target_groups']={'sha256':hashlib.sha256(rp.read_bytes()).hexdigest(),'target_mentions':[]}
def scan(x,path=''):
 if isinstance(x,dict):
  if target in json.dumps(x) and not any(isinstance(v,(dict,list)) for v in x.values()):found['related_target_groups']['target_mentions'].append({'path':path,'value':x})
  for k,v in x.items():scan(v,path+'/'+str(k))
 elif isinstance(x,list):
  if target in [str(v) for v in x]:found['related_target_groups']['target_mentions'].append({'path':path,'value':x})
  for i,v in enumerate(x):scan(v,path+'/'+str(i))
scan(rv)
history=[]
hp=root/'unsolved_math_prioritization/history.jsonl'
for i,line in enumerate(hp.read_text().splitlines(),1):
 v=json.loads(line)
 if str(v.get('id'))==target:history.append({'line':i,'event':v})
found['history_target']={'sha256':hashlib.sha256(hp.read_bytes()).hexdigest(),'events':history}
ip=root/'draft_pr_publication_program_20260930/inventory.json';inv=json.loads(ip.read_text());entries=[]
def pick(x):
 if isinstance(x,dict):
  if any(str(x.get(k))=='38' for k in ['number','pr_number','pr']):entries.append(x);return
  for v in x.values():pick(v)
 elif isinstance(x,list):
  for v in x:pick(v)
pick(inv);found['inventory_entry']=entries
pin=out/'original_pin';rs=json.loads((pin/'review/review_summary.json').read_text());found['review_manifest_integrity']={k:{'listed_sha256':h,'actual_sha256':hashlib.sha256((pin/'review'/k).read_bytes()).hexdigest(),'match':h==hashlib.sha256((pin/'review'/k).read_bytes()).hexdigest()} for k,h in rs['files'].items()}
found['at']=datetime.datetime.now(datetime.timezone.utc).isoformat();(out/'POST_SEAL_HISTORY_METADATA.json').write_text(json.dumps(found,indent=2)+'\n');print(json.dumps(found,indent=2))
