from pathlib import Path
import json,subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp")
assert json.loads((T/"root-receipts/WHOLE_REVIEW_READY_CHECKPOINT_RECEIPT.json").read_text())["commit"]=="e0eca0b865f7e79474c9ce3eb40981a969a1fe33"
assert not(T/"publication/CREATION_INTENT.json").exists()and not(T/"publication/PUBLISH_RECEIPT.json").exists(),"Existing intent/record: inspect before any mutation"
r=subprocess.run([sys.executable,"-B",str(T/"publication_driver.py"),"stage"],cwd=T,capture_output=True,text=True,timeout=300)
(T/"root-receipts/STAGE_CLI_STDOUT.txt").write_text(r.stdout)
(T/"root-receipts/STAGE_CLI_STDERR.txt").write_text(r.stderr)
assert r.returncode==0,(r.stdout,r.stderr)
a=json.loads(r.stdout);assert a["state"]=="ready_to_publish"and a["metadata_normalizations"]==[]
print(json.dumps(a))

