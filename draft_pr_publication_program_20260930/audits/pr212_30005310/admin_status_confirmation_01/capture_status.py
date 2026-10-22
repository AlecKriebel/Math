"""Three finite read-only GETs confirming PR212's corrected draft status.
No Git, PR write, publication, reference, lock or global-five action exists.
"""
import base64
import datetime
import hashlib
import json
import os
from pathlib import Path
import types

BASE = Path(__file__).resolve().parent
CASE = BASE.parent
PRIMITIVES = CASE / 'native_custody_01/get_primitives.py'
EXPECTED = '808149b347a61809e37a0b71fc4dc602ec17e63e38e985d99123827268286e09'
HEAD = '99af7a27a711271bcd0b9e7ce90e374e4100ea6d'
BLOB = '75dd3438de4cd64c023595f67b9331392278315f'


def pin(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def put(name, raw):
    assert '/' not in name and name not in ('.', '..')
    p = BASE / name
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o444)
    try:
        assert os.write(fd, raw) == len(raw)
        os.fsync(fd)
    finally:
        os.close(fd)
    return {'path': name, **pin(raw)}


def save(name, value):
    return put(name, (json.dumps(value, sort_keys=True, indent=2) + '\n').encode())


def main():
    raw = PRIMITIVES.read_bytes()
    assert len(raw) == 3794 and hashlib.sha256(raw).hexdigest() == EXPECTED
    g = types.ModuleType('pinned_GET_primitives')
    exec(compile(raw, str(PRIMITIVES), 'exec'), g.__dict__)
    for name, size, sha in [
        ('ROOT_NATIVE_CUSTODY_ACCEPTANCE_01.json', 6525, 'c240a9b71efee22f0699f42d1437d5731b5542024704c2ca7ceb129badbe3529'),
        ('ROOT_MATHEMATICAL_ACCEPTANCE_01.json', 7885, '790b6482fcc2ef5fe39ebb7fc12850213b67133de0221861ee6cb5eb122e4512'),
        ('ROOT_PRIORITY_ACCEPTANCE_01.json', 6441, '1ad1506d4a21c4d1b4cef16a3db059ad3609fab1a33e1834c7b813356b9a73d2'),
    ]:
        v = g.regular(CASE / name)
        assert pin(v) == {'bytes': size, 'sha256': sha}
        assert g.decode(v)['accepted'] is True
    records = []

    def get(route):
        assert route in ('pulls/212', 'git/blobs/' + BLOB)
        stem = str(len(records) + 1).zfill(2)
        argv = ['/opt/homebrew/Cellar/gh/2.85.0/bin/gh', 'api', '--hostname',
                'github.com', '--method', 'GET', 'repos/AlecKriebel/Math/' + route]
        intent = save(stem + '.intent.json', {'argv': argv, 'retries': 0})
        response = g.bounded_get(argv)
        out = put(stem + '.stdout.json', response.stdout)
        err = put(stem + '.stderr.txt', response.stderr)
        receipt = save(stem + '.receipt.json', {
            'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'intent': intent, 'stdout': out, 'stderr': err,
            'exit_code': response.returncode, 'method': 'GET', 'route': route})
        assert response.returncode == 0
        records.append({'route': route, 'intent': intent, 'response': out,
                        'stderr': err, 'receipt': receipt})
        return g.decode(response.stdout)

    def guard(pr):
        assert type(pr['number']) is int and pr['number'] == 212
        assert pr['state'] == 'open' and pr['draft'] is True and pr['merged'] is False
        assert pr['head']['sha'] == HEAD and pr['base']['ref'] == 'main'
        assert pr['head']['ref'] == 'math/30005310-colored-threshold-wip'
        assert pr['title'] == '30005310: Credited prior counterexamples to literal numerical scenarios'
        assert type(pr['commits']) is int and pr['commits'] == 3

    start = get('pulls/212')
    guard(start)
    value = get('git/blobs/' + BLOB)
    assert value['sha'] == BLOB and value['encoding'] == 'base64'
    assert type(value['size']) is int and value['size'] == 371408
    body = base64.b64decode(''.join(value['content'].split()), validate=True)
    assert g.native('blob', body) == BLOB
    assert pin(body) == {'bytes': 371408, 'sha256': '3370b842e51760df443f3d08f26951cb9915e9946f2f3e0a200c5d75d07a552e'}
    rows = []
    for line in body.splitlines(keepends=True):
        cells = line.decode().split('|')
        if len(cells) == 14 and cells[2].strip().split(' / ')[0] == '30005310':
            rows.append((line, cells))
    assert len(rows) == 1
    row, cells = rows[0]
    assert cells[8].strip() == 'already_solved' and cells[9].strip() == '1/5'
    assert pin(row) == {'bytes': 583, 'sha256': '888486f42b1d43c32114cd971d988579926215f4050adf5dbe8c7d51fe86b691'}
    finish = get('pulls/212')
    guard(finish)
    keys = ('number', 'title', 'state', 'draft', 'merged', 'commits', 'body',
            'created_at', 'updated_at', 'merged_at', 'merge_commit_sha')
    assert all(g.exact(start.get(k), finish.get(k)) for k in keys)
    save('FACTUAL_STATUS_CONFIRMATION.json', {
        'schema': 'pr212-fresh-corrected-draft-status-confirmation-v1',
        'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'PR': 212, 'HEAD': HEAD, 'state': 'open', 'draft': True, 'merged': False,
        'current_native_QUEUE_blob': BLOB, 'current_status': 'already_solved',
        'current_effort_cell': '1/5', 'QUEUE_row_pin': pin(row),
        'original_eligible_status_remains': 'claimed_solved',
        'actual_GETs': records, 'start_end_selected_metadata_identical': True,
        'native_path_association': 'Current HEAD equals the earlier accepted exact canonical commit/root; ROOT_NATIVE_CUSTODY_ACCEPTANCE_01.json binds this immutable QUEUE blob to its exact native path. Fresh PR observations bind that same HEAD; blob body is independently freshly fetched.',
        'Root_disposition_or_checkpoint_acceptance': False,
        'perpetual_PR_or_Main_lease': False, 'mutation_actions': 0})
    print(json.dumps({'status': 'PASS_FACTUAL_ONLY', 'GETs': len(records),
                      'current_status': cells[8].strip(), 'HEAD': HEAD}))


if __name__ == '__main__':
    main()
