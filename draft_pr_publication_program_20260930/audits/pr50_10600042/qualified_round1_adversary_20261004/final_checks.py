from pathlib import Path
import datetime,hashlib,json
base=Path(__file__).resolve().parent;audit=base.parent;package=audit/'publication_package_v3'
pin=lambda b:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
initial=json.loads((base/'INPUT_PINS.json').read_text())
assert {n:pin((package/n).read_bytes()) for n in initial['qualified_inputs']}==initial['qualified_inputs']
commands=base/'private/commands'
captures={}
completed_names=('inspect_inputs','portable_checker','rebuild_archive','render_pdf','distinct_controls',
 'standalone_recompile','pdf_info','render_rebuilt','prepare_mutant','zero_shift_mutant')
for name in completed_names:
    p=commands/name
    record=json.loads((p/'CAPTURE.json').read_text())
    assert record['completed'] and record['exit_code']==(1 if p.name=='zero_shift_mutant' else 0)
    for stream in ('stdout','stderr'): assert pin((p/(stream+'.bin')).read_bytes())==record[stream]
    captures[p.name]=record
assert (commands/'portable_checker/stdout.bin').read_bytes()==(package/'expected_results.json').read_bytes()
assert (base/'private/extracted/even-strand-markov-verification-v3.zip').read_bytes()==(package/'even-strand-markov-verification-v3.zip').read_bytes()
assert b'primary literal unrestricted left index shift' in (commands/'zero_shift_mutant/stderr.bin').read_bytes()
assert json.loads((commands/'distinct_controls/stdout.bin').read_text())['checks']==17266
pages=[]
for n in range(1,6):
    current=base/f'private/page-{n}.png';rebuilt=base/f'private/rebuilt-{n}.png'
    assert current.read_bytes()==rebuilt.read_bytes()
    pages.append({'page':n,'png':pin(current.read_bytes()),'rebuilt_pixels_identical':True,'reviewer_personally_viewed_current_page':True})
assert not (base/'private/page-6.png').exists()
old=audit/'qualified_publication_20261004/preauthorization_snapshot/even_strand_markov.tex.before-qualification'
assert old.is_file()
oldproof=old.read_text().split('\\section{Scope and conventions}')[1].split('\\section{Double moves')[0]
newproof=(package/'even_strand_markov.tex').read_text().split('\\section{Scope and conventions}')[1].split('\\section{Double moves')[0]
assert oldproof==newproof
v=json.loads((package/'VERIFICATION_RECORD.json').read_text())
assert v['manuscript_provenance']['submission_tex_binding']==initial['qualified_inputs']['even_strand_markov.tex']
assert v['checker_binding']==pin((package/'verify_even_calculus.py').read_bytes())
assert v['expected_result_binding']==pin((package/'expected_results.json').read_bytes())
prior=audit.parent/'pr45_9900007/root_pr50_v3_checker_actual_capture'
actual=json.loads((prior/'CAPTURE.json').read_text())
claim=v['actual_completed_run']
assert actual['pid']==claim['child_pid']==76825 and actual['exit_code']==claim['exit_code']==0
assert actual['started_utc']==claim['operator_interval_utc']['started'] and actual['finished_utc']==claim['operator_interval_utc']['finished']
assert (prior/'stdout.bin').read_bytes()==(package/'expected_results.json').read_bytes()
assert len((prior/'stderr.bin').read_bytes())==0
assert v['priority_review']['novelty_certified'] is False and v['priority_review']['fuller_Nencka_bodies_accessed'] is False
primary=audit/'current_promotion_adversary_20261004/private'
source_names=['gks.pdf','kamada.pdf','kl.pdf','survey.pdf','survey_publisher_correct.pdf','gks_page5.png','kamada_page4.png','kamada_page5.png','kamada_page6.png','kamada_page7.png','kl_page30.png','survey_page34.png','survey_publisher_correct_page29.png','nencka_scan_153.webp','nencka_scan_154.webp','nencka_scan_004.webp','fiedler_crossref.json']
sources={name:pin((primary/name).read_bytes()) for name in source_names}
original_sources=json.loads((audit/'original/source_manifest.json').read_text())['pdfs']
mapping={'survey.pdf':'survey.pdf','survey-published.pdf':'survey_publisher_correct.pdf','kamada.pdf':'kamada.pdf','lmove.pdf':'kl.pdf'}
for row in original_sources: assert sources[mapping[row['name']]]=={'bytes':row['bytes'],'sha256':row['sha256']}
record={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_FINAL_BINDINGS_REPRODUCTION_PIXELS_AND_PROVENANCE',
 'captures':captures,'PDF_pages':pages,'primary_source_inputs':sources,'main_mathematical_proof_unchanged_by_qualification':True,
 'published_payload_still_exact_initial_pins':True,'no_new_central_proof_attempt':True,'qualified_review_completion_percent':95,
 'priority_certified':False,'fuller_Nencka_bodies_accessed':False,'release_verdict_pending_final_report':True}
(base/'FINAL_CHECKS.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':record['status'],'capture_count':len(captures),'all_five_PDF_pixels_exact_rebuilt':True,
 'primary_sources_pinned':len(sources),'qualification_changes_main_proof':False,'priority_certified':False},indent=2))
