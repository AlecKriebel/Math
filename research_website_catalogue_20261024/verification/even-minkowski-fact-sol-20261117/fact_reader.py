"""One private editorial data audit; standard library only, no project imports."""
import datetime
import hashlib
from html import unescape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import stat
import time
import traceback
from urllib.parse import urlsplit, unquote

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P / 'verification/even-minkowski-fact-sol-20261117'
WRITER = P / 'verification/even-minkowski-editorial-sol-20261117'
SOURCE = P / 'papers/23203081/sources'
CLEARANCE = P / 'verification/root-clearance-23203081-20261117.json'
ROOT_REVIEW = P / 'papers/23203081/reviews/root-continuation-20261117/ROOT_REVIEW.md'
PINS = {
    WRITER / 'FINAL.json': 'f4cf5022b4e19301209d8f8337c34bea029f6641e0552ab781f1b6aab90b7cb6',
    WRITER / 'MANIFEST.json': '0facbc135d6de17673134b549fedee4054ceeca1de6ac6d32a9d5fb6ef88ac29',
    WRITER / 'article.html': '0584e50a534125899a98b6dea69d1c61fea70aaeaea966e1d1cc1c719ecadef4',
    WRITER / 'head.html': '223bda8ffa5cdcbbcfb108152fc7253644c2ee6601f7048f31efec206ccc51ff',
    WRITER / 'main.html': '6ad6372bc561c8b17b47e41401e3ba4223019e798039761151ac88b76d84acf1',
    WRITER / 'page-model.json': '7386763d79fa076fefca7a04d404761af5d612c12d1760157fbe46409784bec0',
    WRITER / 'citation.bib': '4e1dfe1fb9a15d305fe49f4f51d53053d98fb314f15143081d3c6b0ecd260f9a',
    SOURCE / 'SOURCE_MANIFEST.json': '8c5a0654a6439a632f286e60dcaec2897edba6d9f6e40eff796962da3da6b8a3',
    SOURCE / 'SOURCE_FINAL.json': 'b5b65ecc9a2cc31bfec3a7e97236b92d8dfebe4a7c5c7ace1f875586dfab9de2',
    CLEARANCE: '008042d4a6d50c8bd0bfdc979db9afeff5c808091aaa2c8be5b4ec25c9dd6ada',
    ROOT_REVIEW: '527f2415f022d84d4344175c3abaedb8057c8006b4f6a184830bdd2eebfce848'
}
CHECKS = []
TERMINALS = {'MANIFEST.json', 'FINAL.json'}


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def need(condition, label):
    if not condition:
        raise AssertionError(label)


def check(label, **data):
    CHECKS.append({'UTC': utc(), 'check': label, **data})


def write(name, data):
    path = OWN / name
    need(path.parent == OWN and not path.exists(), 'fresh direct own output ' + name)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def inventory(root):
    rows = []
    def visit(path):
        st = path.lstat()
        rel = path.relative_to(root).as_posix()
        row = {'path': rel, 'mode': oct(stat.S_IMODE(st.st_mode)),
               'hidden': any(x.startswith('.') and x != '.' for x in Path(rel).parts)}
        if stat.S_ISDIR(st.st_mode):
            children = sorted(path.iterdir(), key=lambda p: os.fsencode(p.name))
            row.update(kind='directory', empty=not children)
            rows.append(row)
            for child in children:
                visit(child)
        else:
            need(stat.S_ISREG(st.st_mode), 'no symlink/special object: ' + str(path))
            data = path.read_bytes()
            need(len(data) == st.st_size, 'stable bytes during read')
            row.update(kind='file', bytes=len(data), SHA256=sha(data), MD5=hashlib.md5(data).hexdigest(), empty=not data)
            rows.append(row)
    visit(root)
    return {'root': str(root), 'files': sum(r['kind'] == 'file' for r in rows),
            'child_directories': sum(r['kind'] == 'directory' for r in rows) - 1, 'entries': rows}


def guards():
    return {'writer': inventory(WRITER), 'source': inventory(SOURCE),
            'controls': {str(p): {'bytes': p.stat().st_size, 'SHA256': sha(p.read_bytes()),
                                  'mode': oct(stat.S_IMODE(p.lstat().st_mode))} for p in [CLEARANCE, ROOT_REVIEW]}}


