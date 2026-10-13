"""Owned complete capture of one authorized step; no ROOT helper."""
import argparse,datetime,hashlib,json,os,pathlib,platform,subprocess,sys
r=pathlib.Path(__file__).resolve().parent;p=argparse.ArgumentParser();p.add_argument("step",choices=["accounting","submitted_replay","historical_replay"]);a=p.parse_args()
ops={"accounting":r/"account_original.py","submitted_replay":r/"original/verify.py","historical_replay":r/"reproduction/historical/independent_checks.py"};op=ops[a.step]
cap=r/"captures"/a.step;cap.mkdir(parents=True,exist_ok=False);ob=op.read_bytes();cb=pathlib.Path(__file__).read_bytes()
(cap/"operator_prelaunch.py").write_bytes(ob);(cap/"controller_prelaunch.py").write_bytes(cb)
deps=[]
if a.step=="submitted_replay":
 dep=op.with_name("OBSTRUCTION.md");db=dep.read_bytes();(cap/"OBSTRUCTION_prelaunch.md").write_bytes(db);deps=[{"path":str(dep),"bytes":len(db),"sha256":hashlib.sha256(db).hexdigest()}]
s=datetime.datetime.now(datetime.timezone.utc).isoformat();argv=[sys.executable,"-B",str(op)]
proc=subprocess.Popen(argv,cwd=str(op.parent),env={**os.environ,"GIT_OPTIONAL_LOCKS":"0"},stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out,err=proc.communicate();e=datetime.datetime.now(datetime.timezone.utc).isoformat()
(cap/"stdout.bin").write_bytes(out);(cap/"stderr.bin").write_bytes(err)
j={"schema":"pr62-owned-step-capture/v1","step":a.step,"actual_execution":True,"controller_pid":os.getpid(),"pid":proc.pid,"started_utc":s,"finished_utc":e,"argv":argv,"cwd":str(op.parent),"exit_code":proc.returncode,"python_version":platform.python_version(),"runtime":sys.executable,"operator_prelaunch_sha256":hashlib.sha256(ob).hexdigest(),"controller_prelaunch_sha256":hashlib.sha256(cb).hexdigest(),"operator_unchanged":op.read_bytes()==ob,"local_transitive_inputs":deps,"imports":"Python standard library only; all local authored code is direct operator; author data dependency captured separately.","stdout":{"path":"stdout.bin","bytes":len(out),"sha256":hashlib.sha256(out).hexdigest()},"stderr":{"path":"stderr.bin","bytes":len(err),"sha256":hashlib.sha256(err).hexdigest()},"ROOT_helper_run":False,"new_math_or_review_credit":0,"actual_knot_Floer_computation":False}
(cap/"CAPTURE.json").write_text(json.dumps(j,sort_keys=True,indent=2)+"\n")
print(json.dumps({"step":a.step,"pid":proc.pid,"controller_pid":os.getpid(),"exit_code":proc.returncode,"stdout_bytes":len(out),"stderr_bytes":len(err)},sort_keys=True));sys.exit(proc.returncode)
