"""Editorial input checks only: no rendering, publication, or submitted math execution.

Each invocation needs a new output stem. Existing receipts are never overwritten.
"""
from pathlib import Path
import argparse
from datetime import datetime, timezone
import hashlib
import json
import re
import subprocess
import sys
import zipfile

P = Path(__file__).resolve().parents[2]
B = P.parents[1]
O = P / 'reviews/publication'
S = P / 'sources'
ROOT_SHA = '9faabde229535455e707dfae14639727c129953be08b08b2984299a83da0b436'
TEX = 'sources/published-source/nonunique_nearest_stable_complex_quadratics_verification/nonunique_nearest_stable_complex_quadratics_verification/nonunique_nearest_stable_complex_quadratics.tex'
TEX_SHA = 'caf327484a7068244ab98494eab835f50b84521a6d7ba364007bda31f7478677'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_abstract(body):
    return ' '.join(body.replace('$z^2$', 'z²').split())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-stem', required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+', args.output_stem):
        parser.error('Use a simple output filename stem.')
    target = O / (args.output_stem + '.json')
    if target.exists():
        parser.error('Existing evidence is preserved; choose a new output stem.')
    checks = []

    def need(name, condition):
        if not condition:
            raise RuntimeError(name)
        checks.append({'name': name, 'valid': True})

    c = json.loads((P / 'publication.json').read_text())
    g = json.loads((P / 'promotion.json').read_text())
    rec = json.loads((S / 'metadata.json').read_text())
    receipt = json.loads((S / 'receipt.json').read_text())
    clear_path = B / g['root_clearance_file']
    clear = json.loads(clear_path.read_text())
    need('exact_root_authority', sha(clear_path) == g['root_clearance_sha256'] == c['review_metadata']['root_clearance_sha256'] == ROOT_SHA)
    need('root_decision_exact', clear == g['root_clearance_record'] and clear['status'] == g['status'] == 'PASS' and clear['disposition_by'] == g['disposition_by'] == 'root' and g['approved_scope'] == clear['approved_scope'])
    need('publication_receipt_binding', sha(P / 'publication.json') == g['publication_sha256'] and sha(S / 'receipt.json') == g['source_receipt_sha256'] == clear['source_receipt_sha256'] == c['source_binding']['receipt_sha256'])
    need('original_metadata_path_and_hash', not (S / 'record.json').exists() and c['source_binding']['metadata_path'] == c['source_binding']['record_path'] == g['metadata_path'] == 'sources/metadata.json' and sha(S / 'metadata.json') == receipt['metadata_sha256'] == g['metadata_sha256'] == c['source_binding']['metadata_sha256'] == c['source_binding']['record_sha256'])
    need('title_date_version_doi', all(c[k] == rec['metadata'][k] for k in ['title', 'publication_date', 'version', 'doi']) and c['title'] == 'Nonunique nearest stable complex quadratics' and c['doi'] == '10.5281/zenodo.23306332')
    need('author_orcid', c['author'] == 'Alec Kriebel' and c['orcid'] == 'https://orcid.org/0009-0001-9320-500X')
    need('edition_date_distinction', c['version'] == c['source_binding']['zenodo_version'] == '1.0' and c['source_binding']['manuscript_version'] is None and c['publication_date'] == c['source_binding']['manuscript_date'] == '2026-10-11' and c['edition_label'] == c['citation_edition_label'] == 'Zenodo version 1.0' and c['publication_date_label'] == 'Manuscript dated')
    need('record_creation_separate', rec['created'] == c['source_binding']['record_created_utc'] == '2026-10-11T23:14:10.664861+00:00' and 'without printing a version number' in c['edition_note'] and 'do not establish first priority' in c['edition_note'])
    need('two_original_assets', len(receipt['files']) == 2 and {x['filename'] for x in receipt['files']} == {c['pdf_filename'], c['supplement_filename']} and c['additional_assets'] == c['source_binding']['embedded_assets'] == [])
    need('asset_records_exact', g['source_files'] == c['source_binding']['files'] == receipt['files'])
    for item in receipt['files']:
        path = S / item['filename']
        need('asset_' + item['filename'], path.stat().st_size == item['bytes'] and sha(path) == item['sha256'] and hashlib.md5(path.read_bytes()).hexdigest() == item['md5'])
    need('pdf_zip_bindings', sha(S / c['pdf_filename']) == clear['pdf_sha256'] == g['pdf_sha256'] == c['source_binding']['pdf_sha256'] and sha(S / c['supplement_filename']) == g['supplement_sha256'] == c['source_binding']['supplement_sha256'])
    count = 0
    with zipfile.ZipFile(S / c['supplement_filename']) as archive:
        need('zip_crc', archive.testzip() is None)
        members = [x for x in archive.infolist() if not x.is_dir()]
        need('zip_no_embedded_reader_or_nested_archive', not any(x.filename.lower().endswith(('.pdf', '.zip', '.tar', '.gz')) for x in members))
        for item in members:
            path = S / 'published-source/nonunique_nearest_stable_complex_quadratics_verification' / item.filename
            need('archive_member_' + item.filename, path.read_bytes() == archive.read(item))
            count += 1
    need('twelve_exact_members', count == 12)
    text = subprocess.check_output(['/opt/homebrew/bin/pdftotext', str(S / c['pdf_filename']), '-'], text=True)
    pages = text.split('\f')
    if not pages[-1].strip():
        pages.pop()
    need('six_searchable_pdf_pages', len(pages) == c['pdf_pages'] == 6 and all(len(x.strip()) > 100 for x in pages))
    tp = P / TEX
    tex = tp.read_text()
    raw = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1).strip()
    need('source_tex_identity', sha(tp) == c['source_binding']['source_tex_sha256'] == c['source_binding']['abstract_source_sha256'] == TEX_SHA and c['source_binding']['source_tex_path'] == c['source_binding']['abstract_source'] == TEX)
    need('raw_abstract_identity', hashlib.sha256(raw.encode()).hexdigest() == c['source_binding']['abstract_tex_sha256'] == 'e923d5b23fa4b00127bb3c3b1a9ec5382d45ebb2d366aadab0ce6f3e959c8aff' and (O / 'ABSTRACT.tex').read_text() == raw + '\n')
    frozen = json.loads((P / 'reviews/scope/public-candidate.json').read_text())
    need('full_original_abstract', normalized_abstract(raw) == c['abstract'] == frozen['full_original_abstract'] == (O / 'ABSTRACT.txt').read_text().strip() == json.loads((O / 'candidate.json').read_text())['abstract'])
    need('full_abstract_seven_sentences_124_words_one_paragraph', len(c['abstract'].split()) == c['source_binding']['abstract_word_count'] == 124 and len(re.findall(r'\.(?:\s|$)', c['abstract'])) == 7 and len(re.split(r'\n\s*\n', raw)) == 1 and '\n\n' not in c['abstract'])
    need('printed_manuscript_date_no_version', r'\date{11 October 2026\quad\textnormal{(research note; unrefereed preprint)}}' in tex and 'version 1.0' not in tex.lower())
    need('frozen_scope_content_binding', c['source_binding']['frozen_scope_content_path'] == 'reviews/scope/public-candidate.json' and c['source_binding']['frozen_scope_content_sha256'] == sha(P / 'reviews/scope/public-candidate.json') and c['source_binding']['frozen_scope_abstract_field'] == 'full_original_abstract')
    need('three_original_review_objects', set(g['reviews']) == set(clear['reviews']) == {'analytic', 'adversarial', 'scope'})
    for role, item in g['reviews'].items():
        need('original_review_' + role, sha(P / item['report']) == item['sha256'] == clear['reviews'][role]['report_sha256'] and sha(P / item['verdict_file']) == item['verdict_sha256'] == clear['reviews'][role]['verdict_sha256'] and json.loads((P / item['verdict_file']).read_text()) == item['verdict'])
    av, dv, sv = (g['reviews'][x]['verdict'] for x in ['analytic', 'adversarial', 'scope'])
    need('custom_scientific_verdicts_preserved', av['verdict'] == 'PASS_WITH_BOUNDED_BIBLIOGRAPHIC_LIMITS' and av['publication_clearance'] is False and dv['result'] == 'no_substantive_mathematical_defect_found' and dv['promotion_clearance'] is False and g['reviews']['analytic']['root_disposition'] == g['reviews']['adversarial']['root_disposition'] == 'PASS')
    need('scope_pending_chronology_preserved', sv['scope_status'] == 'COMPLETE — conditional scope candidate ready' and sv['mathematical_pass'] is False and sv['mathematical_verdict'] is None and sv['promotion_authorized'] is False and g['reviews']['scope']['root_disposition'] == 'SCOPE_COMPLETE' and g['scope_gate_resolution'] == clear['scope_gate_resolution'])
    need('root_seals_preserved', all(sha(B / x['path']) == x['sha256'] for x in clear['root_review_seals_rehashed']))
    result, proof, limits = ('\n'.join(c[x]) for x in ['result', 'why_it_works', 'limitations'])
    need('complex_closed_monic_fixed_metric', all(x in result for x in ['complex monic quadratic', 'α(p)≤0', '(Re a, Im a, Re b, Im b)', 'For each fixed real symmetric positive-definite', 'every neighborhood', 'some unstable quadratic', 'at least two distinct attained global nearest points', 'all complex stable quadratics', 'imaginary-axis roots']))
    need('full_degree_all_directions_and_attainment', all(x in result for x in ['ℓ≠0', '(1,0,0)', 'metric on ℝ⁶', 'Both real leading-coefficient directions', 'original exact-degree set', 'not globally closed']) and all(x in proof for x in ['compact', 'less than R/3', 'more than 2R/3', 'global minimizers coincide']))
    need('whole_epigraph_mixed_covector', all(x in result for x in ['entire abscissa epigraph', 'height zero', 'monic and full-degree', 'metric may mix height and coefficient', 'support covector is horizontal', 'normal vector can tilt']))
    need('separate_fixed_finite_subgradient_function', all(x in result for x in ['Separately', 'each fixed finite limiting subgradient', 'real Euclidean coefficient metric', 'constants may depend', '(v₀,−1)']) and all(x in limits for x in ['uniform over all finite subgradients', 'full-degree function theorem', 'every mixed coefficient/height metric']))
    need('actual_normal_and_classical_projection', all(x in proof for x in ['x≥0, U=u+y²/4≥0', 'V²≤x²U', 'n₀·cₜ=t³', '2t⁴+t⁶', 'actual proximal normals', 'classical Poliquin–Rockafellar–Thibault projection characterization', 'bounded minimizing-sequence']))
    need('function_direct_diffeomorphism_and_citation_caveat', all(x in proof for x in ['invertible discriminant-coordinate map', 'transports lower supports in both directions', 'Fixing a finite subgradient']) and all(x in limits for x in ['Theorem 3.1', 'does not itself state unconditional exact subdifferential equality', 'two-sided diffeomorphism and lower-support argument']))
    need('real_only_and_metric_boundaries', all(x in limits for x in ['no all-degree or real-only classification', 'convex orthant a≥0,b≥0', 'arbitrary norms, singular or varying metrics', 'nonlinear parameter-dependent metrics', 'No explicit unstable input']))
    background = json.dumps(c['background'], ensure_ascii=False)
    need('historical_conventions_qualified', all(x in background for x in ['Section 8', 'pp.166–168', 'Question 1 on p.106', 'leaves field, normalization and metric unspecified']) and 'no unqualified real-only answer' in limits)
    need('prior_projection_and_approximation_credit', all(x in background for x in ['Theorem 1.3(a),(k)', 'Closedness is essential', 'local weak-closedness', 'Orban de Xivry', 'Kirillov and Overton', 'Burke and Overton', 'Moses and Liu']))
    need('bounded_unread_historical_bodies', all(x in limits for x in ['original Cross, Moses–Liu and Bottema bodies were not inspected', 'exact example and nonuniqueness comparisons are not asserted here', 'No historical firstness, exhaustive novelty clearance or continued worldwide openness']))
    need('finite_controls_not_proof', all(x in limits for x in ['Decimal controls are not interval-certified', 'finite computations do not establish', 'by themselves']))
    public = '\n'.join([c['title'], c['description'], c['abstract'], *c['plain_language'], result, proof, limits, background, c['ai_disclosure'], c['collaboration'], c['edition_note']])
    need('private_audit_narratives_absent', re.search(r'31,233|31233|4,305|4305|2,005|2005 rational|90-digit|12 members|root-clearance|SHA-?256|replay|25 October 2026|2026-10-25', public, re.I) is None)
    need('ai_unrefereed_authorship', all(x in c['ai_disclosure'] for x in ['used extensively', 'not independent human or journal peer review', 'unrefereed preprint', 'without formal proof-assistant certification', 'named author is responsible']) and 'actual research contributions' in c['collaboration'])
    need('followup_null', c['follow_up'] is g['follow_up'] is clear['follow_up'] is None and bool(c['followup_rationale']))
    need('canonical_description', c['canonical_url'] == 'https://aleckriebel.com/research/' + c['slug'] + '/' and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', c['slug']) is not None and 90 <= len(c['description']) <= 170)
    need('renderer_fields', all(k in c for k in ['title', 'slug', 'description', 'abstract', 'plain_language', 'result', 'why_it_works', 'limitations', 'background', 'collaboration', 'publication_date', 'version', 'doi', 'author', 'pdf_filename', 'supplement_filename']))
    need('actual_page_not_rendered_or_approved', c['review_metadata']['rendered'] is False and c['review_metadata']['deployed'] is False and g['preparation_state'] == 'BINDINGS_READY_RENDERING_PENDING' and g['source_repair'] is False and g['human_peer_review'] is False and g['formal_machine_verification'] is False)
    # Direct full-text equality protects even mathematical symbols ignored by word tokenizers.
    sentences = re.split(r'(?<=\.)\s+', c['abstract'])
    for name, index in [('first', 0), ('middle', len(sentences) // 2), ('last', len(sentences) - 1)]:
        altered = ' '.join(x for i, x in enumerate(sentences) if i != index)
        need('negative_' + name + '_abstract_sentence_omission', normalized_abstract(raw) != altered)
    need('negative_abstract_symbol_change', normalized_abstract(raw) != c['abstract'].replace('z²', 'z³', 1))
    baseline = json.loads((O / 'frozen-baseline.json').read_text())['files']
    need('all_original_inputs_unchanged', len(baseline) == 166 and all(sha(P / name) == h for name, h in baseline.items()))
    need('all_seventeen_original_source_files_unchanged', sum(x.startswith('sources/') for x in baseline) == 17)
    # Check the renderer's asset interface without importing/executing the renderer.
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(B / 'scripts'))
    from published_assets import PublishedAssets, normalized_receipt_view
    resolved = PublishedAssets(S, normalized_receipt_view(receipt), [])
    need('existing_asset_interface_accepts_original_filename_schema', all(resolved.resolve(x['filename']).sha256 == x['sha256'] for x in receipt['files']))
    report = {'checked_utc': datetime.now(timezone.utc).isoformat(), 'record_id': '23306332',
              'status': 'EDITORIAL_BINDINGS_VALID_RENDER_PENDING', 'completion_percent': 100,
              'checks': checks, 'check_count': len(checks), 'public_assets_verified': 2,
              'archive_members_verified': count, 'original_source_files_unchanged': 17,
              'all_original_inputs_unchanged': len(baseline), 'pdf_searchable_pages': len(pages),
              'publication_sha256': sha(P / 'publication.json'), 'promotion_sha256': sha(P / 'promotion.json'),
              'submitted_math_executed': False, 'rendered': False, 'deployed': False,
              'shared_files_changed': False, 'existing_evidence_overwritten': False}
    with target.open('x') as stream:
        stream.write(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'checks': len(checks),
                      'source_files_unchanged': 17, 'frozen_inputs_unchanged': len(baseline),
                      'archive_members': count, 'pdf_pages': len(pages)}))


if __name__ == '__main__':
    main()
