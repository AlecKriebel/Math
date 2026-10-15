"""Read-only native raw/SQL/accounting observations; no proof attempt."""
import base64,datetime,hashlib,json,os,pathlib,sqlite3,subprocess
r=pathlib.Path(__file__).resolve().parent;N=pathlib.Path("/Users/alec/Documents/Math")
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(n,x):(r/n).write_text(json.dumps(x,sort_keys=True,indent=2)+"\n")
start=datetime.datetime.now(datetime.timezone.utc).isoformat();commands=[]
def git(label,*args,expected=(0,)):
 argv=["git",*args];s=datetime.datetime.now(datetime.timezone.utc).isoformat()
 p=subprocess.Popen(argv,cwd=N,env={**os.environ,"GIT_OPTIONAL_LOCKS":"0"},stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 out,err=p.communicate();commands.append({"label":label,"argv":argv,"pid":p.pid,"started_utc":s,"finished_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"exit_code":p.returncode,"stdout_base64":base64.b64encode(out).decode(),"stderr_base64":base64.b64encode(err).decode()});dump("ACCOUNTING_FULL_GIT_STREAMS.json",commands)
 assert p.returncode in expected;return p.returncode,out.decode().strip()
_,branch=git("branch","branch","--show-current");assert branch=="main"
_,nativehead=git("native_head","rev-parse","HEAD")
exists,_=git("local_original_head_object","cat-file","-e","98cc2821e9376507caf2d2c57414f7c7e7719c1b^{commit}",expected=(0,1,128))
cache=N/"unsolved_math_prioritization/cache";manifest=json.loads((N/"unsolved_math_prioritization/manifest.json").read_bytes());corpus={}
for name in ["problems.json","research_results.json"]:
 p=cache/name;b=p.read_bytes();assert len(b)==manifest["files"][name]["bytes"] and sha(b)==manifest["files"][name]["sha256"]
 corpus[name]={"path":str(p),"bytes":len(b),"sha256":sha(b),"manifest_match":True,"not_copied":True}
 if name=="problems.json":
  rows=[x for x in json.loads(b) if x["id"]==2715];assert len(rows)==1;rawproblem=rows[0]
 else:
  reports=json.loads(b);present="KP-1.56" in reports;rawprior=reports.get("KP-1.56")
conn=sqlite3.connect((cache/"catalog.sqlite").as_uri()+"?mode=ro&immutable=1",uri=True)
key,payload,report,kind=conn.execute("SELECT key,payload,report,typeof(report) FROM records WHERE key=?",("2715",)).fetchone()
revision=conn.execute("SELECT revision FROM metadata").fetchone()[0];conn.close()
record=json.loads((r/"original/source_record.json").read_bytes());assert json.loads(payload)==rawproblem==record
if isinstance(report,str):(r/"RAW_PRIOR_SQL_TEXT.txt").write_bytes(report.encode())
dump("SELECTED_RAW_PRIOR.json",rawprior)
decoded=json.loads(report) if isinstance(report,str) else None
if present:assert decoded==rawprior
state=json.loads((N/"unsolved_math_prioritization/state.json").read_bytes())
queue=(N/"unsolved_math_prioritization/QUEUE.md").read_text();selected=[{"line":i,"text":x} for i,x in enumerate(queue.split("\n"),1) if "| 2715 /" in x];assert len(selected)==1
related=json.loads((N/"unsolved_math_prioritization/review_v2/related_target_groups.json").read_bytes())
def contains(x):
 if isinstance(x,dict):return any(k=="2715" or contains(v) for k,v in x.items())
 if isinstance(x,list):return any(contains(v) for v in x)
 return x in (2715,"2715")
rm=[{"key":k,"value":v} for k,v in related.items() if k=="2715" or contains(v)] if isinstance(related,dict) else [x for x in related if contains(x)]
p=N/"draft_pr_publication_program_20260930/audits/pr38_2765/primary_scope_family/ignoredtmp/primary_sources"
def pin(x):
 b=x.read_bytes();return {"path":str(x),"bytes":len(b),"sha256":sha(b),"full_mode_07777":format(x.stat().st_mode&0o7777,"04o"),"not_copied":True,"private_external_in_place":True}
primary={"pdf":pin(p/"K3_preliminary_202604.pdf"),"text":pin(p/"K3_preliminary_202604.pdf.txt"),"LF_lines_1_based":[2867,2893],"printed_pages":[55,56],"exact_question_and_both_remarks_read_by_preparer":True,"new_download":False,"visual_read_claimed":False}
assert primary["text"]["sha256"]=="3f42d6ebef41f9c4112638f001f16f1bc45e720231b18bc3a8b4f936a51ff790"
turn=json.loads((r/"original/turns.json").read_bytes());assert turn["substantive_proof_attempts"]==1 and turn["budget"]==5 and len(turn["turns"])==1 and turn["turns"][0]["outcome"]=="unsolved"
auth=json.loads((r/"ORIGINAL_AUTHENTICATION.json").read_bytes());assert len(auth["scientific_files"])==17
out={"schema":"pr62-original-source-accounting/v1","actual_operator_pid":os.getpid(),"started_utc":start,"finished_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"head":auth["head"],"native_branch":branch,"native_head":nativehead,"local_original_head_object_present":exists==0,"native_ref_or_index_mutation":False,"corpus":corpus,"manifest_revision":revision,"raw_problem_equals_SQL_payload_equals_original_record":True,"raw_prior":{"key":"KP-1.56","key_present":present,"selected_value_type":type(rawprior).__name__,"selected_value_is_NULL":rawprior is None,"object_keys":list(rawprior) if isinstance(rawprior,dict) else None,"classification":rawprior.get("classification") if isinstance(rawprior,dict) else None,"direct_dict_no_report_wrapper":isinstance(rawprior,dict),"SQL_storage_type":kind,"SQL_literal_is_NULL":report is None,"SQL_exact_text_bytes":len(report.encode()) if isinstance(report,str) else None,"SQL_exact_text_sha256":sha(report.encode()) if isinstance(report,str) else None,"SQL_decoded_matches_raw":decoded==rawprior,"SQL_literal_empty_object":report=="{}"},"native_queue_selected":selected,"native_state_key_present":"2715" in state,"native_state_selected":state.get("2715"),"related_group_matches":rm,"primary_problem":primary,"original_substantive_attempts":1,"budget":5,"new_attempts":0,"audit_increment":0,"ROOT_helper_run":False}
dump("SOURCE_ACCOUNTING.json",out)
print(json.dumps({"status":"PASS_TYPED_RAW_SQL_ACCOUNTING_ONLY","raw_prior_present":present,"raw_value_type":type(rawprior).__name__,"SQL_storage_type":kind,"SQL_text_bytes":out["raw_prior"]["SQL_exact_text_bytes"],"original_budget":"1/5","operator_pid":os.getpid()},sort_keys=True))
