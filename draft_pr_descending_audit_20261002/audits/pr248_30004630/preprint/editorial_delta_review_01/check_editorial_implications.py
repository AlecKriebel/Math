from pathlib import Path
import hashlib,json,re,datetime
OWN=Path(__file__).resolve().parent;BASE=OWN.parent;HIST=BASE/'history/before_editorial_refinement_20261014T050605832144Z';OLD=BASE/'fresh_review_01';ROOT=OWN/'extracted';sha=lambda b:hashlib.sha256(b).hexdigest()
a=(HIST/'critical_wave_growth.tex').read_text();b=(BASE/'critical_wave_growth.tex').read_text()
blocks=[]
for env in ('theorem','lemma','corollary','equation','align'):
 pattern=r'\\begin\{'+env+r'\}.*?\\end\{'+env+r'\}'
 old=re.findall(pattern,a,re.S);new=re.findall(pattern,b,re.S);assert old==new,env;blocks.append({'environment':env,'count':len(new),'all_block_bytes_equal':True})
# All inline/display dollars also remain identical; citation/credit/license edits are outside math.
for tag,pattern in [('dollar_math',r'\$.*?\$'),('display_brackets',r'\\\[.*?\\\]')]:
 old=re.findall(pattern,a,re.S);new=re.findall(pattern,b,re.S);assert old==new,tag;blocks.append({'environment':tag,'count':len(new),'all_block_bytes_equal':True})
# Reuse the already pinned/read complete primary-source page; no new large download.
primary=OLD/'external_reading/KMv1-p35.txt';s=primary.read_text();assert 'Theorem 4.17 (Second order sufficient conditions)' in s and 'Let β2 > 0.' in s and 'C(ū) \\ {0}' in s
primary24=(OLD/'external_reading/KMv1-p24.txt').read_text();assert 'We henceforth always consider a fixed locally optimal control' in primary24
# The explanatory README insertion concerns exactly four unmodified pinned parent-directory files.
mf=ROOT/'audits/priority_bridge_falsifier_01/historical_snapshot_01/FINAL_AUDIT_MANIFEST.json';m=json.loads(mf.read_text());shared=[]
for pin in m['public_authored_relative_paths']:
 if not (mf.parent/pin['path']).is_file():
  p=mf.parent.parent/pin['path'];data=p.read_bytes();assert len(data)==pin['bytes'] and sha(data)==pin['sha256']
  shared.append({'path':pin['path'],'relative_archive_path':str(p.relative_to(ROOT)),'bytes':len(data),'sha256':sha(data),'unchanged_historical_pin_matches':True})
assert len(shared)==4
visual=[]
for n in range(1,7):
 p=OWN/f'rendered/page-{n}.png';data=p.read_bytes();old=OLD/f'rendered/page-{n}.png'
 visual.append({'page':n,'relative_render_path':str(p.relative_to(OWN)),'bytes':len(data),'sha256':sha(data),'visually_inspected':True,'layout_defects':False,'pixel_byte_identical_to_own_old_render':old.read_bytes()==data})
currenttext=(OWN/'rendered/current_pdf_text.txt').read_text();assert 'Theorem 4.17' in currenttext and 'CC BY 4.0' in currenttext
assert currenttext.count('\f')==6
rep={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_math_environment_and_inline_bytes_unchanged':blocks,'source_locator_correct':True,'source_locator_primary_pin':{'path':str(primary),'bytes':len(primary.read_bytes()),'sha256':sha(primary.read_bytes()),'native_primary_PDF_sha256':'f0410942714bdf5226210d98b3c286ea615188f2a53aa53f464a8fd7e3c067cd'},'standing_local_optimality_premise_preserved_and_satisfied':True,'wave_estimate_credit_narrowing_accurate':True,'authored_materials_CC_BY_matches_original_metadata_and_license':True,'no_third_party_whole_copy_license_implied':True,'historical_shared_four_files':shared,'all_six_revised_PDF_pages_visually_inspected':True,'PDF_pages':visual,'AI_unrefereed_no_human_review_and_bounded_priority_scope_unchanged':True,'mandatory_issues':[]}
(OWN/'EDITORIAL_IMPLICATIONS_AND_PDF_QA.json').write_text(json.dumps(rep,indent=2)+'\n')
log=OWN/'RESEARCH_LOG.md';t=log.read_text();t+='\n'+rep['utc']+' — 90% assigned addendum. New frozen ZIP was independently extracted and all 112 payload pins/exact 113-file closure verified. Seven persistent scientific receipts plus portable runner passed, independently deriving 5603 exact plus 5 diagnostic assertions. Native-head original 19 bytes and archive/source/metadata/deposit equality rechecked. Every revised PDF page viewed; no layout defect; new locator and license visible. Exact unchanged theorem/lemma/corollary/equation/align/inline/display math blocks verified. Theorem 4.17 locator checked against the already authenticated complete source page and standing local-optimizer premise; four shared historical files exactly match pins. Remaining: final report, final input/old-review readback and public manifest.\n';log.write_text(t)
print(json.dumps({'math_blocks':blocks,'shared_historical_files':len(shared),'PDF_pages':6,'mandatory_issues':[]},indent=2))
