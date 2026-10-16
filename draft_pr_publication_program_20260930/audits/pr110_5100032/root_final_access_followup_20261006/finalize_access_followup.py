from pathlib import Path
import datetime,hashlib,json,os
D=Path(__file__).resolve().parent;A=D.parent;P=A.parents[1]
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
private=[]
for p in sorted((D/'private_sources').iterdir()):
    if p.is_file():
        b=p.read_bytes();private.append({'path':p.relative_to(D).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'redistributed':False})
labels=['root_access_followup_crossref_metadata','root_access_followup_openalex_metadata','root_access_followup_semanticscholar_metadata','root_access_followup_crossref_fulltext_html','root_access_followup_publisher_html_diagnostic','root_access_followup_publisher_public_Fig6']
operations=[]
for label in labels:
    f=A/'actual_operations'/label/'execution.json';r=json.loads(f.read_text())
    for name in ('stdout','stderr'):
        b=(f.parent/r[name]['path']).read_bytes()
        if len(b)!=r[name]['bytes'] or hashlib.sha256(b).hexdigest()!=r[name]['sha256']:raise RuntimeError('actual stream pin')
    operations.append({'label':label,'child_PID':r['child_PID'],'exit_code':r['exit_code'],'copyrighted_preview_stdout_excluded_from_public_checkpoint':label=='root_access_followup_publisher_html_diagnostic'})
