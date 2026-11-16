"""One bounded read-only copy/data/custody comparison. No science or renderer."""
from pathlib import Path
from hashlib import sha256, md5
from html import unescape
from datetime import datetime, timezone
import json
import re
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O = P / 'verification/fixed-city-editorial-fact-sol-20261116'
W = P / 'papers/23393139/reviews/editorial'
S = P / 'papers/23393139/sources'
checks = []


def pin(path):
    b = path.read_bytes()
    return {'bytes': len(b), 'sha256': sha256(b).hexdigest()}


def load(path):
    return json.loads(path.read_text())


def ordered(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def check(name, value):
    checks.append({'name': name, 'status': 'PASS' if value else 'FAIL'})


def plain(value):
    return ' '.join(unescape(re.sub(r'<[^>]*>', '', value)).split())


def canon(value):
    return re.sub(r'\s*([><=])\s*', r'\1', ' '.join(value.split()))


def main():
    own_seal = load(O / 'INITIAL_SEAL.json')
    check('original own INITIAL seal unchanged', pin(O / 'INITIAL_SEAL.json') == {'bytes': 1603, 'sha256': 'b15d46600ea247888387aa4d8a14ebb5e1d82d8b09a06a8c7d06e1eb5b5911a2'})
    check('six original own payloads unchanged', all(pin(O / q['path']) == {'bytes': q['bytes'], 'sha256': q['sha256']} for q in own_seal['payloads']))
    source_pins = load(O / 'SOURCE_PINS.json')['entries']
    check('all finite source and reused-raster pins unchanged', all(pin(P / q['path']) == {'bytes': q['bytes'], 'sha256': q['sha256']} for q in source_pins))
    check('actual root clearance pinned', pin(P / 'verification/root-clearance-23393139-20261116.json') == {'bytes': 2269, 'sha256': 'cc1f3fac832e448d9a78e5ad31fb23e789d4db6050677a9f3929645ea5c1ba43'})
    check('actual root review pinned', pin(P / 'papers/23393139/reviews/root/ROOT_REVIEW.md') == {'bytes': 7093, 'sha256': 'd72bfc5681dbfbfd277c86da2f1a3b3603b3c3fd7062a1ff87afe25ae4465ba2'})
    check('actual writer FINAL pinned', pin(W / 'FINAL.json') == {'bytes': 4490, 'sha256': '833d8a15d34e82e405f655f8f0fbfe4eb7ba3ff3e8c662befa95691bdb8f3da7'})
    check('actual writer manifest pinned', pin(W / 'OWNED_MANIFEST.json') == {'bytes': 5915, 'sha256': '1321a89d6bef609f753e00aceb11b7d7eef287bd653d1cb4700b3ec2e025ab69'})
    final = load(W / 'FINAL.json')
    manifest = load(W / 'OWNED_MANIFEST.json')
    actual_files = []
    actual_dirs = []
    special = []
    for f in sorted(W.rglob('*')):
        rel = f.relative_to(W).as_posix()
        st = f.lstat()
        if stat.S_ISREG(st.st_mode):
            actual_files.append({'path': rel, **pin(f), 'mode': stat.S_IMODE(st.st_mode)})
        elif stat.S_ISDIR(st.st_mode):
            actual_dirs.append({'path': rel, 'mode': stat.S_IMODE(st.st_mode)})
        else:
            special.append(rel)
    listed = {q['path']: {'bytes': q['bytes'], 'sha256': q['sha256']} for q in manifest['files']}
    actual = {q['path']: {'bytes': q['bytes'], 'sha256': q['sha256']} for q in actual_files if q['path'] not in ['FINAL.json', 'OWNED_MANIFEST.json']}
    check('writer exact 35 payloads plus two terminal controls, including ignored material', actual == listed and len(actual_files) == 37 and not special)
    check('writer exact three directories', [q['path'] for q in actual_dirs] == ['preview', 'renders', 'source-pdf-pages'])
    html = (W / 'preview/index.html').read_text()
    main_html = re.search(r'<main\b[^>]*>[\s\S]*?</main>', html).group()
    head = re.search(r'<head\b[^>]*>[\s\S]*?</head>', html).group()
    check('whole MAIN exact fragment identity', (W / 'MAIN.html').read_bytes() == main_html.encode())
    check('whole page, MAIN and head bind actual FINAL', pin(W / 'preview/index.html') == {k: final['whole_page'][k] for k in ['bytes', 'sha256']} and pin(W / 'MAIN.html') == {k: final['whole_MAIN'][k] for k in ['bytes', 'sha256']} and {'bytes': len(head.encode()), 'sha256': sha256(head.encode()).hexdigest()} == final['whole_head'])
    model = load(W / 'PAGE_MODEL.json')
    native = load(S / 'record.response.body')
    native_files = load(S / 'files-23393139.response.body')
    authored = load(S / 'published-source/container-001/tree/metadata.json')
    source_facts = load(O / 'SOURCE_FACTS.json')
    check('full native metadata preserves key order, types and values', ordered(model['native_metadata_original']) == ordered(native['metadata']))
    check('native record files preserve original list/key order and types', ordered(model['native_record_files']) == ordered(native['files']))
    check('full files response preserves wrappers, null, empty order, types and keys', ordered(model['native_files_response']) == ordered(native_files))
    check('full authored metadata preserves original order and values', ordered(model['authored_metadata_original']) == ordered(authored))
    check('separate full native Description preserved exactly', model['native_description_original'] == native['metadata']['description'] == source_facts['native_description_html_exact'] and model['visible_duplicate_description'] is False)
    metas = {name: unescape(content) for name, content in re.findall(r'<meta (?:name|property)="([^"]+)" content="([^"]*)">', head)}
    article = json.loads(re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>', head).group(1))
    visible_abstract = plain(re.search(r'<section id="original-abstract"[\s\S]*?<p>([\s\S]*?)</p>[\s\S]*?</section>', main_html).group(1))
    abstract = source_facts['abstract_full_text_math_rendering']
    check('full original abstract in body, DC, JSONLD and model', all(canon(x) == canon(abstract) for x in [visible_abstract, metas['DC.description'], article['abstract'], model['abstract']]) and model['abstract_tex'] == source_facts['abstract_tex_exact'])
    check('title, DOI, author and ORCID', article['name'] == native['metadata']['title'] == metas['citation_title'] and article['identifier']['value'] == native['doi'] == metas['citation_doi'] and article['author']['name'] == 'Alec Kriebel' and article['author']['identifier'] == 'https://orcid.org/0009-0001-9320-500X')
    check('printed and native date/version without synthetic replacement', article['datePublished'] == model['native_metadata_original']['publication_date'] == '2026-10-15' and article['version'] == model['printed_version'] == model['native_version'] == metas['citation_version'] == '1.0.0' and model['native_created'] == native['created'])
    check('actual CC BY 4.0 rights without MIT inference', article['license'] == 'https://creativecommons.org/licenses/by/4.0/' and native['metadata']['license']['id'] == authored['license'] == 'cc-by-4.0' and not re.search(r'\bMIT\b', main_html))
    check('private noindex and null production/follow-up fields', metas['robots'] == 'noindex, nofollow, noarchive' and not re.search(r'<link\b[^>]*rel="canonical"|<base\b', head) and all(model[k] is None for k in ['canonical_url', 'base_url', 'production_url', 'AA', 'follow_up']) and model['publication_authority'] is False)
    check('one semantic MAIN, one H1, unique IDs', len(re.findall(r'<main\b', html)) == len(re.findall(r'<h1\b', html)) == 1 and '<main id="main">' in html and len(re.findall(r'\bid="([^"]+)"', html)) == len(set(re.findall(r'\bid="([^"]+)"', html))))
    downloads = re.search(r'<ol id="native-downloads">([\s\S]*?)</ol>', main_html).group(1)
    order = re.findall(r'<li><a href="([^"]+)" download>', downloads)
    check('original PDF then ZIP order in downloads/model/schema', order == model['native_asset_order'] == [q['key'] for q in native['files']] == [q['contentUrl'] for q in article['encoding']])
    assets = []
    for i, q in enumerate(native['files']):
        b = (W / 'preview' / q['key']).read_bytes()
        good = b == (S / 'assets' / q['key']).read_bytes() and len(b) == q['size'] and 'md5:' + md5(b).hexdigest() == q['checksum'] and article['encoding'][i]['sameAs'] == q['links']['self']
        assets.append({'name': q['key'], **pin(W / 'preview' / q['key']), 'exact_native_identity': good})
    check('both native assets byte exact with original URLs/checksums', all(q['exact_native_identity'] for q in assets))
    check('titled original embed, direct open and downloads', 'src="city-ode-persistence-note.pdf#view=FitH"' in main_html and 'title="Original five-page manuscript:' in main_html and 'href="city-ode-persistence-note.pdf" target="_blank"' in main_html and 'href="city-ode-persistence-note.pdf" download' in main_html)
    bib = (W / 'preview/citation.bib').read_text()
    check('Bib title, original DOI, date, version and CC BY', all(x in bib for x in [native['metadata']['title'], native['doi'], 'year = {2026}', 'month = oct', 'day = {15}', 'version = {1.0.0}', 'license = {CC-BY-4.0}']))
    check('no detailed internal review/replay narrative in public MAIN', not any(x in main_html for x in ['ROOT_REVIEW', 'root-clearance', '2026-11-16', '216 finite', 'self-test', 'SOURCE_FIRST', 'rejection tests']))
    receipt = load(W / 'RENDER_RECEIPT.json')
    check('literal twelve Chrome console and failed-request diagnostics retained', receipt['diagnostics']['console_errors'] == ['Failed to load resource: net::ERR_FAILED'] * 12 and len(receipt['diagnostics']['failed_requests']) == 12 and len(receipt['diagnostics']['nonlocal_page_routes_aborted']) == 12 and receipt['diagnostics']['page_errors'] == [])
    check('six saved captures bind actual image bytes', len(receipt['captures']) == 6 and all(pin(W / q['path']) == {'bytes': q['bytes'], 'sha256': q['sha256']} for q in receipt['captures']))
    check('PDF display/live/download limits remain false', receipt['actual_embedded_PDF_display_certified'] is False and final['actual_PDF_display_certified'] is False and final['actual_download_clicks_or_live_checks'] is False)
    print(json.dumps({'UTC': datetime.now(timezone.utc).isoformat(), 'status': 'PASS' if all(q['status'] == 'PASS' for q in checks) else 'NO_GO', 'record_id': '23393139', 'kind': 'one read-only data/custody comparison; no proof or browser test', 'checks': checks, 'native_assets': assets, 'writer_files_including_ignored': actual_files, 'writer_directories': actual_dirs, 'literal_render_diagnostics_by_pinned_reference': {'path': 'papers/23393139/reviews/editorial/RENDER_RECEIPT.json', **pin(W / 'RENDER_RECEIPT.json')}, 'functions_actually_called': ['main', 'pin', 'load', 'ordered', 'check', 'plain', 'canon'], 'writes_by_this_utility': 0, 'scientific_or_native_or_render_executions': 0}, ensure_ascii=False, indent=2))
    return 0 if all(q['status'] == 'PASS' for q in checks) else 1


if __name__ == '__main__':
    raise SystemExit(main())
