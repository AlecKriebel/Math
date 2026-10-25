from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, zipfile, io
from pypdf import PdfReader

B = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
for id, main, archive, manifest_name in [
    ('23410944', 'paper.pdf', 'source-and-verification.zip', 'MANIFEST.json'),
    ('23422055', 'anti-invariant-four-manifold-v1.0.pdf', 'anti-invariant-four-manifold-verification-v1.0.zip', 'PACKAGE_MANIFEST.json'),
]:
    p = B/id
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
        checks.append(dict(filename=f['name'], bytes=len(b), sha256=sha, md5=md5, passed=True))
    z = zipfile.ZipFile(s/archive)
    assert z.testzip() is None
    manifest = json.loads(z.read(manifest_name))['files']
    if isinstance(manifest, dict):
        manifest = [dict(path=k, **v) for k,v in manifest.items()]
    for f in manifest:
        b = z.read(f['path'])
        assert len(b) == f['bytes'] and hashlib.sha256(b).hexdigest() == f['sha256']
    main_bytes = (s/main).read_bytes()
    pdfs, nested = [], []
    def inspect(zz, prefix=''):
        for name in zz.namelist():
            if name.endswith('.pdf'):
                b = zz.read(name)
                pdfs.append(dict(path=prefix+name, pages=len(PdfReader(io.BytesIO(b)).pages), sha256=hashlib.sha256(b).hexdigest(), identical_to_main=b == main_bytes))
            elif name.endswith('.zip'):
                inner = zipfile.ZipFile(io.BytesIO(zz.read(name)))
                assert inner.testzip() is None
                nested.append(dict(path=prefix+name, members=len(inner.infolist()), crc_pass=True))
                inspect(inner, prefix+name+'!/')
    inspect(z)
    result = dict(timestamp_utc=datetime.now(timezone.utc).isoformat(), all_public_record_assets_present=True,
                  files=checks, zip_crc_pass=True, top_level_manifest=manifest_name,
                  manifest_entries_verified=len(manifest), main_pdf_pages=len(PdfReader(s/main).pages),
                  pdf_members=pdfs, nested_archives=nested, passed=True,
                  boundary='Read-only byte integrity and page inventory; no archived review verdict contents read or adopted.')
    (p/'reviews/scope/source_integrity.json').write_text(json.dumps(result, indent=2)+'\n')
    (p/'reviews/scope/rendered/.gitignore').write_text('*\n!.gitignore\n')
    print(id, len(manifest), pdfs, nested)
