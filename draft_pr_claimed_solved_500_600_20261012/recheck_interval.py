#!/usr/bin/env python3
"""Status identification only; no mathematics or mutations for excluded drafts."""
import argparse,datetime,json,subprocess
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
from capture_eligible_pr import queue_row,ROOT,REPO

def main():
 p=argparse.ArgumentParser();p.add_argument('start',type=int);p.add_argument('end',type=int);a=p.parse_args()
 if not 500<=a.start<=a.end<=600:raise ValueError('Outside authorized range')
 raw=subprocess.run(['gh','pr','list','--repo','AlecKriebel/Math','--state','open','--limit','1000','--json','number,isDraft,headRefOid,title,url'],cwd=REPO,capture_output=True,text=True,check=True).stdout
 prs=[p for p in json.loads(raw) if a.start<=p['number']<=a.end and p['isDraft']]
 def classify(pr):
  prior=json.loads((ROOT/'eligibility'/f"pr{pr['number']}.json").read_text());pid=int(prior['problem_id'])
  row=queue_row(pr['headRefOid'],pid)
  return {'number':pr['number'],'problem_id':pid,'head':pr['headRefOid'],'status':row['status'],'eligible':row['status']=='claimed_solved','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 results=[]
 with ThreadPoolExecutor(max_workers=4) as pool:
  for future in as_completed([pool.submit(classify,pr) for pr in prs]):results.append(future.result())
 results.sort(key=lambda x:x['number'])
 receipt={'interval':[a.start,a.end],'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status_only':True,'results':results,'eligible_prs':[r['number'] for r in results if r['eligible']]}
 dest=ROOT/'eligibility'/f"recheck_{a.start}_{a.end}_{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
 dest.write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps({'receipt':str(dest),'eligible_prs':receipt['eligible_prs'],'skipped_nonclaimed':len(results)-len(receipt['eligible_prs']),'observed_open_drafts':len(results)},indent=2))
if __name__=='__main__':main()
