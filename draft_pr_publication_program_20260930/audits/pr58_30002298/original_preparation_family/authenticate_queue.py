from capture_command import HERE,run
import hashlib,json
a=json.loads((HERE/"ORIGINAL_AUTHENTICATION.json").read_bytes())
tree=json.loads((HERE/"captures/tree_unsolved_math_prioritization/stdout.bin").read_bytes())
entry=next(x for x in tree["tree"] if x["path"]=="QUEUE.md")
assert entry["type"]=="blob" and entry["sha"]==a["original_queue_destination_blob_sha1"]
argv=["gh","api","repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref="+a["original_head"],"--jq",'.content|@base64d|split("\n")[]|select(contains("30002298 / OWR-12339-004"))']
cap,out,err=run("head_queue_literal",argv)
assert cap["exit_code"]==0
lines=out.decode().splitlines();assert len(lines)==1
proposal=[x[1:] for x in a["original_queue_diff"].splitlines() if x.startswith("+|") and "30002298 / OWR-12339-004" in x]
assert lines==proposal
r={"schema":"pr58-original-selected-queue-authentication/v1","head":a["original_head"],"queue_blob_sha1_in_authenticated_tree":entry["sha"],"same_as_GitHub_changed_file_destination":True,"selected_head_queue_literal":lines[0],"exactly_equal_to_original_full_diff_proposal":True,"actual_capture":"captures/head_queue_literal/CAPTURE.json","whole_head_queue_body_retained":False,"qualification":"The complete tree body is binary-hash authenticated. The head-specific GitHub contents request emits only the selected row; no independent hash of the entire queue blob body is claimed.","root_approval":False,"native_mutation":False}
(HERE/"QUEUE_SOURCE_AUTHENTICATION.json").write_text(json.dumps(r,indent=2)+"\n")
print(json.dumps({"status":"PASS_SELECTED_ORIGINAL_QUEUE_SOURCE_ONLY","actual_GitHub_child_pid":cap["child_pid"],"queue_blob_sha1":entry["sha"]}))
