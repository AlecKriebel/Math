"""Scoped ordinary commits using the independent GraphQL quota.

Uses an atomic expectedHeadOid condition, explicit regular-file additions only,
and an independently computed complete resulting Git tree hash. No force,
deletion, local Git objects/index/ref/checkout writes, or branch creation.
"""
import base64
import datetime
import json
import subprocess
import urllib.parse
import urllib.request

from remote_scoped_commit import REPO, Remote as BaseRemote, need, oid, path_parts, tree_oid


def gql(query, variables=None, check=True):
    result = subprocess.run(['gh', 'api', 'graphql', '--input', '-'],
                            input=json.dumps({'query': query, 'variables': variables or {}}),
                            text=True, capture_output=True, cwd=REPO)
    try:
        response = json.loads(result.stdout)
    except ValueError:
        response = {'errors': [{'message': result.stderr}]}
    if result.returncode or response.get('errors'):
        if check:
            raise RuntimeError(json.dumps(response.get('errors')) + ' ' + result.stderr)
        return {'_error': response.get('errors'), '_stderr': result.stderr}
    return response['data']


def head_oid():
    return gql('query { repository(owner:"AlecKriebel",name:"Math") { ref(qualifiedName:"refs/heads/main") { target { oid } } } }')['repository']['ref']['target']['oid']


def get_pr(number):
    result = gql('query($n:Int!) { repository(owner:"AlecKriebel",name:"Math") { pullRequest(number:$n) { state isDraft merged headRefOid closedAt } } }', {'n': number})['repository']['pullRequest']
    return {'state': result['state'].lower(), 'draft': result['isDraft'], 'merged': result['merged'],
            'head': {'sha': result['headRefOid']}, 'closed_at': result['closedAt']}


class Remote(BaseRemote):
    def __init__(self, parent):
        self.parent = parent
        result = gql('query($o:GitObjectID!) { repository(owner:"AlecKriebel",name:"Math") { object(oid:$o) { ... on Commit { oid tree { oid } } } } }', {'o': parent})['repository']['object']
        need(result['oid'] == parent, 'Commit identity mismatch')
        self.root = result['tree']['oid']
        self.cache = {}

    def entries(self, sha):
        if sha is None:
            return {}
        if sha not in self.cache:
            result = gql('query($o:GitObjectID!) { repository(owner:"AlecKriebel",name:"Math") { object(oid:$o) { ... on Tree { oid entries { name mode type oid } } } } }', {'o': sha})['repository']['object']
            rows = {r['name']: {'mode': format(r['mode'], '06o'), 'type': r['type'].lower(), 'sha': r['oid']} for r in result['entries']}
            need(result['oid'] == sha and len(rows) == len(result['entries']), 'Tree identity or duplicate names')
            need(tree_oid(rows) == sha, 'Tree truncation or Merkle hash mismatch')
            self.cache[sha] = rows
        return dict(self.cache[sha])

    def read(self, path):
        row = self.entry(path)
        need(row is not None and row['type'] == 'blob' and row['mode'] == '100644', 'Expected regular native text')
        url = 'https://raw.githubusercontent.com/AlecKriebel/Math/' + self.parent + '/' + urllib.parse.quote(path, safe='/')
        with urllib.request.urlopen(url, timeout=45) as response:
            raw = response.read()
        need(oid('blob', raw) == row['sha'], 'Immutable raw blob hash mismatch')
        return raw.decode()


def commit_updates(remote, updates, message):
    need(subprocess.check_output(['git', 'branch', '--show-current'], cwd=REPO, text=True).strip() == 'main', 'Must stay on main')
    rows, additions = {}, []
    for path, value in updates.items():
        path_parts(path)
        raw = value.encode() if isinstance(value, str) else value
        row = {'mode': '100644', 'type': 'blob', 'sha': oid('blob', raw)}
        existing = remote.entry(path)
        need(existing is None or (existing['type'] == 'blob' and existing['mode'] == '100644'), 'Cannot replace nonregular file')
        if existing == row:
            continue
        rows[path] = row
        additions.append({'path': path, 'contents': base64.b64encode(raw).decode()})
    need(bool(rows), 'No changed paths')
    expected = remote.expected_tree(rows)
    request = {'branch': {'repositoryNameWithOwner': 'AlecKriebel/Math', 'branchName': 'main'},
               'expectedHeadOid': remote.parent, 'message': {'headline': message},
               'fileChanges': {'additions': additions}}
    need(len(json.dumps({'i': request}).encode()) < 44000000, 'Encoded GraphQL payload needs a smaller scoped batch before mutation')
    result = gql('mutation($i:CreateCommitOnBranchInput!) { createCommitOnBranch(input:$i) { commit { oid tree { oid } parents(first:2) { nodes { oid } } } } }', {'i': request}, check=False)
    if '_error' in result:
        current = head_oid()
        candidate = gql('query($o:GitObjectID!) { repository(owner:"AlecKriebel",name:"Math") { object(oid:$o) { ... on Commit { oid tree { oid } messageHeadline parents(first:2) { nodes { oid } } } } } }', {'o': current})['repository']['object']
        if candidate['tree']['oid'] == expected and candidate['messageHeadline'] == message and [p['oid'] for p in candidate['parents']['nodes']] == [remote.parent]:
            commit = candidate
        elif current != remote.parent and any('expected' in str(error).lower() or 'head' in str(error).lower() for error in result['_error']):
            return None
        else:
            raise RuntimeError('Commit mutation outcome unconfirmed; do not repeat blindly: ' + json.dumps(result))
    else:
        commit = result['createCommitOnBranch']['commit']
    need(commit['tree']['oid'] == expected, 'PUBLISHED tree differs from exact expected tree; stop and investigate')
    need([p['oid'] for p in commit['parents']['nodes']] == [remote.parent], 'Unexpected commit parents')
    receipt = {'status': 'pushed', 'commit': commit['oid'], 'parent': remote.parent,
               'pushed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'paths': list(rows), 'message': message,
               'backend': 'GitHub GraphQL createCommitOnBranch; atomic expectedHeadOid ordinary single-parent commit',
               'entire_resulting_tree_sha_computed_before_mutation_and_verified_after': True,
               'shared_checkout_index_objects_and_local_refs_untouched': True}
    print(json.dumps(receipt), flush=True)
    return receipt
