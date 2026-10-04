"""Owned PR60 source/accounting checks. Read-only native and remote access; no author-code replay."""
import datetime,hashlib,json,os,pathlib,sqlite3,subprocess
ROOT=pathlib.Path(__file__).resolve().parent
NATIVE=pathlib.Path("/Users/alec/Documents/Math")
HEAD="1e762651b698c1fb519901bd924c5bd3717cc5ef"
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
tree=json.loads((ROOT/"captures"/"retry_v2"/"git_commit"/"stdout.bin").read_text())["tree"]["sha"]
for level in ["unsolved_math_prioritization","attempts","10300054"]:
 row=api("tree_path_"+level,"repos/AlecKriebel/Math/git/trees/"+tree,'.tree[]|select(.path=="'+level+'")')
 assert row["type"]=="tree";tree=row["sha"]
attempt=api("tree_scientific","repos/AlecKriebel/Math/git/trees/"+tree)
modepins=[]
def files(rows,prefix):
 for x in rows:
  if x["type"]=="blob":modepins.append({"repository_path":prefix+x["path"],"git_mode":x["mode"],"git_blob_sha1":x["sha"]})
files(attempt["tree"],"unsolved_math_prioritization/attempts/10300054/")
reviewtree=next(x["sha"] for x in attempt["tree"] if x["path"]=="independent_review")
review=api("tree_review","repos/AlecKriebel/Math/git/trees/"+reviewtree)
files(review["tree"],"unsolved_math_prioritization/attempts/10300054/independent_review/")
replaytree=next(x["sha"] for x in review["tree"] if x["path"]=="author_replay")
replay=api("tree_author_replay","repos/AlecKriebel/Math/git/trees/"+replaytree)
files(replay["tree"],"unsolved_math_prioritization/attempts/10300054/independent_review/author_replay/")
assert len(modepins)==17
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
 if name=="problems.json":selected=[r for r in json.loads(b) if r["id"]==10300054];assert len(selected)==1;rawproblem=selected[0]
 else:
  reports=json.loads(b);present="AMR-102-0054" in reports;rawreport=reports.get("AMR-102-0054")
c=sqlite3.connect((cache/"catalog.sqlite").as_uri()+"?mode=ro",uri=True)
key,payload,report,kind=c.execute("SELECT key,payload,report,typeof(report) FROM records WHERE key=?",("10300054",)).fetchone()
revision=c.execute("SELECT revision FROM metadata").fetchone()[0];c.close()
record=json.loads((ROOT/"original"/"source_record.json").read_text())
assert json.loads(payload)==rawproblem==record
assert kind=="text" and json.loads(report)==rawreport and present and isinstance(rawreport,dict) and rawreport
save(ROOT/"RAW_PRIOR_SQL_TEXT.txt",report.encode())
js(ROOT/"SELECTED_RAW_PRIOR.json",rawreport)
nativequeue=NATIVE/"unsolved_math_prioritization/QUEUE.md";q=nativequeue.read_text()
qlines=[{"line":i+1,"text":line} for i,line in enumerate(q.splitlines()) if "| 10300054 /" in line];assert len(qlines)==1
state=json.loads((NATIVE/"unsolved_math_prioritization/state.json").read_text())
related=json.loads((NATIVE/"unsolved_math_prioritization/review_v2/related_target_groups.json").read_text())
if isinstance(related,dict):relatedmatches=[{"key":k,"value":v} for k,v in related.items() if "10300054" in json.dumps(v)]
else:relatedmatches=[v for v in related if "10300054" in json.dumps(v)]
dups=[{"file":n,"equal_to_author":(ROOT/"original"/n).read_bytes()==(ROOT/"original"/"independent_review"/"author_replay"/n).read_bytes()} for n in ["OBSTRUCTION.md","verify.py","verification.json"]]
assert all(x["equal_to_author"] for x in dups)
primary=NATIVE/"draft_pr_publication_program_20260930/audits/pr56_10300016/private_primary_reading_cache/geometric_splitting_adversary_family/sources"
ppdf=bind(primary/"calegari_2002.pdf");ptext=bind(primary/"calegari_2002.txt")
assert ppdf["sha256"]=="dd77919a55a546000be384974a5c771a7de4f88a36b37fc25294045355fb651e"
lines=(primary/"calegari_2002.txt").read_text().splitlines()
assert lines[1379].startswith("Question 13.1.")
js(ROOT/"SOURCE_ACCOUNTING.json",{"schema":"pr60-actual-source-accounting/v1","started_utc":start,"finished_utc":utc(),"operator_pid":os.getpid(),"head":HEAD,"git_scientific_modes":modepins,"github_compare":compare,"native_branch":branch,"native_head":headnative,"native_local_head_object_at_initial_read":"absent; failed object/merge-base access, no fetch","corpus":corpus,"revision":revision,"raw_problem_equals_original_source_record":True,"prior_report":{"upstream_key":"AMR-102-0054","key_present":present,"upstream_value_type":type(rawreport).__name__,"upstream_object_empty":False,"upstream_flat_wrapper":"no report wrapper; direct report object","raw_object_keys":sorted(rawreport),"classification":rawreport["classification"],"SQL_storage_type":kind,"SQL_exact_text_bytes":len(report.encode()),"SQL_exact_text_sha256":sha(report.encode()),"SQL_decoded_equals_raw_upstream":True,"catalog_path":str(cache/"catalog.sqlite"),"catalog_not_copied":True},"native_queue_selected":qlines,"native_state_key_present":"10300054" in state,"native_state_selected":state.get("10300054"),"related_group_matches":relatedmatches,"original_duplicate_replay_files":dups,"primary_problem":{"url":"https://arxiv.org/abs/math/0209081","pdf":ppdf,"text":ptext,"question":"13.1","printed_pdf_page":29,"selected_text_lines_1_based":[1377,1413],"own_model_read_question_and_four_remarks":True,"own_new_download":False,"historical_cache_from_prior_PR56_work":True,"redistributed_full_primary":False},"new_mathematical_attempts":0,"new_mathematical_review_credit":0,"author_or_historical_checker_run_by_this_preparer":False,"ROOT_helper_run":False})
print(json.dumps({"status":"PASS_SOURCE_ACCOUNTING_ONLY","operator_pid":os.getpid(),"original_scientific_files":17,"raw_prior":"PRESENT_SQL_TEXT_OPEN_TRIAGE","source_record_exact_json_match":True,"github_merge_base":compare["merge_base_commit"],"native_unchanged_main":True,"new_math_credit":0},sort_keys=True))

