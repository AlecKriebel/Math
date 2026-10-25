"""Read-only checks; writes fresh editorial result paths supplied as one stem."""
from pathlib import Path, PurePosixPath
import datetime
import hashlib
import json
import re
import sys
import unicodedata
import zipfile
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[4]
PAPER = ROOT / 'papers/23383961'
OUT = PAPER / 'reviews/editorial'
stem = sys.argv[1]
assert re.fullmatch(r'[a-z0-9-]+', stem)
result_path = OUT / (stem + '.json')
custody_path = OUT / (stem + '-source-custody-after.json')
assert not result_path.exists() and not custody_path.exists()
checks = []

def check(name, condition, detail=None):
    checks.append({'name': name, 'pass': bool(condition), **({'detail': detail} if detail is not None else {})})
    if not condition:
        raise AssertionError(name)

def load(p):
    return json.loads(p.read_text())

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

pub = load(PAPER / 'publication.json')
gate = load(PAPER / 'promotion.json')
record = load(PAPER / 'sources/record.json')
receipt = load(PAPER / 'sources/receipt.json')
candidate = load(PAPER / 'reviews/scope/candidate.json')
clearpath = ROOT / gate['root_clearance_file']
clear = load(clearpath)
check('exact_root_clearance_authority', sha(clearpath) == gate['root_clearance_sha256'] == '2a9214e52b408d2a67a4aef4d6887b8cf86f8eb46f99423ad977c4a8cf847122')
check('root_clearance_record_preserved', gate['root_clearance_record'] == clear)
check('root_pass_not_live_pass', gate['status'] == clear['status'] == 'PASS' and gate['disposition_by'] == 'root' and not gate['rendered_copy_verified'] and not gate['live_verified'] and gate['native_sheet_aa_url'] is None)
check('approved_scope_exact', gate['approved_scope'] == clear['approved_scope'])
check('publication_binding', sha(PAPER/'publication.json') == gate['publication_sha256'])
check('source_metadata_binding', sha(PAPER/'sources/record.json') == gate['metadata_sha256'] == receipt['record_sha256'] == pub['source_binding']['metadata_sha256'])
check('source_receipt_binding', sha(PAPER/'sources/receipt.json') == clear['source_receipt_sha256'] == gate['source_receipt_sha256'] == pub['source_binding']['receipt_sha256'])
check('scholarly_identity', record['status']=='published' and str(record['id'])==gate['record_id']=='23383961' and pub['title']==record['metadata']['title'] and pub['doi']==record['doi']=='10.5281/zenodo.23383961' and pub['version']==record['metadata']['version']=='1.0')
check('author_orcid', pub['author']=='Alec Kriebel' and pub['orcid']=='https://orcid.org/0009-0001-9320-500X' and record['metadata']['creators'][0]['orcid']=='0009-0001-9320-500X')
check('date_without_priority_claim', pub['publication_date']==record['metadata']['publication_date']=='2026-10-14' and record['created']=='2026-10-15T04:00:29.066300+00:00' and pub['source_binding']['record_created_utc']==record['created'] and 'historical priority' in pub['edition_note'])
check('canonical_from_final_slug', re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',pub['slug']) and pub['canonical_url']=='https://aleckriebel.com/research/'+pub['slug']+'/')
check('no_followup', pub['follow_up'] is None and gate['follow_up'] is None and clear['follow_up'] is None and candidate['followup'] is None)
check('complete_original_abstract', pub['abstract']==candidate['original_abstract'] and pub['abstract_heading']=='Original abstract' and pub['abstract_is_original'] is True)
texpath = PAPER/pub['source_binding']['source_tex_path']
tex = texpath.read_text()
raw_abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1).strip()
check('full_original_tex_abstract_bound', pub['source_binding']['abstract_tex']==raw_abstract and hashlib.sha256(raw_abstract.encode()).hexdigest()==pub['source_binding']['abstract_tex_sha256'] and sha(texpath)==pub['source_binding']['source_tex_sha256']=='c4e557a58999b938578eb105c03d7224f087c04f273dbbd86e09ab45b855a4b3')
plain = raw_abstract.replace(r'\(a_2+i10^{-24}(a_4-3a_3)\)','a₂+i10⁻²⁴(a₄−3a₃)').replace('~',' ').replace('--','–')
plain = ' '.join(plain.split())
check('source_normalization_exact',plain==pub['abstract'])
pdftext=(OUT/'published-reader.txt').read_text()
pdf_abstract=pdftext.split('Abstract',1)[1].split('1    The question and precise statement',1)[0]
def words(s):
    s=unicodedata.normalize('NFKC',s).replace('support-\n     point','support-point')
    s=re.sub(r'real part of .*? in\s+the normalized','real part of [FORMULA] in the normalized',s,flags=re.S)
    return re.findall(r'[A-Za-z]+|\d+',s)
