"""Build a lean operative SOURCE package from genuinely closed PR53 evidence."""
import argparse,datetime,hashlib,json,os,pathlib,shutil,stat,subprocess,sys
F=pathlib.Path(__file__).resolve().parent
A=F.parent
R=A.parents[2]
A45=A.parent/'pr45_9900007'
ORIGINAL='d10783bb3d60becaa765d36a5cd5ff303c978049b9527266a2be4b2dc92f49b7'
LOCAL='2058e9c0b5cdb98f270610a46cd40acb3b71b31df44a3103b9aa544be5e1fdf7'
def sha(b):return hashlib.sha256(b).hexdigest()
def mode(p):return format(stat.S_IMODE(p.stat().st_mode),'04o')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(rel,b):
    p=F/rel;p.parent.mkdir(parents=True,exist_ok=True);assert not p.exists(),str(p);p.write_bytes(b)
def jw(rel,x):write(rel,(json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
def row(p):
    b=p.read_bytes();return {'repo_path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'mode':mode(p)}
def bind_family(name,expected):
    d=A/name;p=d/'MANIFEST.json';assert p.exists() and sha(p.read_bytes())==expected
    j=json.loads(p.read_bytes());assert j.get('root_approval') is False
    indexed=j.get('files',j.get('payload_rows'))
    assert type(indexed) is list
    payload=[x for x in indexed if x['path']!='MANIFEST.json']
    actual=sorted(q.relative_to(d).as_posix() for q in d.rglob('*') if q.is_file())
    assert actual==sorted([x['path'] for x in payload]+['MANIFEST.json'])
    for x in payload:
        q=d/x['path'];b=q.read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'] and mode(q)==x['mode']
    dirs=sorted('.' if q==d else q.relative_to(d).as_posix() for q in [d,*d.rglob('*')] if q.is_dir())
    assert not any(q.is_symlink() for q in [d,*d.parents,*d.rglob('*')])
    manifest_dirs=sorted(j['directories'])
    assert dirs==manifest_dirs or dirs==sorted(['.']+manifest_dirs)
    if 'directory_mode' in j:assert all(mode(d if rel=='.' else d/rel)==j['directory_mode'] for rel in dirs)
    return {'family':name,'manifest_sha256':expected,'rows':[row(d/rel) for rel in actual],'directories':[{'repo_path':(d if rel=='.' else d/rel).relative_to(R).as_posix(),'mode':mode(d if rel=='.' else d/rel)} for rel in dirs]}
def bind_root(name,family,expected,kind):
    d=A45/name;c=json.loads((d/'CAPTURE.json').read_bytes())
    assert c['actual_execution'] is True and c['completed'] is True and c['exit_code']==0 and c['status']=='PASS'
    assert type(c['pid']) is int and c['pid']>0 and c['cwd']==str(R)
    start=datetime.datetime.fromisoformat(c['started_utc']);end=datetime.datetime.fromisoformat(c['finished_utc']);assert start<=end
    assert str(A/family/('close_for_ROOT.py' if kind=='close' else 'verify_closed_readonly.py')) in c['argv']
    if kind=='read':assert c['argv'][-1]==expected
    for stream in ['stdout','stderr']:
        x=c[stream];b=(d/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']
    op=d/'prelaunch_operator.py';assert sha(op.read_bytes())==c['operator_sha256'] and c['operator_unchanged'] is True
    out=json.loads((d/'stdout.bin').read_bytes())
    assert expected in out.values(),(name,'actual output does not bind manifest')
    assert out.get('root_approval') is False
    return {'family':family,'kind':kind,'capture':name,'pid':c['pid'],'started_utc':c['started_utc'],'finished_utc':c['finished_utc'],'argv':c['argv'],'manifest_sha256':expected,'rows':[row(q) for q in sorted(d.iterdir()) if q.is_file()]}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--model-manifest-sha',required=True);ap.add_argument('--model-close-name',required=True);ap.add_argument('--model-read-name',required=True);ap.add_argument('--local-read-name',required=True);args=ap.parse_args()
    assert len(args.model_manifest_sha)==64
    for rel in ['EXTERNAL_REFERENCES.json','SCIENCE_INDEX.json','READY.json','FIXED_PAYLOAD_INDEX.json','MANIFEST.json']:assert not (F/rel).exists()
    original=A/'original_preparation_family';local=A/'local_ring_adversary_family';model=A/'model_theory_scope_adversary_family'
    families=[bind_family('original_preparation_family',ORIGINAL),bind_family('local_ring_adversary_family',LOCAL),bind_family('model_theory_scope_adversary_family',args.model_manifest_sha)]
    capture_specs=[('root_pr53_original_preparation_closure_actual_capture','original_preparation_family',ORIGINAL,'close'),('root_pr53_original_preparation_closed_readback_actual_capture','original_preparation_family',ORIGINAL,'read'),('root_pr53_local_ring_adversary_closure_actual_capture','local_ring_adversary_family',LOCAL,'close'),(args.local_read_name,'local_ring_adversary_family',LOCAL,'read'),(args.model_close_name,'model_theory_scope_adversary_family',args.model_manifest_sha,'close'),(args.model_read_name,'model_theory_scope_adversary_family',args.model_manifest_sha,'read')]
    roots=[bind_root(*x) for x in capture_specs]
    for family in ['original_preparation_family','local_ring_adversary_family','model_theory_scope_adversary_family']:
        pair=[x for x in roots if x['family']==family];assert len(pair)==2
        assert datetime.datetime.fromisoformat(pair[0]['finished_utc'])<=datetime.datetime.fromisoformat(pair[1]['started_utc'])
    for d in [local,model]:
        v=json.loads((d/'VERDICT.json').read_bytes())
        assert v['root_approval'] is False
        assert v.get('verdict','').startswith('PASS')
        for key in ['mandatory_mathematical_corrections','mandatory_corrections','mandatory_repairs']:
            if key in v:assert type(v[key]) is list and not v[key]
    ext={'schema':'pr53-current-inplace-closed-inputs/v1','closed_families':families,'actual_root_captures':roots,'root_approval':False,'no_corpus_copies':True,'evidence_scope':'whole closed bodies in place; private source references remain private, not operative publication contents'}
    jw('EXTERNAL_REFERENCES.json',ext)
    auth=json.loads((original/'GITHUB_AUTHENTICATION.json').read_bytes())
    for x in auth['files']:
        rel=x['archive_path'].removeprefix('original_archive/') if hasattr(str,'removeprefix') else x['archive_path'][len('original_archive/'):]
        b=(original/x['archive_path']).read_bytes();write('original_archive/'+rel,b)
        assert len(b)==x['bytes'] and sha(b)==x['sha256']
    qual=(original/'SOURCE_PRECISION_QUALIFICATIONS.md').read_text()
    qual+='\nThis operative package is prepared by the original preparer after consulting the two distinct fresh reviews. It is not a third independent mathematical review. The original source_record record is preserved as historical imported metadata, including its erroneous open-status triage; operative classification is already_solved for the credited prior negative answer.\n\nAll original model/time-window/review events remain historical. New universal boundary proofs establish their stated conditional or special-case claims and do not reconstruct Gabber examples or the full algebraic-residue-field theorem. No counterexample test count is invented. Genuine ROOT custody closure/readback is not ROOT mathematical acceptance.\n'
    write('science/GLOBAL_QUALIFICATIONS.md',qual.encode())
    for rel in ['source_checksums.json','turns.jsonl']:
        write('science/'+rel,(original/'original_archive'/rel).read_bytes())
    rec=json.loads((original/'original_archive/source_record.json').read_bytes())
    rec['operative_audit']={'imported_record_retained_unchanged':True,'imported_open_status_and_2026_triage_are_historical_and_incorrect_for_unrestricted_target':True,'recommended_status':'already_solved','prior_answer':'negative','credit':'Ofer Gabber, as reported by Lou van den Dries','raw_report_key_present':False,'selected_sql_report_type':'TEXT, non-NULL','selected_sql_report_literal':'{}','archived_null_is_absence_marker':True,'historical_counterexample_proof_independently_reconstructed':False,'full_2008_article_read':False,'current_integral_domain_status':'not assessed','qualifications':'GLOBAL_QUALIFICATIONS.md','root_approval':False}
    jw('science/source_record.json',rec)
    status=(original/'original_archive/SOURCE_STATUS.md').read_text()
    old='Separate adversarial source review passed; see [the report](review/REVIEW.md).'
    new='The historical source review and two fresh distinct review families support this source-status correction; their scope is recorded in [the current review wrapper](review/REVIEW.md). The historical counterexample construction remains unverified. [Global qualifications](GLOBAL_QUALIFICATIONS.md) govern the imported metadata and absence markers.'
    assert status.count(old)==1;status=status.replace(old,new)
    write('science/SOURCE_STATUS.md',status.encode())
    write('science/README.md',('''# Complete local rings: credited prior negative answer

The unrestricted question in 30000671 / OWR-1453-004 had a reported negative answer in its original source. Recommend already_solved with Gabber credited, zero new substantive attempts, and no new preprint.

[Exact target and source status](SOURCE_STATUS.md), [global qualifications](GLOBAL_QUALIFICATIONS.md), [source audit](SOURCE_AUDIT.md), and [review scope](review/REVIEW.md) state the operative limits. [Pinned record plus audit metadata](source_record.json) preserves the imported record without treating its erroneous open label as operative status.

[Boundary proofs](BOUNDARY_PROOFS.md) and [inverse-system audit](INVERSE_SYSTEM_SCOPE.md) are credited first-party verification support from two distinct new reviewers. They do not reconstruct Gabber's examples or the full 2008 proof. The domain-restricted question's current status is unassessed. No human peer review or formal verification is claimed. ROOT acceptance and native transitions remain pending.
''').encode())
    audit='''# Operative source audit

This SOURCE package corrects the imported status of the exact unrestricted complete-local-Noetherian-ring question. It imports the original source testimony with the proof-access limits in SOURCE_STATUS.md, and carries GLOBAL_QUALIFICATIONS.md throughout.

The raw research-results dictionary has no OWR-1453-004 key. Selected SQLite report is non-NULL TEXT containing literal "{}". The original null markers serialize absence; they do not describe present JSON-null data or SQL NULL. The imported source record and its open-status triage are preserved as historical dataset metadata; the operative recommendation is already_solved.

The original PR changes eleven attempt files and its QUEUE.md row. The old source gate's statement that shared queue/state were untouched is stage-specific, not a description of the final diff. No new substantive proof attempts were made: original readiness records 0/5 and original turns.jsonl is empty. No separate original assistant-response count is inferred.

The original official report's relevant contribution was freshly read and viewed by the preparer and checked by two distinct new reviewers. The 2008 institutional abstract corroborates prior credit; the full article and construction were not proof-audited. Finite residue fields, compatible limits, Artinian boundaries, and abstract inverse-system countermodels are independently checkable scope support, not historical ring counterexamples.

The two new reviews and real ROOT custody closures/readbacks are bound in the preparation evidence ledger. Those command records are not mathematical acceptance. No source PDF, image, raw cache, database, or command-capture corpus is copied into these operative science files. No external person was contacted. No present-day domain-case openness, new discovery, new paper, preprint, DOI, or publication is asserted.
'''
    write('science/SOURCE_AUDIT.md',audit.encode())
    for rel,d,source in [('BOUNDARY_PROOFS.md',local,'INDEPENDENT_BOUNDARY_PROOFS.md'),('INVERSE_SYSTEM_SCOPE.md',model,'INVERSE_SYSTEM_PROOF.md')]:
        header='# Credited verification support\n\nCopied from the closed first-party review source `'+str((d/source).relative_to(R))+'`, SHA-256 '+sha((d/source).read_bytes())+'. This is reused reviewer evidence, not a new independent review by the operative preparer. Historical preparation/completion labels in the source remain historical. Its deductions do not reconstruct Gabber counterexamples.\n\n'
        write('science/'+rel,(header+(d/source).read_text()).encode())
    report='''# Operative mathematical review wrapper

Recommend already_solved for the unrestricted original question, crediting the prior negative answer. This wrapper synthesizes the historical source review and two fresh, materially distinct reviewer families. It is written by the original preparer and is not a third independent review.

The local-ring family proves compatible-limit, finite-residue, Artinian, arbitrary bounded-truncation, and finite-length distinctions. The inverse-system/model-theory family independently proves the finite branching boundary and identifies why nonempty levels or logical compactness do not supply maps inside the original rings without a realization/descent argument. Their small supporting computation is bounded evidence for stated examples; it is neither Gabber reconstruction nor proof of the full algebraic-residue-field theorem.

The original report explicitly states the credited negative answer, and the institutional 2008 abstract corroborates it. SOURCE_STATUS.md preserves the exact unrestricted hypotheses and historical source limits. The original report does not supply defining counterexample rings and their all-order quotient maps/nonisomorphism invariant; the full 2008 article is unavailable. No current integral-domain result is inferred.

GLOBAL_QUALIFICATIONS.md applies to every historical source marker and model/review claim: absent raw report key, non-NULL SQL TEXT "{}", serialized null absence marker, eleven attempt files plus QUEUE.md, and no invented original response count/checker. The imported open-status triage is retained as historical source metadata but explicitly corrected operatively.

No mandatory mathematical issue was found by the two fresh review families. The source-only disposition is ready for ROOT's reconciliation, not yet accepted or merged. Original budget remains 0/5; no new proof-search turn, paper, preprint, DOI, human peer review, formal proof certificate, or counterexample reconstruction is claimed.

Closed evidence source paths, which already exist in this repository:

- `draft_pr_publication_program_20260930/audits/pr53_30000671/original_preparation_family/REPORT.md`
- `draft_pr_publication_program_20260930/audits/pr53_30000671/local_ring_adversary_family/REPORT.md`
- `draft_pr_publication_program_20260930/audits/pr53_30000671/model_theory_scope_adversary_family/REPORT.md`

Operative links: [exact statement](../SOURCE_STATUS.md), [global qualifications](../GLOBAL_QUALIFICATIONS.md), [boundary proofs](../BOUNDARY_PROOFS.md), [inverse-system scope](../INVERSE_SYSTEM_SCOPE.md). No anticipated future canonical evidence path is represented as present.
'''
    write('science/review/REVIEW.md',report.encode())
    verdict={'schema':'pr53-operative-review-wrapper/v1','problem_id':30000671,'problem_code':'OWR-1453-004','verdict':'PASS_SOURCE_STATUS_PREPARATION','recommended_status':'already_solved','prior_answer':'negative','counterexample_credit':'Ofer Gabber, as reported by Lou van den Dries','original_substantive_attempts':0,'maximum_original_attempts':5,'new_proof_search_turns':0,'separate_original_response_count_inferred':False,'fresh_distinct_review_families':2,'third_independent_review_by_preparer':False,'historical_construction_independently_reproduced':False,'full_2008_article_read':False,'current_integral_domain_status':'not assessed','new_discovery':False,'new_paper_recommended':False,'root_approval':False,'native_or_git_writes':False,'global_qualifications':'../GLOBAL_QUALIFICATIONS.md'}
    jw('science/review/review_summary.json',dict(verdict,artifact='../SOURCE_STATUS.md',artifact_sha256=sha((F/'science/SOURCE_STATUS.md').read_bytes()),report_sha256=sha((F/'science/review/REVIEW.md').read_bytes())))
    jw('science/review/source_verification.json',{'schema':'pr53-operative-source-precision/v1','raw_report_key_present':False,'selected_sql_report_type':'TEXT, non-NULL','selected_sql_report_literal':'{}','archived_null_marks_absence':True,'imported_record_is_historical':True,'operative_prior_answer':'negative','source_status_correction_only':True,'original_archive_untouched':True,'closed_source_families':[{'family':x['family'],'manifest_sha256':x['manifest_sha256']} for x in families],'genuine_root_custody_events':[{'family':x['family'],'kind':x['kind'],'pid':x['pid'],'started_utc':x['started_utc'],'finished_utc':x['finished_utc']} for x in roots],'mathematical_acceptance':False,'root_approval':False,'construction_proof_verified':False,'full_article_read':False,'private_reference_not_publication_content':True,'qualifications':'../GLOBAL_QUALIFICATIONS.md'})
    readiness=json.loads((original/'original_archive/readiness.json').read_bytes())
    readiness['artifact_sha256']=sha((F/'science/SOURCE_STATUS.md').read_bytes())
    readiness['independent_review']={'verdict':'PASS_SOURCE_STATUS_PREPARATION','report':'review/REVIEW.md','report_sha256':sha((F/'science/review/REVIEW.md').read_bytes()),'required_corrections':[],'fresh_distinct_review_families':2,'scope':'credited source-status correction, not historical-construction proof'}
    readiness['operative_qualifications']='GLOBAL_QUALIFICATIONS.md'
    readiness['root_approval']=False
    readiness['original_model_and_window_are_historical_metadata']=True
    readiness['raw_prior_report_absent']=True
    readiness['new_substantive_proof_attempts']=0
    readiness['no_new_paper']=True
    jw('science/readiness.json',readiness)
    log=(original/'original_archive/RESEARCH_LOG.md').read_text()+'\n## '+now()+': operative source preparation\n\nThe exact original archive remains preserved. Absent prior-report semantics, imported open triage, final diff scope, and historical versus new-review authority are now qualified globally. Two fresh distinct reviewer families are genuinely closed and separately read back; their elementary boundary proofs are reused with credit. No historical counterexample or full 2008 proof is certified, no present-day domain-case conclusion is made, and no new paper is prepared. ROOT mathematical acceptance is pending. Original substantive budget remains 0/5; no separate response count is inferred. Operative preparation estimate: 100%.\n'
    write('science/RESEARCH_LOG.md',log.encode())
    jw('VERDICT.json',verdict)
    science=[]
    for p in sorted((F/'original_archive').rglob('*'))+sorted((F/'science').rglob('*')):
        if p.is_file():science.append({'path':p.relative_to(F).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'category':'original_archive' if 'original_archive' in p.parts else 'operative_science'})
    assert len(science)==25
    jw('SCIENCE_INDEX.json',{'schema':'pr53-lean-science-index/v1','files':science,'original_archive_files':11,'operative_science_files':14,'no_production_promotion_performed':True})
    write('REPORT.md',('''# Lean operative PR53 preparation

Original eleven archive bodies are exact; fourteen operative science files repair provenance and final diff wording and add two small credited proof supports. Global qualifications correct absent report semantics and explicitly distinguish the imported erroneous open triage from already_solved as the operative recommendation.

Three closed families and six actual ROOT closure/readback captures are bound as whole-body references in place. Their custody is not mathematical acceptance. No PDF, pixel, SQL/raw cache, or command corpus is copied here. Two fresh review routes found no mandatory mathematical correction, with the full historical counterexample construction and 2008 proof still unverified and current domain restriction unassessed.

This is the original preparer's synthesis, not a third independent mathematical review. Original 0/5 and empty turn file are preserved; no original response count or author checker is invented. No native/Git acceptance, paper, preprint, upload, DOI, or outside contact occurred. ROOT must inspect source and perform its own absent-only closure and separate readback before any promotion.

Preparation estimate: 100% of operative SOURCE handoff; no ROOT approval.\n''').encode())
    write('accepted_pr_body_draft.md',((original/'accepted_pr_body_draft.md').read_text()+'\nTwo fresh distinct AI review families independently checked the source scope and elementary boundary arguments. Their whole closed evidence and genuine ROOT custody readbacks are bound in the operative preparation. These reviews do not reconstruct Gabber\'s historical construction, confer human peer review/formal verification, or claim a third independent review by the preparer. ROOT acceptance remains pending.\n').encode())
    write('RESEARCH_LOG.md',('# Operative preparation log\n\n'+now()+': Built current SOURCE from genuinely closed original/local-ring/model-theory families and six real ROOT custody captures. Preparation estimate 90%, pending own complete source/custody check and absent-manifest freeze. No native or Git writes; no original proof-search budget change.\n').encode())
    d=F/'actual_preparation_check';d.mkdir()
    operator=pathlib.Path(__file__).read_bytes();child=(F/'verify_current.py').read_bytes()
    (d/'prelaunch_operator.py').write_bytes(operator);(d/'prelaunch_child.py').write_bytes(child)
    argv=['/usr/bin/python3','-B',str(F/'verify_current.py')]
    start=now();p=subprocess.Popen(argv,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();end=now()
    (d/'stdout.bin').write_bytes(out);(d/'stderr.bin').write_bytes(err)
    cap={'schema':'pr53-current-actual-preparation-check/v1','pid':p.pid,'argv':argv,'cwd':str(R),'started_at':start,'completed_at':end,'exit_code':p.returncode,'operator_sha256':sha(operator),'child_sha256':sha(child),'operator_unchanged':pathlib.Path(__file__).read_bytes()==operator,'child_unchanged':(F/'verify_current.py').read_bytes()==child,'stdout':{'path':'stdout.bin','bytes':len(out),'sha256':sha(out)},'stderr':{'path':'stderr.bin','bytes':len(err),'sha256':sha(err)}}
    (d/'CAPTURE.json').write_text(json.dumps(cap,indent=2)+'\n')
    assert p.returncode==0,(p.returncode,err.decode())
    with (F/'RESEARCH_LOG.md').open('a') as stream:stream.write(end+': Actual child PID '+str(p.pid)+' passed complete preparation verification; full streams retained. Preparation estimate 100%; ROOT closure still absent.\n')
    for q in F.rglob('*'):
        assert not q.is_symlink()
        if q.is_file():os.chmod(q,0o444)
        else:assert q.is_dir();os.chmod(q,0o755)
    os.chmod(F,0o755)
    files=[{'path':q.relative_to(F).as_posix(),'bytes':q.stat().st_size,'sha256':sha(q.read_bytes()),'mode':'0444'} for q in sorted(F.rglob('*')) if q.is_file()]
    dirs=sorted('.' if q==F else q.relative_to(F).as_posix() for q in [F,*F.rglob('*')] if q.is_dir())
    assert len(files)+2<=45
    assert sum(x['bytes'] for x in files)<1024*1024
    jw('FIXED_PAYLOAD_INDEX.json',{'schema':'pr53-current-prepared-index/v1','files':files,'directories':dirs});os.chmod(F/'FIXED_PAYLOAD_INDEX.json',0o444)
    jw('READY.json',{'schema':'pr53-current-source-ready/v1','recorded_at':now(),'payload_files':len(files)+2,'payload_bytes_excluding_index_ready':sum(x['bytes'] for x in files),'fixed_index_sha256':sha((F/'FIXED_PAYLOAD_INDEX.json').read_bytes()),'science_index_sha256':sha((F/'SCIENCE_INDEX.json').read_bytes()),'report_sha256':sha((F/'REPORT.md').read_bytes()),'verdict_sha256':sha((F/'VERDICT.json').read_bytes()),'external_references_sha256':sha((F/'EXTERNAL_REFERENCES.json').read_bytes()),'manifest_absent_at_handoff':True,'root_approval':False,'original_substantive_attempts':0,'new_proof_search_turns':0,'new_paper':False,'required_math_corrections':[],'preparation_percent':100});os.chmod(F/'READY.json',0o444)
    from closed_scope_common import verify_prepared
    verify_prepared(False)
    print(json.dumps({'status':'SOURCE_READY_UNCLOSED','payload_files':len(files)+2,'payload_bytes_excluding_index_ready':sum(x['bytes'] for x in files),'actual_preparation_child_pid':p.pid,'manifest_absent':True,'root_approval':False,'fixed_index_sha256':sha((F/'FIXED_PAYLOAD_INDEX.json').read_bytes())}))
if __name__=='__main__':main()
