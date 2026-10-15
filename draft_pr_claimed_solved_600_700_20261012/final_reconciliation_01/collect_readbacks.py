#!/usr/bin/env python3
"""Read-only readbacks of precisely seven already completed eligible PRs."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,hashlib,subprocess,urllib.request,urllib.error,traceback
import sys
sys.dont_write_bytecode=True
from scope_sheet_evidence import PRIVATE_KEYS,scoped_evidence
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent
NUMBERS=(615,618,623,628,630,662,672)
SHEET='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
def now():return datetime.now(timezone.utc).isoformat()
def dump(name,d):
 (OUT/name).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def api_cli(args):
 p=subprocess.run(args,capture_output=True,text=True,timeout=90)
 result={'checked_utc':now(),'command':args,'returncode':p.returncode}
 if p.returncode==0:
  try:result['response']=json.loads(p.stdout)
  except Exception:result['unparsed_stdout']=p.stdout
 else:result['stderr']=p.stderr;result['stdout']=p.stdout
 return result
def public_get(url,name,accept=None,binary=False):
 headers={'User-Agent':'Independent-Research-ReadOnly-Reconciliation/1.0'}
 if accept:headers['Accept']=accept
 req=urllib.request.Request(url,headers=headers,method='GET')
 try:
  with urllib.request.urlopen(req,timeout=60) as f:
   b=f.read(25_000_001)
   if len(b)>25_000_000:raise ValueError('Response exceeds readback size limit')
   receipt={'checked_utc':now(),'requested_url':url,'http_status':f.status,'resolved_url':f.url,'content_type':f.headers.get('Content-Type'),'bytes':len(b),'sha256':sha(b),'md5':hashlib.md5(b).hexdigest(),'only_read_request':True}
  if binary:(OUT/'tmp'/name).write_bytes(b);receipt['temporary_path']='tmp/'+name
  else:
   try:receipt['response']=json.loads(b)
   except Exception:
    (OUT/'tmp'/name).write_bytes(b);receipt['temporary_path']='tmp/'+name
  return receipt
 except Exception as e:return {'checked_utc':now(),'requested_url':url,'error_type':type(e).__name__,'error':str(e),'only_read_request':True}
def main():
 completed=load(OUT/'PROGRAM_COMPLETED_INPUT.json')['completed']
 expected=[]
 inputs={}
 def bind(p):
  d=load(p) if p.suffix=='.json' else p.read_text()
  inputs[str(p.relative_to(ROOT))]={'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
  return d
 for entry in completed:
  n=entry['pr'];a=next((ROOT/'audits').glob(f'pr{n}_*'))
  e=dict(entry,audit_directory=str(a.relative_to(ROOT)))
  if n==615:
   c=bind(a/'CLOSURE_RECEIPT.json');e['original_head']=e['accepted_head']=c['headRefOid']
   e['closure_body_file']=str((a/'CLOSURE_COMMENT_SENT.md').relative_to(ROOT));e['closure_body_sha256']=sha((a/'CLOSURE_COMMENT_SENT.md').read_bytes());bind(a/'CLOSURE_COMMENT_SENT.md')
   e['closed_at']=c['closedAt']
  elif n in (628,630):
   s=bind(a/'SCOPE_AND_SNAPSHOT.json');c=bind(a/'CLOSURE_RECEIPT.json')
   e['original_head']=e['accepted_head']=s['original_head'];e['closed_at']=c['pr']['closedAt'];e['closure_body_sha256']=c['comment']['body_sha256']
   e['closure_body_file']=str((a/'CLOSURE_COMMENT_CANDIDATE.md').relative_to(ROOT));bind(a/'CLOSURE_COMMENT_CANDIDATE.md')
  elif n==672:
   s=bind(a/'SCOPE_AND_SNAPSHOT.json');c=bind(a/'FINAL_DISPOSITION.json');bind(a/'CLOSE_RECEIPT.json');bind(a/'CLOSURE_COMMENT_RECEIPT.json')
   e['original_head']=e['accepted_head']=s['original_head'];e['closed_at']=c['closed_at'];e['closure_body_sha256']=c['body_sha256']
   e['closure_body_file']=str((a/'CLOSURE_COMMENT.md').relative_to(ROOT));bind(a/'CLOSURE_COMMENT.md')
  elif n==618:
   c=bind(a/'MERGE_RECEIPT.json');i=bind(a/'INTEGRATION_RECEIPT.json');g=bind(a/'FINAL_PUBLICATION_GATE.json')
   e['original_head']=i['existing_pr_head'];e['accepted_head']=c['headRefOid'];e['merged_at']=c['mergedAt'];e['original_head_gate_agrees']=g['live_pr_gate']['headRefOid']==e['original_head']
  elif n==623:
   s=bind(a/'LIVE_SCOPE_GATE.json');c=bind(a/'MERGE_RECEIPT.json');i=bind(a/'INTEGRATION_PUSHED_RECEIPT.json');bind(a/'FINAL_PUBLICATION_GATE.json')
   e['original_head']=s['head'];e['accepted_head']=c['accepted_head'];e['merged_at']=c['merged_at'];e['accepted_head_receipts_agree']=i['integration_commit']==e['accepted_head']
  elif n==662:
   s=bind(a/'SCOPE_AND_SNAPSHOT.json');c=bind(a/'FINAL_DISPOSITION.json');bind(a/'GH_MERGE_RECEIPT.json');bind(a/'ACCEPTED_PUBLICATION_INPUTS.json');bind(a/'FINAL_PUBLICATION_GATE.json')
   e['original_head']=s['original_head'];e['accepted_head']=c['accepted_head'];e['merged_at']=c['merged_utc']
  if 'doi' in e:
   z=bind(a/'ZENODO_PUBLICATION_RECEIPT.json');t=bind(a/'TRACKER_RECEIPT.json');meta=bind(a/'publication/zenodo-deposit.json')
   e['publication_receipt']=z;e['metadata']=meta;e['tracker_row']=t['row'];e['tracker_range']=t['updated_range']
   for f in z['files']:
    p=a/'publication'/f['name'];inputs[str(p.relative_to(ROOT))]={'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'md5':hashlib.md5(p.read_bytes()).hexdigest()}
  expected.append(e)
 dump('EXPECTED_COMPLETED_SEVEN.json',{'created_utc':now(),'entries':expected})
 dump('INPUT_BINDINGS.json',{'created_utc':now(),'files':inputs})
 tasks={}
 for e in expected:
  n=e['pr']
  tasks[f'pr{n}_github']=lambda n=n:api_cli(['gh','pr','view',str(n),'--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,mergeCommit,mergedAt,closedAt,url'])
  for role in ('original_head','accepted_head'):
   if role=='accepted_head' and e[role]==e['original_head']:continue
   h=e[role]
   tasks[f'pr{n}_{role}_commit']=lambda h=h:api_cli(['gh','api',f'repos/AlecKriebel/Math/commits/{h}'])
  if 'comment_url' in e:
   c=e['comment_url'].split('issuecomment-')[1]
   tasks[f'pr{n}_closure_comment']=lambda c=c:api_cli(['gh','api',f'repos/AlecKriebel/Math/issues/comments/{c}'])
  if 'doi' in e:
   rid=e['doi'].split('.')[-1]
   tasks[f'pr{n}_zenodo_native']=lambda rid=rid,n=n:public_get(f'https://zenodo.org/api/records/{rid}',f'pr{n}_record.bin','application/vnd.inveniordm.v1+json')
   tasks[f'pr{n}_doi_resolution']=lambda doi=e['doi'],n=n:public_get(f'https://doi.org/{doi}',f'pr{n}_doi.html')
   tasks[f'pr{n}_merge_commit']=lambda h=e['merge_commit']:api_cli(['gh','api',f'repos/AlecKriebel/Math/commits/{h}'])
   tasks[f'pr{n}_tracker_exact']=lambda rg=e['tracker_range']:api_cli(['gws','sheets','spreadsheets','values','get','--params',json.dumps({'spreadsheetId':SHEET,'range':rg})])
   for f in e['publication_receipt']['files']:
    tasks[f'pr{n}_public_{f["name"]}']=lambda n=n,rid=rid,f=f:public_get(f'https://zenodo.org/api/records/{rid}/files/{f["name"]}/content',f'pr{n}_{f["name"]}',binary=True)
 tasks['tracker_metadata']=lambda:api_cli(['gws','sheets','spreadsheets','get','--params',json.dumps({'spreadsheetId':SHEET,'fields':'spreadsheetId,sheets.properties'})])
 tasks['tracker_all_A_D']=lambda:api_cli(['gws','sheets','spreadsheets','values','get','--params',json.dumps({'spreadsheetId':SHEET,'range':"'Math Puzzles'!A:D"})])
 results={}
 with ThreadPoolExecutor(max_workers=5) as pool:
  futures={pool.submit(fn):k for k,fn in tasks.items()}
  for f in as_completed(futures):
   key=futures[f]
   try:result=f.result()
   except Exception as exc:result={'error_type':type(exc).__name__,'error':str(exc),'checked_utc':now()}
   results[key]=result
   if key in PRIVATE_KEYS:
    dump('tmp/'+key+'.json',result)
    private_bytes=(OUT/'tmp'/(key+'.json')).read_bytes()
    dump(key+'.json',scoped_evidence(key,result,private_bytes,expected))
   else:dump(key+'.json',result)
 private_pins={}
 for key in PRIVATE_KEYS:
  private_path=OUT/'tmp'/(key+'.json')
  if private_path.exists():
   b=private_path.read_bytes();private_pins['tmp/'+key+'.json']={'bytes':len(b),'sha256':sha(b),'excluded_from_publication':True}
 input_document=load(OUT/'INPUT_BINDINGS.json');input_document['private_readbacks']=private_pins;dump('INPUT_BINDINGS.json',input_document)
 dump('COLLECTION_SUMMARY.json',{'completed_utc':now(),'readback_count':len(results),'keys':sorted(results),'only_external_read_operations':True,'allowed_prs':list(NUMBERS),'failed_keys':[k for k,v in results.items() if 'error' in v or v.get('returncode',0)!=0]})
 print(json.dumps({'readbacks':len(results),'failed':[k for k,v in results.items() if 'error' in v or v.get('returncode',0)!=0]},indent=2))
if __name__=='__main__':main()
