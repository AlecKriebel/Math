#!/usr/bin/env python3
import datetime, hashlib, json, pathlib
root=pathlib.Path(__file__).resolve().parent
orig=root.parent/'original_source_authentication_20261004'/'process_evidence'
def digest(p):
    p=pathlib.Path(p); b=p.read_bytes();return {'path':str(p.resolve()),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
rows=[
('bruss2004_arxiv_v3_pdf','original_stream','source-first','quant-ph/0407037v3, 8 Dec 2004','Header, unitary product-input/routing/cut passages, W question p4; extraction complete, selective substantive reading'),
('bruss2004_prl_author_pdf','original_stream','source-first and post-freeze visual','Published PRL93,210501 (2004)','Textual original W question and model; final printed p210501-4 rendered and visually inspected post-freeze'),
('owr2005_pdf','original_stream','source-first','OWR4/2005 pp203-205','Complete relevant contribution pp203-205 and references, extracted text; unrelated OWR contributions not adjudicated'),
('bruss2005_pdf','original_stream','source-first','quant-ph/0507146v1, 15 Jul 2005','Header, sections2-4 asymptotic/unitary model, sections5-7 receiver model/bounds/shells and relevant examples; not every unrelated discussion read'),
('original_pdf_winter2001','original_stream','source-first','quant-ph/9807019v3, 1 Feb 2001','Header, sectionII model/code definitions, Theorem9 and surrounding proof start pp4-5; whole proof not reaudit'),
('original_pdf_pradhan2007','original_stream','source-first','0705.1917v1, 14 May 2007','Sec4.2.3 p36 eq108-109 and neighboring multi-receiver model/context; not whole40-page paper'),
('original_pdf_das2015','original_stream','source-first plus post-freeze published abstract','1412.6247v1; PRA92,0523302015','Header/introduction, sectionII model and upper-bound derivation passages; not whole noise proof; final publisher abstract read; finalbody identity unverified'),
('original_pdf_nonmarkov2024','original_stream','source-first plus post-freeze published abstract','2211.13057v2, 24 Mar2024; PRA109,032616','Header, introduction, sectionII eq6-7, full relevant two-receiver bound discussion snippets/Fig3 labeling; not every noise calculation; finalbody identity unverified'),
('cao2006','own_stream','source-first','CPL23,290-2922006 publisher PDF','All3 pages rendered and visually inspected. pdftotext exits0 but fontmappingbroken; substantive reading from images'),
('hayashi_arxiv','own_stream','source-first','2109.12518v1, 26 Sep2021','Header, model, Assumption1, encoder/decoder definitions and direct theorem scope. FinalTheorem2 separately read via publisherweb; v1 not substituted for final'),
('crossref_yuan_ijqi','own_stream','source-first','Publisher-deposited Crossref metadata DOI10.1142/S0219749911006879','Complete record downloaded; title/abstract/model/advertisedtwo-bit result read. Bodyunread'),
('crossref_yuan_ijtp_retry','own_stream','source-first','Crossrefmetadata DOI10.1007/s10773-011-0729-7','Title/link metadata read; publisherabstract separately readviaweb. Bodyunread'),
('crossref_zhao2012_retry','own_stream','source-first','Crossrefmetadata DOI10.1016/j.proeng.2012.01.005','Title, DOI, PII/linkauthentication only; abstractnull. Bodyunread'),
('zhao_elsevier_xml','own_stream','source-first','Elsevierprimary XML PII S187770581200015X','Complete1971byte XMLread; coremetadata only, no body/abstract'),
('shukla2012v1','own_stream','source-first','1204.4573v1, 20 Apr2012','Introductionselected and fullrelevant sections2-3protocols, rateclaims and references; not every securitycalculation'),
('liu2023v1','own_stream','source-first','2310.02923v1; relatedQIP2020paper','Definition/readout context, Table4differentW1, appendixsymmetricsingleexcitationW2 scope. Fullbodynotread'),
('huang2000v5','own_stream','post-freeze familylead','quant-ph/9911120v5, 6 Nov2000','Introduction/model and complete section6pp9-11 dense-codingapplication, commonreceiver allocation'),
('localsubentropy2006v2','own_stream','post-freeze familylead','quant-ph/0505137v2','Introduction, lower-bound derivation/scope p2-3eq2, separablesuperoperator scope. Notindependentlyintegrated'),
('wangyan2011','own_stream','post-freeze familylead','CPB20,1203092011publisher PDF','Section3p4/Table3throughconclusion senderownership/four-particleglobalreadout'),
('routing2026v2','own_stream','post-freeze familylead','2503.16122v2, 7 Jul2026','Header/abstract and relevant model/coherent-control/single-sender routing passages. Notwholenoisycapacityanalysis'),
('pauwels2026v1','own_stream','post-freeze familylead','2608.21185v1, 21 Aug2026','Introduction and sectionIIdefinitions/independentlabels, discussion, AppendixDstate/resources; notfullproofaudit. pdftotextfont warningretained'),
('matthews2009_pdf','root_private_stream','post-freeze correction','0810.2327v2 banner26Oct2008; title date10Oct2008','Header, Section2A p8 uniformPOVM/Theorem9, complete Section4 pp17-19; remaining sections only navigation searches, not whole-paper clearance'),
('crossref_das_publishers_note','own_stream','post-freeze correction','Publisher-deposited metadata DOI10.1103/PhysRevA.92.069903, published10Dec2015','Complete2618byte metadata record read for exact title/authors/date/links; no abstract/body available in this record'),
]
ledger=['# Source and read-scope ledger','', 'Acquisition/extraction is not a claim of full reading. This ledger records substantive scope. No author SOURCES or whole preprint was read. ROOT comparison reading occurred only after independently freezing the correction assessment, as detailed below. Web-tool process metadata are unavailable; no shell PID is invented.','', '| Source stream | Stage | Version/role | Actual substantive reading | Input SHA256 |','| --- | --- | --- | --- | --- |']
sources=[]
for name,kind,stage,version,scope in rows:
    source_base=orig if kind=='original_stream' else (root.parent/'ROOT_priority_20261004'/'private_sources'/'process_evidence' if kind=='root_private_stream' else root/'process_evidence')
    p=source_base/name/'stdout.bin';entry={**digest(p),'label':name,'stage':stage,'version_role':version,'actual_read_scope':scope};sources.append(entry)
    ledger.append(f'| {name} | {stage} | {version} | {scope} | `{entry["sha256"]}` |')
ledger+=['','## Other allowed reads','', '- Root AGENTS.md and PDF skill before primary PDF extraction/rendering.', '- TARGET_SCOPE_PIN and SOURCE_FIRST_ASSESSMENT_FROZEN were byte-pinned before candidate reading; see freeze_receipt/request/result. They remain unmodified after the correction.', '- Immutable candidate read in full after freeze, then complete target and mechanism REPORT.md files. Their VERDICT.json files were only listed by filename, not read.', '- Target LITERATURE_LEDGER decisive source-lead rows were read after both report reads; its conclusions were hypotheses, followed by independent primary checks.', '- Original-source tree was listed by filename only initially (one oversized listing truncated); no original-source-authentication conclusions or ROOT priority notes were read during initial adjudication.', '- Initial REPORT/VERDICT/ledger/manifest/validation preserved byte-for-byte in initial_adjudication_preserved_20261004 before correction reading; preserve_initial_adjudication capture records custody.', '- CORRECTION_SOURCE_ASSESSMENT_FROZEN pinned at23:04:52Z after independent MWW primary inspection and before ROOT comparison read. Only ROOT AFTER_FIRST_PRIOR_BOUND_COMPARISON_20261004 was read, in full, at23:05:36Z; other ROOT assessments remained unread.', '- check_isotropic_instrument.py and its captured output document an analytic instrument-specific information bound and numerical cross-check. No general LOCC capacity converse or interval numerical certificate is claimed.', '- Saved web results include exact query strings encoded in provider result descriptions where available; initial web calls not separately saved remain in the conversation record. Saved JSON files contain unmodified returned native-tool strings/objects, not invented full binary PDFs.', '- Publisher Hayashi final PDF model/Theorem2/Assumption1 were read through web extraction. Curl failed; primary arXivv1 binary separately retained.', '- Yuan IJTP publisher abstract; Yuan IJQI publisher-deposited Crossref abstract; Zhao coremetadata and Shukla primary citation context; no body clearance claimed.', '- Das/Muhuri final publisher abstracts read. Exact Das Publisher Note metadata inspected post-freeze; APS recent-articles search metadata confirms title/date. APS abstract/PDF/DOI and publisher-harvest body attempts failed. No note content inferred. Tsai2013 publisher PDF attempt failed; source not counted as body-read. Tsai2010 primary publisher snippet concerns threequbitW.', '- One search exposed rehosted Zhao body text; it was not used as primary body clearance. Correction search likewise exposed rehosted Das-note metadata, not used for body clearance.', '', '## Failure accounting', '', '- Eight initial extraction launcher invocations exited1 before launching pdftotext because command parsed as --pin. Their request/pinned launcher/empty stdout-stderr files are retained. No child PID/status is claimed.', '- Networkchild failures have actual subprocess exit56 and complete capturedstderr. Successfulcurl/XML/metadata responses are validated by content; HTTPsuccess does not imply fullpaper content.', '- Nativeweb failures retained where saved; no child process status applies.', '- Direct setup/exploratory read commands have normal tool transcripts only; they are not represented as PID-captured scripts. All decisive retrieval/extraction/render/candidate/family/freeze commands and finalcustody scripts use the captured childwrapper.']
(root/'SOURCE_READ_SCOPE_LEDGER.md').write_text('\n'.join(ledger)+'\n')
processes=[]; issues=[]
for folder in sorted((root/'process_evidence').iterdir()):
    req=folder/'request.json';result=folder/'result.json'
    if not req.exists():continue
    q=json.loads(req.read_text());r=json.loads(result.read_text()) if result.exists() else None
    entry={'label':folder.name,'request':digest(req),'argv':q['argv'],'launcher_pid':q['launcher_pid'],'prelaunch_pins':q['prelaunch_pins'],'result':r}
    if r:
        for key in ['stdout','stderr']:
            actual=digest(r[key]['path'])
            if actual['sha256']!=r[key]['sha256'] or actual['bytes']!=r[key]['bytes']:issues.append(folder.name+': '+key+' mismatch')
        entry['status']='completed_child';entry['child_exit_code']=r['child_exit_code'];entry['child_pid']=r['child_pid']
    elif folder.name.startswith('extract_') and not folder.name.endswith('_retry') and q['argv'][0]=='--pin':
        entry['status']='launcher_failed_before_child';entry['launcher_exit_code_from_tool']=1;entry['child_pid']=None;entry['child_exit_code']=None
    else:entry['status']='capture_currently_running_or_no_result_yet';entry['completion_record_path']=str(result)
    processes.append(entry)
files=[]
for p in sorted(root.rglob('*')):
    if p.is_file() and p.name!='EVIDENCE_MANIFEST.json':files.append(digest(p))
manifest={'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'private assigned folder only','source_inputs':sources,'captured_processes':processes,'files_snapshot':files,'validation_issues':issues,'generation_capture_note':'The correction manifest-generating child and subsequent validation finish after this snapshot; actual completed records reside at process_evidence/finalize_evidence_correction and validate_evidence_correction. Initial artifacts are preserved in initial_adjudication_preserved_20261004.','web_metadata_note':'Native tools expose no shell PID or exit; no such fields fabricated.'}
(root/'EVIDENCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'source_count':len(sources),'captured_process_count':len(processes),'files_snapshot_count':len(files),'validation_issues':issues},indent=2))
if issues:raise SystemExit(1)
