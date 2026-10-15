"""Merge only an accepted, unchanged PR919; retain uncertain-action readback."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

P = Path(__file__).resolve().parent
ROOT = P.parent
A = P / 'audits/pr919_30002555'
HEAD = '704685791ec0053dc0a52590fdef49ed4aae61d9'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def run(args):
    return subprocess.run(args, cwd=ROOT, check=True, capture_output=True,
                          text=True).stdout


def save(name, value):
    (A / name).write_text(json.dumps(value, indent=2) + '\n')


def rawblob(ref, path):
    return subprocess.run(['git', 'show', ref + ':' + path], cwd=ROOT,
                          check=True, capture_output=True).stdout


def view():
    return json.loads(run(['gh', 'pr', 'view', '919', '--repo',
                          'AlecKriebel/Math', '--json',
                          'number,state,isDraft,headRefOid,headRefName,url,'
                          'mergeCommit,mergedAt,mergeable,mergeStateStatus']))


def main():
    decision = json.loads((A / 'PUBLICATION_DISPOSITION.json').read_text())
    require(decision['decision'] == 'PREPARE_EXPLICITLY_ATTRIBUTED_APPLICATION_NOTE', 'Publication disposition changed')
    accepted = json.loads((A / 'ACCEPTANCE.json').read_text())
    require(accepted.get('accepted') is True and
            accepted['original_pr_head'] == HEAD and
            len(accepted['full_package_reviews']) >= 2,
            'Exact-source acceptance after sequential fresh reviews required')
    pub = A / 'publication'
    freeze_bytes = (pub / 'PREPUBLICATION_FREEZE.json').read_bytes()
    require(hashlib.sha256(freeze_bytes).hexdigest() ==
            accepted['freeze_sha256'], 'Accepted freeze changed')
    freeze = json.loads(freeze_bytes)
    for name, record in freeze['files'].items():
        path = pub / name
        require(path.is_file() and not path.is_symlink(), 'Nonregular frozen file')
        data = path.read_bytes()
        require(len(data) == record['bytes'] and
                hashlib.sha256(data).hexdigest() == record['sha256'],
                'Accepted release changed: ' + name)
    expected_head = HEAD
    integration = A / 'ACCEPTANCE_INTEGRATION_ADDENDUM.json'
    if integration.exists():
        addendum = json.loads(integration.read_text())
        require(addendum.get('accepted') is True and
                addendum['original_audited_head'] == HEAD,
                'Integration review not accepted')
        expected_head = addendum['integrated_head']
    pr = view()
    require(pr['headRefOid'] == expected_head, 'Live PR head changed')
    snapshot = json.loads((A / 'ORIGINAL_SNAPSHOT.json').read_text())
    require(snapshot['head'] == HEAD and len(snapshot['files']) == 27,
            'Wrong original packet scope')
    if pr['state'] != 'MERGED':
        require(pr['state'] == 'OPEN', 'PR no longer open')
        paths = run(['gh', 'api', 'repos/AlecKriebel/Math/pulls/919/files',
                     '--paginate', '--jq', '.[].filename']).splitlines()
        require(set(paths) <= set(snapshot['files']) | {QUEUE},
                'Unexpected live PR change scope')
        run(['git', 'fetch', '--no-write-fetch-head', 'origin', expected_head])
        for name, pin in snapshot['files'].items():
            require(hashlib.sha256(rawblob(expected_head, name)).hexdigest() == pin,
                    'Pre-merge source differs from reviewed original: ' + name)
        parent = run(['git', 'ls-remote', 'origin', 'refs/heads/main']).split()[0]
        run(['git', 'fetch', '--no-write-fetch-head', 'origin', parent])
        source = json.loads((A / 'TARGET_IDENTITY_PREFLIGHT.json').read_text())
        catalogue = json.loads(rawblob(parent, 'unsolved_math_prioritization/catalog.json'))
        target = next(r for r in catalogue if str(r['id']) == '30002555')
        require(target.get('present') is True and target.get('holds') == [] and
                target['statement_hash'] == source['statement_hash'] and
                target['review_hash'] == source['review_hash'],
                'Current main target identity or review holds changed')
        queue = run(['gh', 'api',
                     'repos/AlecKriebel/Math/contents/' + QUEUE + '?ref=' + expected_head,
                     '-H', 'Accept: application/vnd.github.raw+json'])
        rows = [s for s in queue.splitlines() if '| 30002555 /' in s]
        require(len(rows) == 1 and rows[0].split('|')[8].strip() == 'claimed_solved'
                and rows[0].split('|')[9].strip() == '1/5',
                'Exact claimed_solved gate or original attempt count changed')
        # Unknown mergeability is not evidence of a conflict. A rejected merge
        # action is recorded and read back once; it is never blindly retried.
        intent = {'utc': datetime.now(timezone.utc).isoformat(),
                  'expected_head': expected_head, 'pre_action': pr,
                  'accepted_freeze_sha256': accepted['freeze_sha256']}
        save('PR_MERGE_INTENT.json', intent)
        if pr['isDraft']:
            run(['gh', 'pr', 'ready', '919', '--repo', 'AlecKriebel/Math'])
        action = subprocess.run(['gh', 'pr', 'merge', '919', '--repo',
                                 'AlecKriebel/Math', '--merge',
                                 '--match-head-commit', expected_head], cwd=ROOT,
                                capture_output=True, text=True)
        save('PR_MERGE_ACTION.json', {'utc': datetime.now(timezone.utc).isoformat(),
                                    'returncode': action.returncode,
                                    'stdout': action.stdout, 'stderr': action.stderr})
        pr = view()
        save('PR_MERGE_ACTION_READBACK.json', pr)
        require(pr['state'] == 'MERGED' and pr['headRefOid'] == expected_head,
                'Merge not confirmed; inspect recorded action and readback before proceeding')
    sha = pr['mergeCommit']['oid']
    run(['git', 'fetch', '--no-write-fetch-head', 'origin', sha])
    for name, pin in snapshot['files'].items():
        require(hashlib.sha256(rawblob(sha, name)).hexdigest() == pin,
                'Merged source differs from reviewed original: ' + name)
    parents = run(['git', 'show', '-s', '--format=%P', sha]).split()
    require(len(parents) == 2 and parents[1] == expected_head,
            'Expected ordinary two-parent merge')
    before = rawblob(parents[0], QUEUE).decode('utf-8')
    after = rawblob(sha, QUEUE).decode('utf-8')
    def without_target(text):
        lines = text.splitlines(keepends=True)
        matches = [i for i, row in enumerate(lines) if '| 30002555 /' in row]
        require(len(matches) == 1, 'Ambiguous merged target queue row')
        target = lines.pop(matches[0])
        return ''.join(lines), target
    old_rest, _ = without_target(before)
    new_rest, row = without_target(after)
    require(old_rest == new_rest, 'Merge changed a different queue row')
    require(row.split('|')[8].strip() == 'claimed_solved' and
            row.split('|')[9].strip() == '1/5', 'Merged target gate changed')
    save('PR_MERGE_RECEIPT.json', pr)
    save('MERGED_PACKET_INTEGRITY.json', {
        'utc': datetime.now(timezone.utc).isoformat(), 'merge_commit': sha,
        'original_head': HEAD, 'merged_head': expected_head,
        'all_27_original_files_byte_identical': True,
        'all_other_main_queue_bytes_preserved': True,
        'original_attempts': '1/5', 'shared_checkout_index_head_untouched': True})
    print(json.dumps({'state': pr['state'], 'merge_commit': sha,
                      'original_files_verified': 27}, indent=2))


if __name__ == '__main__':
    main()
