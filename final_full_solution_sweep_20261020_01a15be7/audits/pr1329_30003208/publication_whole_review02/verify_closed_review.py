"""Read-only externally pinned closure verifier for this independent review."""
from pathlib import Path
import argparse,hashlib,json,stat
def need(ok,m):
 if not ok:raise RuntimeError(m)
def digest(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument("--manifest-sha256",required=True);a=p.parse_args()
 root=Path(__file__).resolve().parent;mf=root/"MANIFEST.json";raw=mf.read_bytes()
 need(digest(raw)==a.manifest_sha256,"external manifest anchor mismatch")
 m=json.loads(raw);members=m["entries"]
 actual={"."}|{x.relative_to(root).as_posix()for x in root.rglob("*")if x!=mf}
 need(actual==set(members),"closed path set changed")
 for n,v in members.items():
  x=root if n=="."else root/n;s=x.lstat()
  need(not stat.S_ISLNK(s.st_mode),"symlink")
  need(stat.S_IMODE(s.st_mode)==v["mode"]and s.st_mtime_ns==v["mtime_ns"],"metadata "+n)
  if v["kind"]=="file":
   b=x.read_bytes();need(stat.S_ISREG(s.st_mode)and len(b)==v["bytes"]and digest(b)==v["sha256"],"file "+n)
  else:need(stat.S_ISDIR(s.st_mode),"directory "+n)
 inputs=json.loads((root/"INPUT_CLOSURE.json").read_bytes());prep=Path(inputs["input"])
 need(digest((prep/"MANIFEST.json").read_bytes())==inputs["manifest_sha256"],"preparation manifest")
 current={x.relative_to(prep).as_posix()for x in prep.rglob("*")if x.is_file()}
 need(current==set(inputs["files"])|{"MANIFEST.json"},"preparation closure")
 for n,v in inputs["files"].items():
  x=prep/n;s=x.lstat();b=x.read_bytes()
  need(stat.S_ISREG(s.st_mode)and not x.is_symlink(),"preparation regularity")
  need(len(b)==v["bytes"]and digest(b)==v["sha256"],"preparation bytes "+n)
  need(stat.S_IMODE(s.st_mode)==v["mode"]and s.st_mtime_ns==v["mtime_ns"],"preparation metadata "+n)
 print(json.dumps({"status":"PASS","review_files":m["file_count"],"review_directories":m["directory_count"],"preparation105members_preserved":True,"readonly":True,"publication_authority":False},sort_keys=True))
if __name__=="__main__":main()

