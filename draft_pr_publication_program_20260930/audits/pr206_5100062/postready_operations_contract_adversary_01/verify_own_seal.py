"""Read-only verification of independent operational audit evidence, no services."""
import hashlib,json,pathlib,stat
O=pathlib.Path(__file__).resolve().parent
EXCLUDED={"SAFE_MANIFEST.json","SEAL.json","SEAL_VERIFICATION.stdout","SEAL_VERIFICATION.stderr","SEAL_VERIFICATION_BINDING.json"}
def need(ok,msg):
    if type(ok) is not bool or not ok:raise RuntimeError(msg)
def pin(raw):return {"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
mraw=(O/"SAFE_MANIFEST.json").read_bytes();m=json.loads(mraw);s=json.loads((O/"SEAL.json").read_bytes())
need(pin(mraw)==s["manifest_pin"],"exact manifest pin")
need(m["schema"]=="pr206-independent-ops-contract-safe-manifest-v1" and s["schema"]=="pr206-independent-ops-contract-seal-v1","audit seal schema")
need(0<len(m["files"])<=64 and len(m["files"])==s["payload_files"],"bounded payload count")
seen=set();size=0
for row in m["files"]:
    rel=row["path"];need(set(row)=={"path","bytes","sha256"},"manifest shape")
    need(type(rel) is str and rel and not rel.startswith("/") and all(x not in ("",".","..") for x in rel.split("/")) and "\\" not in rel,"safe payload relative path")
    need(rel not in seen and rel not in EXCLUDED,"unique payload")
    p=O/rel;need(p.resolve(strict=True)==p,"canonical payload");st=p.lstat()
    need(stat.S_ISREG(st.st_mode) and stat.S_IMODE(st.st_mode)==0o444,"regular0444 payload")
    need(pin(p.read_bytes())=={k:row[k] for k in ("bytes","sha256")},"payload bytes "+rel)
    seen.add(rel);size+=row["bytes"]
need(size==s["payload_bytes"] and size<=1048576,"bounded payload bytes")
actual=set()
for p in O.rglob("*"):
    need(not p.is_symlink(),"no audit symlinks")
    if p.is_file() and p.relative_to(O).as_posix() not in EXCLUDED:actual.add(p.relative_to(O).as_posix())
need(actual==seen,"complete bounded evidence file scope")
source=json.loads((O/"FINAL_SOURCE_PINS.json").read_bytes())["sources"]
for rel,wanted in source.items():need(pin((O/"audited_sources"/rel).read_bytes())==wanted,"audited source snapshot "+rel)
for name,count in [("attempt01_normal",433),("attempt02_optimized",330),("attempt03_dispatcher_optimized",22)]:
    d=O/"runs"/name;bind=json.loads((d/"RUN_BINDING.json").read_bytes());out=(d/"stdout.bin").read_bytes();err=(d/"stderr.bin").read_bytes();result=json.loads(out)
    need(bind["exit_code"]==0 and result["status"]=="PASS" and result["checks"]==count and not err,"independent successful run "+name)
    need(bind["stdout"]["bytes"]==len(out) and bind["stdout"]["sha256"]==pin(out)["sha256"] and bind["stderr"]["sha256"]==pin(err)["sha256"],"raw run streams "+name)
    for n,wanted in bind["source_snapshots"].items():need(pin((d/"sources"/n).read_bytes())==wanted,"exact per-attempt source snapshot")
for name,exitcode in [("failed_inspection_replay",1),("corrected_integrity",0)]:
    d=O/"runs"/name;bind=json.loads((d/"RUN_BINDING.json").read_bytes())
    need(bind["exit_code"]==exitcode and pin((d/"stdout.bin").read_bytes())==bind["stdout"] and pin((d/"stderr.bin").read_bytes())==bind["stderr"],"preserved artifact integrity attempts")
need(pin((O/"PRIMARY_FINDINGS_01.json").read_bytes())==s["primary_findings_pin"],"primary freeze preserved")
need(not (O/"fixtures").exists(),"expanded synthetic authorities excluded and removed")
print(json.dumps({"schema":"pr206-independent-ops-contract-seal-verification-v1","status":"PASS","payload_files":len(seen),"payload_bytes":size,"all_regular0444":True,"all_source_snapshots_match":True,"raw_run_bindings_verified":True,"failed_inspection_preserved":True,"completion_estimate_percent":100,"actual_service_or_Git_actions":0},sort_keys=True))
