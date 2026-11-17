from pathlib import Path
import json,hashlib,stat,datetime
p=Path(__file__).resolve().parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
excluded={"SOURCE_ONLY_MANIFEST.json","SOURCE_ONLY_SEAL.json"}
files=[];dirs=[]
for q in sorted(p.rglob("*")):
 r=str(q.relative_to(p));st=q.lstat()
 if stat.S_ISREG(st.st_mode):
  if r not in excluded:files.append({"path":r,"bytes":st.st_size,"SHA256":hashlib.sha256(q.read_bytes()).hexdigest(),"mode":stat.S_IMODE(st.st_mode)})
 elif stat.S_ISDIR(st.st_mode):dirs.append({"path":r,"mode":stat.S_IMODE(st.st_mode)})
 else:raise RuntimeError("nonregular input: "+r)
m={"schema":"finite-source-only-continuation-manifest-v1","UTC":now,"root":str(p),"root_mode":stat.S_IMODE(p.stat().st_mode),"files":files,"directories":dirs,"exact_terminal_exclusions":sorted(excluded),"no_future_or_subtree_exclusions":True}
mp=p/"SOURCE_ONLY_MANIFEST.json";mp.write_text(json.dumps(m,indent=2)+"\n")
s={"schema":"source-only-continuation-seal-v1","UTC":now,"manifest":"SOURCE_ONLY_MANIFEST.json","manifest_bytes":mp.stat().st_size,"manifest_SHA256":hashlib.sha256(mp.read_bytes()).hexdigest(),"manifested_files":len(files),"manifested_directories":len(dirs),"stage":"before reopening earlier opinions, supporting proofs/code and imported primary evidence","informed_continuation":True,"completion_estimate_percent":35,"exact_manifest_exclusions":sorted(excluded),"original_INITIAL_SEAL_SHA256":"df5f4aa31839b17cee7c5fb603759531ae8a5205641eae9e157b97b9ecf6b715","future_changes_require_final_lane_manifest":True}
(p/"SOURCE_ONLY_SEAL.json").write_text(json.dumps(s,indent=2)+"\n")
