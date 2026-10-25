from pathlib import Path
import hashlib,json,shutil,subprocess,datetime,time
here=Path(__file__).resolve().parent
src=here.parents[1]/'sources/published-source/simple-brace-counterexample-source-and-verification'
cache=here/'cache/replay-publication'
assert not cache.exists()
shutil.copytree(src,cache)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs={str(p.relative_to(src)):h(p) for p in src.rglob('*') if p.is_file()}
(here/'replay-inputs.json').write_text(json.dumps(inputs,indent=2,sort_keys=True)+'\n')
py='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
cmd=[py,'-B',str(cache/'verification/verify_all.py'),'--mode','both']
started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
with (here/'replay.stdout.txt').open('w') as out,(here/'replay.stderr.txt').open('w') as err:
 r=subprocess.run(cmd,stdout=out,stderr=err,timeout=300)
unchanged=all(h(src/name)==digest for name,digest in inputs.items())
assert unchanged
result={'started_utc':started,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'elapsed_seconds':time.monotonic()-t,'exit_code':r.returncode,'python':subprocess.check_output([py,'--version'],text=True).strip(),'source_file_count':len(inputs),'sources_unchanged':unchanged,'isolation':'79-file copy inside ignored review cache; published runner additionally uses temporary per-checker mirrors.','status':'PASS' if r.returncode==0 else 'FAIL','no_archived_assessment_bodies_used':'Executable code and numeric expected artifacts were inspected/replayed; historical report/verdict bodies were not read.'}
(here/'replay.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