def authenticate(g):
    for path, pin in PINS.items():
        need(sha(path.read_bytes()) == pin, 'hard pin ' + str(path))
    need((g['writer']['files'], g['writer']['child_directories']) == (23, 1), 'whole writer23/1')
    need((g['source']['files'], g['source']['child_directories']) == (51, 12), 'whole source51/12')
    wm = json.loads((WRITER / 'MANIFEST.json').read_bytes())
    wf = {r['path']: r for r in g['writer']['entries'] if r['kind'] == 'file'}
    wd = {r['path']: r for r in g['writer']['entries'] if r['kind'] == 'directory'}
    need(set(wm['exact_created_terminal_exclusions']) == TERMINALS, 'actual writer terminal schema')
    need(set(wf) == {r['path'] for r in wm['files']} | TERMINALS, 'whole writer finite file topology')
    for r in wm['files']:
        need(all(wf[r['path']][k] == v for k, v in r.items()), 'all writer manifest metadata ' + r['path'])
    need(wd['.']['mode'] == wm['root_mode'] and wd['.']['empty'] == wm['root_empty'], 'writer root topology')
    need(set(wd) == {'.'} | {r['path'] for r in wm['directories']}, 'writer exact child directory topology')
    for r in wm['directories']:
        need(all(wd[r['path']][k] == v for k, v in r.items()), 'writer child directory mode/empty/hidden')
    for name in TERMINALS:
        need(wf[name]['mode'] == '0o644', 'writer terminal mode')
    sm = json.loads((SOURCE / 'SOURCE_MANIFEST.json').read_bytes())
    sr = {r['path']: r for r in g['source']['entries']}
    exclusions = set(sm['excluded_control_files'])
    need(exclusions == {'SOURCE_MANIFEST.json', 'SOURCE_FINAL.json'}, 'actual source terminal schema')
    need(set(sr) == {r['path'] for r in sm['entries']} | exclusions, 'whole source finite topology')
    translation = {'mode_octal': 'mode', 'sha256': 'SHA256', 'md5': 'MD5'}
    for r in sm['entries']:
        need(all(sr[r['path']][translation.get(k, k)] == v for k, v in r.items()), 'all source manifest metadata ' + r['path'])
    need(all(sr[p]['mode'] == '0o644' for p in exclusions), 'source terminal modes')
    clear = json.loads(CLEARANCE.read_bytes())
    need(clear['verdict'] == 'PASS' and clear['root_review_SHA256'] == PINS[ROOT_REVIEW], 'inherited exact root clearance')
    check('whole actual writer/source authenticated with exact terminal schemas', writer_files=23, writer_childdirs=1, source_files=51, source_childdirs=12)


class Document(HTMLParser):
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.root = {'tag': '#document', 'attrs': {}, 'children': []}
        self.stack, self.nodes, self.duplicate_attrs = [self.root], [], []
        self.feed(text)
        self.close()
        need(len(self.stack) == 1, 'complete static HTML nesting')

    def handle_starttag(self, tag, attrs):
        names = [k for k, v in attrs]
        if len(names) != len(set(names)):
            self.duplicate_attrs.append(tag)
        node = {'tag': tag, 'attrs': dict(attrs), 'children': []}
        self.stack[-1]['children'].append(node)
        self.nodes.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        need(len(self.stack) > 1 and self.stack[-1]['tag'] == tag, 'matching explicit HTML close: ' + tag)
        self.stack.pop()

    def handle_data(self, data):
        self.stack[-1]['children'].append(data)


def text(node):
    return ''.join(c if isinstance(c, str) else text(c) for c in node['children'])


def squash(value):
    return ' '.join(value.split())


