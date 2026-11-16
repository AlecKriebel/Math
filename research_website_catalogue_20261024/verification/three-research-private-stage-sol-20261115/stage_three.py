#!/usr/bin/env python3
"""Fixed three-paper private overlay. Default is read-only verification.

--prepare exclusively creates candidate/ and BUILD_RECEIPT.json here. --seal
exclusively creates two final controls here after actual normal/O checks.
No Git, network, subprocess, source imports, science, installs or outside writes.
"""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.parse import urlsplit
import copy, datetime, fnmatch, hashlib, json, os, re, stat, struct, sys
import xml.etree.ElementTree as ET

N = Path(__file__).absolute().parent
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
PLAN_SHA = '617cc96e28c2c43e9c389734a888f261fe1b465c3e83a65973b0b0fe5b796dac'
TERMS = {'OWNED_MANIFEST.json', 'FINAL_SEAL.json'}
ALLOWED = {}
CHECKS = 0

def need(ok, reason):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(reason)

def pin(data):
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest()}

def read(path):
    path = Path(path)
    need(path.is_absolute() and '..' not in path.parts, 'canonical absolute input')
    need(path.is_relative_to(N) or path.is_relative_to(W) or str(path) in ALLOWED, 'bounded input')
    for parent in path.parents:
        need(not parent.is_symlink(), 'no symlink ancestor')
    first = path.lstat()
    need(stat.S_ISREG(first.st_mode), 'regular input ' + str(path))
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        opened = os.fstat(fd)
        need((first.st_dev, first.st_ino) == (opened.st_dev, opened.st_ino), 'open identity')
        chunks = []
        while True:
            block = os.read(fd, 1048576)
            if not block:
                break
            chunks.append(block)
        last = os.fstat(fd)
        final = path.lstat()
        need((opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns) == (last.st_size, last.st_mtime_ns, last.st_ctime_ns), 'stable whole read')
        need((opened.st_dev, opened.st_ino) == (final.st_dev, final.st_ino), 'stable pathname')
        data = b''.join(chunks)
        need(len(data) == opened.st_size, 'complete buffer')
        if str(path) in ALLOWED:
            need(pin(data) == ALLOWED[str(path)], 'bound external pin')
        return data
    finally:
        os.close(fd)

def obj(path):
    return json.loads(read(path))

def bound(row):
    value = {key: row[key] for key in ['bytes', 'SHA256']}
    need(str(Path(row['path'])) == row['path'], 'literal bound pathname')
    need(row['path'] not in ALLOWED or ALLOWED[row['path']] == value, 'no conflicting pin')
    ALLOWED[row['path']] = value
    return read(Path(row['path']))

def typed(a, b):
    need(type(a) is type(b), 'literal JSON type')
    if type(a) is dict:
        need(list(a) == list(b), 'literal JSON key order')
        for key in a:
            typed(a[key], b[key])
    elif type(a) is list:
        need(len(a) == len(b), 'literal JSON list extent')
        for x, y in zip(a, b):
            typed(x, y)
    else:
        need(a == b, 'literal JSON scalar/null/history')

def new(path, data):
    need(path.is_relative_to(N), 'owned writes only')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as target:
        need(target.write(data) == len(data), 'complete exclusive write')
        target.flush()
        os.fsync(target.fileno())

def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags, self.ids = [], []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])

def load_contract():
    raw = read(N / 'PRIVATE_STAGE_PLAN.json')
    need(pin(raw)['SHA256'] == PLAN_SHA, 'fixed additive19path plan')
    plan = json.loads(raw)
    ref = json.loads(bound(plan['original_reference_inputs']))
    base = json.loads(bound(plan['original_baseline']))
    scope = json.loads(bound(plan['root_private_hosting_scope']))
    need(scope['private_candidate_assembly_authorized_after_root_forwarding'] is True and scope['W_mutation_authority'] is False, 'private authority only')
    need([row['record_id'] for row in ref['records']] == plan['fixed_records'] == ['23418581', '23202966', '23205305'], 'fixed three only')
    need(plan['total_W_paths'] == 19 and plan['public_overlay_count'] == 18 and plan['virtual_counts'] == [647, 99, 100], 'exact additive scope')
    return plan, ref, base

