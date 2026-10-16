"""PR789 production publication driver. Mutations require the completed exact-package gate.
Uses the repository's unchanged Zenodo tool; keeps private state outside published paths.
"""
from pathlib import Path
import argparse,datetime,hashlib,importlib.util,json,os,subprocess,sys,urllib.request
sys.dont_write_bytecode=True
R=Path("/Users/alec/Documents/Math")
D=R/"draft_pr_claimed_solved_700_800_20261012"
T=D/"audits/pr789_30001478/tmp";P=T/"preprint";U=T/"publication"
def need(ok,message):
    if not ok:raise RuntimeError(message)
def save(path,value):
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n")
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load_tool():
    path=R/"zenodo_deposit_tool/zenodo.py"
    need(hashlib.sha256(path.read_bytes()).hexdigest()=="a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca","Upload-tool bytes changed")
    sys.path.insert(0,str(path.parent))
    spec=importlib.util.spec_from_file_location("pr789_original_zenodo",path)
    z=importlib.util.module_from_spec(spec);spec.loader.exec_module(z)
    z.STATE_DIR=T/"zenodo-state-private"
    z.STATE_DIR.mkdir(mode=0o700,exist_ok=True);os.chmod(z.STATE_DIR,0o700)
    return z
def review_path(relative):
    need(isinstance(relative,str)and relative and"\\"not in relative
         and not relative.startswith("/")and all(p not in("","..",".")for p in relative.split("/")),
         "Unsafe review binding path")
    p=T
    for part in relative.split("/"):
        p=p/part
        need(not p.is_symlink(),"Review binding symlink")
    need(p.is_file()and p.stat().st_nlink==1,"Review binding must be a single regular file")
    return p
def exact_hash(path,pin):
    need(isinstance(pin,str)and len(pin)==64 and all(c in"0123456789abcdef"for c in pin)
         and hashlib.sha256(path.read_bytes()).hexdigest()==pin,"Review artifact digest differs")
def completed_reviews(g,inv):
    need(type(g.get("actual_whole_preprint_rounds"))is int
         and g["actual_whole_preprint_rounds"]>=2
         and g.get("final_current_round_clean")is True,"Strict completed-review gate")
    records=g.get("completed_whole_reviews")
    need(type(records)is list and len(records)==g["actual_whole_preprint_rounds"],"Missing completed-review bindings")
    identities=set()
    for index,row in enumerate(records,1):
        need(type(row)is dict and type(row.get("round"))is int and row["round"]==index
             and row.get("freshly_initialized")is True
             and isinstance(row.get("reviewer"),str)and row["reviewer"].startswith("/root/pr789_whole_preprint_round")
             and row["reviewer"]not in identities,"Distinct fresh completed reviewers required")
        identities.add(row["reviewer"])
        packet=row.get("packet")
        need(isinstance(packet,str)and"/"not in packet and packet.startswith("whole_preprint_round"),
             "Unexpected review packet")
        mf=review_path(packet+"/MANIFEST.json");exact_hash(mf,row["manifest_sha256"])
        checker=row.get("checker_name")
        need(isinstance(checker,str)and"/"not in checker and checker.endswith(".py"),"Unsafe review checker")
        exact_hash(review_path(packet+"/"+checker),row["checker_sha256"])
        entries=json.loads(mf.read_text())["files"]
        entries=entries if isinstance(entries,list)else[dict(path=n,**v)for n,v in entries.items()]
        actual=set()
        for entry in entries:
            name=entry["path"];need(name not in actual and name!="MANIFEST.json","Repeated review entry");actual.add(name)
            p=review_path(packet+"/"+name);exact_hash(p,entry["sha256"]);need(p.stat().st_size==entry["bytes"],"Review size")
        actual_files=set();actual_dirs=set()
        for item in(T/packet).rglob("*"):
            need(not item.is_symlink(),"Review packet symlink")
            relative=item.relative_to(T/packet).as_posix()
            if item.is_dir():actual_dirs.add(relative)
            else:
                need(item.is_file()and item.stat().st_nlink==1,"Nonregular/multiply linked review packet entry")
                actual_files.add(relative)
        expected_dirs={str(parent)for name in actual for parent in Path(name).parents if str(parent)!="."}
        need(actual_files==actual|{"MANIFEST.json"}and actual_dirs==expected_dirs,
             "Review closed inventory differs")
        receipt_path=review_path(row["root_replay_receipt"]);exact_hash(receipt_path,row["root_replay_sha256"])
        receipt=json.loads(receipt_path.read_text())
        need(receipt.get("result")=="PASS"and receipt.get("completed")is True
             and receipt.get("problem")=="30001478"and receipt.get("pr")==789
             and receipt.get("original_scientific_head")=="aa44dec3baf8c1cd179cf8b55f32be95c74ee81a"
             and receipt.get("reviewer")==row["reviewer"]
             and receipt.get("manifest_sha256")==row["manifest_sha256"]
             and receipt.get("checker_sha256")==row["checker_sha256"]
             and receipt.get("source_manifest_sha256")==row["reviewed_source_manifest_sha256"]
             and receipt.get("publication_files")==row["reviewed_publication_files"]
             and type(row.get("actionable_issues"))is int
             and type(receipt.get("review_actionable_issues"))is int
             and receipt["review_actionable_issues"]==row["actionable_issues"]
             and row["actionable_issues"]>=0,"Completed root-review receipt differs")
        if index==len(records):
            need(row["actionable_issues"]==0
                 and row["reviewed_source_manifest_sha256"]==inv["source_manifest_sha256"]
                 and row["reviewed_publication_files"]==inv["files"],"Final review does not clear the current exact package")
    return records

