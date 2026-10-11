"""Read-only integrity replay for source caches and derived provenance assertions."""
from pathlib import Path
import hashlib
import json
import gzip
import subprocess
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
rows = []
for manifest_name in ('source_download_manifest.json', 'archive_download_manifest.json', 'archive_text_manifest.json'):
    for source in json.loads((HERE / manifest_name).read_text()):
        cache = HERE / 'tmp' / source['id']
        digest = hashlib.sha256(cache.read_bytes()).hexdigest()
        rows.append({'id': source['id'], 'sha256': digest, 'matched': digest == source['sha256']})
source = json.loads((HERE / 'arxiv_source_manifest.json').read_text())
for name, expected in [('arxiv_source.bin', source['sha256']), ('arxiv_source.tex', source['tex_sha256'])]:
    digest = hashlib.sha256((HERE / 'tmp' / name).read_bytes()).hexdigest()
    rows.append({'id': name, 'sha256': digest, 'matched': digest == expected})
assert gzip.decompress((HERE / 'tmp' / 'arxiv_source.bin').read_bytes()) == (HERE / 'tmp' / 'arxiv_source.tex').read_bytes()
metadata = json.loads((HERE / 'bibliographic_metadata.json').read_text())
digest = hashlib.sha256((HERE / 'tmp' / 'crossref.json').read_bytes()).hexdigest()
rows.append({'id': 'crossref.json', 'sha256': digest, 'matched': digest == metadata['sha256']})
probe = HERE / 'current_corrections_probe'
for source in json.loads((probe / 'source_manifest.json').read_text())['sources']:
    digest = hashlib.sha256((probe / source['cache_path']).read_bytes()).hexdigest()
    rows.append({'id': source['source_id'], 'sha256': digest, 'matched': digest == source['sha256']})

initial = json.loads((HERE / 'tmp' / 'initial_commit.json').read_text())
extension = json.loads((HERE / 'tmp' / 'extension_commit.json').read_text())
initial_review = (HERE / 'tmp' / 'initial_review.md').read_bytes()
extension_review = (HERE / 'tmp' / 'extension_review.md').read_bytes()
blob_hash = hashlib.sha1(b'blob ' + str(len(initial_review)).encode() + b'\0' + initial_review).hexdigest()
tex = (HERE / 'tmp' / 'arxiv_source.tex').read_text()
claims = {
    'review_bytes_identical_at_both_pins': initial_review == extension_review,
    'review_git_blob_matches': blob_hash == '274c04c5f59fd5f56be95373191ae36d278b3618',
    'initial_author_date_matches': initial['commit']['author']['date'] == '2026-08-30T12:01:44Z',
    'initial_committer_date_matches': initial['commit']['committer']['date'] == '2026-08-30T12:01:44Z',
    'extension_author_date_matches': extension['commit']['author']['date'] == '2026-09-03T09:58:29Z',
    'extension_committer_date_matches': extension['commit']['committer']['date'] == '2026-09-03T09:58:29Z',
    'both_metadata_verifications_unsigned': all(c['commit']['verification']['reason'] == 'unsigned' and not c['commit']['verification']['verified'] for c in [initial, extension]),
    'whole_word_inverse_in_tex': r'\bar \sigma_{i_1 \dots i_k}$ for $\sigma_{i_1 \dots i_k}^{-1}' in tex,
    'RBn_terminal_sigma_n_in_tex': r'Then $Z_n$ is the algebra $RB_n$' in tex and r'\bar \sigma_{n \dots 1}' in tex and r'\sigma_{1 \dots n}) X_n' in tex,
    'source_sum_unit_from_now_on': r'now on that $q_1 + q_2$ is a unit of $R$' in tex,
}
receipt = {'checked_utc': datetime.now(timezone.utc).isoformat(), 'files': rows, 'assertions': claims, 'all_passed': all(r['matched'] for r in rows) and all(claims.values()), 'boundary': 'Integrity and exact provenance assertions only; not a mathematical theorem, external timestamp, or exhaustive search certificate.'}
(HERE / 'retrieval_integrity.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'files_checked': len(rows), 'assertions_checked': len(claims), 'all_passed': receipt['all_passed']}, indent=2))
if not receipt['all_passed']:
    raise SystemExit(1)
