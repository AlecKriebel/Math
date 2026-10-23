from pathlib import Path
import subprocess,hashlib,json,base64,datetime,os,gzip
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7');A=R/'audits'
D=A/'root_final_actual_inventory_and_numeric43_01'
GH=Path('/opt/homebrew/Cellar/gh/2.85.0/bin/gh')
GWS=Path('/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/@googleworkspace/cli/bin/gws')
BOOK='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20';GID=1254632077
H=lambda b:hashlib.sha256(b).hexdigest()
can=lambda v:json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def native_run(argv,timeout):
 from types import SimpleNamespace
 try:
  r=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
  return SimpleNamespace(returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,transport_error=None)
 except subprocess.TimeoutExpired as exc:
  return SimpleNamespace(returncode=None,stdout=exc.stdout or b'',stderr=exc.stderr or b'',transport_error={'type':'TimeoutExpired','timeout':exc.timeout,'read_only':True})
 except BaseException as exc:
  return SimpleNamespace(returncode=None,stdout=b'',stderr=b'',transport_error={'type':type(exc).__name__,'message':str(exc),'read_only':True})
assert H(GH.read_bytes())=='91f6e182bce24da56581ab999088c55ae0216309af19bc6167bbc4396c3f4ea5'
assert H(GWS.read_bytes())=='0f27b8b0815bf09cdf95da48d3c604f05ceb8f16bf5c9f0ba355b1f957cdd47e'
# ACTUAL completed outcomes are required; no prospective endpoint assumption.
pub=json.loads((R/'PR1131_PUBLICATION_VERIFICATION.json').read_bytes())
existing=json.loads((R/'EXISTING_PUBLICATION_REMAINING34_RECONCILIATION.json').read_bytes())
assert pub['pr']==1131 and pub['complete']is True and existing['complete']is True and existing['new_publications']==0
D.mkdir(mode=0o700,exist_ok=False)
def save(name,v):
 b=gzip.compress(json.dumps(v,sort_keys=True,ensure_ascii=False,indent=2).encode()+b'\n',mtime=0)
 used=sum(p.lstat().st_blocks*512 for p in [D,*D.rglob('*')])
 assert used+len(b)<=16*1024**2 and os.statvfs(D).f_bavail*os.statvfs(D).f_frsize-len(b)>=125829120
 p=D/name
 with p.open('xb')as f:f.write(b);f.flush();os.fsync(f.fileno())
 return {'path':str(p),'bytes':len(b),'sha256':H(b)}
save('INTENT.json.gz',{'at':now(),'read_only':True,'actual_outcome_pr1131':H((R/'PR1131_PUBLICATION_VERIFICATION.json').read_bytes()),'actual_outcome34':H((R/'EXISTING_PUBLICATION_REMAINING34_RECONCILIATION.json').read_bytes()),'gh_binary_sha256':H(GH.read_bytes()),'gws_binary_sha256':H(GWS.read_bytes()),'native_effects':0,'resource_cap':16*1024**2,'reserve':125829120})
def request(url,name):
 argv=[str(GH),'api','--method','GET','--include',url];at=now();r=native_run(argv,120);end=now()
 original={'argv':argv,'before':at,'after':end,'returncode':r.returncode,'transport_error':r.transport_error,'stdout_base64':base64.b64encode(r.stdout).decode(),'stderr_base64':base64.b64encode(r.stderr).decode(),'binary_sha256':H(GH.read_bytes())}
 native=save(name+'_ORIGINAL_NATIVE.json.gz',original)
 assert r.returncode==0 and r.transport_error is None,r.stderr
 sep=b'\r\n\r\n'if b'\r\n\r\n'in r.stdout else b'\n\n';head,body=r.stdout.split(sep,1);status=int(head.splitlines()[0].split()[1])
 envelope={'method':'GET','url':url,'at':at,'completed_at':end,'status':status,'raw_headers_base64':base64.b64encode(head+sep).decode(),'raw_body_base64':base64.b64encode(body).decode(),'raw_body_sha256':H(body),'original_cli':original,'original_native_pin':native}
 pin=save(name+'_COMPLETE_GET_ENVELOPE.json.gz',envelope)
 assert status==200,(status,pin)
 return pin,json.loads(body)
