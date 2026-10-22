from pathlib import Path
import sqlite3,hashlib,json,sys,datetime
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";I=T/"intake";sys.path.insert(0,str(D));from graphql_scoped_commit import Remote,gql
G=json.loads((I/"ELIGIBILITY_GATE.json").read_text());head=G["pr_metadata"]["headRefOid"];r=Remote(head);cat=json.loads((I/"CATALOG_ENTRY.json").read_text())
cache=R/"unsolved_math_prioritization/cache/catalog.sqlite";con=sqlite3.connect("file:"+str(cache)+"?mode=ro",uri=True);row=con.execute("SELECT payload,report FROM records WHERE key=?",("30001478",)).fetchone();con.close();assert row
p,prior=map(json.loads,row);statement=hashlib.sha256(p["statement"].encode()).hexdigest();review=hashlib.sha256(json.dumps([p,prior],sort_keys=True).encode()).hexdigest();assert statement==cat["statement_hash"]and review==cat["review_hash"]
selected={"problem":p,"prior_research":prior};(I/"SELECTED_PUBLIC_RECORD.json").write_text(json.dumps(selected,ensure_ascii=False,indent=2)+"\n")
files=[];cursor=None
while True:
 v=gql('query($n:Int!,$c:String){repository(owner:"AlecKriebel",name:"Math"){pullRequest(number:$n){headRefOid changedFiles files(first:100,after:$c){pageInfo{hasNextPage endCursor}nodes{path changeType}}}}}',{'n':789,'c':cursor})['repository']['pullRequest'];assert v["headRefOid"]==head;files+=v["files"]["nodes"]
 if not v["files"]["pageInfo"]["hasNextPage"]:break
 cursor=v["files"]["pageInfo"]["endCursor"]
assert len(files)==len({x["path"]for x in files})==v["changedFiles"]
allowed="unsolved_math_prioritization/attempts/30001478/";assert all(x["path"]=="unsolved_math_prioritization/QUEUE.md"or x["path"].startswith(allowed)for x in files)
assert all(x["changeType"]in["ADDED","MODIFIED"]for x in files)
(I/"PR_CHANGED_PATHS.json").write_text(json.dumps({"head":head,"changed_files":files},indent=2)+"\n")
manifest=json.loads(r.read("unsolved_math_prioritization/manifest.json"));assert manifest==json.loads((R/"unsolved_math_prioritization/manifest.json").read_text());(I/"SOURCE_DATASET_MANIFEST.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps({"problem":p,"prior_research":prior,"statement_hash":statement,"review_hash":review,"head":head,"PR_changed_files":files},ensure_ascii=False,indent=2))
