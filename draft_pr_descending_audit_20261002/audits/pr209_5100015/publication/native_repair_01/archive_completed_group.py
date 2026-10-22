"""Archive finished synthetic fixtures between probe groups to bound disk use."""
from pathlib import Path
import hashlib, json, shutil, zipfile


def archive_completed_group(here, runs, label):
    here, runs = Path(here), Path(runs)
    folders = sorted(runs.iterdir()) if runs.exists() else []
    if not folders:
        return None
    rows, files = [], []
    for folder in folders:
        if not folder.is_dir() or folder.is_symlink():
            raise RuntimeError('Unsafe fixture ownership')
        for p in sorted(folder.rglob('*')):
            if p.is_symlink():
                raise RuntimeError('Symlinked fixture')
            if p.is_file():
                raw = p.read_bytes()
                rows.append(dict(path=p.relative_to(here).as_posix(), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
                files.append(p)
    out = here / ('FIXTURES_' + label + '.zip')
    with zipfile.ZipFile(out, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for row, p in zip(rows, files):
            archive.writestr(row['path'], p.read_bytes())
        archive.writestr('SYNTHETIC_FIXTURE_MANIFEST.json', json.dumps(dict(synthetic_only=True, files=rows), indent=2) + '\n')
    with zipfile.ZipFile(out) as archive:
        if set(archive.namelist()) != {r['path'] for r in rows} | {'SYNTHETIC_FIXTURE_MANIFEST.json'}:
            raise RuntimeError('Archive set mismatch; originals retained')
        for row, p in zip(rows, files):
            raw = archive.read(row['path'])
            if raw != p.read_bytes() or len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
                raise RuntimeError('Archive byte mismatch; originals retained')
    receipt = dict(path=out.name, bytes=out.stat().st_size, sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
        fixture_files=len(rows), uncompressed_bytes=sum(r['bytes'] for r in rows),
        synthetic_only=True, full_set_and_every_body_verified_before_removing_duplicates=True)
    (here / ('FIXTURES_' + label + '.receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n')
    for folder in folders:
        shutil.rmtree(folder)
    return receipt