def expected(plan, ref, base):
    outputs, details = {}, []
    baseline_files = {row['path']: {key: row[key] for key in ['bytes', 'SHA256']} for row in base['public_files']}
    def cached(name):
        data = read(N / 'raw/public' / name)
        need(pin(data) == baseline_files[name], 'original native cache pin')
        return data
    frame = cached('research/five-outgoing-centers-alpha16/index.html').decode()
    css = cached('research/research.css')
    need(b'background: #fff' in css and b'Arial, Helvetica, sans-serif' in css, 'actual native white Arial style')
    prefix = frame.split('<body>', 1)[1].split('<main ', 1)[0]
    suffix = frame.rsplit('</main>', 1)[1]
    style = re.search(r'<style>(.*?)</style>', frame, re.S).group(1)
    style += 'main .table-wrap{overflow-x:auto}main .formula{white-space:pre-wrap;overflow-wrap:anywhere}'
    for row in ref['records']:
        config = json.loads(bound(row['approved_config']))
        main = bound(row['approved_MAIN'])
        source_head = bound(row['approved_head_source']).decode()
        need(main.startswith(('<main id="' + row['semantic_main_id'] + '">').encode()), 'whole approved semantic MAIN')
        if row['record_id'] == '23418581':
            source_head = source_head.split('</head>', 1)[0]
            title, date, doi = config['title'], config['publication_date'], config['doi']
        else:
            title, date, doi = config['title'], config['publication']['datePublished'], config['publication']['DOI']
        url = row['proposed_article_URL']
        need(url == 'https://aleckriebel.com/research/' + row['slug'] + '/', 'exact proposed URL')
        parsed = Page(); parsed.feed(source_head)
        names = [(attrs['name'], attrs['content']) for tag, attrs in parsed.tags if tag == 'meta' and 'name' in attrs]
        props = [(attrs['property'], attrs['content']) for tag, attrs in parsed.tags if tag == 'meta' and 'property' in attrs]
        need(len(dict(names)) == len(names) and len(dict(props)) == len(props), 'unique original head metadata')
        description = dict(names)['description']
        names = [(key, 'index,follow' if key == 'robots' else url + 'paper.pdf' if key == 'citation_pdf_url' else value) for key, value in names]
        for key, value in [('author', 'Alec Kriebel'), ('citation_author_orcid', 'https://orcid.org/0009-0001-9320-500X'), ('citation_language', 'en'), ('twitter:card', 'summary')]:
            if key not in dict(names): names.append((key, value))
        props = [(key, url if key == 'og:url' else value) for key, value in props]
        for key, value in [('og:type', 'article'), ('og:title', title), ('og:description', description), ('og:url', url), ('og:site_name', 'Alec Kriebel'), ('article:published_time', date)]:
            if key not in dict(props): props.append((key, value))
        need(dict(names)['citation_doi'] == doi and dict(names)['citation_publication_date'] == date.replace('-', '/'), 'original scholarly identity/date')
        need(('citation_version' in dict(names)) == (row['record_id'] == '23418581'), 'original version presence preserved')
        source_ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', source_head, re.S).group(1))
        article = copy.deepcopy(source_ld)
        article.update({'@id': url + '#article', 'url': url, 'mainEntityOfPage': {'@id': url + '#page'}, 'isAccessibleForFree': True})
        if 'creativeWorkStatus' not in article: article['creativeWorkStatus'] = 'Unrefereed preprint'
        if 'description' not in article: article['description'] = description
        assets = row['native_assets_in_original_order']
        media_key = 'encoding' if 'encoding' in article else 'associatedMedia'
        media_before = copy.deepcopy(article[media_key])
        native = {asset['original_api_file_object']['key']: asset for asset in assets}
        need(len(article[media_key]) == len(native), 'all original scholarly media')
        for media in article[media_key]:
            name = Path(urlsplit(media['contentUrl']).path).name
            need(name in native, 'original media filename')
            media['contentUrl'] = url + name
            media['sameAs'] = native[name]['original_api_file_object']['links']['self']
        for before, after in zip(media_before, article[media_key]):
            typed(before, {key: value for key, value in after.items() if key != 'sameAs'} | ({'contentUrl': before['contentUrl']} if 'contentUrl' in before else {}))
        for key in source_ld:
            if key not in ['@id', 'url', media_key]: typed(source_ld[key], article[key])
        webpage = {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': title, 'dateCreated': plan['preparation_date_UTC'], 'dateModified': plan['preparation_date_UTC'], 'mainEntity': {'@id': url + '#article'}}
        schema = {'@context': 'https://schema.org', '@graph': [webpage, article]}
        title_html = re.search(r'<title>(.*?)</title>', source_head, re.S).group(1)
        head = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>' + title_html + '</title>\n'
        head += ''.join('<meta name="' + escape(key, quote=True) + '" content="' + escape(value, quote=True) + '">\n' for key, value in names if key != 'viewport')
        head += '<link rel="canonical" href="' + url + '">\n<link rel="icon" href="/favicon.ico">\n<link rel="stylesheet" href="/research/research.css">\n'
        head += ''.join('<meta property="' + escape(key, quote=True) + '" content="' + escape(value, quote=True) + '">\n' for key, value in props)
        head += '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c') + '</script>\n<style>' + style + '</style>\n</head>\n<body>'
        body_prefix = prefix.replace('href="#main"', 'href="#' + row['semantic_main_id'] + '"')
        page = head.encode() + body_prefix.encode() + main + suffix.encode()
        root = 'public/research/' + row['slug'] + '/'
        for asset in assets:
            name = asset['original_api_file_object']['key']
            data = bound(asset)
            need(hashlib.md5(data).hexdigest() == asset['original_api_file_object']['checksum'].removeprefix('md5:'), 'whole native checksum')
            outputs[root + name] = data
        outputs[root + 'citation.bib'] = bound(row['approved_Bib'])
        outputs[root + 'index.html'] = page
        details.append({'record_id': row['record_id'], 'title': title, 'date': date, 'doi': doi, 'url': url, 'description': description, 'native_asset_order': list(native), 'whole_MAIN': pin(main), 'source_scholarly_metadata': source_ld, 'stage_scholarly_metadata': article, 'native_header_prefix': body_prefix, 'native_footer_suffix': suffix})
    index = cached('research/index.html').decode()
    match = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', index, re.S)
    old_script = match.group(2)
    collection = json.loads(old_script)
    need(collection['mainEntity']['numberOfItems'] == len(collection['mainEntity']['itemListElement']) == 96, 'actual original96 inventory')
    need(old_script.endswith(']}}') and old_script.count('"numberOfItems": 96') == 1, 'exact native JSON append boundary')
    items = [{'@type': 'ListItem', 'position': 97 + number, 'url': detail['url'], 'name': detail['title']} for number, detail in enumerate(details)]
    appended = ', ' + json.dumps(items, ensure_ascii=False)[1:-1]
    new_script = old_script.replace('"numberOfItems": 96', '"numberOfItems": 99', 1)[:-3] + appended + ']}}'
    new_collection = json.loads(new_script)
    restored = copy.deepcopy(new_collection); restored['mainEntity']['numberOfItems'] = 96; del restored['mainEntity']['itemListElement'][96:]
    typed(collection, restored)
    entries = ''
    for detail in details:
        date = datetime.date.fromisoformat(detail['date'])
        label = str(date.day) + ' ' + date.strftime('%B %Y')
        relative = urlsplit(detail['url']).path
        entries += '      <li><a href="' + relative + '">' + escape(detail['title']) + '</a><br><span class="entry-meta">' + label + ' · Unrefereed preprint</span><p>' + escape(detail['description']) + '</p><p><a href="' + relative + 'paper.pdf">PDF</a> · <a href="https://doi.org/' + detail['doi'] + '">Zenodo</a></p></li>\n'
    need(index.count('    </ul>') == 1, 'exact native HTML list append boundary')
    new_index = (index[:match.start(2)] + new_script + index[match.end(2):]).replace('    </ul>', entries + '    </ul>', 1)
    need(new_index.replace(entries, '', 1).replace(new_script, old_script, 1) == index, 'all original index bytes recover exactly')
    outputs['public/research/index.html'] = new_index.encode()
    sitemap = cached('research/sitemap.xml').decode()
    need(sitemap.count('</urlset>') == 1 and len(ET.fromstring(sitemap)) == 97, 'actual original97 sitemap')
    additions = ''.join('  <url><loc>' + detail['url'] + '</loc><lastmod>' + plan['preparation_date_UTC'] + '</lastmod></url>\n' for detail in details)
    new_sitemap = sitemap.replace('</urlset>', additions + '</urlset>', 1)
    need(new_sitemap.replace(additions, '', 1) == sitemap, 'all original sitemap bytes recover exactly')
    outputs['public/research/sitemap.xml'] = new_sitemap.encode()
    original_firebase = read(N / 'raw/controls/firebase.json')
    firebase = bound(plan['root_exact_proposed_firebase'])
    line = b'      "**/README.md",\n'
    need(original_firebase.count(line) == 1 and firebase == original_firebase.replace(line, b'', 1), 'only root-authorized README ignore line removed')
    original_config, config = json.loads(original_firebase), json.loads(firebase)
    restored_config = copy.deepcopy(config); restored_config['hosting']['ignore'].insert(original_config['hosting']['ignore'].index('**/README.md'), '**/README.md')
    typed(original_config, restored_config)
    for path in plan['public_overlay_paths']:
        need(not any(fnmatch.fnmatchcase(path, pattern) for pattern in config['hosting']['ignore']), 'proposed hosting serves every overlay')
    outputs['firebase.json'] = firebase
    need(set(outputs) == set(plan['W_overlay_paths']) and len(outputs) == 19, 'exact19 website-relative paths')
    new_paths = [name for name in outputs if name.startswith('public/') and name[7:] not in baseline_files]
    need(len(new_paths) == 16 and len(baseline_files) + len(new_paths) == 647, 'exact16 absent new leaves; virtual647public')
    return outputs, details