check('published_pdf_full_abstract_words',words(pdf_abstract)==words(pub['abstract']))
reader=PdfReader(PAPER/'sources/support_slit.pdf')
check('five_page_searchable_reader',len(reader.pages)==pub['pdf_pages']==5 and all(len(p.extract_text())>500 for p in reader.pages))
asset_results=[]
for asset in receipt['files']:
    p=PAPER/'sources'/asset['name']
    asset_results.append({'name':asset['name'],'sha256':sha(p),'bytes':p.stat().st_size})
    check('asset_'+asset['name'],sha(p)==asset['sha256'] and p.stat().st_size==asset['bytes'] and hashlib.md5(p.read_bytes()).hexdigest()==asset['md5'])
check('exact_published_asset_set',set(x['name'] for x in receipt['files'])=={pub['pdf_filename'],pub['supplement_filename']} and len(pub['additional_assets'])==0)
check('fixed_pdf_and_support_hashes',gate['pdf_sha256']==clear['pdf_sha256']=='a6d227d606fda3e68adc6db4eab462ee3f12b0544a201121b5c3a21aa5099e3d' and gate['supplement_sha256']==clear['supplement_sha256']=='58853fd56272184efe8232c58c356b1a669ba43032e3c4f35e4b17e317898f51')
member_count=hidden=embedded=nested=0
with zipfile.ZipFile(PAPER/'sources/verification_package.zip') as z:
    check('zip_crc',z.testzip() is None)
    for info in z.infolist():
        if info.is_dir():
            continue
        name=PurePosixPath(info.filename)
        check('safe_member_'+info.filename,not name.is_absolute() and '..' not in name.parts)
        data=z.read(info)
        extracted=PAPER/'sources/published-source/verification_package'/info.filename
        check('identical_member_'+info.filename,extracted.is_file() and extracted.read_bytes()==data)
        member_count+=1
        hidden+=any(p.startswith('.') for p in name.parts)
        embedded+=data.startswith(b'%PDF-')
        nested+=data.startswith((b'PK\x03\x04',b'\x1f\x8b'))
check('archive_shape',member_count==255 and hidden==12 and embedded==nested==0,{'members':member_count,'hidden':hidden,'embedded_pdf':embedded,'nested_archive':nested})
source_before=load(OUT/'source-custody-before.json')['files']
source_after={str(p.relative_to(PAPER/'sources')):sha(p) for p in sorted((PAPER/'sources').rglob('*')) if p.is_file()}
baseline=load(PAPER/'reviews/scope/source-baseline.json')['files_sha256']
check('all_259_source_files_unchanged',source_before==source_after==baseline and len(source_after)==259)
custody_path.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':source_after,'count':len(source_after),'unchanged_from_editorial_start_and_frozen_scope_baseline':True},indent=2)+'\n')
review_results=[]
for role,obj in gate['reviews'].items():
    verdictpath=PAPER/obj['verdict_file']
    check(role+'_complete_report_and_exact_verdict',sha(PAPER/obj['report'])==obj['sha256']==clear['reviews'][role]['report_sha256'] and sha(verdictpath)==obj['verdict_sha256']==clear['reviews'][role]['verdict_sha256'] and obj['verdict']==load(verdictpath))
    review_results.append({'role':role,'report_sha256':obj['sha256'],'verdict_sha256':obj['verdict_sha256'],'root_disposition':obj['root_disposition']})
