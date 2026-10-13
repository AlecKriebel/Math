#!/usr/bin/env python3
"""Capture only an exact claimed_solved PR, staying on main and never editing remote state."""
import argparse,base64,datetime,hashlib,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).absolute().parent
REPO=ROOT.parent
QUEUE='unsolved_math_prioritization/QUEUE.md'
def run(args):return subprocess.run(args,cwd=REPO,capture_output=True,text=True,check=True).stdout

def queue_row(ref,problem_id):
 blob=json.loads(run(['gh','api',f'repos/AlecKriebel/Math/contents/{QUEUE}?ref={ref}']))
 text=base64.b64decode(blob['content']).decode()
 rows=[];header=None
 for line in text.splitlines():
  cells=[v.strip() for v in line.split('|')][1:-1]
  if cells and cells[0]=='Rank':
   header={name:i for i,name in enumerate(cells)}
   if not {'Rank','ID / code','Status'}<=header.keys():raise RuntimeError('Queue header changed')
  if header and len(cells)>header['Status'] and re.search(rf'(?<!\d){problem_id}(?!\d)',cells[header['ID / code']]):
   rows.append({'problem_id':problem_id,'rank':cells[header['Rank']],'id_code':cells[header['ID / code']],'status':cells[header['Status']]})
 if len(rows)!=1:raise RuntimeError(f'Expected one target row, found {len(rows)}')
 return rows[0]

def main():
 p=argparse.ArgumentParser();p.add_argument('pr',type=int);p.add_argument('problem_id',type=int);p.add_argument('--snapshot',action='store_true');a=p.parse_args()
 if not 500<=a.pr<=600:raise ValueError('Outside authorized range')
 if run(['git','branch','--show-current']).strip()!='main':raise RuntimeError('Shared branch changed')
 meta=json.loads(run(['gh','pr','view',str(a.pr),'--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,url,title']))
 row=queue_row(meta['headRefOid'],a.problem_id);mainrow=queue_row('main',a.problem_id)
 eligible=meta['state']=='OPEN' and meta['isDraft'] and row['status']=='claimed_solved'
 if mainrow['status'] in ('preprint_published','merged'):eligible=False
 receipt={'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'metadata':meta,'row':row,'main_row':mainrow,'eligible':eligible}
 d=ROOT/'audits'/f'pr{a.pr}_{a.problem_id}';d.mkdir(parents=True,exist_ok=True)
 name='ELIGIBILITY.json' if a.snapshot and not (d/'ELIGIBILITY.json').exists() else 'ELIGIBILITY_LIVE.json'
 (d/name).write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt,indent=2))
 if not eligible:return
 if not a.snapshot:return
 if (d/'ORIGINAL_SNAPSHOT.json').exists():raise RuntimeError('Frozen snapshot already exists; no overwrite')
 full=json.loads(run(['gh','pr','view',str(a.pr),'--repo','AlecKriebel/Math','--json','number,title,body,state,isDraft,headRefOid,url,files']))
 if full['headRefOid']!=meta['headRefOid']:raise RuntimeError('Head changed before capture')
 (d/'PR_METADATA.json').write_text(json.dumps(full,indent=2)+'\n')
 run(['git','fetch','origin',f'refs/pull/{a.pr}/head'])
 if run(['git','rev-parse','FETCH_HEAD']).strip()!=meta['headRefOid']:raise RuntimeError('Head changed during fetch')
 captured=[]
 for file in full['files']:
  name=file['path']
  if not name.startswith(f'unsolved_math_prioritization/attempts/{a.problem_id}/'):continue
  dest=d/'original'/name;dest.parent.mkdir(parents=True,exist_ok=True)
  data=subprocess.run(['git','show',f"{meta['headRefOid']}:{name}"],cwd=REPO,capture_output=True,check=True).stdout
  dest.write_bytes(data);captured.append({'path':name,'sha256':hashlib.sha256(data).hexdigest(),'size':len(data)})
 (d/'ORIGINAL_SNAPSHOT.json').write_text(json.dumps({'head':meta['headRefOid'],'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':captured},indent=2)+'\n')
 print(f'Captured {len(captured)} authored files')
if __name__=='__main__':main()
