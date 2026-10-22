#!/usr/bin/env python3
import pathlib,sys,json,subprocess,shutil,hashlib,os,tempfile
sys.dont_write_bytecode=True
Q=pathlib.Path(__file__).resolve().parent;A=Q.parents[1];P=A.parents[1]/'private/pr0399_package_adversary_02'
B=P/'extract/free-product-tensor-core-verification'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def reseal(root,path,manifest):
 f=root/manifest;m=json.loads(f.read_text());e=next(e for e in m['files'] if e['path']==path);p=root/path;e.update(bytes=p.stat().st_size,sha256=digest(p));f.write_text(json.dumps(m))

results=[]
for mode in ['normal','optimized']:
 flags=['-O']if mode=='optimized'else[]
 with tempfile.TemporaryDirectory(dir=P) as name:
  root=pathlib.Path(name);(root/'a').write_bytes(b'example')
  good={'schema':1,'files':[{'path':'a','bytes':7,'sha256':digest(root/'a')}]}
  cases=[]
  def case(label,alter,expected=False):
   for p in root.iterdir():
    if p.name not in ['a']:p.unlink()
   (root/'a').write_bytes(b'example');(root/'FILES.json').write_text(json.dumps(good));alter(root)
   r=subprocess.run([sys.executable,*flags,'-B',str(B/'tools/integrity.py'),str(root)],capture_output=True,text=True)
   ok=(r.returncode==0)==expected
   if not ok:raise RuntimeError(label+' outcome wrong '+r.stderr)
   cases.append({'label':label,'accepted':r.returncode==0,'as_expected':ok})
  case('valid',lambda r:None,True)
  case('byte_change',lambda r:(r/'a').write_bytes(b'Example'))
  case('extra_file',lambda r:(r/'extra').write_bytes(b''))
  case('symlink',lambda r:(r/'link').symlink_to(r/'a'))
  case('bool_length',lambda r:(r/'FILES.json').write_text(json.dumps({'schema':1,'files':[{'path':'a','bytes':True,'sha256':digest(r/'a')}]})))
  case('bool_schema',lambda r:(r/'FILES.json').write_text(json.dumps({**good,'schema':True})))
  case('escape',lambda r:(r/'FILES.json').write_text(json.dumps({'schema':1,'files':[{'path':'../a','bytes':7,'sha256':digest(r/'a')}]})))
  case('duplicate_path',lambda r:(r/'FILES.json').write_text(json.dumps({'schema':1,'files':good['files']*2})))
  case('duplicate_json_key',lambda r:(r/'FILES.json').write_text('{"schema":1,"schema":1,"files":[]}'))
  case('extra_schema_key',lambda r:(r/'FILES.json').write_text(json.dumps({**good,'surprise':1})))
  case('uppercase_digest',lambda r:(r/'FILES.json').write_text(json.dumps({'schema':1,'files':[{'path':'a','bytes':7,'sha256':digest(r/'a').upper()}]})))
  results.append({'mode':mode,'integrity':cases})
 # Mutation with all byte manifests updated: replay must still reject semantic failure.
 for mutant in ['nested_historical_assert','guarded_family_count']:
  root=P/('mutant_'+mode+'_'+mutant)
  if root.exists():shutil.rmtree(root)
  shutil.copytree(B,root)
  if mutant=='nested_historical_assert':
   path='original/check_density_chain.py';p=root/path;p.write_text('assert False, "reviewer02 deliberate nested child failure"\n')
   # Historical manifest uses a path-keyed object, independently preserve schema.
   m=json.loads((root/'original/PUBLIC_PACKET_MANIFEST.json').read_text())
   if isinstance(m['files'],list):
    e=next(e for e in m['files'] if e['path']=='check_density_chain.py');e.update(bytes=p.stat().st_size,sha256=digest(p))
   elif isinstance(m['files'],dict):m['files']['check_density_chain.py'].update(bytes=p.stat().st_size,sha256=digest(p))
   else:raise RuntimeError('unexpected old manifest shape')
   (root/'original/PUBLIC_PACKET_MANIFEST.json').write_text(json.dumps(m))
   reseal(root,path,'FILES.json');reseal(root,'original/PUBLIC_PACKET_MANIFEST.json','FILES.json')
  else:
   path='reviews/measure_ordinal/independent_controls.py';p=root/path;s=p.read_text();p.write_text(s.replace('10128','10129'))
   if p.read_text()==s:
    # change serialized output status while keeping source code syntactically valid
    p.write_text(s.replace('"PASS"','"FAIL"').replace("'PASS'","'FAIL'"))
   reseal(root,path,'FILES.json')
  env=dict(os.environ);env['PYTHONOPTIMIZE']='2'
  r=subprocess.run([sys.executable,*flags,'-B',str(root/'tools/reproduce.py'),str(root)],capture_output=True,text=True,env=env)
  if r.returncode==0:raise RuntimeError(mutant+' escaped wrapper')
  results.append({'mode':mode,'semantic_mutant':mutant,'rejected':True,'diagnostic':r.stderr[-900:]})
  shutil.rmtree(root)
(Q/'PACKAGE_CONTROLS.json').write_text(json.dumps({'results':results},indent=2)+'\n');print(json.dumps({'status':'PASS','mode_cases':len(results),'all_integrity_cases':22,'semantic_mutants':4}))
