#!/usr/bin/env python3
"""In-place raw source selection; read-only immutable SQLite URI, no imports."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sqlite3
HERE=Path(__file__).resolve().parent;NATIVE=HERE.parents[3]/'unsolved_math_prioritization'
def pin(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        while True:
            b=f.read(1048576)
            if not b:break
            h.update(b)
    return {'path':str(p),'bytes':p.stat().st_size,'sha256':h.hexdigest(),'mode':format(p.stat().st_mode&0o7777,'04o')}
def read(p):return json.loads(p.read_text())
manifest=read(NATIVE/'manifest.json');before={}
for name in ['problems.json','research_results.json']:
    p=NATIVE/'cache'/name;before[name]=pin(p)
    assert all(before[name][k]==manifest['files'][name][k] for k in ['bytes','sha256'])
problems=read(NATIVE/'cache/problems.json');reports=read(NATIVE/'cache/research_results.json')
by_id=[p for p in problems if str(p['id'])=='30003354'];by_code=[p for p in problems if p['problem_number']=='OWR-15208-008']
assert len(by_id)==len(by_code)==1 and by_id==by_code
wrapper=read(HERE/'original/source_record.json');original=wrapper;assert original==by_id[0]
assert read(HERE/'original/provenance.json')['pinned_dataset_revision']==manifest['revision']
key='OWR-15208-008';present=key in reports
dbpath=NATIVE/'cache/catalog.sqlite';db_before=pin(dbpath)
db=sqlite3.connect('file:'+str(dbpath)+'?mode=ro&immutable=1',uri=True)
rows=db.execute('SELECT key,payload,report FROM records WHERE key=?',('30003354',)).fetchall()
revision=db.execute('SELECT revision FROM metadata').fetchall();db.close()
assert len(rows)==1;sql=rows[0];assert json.loads(sql[1])==original
catalog=[r for r in read(NATIVE/'catalog.json') if str(r['id'])=='30003354'];assert len(catalog)==1
state=read(NATIVE/'state.json');state_present='30003354' in state
qlines=[s for s in (NATIVE/'QUEUE.md').read_text().splitlines() if '30003354 / OWR-15208-008' in s];assert len(qlines)==1
assert before=={name:pin(NATIVE/'cache'/name) for name in before} and db_before==pin(dbpath)
auth=read(HERE/'ORIGINAL_AUTHENTICATION.json');original_hunk=auth['original_queue_diff']
proposal=[s for s in original_hunk.splitlines() if s.startswith('+|') and '30003354 / OWR-15208-008' in s];assert len(proposal)==1
cells=[s.strip() for s in proposal[0][1:].split('|')];turn_record=read(HERE/'original/turns.json');turns=turn_record['turns']
out={'schema':'pr57-original-source-accounting/v1','utc':datetime.now(timezone.utc).isoformat(),
 'original_head':auth['original_head'],'manifest':manifest,'raw_corpus_references_before_after_equal':True,'raw_corpus_references':before,
 'problem_count':len(problems),'unique_numeric_and_source_code_matches':1,'original_problem_typed_equal_to_raw_and_SQL':True,
 'raw_report_key_present':present,'raw_report_value_if_present':reports.get(key),
 'raw_report_interpretation':('literal null' if reports.get(key) is None else 'literal value') if present else 'ABSENT; no raw value',
 'SQL_database_reference':db_before,'SQL_revision_rows':revision,
 'SQL_selected_row':{'key':sql[0],'payload_literal':sql[1],'report_literal':sql[2],'report_is_SQL_NULL':sql[2] is None},
 'archived_wrapper_upstream_report_field_present':'upstream_report' in wrapper,
 'archived_wrapper_upstream_report_value':wrapper.get('upstream_report'),
 'archived_separate_prior_report_file_present':(HERE/'original/prior_report.json').exists(),
 'native_catalog_selected':catalog[0],'native_state_key_present':state_present,'native_state_selected_if_present':state.get('30003354'),
 'native_queue_literal':qlines[0],'native_small_body_references':{name:pin(NATIVE/name) for name in ['manifest.json','catalog.json','state.json','QUEUE.md','queue.py']},
 'original_draft_proposed_queue_literal':proposal[0],'original_draft_proposes':{'Status':cells[8],'Turns':cells[9]},
 'original_status_file_present':False,'original_status_literal_from_status_file':None,
 'original_turns_used':turn_record['substantive_proof_attempts'],'original_turn_limit':turn_record['budget'],
 'original_turn_log_entry_count':len(turns),'original_turn_log_entries':turns,
 'generic_original_response_count':'not separately supplied; no count invented','new_response_or_route_increment':False,'native_mutation':False,
 'qualification':'Raw report presence and literal value, SQL NULL/text, and flat original source-record field presence are separate typed observations. No absence is called null and no empty SQL object is promoted to a raw report.'}
(HERE/'SOURCE_ACCOUNTING.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:out[k] for k in ['raw_report_key_present','raw_report_interpretation','original_draft_proposes','original_status_literal','original_turns_used','original_turn_limit','native_queue_literal','native_state_key_present']},indent=2))
