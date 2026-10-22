"""Reproduce the package controls and require rejection of deliberate corruptions."""
from pathlib import Path
import tempfile,subprocess,sys,json,hashlib
P=Path(__file__).resolve().parent
def require(c,m):
    if not c:raise RuntimeError(m)
def run(d,optimized):
    flags=["-E","-S","-B","-P"]+(["-O"] if optimized else [])
    return subprocess.run([sys.executable,*flags,str(d/"verify.py")],cwd=d,capture_output=True,text=True)
source=(P/"verify.py").read_text()
good=[]
for opt in (False,True):
    r=run(P,opt);require(r.returncode==0,"baseline failed")
    j=json.loads(r.stdout);require(j["checks"]==33512,"wrong control count")
    name="verification.optimized.json" if opt else "verification.normal.json"
    (P/name).write_text(r.stdout)
    good.append({"optimized":opt,"exit_code":r.returncode,"checks":j["checks"]})
mutations={
"wrong_sign":("def eps(c):return 1 if c%4 in (0,1) else -1","def eps(c):return 1"),
"wrong_index_kernel":("idx1=1 if c==0 else 2;idx2=4//len(K)","idx1=1 if c==0 else 2;idx2=4//len(K)+1")}
bad=[]
with tempfile.TemporaryDirectory(prefix="pr156_controls_") as tmp:
    root=Path(tmp)
    for name,(old,new) in mutations.items():
        require(source.count(old)==1,"mutation anchor missing")
        d=root/name;d.mkdir();(d/"verify.py").write_text(source.replace(old,new))
        (d/"property_s_counterexample.tex").write_bytes((P/"property_s_counterexample.tex").read_bytes())
        for opt in (False,True):
            r=run(d,opt);require(r.returncode!=0 and "RuntimeError" in r.stderr,"broken control falsely passed")
            bad.append({"mutation":name,"optimized":opt,"exit_code":r.returncode,"stderr":r.stderr.replace(str(root),"<TEMP>")})
out={"status":"PASS_BASELINES_AND_REJECT_ALL_NEGATIVE_CONTROLS","good":good,"negative_controls":bad,"verifier_sha256":hashlib.sha256((P/"verify.py").read_bytes()).hexdigest(),"manuscript_sha256":hashlib.sha256((P/"property_s_counterexample.tex").read_bytes()).hexdigest(),"limitation":"Finite and symbolic diagnostics support the written universal proof; finite tests do not prove infinitude or priority."}
(P/"negative_controls.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"baselines":len(good),"mutations_rejected":len(bad)},indent=2))

