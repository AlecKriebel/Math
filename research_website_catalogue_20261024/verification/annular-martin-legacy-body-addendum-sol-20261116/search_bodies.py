#!/usr/bin/env python3
"""Finite offline data-only HTML search; default reads pinned data and emits JSON."""
import datetime
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re

O = Path(__file__).resolve().parent


def checked(pin):
    data = Path(pin['path']).read_bytes()
    assert len(data) == pin['bytes']
    assert hashlib.sha256(data).hexdigest() == pin['SHA256']
    return data


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def main():
    initial = json.loads((O / 'INITIAL.json').read_bytes())
    for key in ('original_packet_FINAL', 'original_packet_manifest', 'source_identity', 'native_record'):
        checked(initial[key])
    corpus = json.loads(checked(initial['original_47_reference_map']))
    root = json.loads(json.loads((O / 'OPEN_ROOT.connector.json').read_bytes())['structuredContent']['content'])
    assert next(e for e in root['tree'] if e['path'] == 'docs')['sha'] == corpus['docs_tree'] == initial['current_docs_required']
    assert corpus['HTML_count'] == len(corpus['HTML_identity_rows']) == 47
    rows, hits, total_bytes = [], [], 0
    assert len({e['path'] for e in corpus['HTML_identity_rows']}) == 47
    for entry in corpus['HTML_identity_rows']:
        data = checked(entry['whole_body_authenticated_reference'])
        assert len(data) == entry['bytes'] and hashlib.sha256(data).hexdigest() == entry['SHA256']
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == entry['Git_blob']
        raw = data.decode('utf-8')
        parser = Text()
        parser.feed(raw)
        parser.close()
        views = {'raw': raw, 'entity_decoded': html.unescape(raw), 'text_nodes': ' '.join(parser.parts)}
        views['spacing_free_decoded'] = re.sub(r'\s+', '', views['entity_decoded'])
        matches = []
        for name, text in views.items():
            for term in initial['terms']:
                needle = re.sub(r'\s+', '', term) if name == 'spacing_free_decoded' else term
                found = list(re.finditer(re.escape(needle.casefold()), text.casefold()))
                if found:
                    matches.append({'view': name, 'term': term, 'count': len(found), 'first_contexts': [text[max(0, m.start()-180):m.end()+220] for m in found[:4]]})
        row = {k: entry[k] for k in ('path', 'Git_blob', 'bytes', 'SHA256', 'whole_body_authenticated_reference')}
        row['matching_terms'] = sorted({m['term'] for m in matches})
        rows.append(row)
        if matches:
            hits.append({'path': entry['path'], 'matches': matches})
        total_bytes += len(data)
    print(json.dumps({'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'docs_tree': corpus['docs_tree'], 'HTML_count': len(rows), 'whole_HTML_bytes_hashed_and_searched': total_bytes, 'terms': initial['terms'], 'representations_per_body': list(views), 'bodies': rows, 'hits': hits, 'candidate_correspondence_requires_human_reading': True, 'PDF_ZIP_history_or_other_body_reads': False}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
