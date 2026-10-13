"""SOURCE body/accounting/receipt verifier, not a fresh mathematical adversary or ROOT acceptance."""
import datetime,hashlib,json,pathlib,stat,os,re
F=pathlib.Path(__file__).absolute().parent
R=F.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def js(p):return json.loads(p.read_bytes())
def mode(p):return format(stat.S_IMODE(p.stat().st_mode),'04o')
checks=0
def require(ok):
    global checks
    assert ok
    checks+=1
require(not (F/'MANIFEST.json').exists())
source=js(F/'SOURCE_ACCOUNTING_CURRENT.json');q=js(F/'science/CURRENT_QUALIFICATIONS.json')
require(source['original_head']=='85c78d0cf3959d9d492a637cb90835ebc6a0e828')
require(source['actual_merge_base']=='01358d66fc67d1c462bddf31c0d4ee5b120e6737')
require(source['reported_GitHub_base']=='c6975ca76f9f667f1250ba403d0e6da2aafe14d0')
require(source['raw_key_present'] is False and source['raw_value']=='ABSENT; no raw value')
require(source['SQL_report_is_NULL'] is False and source['SQL_report_literal']=='{}' and source['wrapper_upstream_report'] is None)
require(source['original_turns_used']==1 and source['original_turn_limit']==5 and source['new_proof_search_turns']==0)
require(source['original_JSONL_turn_entry_count']==1 and source['generic_response_count']=='not separately supplied; no count invented')
require(q['current_source_status']=='already_solved' and q['paper_preprint_Zenodo_DOI'] is False and q['current_preparer_is_new_independent_math_family'] is False)
require(q['original_substantive_attempts']==1 and q['original_JSONL_turn_entries']==1 and q['novel_discovery_completion_percent']==0)
auth=js(F.parent/'original_preparation_family/ORIGINAL_AUTHENTICATION.json')
idx=js(F/'SCIENCE_INDEX.json')
require(idx['original_archive_files']==16 and idx['operative_science_files']==20)
for row in idx['files']:
    p=F/row['path'];b=p.read_bytes();require(len(b)==row['bytes'] and sha(b)==row['sha256'])
for row in auth['original_science_files']:
    rel=row['relative_path'];b=(F/'original_archive'/rel).read_bytes()
    require(sha(b)==row['sha256'] and len(b)==row['bytes'])
    require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1'])
    require(b==(F.parent/'original_preparation_family/original'/rel).read_bytes())
for rel in q['historical_receipts_kept_byte_exact']+['verify_product_vectors.py','review/independent_checks.py']:
    require((F/'science'/rel).read_bytes()==(F/'original_archive'/rel).read_bytes())
candidate=(F/'science/CANDIDATE.md').read_bytes();original=(F/'original_archive/CANDIDATE.md').read_bytes()
require(candidate.endswith(original) and q['original_candidate_sha256']==sha(original))
require((F/'science/review/REVIEW.md').read_bytes().endswith((F/'original_archive/review/REVIEW.md').read_bytes()))
require((F/'science/RESEARCH_LOG.md').read_bytes().endswith((F/'original_archive/RESEARCH_LOG.md').read_bytes()))
require((F/'science/SOURCES.md').read_bytes().endswith((F/'original_archive/SOURCES.md').read_bytes()))
require((F/'science/PRIOR_ART_SPECIALIZATION.md').read_bytes().endswith((F.parent/'prior_newton_formula_audit/DERIVATION.md').read_bytes()))
status=js(F/'science/status.json');ready=js(F/'science/readiness.json');rec=js(F/'science/source_record.json')
require(status['status']=='already_solved' and status['full_source_solved'] is False and status['new_paper'] is False)
require(status['proof_sha256']==sha(candidate) and status['original_reviewed_proof_sha256']==sha(original))
require(status['verifier_sha256']==sha((F/'science/verify_product_vectors.py').read_bytes()))
require(ready['current_source_disposition']=='already_solved' and ready['paper_ready_or_recommended'] is False)
require(rec['problem']==js(F/'original_archive/source_record.json')['problem'] and rec['upstream_report'] is None)
require(rec['current_review_qualification']['historical_raw_triage_superseded_for_current_disposition'] is True)
require(js(F/'science/review/review_summary.json')['current_source_disposition']=='already_solved')
require(len((F/'science/turns.jsonl').read_text().splitlines())==1)
# Resolve every local Markdown link wholly inside operative science; official URLs stay external.
for p in (F/'science').rglob('*.md'):
    for dest in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if dest.startswith(('https://','http://','mailto:','#')):continue
        base=dest.split('#')[0]
        if base:require((p.parent/base).resolve().is_file())
