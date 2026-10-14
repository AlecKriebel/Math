from pathlib import Path
import subprocess,time,datetime,json,hashlib,concurrent.futures
out=Path(__file__).resolve().parent;root=out.parent.parent/'preprint';raw=out/'sources/raw/rerun';raw.mkdir(parents=True,exist_ok=True)
py='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
items=[('transfer',root/'evidence/fresh_20261013/transfer_01/fresh_checks.py'),('invariant',root/'evidence/fresh_20261013/invariant_01/verify_invariants.py')]
for mode,p in items:
 dest=raw/mode;dest.mkdir(exist_ok=True);(dest/p.name).write_bytes(p.read_bytes())
def run(item):
 mode,p=item;dest=raw/mode;script=dest/p.name;started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
 argv=[py,'-B',str(script),'--mode','all']
 if mode=='invariant':argv+=['--max-m','6','--max-n','7','--max-r','6','--output',str(dest/'CHECK_RESULTS.json')]
 r=subprocess.run(argv,cwd=dest,capture_output=True,timeout=240)
 (out/('RERUN_'+mode+'.stdout')).write_bytes(r.stdout);(out/('RERUN_'+mode+'.stderr')).write_bytes(r.stderr)
 row={'mode':mode,'argv':argv,'utc':started,'elapsed_seconds':time.monotonic()-t,'exit_code':r.returncode,'stderr_empty':not r.stderr,'code_sha256':hashlib.sha256(script.read_bytes()).hexdigest()}
 if r.returncode==0:
  filename='CHECK_RESULTS_all.json' if mode=='transfer' else 'CHECK_RESULTS.json';b=(dest/filename).read_bytes();(out/('RERUN_'+mode+'_RESULTS.json')).write_bytes(b);row['result_sha256']=hashlib.sha256(b).hexdigest();row['bytes']=len(b)
 print(json.dumps(row),flush=True);return row
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e:rows=list(e.map(run,items))
(out/'RERUN_RECEIPTS.json').write_text(json.dumps(rows,indent=2)+'\n')
