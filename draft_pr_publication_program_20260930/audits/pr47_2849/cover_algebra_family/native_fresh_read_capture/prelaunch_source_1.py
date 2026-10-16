#!/usr/bin/env python3
"""Fresh selected native/cache read only; no cache, SQL body or report body retained."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sqlite3
B=Path(__file__).resolve().parent;R=B.parents[3];C=R/'unsolved_math_prioritization'
def bind(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'full_mode':p.stat().st_mode&0o7777}
paths=[C/'cache/catalog.sqlite',C/'cache/problems.json',C/'cache/research_results.json',C/'catalog.json',C/'state.json',C/'history.jsonl',C/'QUEUE.md']
before=[bind(p) for p in paths]
db=sqlite3.connect((C/'cache/catalog.sqlite').as_uri()+'?mode=ro&immutable=1',uri=True)
rows=db.execute('SELECT payload,report FROM records WHERE key=?',('2849',)).fetchall();db.close();assert len(rows)==1
problem=json.loads(rows[0][0]);prior=json.loads(rows[0][1]);reports=json.loads((C/'cache/research_results.json').read_bytes())
assert problem==json.loads((B.parent/'source_snapshot/source_record.json').read_bytes()) and prior=={}
assert problem['problem_number']=='KP-3.51' and 'KP-3.51' not in reports
literal=(B.parent/'source_snapshot/prior_report.json').read_bytes();assert literal==b'null\n' and json.loads(literal) is None
catalog=json.loads((C/'catalog.json').read_bytes());selected=[x for x in catalog if str(x.get('id'))=='2849'];assert len(selected)==1
state=json.loads((C/'state.json').read_bytes());history=[json.loads(x) for x in (C/'history.jsonl').read_bytes().splitlines() if x.strip()]
hs=[x for x in history if str(x.get('id'))=='2849'];queue=[x for x in (C/'QUEUE.md').read_text().splitlines() if '| 2849 / ' in x]
after=[bind(p) for p in paths];assert before==after
out={'read_utc':datetime.now(timezone.utc).isoformat(),'bindings':before,'read_only_immutable_SQLite':True,'selected_problem_matches_original':True,'selected_payload_literal_sha256':hashlib.sha256(rows[0][0].encode()).hexdigest(),'selected_report_literal_sha256':hashlib.sha256(rows[0][1].encode()).hexdigest(),'selected_report_literal_bytes':len(rows[0][1].encode()),'upstream_report_key':'KP-3.51','upstream_key_presence':'ABSENT','SQLite_absent_fallback_value':{},'original_prior_literal':'null\n','original_prior_value_is_null':True,'original_prior_not_equal_SQLite_default':True,'no_actual_report_present':True,'current_selected_catalog_status':selected[0]['local_status'],'current_selected_catalog_turns':selected[0]['turns_used'],'current_selected_state_present':'2849' in state,'current_selected_history_count':len(hs),'current_selected_queue_rows':queue,'native_inputs_unchanged':True,'foreign_body_or_SQL_or_headers_copied':False,'transition_or_writes':False,'future_mirror_status':'PENDING','not_mathematical_defect':True}
(B/'FRESH_NATIVE_SELECTED_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='bindings'},indent=2))
