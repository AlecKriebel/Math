"""Root's additive custody/adoption checks after full actual editorial reading."""
import datetime
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parents[1]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(p):
    return json.loads(p.read_text())


def check_binding(p, b):
    assert p.stat().st_size == b['bytes'], str(p)
    assert sha(p) == b['sha256'], str(p)


for rid, expected_seal in {
    '23181280': '069f07aba507841b1ae7c10edfce4b1fe8c6f46f772b6f31c58928415017c329',
    '23442760': '68f8df479dede0ea7b65d87fd206ad0d23331f6beb0969afedc1ffd719bb9cde',
    '23395703': '2a1acfdc2968c942cada8bce7a114e623270c4f9f28b72f9610c600a6f4e0101',
}.items():
    d = P / 'papers' / rid
    e = d / 'reviews/editorial'
    assert sha(e / 'SEAL.json') == expected_seal
    seal = read(e / 'SEAL.json')
    manifest = read(e / 'MANIFEST.json')
    assert sha(e / 'MANIFEST.json') == seal['manifest_sha256']
    for path, binding in manifest['owned_output_bindings'].items():
        check_binding(d / path, binding)
    originals = read(e / 'ORIGINAL_BINDINGS_BEFORE.json')['originals']
    for path, binding in originals.items():
        check_binding(Path(path), binding)
    pub, prom = read(d / 'publication.json'), read(d / 'promotion.json')
    s = pub['source_binding']
    root_path = P / prom['root_clearance_file']
    root = read(root_path)
    assert sha(root_path) == prom['root_clearance_sha256'] == seal['root_clearance_sha256']
    assert prom['root_clearance_record'] == root
    for k in ['status', 'disposition_by', 'approved_scope']:
        assert prom[k] == root[k]
    for lane, review in prom['reviews'].items():
        assert review['root_authority_entry'] == root['reviews'][lane]
        assert review['verdict'] == read(d / review['verdict_file'])
        assert sha(d / review['verdict_file']) == review['verdict_sha256']
        assert sha(d / review['report']) == review['sha256']
    receipt = read(d / s['source_receipt_path'])
    assert receipt == s['source_receipt_record'] == prom['source_receipt_record']
    assert sha(d / s['source_receipt_path']) == s['source_receipt_sha256'] == prom['source_receipt_sha256']
    assert receipt[s['source_assets_field']] == s['files'] == prom['source_files']
    transport = read(d / s['transport_receipt_path'])
    assert transport == s['transport_receipt_record'] == prom['transport_receipt_record']
    assert sha(d / s['transport_receipt_path']) == s['transport_receipt_sha256']
    raw = read(d / s['raw_record_path'])
    assert raw['files'] == s['published_file_objects'] == prom['published_file_objects']
    assert sha(d / s['raw_record_path']) == s['raw_record_sha256']
    assert sha(d / s['metadata_path']) == s['metadata_sha256']
    assert raw['metadata']['doi'] == pub['doi']
    assert raw['metadata']['publication_date'] == pub['publication_date']
    assert raw['metadata'].get('version') == pub['version']
    for a in s['files']:
        path = Path(a['path']); b = path.read_bytes()
        assert len(b) == a['bytes'] == a['api_file_object']['size']
        assert hashlib.sha256(b).hexdigest() == a.get('sha256', a.get('SHA256'))
        assert 'md5:' + hashlib.md5(b).hexdigest() == a['api_file_object']['checksum']
        assert a['api_file_object'] in raw['files']
    source = (d / s['source_tex_path']).read_text()
    assert sha(d / s['source_tex_path']) == s['source_tex_sha256']
    assert s['abstract_tex'] in source
    assert (e / 'ORIGINAL_ABSTRACT.tex').read_text() == s['abstract_tex']
    abstract = s['abstract_tex'].replace('~', ' ')
    for a, b in s['abstract_normalization']['exact_presentational_replacements'].items():
        abstract = abstract.replace(a, b)
    assert ' '.join(abstract.split()) == pub['abstract']
    sections = read(e / 'public-sections.json')
    for key, value in sections.items():
        if key != 'publication_config_sha256':
            assert pub[key] == value, key
    assert sections['publication_config_sha256'] == sha(d / 'publication.json')
    assert (e / 'CITATION.bib').read_text() == pub['prepared_bibtex']
    for obj in [pub, prom]:
        assert obj['canonical_url'] is None and obj['follow_up'] is None
    assert prom['AA'] is None
    for k in ['rendered_copy_verified', 'live_verified', 'browser_verified', 'native_verified']:
        assert prom[k] is False
    assert pub['review_metadata']['native_sheet_aa_url'] is None
    if rid == '23395703':
        assert 'version' not in raw['metadata'] and pub['version_field_present'] is False
        assert prom['version'] is None and len(s['files']) == 3
        assert '\n  version =' not in pub['prepared_bibtex']
    else:
        assert sha(d / prom['pending_intake_seal_path']) == prom['pending_intake_seal_sha256'] == seal['pending_intake_seal_sha256']
    result = {
        'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'record_id': rid,
        'status': 'ROOT_EDITORIAL_ACCEPTED_FOR_PRIVATE_STAGE',
        'complete_REPORT_PUBLIC_COPY_SCHEMA_ADAPTER_and_unique_config_prose_metadata_actually_read_by_root': True,
        'exact_editorial_seal_sha256': expected_seal,
        'owned_bindings_rehashed': len(manifest['owned_output_bindings']),
        'original_bindings_rehashed': len(originals),
        'complete_original_source_transport_verdict_root_objects_equal': True,
        'whole_original_abstract_and_prepared_BibTeX_verified': True,
        'version_absence_preserved_when_applicable': True,
        'full_scientific_scope_prior_credit_and_limits_accepted': True,
        'private_staging_authorized': True,
        'production_integration_authorized': False,
        'rendered_live_browser_native_gates_passed': False,
        'AA': None, 'follow_up': None,
        'scientific_repair_or_original_object_rewrite': False,
        'this_editorial_review_completion_percent': 100,
        'overall203_goal_complete': False,
    }
    output = P / 'verification' / f'root-editorial-{rid}-20261025.json'
    assert not output.exists(), str(output)
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(rid, len(manifest['owned_output_bindings']), len(originals), sha(output))
