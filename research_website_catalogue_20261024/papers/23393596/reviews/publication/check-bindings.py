"""Read-only editorial/source checks; no rendering or submitted math execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import zipfile

P = Path(__file__).resolve().parents[2]
B = P.parents[1]
O = P / 'reviews/publication'
S = P / 'sources'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def normalized_abstract(body):
    for old, new in [('$', ''), (r'\geq', '≥'), (r'\not\subset', '⊄'), (r'\F', 'F'), ('--', '–')]:
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
    receipt = json.loads((S / 'receipt.json').read_text())
    cp = B / g['root_clearance_file']
    clear = json.loads(cp.read_text())
    need('exact_root_authority', sha(cp) == g['root_clearance_sha256'] == '36b0ccc972b713e507c5ea5a60f86f332fc0668fb9805e8e523d755c6643a871')
    need('root_scientific_decision_preserved', clear == g['root_clearance_record'] and g['status'] == clear['status'] == 'PASS' and g['disposition_by'] == clear['disposition_by'] == 'root' and g['approved_scope'] == clear['approved_scope'])
    need('publication_receipt_bindings', sha(P / 'publication.json') == g['publication_sha256'] and sha(S / 'receipt.json') == g['source_receipt_sha256'] == clear['source_receipt_sha256'])
    need('record_hash', sha(S / 'record.json') == receipt['record_sha256'] == c['source_binding']['record_sha256'])
    need('exact_title_date_version_doi', all(c[k] == rec['metadata'][k] for k in ['title', 'publication_date', 'version', 'doi']))
    need('author_orcid', c['author'] == 'Alec Kriebel' and c['orcid'] == 'https://orcid.org/0009-0001-9320-500X')
    need('printed_and_metadata_version', c['version'] == c['source_binding']['manuscript_version'] == c['source_binding']['zenodo_version'] == '1.0' and c['publication_date'] == '2026-10-15' and c['edition_label'] == 'Version 1.0' and c['publication_date_label'] == 'Manuscript dated')
    need('separate_record_creation', rec['created'] == c['source_binding']['record_created_utc'] == '2026-10-15T11:19:16.531335+00:00' and 'do not establish first priority' in c['edition_note'])
    need('two_assets_one_standard_supplement', len(receipt['files']) == 2 and c['supplement_filename'] == 'deep-derived-pure-braids-source-verification-v1.0.zip' and c['additional_assets'] == [] and c['source_binding']['embedded_assets'] == [] and {a['name'] for a in receipt['files']} == {c['pdf_filename'], c['supplement_filename']})
    need('asset_records_exact', g['source_files'] == c['source_binding']['files'] == receipt['files'])
    for a in receipt['files']:
        f = S / a['name']
        need('asset_' + a['name'], f.stat().st_size == a['bytes'] and sha(f) == a['sha256'] and hashlib.md5(f.read_bytes()).hexdigest() == a['md5'])
    need('pdf_zip_root_and_config_hashes', g['pdf_sha256'] == clear['pdf_sha256'] == c['source_binding']['pdf_sha256'] == sha(S / c['pdf_filename']) and g['supplement_sha256'] == c['source_binding']['supplement_sha256'] == sha(S / c['supplement_filename']))
    count = 0
    with zipfile.ZipFile(S / c['supplement_filename']) as z:
        need('zip_crc', z.testzip() is None)
        for i in z.infolist():
            if i.is_dir():
                continue
            f = S / 'published-source/deep-derived-pure-braids-source-verification-v1.0' / i.filename
            if f.read_bytes() != z.read(i):
                raise RuntimeError('Changed member: ' + i.filename)
            count += 1
    need('all_213_members_equal', count == 213)
    baseline = json.loads((O / 'source-baseline.json').read_text())['files']
    need('all_218_original_source_files_unchanged', len(baseline) == 218 and all(sha(P / rel) == h for rel, h in baseline.items()))
    need('embedded_reader_is_duplicate', sha(S / 'published-source/deep-derived-pure-braids-source-verification-v1.0/note.pdf') == sha(S / c['pdf_filename']) and c['pdf_pages'] == 4)
    tp = P / c['source_binding']['source_tex_path']
    tex = tp.read_text()
    raw = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1).strip()
    need('actual_tex_hash', sha(tp) == c['source_binding']['source_tex_sha256'] == c['source_binding']['abstract_source_sha256'])
    need('full_original_abstract', normalized_abstract(raw) == c['abstract'] == json.loads((P / 'reviews/scope/candidate.json').read_text())['abstract'] == json.loads((O / 'candidate.json').read_text())['abstract'])
    need('abstract_count_and_paragraph', len(c['abstract'].split()) == c['source_binding']['abstract_word_count'] == 81 and len(re.findall(r'\.(?:\s|$)', c['abstract'])) == 5 and '\n\n' not in c['abstract'])
    need('printed_version_date', r'\date{October 15, 2026\quad (version 1.0)}' in tex)
    need('three_review_objects', set(g['reviews']) == {'analytic', 'adversarial', 'scope'})
    for role, v in g['reviews'].items():
        need('original_review_' + role, sha(P / v['report']) == v['sha256'] == clear['reviews'][role]['report_sha256'] and sha(P / v['verdict_file']) == v['verdict_sha256'] == clear['reviews'][role]['verdict_sha256'] and json.loads((P / v['verdict_file']).read_text()) == v['verdict'])
    sv = g['reviews']['scope']['verdict']
    need('pending_scope_chronology', sv['status'] == 'SCOPE_COMPLETE_MATHEMATICAL_REVIEW_PENDING' and sv['publication_authorized'] is False and sv['mathematical_verdict'] is None and g['reviews']['scope']['root_disposition'] == 'SCOPE_COMPLETE' and g['scope_gate_resolution'] == clear['scope_gate_resolution'])
    result = '\n'.join(c['result'])
    need('all_rank_finite_depth_model', all(x in result for x in ['classical disk pure braid group', 'P_m^(k+1)=[P_m^(k),P_m^(k)]', 'every m≥3 and every finite integer k≥1', 'standard oriented closure', 'integrally smoothly 1-solvable', 'Otto Definition 2.3']))
    need('corollary_positive_n_only', 'P_m^(n+2)⊄F_n^m for every m≥3 and integer n≥1' in result and 'prior n=0 containment' in '\n'.join(c['limitations']))
    need('literal_finite_witness', all(x in result for x in ['a=σ₁²', 'b=σ₂²', 'c=[a,b]', 'd=a⁻¹ca', 'e=b⁻¹cb', 'u=[c,d]', 'v=[d,e]', 'β=[u,v]', '104-letter freely reduced Artin word', 'signature −2']))
    limits = '\n'.join(c['limitations'])
    need('witness_depends_on_depth_no_intersection', all(x in limits for x in ['may depend on the finite depth k', 'No single braid in the intersection', 'only for k=3', 'No minimal crossing number']))
    need('excluded_model_extensions', all(x in limits for x in ['power subgroups', 'lower central series', 'rational derived series', 'surface braid groups', 'rational solvability', 'topological solvability']))
    proof = '\n'.join(c['why_it_works'])
    need('signature_homogenization_power_distinction', all(x in proof for x in ['ordinary signature s', 'homogenization q', 'P₃ is not a homomorphism', 'positive power is essential', 'nonzero q', 'same braid']))
    need('bounded_erle_qualification', all(x in limits for x in ['separate explicit example', 'printed index discrepancy', 'crossing geometry', 'Burau–Meyer', 'arbitrary-depth existence proof is independent']))
    background = json.dumps(c['background'], ensure_ascii=False)
    need('primary_question_classical_credit', all(x in background for x in ['Question 3', '3021', '2017/50', 'published in 2018', 'Gambaudo', 'Calegari', 'Lemma 7.12', 'Definition 2.3', '(4.21)']))
    need('no_firstness_current_openness_claim', 'No historical firstness' in limits and 'continued worldwide openness' in limits)
    public = '\n'.join([c['title'], c['description'], c['abstract'], *c['plain_language'], *c['result'], *c['why_it_works'], *c['limitations'], c['ai_disclosure'], c['collaboration'], *[x['note'] for x in c['background']]])
    need('private_replay_narratives_absent', re.search(r'3,603|3603|286 additional|44-file|proof-search response|root-clearance|SHA-?256|replay', public, re.I) is None)
    need('ai_unrefereed_status', 'unrefereed' in c['status'].lower() and 'extensively' in c['ai_disclosure'] and 'do not constitute independent human or journal peer review' in c['ai_disclosure'])
    need('followup_null_passive_collaboration', c['follow_up'] is g['follow_up'] is clear['follow_up'] is None and 'actual research contributions' in c['collaboration'])
    need('canonical_description', c['canonical_url'] == 'https://aleckriebel.com/research/' + c['slug'] + '/' and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', c['slug']) is not None and 90 <= len(c['description']) <= 170)
    need('existing_renderer_fields', all(k in c for k in ['title', 'slug', 'description', 'abstract', 'plain_language', 'result', 'why_it_works', 'limitations', 'background', 'collaboration', 'publication_date', 'version', 'doi', 'author', 'pdf_filename', 'supplement_filename']))
    need('actual_page_not_approved_or_rendered', c['review_metadata']['rendered'] is False and c['review_metadata']['deployed'] is False and g['preparation_state'] == 'BINDINGS_READY_RENDERING_PENDING')
    out = {'checked_utc': datetime.now(timezone.utc).isoformat(), 'record_id': '23393596', 'status': 'EDITORIAL_BINDINGS_VALID_RENDER_PENDING', 'checks': checks, 'check_count': len(checks), 'public_assets_verified': 2, 'archive_members_verified': count, 'original_source_files_unchanged': len(baseline), 'publication_sha256': sha(P / 'publication.json'), 'promotion_sha256': sha(P / 'promotion.json'), 'submitted_math_executed': False, 'rendered': False, 'deployed': False, 'shared_files_changed': False}
    (O / 'editorial-checks.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': out['status'], 'checks': len(checks), 'public_assets': 2, 'archive_members': count, 'original_source_files': len(baseline)}))


if __name__ == '__main__':
    main()
