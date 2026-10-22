from pathlib import Path
import datetime,hashlib,json,subprocess,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";M=T/"root-receipts";sys.path.insert(0,str(D));from graphql_scoped_commit import head_oid
pin="ce10be213b614cad6a4de85ea500d8935c17c5f8238cbe8b912d33d06d57276e";p=T/"admin_scope/packet/TRACKER_VERIFY.py";assert hashlib.sha256(p.read_bytes()).hexdigest()==pin
r=subprocess.run([sys.executable,"-I","-B",str(p),"--controls-only"],capture_output=True,text=True,timeout=60);assert r.returncode==0 and not r.stderr,(r.stdout,r.stderr);a=json.loads(r.stdout);assert a["result"]=="PASS_TRACKER_PARSER_CONTROLS_ONLY"and len(a["controls"])==18 and all(x["control_pass"]for x in a["controls"])
(M/"ROOT_TRACKER18_CONTROLS.json").write_text(r.stdout)
p=T/"admin_scope/packet/MERGE_SCOPE.py";assert hashlib.sha256(p.read_bytes()).hexdigest()=="175d1ead75b4de1eafa3b44ce45b86d618074a290f890ab377e72adfc43cdfff"
base=head_oid();r=subprocess.run([sys.executable,"-I","-B",str(p),"--base",base,"--public-github"],capture_output=True,text=True,timeout=180)
assert r.returncode==0 and not r.stderr,(r.stdout,r.stderr);a=json.loads(r.stdout);assert a["result"]=="PASS_SCOPE_DESIGN_AND_CONTROLS"and len(a["controls"])==7
(M/"ROOT_CURRENT_PREMERGE_SCOPE.json").write_text(r.stdout)
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","main_base":base,"merge_scope_controls":7,"tracker_parser_controls":18,"tracker_helper_sha256":pin,"unknown_diagnostics_still_rejected":True,"source_or_remote_mutation":False}
(M/"ROOT_PREMERGE_AND_TRACKER18_CHECKS.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out))

