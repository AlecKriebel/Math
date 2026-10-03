"""Administrative receipts/READY only. Scientific and ROOT helpers are not run."""
import hashlib, json, os, stat
from datetime import datetime, timezone
from pathlib import Path
FAMILY = Path(__file__).resolve().parent
PREPARER = FAMILY.parent / 'original_preparation_family'
HEAD = '465d771ec1ddc91877e8d9db51ed59aea1b0d97d'
def utc(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_bytes())
def write(name,obj): (FAMILY/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def main():
    auth=load(PREPARER/'ORIGINAL_AUTHENTICATION.json'); acc=load(PREPARER/'SOURCE_ACCOUNTING.json')
    source=load(PREPARER/'original/source_record.json')
    assert auth['original_head']==acc['original_head']==HEAD
    assert auth['original_science_file_count']==17 and auth['complete_diff_file_count']==18
    assert auth['actual_merge_base_oid']=='60292bed09f59236aa192cb17aa138f7b4750e1a'
    assert auth['github_base_oid']=='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
    assert not auth['github_base_equals_actual_merge_base']
    assert source['record']['id']==30002298 and source['record']['problem_number']=='OWR-12339-004'
    assert 'research_result_for_code' in source and source['research_result_for_code'] is None
    assert (PREPARER/'original/turns.jsonl').read_bytes()==b''
    assert not acc['raw_report_key_present'] and not acc['SQL_selected_row']['report_is_SQL_NULL']
    assert acc['SQL_selected_row']['report_literal']=='{}'
    assert acc['original_used_substantive_attempts']==0 and acc['original_maximum_substantive_attempts']==5
    assert acc['original_readiness_status_literal']=='already_solved'
    refs=[]
    for name in ('original/SOURCE_STATUS.md','original/source_record.json','original/turns.jsonl',
                 'original/readiness.json','ORIGINAL_AUTHENTICATION.json','SOURCE_ACCOUNTING.json'):
        p=PREPARER/name; b=p.read_bytes()
        refs.append({'absolute_path':str(p),'bytes':len(b),'sha256':sha(b),
                     'observed_full_mode_07777':format(stat.S_IMODE(p.stat().st_mode),'04o')})
    assert refs[0]['sha256']=='fc9b927d0755ca48a61e4d2e90f5189c9d896e00a417ff8f1c10ec880bc8ec3e'
    assert refs[1]['sha256']=='def524a2a55c639160291f6308a7f19c63dca7955536e2e7086e24f255f461a0'
    write('INPLACE_SOURCE_BINDINGS.json',{'schema':'pr58-tangent-inplace-source-bindings/v1','utc':utc(),
        'original_head':HEAD,'bindings':refs,'preparer_evidence_is_not_our_Git_authentication_or_ROOT_custody':True,
        'mode_chronology_rule':'Exact observed mode, or only subsequent 0644->0444 preparer freeze with identical bytes; current full mode recorded at ROOT execution',
        'whole_primary_cache_required':False})
    write('AUDIT_ACCOUNTING.json',{'schema':'pr58-tangent-audit-accounting/v1','utc':utc(),
        'original_head':HEAD,'original_science_count_as_preparer_authenticated':17,'original_diff_count':18,
        'actual_merge_base_as_preparer_authenticated':auth['actual_merge_base_oid'],
        'GitHub_base_as_preparer_records':auth['github_base_oid'],'bases_differ':True,
        'raw_report_key_present_as_preparer_records':False,'raw_report_value':'ABSENT; no raw value',
        'SQL_report_is_NULL_as_preparer_records':False,'SQL_report_text_as_preparer_records':'{}',
        'archived_wrapper_research_result_for_code_present_directly_checked':True,
        'archived_wrapper_research_result_for_code_literal_directly_checked':None,
        'giant_corpora_or_SQL_reread_by_family':False,'preparer_accounting_reference':refs[-1],
        'original_status_json_present_as_preparer_records':False,
        'original_readiness_status':'already_solved','original_used_substantive_attempts':0,
        'original_attempt_limit':5,'original_turns_jsonl_actual_bytes':0,
        'native_selection_status_as_preparer_records':'queued','native_selection_turns':'0/5',
        'native_selection_is_dated_not_acceptance':True,'native_mutation':False,
        'audit_substantive_proof_attempt_increment':0,'novelty_or_discovery_credit':False,
        'fresh_exact_control_families':8,'original_284_6463_counts_not_fresh_evidence':True,
        'historical_review_checker_bodies_read_or_replayed':False,'other_fresh_family_findings_used':False,
        'prior_PR56_PR57_roles_disclosed':True,'universal_proof_separate_from_finite_controls':True})
    write('SOURCE_SCOPE_LOCATORS.json',{'schema':'pr58-selected-primary-locators/v1','utc':utc(),
        'receipt':'PRIMARY_SOURCE_RECEIPTS.json','selected_passages':[
            {'source':'owr_2013','printed_pages':'637-638','physical_layout_lines':[2841,2910],
             'topics':'Unit ambient density, compact union, V intersection, cancellation, exact Question1','rendered_page':60},
            {'source':'akopyan_barany_robins_v2','printed_pages':'1-2','physical_layout_lines':[24,79],
             'topics':'Definition1 and Theorem1 full statement','rendered_page':1},
            {'source':'akopyan_barany_robins_v2','printed_pages':'3-4','physical_layout_lines':[103,166],
             'topics':'a.e. algebra, union/overlap, tangent construction','rendered_page':3},
            {'source':'akopyan_barany_robins_v2','printed_pages':'8-10','physical_layout_lines':[398,520],
             'topics':'Full Lemmas5/6 proof and finite flip/overlay mechanism','rendered_pages':[8,9,10]},
            {'source':'akopyan_barany_robins_v2','printed_pages':'12','physical_layout_lines':[620,652],
             'topics':'Different vertex conventions, Remark10 exact denominator identification','rendered_page':12},
            {'source':'gravin_pasechnik_shapiro_v2','printed_pages':'3','physical_layout_lines':[137,165],
             'topics':'Simplex and partial-fraction formula; simplicity scope','rendered_page':3}],
        'eight_selected_rendered_pages_visually_read':True,
        'publisher_PDF_access':'Actual 403; failure retained privately',
        'published_metadata':'Crossref acquired and official publisher/arXiv metadata checked',
        'author_v2_not_asserted_byte_identical_to_published_version':True,
        'complete_all_paper_proofs_or_current_literature_audit':False,
        'whole_primary_PDF_bulk_text_PNG_public_redistribution':False,'private_cache_required_by_ROOT':False})
    write('READY.json',{'schema':'pr58-tangent-family-ready/v1','utc':utc(),'prepared_by_pid':os.getpid(),
        'status':'READY_FOR_ROOT_CUSTODY_AND_REVIEW','original_head':HEAD,
        'mathematical_verdict':'PASS_COMPLETE_PRIOR_GEOMETRIC_CHARACTERIZATION',
        'recommended_disposition':'already_solved','original_budget':'0/5','audit_new_turn':0,
        'credited_prior':'Akopyan-Barany-Robins, AdvMath308(2017)627-644, DOI10.1016/j.aim.2016.12.026',
        'scope':'Unit ambient Lebesgue density, compact finite polytope unions, exact triangulation V and origin exception',
        'remaining_math_gap_found':None,'novelty_claim':False,'AI_reviewed_unrefereed':True,
        'publisher_full_PDF_access_claimed':False,'exact_controls':8,'finite_controls_are_not_universal_proof':True,
        'SOURCE_index':'SOURCE.json','index_self_absent':True,'full_file_modes_07777':'0444',
        'full_directory_modes_07777':'0755','private_primary_cache_required_by_ROOT':False,
        'ROOT_close_helper':'root_close_tangent_family.py','ROOT_readback_helper':'root_readback_tangent_family.py',
        'ROOT_helpers_executed':False,'ROOT_closure_readback_claimed':False,
        'native_Git_index_remote_ref_paper_DOI_publication_actions':False})
    with (FAMILY/'RESEARCH_LOG.md').open('a') as log:
        log.write('\n- 2026-10-03 15:10:16–15:10:22 UTC — Owned primary operator22956/collector22948 '
            'acquired three PDFs,11Poppler children exit0, published Crossref metadata acquired. '
            'Publisher PDF403 with genuine private response retained; no full typeset-proof access '
            'inferred. Eight selected rendered pages read. Audit65%.\n')
        log.write('- 2026-10-03 15:13:35 UTC — Owned operator25257/collector25249 passed eight '
            'independent exact geometric control families, no failure. Universal proof separate. Audit75%.\n')
        log.write('- 2026-10-03 15:21:16 UTC — Universal denominator/iff and complete local signed '
            'chamber criterion report written. No math gap. Candidate scope includes null pieces, '
            'overlaps, holes and nonsimple cones; stronger shortcuts falsified. Audit90%.\n')
        log.write(f'- {utc()} — Typed prior/budget/merge-base/source-mode receipts prepared; '
            'original already_solved0/5 unchanged, no new math turn or novelty. Source-only ROOT '
            'helpers remain unexecuted. Lean handoff prepared. Audit95%.\n')
    print(json.dumps({'operator_pid':os.getpid(),'utc':utc(),'prepared':True,
        'inplace_references':6,'private_cache_read':False,'ROOT_helpers_executed':False,
        'fresh_exact_controls':8,'new_substantive_attempt':0},sort_keys=True))
if __name__=='__main__':main()
