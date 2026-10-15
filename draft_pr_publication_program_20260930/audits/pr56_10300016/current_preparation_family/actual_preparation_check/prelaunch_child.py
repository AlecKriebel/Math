"""Current qualified SOURCE checks only; no fresh mathematical family or ROOT authority."""
import datetime,hashlib,json,pathlib,stat,re,os
F=pathlib.Path(__file__).absolute().parent;A=F.parent;R=F.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def js(p):return json.loads(p.read_bytes())
def mode(p):return format(stat.S_IMODE(p.stat().st_mode),'04o')
checks=0
def require(ok):
    global checks
    assert ok
    checks+=1
require(not (F/'MANIFEST.json').exists())
s=js(F/'SOURCE_ACCOUNTING_CURRENT.json');q=js(F/'science/CURRENT_QUALIFICATIONS.json')
require(s['original_head']=='6afe45fdc0dc8cca35c94227f4660dadcfd0de90')
require(s['actual_merge_base']=='01358d66fc67d1c462bddf31c0d4ee5b120e6737')
require(s['reported_GitHub_base']=='c6975ca76f9f667f1250ba403d0e6da2aafe14d0')
require(s['raw_report_key_present'] is True and isinstance(s['raw_report_value'],dict) and bool(s['raw_report_value']))
require(s['SQL_report_is_NULL'] is False and json.loads(s['SQL_report_literal'])==s['raw_report_value']==s['wrapper_upstream_report'])
require(s['separate_prior_report_file_present'] is False and s['original_JSONL_turn_entry_count']==2)
require(s['original_turns_used']==2 and s['original_turn_limit']==5 and s['new_substantive_attempt_turns']==0)
require(q['current_source_status']=='unsolved' and q['paper_preprint_Zenodo_DOI'] is False and q['current_preparer_new_independent_math_family'] is False)
require(q['full_target_completion_percent']==0 and q['original_substantive_attempts']==2)
auth=js(A/'original_preparation_family/ORIGINAL_AUTHENTICATION.json');idx=js(F/'SCIENCE_INDEX.json')
require(idx['original_archive_files']==16 and idx['operative_science_files']==19)
for row in idx['files']:
    b=(F/row['path']).read_bytes();require(len(b)==row['bytes'] and sha(b)==row['sha256'])
for row in auth['original_science_files']:
    rel=row['relative_path'];b=(F/'original_archive'/rel).read_bytes()
    require(len(b)==row['bytes'] and sha(b)==row['sha256'])
    require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1'])
    require(b==(A/'original_preparation_family/original'/rel).read_bytes())
for rel in q['historical_receipts_kept_exact']+['OBSTRUCTION.md','verify_cone_controls.py','review/independent_checks.py']:
    require((F/'science'/rel).read_bytes()==(F/'original_archive'/rel).read_bytes())
artifact=(F/'science/OBSTRUCTION.md').read_bytes();require(q['original_artifact_sha256']==sha(artifact))
for name in ['review/REVIEW.md','RESEARCH_LOG.md','SOURCES.md']:
    require((F/'science'/name).read_bytes().endswith((F/'original_archive'/name).read_bytes()))
status=js(F/'science/status.json');ready=js(F/'science/readiness.json');rec=js(F/'science/source_record.json');oldrec=js(F/'original_archive/source_record.json')
require(status['status']=='unsolved' and status['turns_used']==2 and status['turn_limit']==5 and status['full_source_solved'] is False and status['paper_recommended'] is False)
require(status['artifact_sha256']==sha(artifact) and status['verifier_sha256']==sha((F/'science/verify_cone_controls.py').read_bytes()))
require(status['new_substantive_attempts']==0 and status['exact_gap']==q['exact_remaining_gap'])
require(ready['current_source_disposition']=='unsolved' and ready['paper_ready_or_recommended'] is False)
require(rec['problem']==oldrec['problem'] and rec['upstream_report']==oldrec['upstream_report']==s['raw_report_value'])
require(rec['current_review_qualification']['SQL_report_typed_equal_raw_and_wrapper'] is True)
require(js(F/'science/review/review_summary.json')['current_source_disposition']=='unsolved')
require([json.loads(x) for x in (F/'science/turns.jsonl').read_text().splitlines()]==s['original_JSONL_turns'])
for p in (F/'science').rglob('*.md'):
    for dest in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if dest.startswith(('https://','http://','mailto:','#')):continue
        base=dest.split('#')[0]
        if base:require((p.parent/base).resolve().is_file())
ext=js(F/'EXTERNAL_REFERENCES.json');n=0
def verify_row(row):
    p=R/row['repo_path'];b=p.read_bytes();require(not p.is_symlink() and p.is_file() and len(b)==row['bytes'] and sha(b)==row['sha256'] and mode(p)==row['mode'])
