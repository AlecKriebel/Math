"""Owned retrieval controller; not a ROOT helper."""
import datetime,hashlib,json,os,pathlib,subprocess,sys
r=pathlib.Path(__file__).resolve().parent;cap=r/"captures/retrieval";cap.mkdir(parents=True,exist_ok=False)
op=r/"retrieve_original.py";ob=op.read_bytes();cb=pathlib.Path(__file__).read_bytes()
(cap/"operator_prelaunch.py").write_bytes(ob);(cap/"controller_prelaunch.py").write_bytes(cb)
start=datetime.datetime.now(datetime.timezone.utc).isoformat();argv=[sys.executable,"-B",str(op)]
p=subprocess.Popen(argv,cwd="/Users/alec/Documents/Math",stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,"GIT_OPTIONAL_LOCKS":"0"})
out,err=p.communicate();end=datetime.datetime.now(datetime.timezone.utc).isoformat()
(cap/"stdout.bin").write_bytes(out);(cap/"stderr.bin").write_bytes(err)
j={"schema":"pr62-owned-retrieval-capture/v1","actual_execution":True,"controller_pid":os.getpid(),"pid":p.pid,"started_utc":start,"finished_utc":end,"argv":argv,"cwd":"/Users/alec/Documents/Math","exit_code":p.returncode,"operator_prelaunch_sha256":hashlib.sha256(ob).hexdigest(),"controller_prelaunch_sha256":hashlib.sha256(cb).hexdigest(),"operator_unchanged":op.read_bytes()==ob,"stdout":{"path":"stdout.bin","bytes":len(out),"sha256":hashlib.sha256(out).hexdigest()},"stderr":{"path":"stderr.bin","bytes":len(err),"sha256":hashlib.sha256(err).hexdigest()},"ROOT_helper_run":False,"native_mutation":False}
(cap/"CAPTURE.json").write_text(json.dumps(j,sort_keys=True,indent=2)+"\n")
print(json.dumps({"pid":p.pid,"controller_pid":os.getpid(),"exit_code":p.returncode,"stdout_bytes":len(out),"stderr_bytes":len(err)},sort_keys=True));sys.exit(p.returncode)