def extent(root):
    files, directories = [], []
    def visit(directory):
        first = directory.lstat(); need(stat.S_ISDIR(first.st_mode), 'ordinary directory')
        for path in sorted(directory.iterdir()):
            name = path.relative_to(root).as_posix(); mode = path.lstat().st_mode
            if stat.S_ISDIR(mode): directories.append(name); visit(path)
            elif stat.S_ISREG(mode): files.append({'path': name, **pin(read(path))})
            else: raise ValueError('special namespace entry ' + name)
        last = directory.lstat()
        need((first.st_dev, first.st_ino, first.st_mtime_ns, first.st_ctime_ns) == (last.st_dev, last.st_ino, last.st_mtime_ns, last.st_ctime_ns), 'stable directory enumeration')
    visit(root)
    return sorted(files, key=lambda row: row['path']), sorted(directories)

def fence(base):
    files, directories = extent(W / 'public')
    typed(files, base['public_files']); typed(directories, base['public_directories'])
    for row in base['site_and_Git_controls']:
        need(pin(read(Path(row['path']))) == {key: row[key] for key in ['bytes', 'SHA256']}, 'all original site/Git controls unchanged')
    index = read(W / '.git/index')
    need(index == read(N / 'raw/shared-index.before'), 'entire native index unchanged after private assembly')
    need(stat.S_IMODE((W / '.git/index').stat().st_mode) == 0o600, 'actual prior native index0600')
    need(index[:4] == b'DIRC' and struct.unpack('>II', index[4:12]) == (2, 58571) and hashlib.sha1(index[:-20]).digest() == index[-20:], 'whole58571 native records/checksum')
    need(not os.path.lexists(W / '.git/index.lock'), 'no native index lock')

