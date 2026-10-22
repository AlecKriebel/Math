from pathlib import Path
import hashlib,json,zipfile,ast,subprocess,os,sys
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent
P=HERE.parent/'publication_package_v1'; M=P/'materials'
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def need(c,s):
 if not c:raise RuntimeError(s)
seal=json.loads((P/'PACKAGE_SEAL.json').read_bytes())
need(pin(P/'PACKAGE_SEAL.json')=={'bytes':21091,'sha256':'d8bf1dbb37175a2b8799f81564d2f742f04f942628d6463f32af30adb0db0bd6'},'seal')
actual={str(p.relative_to(P)):pin(p) for p in P.rglob('*') if p.is_file() and p.name!='PACKAGE_SEAL.json'}
need(actual==seal['package_files_excluding_this_seal'],'outer exact inventory')
manifest=json.loads((M/'MANIFEST.json').read_bytes())
materials={str(p.relative_to(M)):pin(p) for p in M.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
# Exclude only root manifest, not original nested manifest.
materials={str(p.relative_to(M)):pin(p) for p in M.rglob('*') if p.is_file() and p!=M/'MANIFEST.json'}
need(materials==manifest['files'],'material exact inventory')
need(not any(p.is_symlink() for p in P.rglob('*')),'symlinks')
with zipfile.ZipFile(P/'verification-package.zip') as z:
 names=z.namelist();need(len(names)==len(set(names)),'duplicate zip names')
 need(set(names)==set(materials)|{'MANIFEST.json'},'zip exact membership')
 need(not any(n.startswith('/') or '..' in Path(n).parts for n in names),'zip traversal')
 need(all(z.read(n)==(M/n).read_bytes() for n in names),'zip bytes')
 zipinfo=[{'name':i.filename,'bytes':i.file_size,'compressed_bytes':i.compress_size,'mode':oct(i.external_attr>>16)} for i in z.infolist()]
need((P/'original_pedal_flag.tex').read_bytes()==(M/'original_pedal_flag.tex').read_bytes(),'source equality')
need(json.loads((P/'zenodo-deposit.json').read_bytes())['metadata']==json.loads((M/'metadata.json').read_bytes()),'metadata equality')
provenance=json.loads((M/'PORTABILITY_PROVENANCE.json').read_bytes())
for name,r in provenance.items():
 old=M/r['original_path'];new=M/'verification'/name
 need(pin(old)==r['original'] and pin(new)==r['portable'],'portable pins '+name)
 data=old.read_text()
 for line in r['only_removed_lines']:
  need(data.count(line)==1,'removed line occurrence');data=data.replace(line,'')
 need(data==new.read_text(),'only declared line removal '+name)
python=[]
for p in M.rglob('*.py'):
 tree=ast.parse(p.read_text());python.append({'path':str(p.relative_to(M)),'pin':pin(p),'assert_nodes':sum(isinstance(a,ast.Assert) for a in ast.walk(tree))})
textfiles=[]
for p in M.rglob('*'):
 if p.is_file():
  b=p.read_bytes()
  try:s=b.decode('utf-8')
  except UnicodeDecodeError:raise RuntimeError('unexpected binary material '+str(p))
  textfiles.append({'path':str(p.relative_to(M)),'bytes':len(b),'lines':len(s.splitlines())})
report={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','seal':pin(P/'PACKAGE_SEAL.json'),'outer_files_excluding_seal':len(actual),'outer_files_including_seal':len(actual)+1,'material_pins':len(materials),'zip_entries':len(zipinfo),'zip_inventory':zipinfo,'python':python,'all_utf8_material_inventory':textfiles,'metadata_equal':True,'manuscript_sources_equal':True,'portable_changes_exactly_declared':True}
(HERE/'INTEGRITY_RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['zip_inventory','python','all_utf8_material_inventory']}))
runtime=HERE.parent.parent/'pr200_5100007/math_algebra_family_01/runtime_packages'
env=dict(os.environ,PYTHONPATH=str(runtime),PYTHONDONTWRITEBYTECODE='1')
results=[]
for opt in [False,True]:
 argv=[sys.executable,'-B']+(['-O'] if opt else [])+[str(M/'verification/run_checks.py')]
 r=subprocess.run(argv,capture_output=True,text=True,env=env);need(r.returncode==0,'runner '+r.stderr)
 results.append({'optimized':opt,'returncode':r.returncode,'report':json.loads(r.stdout)})
 for suffix in [['--guard-false']]:
  fail=subprocess.run(argv+suffix,capture_output=True,text=True,env=env)
  need(fail.returncode!=0 and 'DELIBERATE FALSE CONDITION' in fail.stderr,'false guard enforcement')
  results.append({'optimized':opt,'probe':suffix,'returncode':fail.returncode,'stderr':fail.stderr})
(HERE/'FRESH_REPRODUCTION_RECEIPT.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'results':results},indent=2)+'\n')
print('FRESH ORDINARY/OPTIMIZED RUNNERS AND FALSE GUARDS: PASS')
