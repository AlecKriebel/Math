"""Pure informed editorial custody. No project/science imports, campaigns, subprocess, network or writes."""
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
S = P / 'papers/23306203/sources'
E = P / 'papers/23306203/reviews/editorial'
N = 0


def need(value, reason):
    global N
    N += 1
    if not value:
        raise ValueError(reason)


def read(path):
    need('.git' not in path.parts and not str(path).startswith('/Users/alec/Desktop/'), 'no Git/site input')
    need(path.is_file() and not path.is_symlink() and path.resolve() == path, 'real regular input')
    return path.read_bytes()


def obj(path):
    return json.loads(read(path))


def pin(path, row):
    body = read(path)
    need(len(body) == row['bytes'] and hashlib.sha256(body).hexdigest() == row['SHA256'], 'whole bytes')
    return body


def typed(a, b):
    need(type(a) is type(b), 'literal native type')
    if isinstance(a, dict):
        need(list(a) == list(b), 'whole ordered keys')
        for key in a:
            typed(a[key], b[key])
    elif isinstance(a, list):
        need(len(a) == len(b), 'whole ordered array')
        for left, right in zip(a, b):
            typed(left, right)
    else:
        need(a == b, 'whole scalar')


def namespace(root, files, directories):
    paths = list(root.rglob('*'))
    need(root.resolve() == root and not root.is_symlink()
         and all(not x.is_symlink() and (x.is_file() or x.is_dir()) for x in paths), 'whole ordinary namespace')
    need(sorted(x.relative_to(root).as_posix() for x in paths if x.is_file()) == sorted(files), 'strict files')
    need(sorted(x.relative_to(root).as_posix() for x in paths if x.is_dir()) == directories, 'strict directories')


def source_checks():
    need(hashlib.sha256(read(O / 'INITIAL_SEAL.json')).hexdigest()
         == 'c19c9bec6c41dee5d1607bffc0a2ff188410f57aa934b3e4b228cf0782ed7bec', 'pre-editorial initial seal')
    for row in obj(O / 'INITIAL_SEAL.json')['payloads']:
        pin(O / row['path'], row)
    source = obj(O / 'INITIAL_SOURCE_MANIFEST.json')
    namespace(S, [r['path'] for r in source['files']], source['exact_relative_directories'])
    need(len(source['files']) == 66, 'complete source66')
    for row in source['files']:
        pin(S / row['path'], row)
    bindings = obj(O / 'INITIAL_INPUT_BINDINGS.json')
    for row in bindings['root_files']:
        pin(Path(row['path']), row)
    saved = obj(O / 'INITIAL_NATIVE_INPUTS.json')
    for row in saved['whole_source_JSON_objects']:
        typed(row['whole_object'], obj(S / row['relative_path']))
    root = obj(Path(bindings['root_clearance_path']))
    typed(saved['whole_root_clearance'], root)
    ready = obj(S / 'SOURCE_READY.json')
    typed(root['whole_original_SOURCE_READY_unchanged'], ready)
    archive = obj(S / 'ARCHIVE_CUSTODY.json')
    need(len(archive['regular_payload_occurrences']) == 13 and ready['embedded_PDFs'] == [], 'archive13/no embedded PDF')
    with zipfile.ZipFile(S / 'assets/focal_product_support.zip') as zipped:
        infos = zipped.infolist()
        need(len(infos) == len(archive['containers'][0]['members']), 'whole ZIP extent')
        for row in archive['regular_payload_occurrences']:
            info = infos[row['ordinal_zero_based']]
            body = zipped.read(info)
            need(info.filename == row['original_member_name'] and not info.is_dir(), 'ordered member')
            need(body == pin(Path(row['extracted_path']), row), 'whole member/extracted bytes')
            need((f'{info.CRC:08x}', info.compress_size, info.compress_type, info.external_attr,
                  info.create_system, info.flag_bits, list(info.date_time))
                 == (row['CRC32'], row['compressed_bytes'], row['compression_method'], row['native_external_attr'],
                     row['native_create_system'], row['native_flags'], row['native_date_time']), 'whole native ZIP metadata')
    need(ready['mathematical_PDF_TeX_or_pixels_read'] is False and ready['printed_version'] is None
         and ready['scientific_verdict'] is None, 'historical unread/null flags unchanged')
    return ready, root


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.tags = [], []

    def handle_starttag(self, tag, pairs):
        attributes = dict(pairs)
        self.tags.append((tag, attributes))
        if 'id' in attributes:
            self.ids.append(attributes['id'])


