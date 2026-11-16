#!/usr/bin/env python3
"""One fixed stdout-only stage data audit; no writer/science/helper execution."""
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
from urllib.parse import urlsplit, urljoin, unquote
import hashlib
import json
import os
import re
import stat
import subprocess

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
N = P/'verification/habiro-fixed-area-stage-audit-sol-20261116'
R = P/'verification/habiro-fixed-area-private-stage-sol-20261116'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')


def pin(data):
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest()}


def load(path):
    return json.loads(path.read_bytes())


def fixed(path, row):
    data = path.read_bytes()
    assert pin(data) == {k: row[k] for k in ('bytes', 'SHA256')}, str(path)
    if 'mode' in row:
        assert oct(stat.S_IMODE(path.stat().st_mode)) == row['mode'], str(path)
    return data


def one(text, expression):
    hits = re.findall(expression, text)
    assert len(hits) == 1
    return hits[0]


def normal(text):
    return re.sub(r'\s+', ' ', text.replace('−', '-')).strip()


class Tags(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta, self.links, self.ids, self.count = {}, [], [], {}
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        self.count[tag] = self.count.get(tag, 0)+1
        if 'id' in d:
            self.ids.append(d['id'])
        if tag == 'meta':
            self.meta[d.get('name', d.get('property'))] = d.get('content')
        for key in ('href', 'src'):
            if key in d:
                self.links.append((tag, key, d[key], d.get('rel')))


class MathText(HTMLParser):
    """Serialize explicit sub/sup markup; never flatten away mathematical powers."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag == 'sub': self.parts.append('_{')
        elif tag == 'sup': self.parts.append('^(')
    def handle_endtag(self, tag):
        if tag == 'sub': self.parts.append('}')
        elif tag == 'sup': self.parts.append(')')
    def handle_data(self, data):
        self.parts.append(data)


def abstract_text(section):
    paragraphs = re.findall(r'<p(?:\s[^>]*)?>([\s\S]*?)</p>', section)
    texts = []
    for paragraph in paragraphs:
        parser = MathText(); parser.feed(paragraph)
        texts.append(normal(''.join(parser.parts)))
    return normal(' '.join(texts)), len(texts)


def git(repo, *args):
    return subprocess.run(['git', '--no-optional-locks', '-C', str(repo), *args],
                          capture_output=True, text=True, check=True,
                          env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'}).stdout.strip()


def main():
    final = json.loads(fixed(R/'FINAL.json', {'bytes':6550,'SHA256':'f46e94682de84ecbcb12c51a158917eccf4deee0d6cda9f73d2a6888fdc47adc'}))
    manifest = json.loads(fixed(R/'MANIFEST.json', {'bytes':4566,'SHA256':'c93f98af41b6dc214c894f2e68788690c0b8dbcdb4a115292cdb395dbe490e09'}))
    payloads = manifest['payload_pins']
    assert {str(q.relative_to(R)) for q in R.rglob('*') if q.is_file()} == {x['path'] for x in payloads}|{'FINAL.json','MANIFEST.json'}
    assert sorted(str(q.relative_to(R)) for q in R.rglob('*') if q.is_dir()) == manifest['directories']
    assert len(payloads)+2 == 22 and len(manifest['directories']) == 5
    for row in payloads:
        assert not (R/row['path']).is_symlink()
        fixed(R/row['path'], row)
    build = json.loads(fixed(R/'BUILD_INPUTS.json', final['actual_corrected_root_BINDING']))
    base = load(N/'BASELINE.json'); sources = load(N/'SOURCES.json')['sources']
    for line in (N/'INITIAL_MANIFEST.txt').read_text().splitlines():
        digest, name = line.split('  ',1)
        assert hashlib.sha256((N/name).read_bytes()).hexdigest() == digest, name
    C = R/final['candidate_root']
    candidate = {str(q.relative_to(C)):q for q in C.rglob('*') if q.is_file()}
    expected = {'public/research/index.html','public/research/sitemap.xml'}
    for source in sources:
        prefix = 'public/research/'+source['slug_from_original_approved_model']+'/'
        expected |= {prefix+'index.html',prefix+'citation.bib'}|{prefix+x['key'] for x in source['native_assets']}
    assert set(candidate) == set(final['exact_paths']) == expected and len(candidate) == 10
    assert len([q for q in C.rglob('*') if q.is_dir()]) == 4
    for row in final['candidate_pins']:
        fixed(candidate[row['path']], row)
    oldfiles = {x['relative_path']:x for x in base['public_files']}
    assert len(expected-set(oldfiles)) == 8 and len(expected&set(oldfiles)) == 2
    projected = set(oldfiles)|expected
    assert len(projected) == 690
    article_results = []
    for source in sources:
        rid = source['record_id']; authority = source['adoption_fields']
        fixed(P/authority['whole_MAIN']['path'], authority['whole_MAIN'])
        fixed(Path(source['adoption']['path']), source['adoption'])
        acquired = json.loads(fixed(Path(source['ACQUIRED']['path']), source['ACQUIRED']))['records'][0]
        original = load(Path(acquired['record_body_path']))
        buildrow = next(x for x in build['records'] if x['record_id'] == rid)
        assert buildrow['native_metadata'] == original['metadata']
        assert buildrow['authority']['SHA256'] == source['adoption']['SHA256']
        canonical = source['expected_target']; prefix = 'public/research/'+source['slug_from_original_approved_model']+'/'
        page = candidate[prefix+'index.html'].read_text(); tags = Tags(); tags.feed(page)
        main_html = one(page, r'<main id="main">[\s\S]*?</main>')
        assert main_html.encode() == (P/authority['whole_MAIN']['path']).read_bytes()
        assert tags.count['main'] == tags.count['h1'] == 1 and len(tags.ids) == len(set(tags.ids))
        assert 'native-description' not in tags.ids and 'Original Zenodo description' not in page
        assert '<link rel="canonical" href="'+canonical+'">' in page
        assert tags.meta['robots'] == 'index,follow' and 'editorial-status' not in tags.meta
        meta = original['metadata']
        for name, value in [('citation_title',meta['title']),('citation_author','Alec Kriebel'),('citation_author_orcid','https://orcid.org/0009-0001-9320-500X'),('citation_doi',original['doi']),('citation_version',meta['version']),('citation_publication_date',meta['publication_date'].replace('-','/')),('article:published_time',meta['publication_date'])]:
            assert tags.meta[name] == value, name
        graph = json.loads(one(page,r'<script type="application/ld\+json">([\s\S]*?)</script>'))['@graph']
        article = next(x for x in graph if x['@type']=='ScholarlyArticle')
        webpage = next(x for x in graph if x['@type']=='WebPage')
        assert article['name'] == meta['title'] and article['datePublished'] == meta['publication_date'] and article['version'] == meta['version']
        assert article['url'] == webpage['url'] == canonical and article['sameAs'] == 'https://doi.org/'+original['doi']
        assert article['identifier']['value'] == original['doi'] and article['license'] == 'https://creativecommons.org/licenses/by/4.0/'
        assert article['creativeWorkStatus'] == 'Unrefereed preprint' and article['author']['identifier'] == 'https://orcid.org/0009-0001-9320-500X'
        actual_abstract, paragraphs = abstract_text(source['full_actual_abstract_HTML'])
        assert normal(article['abstract']) == normal(tags.meta['DC.description']) == actual_abstract
        assert paragraphs == (3 if rid==23443039 else 1)
        if rid == 23443039:
            assert '^(-2)' in article['abstract'] and 'e^(-1)' in article['abstract'] and '∑_{j}' in article['abstract'] and '∫_{{|z|<R}∖S(g)}' in article['abstract']
        fixed(Path(source['BibTeX']['path']),source['BibTeX'])
        assert candidate[prefix+'citation.bib'].read_bytes() == Path(source['BibTeX']['path']).read_bytes()
        order = [x['key'] for x in source['native_assets']]
        downloads = one(page,r'<ol id="native-downloads">([\s\S]*?)</ol>')
        assert re.findall(r'<a href="([^"]+)" download>',downloads) == order
        assert [x['name'] for x in article['encoding']] == order
        for asset, encoding in zip(source['native_assets'],article['encoding']):
            data = candidate[prefix+asset['key']].read_bytes()
            assert data == Path(asset['path']).read_bytes() and pin(data) == {k:asset[k] for k in ('bytes','SHA256')}
            assert hashlib.md5(data).hexdigest() == asset['original_API_file_object']['checksum'][4:]
            assert encoding['contentUrl'] == canonical+asset['key'] and encoding['sameAs'] == asset['original_API_file_object']['links']['self']
        pdf = next(x['key'] for x in source['native_assets'] if x['key'].endswith('.pdf'))
        assert tags.meta['citation_pdf_url'] == canonical+pdf and 'src="'+pdf+'#view=FitH"' in page
        article_results.append({'record_id':rid,'page':pin(page.encode()),'whole_MAIN':pin(main_html.encode()),'abstract_parts':paragraphs,'full_abstract_in_JSONLD_and_DC':True,'explicit_math_serialization':article['abstract'],'native_assets_and_Bib_exact':True,'canonical':canonical})
    index = candidate['public/research/index.html'].read_text()
    collection = json.loads(one(index,r'<script type="application/ld\+json">([\s\S]*?)</script>'))['mainEntity']
    visible = re.findall(r'<li(?:\s[^>]*)?>[\s\S]*?</li>',index)
    items = collection['itemListElement']
    assert len(visible) == len(items) == collection['numberOfItems'] == 109
    assert visible[:107] == base['old_visible_li_HTML'] and items[:107] == base['old_JSONLD_item_values']
    assert [x['position'] for x in items] == list(range(1,110)) and len({x['url'] for x in items})==109
    assert {x['url'] for x in items[107:]} == {x['expected_target'] for x in sources}
    for source in sources:
        item = next(x for x in items[107:] if x['url']==source['expected_target'])
        assert item['name'] == source['native_record_summaries'][0]['title']
    xml = candidate['public/research/sitemap.xml'].read_text()
    urls = re.findall(r'<url>[\s\S]*?</url>',xml)
    assert len(urls)==110 and urls[:108] == base['old_sitemap_URL_HTML']
    assert {one(x,r'<loc>([\s\S]*?)</loc>') for x in urls[108:]} == {x['expected_target'] for x in sources}
    reference_count = 0
    for name, q in candidate.items():
        if not name.endswith('.html'): continue
        page=q.read_text(); tags=Tags();tags.feed(page)
        base_url='https://aleckriebel.com/'+name.removeprefix('public/')
        for tag,key,href,rel in tags.links:
            target=urlsplit(urljoin(base_url,href))
            if target.scheme not in ('http','https') or target.netloc!='aleckriebel.com':continue
            path='public'+unquote(target.path)
            if path.endswith('/'):path+='index.html'
            if path not in projected and path+'/index.html' in projected:path+='/index.html'
            assert path in projected,(name,href,path)
            if target.fragment and path.endswith('.html'):
                content=(candidate[path] if path in candidate else W/path).read_text()
                target_tags=Tags();target_tags.feed(content)
                assert unquote(target.fragment) in target_tags.ids,(name,href)
            reference_count+=1
    current = {str(q.relative_to(W)):q for q in (W/'public').rglob('*') if q.is_file()}
    assert set(current)==set(oldfiles)
    assert sorted(str(q.relative_to(W)) for q in (W/'public').rglob('*') if q.is_dir()) == base['public_directories']
    for name,q in current.items():
        assert not q.is_symlink()
        fixed(q,oldfiles[name])
    for key in ('W','Math'):
        repo=base[key];root=Path(repo['root'])
        assert git(root,'rev-parse','HEAD') == repo['HEAD'] and git(root,'rev-parse','HEAD^{tree}') == repo['HEAD_tree']
        assert git(root,'symbolic-ref','HEAD') == repo['symbolic_HEAD']
        fixed(Path(repo['index']['path']),repo['index'])
    assert final['AA'] is final['follow_up'] is None and final['publication_authority'] is False
    print(json.dumps({'status':'PASS_INDEPENDENT_FIXED_TWO_PAGE_STAGE','writer_packet':[22,5],'candidate':[10,4],
                      'candidate_pins':final['candidate_pins'],'articles':article_results,'projected_counts':[690,109,110],
                      'preserved_old_visible_HTML_units':107,'preserved_old_JSONLD_item_values':107,'preserved_old_URL_XML_units':108,
                      'resolved_local_references':reference_count,'W_public_HEAD_tree_index_and_Math_HEAD_tree_index_unchanged':True,
                      'own_source_INITIAL_payloads_unchanged':True,'new_stage_helper_native_science_render_browser_network_execution':False,
                      'publication_authority':False},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
