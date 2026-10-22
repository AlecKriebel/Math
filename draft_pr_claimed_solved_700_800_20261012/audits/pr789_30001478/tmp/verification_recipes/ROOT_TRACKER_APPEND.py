from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";U=T/"publication";M=T/"root-receipts";cfg=T/"gws-config-private"
pub=json.loads((U/"PUBLISH_RECEIPT.json").read_text());assert pub["state"]=="published"and not pub["metadata_normalizations"]
public=json.loads((U/"PUBLIC_VERIFICATION.json").read_text());assert public["result"]=="PASS"and public["doi"]==pub["doi"]
assert json.loads((M/"PREPUBLICATION_TRACKER_PREFLIGHT.json").read_text())["result"]=="PASS_READ_ONLY_PREPUBLICATION_PREFLIGHT"
env=dict(os.environ,GOOGLE_WORKSPACE_CLI_CONFIG_DIR=str(cfg),PATH="/Users/alec/.nvm/versions/node/v22.16.0/bin:"+os.environ.get("PATH",""))
intent=U/"TRACKER_APPEND_INTENT.json"
if not intent.exists():intent.write_text(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"doi":pub["doi"],"one_append_only":"Helper first deduplicates current rows; uncertain outcomes must reconcile by GET before retry."},indent=2)+"\n")
r=subprocess.run([sys.executable,"-B",str(D/"record_preprint_sheet.py"),str(T),"30001478","789",pub["doi"]],cwd=R,env=env,capture_output=True,text=True,timeout=180)
if r.returncode:
 p=cfg/"append-error-private.txt";p.write_text(r.stderr or r.stdout);os.chmod(p,0o600)
 raise RuntimeError("GWS append unconfirmed; reconcile existing target/DOI with read-only GET before another write. Private diagnostic retained.")
(M/"GWS_APPEND_STDOUT.txt").write_text(r.stdout);assert not r.stderr
receipt=json.loads((U/"SHEET_VERIFICATION.json").read_text());assert receipt["result"]=="PASS"and receipt["doi"]==pub["doi"]and receipt["readback"]["values"]==[receipt["intended_values"]]
print(r.stdout.strip())

