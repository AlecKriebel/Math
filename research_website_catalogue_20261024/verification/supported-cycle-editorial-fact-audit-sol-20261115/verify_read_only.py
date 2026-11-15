"""Offline editorial fact/custody closure; no project imports, science, subprocess, network or writes."""
from pathlib import Path, PurePosixPath
from html.parser import HTMLParser
import hashlib
import html
import json
import re
import sys
import zipfile

O = Path(__file__).resolve().parent
P = O.parent.parent
S = P / 'papers/23578142/sources'
E = P / 'papers/23578142/reviews/editorial'
N = 0


def need(value, why):
    global N
    N += 1
    if not value:
        raise ValueError(why)


def read(path):
    need(path.is_file() and not path.is_symlink() and path.resolve() == path, 'real regular input')
    return path.read_bytes()


def obj(path):
    return json.loads(read(path))


def pin(path, row):
    body = read(path)
    need(len(body) == row['bytes'] and hashlib.sha256(body).hexdigest() == row['SHA256'], 'whole byte binding')
    return body


def typed(a, b):
    need(type(a) is type(b), 'native type')
    if isinstance(a, dict):
        need(list(a) == list(b), 'complete ordered keys')
        for key in a:
            typed(a[key], b[key])
    elif isinstance(a, list):
        need(len(a) == len(b), 'complete ordered array')
        for left, right in zip(a, b):
            typed(left, right)
    else:
        need(a == b, 'complete scalar')


def namespace(root, files, directories):
    paths = list(root.rglob('*'))
    need(root.resolve() == root and not root.is_symlink()
         and all(not p.is_symlink() and (p.is_file() or p.is_dir()) for p in paths), 'whole ordinary namespace')
    need(sorted(p.relative_to(root).as_posix() for p in paths if p.is_file()) == sorted(files), 'exact files')
    need(sorted(p.relative_to(root).as_posix() for p in paths if p.is_dir()) == directories, 'exact directories')


def original_checks():
    initial = obj(O / 'INITIAL_SEAL.json')
    need(hashlib.sha256(read(O / 'INITIAL_SEAL.json')).hexdigest()
         == '0fb088da67e226cc068394fe13d9e987cab320016790f7bbad97394c98023e92', 'pre-editorial initial seal')
    for row in initial['payloads']:
        pin(O / row['path'], row)
    source = obj(O / 'INITIAL_SOURCE_MANIFEST.json')
    namespace(S, [r['path'] for r in source['files']], source['exact_relative_directories'])
    need(len(source['files']) == 77, 'all77 sources')
    for row in source['files']:
        pin(S / row['path'], row)
    roots = obj(O / 'INITIAL_INPUT_BINDINGS.json')
    for row in roots['root_files']:
        pin(Path(row['path']), row)
    native = obj(O / 'INITIAL_NATIVE_INPUTS.json')
    for item in native['whole_source_JSON_objects']:
        typed(item['whole_object'], obj(S / item['relative_path']))
    typed(native['whole_root_clearance'], obj(Path(roots['root_clearance_path'])))
    ready = obj(S / 'SOURCE_READY.json')
    typed(native['whole_root_clearance']['source_native_ready_whole_unchanged'], ready)
    archive = obj(S / 'ARCHIVE_CUSTODY.json')
    with zipfile.ZipFile(S / 'assets/supported-cycle-source-and-verification.zip') as zipped:
        infos = zipped.infolist()
        need(len(infos) == len(archive['containers'][0]['members']), 'all ZIP members')
        need(len(archive['regular_payload_occurrences']) == 27, 'all27 regular payloads')
        for row in archive['regular_payload_occurrences']:
            info = infos[row['ordinal_zero_based']]
            body = zipped.read(info)
            need(info.filename == row['original_member_name'] and not info.is_dir(), 'native ordered member')
            need(body == pin(Path(row['extracted_path']), row), 'whole ZIP payload/extracted identity')
            need((f'{info.CRC:08x}', info.compress_size, info.compress_type, info.external_attr,
                  info.create_system, info.flag_bits, list(info.date_time))
                 == (row['CRC32'], row['compressed_bytes'], row['compression_method'], row['native_external_attr'],
                     row['native_create_system'], row['native_flags'], row['native_date_time']), 'all ZIP metadata')
    need(ready['mathematical_PDF_TeX_or_pixels_read'] is False and ready['scientific_verdict'] is None,
         'original historical unread/null fields remain original')
    return ready, native['whole_root_clearance']


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.tags = []

    def handle_starttag(self, tag, attributes):
        values = dict(attributes)
        self.tags.append((tag, values))
        if 'id' in values:
            self.ids.append(values['id'])


