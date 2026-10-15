from pathlib import Path
import datetime, hashlib, json, re, html
p=Path(__file__).resolve().parent
def pin(f):
 b=f.read_bytes();return {'path':str(f.relative_to(p)), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()}
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
results=[]
for f in sorted((p/'process_evidence').glob('*/result.json')):
 d=json.loads(f.read_text())
 for which in ['stdout','stderr']:
  b=Path(d[which+'_path']).read_bytes()
  assert len(b)==d[which+'_bytes'],(f,which,'size')
  assert hashlib.sha256(b).hexdigest()==d[which+'_sha256'],(f,which,'digest')
 for s in d['retained_sources_prelaunch']:
  b=Path(s['retained_path']).read_bytes()
  assert len(b)==s['bytes'] and hashlib.sha256(b).hexdigest()==s['sha256'],(f,s)
 if d['label'].startswith(('extract_','render_','metadata_','freeze_')):assert d['exit_code']==0,(f,'required child exit')
 results.append({k:d[k] for k in ['label','argv','cwd','actual_PID','start_UTC','end_UTC','exit_code','stdout_bytes','stdout_sha256','stderr_bytes','stderr_sha256']})
assert pin(p/'private/CANDIDATE_pinned.md')['bytes']==11679
assert pin(p/'private/CANDIDATE_pinned.md')['sha256']=='fb8646bbe3cd8512ec7736fc180fa08a76740ac8b0dbb60b539a0320328c6404'
assert pin(p/'FIRST_PRIORITY_VERDICT.json')['sha256']=='0bc1d3157f74c27c002a0c6a6c22059146fe96fab352e6520491b6d853a9f7f2'
scopes={
 'owr2005_pdf.pdf':'Complete original contribution printed203–205 read; relevant PDF pages19–21 rendered,20–21 visually inspected; unrelated OWR contributions excluded from adjudication.',
 'bruss2004_arxiv_v3_pdf.pdf':'Complete four-page original model text read; decisive p3 rendered and visually inspected.',
 'bruss2004_prl_author_pdf.pdf':'Complete four-page published-author model text read; p3–4 rendered, p4 visually inspected.',
 'bruss2005_pdf.pdf':'Complete expanded original model text read; p7 rendered and visually inspected.',
 'pradhan2007_v1.pdf':'Introduction/model and complete dense-coding sections4.1–4.2/conclusion read; relevant W4 single-receiver and receiver-LOCC protocols read in full; p36 rendered and visually inspected. Teleportation calculations not independently verified.',
 'winter2001_v3.pdf':'Complete seven-page text, theorem9 proof, converse, appendix and references read. No fresh proof verification claimed.',
 'huang1999_v1.pdf':'Complete main text/read theorem and generalized dense-coding application; references partially inspected.',
 'huang2000_v5.pdf':'Complete main text sections1–7/theorem/proof/application read; references partially inspected.',
 'allahverdyan1997_v1.pdf':'Complete twelve-page text read; no independent bosonic model calculation.',
 'das2015_v1.pdf':'Introduction, full relevant model/bound derivation p1–4, later noisy capacity interpretation and conclusion inspected; noise-specific calculations/plots not independently reverified.',
 'nonmarkov2024_v2.pdf':'Introduction/model definitions and full relevant two-receiver W4 discussion/figures read; p9 rendered and visually inspected; unrelated numerical optimization not reverified.',
 'singh2015_v1.pdf':'Introduction/resource definition and complete dense-coding sectionV/conclusion read.',
 'singh2016_v2.pdf':'Version diff checked; dense-coding allocation unchanged; full text retained, unrelated teleportation proofs not reverified.',
 'secure2011_v1.pdf':'Introduction, complete protocols2B–D and receiver-unlocking resource definitions read; security later sections not reverified.',
 'secure2016_v2.pdf':'Relevant full W protocol2.3 and resource/unlocking sections3.1–3.2 read; security appendices not reverified.',
 'horodecki_piani2007.pdf':'Resolved version is quant-ph/0701134v2,11Sep2009. Introduction/model/organization and relevant one-receiver allocation read; filename2007 refers only first-submission year.',
 'sen2009_v2.pdf':'Complete main text read, defining single-copy remote singlet probabilities, including W4 case and conclusion; references partly inspected.',
 'shukla2012_v1.pdf':'Introduction, framework, relevant complete W4 dense-coding protocols/tables/comparison and conclusion read; no security proof verification.',
 'agrawal2006_v1.pdf':'Introduction, asymmetric W-class definitions and complete dense-coding sectionIV/conclusion read; teleportation proof not reverified.',
 'roy2018_v3.pdf':'Introduction/framework and relevant higher-sender/protocol sections4–5 read; numerical and full appendices not independently reverified.',
 'hayashi2021_v1.pdf':'Relevant model, Assumption1, local-decoder conditions, enhanced setting and main theorems7–10 read; main direct-part hypotheses checked. Complete preprint retained; no complete appendix proof verification.',
 'wang_yan2011.pdf':'Complete five-page main body and references read; dense-coding p4 rendered and visually inspected.',
 'cao_song2006.pdf':'Post-FIRST primary source supplied as ROOT route lead; all three complete pages visually read, including p290 Eq1, p291 protocol/Table1, p292 conclusion/references. Text extraction has broken font mapping despite childexit0, so substantive reading used rendered pages.',
}
pdfs=[]
for f in sorted((p/'private').glob('*.pdf')):
 assert f.read_bytes().startswith(b'%PDF'),f
 pdfs.append({**pin(f),'retained_complete_file':True,'read_scope':scopes.get(f.name,'Post-freeze primary source; see report read scope.')})
