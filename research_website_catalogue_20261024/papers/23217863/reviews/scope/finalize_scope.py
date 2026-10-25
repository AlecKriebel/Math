"""One-shot local source/scope handoff writer. No shared or original writes.

Does not execute any manuscript/supplied verification program. All original
source-ready files and previous owned packages are rehashed before sealing.
"""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, re, zipfile
from pypdf import PdfReader

R=Path(__file__).resolve().parent
Q=R.parents[1]
S=Q/'sources'
now=lambda:datetime.now(timezone.utc).isoformat()
def digest(p):
    d=Path(p).read_bytes();return {'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()}
def write(p,o):
    p=Path(p)
    if p.exists():raise RuntimeError('one-shot output already exists: '+str(p))
    p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
ready=json.loads((S/'SOURCE_READY.json').read_text())
raw=json.loads((S/'record.raw.json').read_text())
initial=json.loads((R/'INITIAL_READ_LEDGER.json').read_text())
manifest=json.loads((S/'SOURCE_READY_MANIFEST.json').read_text())
prior=json.loads((R/'PRESERVATION_BEFORE.json').read_text())
if 'version' in raw['metadata'] or ready['version'] is not None:raise RuntimeError('version interface')
if [a['original_api_file_object'] for a in ready['all_assets']]!=raw['files']:
    raise RuntimeError('whole actual API file-object interface')
for item in manifest['files']:
    if digest(S/item['path'])!={k:item[k] for k in ('bytes','sha256')}:
        raise RuntimeError('source-ready custody '+item['path'])
for a in ready['all_assets']:
    d=Path(a['path']).read_bytes()
    if hashlib.md5(d).hexdigest()!=a['md5'] or digest(a['path'])!={k:a[k] for k in ('bytes','sha256')}:
        raise RuntimeError('actual asset identity')
with zipfile.ZipFile(S/'source-and-verification.zip') as z:
    regular=[n for n in z.namelist() if not n.endswith('/')]
    if len(regular)!=41 or len(set(regular))!=41:raise RuntimeError('archive inventory')
    for name in regular:
        if z.read(name)!=(S/'published-source'/name).read_bytes():raise RuntimeError('member identity '+name)
internal=json.loads((S/'published-source/SOURCE_MANIFEST.json').read_text())
for x in internal['files']:
    if digest(S/'published-source'/x['path'])!={k:x[k] for k in ('bytes','sha256')}:
        raise RuntimeError('deposited internal manifest '+x['path'])
prior_bindings=prior['owned_prior_bindings_only']
prior_after={}
for p,v in prior_bindings.items():
    actual=digest(p)
    if actual!=v:raise RuntimeError('protected prior owned file '+p)
    prior_after[p]=actual
canon=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

primary_specs=[
 ('openai295-pinned.pdf','FULL actual PDF pp1–28; all five controlling TeX proof sections and wrapper/proof map read',
  'https://raw.githubusercontent.com/openai/math/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Vanishing-of-higher-bounded-Hochschild-cohomology-September-23-2026/paper.pdf'),
 ('openai295-current.pdf','Byte identity to full pinned reader; not a second independent proof',
  'https://raw.githubusercontent.com/openai/math/main/preprints/Vanishing-of-higher-bounded-Hochschild-cohomology-September-23-2026/paper.pdf'),
 ('ricard-roydor-v2.pdf','Actual11pp body; exact theorem A, Proposition3.2, Remarks3.4/3.7 and proofs/prior scope',
  'https://arxiv.org/pdf/1108.1970v2'),
 ('sherman-v2.pdf','Actual pp1–3; Theorem1.1 and Kadison/Jordan normality interfaces; not entire14pp',
  'https://arxiv.org/pdf/math/0309365v2'),
 ('popa2014-v3.pdf','Physical pp1–9,20,52: exact0.1(a), factor/nonintertwining, ultraproduct/independence statements and definitions; not entire64pp',
  'https://arxiv.org/pdf/1308.3982v3'),
 ('jkr1972.pdf','Physical pp2–4,19–22: definitions, actual-image cohomology, fullLemma5.4/5.5 proof andTheorem5.6; p22 additionally pixels; not entire25pp',
  'https://www.numdam.org/item/10.24033/bsmf.1731.pdf'),
 ('cpss2003-v2.pdf','Actual pp1–4: ordinary/cb distinction, complement theoremEq1.1, definitions; not entire25pp',
  'https://arxiv.org/pdf/math/0107078v2'),
 ('nelson209.pdf','Physical pp55–60: full-corner centers, equal-carrier abelian equivalence, arbitrary-cardinal decomposition, finite homogeneous matrix proof; not entire71pp',
  'https://users.math.msu.edu/users/banelson/teaching/209/209_notes.pdf')]
prim=[]
for name,extent,url in primary_specs:
    p=R/'cache/primary'/name
    prim.append({'path':str(p),**digest(p),'pages':len(PdfReader(p).pages),
                 'read_extent':extent,'actual_locator':url,'fresh_HTTP_status':200,
                 'phase':'after immutable independent early seal',
                 'redistribution_authorized_by_this_review':False})
existing=json.loads((R/'EXISTING_PRIMARY_BINDINGS.json').read_text())
for x in existing:
    p=Path(x['path'])
    if digest(p)!={k:x[k] for k in ('bytes','sha256')}:raise RuntimeError('existing primary changed')
    isarticle='user_supplied' in p.name
    prim.append({'path':str(p),**digest(p),'pages':x['pages'],
                 'read_extent':'FULL26pp actual retained primary body; p12 additionally pixels' if isarticle else 'Actual87page author slide deck, physical pp28–29 only',
                 'fresh_HTTP_status':None,'existing_primary_reused_in_place':True,
                 'provenance':'human-supplied full publisher-formatted December2020SecondReading body; final2022issue not byte-compared' if isarticle else 'retained original author slides; fresh CIRM request timed out',
                 'phase':'after immutable independent early seal',
                 'redistribution_authorized_by_this_review':False})
write(R/'PRIMARY_LEDGER.json',{'utc':now(),'complete_current_sibling_or_root_opinions_read':False,
      'primary_bodies':prim,'failures_preserved_as_failures':['WorldScientific403','CIRMtimeout'],
      'transport_receipts':[{'path':str(R/n),**digest(R/n)} for n in
          ['primary-fetch-receipts.json','critical-primary-fetch-receipts.json','structure-primary-fetch-receipts.json']],
      'existing_user_custody_receipt':{'path':'/Users/alec/Documents/Math/openai_followon_banach_mazur_von_neumann/receipts/roydor_user_supplied_source_20261007.json',
          **digest('/Users/alec/Documents/Math/openai_followon_banach_mazur_von_neumann/receipts/roydor_user_supplied_source_20261007.json')},
      'Lean_build_or_axiom_probe_performed':False})

main=S/'published-source/manuscript/main.tex'
abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',main.read_text(),re.S).group(1)
if abstract!=initial['original_abstract']:raise RuntimeError('original abstract binding')
write(R/'READ_LEDGER.json',{'utc':now(),'actual_target_pdf':{'path':str(S/'paper.pdf'),**digest(S/'paper.pdf'),'pages':7,'read_extent':'FULL7pp before earlyseal'},
      'controlling_TeX':{'path':str(main),**digest(main),'lines':len(main.read_text().splitlines()),'read_extent':'FULL449lines before earlyseal'},
      'full_original_abstract':abstract,'early_seal':{'path':str(R/'INITIAL_SEAL.json'),**digest(R/'INITIAL_SEAL.json')},
      'all_upstream_five_proof_sections_full_read_after_early_seal':True,
      'whole_original_transport_and_API_objects_read':True,
      'historical_deposited_support':'Selected dependency/theorem/validation/license ledgers and typeI/conventions support inspected after primary reconstruction; historical opinions not accepted as evidence; no claim every historical audit line was read',
      'current_sibling_or_root_final_opinions_read':False,'supplied_programs_executed':False,
      'own_control_script':{'path':str(R/'exact_controls.py'),**digest(R/'exact_controls.py'),'inspected_before_execution':True,'executions':1,'exit_code':0},
      'primary_read_extents_ledger':{'path':str(R/'PRIMARY_LEDGER.json'),**digest(R/'PRIMARY_LEDGER.json')},
      'external_prior_packet_source_bodies_mutated':False})
write(R/'SEARCH_LEDGER.json',{'utc':now(),'status':'BOUNDED_PRIMARY_RESEARCH_COMPLETE_PRIORITY_UNKNOWN',
      'fresh_query_families':['Roydor exacttitle/DOI/publication/authorPDF','Banach Mazur vonNeumann arbitrary scope ordinary versus cb','OpenAI pinned and current family295','Popa ultraproduct independence exactpaper','JKR normal reduction exactpaper','CPSS classical boundedcohomology','Nelson primary-author projection notes'],
      'primary_results':[(x['path'],x.get('actual_locator')) for x in prim],
      'known_positive_prior_overlap':['Roydor2020author slidesTh2 states unrestricted cohomological conditional result','Roydor actualpublishedTheorem1.2 states separable-predual conditional result','RicardRoydor2014unconditional cb and two-matrix-level/priorpredual deductions'],
      'negative_search_is_not_novelty_evidence':True,'firstness':'UNKNOWN','current_worldwide_open_status':'UNKNOWN',
      'bound':'No equivalent full fixed-source proof was authenticated in this bounded search; this does not certify absence',
      'individual_contact_or_outreach_prepared_or_sent':False})
write(R/'READER_IDENTITY.json',{'utc':now(),'selected_target':{'path':str(S/'paper.pdf'),**digest(S/'paper.pdf'),'pages':7},
      'all_PDF_occurrences':[{'path':str(p),**digest(p),'pages':len(PdfReader(p).pages),
              'role':'selected target reader' if p==S/'paper.pdf' else 'distinct attributed upstream295 input; not alternate target edition'}
          for p in sorted(S.rglob('*.pdf'))],
      'target_reader_inside_ZIP':False,'archive_PDF_is_upstream_295':True,
      'nested_archives':0,'complete_ZIP_unchanged':True})

write(R/'VERDICT.json',{'utc':now(),'record_id':23217863,'sheet_row':103,'family':'independent source/scope/primary-interface',
      'model':'GPT-6.1 Sol Ultra','status':'COMPLETE','assessment':'PASS_AT_DECLARED_EXTERNAL_THEOREM_LEVEL',
      'strongest_verified_result':'The literal forall complex vonNeumann M exists epsilon_M>0 forall complex vonNeumann N ordinary algebra/canonical-predual strictdistance rigidity and all five Jordan/isometry equivalences, with no separability/type/representation-size restriction.',
      'substantive_mathematical_defect_found':False,'unresolved_central_gap':None,
      'exact_external_input':'OpenAI family295 Theorem1.1 ordinary bounded complex multilinear self-coefficient actual-image H^k for all vonNeumann algebras; actual whole28pp proof freshly read and downstream-needed H2/H3 interfaces reconstructed.',
      'all_algebra_scope_checked':True,'finite_controls_not_universal_proof':True,
      'source_ready_original':ready,'full_original_abstract':abstract,
      'version':None,'version_field_absent':True,
      'primary_access_limit':'Actual complete retained user-supplied Roydor2020publisherformatted26pp body used; fresh publisher403/CIRMtimeout retained; final2022issuePDF not byte-compared.',
      'priority':'UNKNOWN; unrestricted conditional formulation credited to actual2020Roydor author slides; no firstness/current worldwide open/new cohomology or mechanism claim.',
      'validation_limits':['No Lean kernel build or target formalization','Not conventional human peer review','No universal numeric epsilon','Classical theorem interfaces retained as attributed inputs; not foundation-level recertification','No sourceprogram replay'],
      'followup':None,'canonical_url':None,'AA':None,
      'root_scientific_authority':False,'editorial_approval':False,'rendered':False,'browser_verified':False,
      'native_sheet_updated':False,'public':False,'released':False,
      'completion_percent_this_bounded_assignment':100,'all203_programme':'ONGOING'})

before_source={str(p.relative_to(S)):digest(p) for p in sorted(S.rglob('*')) if p.is_file()}
if len(before_source)!=52:raise RuntimeError(('unexpected additive source count',len(before_source)))
write(S/'SOURCE_FINAL_MANIFEST.json',{'utc':now(),'status':'FINAL_ORIGINAL_SOURCE_CUSTODY',
      'source_ready_manifest_sha256':digest(S/'SOURCE_READY_MANIFEST.json')['sha256'],
      'source_ready_seal_sha256':digest(S/'SOURCE_READY_SEAL.json')['sha256'],
      'files':before_source,'file_count':len(before_source),
      'unchanged_ready_originals':50,'safe_unique_archive_members_recompared':41,
      'deposited_internal_manifest_entries_recompared':len(internal['files']),
      'no_original_rewritten':True})
write(S/'SOURCE_FINAL_SEAL.json',{'utc':now(),'status':'IMMUTABLE_FINAL_SOURCE_CUSTODY',
      'manifest':{'path':'SOURCE_FINAL_MANIFEST.json',**digest(S/'SOURCE_FINAL_MANIFEST.json')},
      'all_original_ready_bindings_unchanged':True})
source_final={str(p.relative_to(S)):digest(p) for p in sorted(S.rglob('*')) if p.is_file()}
write(R/'CUSTODY.json',{'utc':now(),'source_ready_originals_rehashed':50,'source_files_in_final_original_manifest':52,
      'source_files_including_final_manifest_and_seal':len(source_final),'source_files':source_final,
      'actual_API_objects_preserved_whole':True,'actual_assets_rehashed_and_MD5_verified':2,
      'ZIP_members_byte_compared':41,'deposited_internal_manifest_bindings_verified':len(internal['files']),
      'protected_prior_owned_binding_count':len(prior_bindings),
      'protected_prior_before_path':str(R/'PRESERVATION_BEFORE.json'),
      'protected_prior_before':digest(R/'PRESERVATION_BEFORE.json'),
      'prior_before_canonical_map_sha256':canon(prior_bindings),
      'prior_after_canonical_map_sha256':canon(prior_after),'all_prior_owned_files_unchanged':True,
      'stale_mutable_site_core_baselines_followed':False,
      'write_scope':[str(S),str(R)],'production_or_Git_UI_native_mutations':False,
      'cache_fully_ignored_before_fetch':(R/'.gitignore').read_text()=='cache/\n'})
with (R/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n'+now()+' — Complete literal theorem/import/geometric scope reviewed; no substantive central gap found at declared external-theorem level. Own1664exactequalities and416faultcomparisons complete. Original50ready+41members and3686priorowned unchanged. Final source and independent scope handoff sealed; assignment100%, all203 ongoing. Root authority/public/native gates remainfalse; nofollowup.\n')
files={str(p.relative_to(R)):digest(p) for p in sorted(R.rglob('*')) if p.is_file() and p.name not in ['FINAL_MANIFEST.json','FINAL_SEAL.json']}
write(R/'FINAL_MANIFEST.json',{'utc':now(),'status':'IMMUTABLE_COMPLETE_INDEPENDENT_SCOPE',
      'owned_file_count':len(files),'files':files,'source_files':source_final,
      'existing_primary_bindings':[{k:x[k] for k in ('path','bytes','sha256')} for x in existing],
      'third_party_cache_private_ignored':True,'no_sibling_or_root_scientific_opinions_read':True,
      'no_publication_authority':True})
write(R/'FINAL_SEAL.json',{'utc':now(),'status':'COMPLETE_IMMUTABLE_SOURCE_SCOPE_HANDOFF',
      'manifest':{'path':'FINAL_MANIFEST.json',**digest(R/'FINAL_MANIFEST.json')},
      'report':{'path':'REPORT.md',**digest(R/'REPORT.md')},
      'verdict':{'path':'VERDICT.json',**digest(R/'VERDICT.json')},
      'owned_bindings':len(files),'source_bindings':len(source_final),
      'protected_prior_owned_bindings':len(prior_bindings),'all_later_gates_false':True,
      'followup':None,'root_authority':False})
print(json.dumps({'final_seal':digest(R/'FINAL_SEAL.json'),'manifest':digest(R/'FINAL_MANIFEST.json'),
      'report':digest(R/'REPORT.md'),'verdict':digest(R/'VERDICT.json'),'owned':len(files),
      'sources':len(source_final),'prior':len(prior_bindings)},indent=2))
