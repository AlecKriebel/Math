#!/usr/bin/env python3
"""Assemble neutral source metadata only; never read mathematics or execute code.

All outputs are new source-packet files. Original API/asset/archive bytes remain
unchanged. Existing queue provenance is not a fresh native Sheet observation.
"""
from pathlib import Path
import datetime
import hashlib
import json

R=Path(__file__).absolute().parent
P=R.parents[2]

def need(ok,why):
    if not ok:
        raise ValueError(why)

def load(path):
    return json.loads(path.read_bytes())

def binding(path):
    b=path.read_bytes()
    return {'path':str(path),'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}

def write(name,value):
    with (R/name).open('x') as f:
        f.write(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def field(value,key):
    return {'present':key in value,'original_value':value.get(key)}

def main():
    need(not (R/'SOURCE_READY.json').exists(),'READY already exists; preserve earlier packet')
    a=load(R/'ACQUIRED_NATIVE.json');m=load(R/'MANUSCRIPT_CUSTODY.json');arc=load(R/'ARCHIVE_CUSTODY.json')
    q=load(R/'QUEUE_BINDING.json');record=load(R/'record.response.body');meta=record['metadata']
    need(record['id']==23130727 and q['identity_only']['sheet_row']==141,'exact target')
    need(record['status']=='published' and meta['resource_type']['type']=='publication','published paper record')
    receipts=load(R/'ALL_TRANSPORT_RECEIPTS.json')
    native={row['role']:load(Path(row['path'])) for row in a['whole_native_API_objects']}
    versions=[v for role,obj in native.items() if role.startswith('versions-page') for v in obj['hits']['hits']]
    files=native['files']
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    core_ref=P/'verification/supported-cycle-focal-independent-code-audit-sol-20261115/ACTUAL623_QUALIFIED_CORE.json'
    need(binding(core_ref)['SHA256']=='0f285e35daa206f53aa931946c4bcc6c5b01ae6b4b59a231a861b0a6fe11d104','qualified core reference')
    old_core=load(core_ref)
    core=[]
    for row in old_core['files']:
        current=binding(Path(row['path']))
        need(all(current[k]==row[k] for k in ['bytes','SHA256']),'qualified source core changed')
        core.append(current)
    write('QUALIFIED_CORE_BINDINGS.json',{'UTC':now,'reference':binding(core_ref),'original17_plus_sole_authorized405b':True,
        'all18_original_unchanged_claim':False,'files':core,'global_cache_Git_HEAD_index_constraints':False,'programs_executed':[]})
    load(R/'HELPER_READS.json')
    inputs=[{'role':'neutral existing exact queue binding; not live Sheet',**binding(R/'QUEUE_BINDING.json')},
            {'role':'source protocol base key order',**binding(R/'READY_KEY_SCHEMA.json')},
            {'role':'fully read prior metadata templates, never executed',**binding(R/'TEMPLATE_READ_LEDGER.json')},
            {'role':'fully read actual current owned helper bodies',**binding(R/'HELPER_READS.json')},
            {'role':'qualified17original plus sole405b source-only contract',**binding(R/'QUALIFIED_CORE_BINDINGS.json')},
            {'role':'source start and exposure boundary',**binding(R/'START.json')}]
    for n in ['ordinary_get.py','acquire_native.py','archive_inventory.py','manuscript_custody.py','assemble_ready.py','verify_custody.py','seal_source.py']:
        inputs.append({'role':'actual fully read owned source-custody helper',**binding(R/n)})
    for path in [P/'MODEL_POLICY.md',P.parent/'AGENTS.md']:
        inputs.append({'role':'read-only governing instruction at intake; historical by-reference pin',**binding(path)})
    write('INPUT_MANIFEST.json',{'UTC':now,'files':inputs,'queue_snapshot_provenance':q['queue_snapshot_provenance'],
        'queue_snapshot_is_historical_not_global_immutability_requirement':True,'old_queue_scientific_triage_or_target_body_read':False,
        'native_Sheet_read':False,'source_helpers_only_not_scientific_programs':True})
    texs=[]
    for original in m['all_TeX_candidates']:
        enriched=dict(original)
        enriched['opaque_byte_splitlines_count']=len(Path(original['extracted_path']).read_bytes().splitlines())
        enriched['preamble_or_mathematical_body_read']=False
        texs.append(enriched)
    chosen=m['controlling_TeX']
    associations=[{'native_PDF_key':r['original_api_file_object']['key'],'native_PDF_SHA256':r['SHA256'],
        'archived_TeX_member':chosen.get('original_member_name'),'archived_TeX_SHA256':chosen['SHA256'],
        'native_standalone_TeX_key':None,'association':'Sole archived TeX co-deposited with sole native PDF; structural custody only. No mathematical or typeset/build equivalence is assessed.'} for r in m['actual_standalone_readers']]
    readers=[]
    for original in m['actual_standalone_readers']:
        enriched=dict(original)
        enriched['structural_source_associations']=[x for x in associations if x['native_PDF_key']==original['original_api_file_object']['key']]
        enriched['scientific_role_or_typeset_equivalence_assessed']=False
        readers.append(enriched)
    ordered={
      'schema':'fresh_source_only_native_custody_126_128_v1','status':'SOURCE_READY','UTC':now,
      'record_id':a['record_id'],'sheet_row':141,'title':a['title'],'DOI':a['doi'],
      'version_field_present':a['version_field_present'],'version':a['version_original'],
      'publication_date':a['publication_date'],'created':a['created'],'updated':a['updated'],
      'native_conceptrecid_whole_field':field(record,'conceptrecid'),'native_version_whole_field':field(meta,'version'),
      'native_license_metadata_whole_field':field(meta,'license'),'native_resource_type_whole_field':field(meta,'resource_type'),
      'latest_record_id':a['latest_record_id'],'all_enumerated_version_ids':a['all_version_ids'],
      'version_enumeration_exhaustive_no_next_link':a['version_pagination_exhaustive'],
      'all_versions_total_original_fields':a['all_versions_total_original_fields'],
      'whole_native_API_objects':a['whole_native_API_objects'],'all_native_assets_in_original_order':a['all_assets_in_original_order'],
      'actual_transport_receipts':binding(R/'ALL_TRANSPORT_RECEIPTS.json'),
      'HTTP_status_sequence':[x['HTTP_status'] for x in receipts],
      'actual_ordinary_native_HTTP_requests':len(receipts),'logical_requests':len({x['logical_role'] for x in receipts}),
      'raw_non_200_response_bodies':[x for x in receipts if x.get('HTTP_status') is not None and x['HTTP_status']!=200],
      'failed_transports_preserved_whole':[x for x in receipts if x.get('error_type') is not None],
      'native_redirect_followed_from_actual_Location_only':True,'native_schema_types':binding(R/'NATIVE_SCHEMA_TYPES.json'),
      'native_schema_distinctions':{'record_swh':field(record,'swh'),'latest_swh':field(native['latest'],'swh'),
        'versions_swh_fields':[field(v,'swh') for v in versions],'versions_total_original_fields':a['all_versions_total_original_fields'],
        'files_entries_original_type':type(files['entries']).__name__,'files_order':field(files,'order'),
        'files_default_preview':field(files,'default_preview'),'original_header_order_and_duplicates_preserved':True},
      'current_native_sheet_identity_subset':None,'current_sheet_tab_and_bounds':None,'queue_binding':binding(R/'QUEUE_BINDING.json'),
      'current_native_sheet_and_fresh_published_record_identity_match':None,
      'selected_actual_PDF':m['selected_actual_PDF'],'actual_standalone_readers':readers,
      'controlling_TeX':m['controlling_TeX'],'controlling_TeX_selection_basis':m['controlling_TeX_selection_basis'],
      'all_TeX_candidates':texs,'actual_standalone_TeX_assets':m['actual_standalone_TeX_assets'],
      'embedded_PDFs':m['embedded_PDFs'],'manuscript_custody':binding(R/'MANUSCRIPT_CUSTODY.json'),
      'fresh_page_rasters':m['fresh_page_rasters'],'whole_archive_custody':binding(R/'ARCHIVE_CUSTODY.json'),
      'top_level_archive_count':arc['top_level_archive_count'],'recursive_archive_container_count':arc['recursive_archive_container_count'],
      'nested_archive_count':arc['nested_archive_count'],'whole_regular_payload_occurrences':arc['whole_regular_payload_occurrences'],
      'expanded_bytes_all_depths':arc['expanded_bytes_all_depths'],'unsafe_names':arc['unsafe_names'],
      'duplicate_or_case_colliding_names':arc['duplicate_or_case_colliding_names'],'nonregular_payloads':arc['nonregular_payloads'],
      'unsupported_nested_magic':arc['unsupported_nested_magic'],'native_CRC_size_SHA_and_whole_extracted_bytes_verified':True,
      'support_program_bindings':[x for x in arc['regular_payload_occurrences'] if Path(x['original_member_name']).suffix.lower() in ['.py','.sage','.lean','.sh','.js','.ipynb']],
      'printed_title_date_version_inspected':False,'printed_date':None,'printed_version':None,
      'target_PDF_text_extracted':False,'target_PDF_pages_rendered':True,'target_PDF_rasters_visually_read':False,
      'mathematical_PDF_TeX_or_pixels_read':False,'TeX_preamble_or_mathematical_body_read':False,
      'source_scientific_proofs_code_results_triage_reviews_or_opinions_read':False,'source_programmes_executed':[],
      'cached_bytes_reused':False,'all_original_assets_received_by_actual_fresh_native_GET':True,
      'explicit_standard_request_headers_recorded_in_sent_order':True,'custom_auth_proxy_query_retry_or_bypass_tricks_used':False,
      'ignored_assets_and_extraction_paths_established_before_acquisition':True,'source_directory_preexisting':False,
      'originals_overwritten':False,'old_source_collectors_builders_or_scientific_campaigns_executed':False,
      'queue_Sheet_Git_site_or_old_packet_changes':[],
      'exposure_limit':'Existing exact inventory queue neutral identity subset; fresh native record/latest/allversions/files metadata and whole original assets; opaque archive/file/CRC/hash custody; actual standalone PDF metadata and fresh unread rasters; opaque TeX byte-line count only. No PDF text/pixels, TeX preamble/body, native scientific code/results, archived/current target opinions or old queue triage read. Current native Sheet was not accessed; its base fields are explicitly null rather than fabricated.',
      'scientific_verdict':None,'publication_authority':False,'completion_percent_at_preseal':100}
    schema=load(R/'READY_KEY_SCHEMA.json')
    need(list(ordered)==schema['SOURCE_READY_key_order'],'base READY key order')
    ordered.update({'source_custody_schema_additions':'Complete-record reader/source associations and explicit queue-only identity provenance, preserving base key order and whole original native objects.',
      'additional_controlling_TeX_sources':[x for x in texs if x['extracted_path']!=chosen['extracted_path']],
      'controlling_TeX_sources_in_original_archive_order':texs,
      'native_reader_source_structural_associations':associations,
      'whole_record_source_reading_requirement_for_future_science':'Before scientific reconstruction read every actual standalone reader and every controlling/additional source. No mathematical role or edition equivalence is determined during neutral custody.',
      'all_native_reader_total_pages':m['all_native_reader_total_pages'],
      'source_mapping_is_structural_only_no_typeset_or_scientific_equivalence_certified':True,
      'source_identity_binding':binding(R/'NATIVE_IDENTITY_MATCH.json'),
      'source_identity_provenance_qualification':'Existing inventory queue plus fresh native Zenodo identity only. No fresh native Sheet/tab/bounds/eligibility read; corresponding inherited fields are null.',
      'qualified_core_original17_plus_authorized405b':binding(R/'QUALIFIED_CORE_BINDINGS.json')})
    write('SOURCE_READY.json',ordered)
    with (R/'SOURCE_LOG.md').open('a') as f:
        f.write('\n'+now+' — 90%: Complete SOURCE_READY assembled in original base field order; live-Sheet fields explicitly unknown/null, existingqueue/native identity separately bound. Source/science body/pixels/programs/results/opinions remain unread. Strict closure/seal pending.\n')
    print(json.dumps({'status':'SOURCE_READY_PRESEAL','record_id':23130727,'source_only':True,'scientific_verdict':None,
        'PDF_pages':m['PDF_pages'],'TeX_lines':chosen['opaque_byte_splitlines_count'],'native_assets':len(a['all_assets_in_original_order']),
        'archive_regular_payloads':arc['whole_regular_payload_occurrences'],'native_Sheet_read':False,'publication_authority':False}))

if __name__=='__main__':
    main()
