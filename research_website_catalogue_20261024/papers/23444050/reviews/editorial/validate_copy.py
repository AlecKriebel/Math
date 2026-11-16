"""One bounded offline data comparison; stdout only, no source-program execution."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import re

O = Path(__file__).resolve().parent


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.meta, self.frames = [], [], {}, []
        self.abstract, self.in_abstract = [], False
        self.native_order, self.in_native = [], False
        self.scripts, self.script = [], None
        self.canonicals = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'section' and a.get('id') == 'original-abstract':
            self.in_abstract = True
        if tag == 'ol' and a.get('id') == 'native-downloads':
            self.in_native = True
        if tag == 'a':
            self.links.append(a)
            if self.in_native and 'download' in a:
                self.native_order.append(a['href'])
        if tag == 'meta':
            self.meta[a.get('name', a.get('property'))] = a.get('content')
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonicals.append(a)
        if tag == 'iframe':
            self.frames.append(a)
        if tag == 'script':
            assert a.get('type') == 'application/ld+json'
            self.script = ''

    def handle_endtag(self, tag):
        if tag == 'section':
            self.in_abstract = False
        if tag == 'ol':
            self.in_native = False
        if tag == 'script':
            self.scripts.append(json.loads(self.script))
            self.script = None

    def handle_data(self, text):
        if self.in_abstract:
            self.abstract.append(text)
        if self.script is not None:
            self.script += text


def check_pin(p):
    data = Path(p['path']).read_bytes()
    assert len(data) == p['bytes'] and hashlib.sha256(data).hexdigest() == p['SHA256']
    return data


def main():
    seal = json.loads((O / 'INITIAL_SEAL.json').read_bytes())
    for p in seal['payload_files']:
        check_pin({**p, 'path': str(O / p['path'])})
    source = json.loads((O / 'SOURCE_PINS.json').read_bytes())
    for key in ('native_record', 'native_files_response', 'operative_TeX', 'actual_LICENSE_txt'):
        check_pin(source[key])
    for p in source['native_assets_in_record_and_entries_order']:
        check_pin(p)
    model = json.loads((O / 'PAGE_MODEL.json').read_bytes())
    data = (O / 'preview/index.html').read_bytes()
    page = Page()
    page.feed(data.decode())
    assert len(page.ids) == len(set(page.ids))
    assert not page.canonicals and 'noindex' in page.meta['robots']
    assert model['public_canonical'] is None and model['AA'] is None and model['follow_up'] is None
    abstract = model['original_abstract']
    assert ' '.join(''.join(page.abstract).split()) == 'Original manuscript abstract ' + abstract
    assert page.scripts[0]['abstract'] == page.meta['DC.description'] == abstract
    assert page.meta['description'] == page.scripts[0]['description'] == model['description'] != abstract
    assert page.meta['citation_doi'] == model['native_DOI'] == '10.5281/zenodo.23444050'
    assert page.meta['citation_version'] == model['version'] == '1.0.0'
    assert re.search(rb'<main\b[^>]*>.*?</main>', data, re.S).group() + b'\n' == (O / 'MAIN.html').read_bytes()
    names = [p['native_key'] for p in source['native_assets_in_record_and_entries_order']]
    assert page.native_order == names
    for p in source['native_assets_in_record_and_entries_order']:
        assert (O / 'preview' / p['native_key']).read_bytes() == check_pin(p)
    assert (O / 'citation.bib').read_bytes() == (O / 'preview/citation.bib').read_bytes()
    assert 'MIT' not in data.decode() and 'CC BY 4.0' in data.decode()
    assert len(page.frames) == 1 and page.frames[0]['src'].split('#')[0] == names[0]
    local = []
    for link in page.links:
        href = link['href']
        if href.startswith('#'):
            assert href[1:] in page.ids
        elif ':' not in href:
            assert (O / 'preview' / href.split('#')[0]).is_file()
            local.append(href)
    print(json.dumps({'status': 'PASS_PRIVATE_DATA_COMPARISON', 'whole_MAIN_bytes': (O / 'MAIN.html').stat().st_size, 'page_bytes': len(data), 'unique_IDs': len(page.ids), 'full_original_abstract_visible_JSONLD_DC_equal': True, 'native_assets_exact_in_order': names, 'local_links_resolve': local, 'INITIAL_unchanged': True, 'runtime_or_live_reader_download_certification': False}, indent=2))


if __name__ == '__main__':
    main()
