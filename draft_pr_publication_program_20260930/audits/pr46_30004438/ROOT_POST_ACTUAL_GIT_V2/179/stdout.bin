"""Author PR46 SOURCE-only contracts. Production is handled strictly as text."""
from pathlib import Path
import datetime as dt, hashlib, json, os
F=Path(__file__).resolve().parent
A=F.parent
R=A.parents[2]
B=R/'draft_pr_publication_program_20260930/audits/pr45_9900007/current_preparation_family'
def write(name,raw):
    if isinstance(raw,str): raw=raw.encode()
    with (F/name).open('xb') as handle: handle.write(raw); handle.flush(); os.fsync(handle.fileno())
def js(name,obj): write(name,json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def main():
    # These are source-text administrative patterns only, never executed here.
    basis=(B/'prepare_current_packet.py').read_text()
    op=(B/'capture_root_builder_operation.py').read_text()
    write('READ_PR45_ADMINISTRATIVE_BUILDER_BASIS.py',basis)
    write('READ_PR45_ADMINISTRATIVE_OPERATOR_BASIS.py',op)
    prefix=basis[:basis.index('def build(')]
    prefix=prefix.replace('PR45','PR46').replace('1/5','0/5')
    prefix=prefix.replace("HEAD = 'd9b4acf5d070d1f04ffac86a4f08916a5629ff16'", "HEAD = 'a39d178b10f75fb127058b08e0d0002b3ae97f8a'")
    prefix=prefix.replace("MERGE_BASE = '01358d66fc67d1c462bddf31c0d4ee5b120e6737'", "MERGE_BASE = BASE")
    prefix=prefix.replace("SCIENCE = '7123c345d3ecdf4fecb8941596687da54c44e169831eb23177ea485fa8386722'", "SCIENCE = 'a0d374da6984537cd9902e2e790177791739bdc32ea820b74830a6b50241ea6c'")
    flags=['original13_complete14_path_diff_helpers_results_metadata_fully_read',
      'operative_OWR668669_v1Theorem2_Section22_v2Example1_Lemma9_Theorem3_fully_read',
      'every_degree_all_periods_RP1_full2dplus1_ordinary_real_open_proof_accepted',
      'whole_raw_SQL_prior_presence_or_null_and_literal_empty_fallback_fully_read',
      'unchanged_author51_and_independent848_actual_reproductions_fully_read',
      'both_closed_independent_math_families_fully_read',
      'scoped_original_closure_family_exclusions_first_party_topology_checked',
      'known_Kozhasov_Kummer_preprint_credit_no_discovery_scope_accepted',
      'new_source_adversary_closed_clean_complete_report_personally_read']
    a=prefix.index('FLAGS = '); b=prefix.index('\nHEADER = ',a)
    prefix=prefix[:a]+'FLAGS = '+repr(flags)+prefix[b:]
    a=prefix.index('IMMUTABLE = '); b=prefix.index('\n\ndef require',a)
    immutable=['SOURCE_STATUS.md','verification.json','verify.py','source_record.json','turns.json',
      'provenance.json','independent_review/independent_checks.py','independent_review/independent_results.json']
    prefix=prefix[:a]+'IMMUTABLE = '+repr(immutable)+prefix[b:]
    prefix=prefix.replace("and '\\\\' not in value", "and '\\\\' not in value and '\\0' not in value")
    write('prepare_current_packet.py',prefix+(F/'BUILDER_BODY.source.txt').read_text())
    op=op.replace('PR45','PR46').replace('pr45_9900007','pr46_30004438').replace('pr45_current','pr46_current')
    write('capture_root_builder_operation.py',op)
    root_common={'created_utc':None,'reading_completed':False,'root_flags':{k:False for k in flags},
      'reading_notes':'DRAFT only; ROOT must independently author its actual reading after source closure.',
      'scope_certificate_sha256':None,'preparation_manifest_sha256':None,'source_qualification_sha256':None,
      'evidence_bindings_sha256':None,'family_manifest_sha256':{},'original_substantive_attempts':0,
      'original_source_verification_responses':1,'new_substantive_attempts':0,'audit_turns':0}
    js('DRAFT_ROOT_READ_LEDGER.json',dict(root_common,schema='PR46_ROOT_PRIMARY_READ_LEDGER_v1'))
    js('DRAFT_ROOT_SCIENCE_CARD.json',dict(root_common,schema='PR46_ROOT_SCIENCE_CARD_v1',status='already_solved',
      exact_known_target_verified=False,full_problem_solved=False,full_target_prior_result_verified=False,project_solved=False,novelty_claimed=False,turn_limit=5,
      read_ledger_sha256=None,current_input_manifest_sha256=None,new_whole_current_gate='PENDING',
      paper_created=False,new_DOI_created=False,tracker_row_created=False,current_model=None,
      current_reasoning_effort=None,current_deadline_utc=None,current_verdict=None,
      existing_result_credit=['Khazhgali Kozhasov','Mario Kummer'],source_publication_kind='preprint'))
    js('DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json',{'schema':'PR46_ROOT_FRESH13_INPUT_PREIMAGES_v1',
      'approved_by_root':False,'created_utc':None,'reason':'DRAFT; complete ROOT current bindings are pending.',
      'current_head':None,'files':[]})
    js('DRAFT_ROOT_EVIDENCE_BINDINGS.json',{'schema':'PR46_ROOT_EVIDENCE_BINDINGS_v1','approved_by_root':False,
      'created_utc':None,'notes':'DRAFT only. ROOT actual evidence anchors and typed summaries are pending.',
      'manifest':None,'proof_notes':None,'summary':None,'raw_audit':None,'source_adversary':None})
    write('DRAFT_ROOT_CURRENT_KNOWN_RESULT_SCOPE_CERTIFICATE.md',
      '# DRAFT PR46 exact known-result scope certificate\n\nNo acceptance sentinel is supplied. ROOT must separately author the actual certificate after its reading and the new source adversary. Status proposed: already_solved; original0/5, source-verification responses1, new0, audit0. Full target verification is pending in this draft. Existing result credit: Khazhgali Kozhasov and Mario Kummer (2020 preprint). No novelty, paper, new DOI or tracker.\n')
    js('SOURCE_STATUS.json',{'schema':'PR46_CURRENT_SOURCE_ONLY_STATUS_v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
      'status':'SOURCE_ONLY_ROOT_PREREQUISITES_PENDING','builder_executed':False,'ROOT_operator_executed':False,
      'production_import_compile_or_execution':False,'ROOT_approval':None,'actual_current_freeze':False,
      'new_source_adversary':None,'new_whole_current_verdict':None,'current_model':None,
      'current_reasoning_effort':None,'current_deadline_utc':None,'current_verdict':None,
      'historical_source_fields_are_attribution_only':True,'original_substantive_attempts':0,
      'original_source_verification_responses':1,'new_substantive_attempts':0,'audit_turns':0,
      'paper_created':False,'new_DOI_created':False,'tracker_row_created':False,'new_discovery_credit_percent':0})
    print(json.dumps({'actual_pid':os.getpid(),'status':'AUTHORED_SOURCE_ONLY_DRAFTS',
      'production_import_compile_or_execution':False,'ROOT_approval':None,'builder_sha256':hashlib.sha256((F/'prepare_current_packet.py').read_bytes()).hexdigest()}))
if __name__=='__main__': main()
