"""Read-only primary acquisition/extraction; whole bodies remain private/excluded."""
import hashlib, json, os, subprocess, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path
from pypdf import PdfReader
FAMILY = Path(__file__).resolve().parent
PRIVATE = FAMILY.parent / 'private_primary_reading_cache' / FAMILY.name
CHILDREN = FAMILY / 'primary_child_captures'
def utc(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def write(p, obj): p.write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')
def download(name, url, pdf):
    start = utc()
    request = urllib.request.Request(url, headers={'User-Agent': 'Independent math source verification'})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            b = response.read(10000001)
            status, final = response.status, response.url
        assert len(b) <= 10000000
        if pdf: assert b.startswith(b'%PDF-')
        path = PRIVATE / (name + ('.pdf' if pdf else '.json'))
        path.write_bytes(b); path.chmod(0o444)
        rec = {'name': name, 'requested_url': url, 'final_url': final, 'HTTP_status': status,
               'started_utc': start, 'ended_utc': utc(), 'bytes': len(b), 'sha256': sha(b),
               'private_absolute_path': str(path), 'acquired': True, 'whole_body_redistributed': False}
        if pdf: rec['pages'] = len(PdfReader(path).pages)
        return rec
    except Exception as error:
        # Preserve failed response bodies privately if the HTTPError supplies one.
        body = error.read() if isinstance(error, urllib.error.HTTPError) else b''
        if body:
            p = PRIVATE / (name + '.failed_response.bin'); p.write_bytes(body); p.chmod(0o444)
        return {'name': name, 'requested_url': url, 'started_utc': start, 'ended_utc': utc(),
                'acquired': False, 'error_type': type(error).__name__, 'error': str(error),
                'HTTP_failure_body_bytes': len(body), 'HTTP_failure_body_sha256': sha(body),
                'HTTP_failure_body_private_retained': bool(body), 'whole_body_redistributed': False}
def child(name, argv, source_sha):
    started = utc()
    with (CHILDREN / (name + '.stdout.bin')).open('wb') as out, (CHILDREN / (name + '.stderr.bin')).open('wb') as err:
        proc = subprocess.Popen(argv, stdout=out, stderr=err)
        cap = {'owner_pid': os.getpid(), 'owned_child_pid': proc.pid, 'argv': argv,
               'started_utc': started, 'source_pdf_sha256': source_sha}
        write(CHILDREN / (name + '.PRELAUNCH.json'), cap); code = proc.wait()
    cap.update(ended_utc=utc(), exit_code=code)
    for stream in ('stdout', 'stderr'):
        p = CHILDREN / (name + '.' + stream + '.bin'); b = p.read_bytes()
        cap[stream + '_file'] = p.name; cap[stream + '_bytes'] = len(b); cap[stream + '_sha256'] = sha(b)
    return cap
def main():
    PRIVATE.mkdir(parents=True, exist_ok=False); CHILDREN.mkdir()
    # Whole primary cache excluded from future Git/publication packages.
    (PRIVATE / '.gitignore').write_text('*\n'); (PRIVATE / '.gitignore').chmod(0o444)
    specs = [('owr_2013', 'https://ems.press/content/serial-article-files/46446', [60]),
        ('akopyan_barany_robins_v2', 'https://arxiv.org/pdf/1508.07594v2', [1,3,8,9,10,12]),
        ('gravin_pasechnik_shapiro_v2', 'https://arxiv.org/pdf/1210.3193v2', [3])]
    sources, runs = [], []
    for name, url, pages in specs:
        rec = download(name, url, True); sources.append(rec)
        if not rec['acquired']: continue
        p = Path(rec['private_absolute_path'])
        runs.append(child(name + '_text', ['/opt/homebrew/bin/pdftotext', '-layout', str(p),
                           str(PRIVATE / (name + '.layout.txt'))], rec['sha256']))
        for page in pages:
            runs.append(child(name + '_page_' + str(page), ['/opt/homebrew/bin/pdftoppm',
                '-f', str(page), '-l', str(page), '-scale-to', '1500', '-png', '-singlefile',
                str(p), str(PRIVATE / (name + '_page_' + str(page)))], rec['sha256']))
    # Publisher version access is tried once; failure is preserved and qualified.
    sources.append(download('ABR_publisher_pdf_attempt',
        'https://www.sciencedirect.com/science/article/pii/S0001870815302425/pdfft', True))
    crossref = download('ABR_crossref_metadata',
        'https://api.crossref.org/works/10.1016/j.aim.2016.12.026', False)
    sources.append(crossref)
    published = None
    if crossref['acquired']:
        m = json.loads(Path(crossref['private_absolute_path']).read_bytes())['message']
        published = {key: m.get(key) for key in ('DOI','title','container-title','volume','page','published','publisher')}
    private = []
    for p in sorted(PRIVATE.iterdir()):
        if p.is_file():
            p.chmod(0o444); b = p.read_bytes()
            private.append({'absolute_path': str(p), 'bytes': len(b), 'sha256': sha(b), 'full_mode_07777': '0444'})
    PRIVATE.chmod(0o755)
    write(CHILDREN / 'OWNED_RUNS.json', runs)
    write(FAMILY / 'PRIMARY_SOURCE_RECEIPTS.json', {'schema': 'pr58-tangent-primary-receipts/v1',
        'operator_pid': os.getpid(), 'utc': utc(), 'sources': sources, 'published_metadata': published,
        'private_whole_body_references': private, 'ROOT_cache_required': False,
        'whole_PDF_bulk_text_PNG_public_redistribution': False,
        'publisher_full_PDF_available': sources[-2]['acquired'],
        'author_manuscript_is_not_asserted_byte_identical_to_published_article': True})
    print(json.dumps({'operator_pid': os.getpid(), 'utc': utc(), 'sources': sources,
                       'owned_Poppler_children': len(runs), 'child_exit_codes': [c['exit_code'] for c in runs],
                       'published_metadata': published}, indent=2, sort_keys=True))
    assert all(c['exit_code'] == 0 for c in runs)
    assert all(s['acquired'] for s in sources[:3])
if __name__ == '__main__': main()
