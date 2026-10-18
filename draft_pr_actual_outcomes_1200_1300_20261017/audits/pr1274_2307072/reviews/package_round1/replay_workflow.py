from pathlib import Path
import datetime, hashlib, importlib.util, json, os, socket, subprocess, sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent; A=R.parent.parent; P=A/"publication"
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if "--worker" in sys.argv:
    def denied(*args,**kwargs):raise RuntimeError("Network operation forbidden during independent offline review")
    socket.create_connection=denied;socket.socket.connect=denied
    real_run=subprocess.run; real_output=subprocess.check_output
    def checked(fn):
        def call(args,*rest,**kwargs):
            if not isinstance(args,(list,tuple)) or Path(str(args[0])).name in {"git","gh","gws","curl","wget"}:raise RuntimeError("Live shell/service/Git call forbidden")
            return fn(args,*rest,**kwargs)
        return call
    subprocess.run=checked(real_run);subprocess.check_output=checked(real_output)
    spec=importlib.util.spec_from_file_location("independent_current_workflow",P/"workflow_regression.py");m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    m.REPORT_ROOT=R/"own_local/workflow"
    print(json.dumps(m.worker(),sort_keys=True));raise SystemExit
start=datetime.datetime.now(datetime.timezone.utc).isoformat();runs=[]
for flags in [[],["-O"],["-OO"]]:
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1");env.pop("PYTHONOPTIMIZE",None)
    run=subprocess.run([sys.executable,"-B",*flags,str(Path(__file__).resolve()),"--worker"],capture_output=True,text=True,env=env,timeout=180)
    label="normal" if not flags else flags[0][1:]
    (R/"own_local"/("workflow_"+label+".stdout")).write_text(run.stdout)
    (R/"own_local"/("workflow_"+label+".stderr")).write_text(run.stderr)
    if run.returncode:raise RuntimeError(run.stderr)
    result=json.loads(run.stdout);runs.append({"flags":flags,"result":result})
summary={"schema":"math-pr1274-review-workflow-replay-v1","started_at_utc":start,"completed_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"PASS","all_modes_identical":all(x["result"]==runs[0]["result"] for x in runs),"current_regression_sha256":digest(P/"workflow_regression.py"),"modes":[x["flags"] for x in runs],"identity_cases_per_mode":len(runs[0]["result"]["identity_action_matrix"]["cases"]),"postmerge_cases_per_mode":len(runs[0]["result"]["postmerge_complete_main"]["cases"]),"coordinator_cases_per_mode":len(runs[0]["result"]["deposit_coordinator_actual_kit_mocked_clients"]),"literal_results_summary":{k:v for k,v in runs[0]["result"].items() if k not in {"identity_action_matrix","postmerge_complete_main"}},"limits":"Current actual helper sources and read-only shared Zenodo kit executed only through mocked clients/Git/services and isolated synthetic fixtures; no credentials or live mutation. This supplements separate actual document/archive/mathematical review."}
(R/"WORKFLOW_REPLAY.json").write_text(json.dumps(summary,indent=2)+"\n");print(json.dumps({k:v for k,v in summary.items() if k!="literal_results_summary"}))
