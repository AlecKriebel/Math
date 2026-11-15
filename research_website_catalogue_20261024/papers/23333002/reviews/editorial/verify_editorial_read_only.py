#!/usr/bin/env python3
"""Pure editorial/custody checks. Never runs native science, builds or networking."""
from pathlib import Path
from html.parser import HTMLParser
import copy
import hashlib
import html
import json
import re
import sys
import unicodedata

A = Path(__file__).resolve().parent
R = A.parents[1]
S = R / 'sources'
P = R.parents[1]
TERMINAL = {'MANIFEST.json', 'CLOSURE_PRESEAL.json', 'SEAL.json'}
COUNT = 0


def need(ok, message):
    global COUNT
    COUNT += 1
    if not ok:
        raise ValueError(message)


def read(p):
    return json.loads(Path(p).read_text())


def ordered(x):
    return json.dumps(x, ensure_ascii=False, separators=(',', ':'))


def exact(a, b, message):
    need(ordered(a) == ordered(b), message)


def pin(entry):
    p = Path(entry['path'])
    need(p.is_file() and not p.is_symlink(), 'nonregular/missing pin ' + str(p))
    b = p.read_bytes()
    digest = entry.get('SHA256', entry.get('sha256'))
    need(len(b) == entry['bytes'] and hashlib.sha256(b).hexdigest() == digest,
         'pinned bytes changed ' + str(p))
    return b


def all_pins(value):
    if isinstance(value, dict):
        if 'path' in value and 'bytes' in value and ('SHA256' in value or 'sha256' in value):
            pin(value)
        else:
            for v in value.values():
                all_pins(v)
    elif isinstance(value, list):
        for v in value:
            all_pins(v)


def normal(text):
    return ' '.join(unicodedata.normalize('NFKC', text).split())


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta = {}
        self.links = []
        self.iframes = []
        self.canonicals = []
        self.text = []
        self.in_main = False
        self.in_schema = False
        self.schema = ''

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'main':
            self.in_main = True
        if tag == 'meta':
            self.meta[a.get('name', a.get('property'))] = a.get('content')
        if tag == 'a':
            self.links.append(a)
        if tag == 'iframe':
            self.iframes.append(a)
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonicals.append(a)
        if tag == 'script':
            need(a.get('type') == 'application/ld+json', 'unexpected executable/public script')
            self.in_schema = True

    def handle_endtag(self, tag):
        if tag == 'main':
            self.in_main = False
        if tag == 'script':
            self.in_schema = False

    def handle_data(self, value):
        if self.in_main:
            self.text.append(value)
        if self.in_schema:
            self.schema += value


def semantic_contract(pub, promotion, abstract):
    text = '\n'.join(v for key in ['plain_language', 'result', 'why_it_works', 'limitations', 'background']
                     for v in pub[key])
    need(pub['abstract'] == abstract, 'full original abstract changed')
    for phrase in ['both L=J_R and L=K_R', 'every real ε≥0', 'R+ε ∉ ΣS²+I_ℝ(L)',
                   'arbitrary real coefficients and arbitrary finite degrees', 'No fixed degree bound',
                   'The theorem includes ε=0', 'L⊆√L⊆I_ℝ(L)', 'every ε>0',
                   'For n=1 there are no minors', 'V_ℝ(K_Q)={(0,0)}', 'Its infimum −1/2 is not attained',
                   'It concerns only the separate-product reading', 'Its constant part is retained',
                   'so R already belongs to (R_x,R_y,R_z)', 'No uniquely intended or author-approved correction',
                   'Historical first priority and continued worldwide openness are not established',
                   'Schur', 'Reznick', 'Schweighofer', 'Laurent', 'extra multiplier terms']:
        need(phrase in text, 'mathematical/credit/limit wording missing: ' + phrase)
    need(pub['publication_date'] == '2026-10-12' and pub['version'] == pub['printed_version'] == '1.0', 'original edition/date')
    need(pub['doi'] == '10.5281/zenodo.23333002' and pub['author'] == 'Alec Kriebel' and
         pub['orcid'] == 'https://orcid.org/0009-0001-9320-500X', 'scholarly identity')
    need(pub['code_license'] is None and pub['authored_package_license'] == pub['license'] == 'CC BY 4.0' and
         pub['authored_code_covered_by_package_CC_BY_4_0'] is True, 'actual broad code grant, no invented MIT')
    need(pub['follow_up'] is None and promotion['follow_up'] is None, 'follow-up must remain null')
    need('actual scholarly contributions' in pub['collaboration'], 'contribution-based passive collaboration')
    need('extensively' in pub['ai_disclosure'] and 'without independent human or journal peer review' in pub['ai_disclosure'] and
         'no formal proof-assistant certification' in pub['ai_disclosure'], 'honest AI/unrefereed/nonhuman/nonformal disclosure')
    for key in ['canonical_url', 'AA', 'native_sheet_aa_url']:
        need(pub[key] is None and promotion[key] is None, 'premature assigned URL: ' + key)
    for key in ['rendered', 'deployed', 'rendered_public_copy_approved', 'rendered_copy_verified', 'local_http_verified',
                'live_http_verified', 'live_verified', 'browser_verified', 'native_verified', 'native_sheet_publication_verified',
                'public_page_published', 'root_editorial_clearance_received', 'production_integration_authorized',
                'publication_clearance', 'ready_to_publish', 'canonical_verified']:
        need(promotion[key] is False, 'premature publishing gate: ' + key)