def verify(plan, ref, base, outputs, details):
    files, directories = extent(N / 'candidate')
    need(files == [{'path': name, **pin(data)} for name, data in sorted(outputs.items())], 'exact complete candidate files/buffers')
    expected_dirs = sorted({str(parent) for name in outputs for parent in Path(name).parents if str(parent) != '.'})
    need(directories == expected_dirs, 'exact candidate directories')
    for row, detail in zip(ref['records'], details):
        relative = 'public/research/' + row['slug'] + '/index.html'
        data = read(N / 'candidate' / relative)
        main = bound(row['approved_MAIN'])
        need(data.count(main) == 1, 'entire whole approved MAIN appears once')
        page = Page(); page.feed(data.decode())
        need(len(page.ids) == len(set(page.ids)), 'unique page IDs')
        need([attrs.get('id') for tag, attrs in page.tags if tag == 'main'] == [row['semantic_main_id']], 'one semantic MAIN')
        need([attrs.get('href') for tag, attrs in page.tags if tag == 'a' and attrs.get('class') == 'skip-link'] == ['#' + row['semantic_main_id']], 'matching native skip anchor')
        metas = {attrs.get('name'): attrs.get('content') for tag, attrs in page.tags if tag == 'meta' and 'name' in attrs}
        need(metas['robots'] == 'index,follow' and metas['citation_pdf_url'] == detail['url'] + 'paper.pdf', 'proposed production discovery head')
        need([attrs['href'] for tag, attrs in page.tags if tag == 'link' and attrs.get('rel') == 'canonical'] == [detail['url']], 'one exact proposed canonical')
        for tag, attrs in page.tags:
            if tag in ('iframe', 'a'):
                link = attrs.get('src') if tag == 'iframe' else attrs.get('href')
                if link and not urlsplit(link).scheme and not link.startswith(('/', '#')):
                    target = 'public/research/' + row['slug'] + '/' + urlsplit(link).path
                    need(target in outputs, 'every relative reader/download target present')
                if tag == 'iframe': need(attrs.get('title') and link.endswith('#view=FitH'), 'original titled FitH reader')
    need(len(ET.fromstring(outputs['public/research/sitemap.xml'])) == 100, 'virtual100 research sitemap')
    fence(base)
    if (N / 'FINAL_SEAL.json').exists():
        seal = obj(N / 'FINAL_SEAL.json'); manifest_raw = read(N / 'OWNED_MANIFEST.json'); manifest = json.loads(manifest_raw)
        need(pin(manifest_raw) == seal['manifest'], 'whole final manifest')
        owned_files, owned_dirs = extent(N)
        need([row for row in owned_files if row['path'] not in TERMS] == manifest['files'] and owned_dirs == manifest['directories'], 'strict entire final owned namespace')
        need(manifest['exact_root_terminal_exclusions'] == sorted(TERMS) and manifest['subtree_or_future_exclusions'] == [], 'only two exact root controls excluded')
    return {'status': 'PRIVATE_THREE_STAGE_VERIFIED', 'checks': CHECKS, 'public_overlay_paths': 18, 'nonpublic_config_paths': 1, 'total_W_paths': 19, 'new_public_leaves': 16, 'virtual_counts': [647, 99, 100], 'whole_MAIN_bytes': sum(detail['whole_MAIN']['bytes'] for detail in details), 'native_assets_unchanged': 10, 'current_public631_and_native58571_unchanged': True, 'root_stage_adopted': False, 'production_authority': False, 'canonical_url': None, 'AA': None, 'follow_up': None, 'writes': 0, 'network_requests': 0}

