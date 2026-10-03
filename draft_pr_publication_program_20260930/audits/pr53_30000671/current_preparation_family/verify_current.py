"""Verify operative science, exact original archive, and all genuine closed inputs."""
import hashlib,json,pathlib,re,stat
F=pathlib.Path(__file__).resolve().parent
R=F.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def mode(p):return format(stat.S_IMODE(p.stat().st_mode),'04o')
def main():
    ext=json.loads((F/'EXTERNAL_REFERENCES.json').read_bytes())
    assert ext['schema']=='pr53-current-inplace-closed-inputs/v1' and ext['root_approval'] is False
    count=0
    for group in ext['closed_families']+ext['actual_root_captures']:
        for row in group['rows']:
            p=R/row['repo_path'];b=p.read_bytes()
            assert not p.is_symlink() and p.is_file()
            assert len(b)==row['bytes'] and sha(b)==row['sha256'] and mode(p)==row['mode'],row['repo_path']
            count+=1
        for row in group.get('directories',[]):assert mode(R/row['repo_path'])==row['mode']
    assert len(ext['closed_families'])==3 and len(ext['actual_root_captures'])==6
    for group in ext['closed_families']:
        base=R/'draft_pr_publication_program_20260930/audits/pr53_30000671'/group['family']
        actual=sorted(p.relative_to(R).as_posix() for p in base.rglob('*') if p.is_file())
        assert actual==sorted(r['repo_path'] for r in group['rows'])
        assert sha((base/'MANIFEST.json').read_bytes())==group['manifest_sha256']
    orig=R/'draft_pr_publication_program_20260930/audits/pr53_30000671/original_preparation_family'
    auth=json.loads((orig/'GITHUB_AUTHENTICATION.json').read_bytes())
    for row in auth['files']:
        rel=row['archive_path'];b=(F/rel).read_bytes()
        assert b==(orig/rel).read_bytes() and len(b)==row['bytes'] and sha(b)==row['sha256']
        assert hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==row['git_blob_sha1']
    idx=json.loads((F/'SCIENCE_INDEX.json').read_bytes())
    assert idx['original_archive_files']==11 and idx['operative_science_files']==14 and len(idx['files'])==25
    listed={r['path'] for r in idx['files']}
    actual={p.relative_to(F).as_posix() for root in ['original_archive','science'] for p in (F/root).rglob('*') if p.is_file()}
    assert listed==actual
    for row in idx['files']:
        b=(F/row['path']).read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256']
    rec=json.loads((F/'science/source_record.json').read_bytes())
    historic=json.loads((F/'original_archive/source_record.json').read_bytes())
    assert rec['record']==historic['record'] and rec['record']['status']=='open'
    audit=rec['operative_audit']
    assert audit['recommended_status']=='already_solved' and audit['raw_report_key_present'] is False
    assert audit['selected_sql_report_literal']=='{}' and audit['archived_null_is_absence_marker'] is True
    assert audit['root_approval'] is False and audit['full_2008_article_read'] is False
    ready=json.loads((F/'science/readiness.json').read_bytes())
    assert ready['used_substantive_attempts']==0 and ready['maximum_substantive_attempts']==5
    assert ready['root_approval'] is False and ready['new_substantive_proof_attempts']==0 and ready['no_new_paper'] is True
    assert (F/'science/turns.jsonl').read_bytes()==(F/'original_archive/turns.jsonl').read_bytes()==b''
    assert ready['artifact_sha256']==sha((F/'science/SOURCE_STATUS.md').read_bytes())
    assert ready['independent_review']['report_sha256']==sha((F/'science/review/REVIEW.md').read_bytes())
    for rel in ['science/review/review_summary.json','VERDICT.json']:
        v=json.loads((F/rel).read_bytes());assert v['fresh_distinct_review_families']==2
        assert v['third_independent_review_by_preparer'] is False and v['root_approval'] is False and v['new_paper_recommended'] is False
        assert v['historical_construction_independently_reproduced'] is False and v['full_2008_article_read'] is False
        assert v['current_integral_domain_status']=='not assessed'
        assert v['separate_original_response_count_inferred'] is False
    # All real links between operative science files must survive promotion of science/ to the canonical attempt root.
    for p in (F/'science').rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if target.startswith(('https://','http://','/')):continue
            assert (p.parent/target).is_file(),(str(p),target)
            assert (F/'science') in (p.parent/target).resolve().parents
    for rel in ['BOUNDARY_PROOFS.md','INVERSE_SYSTEM_SCOPE.md']:
        assert 'not a new independent review' in (F/'science'/rel).read_text()
    print(json.dumps({'status':'PASS_SOURCE_PREPARATION_ONLY','whole_closed_external_rows':count,'exact_original_science_files':11,'operative_science_files':14,'genuine_root_custody_events':6,'fresh_distinct_review_families':2,'third_independent_math_review':False,'native_git_writes':False,'root_approval':False,'new_paper':False,'historical_counterexample_reproduced':False}))
if __name__=='__main__':main()
