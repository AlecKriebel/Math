#!/usr/bin/env python3
import pathlib,datetime,hashlib,json,subprocess,sys
script=pathlib.Path(sys.argv[1]); stem=sys.argv[2]
out=script.parent
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.run([sys.executable,script.name],cwd=out,capture_output=True)
end=datetime.datetime.now(datetime.timezone.utc).isoformat()
stdout=out/(stem+'.stdout.json');stderr=out/(stem+'.stderr.txt')
stdout.write_bytes(p.stdout);stderr.write_bytes(p.stderr)
receipt={'check':script.name,'start_utc':start,'end_utc':end,'returncode':p.returncode,'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'stdout_path':stdout.name,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_path':stderr.name,'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()}
(out/(stem+'_RUN.json')).write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2));print(p.stdout.decode());print(p.stderr.decode());sys.exit(p.returncode)
