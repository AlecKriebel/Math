"""Original-source integrity checks. No author numerical checker exists in PR53."""
import hashlib,json,pathlib,re
F=pathlib.Path(__file__).resolve().parent
R=F.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    a=json.loads((F/'GITHUB_AUTHENTICATION.json').read_text())
    for row in a['files']:
        b=(F/row['archive_path']).read_bytes()
        assert len(b)==row['bytes'] and sha(b)==row['sha256']
        assert hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==row['git_blob_sha1']
    assert len(a['files'])==11 and not any(x['repo_path'].endswith('.py') for x in a['files'])
    old=F/'original_archive'
    ready=json.loads((old/'readiness.json').read_text())
    rev=json.loads((old/'review/review_summary.json').read_text())
    assert ready['id']==30000671 and ready['used_substantive_attempts']==0
    assert (old/'turns.jsonl').read_bytes()==b''
    assert ready['status']==rev['recommended_queue_status']=='already_solved'
    assert ready['our_new_discovery'] is False and rev['new_discovery'] is False
    assert ready['artifact_sha256']==rev['artifact_sha256']==sha((old/'SOURCE_STATUS.md').read_bytes())
    assert ready['independent_review']['report_sha256']==rev['report_sha256']==sha((old/'review/REVIEW.md').read_bytes())
    assert ready['full_2008_article_retrieved'] is False and rev['full_2008_article_retrieved'] is False
    assert ready['historical_construction_independently_reproved'] is False and rev['independent_construction_verification'] is False
    assert ready['distinct_domain_restriction_current_status']=='not determined'
    record=json.loads((old/'source_record.json').read_text())
    manifest=json.loads((R/'unsolved_math_prioritization/manifest.json').read_text())
    assert record['revision']==manifest['revision']=='37e53eabe540fb458758e198be61634bd02ee008'
    rawhash=json.loads((F/'RAW_CACHE_HASHES.json').read_text())
    for name in ['problems.json','research_results.json']:
        row=next(x for x in rawhash if x['absolute_path'].endswith('/'+name))
        assert row['bytes']==manifest['files'][name]['bytes'] and row['sha256']==manifest['files'][name]['sha256']
    raw=json.loads((R/'unsolved_math_prioritization/cache/problems.json').read_bytes())
    selected=[x for x in raw if x['id']==30000671]
    assert selected==[record['record']]
    duplicate_ids=[x['id'] for x in raw if x['id']!=30000671 and x.get('clean_statement',x.get('statement'))==record['record']['clean_statement']]
    join=json.loads((F/'RAW_PRIOR_REPORT_JOIN.json').read_text())
    assert join['raw_research_results_key_present'] is False and join['sql_report_literal']=='{}'
    assert record['research_result_for_code'] is None
    diff=(F/'FULL_PR_DIFF.patch').read_text()
    headers=re.findall(r'^diff --git a/(\S+) b/(\S+)$',diff,re.M)
    assert len(headers)==12 and all(a==b for a,b in headers)
    assert {x[1] for x in headers}=={x['repo_path'] for x in a['files']}|{'unsolved_math_prioritization/QUEUE.md'}
    queue=diff.split('diff --git a/unsolved_math_prioritization/attempts/')[0]
    added=[x for x in queue.splitlines() if x.startswith('+|')]
    removed=[x for x in queue.splitlines() if x.startswith('-|')]
    assert len(added)==len(removed)==1 and '30000671 / OWR-1453-004' in added[0] and '| already_solved | 0/5 |' in added[0]
    original=(F/'original_status_before_review.md').read_bytes()
    assert sha(original)==rev['original_artifact_sha256']
    final=(old/'SOURCE_STATUS.md').read_bytes()
    oldlines=original.splitlines(keepends=True);newlines=final.splitlines(keepends=True)
    assert len(oldlines)==len(newlines)
    changed=[i for i,(x,y) in enumerate(zip(oldlines,newlines)) if x!=y]
    assert changed==[2]
    assert newlines[2].endswith(b'Separate adversarial source review passed; see [the report](review/REVIEW.md).\n')
    fresh=json.loads((F/'FRESH_PRIMARY_DOWNLOAD.json').read_text())
    assert fresh['pdf_sha256']==json.loads((old/'source_checksums.json').read_text())['original_report']['sha256']
    summary={'schema':'pr53-original-source-integrity/v1','status':'PASS','authenticated_original_files':11,'complete_diff_files':12,'original_attempt_budget':{'used':0,'maximum':5,'turn_file_bytes':0},'author_math_checkers_present':False,'historical_author_checker_reproduction':'not applicable; the original PR contains no computation or executable proof checker','source_status_correction_only':True,'counterexample_construction_independently_verified':False,'full_2008_article_inspected':False,'raw_report_absence_precision_confirmed':True,'exact_statement_other_ids':duplicate_ids,'duplicate_search_scope':'literal full clean-statement equality in the pinned raw problem JSON; absence is not a semantic-duplicate theorem','metadata_only_change_verified':True,'native_state_or_git_writes':False}
    p=F/'ORIGINAL_SCOPE_CHECKS.json';assert not p.exists();p.write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))
if __name__=='__main__':main()