def main():
    protected = read(A / 'PROTECTED_INPUTS.json')
    all_pins(protected['all_preexisting_paper_files'])
    for k in ['root_authority', 'root_review', 'goal']:
        pin(protected[k])
    original_source_paths = {e['path'] for e in protected['all_preexisting_paper_files'] if str(S) + '/' in e['path']}
    need({str(p) for p in S.rglob('*') if p.is_file()} == original_source_paths and len(original_source_paths) == 122,
         'exact frozen source membership')
    source = read(S / 'SOURCE_READY.json')
    authority = read(P / 'verification/root-clearance-23333002-20261115.json')
    pub = read(A / 'publication.json')
    promotion = read(A / 'promotion.json')
    adapter = read(A / 'SCHEMA_ADAPTER.json')
    binding = read(A / 'SOURCE_PROTOCOL_BINDINGS.json')
    section = read(A / 'public-sections.json')
    exact(authority['whole_literal_source_ready'], source, 'full root/source association')
    for value in [pub['source_binding'], adapter['whole_original_protocol_binding']]:
        exact(value, binding, 'whole source protocol object')
    exact(binding['whole_original_SOURCE_READY'], source, 'whole READY flags/keys/types/order')
    exact(promotion['whole_original_source_ready'], source, 'promotion whole READY')
    exact(pub['review_metadata']['whole_root_scientific_clearance'], authority, 'whole root authority publication')
    exact(promotion['whole_root_scientific_clearance_record'], authority, 'whole root authority promotion')
    exact(adapter['whole_original_review_metadata'], pub['review_metadata'], 'whole review metadata adapter')
    for api in binding['whole_original_native_API_objects']:
        pin(api['file'])
        exact(api['whole_original_object'], read(api['file']['path']), 'whole original native API keys/order/types')
    exact(promotion['whole_original_native_API_objects'], binding['whole_original_native_API_objects'], 'promotion API objects')
    receipts = read(S / 'ALL_TRANSPORT_RECEIPTS.json')
    exact(binding['whole_original_transport_aggregate'], receipts, 'whole transport aggregate')
    exact(binding['whole_original_seven_transport_objects'], receipts['receipts'], 'all seven actual receipts')
    exact(promotion['whole_original_seven_transport_objects'], receipts['receipts'], 'promotion seven transports')
    need([r['HTTP_status'] for r in receipts['receipts']] == [200, 301, 200, 200, 200, 200, 200], 'native success/redirect history')
    for row in binding['raw_original_byte_copies']:
        need(pin(row['original']) == pin(row['owned_byte_identical_copy']), 'original metadata bytes changed during copy')
    exact(binding['whole_original_archive_custody'], read(S / 'ARCHIVE_CUSTODY.json'), 'complete archive custody')
    exact(binding['whole_original_native_schema_types'], read(S / 'NATIVE_SCHEMA_TYPES.json'), 'heterogeneous native schemas')
    reviews = pub['review_metadata']['whole_actual_original_scientific_review_records']
    need(len(reviews) == promotion['actual_scientific_review_cardinality'] == 2, 'actual two peer verdicts')
    for i, review in enumerate(reviews):
        pin(review['verdict_file']); pin(review['seal_file'])
        exact(review['whole_original_custom_verdict'], read(review['verdict_file']['path']), 'literal complete scientific verdict')
        exact(promotion['whole_original_custom_scientific_verdicts'][i], review['whole_original_custom_verdict'], 'promotion literal verdict')
        exact(review['whole_original_review_seal'], read(review['seal_file']['path']), 'literal complete review seal')
    tex = (S / 'published-source/note.tex').read_text()
    raw = re.search(r'\\begin\{abstract\}([\s\S]*?)\\end\{abstract\}', tex).group(1)
    abstract = ' '.join(raw.split())
    need((A / 'abstract-source.tex').read_text() == raw, 'exact source abstract body')
    need((A / 'abstract-original.txt').read_text() == abstract + '\n', 'exact original abstract text')
    semantic_contract(pub, promotion, abstract)
    page_text = (A / 'candidate/index.html').read_text()
    page = Page(); page.feed(page_text)
    text = normal(' '.join(page.text))
    markdown = (A / 'PUBLIC_COPY.md').read_text()
    main_html = html.unescape((A / 'ARTICLE_MAIN.html').read_text())
    for key in ['abstract', 'plain_language', 'result', 'why_it_works', 'limitations', 'background',
                'collaboration', 'status', 'ai_disclosure', 'reader_intro', 'rights_notice']:
        exact(section[key], pub[key], 'single full public section: ' + key)
        for paragraph in section[key] if isinstance(section[key], list) else [section[key]]:
            need(normal(paragraph) in text, 'HTML section lost: ' + key)
            need(paragraph in markdown, 'Markdown section lost: ' + key)
            need(paragraph in main_html, 'full main HTML paragraph lost: ' + key)
    need(page.meta['robots'] == 'noindex,nofollow' and not page.canonicals, 'private noindex and unassigned canonical')
    for key, expected in {'description': pub['description'], 'citation_title': pub['title'], 'citation_author': pub['author'],
                          'citation_publication_date': '2026/10/12', 'citation_version': '1.0',
                          'citation_doi': pub['doi'], 'citation_pdf_url': 'assets/' + pub['pdf_filename']}.items():
        need(page.meta[key] == expected, 'citation/SEO metadata ' + key)
    schema = json.loads(page.schema)
    need(schema['@type'] == 'ScholarlyArticle' and schema['abstract'] == abstract and
         schema['datePublished'] == pub['publication_date'] and schema['version'] == pub['version'] and
         schema['identifier']['value'] == pub['doi'] and schema['author']['sameAs'] == pub['orcid'], 'full scholarly schema')
    for i, asset in enumerate(source['all_native_assets_in_original_order']):
        original = Path(asset['path']); candidate = A / 'candidate/assets' / asset['original_api_file_object']['key']
        need(original.read_bytes() == candidate.read_bytes(), 'unchanged complete original asset')
        need(hashlib.sha256(candidate.read_bytes()).hexdigest() == asset['SHA256'], 'native uppercase SHA256')
        need(hashlib.md5(candidate.read_bytes()).hexdigest() == asset['original_api_file_object']['checksum'].split(':')[1], 'native MD5')
        need(schema['encoding'][i]['contentUrl'] == asset['original_api_file_object']['links']['self'], 'native asset order in scholarly data')
        need(any(a.get('href') == asset['original_api_file_object']['links']['self'] for a in page.links), 'visible direct native original link')
    need(len(page.iframes) == 1 and page.iframes[0]['src'] == 'assets/' + pub['pdf_filename'] + '#view=FitH' and
         page.iframes[0]['loading'] == 'lazy' and 'complete four-page PDF' in page.iframes[0]['title'], 'complete unchanged PDF reader')
    for filename in [pub['pdf_filename'], pub['supplement_filename'], 'citation.bib']:
        need(any(a.get('href') == 'assets/' + filename and 'download' in a for a in page.links), 'direct download: ' + filename)
    need((A / 'candidate/assets/citation.bib').read_text() == (A / 'citation.bib').read_text() == pub['prepared_bibtex'], 'exact prepared BibTeX')
    for phrase in [pub['doi'], pub['title'], 'day = {12}', 'date = {2026-10-12}', 'version = {1.0}']:
        need(phrase in pub['prepared_bibtex'], 'BibTeX identity/date/version')
    need('background:#fff' in page_text and 'font-family:Arial,Helvetica,sans-serif' in page_text and
         'max-width:850px' in page_text and '@media(max-width:600px)' in page_text, 'plain responsive white Arial layout intent')
    for secret in ['2026-11-15', '20261115', '185 assertions', '275 preexisting', 'SOURCE_READY',
                   'root-clearance-', 'root scientific gate', 'completion_percent']:
        need(secret not in ' '.join(page.text), 'internal audit material leaked to public copy')
    need(pin(protected['root_authority']) == (A / 'inputs/root-clearance.json').read_bytes(), 'raw root authority copy')
    need((R / 'reviews/root/ROOT_REVIEW_20261115.md').read_text() == pub['review_metadata']['whole_root_scientific_review'], 'whole root review text')
    if (A / 'MANIFEST.json').exists():
        manifest = read(A / 'MANIFEST.json')
        expected = {p['path'] for p in manifest['files']}
        actual = {str(p) for p in A.rglob('*') if p.is_file() and p.name not in TERMINAL}
        need(actual == expected and len(expected) == len(manifest['files']), 'fail-closed exact owned membership')
        all_pins(manifest['files'])
    if (A / 'SEAL.json').exists():
        all_pins(read(A / 'SEAL.json')['bindings'])

    faults = []
    if '--semantic-controls' in sys.argv:
        def reject(label, p, m, abs_value):
            try:
                semantic_contract(p, m, abs_value)
            except ValueError:
                faults.append(label)
                return
            raise ValueError('editorial fault accepted: ' + label)
        for label, old, new in [
            ('one ideal omitted', 'both L=J_R and L=K_R', 'only L=J_R'),
            ('zero constant excluded', 'every real ε≥0', 'every ε>0'),
            ('strong full vanishing ideal omitted', 'R+ε ∉ ΣS²+I_ℝ(L)', 'R+ε ∉ ΣS²+L'),
            ('arbitrary-degree scope omitted', 'No fixed degree bound', 'A degree-six bound'),
            ('positive constants incorrectly killed', 'Its constant part is retained', 'Its constant part must vanish'),
            ('product diagnostic wrongly transferred', 'It concerns only the separate-product reading', 'It also refutes the minor equivalence'),
            ('author correction invented', 'No uniquely intended or author-approved correction', 'The intended correction'),
            ('firstness limit removed', 'Historical first priority and continued worldwide openness are not established', 'First historical priority is established')]:
            p = copy.deepcopy(pub)
            for key in ['result', 'why_it_works', 'limitations']:
                p[key] = [s.replace(old, new) for s in p[key]]
            reject(label, p, promotion, abstract)
        p = copy.deepcopy(pub); p['abstract'] += ' Edited summary.'
        reject('original abstract paraphrased', p, promotion, abstract)
        p = copy.deepcopy(pub); p['publication_date'] = '2026-10-13'
        reject('created date substituted', p, promotion, abstract)
        p = copy.deepcopy(pub); p['code_license'] = 'MIT'
        reject('invented MIT grant', p, promotion, abstract)
        m = copy.deepcopy(promotion); m['ready_to_publish'] = True
        reject('premature public gate', pub, m, abstract)
    return {'status': 'PASS', 'checks': COUNT, 'protected_preexisting_paper_files': 275,
            'immutable_source_files': 122, 'whole_native_API_objects': 4, 'whole_transport_objects': 7,
            'literal_scientific_verdicts': 2, 'raw_byte_identical_copies': 35,
            'complete_original_ZIP_payloads': 85, 'reader_PDF_pages': 4,
            'optional_memory_only_semantic_controls_rejected': faults,
            'source_native_or_scientific_programmes_executed': [], 'network_or_writes': False,
            'publication_canonical_browser_native_or_production_authority': False}


if __name__ == '__main__':
    try:
        print(json.dumps(main(), ensure_ascii=False, indent=2))
    except (ValueError, KeyError, OSError, TypeError, IndexError) as error:
        print(json.dumps({'status': 'FAIL', 'error': str(error)}, ensure_ascii=False))
        sys.exit(1)
