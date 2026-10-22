"""Run only after actual final whole-preprint gate; private auth copy and read-only tracker preflight."""
from pathlib import Path
import datetime,importlib.util,json,os,stat,subprocess
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");M=T/"root-receipts"
assert(T/"FINAL_READINESS.json").exists(),"Required actual completed-review gate is absent; no auth copy/API call"
spec=importlib.util.spec_from_file_location("pr789_approved_publication_driver",T/"publication_driver.py");driver=importlib.util.module_from_spec(spec);spec.loader.exec_module(driver);g,inv=driver.gate()
assert g["actual_whole_preprint_rounds"]>=2 and g["final_current_round_clean"]is True
cfg=T/"gws-config-private";source=T.parent.parent/"pr788_30001522/tmp/gws-config-private"
assert source.is_dir()and not source.is_symlink()
cfg.mkdir(mode=0o700,exist_ok=True)
assert cfg.is_dir()and not cfg.is_symlink()and cfg.stat().st_uid==os.getuid()and stat.S_IMODE(cfg.stat().st_mode)==0o700
for name in["token_cache.json","client_secret.json","credentials.enc"]:
 target=cfg/name
 if target.exists():
  value=target.lstat();assert stat.S_ISREG(value.st_mode)and value.st_uid==os.getuid()and value.st_nlink==1 and stat.S_IMODE(value.st_mode)==0o600
  continue
 p=source/name;before=p.lstat();assert stat.S_ISREG(before.st_mode)and before.st_uid==os.getuid()and before.st_nlink==1
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
 with os.fdopen(fd,"rb")as f:
  value=os.fstat(f.fileno());assert(value.st_dev,value.st_ino)==(before.st_dev,before.st_ino)and value.st_size<10485760;raw=f.read()
 fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 with os.fdopen(fd,"wb")as f:f.write(raw)
 os.chmod(target,0o600)
assert cfg.is_dir()and not cfg.is_symlink()and stat.S_IMODE(cfg.stat().st_mode)==0o700
binary="/Users/alec/.nvm/versions/node/v22.16.0/bin/gws";env=dict(os.environ,GOOGLE_WORKSPACE_CLI_CONFIG_DIR=str(cfg))
def call(args):
 p=subprocess.run([binary]+args,env=env,capture_output=True,text=True,timeout=90)
 if p.returncode:
  err=cfg/"preflight-error-private.txt";err.write_text(p.stderr or p.stdout);os.chmod(err,0o600)
  raise RuntimeError("GWS preflight failed; private diagnostic retained without printing authentication content")
 return json.loads(p.stdout)
# Inspect schema under the private configuration before the methods used.
for method in["sheets.spreadsheets.get","sheets.spreadsheets.values.get","sheets.spreadsheets.values.append"]:
 call(["schema",method])
sheet="1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20"
metadata=call(["sheets","spreadsheets","get","--params",json.dumps({"spreadsheetId":sheet,"fields":"sheets(properties(sheetId,title))"})])
tabs=[s["properties"]for s in metadata["sheets"]if s["properties"]["sheetId"]==1254632077];assert len(tabs)==1 and tabs[0]["title"]=="Math Puzzles"
values=call(["sheets","spreadsheets","values","get","--params",json.dumps({"spreadsheetId":sheet,"range":"'Math Puzzles'!A:D","valueRenderOption":"UNFORMATTED_VALUE"})]).get("values",[])
assert values and values[0]==["Original Problem","Solution Chat URL","DOI","Notes"]
title=json.loads((T/"preprint/zenodo-metadata.json").read_text())["metadata"]["title"];pr="https://github.com/AlecKriebel/Math/pull/789";problem="30001478"
matches=[i+1 for i,row in enumerate(values)if any(str(cell).rstrip("/").endswith("/"+problem)or title in str(cell)or pr in str(cell)for cell in row)]
assert not matches,"Existing target/title/PR tracker entry; reconcile before creating a deposit"
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS_READ_ONLY_PREPUBLICATION_PREFLIGHT","spreadsheetId":sheet,"tab_gid":1254632077,"tab_title":"Math Puzzles","headers":values[0],"target_title_problem_PR_matches":0,"existing_rows_including_header":len(values),"private_override_used":True,"default_auth_config_unmodified":True,"private_auth_values_and_other_tracker_rows_not_logged":True,"absolute_GWS_binary":binary,"append_or_other_write_performed":False,"preflight_actual_source_manifest_sha256":inv["source_manifest_sha256"]}
(M/"PREPUBLICATION_TRACKER_PREFLIGHT.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"result":out["result"],"target_matches":0,"tab_gid":1254632077,"write_performed":False}))
