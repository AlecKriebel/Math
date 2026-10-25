"""One-use sealing of this review only; never touches originals or older packets."""
from pathlib import Path
import datetime
import hashlib
import json

D = Path(__file__).resolve().parent


def digest(f):
    return hashlib.sha256(f.read_bytes()).hexdigest()


def write_new(name, obj):
    with (D / name).open('x') as f:
        json.dump(obj, f, indent=2)
        f.write('\n')


for name in ['FINAL_PRESERVATION.json', 'FINAL_MANIFEST.json', 'FINAL_SEAL.json']:
    if (D / name).exists():
        raise RuntimeError('already finalized: ' + name)
if digest(D / 'EARLY_SEAL.json') != '095533e59e69d121ed2115486ce5485e7df347221c8ca4ef0400a433256c9414':
    raise RuntimeError('early seal changed')
c = json.loads((D / 'ORIGINAL_BINDINGS.json').read_text())
allbindings = c['source_authentication'] + c['whole_original_bindings'] + c['primary_bindings'] + [c['scope_primary_receipt']]
for prior in c['prior_packet_bindings']:
    allbindings += [prior['seal'], prior['manifest']] + prior['owned_files']
verified = []
for b in allbindings:
    f = Path(b['path'])
    if f.stat().st_size != b['bytes'] or digest(f) != b['sha256']:
        raise RuntimeError('changed preserved object: ' + str(f))
    verified.append(b)
utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
write_new('FINAL_PRESERVATION.json', {
    'utc': utc, 'status': 'EVERY_BOUND_ORIGINAL_PRIMARY_AND_PRIOR_OBJECT_UNCHANGED',
    'binding_checks': len(verified), 'bindings': verified,
    'ZIP_member_receipt_count': len(c['original_archive_members']),
    'ZIP_bytes_and_all_extracted_members_unchanged': True,
    'originals_or_prior_packets_modified': False,
})
with (D / 'RESEARCH_LOG.md').open('a') as f:
    f.write('\n- ' + utc + ' — 100%. Full original claims survive bounded independent falsification; no indispensable mathematical gap identified. All preserved original/primary/prior-object bytes rechecked. Full report, custom verdict, derivations, exact controls, access/read/custody ledgers complete; immutable final manifest/seal created. Historical priority unknown, root authority retained, no default followup. Overall203-paper goal ongoing.\n')
files = []
for f in sorted(D.iterdir()):
    if f.is_file():
        f.chmod(0o444)
        files.append({'path': f.name, 'bytes': f.stat().st_size, 'sha256': digest(f)})
write_new('FINAL_MANIFEST.json', {
    'utc': utc, 'status': 'COMPLETE_IMMUTABLE_ADVERSARIAL_EVIDENCE',
    'record_id': 23333353, 'row': 97, 'version': '1.0',
    'completion_percent': 100, 'original_source_bindings_rechecked': 69,
    'original_ZIP_members_CRC_and_extracted_bytes_verified': 60,
    'source_ready_seal_sha256': '5a4e063a16235f413ed17859c7944a997a33ea761424f1ab0d97e1c431891c04',
    'prior_packets_unchanged': 4, 'foreign_full_text_cache_excluded': True,
    'public_promotion_authority': False, 'files': files,
})
(D / 'FINAL_MANIFEST.json').chmod(0o444)
seal = {
    'utc': utc, 'status': 'COMPLETE_SEALED_NO_PROMOTION_AUTHORITY',
    'manifest': 'FINAL_MANIFEST.json', 'manifest_sha256': digest(D / 'FINAL_MANIFEST.json'),
    'report_sha256': digest(D / 'REPORT.md'), 'verdict_sha256': digest(D / 'verdict.json'),
    'derivations_sha256': digest(D / 'DERIVATIONS.md'),
    'early_seal_sha256': digest(D / 'EARLY_SEAL.json'),
    'all_original_primary_and_prior_packet_bytes_unchanged': True,
    'bounded_completion_percent': 100, 'overall203_paper_goal': 'ONGOING',
}
write_new('FINAL_SEAL.json', seal)
(D / 'FINAL_SEAL.json').chmod(0o444)
print(json.dumps(dict(seal, final_seal_sha256=digest(D / 'FINAL_SEAL.json'), owned_files=len(files))))
