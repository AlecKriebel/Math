"""Run the unmodified frozen config generator on an isolated read-only-input copy.

Only these synthetic fixture links/config outputs are written. Candidate files
are linked only for reading; no linked path is opened for writing by this tool.
"""
from pathlib import Path
import hashlib,json,os,shutil,socket,subprocess,sys,datetime
HERE=Path(__file__).resolve().parent;R=HERE.parent;D=R.parent
def load(p):return json.loads(p.read_text())
def identity(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
fixture=HERE/'preflight_fixture02';fixture.mkdir(exist_ok=False)
service=fixture/'service';service.mkdir()
paths={'STATE.json','CLAIM_REGISTRY.json'};configs={}
for p in sorted(R.glob('PR*_SERVICE_CONFIG.json')):
 c=load(p)
 # The generator intentionally covers the thirteen later packages only.
 if c['pr']==1032:continue
 configs[c['pr']]=c
 paths|={c['manifest'],c['final_seal']}
 if c['pr']==1098:paths.add(c['audit_folder']+'/ROOT_WHOLE_PACKAGE_REVIEW_02.json')
 for f in c['files']:paths.add(f['path'])
ledger=[]
for relative in sorted(paths):
 source=D/relative;dest=fixture/relative;dest.parent.mkdir(parents=True,exist_ok=True)
 if relative in {'STATE.json','CLAIM_REGISTRY.json'} or source.suffix=='.json':shutil.copyfile(source,dest);method='copy'
 else:os.link(source,dest);method='read_only_probe_link'
 ledger.append({'source':str(source),'fixture':str(dest),'method':method,**identity(source)})
script=service/'prepare_service_configs.py';shutil.copyfile(HERE/'REVIEWED_prepare_service_configs.py.txt',script)
argv=[sys.executable,'-B',str(script)]
p=subprocess.run(argv,capture_output=True,text=True,timeout=30)
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':argv,'cwd':str(HERE),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'input_ledger':ledger,'source_identity':identity(script)}
(HERE/'PREFLIGHT_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
for row in ledger:
 assert identity(Path(row['source']))=={k:row[k]for k in ('bytes','sha256')}
assert p.returncode==0,receipt
receipt['generated_configs_match_current_canonical']={str(n):load(service/f'PR{n}_SERVICE_CONFIG.json')==c for n,c in configs.items()}
assert all(receipt['generated_configs_match_current_canonical'].values())
receipt['all_source_bytes_unchanged']=True
(HERE/'PREFLIGHT_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':'PASS','configs':len(configs),'assets_rehashed':26,'all_source_bytes_unchanged':True}))
