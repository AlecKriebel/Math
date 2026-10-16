"""Literal/typed PR47 inspection, exact-ID native selection; no old scientific execution."""
from pathlib import Path
import datetime as dt, hashlib, json, os, sqlite3, stat, subprocess
A=Path(__file__).resolve().parent
R=A.parents[2]
ID='2849'
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(xs):
    d={}
    for k,v in xs:assert k not in d,('duplicate key',k);d[k]=v
    return d
def parse(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def write(name,b):
    with (A/name).open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def js(name,x):write(name,(json.dumps(x,indent=2,sort_keys=True)+'\n').encode())
def bind(p):
    st=p.stat();h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    en=p.stat();assert (st.st_size,st.st_mtime_ns,stat.S_IMODE(st.st_mode))==(en.st_size,en.st_mtime_ns,stat.S_IMODE(en.st_mode))
    return dict(path=p.relative_to(R).as_posix(),bytes=st.st_size,sha256=h.hexdigest(),full_mode=stat.S_IMODE(st.st_mode),mtime_ns=st.st_mtime_ns,copied_into_owned_topology=False)
def main():
    source=Path(__file__).read_bytes();write('INSPECTION_V2_PRELAUNCH_SOURCE.py',source)
    manifest=parse((A/'snapshot_manifest.json').read_bytes());texts={};objects={};receipts=[]
    assert len(manifest['files'])==16
    for row in manifest['files']:
        p=A/'source_snapshot'/row['relative_path'];b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
        texts[row['relative_path']]=b.decode()
        if p.suffix=='.json':objects[row['relative_path']]=parse(b)
        receipts.append(dict(path=row['relative_path'],bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode)))
    assert len(objects)==9
    diff=(A/'original_diff.patch').read_bytes();chunks=diff.split(b'diff --git ')[1:];assert len(chunks)==17
    reconstructed=[]
    for c in chunks:
        lines=c.splitlines(keepends=True);path=lines[0].decode().strip().split(' b/',1)[1]
        if '/attempts/2849/' not in path:continue
        rel=path.split('/attempts/2849/',1)[1];assert b'new file mode 100644\n' in lines
        j=next(i for i,v in enumerate(lines) if v.startswith(b'@@ '));assert all(v.startswith(b'+') for v in lines[j+1:])
        b=b''.join(v[1:] for v in lines[j+1:]);assert b==(A/'source_snapshot'/rel).read_bytes();reconstructed.append(rel)
    assert set(reconstructed)==set(texts)
    author=objects['verification.json'];review=objects['review/independent_results.json'];sub=objects['review/submitted_results.json'];verdict=objects['review/verdict.json'];turns=objects['turns.json'];readiness=objects['readiness.json']
    assert type(author['passed']) is bool and author['passed'] is True and author['assertions']==114 and len(author['checks'])==114 and all(type(x) is str for x in author['checks'])
    assert {k:v for k,v in author.items() if k!='checks'}==sub
    assert type(review['passed']) is int and review['passed']==100 and review['failed']==0 and len(review['checks'])==100 and all(v=='PASS' for v in review['checks'].values())
    assert review['trefoil_rank_one_H1']==[0,1,0,0,0,1] and review['trefoil_squared_rank_one_H1']==[0]*6
    assert (A/'source_snapshot/verify.py').read_bytes()==(A/'source_snapshot/review/submitted_verify.py').read_bytes()
    artsha=sha((A/'source_snapshot/OBSTRUCTION.md').read_bytes());revsha=sha((A/'source_snapshot/review/REVIEW.md').read_bytes())
    assert verdict['reviewed_artifact_sha256']==turns['attempts'][0]['sha256']==artsha and verdict['review_sha256']==revsha
    assert turns['count']==len(turns['attempts'])==1 and readiness['budget']['used']==1 and readiness['budget']['maximum_substantive_attempts']==5
    assert objects['prior_report.json'] is None
    correction=parse((A/'ORIGINAL_SELECTION_CORRECTION.json').read_bytes())
    for row in correction['corrections']:
        obj=parse((A/row['path']).read_bytes())
        assert sha((A/row['path']).read_bytes())==row['corrected_sha256']
        chosen=obj['complete_selected_objects']
        if isinstance(chosen,list):assert all(str(x.get('id'))==ID for x in chosen)
    cache=R/'unsolved_math_prioritization/cache/catalog.sqlite';before=bind(cache)
    db=sqlite3.connect(cache.as_uri()+'?mode=ro&immutable=1',uri=True)
    tables=db.execute("SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name").fetchall();rows=db.execute('SELECT key,payload,report FROM records WHERE key=?',(ID,)).fetchall();revision=db.execute('SELECT revision FROM metadata').fetchall();count=db.execute('SELECT count(*) FROM records').fetchone()[0];db.close();assert bind(cache)==before and len(rows)==1
    problem=parse(rows[0][1]);prior=parse(rows[0][2]);assert problem==objects['source_record.json'] and prior=={}
    # Raw cache files are parsed in place only. Report-key presence is distinct from null value.
    bp=R/'unsolved_math_prioritization/cache/problems.json';br=R/'unsolved_math_prioritization/cache/research_results.json';problems=parse(bp.read_bytes());reports=parse(br.read_bytes())
    selected=[x for x in problems if str(x.get('id'))==ID];assert len(selected)==1 and selected[0]==problem
    code=problem['problem_number'];present=code in reports;assert not present and prior=={}
    manifest_native=parse((R/'unsolved_math_prioritization/manifest.json').read_bytes());assert revision==[(manifest_native['revision'],)] and count==manifest_native['records']==len(problems)
    for name,path in [('problems.json',bp),('research_results.json',br)]:
        row=bind(path);assert manifest_native['files'][name]==dict(bytes=row['bytes'],sha256=row['sha256'])
    reviewhash=sha(json.dumps([problem,prior],sort_keys=True).encode());statementhash=sha(problem['statement'].encode())
    assert reviewhash==readiness['review_hash'] and statementhash==readiness['statement_hash']
    sql=dict(schema='pr47-original-selected-native-source/v1',actual_pid=os.getpid(),read_at_utc=now(),sqlite_open_mode='ro&immutable=1',foreign_sqlite_body_copied=False,schema_rows=tables,revision_rows=revision,records_count=count,selected_rows_count=1,complete_selected_problem=problem,complete_selected_prior_report=prior,selected_payload_literal_bytes=len(rows[0][1].encode()),selected_payload_sha256=sha(rows[0][1].encode()),selected_report_literal_bytes=len(rows[0][2].encode()),selected_report_sha256=sha(rows[0][2].encode()),exact_original_source_record_JSON_match=True,original_source_record_kind='plain selected problem, not queue.py show wrapper',upstream_report_key=code,upstream_report_key_presence='ABSENT',upstream_report_value=None,prior_report_presence_kind='ABSENT_EMPTY_OBJECT_IN_SQLITE',original_prior_report_file_value=None,original_prior_report_file_literal='null\n',original_vs_native_prior_JSON_equal=False,original_null_must_not_be_inferred_as_present_upstream_report=True,upstream_reports_total_keys=len(reports),selected_problem_cache_match=True,selected_prior_SQLite_matches_queue_sync_absent_default=True,review_hash=reviewhash,statement_hash=statementhash,source_truth_or_current_priority_certified=False)
    js('ORIGINAL_SELECTED_NATIVE_SOURCE_READ.json',sql)
    # Independently dated current canonical13 bindings; cannot authorize future main or any transition.
    mainhead=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip();bindings=parse((A/'original_native_input_bindings.json').read_bytes());currentbindings=[bind(R/r['path']) for r in bindings['current_canonical_native_inputs']]
    C=R/'unsolved_math_prioritization'
    catalog=parse((C/'catalog.json').read_bytes());cs=[x for x in catalog if str(x.get('id'))==ID];assert len(cs)==1
    assessments=parse((C/'assessments.json').read_bytes());state=parse((C/'state.json').read_bytes());history=[parse(line) for line in (C/'history.jsonl').read_bytes().splitlines() if line.strip()];ah=[parse(line) for line in (C/'assessment_history.jsonl').read_bytes().splitlines() if line.strip()]
    hs=[x for x in history if str(x.get('id'))==ID];ahs=[x for x in ah if str(x.get('id'))==ID]
    queue=(C/'QUEUE.md').read_text();qrows=[x for x in queue.splitlines() if '| '+ID+' / ' in x or x.startswith('| '+ID+' |')]
    codebytes=(C/'queue.py').read_bytes();readmebytes=(C/'README.md').read_bytes();agentbytes=(C/'AGENTS.md').read_bytes();policy=parse((C/'policy.json').read_bytes());related=parse((C/'review_v2/related_target_groups.json').read_bytes())
    assert cs[0]['review_hash']==assessments[ID]['review_hash']==reviewhash and cs[0]['statement_hash']==statementhash
    js('ORIGINAL_CURRENT_NATIVE_SELECTED_READ.json',dict(schema='pr47-original-current-native-selected/v1',actual_pid=os.getpid(),read_at_utc=now(),observed_main_head=mainhead,authority_for_future_main=False,current_canonical13_bindings=currentbindings,canonical_count=13,complete_selected_catalog=cs[0],complete_selected_assessment=assessments[ID],selected_state_key_present=ID in state,complete_selected_state=state.get(ID),complete_selected_history_events=hs,complete_selected_assessment_history_events=ahs,selected_queue_rows=qrows,complete_policy=policy,complete_related_target_groups=related,native_counts=dict(catalog=len(catalog),assessments=len(assessments),state=len(state),history=len(history),assessment_history=len(ah),selected_history=len(hs),selected_assessment_history=len(ahs)),program_source_bindings=[bind(C/'queue.py'),bind(C/'README.md'),bind(C/'AGENTS.md')],native_writes=False,transition_performed=False,review_hash_matches=True,statement_hash_matches=True,selected_current_source_matches_original=True))
    foreignsources=[dict(original_receipt_fields=row,body_copied=False,body_freshly_read=False,hash_and_size_role='Literal original provenance claim only; no newly authenticated source body') for row in objects['source_checksums.json']['sources']]
    foreignsources.append(dict(original_receipt_fields=objects['source_checksums.json']['original_k3'],body_copied=False,body_freshly_read=False,hash_and_size_role='Literal original K3 hash claim; no fresh PDF authentication'))
    js('ORIGINAL_FOREIGN_SOURCE_BINDINGS.json',dict(schema='pr47-original-foreign-source-claimed-bindings/v1',sources=foreignsources,original_pdf_ocr_pixel_bodies_in_owned_topology=False,literal_provenance_sha256=sha((A/'source_snapshot/source_checksums.json').read_bytes()),fresh_foreign_source_read=False,source_claim_validation=False))
    js('ORIGINAL_COMPLETE_READ_RECEIPT.json',dict(schema='pr47-original-complete-byte-and-typed-inspection/v1',actual_pid=os.getpid(),created_utc=now(),original_files_read_in_full=len(receipts),original_bytes_read=sum(x['bytes'] for x in receipts),all_original_file_receipts=receipts,complete_original_JSON_objects=objects,original_JSON_object_files=list(objects),original_JSONL_object_files=[],full_diff_bytes_read=len(diff),full_diff_sha256=sha(diff),all_16_added_hunks_reconstructed_byte_exact=True,complete_author114_labels_structurally_inspected=True,complete_independent100_labels_values_structurally_inspected=True,original_artifact_and_review_hash_references_match=True,duplicate_helper_bytes_equal=True,helper_execution_performed=False,mathematical_predicates_reproduced=False,foreign_primary_content_freshly_read=False,acceptance_verdict=None,original_ledger_kind='JSON object turns.json',original_substantive_turns=1,new_substantive_turns=0,turn_limit=5,original_model_runtime_and_PASS_attribution_only=True))
    assert Path(__file__).read_bytes()==source
    print(json.dumps(dict(status='ORIGINAL_LITERAL_INSPECTION_COMPLETED_ONLY',original_files=16,original_JSON_objects=len(objects),original_substantive_turns=1,turn_limit=5,prior_report_presence='UPSTREAM_ABSENT_SQLITE_EMPTY_OBJECT_ORIGINAL_NULL',original_source_kind='plain problem',submitted_checks=114,original_review_checks=100,helpers_executed=0,current_selected_native_state_present=ID in state,current_selected_native_history_events=len(hs),current_queue_rows=qrows,acceptance_verdict=None),sort_keys=True))
if __name__=='__main__':main()
