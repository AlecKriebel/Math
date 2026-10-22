from pathlib import Path
import json,datetime,hashlib,sys,urllib.request,urllib.parse,concurrent.futures,zipfile,stat
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";I=T/"intake";M=T/"root-receipts";M.mkdir(exist_ok=True);sys.path.insert(0,str(D));from graphql_scoped_commit import Remote,get_pr
initial=M/"ROOT_INITIAL_POSITION.md";assert not initial.exists()
initial.write_text("# Independent root target-only position\n\n"+datetime.datetime.now(datetime.timezone.utc).isoformat()+" — Before author/audit exposure.\n\nLiteral six relations vanish under all x_i=t, giving a candidate k[t] quotient with nonzero linear kernel and a projective-point THCR, but source nontrivial/positive-dimensional-image semantics are unresolved. A stronger possible route sets x3=x1=u and x4=x2=v: f1--f4 vanish and f5=f6=beta(u^2-v^2)+vu-uv. For char!=2 the basis a=u+v,b=u-v yields a quantum-plane relation; char2 needs a triangular/Jordan-plane change and independent checking. These are independent target-only algebra deductions to verify a completed candidate, not assumed conclusions or new open-ended proof search. Must prove full kernel, domain, actual THCR for every allowed field and exact source relations/context. No claim of original-source resolution or priority until primary text is read. Case8%; shard83%; original1/5 budget,0additional proofsearchturns.\n")
G=json.loads((I/"ELIGIBILITY_GATE.json").read_text());head=G["pr_metadata"]["headRefOid"];r=Remote(head);paths=json.loads((I/"PR_CHANGED_PATHS.json").read_text())["changed_files"];rows=[]
for x in paths:
 if x["path"]=="unsolved_math_prioritization/QUEUE.md":continue
 e=r.entry(x["path"]);assert e and e["mode"]=="100644"and e["type"]=="blob";rows.append({"path":x["path"],"git_blob":e["sha"],"changeType":x["changeType"]})
def get(row):
 path=row["path"];url="https://raw.githubusercontent.com/AlecKriebel/Math/"+head+"/"+urllib.parse.quote(path,safe="/")
 with urllib.request.urlopen(url,timeout=90)as response:b=response.read()
 assert hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==row["git_blob"]
 dest=I/"original"/path;dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.exists():assert dest.read_bytes()==b
 else:dest.write_bytes(b)
 return {**row,"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=5)as ex:records=list(ex.map(get,rows))
assert get_pr(789)["head"]["sha"]==head
archives=[]
for row in records:
 if not row["path"].endswith(".zip"):continue
 members=[]
 with zipfile.ZipFile(I/"original"/row["path"])as z:
  assert len(z.namelist())==len(set(z.namelist()))and len(z.namelist())<1000
  for e in z.infolist():
   p=Path(e.filename);assert not p.is_absolute()and".. "not in p.parts and".."not in p.parts and not stat.S_ISLNK(e.external_attr>>16)and e.file_size<20000000
   data=z.read(e);members.append({"path":e.filename,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()})
 archives.append({"path":row["path"],"members":members})
selected=json.loads((I/"SELECTED_PUBLIC_RECORD.json").read_text());cat=json.loads((I/"CATALOG_ENTRY.json").read_text());identity={"verified_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"problem":"30001478","pr":789,"reviewed_head":head,"statement_sha256":cat["statement_hash"],"review_hash":cat["review_hash"],"review_hash_formula":"SHA256(json.dumps([complete_problem,complete_prior_report],sort_keys=True))","prior_research":selected["prior_research"],"selected_record_sha256":hashlib.sha256((I/"SELECTED_PUBLIC_RECORD.json").read_bytes()).hexdigest(),"original_files":records,"ZIP_archives":archives,"same_immutable_head_rechecked":True,"full_PR_changed_paths_only_own_attempt_plus_QUEUE":True,"new_substantive_proof_turns":0}
(I/"ROOT_SOURCE_IDENTITY.json").write_text(json.dumps(identity,indent=2)+"\n")
print(json.dumps({"result":"PASS_ORIGINAL_INTAKE","head":head,"original_files":len(records),"bytes":sum(x["bytes"]for x in records),"archives":len(archives),"source_statement_sha256":cat["statement_hash"],"review_hash":cat["review_hash"],"source_identity_sha256":hashlib.sha256((I/"ROOT_SOURCE_IDENTITY.json").read_bytes()).hexdigest()}))
