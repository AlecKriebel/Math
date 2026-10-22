"""Independent read-only final author packet integrity, after primary freeze."""
import datetime,hashlib,json,pathlib,stat
OWN=pathlib.Path(__file__).resolve().parent
BASE=OWN.parent/"publication_operations_preparation_02"
def need(ok,msg):
    if type(ok) is not bool or not ok:raise RuntimeError(msg)
def pin(raw):return {"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
refs={"SAFE_MANIFEST_02.json":{"bytes":14220,"sha256":"d4f432fe81a61ad74ce6b658faeb6ffcddd8ca7de92b744e96bfda04ad15d8fe"},"SEAL_02.json":{"bytes":2519,"sha256":"dfec8f531253e0e76cfbc2dfa4827bbee01e636a7305ac027783b4245fac11d6"},"ADOPTION_SOURCE_MAP_ONLY.json":{"bytes":837,"sha256":"8483bc7f5dd448ccf12526c10e1a314e16cf1b2d9f34429b58e2117e4177c171"},"verify_artifacts_02.py":{"bytes":3356,"sha256":"faf716cc461a7e347b4ebc3bb553d0fda72800bd4d823c5fa9acda26ebbdeb0d"}}
for rel,wanted in refs.items():need(pin((BASE/rel).read_bytes())==wanted,"Root-supplied author packet pin "+rel)
m=json.loads((BASE/"SAFE_MANIFEST_02.json").read_bytes());s=json.loads((BASE/"SEAL_02.json").read_bytes());source=json.loads((BASE/"ADOPTION_SOURCE_MAP_ONLY.json").read_bytes());final=json.loads((OWN/"FINAL_SOURCE_PINS.json").read_bytes())["sources"]
need(s["manifest_pin"]==refs["SAFE_MANIFEST_02.json"],"seal binds exact manifest")
need(len(m["files"])==s["payload_file_count"]==81,"exact81 payload count")
seen=set();total=0
for row in m["files"]:
    need(set(row)=={"path","bytes","sha256"},"exact manifest record")
    rel=row["path"];need(type(rel) is str and rel and not rel.startswith("/") and all(x not in ("",".","..") for x in rel.split("/")) and "\\" not in rel,"safe relative payload")
    need(rel not in seen,"duplicate manifest path");seen.add(rel)
    p=BASE/rel;need(p.resolve(strict=True)==p,"canonical payload")
    st=p.lstat();need(stat.S_ISREG(st.st_mode) and stat.S_IMODE(st.st_mode)==0o444,"regular0444 payload")
    need(pin(p.read_bytes())=={k:row[k] for k in ("bytes","sha256")},"payload byte pin "+rel);total+=row["bytes"]
need(total==s["payload_total_bytes"]==1186763,"total payload bytes")
actual=set()
for p in BASE.rglob("*"):
    need(not p.is_symlink(),"no packet symlinks")
    if p.is_file():actual.add(p.relative_to(BASE).as_posix())
need(actual==seen|{"SAFE_MANIFEST_02.json","SEAL_02.json"},"bounded complete final packet")
expected={rel:v for rel,v in final.items() if rel.startswith("publication_operations_preparation_02/")}
need(source==expected,"exact five runtime source map excludes artifact/test receipts")
need(s["source_pins"]=={pathlib.Path(k).name:v for k,v in expected.items()},"seal source pins agree")
need("ARTIFACT_VERIFIER_ATTEMPT_01_BINDING.json" in seen and "ARTIFACT_VERIFIER_ATTEMPT_01.stderr" in seen and "verify_artifacts.py" in seen and "verify_artifacts_02.py" in seen,"first verifier failure and correction preserved")
print(json.dumps({"schema":"pr206-independent-author-integrity-only-v1","status":"PASS","UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"payloads":81,"total_bytes":total,"all_payloads_regular0444":True,"exact_final_source_map":True,"initial_verifier_failure_preserved":True,"author_harness_or_verifier_executed":False,"author_functional_claims_used_as_primary_evidence":False,"primary_findings_pin":pin((OWN/"PRIMARY_FINDINGS_01.json").read_bytes()),"reference_pins":refs},sort_keys=True))
