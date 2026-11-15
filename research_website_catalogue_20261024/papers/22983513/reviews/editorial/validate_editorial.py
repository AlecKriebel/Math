#!/usr/bin/env python3
"""Pure offline editorial validation/custody; no scientific replay or file writes."""
from pathlib import Path
import json,hashlib,re,copy,argparse

ROOT=Path(__file__).resolve().parent
PAPER=ROOT.parent.parent
P=PAPER.parent.parent
SOURCE=PAPER/'sources'
A=SOURCE/'attempts/20261115T032014Z'
COUNT=0
GATES=['rendered','deployed','rendered_public_copy_approved','local_http_verified','live_http_verified','browser_verified','native_sheet_publication_verified','public_page_published','root_editorial_clearance_received','production_integration_authorized','publication_clearance','ready_to_publish','canonical_verified']


def need(x,m):
    global COUNT
    COUNT+=1
    if not x:raise RuntimeError(m)


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p):return json.loads(p.read_bytes())


def literal(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return list(a)==list(b) and all(literal(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(literal(x,y) for x,y in zip(a,b))
    return a==b


def config_checks(pub,prom,env):
    definition,ready,authority,abstract=env
    for key,value in definition.items():need(literal(pub[key],value),'Copy/edition/scope field differs: '+key)
    need(pub['abstract']==abstract and pub['abstract_is_original'] is True and pub['abstract_heading']=='Original abstract','Full original abstract lost')
    need(pub['pdf_pages']==3 and pub['pdf_filename']=='paper.pdf' and pub['supplement_filename']=='source-and-verification.zip','Complete reader/source identity')
    need(pub['canonical_url'] is None and pub['AA'] is None and pub['follow_up'] is None,'Premature actual canonical/AA/follow-up')
    sb=pub['source_binding']
    need(literal(sb['whole_original_source_ready'],ready),'Whole original source-ready changed')
    native_files={'whole_native_record':'record.attempt-001.raw','whole_native_latest_record':'latest.raw.json','whole_native_versions':'versions.page-001.attempt-002.raw.json','whole_native_failed_versions_response':'versions.page-001.raw.json','whole_native_files_endpoint':'files.raw.json','whole_native_acquisition_transport_receipt':'ALL_TRANSPORT_RECEIPTS.json','whole_native_record_transport_receipt':'record.attempt-001.transport.json'}
    for key,name in native_files.items():need(literal(sb[key],load(A/name)),'Original native schema/value/order changed: '+key)
    need(literal(sb['all_native_assets_in_original_order'],ready['all_assets_in_original_order']),'Original asset order/body changed')
    need(sb['manuscript_date']=='23 September 2026' and sb['version']==sb['manuscript_version']=='1.0.1','Exact printed edition')
    need(sb['record_created_utc']==ready['created'] and sb['record_updated_utc']==ready['updated'] and pub['publication_date']==ready['publication_date']=='2026-09-23','Distinct chronology substituted')
    need(pub['license']=='CC BY 4.0' and pub['code_license']=='MIT' and sb['original_CFF_DOI_placeholder_preserved'] is True,'Mixed rights/history lost')
    need(pub['review_metadata']['scientific_status']==authority['status'] and pub['review_metadata']['editorial_review_is_informed_not_fresh_blind_science'] is True,'Exact scientific authority/informed role')
    need(prom['scientific_status']==authority['status'] and literal(prom['whole_root_scientific_clearance_record'],authority),'Whole root authority changed')
    need(literal(prom['whole_original_source_ready'],ready) and literal(prom['whole_native_acquisition_transport_receipt'],load(A/'ALL_TRANSPORT_RECEIPTS.json')),'Promotion native objects changed')
    for entry in authority['independent_review_packets']:
        lane=entry['lane'];r=prom['reviews'][lane]
        need(literal(r['root_authority_entry'],entry) and literal(r['whole_original_custom_verdict'],entry['whole_literal_custom_verdict']),'Custom verdict/root entry normalized: '+lane)
        need(literal(r['whole_original_custom_verdict'],load(Path(r['verdict_path']))),'Original custom verdict differs: '+lane)
    for key in GATES:need(prom[key] is False,'Premature publication gate: '+key)
    for key in ['canonical_url','AA','native_sheet_aa_url','follow_up']:need(prom[key] is None,'Premature actual URL/follow-up: '+key)
    need(prom['source_repair'] is False and prom['narrowed_replacement'] is False and prom['human_peer_review'] is False and prom['formal_certification'] is False,'Unsupported scientific/review claim')
    need(prom['status']=='PRIVATE_EDITORIAL_PREPARED_UNPUBLISHED' and prom['editorial_review_is_informed_not_fresh_blind_science'] is True,'Editorial state/role mismatch')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--sealed',action='store_true');args=ap.parse_args()
    ready=load(SOURCE/'SOURCE_READY.json');authority=load(P/'verification/root-clearance-22983513-20261115.json')
    need(sha(SOURCE/'SOURCE_READY.json')=='9ab3aa2364dbc078c0cae228e9a627b75586a6da5f9a1a4c2111391c5bd5ca20','Wrong actual readiness')
    need(sha(P/'verification/root-clearance-22983513-20261115.json')=='048205b0aa267298ac034afa9fdf2c88973c05e68e6d0278e4accfcac2c0da57','Wrong root authority')
    definition=load(ROOT/'COPY_DEFINITION.json');tex_path=Path(ready['controlling_TeX']['extracted_path']);text=tex_path.read_text();raw=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',text,re.S).group(1);abstract=' '.join(raw.replace('--','–').replace("Yang's",'Yang’s').split());need((ROOT/'ORIGINAL_ABSTRACT.tex').read_text()==raw,'Original abstract substring changed')
    pub=load(PAPER/'publication.json');prom=load(PAPER/'promotion.json');env=(definition,ready,authority,abstract);config_checks(pub,prom,env)
    need(prom['publication_sha256']==sha(PAPER/'publication.json'),'Promotion publication binding')
    for name in ['publication.json','promotion.json']:need((ROOT/'prepared-configs'/name).read_bytes()==(PAPER/name).read_bytes(),'Prepared config copy differs')
    for r in load(ROOT/'PROTECTED_INPUTS.json')['files']:
        q=Path(r['path']);need(q.is_file() and q.stat().st_size==r['bytes'] and sha(q)==r['sha256'],'Protected original changed: '+str(q))
    for r in load(ROOT/'ORIGINAL_OBJECT_COPIES.json'):
        q=ROOT/r['private_copy_path'];original=Path(r['original_path']);need(q.read_bytes()==original.read_bytes() and q.stat().st_size==r['bytes'] and sha(q)==r['sha256'],'Raw original-object copy differs')
    for r in load(ROOT/'PREPARED_ASSETS.json'):
        q=ROOT/r['prepared_copy'];original=Path(r['source']);need(q.read_bytes()==original.read_bytes() and q.stat().st_size==r['bytes'] and sha(q)==r['sha256'],'Prepared complete asset differs')
    need((ROOT/'prepared-assets/paper.pdf').read_bytes()==Path(ready['selected_actual_PDF']['path']).read_bytes() and ready['selected_actual_PDF']['pages']==3,'Complete actual three-page reader identity')
    bib=(ROOT/'CITATION.bib').read_text();need(pub['prepared_bibtex']==bib and (ROOT/'prepared-assets/citation.bib').read_text()==bib,'Exact prepared BibTeX')
    for term in ['10.5281/zenodo.22983513','version = {1.0.1}','day = {23}','26 September 2026','10 October 2026']:need(term in bib,'BibTeX edition/DOI note lost')
    public=load(ROOT/'public-sections.json');md=(ROOT/'PUBLIC_COPY.md').read_text();need(public['abstract']['text']==abstract and md.count(abstract)==1,'Complete original abstract not unique in public copy')
    paragraphs=[]
    for key in ['plain_language','result','why_it_works','limitations']:paragraphs+=pub[key]
    paragraphs += [pub[k] for k in ['edition_note','rights_note','ai_disclosure','collaboration']]
    need([x for s in public['sections'] for x in s['paragraphs']]==paragraphs,'Public section/config body divergence')
    for para in paragraphs:need(md.count(para)==1,'Full public paragraph absent/duplicated')
    for b in pub['background']:
        need(b['title'] in md and b['url'] in md and b['note'] in md,'Classical/background credit lost')
    need(public['follow_up'] is None and '## Follow' not in md and '## Further' not in md,'Unapproved follow-up section')
    scholarly=load(ROOT/'SCHOLARLY_METADATA.json');need(scholarly['private_template_not_published_JSONLD'] is True and scholarly['canonical_url'] is None and scholarly['citation_pdf_url'] is None,'Unfinalized scholarly URLs')
    j=scholarly['jsonld'];need(j['abstract']==abstract and j['headline']==pub['title'] and j['datePublished']==pub['publication_date'] and j['version']==pub['version'] and j['url'] is None and j['encoding'][0]['contentUrl'] is None,'Scholarly title/edition/full abstract/template')
    need(scholarly['open_graph']['url'] is None and scholarly['open_graph']['proposed_url']==pub['proposed_canonical_url'],'Planned/actual OG distinction')
    req=load(ROOT/'PUBLICATION_REQUIREMENTS.json');r=req['reader'];need(req['private_only'] is True and r['iframe_count']==1 and r['complete_page_count']==3 and r['iframe_src']==r['direct_open']=='paper.pdf','Exactly one complete accessible reader contract')
    for key,filename in [('local_PDF_download','paper.pdf'),('local_ZIP_download','source-and-verification.zip'),('original_checksums_download','SHA256SUMS.txt'),('citation_download','citation.bib')]:need(r[key]=={'href':filename,'download_attribute':filename},'Actual future download control contract')
    need(req['presentation']['Research_navigation']=='/research/' and req['presentation']['stylesheet']=='/research/research.css' and req['legacy_page_candidate']['redirect_authority'] is False,'Design/navigation/redirect boundary')
    # Eight bounded semantic faults remain entirely in memory; pristine files unchanged.
    bad=[]
    x=copy.deepcopy(pub);x['abstract']=x['abstract'].rsplit(' ',1)[0];bad.append(('truncated_original_abstract',x,prom))
    x=copy.deepcopy(pub);x['publication_date']='2026-09-26';bad.append(('creation_date_substitution',x,prom))
    x=copy.deepcopy(pub);x['result'][1]=x['result'][1].replace('M₂²','M₂');bad.append(('missing_second_moment_square',x,prom))
    x=copy.deepcopy(pub);x['source_binding']['whole_native_files_endpoint']['default_preview']={};bad.append(('native_null_to_empty_object',x,prom))
    y=copy.deepcopy(prom);y['reviews']['scope']['whole_original_custom_verdict']={'status':'PASS'};bad.append(('generic_custom_verdict_substitution',pub,y))
    y=copy.deepcopy(prom);y['ready_to_publish']=True;bad.append(('premature_publication_gate',pub,y))
    x=copy.deepcopy(pub);x['canonical_url']=x['proposed_canonical_url'];bad.append(('premature_actual_canonical',x,prom))
    x=copy.deepcopy(pub);x['source_binding']['whole_native_acquisition_transport_receipt']=[r for r in x['source_binding']['whole_native_acquisition_transport_receipt'] if r['HTTP_status']==200];bad.append(('failed_transport_erased',x,prom))
    rejected=[]
    for name,x,y in bad:
        try:config_checks(x,y,env)
        except RuntimeError:rejected.append(name)
        else:raise RuntimeError('Targeted semantic fault escaped: '+name)
    if args.sealed:
        mb=(ROOT/'MANIFEST.json').read_bytes();m=json.loads(mb);seal=load(ROOT/'SEAL.json');need(seal['manifest_sha256']==hashlib.sha256(mb).hexdigest(),'Final manifest seal mismatch')
        actual=set()
        for q in ROOT.rglob('*'):
            need(not q.is_symlink(),'Unexpected owned symlink')
            if q.is_file():actual.add(q.relative_to(ROOT).as_posix())
        names=[z['path'] for z in m['files']];need(len(names)==len(set(names)) and set(names)==actual-{'MANIFEST.json','SEAL.json'},'Owned final inventory')
        for z in m['files']:
            q=ROOT/z['path'];need(q.resolve().is_relative_to(ROOT) and q.stat().st_size==z['bytes'] and sha(q)==z['sha256'],'Final owned byte binding')
        need(seal['publication_sha256']==sha(PAPER/'publication.json') and seal['promotion_sha256']==sha(PAPER/'promotion.json'),'Final external configs binding')
    print(json.dumps({'status':'PRIVATE_EDITORIAL_CLOSURE_PASS','record_id':22983513,'checks':COUNT,'protected_original_files':len(load(ROOT/'PROTECTED_INPUTS.json')['files']),'byte_identical_original_object_copies':len(load(ROOT/'ORIGINAL_OBJECT_COPIES.json')),'targeted_semantic_faults_rejected':rejected,'publication_gates_closed':True,'canonical_and_AA_null':True,'source_scientific_or_old_campaign_replays':0,'network':0,'writes':0,'sealed':args.sealed},sort_keys=True))


if __name__=='__main__':main()
