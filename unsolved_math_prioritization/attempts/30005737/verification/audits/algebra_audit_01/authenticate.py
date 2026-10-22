import hashlib,json,subprocess
from pathlib import Path
b=Path("draft_pr_claimed_solved_800_900_20261012/audits/pr894_30005737")
mbytes=(b/"SOURCE_MANIFEST.json").read_bytes();assert hashlib.sha256(mbytes).hexdigest()=="1d677ef16697e1e294f9f86800c10fe3189270cf2d9771a75d7c4e64954c0d1c"
m=json.loads(mbytes); rows=[]
for f in m["files"]:
 d=(b/"source"/f["path"]).read_bytes();blob=subprocess.run(["git","cat-file","blob",f["git_blob"]],capture_output=True)
 row={"path":f["path"],"bytes":len(d),"sha256":hashlib.sha256(d).hexdigest(),"computed_git_blob":hashlib.sha1(b"blob "+str(len(d)).encode()+b"\0"+d).hexdigest(),"git_cat_file_rc":blob.returncode,"git_blob_bytes_equal":blob.stdout==d}
 row["pin_match"]=len(d)==f["bytes"] and row["sha256"]==f["sha256"] and row["computed_git_blob"]==f["git_blob"] and blob.returncode==0 and blob.stdout==d;rows.append(row)
n=(b/"private_native/canonical_pair.json").read_bytes();native={"bytes":len(n),"sha256":hashlib.sha256(n).hexdigest()};native["pin_match"]=len(n)==3524 and native["sha256"]=="b27d5dbb0f92c0ab330bf44891ec4467f7d8c593cef610196cbd82d4cc6d5298"
print(json.dumps({"external_manifest_sha256":hashlib.sha256(mbytes).hexdigest(),"file_count":len(rows),"files":rows,"native":native},indent=2))
assert len(rows)==18 and all(r["pin_match"] for r in rows) and native["pin_match"]
