"""Read-only correspondence screening; writes evidence only inside this cache."""
from pathlib import Path
from datetime import datetime, timezone
from html.parser import HTMLParser
from html import unescape
import hashlib
import json
import re
import subprocess
import unicodedata

C = Path(__file__).resolve().parent
B = C.parents[1]
D = B.parent / 'docs'
IDS = ['23393596', '23358014', '23356964']
ROOT_HASHES = {
    '23393596': '36b0ccc972b713e507c5ea5a60f86f332fc0668fb9805e8e523d755c6643a871',
    '23358014': '7ecd074783bbf82d6a7a6f31074cd6c6e0bf22fa9180400cc96949c259a5b8cf',
    '23356964': 'e845d4a8a6c1db3c442a3d67889bbb5cfe027b5b87897243dc1782935818ca6b',
}
MARKERS = {
    '23393596': {
        'braid_topic': r'\bbraids?\b',
        'solvability': r'\b(?:1|one)[\s-]*solv',
        'signature_mechanism': r'Gambaudo|Toffoli|Burau|quasimorph|homogeniz|commutator.{0,30}signature',
        'derived_pure_braid': r'pure[\s-]+braid|derived.{0,35}braid|braid.{0,35}derived',
    },
    '23358014': {
        'critical_wave': r'critical[\s-]+wave|quintic|defocusing',
        'sparse_growth': r'sparse[\s-]+control|strong[\s-]+quadratic|critical[\s-]+cone',
        'pde_control_predecessor': r'Brezis[\s–-]*Shatah|Shatah[\s–-]*Struwe|Kunisch|Wachsmuth|Tr[öo]ltzsch',
    },
    '23356964': {
        'cantor_hyperfinite': r'Cantor|hyperfin|Borel[\s-]+asympt',
        'height_or_group': r'profinite|wreath',
        'central_predecessors': r'CJMST|Tucker[\s–-]*Drob|\bIyer\b|\bShinko\b',
    },
}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def info(p):
    return {'path': str(p), 'bytes': p.stat().st_size, 'sha256': sha(p)}


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def norm(text):
    text = unicodedata.normalize('NFKC', unescape(text)).lower()
    return re.sub(r'[^a-z0-9]+', '', text)


