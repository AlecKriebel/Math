"""Complete literal/typed PR48 inspection; never executes scientific helpers."""
from pathlib import Path
import ast, collections, datetime as dt, hashlib, json, os, sqlite3, stat, subprocess
A=Path(__file__).resolve().parent
R=A.parents[2]
C=R/'unsolved_math_prioritization'
IDS=['2961','30004403']
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(xs):
    d={}
    for k,v in xs:assert k not in d,('duplicate key',k);d[k]=v
    return d
def parse(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))
def write(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def js(name,x):write(A/name,(json.dumps(x,indent=2,sort_keys=True)+'\n').encode())
def fullread(p):
    before=p.stat();b=p.read_bytes();after=p.stat();assert (before.st_size,before.st_mtime_ns,before.st_mode)==(after.st_size,after.st_mtime_ns,after.st_mode)
    return b,dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(before.st_mode),mtime_ns=before.st_mtime_ns,body_read_in_full=True,raw_body_copied=False)
def native_select(obj,key):
    if isinstance(obj,list):return [x for x in obj if isinstance(x,dict) and type(x.get('id')) is str and x['id']==key]
    assert isinstance(obj,dict);return dict(key=key,key_present=key in obj,value=obj.get(key))
def qrows(b,key):return [x for x in b.decode().splitlines() if x.startswith('|') and any(c.strip()==key or c.strip().startswith(key+' / ') for c in x.split('|')[1:-1])]
def main():
    source=Path(__file__).read_bytes();write(A/'INSPECTION_PRELAUNCH_SOURCE.py',source)
    manifest=parse((A/'snapshot_manifest.json').read_bytes());assert len(manifest['files'])==17
    texts={};objects={};lines={};receipts=[];helper_ast=[]
    for row in manifest['files']:
        p=A/'source_snapshot'/row['relative_path'];b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
        name=row['relative_path'];texts[name]=b.decode();receipts.append(dict(path=name,bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode)))
        if p.suffix=='.json':objects[name]=parse(b)
        if p.suffix=='.jsonl':lines[name]=[parse(x) for x in b.splitlines() if x.strip()]
        if p.suffix=='.py':
            tree=ast.parse(b,filename=name);helper_ast.append(dict(path=name,syntax_parsed_without_execution=True,imports=[ast.unparse(n) for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom))],top_level_functions=[n.name for n in tree.body if isinstance(n,ast.FunctionDef)],full_ast_nodes=sum(1 for n in ast.walk(tree))))
    assert len(objects)==8 and len(lines)==1 and len(helper_ast)==3
    diff=(A/'original_diff.patch').read_bytes();chunks=diff.split(b'diff --git ')[1:];assert len(chunks)==18;reconstructed=[]
    for c in chunks:
        ls=c.splitlines(keepends=True);path=ls[0].decode().strip().split(' b/',1)[1]
        if not path.startswith('unsolved_math_prioritization/attempts/2961/'):continue
        rel=path.split('/attempts/2961/',1)[1];assert b'new file mode 100644\n' in ls
        j=next(i for i,v in enumerate(ls) if v.startswith(b'@@ '));assert all(v.startswith(b'+') for v in ls[j+1:]);assert b''.join(v[1:] for v in ls[j+1:])==(A/'source_snapshot'/rel).read_bytes();reconstructed.append(rel)
    assert set(reconstructed)==set(texts)
    author=objects['check_results.json'];review=objects['review/independent_results.json'];summary=objects['review/review_summary.json'];ready=objects['readiness.json'];ledger=lines['turns.jsonl']
    assert author==objects['review/author_replay/check_results.json'] and (A/'source_snapshot/check_algebra.py').read_bytes()==(A/'source_snapshot/review/author_replay/check_algebra.py').read_bytes()
    assert type(author['all_passed']) is bool and author['all_passed'] is True and type(author['assertions']) is int and author['assertions']==6570
    assert review['status']=='PASS' and review['assertions']==sum(review['checks'].values())==228 and all(type(v) is int and v>0 for v in review['checks'].values())
    assert review['sympy_version']=='1.14.0' and review['free_group_cases']==9 and review['finite_cocycle_action_pairs']==108 and review['nonzero_noninvariant_defects']==43
    finalsha=sha(texts['PARTIAL.md'].encode());assert ready['artifact_sha256']==summary['author_sha256']==finalsha
    assert ready['independent_review']['report_sha256']==summary['files']['REVIEW.md']==sha(texts['review/REVIEW.md'].encode())
    for name,h in summary['files'].items():assert sha(texts['review/'+name].encode())==h
    assert ready['used_substantive_attempts']==len(ledger)==2 and ready['maximum_substantive_attempts']==5 and [r['turn'] for r in ledger]==[1,2]
    oldsha=author['partial_sha256'];assert oldsha==summary['original_author_sha256']==ready['reviewed_mathematical_snapshot_sha256'] and oldsha!=finalsha
    # The old mathematical receipt is attributed, not mistaken for the final byte hash.
    oldsentence='Separate adversarial AI review passed; see [the report](review/REVIEW.md). This has not undergone human peer review.'
    candidates=['Separate adversarial AI review is pending.','Separate adversarial review is pending.']
    sentence_results=[dict(replacement=v,sha256=sha(texts['PARTIAL.md'].replace(oldsentence,v).encode()),equals_claimed_original=sha(texts['PARTIAL.md'].replace(oldsentence,v).encode())==oldsha) for v in candidates]
    # Preserve the actual string-ID selection correction as separate outputs.
    corrections=[]
    for p in sorted((A/'original_native_selected').iterdir()):
        obj=parse(p.read_bytes());name=p.name
        b=subprocess.check_output(['git','cat-file','blob',obj['original_git_binding']['git_object']],cwd=R)
        assert len(b)==obj['original_git_binding']['bytes'] and sha(b)==obj['original_git_binding']['sha256']
        val=[parse(x) for x in b.splitlines() if x.strip()] if name.endswith('.jsonl') else parse(b)
        s=val if name in ('manifest.json','review_v2__related_target_groups.json') else native_select(val,'2961')
        related=val if name in ('manifest.json','review_v2__related_target_groups.json') else native_select(val,'30004403')
        out=dict(original_path=obj['original_path'],original_git_binding=obj['original_git_binding'],selected_problem_id='2961',complete_selected_objects=s,complete_related_selected_objects=related,selection_method='exact string id field in catalog/history or exact string dictionary key; full manifest/group bodies',original_integer_source_IDs_remain_integer=True,priority_or_claim_verification=False)
        dest='original_native_selected_v2/'+name;js(dest,out)
        corrections.append(dict(original_path=p.relative_to(A).as_posix(),original_sha256=sha(p.read_bytes()),corrected_path=dest,corrected_sha256=sha((A/dest).read_bytes()),selection_changed=obj['complete_selected_objects']!=s))
    js('ORIGINAL_SELECTION_CORRECTION.json',dict(schema='pr48-original-exact-string-native-selection-correction/v1',at_utc=now(),actual_pid=os.getpid(),initial_selection_method_incorrect_for_string_list_ids=True,initial_receipts_retained=True,corrected_receipts_separate=True,corrections=corrections))
    # Raw foreign corpus and SQLite are read fully in place; only exact selected rows retained.
    bp=C/'cache/problems.json';br=C/'cache/research_results.json';bd=C/'cache/catalog.sqlite'
    pb,pbind=fullread(bp);rb,rbind=fullread(br);dbbytes,dbbind=fullread(bd)
    problems=parse(pb);reports=parse(rb);assert isinstance(problems,list) and isinstance(reports,dict)
    assert all(isinstance(p,dict) and type(p.get('id')) is int and type(p.get('problem_number')) is str for p in problems)
    allkeys=[str(p['id']) for p in problems];assert len(allkeys)==len(set(allkeys));codecounts=collections.Counter(p['problem_number'] for p in problems)
    db=sqlite3.connect(bd.as_uri()+'?mode=ro&immutable=1',uri=True);schema=db.execute("SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name").fetchall();revision=db.execute('SELECT revision FROM metadata').fetchall();count=db.execute('SELECT count(*) FROM records').fetchone()[0];rows=db.execute('SELECT key,payload,report FROM records WHERE key IN (?,?) ORDER BY key',tuple(IDS)).fetchall();db.close()
    assert fullread(bd)[1]==dbbind and len(rows)==2
    selected=[]
    for key,payload,report in rows:
        problem=parse(payload);prior=parse(report);raw=[p for p in problems if p['id']==int(key)];assert len(raw)==1
        originalname='source_record.json' if key=='2961' else 'related_source_record.json';assert problem==raw[0]==objects[originalname]
        assert 'problem' not in problem and 'prior_research' not in problem and type(problem['id']) is int
        code=problem['problem_number'];present=code in reports;value=reports[code] if present else None
        assert not present and prior=={} and type(prior) is dict and report=='{}'
        rh=sha(json.dumps([problem,prior],sort_keys=True).encode());sth=sha(problem['statement'].encode())
        selected.append(dict(key=key,integer_problem_id=problem['id'],problem_code=code,complete_selected_problem=problem,complete_selected_prior_SQLite=prior,complete_upstream_report=value,upstream_report_key_present=present,upstream_report_presence='ABSENT',upstream_report_value_type='not applicable (key absent)',sqlite_report_literal=report,sqlite_report_value_type=type(prior).__name__,selected_payload_literal_bytes=len(payload.encode()),selected_payload_sha256=sha(payload.encode()),selected_report_literal_bytes=len(report.encode()),selected_report_sha256=sha(report.encode()),source_record_semantics='plain selected problem; no queue.py show wrapper',original_prior_report_file_exists=(A/'source_snapshot/prior_report.json').exists(),original_prose_null_report_claim='SOURCE_AUDIT.md says research-results entry is null',absent_null_empty_object_distinct=True,report_code_occurrences=codecounts[code],review_hash=rh,statement_hash=sth,constructed_show_wrapper_for_semantics_only=dict(review_hash=rh,problem=problem,prior_research=prior),show_program_not_executed=True))
    mb,mbind=fullread(C/'manifest.json');native_manifest=parse(mb);assert revision==[(native_manifest['revision'],)] and count==native_manifest['records']==len(problems)
    for name,binding in [('problems.json',pbind),('research_results.json',rbind)]:assert native_manifest['files'][name]==dict(bytes=binding['bytes'],sha256=binding['sha256'])
    js('ORIGINAL_SELECTED_NATIVE_SOURCE_READ.json',dict(schema='pr48-original-selected-native-source/v1',at_utc=now(),actual_pid=os.getpid(),sqlite_open_mode='ro&immutable=1',foreign_full_raw_bodies_copied=False,foreign_selected_original_source_bodies_already_present_in_PR=True,raw_problem_top_level_type=type(problems).__name__,raw_report_top_level_type=type(reports).__name__,raw_problems_count=len(problems),raw_reports_count=len(reports),raw_integer_IDs_complete_schema_checked=True,raw_problem_IDs_unique=True,schema_rows=schema,revision_rows=revision,sqlite_records_count=count,selected_rows_count=2,selected=selected,raw_native_bindings=[pbind,rbind,dbbind,mbind],queue_show_wrapper_semantics_explicit=True,source_claims_not_validated=True))
    # Date and bind actual current native13 independently; inspect every full body.
    mainhead=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip();bindings=parse((A/'original_native_input_bindings.json').read_bytes());current={};currentbindings=[]
    for row in bindings['current_canonical_native_inputs']:
        b,binding=fullread(R/row['path']);current[row['path']]=b;binding.update(observed_main_head=mainhead,authority_for_future_main=False);currentbindings.append(binding)
    assert len(current)==13
    catalog=parse(current['unsolved_math_prioritization/catalog.json']);assess=parse(current['unsolved_math_prioritization/assessments.json']);state=parse(current['unsolved_math_prioritization/state.json']);hist=[parse(v) for v in current['unsolved_math_prioritization/history.jsonl'].splitlines() if v.strip()]
    ahb,ahbind=fullread(C/'assessment_history.jsonl');ah=[parse(v) for v in ahb.splitlines() if v.strip()]
    selected_current=[]
    for key in IDS:
        rowscat=native_select(catalog,key);assert len(rowscat)==1;rawsel=next(s for s in selected if s['key']==key)
        assert rowscat[0]['review_hash']==assess[key]['review_hash']==rawsel['review_hash'] and rowscat[0]['statement_hash']==rawsel['statement_hash']
        selected_current.append(dict(key=key,complete_selected_catalog=rowscat[0],assessment_key_present=key in assess,complete_selected_assessment=assess[key],state_key_present=key in state,complete_selected_state=state.get(key),complete_selected_history_events=native_select(hist,key),complete_selected_assessment_history_events=native_select(ah,key),selected_queue_rows=qrows(current['unsolved_math_prioritization/QUEUE.md'],key),review_hash=rawsel['review_hash'],statement_hash=rawsel['statement_hash']))
    queue_source=current['unsolved_math_prioritization/queue.py'].decode();queue_ast=ast.parse(queue_source);source_segments={n.name:ast.get_source_segment(queue_source,n) for n in queue_ast.body if isinstance(n,ast.FunctionDef) and n.name in ('sync','show','score','require_cache')}
    js('ORIGINAL_CURRENT_NATIVE_SELECTED_READ.json',dict(schema='pr48-original-current-native-selected/v1',at_utc=now(),actual_pid=os.getpid(),observed_main_head=mainhead,authority_for_future_main=False,current_canonical13_bindings=currentbindings,canonical_count=13,selected=selected_current,native_counts=dict(catalog=len(catalog),assessments=len(assess),state=len(state),history=len(hist),assessment_history=len(ah)),complete_policy=parse(current['unsolved_math_prioritization/policy.json']),complete_related_target_groups=parse(current['unsolved_math_prioritization/review_v2/related_target_groups.json']),assessment_history_binding=ahbind,queue_source_relevant_functions_read_without_execution=source_segments,native_writes=False,transition_performed=False,current_selected_raw_problem_matches_original=True,report_key_absence_not_inferred_from_hash_or_substring=True))
    sources=objects['source_checksums.json'];assert isinstance(sources,list) and len(sources)==5
    assert [(r['url'],r['sha256']) for r in sources]==[(r['url'],r['sha256']) for r in summary['sources_verified']]
    js('ORIGINAL_FOREIGN_SOURCE_BINDINGS.json',dict(schema='pr48-original-foreign-source-literal-claims/v1',original_literal_receipts=sources,review_claimed_verification=summary['sources_verified'],literal_provenance_sha256=sha((A/'source_snapshot/source_checksums.json').read_bytes()),original_pdf_ocr_pixel_bodies_in_owned_topology=False,foreign_primary_content_freshly_read=False,source_claim_validation=False,sha_and_size_role='Literal dated source provenance claims; no freshly authenticated source bodies'))
    js('ORIGINAL_COMPLETE_READ_RECEIPT.json',dict(schema='pr48-original-complete-byte-typed-inspection/v1',actual_pid=os.getpid(),created_utc=now(),original_files_read_in_full=len(receipts),original_bytes_read=sum(r['bytes'] for r in receipts),all_original_file_receipts=receipts,complete_original_JSON_values=objects,complete_original_JSONL_values=lines,original_JSON_value_files=list(objects),original_JSONL_value_files=list(lines),helper_syntax_inspections=helper_ast,full_diff_bytes_read=len(diff),full_diff_sha256=sha(diff),all_17_added_hunks_reconstructed_byte_exact=True,original_author6570_receipt_structurally_inspected=True,original_independent228_labels_counts_structurally_inspected=True,duplicate_author_helpers_and_results_byte_equal=True,final_artifact_sha256=finalsha,original_mathematical_snapshot_sha256=oldsha,final_and_old_SHA_distinction_explicit=True,original_sentence_reversal_candidates=sentence_results,original_ledger_kind='JSONL turns.jsonl',original_substantive_turns=2,new_substantive_turns=0,turn_limit=5,helper_execution_performed=False,mathematical_predicates_reproduced=False,foreign_primary_content_freshly_read=False,original_model_runtime_and_PASS_attribution_only=True,acceptance_verdict=None))
    assert Path(__file__).read_bytes()==source
    print(json.dumps(dict(status='ORIGINAL_LITERAL_TYPED_INSPECTION_ONLY',original_files=17,JSON_values=8,JSONL_ledgers=1,substantive_turns=2,turn_limit=5,submitted_assertions=6570,independent_assertions=228,source_record_type='plain selected problem',related_source_record_id=30004403,prior_semantics='BOTH_UPSTREAM_KEYS_ABSENT_SQLITE_EMPTY_OBJECT_NO_PRIOR_FILE_PROSE_NULL',current_native13_full_reads=True,observed_main_head=mainhead,helpers_executed=0,acceptance_verdict=None),sort_keys=True))
if __name__=='__main__':main()
