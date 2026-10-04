"""One actual preparer source-integrity child capture; no ROOT authority."""
import datetime,hashlib,json,os,pathlib,subprocess,sys
F=pathlib.Path(__file__).absolute().parent
R=F.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
cap=F/'actual_preparation_check';cap.mkdir(exist_ok=False)
operator=pathlib.Path(__file__).read_bytes();child=(F/'verify_priority.py').read_bytes()
(cap/'prelaunch_operator.py').write_bytes(operator);(cap/'prelaunch_child.py').write_bytes(child)
argv=['/usr/bin/python3','-B',str(F/'verify_priority.py')]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.Popen(argv,cwd=str(R),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out,err=p.communicate();end=datetime.datetime.now(datetime.timezone.utc).isoformat()
(cap/'stdout.bin').write_bytes(out);(cap/'stderr.bin').write_bytes(err)
c={'schema':'actual-priority-source-preparation-capture/v1','pid':p.pid,'capture_parent_pid':os.getpid(),'argv':argv,'cwd':str(R),'started_at':start,'completed_at':end,'exit_code':p.returncode,'operator_sha256':sha(operator),'child_sha256':sha(child),'operator_unchanged':operator==pathlib.Path(__file__).read_bytes(),'child_unchanged':child==(F/'verify_priority.py').read_bytes(),'stdout':{'path':'stdout.bin','bytes':len(out),'sha256':sha(out)},'stderr':{'path':'stderr.bin','bytes':len(err),'sha256':sha(err)},'root_authority':False,'is_root_closure':False}
(cap/'CAPTURE.json').write_text(json.dumps(c,indent=2)+'\n')
print(json.dumps(c,indent=2));sys.exit(p.returncode)
