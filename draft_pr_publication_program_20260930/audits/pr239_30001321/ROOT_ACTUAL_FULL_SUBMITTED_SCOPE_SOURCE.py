from pathlib import Path
import types,json,hashlib,base64,datetime,os,re
A=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr239_30001321");D=A/"root_full_submitted_scope_01";D.mkdir(exist_ok=False)
S=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/ordered_intakes_after_PR218_20261018")/"preparation_01/status_only_intake_after_pr218.py";sb=S.read_bytes()
assert len(sb)==21987 and hashlib.sha256(sb).hexdigest()=="73f714debe6232fab027184a6c72239f93c00bfa295aa01d9daf88bee03a6ae4"
m=types.ModuleType("full239");m.__file__=str(S);exec(compile(sb,str(S),"exec"),m.__dict__)
T=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr218_30006020/native_completion_preparation_01")/"native_trees_readonly.py";tb=T.read_bytes()
assert len(tb)==4719 and hashlib.sha256(tb).hexdigest()=="c71575a580c43fea8d302c978e0b6c340a16474779ffeb4671e77b967cf6e2ce"
n=types.ModuleType("fulltrees239");exec(compile(tb,str(T),"exec"),n.__dict__)
status_path=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/ordered_intakes_after_PR218_20261018")/"root_PR239_status_observation_01/ROOT_CURRENT_QUEUE_STATUS_OBSERVATION_01.json"
status_raw=status_path.read_bytes();assert m.pin(status_raw)=={"bytes":24741,"sha256":"70edb8700788eedd1381955977157e07759cac553670a780769bd2981d79e7c8"}
status=m.decode(status_raw);submitted=status["current_status_custody"]["current_PR_commits_metadata"]
assert len(submitted)==4 and submitted[-1]["sha"]=="7f17eef77c52b2d9b2ec3ad0803c016267fa6496"
assert all(len(c["parents"])==1 for c in submitted)
assert all(b["parents"][0]["sha"]==a["sha"] for a,b in zip(submitted,submitted[1:]))
origin=submitted[0]["parents"][0]["sha"];head=submitted[-1]["sha"];requests=[]
def save(name,b):
 p=D/name;fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
 with os.fdopen(fd,"wb")as f:f.write(b);f.flush();os.fsync(f.fileno())
 return {"path":str(p),**m.pin(b)}
def fetch(method,route):
 assert method=="GET" and len(requests)<80
 assert route=="pulls/239" or re.fullmatch(r"git/(commits|trees|blobs)/[0-9a-f]{40}",route)
 r=m.bounded_get(m.api_argv(239,route));assert r.returncode==0 and not r.stderr
 pin=save("%03d_RAW_PRIVATE.json"%(len(requests)+1),r.stdout);requests.append({"method":"GET","route":route,"raw":pin});return m.decode(r.stdout)
def commit(oid):
 c=fetch("GET","git/commits/"+oid);assert c["sha"]==oid and m.hexid(c["tree"]["sha"]);return c
pr=fetch("GET","pulls/239");assert pr["head"]["sha"]==head and pr["commits"]==4 and pr["state"]=="open" and pr["draft"]is True and pr["merged"]is False
chain=[]
for dated in submitted:
 c=commit(dated["sha"]);assert [p["sha"]for p in c["parents"]]==[dated["parents"][0]["sha"]]
 chain.append({"commit":c["sha"],"root_tree":c["tree"]["sha"],"sole_parent":c["parents"][0]["sha"]})
base=commit(origin);trees=n.NativeTrees(fetch);rt=chain[-1]["root_tree"];bt=base["tree"]["sha"]
leaves,added,deleted=trees.changes(bt,rt)
smraw=(A/"authenticated_sources_01/SOURCE_MATERIALIZATION_MANIFEST.json").read_bytes()
assert m.pin(smraw)=={"bytes":65348,"sha256":"4ddb9e5c9dc2487b9fb5fd8f993e562517b5efe2b4af2c2ae87c1a5c61feefa4"}
files=[e for e in m.decode(smraw)["files"] if e["snapshot"]=="current"]
wanted={e["repository_path"]:("100644" if e["mode"]=="100644" else e["mode"],"blob",e["native_blob"]) for e in files}
assert len(wanted)==32 and leaves==set(wanted)|{"unsolved_math_prioritization/QUEUE.md"} and not deleted
for p,w in wanted.items():
 assert trees.lookup(bt,p)is None and trees.lookup(rt,p)==w
qe=trees.lookup(bt,"unsolved_math_prioritization/QUEUE.md");assert qe[:2]==("100644","blob")
v=fetch("GET","git/blobs/"+qe[2]);assert v["sha"]==qe[2] and v["encoding"]=="base64"
qb=base64.b64decode("".join(v["content"].split()),validate=True);assert len(qb)==v["size"] and m.native("blob",qb)==qe[2]
qa=(A/"authenticated_sources_01/current/unsolved_math_prioritization/QUEUE.md").read_bytes()
def own(raw):
 rows=[r for r in raw.splitlines(keepends=True) if len(r.decode().split("|"))==14 and r.decode().split("|")[2].strip().split(" / ")[0]=="30001321"]
 assert len(rows)==1;return rows[0]
br,ar=own(qb),own(qa);assert qb.replace(br,b"",1)==qa.replace(ar,b"",1)
fresh=fetch("GET","pulls/239");assert fresh["head"]["sha"]==head and all(fresh.get(k)==pr.get(k)for k in ["number","title","state","draft","merged","body","updated_at","commits"])
record={"schema":"pr239-root-complete-four-submitted-commit-native-scope-v1","UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"PR":239,"HEAD":head,"complete_linear_submitted_chain":chain,"first_submitted_commit_sole_parent":origin,"first_parent_root_tree":bt,"head_root_tree":rt,"changed_leaves":sorted(leaves),"added_directories":sorted(added),"deleted_directories":sorted(deleted),"all32attempt_files_are_additions_exactly_authentic_current_blobs":True,"whole_QUEUE_foreign_bytes_preserved_across_all4commits":True,"first_parent_QUEUE":{"native_blob":qe[2],**m.pin(qb)},"first_parent_own_row":br.decode(),"head_own_row":ar.decode(),"original_current_status_source_pin":m.pin(status_raw),"source_materialization_manifest_pin":m.pin(smraw),"fresh_PR_same_HEAD_fields_body":True,"native_immediate_tree_count":len(trees.cache),"requests":requests,"scope":"Complete actual four-commit PR changed scope authenticated against first submitted commit parent; every changed leaf is32own attempt additions or the exact own-row-only QUEUE delta. Git commit identities remain GitHub native metadata observations, not future candidate/CAS admission or mathematical novelty evidence.","operational_authority":False,"published":False,"completed":False}
pin=save("ROOT_COMPLETE_SUBMITTED_SCOPE.json",(json.dumps(record,indent=2,sort_keys=True)+"\n").encode())
print(json.dumps({"chain":chain,"first_parent":origin,"changed_leaf_count":len(leaves),"added_directories":sorted(added),"first_parent_row":br.decode(),"foreign_QUEUE_bytes_exact":True,"receipt":pin},indent=2))

