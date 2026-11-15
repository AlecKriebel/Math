#!/usr/bin/env python3
"""Read-only, targeted editorial/source validator. No proof replay, network or writes.
Prints a JSON receipt. A caller may capture stdout to a new editorial artifact.
"""
import copy, hashlib, io, json, re, subprocess, zipfile
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone
E=Path(__file__).resolve().parent
P=E.parents[1]
ROOT=P.parents[1]
CLEAR=ROOT/'verification/root-clearance-23383952-20261114.json'
PIN='60f0f19bb3083fd5c5602694dcfedca96bc8597580c01783f0f11ed9a91d366a'
load=lambda x:json.loads(x.read_text())
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
checks=[]
def need(test,label):
    if not test:raise ValueError(label)
def ok(test,label):need(test,label);checks.append(label)
def norm(s):
    s=s.replace('\\(','').replace('\\)','').replace('--','–').replace("'",'’')
    return ' '.join(s.split())
C=load(CLEAR);R=load(P/'sources/SOURCE_READY.json');M=load(P/'sources/record.raw.json')
X=load(P/'publication.json');G=load(P/'promotion.json')
T=(P/'sources/published-source/note.tex').read_text()
A=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',T,re.S).group(1).strip()
expected='https://aleckriebel.com/research/'+X['slug']+'/'
def core(x,g):
    need(sha(CLEAR)==PIN,'root authority hash')
    need(g['whole_root_scientific_clearance_record']==C,'whole root authority preserved')
    need(g['scientific_status']==C['status']==x['review_metadata']['scientific_status'],'root exact custom status')
    need(x['source_binding']['whole_original_source_ready']==R==g['whole_original_source_ready'],'whole original READY preserved')
    need(x['source_binding']['whole_native_record']==M,'whole native record preserved')
    need(norm(x['abstract'])==norm(A),'complete original abstract')
    need(x['abstract_heading']=='Original abstract' and x['abstract_is_original'] is True,'original abstract label')
    need(x['title']==M['metadata']['title'] and x['doi']==M['doi'],'exact title DOI')
    need(x['version']==M['metadata']['version']=='1.0.0','literal version')
    need(x['publication_date']==M['metadata']['publication_date']=='2026-10-13','declared date')
    need(x['source_binding']['record_created_utc']==M['created']=='2026-10-15T04:00:37.039113+00:00','separate creation date')
    need(x['license']=='CC BY 4.0' and M['metadata']['license']['id']=='cc-by-4.0','license')
    need(x['canonical_url'] is None and g['canonical_url'] is None,'canonical withheld')
    need(x['proposed_canonical_url']==g['proposed_canonical_url']==expected,'proposed canonical consistency')
    need(x['follow_up'] is None and g['follow_up'] is None,'follow-up null')
    need(g['status']=='PRIVATE_EDITORIAL_PREPARED_UNPUBLISHED','no generic publishing PASS')
    for key in ['production_integration_authorized','publication_clearance','ready_to_publish','rendered_copy_verified','local_http_verified','live_verified','browser_verified','native_verified','canonical_verified']:
        need(g[key] is False,'unreleased gate '+key)
    for key in ['native_sheet_aa_url','AA']:need(g[key] is None,'blank native gate '+key)
    for key in ['rendered','deployed','publication_clearance','production_integration_authorized','browser_verified','native_verified','canonical_verified']:
        need(x['review_metadata'][key] is False,'publication metadata gate '+key)
    need(x['review_metadata']['canonical_url'] is None and x['review_metadata']['native_sheet_aa_url'] is None,'publication metadata nulls')
    for name,vn in [('scope','verdict.json'),('analytic','VERDICT.json'),('adversarial','VERDICT.json')]:
        report=P/f'reviews/{name}/REPORT.md';verdict=P/f'reviews/{name}/{vn}'
        original=load(verdict);entry=g['reviews'][name]
        need(entry['whole_original_custom_verdict']==original==C['reviews'][name]['whole_original_custom_verdict'],'whole custom verdict '+name)
        need(entry['root_clearance_review_object']==C['reviews'][name],'whole root family object '+name)
        need(entry['report_sha256']==sha(report)==C['reviews'][name]['report_sha256'],'report binding '+name)
        need(entry['verdict_sha256']==sha(verdict)==C['reviews'][name]['verdict_sha256'],'verdict binding '+name)
    need(x['source_binding']['all_assets_in_original_order']==R['all_assets_in_original_order'],'original asset order')
    native_files=[v['original_api_file_object'] for v in R['all_assets_in_original_order']]
    need(native_files==M['files'] and [v['key'] for v in native_files]==[x['pdf_filename'],x['supplement_filename']],'native PDF then ZIP order')
    need(x['pdf_pages']==4 and x['additional_assets']==[] and x['source_binding']['additional_unique_reader_pdfs']==[],'sole complete four-page reader')
    need('extensively' in x['ai_disclosure'] and 'unrefereed' in x['ai_disclosure'] and 'human or journal peer review' in x['ai_disclosure'] and 'no formal proof-assistant certification' in x['ai_disclosure'],'complete AI/status disclosure')
    need('actual research and writing contributions' in x['collaboration'] and 'mutual agreement' in x['collaboration'],'contribution-based collaboration')
    need('n ≥ 4' in ' '.join(x['limitations']) and 'Historical priority' in ' '.join(x['limitations']) and 'unestablished' in ' '.join(x['limitations']),'dimension/priority limits')
