from pathlib import Path
import subprocess,os,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr788_30001522/tmp";env=dict(os.environ,GOOGLE_WORKSPACE_CLI_CONFIG_DIR=str(T/"gws-config-private"))
r=subprocess.run([sys.executable,"-B",str(D/"record_preprint_sheet.py"),str(T),"30001522","788","10.5281/zenodo.23422039"],cwd=R,env=env,capture_output=True,text=True)
(T/"root-receipts/GWS_APPEND_STDOUT.txt").write_text(r.stdout);(T/"root-receipts/GWS_APPEND_STDERR.txt").write_text(r.stderr)
if r.returncode:raise RuntimeError(r.stderr or r.stdout)
print(r.stdout)