def editorial_checks(ready, root):
    binding = obj(O / 'EDITORIAL_BINDINGS.json')
    namespace(E, [r['path'] for r in binding['files']], binding['exact_relative_directories'])
    need(len(binding['files']) == 328 and len(binding['exact_relative_directories']) == 11, 'whole actual328/11')
    for row in binding['files']:
        pin(E / row['path'], row)
    need(hashlib.sha256(read(E / 'SEAL.json')).hexdigest()
         == 'cf6c0798358d3db769501626c486d5e7be76e4d10082f7615a941215cbca64c9', 'actual final owner seal')
    manifest = obj(E / 'MANIFEST.json')
    need(sorted(manifest['payloads']) == sorted(r['path'] for r in binding['files']
                                              if r['path'] not in {'MANIFEST.json', 'SEAL.json'}),
         'only exact root terminal exclusions; no basename exclusion')
    protected = obj(E / 'PROTECTED_INPUTS.json')
    rows = {r['path']: r for r in protected['files']}
    need(len(rows) == len(protected['files']) == 300, 'all300 distinct protected originals')
    for row in rows.values():
        original = Path(row['path'])
        need(not str(original).startswith('/Users/alec/Desktop/'), 'no website input')
        need(pin(original, row) == pin(E / row['copy'], row), 'whole original/raw copy')
    pub = obj(E / 'publication.json')
    promotion = obj(E / 'promotion.json')
    protocol = obj(E / 'SOURCE_PROTOCOL_BINDINGS.json')

    def wrappers(value):
        if isinstance(value, dict):
            if all(key in value for key in ['original', 'copy', 'whole_literal_object']):
                path = value['original']['path']
                need(path in rows, 'wrapper original is among exact protected originals')
                need(value['copy'] == rows[path]['copy'], 'exact raw wrapper copy location')
                typed(value['whole_literal_object'], obj(Path(path)))
                typed(value['whole_literal_object'], obj(E / value['copy']))
            for item in value.values():
                wrappers(item)
        elif isinstance(value, list):
            for item in value:
                wrappers(item)

    wrappers(protocol)
    wrappers(pub)
    wrappers(promotion)
    typed(pub['source_binding']['whole_original_source_ready'], ready)
    typed(pub['native_assets_in_original_order'], ready['all_native_assets_in_original_order'])
    peers = {'scope': root['whole_original_scope_verdict'], 'adversarial': root['whole_original_adversarial_verdict']}
    typed(pub['review_metadata']['whole_original_scientific_verdicts'], peers)
    typed(promotion['whole_original_scientific_verdicts'], peers)
    typed(promotion['whole_root_scientific_authority']['whole_literal_object'], root)
    typed(promotion['whole_source_binding'], pub['source_binding'])

    # Printed paper abstract and native deposit description are different full objects.
    tex = read(Path(ready['controlling_TeX']['extracted_path'])).decode()
    abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S)[1]
    need(read(E / 'ORIGINAL_ABSTRACT.tex').decode() == abstract, 'complete raw printed abstract')
    rendered = abstract.replace('$r$', 'r').replace('$n\\ge2$', 'n ≥ 2').replace('$n$th', 'nth')
    need('$' not in rendered, 'all printed abstract math conversions explicitly accounted')
    rendered = ' '.join(rendered.split())
    need(pub['abstract'] == rendered, 'exact complete printed abstract rendering')
    native = obj(S / 'record.response.body')
    need(native['metadata']['description'] == obj(O / 'INITIAL_NATIVE_INPUTS.json')['native_abstract_HTML'],
         'distinct complete three-paragraph native deposit description unchanged')
    need(len(re.findall('<p>', native['metadata']['description'])) == 3, 'all native description paragraphs')
    copy = read(E / 'PUBLIC_COPY.md').decode()
    main = read(E / 'PUBLIC_MAIN.html').decode()
    candidate = read(E / 'candidate/index.html').decode()
    need(rendered in copy and '<p>' + html.escape(rendered) + '</p>' in main, 'entire visible printed abstract')
    need(re.findall(r'<main\b[^>]*>.*?</main>', candidate, re.S) == [main[:-1]], 'entire actual main')
    scholarly = obj(E / 'SCHOLARLY_METADATA.json')
    embedded = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', candidate, re.S)[1])
    typed(scholarly, embedded)
    need(scholarly['abstract'] == rendered and scholarly['abstract'] != scholarly['description'], 'whole scholarly abstract, distinct summary')
    need(pub['version'] == pub['printed_version'] == scholarly['version'] == native['metadata']['version'] == '1.0.0', 'all actual edition fields')
    need(pub['publication_date'] == scholarly['datePublished'] == native['metadata']['publication_date'] == '2026-10-22', 'all actual original dates')
    need(scholarly['identifier'] == pub['doi'] == '10.5281/zenodo.23578142', 'actual DOI')
    need(scholarly['author']['identifier'] == pub['orcid'] == 'https://orcid.org/0009-0001-9320-500X', 'actual ORCID')
    need(len(scholarly['encoding']) == 2 and 'license' not in scholarly['encoding'][0]
         and scholarly['encoding'][1]['license'] == scholarly['license'] == 'https://creativecommons.org/licenses/by/4.0/', 'mixed ZIP/PDF rights')
    for row, encoding in zip(ready['all_native_assets_in_original_order'], scholarly['encoding']):
        need(read(E / 'candidate' / row['original_api_file_object']['key']) == pin(Path(row['path']), row), 'entire native download')
        need(encoding['contentUrl'] == row['original_api_file_object']['links']['self'], 'native encoding order and URL')
    rights = obj(E / 'RIGHTS_AND_IDENTITY.json')
    for key, filename in [('original_prose_license', 'LICENSE-PROSE.txt'), ('original_code_license', 'LICENSE-CODE.txt')]:
        need(rights[key]['whole_literal_text'] == read(S / 'published-source/asset-001/supported_cycle_verification' / filename).decode(), 'entire actual license text')
    need(pub['code_license'] == 'MIT' and rights['mixed_archive_blanket_license'] is None, 'distinct license instruments')
    need(read(E / 'citation.bib') == read(E / 'candidate/citation.bib') == pub['prepared_bibtex'].encode(), 'whole actual BibTeX')

    outputs = ['PUBLIC_COPY.md', 'PUBLIC_MAIN.html', 'SCHOLARLY_METADATA.json', 'citation.bib',
               'candidate/index.html', 'candidate/citation.bib', 'candidate/supported-cycle-source-and-verification.zip',
               'candidate/supported-cycle-bound.pdf']
    history = E / 'history/first-authoring'
    receipt = obj(history / 'HISTORY_RECEIPT.json')
    old, new = receipt['old_paragraph'], receipt['new_paragraph']
    for name in outputs:
        current = read(E / name)
        first = read(history / name)
        need(current == read(E / 'optimized-authoring' / name), 'whole normal/O current authoring')
        need(first == read(history / 'optimized-authoring' / name), 'whole normal/O first authoring')
        if name in ['PUBLIC_COPY.md', 'PUBLIC_MAIN.html', 'candidate/index.html']:
            before, after = (old, new) if name.endswith('.md') else (html.escape(old), html.escape(new))
            need(first.decode().count(before) == 1 and first.decode().replace(before, after) == current.decode(), 'only declared full category clarification')
        else:
            need(first == current, 'unchanged first/current remaining buffers')
    for directory in [E, history]:
        for name, level in [('AUTHOR_NORMAL', 0), ('AUTHOR_OPTIMIZED', 1)]:
            need(obj(directory / (name + '.stdout.json'))['optimization_level'] == level, 'actual saved optimization field')
            need(read(directory / (name + '.stderr')) == b'', 'actual author stderr')
    actual = obj(E / 'AUTHORING_RECEIPT.json')
    need([r['actual_process_exit_code'] for r in actual['actual_tool_results']] == [0, 0], 'actual successful process exits distinct from optimization')
    need(receipt['prior_actual_authoring_exit_codes'] == [0, 0] and receipt['no_failed_authoring_or_custody_run'] is True, 'whole first history disposition')

    page = Page(); page.feed(candidate)
    need(len(page.ids) == len(set(page.ids)), 'unique accessible IDs')
    need(sum(tag == 'h1' for tag, _ in page.tags) == 1 and sum(tag == 'main' for tag, _ in page.tags) == 1, 'one visible h1/main')
    need(('html', {'lang': 'en'}) in page.tags and '<a href="#main">Skip to content</a>' in candidate, 'language and skip target')
    frames = [a for tag, a in page.tags if tag == 'iframe']
    need(len(frames) == 1 and frames[0]['title'] == 'Complete seven-page paper'
         and frames[0]['src'] == 'supported-cycle-bound.pdf#view=FitH', 'titled original reader')
    need('background:#fff' in candidate and 'Arial,Helvetica,sans-serif' in candidate and 'width=device-width' in candidate, 'actual light responsive style')
    need(not re.search(r'display\s*:\s*none|visibility\s*:\s*hidden|opacity\s*:\s*0', candidate, re.I), 'no hidden copy')
    need('noindex,nofollow,noarchive' in candidate and '<link rel="canonical"' not in candidate, 'private candidate gate')
    for key in ['canonical_url', 'AA', 'follow_up', 'native_sheet_aa_url']:
        need(pub[key] is None, 'actual private null gate')
    for key in ['production_installation_authorized', 'ready_to_publish', 'rendered_public_copy_approved', 'installed',
                'deployed', 'live_verified', 'browser_verified', 'native_sheet_publication_verified', 'all203_complete_claimed']:
        need(promotion[key] is False, 'actual private false gate')
    need(promotion['follow_up'] is None, 'no invented follow-up')


