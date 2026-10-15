"""Inspect literal original objects and source bindings; no submitted helper execution."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import sqlite3
import stat

A=Path(__file__).resolve().parent
R=A.parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(xs):
    d={}
    for k,v in xs:
        assert k not in d,('duplicate key',k)
        d[k]=v
    return d
def parse(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def write(name,b):
    with (A/name).open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def js(name,x):write(name,(json.dumps(x,indent=2,sort_keys=True)+'\n').encode())
def main():
    src=Path(__file__).read_bytes();write('INSPECTION_PRELAUNCH_SOURCE.py',src)
    m=parse((A/'snapshot_manifest.json').read_bytes());texts={};objects={};receipts=[]
    assert len(m['files'])==13
    for row in m['files']:
        p=A/'source_snapshot'/row['relative_path'];b=p.read_bytes()
        assert len(b)==row['bytes'] and sha(b)==row['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
        texts[row['relative_path']]=b.decode()
        if p.suffix=='.json':objects[row['relative_path']]=parse(b)
        receipts.append(dict(path=row['relative_path'],bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode)))
    diff=(A/'original_diff.patch').read_bytes();chunks=diff.split(b'diff --git ')[1:]
    assert len(chunks)==14
    reconstructed=[]
    for c in chunks:
        lines=c.splitlines(keepends=True)
        path=lines[0].decode().strip().split(' b/',1)[1]
        if '/attempts/30004438/' not in path:continue
        rel=path.split('/attempts/30004438/',1)[1]
        assert b'new file mode 100644\n' in lines
        j=next(i for i,v in enumerate(lines) if v.startswith(b'@@ '))
        assert all(v.startswith(b'+') for v in lines[j+1:])
        b=b''.join(v[1:] for v in lines[j+1:]);assert b==(A/'source_snapshot'/rel).read_bytes()
        reconstructed.append(rel)
    assert set(reconstructed)==set(texts)
    author=objects['verification.json'];review=objects['independent_review/independent_results.json']
    for obj,n in [(author,51),(review,848)]:
        assert type(obj['passed']) is int and obj['passed']==n and obj['failed']==0
        assert len(obj['checks'])==n and all(type(v) is str and v=='PASS' for v in obj['checks'].values())
    turns=objects['turns.json'];p=objects['provenance.json'];s=objects['independent_review/review_summary.json']
    assert turns['substantive_turns_used']==0 and turns['source_verification_responses']==1 and turns['turn_limit']==5
    assert p['artifact_sha256']==s['reviewed_artifact_sha256']==sha((A/'source_snapshot/SOURCE_STATUS.md').read_bytes())
    assert p['independent_review']['review_sha256']==s['review_sha256']==sha((A/'source_snapshot/independent_review/REVIEW.md').read_bytes())
    # Open the foreign native cache strictly read-only and export only the selected record.
    cache=R/'unsolved_math_prioritization/cache/catalog.sqlite'
    db=sqlite3.connect(cache.as_uri()+'?mode=ro&immutable=1',uri=True)
    tables=db.execute("SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
    rows=db.execute('SELECT key,payload,report FROM records WHERE key=?',('30004438',)).fetchall()
    revision=db.execute('SELECT revision FROM metadata').fetchall();db.close()
    assert len(rows)==1
    problem=parse(rows[0][1]);prior=parse(rows[0][2])
    assert problem==objects['source_record.json']
    sql=dict(actual_pid=os.getpid(),read_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),sqlite_open_mode='ro&immutable=1',
       foreign_sqlite_body_copied=False,schema_rows=tables,revision_rows=revision,selected_rows_count=len(rows),
       complete_selected_problem=problem,complete_selected_prior_report=prior,
       selected_payload_literal_bytes=len(rows[0][1].encode()),selected_payload_sha256=sha(rows[0][1].encode()),
       selected_report_literal_bytes=len(rows[0][2].encode()),selected_report_sha256=sha(rows[0][2].encode()),
       exact_original_source_record_JSON_match=True,source_truth_or_current_priority_certified=False)
    js('ORIGINAL_SELECTED_NATIVE_SOURCE_READ.json',sql)
    foreignsources=[]
    for row in p['sources']:
        foreignsources.append(dict(original_receipt_fields=row,body_copied=False,body_freshly_read=False,
          hash_and_size_role='Literal original provenance claim, not newly authenticated source body'))
    js('ORIGINAL_FOREIGN_SOURCE_BINDINGS.json',dict(schema='pr46-original-foreign-source-individual-receipt-bindings/v1',
       sources=foreignsources,original_pdf_ocr_pixel_bodies_in_owned_topology=False,
       original_source_receipt_comparison_to_review=[x==y for x,y in zip(p['sources'],s['source_identities'])],
       literal_provenance_sha256=sha((A/'source_snapshot/provenance.json').read_bytes()),
       fresh_foreign_source_read=False,source_claim_validation=False))
    js('ORIGINAL_COMPLETE_READ_RECEIPT.json',dict(schema='pr46-original-complete-byte-and-typed-inspection/v1',
       actual_pid=os.getpid(),created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
       original_files_read_in_full=len(receipts),original_bytes_read=sum(x['bytes'] for x in receipts),
       all_original_file_receipts=receipts,complete_original_JSON_objects=objects,
       original_JSON_object_files=list(objects),original_JSONL_object_files=[],
       full_diff_bytes_read=len(diff),full_diff_sha256=sha(diff),all_13_added_hunks_reconstructed_byte_exact=True,
       complete_author_51_labels_values_structurally_inspected=True,complete_independent_848_labels_values_structurally_inspected=True,
       original_artifact_and_review_hash_references_match=True,helper_execution_performed=False,
       mathematical_predicates_reproduced=False,foreign_primary_content_freshly_read=False,
       acceptance_verdict=None,original_substantive_turns=0,new_substantive_turns=0,original_source_verification_responses=1))
    assert Path(__file__).read_bytes()==src
    print(json.dumps(dict(status='ORIGINAL_LITERAL_INSPECTION_COMPLETED_ONLY',original_files=13,
        original_JSON_objects=len(objects),original_substantive_turns=0,source_verification_responses=1,
        submitted_checks=51,original_review_checks=848,helpers_executed=0,acceptance_verdict=None),sort_keys=True))
if __name__=='__main__':main()