metadata=[]
for f in sorted((p/'private').glob('*_metadata.html')):
 s=f.read_text(errors='replace')
 m=re.findall(r'<meta\s+name="(citation_[^"]+)"\s+content="([^"]*)"',s)
 history=''
 if '<div class="submission-history">' in s:
  a=s.index('<div class="submission-history">');b=s.find('</div>',a)
  history=html.unescape(re.sub('<[^>]+>','',s[a:b])).strip()
 metadata.append({**pin(f),'citation_metadata':m,'submission_history':history})
manifest={
 'generated_at_UTC':utc,'family':'mechanism_priority_family_20261004',
 'input_pins':json.loads((p/'INPUT_PINS.json').read_text()),
 'frozen_artifacts':[pin(p/f) for f in ['FIRST_SOURCE_ONLY.json','FIRST_SOURCE_ONLY.md','FIRST_PRIORITY_VERDICT.json','FIRST_PRIORITY_VERDICT.md']],
 'candidate':pin(p/'private/CANDIDATE_pinned.md'),
 'authored_findings':[pin(p/f) for f in ['REPORT.md','RESEARCH_LOG.md','SEARCH_LEDGER.md']],
 'authored_reproducibility_sources':[pin(f) for f in sorted(p.glob('*.py'))],
 'primary_pdfs':pdfs,'primary_metadata':metadata,
 'extracted_texts_and_rendered_pages':[pin(f) for f in sorted((p/'private').glob('*.txt'))]+[pin(f) for f in sorted((p/'private').glob('*.png'))],
 'web_tool_streams':[pin(f) for f in sorted((p/'private').glob('search*.json'))]+[pin(f) for f in sorted((p/'private').glob('meta*.json'))],
 'other_private_source_receipts':[pin(f) for f in sorted((p/'private').glob('*_crossref.json'))],
 'captured_commands':results,
 'inspected_child_exits':True,
 'failed_commands':[r for r in results if r['exit_code']!=0],
 'success_without_requested_media':[r['label'] for r in results if r['label'] in ['download_yuan2011_ijtp_pdf','metadata_cao2006']],
 'custody_limits':['Final Hayashi publisher PDF accessible and decisive passages read through web; complete binary not retained.','Springer Yuan PDF URL returned HTTP-success subscription HTML, not a PDF.','Initial Cao DOI route returned homepage HTML, not requested article metadata; authenticated article-id route and complete PDF subsequently captured.','Cao text extraction exits0 but has broken font mapping; all three pages rendered and visually read.','Web tools do not report shell argv/PID; none invented.','Post-freeze web batch17 response retained, but exact query request was not recovered after context compaction; no query string invented.'],
 'independence':{'author_SOURCES_read':False,'prior_reviews_read':False,'sibling_reports_read':False,'ROOT_conclusions_read_before_FIRST':False,'post_FIRST_ROOT_messages':'Gap clarification, primary metadata/model corroboration and Cao publisher route. Cao independently captured and visually read after FIRST; FIRST preserved.'},
 'integrity_validation':'All completed capture stream hashes and retained launch-source hashes verified; candidate identity and frozen first priority hash asserted. This does not verify the central theorem.'
}
(p/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
first=json.loads((p/'FIRST_PRIORITY_VERDICT.json').read_text())
verdict={
 'generated_at_UTC':utc,'problem_id':'30000177','PR':80,'family':'mechanism-first literature priority',
 'source_model_frozen_at_UTC':'2026-10-04T22:06:24.651025+00:00','first_priority_frozen_at_UTC':first['frozen_at_UTC'],
 'original_candidate_head':'dcfeb5d8ad68b397ec509c70e85c6fca46cd01e3','original_candidate_sha256':pin(p/'private/CANDIDATE_pinned.md')['sha256'],
 'original_claimed_solved_fraction':{'numerator':1,'denominator':5,'preserved':True},
 'priority_status':'NO_IDENTIFIED_COMPLETE_PRIOR_APPLICATION_IN_AUDITED_CORPUS; GLOBAL_PRIORITY_UNESTABLISHED',
 'already_solved_supported':False,'novelty_certified':False,'affirmative_specific_priority_obstruction_identified':False,
 'mathematical_validity_status':'NOT_ASSIGNED_BY_THIS_FAMILY',
 'established_prior_ingredients':['W4 paired Bell decomposition: Cao–Song2006 Eq1; secret communication using sender classical disclosure is a distinct operational task.','W4 Bell measurement/classical forwarding followed by Bell decoding: Pradhan et al.2007 section4.2.3, exactly2bits.','Independent-input cq-MAC achievability: Winter1998/2001.','Pure-output MAC theorem plus generalized dense-coding application with one common receiver: Huang et al.1999/2000.'],
 'exact_gap':'Whether the original independent-sender, split-routed receiver-LOCC strict >2-bit asymptotic symmetricW4 application was explicitly published earlier; none established in the inspected corpus.',
 'local_access_limits':[
  {'source':'Yuan IJTP2011 DOI10.1007/s10773-011-0729-7','detail':'Full protocol unread; primary publisher abstract explicitly advertises exactly2bits; PDF route returns subscription HTML. Low plausibility for original strict-rate collision.'},
  {'source':'Yuan IJQI2011 DOI10.1142/S0219749911006879','detail':'Full protocol unread; publisher-deposited Crossref abstract explicitly specifies exactly2bits, two users, additional classical information. Low plausibility for original strict-rate collision.'},
  {'source':'Zhao2012 DOI10.1016/j.proeng.2012.01.005','detail':'Full body unread in this family; Crossref authenticates publisher PII S187770581200015X. Later primary source describes2bit two-user security protocol. Original body needed for complete exclusion.'},
 ],
 'inherent_search_limit':'Finite literature coverage is not proof of worldwide absence; this is distinct from the concrete access limits and is not an affirmative obstruction.',
 'required_attribution':'Prior Bell preprocessing and MAC theorem/application antecedents must be cited; no new general MAC theorem or first generic MAC-dense-coding claim supported.',
 'promotion':'No promotion or publication authorization/action by this family. Candidate application and independent validity review remain separate.',
 'artifacts':['REPORT.md','FIRST_SOURCE_ONLY.md','FIRST_SOURCE_ONLY.json','FIRST_PRIORITY_VERDICT.md','FIRST_PRIORITY_VERDICT.json','SEARCH_LEDGER.md','MANIFEST.json','RESEARCH_LOG.md'],
 'audit_completion_percent':100,'completion_scope':'Assigned independent mechanism-priority audit with explicit retained access limits; not a percentage of global novelty certainty or central proof completion.',
}
(p/'VERDICT.json').write_text(json.dumps(verdict,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'verification_UTC':utc,'captured_commands_verified':len(results),'complete_pdfs':len(pdfs),'failed_child_exits':[(r['label'],r['exit_code']) for r in results if r['exit_code']!=0],'nonrequested_media_HTTP_success':['download_yuan2011_ijtp_pdf','metadata_cao2006'],'candidate_sha256':pin(p/'private/CANDIDATE_pinned.md')['sha256'],'FIRST_PRIORITY_VERDICT_sha256':pin(p/'FIRST_PRIORITY_VERDICT.json')['sha256']},indent=2))
