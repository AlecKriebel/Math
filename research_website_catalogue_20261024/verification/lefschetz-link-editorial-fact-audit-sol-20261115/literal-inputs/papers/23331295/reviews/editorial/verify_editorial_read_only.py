"""Standalone offline custody/data closure. No project imports, writes or runs.

Does not import the authoring helper, semantic checker, controls, source code or
owner programmes. --payload-only is the explicitly recorded preseal phase.
"""
from pathlib import Path
import hashlib
import json
import sys

CONTROL = {'MANIFEST.json','SEAL.json','CLOSURE_NORMAL.stdout.json','CLOSURE_NORMAL.stderr',
           'CLOSURE_OPTIMIZED.stdout.json','CLOSURE_OPTIMIZED.stderr','CLOSURE_RECEIPT.json'}


def need(value, message):
    if not value: raise ValueError(message)


def sha(raw): return hashlib.sha256(raw).hexdigest()
def obj(path): return json.loads(Path(path).read_bytes())
def same(a,b):
    need(type(a) is type(b) and json.dumps(a,ensure_ascii=False,separators=(',',':'),allow_nan=False)==
         json.dumps(b,ensure_ascii=False,separators=(',',':'),allow_nan=False),'whole typed/key/list ordered object differs')


def bound(path, row):
    path=Path(path);need(path.is_file() and not path.is_symlink(),'absent/symlink: '+str(path));raw=path.read_bytes()
    need(len(raw)==row['bytes'] and sha(raw)==row['SHA256'],'whole byte binding differs: '+str(path));return raw


