"""Strict byte/recursive JSON-type comparisons; selected row transport differences explicit."""
from pathlib import Path
import datetime
import hashlib
import json

F=Path(__file__).resolve().parent


def unique(pairs):
    d={}
    for k,v in pairs:
        assert k not in d, ('duplicate JSON key',k)
        d[k]=v
    return d


def parse(b):return json.loads(b,object_pairs_hook=unique)


def identical(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(identical(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(identical(x,y) for x,y in zip(a,b))
    return a==b


rows=[]
for name,expected in [('author_private_replay','verification.json'),
                      ('historical_independent_private_replay','independent_review/independent_results.json')]:
    c=F/'captures'/name
    complete=parse((c/'COMPLETE.json').read_bytes())
    assert complete['completed'] is True and complete['exit_code']==0
    a=(F/'source_snapshot'/expected).read_bytes();b=(c/'STDOUT.bin').read_bytes()
    assert (c/'STDERR.bin').read_bytes()==b''
    ja,jb=parse(a),parse(b)
    assert a==b and identical(ja,jb)
    rows.append({'capture':name,'expected':expected,'byte_identical':True,
                 'all_keys_values_and_types_identical':True,
                 'duplicate_json_keys_rejected':True,'expected_bytes':len(a),
                 'stdout_bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),
                 'assertions_actual':jb['assertions'],'status_actual':jb['status'],
                 'qualification':'Unchanged historical checker replay, not a new independent diagnostic family'})
selected=[]
for key,filename,cap in [('30000166','source_record.json','selected_catalog_target'),
                         ('30000167','duplicate_source_record.json','selected_catalog_duplicate')]:
    original=parse((F/'source_snapshot'/filename).read_bytes())
    saved=parse((F/'captures'/cap/'STDOUT.bin').read_bytes())
    native=saved['parsed_payload']
    assert type(original['id']) is int and type(native['id']) is int and original['id']==int(key)==native['id']
    assert original.keys()==native.keys()
    diffs=[]
    for k in original:
        if not identical(original[k],native[k]):
            diffs.append({'key':k,'original_type':type(original[k]).__name__,'native_type':type(native[k]).__name__,
                          'original':original[k],'native':native[k]})
    selected.append({'key':key,'keys_identical':True,'literal_values_identical':not diffs,
                      'literal_differences':diffs,'original_prior_report_key_present':'prior_report' in original,
                      'native_prior_report_key_present':'prior_report' in native,
                      'raw_sql_report':saved['raw_row']['report'],
                      'raw_sql_report_sql_null':saved['report_sql_null'],
                      'parsed_sql_report':saved.get('parsed_report'),
                      'original_source_record_sha256':hashlib.sha256((F/'source_snapshot'/filename).read_bytes()).hexdigest()})
turns=parse((F/'source_snapshot'/'turns.json').read_bytes())
assert type(turns) is dict and turns['substantive_proof_attempts']==0 and turns['budget']==5
summary={'schema':'pr51-preparation-replay-and-selected-scope/v1',
         'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'fresh_replays':rows,'selected_source_rows':selected,
         'original_turns_json_top_level_type':'object','original_turns_json_documents':1,
         'original_events_count':len(turns['events']),
         'substantive_proof_attempts_original':0,'budget_original':5,
         'source_verification_response_count_separately_recorded':False,
         'new_proof_attempts':0,'audit_proof_attempts':0,
         'fresh_independent_mathematical_verdict':None,'publication_approved':False}
(F/'REPRODUCTION_AND_SELECTED_SCOPE.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(summary,indent=2,ensure_ascii=False))