pages=[];nodes={};i=1
while True:
 url='https://api.github.com/repos/AlecKriebel/Math/pulls?state=all&sort=created&direction=asc&per_page=100&page='+str(i)
 pin,values=request(url,'INVENTORY_PAGE_%04d'%i);pages.append(pin)
 assert type(values)is list and len(values)<=100
 if not values:break
 for v in values:
  n=v['number'];assert type(n)is int and n>0 and n not in nodes
  nodes[n]=v
 i+=1
newest,values=request('https://api.github.com/repos/AlecKriebel/Math/pulls?state=all&sort=created&direction=desc&per_page=1','INVENTORY_NEWEST')
assert type(values)is list and len(values)==1 and values[0]['number']==max(nodes)
inventory={'pages':pages,'newest':newest,'observed_at':now(),'highest':max(nodes),'numeric_slots_from9':max(nodes)-8,'gaps_from9':[n for n in range(9,max(nodes)+1)if n not in nodes]}
save('COMPLETE_ACTUAL_FINAL_INVENTORY_DESCRIPTOR.json.gz',inventory)
# Load only the unchanged strict numeric/core module buffers via the caller-prehashed closed05 bootstrap.
E=A/'existing_publication_remaining34_preparation05';p=E/'source/bootstrap.py';b=p.read_bytes()
assert H(b)=='d69da788bded29032a17841dda615396ed3107b6fc4a93cc2c1e9452aa5ffe6b'
n={'__file__':str(p),'__name__':'_root_final_numeric_bootstrap'}
exec(compile(b,str(p),'exec',optimize=0),n);M,verify=n['load_verified']('9f45dc2caaa86c22e4804b8f529e5d7f6c52ea7b468353500b9c8877fa2269f4')
roles=['metadata_before','values','formulas','metadata_after'];originals={}
class Reader:
 def gws(self,args,params,body=None):
  role=roles[len(originals)]
  assert args==['get']or args==['values','batchGetByDataFilter']
  assert params['spreadsheetId']==BOOK
  argv=[str(GWS),'sheets','spreadsheets',*args,'--params',json.dumps(params)]
  if body is not None:argv+=['--json',json.dumps(body,ensure_ascii=False)]
  before=now();r=native_run(argv,120);after=now()
  native={'argv':argv,'before':before,'after':after,'returncode':r.returncode,'transport_error':r.transport_error,'stdout_base64':base64.b64encode(r.stdout).decode(),'stderr_base64':base64.b64encode(r.stderr).decode(),'binary_sha256':H(GWS.read_bytes()),'underlying_http_status':'not_observable_via_CLI_returncode'}
  originals[role]=save('NUMERIC43_'+role+'_ORIGINAL_NATIVE.json.gz',native)
  assert r.returncode==0 and r.transport_error is None,r.stderr
  return M['ops_core'].strict_json(r.stdout)
snapshot=M['numeric'].observe(Reader());verify()
assert set(originals)==set(roles)
ledger={'snapshot':save('COMPLETE_FINAL_NUMERIC43_SNAPSHOT.json.gz',snapshot),'observed_at':now(),'original_transports':originals}
out={'kind':'ROOT_ACTUAL_FINAL_NATIVE_COLLECTION_COMPLETE_NOT_COVERAGE_ADOPTION','at':now(),'final_inventory':inventory,'final_ledger':ledger,'actual_ledger_rows':len(snapshot['values']),'gh_binary_after_sha256':H(GH.read_bytes()),'gws_binary_after_sha256':H(GWS.read_bytes()),'actual_service_effects':0,'not_final_coverage':True}
pin=save('ROOT_COMPLETE_ACTUAL_FINAL_COLLECTION.json.gz',out)
print(json.dumps({'collection_pin':pin,'highest':max(nodes),'all_PR_objects':len(nodes),'slots_from9':max(nodes)-8,'gaps':inventory['gaps_from9'],'actual_ledger_rows':len(snapshot['values']),'actual_effects':0},sort_keys=True))

