"""Read only the target record; authenticate cached upstream files without syncing."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sqlite3
A=Path(__file__).resolve().parent;R=A.parents[2];Q=R/'unsolved_math_prioritization'
D=A/'root_imported_record_private';D.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest=json.loads((Q/'manifest.json').read_text());cachepins={}
for name,expected in manifest['files'].items():
    path=Q/'cache'/name;h=hashlib.sha256()
    with path.open('rb') as f:
        while True:
            b=f.read(1048576)
            if not b:break
            h.update(b)
    actual={'bytes':path.stat().st_size,'sha256':h.hexdigest()}
    assert actual==expected,(name,actual,expected)
    cachepins[name]=actual
c=sqlite3.connect((Q/'cache/catalog.sqlite').resolve().as_uri()+'?mode=ro',uri=True)
assert c.execute('SELECT revision FROM metadata').fetchone()[0]==manifest['revision']
row=c.execute('SELECT payload,report FROM records WHERE key=?',('5100034',)).fetchone();c.close();assert row
sqlite_inputs=[json.loads(x) for x in row]
problem_matches=[x for x in json.loads((Q/'cache/problems.json').read_text()) if str(x.get('id'))=='5100034']
assert len(problem_matches)==1 and problem_matches[0]==sqlite_inputs[0]
research=json.loads((Q/'cache/research_results.json').read_text())
assert research['AMR-050-0034']==sqlite_inputs[1]
declared={x['path']:x for x in json.loads((A/'snapshot/problems/5100034_focal_pedal_equality/SOURCE_HASHES.json').read_text())['reference_inputs_local_only']}
pins={}
for name,obj in zip(['source_record.json','upstream_research.json'],sqlite_inputs):
    b=(json.dumps(obj,indent=2)+'\n').encode();actual={'bytes':len(b),'sha256':sha(b)}
    assert actual=={k:declared[name][k] for k in ['bytes','sha256']}
    p=D/name;p.write_bytes(b);p.chmod(0o444);pins[name]={**actual,'mode':'0444'}
statement=sqlite_inputs[0]['statement'];assert 'constant as $P$ varies' in statement
assert sha(statement.encode())=='0fdec77aa82108e5b4471f6a29e2d8f0d34c8cae4d9636a855ee24b2109c4083'
j={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_TARGET_IMPORTED_RECORD_EXACT_HASH_AND_CACHED_REVISION_CHAIN',
   'problem_id':5100034,'dataset':manifest['dataset'],'recorded_revision':manifest['revision'],
   'cache_full_file_pins_verified':cachepins,'target_raw_files':pins,
   'statement_hash':sha(statement.encode()),'explicit_phase_constancy_present':True,
   'qualification':'The imported constancy wording is authenticated and mathematically false. The primary papers also strongly imply it. The displayed equality E is a separate true statement; source framing must retain both outcomes.',
   'upstream_research_is_historical_claim_not_current_priority_evidence':True,
   'no_source_cache_sqlite_or_shared_tracked_index_ref_write':True}
(A/'ROOT_IMPORTED_RECORD_AUTHENTICATION.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j,indent=2))
