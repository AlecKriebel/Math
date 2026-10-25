#!/usr/bin/env python3
"""Read-only Discotope authority/source/config/preservation checks; no staging."""
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

def check_manifest(folder,manifest_name):
    m=json.loads((folder/manifest_name).read_text())
    for b in m['files']:
        f=folder/b['path'];expected=b.get('SHA256',b.get('sha256'))
        require(sha(f)==expected and f.stat().st_size==b['bytes'],'preserved_manifest_binding:'+str(f))
    return len(m['files'])

def check_false_gates(pub,promo,canonical_null=False):
    for obj in [promo,pub['review_metadata']]:
        require(obj['AA'] is None and obj['follow_up'] is None,'AA_followup_null')
        for key in ['rendered_public_copy_approved','local_http_verified','live_http_verified','browser_verified','native_sheet_publication_verified','public_page_published']:
            require(obj[key] is False,'public_render_live_browser_native_gate_false:'+key)
    require(pub['AA'] is None and pub['follow_up'] is None,'publication_AA_followup_null')
    if canonical_null:require(pub['canonical_url'] is None and promo['canonical_url'] is None,'canonical_URL_null')

def verify():
    s=PAPER/'sources';pub=json.loads((PAPER/'publication.json').read_text());promo=json.loads((PAPER/'promotion.json').read_text())
    authority=PROGRAM/'verification/root-clearance-23074543-20261025.json'
    require(sha(authority)=='4b826fb8e8e99805ebf23d0d8435846ed1983a90a738bb536c665cd3606a2fc5','exact_discotope_root_authority')
    root=json.loads(authority.read_text());require(root['status']=='PASS' and root['record_id']=='23074543','scientific_root_scope')
    require(promo['root_clearance_record']==root and promo['root_clearance_sha256']==sha(authority),'whole_original_root_clearance')
    for k in ['root_review','root_custody_receipt']:require(sha(PROGRAM/root[k])==root[k+'_sha256'],'root_final_evidence')
    require(promo['publication_sha256']==sha(PAPER/'publication.json'),'publication_hash')
    for name in ['publication.json','promotion.json']:
        require((OUT/name).read_bytes()==(PAPER/name).read_bytes(),'canonical_config_copy')
    receipt=json.loads((s/'receipt.json').read_text())
    require('actual_assets' in receipt and 'exact_assets' not in receipt and 'selected_PDF' not in receipt and 'files' not in receipt,'original_actual_assets_schema')
    require(len(receipt['actual_assets'])==2,'complete_original_asset_objects')
    require(pub['source_binding']['source_receipt_original']==receipt==promo['source_receipt_original'],'whole_original_receipt_not_normalized')
    require((OUT/'source-receipt.original.json').read_bytes()==(s/'receipt.json').read_bytes(),'verbatim_receipt_copy')
    require(sha(s/'receipt.json')==root['source_receipt_sha256'],'receipt_root_binding')
    require(sha(s/'metadata.normalized.json')==root['metadata_sha256'],'metadata_root_binding')
    raw=json.loads((s/'zenodo-record.raw.json').read_text())
    for asset in receipt['actual_assets']:
        obj=asset['file_object'];require(obj in raw['files'],'actual_complete_API_file_object')
        f=s/obj['key'];require(f.stat().st_size==obj['size']==asset['bytes'],'API_asset_size')
        require(sha(f)==asset['SHA256'],'actual_uppercase_SHA256')
        require(hashlib.md5(f.read_bytes()).hexdigest()==asset['MD5']==obj['checksum'].split(':',1)[1],'actual_uppercase_MD5')
    with zipfile.ZipFile(s/'source-and-verification.zip') as z:
        require(z.testzip() is None and len(z.infolist())==87,'whole_original_ZIP_CRC')
        require(sha(s/'published-source/paper.tex')==root['source_tex_sha256'],'controlling_current_TeX')
        require(z.read('paper.tex')==(s/'published-source/paper.tex').read_bytes(),'archived_current_TeX')
        old=z.read('verification/source_snapshot/proof.pdf')
        require(hashlib.sha256(old).hexdigest()=='e6e32c1612ea88360d887c1ea37b82d41a5463cad24c204ef023bfd32b49dc0f','historical_PDF_distinct_and_preserved')
        require(hashlib.sha256(old).hexdigest()!=sha(s/'paper.pdf'),'selected_reader_not_historical_PDF')
    for lane,b in root['reviews'].items():
        report=PROGRAM/b['report'];verdict=PROGRAM/b['verdict']
        require(sha(report)==b['report_sha256'] and sha(verdict)==b['verdict_sha256'],'complete_original_report_verdict_binding')
        require(promo['reviews'][lane]['verdict']==json.loads(verdict.read_text()),'whole_custom_verdict_original_shape')
    tex=(s/'published-source/paper.tex').read_text();abstract=re.search(r'\\begin\{abstract\}([\s\S]*?)\\end\{abstract\}',tex).group(1)
    require((OUT/'ORIGINAL_ABSTRACT.tex').read_text()==abstract,'exact_original_abstract')
    rendered=' '.join(abstract.split()).replace('\\Poi','\\operatorname{Poisson}').replace('--','–')
    require(pub['abstract']==rendered,'whole_abstract_in_config')
    copy=(OUT/'PUBLIC_COPY.md').read_text();visible=copy.split('## Abstract\n\n',1)[1].split('\n\n## ',1)[0]
    require(visible==rendered and pub['public_copy_markdown']==copy,'whole_abstract_and_full_public_prose')
    require(not any(x in copy for x in ['SHA256','SOURCE_READY','ROOT_REVIEW','replay','PASS','early seal']),'no_internal_audit_narrative_in_public_copy')
    require(pub['version']=='1.0' and pub['publication_date']=='2026-09-30' and pub['doi']=='10.5281/zenodo.23074543','exact_selected_edition')
    require(pub['source_binding']['record_created_utc']=='2026-10-01T04:23:09.001448+00:00','separate_API_creation_timestamp')
    check_false_gates(pub,promo,canonical_null=True)
    preserved={}
    for rid in ['23387774','23074543']:
        p=PROGRAM/'papers'/rid;intake=p/'reviews/editorial-intake';seal=json.loads((intake/'SEAL.json').read_text())
        require(sha(intake/'MANIFEST.json')==seal['manifest_SHA256'],'intake_manifest_seal')
        count=check_manifest(intake,'MANIFEST.json');baseline=json.loads((intake/'PRESERVATION_BASELINE.json').read_text())
        for b in baseline['files']:
            f=p/b['path'];require(sha(f)==b['SHA256'] and f.stat().st_size==b['bytes'],'all_preexisting_source_review_bytes_preserved')
        preserved[rid]={'intake_seal_SHA256':sha(intake/'SEAL.json'),'intake_bindings_preserved':count,'source_review_baseline_files_preserved':len(baseline['files'])}
    cylinder=PROGRAM/'papers/23387774';cyled=cylinder/'reviews/editorial';cylseal=json.loads((cyled/'FINAL_SEAL.json').read_text())
    require(sha(cyled/'FINAL_SEAL.json')=='25f94cf91866cbcfd465a7bf00492180a75a862849ef78c640b7ed610e4319a0','original_cylinder_final_seal')
    require(sha(cyled/'FINAL_MANIFEST.json')==cylseal['manifest_SHA256'],'cylinder_final_manifest_seal')
    preserved['cylinder_final_editorial_bindings']=check_manifest(cyled,'FINAL_MANIFEST.json')
    cylm=json.loads((cyled/'FINAL_MANIFEST.json').read_text())
    for b in cylm['canonical_configs']:require(sha(PROGRAM/b['path'])==b['SHA256'],'original_cylinder_canonical_configs')
    check_false_gates(json.loads((cylinder/'publication.json').read_text()),json.loads((cylinder/'promotion.json').read_text()))
    transition=json.loads((OUT/'CROSS_PACKET_GATE_TRANSITION.json').read_text())
    require(transition['historical_cylinder_verifier_SHA256']==sha(cyled/'verify_handoff.py'),'historical_cylinder_checker_not_edited')
    require(transition['historical_cylinder_validation_receipt_SHA256']==sha(cyled/'VALIDATION_RECEIPT.json'),'historical_cylinder_passing_receipt_not_edited')
    previous=PROGRAM/'papers/23181280';prev=previous/'reviews/analytic'
    require(sha(prev/'FINAL_SEAL.json')=='e814f10301234a6fbc54b5e3fb7d32b49b11954639bcf9c0850d3687c5bb0b88','earlier_complexity_analytic_packet_seal')
    preserved['earlier_complexity_analytic_bindings']=check_manifest(prev,'FINAL_MANIFEST.json')
    preserved['earlier_complexity_source_bindings']=check_manifest(previous/'sources','SOURCE_READY_MANIFEST.json')
    if (OUT/'FINAL_MANIFEST.json').exists():check_manifest(OUT,'FINAL_MANIFEST.json')
    return {'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'COMPLETE_DISCOTOPE_BINDING_AND_GATE_CHECKS','exact_root_authority_SHA256':sha(authority),'publication_SHA256':sha(PAPER/'publication.json'),'promotion_SHA256':sha(PAPER/'promotion.json'),'whole_actual_assets_receipt_and_custom_verdicts_preserved':True,'complete_original_abstract_preserved':True,'original_archive_members_CRC_checked':87,'selected_reader':'current four-page paper.pdf; historical five-page proof.pdf remains separate','all_public_render_live_browser_native_gates_false':True,'canonical_URL_null':True,'AA_followup_null':True,'preservation':preserved,'historical_cylinder_pending_target_guard_rerun':False,'new_transition_separately_authorized':True,'network_stage_render_shared_site_UI_Git_or_outreach_actions':False}

if __name__=='__main__':print(json.dumps(verify(),indent=2))
