from pathlib import Path
import hashlib,json,subprocess,sys,shutil,datetime,os
OWN=Path(__file__).resolve().parent
ROOT=OWN/'extracted'
manifest=json.loads((ROOT/'FILE_MANIFEST.json').read_text())
listed={pin['path'] for pin in manifest['files']}
actual={str(f.relative_to(ROOT)) for f in ROOT.rglob('*') if f.is_file()}
assert actual==listed|{'FILE_MANIFEST.json'},(actual-listed,listed-actual)
file_results=[]
for pin in manifest['files']:
 p=ROOT/pin['path'];assert p.resolve().is_relative_to(ROOT)
 data=p.read_bytes();r={'path':pin['path'],'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'complete_pin_match':len(data)==pin['bytes'] and hashlib.sha256(data).hexdigest()==pin['sha256']};assert r['complete_pin_match'],r;file_results.append(r)
checks=json.loads((ROOT/'CHECKSETS.json').read_text())
results=[]
for spec in checks:
 out=OWN/'replays'/spec['name'];out.mkdir(parents=True,exist_ok=True)
 target=out/Path(spec['script']).name;shutil.copyfile(ROOT/spec['script'],target)
 run=subprocess.run([sys.executable,str(target)],cwd=out,capture_output=True,text=True,timeout=120)
 (out/'stdout.txt').write_text(run.stdout);(out/'stderr.txt').write_text(run.stderr)
 assert run.returncode==0,(spec['name'],run.returncode,run.stderr)
 receipt=json.loads((out/spec['emitted_receipt']).read_text()) if spec['emitted_receipt'] else json.loads(run.stdout)
 expected=json.loads((ROOT/spec['reference']).read_text())
 ignored=[k for k in ('utc','python') if k in receipt or k in expected]
 norm=lambda q:{k:v for k,v in q.items() if k not in ('utc','python')}
 assert norm(receipt)==norm(expected),spec['name']
 (out/'ACTUAL_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
 stdout=json.loads(run.stdout)
 if spec['emitted_receipt'] and 'sha256' in stdout:
  assert stdout['sha256']==hashlib.sha256((out/spec['emitted_receipt']).read_bytes()).hexdigest()
 count=receipt.get('assertions',receipt.get('exact_assertions',receipt.get('exact_checks')))
 diagnostics=receipt.get('categories',{}).get('numeric_linear_pulse_diagnostic',0)
 results.append({'name':spec['name'],'returncode':run.returncode,'complete_scientific_receipt_match':True,'ignored_informational_top_level_fields':ignored,'reported_count':count,'receipt':receipt})
 (out/'COMPARISON.json').write_text(json.dumps(results[-1],indent=2)+'\n')
 print(spec['name'],count,ignored,flush=True)
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'file_manifest_entries':len(listed),'exact_archive_files':len(actual),'all_payload_pins_verified':True,'exact_file_set_verified':True,'seven_complete_receipt_matches':True,'file_results':file_results,'checksets':results}
(OWN/'FROZEN_ARCHIVE_REPLAY.json').write_text(json.dumps(report,indent=2)+'\n')
temp=OWN/'runner_temp';temp.mkdir(exist_ok=True)
run=subprocess.run([sys.executable,str(ROOT/'verify_all.py')],cwd=OWN,capture_output=True,text=True,timeout=240,env={**os.environ,'TMPDIR':str(temp)})
(OWN/'runner_stdout.txt').write_text(run.stdout);(OWN/'runner_stderr.txt').write_text(run.stderr)
assert run.returncode==0,(run.returncode,run.stderr)
print(run.stdout)
