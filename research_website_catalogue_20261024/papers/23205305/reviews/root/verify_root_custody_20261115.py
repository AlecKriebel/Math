"""Read-only root custody; no project import, subprocess, network or execution."""
from pathlib import Path
import hashlib
import json
import os
import stat
import zipfile

ROOT = Path(__file__).absolute().parent
PAPER = ROOT.parent.parent
CHECKS = 0


def need(ok, label):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(label)


def read(path):
    need(path.resolve() == path and stat.S_ISREG(path.lstat().st_mode),
         'ordinary real file: ' + str(path))
    return path.read_bytes()


def desc(body):
    return {'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest()}


def pinned(path, row):
    body = read(path)
    need(desc(body) == {k: row[k] for k in ('bytes', 'SHA256')},
         'whole unchanged: ' + str(path))
    return body


def extent(root):
    files, directories = [], []
    need(root.resolve() == root and stat.S_ISDIR(root.lstat().st_mode), 'real root')
    for directory, subdirectories, names in os.walk(root, followlinks=False):
        for name in subdirectories:
            path = Path(directory) / name
            need(stat.S_ISDIR(path.lstat().st_mode), 'no directory symlink')
            directories.append(path.relative_to(root).as_posix())
        for name in names:
            path = Path(directory) / name
            need(stat.S_ISREG(path.lstat().st_mode), 'no link or special')
            files.append(path.relative_to(root).as_posix())
    return sorted(files), sorted(directories)


def sealed_family(lane, final_sha, manifest_name, payload_key, terms, dirs_key):
    root = PAPER / 'reviews' / lane
    body = read(root / 'FINAL_SEAL.json')
    need(hashlib.sha256(body).hexdigest() == final_sha, 'exact family FINAL')
    seal = json.loads(body)
    manifest_body = pinned(root / manifest_name, seal['manifest'])
    manifest = json.loads(manifest_body)
    rows = manifest[payload_key]
    if isinstance(rows, list):
        rows = {r['path']: r for r in rows}
    need(extent(root) == (sorted([*rows, *terms]), manifest[dirs_key]),
         'finite family files and exact directories')
    for name, row in rows.items():
        pinned(root / name, row)
    return seal, manifest


def main():
    _, scope = sealed_family(
        'scope', 'c3a4d4e12269affee86657633b38f910296545b8d909c613587a1e9fcfce222f',
        'MANIFEST.json', 'payloads', ['MANIFEST.json', 'FINAL_SEAL.json'], 'directories')
    _, adversarial = sealed_family(
        'adversarial', '67e2e3b9b6ba7bee3be26055cd516516fea33e44d85476019befea236dd1ded8',
        'FINAL_MANIFEST.json', 'owned_payloads',
        ['FINAL_MANIFEST.json', 'FINAL_CLOSURE.json', 'FINAL_SEAL.json'], 'owned_directories')
    inputs = json.loads(read(PAPER / 'reviews/adversarial/FINAL_INPUTS.json'))
    source = PAPER / 'sources'
    rows = inputs['source_fullbyte_pins']
    need(len(rows) == 126, 'literal source126')
    need(extent(source) ==
         (sorted(Path(r['path']).relative_to(source).as_posix() for r in rows),
          inputs['source_directories']), 'entire frozen source namespace')
    for row in rows:
        pinned(Path(row['path']), row)
    ready = read(source / 'SOURCE_READY.json')
    seal = read(source / 'SOURCE_READY_SEAL.json')
    need(hashlib.sha256(ready).hexdigest() ==
         'd5e1575052e0db802b6d8ff47309660b50213d91594856eb4df141943bf0db91', 'READY')
    need(hashlib.sha256(seal).hexdigest() ==
         '6540b1c94839ae033e0747843452bd6c33d29c3734680332c8cbc119e79fdcc8', 'source FINAL')
    protected = json.loads(read(PAPER / 'reviews/scope/PROTECTED_INPUTS.json'))
    need(len(protected['files']) == 144 and len(protected['core_files']) == 18,
         'source126 plus qualified17original and sole405b')
    for row in protected['files']:
        body = pinned(Path(row['path']), row)
        need(body == read(PAPER / 'reviews/scope' / row['copy']), 'whole protected copy')
    initial = read(ROOT / 'INITIAL_RECONSTRUCTION_20261115.md')
    need(hashlib.sha256(initial).hexdigest() ==
         'dd590d0b54b7ec072d910d6526db36707b0fa105be77f28580c4f2cda23cd9d5',
         'unchanged manuscript-first root INITIAL')
    manifest = json.loads(read(source / 'SOURCE_READY_MANIFEST.json'))
    for row in manifest['files']:
        pinned(source / row['path'], row)
    archives = sorted((source / 'assets').glob('*.zip'))
    need(len(archives) == 2, 'actual two native ZIP containers')
    count, expanded = 0, 0
    for path in archives:
        with zipfile.ZipFile(path) as archive:
            for member in archive.infolist():
                if member.is_dir():
                    continue
                body = archive.read(member)
                need(len(body) == member.file_size, 'whole member length/CRC')
                count += 1
                expanded += len(body)
    need(count == 61 and expanded == 567624, 'native whole regular occurrences')
    print(json.dumps({'status': 'PASS_ROOT_SOURCE_AND_INDEPENDENT_FAMILY_CUSTODY',
                      'checks': CHECKS, 'source_files': 126,
                      'scope_files': len(scope['payloads']) + 2,
                      'adversarial_files': len(adversarial['owned_payloads']) + 3,
                      'protected_original_files': 144,
                      'native_ZIP_regular_occurrences': count,
                      'source_or_scientific_execution': False,
                      'writes': 0, 'network': 0}, sort_keys=True))


if __name__ == '__main__':
    main()
