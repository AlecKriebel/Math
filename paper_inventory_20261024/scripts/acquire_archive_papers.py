"""Read-only HTTP-range inspection of published whole-repository Zenodo ZIPs.

The full archive MD5 is advertised by Zenodo, not recomputed. Individual extracted
members are checked against ZIP CRC32 and persisted with exact SHA256/MD5 hashes.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import difflib
import hashlib
import io
import json
from pathlib import Path
import re
import struct
import threading
import time
import urllib.parse
import urllib.request
import zipfile
import zlib
from pypdf import PdfReader
from acquire_corpus import SOURCES, TEXTS, ROOT, write_json, stamp, digest

REQUEST_LOCK = threading.Lock()
LAST_REQUEST = 0.0

def range_read(url, start, stop):
    global LAST_REQUEST
    for attempt in range(4):
        try:
            with REQUEST_LOCK:
                pause = 0.5 - (time.monotonic() - LAST_REQUEST)
                if pause > 0:
                    time.sleep(pause)
                LAST_REQUEST = time.monotonic()
            req = urllib.request.Request(url, headers={'Range': f'bytes={start}-{stop - 1}',
                                                      'User-Agent': 'Independent-research-paper-inventory/1.0'})
            with urllib.request.urlopen(req, timeout=90) as response:
                if response.status != 206:
                    raise RuntimeError(f'Expected HTTP206, got {response.status}')
                data = response.read(stop - start + 1)
            if len(data) != stop - start:
                raise RuntimeError('HTTP range byte count differs')
            return data
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)

class RangeFile(io.RawIOBase):
    def __init__(self, url, size):
        self.url, self.size, self.pos = url, size, 0
    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.pos
    def seek(self, offset, whence=0):
        self.pos = offset if whence == 0 else self.pos + offset if whence == 1 else self.size + offset
        return self.pos
    def read(self, count=-1):
        if count < 0: count = self.size - self.pos
        count = min(count, self.size - self.pos)
        if count <= 0: return b''
        result = range_read(self.url, self.pos, self.pos + count)
        self.pos += len(result)
        return result

def list_one(record, file):
    rid = record['id']
    url = f"https://zenodo.org/records/{rid}/files/{urllib.parse.quote(file['filename'])}?download=1"
    row = {'deposit_id': rid, 'deposit_title': record['title'], 'publication_date': record['publication_date'],
           'archive_filename': file['filename'], 'archive_advertised_md5': file['checksum'],
           'archive_bytes': file['filesize'], 'archive_full_hash_verified': False, 'url': url}
    try:
        archive = zipfile.ZipFile(RangeFile(url, file['filesize']))
        entries = []
        for member in archive.infolist():
            if member.filename.lower().endswith('.pdf') or any(x in member.filename for x in ['RELEASE_RECORD', '/PUBLICATION.md']):
                entries.append({'member': member.filename, 'bytes': member.file_size,
                    'compressed_bytes': member.compress_size, 'crc32': f'{member.CRC:08x}',
                    'header_offset': member.header_offset, 'compress_type': member.compress_type})
        row.update({'status': 'ok', 'total_members': len(archive.infolist()), 'selected_members': entries,
                    'pdf_members': sum(e['member'].lower().endswith('.pdf') for e in entries)})
    except Exception as exc:
        row.update({'status': 'error', 'error': str(exc)})
    print(f"Archive {rid}: {row.get('pdf_members', 'error')} PDFs", flush=True)
    return row

def extract_member(archive, member):
    offset = member['header_offset']
    header = range_read(archive['url'], offset, offset + 30)
    values = struct.unpack('<4s5H3I2H', header)
    if values[0] != b'PK\x03\x04': raise RuntimeError('ZIP local header signature differs')
    filename_bytes, extra_bytes = values[-2:]
    start = offset + 30 + filename_bytes + extra_bytes
    compressed = range_read(archive['url'], start, start + member['compressed_bytes'])
    if member['compress_type'] == 0: data = compressed
    elif member['compress_type'] == 8: data = zlib.decompress(compressed, -15)
    else: raise RuntimeError(f"Unsupported ZIP compression {member['compress_type']}")
    if len(data) != member['bytes'] or f'{zlib.crc32(data):08x}' != member['crc32']:
        raise RuntimeError('ZIP member size/CRC32 differs')
    return data

def author_candidate(member):
    name = member['member'].lower()
    if not name.endswith('.pdf'): return False
    # Preserve all other candidates for first-page authorship adjudication.
    excluded = ['/literature/', '/tmp_literature/', '/references/', '/external/', '/sources/',
                '/research/literature/', '/reference_papers/', '/downloaded/']
    return not any(part in name for part in excluded)

def extract_one(archive, member):
    tag = f"{member['crc32']}_{member['bytes']}"
    pdf_path = SOURCES / 'corpus_archive_pdfs' / (tag + '.pdf')
    text_path = TEXTS / 'archives' / (tag + '.txt')
    result = {'source_deposit_id': archive['deposit_id'], 'archive_filename': archive['archive_filename'],
        'archive_advertised_md5': archive['archive_advertised_md5'], 'archive_full_hash_verified': False,
        **member, 'pdf_path': str(pdf_path), 'text_path': str(text_path)}
    try:
        if pdf_path.exists():
            data = pdf_path.read_bytes()
        else:
            data = extract_member(archive, member)
            pdf_path.parent.mkdir(parents=True, exist_ok=True)
            pdf_path.write_bytes(data)
        if len(data) != member['bytes'] or f'{zlib.crc32(data):08x}' != member['crc32']:
            raise RuntimeError('Cached member failed size/CRC32')
        reader = PdfReader(io.BytesIO(data))
        pages = [page.extract_text() or '' for page in reader.pages]
        text = '\n\n'.join(f'===== PAGE {i + 1} =====\n{page}' for i, page in enumerate(pages))
        text_path.parent.mkdir(parents=True, exist_ok=True)
        text_path.write_text(text)
        first = pages[0] if pages else ''
        pdf_metadata = reader.metadata or {}
        metadata_title = str(pdf_metadata.get('/Title', '') or '').strip()
        metadata_author = str(pdf_metadata.get('/Author', '') or '').strip()
        before_author = re.split(r'Alec\s*Kriebel', first, flags=re.I)[0].strip()
        guessed_title = ' '.join(before_author.split()) if 0 < len(before_author) < 400 else (first.splitlines()[0] if first else '')
        result.update({'status': 'ok', 'member_md5': hashlib.md5(data).hexdigest(),
            'member_sha256': hashlib.sha256(data).hexdigest(), 'member_crc32_verified': True,
            'pages': len(pages), 'characters': len(text), 'first_page_text': first,
            'pdf_metadata_title': metadata_title, 'pdf_metadata_author': metadata_author,
            'title': metadata_title or guessed_title,
            'title_basis': 'embedded PDF metadata' if metadata_title else 'first-page text, requires semantic review',
            'relationship_to_main_corpus': 'Pending semantic duplicate/version adjudication',
            'alec_name_on_first_page': bool(re.search(r'Alec\s*Kriebel|Kriebel,?\s*Alec', first, re.I))})
    except Exception as exc:
        result.update({'status': 'error', 'error': str(exc)})
    print(f"Member {tag}: {result['status']}", flush=True)
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cached-listings', action='store_true')
    ap.add_argument('--list-only', action='store_true')
    args = ap.parse_args()
    rows = json.loads((SOURCES / 'corpus_records.json').read_text())['records']
    if args.cached_listings:
        listings = json.loads((SOURCES / 'archive_listings.json').read_text())['archives']
    else:
        tasks = [(r, f) for r in rows if r['classification'] != 'paper' for f in r['files']
                 if f['filename'].lower().endswith('.zip')]
        listings = []
        with ThreadPoolExecutor(max_workers=3) as pool:
            for result in pool.map(lambda pair: list_one(*pair), tasks): listings.append(result)
        write_json(SOURCES / 'archive_listings.json', {'utc': stamp(), 'archives': listings})
    if args.list_only: return
    # CRC/size identity locates repeated payloads across release archives. Preserve all
    # archive occurrences, extract one exact byte copy per candidate payload.
    existing_crc = {}
    for row in rows:
        for source in row.get('sources', []):
            if source.get('status') == 'ok':
                data = Path(source['pdf_path']).read_bytes()
                existing_crc[(f'{zlib.crc32(data):08x}', len(data))] = row['id']
    selected, occurrences = {}, {}
    for archive in listings:
        if archive['status'] != 'ok': continue
        for member in archive['selected_members']:
            if not author_candidate(member): continue
            key = (member['crc32'], member['bytes'])
            occurrences.setdefault(key, []).append({'deposit_id': archive['deposit_id'],
                'archive_filename': archive['archive_filename'], 'archive_md5': archive['archive_advertised_md5'],
                'member': member['member']})
            selected.setdefault(key, (archive, member))
    results = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs = {pool.submit(extract_one, *pair): key for key, pair in selected.items() if key not in existing_crc}
        for future in as_completed(jobs):
            key = jobs[future]; result = future.result()
            result['all_archive_occurrences'] = occurrences[key]
            results.append(result)
    matches = [{'crc32': k[0], 'bytes': k[1], 'main_corpus_id': existing_crc[k],
                'all_archive_occurrences': occurrences[k]} for k in selected if k in existing_crc]
    def normalized(value):
        return re.sub(r'[^a-z0-9]+', ' ', value.lower()).strip()
    main_papers = [r for r in rows if r['classification'] == 'paper' and r.get('is_latest_paper_version')]
    for result in results:
        if result['status'] != 'ok': continue
        related = []
        for main_paper in main_papers:
            similarity = difflib.SequenceMatcher(None, normalized(result['title']), normalized(main_paper['title'])).ratio()
            if similarity >= .69:
                related.append({'id': main_paper['id'], 'title': main_paper['title'], 'title_similarity': round(similarity, 3)})
        result['relationship_to_main_corpus'] = {
            'status': 'unadjudicated; title similarity is only a screening aid',
            'candidate_related_main_records': sorted(related, key=lambda r: -r['title_similarity'])}
    write_json(SOURCES / 'archive_papers.json', {'utc': stamp(),
        'complete': all(a['status'] == 'ok' for a in listings) and all(r['status'] == 'ok' for r in results),
        'method': 'Public HTTPS byte ranges; advertised archive MD5 retained; each PDF member size/CRC32 and SHA256 checked',
        'limitations': 'Full-archive MD5 not recomputed. Semantic authorship and duplicate/version adjudication is separate.',
        'candidate_unique_pdf_payloads': len(selected), 'exact_matches_to_main_corpus': matches,
        'summary': {'archives_listed': len(listings), 'unique_non_literature_pdf_payloads': len(selected),
            'exact_main_corpus_matches': len(matches), 'additional_payloads_extracted': len(results),
            'extraction_errors': sum(r['status'] != 'ok' for r in results),
            'first_page_alec_name': sum(r.get('alec_name_on_first_page', False) for r in results),
            'full_archive_md5_recomputed': False},
        'papers': sorted(results, key=lambda r: (r['source_deposit_id'], r['member']))})
    print(f"Extracted {len(results)} unique payloads outside main corpus; {len(matches)} exact matches", flush=True)

if __name__ == '__main__': main()
