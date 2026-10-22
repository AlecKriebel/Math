from pathlib import Path
import datetime,hashlib,json,stat
A=Path(__file__).resolve().parent
cases=[
("priority_direct_history","private/FINAL_INVENTORY.json","d06858b45a3c2a2719f305d9a7af1ec16855309f69cc3d8523d8e05a4a76401e",102,"relative_path"),
("priority_real_algebraic","public/FINAL_INVENTORY.json","1e8cf1414f924645a9bae2fb59078a1cd544f6618bfcc42ec76db28b786ca1cd",46,"path"),
("priority_quantum_spectra","FINAL_MANIFEST.json","f18064ea3ed5b02625c003c6583af6cc845a3238c10a2dc1200ba7a06517632b",165,"path")]
first=[
("priority_direct_history/public/FIRST_ASSESSMENT.md","9a97bf6265dcd44ef69ac016056437abe56c51596ba5a6a999e62cdc9dd76f22"),
("priority_direct_history/public/FIRST_SEAL.json","0b50b7800826d611449a78d6a27bc6c3b2f5f32114adccfe65c71aa392d3e478"),
("priority_real_algebraic/public/FIRST_ASSESSMENT.md","267cd314cfc80018369a4e01caf50ad8eea2fd20f98d8acf31bc88f9a65b61ab"),
("priority_real_algebraic/public/FIRST_ASSESSMENT_SEAL.json","516dbbb826b4294e8a636588489009559fd1b85c1bfb14effede28455e19152e"),
("priority_quantum_spectra/first_assessment.md","0ce16b6a07deb7c0af7a4511414d552667e0113c6d2758cb316c6c781b957117"),
("priority_quantum_spectra/FIRST_ASSESSMENT_SEAL.json","36d1840ab2d5b44ceab86a2660c1136ece57a47e96998d294a237437dbe71815")]
def require(c,m):
 if not c:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),"mode":f"{stat.S_IMODE(p.stat().st_mode):04o}"}
results=[]
for name,mname,msha,count,key in cases:
 D=A/name;M=D/mname
 require(pin(M)["sha256"]==msha and pin(M)["mode"]=="0444","Manifest changed "+name)
 j=json.loads(M.read_text());entries=j["files"]
 require(len(entries)==count,"Wrong inventory count "+name)
 names={e[key] for e in entries}
 require(len(names)==count and names=={str(p.relative_to(D)) for p in D.rglob("*") if p.is_file() and p!=M},"Incomplete retained inventory "+name)
 for e in entries:
  p=D/e[key];require(p.resolve().is_relative_to(D.resolve()),"Escaping entry")
  actual=pin(p)
  require(actual["bytes"]==e["bytes"] and actual["sha256"]==e["sha256"] and actual["mode"]=="0444","Artifact changed "+name+"/"+e[key])
 if name=="priority_direct_history":allow=json.loads((D/j["public_allowlist"]).read_text())["allowlisted_relative_paths"]
 elif name=="priority_real_algebraic":allow=json.loads((D/j["publication_allowlist"]).read_text())["allowlist"]
 else:allow=j["own_output_public_allowlist"]
 require(set(allow)<=names|{mname},"Unknown public member "+name)
 require(not any(x.startswith("private/") or "raw_headers" in x for x in allow),"Private public member "+name)
 results.append({"family":name,"manifest":str(M.relative_to(A)),"manifest_identity":pin(M),"retained_entries":count,"public_allowlist":allow})
for name,sha in first:
 require(pin(A/name)["sha256"]==sha and pin(A/name)["mode"]=="0444","First record changed "+name)
receipt={"UTC":datetime.datetime.now(datetime.UTC).isoformat(),"status":"PASS_THREE_COMPLETE_PRIORITY_INVENTORIES_AND_ORIGINAL_FIRST_SEALS","retained_entries":sum(x[3] for x in cases),"inventories":results,"unchanged_first_records":[{"relative_path":n,**pin(A/n)} for n,h in first],"scientific_report_full_read_by_ROOT":True,"no_exhaustive_priority_certificate":True}
(A/"root_priority/PRIORITY_MANIFEST_AUTHENTICATION.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"status":receipt["status"],"entries":receipt["retained_entries"],"first_records":len(first)}))
