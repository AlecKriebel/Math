"""Read-only editorial/source checks; no submitted mathematics or rendering."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import sys
import zipfile

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parents[2]
B = P.parents[1]
O = P / 'reviews/publication'
S = P / 'sources'
sys.path.insert(0, str(B / 'scripts'))
from published_assets import normalized_receipt_view, PublishedAssets


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def normalized_abstract(body):
    return ' '.join(body.split()).replace('$L^2$', 'L²').replace('$L^\\infty$', 'L∞').replace('$L^1$', 'L¹').replace('$\\{0\\}$', '{0}').replace('$o(\\norm{u}_{L^2}^2)$', 'o(‖u‖²L²)')


def main():
    checks = []

    def need(name, condition):
        if not condition:
            raise RuntimeError(name)
        checks.append({'name': name, 'valid': True})

    c = json.loads((P / 'publication.json').read_text())
    g = json.loads((P / 'promotion.json').read_text())
    rec = json.loads((S / 'record.json').read_text())
    raw = json.loads((S / 'receipt.json').read_text())
    receipt = normalized_receipt_view(raw)
    cp = B / g['root_clearance_file']
    clear = json.loads(cp.read_text())
    need('FINAL_root_authority_only', sha(cp) == g['root_clearance_sha256'] == '7ecd074783bbf82d6a7a6f31074cd6c6e0bf22fa9180400cc96949c259a5b8cf' and cp.name == 'root-clearance-23358014-20261025.json')
    need('root_decision_exact_not_new_scientific_verdict', clear == g['root_clearance_record'] and g['approved_scope'] == clear['approved_scope'] and g['status'] == clear['status'] == 'PASS' and g['disposition_by'] == clear['disposition_by'] == 'root')
    need('publication_receipt_binding', g['publication_sha256'] == sha(P / 'publication.json') and g['source_receipt_sha256'] == sha(S / 'receipt.json') == clear['source_receipt_sha256'])
    need('raw_assets_receipt_unchanged', 'assets' in raw and 'files' not in raw and receipt['files'] == raw['assets'] == c['source_binding']['files'] == g['source_files'])
    need('record_metadata_hash', sha(S / 'record.json') == raw['record_sha256'] == c['source_binding']['record_sha256'])
    need('title_date_version_doi', all(c[k] == rec['metadata'][k] for k in ['title', 'publication_date', 'version', 'doi']))
    need('author_orcid', c['author'] == 'Alec Kriebel' and c['orcid'] == 'https://orcid.org/0009-0001-9320-500X')
    need('printed_and_metadata_edition', c['version'] == c['source_binding']['manuscript_version'] == c['source_binding']['zenodo_version'] == '1.0' and c['publication_date'] == '2026-10-14' and c['edition_label'] == 'Version 1.0' and c['publication_date_label'] == 'Manuscript dated')
    need('creation_not_priority', rec['created'] == c['source_binding']['record_created_utc'] == '2026-10-14T05:39:12.680683+00:00' and 'do not establish first priority' in c['edition_note'])
    need('two_standard_public_assets', len(receipt['files']) == 2 and c['pdf_filename'] == 'critical_wave_growth.pdf' and c['supplement_filename'] == 'critical_wave_verification.zip' and c['additional_assets'] == [] and c['source_binding']['embedded_assets'] == [] and {a['name'] for a in receipt['files']} == {c['pdf_filename'], c['supplement_filename']})
    resolver = PublishedAssets(S, raw)
    for asset in receipt['files']:
        data = resolver.resolve(asset['name']).read_bytes()
        need('asset_' + asset['name'], len(data) == asset['bytes'] and hashlib.md5(data).hexdigest() == asset['md5'])
    need('pdf_zip_gate_hashes', sha(S / c['pdf_filename']) == g['pdf_sha256'] == clear['pdf_sha256'] == c['source_binding']['pdf_sha256'] and sha(S / c['supplement_filename']) == g['supplement_sha256'] == c['source_binding']['supplement_sha256'])
    count = 0
    with zipfile.ZipFile(S / c['supplement_filename']) as z:
        need('zip_crc', z.testzip() is None)
        for item in z.infolist():
            if item.is_dir():
                continue
            data = z.read(item)
            f = S / 'published-source/critical_wave_verification' / item.filename
            if f.read_bytes() != data:
                raise RuntimeError('Changed member: ' + item.filename)
            if data.startswith((b'%PDF', b'PK\x03\x04', b'\x1f\x8b')):
                raise RuntimeError('Unexpected reader/archive member: ' + item.filename)
            count += 1
    need('113_members_one_six_page_reader', count == 113 and c['pdf_pages'] == 6 and c['source_binding']['unique_reader_pdf_count'] == 1 and c['source_binding']['archive_embedded_pdf_count'] == 0)
    baseline = json.loads((O / 'source-baseline.json').read_text())['files']
    need('118_original_source_files_unchanged', len(baseline) == 118 and all(sha(P / rel) == h for rel, h in baseline.items()))
    tp = P / c['source_binding']['source_tex_path']
    tex = tp.read_text()
    at = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1).strip()
    need('actual_tex_and_full_abstract', sha(tp) == c['source_binding']['source_tex_sha256'] == c['source_binding']['abstract_source_sha256'] and normalized_abstract(at) == c['abstract'] == json.loads((P / 'reviews/scope/content.json').read_text())['abstract'] == json.loads((O / 'source-content.json').read_text())['abstract'])
    need('abstract_no_excerpt', len(c['abstract'].split()) == c['source_binding']['abstract_word_count'] == 116 and len(re.findall(r'\.(?:\s|$)', c['abstract'])) == 6 and '\n\n' not in c['abstract'])
    need('printed_date_version', r'\date{October 14, 2026 \quad (version 1.0)}' in tex)
    need('all_three_original_reviews', set(g['reviews']) == {'analytic', 'adversarial', 'scope'})
    for role, v in g['reviews'].items():
        need('original_' + role, sha(P / v['report']) == v['sha256'] == clear['reviews'][role]['report_sha256'] and sha(P / v['verdict_file']) == v['verdict_sha256'] == clear['reviews'][role]['verdict_sha256'] and json.loads((P / v['verdict_file']).read_text()) == v['verdict'])
    sv = g['reviews']['scope']['verdict']
    need('custom_scope_pending_chronology', sv['status'] == 'SCOPE_COMPLETE_PENDING_MATHEMATICAL_REVIEW' and sv['mathematical_pass'] is False and sv['promotion_authorized'] is False and g['reviews']['scope']['root_disposition'] == 'SCOPE_COMPLETE' and g['scope_gate_resolution'] == clear['scope_gate_resolution'])
    result = '\n'.join(c['result'])
    need('exact_nonlinear_model', all(x in result for x in ['real defocusing quintic', 'three-dimensional unit ball', 'zero position and velocity', 'Dirichlet', 'final time 1', 'L²(0,1;H)', '0<ρ≤ρ*', 'fixed finite ν≥0']))
    need('retained_costs_only_beta2_removed', all(x in result for x in ['one half of the squared terminal-position', 'one quarter of the fourth power', 'γ=β₁=1', 'β₂=0', 'ν‖yₜ(1)‖²H⁻¹(B)/2']))
    need('global_actual_optimizer_and_vacuity', all(x in result for x in ['unique global optimizer over all admissible controls', 'Δ(u)≥A³/(12ρ²)', 'critical cone is {0}', 'condition is vacuous']))
    need('actual_nonlinear_pulses_both_neighborhoods', all(x in result for x in ['actual nonlinear feasible pulses', '2h³', '(π²/3+2/π²)h⁴+O(h⁶)', 'both L² and L∞ neighborhoods']))
    need('every_optimizer_radial_divergence', all(x in result for x in ['every terminal target d∈H', 'every choice of global optimizers', 'positive values', '‖uε‖L²/ε→∞']))
    need('weaker_L1_growth_all_feasible', all(x in result for x in ['Δ(u)≥‖u‖²L¹/(4π²)', 'every admissible control', 'sufficiently small L¹ norm']))
    need('arbitrary_target_every_optimizer_fixed_basepoint', all(x in result for x in ['arbitrary nearby target πe+w', 'ε=‖w‖H', 'Every global optimizer', 'fixed zero optimizer', 'O(ε)', 'O(√ε)']))
    need('nu_uniform_upper_dependent_lower_neighborhood', all(x in result for x in ['upper-bound neighborhood', 'uniformly over all finite ν≥0', 'lower-comparison neighborhood may depend on the fixed ν', 'Θ(ε)', 'cε³ᐟ⁴', 'C√ε']))
    limits = '\n'.join(c['limitations'])
    need('Hilbert_cap_not_space_time_cap', all(x in limits for x in ['pointwise in time on the spatial L² norm', 'not a pointwise bound on |u(t,x)|', 'time norms with values in L²(B)']))
    need('linear_projection_not_invariant_nonlinear_span', 'does not assume that the nonlinear solution stays in one eigenmode' in '\n'.join(c['why_it_works']))
    need('no_forbidden_stability_claim', all(x in limits for x in ['perturbed-optimizer uniqueness', 'pairwise Lipschitz selection', 'L∞ convergence of perturbed optimizers', 'sharp exponent']))
    need('zero_target_growth_countercase', all(x in limits for x in ['target d=0', 'J0,ν(u)≥‖u‖L¹≥‖u‖²L²/ρ', 'does not assert failure for all targets or all control caps']))
    need('unchanged_implication_only', 'does not rule out adapted sufficient conditions' in limits and 'unchanged' in limits)
    bg = json.dumps(c['background'], ensure_ascii=False)
    need('author_preprint_and_classical_credit', all(x in bg for x in ['1907.02744v1', 'final body was not inspected', 'Dunn', '438–440', 'Strichartz', 'subgradient', 'nondegeneracy']))
    public = '\n'.join([c['title'], c['description'], c['abstract'], *c['plain_language'], *c['result'], *c['why_it_works'], *c['limitations'], c['ai_disclosure'], c['collaboration'], *[x['note'] for x in c['background']]])
    need('no_public_internal_counts_or_replay_story', re.search(r'13,201|13201|6,561|6561|3,937|3937|5,575|5575|root-clearance|SHA-?256|replay', public, re.I) is None)
    need('AI_unrefereed_no_certification', 'unrefereed' in c['status'].lower() and 'extensively' in c['ai_disclosure'] and 'not external human peer review or proof-assistant certification' in c['ai_disclosure'])
    need('followup_null_passive_authorship', c['follow_up'] is g['follow_up'] is clear['follow_up'] is None and 'actual research contributions' in c['collaboration'])
    need('canonical_SEO', c['canonical_url'] == 'https://aleckriebel.com/research/' + c['slug'] + '/' and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', c['slug']) is not None and 90 <= len(c['description']) <= 170)
    need('existing_renderer_fields', all(k in c for k in ['title', 'slug', 'description', 'abstract', 'plain_language', 'result', 'why_it_works', 'limitations', 'background', 'collaboration', 'publication_date', 'version', 'doi', 'author', 'pdf_filename', 'supplement_filename']))
    need('render_and_publication_pending', c['review_metadata']['rendered'] is False and c['review_metadata']['deployed'] is False and g['preparation_state'] == 'BINDINGS_READY_RENDERING_PENDING')
    out = {'checked_utc': datetime.now(timezone.utc).isoformat(), 'record_id': '23358014', 'status': 'EDITORIAL_BINDINGS_VALID_RENDER_PENDING', 'checks': checks, 'check_count': len(checks), 'public_assets_verified': 2, 'archive_members_verified': count, 'original_source_files_unchanged': len(baseline), 'raw_assets_receipt_preserved': True, 'publication_sha256': sha(P / 'publication.json'), 'promotion_sha256': sha(P / 'promotion.json'), 'submitted_math_executed': False, 'rendered': False, 'deployed': False, 'shared_files_changed': False}
    (O / 'editorial-checks.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': out['status'], 'checks': len(checks), 'assets': 2, 'members': count, 'source_files': len(baseline)}))


if __name__ == '__main__':
    main()
