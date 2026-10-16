from pathlib import Path
import hashlib,json,subprocess,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr788_30001522/tmp";M=T/"root-receipts"
helper=D/"finalize_native_acceptance_api.py";assert hashlib.sha256(helper.read_bytes()).hexdigest()=="2e96ba8c808e2079a3d111ac3ea63e3dd85d68e3d629b84fdfd77d08ab1b8d25"
assert hashlib.sha256((T/"FINAL_READINESS.json").read_bytes()).hexdigest()=="985a4f9f661a5dd3691f078b0cc39b9883e6a642a8a18992584e7ded92c7b6b6"
assert not(M/"NATIVE_ACCEPTANCE_INTENT.json").exists(),"Prior intent: reconcile remote own acceptance; never blind repeat"
(M/"NATIVE_ACCEPTANCE_INTENT.json").write_text(json.dumps({"pr":788,"problem":"30001522","original_reviewed_head":"3412d5a074c3f3a03f75735a9ccf1755e172204a","readiness_sha256":"985a4f9f661a5dd3691f078b0cc39b9883e6a642a8a18992584e7ded92c7b6b6","readiness_checkpoint":"a27ceea28f92254f65d98e0c89b0ef4695ef7653","only_own7paths":True},indent=2)+"\n")
r=subprocess.run([sys.executable,"-B",str(helper),str(T),"30001522","788","3412d5a074c3f3a03f75735a9ccf1755e172204a"],cwd=R,capture_output=True,text=True)
(M/"NATIVE_ACCEPTANCE_STDOUT.txt").write_text(r.stdout);(M/"NATIVE_ACCEPTANCE_STDERR.txt").write_text(r.stderr)
receipts=[]
for line in r.stdout.splitlines():
 try:value=json.loads(line)
 except ValueError:continue
 if value.get("result")=="PASS"and value.get("pr")==788 and value.get("file_hashes"):receipts.append(value)
if len(receipts)!=1:raise RuntimeError("Native outcome must be reconciled; CLI="+str(r.returncode)+" "+r.stderr[-1000:])
receipt=receipts[0];(M/"NATIVE_ACCEPTANCE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
if r.returncode:raise RuntimeError("Native remote commit confirmed but local helper error; inspect saved receipt "+str(r.stderr[-1000:]))
print(json.dumps({"result":"PASS_NATIVE_PUSHED","commit":receipt["commit"],"parent":receipt["parent"],"doi":receipt["doi"],"paths":len(receipt["paths"])}))