def main():
    need(sys.argv[1:] in [[], ['--preseal']], 'bounded pure options')
    ready, root = original_checks()
    editorial_checks(ready, root)
    if sys.argv[1:] != ['--preseal']:
        seal = obj(O / 'FINAL_SEAL.json')
        need(hashlib.sha256(read(O / 'FINAL_MANIFEST.json')).hexdigest() == seal['MANIFEST_SHA256'], 'final manifest seal')
        manifest = obj(O / 'FINAL_MANIFEST.json')
        namespace(O, [row['path'] for row in manifest['files']] + ['FINAL_MANIFEST.json', 'FINAL_SEAL.json'], manifest['directories'])
        need(manifest['excluded_exact_root_terminal_files'] == ['FINAL_MANIFEST.json', 'FINAL_SEAL.json'], 'exact root terminals only')
        for row in manifest['files']:
            rel = PurePosixPath(row['path'])
            need(not rel.is_absolute() and '..' not in rel.parts and str(rel) == row['path'], 'safe whole owned path')
            pin(O / rel, row)
    print(json.dumps({'status': 'PASS_INFORMED_SUPPORTED_CYCLE_EDITORIAL_FACT_CUSTODY', 'checks': N,
                      'mode': 'preseal' if sys.argv[1:] else 'final', 'original_source_files': 77,
                      'editorial_files': 328, 'editorial_directories': 11, 'all_historical_native_wrappers_compared': True,
                      'printed_full_abstract_and_native_deposit_description_distinguished': True,
                      'science_authoring_network_project_imports_subprocess_or_writes': False,
                      'publication_authority': False}, sort_keys=True))


if __name__ == '__main__':
    main()
