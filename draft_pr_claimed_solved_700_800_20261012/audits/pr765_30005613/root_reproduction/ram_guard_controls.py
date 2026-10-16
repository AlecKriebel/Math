from pathlib import Path
from unittest.mock import patch
import json,hashlib,copy,sys
p=Path("draft_pr_claimed_solved_700_800_20261012/audits/pr765_30005613/original/unsolved_math_prioritization/attempts/30005613").resolve()
payload={x.relative_to(p).as_posix():x.read_bytes() for x in p.rglob("*") if x.is_file()}
ns={"__file__":str(p/"verify_publication.py"),"__name__":"root_guard_audit"}
exec(compile(payload["verify_publication.py"],ns["__file__"],"exec"),ns)
root=Path("/RAM_PR765")
ns["ROOT"]=root
rows=[]
def run_case(name,mutator,reject):
 data=dict(payload);links=set();special=set()
 mutator(data,links,special)
 directories={""}
 for name0 in data:
  directories.update(str(x) if str(x)!="." else "" for x in Path(name0).parents)
 def rel(x):
  try:return x.relative_to(root).as_posix().replace(".","",1) if x==root else x.relative_to(root).as_posix()
  except ValueError:return None
 def read(x):return data[rel(x)]
 def glob(x,pat):return [root/k for k in sorted((set(data)|directories)-{""})]
 def islink(x):return rel(x) in links
 def isfile(x):return rel(x) in data and rel(x) not in special
 def isdir(x):return rel(x) in directories
 with patch.object(Path,"read_bytes",read),patch.object(Path,"rglob",glob),patch.object(Path,"is_symlink",islink),patch.object(Path,"is_file",isfile),patch.object(Path,"is_dir",isdir):
  try:count=ns["manifest_check"](root,"PUBLICATION_MANIFEST.json");failed=False;error=None
  except (ValueError,KeyError) as exc:failed=True;error=str(exc)
 if failed!=reject:raise RuntimeError(name+": unexpected acceptance/rejection")
 rows.append({"case":name,"expected_rejection":reject,"rejected":failed,"diagnostic":error,"baseline_payload_files":None if failed else count})
def manifest_mutator(change):
 def apply(data,links,special):
  m=json.loads(data["PUBLICATION_MANIFEST.json"]);change(m);data["PUBLICATION_MANIFEST.json"]=json.dumps(m).encode()
 return apply
run_case("unmodified_RAM_baseline",lambda d,l,s:None,False)
run_case("duplicate_manifest",manifest_mutator(lambda m:m["files"].append(m["files"][0])),True)
run_case("unsafe_parent_path",manifest_mutator(lambda m:m["files"][0].update(path="../escape")),True)
run_case("unsafe_absolute_path",manifest_mutator(lambda m:m["files"][0].update(path="/escape")),True)
run_case("changed_proof",lambda d,l,s:d.update({"author/PROOF.md":d["author/PROOF.md"]+b"changed"}),True)
run_case("changed_archive",lambda d,l,s:d.update({"archives/QUASICONICAL_30005613_AUTHOR_SAFE_FREEZE.zip":b"bad"}),True)
run_case("extra_file",lambda d,l,s:d.update({"unexpected.txt":b"extra"}),True)
run_case("missing_file",lambda d,l,s:d.pop("author/verification.json"),True)
run_case("symlink",lambda d,l,s:l.add("author/README.md"),True)
run_case("nonregular_object",lambda d,l,s:s.add("author/README.md"),True)
print(json.dumps({"status":"PASS","python":sys.version,"outer_optimization":sys.flags.optimize,"scope":"Actual immutable verifier manifest_check and inventory functions, tested against an in-memory filesystem adapter. Nine corruptions rejected under -O and PYTHONOPTIMIZE=2; this is not a physical relocated-package replay or analytic proof.","checks":rows,"original_files_not_written":True},indent=2))
