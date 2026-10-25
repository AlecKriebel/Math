"""Own one-use additive custody receipts; originals and prior packets read-only."""
from pathlib import Path, PurePosixPath
import datetime
import hashlib
import json
import stat
import zipfile

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S = P / 'papers/23217863/sources'
D = P / 'papers/23217863/reviews/adversarial'
E = P / 'papers/23217863/reviews/scope'
R = Path('/Users/alec/Documents/Math/openai_followon_banach_mazur_von_neumann')


def binding(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def check(path, row):
    result = binding(path)
    assert result['bytes'] == row['bytes'] and result['sha256'] == row['sha256'], str(path)
    return result


def write(name, obj):
    path = D / name
    assert not path.exists()
    path.write_text(json.dumps(obj, indent=2) + '\n')


utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest = json.loads((S / 'SOURCE_READY_MANIFEST.json').read_text())
originals = [check(S / row['path'], row) for row in manifest['files']]
assert len(originals) == 50
seal = json.loads((S / 'SOURCE_READY_SEAL.json').read_text())
assert binding(S / 'SOURCE_READY_MANIFEST.json')['sha256'] == seal['manifest_sha256']
assert binding(S / 'SOURCE_READY.json')['sha256'] == seal['SOURCE_READY_sha256']
members = []
names = set()
archive = S / 'source-and-verification.zip'
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for info in z.infolist():
        name = info.filename
        path = PurePosixPath(name)
        assert not path.is_absolute() and '..' not in path.parts and '\\' not in name
        assert name.rstrip('/') == str(path) and name not in names
        names.add(name)
        assert not info.flag_bits & 1
        if info.is_dir():
            continue
        mode = info.external_attr >> 16
        assert stat.S_IFMT(mode) in (0, stat.S_IFREG)
        raw = z.read(info)
        assert not raw.startswith((b'PK\x03\x04', b'\x1f\x8b'))
        assert raw[257:262] != b'ustar'
        local = S / 'published-source' / name
        assert raw == local.read_bytes()
        members.append(dict(member=name, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                            crc32=f'{info.CRC:08x}', existing_original=str(local)))
assert len(members) == 41
write('ORIGINAL_BINDINGS.json', dict(utc=utc, originals=originals,
      source_manifest=binding(S / 'SOURCE_READY_MANIFEST.json'),
      source_seal=binding(S / 'SOURCE_READY_SEAL.json'), archive=binding(archive),
      complete_regular_zip_members=members, nested_archives_detected=0,
      no_extraction_or_original_mutation=True))
prior = []
for folder in [P / 'papers' / rid / 'reviews/adversarial' for rid in
               ('23074543', '23442760', '23395703', '23333353', '23416806', '23441617', '23576280', '23331258')
               ] + [P / 'verification/cfh-independent-code-audit-sol-20261025']:
    mp, sp = folder / 'FINAL_MANIFEST.json', folder / 'FINAL_SEAL.json'
    m, s = json.loads(mp.read_text()), json.loads(sp.read_text())
    assert binding(mp)['sha256'] == s['manifest_sha256']
    rows = m['files']
    if isinstance(rows, dict):
        rows = [dict(path=name, **row) for name, row in rows.items()]
    owned = [check(folder / row['path'], row) for row in rows]
    prior.append(dict(directory=str(folder), manifest=binding(mp), seal=binding(sp), owned_files=owned))
names = ('openai295-pinned.pdf', 'openai295-current.pdf', 'ricard-roydor-v2.pdf',
         'sherman-v2.pdf', 'popa2014-v3.pdf', 'jkr1972.pdf', 'cpss2003-v2.pdf', 'nelson209.pdf')
primaries = [binding(E / 'cache/primary' / name) for name in names]
primaries.extend(binding(R / 'sources/roydor' / name) for name in
                 ('roydor2020_user_supplied.pdf', 'roydor_slides.pdf'))
assert all(Path(row['path']).read_bytes().startswith(b'%PDF-') for row in primaries)
upstream = S / 'published-source/sources/upstream/Vanishing-of-higher-bounded-Hochschild-cohomology-September-23-2026/paper.pdf'
assert (E / 'cache/primary/openai295-pinned.pdf').read_bytes() == upstream.read_bytes()
assert (E / 'cache/primary/openai295-current.pdf').read_bytes() == upstream.read_bytes()
receipts = [binding(E / name) for name in ('primary-fetch-receipts.json',
             'critical-primary-fetch-receipts.json', 'structure-primary-fetch-receipts.json')]
receipts.append(binding(R / 'receipts/roydor_user_supplied_source_20261007.json'))
write('PRESERVATION_BINDINGS.json', dict(utc=utc, prior_packets=prior,
      prior_packet_count=len(prior), prior_owned_file_count=sum(len(x['owned_files']) for x in prior),
      actual_primary_pdf_objects=primaries, raw_primary_receipts=receipts,
      pinned_current_and_bundled_upstream_pdf_byteidentical=True,
      human_supplied_roydor_not_misrepresented_as_fresh_http=True))
print(json.dumps(dict(originals=len(originals), zip_members=len(members),
      prior_packets=len(prior), prior_owned_files=sum(len(x['owned_files']) for x in prior),
      actual_primary_pdf_objects=len(primaries)), sort_keys=True))