def audit(g):
    authenticate(g)
    article = (WRITER / 'article.html').read_text()
    head = (WRITER / 'head.html').read_text()
    main = (WRITER / 'main.html').read_text()
    model = json.loads((WRITER / 'page-model.json').read_bytes())
    bib = (WRITER / 'citation.bib').read_text()
    tex = (SOURCE / 'archives/02-source-and-verification.zip.extracted/main.tex').read_text()
    api = json.loads((SOURCE / 'native-metadata/record-api.json').read_bytes())
    metadata = api['metadata']
    parsed = Document(article)
    hp, mp = Document(head), Document(main)
    need(re.search(r'<head>.*?</head>', article, re.S).group() == head.strip(), 'actual whole wrapped HEAD embedded exact')
    need(re.search(r'<main\b.*?</main>', article, re.S).group() == main.strip(), 'actual whole MAIN embedded exact')
    ids = [n['attrs']['id'] for n in parsed.nodes if 'id' in n['attrs']]
    need(len(ids) == len(set(ids)) and not parsed.duplicate_attrs, 'no duplicate actual IDs/attributes')
    by_id = {n['attrs']['id']: n for n in parsed.nodes if 'id' in n['attrs']}
    metas = {}
    for n in hp.nodes:
        if n['tag'] == 'meta' and ('name' in n['attrs'] or 'property' in n['attrs']):
            key = n['attrs'].get('name', n['attrs'].get('property'))
            need(key not in metas, 'no duplicate named static metadata')
            metas[key] = n['attrs']['content']
    scripts = [n for n in parsed.nodes if n['tag'] == 'script']
    need(len(scripts) == 1 and scripts[0]['attrs'].get('type') == 'application/ld+json', 'single JSON-LD script only')
    scholar = json.loads(text(scripts[0]))
    need(scholar['@type'] == 'ScholarlyArticle', 'single Scholar object')
    raw_abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1)
    replacements = {r'$n\ge2$': 'n ≥ 2', r'$0\le p<1$': '0 ≤ p < 1', r'$S^{n-1}$': 'Sⁿ⁻¹',
                    r'$h^{1-p}\det(\nabla^2h+hI)=f$': 'h¹⁻ᵖ det(∇²h+hI)=f',
                    r'$0<p<1$': '0 < p < 1', r'$L_p$': 'Lₚ', r'$p=0$': 'p=0'}
    for a, b in replacements.items():
        raw_abstract = raw_abstract.replace(a, b)
    expected = squash(raw_abstract.replace('--', '–'))
    need('$' not in expected and '\\' not in expected, 'complete independent native abstract rendering')
    surfaces = {'native_rendered': expected, 'ABSTRACT.txt': (WRITER / 'ABSTRACT.txt').read_text().strip(),
                'visible_article': text(by_id['abstract-text']), 'DC.description': metas['DC.description'],
                'JSON-LD.abstract': scholar['abstract'], 'model.abstract': model['abstract']}
    need(all(v == expected for v in surfaces.values()), 'entire abstract exact across all offered surfaces')
    mp_abs = next(n for n in mp.nodes if n['attrs'].get('id') == 'abstract-text')
    need(text(mp_abs) == expected, 'standalone MAIN complete abstract')
    hp_scholar = json.loads(text(next(n for n in hp.nodes if n['tag'] == 'script')))
    need(hp_scholar['abstract'] == expected, 'standalone HEAD complete abstract')
    need(expected != unescape(metadata['description']), 'native Description not substituted for original abstract')
    check('full independently rendered native abstract exact', characters=len(expected), surfaces=list(surfaces) + ['standalone MAIN', 'standalone HEAD'])

    names = [f['key'] for f in api['files']]
    need(names == ['paper.pdf', 'source-and-verification.zip', 'README.md'], 'exact native3asset order')
    need([r['name'] for r in model['native_asset_order']] == names, 'model native asset order')
    need([r['name'] for r in scholar['encoding']] == names and len(scholar['encoding']) == 3, 'single Scholar three encodings exact order')
    asset_rows = []
    for native, modeled, encoded in zip(api['files'], model['native_asset_order'], scholar['encoding']):
        name = native['key']
        a, b = (SOURCE / 'zenodo-files' / name), (WRITER / 'assets' / name)
        data = a.read_bytes()
        need(data == b.read_bytes(), 'actual native asset bytes exact ' + name)
        need(oct(stat.S_IMODE(a.lstat().st_mode)) == oct(stat.S_IMODE(b.lstat().st_mode)) == modeled['mode'], 'asset native mode ' + name)
        need(len(data) == native['size'] == modeled['bytes'] and sha(data) == modeled['SHA256'], 'asset size/SHA identity ' + name)
        need('md5:' + hashlib.md5(data).hexdigest() == native['checksum'] == modeled['native_checksum'], 'asset native checksum ' + name)
        need(encoded['contentUrl'] == modeled['local_path'] == 'assets/' + name, 'asset local encoding path ' + name)
        need(encoded['sameAs'] == modeled['native_url'] == native['links']['self'], 'asset native encoding URL ' + name)
        need(encoded['contentSize'] == str(len(data)) + ' bytes' and encoded['encodingFormat'] == modeled['format'], 'asset encoding metadata ' + name)
        asset_rows.append({'name': name, 'bytes': len(data), 'SHA256': sha(data), 'mode': modeled['mode']})
    native_list = text(by_id['native-assets'])
    need(native_list.find('PDF') < native_list.find('ZIP') < native_list.find('README.md'), 'visible native asset order')
    check('all three original native assets byte/mode/checksum exact', assets=asset_rows)

    need('version' not in metadata and model['native_version'] is None and model['native_API_version_field_absent'], 'native absent API version retained')
    need('version' not in scholar and 'citation_version' not in metas and not re.search(r'\bversion\s*=', bib, re.I), 'no invented schema/citation/Bib version')
    need(model['native_HTML_display_version'] == 'v1' and 'not an author-supplied API version' in model['host_edition_qualification'], 'host-only display label qualified')
    need('no author version field in API metadata' in bib and 'Zenodo displays edition v1' in bib, 'Bib host version qualification')
    for field in ['canonical_url', 'base_url', 'production_url', 'actual_publication_date', 'AA', 'follow_up']:
        need(model[field] is None, 'private actual null field ' + field)
    need(model['publication_authority'] is False and model['rendered_or_live_certificate'] is False, 'no action/live authority')
    need(metas['robots'] == metas['googlebot'] == model['robots'] == 'noindex, nofollow', 'private noindex metadata')
    need(not any(n['tag'] == 'base' or (n['tag'] == 'link' and n['attrs'].get('rel') == 'canonical') for n in parsed.nodes), 'no actual base/canonical HTML')
    need('og:url' not in metas, 'no actual public og:url')
    proposal = model['deployment_proposal']
    need(proposal['path'] == '/research/' + proposal['slug'] + '/' and proposal['proposed_canonical_url'] == 'https://aleckriebel.com' + proposal['path'], 'proposed slug/canonical harmonized')
    need(model['title'] == metadata['title'] == scholar['name'] == metas['citation_title'] == text(by_id['paper-title']), 'all exact titles')
    need(model['publication_date'] == metadata['publication_date'] == scholar['datePublished'] == metas['DC.date'] == '2026-10-06', 'native declared manuscript date')
    need(model['record_created'] == api['created'] == scholar['dateCreated'], 'creation date exact and distinct')
    need(model['record_updated'] == api['updated'] == scholar['dateModified'] == metas['article:modified_time'], 'update date exact')
    need(model['doi'] == api['doi'] == metas['citation_doi'] == scholar['identifier']['value'] and model['doi'] in bib, 'record-specific DOI consistency')
    need(metadata['license']['id'] == 'cc-by-4.0' and scholar['license'] == 'https://creativecommons.org/licenses/by/4.0/', 'native owned CC BY4')
    need(model['rights']['owned_contribution'] == 'CC BY 4.0' and 'third-party' in metas['DC.rights'], 'retained third-party rights')
    need('MIT' not in article + bib and 'Apache' not in article + bib, 'no invented license split')
    check('metadata edition dates DOI rights and private proposal consistent')

    local, fragments, aria, external = [], [], [], []
    for node in parsed.nodes:
        attrs = node['attrs']
        for key in ['aria-labelledby', 'aria-describedby', 'aria-controls']:
            if key in attrs:
                for token in attrs[key].split():
                    need(token in by_id, 'actual ARIA target exists ' + token)
                    aria.append(token)
        for key in ['href', 'src']:
            if key not in attrs:
                continue
            value = attrs[key]
            url = urlsplit(value)
            if url.scheme or url.netloc:
                need(url.scheme == 'https' and url.netloc, 'ordinary static https external link')
                external.append(value)
            elif url.path.startswith('/'):
                need(value == '/research/research.css' and node['tag'] == 'link', 'only declared shared absolute dependency')
                local.append({'path': value, 'status': 'declared shared stylesheet; integration outside scope'})
            elif url.path:
                rel = unquote(url.path)
                need('..' not in Path(rel).parts and (WRITER / rel).is_file(), 'local actual payload exists ' + rel)
                need(rel in {'citation.bib', 'assets/paper.pdf', 'assets/source-and-verification.zip', 'assets/README.md'}, 'only intended public payload local links')
                need(not url.fragment or rel.endswith('.pdf'), 'local non-PDF fragment explicitly checked')
                local.append({'path': rel, 'fragment': url.fragment})
            elif url.fragment:
                need(url.fragment in by_id, 'same-document fragment exists')
                fragments.append(url.fragment)
    styles = [n['attrs'].get('href') for n in parsed.nodes if n['tag'] == 'link' and n['attrs'].get('rel') == 'stylesheet']
    need(styles == ['/research/research.css'] and not any(n['tag'] == 'style' or 'style' in n['attrs'] for n in parsed.nodes), 'shared CSS only')
    need(not any(n['tag'] in ('form', 'input', 'button') for n in parsed.nodes), 'no action/contact UI')
    need(all(not k.startswith('on') for n in parsed.nodes for k in n['attrs']), 'no inline event handlers')
    need(scholar['description'] == model['meta_description'] == metas['description'] == metas['og:description'] == metas['twitter:description'], 'short SEO descriptions consistent')
    check('actual static HTML metadata references and duplicate checks', IDs=len(ids), aria_references=len(aria), fragments=fragments, local_references=local, external_links_static_only=len(external))

    visible = squash(text(mp.root))
    needed = ['strictly positive even', 'support function', 'n ≥ 2', '0 ≤ p < 1', '0 < p < 1 only',
              'full-dimensional origin-symmetric', 'unnormalized', 'No volume-one condition', 'n−p',
              'local smooth support-function path', 'n+1', 'both extrema', 'atomic', 'outside the smooth strictly positive density class',
              'Böröczky–Lutwak–Yang–Zhang', 'He–Liu', 'Bianchi–Böröczky–Colesanti–Yang', 'Chou–Wang',
              'Stancu', 'CC BY 4.0', 'Cited third-party works retain their own rights',
              'unrefereed, AI-assisted preprint', 'not conventional human peer review', 'authorship would be based on actual contributions']
    for phrase in needed:
        need(phrase in visible, 'cleared scope/credit/limit retained: ' + phrase)
    need('adc7f1241b42e322a6451854ab7e4b4c146bf78a' in visible, 'exact pinned primary credit')
    need('2026-11-17' not in visible and not re.search(r'\bPASS\b|\b450\b|\b2100\b|\bkernel verified\b', visible), 'no dated review replay/internal counts/fresh certificate')
    need('No reproduced Lean kernel/axiom/Comparator certification or formalization' in visible, 'formal limit explicit')
    need('no new inequality, transfer or first-public-announcement claim' in visible, 'attributed consequence status explicit')
    check('manually read mathematical scope and public status mirrored in static data', new_scientific_verdict=False)
    return {'schema': 'independent-even-minkowski-editorial-fidelity-data-v1', 'UTC': utc(), 'status': 'PASS_EDITORIAL_FIDELITY',
            'checks': CHECKS, 'findings': [], 'scientific_PASS_inherited': True, 'new_scientific_verdict': False,
            'static_only_no_browser_or_live_certificate': True, 'follow_up': None, 'action_authority': False}


