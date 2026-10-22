from pathlib import Path
import hashlib,json,subprocess,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";M=T/"root-receipts"
helper=D/"finalize_native_acceptance_api.py";assert hashlib.sha256(helper.read_bytes()).hexdigest()=="2e96ba8c808e2079a3d111ac3ea63e3dd85d68e3d629b84fdfd77d08ab1b8d25"
freeze=json.loads((M/"NATIVE_GATE_FREEZE.json").read_text());expected_sha=freeze["readiness_sha256"]
assert freeze["result"]=="PASS_NATIVE_READY"and hashlib.sha256((T/"FINAL_READINESS.json").read_bytes()).hexdigest()==expected_sha
g=json.loads((T/"FINAL_READINESS.json").read_text());assert g["native_acceptance_state"]=="READY_FOR_SCOPED_PRESENT_DAY_SEVEN_PATH_MIRROR"and g["reviewed_head"]=="eb9f6de34861610cf7355a630603a0d18a13f39a"
cp=json.loads((M/"MERGE_READINESS_CHECKPOINT_RECEIPT.json").read_text());sys.path.insert(0,str(D));from graphql_scoped_commit import Remote
assert hashlib.sha256(Remote(cp["commit"]).read((T/"FINAL_READINESS.json").relative_to(R).as_posix()).encode()).hexdigest()==expected_sha
assert not(M/"NATIVE_ACCEPTANCE_INTENT.json").exists(),"Prior intent: reconcile remote own acceptance; never blind repeat"
(M/"NATIVE_ACCEPTANCE_INTENT.json").write_text(json.dumps({"pr":789,"problem":"30001478","original_reviewed_head":"aa44dec3baf8c1cd179cf8b55f32be95c74ee81a","approved_administrative_head":"eb9f6de34861610cf7355a630603a0d18a13f39a","readiness_sha256":expected_sha,"readiness_checkpoint":cp["commit"],"only_own7paths":True},indent=2)+"\n")
r=subprocess.run([sys.executable,"-B",str(helper),str(T),"30001478","789","eb9f6de34861610cf7355a630603a0d18a13f39a"],cwd=R,capture_output=True,text=True)
(M/"NATIVE_ACCEPTANCE_STDOUT.txt").write_text(r.stdout);(M/"NATIVE_ACCEPTANCE_STDERR.txt").write_text(r.stderr)
receipts=[]
for line in r.stdout.splitlines():
 try:value=json.loads(line)
 except ValueError:continue
 if value.get("result")=="PASS"and value.get("pr")==789 and value.get("file_hashes"):receipts.append(value)
if len(receipts)!=1:raise RuntimeError("Native outcome must be reconciled; CLI="+str(r.returncode)+" "+r.stderr[-1000:])
receipt=receipts[0];(M/"NATIVE_ACCEPTANCE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
if r.returncode:raise RuntimeError("Native remote commit confirmed but local helper error; inspect saved receipt "+str(r.stderr[-1000:]))
print(json.dumps({"result":"PASS_NATIVE_PUSHED","commit":receipt["commit"],"parent":receipt["parent"],"doi":receipt["doi"],"paths":len(receipt["paths"])}))
