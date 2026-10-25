"""Owned read-only source/editorial checks; no rendering or mathematical replay."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib
import io
import json
import re
import stat
import subprocess
import sys
import zipfile

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parents[2]
B = P.parents[1]
O = P / 'reviews/publication'
S = P / 'sources'
sys.path.insert(0, str(B / 'scripts'))
from published_assets import normalized_receipt_view


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def normal_abstract(body):
    for old, new in [('$', ''), (r'G_\delta', 'Gδ'), (r'\Z\wr\Z', 'ℤ ≀ ℤ'), ('--', '–')]:
        body = body.replace(old, new)
    return ' '.join(body.split())


def main():
    checks = []

    def need(name, condition):
        if not condition:
            raise RuntimeError(name)
        checks.append({'name': name, 'valid': True})

    c = json.loads((P / 'publication.json').read_text())
    g = json.loads((P / 'promotion.json').read_text())
    rec = json.loads((S / 'record.json').read_text())
    raw_receipt = json.loads((S / 'receipt.json').read_text())
    receipt = normalized_receipt_view(raw_receipt)
    cp = B / g['root_clearance_file']
    clear = json.loads(cp.read_text())
    need('exact_final_root_authority', sha(cp) == g['root_clearance_sha256'] == 'e845d4a8a6c1db3c442a3d67889bbb5cfe027b5b87897243dc1782935818ca6b')
    need('root_decision_and_scope_exact', g['root_clearance_record'] == clear and g['status'] == clear['status'] == 'PASS' and g['disposition_by'] == clear['disposition_by'] == 'root' and g['approved_scope'] == clear['approved_scope'])
    need('publication_and_original_receipt_hashes', sha(P / 'publication.json') == g['publication_sha256'] and sha(S / 'receipt.json') == g['source_receipt_sha256'] == clear['source_receipt_sha256'] == c['source_binding']['source_receipt_sha256'])
    need('original_receipt_normalization_read_only', receipt == raw_receipt and sha(S / 'receipt.json') == '61fe4c17c9abaacc23d87730c29ee688417358e61ffb8d4965514df5603f5b18')
    need('record_hash', sha(S / 'record.json') == receipt['record_sha256'] == c['source_binding']['record_sha256'] == 'f4096d4c3f6357b761902cc97f30454d12e3dbbfe78e8ff4f2ec5201bb0eb827')
    need('exact_title_doi_date_version', all(c[k] == rec['metadata'][k] for k in ['title', 'doi', 'publication_date', 'version']) and c['doi'] == '10.5281/zenodo.23356964')
    need('author_orcid_license', c['author'] == 'Alec Kriebel' and c['orcid'] == 'https://orcid.org/0009-0001-9320-500X' and rec['metadata']['creators'][0]['orcid'] == '0009-0001-9320-500X' and c['license'] == 'CC BY 4.0' and rec['metadata']['license']['id'] == 'cc-by-4.0')
    need('printed_and_metadata_version_date', c['version'] == c['source_binding']['manuscript_version'] == c['source_binding']['zenodo_version'] == '1.0.0' and c['publication_date'] == c['source_binding']['manuscript_date'] == '2026-10-13' and c['edition_label'] == 'Version 1.0.0' and c['publication_date_label'] == 'Manuscript dated')
    need('record_creation_separate', rec['created'] == c['source_binding']['record_created_utc'] == '2026-10-14T04:32:49.677542+00:00' and '14 October 2026 UTC' in c['edition_note'] and 'do not establish first priority' in c['edition_note'])
    need('two_assets_standard_supplement_only', len(receipt['files']) == 2 and c['pdf_filename'] == 'generic-wreath-hyperfiniteness-note.pdf' and c['supplement_filename'] == 'generic-wreath-hyperfiniteness-verification.zip' and c['additional_assets'] == [] and c['source_binding']['embedded_assets'] == [] and {a['name'] for a in receipt['files']} == {c['pdf_filename'], c['supplement_filename']})
    need('asset_records_exact', g['source_files'] == c['source_binding']['files'] == receipt['files'])
    for a in receipt['files']:
        f = S / a['name']
        need('asset_' + a['name'], f.stat().st_size == a['bytes'] and sha(f) == a['sha256'] and hashlib.md5(f.read_bytes()).hexdigest() == a['md5'] and a['zenodo_checksum'] == 'md5:' + a['md5'])
    need('pdf_zip_root_and_config_bindings', sha(S / c['pdf_filename']) == g['pdf_sha256'] == clear['pdf_sha256'] == c['source_binding']['pdf_sha256'] and sha(S / c['supplement_filename']) == g['supplement_sha256'] == c['source_binding']['supplement_sha256'])

    inventory = json.loads((S / 'extraction-integrity.json').read_text())
    records = []
    nested = []
    readers = []
    prefix = S / 'published-source/generic-wreath-hyperfiniteness-verification'

    def scan(data, archive_name, depth=0):
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            if z.testzip() is not None:
                raise RuntimeError('ZIP CRC failed: ' + archive_name)
            for i in z.infolist():
                if i.is_dir():
                    continue
                rel = PurePosixPath(i.filename)
                mode = i.external_attr >> 16
                if rel.is_absolute() or '..' in rel.parts or '\\' in i.filename or stat.S_IFMT(mode) not in (0, stat.S_IFREG):
                    raise RuntimeError('Unsafe archive path/type: ' + i.filename)
                content = z.read(i)
                logical = archive_name + '!/' + i.filename
                h = hashlib.sha256(content).hexdigest()
                record = {'archive': archive_name, 'member': i.filename, 'logical_path': logical, 'bytes': len(content), 'sha256': h, 'crc32': f'{i.CRC:08x}', 'original_mode': oct(mode), 'hidden': any(part.startswith('.') for part in rel.parts), 'depth': depth}
                if depth == 0:
                    extracted = prefix / i.filename
                    if extracted.read_bytes() != content or stat.S_IMODE(extracted.stat().st_mode) != stat.S_IMODE(mode):
                        raise RuntimeError('Extracted outer member differs: ' + i.filename)
                    record['extracted_path'] = str(extracted.relative_to(P))
                records.append(record)
                if rel.suffix.lower() == '.pdf':
                    readers.append({'logical_path': logical, 'sha256': h, 'bytes': len(content)})
                if rel.suffix.lower() == '.zip':
                    nested.append({'logical_path': logical, 'sha256': h, 'bytes': len(content), 'type': 'zip'})
                    scan(content, logical, depth + 1)

    scan((S / c['supplement_filename']).read_bytes(), c['supplement_filename'])
    need('archive_crc_safe_paths_and_all_member_hashes', sorted(records, key=lambda a: a['logical_path']) == sorted(inventory['regular_members'], key=lambda a: a['logical_path']))
    outer_count = sum(r['depth'] == 0 for r in records)
    nested_count = sum(r['depth'] > 0 for r in records)
    need('all_121_outer_51_nested_members', outer_count == clear['root_extracted_outer_members_compared'] == 121 and nested_count == clear['root_nested_member_crc_checked'] == 51)
    need('all_three_nested_archives', nested == inventory['nested_archives'] and len(nested) == clear['root_nested_archives_checked'] == 3)
    need('sole_embedded_reader_duplicate', len(readers) == 1 and readers[0]['sha256'] == g['pdf_sha256'] and sha(prefix / 'note.pdf') == g['pdf_sha256'])
    baseline = json.loads((O / 'source-baseline.json').read_text())['files']
    current = {str(f.relative_to(P)): sha(f) for f in sorted(S.rglob('*')) if f.is_file()}
    need('all_126_original_source_files_unchanged', current == baseline and len(current) == 126)
    main = subprocess.check_output(['pdftotext', '-layout', str(S / c['pdf_filename']), '-'])
    info = subprocess.check_output(['pdfinfo', str(S / c['pdf_filename'])], text=True)
    need('complete_actual_five_page_pdf_text', main == (P / 'reviews/analytic/main.txt').read_bytes() and re.search(r'^Pages:\s+5\s*$', info, re.M) is not None and c['pdf_pages'] == 5)

    tp = P / c['source_binding']['source_tex_path']
    tex = tp.read_text()
    raw = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1).strip()
    need('current_tex_hash_and_printed_date', sha(tp) == c['source_binding']['source_tex_sha256'] == c['source_binding']['abstract_source_sha256'] == 'd636a7b3502bfa2e5bd79e01d5b332fd3b796c9ada60b67bbce30e54eac5aa02' and r'\date{October 13, 2026\quad (version 1.0.0)}' in tex)
    need('complete_original_abstract', normal_abstract(raw) == c['abstract'] == json.loads((P / 'reviews/scope/candidate.json').read_text())['abstract'] == json.loads((O / 'candidate.json').read_text())['abstract'] == (O / 'ABSTRACT.txt').read_text().strip() and (O / 'ABSTRACT.tex').read_text().strip() == raw)
    need('abstract_count_hash_and_normalization', len(c['abstract'].split()) == c['source_binding']['abstract_word_count'] == 93 and len(re.findall(r'\.(?:\s|$)', c['abstract'])) == 6 and hashlib.sha256(raw.encode()).hexdigest() == c['source_binding']['abstract_tex_sha256'] and '\n\n' not in c['abstract'])
    need('frozen_scope_candidate_hash', sha(P / c['source_binding']['frozen_scope_content_path']) == c['source_binding']['frozen_scope_content_sha256'] == sha(O / 'candidate.json') == '0b95149ea4cc9f4ca018ce4d31f9527150d223695d357442e17dc84c87297623')
    need('three_original_review_objects', set(g['reviews']) == {'analytic', 'adversarial', 'scope'})
    for role, v in g['reviews'].items():
        need('original_review_' + role, sha(P / v['report']) == v['sha256'] == clear['reviews'][role]['report_sha256'] and sha(P / v['verdict_file']) == v['verdict_sha256'] == clear['reviews'][role]['verdict_sha256'] and json.loads((P / v['verdict_file']).read_text()) == v['verdict'])
    sv = g['reviews']['scope']['verdict']
    need('pending_scope_chronology_preserved', sv['status'] == 'SCOPE_COMPLETE_MATHEMATICAL_REVIEW_PENDING' and sv['publication_authorized'] is False and sv['mathematical_verdict'] is None and sv['candidate_only'] is True and g['reviews']['scope']['root_disposition'] == 'SCOPE_COMPLETE' and g['scope_gate_resolution'] == clear['scope_gate_resolution'] and sv['completed_utc'] < clear['utc'])

    result = '\n'.join(c['result'])
    proof = '\n'.join(c['why_it_works'])
    limits = '\n'.join(c['limitations'])
    need('restricted_countable_discrete_full_space_whole_phase', all(s in result for s in ['countable discrete restricted wreath product', 'dense Gδ subset of the full Polish space', 'every action in this subset', 'entire Cantor space']))
    need('actual_borel_height_exact_equivariance', all(s in result for s in ['standard Borel space X', 'actual Borel map p:X→Ẑ', 'p(gx)=p(x)+χ(g)', 'shift homomorphism', 'Ẑ=lim ℤ/n!ℤ', 'all of X']))
    need('stabilizers_nonsurjective_and_not_every_action', all(s in result for s in ['permits stabilizers', 'does not require freeness, minimality, an invariant probability measure or surjectivity', 'requires the height factor', 'does not establish hyperfiniteness for every Borel W-action']))
    need('slab_dimension_not_component_finiteness', all(s in proof for s in ['dimension may grow with the width', 'slab components may be infinite', 'Divisible widths', 'decreasing distances', 'exact compatible-metric hypothesis']))
    need('whole_exceptional_preimage_and_cutoff', all(s in proof for s in ['full preimage of the embedded integers', 'may be uncountable', 'height cutoff is essential', 'classes finite', 'pieces are invariant']))
    need('generic_onto_height_distinguished', 'in this compact Cantor setting it is onto' in proof and 'rather than an added assumption in the Borel theorem' in limits)
    need('no_general_union_or_uniform_dimension', 'Dimension bounds need not be uniform across widths' in limits and 'rather than a general theorem about increasing unions' in limits)
    need('no_generic_conjugacy_uniform_selection_or_phase_restriction', all(s in limits for s in ['does not identify the entire set of hyperfinite actions as Gδ', 'every point of the phase space', 'No comeager conjugacy class', 'uniform Borel choice', 'clopen finite exhaustion']))
    background = json.dumps(c['background'], ensure_ascii=False)
    need('original_question_and_classical_credit', all(s in background for s in ['Question 3', '114–115', 'Conley', 'Jackson', 'Marks', 'Seward', 'Tucker-Drob', 'Corollary 5.5', 'Theorem 7.3', 'Corollary 7.5', 'Akin', 'Glasner', 'Weiss', '2006 author preprint', '2008 journal paper', 'Doucha', 'Melleray', 'Tsankov', 'version 2', 'Iyer', 'Shinko']))
    need('no_firstness_or_current_openness_claim', 'No historical firstness' in limits and 'continued worldwide openness' in limits)
    public = '\n'.join([c['title'], c['description'], c['abstract'], *c['plain_language'], *c['result'], *c['why_it_works'], *c['limitations'], c['ai_disclosure'], c['collaboration'], *[x['note'] for x in c['background']]])
    need('internal_custody_replay_narratives_absent', re.search(r'372.?046|10.?108|97.?924|20.?525|53.?857|12.?349|121 outer|172 (?:archive|members)|root.clearance|SHA.?256|replay|dated priority audit|independent.*\bPASS\b', public, re.I) is None)
    need('extensive_ai_unrefereed_human_review_boundary', 'unrefereed' in c['status'].lower() and 'extensively' in c['ai_disclosure'] and 'do not constitute independent human or journal peer review' in c['ai_disclosure'])
    need('null_followup_passive_actual_contribution_collaboration', c['follow_up'] is g['follow_up'] is clear['follow_up'] is None and 'actual research contributions' in c['collaboration'])
    need('canonical_slug_description', c['canonical_url'] == 'https://aleckriebel.com/research/' + c['slug'] + '/' and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', c['slug']) is not None and 90 <= len(c['description']) <= 170)
    need('renderer_fields_types', all(isinstance(c[k], list) and c[k] for k in ['plain_language', 'result', 'why_it_works', 'limitations', 'background']) and all(k in c for k in ['title', 'slug', 'description', 'abstract', 'collaboration', 'publication_date', 'version', 'doi', 'author', 'pdf_filename', 'supplement_filename']) and all(set(x) == {'title', 'url', 'note'} for x in c['background']))
    need('rendered_public_copy_approval_remains_pending', c['review_metadata']['rendered'] is False and c['review_metadata']['deployed'] is False and c['review_metadata']['root_clearance_sha256'] == sha(cp) and g['preparation_state'] == c['source_binding']['publication_state'] == 'BINDINGS_READY_RENDERING_PENDING' and g['source_repair'] is g['human_peer_review'] is g['formal_machine_verification'] is False)
    primaries = json.loads((P / 'reviews/scope/primary-source-receipts.json').read_text())
    acquired = [a for a in primaries if a['status'] == 'acquired']
    need('all_seven_primary_pdf_custody_bindings', len(acquired) == 7 and all(sha(P / 'reviews/scope/cache/primary-sources' / a['name']) == a['sha256'] and (P / 'reviews/scope/cache/primary-sources' / a['name']).stat().st_size == a['bytes'] for a in acquired))
    output = {'checked_utc': datetime.now(timezone.utc).isoformat(), 'record_id': '23356964', 'status': 'EDITORIAL_BINDINGS_VALID_RENDER_PENDING', 'checks': checks, 'check_count': len(checks), 'public_assets_verified': 2, 'outer_archive_members_verified': outer_count, 'nested_archive_members_verified': nested_count, 'nested_archives_verified': len(nested), 'original_source_files_unchanged': len(baseline), 'primary_pdfs_rehashed': len(acquired), 'publication_sha256': sha(P / 'publication.json'), 'promotion_sha256': sha(P / 'promotion.json'), 'submitted_math_executed': False, 'rendered': False, 'deployed': False, 'shared_files_changed': False}
    (O / 'editorial-checks.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: output[k] for k in ['status', 'check_count', 'public_assets_verified', 'outer_archive_members_verified', 'nested_archive_members_verified', 'nested_archives_verified', 'original_source_files_unchanged']}))


if __name__ == '__main__':
    main()
