"""Source-only integrity checks; does not certify mathematics or priority."""
import datetime,hashlib,json,pathlib,stat
F=pathlib.Path(__file__).absolute().parent
R=F.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def mode(p):return format(stat.S_IMODE(p.stat().st_mode),'04o')
def read(rel):return json.loads((F/rel).read_bytes())
def check_sources():
    assert F==R/'draft_pr_publication_program_20260930/audits/pr55_30006309/priority_adversary_family'
    for row in read('EXTERNAL_REFERENCES.json')['files']:
        p=R/row['repo_path'];b=p.read_bytes()
        assert p.is_file() and not p.is_symlink() and len(b)==row['bytes'] and sha(b)==row['sha256'] and mode(p)==row['mode']
    v=read('VERDICT.json')
    assert v['candidate_sha256']=='4931eccbb464b53af07b90e24b72060e681b9a7f1769c0030a9d7090e59b129c'
    assert v['exact_prior_full_candidate_mechanism_located'] is False and v['root_acceptance'] is False and v['native_changes'] is False
    assert v['third_fresh_math_adversary_credit'] is False and v['search_complete_or_exhaustive'] is False
    c=read('primary_retrieval_actual_capture/RESULT.json');s=read('primary_retrieval_actual_capture/START.json')
    assert c['child_pid']==s['child_pid']==read('PRIMARY_RETRIEVAL_METADATA.json')['actual_pid'] and c['returncode']==0 and c['is_root_closure'] is False
    assert datetime.datetime.fromisoformat(c['started_utc'])<=datetime.datetime.fromisoformat(c['finished_utc'])
    for name in ['stdout','stderr']:
        b=(F/'primary_retrieval_actual_capture'/f'{name}.txt').read_bytes()
        assert len(b)==c[f'{name}_bytes'] and sha(b)==c[f'{name}_sha256']
    results=read('PRIMARY_RETRIEVAL_METADATA.json')['results']
    assert len(results)==14 and all(x['http_status']==200 and x['body_retained'] is False for x in results)
    for rel in ['GKZ_FRESH_RETRIEVAL_METADATA.json','GKZ_FRESH_ASSUMPTIONS_RETRIEVAL_METADATA.json']:
        b=read(rel)
        assert b['pdf_sha256']=='82ab9c39254384e439933004d52e04b9959b0f9699b778bd9f6a1b2306b2ca9a' and b['pdf_bytes']==21689298
        assert b['pdf_or_whole_book_retained'] is False and b['selected_book_text_persisted'] is False and b['root_authority'] is False
    for p in F.rglob('*'):
        assert not p.is_symlink()
        if p.is_file():assert p.suffix.lower() not in ['.pdf','.png','.jpg','.sqlite','.db']
    for rel in ['REPORT.md','ESTEROV_SPECIALIZATION.md','SOURCE_LEDGER.md','FRAMING_SOURCE.md','RESEARCH_LOG.md']:
        assert (F/rel).is_file() and (F/rel).stat().st_size>0
    return len(read('EXTERNAL_REFERENCES.json')['files'])
if __name__=='__main__':
    n=check_sources()
    print(json.dumps({'status':'PASS_SOURCE_PRIORITY_PREPARATION_ONLY','external_files_verified':n,'primary_metadata_bodies':14,'mathematical_assertions_certified':None,'priority_cleared':False,'root_acceptance':False,'native_changes':False}))
