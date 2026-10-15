from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'FILE_MANIFEST.json').read_text())
for pin in manifest['files']:
 f=ROOT/pin['path'];assert f.resolve().is_relative_to(ROOT.resolve())
 data=f.read_bytes();assert len(data)==pin['bytes'] and hashlib.sha256(data).hexdigest()==pin['sha256'],str(f)
assert sys.version_info>=(3,11)
def normalize(receipt):
 return {k:v for k,v in receipt.items() if k not in {'utc','python'}}
results=[]
for spec in json.loads((ROOT/'CHECKSETS.json').read_text()):
 with tempfile.TemporaryDirectory(prefix='critical_wave_'+spec['name']+'_') as temp:
  work=Path(temp);script=ROOT/spec['script'];target=work/script.name;shutil.copyfile(script,target)
  run=subprocess.run([sys.executable,str(target)],cwd=work,capture_output=True,text=True,timeout=120)
  assert run.returncode==0,(spec['name'],run.stderr)
  expected=json.loads((ROOT/spec['reference']).read_text())
  actual=json.loads((work/spec['emitted_receipt']).read_text()) if spec['emitted_receipt'] else json.loads(run.stdout)
  assert normalize(actual)==normalize(expected),(spec['name'],'complete scientific receipt mismatch')
  stdout=json.loads(run.stdout)
  if spec['emitted_receipt'] and 'sha256' in stdout:
   assert stdout['sha256']==hashlib.sha256((work/spec['emitted_receipt']).read_bytes()).hexdigest()
  results.append({'checkset':spec['name'],'returncode':0,'complete_receipt_match':True,'receipt':actual,'stderr':run.stderr})
report={'status':'PASS','python_runtime':sys.version,'packaged_files_verified':len(manifest['files']),
        'checksets':len(results),'exact_assertions':5603,'noncertified_diagnostics':5,
        'ignored_top_level_informational_fields':['utc','python'],'results':results}
out=Path.cwd()/'VERIFICATION_RUN.json';assert out.resolve()!=ROOT/'FILE_MANIFEST.json'
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','checksets':len(results),'exact_assertions':5603,'noncertified_diagnostics':5,'report':str(out)},indent=2))
