#!/usr/bin/env python3
"""Local editorial consistency and custody checks, never a scientific/live pass."""
from pathlib import Path, PurePosixPath
import argparse
import datetime
import hashlib
import json
import re
import shutil
import subprocess
import zipfile

PAPER=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
ROOT=PAPER.parents[1]
ID=PAPER.name
pins={'23444606':'8f9acb77adf26af8699a42bfdc1f706e2c77978ae722083f8be50d63f8e89aa1','23440119':'8b51684b5e6cd6b36d8dd3302e2bbc5f29f261eb29affa753636812fb15cba56'}
parser=argparse.ArgumentParser()
parser.add_argument('--output-stem',required=True)
args=parser.parse_args()
assert re.fullmatch(r'[a-zA-Z0-9_-]+',args.output_stem)
dest=OUT/(args.output_stem+'.json')
custody_dest=OUT/(args.output_stem+'-custody-after.json')
assert not dest.exists() and not custody_dest.exists()
checks=[]
def check(ok,label):
    if not ok: raise RuntimeError(label)
    checks.append(label)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text())
def write(p,obj):
    with p.open('x') as f:f.write(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

pub=load(PAPER/'publication.json')
pro=load(PAPER/'promotion.json')
clearpath=ROOT/pro['root_clearance_file']
clear=load(clearpath)
receipt=load(PAPER/'sources/receipt.json')
record=load(PAPER/'sources/record.json')
binding=pub['source_binding']
sections=load(OUT/'public-sections.json')
adapter=load(OUT/'SCHEMA_ADAPTER.json')
copytext=(OUT/'PUBLIC_COPY.md').read_text()
check(sha(clearpath)==pins[ID]==pro['root_clearance_sha256'],'exact independently supplied root-clearance pin')
check(clear==pro['root_clearance_record'],'entire root clearance object preserved')
check(pro['status']==clear['status']=='PASS' and pro['disposition_by']==clear['disposition_by']=='root','top-level status comes only from later root authority')
check(pro['approved_scope']==clear['approved_scope'],'root-approved scope preserved exactly')
check(pro['scope_gate_resolution']==clear['scope_gate_resolution'],'later scope gate resolution separate and exact')
check(pro['source_receipt_record']==receipt and pro['source_files']==receipt['files'],'entire original receipt and every file entry preserved')
check(sha(PAPER/'sources/receipt.json')==pro['source_receipt_sha256']==clear['source_receipt_sha256']==binding['receipt_sha256'],'source receipt pin')
check(sha(PAPER/'sources/record.json')==pro['metadata_sha256']==binding['metadata_sha256']==binding['record_sha256'],'readable record independent pin')
check(sha(PAPER/'publication.json')==pro['publication_sha256'],'promotion binds exact final publication config')
check(binding['files']==receipt['files'],'publication preserves every full receipt file entry')
check(pub['title']==record['metadata']['title'],'exact published title')
check(pub['publication_date']==record['metadata']['publication_date']==clear['publication_date']=='2026-10-17','exact declared edition date')
check(pub['version']==record['metadata']['version']==clear['reviewed_zenodo_version']=='1.0.0','exact edition version')
check(binding['record_created_utc']==record['created']==clear['record_created_utc'],'creation timestamp stays distinct')
check(pub['doi']==record['doi'] and pub['author']=='Alec Kriebel','author and DOI identity')
check(pub['orcid']=='https://orcid.org/0009-0001-9320-500X','author ORCID')
check(pub['canonical_url']=='https://aleckriebel.com/research/'+pub['slug']+'/','final slug-derived canonical')
check(pub['canonical_url']==sections['canonical_url']==adapter['metadata_specification']['canonical_url'],'all proposed canonical references agree')
check(pub['follow_up'] is None and pro['follow_up'] is None and sections['follow_up'] is None,'no invented follow-up')
check(pro['preparation_state']==binding['publication_state']=='BINDINGS_READY_RENDERING_PENDING','editorial preparation remains pending rendering')
check(pro['rendered_copy_verified'] is False and pro['live_verified'] is False and pro['browser_verified'] is False and pro['native_sheet_aa_url'] is None,'no rendered/live/browser/native pass manufactured')
check(adapter['website_rendered'] is False and adapter['live_verified'] is False and adapter['native_tracker_modified'] is False,'adapter withholds later gates')
check(pro['source_repair'] is False and pro['human_peer_review'] is False and pro['formal_machine_verification'] is False,'no source repair or human/formal certification')
for role,item in clear['reviews'].items():
    current=pro['reviews'][role]
    check(sha(ROOT/item['report'])==item['report_sha256']==current['sha256'],role+' complete report hash')
    check(sha(ROOT/item['verdict'])==item['verdict_sha256']==current['verdict_sha256'],role+' complete verdict hash')
    check(load(ROOT/item['verdict'])==current['verdict'],role+' complete original custom object retained')
    check((PAPER/current['report']).resolve()==(ROOT/item['report']).resolve(),role+' report path preserved')
    check((PAPER/current['verdict_file']).resolve()==(ROOT/item['verdict']).resolve(),role+' verdict path preserved')
    check(current['root_disposition']==('SCOPE_COMPLETE' if role=='scope' else clear['status']),role+' separate root disposition')
if ID=='23444606':
    scope=pro['reviews']['scope']['verdict']
    check(scope['mathematical_pass'] is None and scope['root_publication_clearance'] is False and scope['candidate_only'] is True,'surreal original scope null/false history')
else:
    scope=pro['reviews']['scope']['verdict']
    check(scope['mathematical_verdict'] is None and scope['page_promotion_permission'] is False,'cone original scope null/false history')
    check(pro['reviews']['analytic']['verdict']['status']=='COMPLETE' and pro['reviews']['analytic']['verdict']['publication_clearance'] is False,'cone custom analytic COMPLETE and no clearance preserved')
    check(pro['reviews']['adversarial']['verdict']['status']=='COMPLETE' and pro['reviews']['adversarial']['verdict']['promotion_clearance'] is False,'cone custom adversarial COMPLETE and no clearance preserved')
candidate_path=PAPER/binding['frozen_scope_content_path']
candidate=load(candidate_path)
check(sha(candidate_path)==binding['frozen_scope_content_sha256'],'frozen candidate pin')
check(pub['abstract']==candidate['abstract'],'complete original candidate abstract retained')
texpath=PAPER/binding['source_tex_path']
check(sha(texpath)==clear['source_tex_sha256']==binding['source_tex_sha256'],'deposited TeX pin')
abstract_tex=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',texpath.read_text(),re.S).group(1).strip()
check(abstract_tex==binding['abstract_tex'],'complete original TeX abstract retained')
check(hashlib.sha256(abstract_tex.encode()).hexdigest()==binding['abstract_tex_sha256'],'original abstract TeX digest')
if ID=='23444606':
    check(re.sub(r'\s+',' ',abstract_tex)==pub['abstract'],'surreal abstract word-for-word whitespace-only normalization')
else:
    normalized=abstract_tex
    replacements={r"Tun\c{c}el's":'Tunçel’s',r'$K=\{(x,y,z)\geq0:xy^2\geq z^3\}$':'K = {(x,y,z) ≥ 0: xy² ≥ z³}',r'$F=-25\log\bigl(z(xy^2-z^3)\bigr)$':'F = −25 log(z(xy² − z³))',r'$100$':'100',r'$D^3F(a)[h,u,u]\leq0$':'D³F(a)[h,u,u] ≤ 0',r'$a\in\inter K$':'a ∈ int K',r'$h\in K$':'h ∈ K',r'$u\in\R^3$':'u ∈ ℝ³',r'$K$':'K',r'$\R^3$':'ℝ³',"Hildebrand's":'Hildebrand’s'}
    for old,new in replacements.items():normalized=normalized.replace(old,new)
    check(re.sub(r'\s+',' ',normalized)==pub['abstract'],'cone full abstract exact approved mathematical typography normalization')
check(pub['abstract_is_original'] is True and pub['abstract_heading']=='Original abstract','explicit original abstract heading')
check(pub['abstract'] in copytext and sections['sections'][0]['paragraphs']==[pub['abstract']],'full abstract retained in both public-copy representations')
for name,expected in [(pub['pdf_filename'],clear['pdf_sha256']),(pub['supplement_filename'],clear['supplement_sha256'])]:
    p=PAPER/'sources'/name
    check(sha(p)==expected,'exact source asset '+name)
    entry=next(x for x in receipt['files'] if x['name']==name)
    api=next(x for x in record['files'] if x['key']==name)
    check(p.stat().st_size==entry['bytes']==api['size'],'asset sizes '+name)
    check(hashlib.md5(p.read_bytes()).hexdigest()==entry['md5']==api['checksum'].split(':')[-1],'Zenodo checksum '+name)
    check(entry['sha256']==expected,'receipt asset SHA256 '+name)
pdf=PAPER/'sources'/pub['pdf_filename']
info=subprocess.run([shutil.which('pdfinfo'),str(pdf)],capture_output=True,text=True,check=True).stdout
check(int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))==pub['pdf_pages'],'actual PDF page count')
fresh=subprocess.run([shutil.which('pdftotext'),'-layout',str(pdf),'-'],capture_output=True,check=True).stdout
check(fresh==(OUT/'published-reader.txt').read_bytes(),'fresh actual PDF extraction equals read text')
check(len(fresh)>10000,'actual PDF has searchable mathematical text')
comparison=PAPER/('reviews/scope/paper.txt' if ID=='23444606' else 'reviews/scope/published_pdf.txt')
check(fresh==comparison.read_bytes(),'actual PDF text matches frozen scope reader')
archive=PAPER/'sources'/pub['supplement_filename']
extract=PAPER/('sources/published-source/initial-omnific-models-source-and-verification' if ID=='23444606' else 'sources/support')
archive_members=[]
embedded=[]
with zipfile.ZipFile(archive) as z:
    check(z.testzip() is None,'ZIP CRC integrity')
    names=[]
    for item in z.infolist():
        if item.is_dir():continue
        name=item.filename;parts=PurePosixPath(name).parts
        check(not name.startswith('/') and '..' not in parts and '\\' not in name,'safe ZIP path '+name)
        check(((item.external_attr>>16)&0o170000) in (0,0o100000),'regular ZIP member '+name)
        data=z.read(item)
        check((extract/name).read_bytes()==data,'original extracted member unchanged '+name)
        check(not name.lower().endswith(('.zip','.tar','.gz','.7z','.rar')),'no nested archive '+name)
        names.append(name)
        archive_members.append({'member':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
        if name.lower().endswith('.pdf'):
            embedded.append(name)
            check(data==pdf.read_bytes(),'embedded PDF byte-identical to main reader')
    check(len(names)==len(set(names))==binding['archive_regular_file_count'],'complete unique ZIP member inventory')
check(len(embedded)==1 and binding['unique_reader_pdf_count']==1,'one unique published PDF reader')
rootcustody=ROOT/clear['root_custody_receipt']
check(sha(rootcustody)==clear['root_custody_receipt_sha256'],'root custody receipt unchanged')
seal_bindings=[]
for sealentry in load(rootcustody)['seals']:
    sealpath=ROOT/sealentry['path'];seal=load(sealpath)
    check(sha(sealpath)==sealentry['sha256'],'frozen family seal '+str(sealpath.relative_to(ROOT)))
    entries=[]
    if ID=='23440119' and 'report_artifacts' in seal:
        entries += [(sealpath.parent/x['path'],x) for x in seal['report_artifacts']]
        entries += [(PAPER/x['path'],x) for x in seal['source_authorities']]
    else:
        items=seal['files']
        if isinstance(items,list):
            for x in items:
                path=Path(x['path'])
                entries.append((path if path.is_absolute() else sealpath.parent/path,x))
        else:
            for name,x in items.items():
                entries.append(((PAPER/name) if name.startswith('reviews/') else (sealpath.parent/name),x))
        if 'source_receipt' in seal:
            x=seal['source_receipt'];entries.append((Path(x['path']),x))
    check(len(entries)==sealentry['bindings'],'exact family-seal binding count')
    for path,x in entries:
        check(sha(path)==x['sha256'] and path.stat().st_size==x['bytes'],'existing sealed binding '+str(path.relative_to(ROOT)))
        seal_bindings.append({'path':str(path.relative_to(ROOT)),'sha256':x['sha256'],'bytes':x['bytes']})
check(len(seal_bindings)==clear['root_seal_bindings_rehashed'],'all root-listed final seal bindings freshly match')
before=load(OUT/'frozen-inputs-before.json')
after={}
for name,x in before['files'].items():
    path=ROOT/name
    actual={'bytes':path.stat().st_size,'sha256':sha(path)}
    check(actual==x,'frozen authority/source/review unchanged '+name)
    after[name]=actual
for entry in load(OUT/'READ_LEDGER.json')['read_files']:
    check(sha(Path(entry['path']))==entry['sha256'],'read-input identity '+entry['path'])
expected=adapter['expected_sections']
check([s['heading'] for s in sections['sections']]==expected,'all public sections in intended order')
for s in sections['sections']:
    check('## '+s['heading'] in copytext,'public-copy heading '+s['heading'])
    for paragraph in s.get('paragraphs',[]):check(paragraph in copytext,'full proposed paragraph '+s['id'])
    for reference in s.get('references',[]):
        check(reference['title'] in copytext and reference['url'] in copytext and reference['note'] in copytext,'credited reference '+reference['title'])
    for link in s.get('links',[]):check(link['url'] in copytext,'public asset/citation link '+link['label'])
    if s['id']=='paper':
        check(s['iframe']['src']==pub['pdf_filename']+'#view=FitH','iframe uses exact local source filename')
        check(any(x.get('download') is True and x['url']==pub['canonical_url']+pub['pdf_filename'] for x in s['links']),'explicit local PDF download specification')
    if s['id']=='materials':check(any(x.get('download') is True and x['url']==pub['canonical_url']+pub['supplement_filename'] for x in s['links']),'complete local ZIP download specification')
check((OUT/'citation.bib').read_text()==sections['bibtex'],'proposed BibTeX identical in section data')
check(sections['bibtex'].rstrip() in copytext,'full reusable BibTeX present in public draft')
for token in ['SHA-256','SHA256','ROOT_REVIEW','root clearance','quarantine','ENOSPC','verdict','2026-10-25','Sheet','replay','reviewer']:
    check(token.lower() not in copytext.lower(),'public copy excludes private narrative '+token)
check(re.search(r'\b[0-9a-f]{64}\b',copytext) is None,'no private hashes in public draft')
check('extensively' in pub['ai_disclosure'] and 'unrefereed' in pub['ai_disclosure'] and 'human or journal peer review' in pub['ai_disclosure'] and 'formal proof-assistant certification' in pub['ai_disclosure'],'complete AI/review disclosure')
check('actual research and writing contributions' in pub['collaboration'] and 'mutual agreement' in pub['collaboration'],'substantive contribution-based passive collaboration')
check(pub['additional_assets']==[],'no public source cache or extra reader assets')
check('Arial' in adapter['layout'] and 'white' in adapter['layout'] and 'single column' in adapter['layout'],'existing plain-blog layout specified')
for other in (ROOT/'papers').glob('*/publication.json'):
    if other==PAPER/'publication.json':continue
    otherpub=load(other)
    check(otherpub.get('canonical_url')!=pub['canonical_url'] and otherpub.get('slug')!=pub['slug'],'canonical uniqueness against '+other.parent.name)
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
write(custody_dest,{'record_id':ID,'utc':utc,'frozen_files':after,'all_frozen_bytes_unchanged':True,'archive_members_byte_compared':archive_members,'family_seal_bindings_rehashed':seal_bindings,'source_programs_executed':False})
write(dest,{'record_id':ID,'utc':utc,'status':'PASS_EDITORIAL_CONSISTENCY_ONLY','checks_passed':len(checks),'checks':checks,'source_programs_executed':False,'new_mathematical_review_claimed':False,'frozen_files_preserved':len(after),'archive_members_compared':len(archive_members),'family_seal_bindings_rehashed':len(seal_bindings),'publication_sha256':sha(PAPER/'publication.json'),'promotion_sha256':sha(PAPER/'promotion.json'),'custody_after':custody_dest.name,'custody_after_sha256':sha(custody_dest),'website_rendered':False,'live_verified':False,'browser_verified':False,'native_sheet_aa_url':None})
print(json.dumps({'record_id':ID,'checks_passed':len(checks),'frozen_files':len(after),'archive_members':len(archive_members),'family_seal_bindings':len(seal_bindings),'status':'PASS_EDITORIAL_CONSISTENCY_ONLY'}))
