import sys, pathlib, subprocess, hashlib, json, datetime, os
assert __debug__
root=pathlib.Path(__file__).resolve().parent
name=sys.argv[1]
assert '/' not in name and name not in ('.','..')
argv=sys.argv[3:]
assert sys.argv[2]=='--' and argv
folder=root/name
folder.mkdir(exist_ok=False)
source=pathlib.Path(__file__).read_bytes()
(folder/'prelaunch_operator.py').write_bytes(source)
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
proc=subprocess.Popen(argv,cwd='/Users/alec/Documents/Math',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out,err=proc.communicate()
end=datetime.datetime.now(datetime.timezone.utc).isoformat()
for path,data in [('stdout.bin',out),('stderr.bin',err)]:
 (folder/path).write_bytes(data)
rec={'schema':'pr48-smooth-geometry-actual-command-capture/v1','argv':argv,'cwd':'/Users/alec/Documents/Math','pid':proc.pid,'started_utc':start,'finished_utc':end,'exit_code':proc.returncode,'operator_sha256':hashlib.sha256(source).hexdigest(),'streams':{path:{'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()} for path,data in [('stdout.bin',out),('stderr.bin',err)]}}
(folder/'CAPTURE.json').write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec,indent=2))
sys.exit(proc.returncode)
