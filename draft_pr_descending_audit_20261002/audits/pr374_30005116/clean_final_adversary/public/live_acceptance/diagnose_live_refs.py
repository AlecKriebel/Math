#!/usr/bin/env python3
"""Read-only diagnosis of stale PR merge metadata; outputs stay in --own."""
import argparse
import datetime
import hashlib
import json
import pathlib
import subprocess

QUERY = '''query {
  repository(owner: "AlecKriebel", name: "Math") {
    defaultBranchRef { name target { oid ... on Commit { tree { oid } } } }
    pullRequest(number: 374) {
      number isDraft baseRefName baseRefOid headRefName headRefOid mergeable mergeStateStatus
      baseRef { target { oid ... on Commit { tree { oid } } } }
      headRef { target { oid ... on Commit { tree { oid } } } }
      mergeCommit { oid parents(first: 2) { nodes { oid } } tree { oid } }
      potentialMergeCommit { oid parents(first: 2) { nodes { oid } } tree { oid } }
    }
  }
}'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--own', required=True)
    parser.add_argument('--git', required=True)
    args = parser.parse_args()
    own = pathlib.Path(args.own)
    private = own / 'private' / 'diagnosis'
    private.mkdir(parents=True, exist_ok=True)
    public = own / 'public'
    public.mkdir(parents=True, exist_ok=True)
    assert not (public / 'diagnosis_receipt.json').exists(), 'Use a new output directory'
    records = []
    def run(label, argv):
        r = subprocess.run(argv, cwd=args.git, capture_output=True)
        for name, data in [('stdout', r.stdout), ('stderr', r.stderr)]:
            (private / (label + '.' + name)).write_bytes(data)
        records.append({'label': label, 'exit': r.returncode,
                        'stdout_sha256': hashlib.sha256(r.stdout).hexdigest(), 'stdout_bytes': len(r.stdout),
                        'stderr_sha256': hashlib.sha256(r.stderr).hexdigest(), 'stderr_bytes': len(r.stderr)})
        return r
    rest = run('rest_pull', ['gh', 'api', 'repos/AlecKriebel/Math/pulls/374'])
    main_ref = run('main_ref', ['gh', 'api', 'repos/AlecKriebel/Math/git/ref/heads/main'])
    merge_ref = run('merge_ref_rest', ['gh', 'api', 'repos/AlecKriebel/Math/git/ref/pull/374/merge'])
    refs = run('git_remote_refs', ['git', 'ls-remote', 'https://github.com/AlecKriebel/Math.git',
                'refs/heads/main', 'refs/heads/math/30005116-induced-four-cycle-wip', 'refs/pull/374/merge'])
    graphql = run('graphql', ['gh', 'api', 'graphql', '-f', 'query=' + QUERY])
    (private / 'query.graphql').write_text(QUERY)
    assert rest.returncode == main_ref.returncode == refs.returncode == 0
    pr = json.loads(rest.stdout)
    actual_main = json.loads(main_ref.stdout)['object']['sha']
    test = run('test_merge_commit', ['gh', 'api', 'repos/AlecKriebel/Math/git/commits/' + pr['merge_commit_sha']])
    assert test.returncode == 0
    commit = json.loads(test.stdout)
    result = {'actual_remote_main': actual_main,
              'rest_base_sha': pr['base']['sha'], 'rest_head_sha': pr['head']['sha'],
              'draft': pr['draft'], 'body_sha256': hashlib.sha256(pr['body'].encode()).hexdigest(),
              'rest_test_merge_sha': commit['sha'], 'rest_test_merge_tree': commit['tree']['sha'],
              'rest_test_merge_parents': [p['sha'] for p in commit['parents']],
              'git_remote_refs': dict(line.split()[::-1] for line in refs.stdout.decode().splitlines()),
              'merge_ref_rest': json.loads(merge_ref.stdout) if merge_ref.returncode == 0 else {'exit': merge_ref.returncode},
              'graphql': json.loads(graphql.stdout) if graphql.returncode == 0 else {'exit': graphql.returncode}}
    receipt = {'observed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'result': result, 'command_records': records, 'read_only': True,
               'raw_streams_stay_private': True, 'query_sha256': hashlib.sha256(QUERY.encode()).hexdigest(),
               'permitted_reproduction_differences': ['observed_utc', 'explicitly changed live remote metadata']}
    (public / 'diagnosis_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__':
    main()
