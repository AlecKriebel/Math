"""Fixed private14-buffer assembly; default verifies offline, --build writes owned candidate only."""
from pathlib import Path
from html.parser import HTMLParser
import copy
import datetime
import hashlib
import html
import json
import re
import stat
import sys

O = Path(__file__).resolve().parent
INPUT_SHA = '870ff0a54ff8f67a95410acddcca698a3002acb0de288b756633debfd74396a2'


def checked(p):
    b = Path(p['path']).read_bytes()
    assert len(b) == p['bytes'] and hashlib.sha256(b).hexdigest() == p['SHA256'], p['path']
    if 'mode' in p:
        assert oct(stat.S_IMODE(Path(p['path']).stat().st_mode)) == p['mode']
    return b


def head(root):
    ref = (root / '.git/HEAD').read_text().strip().removeprefix('ref: ')
    p = root / '.git' / ref
    return p.read_text().strip() if p.exists() else next(x.split(' ', 1)[0] for x in (root / '.git/packed-refs').read_text().splitlines() if x.endswith(' ' + ref))


def fragment(data):
    return re.search(rb'<main\b[^>]*>.*?</main>', data, re.S).group()


def abstract(data):
    section = re.search(rb'<section id="original-abstract".*?</section>', data, re.S).group()
    p = re.search(rb'<p>(.*?)</p>', section, re.S).group(1).decode()
    return ' '.join(html.unescape(re.sub('<[^>]+>', '', p)).split())


def typed(data):
    match = re.search(rb'<script type="application/ld\+json">(.*?)</script>', data, re.S)
    text = match.group(1).decode()
    obj = json.loads(text)
    array = obj['mainEntity']['itemListElement']
    i = text.index('[', text.index('"itemListElement"')) + 1
    raw = []
    for item in array:
        while text[i].isspace() or text[i] == ',':
            i += 1
        value, end = json.JSONDecoder().raw_decode(text, i)
        assert value == item
        raw.append(text[i:end].encode())
        i = end
    return match, text, obj, raw, i


class Links(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs, self.ids, self.meta, self.links = [], [], {}, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag in ('a', 'link', 'iframe'):
            self.refs.append(a.get('href', a.get('src')))
        if tag == 'meta':
            self.meta[a.get('name', a.get('property'))] = a.get('content')
        if tag == 'link':
            self.links.append(a)


def wrapper(a):
    main = fragment(checked(a['source_page']))
    assert len(main) == a['MAIN_bytes'] and hashlib.sha256(main).hexdigest() == a['MAIN_SHA256']
    canonical = a['canonical']
    schema = copy.deepcopy(a['source_schema'])
    schema.update({'@id': canonical + '#article', 'url': canonical, 'mainEntityOfPage': {'@type': 'WebPage', '@id': canonical}})
    schema['encoding'] = [{'@type': 'MediaObject', 'name': x['name'], 'encodingFormat': 'application/pdf' if x['name'].endswith('.pdf') else 'application/zip', 'contentUrl': canonical + x['name'], 'contentSize': str(x['source']['bytes']) + ' bytes', 'sameAs': x['native_url']} for x in a['assets']]
    fields = [('description', a['description']), ('robots', 'index, follow, max-image-preview:large'), ('author', 'Alec Kriebel'), ('citation_title', a['title']), ('citation_author', 'Alec Kriebel'), ('citation_author_orcid', 'https://orcid.org/0009-0001-9320-500X'), ('citation_publication_date', a['publication_date'].replace('-', '/')), ('citation_date', a['publication_date'].replace('-', '/')), ('citation_version', a['native_version']), ('citation_doi', a['DOI']), ('citation_pdf_url', canonical + a['assets'][0]['name']), ('citation_language', 'en'), ('DC.title', a['title']), ('DC.description', a['abstract']), ('DC.identifier', 'doi:' + a['DOI']), ('DC.rights', a['rights']), ('twitter:card', 'summary'), ('twitter:title', a['title']), ('twitter:description', a['description'])]
    lines = ['<!DOCTYPE html>', '<html lang="en">', '<head>', '<meta charset="utf-8">', '<meta name="viewport" content="width=device-width, initial-scale=1">', '<title>' + html.escape(a['SEO_title']) + '</title>']
    lines += ['<meta name="' + k + '" content="' + html.escape(v, quote=True) + '">' for k, v in fields]
    lines += ['<meta property="' + k + '" content="' + html.escape(v, quote=True) + '">' for k, v in [('og:type', 'article'), ('og:title', a['title']), ('og:description', a['description']), ('og:url', canonical), ('og:site_name', 'Alec Kriebel'), ('article:published_time', a['publication_date'])]]
    lines += ['<link rel="canonical" href="' + canonical + '">', '<link rel="icon" href="/favicon.ico">', '<link rel="stylesheet" href="/research/research.css">', '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c') + '</script>', '</head>', '<body>', '<a class="skip-link" href="#main">Skip to content</a>', '<header><p class="site-title"><a href="/">Alec Kriebel</a></p><nav aria-label="Main navigation"><a href="/">Home</a> · <a href="/research/">Research</a></nav></header>']
    return ('\n'.join(lines) + '\n').encode() + main + b'\n<footer><p><a href="/research/">Research</a></p><p class="copyright">\xc2\xa9 2013\xe2\x80\x932026 Kriebel LLC</p></footer>\n</body>\n</html>\n'