class Doc(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.text = []
        self.links = []
        self.titles = []
        self.h1 = []
        self.canonical = []
        self.meta = []
        self.title_depth = False
        self.h1_depth = False
        self.ignored = 0
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('script', 'style'):
            self.ignored += 1
        if tag == 'title':
            self.title_depth = True
        if tag == 'h1':
            self.h1_depth = True
        if tag in ('a', 'iframe', 'embed', 'object'):
            self.links.append({'tag': tag, 'url': a.get('href') or a.get('src') or a.get('data')})
        if tag == 'link' and 'canonical' in a.get('rel', '').split():
            self.canonical.append(a.get('href'))
        if tag == 'meta':
            self.meta.append(a)

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.ignored = max(0, self.ignored - 1)
        if tag == 'title':
            self.title_depth = False
        if tag == 'h1':
            self.h1_depth = False

    def handle_data(self, data):
        if self.title_depth:
            self.titles.append(data)
        if self.h1_depth:
            self.h1.append(data)
        if not self.ignored:
            self.text.append(data)


def screen(text, targets):
    found = {}
    compact = norm(text)
    text = unicodedata.normalize('NFKC', text)
    text = re.sub(r'(?<=\w)-\s*\n\s*(?=\w)', '', text)
    for rid, t in targets.items():
        exact = []
        for label, value in [('title', t['title']), ('doi', t['doi']), ('concept_doi', t['concept_doi'])]:
            if norm(value) in compact:
                exact.append(label)
        markers = {}
        for label, pat in MARKERS[rid].items():
            snippets = []
            for m in re.finditer(pat, text, re.I | re.S):
                snippets.append(' '.join(text[max(0, m.start()-110):m.end()+160].split()))
            if snippets:
                markers[label] = {'occurrences': len(snippets), 'contexts': snippets[:12]}
        if exact or markers:
            found[rid] = {'exact_title_doi_hits': exact, 'marker_hits': markers}
    return found


def main():
    for name in ['old-pdf-text', 'old-html', 'old-html-text', 'target-pdf-text']:
        (C / name).mkdir(exist_ok=True)
    baseline = json.loads((C / 'protected-input-baseline.json').read_text())['files']
    assert all(sha(B / name) == h for name, h in baseline.items())
    targets = {}
    for rid in IDS:
        p = B / 'papers' / rid
        c = json.loads((p / 'publication.json').read_text())
        g = json.loads((p / 'promotion.json').read_text())
        record = json.loads((p / 'sources/record.json').read_text())
        receipt = json.loads((p / 'sources/receipt.json').read_text())
        if 'files' in receipt and 'assets' in receipt:
            assert receipt['files'] == receipt['assets']
        assets = receipt.get('files', receipt.get('assets'))
        assert isinstance(assets, list)
        root = B / f'verification/root-clearance-{rid}-20261025.json'
        clearance = json.loads(root.read_text())
        assert sha(root) == ROOT_HASHES[rid] == g['root_clearance_sha256']
        assert g['root_clearance_record'] == clearance
        assert sha(p / 'publication.json') == g['publication_sha256']
        assert sha(p / 'sources/receipt.json') == g['source_receipt_sha256'] == clearance['source_receipt_sha256']
        for key in ['title', 'doi', 'version', 'publication_date']:
            assert c[key] == record['metadata'][key]
        pdf = p / 'sources' / c['pdf_filename']
        a = next(a for a in assets if a.get('name', a.get('filename')) == c['pdf_filename'])
        assert sha(pdf) == a['sha256'] == clearance['pdf_sha256'] == g['pdf_sha256']
        assert pdf.stat().st_size == a['bytes']
        text = subprocess.check_output(['pdftotext', '-layout', str(pdf), '-'])
        target_text = C / 'target-pdf-text' / (rid + '.txt')
        target_text.write_bytes(text)
        first = text.decode().split('\f')[0]
        first_lines = [l.strip() for l in first.splitlines() if l.strip()][:16]
        pdfinfo = subprocess.check_output(['pdfinfo', str(pdf)], text=True)
        pages = int(re.search(r'^Pages:\s+(\d+)', pdfinfo, re.M).group(1))
        assert pages == c['pdf_pages']
        targets[rid] = {'record_id': rid, 'title': c['title'], 'doi': c['doi'], 'concept_doi': record['conceptdoi'], 'zenodo_record_url': 'https://zenodo.org/records/' + rid, 'published_status': record['status'], 'declared_publication_date': c['publication_date'], 'record_created_utc': record['created'], 'zenodo_version': c['version'], 'manuscript_version': c['source_binding']['manuscript_version'], 'published_pdf': info(pdf), 'pdf_pages': pages, 'first_page_header_lines': first_lines, 'full_target_pdf_text': info(target_text), 'record_binding': info(p / 'sources/record.json'), 'receipt_binding': info(p / 'sources/receipt.json'), 'receipt_asset_key': 'files' if 'files' in receipt else 'assets', 'root_clearance_binding': info(root), 'publication_binding': info(p / 'publication.json'), 'promotion_binding': info(p / 'promotion.json'), 'new_page_live_status': 'Not asserted. No actual rendering or public-copy/live/browser approval is performed in this preflight.'}
    tree = json.loads((C / 'remote-docs-tree.json').read_text())
    ref = json.loads((C / 'remote-main-ref.json').read_text())
    assert tree['truncated'] is False
    remote = {i['path']: i for i in tree['tree'] if i['type'] == 'blob' and Path(i['path']).suffix.lower() in ('.pdf', '.html')}
    local = {str(p.relative_to(D)): p for p in D.rglob('*') if p.is_file() and p.suffix.lower() in ('.pdf', '.html')}
    assert set(remote) == set(local)
    blobs = []
    html = []
    pdfs = []
    hits = []
    for rel, p in sorted(local.items()):
        data = p.read_bytes()
        blob = git_blob(data)
        r = remote[rel]
        assert blob == r['sha'] and len(data) == r['size'], rel
        blobs.append({'relative_path': rel, 'local': dict(info(p), git_blob_sha1=blob), 'remote_blob_sha1': r['sha'], 'remote_size': r['size'], 'matches_current_remote': True})
        cache_stem = rel.replace('/', '__')
        if p.suffix.lower() == '.html':
            raw = data.decode('utf-8')
            doc = Doc(raw)
            text = '\n'.join(doc.text)
            body_path = C / 'old-html' / cache_stem
            body_path.write_bytes(data)
            text_path = C / 'old-html-text' / (cache_stem + '.txt')
            text_path.write_text(text)
            found = screen(text + '\n' + raw, targets)
            item = {'relative_path': rel, 'source': info(p), 'title': ' '.join(doc.titles).strip(), 'h1': ' '.join(doc.h1).strip(), 'canonical': doc.canonical, 'links': doc.links, 'metadata': doc.meta, 'full_html_cache': info(body_path), 'full_text_cache': info(text_path), 'screen': found, 'paper_article': rel.startswith('papers/') and rel.endswith('/index.html')}
            html.append(item)
        else:
            text_bytes = subprocess.check_output(['pdftotext', '-layout', str(p), '-'], stderr=subprocess.PIPE)
            assert sha(p) == hashlib.sha256(data).hexdigest(), 'Concurrent local PDF change: ' + rel
            text_path = C / 'old-pdf-text' / (cache_stem + '.txt')
            text_path.write_bytes(text_bytes)
            text = text_bytes.decode('utf-8')
            found = screen(text, targets)
            exact_pdf = [rid for rid, t in targets.items() if t['published_pdf']['sha256'] == hashlib.sha256(data).hexdigest()]
            item = {'relative_path': rel, 'source': info(p), 'first_page_header_lines': [l.strip() for l in text.split('\f')[0].splitlines() if l.strip()][:14], 'full_text_cache': info(text_path), 'full_text_characters': len(text), 'screen': found, 'exact_target_pdf_sha256_matches': exact_pdf}
            pdfs.append(item)
        if found:
            hits.append({'relative_path': rel, 'screen': found})
    assert len(blobs) == 123 and len(html) == 47 and len(pdfs) == 76
    assert sum(x['paper_article'] for x in html) == 40
    assert all(sha(B / name) == h for name, h in baseline.items())
    output = {'utc': datetime.now(timezone.utc).isoformat(), 'completion_percent': 80, 'current_remote_commit': ref['object']['sha'], 'docs_tree_sha': tree['sha'], 'remote_truncated': tree['truncated'], 'current_local_remote_scoped_path_sets_equal': True, 'current_local_remote_blob_matches': blobs, 'pdf_count': len(pdfs), 'paper_article_count': 40, 'total_html_count': len(html), 'marker_patterns': MARKERS, 'targets': targets, 'html_screen': html, 'pdf_full_text_screen': pdfs, 'candidate_hits': hits, 'protected_inputs_unchanged': True}
    (C / 'screen.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    with (C / 'RESEARCH_LOG.md').open('a') as f:
        f.write(f'\n- {output["utc"]} — 80%: Current sampled remote docs and local path sets/blob hashes agree for all 123 HTML/PDF objects. Fresh full-text extraction screened all 76 PDFs; complete HTML bodies, titles, H1, metadata and links screened all 47 pages (40 paper articles). All three target PDFs match source receipts/root/config bindings; wave assets schema preserved. Broad lexical hits require manual correspondence assessment before final classification. Protected inputs remain unchanged.\n')
    print(json.dumps({'commit': output['current_remote_commit'], 'docs_tree': tree['sha'], 'blob_matches': len(blobs), 'pdfs': 76, 'html': 47, 'articles': 40, 'hits': hits}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
