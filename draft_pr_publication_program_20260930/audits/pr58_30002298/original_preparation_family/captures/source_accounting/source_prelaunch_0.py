from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sqlite3
HERE=Path(__file__).resolve().parent;NATIVE=HERE.parents[3]/"unsolved_math_prioritization"
def pin(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        while True:
            b=f.read(1048576)
            if not b:break
            h.update(b)
    return {"path":str(p),"bytes":p.stat().st_size,"sha256":h.hexdigest(),"mode":format(p.stat().st_mode&0o7777,"04o")}
def read(p):return json.loads(p.read_bytes())
manifest=read(NATIVE/"manifest.json");before={}
for name in ["problems.json","research_results.json"]:
    p=NATIVE/"cache"/name;before[name]=pin(p)
    assert all(before[name][k]==manifest["files"][name][k] for k in ["bytes","sha256"])
problems=read(NATIVE/"cache/problems.json");reports=read(NATIVE/"cache/research_results.json")
byid=[x for x in problems if str(x["id"])=="30002298"];bycode=[x for x in problems if x["problem_number"]=="OWR-12339-004"]
assert len(byid)==len(bycode)==1 and byid==bycode
wrapper=read(HERE/"original/source_record.json");record=wrapper["record"];assert record==byid[0] and wrapper["revision"]==manifest["revision"]
key="OWR-12339-004";present=key in reports
dbpath=NATIVE/"cache/catalog.sqlite";db_before=pin(dbpath)
db=sqlite3.connect("file:"+str(dbpath)+"?mode=ro&immutable=1",uri=True)
rows=db.execute("SELECT key,payload,report FROM records WHERE key=?",("30002298",)).fetchall()
revision=db.execute("SELECT revision FROM metadata").fetchall();db.close()
assert len(rows)==1 and json.loads(rows[0][1])==record
sql=rows[0]
catalog=[x for x in read(NATIVE/"catalog.json") if str(x["id"])=="30002298"];assert len(catalog)==1
state=read(NATIVE/"state.json");statepresent="30002298" in state
qlines=[x for x in (NATIVE/"QUEUE.md").read_text().splitlines() if "30002298 / OWR-12339-004" in x];assert len(qlines)==1
assert before=={name:pin(NATIVE/"cache"/name) for name in before} and db_before==pin(dbpath)
auth=read(HERE/"ORIGINAL_AUTHENTICATION.json")
proposal=[x for x in auth["original_queue_diff"].splitlines() if x.startswith("+|") and "30002298 / OWR-12339-004" in x];assert len(proposal)==1
cells=[x.strip() for x in proposal[0][1:].split("|")]
ready=read(HERE/"original/readiness.json")
turns=[json.loads(x) for x in (HERE/"original/turns.jsonl").read_text().splitlines() if x.strip()]
groups=read(NATIVE/"review_v2/related_target_groups.json")
out={"schema":"pr58-original-source-accounting/v1","utc":datetime.now(timezone.utc).isoformat(),"original_head":auth["original_head"],
"manifest":manifest,"raw_corpus_references_before_after_equal":True,"raw_corpus_references":before,"problem_count":len(problems),
"unique_numeric_and_source_code_matches":1,"original_record_typed_equal_to_raw_and_SQL":True,
"raw_report_key_present":present,"raw_report_interpretation":"ABSENT; no raw value" if not present else "PRESENT",
"SQL_database_reference":db_before,"SQL_revision_rows":revision,"SQL_selected_row":{"key":sql[0],"payload_literal":sql[1],"report_literal":sql[2],"report_is_SQL_NULL":sql[2] is None},
"archived_wrapper_research_result_for_code_field_present":"research_result_for_code" in wrapper,
"archived_separate_prior_report_file_present":(HERE/"original/prior_report.json").exists(),
"original_status_json_present":(HERE/"original/status.json").exists(),
"native_catalog_selected":catalog[0],"native_state_key_present":statepresent,"native_queue_literal":qlines[0],
"native_small_body_references_at_selection":{name:pin(NATIVE/name) for name in ["manifest.json","catalog.json","state.json","QUEUE.md","queue.py"]},
"original_draft_proposed_queue_literal":proposal[0],"original_draft_proposes":{"Status":cells[8],"Turns":cells[9]},
"original_readiness_status_literal":ready["status"],"original_used_substantive_attempts":ready["used_substantive_attempts"],"original_maximum_substantive_attempts":ready["maximum_substantive_attempts"],
"original_turn_log_entry_count":len(turns),"original_turn_log_entries":turns,"generic_original_response_count_supplied":False,
"new_response_or_route_increment":False,"native_mutation":False,
"source_omission_qualification":"No raw report value is inferred from an absent key. SQL non-NULL TEXT '{}' and serialized wrapper null are separate literal values, not a present raw report. Missing status/prior-report files are absent, not placeholders.",
"native_snapshot_qualification":"Native catalog/state/QUEUE references are dated selection observations, not future acceptance or expected immutable current-native hashes."}
if present:out["raw_report_value"]=reports[key]
if "research_result_for_code" in wrapper:out["archived_wrapper_research_result_for_code_value"]=wrapper["research_result_for_code"]
if statepresent:out["native_state_selected"]=state["30002298"]
(HERE/"SOURCE_ACCOUNTING.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps({k:out[k] for k in ["raw_report_key_present","raw_report_interpretation","original_draft_proposes","original_readiness_status_literal","original_used_substantive_attempts","original_maximum_substantive_attempts","original_turn_log_entry_count","native_queue_literal","native_state_key_present","original_status_json_present"]},indent=2))
