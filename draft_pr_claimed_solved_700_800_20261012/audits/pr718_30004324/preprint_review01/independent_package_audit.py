"""Independent read-only archive, hash, metadata, and correspondence audit."""
from pathlib import Path, PurePosixPath
import hashlib
import io
import json
import stat
import zipfile

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / 'snapshot'


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe(name):
    p = PurePosixPath(name)
    return (bool(name) and not p.is_absolute() and '\\' not in name and
            all(x not in ('', '.', '..') for x in name.split('/')) and str(p) == name)


def archive(data, label, ledger):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        require(z.testzip() is None, 'CRC failure ' + label)
        files = {}
        for i in z.infolist():
            require(safe(i.filename), 'Unsafe archive path ' + label)
            require(i.filename not in files, 'Duplicate archive entry ' + label)
            require(not i.is_dir(), 'Directory archive entry ' + label)
            mode = i.external_attr >> 16
            require(not stat.S_ISLNK(mode), 'Symlink archive entry ' + label)
            require(not (i.flag_bits & 1), 'Encrypted archive entry ' + label)
            files[i.filename] = z.read(i)
        ledger.append({'archive': label, 'files': len(files), 'sha256': digest(data),
                       'entries': [{'path': n, 'bytes': len(b), 'sha256': digest(b)}
                                   for n, b in sorted(files.items())]})
    return files