def editorial_checks(ready, root):
    binding = obj(O / 'EDITORIAL_BINDINGS.json')
    namespace(E, [r['path'] for r in binding['files']], binding['exact_relative_directories'])
    need(len(binding['files']) == 304 and len(binding['exact_relative_directories']) == 11, 'complete owner304/11')
    for row in binding['files']:
        pin(E / row['path'], row)
    need(hashlib.sha256(read(E / 'SEAL.json')).hexdigest()
         == 'e3070211dcf78c1d93a95b83d77bba030e37e0f6f09e801d38310605d317f666', 'actual final editorial seal')
    owner = obj(E / 'MANIFEST.json')
    need(sorted(owner['payloads']) == sorted(r['path'] for r in binding['files']
                                            if r['path'] not in {'MANIFEST.json', 'SEAL.json'}), 'exact root terminals only')
    protected = obj(E / 'PROTECTED_INPUTS.json')
    rows = {r['path']: r for r in protected['files']}
    need(len(rows) == len(protected['files']) == 276, 'all276 distinct originals')
    for row in rows.values():
        need(pin(Path(row['path']), row) == pin(E / row['copy'], row), 'whole original/raw copy')
    pub, promotion, protocol = [obj(E / name) for name in ['publication.json', 'promotion.json', 'SOURCE_PROTOCOL_BINDINGS.json']]

    def wrappers(value):
        if isinstance(value, dict):
            if all(key in value for key in ['original', 'copy', 'whole_literal_object']):
                path = value['original']['path']
                need(path in rows and value['copy'] == rows[path]['copy'], 'actual complete wrapper binding')
                typed(value['whole_literal_object'], obj(Path(path)))
                typed(value['whole_literal_object'], obj(E / value['copy']))
            for item in value.values():
                wrappers(item)
        elif isinstance(value, list):
            for item in value:
                wrappers(item)

    wrappers(protocol)
    record = obj(S / 'record.response.body')
    typed(pub['source_binding']['whole_original_source_ready'], ready)
    typed(pub['source_binding']['whole_native_record'], record)
    typed(pub['source_binding']['whole_original_support_metadata'], obj(S / 'published-source/asset-001/metadata.json'))
    typed(pub['review_metadata']['whole_root_scientific_authority'], root)
    peers = {'scope': root['whole_scope_literal_verdict'], 'adversarial': root['whole_adversarial_literal_verdict']}
    typed(pub['review_metadata']['whole_original_scientific_verdicts'], peers)
    typed(promotion['whole_root_scientific_authority'], root)
    typed(promotion['whole_original_scientific_verdicts'], peers)
    typed(promotion['whole_source_binding'], pub['source_binding'])
    typed(pub['native_assets_in_original_order'], ready['all_native_assets_in_original_order'])
    typed([x['whole_original_binding'] for x in protocol['native_API_objects_in_original_order']], ready['whole_native_API_objects'])
    limits = obj(E / 'PRIMARY_SCOPE_AND_EDITION_LIMITS.json')
    need(limits['whole_original_priority_note_text'] == read(S / 'published-source/asset-001/SOURCES_AND_PRIORITY.md').decode(), 'whole original priority note')

    tex = read(Path(ready['controlling_TeX']['extracted_path'])).decode()
    fragment = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S)[1]
    need(fragment == read(E / 'ORIGINAL_PRINTED_ABSTRACT.tex').decode()
         == obj(O / 'INITIAL_NATIVE_INPUTS.json')['whole_printed_TeX_abstract'], 'entire original printed abstract')
    abstract = ' '.join(fragment.split()).replace('\\(2\\)', '2').replace('\\(4\\)', '4').replace('\\(k_{114}\\)', 'k₁₁₄').replace('Reznik--Garcia--Koiller', 'Reznik–Garcia–Koiller')
    need('\\(' not in abstract and pub['abstract'] == abstract, 'all printed abstract typography accounted')
    description = record['metadata']['description']
    need(pub['native_deposit_description_html'] == read(E / 'NATIVE_DEPOSIT_DESCRIPTION.html').decode() == description,
         'entire distinct native four-paragraph description')
    need(len(re.findall('<p>', description)) == 4 and description != abstract, 'native/printed distinction')
    copy, main, candidate = [read(E / name).decode() for name in ['PUBLIC_COPY.md', 'PUBLIC_MAIN.html', 'candidate/index.html']]
    need(re.findall(r'<main\b[^>]*>.*?</main>', candidate, re.S) == [main[:-1]], 'entire actual candidate main')
    need('<h2>Original printed abstract</h2><p>' + html.escape(abstract) + '</p>' in main and abstract in copy, 'whole visible printed abstract')
    deposit = '<details id="native-deposit-description"><summary>Original Zenodo deposit description</summary>' + description + '</details>'
    need(deposit in main and deposit in copy, 'whole separately labelled native description')
    for section in obj(E / 'public-sections.json'):
        for paragraph in section['paragraphs']:
            need('<p>' + html.escape(paragraph) + '</p>' in main and paragraph in copy, 'complete actual section paragraph')
    scholarly = obj(E / 'SCHOLARLY_METADATA.json')
    typed(scholarly, json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', candidate, re.S)[1]))
    need(scholarly['abstract'] == abstract and abstract != scholarly['description'], 'full scholarly abstract vs SEO summary')
    need(pub['printed_version_field_present'] is False and pub['printed_version'] is None
         and scholarly['version'] == pub['version'] == record['metadata']['version'] == '1.0.0', 'printed ABSENT/native version')
    need(pub['version_label'] == 'Native deposit version 1.0.0' and 'printed paper has no version line' in main, 'native version correctly labelled')
    need(scholarly['datePublished'] == pub['publication_date'] == record['metadata']['publication_date'] == '2026-10-11'
         and pub['printed_date'] == '11 October 2026', 'actual dates')
    need(scholarly['identifier'] == pub['doi'] == '10.5281/zenodo.23306203'
         and scholarly['author']['identifier'] == pub['orcid'] == 'https://orcid.org/0009-0001-9320-500X', 'DOI/ORCID')
    need(len(scholarly['encoding']) == 2, 'two encodings')
    for row, encoding in zip(ready['all_native_assets_in_original_order'], scholarly['encoding']):
        need(read(E / 'candidate' / row['original_api_file_object']['key']) == pin(Path(row['path']), row), 'whole unchanged native download')
        need(encoding['contentUrl'] == row['original_api_file_object']['links']['self']
             and encoding['license'] == scholarly['license'] == 'https://creativecommons.org/licenses/by/4.0/', 'original order/CC BY encoding')
    rights = obj(E / 'RIGHTS_AND_IDENTITY.json')
    need(rights['whole_original_license_text'] == read(S / 'published-source/asset-001/LICENSE.md').decode()
         and rights['MIT_license_inferred'] is False and pub['code_license'] == 'CC BY 4.0', 'actual broad code/support instrument')
    need(read(E / 'citation.bib') == read(E / 'candidate/citation.bib') == pub['prepared_bibtex'].encode(), 'entire actual BibTeX')

    outputs = ['PUBLIC_COPY.md', 'PUBLIC_MAIN.html', 'SCHOLARLY_METADATA.json', 'citation.bib', 'candidate/index.html',
               'candidate/citation.bib', 'candidate/focal_product_support.zip', 'candidate/focal_product_period_criterion.pdf']
    history = E / 'history/first-authoring'
    receipt = obj(history / 'HISTORY_RECEIPT.json')
    changes = list(zip(receipt['old_paragraphs'], receipt['new_paragraphs']))
    need(len(changes) == 2, 'two declared notation clarifications')
    for name in outputs:
        current, first = read(E / name), read(history / name)
        need(current == read(E / 'optimized-authoring' / name), 'whole current normal/O pair')
        need(first == read(history / 'optimized-authoring' / name), 'whole first normal/O pair')
        if name in ['PUBLIC_COPY.md', 'PUBLIC_MAIN.html', 'candidate/index.html']:
            expected = first.decode()
            for old, new in changes:
                if name.endswith('.html'):
                    old, new = html.escape(old), html.escape(new)
                need(expected.count(old) == 1, 'one complete old paragraph')
                expected = expected.replace(old, new)
            need(expected == current.decode(), 'only declared Kprime/H clarification')
        else:
            need(first == current, 'remaining five buffers unchanged')
    before = read(history / 'check_editorial_controls_pre_execution_first.py').decode()
    old = 'the full billiard body of the related Dragović–Gajić article remained unavailable'
    new = 'The full billiard body of the related Dragović–Gajić article remained unavailable'
    need(before.count(old) == 2 and before.replace(old, new) == read(E / 'check_editorial_controls.py').decode(), 'only two pre-execution guard case fixes')
    need(receipt['first_controls_body_executed'] is False and receipt['failed_authoring_controls_or_custody_processes'] == [], 'pre-execution review not failed run')
    for directory in [E, history]:
        for stem, level in [('AUTHOR_NORMAL', 0), ('AUTHOR_OPTIMIZED', 1)]:
            need(obj(directory / (stem + '.stdout.json'))['optimization_level'] == level, 'actual optimization field')
            need(read(directory / (stem + '.stderr')) == b'', 'actual author stderr')
    actual = obj(E / 'AUTHORING_RECEIPT.json')
    need([r['actual_process_exit_code'] for r in actual['actual_tool_results']] == [0, 0]
         and receipt['first_actual_process_exit_codes'] == [0, 0], 'actual exits distinct from optimization')
    for call in actual['actual_tool_results'] + actual['actual_editorial_validation_calls']:
        need(call['actual_process_exit_code'] == 0, 'literal successful saved process')
        typed(call['whole_actual_stdout_object'], obj(E / call['stdout']['path']))
        need(pin(E / call['stderr']['path'], call['stderr']) == b'', 'whole saved stderr')
    faults = obj(E / 'EDITORIAL_CONTROLS.stdout.json')
    need(faults['actual_baseline_accepted'] is True and len(faults['whole_receipts']) == faults['new_memory_faults_rejected'] == 13, 'whole actual13 fault receipts')
    need(len({r['required_detection'] for r in faults['whole_receipts']}) == 13, 'distinct recorded faults')
    for item in faults['whole_receipts']:
        need(item['rejected'] is True and item['required_detection'] in item['actual_detected_issues'], 'literal target detection')

    page = Page(); page.feed(candidate)
    need(len(page.ids) == len(set(page.ids)), 'unique IDs')
    need(sum(tag == 'h1' for tag, _ in page.tags) == sum(tag == 'main' for tag, _ in page.tags) == 1, 'one h1/main')
    need(('html', {'lang': 'en'}) in page.tags and '<a href="#main">Skip to content</a>' in candidate, 'language/skip link')
    frame = [a for tag, a in page.tags if tag == 'iframe']
    need(len(frame) == 1 and frame[0]['title'] == 'Complete five-page paper'
         and frame[0]['src'] == 'focal_product_period_criterion.pdf#view=FitH', 'titled unchanged reader')
    need('background:#fff' in candidate and 'Arial,Helvetica,sans-serif' in candidate and 'width=device-width' in candidate, 'actual light responsive style')
    need(not re.search(r'display\s*:\s*none|visibility\s*:\s*hidden|opacity\s*:\s*0', candidate, re.I), 'no hidden-content CSS')
    need('noindex,nofollow,noarchive' in candidate and '<link rel="canonical"' not in candidate, 'private candidate')
    for key in ['canonical_url', 'AA', 'follow_up', 'native_sheet_aa_url']:
        need(pub[key] is None, 'private null gate')
    for key in ['production_installation_authorized', 'ready_to_publish', 'rendered_public_copy_approved', 'installed',
                'deployed', 'live_verified', 'browser_verified', 'native_sheet_publication_verified', 'all203_complete_claimed']:
        need(promotion[key] is False, 'private false gate')
    need(promotion['follow_up'] is None, 'null follow-up')


def main():
    need(sys.argv[1:] in [[], ['--preseal']], 'bounded pure options')
    ready, root = source_checks()
    editorial_checks(ready, root)
    if not sys.argv[1:]:
        seal = obj(O / 'FINAL_SEAL.json')
        need(hashlib.sha256(read(O / 'FINAL_MANIFEST.json')).hexdigest() == seal['MANIFEST_SHA256'], 'final audit manifest')
        manifest = obj(O / 'FINAL_MANIFEST.json')
        need(manifest['excluded_exact_root_terminal_files'] == ['FINAL_MANIFEST.json', 'FINAL_SEAL.json'], 'exact root terminals only')
        namespace(O, [r['path'] for r in manifest['files']] + manifest['excluded_exact_root_terminal_files'], manifest['directories'])
        for row in manifest['files']:
            rel = PurePosixPath(row['path'])
            need(not rel.is_absolute() and '..' not in rel.parts and str(rel) == row['path'], 'safe owned payload')
            pin(O / rel, row)
    print(json.dumps({'status': 'PASS_INFORMED_FOCAL_BILLIARDS_EDITORIAL_FACT_CUSTODY', 'checks': N,
                      'mode': 'preseal' if sys.argv[1:] else 'final', 'source_files': 66, 'editorial_files': 304,
                      'whole_native_wrappers_and_all_history_compared': True, 'printed_version': 'ABSENT',
                      'native_version': '1.0.0', 'fault_science_authoring_network_project_imports_subprocess_or_writes': False,
                      'publication_authority': False}, sort_keys=True))


if __name__ == '__main__':
    main()
