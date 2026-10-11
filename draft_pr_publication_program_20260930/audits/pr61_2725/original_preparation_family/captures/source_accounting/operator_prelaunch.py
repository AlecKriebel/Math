"""Owned PR61 source/accounting checks. Read-only native and remote access; no author-code replay."""
import datetime,hashlib,json,os,pathlib,sqlite3,subprocess
ROOT=pathlib.Path(__file__).resolve().parent
NATIVE=pathlib.Path("/Users/alec/Documents/Math")
HEAD="b5a4829365f2a0bd5f42b7653c5cfacfa6b01d85"
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open("xb") as f:f.write(b)
def js(p,x):save(p,(json.dumps(x,indent=2,sort_keys=True)+"\n").encode())
def run(name,argv):
 cap=ROOT/"captures"/"source_accounting"/name;cap.mkdir(parents=True,exist_ok=False)
 st=utc();p=subprocess.Popen(argv,cwd=str(NATIVE),stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 out,err=p.communicate();end=utc()
 save(cap/"stdout.bin",out);save(cap/"stderr.bin",err)
 js(cap/"CAPTURE.json",{"actual_execution":True,"controller_pid":os.getpid(),"pid":p.pid,"argv":argv,"cwd":str(NATIVE),"started_utc":st,"finished_utc":end,"exit_code":p.returncode,"stdout":{"bytes":len(out),"sha256":sha(out)},"stderr":{"bytes":len(err),"sha256":sha(err)},"operator_sha256":sha(pathlib.Path(__file__).read_bytes()),"read_only":True,"ROOT_helper":False})
 if p.returncode:raise RuntimeError(name)
 return out
def api(name,path,jq=None):
 a=["/opt/homebrew/bin/gh","api",path]
 if jq:a+=["--jq",jq]
 return json.loads(run(name,a))
def bind(p):
 b=p.read_bytes()
 return {"path":str(p),"bytes":len(b),"sha256":sha(b),"full_mode_07777":format(p.stat().st_mode&0o7777,"04o"),"external_in_place":True,"not_redistributed":True}
start=utc();save(ROOT/"captures"/"source_accounting"/"operator_prelaunch.py",pathlib.Path(__file__).read_bytes())
auth=json.loads((ROOT/"ORIGINAL_AUTHENTICATION.json").read_text())
tree=json.loads((ROOT/"captures"/"retrieval"/"git_commit"/"stdout.bin").read_text())["tree"]["sha"]
for level in ["unsolved_math_prioritization","attempts","2725"]:
 row=api("tree_path_"+level,"repos/AlecKriebel/Math/git/trees/"+tree,'.tree[]|select(.path=="'+level+'")')
 assert row["type"]=="tree";tree=row["sha"]
attempt=api("tree_scientific","repos/AlecKriebel/Math/git/trees/"+tree)
modepins=[]
def files(rows,prefix):
 for x in rows:
  if x["type"]=="blob":modepins.append({"repository_path":prefix+x["path"],"git_mode":x["mode"],"git_blob_sha1":x["sha"]})
files(attempt["tree"],"unsolved_math_prioritization/attempts/2725/")
reviewtree=next(x["sha"] for x in attempt["tree"] if x["path"]=="independent_review")
review=api("tree_review","repos/AlecKriebel/Math/git/trees/"+reviewtree)
files(review["tree"],"unsolved_math_prioritization/attempts/2725/independent_review/")
assert len(modepins)==10
by={x["repository_path"]:x for x in auth["scientific_files"]}
for x in modepins:assert x["git_blob_sha1"]==by[x["repository_path"]]["git_blob_sha1"] and x["git_mode"]=="100644"
compare=api("github_compare_base_head","repos/AlecKriebel/Math/compare/c6975ca76f9f667f1250ba403d0e6da2aafe14d0..."+HEAD,"{status,ahead_by,behind_by,total_commits,base_commit:.base_commit.sha,merge_base_commit:.merge_base_commit.sha,commits:[.commits[].sha]}")
branch=run("native_main_observation",["git","branch","--show-current"]).decode().strip();assert branch=="main"
headnative=run("native_head_observation",["git","rev-parse","HEAD"]).decode().strip()
cache=NATIVE/"unsolved_math_prioritization/cache";manifest=json.loads((NATIVE/"unsolved_math_prioritization/manifest.json").read_text())
corpus={}
for name in ["problems.json","research_results.json"]:
 p=cache/name;b=p.read_bytes();assert len(b)==manifest["files"][name]["bytes"] and sha(b)==manifest["files"][name]["sha256"]
 corpus[name]={"path":str(p),"bytes":len(b),"sha256":sha(b),"manifest_match":True,"not_copied":True,"retained_private_ignored_cache":True}
 if name=="problems.json":selected=[r for r in json.loads(b) if r["id"]==2725];assert len(selected)==1;rawproblem=selected[0]
 else:
  reports=json.loads(b);present="KP-1.66" in reports;rawreport=reports.get("KP-1.66")
c=sqlite3.connect((cache/"catalog.sqlite").as_uri()+"?mode=ro",uri=True)
key,payload,report,kind=c.execute("SELECT key,payload,report,typeof(report) FROM records WHERE key=?",("2725",)).fetchone()
revision=c.execute("SELECT revision FROM metadata").fetchone()[0];c.close()
record=json.loads((ROOT/"original"/"source_record.json").read_text())
assert json.loads(payload)==rawproblem==record
assert kind=="text" and report=="{}" and not present and rawreport is None
save(ROOT/"RAW_PRIOR_SQL_TEXT.txt",report.encode())
js(ROOT/"SELECTED_RAW_PRIOR.json",rawreport)
nativequeue=NATIVE/"unsolved_math_prioritization/QUEUE.md";q=nativequeue.read_text()
qlines=[{"line":i+1,"text":line} for i,line in enumerate(q.splitlines()) if "| 2725 /" in line];assert len(qlines)==1
state=json.loads((NATIVE/"unsolved_math_prioritization/state.json").read_text())
related=json.loads((NATIVE/"unsolved_math_prioritization/review_v2/related_target_groups.json").read_text())
def exact_contains(value):
 if isinstance(value,dict):return any(k=="2725" or exact_contains(v) for k,v in value.items())
 if isinstance(value,list):return any(exact_contains(v) for v in value)
 return value==2725 or value=="2725"
if isinstance(related,dict):relatedmatches=[{"key":k,"value":v} for k,v in related.items() if k=="2725" or exact_contains(v)]
else:relatedmatches=[v for v in related if exact_contains(v)]
primary=NATIVE/"draft_pr_publication_program_20260930/audits/pr38_2765/primary_scope_family/ignoredtmp/primary_sources"
ppdf=bind(primary/"K3_preliminary_202604.pdf");ptext=bind(primary/"K3_preliminary_202604.pdf.txt")
assert ppdf["sha256"]=="ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f"
lines=(primary/"K3_preliminary_202604.pdf.txt").read_text().splitlines()
assert any("Problem 1.66." in x for x in lines[3290:3330])
js(ROOT/"SOURCE_ACCOUNTING.json",{"schema":"pr61-actual-source-accounting/v1","started_utc":start,"finished_utc":utc(),"operator_pid":os.getpid(),"head":HEAD,"git_scientific_modes":modepins,"github_compare":compare,"native_branch":branch,"native_head":headnative,"native_local_head_object_at_initial_read":"absent; failed object/merge-base access, no fetch","corpus":corpus,"revision":revision,"raw_problem_equals_original_source_record":True,"prior_report":{"upstream_key":"KP-1.66","key_present":present,"upstream_value_type":type(rawreport).__name__,"upstream_value_absent":True,"upstream_flat_report_field_present":False,"upstream_flat_wrapper":"selected upstream key absent; no report field or object","raw_object_keys":None,"classification":None,"SQL_storage_type":kind,"SQL_exact_text_bytes":len(report.encode()),"SQL_exact_text_sha256":sha(report.encode()),"SQL_empty_object_is_missing_report_join_fallback":True,"catalog_path":str(cache/"catalog.sqlite"),"catalog_not_copied":True},"native_queue_selected":qlines,"native_state_key_present":"2725" in state,"native_state_selected":state.get("2725"),"related_group_matches":relatedmatches,"primary_problem":{"url":"https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf","pdf":ppdf,"text":ptext,"question":"Problem 1.66","printed_pages":[63,64],"selected_text_lines_1_based":[3307,3331],"own_model_read_question_and_four_remarks":True,"own_new_download":False,"historical_private_foreign_cache_from_PR38":True,"redistributed_full_primary":False},"new_mathematical_attempts":0,"new_mathematical_review_credit":0,"author_or_historical_checker_run_by_this_preparer":False,"ROOT_helper_run":False})
print(json.dumps({"status":"PASS_SOURCE_ACCOUNTING_ONLY","operator_pid":os.getpid(),"original_scientific_files":10,"raw_prior":"ABSENT_UPSTREAM_SQL_TEXT_EMPTY_OBJECT","source_record_exact_json_match":True,"github_merge_base":compare["merge_base_commit"],"native_branch_observed_main":True,"new_math_credit":0},sort_keys=True))