def gate():
    g=json.loads((T/"FINAL_READINESS.json").read_text())
    need(g["result"]=="PASS"and g["pr"]==789 and g["problem"]=="30001478"
         and g["actual_whole_preprint_rounds"]>=2 and g["final_current_round_clean"],
         "Completed independent whole-preprint reviews required")
    inv=json.loads((P/"PACKAGE_INVENTORY.json").read_text())
    completed_reviews(g,inv)
    need(inv["source_manifest_sha256"]==g["source_manifest_sha256"]
         and inv["files"]==g["publication_files"],"Frozen inventory/gate differs")
    for row in inv["files"]:
        b=(P/row["path"]).read_bytes()
        need(len(b)==row["bytes"]and hashlib.sha256(b).hexdigest()==row["sha256"],"Release artifact changed")
    r=subprocess.run([sys.executable,"-I","-B",str(P/"source/verify_source.py"),
         "--expected-manifest-sha256",inv["source_manifest_sha256"],"--pdf",str(P/"output/pdf/paper.pdf")],
         cwd="/",capture_output=True,text=True,timeout=120)
    need(r.returncode==0 and not r.stderr and json.loads(r.stdout)["result"]=="PASS","Closed source changed")
    return g,inv
def fresh_eligibility(g):
    sys.path.insert(0,str(D))
    from graphql_scoped_commit import get_pr,Remote,head_oid
    p=get_pr(789)
    need(p["state"]=="open"and not p["merged"]and p["head"]["sha"]==g["reviewed_head"],"Exact eligible PR changed")
    r=Remote(p["head"]["sha"])
    rows=[s for s in r.read("unsolved_math_prioritization/QUEUE.md").splitlines()
          if s.startswith("| ")and" 30001478 / "in s]
    need(len(rows)==1 and rows[0].split("|")[8].strip()=="claimed_solved","Only claimed_solved PR-head status is eligible")
    main=Remote(head_oid())
    need(main.entry("unsolved_math_prioritization/attempts/30001478/acceptance.json")is None,
         "An acceptance already exists; reconcile before publication")
    rows2=[s for s in main.read("unsolved_math_prioritization/QUEUE.md").splitlines()
           if s.startswith("| ")and" 30001478 / "in s]
    baseline_row='| 827 | 30001478 / OWR-4335-003 | Prime Ideals and Coordinate-Ring Maps of $R(\\alpha,\\beta)$ | 0.0983 | 5.5 | 3 | 2010 | queued | 0/5 |  |  |  |'
    need(len(rows2)==1 and rows2[0]in(baseline_row,rows[0]),
         "Main differs from both the exact original-parent baseline and exact eligible candidate; reconcile rather than overwrite")
    selected=[x for x in json.loads(main.read("unsolved_math_prioritization/catalog.json"))if x["id"]=="30001478"]
    need(len(selected)==1 and selected[0]["statement_hash"]==g["statement_hash"]
         and selected[0]["review_hash"]==g["review_hash"],"Main source identity changed")
    save(U/"FRESH_PRE_STAGE_ELIGIBILITY.json",{"utc":now(),"result":"ELIGIBLE",
        "PR":p,"PR_head_claimed_row":rows[0],"main_premerge_row":rows2[0],
        "note":"Eligibility is the draft candidate's exact PR-head claimed_solved status; main must carry the exact original-parent queued baseline or exact candidate row."})
