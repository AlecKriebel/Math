import datetime, hashlib, json, pathlib

root = pathlib.Path(__file__).resolve().parent
cache = pathlib.Path('/Users/alec/.cache/codex-pr65-priority-20261004/analytic_c64ad1e1f0204e27a20201fa06b7ab5c')
utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
pins = json.loads((root/'source_pins.json').read_text())
additional = [('carmona_donaire1999.pdf','/Users/alec/.cache/codex-pr65-priority-20261004/carmona_donaire1999.pdf'),
              ('aan1999.pdf','/Users/alec/.cache/codex-pr65-priority-20261004/aan1999.pdf'),
              ('hayman2019.pdf','/Users/alec/.cache/codex-pr65-priority-20261004/provided_primary_sources_20261004/hayman2019.pdf')]
for name,path in additional:
    pins['sources'].append({'name':name,'input_path':path,'private_copy':str(cache/name),'sha256':sha(cache/name)})
pins['private_artifact_inventory'] = [{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    for p in sorted(cache.rglob('*')) if p.is_file()]
pins['updated_utc'] = utc
(root/'source_pins.json').write_text(json.dumps(pins,indent=2)+'\n')

readings = [
 {'source':'duren1966.pdf','text_scope':'complete body','printed_pages':[247,248,249,250,251,252,253,254],
  'images':[str(cache/f'duren1966-{i}.png') for i in range(1,9)]},
 {'source':'piranian1966.pdf','text_scope':'complete body','printed_pages':[255,256,257,258,259,260,261,262],
  'images':[str(cache/f'piranian1966-{i}.png') for i in range(1,9)]},
 {'source':'carmona_donaire1999.pdf','text_scope':'relevant definitions and theorem plus adjoining extracted context',
  'printed_pages':[207,208],'images':[str(cache/f'carmona_donaire1999-{i:02}.png') for i in (3,4)]},
 {'source':'aan1999.pdf','text_scope':'printed pp.318-320 and 326-329',
  'printed_pages_visually_checked':[320,326,327,328,329],
  'images':[str(cache/f'aan1999-{i:02}.png') for i in (3,9,10,11,12)]},
 {'source':'hayman2019.pdf','text_scope':'Problem and Update5.51 and adjacent page context',
  'printed_pages':[121,122],'images':[str(cache/f'hayman2019-{i}.png') for i in (127,128)]},
]
for r in readings:
    r['sha256'] = sha(cache/r['source'])
    r['image_hashes'] = {p:sha(pathlib.Path(p)) for p in r['images']}
    r['inspection_tool'] = 'functions.exec tools.view_image API'
    r['inspection_subprocess_pid'] = None
    r['inspection_note'] = 'API image views do not supply a subprocess PID; none is fabricated.'
record = {'recorded_utc':utc,'recording_time_is_not_per_call_execution_time':True,
          'complete_1966_scan_inspection_confirmed':True,
          'first_conclusion_saved_before_review_opinions':True,
          'review_opinion_bodies_read':[], 'readings':readings}
(root/'source_read_record.json').write_text(json.dumps(record,indent=2)+'\n')

# Add exact inline-code/argv body hashes to existing genuine receipts without
# changing their historical PID, argv, cwd, timestamps, streams, or runner pin.
for p in sorted((root/'receipts').glob('*.json')):
    d=json.loads(p.read_text())
    d['argv_body_sha256']=hashlib.sha256(json.dumps(d['argv'],ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    if '-c' in d['argv']:
        idx=d['argv'].index('-c')
        d['inline_code_sha256']=hashlib.sha256(d['argv'][idx+1].encode()).hexdigest()
    d['receipt_metadata_enriched_utc']=utc
    p.write_text(json.dumps(d,indent=2)+'\n')

verdict = {
 'schema':'pr65-analytic-priority-verdict-v1','completed_utc':utc,
 'family':'Herglotz / Cayley / canonical factorization / domain precomposition',
 'target':{'pure_blaschke':True,'B_at_zero':0,'bloch_cayley':'(1+B)/(1-B)'},
 '1966_literal_normalized_pure_blaschke_cayley_answer':False,
 '1966_literal_cayley_formula':False,
 '1966_printed_fully_fixed_measure_rule':True,
 '1966_printed_bloch_herglotz_equivalence':True,
 '1966_printed_all_point_finite_positive_derivative_exclusion':True,
 '1966_effective_target_adapter_verified_as_present_deduction':True,
 '1966_historical_complete_adapter_printed':False,
 '1966_adapter_requires_generic_frostman_parameter':False,
 'classification':'Printed effective antecedent data, not a literally printed target theorem; the exact target follows by a checked classical adapter.',
 'AAN1999':{'theorem2_pure_covering_blaschke_verified':True,
    'quadratic_weight_cayley_application_literally_printed':True,
    'domain_precomposition_at_zero_preserves_purity':True,
    'normalized_exact_target_adapter_verified':True,'cayley_bloch_seminorm_upper_bound':8,
    'printed_normalization_adapter_located':False},
 'HL2019':{'update551_read':True,'printed_pages':[121,122],
    'explicit_construction_attribution_to_AAN':True,
    'literal_update_asserts_inner_I_rather_than_normalized_pure_B':True,
    'historical_explicit_need_not_mean_finite_algebraic_recursion':True},
 'new_mathematical_claim_verified':False,
 'submitted_candidate_correctness_falsified_by_these_sources':False,
 'full_submitted_candidate_correctness_audit_performed':False,
 'new_construction_mechanism_priority_supported':False,
 'first_explicit_answer_priority_supported':False,
 'exact_submitted_sign_rule_literally_found_in_1966':False,
 'global_earliest_articulation_of_1966_adapter_established':False,
 'required_package_corrections':'REPORT.md, Required package corrections and remaining novelty scope',
 'original_proof_search_turns_added':0,
 'publication_permission':False,'external_outreach':False,'shared_mutations':False,
 'audit_completion_percent':100,'verified_novel_contribution_percent':0,
 'limitations':['No global earliest-date audit','Original Loomis1943 body not read',
                'No conventional human peer review or formal proof-system verification',
                'Not a complete correctness audit of the submitted proof']}
(root/'verdict.json').write_text(json.dumps(verdict,indent=2)+'\n')
with (root/'RESEARCH_LOG.md').open('a') as f:
    f.write(f'''\n- {utc}: Independently checked Carmona-Donaire pp.207-208 in scans; positivity,
  nontangential limits, ordinary density and normalized circle weights all
  match the purity adapter. Finite exact old-rule checks at levels0-8 and
  the first nontrivial Cayley-stage identity passed. Two-paper analytic
  classification/adapter completion estimate: 100%; global novelty goal:
  0% verified, no new mathematical contribution established.
- {utc}: After FIRST_CONCLUSION, independently checked the requested AAN
  quadratic-weight adapter, purity under domain automorphism, and HL2019
  primary Update5.51. AAN's target adapter is complete with Bloch seminorm
  at most8; its Cayley bound is literally printed, while normalization is
  the checked deduction. Saved REPORT, verdict and reading coverage.
  Assigned audit completion estimate: 100%; publication approval: absent.
''')
print(json.dumps({'completed_utc':utc,'verdict':'No new mathematical claim verified; complete classical adapters checked',
                  'audit_completion_percent':100,'public_folder':str(root),
                  'private_sources':str(cache)},indent=2))
