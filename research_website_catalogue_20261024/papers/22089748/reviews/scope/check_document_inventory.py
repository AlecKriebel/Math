from pathlib import Path
import json, hashlib, subprocess, datetime, re
b = Path(__file__).resolve().parents[2]
r = b / 'reviews/scope'
s = b / 'sources'
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
ex = s / 'published-source'
source = ex / 'complete_graph_extremality_db_source_and_certificates'
outer = ex / 'paper_i_complete_graph_extremality_referee_package_2026-08-23_r4/paper_i_complete_graph_extremality_referee_package_2026-08-23_r4'
manifest = []
for p in [source/'MANIFEST.sha256', outer/'PACKAGE_MANIFEST.sha256', outer/'source_and_certificates/MANIFEST.sha256']:
    entries = []
    for line in p.read_text().splitlines():
        h, name = line.split('  ', 1)
        q = p.parent / name
        assert q.is_file() and sha(q) == h, (q, h)
        entries.append(name)
    actual = [str(q.relative_to(p.parent)) for q in p.parent.rglob('*') if q.is_file() and q != p]
    assert set(actual) == set(entries), (p, set(actual)-set(entries), set(entries)-set(actual))
    manifest.append({'path':str(p.relative_to(b)), 'sha256':sha(p), 'hashed_regular_files':len(entries), 'exact_file_set':True})
assert sha(outer/'complete_graph_extremality_db_source_and_certificates.tar.gz') == sha(s/'complete_graph_extremality_db_source_and_certificates.tar.gz')
pdfs = [s/'complete_graph_extremality_db.pdf'] + sorted(ex.rglob('*.pdf'))
items = []
for p in pdfs:
    h = sha(p)
    info = subprocess.check_output(['pdfinfo', str(p)], text=True)
    n = int(re.search(r'^Pages:\s+(\d+)', info, flags=re.M).group(1))
    assert h == sha(pdfs[0]) and n == 30
    items.append({'path':str(p.relative_to(b)), 'sha256':h, 'bytes':p.stat().st_size, 'pages':n, 'role':'Published main paper' if p==pdfs[0] else 'Byte-identical convenience copy of published main paper', 'read_scope':'Complete manuscript via corresponding TeX; 30-page PDF text extraction and first-page visual check.'})
for p in source.rglob('*'):
    if p.is_file():
        assert sha(p) == sha(outer/'source_and_certificates'/p.relative_to(source))
out = {'record_id':'22089748', 'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'reader_pdfs':items, 'unique_reader_pdf_count':1, 'distinct_supplementary_pdf_count':0, 'nested_source_archive':'Byte-identical to separately published source archive, including its 30-page PDF; no new reader document.', 'source_tree_copy_files_equal':73, 'manifests':manifest, 'scope':'Independent SHA-256 and complete regular-file-set comparison only. No manuscript verification program or replay launcher executed.'}
(r/'reader-documents.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
