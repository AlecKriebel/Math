from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, zipfile, io
from pypdf import PdfReader

B = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
for ident, main, archive, prefix in [
    ('23203334', 'paper.pdf', 'source-and-verification.zip', 'source-and-verification/'),
    ('22013710', 'exceptional-ybe-d4-v1.2.0.pdf', 'exceptional-ybe-d4-v1.2.0-source.zip', 'exceptional-ybe-d4-v1.2.0/'),
]:
    p = B/ident
    s = p/'sources'
    record = json.loads((s/'record.json').read_text())
    receipt = json.loads((s/'receipt.json').read_text())
    assert {f['key'] for f in record['files']} == {f['name'] for f in receipt['files']}
    checks = []
    for f in receipt['files']:
        b = (s/f['name']).read_bytes()
        sha = hashlib.sha256(b).hexdigest()
        md5 = hashlib.md5(b).hexdigest()
        assert sha == f['sha256'] and 'md5:'+md5 == f['zenodo_checksum'] and len(b) == f['bytes']
        live = next(g for g in record['files'] if g['key'] == f['name'])
        assert live['checksum'] == f['zenodo_checksum'] and live['size'] == len(b)
        checks.append(dict(filename=f['name'], bytes=len(b), sha256=sha, md5=md5, passed=True))
    z = zipfile.ZipFile(s/archive)
    assert z.testzip() is None
    if ident == '23203334':
        manifest_name = prefix+'SHA256SUMS.json'
        manifest = json.loads(z.read(manifest_name))
    else:
        manifest_name = prefix+'SHA256SUMS'
        manifest = {line.split(None, 1)[1].lstrip('*'):line.split(None, 1)[0] for line in z.read(manifest_name).decode().splitlines() if line.strip()}
    for name, expected in manifest.items():
        b = z.read(prefix+name)
        assert hashlib.sha256(b).hexdigest() == expected, name
        assert (s/'published-source'/prefix/name).read_bytes() == b, name
    main_bytes = (s/main).read_bytes()
    pdfs, nested = [], []
    def inspect(zz, name_prefix=''):
        for name in zz.namelist():
            if name.endswith('.pdf'):
                b = zz.read(name)
                pdfs.append(dict(path=name_prefix+name, pages=len(PdfReader(io.BytesIO(b)).pages), sha256=hashlib.sha256(b).hexdigest(), identical_to_main=b == main_bytes))
            elif name.endswith('.zip'):
                inner = zipfile.ZipFile(io.BytesIO(zz.read(name)))
                assert inner.testzip() is None
                nested.append(dict(path=name_prefix+name, members=len(inner.infolist()), crc_pass=True))
                inspect(inner, name_prefix+name+'!/')
    inspect(z)
    external_manifest = []
    if ident == '22013710':
        for line in (s/'SHA256SUMS').read_text().splitlines():
            expected, name = line.split(None, 1)
            name = name.lstrip('*')
            assert hashlib.sha256((s/name).read_bytes()).hexdigest() == expected
            external_manifest.append(name)
    result = dict(timestamp_utc=datetime.now(timezone.utc).isoformat(), all_public_record_assets_present=True,
                  files=checks, zip_crc_pass=True, top_level_manifest=manifest_name,
                  manifest_entries_verified=len(manifest), extracted_manifest_bytes_match=True,
                  external_manifest_entries_verified=external_manifest,
                  main_pdf_pages=len(PdfReader(s/main).pages), pdf_members=pdfs, nested_archives=nested,
                  passed=True, boundary='Byte integrity and page inventory only. No mathematical validation is inferred from a successful hash check. Historical opinion exposure is documented separately in REVIEW.md.')
    (p/'reviews/scope/source_integrity.json').write_text(json.dumps(result, indent=2)+'\n')
    print(ident, len(manifest), pdfs, nested)