core(X,G);ok(True,'exact authority, full source/verdict semantics, abstract, metadata and withheld gates')
ok(G['publication_sha256']==sha(P/'publication.json'),'publication config binding')
ok(X['source_binding']['source_receipt_sha256']==G['source_receipt_sha256']==sha(P/'sources/api-receipts.json'),'native receipt hash')
receipts=load(P/'sources/api-receipts.json')
ok(X['source_binding']['whole_native_transport_receipts']==G['whole_original_native_transport_receipts']==receipts and len(receipts)==5,'entire native receipt list retained')
for receipt in receipts:
    body=receipt['body'];bp=Path(body['path'])
    need(bp.stat().st_size==body['bytes'] and sha(bp)==body['sha256'],'native body binding')
    need(isinstance(receipt['response_headers_in_received_order'],list),'ordered native headers')
ok(True,'all native transport body identities and ordered header shapes')
ok(load(P/'sources/versions.raw.json')['hits']['total']==1 and load(P/'sources/latest.raw.json')['id']==23383952,'selected native version identity')
for asset in R['all_assets_in_original_order']:
    f=Path(asset['path']);data=f.read_bytes()
    need(len(data)==asset['bytes'] and hashlib.sha256(data).hexdigest()==asset['sha256'] and hashlib.md5(data).hexdigest()==asset['md5'],'original asset bytes')
ok(True,'unchanged complete PDF and ZIP size/MD5/SHA256')
ok(sha(P/'sources/published-source/note.tex')==X['source_binding']['source_tex_sha256'] and len(T.splitlines())==317,'complete controlling source')
pdf=subprocess.run(['pdftotext','-layout',str(P/'sources'/X['pdf_filename']),'-'],capture_output=True,text=True,check=True).stdout
ok(len([s for s in pdf.split('\f') if s.strip()])==4 and 'Morpurgo' in pdf and 'References' in pdf,'searchable complete four-page PDF')
ok(sha(P/'sources/published-source/note.pdf')==X['source_binding']['pdf_sha256'],'embedded reader byte-identical to standalone')
# Replay custody only, never mathematics or archived audit conclusions.
archive=load(P/'sources/archive-members.json');cm={v['container']:v for v in archive['archive_containers']};mm={(v['container'],v['original_member_name']):v for v in archive['members']};seen=[];containers=[];expanded=0
rootname=X['supplement_filename']
def visit(data,label):
    global expanded
    c=cm[label];need(len(data)==c['bytes'] and hashlib.sha256(data).hexdigest()==c['sha256'],'container binding')
    containers.append(label)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names=z.namelist();need(len(names)==len(set(names)),'no duplicate archive names')
        for zi in z.infolist():
            need(not zi.is_dir() and not zi.filename.startswith('/') and '..' not in Path(zi.filename).parts,'safe regular archive member')
            member=z.read(zi);a=mm[(label,zi.filename)]
            need(len(member)==a['bytes'] and hashlib.sha256(member).hexdigest()==a['sha256'] and f'{zi.CRC:08x}'==a['CRC32'],'member CRC/body binding')
            need(Path(a['extracted_path']).read_bytes()==member,'existing extraction identity')
            seen.append((label,zi.filename));expanded+=len(member)
            if zipfile.is_zipfile(io.BytesIO(member)):visit(member,label+'::'+zi.filename)
