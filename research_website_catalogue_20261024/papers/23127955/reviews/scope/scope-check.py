"""Independent source/edition/asset/editorial checks; no scientific verifier execution."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[1]
SOURCE = PAPER / 'sources'
rows = []

def check(name, condition, detail=None):
    rows.append({'name': name, 'passed': bool(condition), 'detail': detail})
    if not condition:
        raise AssertionError(name)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def norm(text):
    return ' '.join(text.split())

receipt = json.loads((SOURCE / 'receipt.json').read_text())
record = json.loads((SOURCE / 'record.json').read_text())
c = json.loads((HERE / 'content.json').read_text())
tex = (SOURCE / 'published-source/paper.tex').read_text()
check('fresh_metadata_hash', sha(SOURCE / 'record.json') == receipt['record_sha256'])
check('receipt_complete_and_record_selected', receipt['complete'] and str(record['id']) == receipt['record_id'] == '23127955')
for item in receipt['files']:
    path = SOURCE / item['name']
    data = path.read_bytes()
    check('size_' + item['name'], len(data) == item['bytes'])
    check('sha256_' + item['name'], sha(path) == item['sha256'])
    check('md5_' + item['name'], hashlib.md5(data).hexdigest() == item['md5'] == item['zenodo_checksum'].split(':')[1])
    metadata_file = next(f for f in record['files'] if f['key'] == item['name'])
    check('public_metadata_binding_' + item['name'], metadata_file['size'] == len(data) and metadata_file['checksum'] == item['zenodo_checksum'])
with zipfile.ZipFile(SOURCE / c['supplement_filename']) as archive:
    check('zip_crcs', archive.testzip() is None)
    file_members = [member for member in archive.infolist() if not member.is_dir()]
    check('zip_15_regular_files', len(file_members) == 15)
    for member in file_members:
        data = archive.read(member.filename)
        path = SOURCE / 'published-source' / member.filename
        check('extracted_exact_' + member.filename, path.read_bytes() == data)
    extracted_files = {str(p.relative_to(SOURCE / 'published-source')) for p in (SOURCE / 'published-source').rglob('*') if p.is_file()}
    check('exact_extracted_file_set', extracted_files == {member.filename for member in file_members})
pdf_paths = sorted(SOURCE.rglob('*.pdf'))
reader = json.loads((HERE / 'reader-documents.json').read_text())
check('all_reader_pdfs_mapped', {str(p.relative_to(PAPER)) for p in pdf_paths} == {x['path'] for x in reader['reader_pdfs']})
check('one_unique_reader_pdf', len({sha(p) for p in pdf_paths}) == reader['unique_reader_pdf_count'] == 1)
check('no_separate_reader_supplement', reader['supplementary_pdf_count'] == 0 and len(pdf_paths) == 2)
for pdf in pdf_paths:
    info = subprocess.run(['pdfinfo', str(pdf)], capture_output=True, text=True, check=True).stdout
    check('eight_pages_' + str(pdf.relative_to(PAPER)), re.search(r'^Pages:\s+8\s*$', info, re.M) is not None)

matches = re.findall(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S)
check('one_actual_manuscript_abstract', len(matches) == 1)
expected = matches[0].replace('$\\R^3$', 'ℝ³').replace('$2$', '2').replace('~', ' ')
check('full_abstract_exact_after_declared_formatting', norm(expected) == norm(c['abstract']))
check('abstract_paragraphs', len(c['abstract'].split('\n\n')) == 3)
check('title_exact_public_metadata', c['title'] == record['metadata']['title'])
check('version_exact_public_metadata', c['version'] == record['metadata']['version'] == '1.0')
check('date_exact_public_metadata', c['publication_date'] == record['metadata']['publication_date'] == '2026-10-03')
check('manuscript_date_read_from_source', '\\date{3 October 2026' in tex and c['source_binding']['manuscript_date'] == '3 October 2026')
check('no_invented_numbered_manuscript_version', c['source_binding']['manuscript_version'] is None)
check('doi_exact_metadata', c['doi'] == record['doi'] == '10.5281/zenodo.23127955')
check('both_published_downloads_in_candidate', {c['pdf_filename'], c['supplement_filename']} == {x['name'] for x in receipt['files']} and not c['additional_assets'])
binding = c['source_binding']
check('candidate_bound_to_fresh_receipt', binding['source_receipt_sha256'] == sha(SOURCE / 'receipt.json'))
check('candidate_bound_to_metadata', binding['record_metadata_sha256'] == sha(SOURCE / 'record.json'))
check('candidate_bound_to_tex', binding['primary_tex_sha256'] == sha(PAPER / binding['primary_tex_path']))
check('candidate_bound_to_mathematical_support', binding['mathematical_support_sha256'] == sha(PAPER / binding['mathematical_support_path']))
check('pdf_and_zip_candidate_hashes', binding['pdf_sha256'] == sha(SOURCE / c['pdf_filename']) and binding['supplement_sha256'] == sha(SOURCE / c['supplement_filename']))
check('metadata_related_identifiers_preserved', binding['metadata_related_identifiers'] == record['metadata']['related_identifiers'])

plain = ' '.join(c['plain_language'])
result = ' '.join(c['result'])
limits = ' '.join(c['limitations'])
check('actual_contact_and_support_plane_explicit', 'actually meet' in plain and 'supporting plane' in plain and 'actual intersection' in result)
check('spatial_complete_lines_outer_measure_scope', 'complete affine lines' in result and 'three-dimensional Lebesgue outer measure zero' in result)
check('arbitrary_convex_set_scope', all(s in result for s in ['pairwise disjoint', 'closed, bounded, full dimensional', 'closures may intersect', 'contact may be an entire segment']))
check('conjecture_4_versus_3_preserved', 'Conjecture 4' in result and 'does not establish' in result and 'Conjecture 3' in result)
check('no_manifold_or_dimension_overclaim', 'does not prove' in limits and 'Hausdorff-dimension bound of two' in limits and 'smooth surfaces' in limits)
check('nonclosed_locus_boundary_preserved', 'need not itself be closed' in limits)
check('finite_checks_not_universal_proof', 'do not replace the proof' in limits)
check('priority_and_peer_review_limits_explicit', 'not a certification of first priority' in limits and 'not undergone conventional external human peer review' in c['ai_disclosure'])
check('no_filler_followup', c['follow_up'] is None)
check('no_public_internal_audit_replay', not any(s in json.dumps({k:v for k,v in c.items() if k not in ('source_binding','followup_rationale')}) for s in ['October 24', '24 October', 'October 25', '25 October', 'PASS_SCOPE_ONLY', 'SHA-256']))
check('seo_description_bound', 90 <= len(c['description']) <= 160)
check('slug_safe', re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', c['slug']) is not None)
for primary in json.loads((HERE / 'primary-source-receipts.json').read_text()):
    if primary['status'] == 'saved':
        path = HERE / 'primary-sources' / primary['name']
        check('primary_source_bytes_' + primary['name'], path.stat().st_size == primary['bytes'] and sha(path) == primary['sha256'])
check('no_promotion_created', not (PAPER / 'promotion.json').exists() and not (PAPER / 'publication.json').exists())
result = {
    'status': 'PASS_SOURCE_AND_EDITORIAL_CHECKS_ONLY',
    'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scientific_verifier_executed': False,
    'mathematical_verdict': 'NOT_ISSUED',
    'checks_passed': len(rows),
    'checks': rows,
    'source_receipt_sha256': sha(SOURCE / 'receipt.json'),
    'content_sha256': sha(HERE / 'content.json'),
    'checker_sha256': sha(Path(__file__))
}
(HERE / 'scope-check-results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k:result[k] for k in ['status','checked_utc','checks_passed','scientific_verifier_executed']}))