started, tick = utc(), time.monotonic()
before = guards()
write('GUARDS_BEFORE.json', before)
try:
    try:
        result = audit(before)
    finally:
        after = guards()
        write('GUARDS_AFTER.json', after)
    need(before == after, 'complete writer/source/control before-after preservation')
    result['complete_before_after_bytes_modes_hidden_empty_topology_preserved'] = True
    write('DATA_AUDIT.json', result)
    write('EXECUTION.json', {'argv': ['/usr/bin/python3', 'fact_reader.py'], 'started_UTC': started,
                             'finished_UTC': utc(), 'elapsed_seconds_before_seal': time.monotonic() - tick,
                             'invocations': 1, 'exit_code': 0, 'stdout_bytes': 0, 'stderr_bytes': 0,
                             'saved_source_personally_read_before_invocation': True, 'scientific_source_helper_executions': 0,
                             'retries': 0, 'follow_up': None})
    (OWN / 'REPORT.md').write_text('Private editorial-fidelity PASS; no concrete copy defect found. Scientific PASS is inherited, not renewed.\n\n' + (OWN / 'MANUAL_FINDINGS.md').read_text() + '\nThe single fully read data-only auditor exited0 with empty stdout/stderr. All offered abstract surfaces match the independently rendered complete native abstract. All three native assets, metadata and static references passed. Entire writer23/1 and source51/12 byte/mode/hidden/empty topology and root controls remained exact before/after. Shared CSS integration, external-link availability and browser/live rendering remain outside this static review. No writer/source mutation, scientific/source/producer/helper execution, import, AST, compiler, test, Git, W, network, Sheet, deployment, AA, redirect, contact or children. Completion100%; follow_up=null.\n')
    with (OWN / 'RESEARCH_LOG.md').open('a') as log:
        log.write('\n' + utc() + ' — One fully read data-only auditor exited0; complete guards/abstract/asset/static checks passed. Editorial completion100%; no new scientific verdict. Finite sealing then stop; follow_up=null.\n')
    for name in TERMINALS:
        need(not (OWN / name).exists(), 'exact own terminal absent before seal')
    for name in sorted(TERMINALS):
        fd = os.open(str(OWN / name), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        os.close(fd)
    own = inventory(OWN)
    manifest_rows = []
    for row in own['entries']:
        if row['path'] in TERMINALS:
            row = {k: v for k, v in row.items() if k not in ('bytes', 'SHA256', 'MD5', 'empty')}
            row['terminal_control'] = True
        manifest_rows.append(row)
    manifest = {'schema': 'finite-private-even-minkowski-fact-manifest-v1', 'UTC': utc(), 'root': str(OWN),
                'regular_files': own['files'], 'child_directories': own['child_directories'], 'entries': manifest_rows,
                'exact_already_created_terminal_recursive_hash_exclusions': sorted(TERMINALS), 'other_exclusions': [],
                'all_actual_hidden_empty_modes_topology_included': True, 'completion_percent': 100}
    (OWN / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    final = {'schema': 'private-even-minkowski-fact-FINAL-v1', 'UTC': utc(), 'status': 'PASS_EDITORIAL_FIDELITY_FROZEN',
             'completion_percent': 100, 'root': str(OWN), 'regular_files': own['files'], 'child_directories': own['child_directories'],
             'manifest_SHA256': sha((OWN / 'MANIFEST.json').read_bytes()), 'DATA_AUDIT_SHA256': sha((OWN / 'DATA_AUDIT.json').read_bytes()),
             'reader_SHA256': sha((OWN / 'fact_reader.py').read_bytes()), 'writer_FINAL_SHA256': PINS[WRITER / 'FINAL.json'],
             'writer_MANIFEST_SHA256': PINS[WRITER / 'MANIFEST.json'], 'source_FINAL_SHA256': PINS[SOURCE / 'SOURCE_FINAL.json'],
             'source_MANIFEST_SHA256': PINS[SOURCE / 'SOURCE_MANIFEST.json'], 'root_clearance_SHA256': PINS[CLEARANCE],
             'root_review_SHA256': PINS[ROOT_REVIEW], 'writer_extent': [23, 1], 'source_extent': [51, 12],
             'all_before_after_bytes_modes_hidden_empty_topology_exact': True, 'native_version': None,
             'scientific_PASS_inherited': True, 'new_scientific_verdict': False, 'concrete_findings': [],
             'own_reader_invocations': 1, 'own_reader_exit_code': 0, 'stdout_bytes': 0, 'stderr_bytes': 0,
             'no_browser_live_CSS_integration_or_external_availability_certificate': True,
             'source_scientific_producer_helper_import_AST_compiler_test_execution': 0,
             'W_Git_network_Sheet_deploy_AA_redirect_contact_children_other_packet_mutations': 0,
             'action_authority': False, 'follow_up': None, 'frozen_stop': True}
    (OWN / 'FINAL.json').write_text(json.dumps(final, indent=2, sort_keys=True) + '\n')
except BaseException as error:
    write('FAILURE.json', {'UTC': utc(), 'started_UTC': started, 'elapsed_seconds': time.monotonic() - tick,
                           'status': 'FAIL_STOP_NO_RETRY', 'error_type': type(error).__name__, 'error': str(error),
                           'traceback': traceback.format_exc(), 'checks_completed': CHECKS, 'follow_up': None})
    raise
