"""Actual isolated replay and primary-source retrieval for PR124; originals never executed in place."""
from pathlib import Path
import subprocess,hashlib,json,datetime,os,shutil,urllib.request
A=Path(__file__).resolve().parent
O=A/'original_head_authentication_20261006/original_attempt'
D=A/'root_reproduction_20261006'
S=A/'root_primary_sources_20261006'
PY='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def req(b,label):
 if not b:raise RuntimeError(label)
D.mkdir(exist_ok=True);S.mkdir(exist_ok=True)
(S/'.gitignore').write_text('private_sources/\n')
priv=S/'private_sources';priv.mkdir(exist_ok=True)
req(not (D/'RECEIPT.json').exists(),'Replay already complete; do not rerun blindly')
originals={str(f.relative_to(O)):sha(f.read_bytes()) for f in O.rglob('*') if f.is_file()}
env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
runs=[]
for name,relative,result in [('author','verify.py','verification.json'),('independent','independent_review/independent_checks.py','independent_review/independent_results.json')]:
 for optimized in [False,True]:
  tag=name+('_optimized' if optimized else '_normal')
  wd=D/tag
  shutil.copytree(O,wd)
  args=[PY,'-E','-S','-B','-P']+(['-O'] if optimized else [])+[str(wd/relative)]
  child=subprocess.Popen(args,cwd=wd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  out,err=child.communicate()
  (D/(tag+'.stdout.txt')).write_bytes(out);(D/(tag+'.stderr.txt')).write_bytes(err)
  entry={'tag':tag,'PID':child.pid,'argv':args,'UTC':now(),'exit_code':child.returncode,'stdout_sha256':sha(out),'stderr_sha256':sha(err),'result':json.loads((wd/result).read_text())}
  events.append(entry);dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events})
  req(child.returncode==0,'Failed '+tag)
  expected=(O/result).read_bytes()
  entry['output_reproduces_original_bytes']=expected==(wd/result).read_bytes()
  if not optimized:req(entry['output_reproduces_original_bytes'],'Normal output mismatch '+tag)
  runs.append(entry)
source_manifest=json.loads((O/'source_manifest.json').read_text())
sources=[]
for n,item in enumerate(source_manifest['sources']):
 name=['ohtsuki_collection','alcaraz_v1','massuyeau_preprint'][n]
 url=item['url']
 request=urllib.request.Request(url,headers={'User-Agent':'Independent-Math-Audit/1.0'})
 started=now()
 with urllib.request.urlopen(request,timeout=45) as r:
  body=r.read();final=r.url;ctype=r.headers.get('Content-Type')
 req(body.startswith(b'%PDF'),'Not PDF '+url)
 path=priv/(name+'.pdf');path.write_bytes(body)
 textpath=priv/(name+'.txt')
 args=['/opt/homebrew/bin/pdftotext','-layout',str(path),str(textpath)]
 child=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate()
 req(child.returncode==0,'PDF extraction '+name)
 entry={'name':name,'URL':url,'final_URL':final,'requested_UTC':started,'downloaded_UTC':now(),'bytes':len(body),'sha256':sha(body),'declared_original_sha256':item['sha256'],'matches_original_source_hash':sha(body)==item['sha256'],'content_type':ctype,'text_bytes':textpath.stat().st_size,'text_sha256':sha(textpath.read_bytes()),'text_extractor_PID':child.pid,'text_extractor_exit_code':child.returncode,'stderr_sha256':sha(err)}
 sources.append(entry);dump(S/'SOURCES.json',{'UTC':now(),'actual_operator_PID':os.getpid(),'sources':sources})
req(originals=={str(f.relative_to(O)):sha(f.read_bytes()) for f in O.rglob('*') if f.is_file()},'Originals mutated')
receipt={'UTC':now(),'actual_operator_PID':os.getpid(),'runs':runs,'source_acquisitions':sources,'original_files_unchanged':True,'math_proved_by_computation':False,'author_guard_under_O_limitation':'Author ck uses assert and loses falsification under -O; counts alone do not supply optimized assurance. Independent checker uses explicit check and remains active.','new_central_proof_search_turns':0}
dump(D/'RECEIPT.json',receipt)
print(json.dumps({'UTC':receipt['UTC'],'PID':os.getpid(),'normal_runs_reproduced':2,'author_assertions':runs[0]['result']['exact_assertions'],'independent_assertions':runs[2]['result']['independent_assertions'],'sources':[{k:s[k] for k in ['name','bytes','sha256','matches_original_source_hash']} for s in sources],'original_files_unchanged':True}))

