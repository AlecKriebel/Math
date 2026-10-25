"""Post-review byte custody and comparison of independently obtained numbers."""
from pathlib import Path
import datetime
import hashlib
import json
import zipfile

R = Path(__file__).resolve().parent
P = R.parents[1]
S = P / 'sources'
ROOT = S / 'published-source/deep-derived-pure-braids-source-verification-v1.0'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def require(value, reason):
    if not value:
        raise RuntimeError(reason)

expected = {
    'deep-derived-pure-braids-v1.0.pdf':
        '6547831e57c6eb01e7f4632ff67230f1e93d4ca6fec353e128b9c97a1f2c8b89',
    'deep-derived-pure-braids-source-verification-v1.0.zip':
        'a123728e0e8e8c6160738d6703bb757fe285a04c29872d2441d168c33bb2f106',
    'record.json':
        'd050764d8262d87e06c92a2cf3cadc90543828368d83e14460c91a341cf517a0',
}
for name, digest in expected.items():
    require(sha(S / name) == digest, 'Pinned source changed: ' + name)

with zipfile.ZipFile(S / 'deep-derived-pure-braids-source-verification-v1.0.zip') as z:
    members = [n for n in z.namelist() if not n.endswith('/')]
    require(len(members) == len(set(members)) == 213, 'ZIP count or duplicate member')
    for n in members:
        require(not Path(n).is_absolute() and '..' not in Path(n).parts, 'Unsafe ZIP path')
        require((ROOT / n).is_file(), 'Missing extracted member: ' + n)
        require((ROOT / n).read_bytes() == z.read(n), 'Extracted member changed: ' + n)
    require({str(f.relative_to(ROOT)) for f in ROOT.rglob('*') if f.is_file()} == set(members),
            'Extracted inventory mismatch')
require((ROOT / 'note.pdf').read_bytes() == (S / 'deep-derived-pure-braids-v1.0.pdf').read_bytes(),
        'Embedded reader mismatch')

before = json.loads((R / 'source-custody-before.json').read_text())['source_files']
after = {str(f.relative_to(S)): sha(f) for f in sorted(S.rglob('*')) if f.is_file()}
require(before == after, 'Source inventory changed during review')

fresh = json.loads((R / 'fresh_braid_results.json').read_text())['explicit_example']
meyer = json.loads((ROOT / 'reviews/meyer_algebra_family/INDEPENDENT_RESULTS.json').read_text())
goeritz = json.loads((ROOT / 'reviews/goeritz_family/INDEPENDENT_RESULTS.json').read_text())
replay = json.loads((R / 'published-replay.json').read_text())
require(replay['status'] == 'PASS', 'Current isolated replay did not pass')
require(fresh['word'] == meyer['free_reduced_word'] == goeritz['reduced_word'], 'Literal word mismatch')
require(fresh['meyer_terms'] == [t['meyer'] for t in meyer['meyer_terms']], 'A Meyer term disagrees')
require(fresh['matrix'] == [x for row in meyer['final_Burau_matrix'] for x in row], 'Final matrix mismatch')
require(fresh['signature'] == meyer['signature'] == goeritz['link_signature'] == -2, 'Signature mismatch')
require(goeritz['inertia'] == [23, 25, 0] and goeritz['mu'] == 0, 'Goeritz certificate mismatch')
require(int(goeritz['determinant']) == -7154819319988224, 'Determinant mismatch')

receipts = json.loads((P / 'reviews/scope/primary-source-receipts.json').read_text())
primaries = []
for rec in receipts:
    if rec.get('status') != 'acquired':
        continue
    f = P / 'reviews/scope/cache/primary-sources' / rec['name']
    require(sha(f) == rec['sha256'], 'Primary PDF differs from receipt: ' + rec['name'])
    primaries.append({k: rec.get(k) for k in ['name', 'url', 'version', 'retrieved_utc', 'sha256', 'bytes']})

result = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'PASS',
    'public_pins': expected,
    'all_source_files_unchanged': len(after),
    'zip_members_equal_to_original_bytes': len(members),
    'embedded_main_pdf_equals_top_level': True,
    'fresh_vs_replayed_word_and_all_104_meyer_terms_match': True,
    'fresh_vs_replayed_final_matrix_matches': True,
    'fresh_signature': -2,
    'replayed_goeritz_inertia': [23, 25, 0],
    'replayed_goeritz_determinant': -7154819319988224,
    'primary_receipts_checked': primaries,
    'after_source_files': after,
    'limits': 'Hashing archived opinion files is opaque byte custody, not adoption or reading of those opinions. Numerical equality is only finite evidence; the universal argument is separately reconstructed.'
}
(R / 'custody-and-comparison.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ['status', 'all_source_files_unchanged', 'zip_members_equal_to_original_bytes', 'fresh_vs_replayed_word_and_all_104_meyer_terms_match']}))