def assemble(inputs):
    result = {}
    for a in inputs['articles']:
        prefix = 'public/research/' + a['slug'] + '/'
        result[prefix + 'index.html'] = wrapper(a)
        result[prefix + 'citation.bib'] = checked(a['source_Bib'])
        for asset in a['assets']:
            result[prefix + asset['name']] = checked(asset['source'])
    old = (O / 'BASELINE_RESEARCH_INDEX.html').read_bytes()
    sm, text, obj, raw, end = typed(old)
    additions, visible = [], []
    for position, a in enumerate(inputs['articles'], 112):
        additions.append({'@type': 'ListItem', 'position': position, 'url': a['canonical'], 'name': a['title']})
        path = '/research/' + a['slug'] + '/'
        date = datetime.date.fromisoformat(a['publication_date']).strftime('%-d %B %Y')
        visible.append('<li><a href="' + path + '">' + html.escape(a['title']) + '</a><br><span class="entry-meta">' + date + ' · Unrefereed preprint</span><p>' + html.escape(a['description']) + '</p><p><a href="' + path + a['assets'][0]['name'] + '">PDF</a> · <a href="https://doi.org/' + a['DOI'] + '">Zenodo</a></p></li>')
    newtext = text[:end] + ',\n' + ',\n'.join(json.dumps(x, ensure_ascii=False) for x in additions) + text[end:]
    newtext, count = re.subn(r'("numberOfItems"\s*:\s*)111\b', r'\g<1>114', newtext)
    assert count == 1
    tail = list(re.finditer(rb'<li\b[^>]*>.*?</li>', old, re.S))[-1].end()
    new = old[:tail] + ('\n      ' + '\n      '.join(visible)).encode() + old[tail:]
    result['public/research/index.html'] = new[:sm.start(1)] + newtext.encode() + new[sm.end(1):]
    sitemap = (O / 'BASELINE_SITEMAP.xml').read_bytes()
    tail = list(re.finditer(rb'<url>.*?</url>', sitemap, re.S))[-1].end()
    nodes = ''.join('\n  <url><loc>' + a['canonical'] + '</loc><lastmod>2026-11-16</lastmod></url>' for a in inputs['articles']).encode()
    result['public/research/sitemap.xml'] = sitemap[:tail] + nodes + sitemap[tail:]
    assert len(result) == 14
    return result