def verify(root, payload_only=False):
    root=Path(root);protected=obj(root/'PROTECTED_INPUTS.json'); source=root.parent.parent/'sources'
    for row in protected['files']+protected['additional_root_authority_and_existing_primary_bindings']:bound(row['path'],row)
    source_rows=[row for row in protected['files'] if source in Path(row['path']).parents]
    need(len(source_rows)==65 and {str(p) for p in source.rglob('*') if p.is_file()}=={r['path'] for r in source_rows},'whole original65-source namespace')
    for name,key in [('publication.json','top_level_publication_preexisted'),('promotion.json','top_level_promotion_preexisted')]:
        need((root.parent.parent/name).exists()==protected[key],'no paper-level configuration creation')
    protocol=obj(root/'SOURCE_PROTOCOL_BINDINGS.json');wrapper_count=0
    def wrappers(value):
        nonlocal wrapper_count
        if isinstance(value,dict):
            if 'whole_literal_object' in value and 'path' in value:
                raw=bound(value['path'],value);same(json.loads(raw),value['whole_literal_object']);wrapper_count+=1
                if 'raw_blob' in value:need(raw==(root/value['raw_blob']).read_bytes(),'whole original raw JSON blob')
            for child in value.values():wrappers(child)
        elif isinstance(value,list):
            for child in value:wrappers(child)
    wrappers(protocol)
    ready=protocol['whole_original_SOURCE_READY']['whole_literal_object'];authority=protocol['whole_root_scientific_authority']['whole_literal_object']
    need(protocol['whole_root_scientific_authority']['SHA256']=='a4dbd16bc3bd3bb81b674183f3c75f87d1234b5a0facb89320bb8f08a3b5ed25','exact root science authority')
    need(ready['record_id']==23331295 and ready['version']=='1.0' and ready['publication_date']=='2026-10-12','actual native identity')
    need(ready['printed_version'] is None and ready['mathematical_PDF_TeX_or_pixels_read'] is False,'historical source unread flags not rewritten')
    need(len(protocol['whole_original_native_API_objects'])==4 and len(protocol['whole_original_two_scientific_custom_verdicts'])==2,'complete API and peer cardinality')
    transports=protocol['whole_original_eight_ordered_transport_objects']['whole_literal_object']
    need(isinstance(transports,list) and len(transports)==8,'all8 actual ordered transports')
    need([t['HTTP_status'] for t in transports]==ready['HTTP_status_sequence']==[200,301,200,200,200,200,200,200],'actual statuses including redirect')
    need(protocol['root_review']['whole_literal_text']==Path(protocol['root_review']['path']).read_text(),'whole actually read root review')
    for key in ['proof_companion','README_and_rights']:
        item=protocol['actual_source_manuscript_and_companion_read'][key]
        need(bound(item['path'],item).decode()==item['whole_literal_text'],'whole actual source/rights text')
    update=protocol['new_root_Stoimenow_finding_separate_from_immutable_peer_limits'];source_body=update['actual_existing_body_identity_hash_checked_by_editorial']
    bound(source_body['path'],source_body)
    need(source_body['bytes']==618917 and source_body['SHA256']=='86b9466b99f2cf67656b49311e67b97267c807d6c0f99d746a874c74379ca508','actual newly located existing2010 body identity')
    same(update['whole_original_root_qualification'],authority['additional_Stoimenow_root_vs_peer_qualification'])
    need(update['current_root_authenticates_exact_2010_definitions_theorem_and_context'] is True and
         update['root_new_all46page_or_predecessor_absence_certificate'] is False and
         update['private_primary_copied_into_editorial_or_public_assets'] is False,'exact root-primary update scope')
    pub=obj(root/'publication.json');promo=obj(root/'promotion.json');adapter=obj(root/'SCHEMA_ADAPTER.json')
    same(adapter['unique_publication_config'],pub);same(adapter['promotion_config'],promo)
    same(adapter['whole_actual_source_protocol'],protocol);same(adapter['source_binding_complete'],pub['source_binding']);same(adapter['review_metadata_complete'],pub['review_metadata'])
    same(pub['source_binding']['whole_original_source_ready'],ready)
    same(pub['source_binding']['whole_original_native_API_objects'],protocol['whole_original_native_API_objects'])
    same(pub['source_binding']['whole_original_eight_ordered_transport_objects'],protocol['whole_original_eight_ordered_transport_objects'])
    same(pub['review_metadata']['whole_original_two_scientific_custom_verdicts'],protocol['whole_original_two_scientific_custom_verdicts'])
    same(pub['review_metadata']['root_scientific_authority'],protocol['whole_root_scientific_authority'])
    same(pub['review_metadata']['new_root_primary_access_update_separate_from_immutable_peer_limits'],update)
    same(promo['whole_original_two_scientific_custom_verdicts'],protocol['whole_original_two_scientific_custom_verdicts'])
    same(promo['whole_source_binding'],pub['source_binding']);same(promo['new_root_primary_access_update_separate_from_immutable_peer_limits'],update)
    need(pub['printed_version'] is None and pub['printed_version_field_present'] is False and pub['version']=='1.0','no fabricated printed version')
    need(pub['publication_date']=='2026-10-12' and pub['native_record_created']==ready['created'] and pub['native_record_updated']==ready['updated'],'original date distinctions')
    need(pub['license']==pub['authored_package_license']=='CC BY 4.0' and pub['code_license'] is None,'broad actual rights, separate code instrument null')
    need(pub['canonical_url'] is None and pub['AA'] is None and pub['follow_up'] is None and promo['follow_up'] is None,'unassigned actual canonical/AA/followup')
    for key in ['production_integration_authorized','ready_to_publish','installed','deployed','live_verified','local_http_verified','browser_verified','native_verified','native_sheet_publication_verified','canonical_verified','public_page_published']:
        need(promo[key] is False,'private/public gate: '+key)
    need(promo['canonical_url'] is None and promo['AA'] is None,'promotion canonical/AA unassigned')
    need(pub['abstract']==protocol['actual_source_manuscript_and_companion_read']['entire_original_abstract_rendered_plain'],'entire original abstract')
    expected={'index.html','assets/citation.bib','assets/nullstellensatz.tex','assets/verification-package.zip','assets/nullstellensatz.pdf'}
    candidate=root/'candidate';need({p.relative_to(candidate).as_posix() for p in candidate.rglob('*') if p.is_file()}==expected,'complete5-file private candidate')
    need([a['original_api_file_object']['key'] for a in ready['all_native_assets_in_original_order']]==['nullstellensatz.tex','verification-package.zip','nullstellensatz.pdf'],'actual native TeX ZIP PDF order')
    for a in ready['all_native_assets_in_original_order']:
        raw=bound(a['path'],a);need(raw==bound(candidate/'assets'/a['original_api_file_object']['key'],a),'whole unchanged native candidate asset')
    need((candidate/'assets/nullstellensatz.tex').read_bytes()==Path(ready['controlling_TeX']['extracted_path']).read_bytes(),'native/control standalone TeX equality')
    need((root/'citation.bib').read_bytes()==(candidate/'assets/citation.bib').read_bytes()==pub['prepared_bibtex'].encode(),'complete citation bytes')
    need(ready['embedded_PDFs']==[] and ready['whole_regular_payload_occurrences']==15,'no invented embedded PDF, full15 payloads')
    manifest=obj(root/'MANIFEST.json');need(set(manifest['excluded_control_files'])==CONTROL,'manifest control exclusions')
    names=set()
    for row in manifest['files']:
        path=Path(row['path']);need(not path.is_absolute() and '..' not in path.parts and row['path'] not in names,'owned namespace safety')
        names.add(row['path']);bound(root/path,row)
    need({p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}-CONTROL==names,'complete owned inventory')
    need(not any(p.is_symlink() for p in root.rglob('*')),'no owned symlinks')
    if not payload_only:
        seal=obj(root/'SEAL.json');need(sha((root/'MANIFEST.json').read_bytes())==seal['MANIFEST_SHA256'],'final manifest seal')
        for row in seal['terminal_payload_receipts']:bound(root/row['path'],row)
        need(len(seal['terminal_payload_receipts'])==5,'terminal receipt count')
    return {'literal_custom_status':'PURE_PRIVATE_EDITORIAL_WHOLE_NATIVE_HISTORY_AND_COMPLETE_CUSTODY_CONFIRMED',
        'owned_payloads':len(names),'protected_original_paper_files':len(protected['files']),'closed_source_files':65,
        'whole_JSON_wrappers_checked':wrapper_count,'whole_native_API_objects':4,'whole_actual_transports':8,
        'whole_literal_scientific_verdicts':2,'original_candidate_native_assets':3,'candidate_files':5,
        'root_exact2010critical_authentication_retained':True,'old_peer_access_limits_unchanged':True,
        'new_root_all46page_or_absence_claim':False,'project_imports_programme_runs_subprocess_network_or_writes':False,
        'publication_authority':False}


if __name__=='__main__':
    need(sys.argv[1:] in [[],['--payload-only']],'unknown arguments')
    print(json.dumps(verify(Path(__file__).resolve().parent,bool(sys.argv[1:])),indent=2))
