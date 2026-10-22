"""Losslessly archive only the completed unsealed fixtures of this review."""
from pathlib import Path
import datetime, hashlib, json, zipfile
HERE=Path(__file__).resolve().parent
roots=[HERE/'minimal_synthetic_case',HERE/'SYNTHETIC_SUCCESSOR_PARSER_ONLY',HERE/'stream_fixture']
files=sorted(p for root in roots for p in root.rglob('*') if p.is_file())
assert files and all(not p.is_symlink() for p in files)
rows=[]
for p in files:
    b=p.read_bytes()
    rows.append(dict(path=p.relative_to(HERE).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
archive=HERE/'EXACT_OWN_FIXTURES.zip'
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:z.write(p,p.relative_to(HERE).as_posix())
with zipfile.ZipFile(archive) as z:
    assert set(z.namelist())=={r['path'] for r in rows} and len(z.namelist())==len(rows)
    assert z.testzip() is None
    for p,r in zip(files,rows):
        raw=z.read(r['path'])
        assert raw==p.read_bytes() and len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
receipt=dict(schema='pr209-source04-own-fixture-storage-v1',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    archive=dict(path=archive.name,bytes=archive.stat().st_size,sha256=hashlib.sha256(archive.read_bytes()).hexdigest()),
    exact_members_CRC_every_original_body_verified=True,files=rows,
    scope='Only this reviewer completed synthetic fixtures; no candidate, science, prior capsule, cache, environment or foreign path changed',
    original_paths_represented_losslessly_in_archive=True)
(HERE/'EXACT_OWN_FIXTURES_MANIFEST.json').write_text(json.dumps(receipt,indent=2)+'\n')
for p in files:p.unlink()
for root in roots:
    for d in sorted((p for p in root.rglob('*') if p.is_dir()),key=lambda p:len(p.parts),reverse=True):d.rmdir()
    root.rmdir()
print(json.dumps(dict(files=len(rows),original_bytes=sum(r['bytes'] for r in rows),archive_bytes=archive.stat().st_size,verified_before_removal=True)))
