from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re,zipfile,subprocess,copy
B=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23387442');O=B/'reviews/publication';S=B/'sources';T=S/'published-source/satoh_filtration_verification/satoh_filtration_counterexamples.tex'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inf(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':h(p)}
def write(n,d):O.joinpath(n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
now=datetime.now(timezone.utc).isoformat();receipt=json.loads((S/'receipt.json').read_text());record=json.loads((S/'record.json').read_text());c=copy.deepcopy(json.loads((B/'reviews/scope/candidate.json').read_text()))
assert h(S/'record.json')==receipt['record_sha256']
assets=[]
for f in receipt['files']:
 p=S/f['name'];assert p.stat().st_size==f['bytes'] and h(p)==f['sha256'];assert hashlib.md5(p.read_bytes()).hexdigest()==f['md5'];assets.append(inf(p))
assert h(T)==c['source_binding']['source_tex_sha256']
tex=T.read_text();abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1).strip()
plain=re.sub(r'\s+',' ',abstract.replace('$','').replace(r'\SL', 'SL').replace(r'\C','ℂ').replace(r'\setminus',' \\ ').replace(r'\geq','≥').replace("Satoh's","Satoh’s")).strip()
assert plain==c['abstract'],(plain,c['abstract'])
(O/'ABSTRACT.tex').write_text(abstract+'\n');(O/'ABSTRACT.txt').write_text(plain+'\n')
info=subprocess.check_output(['pdfinfo',str(S/c['pdf_filename'])],text=True);assert re.search(r'^Pages:\s+4$',info,re.M)
c['canonical_url']='https://aleckriebel.com/research/'+c['slug']+'/'
c['pdf_pages']=4;c['keywords']=record['metadata']['keywords'];c['candidate_only']=True
c['candidate_gate']='PUBLICATION PREFLIGHT DRAFT ONLY. The three independent reports are complete according to the root assignment, but root scientific clearance has not been granted. This draft confers no mathematical PASS, promotion, rendering, deployment or tracker-update authorization.'
c['source_binding']['publication_state']='DRAFT_ONLY_ROOT_SCIENTIFIC_CLEARANCE_PENDING'
c['source_binding']['reviewed_documents'][0]['read_scope']='Entire four-page published PDF and complete TeX read for source-faithful editorial preflight; no new mathematical certification or helper execution.'
c['source_binding']['editorial_candidate_source']='reviews/scope/candidate.json'
c['source_binding']['editorial_candidate_source_sha256']=h(B/'reviews/scope/candidate.json')
c['source_binding']['publication_preflight_utc']=now
assert c['follow_up'] is None and c['supplement_filename'] is None
write('candidate.json',c)
# This is an integrity inventory, not a replay of any published checker.
member_checks=[]
with zipfile.ZipFile(S/'satoh_filtration_verification.zip') as z:
 for m in z.infolist():
  if m.is_dir():continue
  data=z.read(m);p=S/'published-source/satoh_filtration_verification'/m.filename
  assert p.read_bytes()==data
  member_checks.append({'member':m.filename,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'extracted_equal':True})
assert len(member_checks)==107
embedded=S/'published-source/satoh_filtration_verification/satoh_filtration_counterexamples.pdf';assert h(embedded)==h(S/c['pdf_filename'])
source_paths=[S/'record.json',S/'receipt.json',T,embedded,B/'reviews/scope/candidate.json',B/'reviews/scope/REVIEW.md',B/'reviews/scope/ABSTRACT.tex',B/'reviews/scope/ABSTRACT.txt',B/'reviews/scope/abstract-check.json',B/'reviews/scope/primary-source-receipts.json',B/'reviews/scope/primary-read-ledger.json']
report_paths=[B/'reviews'/r/f for r in ['analytic','adversarial','scope'] for f in ['REVIEW.md','verdict.json']]
write('source-bindings.json',{'created_utc':now,'public_assets':assets,'source_and_scope_inputs':[inf(p) for p in source_paths],'complete_report_set_bindings':[inf(p) for p in report_paths],'report_binding_limit':'Mathematical reports/verdicts are existence/hash-bound here, not adjudicated. Scope report was read for editorial boundaries; root must read and reconcile all reports before promotion.','zip_member_count':len(member_checks),'zip_member_integrity':member_checks,'all_originals_unchanged':True})
write('abstract-check.json',{'created_utc':now,'source_tex':inf(T),'source_abstract_tex':inf(O/'ABSTRACT.tex'),'source_abstract_text':inf(O/'ABSTRACT.txt'),'method':'Fresh extraction of the full actual TeX abstract, exact normalization of SL/C/geq/setminus/math delimiters and whitespace, comparison with candidate text; independently read complete published PDF text.','full_abstract_equal':plain==c['abstract'],'paragraph_count':1,'omitted_sentences':0,'pdf_pages':4})
checks={
'full_source_abstract_no_omission':True,'exact_full_J_quotient_not_single_graded_piece':True,'rational_SL2_complex_matrix_entry_algebra':True,'integral_lower_central_series':True,'degree5_rank_at_least4_and_degree6_rank_at_least3':True,'explicit_automorphism_words_preserved':True,'no_every_degree_or_rank3_degree5_claim':True,'no_larger_matrix_trace_character_or_IA_comparison_claim':True,'classical_identity_credit_Burde_Razmyslov_through_Burde':True,'no_new_Lie_identity_or_PI_method_claim':True,'date_15_Oct_2026_and_archive_version_1_0_exact':True,'printed_version_not_invented':True,'two_public_assets_with_no_distinct_supplement':True,'AI_and_unrefereed_status_preserved':True,'no_worldwide_priority_or_current_openness_claim':True,'no_followup':True,'collaboration_authorship_based_on_real_contributions':True,'no_public_verification_replay':True,'candidate_only_and_root_clearance_pending':True}
write('readiness-manifest.json',{'created_utc':now,'record_id':'23387442','status':'DRAFT_PREFLIGHT_COMPLETE_ROOT_SCIENTIFIC_CLEARANCE_PENDING','mathematical_pass':None,'root_scientific_clearance':False,'promotion_created':False,'rendered':False,'website_changed':False,'publications_or_tracker_changed':False,'candidate':inf(O/'candidate.json'),'source_bindings':inf(O/'source-bindings.json'),'abstract_check':inf(O/'abstract-check.json'),'editorial_checks':checks,'remaining_gates':['Root reads and reconciles complete independent reports and explicitly grants scientific promotion.','After approval only: create publication/promotion with exact report/source hashes, integrate renderer/source-driven final-content checker, inspect rendered site.','After authorized rendering/deployment: actual desktop/mobile/PDF/download visual and live byte checks; tracker update.'],'ownership_release':'Draft preparation complete; no shared files were claimed or changed.'})
print(json.dumps({'candidate':inf(O/'candidate.json'),'readiness':inf(O/'readiness-manifest.json'),'editorial_checks':len(checks),'source_members_checked':len(member_checks)},indent=2))
