from pathlib import Path
import subprocess,sys,hashlib,json,datetime,os
A=Path("draft_pr_claimed_solved_900_1000_20261012/audits/pr967_2616").resolve()
O=A/"original/unsolved_math_prioritization/attempts/2616"
v=O/"author/public/verify.py"; assert hashlib.sha256(v.read_bytes()).hexdigest()=="b805650e49c5096f0fe368653122989c1087f59447871a5cb6fc32843d6983d1"
R=A/"root_execution_checks";R.mkdir(exist_ok=False)
payload=b"["*2000+b"0"+b"]"*2000
rows=[]
for mode,flags in [(0,[]),(1,["-O"]),(2,["-OO"])]:
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 result=subprocess.run([sys.executable,"-I","-S","-B",*flags,str(v),"--stdin"],input=payload,cwd=R,capture_output=True,timeout=20)
 for stream,raw in [("stdout",result.stdout),("stderr",result.stderr)]: (R/f"nested_mode{mode}.{stream}.txt").write_bytes(raw)
 try: structured=json.loads(result.stderr).get("ok") is False
 except (ValueError,AttributeError): structured=False
 rows.append({"start_utc":start,"end_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"mode":mode,"argv":[sys.executable,"-I","-S","-B",*flags,str(v),"--stdin"],"input_bytes":len(payload),"input_sha256":hashlib.sha256(payload).hexdigest(),"exit":result.returncode,"stdout_bytes":len(result.stdout),"stderr_bytes":len(result.stderr),"stderr_sha256":hashlib.sha256(result.stderr).hexdigest(),"structured_json_rejection":structured,"uncaught_recursion_error":b"RecursionError" in result.stderr})
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"purpose":"Independent root confirmation of newly reported optional error-format issue; no theorem impact","verifier_sha256":hashlib.sha256(v.read_bytes()).hexdigest(),"uid":os.getuid(),"python":sys.version,"payload_definition":"2000 opening brackets + ASCII0 +2000 closing brackets","runs":rows,"required_mathematical_repair":False,"frozen_original_unchanged":True}
(R/"ROOT_NESTED_JSON_REPRODUCTION.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