cr=json.loads((D/'private_sources/crossref.json').read_text())['message']
oa=json.loads((D/'private_sources/openalex.json').read_text())
ss=json.loads((D/'private_sources/semanticscholar.json').read_text())
diagnostic=json.loads((D/'PUBLISHER_ACCESS_DIAGNOSTIC.json').read_text())
if not diagnostic['subscription_preview_phrase_present']:raise RuntimeError('inspect changed access')
report='''# PR110 final-version access follow-up

The previous goal turn made progress: fresh combined priority adjudication, root custody and the specific M1 hold were completed and pushed at a54913a3c2330a2f9fe31763000cd047df84cd3b. This follow-up tests additional legitimate retrieval routes for the identified journal final. It does not reopen or replace the verified mathematical proof, close the PR, or clear publication.

The required body remains Garcia–Koiller–Reznik, *Estimating Elliptic Billiard Invariants with Spatial Integrals*, JDCS29:757–767(2023), online2022, DOI10.1007/s10883-022-09608-y. Its nine-page arXiv2102.10899v1 precursor is fully read; the eleven-page final remains unread.

Four targeted indexed searches, covering the authors' UFG/UFJF repositories, HAL and Zenodo, returned no results. These are finite discovery searches, not proof that no legitimate copy exists.

Fresh Crossref metadata supplies publisher-deposited version-of-record PDF and HTML text-mining links. The PDF link is the previously attempted route; its separate HTML fulltext.html link was now retrieved by actual curl57470. Curl succeeded, but inspection58288 shows subscription preview, no Introduction or Conclusions section and no governing final statements/proofs. A successful HTTP response is not a full-body read. The web tool could not open that HTML route.

Fresh OpenAlex metadata labels this DOI closed and has no repository/full-text location in its current record. Semantic Scholar returns no openAccessPdf URL. These are discovery indexes, not exhaustive access inventories or mathematical evidence.

The publisher HTML visibly offers six public figure thumbnails. Root inspected only Figure6 at its actually supplied m312 PNG URL, downloaded by actual curl59442. The plot compares angle-cosine averages with a caustic parameter. It supplies no antipedal norm-sum statement or proof; no caption or complete final body was inferred from it. This is additional partial primary evidence consistent with the precursor's specified average observables, and does not resolve M1.

The existing research Chrome profile was checked through the supported UI tool. Browser2's agent-created tab963512676 displayed the identified publisher page, subscription preview and no institutional affiliation. No authentication credentials were entered, institution selected, purchase made, or permission granted. The temporary research tab was closed. Native-app inventory reported a locked Mac, but browser-page reading worked; the substantive issue is absent authenticated article access, not the native inventory error. UI tools supplied no OS PID or exact action timestamp, so none is invented. Raw UI text, publisher body, public thumbnail and diagnostic preview stream remain private and are not redistributed.

Result: the same finite identified final-version comparison remains unavailable. The pending human legitimate-link/institutional-access question has not been answered. Access failure is not evidence of already_solved. No additional independent mathematical work or unchanged access retry is needed before receiving a legitimate full final body. Root retains the adjudicated hold; source/math100%, selected-candidate priority work90%, current workflow30%, publication0%. The persistent full program is incomplete:17/99 workflows completed,10 published. New central proof-search turns0; original2/5 preserved.
'''
(D/'REPORT.md').write_text(report)
r={'schema':'pr110-final-version-access-followup/v1','UTC':now,'actual_operator_PID':os.getpid(),'previous_goal_turn_classification':'progress','previous_checkpoint':'a54913a3c2330a2f9fe31763000cd047df84cd3b','PR':110,'required_doi':'10.1007/s10883-022-09608-y','new_complete_final_body_obtained':False,'priority_gate_unchanged':'HOLD_FOR_M1_FINAL_JOURNAL_COMPARISON','source_access_question_pending':True,'already_solved_disposition_supported':False,'priority_or_publication_clearance':False,'actual_operations':operations,'additional_indexed_queries':['"s10883-022-09608-y" site:repositorio.ufg.br','"Estimating Elliptic Billiard Invariants" site:repositorio.ufjf.br','"Estimating Elliptic Billiard Invariants" site:hal.science','"s10883-022-09608-y" site:zenodo.org'],'indexed_search_no_results_are_not_exhaustive_absence':True,'crossref_deposited_links':cr.get('link',[]),'openalex_access_metadata':oa.get('open_access'),'semanticscholar_openAccessPdf':ss.get('openAccessPdf'),'publisher_HTML_diagnostic':'PUBLISHER_ACCESS_DIAGNOSTIC.json','root_visual_read':'Publisher public Figure6 thumbnail only','browser_observation':{'retrieval_date':'2026-10-06','browser_id':'2','agent_tab_id':'963512676','subscription_preview':True,'institutional_affiliation_shown':False,'credentials_or_purchase_or_permission_actions':False,'temporary_tab_closed':True,'OS_PID_available':False,'exact_action_UTC_available':False,'raw_UI_and_IP_not_redistributed':True},'private_source_pins':private,'private_copyrighted_preview_stream':{'path':'actual_operations/root_access_followup_publisher_html_diagnostic/stdout.bin','bytes':(A/'actual_operations/root_access_followup_publisher_html_diagnostic/stdout.bin').stat().st_size,'sha256':hashlib.sha256((A/'actual_operations/root_access_followup_publisher_html_diagnostic/stdout.bin').read_bytes()).hexdigest(),'public_checkpoint_excluded':True},'source_math_percent':100,'selected_candidate_priority_work_percent':90,'workflow_percent':30,'publication_percent':0,'new_central_proof_search_turns':0,'persistent_goal_complete':False,'persistent_goal_status':'active','blocked_threshold_not_yet_met':True}
(D/'RESULT.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
note='\n'+now+' — PR110 M1 legitimate-access follow-up (workflow30%; source/math100%; priority90%; publication0%). Four additional repository searches, direct Crossref/OpenAlex/SemanticScholar metadata, Crossref-deposited HTML route and existing browser session inspected. HTML/browser remain subscription previews, metadata points to no accessible final, and Figure6 only shows angle-cosine averages. Full final still unavailable; pending human access answer remains required. No priority/native/PR/publication decision changed; same M1 hold. Raw copyrighted/derived bodies and preview-containing stdout excluded from public checkpoint. Previous goal turn was progress (fresh adjudication and pusheda54913a3…); blocker now repeats in this next goal turn, below blocked threshold. New central proof turns0.\n'
for log in (A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md',P/'CURRENT_PROGRESS.md'):
    with log.open('a') as out:out.write(note)
f=P/'CURRENT_PROGRESS.json';progress=json.loads(f.read_text());progress['UTC']=now;progress['updated_UTC']=now;progress['current_access_followup']='audits/pr110_5100032/root_final_access_followup_20261006/RESULT.json';progress['current_priority_hold_checkpoint_commit']='a54913a3c2330a2f9fe31763000cd047df84cd3b';progress['current_access_blocker_goal_turns_recorded']=2;progress['current_last_goal_turn_classification']='progress';progress['current_human_source_access_question_pending']=True;f.write_text(json.dumps(progress,indent=2,sort_keys=True)+'\n')
ignore=A/'.gitignore';text=ignore.read_text();line='actual_operations/root_access_followup_publisher_html_diagnostic/stdout.bin'
if line not in text.splitlines():ignore.write_text(text+line+'\n')
print(json.dumps({'UTC':now,'actual_operator_PID':os.getpid(),'complete_final_obtained':False,'priority_gate_unchanged':True,'publication_clearance':False,'workflow_percent':30,'source_access_question_pending':True}))
