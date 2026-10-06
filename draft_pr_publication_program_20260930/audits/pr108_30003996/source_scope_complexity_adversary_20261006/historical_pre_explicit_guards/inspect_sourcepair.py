#!/usr/bin/env python3
"""Read-only selected-target authentication; writes only this audit's folder."""
from pathlib import Path
import datetime,hashlib,json,re,sqlite3
HERE=Path(__file__).resolve().parent
A108=HERE.parent
DATA=Path('/Users/alec/Documents/Math/unsolved_math_prioritization')
CODE='OWR-16633-013'; ID=30003996

def pin(path):
    b=path.read_bytes()
    return {'path':str(path),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def norm_statement(s):
    return re.sub(r'\s+','',s).casefold()

def main():
    auth=json.loads((A108/'original_source_authentication_20261006/SOURCEPAIR_AUTHENTICATION.json').read_text())
    pins=[]
    for expected in auth['input_pins']:
        actual=pin(Path(expected['path']))
        assert all(actual[k]==expected[k] for k in ['path','bytes','sha256']), (expected,actual)
        pins.append(actual)
    raw=json.loads((DATA/'cache/problems.json').read_text())
    selected=[p for p in raw if p.get('id')==ID or p.get('problem_number')==CODE]
    assert len(selected)==1
    selected=selected[0]
    reports=json.loads((DATA/'cache/research_results.json').read_text())
    # Explicit no-join semantics: neither identifier has an imported report.
    assert CODE not in reports and str(ID) not in reports
    raw_report={}
    submitted=json.loads((A108/'original_source_authentication_20261006/original_attempt/source_record.json').read_text())
    con=sqlite3.connect('file:'+str(DATA/'cache/catalog.sqlite')+'?mode=ro&immutable=1',uri=True)
    sql_rows=con.execute('select key,payload,report from records where key=?',(str(ID),)).fetchall()
    assert len(sql_rows)==1
    key,payload,report=sql_rows[0]
    sql_payload=json.loads(payload);sql_report=json.loads(report)
    assert submitted==selected==sql_payload
    assert raw_report==sql_report=={}
    revision=con.execute('select revision from metadata').fetchone()[0]
    assert revision==auth['dataset_revision']
    exact_statement=[{'id':p.get('id'),'problem_number':p.get('problem_number')} for p in raw if norm_statement(p.get('statement',''))==norm_statement(selected['statement'])]
    same_title=[{'id':p.get('id'),'problem_number':p.get('problem_number')} for p in raw if p.get('title')==selected['title']]
    # Narrow source-model filter, not a review of unrelated records or science.
    allroot_candidates=[]
    for p in raw:
        s=' '.join(str(p.get(k,'')) for k in ['title','statement','original_statement','clean_statement']).casefold()
        if 'arborescen' in s and 'root' in s and any(t in s for t in ['spanning tree','span-ning tree','root-dependent']):
            allroot_candidates.append({'id':p.get('id'),'problem_number':p.get('problem_number'),'title':p.get('title')})
    adjacent=next(p for p in raw if p.get('id')==30003997)
    ak,ap,ar=con.execute('select key,payload,report from records where key=?',('30003997',)).fetchone()
    assert json.loads(ap)==adjacent
    native=json.loads((A108/'original_source_authentication_20261006/ORIGINAL_BLOB_MANIFEST.json').read_text())
    missing_effort=[f['relative_path'] for f in native['files'] if re.search(r'(^|/)(status|turns)(\.|/|$)',f['relative_path'],re.I)]
    assert missing_effort==[]
    result={
       'schema':'pr108-source-scope-complexity-sourcepair/v1','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'readonly_sql_uri':str(DATA/'cache/catalog.sqlite')+'?mode=ro&immutable=1','dataset_revision':revision,'input_pins_match_existing_authentication':True,
       'input_pins':pins,'source_record_submitted_equals_raw_equals_sql':True,'selected_count_by_id_or_code':1,
       'raw_imported_report_key_absent':True,'raw_numeric_imported_report_key_absent':True,'normalized_imported_prior_report':{},'normalized_report_equals_sql':True,
       'native_prior_report_file_present':False,'native_absence_not_retroactively_rewritten':True,
       'exact_statement_matches':exact_statement,'same_title_matches':same_title,'narrow_allroot_model_candidates':allroot_candidates,
       'adjacent_record':{'id':adjacent['id'],'problem_number':adjacent['problem_number'],'title':adjacent['title'],'raw_equals_sql':True,'source_model':'fixed root, directed arborescence, destination-specific costs on root-to-destination paths'},
       'duplicate_semantics':'No distinct record found by exact statement, exact title, or narrow all-root source-model filter. The adjacent Problem 2 is a distinct source problem; no equivalence inferred. This is not an exhaustive semantic equivalence search.',
       'original_literal_status':native['literal_status'],'original_author_effort':native['original_author_effort'],'native_status_or_turns_files':missing_effort,
       'effort_evidence':'QUEUE projection and prose author log only; no native structured status/turn ledger exists and none is manufactured.',
       'new_central_proof_search_turns':0,'source_curation_open_is_dated_not_priority_clearance':True,'priority_search_performed':False,
       'scope':'Source verification only; no unrelated PR mathematical or status adjudication.'}
    (HERE/'SOURCEPAIR_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['input_pins']},indent=2))
if __name__=='__main__':main()