def fetch(url,method="GET"):
    request=urllib.request.Request(url,headers={"User-Agent":"Math-independent-research/1.0"},method=method)
    with urllib.request.urlopen(request,timeout=90)as response:
        return response.read(),response.status,response.url
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=["check","stage","publish","verify_public"])
    args=parser.parse_args();U.mkdir(exist_ok=True);z=load_tool()
    manifest=P/"zenodo-deposit.json"
    if args.command=="check":
        out=z.run(argparse.Namespace(command="check",manifest=manifest,sandbox=False))
        save(U/"LOCAL_CHECK_RECEIPT.json",{"utc":now(),"read_only":True,"check":out})
        print(json.dumps({"result":"PASS_LOCAL_CHECK","files":out["files"]}));return
    g,inv=gate()
    if args.command=="stage":
        fresh_eligibility(g)
        place,state=z.local_state(manifest.resolve(),"production")
        if state:
            out=z.run(argparse.Namespace(command="inspect",manifest=manifest,sandbox=False,check_doi=False))
        else:
            intent=U/"CREATION_INTENT.json"
            need(not intent.exists(),"Prior creation intent has no saved ID: reconcile account; do not create again")
            save(intent,{"utc":now(),"environment":"production","pr":789,
                 "source_manifest_sha256":inv["source_manifest_sha256"],"one_create_only":True})
            out=z.run(argparse.Namespace(command="stage",manifest=manifest,sandbox=False))
        need(out["state"]=="ready_to_publish","Unexpected state; inspect known record rather than create another")
        save(U/"STAGE_RECEIPT.json",out)
        need(not out["metadata_normalizations"],"Observed metadata normalization requires exact inspection; keep this same record")
        print(json.dumps({"id":out["id"],"state":out["state"],"metadata_normalizations":out["metadata_normalizations"]}));return
    stage=json.loads((U/"STAGE_RECEIPT.json").read_text())
    need(stage["state"]=="ready_to_publish"and not stage["metadata_normalizations"],"Exact metadata stage required")
    if args.command=="publish":
        fresh_eligibility(g)
        intent=U/"PUBLICATION_INTENT.json"
        if intent.exists():
            out=z.run(argparse.Namespace(command="inspect",manifest=manifest,sandbox=False,check_doi=True))
            need(out["state"]=="published","Earlier publish intent unconfirmed; no second POST")
        else:
            save(intent,{"utc":now(),"id":stage["id"],"one_publish_POST_only":True})
            out=z.run(argparse.Namespace(command="publish",manifest=manifest,sandbox=False,confirm_id=stage["id"]))
        need(out["state"]=="published"and out["id"]==stage["id"],"Publication is unconfirmed; inspect known ID")
        save(U/"PUBLISH_RECEIPT.json",out)
        print(json.dumps({"state":out["state"],"id":out["id"],"doi":out["doi"],
              "metadata_normalizations":out["metadata_normalizations"],"doi_resolution":out["doi_resolution"]}));return
    publication=json.loads((U/"PUBLISH_RECEIPT.json").read_text())
    need(publication["state"]=="published"and publication["id"]==stage["id"],"Known publication required")
    inspected=z.run(argparse.Namespace(command="inspect",manifest=manifest,sandbox=False,check_doi=False))
    need(inspected["state"]=="published"and not inspected["metadata_normalizations"],"Exact supplied metadata differs after publication")
    save(U/"INSPECT_AFTER_PUBLISH.json",inspected)
    raw,status,url=fetch("https://zenodo.org/api/records/"+str(publication["id"]))
    record=json.loads(raw);meta=json.loads((P/"zenodo-metadata.json").read_text())["metadata"]
    need(record["id"]==publication["id"]and record["metadata"]["title"]==meta["title"]
         and record["metadata"]["doi"]==publication["doi"],"Public record identity differs")
    need({f["key"]for f in record["files"]}=={f["name"]for f in publication["files"]},"Public file list differs")
    files=[]
    for row in publication["files"]:
        raw,status,url=fetch("https://zenodo.org/records/"+str(publication["id"])+"/files/"+row["name"]+"?download=1")
        need(len(raw)==row["size"]and hashlib.sha256(raw).hexdigest()==row["sha256"],"Public payload differs")
        files.append({"name":row["name"],"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),
                      "status":status,"final_url":url})
    raw,status,url=fetch("https://doi.org/"+publication["doi"],method="HEAD")
    need(status==200,"DOI not yet resolving; do not republish")
    receipt={"utc":now(),"result":"PASS","record_id":publication["id"],"doi":publication["doi"],
       "all_supplied_deposition_metadata_exact_before_and_after_publication":True,
       "public_record_ID_title_DOI_and_filelist_exact":True,"metadata_normalizations":[],
       "public_files":files,"doi_resolution":{"status":status,"final_url":url},
       "one_deposit_and_one_publication":True}
    save(U/"PUBLIC_VERIFICATION.json",receipt)
    print(json.dumps({"result":"PASS","doi":publication["doi"],"public_files":len(files),"DOI_status":status}))
if __name__=="__main__":main()
