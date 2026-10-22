from pathlib import Path
import datetime,hashlib,importlib.util,json
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");M=T/"root-receipts";U=T/"publication";spec=importlib.util.spec_from_file_location("reconcile789",T/"publication_driver.py");d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d);z=d.load_tool()
place,state=z.local_state((T/"preprint/zenodo-deposit.json").resolve(),"production");assert state["id"]==23423736
client=z.ZenodoClient("production",z.token_for("production"));got=client.get(state["id"]);z.validate_record(got,state["id"]);assert got["submitted"]is False
wanted=json.loads((T/"preprint/zenodo-metadata.json").read_text())["metadata"]
diffs=[{"field":k,"wanted":v,"actual":got["metadata"].get(k)}for k,v in wanted.items()if got["metadata"].get(k)!=v]
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"KNOWN_DRAFT_METADATA_DIFFERENCE_NOT_PUBLISHED","record_id":state["id"],"submitted":False,"creation_POSTs":1,"metadata_differences":diffs,"server_files":[{"name":f.get("filename",f.get("key")),"size":f.get("filesize",f.get("size")),"checksum":f.get("checksum")}for f in got["files"]],"no_new_creation_or_publication_or_metadata_mutation":True}
(U/"KNOWN_DRAFT_METADATA_RECONCILIATION.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n")
print(json.dumps(out,ensure_ascii=False))