for g in ext['custody_families']+ext['actual_root_captures']:
    base=R/g['repo_path'];require(not base.is_symlink())
    require({p.relative_to(R).as_posix() for p in base.rglob('*') if p.is_file()}=={row['repo_path'] for row in g['rows']})
    require({p.relative_to(R).as_posix() for p in [base,*base.rglob('*')] if p.is_dir()}=={row['repo_path'] for row in g['directories']})
    for row in g['rows']:verify_row(row);n+=1
    for row in g['directories']:require(mode(R/row['repo_path'])==row['mode'])
for row in ext['standalone_rows']:verify_row(row);n+=1
for g in ext['custody_families']:
    if 'manifest_repo_path' in g:require(sha((R/g['manifest_repo_path']).read_bytes())==g['manifest_sha256'])
    else:
        require(sha((R/g['fixed_index_repo_path']).read_bytes())==g['fixed_index_sha256'])
        ledger=js(R/g['root_custody_record_repo_path']);base=R/g['repo_path']
        require(sha((R/g['root_custody_record_repo_path']).read_bytes())==g['root_custody_record_sha256'])
        require(ledger['actual_writer_pid']==81435 and ledger['source_custody_closed'] and ledger['helpers_write_no_manifest_or_custody'])
        require(len(ledger['files'])==111 and len(ledger['directories'])==10)
        require({(base/row['path']).relative_to(R).as_posix() for row in ledger['files']}=={row['repo_path'] for row in g['rows']})
        for row in ledger['files']:
            p=base/row['path'];b=p.read_bytes();require(len(b)==row['bytes'] and sha(b)==row['sha256'] and mode(p)==row['full_mode_07777'])
        require(not (base/'SELF_MANIFEST.json').exists() and not (base/'MANIFEST.json').exists())
for g in ext['actual_root_captures']:
    base=R/g['repo_path'];c=js(base/'CAPTURE.json')
    require(c['pid']==g['pid'] and c['argv']==g['argv'] and c['exit_code']==0 and c['actual_execution'] is True)
    require(c['started_utc']==g['started_utc'] and c['finished_utc']==g['finished_utc'] and c['operator_unchanged'] is True)
    require(sha((base/'prelaunch_operator.py').read_bytes())==c['operator_sha256'])
    for key in ['stdout','stderr']:
        row=c[key];b=(base/row['path']).read_bytes();require(len(b)==row['bytes'] and sha(b)==row['sha256'])
published=js(A/'geometric_splitting_adversary_family/PUBLISHED_LANDRY_RECEIPT.json')
require(published['full_publisher_PDF_acquired'] is True and published['pdf_sha256']==q['published_Landry_pdf_sha256'])
require(published['pdf_bytes']==2462438 and published['every_dependency_independently_audited'] is False)
require(published['initial_web_viewer_failure_was_not_final_publication_access_failure'] is True and published['private_primary_bodies_included_in_lean_handoff'] is False)
d=F/'actual_current_author_replay';c=js(d/'CAPTURE.json')
require(c['exit_code']==0 and c['actual_execution'] and c['sources_unchanged'] and c['operator_unchanged'])
require(c['argv']==['/usr/bin/python3','-B',str(F/'science/verify_cone_controls.py')])
require(type(c['pid']) is int and c['pid']>0 and datetime.datetime.fromisoformat(c['started_utc'])<=datetime.datetime.fromisoformat(c['finished_utc']))
require(sha((d/'prelaunch_operator.py').read_bytes())==c['operator_sha256'])
for row in c['sources']:
    b=(d/row['prelaunch_copy']).read_bytes();require(len(b)==row['bytes'] and sha(b)==row['sha256'] and b==pathlib.Path(row['path']).read_bytes())
for key in ['stdout','stderr']:
    row=c[key];b=(d/row['path']).read_bytes();require(len(b)==row['bytes'] and sha(b)==row['sha256'])
out=js(d/'stdout.bin');require(out['status']=='PASS' and out['exact_assertions']==191 and out['positive_matrix_controls']==16 and out['branch_cone_controls']==24 and out['unipotent_iterates']==10)
require(out['artifact_sha256']==sha(artifact) and out['verifier_sha256']==sha((F/'science/verify_cone_controls.py').read_bytes()))
require((d/'stdout.bin').read_bytes()==(F/'original_archive/cone_verification.json').read_bytes() and c['artifact_hash_read_by_checker'] is True)
replay=js(F/'CURRENT_REPRODUCTION.json');require(replay['actual_child_pid']==c['pid'] and replay['current_artifact_sha256']==sha(artifact) and replay['new_independence'] is False and replay['root_approval'] is False)
print(json.dumps({'status':'PASS_SOURCE_PREPARATION_ONLY','actual_verifier_pid':os.getpid(),'source_checks':checks,'external_whole_body_rows':n,'archive_files':16,'operative_science_files':19,'full_target_discovery_percent':0,'root_approval':False,'native_git_writes':False}))
