"""Update this merged PR's artifact description with its verified public DOI."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess

D = Path(__file__).resolve().parent
A = D.parent
R = A.parents[2]
load = lambda p: json.loads(p.read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.now(timezone.utc).isoformat()
state = load(A / 'CURRENT_PUBLICATION_STATUS.json')
public = load(D / 'PUBLIC_RECORD_VERIFICATION.json')
merged = load(A / 'ACTUAL_MERGE_VERIFICATION.json')
assert state['all_public_metadata_and_download_bytes_verified']
assert public['doi'] == state['doi'] and public['record_id'] == state['zenodo_record']
assert public['status'] == 'PASS_PUBLIC_RECORD_EXACT_METADATA_AND_ALL_FILE_BYTES'
assert state['actual_merge'] == merged['actual_merge']
C = D / 'private_pr_body_publication_001'
assert not C.exists(), 'Inspect any earlier body-edit outcome before another mutation'
C.mkdir()
captures = []
def run(args, label):
    start = utc()
    r = subprocess.run(args, cwd=R, capture_output=True)
    rec = {'argv': args, 'cwd': str(R), 'started_utc': start, 'completed_utc': utc(), 'exit_code': r.returncode}
    for name, b in [('stdout', r.stdout), ('stderr', r.stderr)]:
        (C / (label + '.' + name)).write_bytes(b)
        rec[name + '_bytes'] = len(b)
        rec[name + '_sha256'] = sha(b)
    (C / (label + '.json')).write_text(json.dumps(rec, indent=2) + '\n')
    captures.append(rec)
    assert r.returncode == 0, (label, r.returncode, r.stderr.decode(errors='replace'))
    return r.stdout
args = ['gh', 'pr', 'view', '359', '--json', 'state,headRefOid,mergeCommit,body,url']
before = json.loads(run(args, 'before'))
assert before['state'] == 'MERGED' and before['headRefOid'] == merged['reviewed_head']
assert before['mergeCommit']['oid'] == state['actual_merge']
old = (A / 'accepted_pr_body.txt').read_text()
assert before['body'] == old, 'Another actor changed the description; preserve it for reconciliation'
last = old.split('\n\n')[-1]
assert last.startswith('The cleared PDF, source, verification archive and exact Zenodo metadata')
tracker = ('The tracker row was appended once and independently read back at `' + state['tracker_updated_range'] + '`.') if state['tracker_exact_readback'] else 'The DOI tracker row remains pending reconnection of the existing Google Workspace CLI login; the initial read-only metadata request failed and no tracker write was attempted.'
new = old[:-len(last)] + ('Published version 1.0: [DOI ' + state['doi'] + '](' + state['doi_url']
      + '), [Zenodo record](' + state['record_url'] + '). The complete public PDF and verification archive and all ten supplied metadata fields match the cleared submission; no metadata normalization occurred. The DOI resolves with HTTP 200. '
      + tracker + ' The canonical PDF, source, archive and metadata are under problems/30001370_basin_boundaries/preprint/. No journal submission or GitHub release was made.\n')
body = A / 'published_pr_body.txt'
assert not body.exists()
body.write_text(new)
run(['gh', 'pr', 'edit', '359', '--body-file', str(body)], 'edit')
after = json.loads(run(args, 'after'))
assert after['state'] == 'MERGED' and after['headRefOid'] == merged['reviewed_head']
assert after['mergeCommit']['oid'] == state['actual_merge'] and after['body'] == new
rec = {'utc': utc(), 'status': 'PASS_MERGED_PR_BODY_PUBLICATION_EXACT_READBACK', 'pr': 359,
       'actual_merge': state['actual_merge'], 'doi': state['doi'], 'body_bytes': len(new.encode()),
       'body_sha256': sha(new.encode()), 'tracker_verified': state['tracker_exact_readback'],
       'native_captures': captures, 'automatic_retry': False}
(D / 'PUBLIC_PR_BODY_VERIFICATION.json').write_text(json.dumps(rec, indent=2) + '\n')
print(json.dumps({k: v for k, v in rec.items() if k != 'native_captures'}, indent=2))
