#!/usr/bin/env python3
"""Read-only exact source/config/gate verification. No staging or network."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import zipfile

PAPER=Path(__file__).resolve().parents[2]
PROGRAM=PAPER.parents[1]
OUT=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def require(condition,message):
    if not condition:raise RuntimeError(message)

def verify():
    source=PAPER/'sources';pub=json.loads((PAPER/'publication.json').read_text());promo=json.loads((PAPER/'promotion.json').read_text())
    authority=PROGRAM/'verification/root-clearance-23387774-20261025.json'
    require(sha(authority)=='71c30130a7d421c601669d56bf8a20f3416f57be0fb7da6694fd54dd9dadc3a3','exact_root_authority')
    root=json.loads(authority.read_text());require(root['status']=='PASS' and root['record_id']=='23387774','cylinder_only_scientific_authority')
    require(promo['root_clearance_record']==root,'whole_original_clearance')
    require(promo['root_clearance_sha256']==sha(authority),'clearance_hash')
    require(promo['publication_sha256']==sha(PAPER/'publication.json'),'publication_hash')
    require((OUT/'publication.json').read_bytes()==(PAPER/'publication.json').read_bytes(),'canonical_publication_copy')
    require((OUT/'promotion.json').read_bytes()==(PAPER/'promotion.json').read_bytes(),'canonical_promotion_copy')
    receipt=json.loads((source/'receipt.json').read_text())
    require('exact_assets' in receipt and 'selected_PDF' in receipt and 'files' not in receipt,'literal_original_receipt_shape')
    require(len(receipt['exact_assets'])==2,'complete_two_asset_receipt')
    require(pub['source_binding']['source_receipt_original']==receipt==promo['source_receipt_original'],'whole_original_receipt')
    require((OUT/'source-receipt.original.json').read_bytes()==(source/'receipt.json').read_bytes(),'verbatim_original_receipt')
    require(sha(source/'receipt.json')==root['source_receipt_sha256'],'root_receipt_binding')
    raw=json.loads((source/'zenodo-record.raw.json').read_text())
    for asset in receipt['exact_assets']:
        obj=asset['file_object'];require(obj in raw['files'],'full_actual_API_file_object')
        f=source/obj['key'];require(f.stat().st_size==obj['size']==asset['bytes'],'API_asset_size')
        require(sha(f)==asset['sha256'],'asset_SHA256')
        require(hashlib.md5(f.read_bytes()).hexdigest()==asset['md5']==obj['checksum'].split(':',1)[1],'API_MD5')
    with zipfile.ZipFile(source/'cylinder_areas_verification.zip') as z:
        require(z.testzip() is None and len(z.infolist())==138,'full_original_ZIP_CRC')
        require(not any(a.filename.lower().endswith(('.pdf','.zip')) for a in z.infolist()),'no_embedded_PDF_or_nested_ZIP')
    for lane,b in root['reviews'].items():
        report=PROGRAM/b['report'];verdict=PROGRAM/b['verdict'];require(sha(report)==b['report_sha256'],'complete_report_binding')
        require(sha(verdict)==b['verdict_sha256'],'original_custom_verdict_binding')
        require(promo['reviews'][lane]['verdict']==json.loads(verdict.read_text()),'whole_custom_verdict_not_normalized')
    tex=(source/'published-source/cylinder_areas.tex').read_text();abstract=re.search(r'\\begin\{abstract\}([\s\S]*?)\\end\{abstract\}',tex).group(1)
    require((OUT/'ORIGINAL_ABSTRACT.tex').read_text()==abstract,'exact_original_abstract')
    rendered=' '.join(abstract.split()).replace('\\Poi','\\operatorname{Poisson}').replace('--','–')
    require(pub['abstract']==rendered,'complete_abstract_in_config')
    copy=(OUT/'PUBLIC_COPY.md').read_text();visible=copy.split('## Abstract\n\n',1)[1].split('\n\n## ',1)[0]
    require(visible==rendered and pub['public_copy_markdown']==copy,'complete_abstract_and_full_public_prose')
    require(not any(x in copy for x in ['SHA256','SOURCE_READY','ROOT_REVIEW','replay','7,100','46,233','PASS','early seal']),'no_internal_audit_narrative_in_public_copy')
    require(pub['version']=='1.0' and pub['publication_date']=='2026-10-15' and pub['doi']=='10.5281/zenodo.23387774','actual_selected_edition')
    require(pub['canonical_url']=='','canonical_URL_not_live_verified')
    for obj in [promo,pub['review_metadata']]:
        require(obj['AA'] is None and obj['follow_up'] is None,'AA_and_followup_null')
        for key in ['rendered_public_copy_approved','local_http_verified','live_http_verified','browser_verified','native_sheet_publication_verified','public_page_published']:
            require(obj[key] is False,'public_render_live_browser_native_gate_false:'+key)
    require(pub['AA'] is None and pub['follow_up'] is None,'public_config_AA_followup_null')
    preserved={}
    for rid in ['23387774','23074543']:
        p=PROGRAM/'papers'/rid;intake=p/'reviews/editorial-intake';seal=json.loads((intake/'SEAL.json').read_text())
        require(sha(intake/'MANIFEST.json')==seal['manifest_SHA256'],'historical_pending_intake_manifest')
        for b in json.loads((intake/'MANIFEST.json').read_text())['files']:
            require(sha(intake/b['path'])==b['SHA256'] and (intake/b['path']).stat().st_size==b['bytes'],'historical_intake_unchanged')
        baseline=json.loads((intake/'PRESERVATION_BASELINE.json').read_text())
        for b in baseline['files']:
            f=p/b['path'];require(sha(f)==b['SHA256'] and f.stat().st_size==b['bytes'],'all_preexisting_source_review_bindings_preserved')
        preserved[rid]={'intake_seal_SHA256':sha(intake/'SEAL.json'),'baseline_files_preserved':len(baseline['files'])}
    pending=PROGRAM/'papers/23074543';require(not (pending/'publication.json').exists() and not (pending/'promotion.json').exists(),'discotope_still_pending_no_configs')
    if (OUT/'FINAL_MANIFEST.json').exists():
        for b in json.loads((OUT/'FINAL_MANIFEST.json').read_text())['files']:
            require(sha(OUT/b['path'])==b['SHA256'],'final_handoff_binding')
    return {'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'COMPLETE_BINDING_AND_GATE_CHECKS','exact_root_authority_SHA256':sha(authority),'publication_SHA256':sha(PAPER/'publication.json'),'promotion_SHA256':sha(PAPER/'promotion.json'),'source_receipt_entire_original_shape_preserved':True,'original_custom_verdicts_preserved':True,'complete_original_abstract_preserved':True,'complete_original_archive_members':138,'all_public_render_live_browser_native_gates_false':True,'AA_and_followup_null':True,'earlier_intakes_sources_and_reviews_preserved':preserved,'site_shared_core_UI_Git_network_or_render_actions':False}

if __name__=='__main__':print(json.dumps(verify(),indent=2))
