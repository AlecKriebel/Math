#!/usr/bin/env python3
"""Read-only closing audit for the already processed claimed_solved PRs.
No source/mathematical file of a skipped PR is opened. No remote writes.
"""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parent
CASES={
810:"pr810_2307042/TRACKER_APPEND_RECEIPT.json",
815:"pr815_30006166/TRACKER_APPEND_RECEIPT.json",
822:"pr822_30001168/TRACKER_APPEND_RECEIPT.json",
826:"pr826_30003060/TRACKER_APPEND_RECEIPT.json",
838:"pr838_10000036/production/GWS_APPEND_RECEIPT.json",
872:"pr872_30006628/production/GWS_APPEND_RECEIPT.json",
880:"pr880_9700026/production/GWS_APPEND_RECEIPT.json",
883:"pr883_9900008/production/GWS_APPEND_RECEIPT.json",
885:"pr885_9700042/GWS_APPEND_RECEIPT.json",
888:"pr888_30005079/GWS_APPEND_RECEIPT.json",
894:"pr894_30005737/GWS_APPEND_RECEIPT.json"}
def need(v,s):
 if not v:raise RuntimeError(s)
def read(p):return json.loads(p.read_bytes())
def pin(b):return {"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def gws(service,action,params):
 r=subprocess.run(["gws","sheets","spreadsheets",*service,action,"--params",json.dumps(params)],capture_output=True)
 need(r.returncode==0,"Workspace read failed")
 return json.loads(r.stdout)
def main():
 need(len(sys.argv)==3,"FINAL_RESCAN_JSON FRESH_OUTPUT required")
 scan=read(Path(sys.argv[1]));outpath=Path(sys.argv[2])
 need(outpath.absolute().is_relative_to(ROOT) and not outpath.exists(),"fresh scoped output")
 need(scan["status"]=="NO_UNPROCESSED_CLAIMED_SOLVED_DRAFTS" and scan["pending_prs_ascending"]==[] and scan["fresh_PR_metadata_count"]==101,"final complete metadata gate")
 original=(ROOT/"eligibility_inventory.json").read_bytes()
 need(hashlib.sha256(original).hexdigest()=="3c50ddb1b333d0b6865681acb64cee79c7b75cace7ef9c8c3b30a287ef9d3609","baseline")
 inventory={e["number"]:e for e in json.loads(original)["entries"]};states={e["pr"]:e for e in scan["entries"]}
 state=read(ROOT/"CURRENT_STATE.json");need(set(state["published_dois"])=={str(n) for n in CASES},"all11 published DOI identities")
 need(set(state["completed_prs"])==set(CASES)|{833} and state["closed_without_merge_prs"]==[833],"all12 eligible dispositions")
 env=os.environ.copy();n=int(env.get("GIT_CONFIG_COUNT","0"));env.update({"GIT_CONFIG_COUNT":str(n+1),"GIT_CONFIG_KEY_"+str(n):"gc.auto","GIT_CONFIG_VALUE_"+str(n):"0"})
 def git(*a):return subprocess.check_output(["git",*a],cwd=ROOT.parent,env=env)
 git("fetch","--no-write-fetch-head","--no-tags","origin","main")
 tip=git("rev-parse","origin/main").decode().strip();queue=git("show",tip+":unsolved_math_prioritization/QUEUE.md")
 sheet="1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20";gid=1254632077
 meta=gws([],"get",{"spreadsheetId":sheet,"fields":"spreadsheetId,sheets(properties(sheetId,title))"})
 need([s["properties"]["title"] for s in meta["sheets"] if s["properties"]["sheetId"]==gid]==["Math Puzzles"],"exact tracker tab")
 values=gws(["values"],"get",{"spreadsheetId":sheet,"range":"'Math Puzzles'!A:D"}).get("values",[])
 need(values and values[0][:4]==["Original Problem","Solution Chat URL","DOI","Notes"],"tracker header")
 rows=[]
 for pr,path in CASES.items():
  original=inventory[pr];need(original["eligible"] and original["head_queue_status"]=="claimed_solved","original exact eligibility")
  need(states[pr]["state"]=="MERGED" and states[pr]["mergeCommit"]["oid"],"merged disposition")
  r=read(ROOT/"audits"/path);wanted=r["intended_row"];doi=state["published_dois"][str(pr)]
  need(wanted[2]==doi and r["final_doi_count"]==1 and r["exact_range_read_back_confirmed"] and r["exact_read_back_row"]==wanted,"saved exact tracker receipt")
  found=[(i+1,(v+[""]*4)[:4]) for i,v in enumerate(values) if len(v)>=3 and str(v[2]).strip().removeprefix("https://doi.org/")==doi.removeprefix("https://doi.org/")]
  need(len(found)==1 and found[0][1]==wanted,"fresh exact unique DOI row "+str(pr))
  pid=original["problem_id"];matches=[]
  for line in queue.decode().splitlines():
   cells=[c.strip() for c in line.split("|")]
   if len(cells)>=13 and cells[2].split(" / ")[0]==pid:matches.append((line,cells))
  need(len(matches)==1,"unique main QUEUE row")
  line,cells=matches[0];effort=original["head_queue_row"].split("|")[9].strip()
  need(cells[8]=="claimed_solved" and cells[9]==effort and doi in cells[12],"published main QUEUE status, effort and DOI")
  subprocess.run(["git","merge-base","--is-ancestor",states[pr]["mergeCommit"]["oid"],tip],cwd=ROOT.parent,env=env,check=True)
  rows.append({"pr":pr,"problem_id":pid,"doi_url":doi,"merge_commit":states[pr]["mergeCommit"]["oid"],"original_effort_preserved":effort,"tracker_exact_unique_range":"'Math Puzzles'!A"+str(found[0][0])+":D"+str(found[0][0]),"tracker_receipt":{"path":"audits/"+path,**pin((ROOT/"audits"/path).read_bytes())},"main_queue_row":line})
 need(states[833]["state"]=="CLOSED" and states[833]["mergeCommit"] is None,"rejected PR833 closed unmerged")
 result={"timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"PASS_ALL_PROCESSED_DISPOSITIONS_AND_FRESH_TRACKER_MAIN_RECONCILIATION","completion_estimate_percent":100,"range":[800,900],"main_tip_observed":tip,"metadata_only_final_rescan":pin(Path(sys.argv[1]).read_bytes()),"published":rows,"merged_and_published":len(rows),"closed_without_merge":[833],"initial_non_claimed_statuses_skipped":89,"all_other_PRs_metadata_only":True,"pending_claimed_solved_drafts":[],"original_efforts_preserved":True,"scope":"Fresh metadata-only complete101 PR gate, current main QUEUE/merge ancestry and live exact unique own11 tracker rows; earlier mathematical/publication acceptance receipts retained. No skipped-source audit, re-review or remote mutation; no claim that every contribution is a novel first solution."}
 with outpath.open("x") as f:json.dump(result,f,indent=2,sort_keys=True);f.write("\n");f.flush();os.fsync(f.fileno())
 print(json.dumps({"status":result["status"],"merged_and_published":len(rows),"closed_without_merge":[833],"all11_tracker_DOIs_exact_unique":True,"pending_claimed_solved_drafts":[]}))
if __name__=="__main__":main()
