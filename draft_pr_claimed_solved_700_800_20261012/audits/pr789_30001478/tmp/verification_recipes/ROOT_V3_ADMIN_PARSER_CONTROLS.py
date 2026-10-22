from pathlib import Path
import datetime,hashlib,json,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");M=T/"root-receipts";W=T/"admin_scope/packet";out=[]
for n,pin in [("PUBLIC_VERIFY.py","cba5bba7181469cdf29617c3a6a4502b9b610ec9e8ec33ef4bc83289e31ffe68"),("TRACKER_VERIFY.py","1df0acfdfe81ead0a824de028392f95e6455a685bf9222fab713512fbd2697e6")]:
 assert hashlib.sha256((W/n).read_bytes()).hexdigest()==pin
 p=subprocess.run([sys.executable,"-I","-B",str(W/n),"--controls-only"],capture_output=True,text=True,timeout=90);assert p.returncode==0 and not p.stderr,(p.stdout,p.stderr)
 v=json.loads(p.stdout);assert "CONTROLS_ONLY"in v["result"]
 (M/("ROOT_V3_"+n.removesuffix(".py")+"_CONTROLS.json")).write_text(p.stdout)
 out.append({"checker":n,"sha256":pin,"result":v["result"],"controls":len(v["controls"])})
print(json.dumps(out))