ext=js(F/'EXTERNAL_REFERENCES.json');n=0
for group in ext['closed_families']+ext['actual_root_captures']+ext['frozen_source_notes']:
    base=R/group['repo_path'];require(not base.is_symlink())
    require({p.relative_to(R).as_posix() for p in base.rglob('*') if p.is_file()}=={x['repo_path'] for x in group['rows']})
    require({p.relative_to(R).as_posix() for p in [base,*base.rglob('*')] if p.is_dir()}=={x['repo_path'] for x in group['directories']})
    for row in group['rows']:
        p=R/row['repo_path'];b=p.read_bytes();require(not p.is_symlink() and p.is_file() and len(b)==row['bytes'] and sha(b)==row['sha256'] and mode(p)==row['mode']);n+=1
    for row in group['directories']:require(mode(R/row['repo_path'])==row['mode'])
for group in ext['closed_families']:
    require(sha((R/group['manifest_repo_path']).read_bytes())==group['manifest_sha256'])
for group in ext['actual_root_captures']:
    base=R/group['repo_path'];cap=js(base/'CAPTURE.json')
    require(cap['pid']==group['pid'] and cap['argv']==group['argv'] and cap['exit_code']==0)
    require(cap['started_utc']==group['started_utc'] and cap['finished_utc']==group['finished_utc'])
    require(cap['actual_execution'] is True and cap['operator_unchanged'] is True)
    require(sha((base/'prelaunch_operator.py').read_bytes())==cap['operator_sha256'])
    for key in ['stdout','stderr']:
        d=cap[key];b=(base/d['path']).read_bytes();require(len(b)==d['bytes'] and sha(b)==d['sha256'])
capdir=F/'actual_current_author_replay';cap=js(capdir/'CAPTURE.json')
require(cap['exit_code']==0 and cap['actual_execution'] and cap['sources_unchanged'] and cap['operator_unchanged'])
require(cap['argv']==['/usr/bin/python3','-B',str(F/'science/verify_product_vectors.py')])
require(type(cap['pid']) is int and cap['pid']>0)
require(datetime.datetime.fromisoformat(cap['started_utc'])<=datetime.datetime.fromisoformat(cap['finished_utc']))
require(sha((capdir/'prelaunch_operator.py').read_bytes())==cap['operator_sha256'])
for row in cap['sources']:
    b=(capdir/row['prelaunch_copy']).read_bytes();require(len(b)==row['bytes'] and sha(b)==row['sha256'] and b==pathlib.Path(row['path']).read_bytes())
for key in ['stdout','stderr']:
    row=cap[key];b=(capdir/row['path']).read_bytes();require(len(b)==row['bytes'] and sha(b)==row['sha256'])
out=js(capdir/'stdout.bin');require(out['status']=='PASS' and out['exact_assertions']==1227 and out['case_count']==8)
require((capdir/'stdout.bin').read_bytes()==(F/'original_archive/product_verification.json').read_bytes())
require(cap['candidate_context_bound_by_operator_not_read_by_checker'] is True)
replay=js(F/'CURRENT_REPRODUCTION.json')
require(replay['actual_child_pid']==cap['pid'] and replay['current_candidate_sha256']==sha(candidate) and replay['new_independence'] is False)
require(replay['stdout_byte_identical_historical_numeric_receipt'] is True and replay['root_approval'] is False)
print(json.dumps({'status':'PASS_SOURCE_PREPARATION_ONLY','actual_verifier_pid':os.getpid(),'source_checks':checks,'external_whole_body_rows':n,'archive_files':16,'operative_science_files':20,'novel_discovery_percent':0,'root_approval':False,'native_git_writes':False}))
