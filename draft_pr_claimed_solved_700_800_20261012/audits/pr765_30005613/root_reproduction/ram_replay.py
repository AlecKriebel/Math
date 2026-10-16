import subprocess,os,sys,json,hashlib
from pathlib import Path
p=Path("draft_pr_claimed_solved_700_800_20261012/audits/pr765_30005613/original/unsolved_math_prioritization/attempts/30005613").resolve()
def inv():
 return {x.relative_to(p).as_posix():[len(b:=x.read_bytes()),hashlib.sha256(b).hexdigest()] for x in p.rglob("*") if x.is_file()}
before=inv()
outcomes=[]
for name,opts,opt in [("normal",[],None),("outer_O",["-O"],None),("env_OPTIMIZE_2",[],"2")]:
 env=os.environ.copy();env.pop("PYTHONOPTIMIZE",None);env["PYTHONDONTWRITEBYTECODE"]="1"
 if opt:env["PYTHONOPTIMIZE"]=opt
 proc=subprocess.run([sys.executable,*opts,"-B",str(p/"verify_publication.py")],cwd="/",env=env,capture_output=True)
 outcomes.append({"mode":name,"returncode":proc.returncode,"stdout":proc.stdout.decode(),"stderr":proc.stderr.decode(),"stdout_sha256":hashlib.sha256(proc.stdout).hexdigest()})
 print(json.dumps({"progress":name,"returncode":proc.returncode}),flush=True)
 if proc.returncode:raise RuntimeError(proc.stderr.decode())
after=inv()
if before!=after:raise RuntimeError("frozen candidate modified")
print(json.dumps({"status":"PASS","python":sys.version,"executable":sys.executable,"modes":outcomes,"original_files":before,"original_files_unchanged":len(before),"stdout_equal":len({x["stdout_sha256"] for x in outcomes})==1,"not_run":["External historical corpora/PDF replay","Whole historical queue replay","Fresh negative controls: filesystem ENOSPC"],"scope":"Finite controls and integrity only; not a PDE proof certificate or priority certificate."}),flush=True)
