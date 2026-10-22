from pathlib import Path
import json,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");U=T/"publication";M=T/"root-receipts"
stage=json.loads((U/"STAGE_RECEIPT.json").read_text());assert stage["id"]==23423736 and stage["state"]=="ready_to_publish"and not stage["metadata_normalizations"]
assert not(U/"PUBLICATION_INTENT.json").exists()and not(U/"PUBLISH_RECEIPT.json").exists(),"Prior publication intent: GET reconcile before any retry"
r=subprocess.run([sys.executable,"-B",str(T/"publication_driver.py"),"publish"],cwd=T,capture_output=True,text=True,timeout=300)
(M/"PUBLISH_CLI_STDOUT.txt").write_text(r.stdout);(M/"PUBLISH_CLI_STDERR.txt").write_text(r.stderr)
assert r.returncode==0,(r.stdout,r.stderr)
a=json.loads(r.stdout);assert a["state"]=="published"and a["id"]==23423736 and a["doi"]=="10.5281/zenodo.23423736"and a["metadata_normalizations"]==[]
print(json.dumps(a))

