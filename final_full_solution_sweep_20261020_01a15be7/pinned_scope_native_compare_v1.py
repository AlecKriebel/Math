"""Read-only exact pinned GitHub comparison when fetching full history is wasteful."""
import base64,datetime as dt,gzip,hashlib,json,re,subprocess
from pathlib import Path
from advance_clear_exclusions import parse_row
from sweep_io import atomic_json
ROOT=Path(__file__).resolve().parent
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def api(endpoint):
 p=subprocess.run(["gh","api","--hostname","github.com","repos/AlecKriebel/Math/"+endpoint],capture_output=True,check=True)
 return json.loads(p.stdout)
def complete_patch(file):
 patch=file.get("patch");need(type(patch)is str,"No full text patch")
 add=delete=0;old=new=None
 for line in patch.splitlines():
  if line.startswith("@@"):
   if old is not None:need(old==new==0,"Previous hunk truncated")
   m=re.match(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@",line);need(m is not None,"Malformed hunk")
   old=int(m[2]or"1");new=int(m[4]or"1")
  elif line.startswith("+"):need(old is not None,"No hunk");add+=1;new-=1
  elif line.startswith("-"):need(old is not None,"No hunk");delete+=1;old-=1
  elif line.startswith(" "):need(old is not None,"No hunk");old-=1;new-=1
  elif line=="\\ No newline at end of file":pass
  else:raise RuntimeError("Unexpected patch line")
  if old is not None:need(old>=0 and new>=0,"Hunk overflow")
 need(old==new==0,"Last hunk truncated")
 need(add==file["additions"]and delete==file["deletions"]and add+delete==file["changes"],"Native patch totals differ")
 return patch
def check(n):
 inv=next(x for x in json.loads((ROOT/"rest_inventory.json").read_text())["pull_requests"]if x["number"]==n);e=json.loads((ROOT/f"eligibility/pr{n:04d}.json").read_text())
 base,head=inv["baseRefOid"],inv["headRefOid"];need(e["inventory_head_sha"]==head and e["inventory_base_sha"]==base,"Inventory drift")
 z=api("compare/"+base+"..."+head);need(z["base_commit"]["sha"]==base,"Base drift");need(0<z["total_commits"]<=250 and len(z["commits"])==z["total_commits"]and z["commits"][-1]["sha"]==head,"Head/full commit range not bound")
 fs=z["files"];need(len(fs)<300 and len(fs)==e["file_count"]and len({x["filename"]for x in fs})==len(fs),"File cap/count")
 need({x["filename"]for x in fs}==set(e["changed_paths"]),"Complete paths differ")
 need(all(x["status"]!="renamed"for x in fs),"Rename requires separate investigation")
 rows=[];queues=[]
 for f in fs:
  if f["filename"]in ["QUEUE.md","unsolved_math_prioritization/QUEUE.md"]:
   patch=complete_patch(f)
   rows.extend(v for line in patch.splitlines()if line.startswith("+")and not line.startswith("+++")if(v:=parse_row(line[1:],f["filename"])))
   queues.append({"path":f["filename"],"actual_head_blob":f["sha"],"patch_sha256":hashlib.sha256(patch.encode()).hexdigest(),"full_patch_native_additions_deletions_verified":True})
 key=lambda x:(x["queue_path"],x["problem_id"],x["status"],x["source_line"])
 need(sorted(map(key,rows))==sorted(map(key,e["added_queue_rows"])),"Actual added rows differ")
 for q in queues:
  cached=next(x for x in e["queue_changes"]if x["path"]==q["path"]);need(q["actual_head_blob"]==cached["sha"],"Queue head blob differs")
 raw=json.dumps(z,separators=(",",":"),ensure_ascii=False).encode();capture=ROOT/"raw"/f"pinned_compare_pr{n:04d}.json.gz";need(not capture.exists(),"Preserve old capture");capture.write_bytes(gzip.compress(raw,mtime=0));need(gzip.decompress(capture.read_bytes())==raw,"Capture readback")
 receipt={"timestamp":dt.datetime.now(dt.timezone.utc).isoformat(),"pr":n,"head":head,"base":base,"merge_base":z["merge_base_commit"]["sha"],"comparison":base+"..."+head,"path_count":len(fs),"all_complete_paths_equal":True,"all_added_rows_equal":True,"added_queue_rows":rows,"queue_blobs":queues,"source":"Native exact-commit GitHub compare; <300full-file cap, all <=250commits/head/base bound; complete QUEUE patch hunk/totals verified against native addition/deletion counts","raw_capture":str(capture.relative_to(ROOT)),"raw_decoded_sha256":hashlib.sha256(raw).hexdigest(),"scope":"Pinned structural eligibility only; no livehead, scientific, priority or publication decision","local_Git_reference_index_object_writes":False}
 target=ROOT/f"PR{n:04d}_PINNED_SCOPE_VERIFICATION.json";need(not target.exists(),"Existing pinned receipt preserved");atomic_json(target,receipt);return receipt
