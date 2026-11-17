"""Passive original-only INITIAL closure; never imports intake or any source program."""
import datetime, hashlib, json, os, stat
from pathlib import Path

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
SRC=P/'papers/23204212/sources'
OWN=P/'papers/23204212/reviews/scope-sol'
TERMINALS={'INITIAL_MANIFEST.json','INITIAL_SEAL.json'}
def pin(p):
    a=p.lstat();assert stat.S_ISREG(a.st_mode) and not p.is_symlink()
    raw=p.read_bytes();z=p.lstat();fields=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mode,s.st_mtime_ns,s.st_ctime_ns)
    assert fields(a)==fields(z) and len(raw)==z.st_size
    return dict(bytes=len(raw),SHA256=hashlib.sha256(raw).hexdigest(),MD5=hashlib.md5(raw).hexdigest(),mode=oct(stat.S_IMODE(a.st_mode)))
def census(root):
    files,dirs={},{'.':oct(stat.S_IMODE(root.lstat().st_mode))};todo=[root]
    while todo:
        here=todo.pop();a=here.lstat();assert stat.S_ISDIR(a.st_mode) and not here.is_symlink()
        for p in sorted(here.iterdir()):
            n=p.relative_to(root).as_posix();s=p.lstat();assert not p.is_symlink()
            if stat.S_ISDIR(s.st_mode):dirs[n]=oct(stat.S_IMODE(s.st_mode));todo.append(p)
            else:files[n]=pin(p)
        z=here.lstat();assert (a.st_dev,a.st_ino,a.st_mode,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_mtime_ns,z.st_ctime_ns)
    return dict(root=str(root),root_mode=dirs['.'],files=files,directories={n:m for n,m in dirs.items() if n!='.'},hidden_paths=[n for n in sorted(set(files)|set(dirs)) if n!='.' and any(x.startswith('.') for x in n.split('/'))],empty_files=[n for n,v in sorted(files.items()) if v['bytes']==0],empty_directories=[n for n in sorted(dirs) if n!='.' and not any(x.startswith(n+'/') for x in set(files)|set(dirs))])
def read(n):return json.loads((OWN/n).read_bytes())
def write(n,data):
    with (OWN/n).open('x') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')
assert not any((OWN/n).exists() for n in TERMINALS)
before,after=read('SOURCE_BEFORE.json'),read('SOURCE_AFTER.json')
final=census(SRC);assert before==after==final and len(final['files'])==55 and len(final['directories'])==14
receipt=read('INTAKE_RECEIPT.json');assert pin(OWN/'intake.py')==receipt['own_reader']
assert all(x['exit_code']==0 for x in receipt['Poppler_calls'])
assert (OWN/'INTAKE.stderr.txt').stat().st_size==0
for i in range(1,5):
    assert pin(OWN/('native-page-'+str(i)+'.txt'))==receipt['fresh_page_texts'][str(i)]
    assert pin(OWN/('pixels/native-page-'+str(i)+'.png'))==receipt['fresh_page_pixels'][str(i)]
archives=read('ARCHIVE_PATH_CENSUS.json')['archives']
for archive in archives:
    names=[m['path'].rstrip('/') for m in archive['members']]
    assert len(names)==len(set(names))
    file_names={m['path'] for m in archive['members'] if not m['is_directory']}
    for n in names:
        parts=n.split('/')
        assert not any('/'.join(parts[:i]) in file_names for i in range(1,len(parts)))
