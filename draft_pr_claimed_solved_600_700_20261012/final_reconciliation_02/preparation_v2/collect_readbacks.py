#!/usr/bin/env python3
"""Read-only readbacks of exactly eight eligible PRs after all final outcomes exist."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,hashlib,subprocess,urllib.request,urllib.error,traceback,argparse
import sys
sys.dont_write_bytecode=True
from scope_sheet_evidence import PRIVATE_KEYS,scoped_evidence
from expected_state import build_expected,NotReady
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent
NUMBERS=(615,618,623,628,630,662,672,681)
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
def collect(snapshot):
 require_no_previous_snapshot=not (OUT/'COLLECTION_SUMMARY.json').exists() and not (OUT/'EXPECTED_COMPLETED_EIGHT.json').exists()
 if not require_no_previous_snapshot:raise NotReady('A snapshot already exists here; do not overwrite final evidence. Use a new dedicated folder for a new collection.')
 expected=snapshot['entries']
 if sha((ROOT/'PROGRAM_STATE.json').read_bytes())!=snapshot['program_state_sha256']:
  raise NotReady('Program state changed after preflight; no external request dispatched')
 (OUT/'tmp').mkdir(exist_ok=True)
 dump('PROGRAM_COMPLETED_INPUT.json',snapshot['program_completed_snapshot'])
 dump('EXPECTED_COMPLETED_EIGHT.json',{'created_utc':snapshot['created_utc'],'program_state_sha256':snapshot['program_state_sha256'],'entries':expected})
 for source in sorted(OUT.glob('*.py')):
  data=source.read_bytes();snapshot['input_bindings']['files'][str(source.relative_to(ROOT))]={'bytes':len(data),'sha256':sha(data)}
 dump('INPUT_BINDINGS.json',snapshot['input_bindings'])
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
  for future in as_completed(futures):
   key=futures[future]
   try:result=future.result()
   except Exception as exc:result={'error_type':type(exc).__name__,'error':str(exc),'checked_utc':now()}
   results[key]=result
   if key in PRIVATE_KEYS:
    dump('tmp/'+key+'.json',result)
    private_bytes=(OUT/'tmp'/(key+'.json')).read_bytes()
    dump(key+'.json',scoped_evidence(key,result,private_bytes,expected))
   else:dump(key+'.json',result)
   if len(results)%10==0:print(json.dumps({'readbacks_completed':len(results),'readbacks_total':len(tasks)}),flush=True)
 private_pins={}
 for key in PRIVATE_KEYS:
  private_path=OUT/'tmp'/(key+'.json')
  if private_path.exists():
   b=private_path.read_bytes();private_pins['tmp/'+key+'.json']={'bytes':len(b),'sha256':sha(b),'excluded_from_publication':True}
 input_document=load(OUT/'INPUT_BINDINGS.json');input_document['private_readbacks']=private_pins;dump('INPUT_BINDINGS.json',input_document)
 summary={'completed_utc':now(),'readback_count':len(results),'keys':sorted(results),'only_external_read_operations':True,'allowed_prs':list(NUMBERS),'failed_keys':[k for k,v in results.items() if 'error' in v or v.get('returncode',0)!=0]}
 dump('COLLECTION_SUMMARY.json',summary)
 print(json.dumps({'readbacks':len(results),'failed':summary['failed_keys']},indent=2))
 return 0 if not summary['failed_keys'] else 1
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 group=parser.add_mutually_exclusive_group(required=True)
 group.add_argument('--preflight',action='store_true',help='Offline readiness check only; never starts any external operation')
 group.add_argument('--collect',action='store_true',help='Run external readbacks only after explicit later authorization and all eight complete receipts')
 args=parser.parse_args()
 try:snapshot=build_expected(ROOT)
 except (NotReady,KeyError,ValueError,FileNotFoundError) as exc:
  print(json.dumps({'checked_utc':now(),'status':'NOT_READY','reason':str(exc),'external_requests_dispatched':0},indent=2));return 2
 if args.preflight:
  print(json.dumps({'checked_utc':now(),'status':'READY_OFFLINE','completed_prs':list(NUMBERS),'publication_count':len([x for x in snapshot['entries'] if 'doi' in x]),'input_files_bound':len(snapshot['input_bindings']['files']),'external_requests_dispatched':0},indent=2));return 0
 try:return collect(snapshot)
 except NotReady as exc:
  print(json.dumps({'checked_utc':now(),'status':'NOT_READY','reason':str(exc),'external_requests_dispatched':0},indent=2));return 2
if __name__=='__main__':raise SystemExit(main())