visit((P/'sources'/rootname).read_bytes(),rootname)
ok(len(seen)==142 and len(containers)==4 and expanded==928042 and set(seen)==set(mm),'whole recursive ZIP custody, three nested archives and every payload')
protected=load(E/'PROTECTED_INPUTS.json')
for group in ['target_original_files','prior109_adversarial_packet_opaque_bindings']:
    for a in protected[group]:
        f=Path(a['path']);need(f.stat().st_size==a['bytes'] and sha(f)==a['sha256'],'protected original '+str(f))
ok(True,'all original target files and prior109 sealed packet unchanged')
public=(E/'PUBLIC_COPY.md').read_text();req=load(E/'PUBLICATION_REQUIREMENTS.json');adapter=load(E/'SCHEMA_ADAPTER.json');md=load(E/'SCHOLARLY_METADATA.json')
for heading in req['required_public_sections']:need('## '+heading+'\n' in public,'public section '+heading)
ok(X['abstract'] in public and all(s in public for key in ['plain_language','result','why_it_works','limitations'] for s in X[key]),'complete planned public prose retained')
ok(not re.search(r'2026-11-14|2026-10-25|SHA-?256|SOURCE_READY|ROOT_REVIEW|replay count|1043 bindings',public,re.I),'private audit dates/counts/hashes absent from public copy')
ok(all(v in public for v in ['1106714561/1700054750','321/500','positive finite times','L = 10000','t* = 4a','classical','unestablished','OpenAI tools were used extensively']),'full result and crucial public qualifications')
ok(Fraction(1106714561,1700054750)>Fraction(13,20)>Fraction(321,500),'transcribed strict threshold ordering')
ok(md['canonical_url'] is None and md['structured_data_template']['url'] is None and md['citation_metadata']['citation_pdf_url'] is None,'draft scholarly canonical fields withheld')
ok(md['structured_data_template']['abstract']==X['abstract'] and md['structured_data_template']['datePublished']==X['publication_date'] and md['structured_data_template']['version']==X['version'] and md['structured_data_template']['license']==X['license_url'],'scholarly metadata matches edition/full abstract/license')
ok(req['pdf']['download_attribute_required'] is True and req['support']['complete_original_zip_required'] is True and req['pdf']['embed_required'] is True,'complete reader/open/download and whole ZIP specifications')
ok(req['canonical_verified'] is False and adapter['canonical_url'] is None and adapter['native_sheet_aa_url'] is None,'adapter/requirements retain root gates')
bib=(E/'citation.bib').read_text();ok(all(s in bib for s in [X['doi'],'2026-10-13','1.0.0','Kriebel, Alec']),'citation edition consistency')
# In-memory rejection controls; no altered source/config is written.
rejected=[]
for label,mutate in [
 ('abridged abstract',lambda x,g:x.__setitem__('abstract',x['abstract'].split('.')[0]+'.')),
 ('false version',lambda x,g:x.__setitem__('version','1.0')),
 ('live canonical promoted',lambda x,g:x.__setitem__('canonical_url',expected)),
 ('native URL promoted',lambda x,g:g.__setitem__('native_sheet_aa_url',expected)),
 ('original verdict normalized',lambda x,g:g['reviews']['analytic']['whole_original_custom_verdict'].__setitem__('assessment','PASS')),
 ('publication authority promoted',lambda x,g:g.__setitem__('publication_clearance',True))]:
    x,g=copy.deepcopy(X),copy.deepcopy(G);mutate(x,g)
    try:core(x,g)
    except ValueError:rejected.append(label)
    else:raise ValueError('negative control escaped: '+label)
ok(len(rejected)==6,'six meaningful in-memory editorial/gate mutations rejected')
print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS_TARGETED_EDITORIAL_STATIC_VALIDATION','scope':'source/config/public-copy/custody consistency; no new proof, priority, render or live verification','checks':checks,'rejected_controls':rejected,'protected_target_originals':len(protected['target_original_files']),'protected_prior109_files':len(protected['prior109_adversarial_packet_opaque_bindings']),'archive_occurrences':len(seen),'archive_containers':len(containers),'publication_sha256':sha(P/'publication.json'),'promotion_sha256':sha(P/'promotion.json'),'source_programs_executed':False,'canonical_url':None,'publication_clearance':False,'browser_verified':False,'native_verified':False},indent=2))
