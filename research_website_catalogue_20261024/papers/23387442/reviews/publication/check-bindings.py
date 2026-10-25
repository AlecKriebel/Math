"""Read-only source/editorial binding checks; no rendering or submitted math run."""
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


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_abstract(body):
    body = body.replace('$', '').replace(r'\SL', 'SL').replace(r'\C', 'ℂ')
    body = body.replace(r'\setminus', ' ' + chr(92) + ' ').replace(r'\geq', '≥')
    return ' '.join(body.replace("Satoh's", 'Satoh’s').split())


def main():
    checks = []

    def require(name, condition):
        if not condition:
            raise RuntimeError(name)
        checks.append({'name': name, 'valid': True})

    c = json.loads((P / 'publication.json').read_text())
    g = json.loads((P / 'promotion.json').read_text())
    rec = json.loads((S / 'record.json').read_text())
    receipt = json.loads((S / 'receipt.json').read_text())
    cp = B / g['root_clearance_file']
    clearance = json.loads(cp.read_text())
    require('exact_authoritative_root_clearance', sha(cp) == g['root_clearance_sha256'] == '1a100a1722debd437303b74a81585a97cce3defca16923179af9fc5b912ede1f')
    require('root_disposition_not_editor_scientific_verdict', clearance == g['root_clearance_record'] and clearance['status'] == g['status'] == 'PASS' and clearance['disposition_by'] == g['disposition_by'] == 'root' and g['approved_scope'] == clearance['approved_scope'])
    require('publication_and_receipt_hashes', g['publication_sha256'] == sha(P / 'publication.json') and g['source_receipt_sha256'] == sha(S / 'receipt.json') == clearance['source_receipt_sha256'])
    require('metadata_record_hash', receipt['record_sha256'] == sha(S / 'record.json') == c['source_binding']['record_sha256'])
    require('exact_metadata', all(c[k] == rec['metadata'][k] for k in ['title', 'publication_date', 'version', 'doi']))
    require('author_orcid', c['author'] == 'Alec Kriebel' and c['orcid'] == 'https://orcid.org/0009-0001-9320-500X')
    require('printed_date_and_metadata_only_version', c['publication_date'] == '2026-10-15' and c['version'] == c['source_binding']['zenodo_version'] == '1.0' and c['source_binding']['manuscript_version'] is None and c['edition_label'] == c['citation_edition_label'] == 'Zenodo version 1.0' and c['publication_date_label'] == 'Manuscript dated')
    require('record_creation_separate', rec['created'] == c['source_binding']['record_created_utc'] == '2026-10-15T07:50:10.998117+00:00' and 'does not print a version number' in c['edition_note'])
    require('two_public_assets_standard_supplement', len(receipt['files']) == 2 and c['supplement_filename'] == 'satoh_filtration_verification.zip' and c['additional_assets'] == [] and c['source_binding']['embedded_assets'] == [] and {x['name'] for x in receipt['files']} == {c['pdf_filename'], c['supplement_filename']})
    require('all_source_asset_records_exact', c['source_binding']['files'] == g['source_files'] == receipt['files'])
    for asset in receipt['files']:
        path = S / asset['name']
        require('public_asset_' + asset['name'], path.stat().st_size == asset['bytes'] and sha(path) == asset['sha256'] and hashlib.md5(path.read_bytes()).hexdigest() == asset['md5'])
    require('pdf_zip_gate_bindings', g['pdf_sha256'] == clearance['pdf_sha256'] == c['source_binding']['pdf_sha256'] == sha(S / c['pdf_filename']) and g['supplement_sha256'] == c['source_binding']['supplement_sha256'] == sha(S / c['supplement_filename']))
    members = []
    with zipfile.ZipFile(S / c['supplement_filename']) as archive:
        require('archive_crc', archive.testzip() is None)
        for info in archive.infolist():
            if info.is_dir():
                continue
            data = archive.read(info)
            path = S / 'published-source/satoh_filtration_verification' / info.filename
            if path.read_bytes() != data:
                raise RuntimeError('Extracted member changed: ' + info.filename)
            members.append({'member': info.filename, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    require('all_107_members_unchanged', len(members) == 107)
    require('sole_embedded_reader_identical', sha(S / 'published-source/satoh_filtration_verification/satoh_filtration_counterexamples.pdf') == sha(S / c['pdf_filename']) and c['pdf_pages'] == 4)
    tp = P / c['source_binding']['source_tex_path']
    source = tp.read_text()
    raw = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', source, re.S).group(1).strip()
    require('actual_source_tex_binding', sha(tp) == c['source_binding']['source_tex_sha256'] == c['source_binding']['abstract_source_sha256'] and c['source_binding']['abstract_source'] == str(tp.relative_to(P)))
    require('complete_original_abstract_exact', normalized_abstract(raw) == c['abstract'] == json.loads((P / 'reviews/scope/candidate.json').read_text())['abstract'] == json.loads((O / 'candidate.json').read_text())['abstract'])
    require('abstract_five_sentences_one_paragraph', len(re.findall(r'\.(?:\s|$)', c['abstract'])) == 5 and '\n\n' not in c['abstract'] and c['source_binding']['abstract_word_count'] == len(c['abstract'].split()) == 104)
    require('printed_manuscript_date', r'\date{15 October 2026}' in source)
    require('exact_three_review_objects', set(g['reviews']) == {'scope', 'analytic', 'adversarial'})
    for role, item in g['reviews'].items():
        require('original_review_' + role, sha(P / item['report']) == item['sha256'] == clearance['reviews'][role]['report_sha256'] and sha(P / item['verdict_file']) == item['verdict_sha256'] == clearance['reviews'][role]['verdict_sha256'] and json.loads((P / item['verdict_file']).read_text()) == item['verdict'])
    sv = g['reviews']['scope']['verdict']
    require('scope_pending_chronology_retained', sv['status'] == 'SCOPE_COMPLETE_MATHEMATICAL_REVIEW_PENDING' and sv['mathematical_verdict'] is None and sv['publication_authorized'] is False and g['reviews']['scope']['root_disposition'] == 'SCOPE_COMPLETE' and g['scope_gate_resolution'] == clearance['scope_gate_resolution'])
    result = '\n'.join(c['result'])
    require('whole_quotient_and_integral_model', all(x in result for x in ['integral lower central series', 'entire J/J^{k+1}', 'rational algebra of SL(2,ℂ) matrix-entry functions']))
    require('literal_degree_five_family', 'w=[[[x₁,x₂],[x₁,x₃]],x₁]' in result and 'n≥4' in result and 'x₄↦x₄w' in result and 'D_n(5) but not A_n(5)' in result)
    require('literal_degree_six_family', 'v=[[[x₁,x₂],[x₁,[x₁,x₂]]],x₁]' in result and 'n≥3' in result and 'x₃↦x₃v' in result and 'D_n(6) but not A_n(6)' in result)
    require('classical_credit_and_versioned_background', all(x in json.dumps(c['background'], ensure_ascii=False) for x in ['Razmyslov', 'through Burde', '1607.05411v2', '1411.0950v2', '2021', 'final journal text was not inspected']))
    limitations = '\n'.join(c['limitations'])
    require('scope_exclusions_explicit', all(x in limitations for x in ['degree-five counterexample at rank three', 'failure in every degree', 'larger matrix sizes', 'trace algebra', 'lower central series of IA_n', 'historical firstness']))
    public_copy = '\n'.join([c['title'], c['description'], c['abstract'], *c['plain_language'], *c['result'], *c['why_it_works'], *c['limitations'], c['ai_disclosure'], c['collaboration'], c['edition_note'], *[x['note'] for x in c['background']]])
    require('no_public_internal_counts_or_replay_story', not re.search(r'489|4,502|4502|62 two|21 check|replay|root-clearance|SHA-?256', public_copy, re.I))
    require('ai_unrefereed_human_review_distinction', 'unrefereed' in c['status'].lower() and 'AI' in c['ai_disclosure'] and 'do not constitute independent human peer review' in c['ai_disclosure'])
    require('followup_null_and_passive_collaboration', c['follow_up'] is g['follow_up'] is clearance['follow_up'] is None and 'actual research contributions' in c['collaboration'])
    require('canonical_slug', re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', c['slug']) is not None and c['canonical_url'] == 'https://aleckriebel.com/research/' + c['slug'] + '/')
    require('descriptive_metadata', 90 <= len(c['description']) <= 170)
    required = {'title', 'slug', 'description', 'abstract', 'plain_language', 'result', 'why_it_works', 'limitations', 'background', 'collaboration', 'publication_date', 'version', 'doi', 'author', 'pdf_filename', 'supplement_filename'}
    require('existing_renderer_fields', required <= set(c) and all(isinstance(c[k], list) and c[k] for k in ['plain_language', 'result', 'why_it_works', 'limitations', 'background']))
    require('no_render_or_deployment_claim', c['review_metadata']['rendered'] is False and c['review_metadata']['deployed'] is False and g['preparation_state'] == 'BINDINGS_READY_RENDERING_PENDING')
    output = {'checked_utc': datetime.now(timezone.utc).isoformat(), 'record_id': '23387442', 'status': 'EDITORIAL_BINDINGS_VALID_RENDER_PENDING', 'checks': checks, 'check_count': len(checks), 'source_members_verified': len(members), 'public_assets_verified': 2, 'submitted_math_executed': False, 'rendered': False, 'shared_files_changed': False, 'deployed': False, 'publication_sha256': sha(P / 'publication.json'), 'promotion_sha256': sha(P / 'promotion.json'), 'root_clearance_sha256': sha(cp), 'remaining_gates': ['Register exact source/abstract/model checks in the shared checker.', 'Root renders and inspects actual public copy.', 'Root completes live HTTP/browser/download and native tracker gates.']}
    (O / 'editorial-checks.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': output['status'], 'checks': len(checks), 'public_assets': 2, 'unchanged_members': len(members), 'rendered': False}))


if __name__ == '__main__':
    main()
