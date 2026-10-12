#!/usr/bin/env python3
"""Read-only input authentication and unmodified isolated replay."""
import base64, concurrent.futures, datetime, hashlib, json, os, pathlib, shutil, subprocess, sys, time

ROOT=pathlib.Path(__file__).resolve().parent
PARENT=ROOT.parent
INTAKE=json.loads((PARENT/'INTAKE.json').read_text())
SOURCE=PARENT/'submitted/unsolved_math_prioritization/attempts/5100026'
sha=lambda b:hashlib.sha256(b).hexdigest()
blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
checks=[]
for f in INTAKE['files']:
 b=pathlib.Path(f['local_path']).read_bytes()
 checks.append({'path':f['repository_path'],'bytes':len(b),'sha256':sha(b),'git_blob_oid':blob(b),'matched':len(b)==f['bytes'] and sha(b)==f['sha256'] and blob(b)==f['git_blob_oid']})
manifests=[]
for name,base in [('FROZEN_MANIFEST.json',SOURCE),('PUBLICATION_MANIFEST.json',SOURCE),('REVIEW_MANIFEST.json',SOURCE/'independent_review')]:
 m=json.loads((base/name).read_text()); items=[]
 for path,pin in m['files'].items():
  b=(base/path).read_bytes(); expected=pin if isinstance(pin,str) else pin['sha256']
  items.append({'path':path,'sha256':sha(b),'bytes':len(b),'matched':sha(b)==expected and (isinstance(pin,str) or len(b)==pin['bytes'])})
 extras={}
 for field,path in [('reviewed_proof_sha256',SOURCE/'PROOF.md'),('reviewed_author_manifest_sha256',SOURCE/'FROZEN_MANIFEST.json')]:
  if field in m:extras[field]={'expected':m[field],'actual':sha(path.read_bytes()),'matched':m[field]==sha(path.read_bytes())}
 manifests.append({'manifest':str(base/name),'sha256':sha((base/name).read_bytes()),'pins':items,'extra_pins':extras})
receipt=json.loads((SOURCE/'independent_review/HASH_AND_REPLAY_RECEIPT.json').read_text())
body=[]
body.append({'path':'FROZEN_MANIFEST.json','expected':receipt['manifest_sha256'],'matched':receipt['manifest_sha256']==sha((SOURCE/'FROZEN_MANIFEST.json').read_bytes())})
for pin in receipt['files']:
 b=(SOURCE/pin['path']).read_bytes();body.append({'path':pin['path'],'sha256':sha(b),'matched':sha(b)==pin['sha256']})
captures=[]
for f in (PARENT/'intake_GET_captures').glob('BLOB_*.stdout.json'):
 o=json.loads(f.read_text()); b=base64.b64decode(o['content']);matches=[p for p in INTAKE['files'] if p['git_blob_oid']==o['sha']]
 captures.append({'capture':f.name,'returned_sha':o['sha'],'recomputed_blob_sha':blob(b),'returned_size':o['size'],'bytes':len(b),'source_file_matches':[x['repository_path'] for x in matches],'matched':blob(b)==o['sha'] and len(b)==o['size'] and len(matches)==1 and b==pathlib.Path(matches[0]['local_path']).read_bytes()})
request_pins=[]
for req in INTAKE['requests']:
 for suffix in ('stdout','stderr'):
  pin=req[suffix]
  candidates=list((PARENT/'intake_GET_captures').glob('*.'+suffix+('*' if suffix=='stdout' else '')))
  matches=[p.name for p in candidates if len(p.read_bytes())==pin['bytes'] and sha(p.read_bytes())==pin['sha256']]
  request_pins.append({'endpoint':req['endpoint'],'stream':suffix,'expected_sha256':pin['sha256'],'matching_capture_filenames':matches,'matched':bool(matches)})
write('AUTHENTICATION.json',{'UTC':utc(),'input_checks':checks,'manifests':manifests,'historical_receipt_body_pins':body,'decoded_blob_captures':captures,'request_body_pins':request_pins,'all_matched':all(x['matched'] for x in checks+body+captures+request_pins) and all(p['matched'] for m in manifests for p in m['pins']) and all(p['matched'] for m in manifests for p in m['extra_pins'].values())})
lib=pathlib.Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr378_30004322/cover_duality_review/runtime_deps')
env=dict(os.environ);env['PYTHONPATH']=str(lib);env['PYTHONDONTWRITEBYTECODE']='1'
version=subprocess.run([sys.executable,'-c','import sys,sympy,mpmath,json;print(json.dumps({"python":sys.version,"executable":sys.executable,"sympy":sympy.__version__,"mpmath":mpmath.__version__,"sympy_path":sympy.__file__,"mpmath_path":mpmath.__file__}))'],env=env,capture_output=True)
write('RUNTIME.json',{'UTC':utc(),'version_stdout':version.stdout.decode(),'version_stderr':version.stderr.decode(),'exit_code':version.returncode,'library_path':str(lib),'uses_only_prior_libraries':True,'prior_audit_helper_imports':False,'initial_default_environment_failures':['Homebrew Python 3.14.6: ModuleNotFoundError sympy','Bundled Python 3.12.14: ModuleNotFoundError sympy']})
jobs=[('author_exact','verify_exact.py','exact_checks.json'),('author_numeric','verify_numeric.py','numeric_checks.json'),('review_exact','independent_review/independent_exact.py','independent_review/INDEPENDENT_EXACT.json'),('review_numeric','independent_review/independent_numeric.py','independent_review/INDEPENDENT_NUMERIC.json')]
def run(job):
 tag,script,expected=job; scratch=ROOT/'replays'/tag;scratch.mkdir(parents=True,exist_ok=True)
 target=scratch/pathlib.Path(script).name;shutil.copyfile(SOURCE/script,target)
 started=utc(); t=time.monotonic();p=subprocess.run([sys.executable,str(target)],cwd=scratch,env=env,capture_output=True)
 (scratch/'stdout.json').write_bytes(p.stdout);(scratch/'stderr.txt').write_bytes(p.stderr)
 original=(SOURCE/expected).read_bytes()
 result={'tag':tag,'script':script,'script_sha256':sha(target.read_bytes()),'command':[sys.executable,str(target)],'working_directory':str(scratch),'PYTHONPATH':str(lib),'startedUTC':started,'finishedUTC':utc(),'seconds':time.monotonic()-t,'exit_code':p.returncode,'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr),'frozen_receipt_path':expected,'frozen_receipt_sha256':sha(original),'byte_identical':p.stdout==original}
 try: result['semantic_json_equal']=json.loads(p.stdout)==json.loads(original)
 except Exception as e:result['JSON_comparison_error']=str(e)
 (scratch/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=list(pool.map(run,jobs))
write('REPLAY_RECEIPTS.json',{'UTC':utc(),'replays':results,'all_exit_zero':all(r['exit_code']==0 for r in results),'all_byte_identical':all(r['byte_identical'] for r in results)})
print(json.dumps({'authentication':'AUTHENTICATION.json','replays':results},indent=2))
