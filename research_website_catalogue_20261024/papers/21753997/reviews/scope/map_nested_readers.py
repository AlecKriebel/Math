"""Inventory nested release archives without executing or extracting contents."""
from pathlib import Path, PurePosixPath
import hashlib, io, json, stat, tarfile, zipfile
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[2]
SCOPE = BASE / 'reviews/scope'
WORK = BASE / 'sources/published-source/AlecKriebel-Math-26f7e00/weakly_reversible_continuum_no_common_factor'
docmap = json.loads((SCOPE / 'reader_document_map.json').read_text())
known = {d['sha256']: d['pages'] for d in docmap['documents']}
out = []

def valid(name):
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or '\\' in name:
        raise ValueError(name)

for path in sorted(WORK.glob('releases/*/dist/*')):
    if not path.name.endswith(('.zip', '.tar.gz')):
        continue
    readers = []
    manifest = []
    if path.suffix == '.zip':
        with zipfile.ZipFile(path) as z:
            for m in z.infolist():
                valid(m.filename)
                mode = m.external_attr >> 16
                if stat.S_ISLNK(mode) or (stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR)):
                    raise ValueError('nonregular ZIP member: ' + m.filename)
                manifest.append({'path': m.filename, 'bytes': m.file_size})
                if m.filename.lower().endswith('.pdf'):
                    b = z.read(m)
                    h = hashlib.sha256(b).hexdigest()
                    if h not in known:
                        raise ValueError('Unmapped new reader PDF: ' + m.filename + ' ' + h)
                    readers.append({'member': m.filename, 'bytes': len(b), 'sha256': h, 'pages': known[h], 'byte_identical_to_read_direct_member': True})
    else:
        with tarfile.open(path, 'r:gz') as t:
            for m in t.getmembers():
                valid(m.name)
                if not (m.isfile() or m.isdir()):
                    raise ValueError('nonregular TAR member: ' + m.name)
                manifest.append({'path': m.name, 'bytes': m.size})
                if m.name.lower().endswith('.pdf'):
                    b = t.extractfile(m).read()
                    if PurePosixPath(m.name).name.startswith('._') and b[:4] == bytes.fromhex('00051607'):
                        manifest[-1]['classification'] = 'AppleDouble metadata, not a reader PDF'
                        continue
                    h = hashlib.sha256(b).hexdigest()
                    if h not in known:
                        raise ValueError('Unmapped new reader PDF: ' + m.name + ' ' + h)
                    readers.append({'member': m.name, 'bytes': len(b), 'sha256': h, 'pages': known[h], 'byte_identical_to_read_direct_member': True})
    out.append({'path': str(path.relative_to(BASE)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'member_count': len(manifest), 'all_paths_and_types_checked': True, 'reader_documents': readers, 'members': manifest})

(SCOPE / 'nested_archive_reader_map.json').write_text(json.dumps({'generated_utc': datetime.now(timezone.utc).isoformat(), 'archives': out, 'new_distinct_pdfs': 0}, indent=2)+'\n')
docmap['nested_archive_inventory'] = 'nested_archive_reader_map.json'
docmap['nested_pdf_occurrences'] = sum(len(a['reader_documents']) for a in out)
docmap['total_pdf_occurrences_including_nested'] = len(docmap['documents']) + docmap['nested_pdf_occurrences']
docmap['nested_reader_hashes_all_match_read_direct_members'] = True
(SCOPE / 'reader_document_map.json').write_text(json.dumps(docmap, indent=2)+'\n')
print(json.dumps({'archives': len(out), 'nested_pdf_occurrences': docmap['nested_pdf_occurrences'], 'distinct_pdfs': len(known), 'distinct_pages': sum(known.values())}))
