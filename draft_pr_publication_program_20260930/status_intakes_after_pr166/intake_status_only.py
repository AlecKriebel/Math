"""Ordered, metadata-only original-head status intake after actual PR166 completion."""
from pathlib import Path
import importlib.util,json,datetime,hashlib
D=Path(__file__).resolve().parent;P=D.parent
s=importlib.util.spec_from_file_location("safe_primitives",P/"audits/pr156_30005432/prepare_scoped_merge.py")
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
registry=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/claimed_solved_scope_20261003/LIVE_DRAFT_ELIGIBILITY_REGISTRY.json")
original=json.loads(registry.read_text());bypr={r["pr"]:r for r in original["rows"]}
out=[]
for number in range(167,501):
 r=m.api("pulls/"+str(number));dated=bypr.get(number)
 m.require(dated is not None,"No dated eligibility projection; stop without reading math")
 targets=dated["status_projection"]["targets"];m.require(len(targets)==1,"Ambiguous original problem")
 problem=targets[0]["problem_id"];head=dated["headRefOid"]
 m.require(r["head"]["sha"]==head,"Author head changed since dated original intake; inspect metadata before proceeding")
 raw=m.body_at("unsolved_math_prioritization/QUEUE.md",head)
 lines=[x for x in raw.decode().splitlines() if "| "+problem+" /" in x];m.require(len(lines)==1,"Unique original status row required")
 cells=lines[0].split("|");m.require(len(cells)==14,"QUEUE schema changed")
 status=cells[8].strip();effort=cells[9].strip()
 m.require(status==targets[0]["status"],"Literal original status differs from dated projection")
 result=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),PR=number,URL=r["html_url"],title=r["title"],original_head=head,current_head=r["head"]["sha"],problem_id=problem,state=r["state"],draft=r["draft"],created_at=r["created_at"],literal_original_QUEUE_status=status,effort=effort,original_status_row_SHA256=hashlib.sha256(lines[0].encode()).hexdigest(),original_whole_QUEUE_bytes=len(raw),original_whole_QUEUE_SHA256=hashlib.sha256(raw).hexdigest(),eligible=r["state"]=="open" and r["draft"] and status=="claimed_solved",status_only_intake=True,mathematical_contents_read_or_retained=False,mathematical_audit_or_repair_started=False,PR_or_native_files_modified=False)
 m.save(D/("PR"+str(number)+"_STATUS_ONLY.json"),result);out.append(result)
 print(json.dumps({k:result[k] for k in ["PR","problem_id","literal_original_QUEUE_status","effort","original_head","eligible"]}),flush=True)
 if result["eligible"]:break
m.save(D/"INTAKE_SUMMARY.json",dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),after_completed_PR=166,completed_case_MAIN="b5c4c8988d66b83f997aa2ff4d9b43ac58021869",fully_completed_count=33,published_count=18,status_only=True,rows=out,next_eligible=next((r for r in out if r["eligible"]),None),all_nonclaimed_cases_untouched=True,MAIN_writer_authority=False,goal_complete=False,dated_registry_SHA256=hashlib.sha256(registry.read_bytes()).hexdigest()))
(D/"RESEARCH_LOG.md").write_text("# Ordered status-only intake after PR166\n\n"+datetime.datetime.now(datetime.timezone.utc).isoformat()+" — Intake batch100%; programme33/dated99=33.33%,18published. Only PR titles/metadata and original-head QUEUE identifier/status projections inspected; full QUEUE not retained. Originally nonclaimed submissions untouched. Next eligible science not yet started. No MAIN/shared Git/index/ref/checkout writer authority. Goal unfinished.\n")
