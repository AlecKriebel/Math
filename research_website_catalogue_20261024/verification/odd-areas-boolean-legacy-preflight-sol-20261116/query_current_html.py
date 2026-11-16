"""One bounded offline data query of fixed47 current wholeHTML references; stdout only."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import html
import json
import re

O = Path(__file__).resolve().parent


def checked(pin):
    data = Path(pin['path']).read_bytes()
    assert len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['SHA256']
    return data


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, value):
        self.parts.append(value)


def main():
    initial = json.loads((O / 'INITIAL.json').read_bytes())
    targets = json.loads(checked(initial['native_identities']))['targets']
    for key in ('reference_FINAL', 'reference_manifest'):
        checked(initial[key])
    reference = json.loads(checked(initial['same47_reference_map']))
    root = json.loads(json.loads((O / 'OPEN_ROOT.connector.json').read_bytes())['structuredContent']['content'])
    assert next(e for e in root['tree'] if e['path'] == 'docs')['sha'] == reference['docs_tree'] == initial['current_docs_required']
    assert reference['HTML_count'] == len(reference['rows']) == len({e['path'] for e in reference['rows']}) == 47
    for target in targets:
        checked(target['native_record'])
    rows, hits = [], []
    for item in reference['rows']:
        body = Path(item['body_reference']['path']).read_bytes()
        if item['body_reference'].get('container') == 'structuredContent.content UTF-8':
            body = json.loads(body)['structuredContent']['content'].encode('utf-8')
        assert len(body) == item['bytes'] and hashlib.sha256(body).hexdigest() == item['SHA256']
        assert hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest() == item['Git_blob']
        raw = body.decode('utf-8')
        parser = Text()
        parser.feed(raw)
        parser.close()
        decoded = ' '.join(html.unescape(' '.join(parser.parts)).split())
        views = {'raw_HTML': raw, 'decoded_text': decoded, 'spacing_free_decoded_text': re.sub(r'\s+', '', decoded)}
        matches = []
        for target in targets:
            for view, text in views.items():
                queries = [(term, re.escape(re.sub(r'\s+', '', term) if view == 'spacing_free_decoded_text' else term)) for term in target['literal_terms']]
                queries += [(term, term) for term in target['label_regexes']]
                for term, expression in queries:
                    found = list(re.finditer(expression, text, re.I))
                    if found:
                        matches.append({'record': target['record'], 'term': term, 'view': view, 'count': len(found), 'contexts': [text[max(0, m.start()-170):m.end()+230] for m in found[:4]]})
        row = {k: item[k] for k in ('path', 'Git_blob', 'bytes', 'SHA256', 'body_reference')}
        row['matching_records'] = sorted({m['record'] for m in matches})
        rows.append(row)
        if matches:
            hits.append({'path': item['path'], 'matches': matches})
    print(json.dumps({'scope': initial['search_scope'], 'docs_tree': reference['docs_tree'], 'HTML_count': len(rows), 'whole_HTML_bytes': sum(r['bytes'] for r in rows), 'views': list(views), 'targets': targets, 'rows': rows, 'hits': hits, 'candidate_identity_requires_personal_whole_article_read': True, 'old_helper_science_network_or_asset_history_campaign': False}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
