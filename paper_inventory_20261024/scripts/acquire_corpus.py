"""Read-only, paginated Zenodo account acquisition and checksum-bound PDF text corpus.

Credentials are read in memory only; public data is all that is persisted.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import http.client
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parents[1]
SOURCES = HERE / 'sources'
TEXTS = SOURCES / 'texts'
PDFS = SOURCES / 'corpus_pdfs'
sys.path.insert(0, str(ROOT / 'zenodo_deposit_tool'))
import zenodo
from pypdf import PdfReader

def stamp():
    return datetime.now(timezone.utc).isoformat()

def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')
    tmp.replace(path)

def digest(path, algorithm='md5'):
    h = hashlib.new(algorithm)
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
    return h.hexdigest()

def fetch_inventory():
    token = zenodo.token_for('production')
    records, evidence = [], []
    for page in range(1, 101):
        endpoint = f'/api/deposit/depositions?size=100&page={page}&all_versions=true'
        for attempt in range(4):
            conn = http.client.HTTPSConnection('zenodo.org', timeout=90)
            try:
                conn.request('GET', endpoint, headers={
                    'Authorization': f'Bearer {token}', 'Accept': 'application/json',
                    'User-Agent': zenodo.USER_AGENT})
                response = conn.getresponse()
                body = response.read(32 * 1024 * 1024 + 1)
                if response.status != 200:
                    raise RuntimeError(f'Inventory HTTP {response.status}')
                data = json.loads(body)
                if not isinstance(data, list):
                    raise RuntimeError('Expected a list of account depositions')
                break
            except Exception:
                if attempt == 3:
                    raise
                time.sleep(2 ** attempt)
            finally:
                conn.close()
        evidence.append({'endpoint': endpoint, 'count': len(data),
                         'response_sha256': hashlib.sha256(body).hexdigest()})
        for raw in data:
            # Persist only fields of public scholarly records; omit ownership, buckets,
            # write links and credentials from the authenticated representation.
            row = {k: raw[k] for k in ('id', 'record_id', 'conceptrecid', 'doi',
                'metadata', 'submitted', 'state', 'created', 'modified') if k in raw}
            row['files'] = [{k: f[k] for k in ('id', 'filename', 'filesize', 'checksum') if k in f}
                            for f in raw.get('files', [])]
            records.append(row)
        print(f'Account page {page}: {len(data)} records; cumulative {len(records)}', flush=True)
        if len(data) < 100:
            break
    else:
        raise RuntimeError('Pagination safety limit exceeded')
    ids = [str(r['id']) for r in records]
    if len(ids) != len(set(ids)):
        raise RuntimeError('Duplicate IDs across pagination')
    payload = {'retrieved_utc': stamp(), 'source': 'Zenodo owned depositions, all_versions=true',
               'pagination': evidence, 'records': records}
    write_json(SOURCES / 'corpus_account_public.json', payload)
    return payload

def build_local_index():
    by_md5, by_name, by_size = {}, {}, {}
    old = ROOT / 'zenodo_discoverability_20261010/SOURCE_CATALOG.json'
    if old.exists():
        for r in json.loads(old.read_text()):
            for source in r.get('sources', []):
                path = Path(source.get('pdf_path', ''))
                if path.is_file():
                    by_md5.setdefault(source.get('md5', ''), []).append(path)
    for state_path in (ROOT / '.zenodo-state').glob('*production.json'):
        try:
            state = json.loads(state_path.read_text())
            manifest = Path(state.get('manifest', ''))
            if not manifest.is_file():
                continue
            mdata = json.loads(manifest.read_text())
            for file in mdata.get('files', []):
                path = Path(file.get('path', ''))
                if not path.is_absolute():
                    path = manifest.parent / path
                if path.suffix.lower() == '.pdf' and path.is_file():
                    by_name.setdefault(path.name, set()).add(path)
        except Exception:
            continue
    # Source publication receipts do not cover every historical record. Filename and
    # size indexing permits a checksum-bound fallback without guessing from a title.
    found = subprocess.run(['rg', '--files', '--hidden', '-g', '*.pdf', '-g', '!.git/**'],
                           cwd=ROOT, text=True, capture_output=True, check=True)
    for rel in found.stdout.splitlines():
        path = ROOT / rel
        try:
            by_name.setdefault(path.name, set()).add(path)
            by_size.setdefault(path.stat().st_size, set()).add(path)
        except OSError:
            pass
    print(f'Local PDF index: {sum(len(v) for v in by_name.values())} paths', flush=True)
    return by_md5, by_name, by_size

def clean_name(name):
    return re.sub(r'[^A-Za-z0-9_.-]+', '_', name)

def bind_pdf(record_id, file, index):
    by_md5, by_name, by_size = index
    filename = file['filename']
    expected = str(file.get('checksum', '')).removeprefix('md5:')
    size = file.get('filesize')
    candidates = list(by_md5.get(expected, []))
    candidates += sorted(by_name.get(filename, set()), key=lambda p: (len(str(p)), str(p)))
    candidates += sorted(by_size.get(size, set()), key=lambda p: (len(str(p)), str(p)))
    seen = set()
    for path in candidates:
        if path in seen:
            continue
        seen.add(path)
        try:
            if size is not None and path.stat().st_size != size:
                continue
            if digest(path) == expected:
                return path, 'local checksum match'
        except OSError:
            pass
    dest = PDFS / str(record_id) / clean_name(filename)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and digest(dest) == expected:
        return dest, 'previous downloaded checksum match'
    url = f'https://zenodo.org/records/{record_id}/files/{urllib.parse.quote(filename)}?download=1'
    req = urllib.request.Request(url, headers={'User-Agent': zenodo.USER_AGENT})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as response:
                data = response.read(100 * 1024 * 1024 + 1)
            if len(data) > 100 * 1024 * 1024:
                raise RuntimeError('PDF download exceeds safety limit')
            if hashlib.md5(data).hexdigest() != expected:
                raise RuntimeError('Downloaded PDF checksum mismatch')
            dest.write_bytes(data)
            return dest, 'public Zenodo download, checksum verified'
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)

def classify(record):
    md = record.get('metadata', {})
    has_pdf = any(f.get('filename', '').lower().endswith('.pdf') for f in record.get('files', []))
    published = bool(record.get('submitted')) and record.get('state') == 'done'
    if not published:
        return 'unpublished_draft', 'Not submitted and done'
    if int(record['id']) == 22929556:
        return 'paper', 'Documented manuscript despite software upload_type in historical account classification'
    if md.get('upload_type') == 'publication' and has_pdf:
        return 'paper', 'Published publication record with a PDF manuscript'
    if md.get('upload_type') == 'publication':
        return 'publication_without_pdf', 'Published publication record without PDF; inspect separately'
    return 'non_manuscript', f"Published {md.get('upload_type', 'unknown')} record"

def process(record, index):
    row = dict(record)
    md = record.get('metadata', {})
    row.update({'title': md.get('title', ''), 'description_html': md.get('description', ''),
        'publication_date': md.get('publication_date', ''), 'version': md.get('version', ''),
        'doi': record.get('doi') or md.get('doi') or f"10.5281/zenodo.{record['id']}",
        'concept_id': str(record.get('conceptrecid') or record['id']),
        'record_url': f"https://zenodo.org/records/{record['id']}"})
    row['classification'], row['classification_reason'] = classify(record)
    row['sources'] = []
    if row['classification'] == 'paper':
        for file in record.get('files', []):
            if not file.get('filename', '').lower().endswith('.pdf'):
                continue
            source = {'filename': file['filename'], 'expected_md5': str(file.get('checksum', '')).removeprefix('md5:'),
                      'expected_bytes': file.get('filesize')}
            try:
                path, provenance = bind_pdf(record['id'], file, index)
                text_path = TEXTS / str(record['id']) / (clean_name(file['filename']) + '.txt')
                text_path.parent.mkdir(parents=True, exist_ok=True)
                reader = PdfReader(path)
                pages = [page.extract_text() or '' for page in reader.pages]
                extracted = '\n\n'.join(f'===== PAGE {i + 1} =====\n{text}' for i, text in enumerate(pages))
                text_path.write_text(extracted, encoding='utf-8')
                source.update({'pdf_path': str(path), 'text_path': str(text_path), 'origin': provenance,
                    'md5': digest(path), 'sha256': digest(path, 'sha256'), 'bytes': path.stat().st_size,
                    'pages': len(pages), 'characters': len(extracted),
                    'text_sha256': digest(text_path, 'sha256'), 'extraction': 'pypdf full page text', 'status': 'ok'})
            except Exception as exc:
                source.update({'status': 'error', 'error': f'{type(exc).__name__}: {exc}'})
            row['sources'].append(source)
    return row

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cached-account', action='store_true')
    args = parser.parse_args()
    account = json.loads((SOURCES / 'corpus_account_public.json').read_text()) if args.cached_account else fetch_inventory()
    index = build_local_index()
    rows = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        jobs = {pool.submit(process, r, index): r['id'] for r in account['records']}
        for future in as_completed(jobs):
            row = future.result()
            rows.append(row)
            if row['classification'] == 'paper':
                print(f"PDFs {row['id']}: {len(row['sources'])} ({','.join(s['status'] for s in row['sources'])})", flush=True)
    concepts = {}
    for row in rows:
        if row['classification'] == 'paper':
            concepts.setdefault(row['concept_id'], []).append(row)
    for concept_rows in concepts.values():
        latest = max(concept_rows, key=lambda r: (r.get('publication_date', ''), int(r['id'])))
        for row in concept_rows:
            row['is_latest_paper_version'] = row['id'] == latest['id']
            row['all_paper_version_ids'] = sorted(r['id'] for r in concept_rows)
    rows.sort(key=lambda r: int(r['id']))
    papers = [r for r in rows if r['classification'] == 'paper']
    latest = [r for r in papers if r['is_latest_paper_version']]
    errors = [{'id': r['id'], **s} for r in papers for s in r['sources'] if s['status'] != 'ok']
    summary = {'retrieved_utc': account['retrieved_utc'], 'acquired_utc': stamp(),
        'owned_all_version_records': len(rows), 'paper_version_records': len(papers),
        'paper_concepts': len(concepts), 'paper_pdf_files': sum(len(r['sources']) for r in papers),
        'pdfs_acquired': sum(s['status'] == 'ok' for r in papers for s in r['sources']),
        'excluded_records': len(rows) - len(papers), 'errors': errors,
        'classification_counts': {k: sum(r['classification'] == k for r in rows) for k in sorted(set(r['classification'] for r in rows))}}
    write_json(SOURCES / 'corpus_records.json', {'summary': summary, 'records': rows})
    write_json(SOURCES / 'corpus_latest_papers.json', {'summary': summary, 'papers': latest})
    write_json(SOURCES / 'corpus_summary.json', summary)
    print(json.dumps(summary, indent=2), flush=True)

if __name__ == '__main__':
    main()
