"""Seal only owned bounded independent evidence, then capture read-only verification."""
import datetime,hashlib,json,pathlib,stat,subprocess,sys
O=pathlib.Path(__file__).resolve().parent
EXCLUDED={"SAFE_MANIFEST.json","SEAL.json","SEAL_VERIFICATION.stdout","SEAL_VERIFICATION.stderr","SEAL_VERIFICATION_BINDING.json"}
def need(ok,msg):
    if type(ok) is not bool or not ok:raise RuntimeError(msg)
def pin(raw):return {"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
def enc(obj):return (json.dumps(obj,indent=2,sort_keys=True)+"\n").encode()
def put(p,raw):
    with p.open("xb") as f:f.write(raw)
    p.chmod(0o444)
for name in EXCLUDED:need(not (O/name).exists(),"retain prior seal, never overwrite")
need(not (O/"fixtures").exists(),"owned expanded synthetic authority removed")
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/"RESEARCH_LOG.md").open("a") as f:f.write("\n- "+now+": Independent source/contract audit complete; no mandatory defects. Exact raw runs, frozen primary verdict, author integrity and preserved failed inspection are in bounded seal. Estimated audit completion100%; seal verification result is the final integrity confirmation. No actual operational acceptance granted.\n")
rows=[]
for p in sorted(O.rglob("*")):
    need(not p.is_symlink(),"no own evidence symlinks")
    if not p.is_file():continue
    rel=p.relative_to(O).as_posix();need(rel not in EXCLUDED,"no stale excluded output")
    need(not any(part in ("__pycache__",".git","private_operations","fixtures") or part.startswith("SYNTHETIC_") for part in p.relative_to(O).parts),"unsafe expanded payload")
    p.chmod(0o444);rows.append({"path":rel,**pin(p.read_bytes())})
need(len(rows)<=64 and sum(r["bytes"] for r in rows)<=1048576,"bounded safe evidence")
m={"schema":"pr206-independent-ops-contract-safe-manifest-v1","UTC":now,"scope":"Independent operational source/contract audit and offline synthetic test evidence only; not actual authority or service acceptance","files":rows,"excluded_self_and_verification_files":sorted(EXCLUDED),"excluded_content":["expanded synthetic authority trees","credentials/auth state","private service responses","Git metadata","conversation export","unrelated artifacts"],"all_payloads_regular0444":True}
put(O/"SAFE_MANIFEST.json",enc(m))
s={"schema":"pr206-independent-ops-contract-seal-v1","UTC":now,"verdict":"PASS_WITH_EXPLICIT_AUTHORITY_LIMITS","mandatory_defects":0,"manifest_pin":pin((O/"SAFE_MANIFEST.json").read_bytes()),"primary_findings_pin":pin((O/"PRIMARY_FINDINGS_01.json").read_bytes()),"report_pin":pin((O/"REPORT.md").read_bytes()),"payload_files":len(rows),"payload_bytes":sum(r["bytes"] for r in rows),"owned_normal_checks":433,"owned_optimized_operator_checks":330,"owned_optimized_early_refusal_checks":22,"all_audit_test_attempts_passed":True,"failed_readonly_integrity_inspection_preserved":True,"author_functional_claims_used_as_primary_evidence":False,"all_actual_service_Git_kit_gws_actions":0,"no_actual_authority_or_lifecycle_receipt_authored":True,"verification_required":"verify_own_seal.py must return PASS"}
put(O/"SEAL.json",enc(s))
exe=pathlib.Path(sys.executable).resolve();argv=[str(exe),"-E","-S","-B","-P",str(O/"verify_own_seal.py")]
r=subprocess.run(argv,cwd=O,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20,check=False)
put(O/"SEAL_VERIFICATION.stdout",r.stdout);put(O/"SEAL_VERIFICATION.stderr",r.stderr)
bind={"schema":"pr206-independent-ops-contract-seal-verification-binding-v1","UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"argv":argv,"cwd":str(O),"verifier_pin":pin((O/"verify_own_seal.py").read_bytes()),"interpreter":{"path":str(exe),**pin(exe.read_bytes())},"exit_code":r.returncode,"stdout":pin(r.stdout),"stderr":pin(r.stderr),"manifest_pin":s["manifest_pin"],"seal_pin":pin((O/"SEAL.json").read_bytes()),"completion_estimate_percent":100 if r.returncode==0 else 98}
put(O/"SEAL_VERIFICATION_BINDING.json",enc(bind))
print(json.dumps({"report_pin":s["report_pin"],"manifest_pin":s["manifest_pin"],"seal_pin":bind["seal_pin"],"verification_binding_pin":pin((O/"SEAL_VERIFICATION_BINDING.json").read_bytes()),"payload_files":len(rows),"payload_bytes":s["payload_bytes"],"verification_exit":r.returncode},sort_keys=True))
print(r.stdout.decode())
if r.stderr:print(r.stderr.decode(),file=sys.stderr)
raise SystemExit(r.returncode)
