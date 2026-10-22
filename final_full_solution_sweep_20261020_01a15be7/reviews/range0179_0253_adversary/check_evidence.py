#!/usr/bin/env python3
"""Read-only replay of the retained PR179–253 identity/binding evidence."""
import hashlib
import json
import os
import re
import subprocess
import zipfile
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent
S=H.parent.parent
REPO=S.parent
load=lambda name:json.loads((H/name).read_text())

def require(x,msg):
    if not x:raise RuntimeError(msg)

def row(line,path):
    c=[v.strip() for v in re.split(r"(?<!\\)\|",line.strip().strip("|"))]
    return {"queue_path":path,"source_line":line,"problem_id":c[1].split("/")[0].strip(),"status":c[7]} if len(c)>7 and c[0].isdigit() else None

def normdoi(v):return re.sub(r"^https?://(?:dx\.)?doi\.org/","",str(v).strip(),flags=re.I)

def main():
    ds=load("dispositions_snapshot.json")
    inv={x["number"]:x for x in json.loads((S/"rest_inventory.json").read_text())["pull_requests"] if 179<=x["number"]<=253}
    live={x["number"]:x for x in load("prs_live.json")["data"]}
    inp={x["pr"]:x for x in load("eligibility_inputs_compact.json")}
    binds={x["pr"]:x for x in load("independent_pinned_bindings.json")}
    require([x["pr"] for x in ds]==list(range(179,254)),"exact disposition order")
    require(set(inv)==set(live)==set(inp)==set(binds)==set(range(179,254)),"range completeness")
    require(load("live_inventory_differences.json")==[],"captured live changes")
    qref=load("canonical_queue_receipt.json")
    qb=subprocess.check_output(["git","cat-file","blob",qref["blob_sha"]],cwd=REPO,env=dict(os.environ,GIT_OPTIONAL_LOCKS="0"))
    require(hashlib.sha256(qb).hexdigest()==load("canonical_queue_receipt.json")["sha256"],"main snapshot digest")
    canon=[]
    for ln in qb.decode().splitlines():
        if ln.startswith("|"):
            cells=[v.strip() for v in ln.strip("|").split("|")]
            if len(cells)>7 and re.match(r"^\d+(?:\s*/|$)",cells[1]):canon.append((cells[1].split("/")[0].strip(),cells[1]))
    env=dict(os.environ,GIT_OPTIONAL_LOCKS="0")
    def git(args):
        r=subprocess.run(["git",*args],cwd=REPO,env=env,capture_output=True)
        require(r.returncode==0,"read-only git command failed: "+r.stderr.decode())
        return r.stdout
    statuses=Counter()
    published=set()
    for d in ds:
        n=d["pr"];e=inp[n];b=binds[n]
        require(e["inventory_head_sha"]==inv[n]["headRefOid"]==live[n]["head"]["sha"],f"PR{n} head binding")
        require(inv[n]["body"]==live[n]["body"] and inv[n]["title"]==live[n]["title"] and inv[n]["isDraft"]==live[n]["draft"],f"PR{n} current description binding")
        require(set(e["path_problem_ids"]).issubset(d["problem_ids"]),f"PR{n} disposition identifier")
        raw=git(["diff","--no-ext-diff","--no-renames","--name-only","-z",b["comparison"]])
        paths=raw.decode().rstrip("\0").split("\0") if raw else []
        require(set(paths)==set(e["changed_paths"]) and len(paths)==e["file_count"],f"PR{n} actual diff scope")
        require(hashlib.sha256(raw).hexdigest()==b["path_list_sha256"],f"PR{n} diff digest")
        for q in e["queue_changes"]:
            sha=git(["rev-parse",b["queue_commit"]+":"+q["path"]]).decode().strip()
            require(sha==q["sha"],f"PR{n} QUEUE blob")
            patch=git(["diff","--no-ext-diff","--no-renames","--unified=0",b["comparison"],"--",q["path"]]).decode()
            actual=[row(l[1:],q["path"]) for l in patch.splitlines() if l.startswith("+|")]
            actual=[r for r in actual if r]
            expected=[{k:r[k] for k in ["queue_path","source_line","problem_id","status"]} for r in e["added_queue_rows"] if r["queue_path"]==q["path"]]
            require(actual==expected,f"PR{n} independent own-row semantics")
        own=[r for r in e["added_queue_rows"] if r["problem_id"] in e["path_problem_ids"]]
        require(len(own)==1,f"PR{n} explicit own status")
        require({r["problem_alias"] for r in own}=={a for i,a in canon if i in e["path_problem_ids"]},f"PR{n} canonical alias")
        st=own[0]["status"];statuses[st]+=1
        if st=="claimed_solved":
            require(d["disposition"] in {"skip_entirely_already_published","reconcile_existing_publication_record"},f"PR{n} uncovered full claim")
            published.add(n)
        else:require(st in {"unsolved","already_solved"} and d["disposition"]=="skip_explicit_non_claimed_solved",f"PR{n} exclusion")
        if n==248:
            require(b["queue_commit"]==live[n]["merge_commit_sha"],"PR248 actual merged diff")
            parents=git(["rev-list","--parents","-n","1",b["queue_commit"]]).decode().split()
            require(e["inventory_head_sha"] in parents[1:],"PR248 original head retained")
    require(statuses==Counter({"unsolved":31,"already_solved":23,"claimed_solved":21}),"status totals")
    cover=load("ledger_coverage_checks.json")
    require({c["pr"] for c in cover}==published,"publication coverage set")
    ledger=load("ledger_fresh.json")["data"]["values"]
    files=0;size=0
    for c in cover:
        n=c["pr"];r=load(f"publication_pr{n:04d}/receipt.json");a=load(f"publication_pr{n:04d}/record_fresh.json")
        require(r["api_status"]==200 and r["state"]=="done" and r["submitted"] is True,"published state")
        require(r["semantic_metadata_unchanged"] and r["file_set_unchanged"],"record changed")
        require(r["doi_resolution"]=={"status":200,"final_url":f"https://zenodo.org/records/{r['record']}"},"DOI resolution")
        matches=[i for i,x in enumerate(ledger,1) if len(x)>2 and normdoi(x[2])==c["doi"]]
        require(matches==[c["expected_row"]] and c["same_unique_row"],"unique combined ledger row")
        require(a["doi"]==c["doi"],"DOI identity")
        apifiles={x.get("key",x.get("filename")):x for x in a["files"]}
        require(bool(r["sources"]),"package manuscript source coverage")
        for f in r["files"]:
            q=REPO/f["existing_payload_path"];raw=q.read_bytes()
            require(f["matches_api_and_prior"] and len(raw)==f["size"]==apifiles[f["name"]]["size"],"payload size")
            require(hashlib.sha256(raw).hexdigest()==f["sha256"] and "md5:"+hashlib.md5(raw).hexdigest()==apifiles[f["name"]]["checksum"],"payload digest")
            if f["name"].endswith(".zip"):
                with zipfile.ZipFile(q) as z:
                    require(z.testzip() is None and any(x.endswith(".py") for x in z.namelist()),"ZIP integrity/code; source may be separate TeX")
            files+=1;size+=len(raw)
        for source in r["sources"]:
            name=source.get("archive",source.get("payload"))
            origin=next(x for x in r["files"] if x["name"]==name)
            q=REPO/origin["existing_payload_path"]
            if "archive" in source:
                with zipfile.ZipFile(q) as z: text=z.read(source["member"])
            else: text=q.read_bytes()
            require(hashlib.sha256(text).hexdigest()==source["sha256"],"deposited source binding")
    require(files==57 and size==8514006,"retained payload totals")
    repair=load("pr0248_repair_check.json")
    require(repair["current_row_matches_repair_final_row"] and repair["only_expected_suffix_added"] and repair["old_note_exactly_preserved_as_prefix"] and repair["record_and_row_reused"] and repair["unique_primary_doi_count"]==1,"PR248 repaired record")
    print(json.dumps({"verdict":"PASS_RANGE0179_0253_COVERAGE","PR_count":75,"historical_statuses":dict(statuses),"explicit_exclusions":54,"published_records_covered":21,"previous_row_repairs_verified":1,"cached_payloads_verified":files,"cached_payload_bytes":size,"new_payload_downloads":0,"nonmaterial_provenance_issue":"PR248 retains earlier REST collection labels/pagecount in rebuilt receipt","scope":"Classification and existing-publication identity only; no new proof or priority clearance."},indent=2))

if __name__=="__main__":main()
