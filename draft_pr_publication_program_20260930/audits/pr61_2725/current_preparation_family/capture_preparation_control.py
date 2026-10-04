"""MIT licensed. New owned preparation capture; this is not a ROOT helper."""
import datetime,hashlib,json,os,pathlib,subprocess,sys
root=pathlib.Path(__file__).resolve().parent
cap=root/"captures"/"preparation_consistency"
cap.mkdir(parents=True,exist_ok=False)
op=root/"prepare_control.py"; opbytes=op.read_bytes()
(cap/"operator_prelaunch.py").write_bytes(opbytes)
dep=(root/"binding_checks.py").read_bytes()
(cap/"binding_checks_prelaunch.py").write_bytes(dep)
controller=pathlib.Path(__file__).read_bytes()
(cap/"controller_prelaunch.py").write_bytes(controller)
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
argv=[sys.executable,"-B",str(op)]
p=subprocess.Popen(argv,cwd=str(root),stdin=subprocess.DEVNULL,
                   stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out,err=p.communicate()
finished=datetime.datetime.now(datetime.timezone.utc).isoformat()
(cap/"stdout.bin").write_bytes(out); (cap/"stderr.bin").write_bytes(err)
receipt={"schema":"pr61-owned-preparation-consistency-capture/v1",
 "actual_execution":True,"wrapper_pid":os.getpid(),"pid":p.pid,
 "started_utc":started,"finished_utc":finished,"argv":argv,"cwd":str(root),
 "stdin_supplied":False,"exit_code":p.returncode,
 "operator_prelaunch_sha256":hashlib.sha256(opbytes).hexdigest(),
 "operator_unchanged":op.read_bytes()==opbytes,
 "controller_prelaunch_sha256":hashlib.sha256(controller).hexdigest(),
 "dependency_prelaunch_sha256":hashlib.sha256(dep).hexdigest(),
 "dependency_unchanged":(root/"binding_checks.py").read_bytes()==dep,
 "stdout":{"path":"stdout.bin","bytes":len(out),"sha256":hashlib.sha256(out).hexdigest()},
 "stderr":{"path":"stderr.bin","bytes":len(err),"sha256":hashlib.sha256(err).hexdigest()},
 "mathematical_proof_or_new_review":False,"ROOT_helper_run":False}
(cap/"CAPTURE.json").write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
print(json.dumps({"capture":str(cap),"pid":p.pid,"exit_code":p.returncode,
 "stdout_bytes":len(out),"stderr_bytes":len(err)},sort_keys=True))
sys.exit(p.returncode)