def main():
    assert sys.argv[1:] in ([], ['--build'])
    data = (O / 'BUILD_INPUTS.json').read_bytes()
    assert hashlib.sha256(data).hexdigest() == INPUT_SHA
    inputs = json.loads(data)
    baseline = json.loads(checked(inputs['baseline']))
    W = Path(baseline['website'])
    M = Path(baseline['Math']['HEAD_file']['path']).parent.parent
    for root, key in [(W, 'W'), (M, 'Math')]:
        assert head(root) == baseline[key]['HEAD']
        checked(baseline[key]['index'])
    for p in baseline['public_file_pins']:
        checked({**p, 'path': str(W / p['path'])})
    assert len([p for p in (W / 'public').rglob('*') if p.is_file()]) == 699
    for p in baseline['public_directory_modes']:
        assert oct(stat.S_IMODE((W / p['path']).stat().st_mode)) == p['mode']
    for p in inputs['source_guards']:
        checked(p)
    for a in inputs['articles']:
        assert not (W / 'public/research' / a['slug']).exists()
    expected = assemble(inputs)
    candidate = O / 'candidate'
    if sys.argv[1:] == ['--build']:
        assert not candidate.exists()
        for name, body in expected.items():
            p = candidate / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(body)
            p.chmod(0o644)
    assert {p.relative_to(candidate).as_posix() for p in candidate.rglob('*') if p.is_file()} == set(expected)
    for name, body in expected.items():
        assert (candidate / name).read_bytes() == body
    old = (O / 'BASELINE_RESEARCH_INDEX.html').read_bytes()
    new = expected['public/research/index.html']
    oldli = re.findall(rb'<li\b[^>]*>.*?</li>', old, re.S)
    newli = re.findall(rb'<li\b[^>]*>.*?</li>', new, re.S)
    assert len(newli) == 114 and newli[:111] == oldli
    assert typed(new)[2]['mainEntity']['numberOfItems'] == 114 and typed(new)[3][:111] == typed(old)[3]
    oldnodes = re.findall(rb'<url>.*?</url>', (O / 'BASELINE_SITEMAP.xml').read_bytes(), re.S)
    nodes = re.findall(rb'<url>.*?</url>', expected['public/research/sitemap.xml'], re.S)
    assert len(nodes) == 115 and nodes[:112] == oldnodes
    for a in inputs['articles']:
        body = expected['public/research/' + a['slug'] + '/index.html']
        assert fragment(body) == fragment(checked(a['source_page']))
        assert abstract(body) == a['abstract']
        p = Links()
        p.feed(body.decode())
        assert len(p.ids) == len(set(p.ids)) and 'noindex' not in p.meta['robots']
        assert p.meta['DC.description'] == a['abstract'] != p.meta['description']
        assert p.meta['citation_pdf_url'] == a['canonical'] + a['assets'][0]['name']
        schema = json.loads(re.search(rb'<script type="application/ld\+json">(.*?)</script>', body, re.S).group(1))
        assert schema['abstract'] == a['abstract'] and schema['url'] == schema['mainEntityOfPage']['@id'] == a['canonical']
        assert [x['contentUrl'] for x in schema['encoding']] == [a['canonical'] + x['name'] for x in a['assets']]
        assert {'rel': 'canonical', 'href': a['canonical']} in p.links
        assert {'rel': 'stylesheet', 'href': '/research/research.css'} in p.links and b'<style' not in body
        for ref in p.refs:
            if not ref or re.match(r'^[a-z]+:', ref, re.I):
                continue
            target = ref.split('#')[0]
            if not target:
                assert ref[1:] in p.ids
                continue
            name = 'public' + target if target.startswith('/') else 'public/research/' + a['slug'] + '/' + target
            if name.endswith('/'):
                name += 'index.html'
            assert name in expected or (W / name).is_file(), name
    for root, key in [(W, 'W'), (M, 'Math')]:
        assert head(root) == baseline[key]['HEAD']
        checked(baseline[key]['index'])
    pins = [{'path': name, 'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest(), 'mode': oct(stat.S_IMODE((candidate / name).stat().st_mode))} for name, body in sorted(expected.items())]
    print(json.dumps({'status': 'PRIVATE14_BUFFER_BUILD_AND_COMPARISON_PASS', 'writes': 14 if sys.argv[1:] else 0, 'candidate_pins': pins, 'new_files': 12, 'aggregate_replacements': 2, 'projected_counts': [711,114,115], 'old111visible_and_raw_typed_items_preserved': True, 'old112XMLnodes_preserved': True, 'all3MAINs_exact': True, 'native_assets_and_Bibs_exact': True, 'W_Math_HEAD_index_unchanged': True, 'production_authority': False}, indent=2))


if __name__ == '__main__':
    main()
