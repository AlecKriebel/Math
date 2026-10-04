#!/usr/bin/env python3
"""Fetch original sources and preserve complete acquisition streams."""
import datetime, gzip, hashlib, json, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parent
PRIVATE = ROOT / 'private_sources'
CAP = ROOT / 'captures'

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def run(label, argv):
    started = utc()
    proc = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    record = {'label': label, 'argv': argv, 'start_utc': started, 'end_utc': utc(),
              'exit_code': proc.returncode}
    for stream, data in [('stdout', proc.stdout), ('stderr', proc.stderr)]:
        path = CAP / (label + '.' + stream + '.gz')
        path.write_bytes(gzip.compress(data, mtime=0))
        record[stream] = {'path': str(path.relative_to(ROOT)), 'bytes': len(data),
                          'sha256': hashlib.sha256(data).hexdigest()}
    (CAP / (label + '.receipt.json')).write_text(json.dumps(record, indent=2) + '\n')
    if proc.returncode:
        raise RuntimeError(json.dumps(record))
    return record

sources = [
    ('hayman_lingham_2018', 'https://arxiv.org/pdf/1809.07200', 1706228,
     '8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0'),
    ('carleson_1976', 'https://www.acadsci.fi/mathematica/Vol02/vol02pp035-039.pdf', 3653618,
     '4f4d183b2bdb68752b9c46d7bd866748a25615d2ab2d8b3b7a2644d28cc29aae'),
]
receipts = []
for name, url, size, expected in sources:
    pdf = PRIVATE / (name + '.pdf')
    headers = PRIVATE / (name + '.http_headers')
    fetched = run(name + '_fetch', ['/usr/bin/curl', '--fail', '--location', '--silent',
                                  '--show-error', '--dump-header', str(headers),
                                  '--output', str(pdf), url])
    data = pdf.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    receipt = {'name': name, 'url': url, 'expected_bytes': size, 'actual_bytes': len(data),
               'expected_sha256': expected, 'actual_sha256': digest,
               'matching': len(data) == size and digest == expected, 'fetch': fetched}
    run(name + '_extract', ['/opt/homebrew/bin/pdftotext', '-layout', str(pdf), str(PRIVATE / (name + '.txt'))])
    if name == 'hayman_lingham_2018':
        run(name + '_page61_extract', ['/opt/homebrew/bin/pdftotext', '-f', '61', '-l', '61', '-layout', str(pdf), str(ROOT / 'hayman_page61.txt')])
        run(name + '_page61_render', ['/opt/homebrew/bin/pdftoppm', '-f', '61', '-l', '61', '-r', '100', '-jpeg', '-singlefile', str(pdf), str(PRIVATE / 'hayman_page61')])
    else:
        run(name + '_render', ['/opt/homebrew/bin/pdftoppm', '-r', '100', '-jpeg', str(pdf), str(PRIVATE / 'carleson')])
        (ROOT / 'carleson_all_pages.txt').write_bytes((PRIVATE / (name + '.txt')).read_bytes())
    for raw in [pdf, PRIVATE / (name + '.txt'), headers]:
        original = raw.read_bytes()
        zipped = raw.with_name(raw.name + '.gz')
        zipped.write_bytes(gzip.compress(original, mtime=0))
        raw.unlink()
        receipt.setdefault('files', []).append({'path': str(zipped.relative_to(ROOT)),
                                               'bytes': len(original), 'sha256': hashlib.sha256(original).hexdigest(),
                                               'gzip_bytes': zipped.stat().st_size})
    receipts.append(receipt)
(ROOT / 'source_receipts.json').write_text(json.dumps({'completed_utc': utc(), 'sources': receipts}, indent=2) + '\n')
print(json.dumps({'completed_utc': utc(), 'matching': [r['matching'] for r in receipts]}))
