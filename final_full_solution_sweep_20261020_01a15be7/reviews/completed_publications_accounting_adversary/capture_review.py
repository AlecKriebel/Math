#!/usr/bin/env python3
from pathlib import Path
import concurrent.futures, datetime as dt, hashlib, json, os, subprocess, urllib.request, urllib.error
B=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7')
R=B/'reviews/completed_publications_accounting_adversary'
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,data):
 p=R/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data if isinstance(data,bytes) else data.encode());return str(p.relative_to(R))
def jput(p,d):return put(p,json.dumps(d,indent=2,ensure_ascii=False)+'\n')
inputs=[]
def cp(p):
 p=B/p;b=p.read_bytes();q=Path('inputs/effort')/p.relative_to(B);put(q,b);inputs.append({'source':str(p),'captured_path':str(q),'captured_at':now(),'bytes':len(b),'sha256':sha(b)})
fixed=['STATE.json','rest_inventory.json','dispositions.jsonl','coverage_snapshot.py','PR0292_PUBLICATION_VERIFICATION.json','PR0397_PUBLICATION_VERIFICATION.json','PR0399_PUBLICATION_VERIFICATION.json','PR0280_REOPENED_PUBLICATION_VERIFICATION.json','PR0280_REOPENED_DISPOSITION.json']
for p in fixed:cp(Path(p))
for p in sorted(B.glob('PR*_DISPOSITION.json')):cp(p.relative_to(B))
receipts=[]
for n in ['PR0292_PUBLICATION_VERIFICATION.json','PR0397_PUBLICATION_VERIFICATION.json','PR0399_PUBLICATION_VERIFICATION.json','PR0280_REOPENED_PUBLICATION_VERIFICATION.json']:
 d=json.loads((R/'inputs/effort'/n).read_text());receipts.append(d)
 for e in d['evidence'].values():
  p=Path(e)
  if not p.is_absolute() and (B/p).is_file():cp(p)
 for p in (B/Path(d['evidence']['publication']).parent).glob('*METADATA*.json'):cp(p.relative_to(B))
jput('INPUT_MANIFEST.json',{'captured_at':now(),'files':inputs,'note':'Exact bytes captured individually; current canonical files may legitimately advance after read. No blanket unchanged assertion.'})
jput('RESEARCH_LOG.json',[{'at':now(),'completion_estimate_percent':15,'event':'Root receipts, dispositions, state, journal, inventory, coverage implementation and direct evidence captured; beginning independent public and live ledger checks.'},{'at':now(),'completion_estimate_percent':15,'event':'Workflow incident recorded separately in INCIDENT.json; no cleanup attempted.'}])
jput('INCIDENT.json',{'command':'gws generate-skills --help && gws schema sheets.spreadsheets.get && gws schema sheets.spreadsheets.values.get','cwd':'/Users/alec/Documents/Math','time_bound':'After 2026-10-21T16:57:36Z tool clock and before this capture; exact command start timestamp unavailable in tool response','recorded_at':now(),'unexpected_behavior':'generate-skills --help executed skill generation instead of help','stdout_paths':['docs/skills.md','skills/'],'stdout_services':['drive','sheets','gmail','calendar','admin-reports','docs','slides','tasks','people','chat','classroom','forms','keep','meet','events','modelarmor','workflow','script','10 personas','41 recipes'],'pre_command_bytes_or_baseline':None,'whether_originals_overwritten':'Unknown: no pre-command byte baseline was captured; cannot infer generated-only versus overlap. Parent notified; no deletion or revert attempted.','other_effects':'No authentication changes, Git mutation or GWS API write was invoked. Subsequent calls limited to values get.'})
# Full formatted-value ledger snapshot through the mandated CLI.
params={'spreadsheetId':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','range':"'Math Puzzles'!A:AQ",'valueRenderOption':'FORMATTED_VALUE'}
args=['gws','sheets','spreadsheets','values','get','--params',json.dumps(params)]
start=now();p=subprocess.run(args,capture_output=True,cwd=R)
put('live/gws_fullsheet.stdout.json',p.stdout);put('live/gws_fullsheet.stderr.txt',p.stderr)
jput('live/gws_request.json',{'at':start,'completed_at':now(),'argv':args,'cwd':str(R),'returncode':p.returncode,'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)})
# Public captures use no account tokens or credentials.
def fetch(url,rel):
 start=now();req=urllib.request.Request(url,headers={'User-Agent':'IndependentPublicationAccountingReview/1.0','Accept':'application/json,text/html,application/octet-stream;q=0.9'})
 try:
  with urllib.request.urlopen(req,timeout=45) as response:
   data=response.read();status=response.status;dest=response.url;headers=dict(response.headers)
 except urllib.error.HTTPError as e:
  data=e.read();status=e.code;dest=e.url;headers=dict(e.headers)
 except Exception as e:
  result={'requested_url':url,'requested_at':start,'completed_at':now(),'error':repr(e)};jput(rel+'.receipt.json',result);return result
 put(rel,data);result={'requested_url':url,'requested_at':start,'completed_at':now(),'status':status,'resolved_url':dest,'headers':headers,'bytes':len(data),'sha256':sha(data),'md5':hashlib.md5(data).hexdigest(),'body':rel};jput(rel+'.receipt.json',result);return result
jobs=[]
for d in receipts:
 record=d['record'];prefix=f'live/zenodo_{record}'
 jobs.extend([(f'https://zenodo.org/api/records/{record}',prefix+'/record.json'),(d['doi_url'],prefix+'/doi_landing.html')])
 for f in d['files']:
  jobs.append((f'https://zenodo.org/records/{record}/files/{f["name"]}?download=1',prefix+'/'+f['name']))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=list(pool.map(lambda args:fetch(*args),jobs))
jput('live/HTTPS_CAPTURE_SUMMARY.json',{'completed_at':now(),'captures':results})
print(json.dumps({'captured_inputs':len(inputs),'gws_returncode':p.returncode,'gws_bytes':len(p.stdout),'captures':[{'url':x['requested_url'],'status':x.get('status'),'bytes':x.get('bytes'),'error':x.get('error')} for x in results]},indent=2))
