#!/usr/bin/env python3
"""Independent operational audit of the revised package; only own cache writes."""
from pathlib import Path
import ast,hashlib,importlib.util,json,os,shutil,subprocess,sys,zipfile
R=Path(__file__).resolve().parent; A=R.parents[1]; C=R/'.cache'; C.mkdir(exist_ok=True)
E=C/'extracted/zero_filling_verification'; PUB=A/'publication'; REPO=A.parents[2]
PROFILE='(version 1) (allow default) (deny network*)'
def sha(b):return hashlib.sha256(b).hexdigest()
def run(cmd,cwd=None,deny=True):
 return subprocess.run((['/usr/bin/sandbox-exec','-p',PROFILE] if deny else [])+list(map(str,cmd)),cwd=cwd,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
def save(name,v):(R/name).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def cp(name,src=E):
 p=C/name;shutil.rmtree(p,ignore_errors=True);shutil.copytree(src,p);return p

def inventory(p):return {x.relative_to(p).as_posix():sha(x.read_bytes()) for x in p.rglob('*') if x.is_file()}
def rehash(p):
 f=p/'MANIFEST.json';m=json.loads(f.read_bytes());m['files']={n:{'bytes':x.stat().st_size,'sha256':sha(x.read_bytes())} for x in p.rglob('*') if x.is_file() and (n:=x.relative_to(p).as_posix())!='MANIFEST.json'};f.write_text(json.dumps(m,indent=2)+'\n')
res={}
# Permit an exact rerun without disturbing frozen extraction or source/PDF cache.
for transient in ('relocated', 'policy'):
 shutil.rmtree(C / transient, ignore_errors=True)
probe=run([sys.executable,'-c','import socket;socket.create_connection(("1.1.1.1",443),timeout=1)'])
assert probe.returncode and ('Operation not permitted' in probe.stderr or 'Permission denied' in probe.stderr)
res['network_denial_probe']={'returncode':probe.returncode,'stderr':probe.stderr}
pre=inventory(E)
snapshot=json.loads((E/'ORIGINAL_SNAPSHOT.json').read_bytes()); originals=[]
for item in snapshot['files']:
 data=(E/'original'/item['path']).read_bytes();g=run(['git','show',snapshot['head']+':'+item['path']],REPO,False)
 # git binary content is text in this exact authored inventory, compare without transcoding.
 raw=subprocess.run(['git','show',snapshot['head']+':'+item['path']],cwd=REPO,capture_output=True,check=True).stdout
 assert data==raw and sha(data)==item['sha256'] and len(data)==item['size']
 originals.append({'path':item['path'],'git_blob_matches':True,'sha256':sha(data)})
res['git_originals']=originals
# Independent verification of every outer and nested seal, with no package imports.
m=json.loads((E/'MANIFEST.json').read_bytes());assert set(pre)==set(m['files'])|{'MANIFEST.json'}
for n,v in m['files'].items():assert pre[n]==v['sha256'] and (E/n).stat().st_size==v['bytes']
entries=0
for seal in json.loads((E/'SEALS.json').read_bytes()):
 f=E/seal['path'];assert sha(f.read_bytes())==seal['sha256']
 if seal['kind']=='sha256sum':records=[(n,d,None) for d,n in [s.split('  ',1) for s in f.read_text().splitlines()]]
 else:records=[(v['path'],v['sha256'],v['bytes']) for v in json.loads(f.read_bytes())['files']]
 for n,d,z in records:
  b=(f.parent/n).read_bytes();assert sha(b)==d and (z is None or len(b)==z);entries+=1
assert entries==90
res['inventory']={'members':len(pre),'payloads':len(m['files']),'seals':len(m['nested_seals']),'nested_entries':entries}
# All seven actual jobs, in distinct disposable copies, independent complete comparisons.
jobs=[]
for i,j in enumerate(json.loads((E/'JOBS.json').read_bytes())):
 p=cp('job'+str(i));f=p/j['script'];r=run([sys.executable,'-B',f,*j.get('args',[])],f.parent)
 assert r.returncode==0,(j['script'],r.stderr)
 actual=json.loads((p/j['result_file']).read_bytes()) if 'result_file' in j else json.loads(r.stdout)
 expected=json.loads((E/j['record']).read_bytes());assert actual==expected,j['script']
 jobs.append({'script':j['script'],'status':'PASS','normalized_fields':[],'result_file_used':j.get('result_file'),'stdout_sha256':sha(r.stdout.encode()),'full_json':actual,'stderr':r.stderr})
 shutil.rmtree(p)
res['seven_actual_jobs']=jobs
r=run([sys.executable,'-B',E/'run_all.py'],E);assert r.returncode==0,r.stderr
res['actual_driver']={'stdout':r.stdout,'stderr':r.stderr,'returncode':r.returncode}
assert pre==inventory(E)
# Current tamper cases are actual driver invocations. Resealing outer bypasses the first boundary intentionally.
mutants=[]
origprefix='original/unsolved_math_prioritization/attempts/30004404/'
for mode in ['extra','outer_payload','nested_resealed_outer','original_resealed_outer','snapshot_resealed_outer','manifested_pdf','manifested_corpus','resealed_snapshot','changed_seal','symlink','optimized_flag','optimized_env']:
 p=cp('mutant'); before=inventory(p)
 if mode=='extra':(p/'surprise.txt').write_text('benign')
 elif mode=='outer_payload':(p/'README.md').write_text('changed')
 elif mode=='nested_resealed_outer':(p/'reviews/algebra01/REPORT.md').write_text('changed');rehash(p)
 elif mode=='original_resealed_outer':(p/origprefix/'verify_release.py').write_text('changed');rehash(p)
 elif mode=='snapshot_resealed_outer':(p/'ORIGINAL_SNAPSHOT.json').write_text('{}');rehash(p)
 elif mode in ['manifested_pdf','manifested_corpus']:
  f=p/origprefix/('source.pdf' if mode.endswith('pdf') else 'imported_corpus.txt');f.write_text('benign authored synthetic sentinel')
  mf=p/origprefix/'RELEASE_MANIFEST.json';v=json.loads(mf.read_bytes());v['files'].append({'path':f.name,'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())});mf.write_text(json.dumps(v,indent=2)+'\n');rehash(p)
 elif mode=='resealed_snapshot':
  f=p/origprefix/'verify_release.py';f.write_bytes(f.read_bytes()+b'\n# benign altered original\n');mf=p/'ORIGINAL_SNAPSHOT.json';v=json.loads(mf.read_bytes())
  for x in v['files']:
   if x['path'].endswith('/verify_release.py'):x.update(size=f.stat().st_size,sha256=sha(f.read_bytes()))
  mf.write_text(json.dumps(v,indent=2)+'\n');rehash(p)
 elif mode=='changed_seal':(p/'reviews/algebra01/SHA256SUMS').write_text('');rehash(p)
 elif mode=='symlink':f=p/'README.md';f.unlink();f.symlink_to(E/'README.md')
 cmd=[sys.executable,'-B']+(['-O'] if mode=='optimized_flag' else [])+[p/'run_all.py']
 if mode=='optimized_env':
  rr=subprocess.run(['/usr/bin/sandbox-exec','-p',PROFILE,*map(str,cmd)],capture_output=True,text=True,env=dict(os.environ,PYTHONOPTIMIZE='1',PYTHONDONTWRITEBYTECODE='1'))
 else:rr=run(cmd,p)
 assert rr.returncode!=0,mode
 mutants.append({'mode':mode,'rejected':True,'error':rr.stderr.strip().splitlines()[-1]})
res['current_driver_negative_controls']=mutants
# Real R1 acceptance under historical verifier, not merely validate(replay=False).
r1=[]
for name in ['source.pdf','imported_corpus.txt']:
 p=cp('old_r1',E/'original/unsolved_math_prioritization/attempts/30004404'); f=p/name;f.write_text('Benign synthetic audit sentinel, no third-party content.\n')
 mf=p/'RELEASE_MANIFEST.json';v=json.loads(mf.read_bytes());v['files'].append({'path':name,'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())});mf.write_text(json.dumps(v,indent=2)+'\n')
 rr=run([sys.executable,'-B',p/'verify_release.py','--self-test'],p);assert rr.returncode==0,rr.stderr;v=json.loads(rr.stdout);assert v['source_files_included'] is False and v['release_files_verified']==22
 r1.append({'name':name,'historical_accepts':True,'full_result':v})
res['historical_R1_reproduction']=r1
# Exact archive reproducibility after real relocation of complete audit.
# Only original snapshot, sealed families and explicitly selected roots are copied; live reviews excluded.
def audit_copy(p):
 p.mkdir(parents=True,exist_ok=True)
 for f in A.iterdir():
  if f.is_file() and f.name in ['ORIGINAL_SNAPSHOT.json','CURRENT_PRIORITY_ASSESSMENT.json','CURRENT_CORRECTIONS.md','ROOT_MATH_ACCEPTANCE.md','ROOT_SOURCE_RECEIPT.json','ROOT_SOURCE_INTAKE.json','ROOT_BODEN_FRIEDL_INTAKE.json','ROOT_JAN2026_SOURCE_INTAKE.json','PRIORITY01_ROOT_ACCEPTANCE.json','PRIORITY02_ROOT_ACCEPTANCE.json','verify_original_snapshot.py']:shutil.copy2(f,p/f.name)
 shutil.copytree(A/'publication',p/'publication',ignore=shutil.ignore_patterns('.cache'))
 shutil.copytree(A/'original',p/'original');shutil.copytree(A/'root_reproduction',p/'root_reproduction')
 for family in ['algebra01','topology01','priority01','priority02']:shutil.copytree(A/'reviews'/family,p/'reviews'/family,ignore=shutil.ignore_patterns('.cache'))
 return p
rel=[]
for label in ['ordinary','literal/.cache','literal/scratch']:
 p=audit_copy(C/'relocated'/label/'audit');orig=inventory(p/'original');rr=run([sys.executable,'-B',p/'publication/make_package.py'],p/'publication');assert rr.returncode==0,rr.stderr
 assert (p/'publication/verification_package.zip').read_bytes()==(PUB/'verification_package.zip').read_bytes();assert orig==inventory(p/'original')
 rel.append({'external_ancestors':label,'byte_identical_zip':True,'producer':json.loads(rr.stdout)})
res['relocated_producer_runs']=rel
p=C/'relocated/ordinary/audit'
for n in ['sources/fake.pdf','.cache/corpus.txt','scratch/local.txt','qa/page.png','.secrets/token.txt','extra.private.txt']:
 f=p/n;f.parent.mkdir(parents=True,exist_ok=True);f.write_text('benign unselected sentinel')
rr=run([sys.executable,'-B',p/'publication/make_package.py'],p/'publication');assert rr.returncode==0 and (p/'publication/verification_package.zip').read_bytes()==(PUB/'verification_package.zip').read_bytes()
res['actual_producer_unselected_sentinels_excluded']=True
# Extract the exact local add function AST without changing its body; policy controls use a synthetic audit.
src=(PUB/'make_package.py').read_text();tree=ast.parse(src);main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');fn=next(n for n in main.body if isinstance(n,ast.FunctionDef) and n.name=='add')
spec=importlib.util.spec_from_file_location('current_integrity',PUB/'integrity.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
testroot=C/'policy/audit';testroot.mkdir(parents=True,exist_ok=True);safe=testroot/'normal.txt';safe.write_text('safe')
namespace={'safe_path':mod.safe_path,'AUDIT':testroot,'files':{}}
exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'actual-add-function','exec'),namespace)
add=namespace['add'];guard=[]
def reject(label,name,path):
 namespace['files']={}
 try:add(name,path)
 except (RuntimeError,ValueError,OSError) as e:guard.append({'case':label,'rejected':True,'error':str(e)})
 else:raise AssertionError('not rejected '+label)
for n in ['/abs','../escape','x/../e','x\\e','x:e','x//e','x/./e','']:
 reject('archive malformed '+repr(n),n,safe)
for component in ['.cache','sources','scratch','qa','.secrets','x.private.data']:
 f=testroot/component/'file.txt';f.parent.mkdir(parents=True,exist_ok=True);f.write_text('sentinel');reject('lexical '+component,'allowed.txt',f);reject('archive '+component,component+'/file.txt',safe)
 # Parent symlink makes lexical path allowed but resolved source excluded.
 link=testroot/('link'+str(len(guard)));link.symlink_to(f.parent,target_is_directory=True);reject('resolved '+component,'allowed.txt',link/'file.txt')
f=C/'outside.txt';f.write_text('outside');reject('outside audit','outside.txt',f)
link=testroot/'leaf.txt';link.symlink_to(safe);reject('leaf symlink','leaf.txt',link)
namespace['files']={};add('normal.txt',safe)
try:add('normal.txt',safe)
except RuntimeError as e:guard.append({'case':'duplicate','rejected':True,'error':str(e)})
else:raise AssertionError('duplicate accepted')
res['actual_add_function_policy_controls']=guard
# Fully operational producer refusal of selected leaf symlink and changed original binding.
f=p/'publication/README.md';f.unlink();f.symlink_to(PUB/'README.md');rr=run([sys.executable,'-B',p/'publication/make_package.py'],p/'publication');assert rr.returncode
res['actual_producer_selected_symlink_rejected']=rr.stderr.strip().splitlines()[-1]
f.unlink();shutil.copy2(PUB/'README.md',f);f=p/'original/unsolved_math_prioritization/attempts/30004404/verify_release.py';f.write_bytes(f.read_bytes()+b'\n');rr=run([sys.executable,'-B',p/'publication/make_package.py'],p/'publication');assert rr.returncode
res['actual_producer_changed_original_rejected']=rr.stderr.strip().splitlines()[-1]
# Verify embedded paper and all external metadata fields, no normalization.
assert json.loads((E/'metadata.json').read_bytes())==json.loads((PUB/'zenodo-deposit.json').read_bytes())
assert (E/'zero_filling.tex').read_bytes()==(PUB/'zero_filling.tex').read_bytes()
assert pre==inventory(E)
res['embedded_metadata_exact']=True;res['frozen_inputs_unchanged']=True
save('CONTROLS_RESULT.json',res);print(json.dumps({'status':'PASS','jobs':len(jobs),'outer_payloads':len(m['files']),'nested_entries':entries,'negative_driver_controls':len(mutants),'policy_controls':len(guard),'relocations':len(rel)}))