write('SOURCE_FINAL_GUARD.json',final)
tex=SRC/'archives/02-thompson-cstar-source.zip.extracted/main.tex'
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
api=json.loads((SRC/'native-metadata/record-api.json').read_bytes())
coverage=dict(schema='independent-original-only-coverage-v1',UTC=utc,record_id='23204212',original_TeX=dict(path=str(tex.relative_to(P)),**pin(tex),physical_lines=len(tex.read_bytes().splitlines()),full_personal_read=True),outer_PDF=dict(path='papers/23204212/sources/zenodo-files/paper.pdf',**final['files']['zenodo-files/paper.pdf']),fresh_text_pages_read=[1,2,3,4],fresh_pixels_individually_viewed=[1,2,3,4],page_read_notes={'1':'Title, author/date, complete abstract, group definitions, reduced algebra and trace, pinned input locator','2':'Both original theorem statements, first consequence and complete countability proof','3':'Circle consequence, scope/provenance limits, reduced/full distinction, disclosure, first bibliography entries','4':'All remaining bibliography entries and edition-numbering note'},full_native_API_personally_read=True,full_native_HTML_visible_and_metadata_personally_read=True,full_Description_personally_read=True,HTML_web_scripts_and_styles_not_executed_or_scientifically_reviewed=True,API_version_present='version' in api['metadata'],API_version=api['metadata'].get('version'),host_display_label='v1, separate from absent API version',declared_publication_date=api['metadata']['publication_date'],created=api['created'],updated=api['updated'],native_metadata_rights=api['metadata']['license'],separate_code_license_contents_not_opened=True,native_file_order=[x['key'] for x in api['files']],whole_source_files_childdirs=[55,14],all_whole_source_before_after_final_exact=True,archive_member_counts={a['name']:len(a['members']) for a in archives},native_scientific_program_body_exposure_count=0,source_support_execution_import_AST_compile_tests=0,support_audit_peer_primary_body_exposure_counts=dict(support=0,packaged_audits=0,old_reviews=0,current_peer_or_root_findings=0,primary_literature=0),INITIAL_gate_completion_percent=100,full_scientific_review_estimate_percent=20,no_verdict_or_promotional_clearance=True)
write('ORIGINAL_COVERAGE.json',coverage)
write('EXPOSURE_LEDGER.json',dict(schema='original-only-exposure-ledger-v1',UTC=utc,order=['Task identity/custody metadata and manifest filenames/byte pins','Full original main.tex and complete native API','Own passive custody reader, fresh text extraction, full native visible HTML/metadata','Fresh four PDF text pages and individually viewed four page pixels','Own conditional reconstruction and hand boundary checks'],original_claims_and_original_Description_audit_or_formal_claims_are_unverified_author_exposure=True,zero_prior_knowledge_claim=False,general_model_training_knowledge_acknowledged=True,session_specific_prior_support_peer_root_or_primary_findings_read=False,hash_only_full_source_reads_are_not_semantic_program_body_review=True,program_bodies_opened=0,programs_or_support_executed_imported_AST_compiled_tested=0,primary_documents_opened=0,old_or_current_reviews_opened=0,not_opened=['Any source verification code or audit body','Packaged support README or dependency ledger','LICENSE_CODE contents','Any OpenAI or classical primary proof','Any peer/root scientific finding'],allowed_passive_tools=['Own fully read standard-library custody/metadata readers','pdfinfo','pdftotext','pdftoppm','Individual image viewing'],source_or_Git_network_W_Sheet_mutations=False,mathematical_findings_withheld_from_root_messages=True))
write('EXECUTION_LEDGER.json',dict(UTC=utc,intake_invocations=1,intake_exit_code=0,intake_literal_stdout=pin(OWN/'INTAKE.stdout.txt'),intake_literal_stderr=pin(OWN/'INTAKE.stderr.txt'),intake_timing=receipt['started_UTC']+' to '+receipt['finished_UTC'],all_saved_owned_sources_personally_read_before_invocation=True,intake=pin(OWN/'intake.py'),seal=pin(OWN/'seal_initial.py'),Poppler_calls=receipt['Poppler_calls'],scientific_program_executions=0,failures=[]))
with (OWN/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc+' — Full original TeX/API/native HTML Description and metadata read; all four fresh PDF text pages and all four separate page pixels personally read. Own scope/dependency reconstruction and falsifiable hand controls saved. Whole source55/14 exact before/after/final; safe archive path census retained; support/scientific-code/peer/primary exposure counts0. INITIAL completion100%; estimated full scientific review20%. No verdict. Freeze and stop pending checkpoint and explicit RESUME in a separate sibling.\n')
payload=census(OWN);assert not (set(payload['files'])&TERMINALS)
names=sorted(set(payload['files'])|TERMINALS)
manifest=dict(schema='finite-independent-INITIAL-manifest-v1',UTC=utc,root=str(OWN),root_mode=payload['root_mode'],payload_files=[dict(path=n,**v) for n,v in sorted(payload['files'].items())],directories=[dict(path=n,mode=m) for n,m in sorted(payload['directories'].items())],actual_files=len(names),actual_childdirs=len(payload['directories']),hidden_paths=payload['hidden_paths'],empty_files=payload['empty_files'],empty_directories=payload['empty_directories'],terminal_control_topology=[dict(path=n,mode='0o644') for n in sorted(TERMINALS)],exact_terminal_self_hash_exclusions=sorted(TERMINALS),scope='Every actual own file/directory including hidden/empty entries, bytes and modes; only exact terminal circular/self-hash pair excluded')
write('INITIAL_MANIFEST.json',manifest)
write('INITIAL_SEAL.json',dict(schema='independent-original-only-INITIAL-seal-v1',UTC=utc,status='INITIAL_FROZEN_PENDING_CHECKPOINT_AND_EXPLICIT_RESUME',record_id='23204212',root=str(OWN),root_mode=payload['root_mode'],INITIAL_gate_completion_percent=100,full_scientific_review_estimate_percent=20,manifest=pin(OWN/'INITIAL_MANIFEST.json'),actual_files=len(names),actual_childdirs=len(payload['directories']),whole_file_names=names,directories=manifest['directories'],exact_terminal_self_hash_exclusions=sorted(TERMINALS),whole_source_files_childdirs=[55,14],source_control_pins=receipt['control_pins'],full_source_before_after_final_exact=True,controlling_outer_PDF=final['files']['zenodo-files/paper.pdf'],full_original_TeX_read=True,fresh_PDF_text_pages_read=4,fresh_PDF_pages_individually_viewed=4,full_native_API_HTML_Description_read=True,support_scientific_code_peer_primary_body_exposure_counts=[0,0,0,0],scientific_execution_import_AST_compile_tests=0,no_scientific_verdict_or_clearance=True,no_followup_decision=True,no_Git_network_W_Sheet_or_outreach_actions=True,findings_withheld_from_root_messages=True,failures=[],future_work_requires_separate_sibling_after_checkpoint_and_explicit_RESUME=True,quiescent_stop=True))
actual=census(OWN)
assert set(actual['files'])==set(names) and actual['directories']==payload['directories']
assert all(actual['files'][n]==v for n,v in payload['files'].items())
assert actual['files']['INITIAL_MANIFEST.json']==read('INITIAL_SEAL.json')['manifest']
assert all(actual['files'][n]['mode']=='0o644' for n in TERMINALS)
print(json.dumps(dict(status='INITIAL_FROZEN',files=len(names),childdirs=len(actual['directories']),source_files_childdirs=[55,14],original_TeX_lines=coverage['original_TeX']['physical_lines'],PDF_text_pages_read=4,PDF_pixels_individually_viewed=4,code_support_peer_primary_exposure_counts=[0,0,0,0],full_review_estimate_percent=20,INITIAL_MANIFEST=actual['files']['INITIAL_MANIFEST.json'],INITIAL_SEAL=actual['files']['INITIAL_SEAL.json'])))
