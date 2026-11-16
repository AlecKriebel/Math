#!/usr/bin/env python3
"""One fixed, stdout-only editorial data comparison; no science or helper imports."""
from pathlib import Path
from html import unescape
import hashlib
import json
import re

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
N = P / 'verification/habiro-rank-editorial-fact-sol-20261116'
W = P / 'papers/23425412/reviews/editorial'
S = P / 'papers/23425412/sources'


def pin(data):
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest()}


def load(path):
    return json.loads(path.read_bytes())


def fixed(path, size, digest):
    data = path.read_bytes()
    assert pin(data) == {'bytes': size, 'SHA256': digest}, str(path)
    return data


def normal(text):
    text = unescape(re.sub(r'<[^>]+>', '', text)).replace('−', '-').replace('’', "'")
    return re.sub(r'\s*,\s*', ',', re.sub(r'\s+', ' ', text).strip())


def main():
    final = json.loads(fixed(W/'FINAL.json', 1642, '4082b143d2d2623fbbeed4952587e82b0883c566f1eebad395971a1fdee141e4'))
    manifest = json.loads(fixed(W/'OWNED_MANIFEST.json', 4942, 'e82bd30d028012ca7f8b21523ab6ba553dbd13c056fac84771f135203a4dbbf8'))
    payload = {x['path']: x for x in manifest['files']}
    assert {str(q.relative_to(W)) for q in W.rglob('*') if q.is_file()} == set(payload)|{'FINAL.json', 'OWNED_MANIFEST.json'}
    assert ['.']+sorted(str(q.relative_to(W)) for q in W.rglob('*') if q.is_dir()) == manifest['directories']
    assert len(payload)+2 == final['actual_files'] == 31
    for name, row in payload.items():
        q = W/name
        assert not q.is_symlink() and pin(q.read_bytes()) == {k: row[k] for k in ('bytes', 'SHA256')}, name
    for line in (N/'INITIAL_MANIFEST.txt').read_text().splitlines():
        digest, name = line.split('  ', 1)
        assert hashlib.sha256((N/name).read_bytes()).hexdigest() == digest, name
    inputs = load(N/'SOURCE_INPUTS.json')
    acquired = load(S/'ACQUIRED.json')['records'][0]
    record = load(Path(acquired['record_body_path']))
    model = load(W/'PAGE_MODEL.json')
    assert model['native_metadata'] == record['metadata']
    assert model['native_record_files'] == record['files']
    assert model['native_files_response'] == load(Path(acquired['files_endpoint_body_path']))
    assert model['native_created'] == record['created'] and model['native_updated'] == record['updated']
    assert model['native_modified'] == record['modified'] and model['native_record_status'] == record['status']
    assert model['native_is_published'] == {'present': 'is_published' in record, 'original_value': record.get('is_published')}
    for key in ('canonical_url', 'base_url', 'production_url', 'AA', 'follow_up'):
        assert model[key] is None
    assert model['publication_authority'] is False and model['private_noindex'] is True
    assert model['rights']['native_authored_work_including_code'] == 'CC-BY-4.0'
    authority = fixed(P/'verification/root-clearance-23425412-20261116.json', 2319, 'e59886b63d3b77fad6aebc56701b88b94e220ec6ba614d5a8fa40d9b8338505f')
    assert {k: model['authority_reference'][k] for k in ('bytes', 'SHA256')} == pin(authority)
    page = (W/'preview/index.html').read_bytes()
    html = page.decode()
    mains = re.findall(r'<main id="main">[\s\S]*?</main>', html)
    heads = re.findall(r'<head>[\s\S]*?</head>', html)
    assert len(mains) == len(heads) == 1
    for key, data in [('whole_MAIN', mains[0].encode()), ('whole_head', heads[0].encode()), ('whole_page', page)]:
        assert pin(data) == model[key] == final[key], key
    assert pin((W/'PAGE_MODEL.json').read_bytes()) == final['page_model']
    assert pin((W/'preview/citation.bib').read_bytes()) == final['BibTeX']
    assert '<meta name="robots" content="noindex, nofollow, noarchive">' in heads[0]
    assert not re.search(r'<link[^>]+rel=["\']canonical["\']', heads[0])
    ld = json.loads(re.search(r'<script type="application/ld\+json">\s*([\s\S]*?)\s*</script>', heads[0])[1])
    assert ld['name'] == record['metadata']['title'] and ld['datePublished'] == '2026-10-16' and ld['version'] == '1.0'
    assert ld['author']['name'] == 'Alec Kriebel' and ld['author']['identifier'] == 'https://orcid.org/0009-0001-9320-500X'
    assert ld['license'] == 'https://creativecommons.org/licenses/by/4.0/' and ld['creativeWorkStatus'] == 'Unrefereed preprint'
    expected_abstract = re.search(r'^> (.+)$', (N/'INITIAL.md').read_text(), re.M)[1]
    actual_abstract = re.search(r'<section id="original-abstract"[\s\S]*?<p>([\s\S]*?)</p>', html)[1]
    assert normal(actual_abstract) == normal(expected_abstract)
    description = re.search(r'<div id="native-description">([\s\S]*?)</div>', html)[1]
    assert description == record['metadata']['description'] == acquired['description_whole_field']['original_value']
    paragraphs = re.findall(r'<p>([\s\S]*?)</p>', description)
    assert len(paragraphs) == len(set(paragraphs)) == 4
    order = [x['key'] for x in record['files']]
    download_list = re.search(r'<ol id="native-downloads">([\s\S]*?)</ol>', html)[1]
    assert re.findall(r'<a href="([^"]+)" download>', download_list) == order
    assert [x['name'] for x in ld['encoding']] == order
    for item in acquired['all_native_assets_in_original_order']:
        source = Path(item['path']).read_bytes()
        local = (W/'preview'/item['key']).read_bytes()
        assert local == source and pin(local) == {k: item[k] for k in ('bytes', 'SHA256')}
        assert hashlib.md5(local).hexdigest() == item['original_API_file_object']['checksum'][4:]
    assert 'src="habiro-rank-interpolation-v1.0.pdf#view=FitH"' in html
    bib = (W/'preview/citation.bib').read_text()
    for value in ['author = {Kriebel, Alec}', 'title = {'+record['metadata']['title']+'}', 'doi = {10.5281/zenodo.23425412}', 'version = {1.0}', 'license = {CC-BY-4.0}', 'Published 16 October 2026. Unrefereed.']:
        assert value in bib, value
    receipt = load(W/'RENDER_RECEIPT.json')
    for name, expected in receipt['inputs'].items():
        assert pin((W/name).read_bytes()) == expected
    assert receipt['remote_page_requests'] == receipt['page_errors'] == []
    images = sorted(x for x in payload if x.startswith('renders/'))
    assert len(images) == 6 and all((W/x).read_bytes().startswith(b'\x89PNG\r\n\x1a\n') for x in images)
    print(json.dumps({'status': 'PASS_FIXED_EDITORIAL_DATA_COMPARISON', 'writer_files': 31,
                      'writer_child_directories': 3, 'whole_MAIN': model['whole_MAIN'], 'whole_head': model['whole_head'],
                      'whole_page': model['whole_page'], 'full_abstract_match': True,
                      'native_Description_exact_distinct_paragraphs': [pin(x.encode()) for x in paragraphs],
                      'metadata_original_values_and_absence_exact': True, 'ordered_native_assets_exact': order,
                      'BibTeX_and_private_noindex_null_boundaries_exact': True, 'saved_render_paths': images,
                      'own_INITIAL_payloads_unchanged': True, 'native_science_browser_or_writer_helper_execution': False,
                      'informed_editorial_not_blind_science': True}, indent=2))


if __name__ == '__main__':
    main()
