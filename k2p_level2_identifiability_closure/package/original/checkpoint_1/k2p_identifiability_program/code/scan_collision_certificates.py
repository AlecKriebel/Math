#!/usr/bin/env python3
from pathlib import Path
import json,re,ast
ROOT=Path('/mnt/data/Math_k2p_work');OUT=Path('/mnt/data/k2p_identifiability_program')
records=[]
def summarize(obj,depth=0):
 if depth>4:return type(obj).__name__
 if isinstance(obj,dict):
  return {str(k):summarize(v,depth+1) for k,v in list(obj.items())[:80]}
 if isinstance(obj,list):
  return {'list_len':len(obj),'sample':[summarize(v,depth+1) for v in obj[:4]]}
 return repr(obj)[:200]
for p in ROOT.rglob('*.json') if ROOT.exists() else []:
 if p.stat().st_size>10_000_000:continue
 low=str(p.relative_to(ROOT)).lower()
 try:obj=json.loads(p.read_text(errors='replace'))
 except:continue
 text=json.dumps(obj)[:500000].lower()
 score=sum(k in low or k in text for k in ['k2p','kimura','collision','theta','continuous_time','continuous-time','jacobian','rank_minor'])
 if score<3:continue
 records.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'score':score,'schema':summarize(obj)})
(OUT/'certificates/collision_json_schema_scan.json').write_text(json.dumps(records,indent=2))
md=['# Collision certificate schema scan','',f'Candidate JSON files: {len(records)}','']
for r in sorted(records,key=lambda x:(-x['score'],x['path'])):
 md += [f"## `{r['path']}`",'',f"- bytes: {r['bytes']}",f"- relevance score: {r['score']}",'','```json',json.dumps(r['schema'],indent=2)[:12000],'```','']
(OUT/'source_extracts/COLLISION_CERTIFICATE_SCHEMA_SCAN.md').write_text('\n'.join(md)+'\n')
