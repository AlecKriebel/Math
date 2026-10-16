#!/usr/bin/env python3
"""Gate on exact QUEUE status before any selected PR body/artifact inspection."""
import concurrent.futures,datetime,hashlib,json,re,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent;REPO='AlecKriebel/Math'
def gh(*a):return subprocess.check_output(['gh',*a])
def raw(path,head):return gh('api',f'repos/{REPO}/contents/{path}?ref={head}','-H','Accept: application/vnd.github.raw+json')
def freeze(number):
 meta=json.loads(gh('pr','view',str(number),'--repo',REPO,'--json','number,title,state,isDraft,headRefName,headRefOid,url'))
 queue=raw('unsolved_math_prioritization/QUEUE.md',meta['headRefOid'])
 ids=list(dict.fromkeys(re.findall(r'(?<!\d)\d{4,9}(?!\d)',meta['title']+' '+meta['headRefName'])))
 rows={};col=None
 for line in queue.decode().splitlines():
  if not line.startswith('|'):continue
  c=[x.strip() for x in line.split('|')[1:-1]]
  if 'Status' in c and 'ID / code' in c:col=c.index('Status')
  if col is None or len(c)<=col:continue
  m=re.match(r'(\d{4,9})(?:\s|/|$)',c[1])
  if m and m.group(1) in ids:rows[m.group(1)]={'status':c[col],'line':line}
 if meta['state']!='OPEN' or not meta['isDraft'] or not rows or any(v['status']!='claimed_solved' for v in rows.values()):
  print(json.dumps({'scope':'skip','metadata':meta,'statuses':{k:v['status'] for k,v in rows.items()}},indent=2));return
 if len(rows)!=1:raise RuntimeError('Multiple mapped problems; root must assess exact scope')
 problem=next(iter(rows));P=R/f'audits/pr{number}_{problem}'
 if P.exists():raise RuntimeError('Snapshot already exists; never overwrite')
 P.mkdir(parents=True)
 frozen_head=meta['headRefOid']
 meta=json.loads(gh('pr','view',str(number),'--repo',REPO,'--json','number,title,state,isDraft,headRefName,headRefOid,url,body,files,comments,reviews,baseRefName'))
 if meta['headRefOid']!=frozen_head or meta['headRefOid']!=json.loads(gh('pr','view',str(number),'--repo',REPO,'--json','headRefOid'))['headRefOid']:raise RuntimeError('Moving head during capture')
 P.joinpath('pr_metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 P.joinpath('selected_queue_row.md').write_text(rows[problem]['line']+'\n')
 prefix=f'unsolved_math_prioritization/attempts/{problem}/'
 paths=[x['path'] for x in meta['files'] if x['path'].startswith(prefix)]
 if not paths:raise RuntimeError('No selected attempt artifacts; inspect changed-path metadata')
 def one(path):
  data=raw(path,meta['headRefOid']);out=P/'source_snapshot'/path;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
  return {'path':path,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:files=list(pool.map(one,paths))
 receipt={'captured_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':number,'problem_id':problem,'head_sha':meta['headRefOid'],'scope_gate':'exact claimed_solved','queue_sha256':hashlib.sha256(queue).hexdigest(),'selected_queue_row':rows[problem]['line'],'files':files,'other_changed_paths':[x['path'] for x in meta['files'] if not x['path'].startswith(prefix)]}
 P.joinpath('SOURCE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
 P.joinpath('RESEARCH_LOG.md').write_text('# Research log\n\n## '+receipt['captured_at_utc']+' — Exact claimed-solved source freeze\n\nHead/status gate passed, target artifacts frozen by SHA256. No new proof-search turn, mutation, publication, or acceptance. Completion estimate: 5% of selected PR disposition.\n')
 print(json.dumps({'scope':'eligible','folder':str(P),'pr':number,'problem_id':problem,'head_sha':meta['headRefOid'],'files':paths,'selected_queue_row':rows[problem]['line'],'other_changed_paths':receipt['other_changed_paths']},indent=2))
if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('pr',type=int);freeze(a.parse_args().pr)
