#!/usr/bin/env python3
"""Publish only this effort's subtree, preserving the shared checkout/index."""
from pathlib import Path
import datetime,json,subprocess
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent

def git(*args,data=None):
 r=subprocess.run(["git","-c","gc.auto=0",*args],cwd=REPO,input=data,capture_output=True)
 if r.returncode:raise RuntimeError(r.stderr.decode())
 return r.stdout

def main():
 if git("branch","--show-current").strip()!=b"main":raise RuntimeError("Stay on main")
 names=set(git("ls-files","-z","--cached","--others","--exclude-standard","--",ROOT.name).decode().split("\0"))
 names.discard("")
 ignored=subprocess.run(["git","check-ignore","--no-index","-z","--stdin"],cwd=REPO,input=("\0".join(sorted(names))+"\0").encode(),capture_output=True)
 if ignored.returncode not in (0,1):raise RuntimeError(ignored.stderr.decode())
 names-=set(ignored.stdout.decode().split("\0"))
 node={}
 for name in sorted(names):
  if not name:continue
  p=REPO/name
  if not p.exists():continue
  if p.is_symlink() or not p.is_file():raise RuntimeError("Unexpected nonregular file")
  parts=Path(name).parts
  if parts[0]!=ROOT.name or len(parts)<2:raise RuntimeError("Foreign path")
  here=node
  for part in parts[1:-1]:here=here.setdefault(part,{})
  mode="100755" if p.stat().st_mode&0o111 else "100644"
  here[parts[-1]]=(mode,"blob",git("hash-object","-w","--",str(p)).decode().strip())
 def build(tree):
  lines=[]
  for name,item in sorted(tree.items()):
   mode,kind,oid=("040000","tree",build(item)) if isinstance(item,dict) else item
   lines.append(f"{mode} {kind} {oid}\t{name}\0".encode())
  return git("mktree","-z",data=b"".join(lines)).decode().strip()
 own=build(node)
 for attempt in range(1,5):
  base=git("ls-remote","origin","refs/heads/main").split()[0].decode()
  exists=subprocess.run(["git","cat-file","-e",base+"^{commit}"],cwd=REPO,capture_output=True)
  if exists.returncode:git("fetch","--no-auto-maintenance","--no-tags","--no-write-fetch-head","origin",base)
  lines=[s for s in git("ls-tree","-z",base).split(b"\0") if s and s.split(b"\t",1)[1]!=ROOT.name.encode()]
  lines.append(f"040000 tree {own}\t{ROOT.name}".encode())
  tree=git("mktree","-z",data=b"\0".join(lines)+b"\0").decode().strip()
  message=b"Audit actual full-solution claims in draft PRs 1200-1300\n\nCheckpoint exact math, priority, corrected provenance and reviewed publication packages.\n"
  commit=git("commit-tree",tree,"-p",base,data=message).decode().strip()
  changed=git("diff-tree","--no-commit-id","--name-only","-r",commit).decode().splitlines()
  if not changed:print("No changes");return
  if any(not n.startswith(ROOT.name+"/") for n in changed):raise RuntimeError("Foreign changed path")
  r=subprocess.run(["git","-c","gc.auto=0","push","origin",commit+":refs/heads/main"],cwd=REPO,capture_output=True,text=True)
  receipt={"at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"base":base,"commit":commit,"files":len(changed),"changed_files":changed,"push_returncode":r.returncode,"push_stderr":r.stderr,"method":"own subtree; other remote root entries reused verbatim","shared_index_modified":False}
  if r.returncode==0:
   receipt["verified_remote_tip"]=git("ls-remote","origin","refs/heads/main").split()[0].decode()
   print(json.dumps({key:receipt[key] for key in ("at_utc","base","commit","files","verified_remote_tip")},indent=2),flush=True)
   (ROOT/"_local/push_receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
   return
  if "non-fast-forward" not in r.stderr and "fetch first" not in r.stderr:raise RuntimeError(r.stderr)
 raise RuntimeError("Remote main kept advancing; no force push attempted")

if __name__=="__main__":main()
