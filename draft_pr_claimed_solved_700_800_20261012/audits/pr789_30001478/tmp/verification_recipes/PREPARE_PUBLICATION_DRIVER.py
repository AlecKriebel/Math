from pathlib import Path
import datetime,hashlib,json,subprocess,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";M=T/"root-receipts";sys.path.insert(0,str(D))
from graphql_scoped_commit import gql,Remote
head="aa44dec3baf8c1cd179cf8b55f32be95c74ee81a"
meta=gql('query($o:GitObjectID!){repository(owner:"AlecKriebel",name:"Math"){object(oid:$o){... on Commit{oid parents(first:3){nodes{oid}}}}}}',{"o":head})["repository"]["object"]
assert meta["oid"]==head and len(meta["parents"]["nodes"])==1
parent=meta["parents"]["nodes"][0]["oid"];r=Remote(parent);rows=[line for line in r.read("unsolved_math_prioritization/QUEUE.md").splitlines()if line.startswith("| ")and" 30001478 / "in line]
assert len(rows)==1 and rows[0].split("|")[8].strip()=="queued"and rows[0].split("|")[9].strip()=="0/5"
template=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr788_30001522/tmp/publication_driver.py").read_text()
text=template.replace("788","789").replace("30001522","30001478")
old=[line for line in text.splitlines()if line.strip().startswith("baseline_row=")]
assert len(old)==1;text=text.replace(old[0],"    baseline_row="+repr(rows[0]))
target=T/"publication_driver.py";assert not target.exists();target.write_text(text)
(M/"PUBLICATION_DRIVER_PREPARATION.json").write_text(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"original_parent":parent,"original_parent_own_queue_row":rows[0],"driver_sha256":hashlib.sha256(target.read_bytes()).hexdigest(),"template_case":"completed788","mutations_not_run":True,"guard":"Only exact immutable claimed_solved PR head; main must be exact original-parent queued0/5 baseline or exact candidate row; no acceptance; matching statement/fullreview hashes; final current clean whole-review gate >=2 required"},indent=2)+"\n")
p=subprocess.run([sys.executable,"-B",str(target),"check"],capture_output=True,text=True,timeout=120)
assert p.returncode==0,(p.stdout,p.stderr);print(p.stdout)
