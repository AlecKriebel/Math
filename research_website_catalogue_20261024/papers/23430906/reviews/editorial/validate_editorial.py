"""Check editorial bindings and untouched inputs; write only a new editorial stem."""
from pathlib import Path, PurePosixPath
import datetime
import hashlib
import json
import re
import stat
import subprocess
import sys
import unicodedata
import zipfile

ROOT = Path(__file__).resolve().parents[4]
PAPER = ROOT/'papers/23430906'
OUT = PAPER/'reviews/editorial'
stem = sys.argv[1]
assert re.fullmatch(r'[a-z0-9-]+', stem)
result_path = OUT/(stem+'.json')
after_path = OUT/(stem+'-custody-after.json')
assert not result_path.exists() and not after_path.exists()
checks = []

def load(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check(name, condition, detail=None):
    checks.append({'name': name, 'pass': bool(condition), **({'detail': detail} if detail is not None else {})})
    if not condition:
        raise AssertionError(name)

pub, gate = load(PAPER/'publication.json'), load(PAPER/'promotion.json')
clearpath = ROOT/gate['root_clearance_file']
clear, receipt = load(clearpath), load(PAPER/'sources/receipt.json')
record = load(PAPER/'sources/record.json')
candidate = load(PAPER/'reviews/scope/content.json')
check('exact_current_root_hash', sha(clearpath) == gate['root_clearance_sha256'] == '86a8ceed51423cf9c79c71b41389c644361d9b75b54b6bce9093ff9fa0307e8d')
check('full_root_record_preserved', gate['root_clearance_record'] == clear)
check('root_disposition_and_scope_copied', gate['status'] == clear['status'] == 'PASS' and gate['disposition_by'] == clear['disposition_by'] == 'root' and gate['approved_scope'] == clear['approved_scope'])
check('publication_bound', sha(PAPER/'publication.json') == gate['publication_sha256'])
check('receipt_bytes_bound', sha(PAPER/'sources/receipt.json') == clear['source_receipt_sha256'] == gate['source_receipt_sha256'] == pub['source_binding']['receipt_sha256'])
check('complete_receipt_object_and_entries_preserved', gate['source_receipt_record'] == receipt and gate['source_files'] == receipt['files'] == pub['source_binding']['files'])
check('receipt_original_shape_preserved', 'record_sha256' not in receipt and receipt['record_raw_sha256'] == sha(PAPER/'sources/record-raw.json'))
check('separate_normalized_record_binding', sha(PAPER/'sources/record.json') == gate['metadata_sha256'] == pub['source_binding']['metadata_sha256'])
check('public_identity', pub['title'] == record['metadata']['title'] and pub['doi'] == record['doi'] == '10.5281/zenodo.23430906' and pub['version'] == record['metadata']['version'] == '1.0' and record['status'] == 'published')
check('author_orcid', pub['author'] == 'Alec Kriebel' and pub['orcid'] == 'https://orcid.org/0009-0001-9320-500X' and record['metadata']['creators'][0]['orcid'] == '0009-0001-9320-500X')
check('edition_dates_distinct', pub['publication_date'] == record['metadata']['publication_date'] == '2026-10-14' and record['created'] == pub['source_binding']['record_created_utc'] == '2026-10-17T05:14:35.437960+00:00' and '17 October 2026 UTC' in pub['edition_note'])
check('final_canonical', pub['canonical_url'] == 'https://aleckriebel.com/research/'+pub['slug']+'/' and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', pub['slug']))
check('full_abstract_same_as_frozen_candidate', pub['abstract'] == candidate['abstract'] and pub['abstract_heading'] == 'Original abstract' and pub['abstract_is_original'] is True and '\n\n' not in pub['abstract'])

texpath = PAPER/pub['source_binding']['source_tex_path']
raw = re.search(r'\\begin\{abstract\}\n(.*?)\\end\{abstract\}', texpath.read_text(), re.S).group(1)
check('raw_abstract_source_identical', raw == pub['source_binding']['abstract_tex'] == candidate['abstract_original_tex'] == (PAPER/'reviews/scope/abstract-source.tex').read_text())
check('tex_and_abstract_hashes', sha(texpath) == clear['source_tex_sha256'] == pub['source_binding']['source_tex_sha256'] and hashlib.sha256(raw.encode()).hexdigest() == pub['source_binding']['abstract_tex_sha256'])
replacements = {
    r'$H\in(1/4,1)$': 'H ∈ (1/4,1)',
    r'$X_T=\int_0^T B^1_s\,dB^2_s$': 'X_T = ∫₀ᵀ B¹_s dB²_s',
    r'$c_HT^{2H}n^{1/2-2H}$': 'c_H T^(2H)n^(1/2−2H)',
    r'$n\ge1$': 'n ≥ 1', r'$T>0$': 'T > 0',
    r'$[0,T]$': '[0,T]', r'$L^2$': 'L²', r'$H$': 'H', r'$n$': 'n'
}
normalized = raw
for old, new in replacements.items():
    normalized = normalized.replace(old, new)
normalized = ' '.join(normalized.split())
check('all_original_abstract_words_exact_under_math_normalization', normalized == pub['abstract'])

pdftext = (OUT/'published-reader.txt').read_text()
pdfabstract = pdftext.split('Abstract', 1)[1].split('Keywords:', 1)[0]
def words(text):
    text = unicodedata.normalize('NFKC', text)
    # Poppler places the stacked integral/upper-limit artifact on its own
    # line between two prose lines; it is mathematical layout, not a word.
    text = re.sub(r'(?m)^\s*RT\s*$', '', text)
    text = re.sub(r'([A-Za-z])-\s*\n\s*([A-Za-z])', r'\1\2', text)
    return re.findall(r'[A-Za-z]+', text)
pdfwords = words(pdfabstract)
position = 0
for index, fragment in enumerate(re.split(r'\$[^$]*\$', raw)):
    target = words(fragment)
    if not target:
        continue
    found = next((i for i in range(position, len(pdfwords)-len(target)+1) if pdfwords[i:i+len(target)] == target), None)
    check('pdf_original_abstract_prose_fragment_'+str(index), found is not None)
    position = found + len(target)
pdfinfo = subprocess.run(['pdfinfo', str(PAPER/'sources/paper.pdf')], capture_output=True, text=True, check=True).stdout
check('seven_page_searchable_reader', int(pdfinfo.split('Pages:')[1].splitlines()[0]) == pub['pdf_pages'] == 7 and all(len(page.strip()) > 300 for page in pdftext.split('\f')[:-1]))

for item in receipt['files']:
    path = PAPER/'sources'/item['name']
    check('asset_'+item['name'], path.stat().st_size == item['bytes'] and sha(path) == item['sha256'] and hashlib.md5(path.read_bytes()).hexdigest() == item['md5'])
check('exact_two_public_assets', {x['name'] for x in receipt['files']} == {pub['pdf_filename'], pub['supplement_filename']} and pub['additional_assets'] == [])
check('fixed_pdf_support_bindings', gate['pdf_sha256'] == clear['pdf_sha256'] == '33b90a4d846db58ea93efd453c13455fbeb3a29dcaa3e4cc49a68c0a8ebdff5b' and gate['supplement_sha256'] == clear['supplement_sha256'] == '4e4a1b20c2da7f5a6e686256f7f8d7bba9c8db71e21f316f99da63285f7b0191')
members = nested = pdfs = 0
with zipfile.ZipFile(PAPER/'sources'/pub['supplement_filename']) as archive:
    check('archive_crc', archive.testzip() is None)
    for item in archive.infolist():
        name = PurePosixPath(item.filename)
        mode = item.external_attr >> 16
        check('safe_archive_member_'+item.filename, not name.is_absolute() and '..' not in name.parts and '\\' not in item.filename and not stat.S_ISLNK(mode) and stat.S_IFMT(mode) in (0, stat.S_IFREG, stat.S_IFDIR))
        if item.is_dir():
            continue
        data = archive.read(item)
        check('unchanged_extracted_member_'+item.filename, (PAPER/'sources/support'/item.filename).read_bytes() == data)
        members += 1
        pdfs += data.startswith(b'%PDF')
        nested += data.startswith((b'PK\x03\x04', b'\x1f\x8b')) or data[257:262] == b'ustar'
check('archive_shape', members == 225 and pdfs == 1 and nested == 0)
check('embedded_reader_identical', (PAPER/'sources/support/paper.pdf').read_bytes() == (PAPER/'sources/paper.pdf').read_bytes())

for role, item in gate['reviews'].items():
    check(role+'_exact_report_hash', sha(PAPER/item['report']) == item['sha256'] == clear['reviews'][role]['report_sha256'])
    check(role+'_exact_custom_verdict', sha(PAPER/item['verdict_file']) == item['verdict_sha256'] == clear['reviews'][role]['verdict_sha256'] and item['verdict'] == load(PAPER/item['verdict_file']))
scope = gate['reviews']['scope']['verdict']
analytic = gate['reviews']['analytic']['verdict']
adversarial = gate['reviews']['adversarial']['verdict']
check('scope_pending_null_false_unchanged', scope['verdict'] == 'SCOPE_COMPLETE_ATTRIBUTION_QUALIFIED_MATHEMATICAL_GATE_PENDING' and scope['mathematical_verdict'] is None and scope['substantive_defect_found'] is None and scope['promotion_authorized'] is False and gate['reviews']['scope']['root_disposition'] == 'SCOPE_COMPLETE')
check('scope_candidate_hold_preserved', candidate['candidate_status'] == 'HELD_CANDIDATE_ONLY_PENDING_SEPARATE_MATHEMATICAL_GATE' and candidate['mathematical_verdict'] is None)
check('analytic_original_schema_preserved', analytic['status'] == 'COMPLETE' and analytic['verdict'] == 'PASS' and analytic['publication_clearance_claimed'] is False and bool(analytic['review_self_correction']))
check('adversarial_custom_verdict_not_manufactured', adversarial['verdict'] == 'NO_SUBSTANTIVE_DEFECT_OR_UNRESOLVED_CENTRAL_GAP_FOUND' and 'status' not in adversarial and adversarial['publication_clearance'] is False)
check('root_scope_resolution_exact', gate['scope_gate_resolution'] == clear['scope_gate_resolution'])
check('root_custody_receipt_exact', sha(ROOT/clear['root_custody_receipt']) == clear['root_custody_receipt_sha256'])
rootcustody = load(ROOT/clear['root_custody_receipt'])
sealed = 0
for row in load(PAPER/'reviews/scope/SEAL.json')['files']:
    check('scope_frozen_binding_'+row['path'], sha(PAPER/row['path']) == row['sha256'])
    sealed += 1
analytic_seal = load(PAPER/'reviews/analytic/FINAL_SEAL.json')
check('analytic_final_manifest_binding', sha(PAPER/'reviews/analytic/MANIFEST_SHA256.json') == analytic_seal['manifest_sha256'])
for row in load(PAPER/'reviews/analytic/MANIFEST_SHA256.json')['all_owned_files_except_seal_manifest']:
    check('analytic_frozen_binding_'+row['path'], sha(PAPER/'reviews/analytic'/row['path']) == row['sha256'])
    sealed += 1
adversarial_seal = load(PAPER/'reviews/adversarial/SEAL.json')
check('adversarial_output_pin_binding', sha(PAPER/'reviews/adversarial/OUTPUT_PINS.json') == adversarial_seal['output_pins_sha256'])
for row in load(PAPER/'reviews/adversarial/OUTPUT_PINS.json')['files']:
    check('adversarial_frozen_binding_'+row['path'], sha(PAPER/'reviews/adversarial'/row['path']) == row['sha256'])
    sealed += 1
for role, name in [('scope','SEAL.json'), ('analytic','FINAL_SEAL.json'), ('adversarial','SEAL.json')]:
    check('root_'+role+'_seal_hash', sha(PAPER/'reviews'/role/name) == rootcustody['manifest_hashes'][role])
check('all_root_sealed_bindings_rechecked', sealed == rootcustody['binding_count'] == clear['root_final_seal_bindings_rehashed'] == 560)

before = load(OUT/'frozen-inputs-before.json')
after = {}
for top in ['sources', 'reviews/scope', 'reviews/analytic', 'reviews/adversarial', 'reviews/root']:
    for path in sorted((PAPER/top).rglob('*')):
        if path.is_file():
            after[str(path.relative_to(PAPER))] = sha(path)
check('all_837_frozen_inputs_preserved', after == before['files'] and len(after) == before['file_count'] == 837)
after_path.write_text(json.dumps({'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'file_count': len(after), 'files': after, 'all_preserved': True, 'root_clearance_sha256': sha(clearpath)}, indent=2)+'\n')

sections = load(OUT/'public-sections.json')
adapter = load(OUT/'SCHEMA_ADAPTER.json')
copy = (OUT/'PUBLIC_COPY.md').read_text()
check('expected_sections_complete_ordered', [x['heading'] for x in sections['sections']] == adapter['expected_sections'] and [x.split('\n')[0] for x in copy.split('## ')[1:]] == adapter['expected_sections'])
check('abstract_one_full_public_paragraph', sections['sections'][0]['paragraphs'] == [pub['abstract']] and copy.split('## Original abstract\n\n',1)[1].split('\n\n## ',1)[0] == pub['abstract'])
fields = [('plain-language','plain_language'),('result','result'),('proof','why_it_works'),('limits','limitations')]
for section_id, field in fields:
    check('public_section_'+field, next(x for x in sections['sections'] if x['id']==section_id)['paragraphs'] == pub[field] and all(paragraph in copy for paragraph in pub[field]))
check('all_prior_links_present', sections['sections'][-1]['references'] == pub['background'] and all(x['url'] in copy for x in pub['background']))
check('asset_and_iframe_specification', sections['sections'][6]['iframe']['src'] == 'paper.pdf#view=FitH' and sections['sections'][6]['links'][1]['download'] is True and sections['sections'][7]['links'][0]['download'] is True and 'https://zenodo.org/records/23430906/files/paper.pdf' in copy and 'https://zenodo.org/records/23430906/files/PR1071_preprint_v1_0_support.zip' in copy)
text = ' '.join(pub['result'])
check('literal_theorem_quantifiers_retained', all(term in text for term in ['H ∈ (1/4,1)', 'independent centered standard', 'same Hurst parameter', 'canonical iterated integral', 'both complete deterministic uniform grids', 'n observations per component', 'including T', 'Every F ∈ L²', 'nonlinear', 'T > 0', 'n ≥ 1', '2πa/(D_H√(P̄_fP̄_g))']))
check('area_factors_retained', all(term in ' '.join(pub['limitations']) for term in ['halved antisymmetric', 'endpoint product is observed', 'same optimal conditional residual', 'unhalved antisymmetric difference has twice']))
check('prior_credit_and_no_priority_clearance', all(term in copy for term in ['Brownian optimum', 'smooth H>1/2', 'Fourier', 'Gaussian', 'Dickinson', 'Jackowski', 'worldwide current-open status remain unverified']))
check('all_exclusions_present', all(term in ' '.join(pub['limitations']) for term in ['unequal Hurst', 'correlated', 'nonuniform or adaptive', 'sharp constant', 'normalized-error limit', 'limiting law', 'uniform in H', 'endpoint']))
check('ai_and_actual_authorship', all(term in pub['ai_disclosure'] for term in ['extensively', 'unrefereed', 'human or journal peer review', 'without formal proof-assistant certification']) and all(term in pub['collaboration'] for term in ['mutual agreement', 'actual research and writing contributions']))
public_text = json.dumps({k: pub[k] for k in ['title','description','abstract','plain_language','result','why_it_works','limitations','background','collaboration','ai_disclosure','edition_note']}, ensure_ascii=False)
check('private_verification_narrative_absent', not re.search(r'[a-f0-9]{64}|2026-10-25|root.clearance|source.custody|quarantine|replay counts|560|225 members|PASS_EDITORIAL|review self-correction', public_text, re.I))
check('followup_null_everywhere', pub['follow_up'] is gate['follow_up'] is clear['follow_up'] is sections['follow_up'] is None)
check('render_live_native_gates_withheld', not pub['review_metadata']['rendered'] and not pub['review_metadata']['deployed'] and not gate['rendered_copy_verified'] and not gate['live_verified'] and not gate['browser_verified'] and gate['native_sheet_aa_url'] is sections['native_sheet_aa_url'] is adapter['native_sheet_aa_url'] is None)
result = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'record_id': '23430906', 'status': 'PASS_EDITORIAL_BINDINGS_ONLY', 'completion_percent_for_assigned_editorial_preparation': 100, 'checks_passed': len(checks), 'checks': checks, 'frozen_input_files_unchanged': len(after), 'sealed_bindings_rechecked': sealed, 'archive_members_compared': members, 'publication_sha256': sha(PAPER/'publication.json'), 'promotion_sha256': sha(PAPER/'promotion.json'), 'root_clearance_sha256': sha(clearpath), 'website_rendered': False, 'live_verified': False, 'browser_verified': False, 'native_tracker_modified': False, 'submitted_mathematical_programs_executed': False}
result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({k: result[k] for k in ['status','checks_passed','frozen_input_files_unchanged','sealed_bindings_rechecked','archive_members_compared','publication_sha256','promotion_sha256']}))
