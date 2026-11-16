"""Bounded offline data-only query of the fixed47 HTML references; stdout only."""
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

    def handle_data(self, text):
        self.parts.append(text)


def main():
    inputs = json.loads((O / 'LEGACY_INPUTS.json').read_bytes())
    for key in ('prior_151_FINAL', 'prior_151_manifest'):
        checked(inputs[key])
    reference = json.loads(checked(inputs['same47_reference_map']))
    tree = json.loads(json.loads((O / 'LEGACY_OPEN_ROOT.connector.json').read_bytes())['structuredContent']['content'])
    assert next(x for x in tree['tree'] if x['path'] == 'docs')['sha'] == reference['docs_tree'] == inputs['required_docs_tree']
    assert reference['HTML_count'] == len(reference['rows']) == 47
    patterns = {}
    for target in inputs['targets']:
        checked(target['native_record'])
        patterns[target['record']] = [(x, re.compile(re.escape(x), re.I)) for x in target['literal_terms']] + [(x, re.compile(x, re.I)) for x in target['alias_regexes']]
    rows, hits = [], []
    for row in reference['rows']:
        data = checked({'path': row['body_reference']['path'], 'bytes': row['bytes'], 'SHA256': row['SHA256']})
        assert len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['SHA256']
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == row['Git_blob']
        raw = data.decode('utf-8')
        p = Text()
        p.feed(raw)
        p.close()
        views = {'raw_HTML': raw, 'decoded_text': ' '.join(html.unescape(' '.join(p.parts)).split())}
        matches = []
        for record, queries in patterns.items():
            for name, text in views.items():
                for term, expression in queries:
                    found = list(expression.finditer(text))
                    if found:
                        matches.append({'record': record, 'view': name, 'term': term, 'count': len(found), 'contexts': [text[max(0, m.start()-160):m.end()+220] for m in found[:4]]})
        rows.append({k: row[k] for k in ('path', 'Git_blob', 'bytes', 'SHA256', 'body_reference')})
        if matches:
            hits.append({'path': row['path'], 'matches': matches})
    print(json.dumps({'docs_tree': reference['docs_tree'], 'HTML_count': len(rows), 'whole_HTML_bytes': sum(x['bytes'] for x in rows), 'rows': rows, 'hits': hits, 'targets': inputs['targets'], 'search_views': list(views), 'candidate_correspondence_requires_personal_read': True, 'scientific_oldhelper_or_network_execution': False}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
