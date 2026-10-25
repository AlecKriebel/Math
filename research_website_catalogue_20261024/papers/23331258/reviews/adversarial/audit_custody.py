"""Read-only originals/archives/prior packets; write own additive receipts only.

No extraction, imports from supplied code, source execution or network access.
"""
import datetime
import gzip
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import stat
import tarfile
import zipfile

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S = P / 'papers/23331258/sources'
D = P / 'papers/23331258/reviews/adversarial'
E = P / 'papers/23331258/reviews/scope'


def binding(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def check(path, expected):
    got = binding(path)
    assert got['sha256'] == expected['sha256'], str(path)
    assert got['bytes'] == expected['bytes'], str(path)
    return got


def safe(name):
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts and '\\' not in name
    assert str(p) == name.rstrip('/') and name


def write(name, obj):
    target = D / name
    assert not target.exists()
    target.write_text(json.dumps(obj, indent=2) + '\n')


def run():
    utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    ready_manifest = json.loads((S / 'SOURCE_READY_MANIFEST.json').read_text())
    original = [check(S / row['path'], row) for row in ready_manifest['files']]
    assert len(original) == 60
    ready_seal = json.loads((S / 'SOURCE_READY_SEAL.json').read_text())
    assert binding(S / 'SOURCE_READY.json')['sha256'] == ready_seal['ready_sha256']
    assert binding(S / 'SOURCE_READY_MANIFEST.json')['sha256'] == ready_seal['manifest_sha256']
    outer = []
    archive = S / 'three-terminal-bsp-source-verification-v1.0.zip'
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        names = set()
        for info in z.infolist():
            safe(info.filename)
            assert info.filename not in names
            names.add(info.filename)
            assert not info.flag_bits & 1
            if info.is_dir():
                continue
            mode = info.external_attr >> 16
            assert not mode or stat.S_IFMT(mode) in (0, stat.S_IFREG)
            raw = z.read(info)
            local = S / 'published-source' / info.filename
            assert raw == local.read_bytes()
            outer.append(dict(member=info.filename, bytes=len(raw),
                              sha256=hashlib.sha256(raw).hexdigest(),
                              crc32=f'{info.CRC:08x}', matches_original=str(local)))
    assert len(outer) == 50
    tarpath = S / 'published-source/original_packet/AUTHOR_FREEZE.tar.gz'
    expanded = gzip.decompress(tarpath.read_bytes())  # validates full gzip CRC/trailer
    inner = []
    with tarfile.open(fileobj=io.BytesIO(expanded), mode='r:') as t:
        names = set()
        for member in t:
            safe(member.name)
            assert member.name not in names
            names.add(member.name)
            if member.isdir():
                continue
            assert member.isfile() and not member.issym() and not member.islnk()
            suffix = PurePosixPath(member.name).relative_to('three_terminal_30000347')
            local = S / 'published-source/original_packet/frozen_packet' / suffix
            raw = t.extractfile(member).read()
            assert len(raw) == member.size and raw == local.read_bytes()
            inner.append(dict(member=member.name, bytes=len(raw),
                              sha256=hashlib.sha256(raw).hexdigest(),
                              matches_existing_original=str(local)))
    assert len(inner) == 7
    write('ORIGINAL_BINDINGS.json', dict(utc=utc, originals=original,
          source_ready_manifest=binding(S / 'SOURCE_READY_MANIFEST.json'),
          source_ready_seal=binding(S / 'SOURCE_READY_SEAL.json'),
          outer_archive=binding(archive), outer_members=outer,
          nested_tar=binding(tarpath), gzip_crc_validated=True,
          uncompressed_tar_bytes=len(expanded),
          uncompressed_tar_sha256=hashlib.sha256(expanded).hexdigest(),
          nested_tar_members=inner, recursive_regular_member_occurrences=57,
          clarification='READY nested detector was ZIP-only; additive tar receipt preserves READY unchanged.'))
    prior = []
    dirs = [P / 'papers' / rid / 'reviews/adversarial' for rid in
            ('23074543', '23442760', '23395703', '23333353', '23416806', '23441617', '23576280')]
    dirs.append(P / 'verification/cfh-independent-code-audit-sol-20261025')
    for folder in dirs:
        manifest_path = folder / 'FINAL_MANIFEST.json'
        seal_path = folder / 'FINAL_SEAL.json'
        manifest = json.loads(manifest_path.read_text())
        seal = json.loads(seal_path.read_text())
        assert binding(manifest_path)['sha256'] == seal['manifest_sha256']
        rows = manifest['files']
        if isinstance(rows, dict):
            rows = [dict(path=name, **data) for name, data in rows.items()]
        owned = [check(folder / row['path'], row) for row in rows]
        prior.append(dict(directory=str(folder), manifest=binding(manifest_path),
                          seal=binding(seal_path), owned_files=owned))
    primary_names = ('krause-owr2005.pdf', 'krause2006.pdf', 'khachiyan2008-response',
                     'poljak1974.pdf', 'ferudun23358810.pdf', 'baier2010.pdf', 'dvorak-knop.pdf')
    primaries = [binding(E / 'cache/primary' / name) for name in primary_names]
    primaries.append(binding(P / 'papers/23181280/reviews/scope/cache/primary/karp1972.pdf'))
    assert all(Path(row['path']).read_bytes().startswith(b'%PDF-') for row in primaries)
    receipt_names = ('primary-fetch-receipts.json', 'tar-custody-addendum.json',
                     'reused-primary-custody.json', 'later-related-primary-receipts.json',
                     'bienstock-access-receipt.json')
    receipts = [binding(E / name) for name in receipt_names]
    receipts.append(binding(E / 'cache/primary/ferudun23358810-record.raw.json'))
    write('PRESERVATION_BINDINGS.json', dict(utc=utc, prior_packets=prior,
          prior_packet_count=len(prior),
          prior_owned_file_count=sum(len(row['owned_files']) for row in prior),
          primary_objects=primaries, primary_receipts=receipts,
          source_ready_manifest=binding(S / 'SOURCE_READY_MANIFEST.json'),
          source_ready_seal=binding(S / 'SOURCE_READY_SEAL.json')))
    print(json.dumps(dict(originals=len(original), outer_members=len(outer),
          nested_tar_members=len(inner), prior_packets=len(prior),
          prior_owned_files=sum(len(row['owned_files']) for row in prior),
          actual_primary_pdfs=len(primaries)), sort_keys=True))


if __name__ == '__main__':
    run()
