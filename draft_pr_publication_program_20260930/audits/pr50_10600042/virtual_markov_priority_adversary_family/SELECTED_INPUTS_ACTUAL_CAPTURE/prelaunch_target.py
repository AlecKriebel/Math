"""Read-only checks of eight exact selected inputs; no foreign code execution."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat
F = Path(__file__).resolve().parent
A = F.parent
HEAD = '7260315f8b8b193020c09d4ef6df9d943a3a13ff'
NAMES = ('CANDIDATE.md', 'SOURCES.md', 'source_record.json', 'source_manifest.json',
         'verify_even_moves.py', 'status.json', 'readiness.json', 'turns.jsonl')
def digest(b): return hashlib.sha256(b).hexdigest()
def main():
    path = A / 'ORIGINAL_MANIFEST.json'
    body = path.read_bytes()
    manifest = json.loads(body)
    assert manifest['schema'] == 'pr50-selected-original-git-snapshot/v1'
    assert manifest['head'] == HEAD and manifest['pr'] == 50
    rows = {r['path']: r for r in manifest['files']}
    assert len(rows) == manifest['files_count'] == 15
    checked = []
    for name in NAMES:
        p = A / 'original' / name
        s = p.lstat()
        assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
        b = p.read_bytes(); r = rows[name]
        blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
        assert len(b) == r['bytes'] and digest(b) == r['sha256']
        assert blob == r['git_blob_sha1'] and r['git_mode'] == '100644'
        assert stat.S_IMODE(s.st_mode) == r['snapshot_full_mode'] == 0o444
        checked.append(dict(path=str(p), bytes=len(b), sha256=digest(b),
                            git_blob_sha1=blob, full_mode=stat.S_IMODE(s.st_mode),
                            content_read=True, original_code_executed=False))
    problem = json.loads((A/'original/source_record.json').read_bytes())['problem']
    assert problem['id'] == 10600042
    status = json.loads((A/'original/status.json').read_bytes())
    turns = [json.loads(x) for x in (A/'original/turns.jsonl').read_text().splitlines() if x]
    assert type(status['turns_used']) is int and status['turns_used'] == 1
    assert len(turns) == 1 and turns[0]['turn'] == 1
    result = dict(schema='pr50-virtual-markov-selected-input-bindings/v1',
                  created_utc=dt.datetime.now(dt.timezone.utc).isoformat(), actual_pid=os.getpid(),
                  pr=50, head=HEAD, problem_id=10600042, selected_count=len(checked), files=checked,
                  source_manifest_metadata=dict(path=str(path), bytes=len(body), sha256=digest(body),
                                               full_mode=stat.S_IMODE(path.lstat().st_mode)),
                  origin='Selected Git snapshot supplied by ROOT; blob bodies independently hashed here.',
                  fresh_Git_API_tree_or_head_reverification=False,
                  historical_turns_used=1, independent_audit_discovery_turns_charged=0,
                  foreign_review_conclusions_accepted=False, original_helper_executed=False)
    with (F/'SELECTED_INPUT_BINDINGS.json').open('xb') as h:
        h.write((json.dumps(result, indent=2, sort_keys=True) + '\n').encode())
    print(json.dumps(result, sort_keys=True))
if __name__ == '__main__': main()