scope=gate['reviews']['scope']['verdict']
check('original_scope_custom_pending_null_false_preserved',scope['status']=='SCOPE_COMPLETE_PENDING_INDEPENDENT_MATHEMATICAL_REVIEW' and scope['mathematical_pass'] is False and scope['scientific_verdict'] is None and scope['defect_found'] is None and scope['ready_to_publish'] is False and gate['reviews']['scope']['root_disposition']=='SCOPE_COMPLETE')
check('original_candidate_gate_preserved',candidate['mathematical_pass'] is False and candidate['ready_to_publish'] is False and candidate['canonical_url'] is None)
seal_results=[]
for item in clear['root_review_seals_rehashed']:
    path=ROOT/item['path']
    check('frozen_seal_hash_'+path.parent.name,sha(path)==item['sha256'])
    seal=load(path)
    for f in seal['files']:
        check('frozen_review_binding_'+path.parent.name+'/'+f['path'],sha(path.parent/f['path'])==f['sha256'])
    check('seal_binding_count_'+path.parent.name,len(seal['files'])==item['bindings_checked'])
    seal_results.append({'path':item['path'],'sha256':sha(path),'bindings_checked':len(seal['files'])})
check('root_custody_receipt_unchanged',sha(ROOT/clear['root_custody_receipt'])==clear['root_custody_receipt_sha256'])
public={k:pub[k] for k in ['title','description','abstract','plain_language','result','why_it_works','limitations','background','collaboration','status','ai_disclosure','edition_note','bibtex_note']}
public_text=json.dumps(public,ensure_ascii=False)
check('no_private_review_implementation_in_public_copy',not re.search(r'[a-f0-9]{64}|2026-10-25|root.clearance|source.custody|quarantine|replay|PASS_SCIENTIFIC|Decimal|195 probes|192 finite',public_text,re.I))
check('explicit_every_actual_fixed_scope',all(s in ' '.join(pub['result']) for s in ['Every such maximizer','actual analytic slit','ε = 10⁻²⁴','signed outward radial angle','ordinary unsigned outward radial angle']))
check('signed_limit_and_unsigned_zero_present',all(s in ' '.join(pub['why_it_works']) for s in ['tends to zero at infinity','interior zero','ordinary angle |β|']))
check('authorship_actual_and_mutual',all(s in pub['collaboration'] for s in ['mutual agreement','actual research and writing contributions']))
check('unrefereed_ai_no_human_or_formal_claim',all(s in pub['ai_disclosure'] for s in ['extensively','unrefereed','human or journal peer review','without formal proof-assistant certification']))
check('no_new_scientific_or_live_clearance',not pub['review_metadata']['rendered'] and not pub['review_metadata']['deployed'] and gate['preparation_state']=='BINDINGS_READY_RENDERING_PENDING')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'record_id':'23383961','status':'PASS_EDITORIAL_BINDINGS_ONLY','completion_percent_for_assigned_editorial_preparation':100,'checks_passed':len(checks),'checks':checks,'assets':asset_results,'reviews':review_results,'review_seals':seal_results,'source_files_unchanged':len(source_after),'archive':{'members':member_count,'hidden_members':hidden,'embedded_readers':embedded,'nested_archives':nested},'publication_sha256':sha(PAPER/'publication.json'),'promotion_sha256':sha(PAPER/'promotion.json'),'root_clearance_sha256':sha(clearpath),'website_rendered':False,'live_verified':False,'browser_verified':False,'native_sheet_modified':False,'submitted_mathematical_programs_executed':False}
result_path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','checks_passed','source_files_unchanged','archive','publication_sha256','promotion_sha256']}))