def main():
    need(sys.argv[1:] in [[], ['--prepare'], ['--seal']], 'finite explicit modes')
    plan, ref, base = load_contract()
    outputs, details = expected(plan, ref, base)
    if sys.argv[1:] == ['--prepare']:
        need(not (N / 'candidate').exists() and not (N / 'BUILD_RECEIPT.json').exists() and not (N / 'FINAL_SEAL.json').exists(), 'new candidate only; preserve failed attempts')
        fence(base)
        for name, data in outputs.items(): new(N / 'candidate' / name, data)
        receipt = {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status': 'PRIVATE_THREE_STAGE_PREPARED', 'plan': pin(read(N / 'PRIVATE_STAGE_PLAN.json')), 'files': [{'path': name, **pin(data)} for name, data in sorted(outputs.items())], 'details': details, 'only_owned_candidate_and_receipt_written': True, 'whole_MAIN_bytes': 40599, 'production_authority': False, 'canonical_url': None, 'AA': None, 'follow_up': None}
        new(N / 'BUILD_RECEIPT.json', encoded(receipt))
        print(json.dumps({'status': 'PRIVATE_THREE_STAGE_PREPARED', 'owned_files_written': 20, 'verification': verify(plan, ref, base, outputs, details), 'outside_writes': 0}, sort_keys=True))
    elif sys.argv[1:] == ['--seal']:
        need(not any((N / name).exists() for name in TERMS), 'exclusive final controls')
        result = verify(plan, ref, base, outputs, details)
        runs = obj(N / 'ACTUAL_CURRENT_PRESEAL_RUNS.json')
        need(runs['helper'] == {'path': str(N / 'stage_three.py'), **pin(read(N / 'stage_three.py'))}, 'actual preseal runs bind current complete helper')
        need([row['label'] for row in runs['runs']] == ['normal', 'optimized'], 'actual distinct normal/O modes')
        need(len(runs['runs']) == 2 and all(row['exit_code'] == 0 and row['stderr']['bytes'] == 0 and row['result']['status'] == 'PRIVATE_THREE_STAGE_VERIFIED' for row in runs['runs']), 'actual normal/O preseal passes')
        for name in ['REPORT.md', 'VERDICT.json', 'FINAL_CODE_READS.json', 'FINAL_EXECUTION_LEDGER.json']: read(N / name)
        files, directories = extent(N)
        manifest = {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'files': files, 'directories': directories, 'exact_root_terminal_exclusions': sorted(TERMS), 'subtree_or_future_exclusions': []}
        manifest_raw = encoded(manifest)
        new(N / 'OWNED_MANIFEST.json', manifest_raw)
        seal = {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status': 'PRIVATE_FIXED_THREE_STAGE_FINAL_PENDING_INDEPENDENT_AUDITS_AND_ROOT_ADOPTION', 'manifest': pin(manifest_raw), 'payload_files': len(files), 'total_owned_files': len(files) + 2, 'directories': len(directories), 'fixed_records': plan['fixed_records'], 'public_overlay_paths': 18, 'nonpublic_config_paths': 1, 'total_W_paths': 19, 'virtual_counts': [647, 99, 100], 'whole_MAIN_bytes': 40599, 'native_assets': 10, 'all58571_native_index_records_unchanged_since_restoration': True, 'historical18publicscope_protected_native_records_expectation': 58569, 'proposed19path_protected_native_records_expectation': 58568, 'old_INITIAL_and_failed_capture_history_preserved': True, 'root_stage_adopted': False, 'independent_integration_audit': None, 'production_install_authority': False, 'publication_authority': False, 'canonical_url': None, 'AA': None, 'follow_up': None, 'bounded_private_preparation_percent': 100}
        new(N / 'FINAL_SEAL.json', encoded(seal))
        print(json.dumps({'status': seal['status'], 'FINAL_SEAL': pin(read(N / 'FINAL_SEAL.json')), 'OWNED_MANIFEST': pin(manifest_raw), 'total_owned_files': len(files) + 2, 'directories': len(directories), 'production_authority': False}, sort_keys=True))
    else:
        print(json.dumps(verify(plan, ref, base, outputs, details), sort_keys=True))

if __name__ == '__main__':
    main()
