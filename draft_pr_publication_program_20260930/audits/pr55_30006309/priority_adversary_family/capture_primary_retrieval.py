from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
F=Path(__file__).resolve().parent
cap=F/'primary_retrieval_actual_capture'
cap.mkdir(exist_ok=False)
argv=['/usr/bin/python3',str(F/'retrieve_primary_metadata.py')]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.Popen(argv,cwd='/Users/alec/Documents/Math',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(cap/'START.json').write_text(json.dumps({'schema':'actual-source-capture/v1','capture_parent_pid':os.getpid(),'child_pid':p.pid,'argv':argv,'cwd':'/Users/alec/Documents/Math','started_utc':start,'root_authority':False},indent=2)+'\n')
out,err=p.communicate()
(cap/'stdout.txt').write_bytes(out);(cap/'stderr.txt').write_bytes(err)
result={'schema':'actual-source-capture-result/v1','child_pid':p.pid,'argv':argv,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'returncode':p.returncode,'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_bytes':len(err),'stderr_sha256':hashlib.sha256(err).hexdigest(),'root_authority':False,'is_root_closure':False}
(cap/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));sys.exit(p.returncode)
