from pathlib import Path
import json,hashlib,datetime
A=Path(__file__).resolve().parent
def require(c,m):
    if not c: raise RuntimeError(m)
def check(base,pin):
    p=Path(pin["path"])
    if not p.is_absolute():p=base/p
    b=p.read_bytes()
    require(len(b)==pin["bytes"] and hashlib.sha256(b).hexdigest()==pin["sha256"],"Pin changed: "+str(p))
    return {"path":str(p),"bytes":len(b),"sha256":pin["sha256"]}
report={}
for family,seal,expected in [
("priority_historical_fc","FINAL_SEAL.json","bfd6cd3f0216536ce5d5f57ded32fd78e106985e7604d190c656e38aa6ba4dbe"),
("priority_current_primary","INPUT_OUTPUT_SEAL.json","103ae7f893664b44e227fbf16816de5191cec3c49e1a09708a958bd479f5ac28"),
("priority_finite_index","INPUT_OUTPUT_BYTEHASH_MANIFEST.json",None)]:
    base=A/family;p=base/seal;b=p.read_bytes();h=hashlib.sha256(b).hexdigest()
    if expected:require(h==expected,"Final seal changed: "+family)
    j=json.loads(b);pins=[]
    if family=="priority_historical_fc":
        for k in ["final_manifest","review","result","private_corpus_manifest","mathematical_derivation"]:pins.append(check(base,j[k]))
        m=json.loads((base/j["final_manifest"]["path"]).read_text())
        for pin in m["initial_inputs"]+m["outputs"]:pins.append(check(base,pin))
        for pin in json.loads((base/"PRIVATE_SOURCE_BYTEHASH_MANIFEST.json").read_text())["files"]:pins.append(check(base,pin))
    elif family=="priority_current_primary":
        pins=[check(base,pin) for pin in j["records"]]
        require(hashlib.sha256((base/"REVIEW.md").read_bytes()).hexdigest()=="0b93515f4927cebfeaddad7ff57592bdc9f2f8fa6d4d5090a0bd9751380b2eaa","Current report changed")
    else:
        pins=[check(base,pin) for pin in j["inputs"]+j["outputs"]]
        require(hashlib.sha256((base/"REVIEW.md").read_bytes()).hexdigest()=="fa956d5d8148d303b2dfb4f3f9a470ce58897e53539532d28a10c10b8ae2d80b","July report changed")
    report[family]={"final_seal_path":seal,"final_seal_sha256":h,"records_authenticated":len(pins),"unique_paths_authenticated":len(set(x["path"] for x in pins)),"pins":pins}
out={"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"ROOT_AUTHENTICATED_ALL_THREE_FINAL_PRIORITY_FAMILY_RECORDS","family_receipts":report,"bibliographic_novelty_or_publication_clearance":False,"mathematical_gate_unchanged":True}
(A/"ROOT_PRIORITY_FAMILY_AUTHENTICATION.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"counts":{f:{"records":r["records_authenticated"],"unique_paths":r["unique_paths_authenticated"]} for f,r in report.items()}}))