def main():
    inventory = json.loads((PACKAGE / 'PACKAGE_INVENTORY.json').read_text())
    checked = []
    for row in inventory['files']:
        require(safe(row['path']), 'Unsafe inventory path')
        b = (PACKAGE / row['path']).read_bytes()
        require(len(b) == row['bytes'], 'Wrong byte count ' + row['path'])
        require(digest(b) == row['sha256'], 'Wrong hash ' + row['path'])
        checked.append({'path': row['path'], 'bytes': len(b), 'sha256': digest(b)})
    require(len(checked) == len({r['path'] for r in checked}) == 6, 'Wrong outer inventory')
    ledger = []
    support = archive((PACKAGE / 'source-and-verification.zip').read_bytes(),
                      'source-and-verification.zip', ledger)
    kit = archive((PACKAGE / 'zenodo-upload-kit.zip').read_bytes(),
                  'zenodo-upload-kit.zip', ledger)
    require(set(kit) == {'paper.pdf', 'source-and-verification.zip',
                         'zenodo-deposit.json', 'zenodo-metadata.json', 'README.md'},
            'Wrong upload kit entries')
    require(kit['paper.pdf'] == (PACKAGE / 'output/pdf/paper.pdf').read_bytes(),
            'Kit PDF mismatch')
    require(kit['source-and-verification.zip'] == (PACKAGE / 'source-and-verification.zip').read_bytes(),
            'Kit support archive mismatch')
    require(support['paper.tex'] == (PACKAGE / 'paper.tex').read_bytes(), 'Support source mismatch')
    require(support['README.md'] == (PACKAGE / 'README-verification.md').read_bytes(), 'Support README mismatch')
    require(support['verify_bundle.py'] == (PACKAGE / 'verify_bundle.py').read_bytes(), 'Support verifier mismatch')
    require(inventory['support_files'] == len(support) == 78, 'Wrong support file count')
    manifest = json.loads(support['MANIFEST.json'])
    manifest_names = set()
    for row in manifest['files']:
        name = row['path']
        require(safe(name) and name not in manifest_names and name != 'MANIFEST.json', 'Bad support manifest entry')
        manifest_names.add(name)
        require(name in support and len(support[name]) == row['bytes'] and
                digest(support[name]) == row['sha256'], 'Support manifest mismatch ' + name)
    require(set(support) == manifest_names | {'MANIFEST.json'}, 'Support closed inventory mismatch')
    deposits = [json.loads((PACKAGE / 'zenodo-deposit.json').read_text()), json.loads(kit['zenodo-deposit.json'])]
    metadata = [json.loads((PACKAGE / 'zenodo-metadata.json').read_text())['metadata'],
                json.loads(support['zenodo-metadata.json'])['metadata'],
                json.loads(kit['zenodo-metadata.json'])['metadata'],
                *[d['metadata'] for d in deposits]]
    require(all(m == metadata[0] for m in metadata), 'Metadata correspondence mismatch')
    require(kit['zenodo-metadata.json'] == support['zenodo-metadata.json'] ==
            (PACKAGE / 'zenodo-metadata.json').read_bytes(), 'Metadata byte mismatch')
    m = metadata[0]
    require(m['title'] == inventory['title'] == 'Positive tangent-bundle Seshadri constants characterize projective space', 'Title mismatch')
    require(m['version'] == inventory['version'] == '1.0', 'Version mismatch')
    require((m['publication_date'], m['publication_type'], m['license'], m['access_right']) ==
            ('2026-10-12', 'preprint', 'cc-by-4.0', 'open'), 'Publication field mismatch')
    require(m['creators'] == [{'name': 'Kriebel, Alec', 'affiliation': 'Independent researcher',
                               'orcid': '0009-0001-9320-500X'}], 'Author metadata mismatch')
    require(deposits[0]['files'] == [{'path': 'output/pdf/paper.pdf', 'name': 'paper.pdf'},
                                   {'path': 'source-and-verification.zip', 'name': 'source-and-verification.zip'}],
            'Outer deposit file mapping wrong')
    require(deposits[1]['files'] == [{'path': 'paper.pdf'}, {'path': 'source-and-verification.zip'}],
            'Flat deposit file mapping wrong')
    all_leaves = {}
    def recurse(files, prefix):
        for name, raw in files.items():
            label = prefix + '/' + name
            if name.endswith('.zip'):
                recurse(archive(raw, label, ledger), label)
            else:
                all_leaves[label] = raw
    recurse(support, 'support')
    forbidden = [n for n, b in all_leaves.items()
                 if b.startswith(b'%PDF-') or PurePosixPath(n).suffix.lower() in
                 {'.pdf', '.docx', '.xlsx', '.png', '.jpg', '.jpeg', '.pem', '.key', '.p12', '.env'}]
    require(not forbidden, 'Third-party/binary/private-content candidate: ' + repr(forbidden))
    credential_marker_counts = {marker: sum(marker in b for b in all_leaves.values())
                                for marker in [b'-----BEGIN PRIVATE KEY-----', b'ghp_', b'github_pat_', b'Bearer ', b'AIza']}
    require(not any(credential_marker_counts.values()), 'Credential marker found')
    sensitive_name_candidates = [n for n in all_leaves if any(v in n.lower() for v in
                                 ['credentials', '.git/', 'coordination', 'transcript', 'source_download', 'source_text'])]
    require(not sensitive_name_candidates, 'Unexpected private/source filename')
    historical_count = sum(n.startswith('historical_candidate/') for n in support)
    require(historical_count == 49, 'Wrong original frozen file count')
    result = {'result': 'PASS', 'inventory': checked, 'support_files': len(support),
              'historical_files': historical_count, 'archive_ledger': ledger,
              'metadata_correspondence': 'Five metadata objects equal; three metadata files byte-identical',
              'nested_leaf_files': len(all_leaves), 'third_party_binary_candidates': forbidden,
              'credential_marker_counts': {k.decode(): v for k, v in credential_marker_counts.items()},
              'scope': 'Independent exact-byte/hash/archive/metadata checks; manual prose and mathematical review separate'}
    (ROOT / 'package_checks.json').write_text(json.dumps(result, indent=2) + '\n')
    clean = ROOT / 'tmp' / 'clean-extraction'
    clean.mkdir()
    for name, b in support.items():
        p = clean / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b)
    print(json.dumps({k: v for k, v in result.items() if k != 'archive_ledger'}, indent=2))


if __name__ == '__main__':
    main()
