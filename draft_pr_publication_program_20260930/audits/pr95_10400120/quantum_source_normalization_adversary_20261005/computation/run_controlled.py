from pathlib import Path
import subprocess,datetime,json,hashlib
p=Path('.')
for filename in ['independent_ht_gauss.py']:
 command=['/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3','computation/'+filename]
 before=datetime.datetime.now(datetime.timezone.utc).isoformat()
 source=Path(command[1]).read_bytes()
 r=subprocess.run(command,capture_output=True)
 stem=filename.removesuffix('.py')
 out=Path('computation/'+stem+'.stdout.txt');err=Path('computation/'+stem+'.stderr.txt')
 out.write_bytes(r.stdout);err.write_bytes(r.stderr)
 rec={'started_utc':before,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':command,'cwd':str(p.resolve()),'script_sha256':hashlib.sha256(source).hexdigest(),'exit_code':r.returncode,'stdout':str(out),'stderr':str(err),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest(),'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr)}
 Path('computation/'+stem+'.process.json').write_text(json.dumps(rec,indent=2)+'\n')
 with Path('operations.jsonl').open('a') as f:f.write(json.dumps({'operation':'controlled_independent_calculation',**rec})+'\n')
 print(json.dumps(rec));print(r.stdout.decode());print(r.stderr.decode())
