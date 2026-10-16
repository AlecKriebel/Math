#!/usr/bin/env python3
"""Independent raw Merkle/tree/commit audit. Reads provider-independent private
objects through Git cat-file only; never imports or executes the Root producer.
All authored output stays in this review directory. No provider/ref/index writes.
"""
import argparse
import base64
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

sys.dont_write_bytecode = True
R = Path('/Users/alec/Documents/Math')
W = R / 'draft_pr_descending_audit_20261002/audits/pr263_30000170/initial_review_20261011'
OWN = W / 'native_integration_adversarial_review'
ROOT = W / 'integration_preparation'
B = R / 'draft_pr_descending_audit_20261002/audits/pr278_30005468/resume_20261011'
TARGET = 'attempts/30000170'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
AUTHOR = 'c4eff3253932a504f8e558c8b5f5b1b5e155de0f'
HELPER_SHA = '7833158162faf6d68dc7d293ee42926fa357a6116004ab87636c6417ba0ece20'
BINARIES = {
    'preprint/output/pdf/nonunique_nearest_stable_complex_quadratics.pdf': (76336, '6439bda84f32d9a5ac1680e184975df159f51f8c7e44e609fa873dfa8ae78e1f'),
    'preprint/output/nonunique_nearest_stable_complex_quadratics_verification.zip': (37068, '2fc6b62d67ab6681c36f7d3806db549073a3f0b2e0d039817f997fab9eb96dee')}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def load(path):
    def pairs(items):
        out = {}
        for k, v in items:
            require(k not in out, 'Duplicate JSON key: ' + k)
            out[k] = v
        return out
    return json.loads(path.read_bytes(), object_pairs_hook=pairs)

def oid(kind, body):
    return hashlib.sha1(kind.encode() + b' ' + str(len(body)).encode() + b'\0' + body).hexdigest()

def pin(path):
    body = path.read_bytes()
    return dict(path=str(path), bytes=len(body), sha256=hashlib.sha256(body).hexdigest())

def encode_tree(entries):
    names = sorted(entries, key=lambda n:n + (b'/' if entries[n][0] == b'40000' else b''))
    return b''.join(entries[n][0] + b' ' + n + b'\0' + bytes.fromhex(entries[n][1]) for n in names)

def census(leaves):
    h = hashlib.sha256()
    for path, (mode, sha) in sorted(leaves.items()):
        h.update(mode + b' ' + sha.encode() + b'\t' + path + b'\0')
    return h.hexdigest()

class Reader:
    def __init__(self):
        driver, objects = ROOT / 'driver.git', ROOT / 'private_objects'
        alternatives = [B / 'checkpoint_resume/private_objects', B / 'reconciliation/private_objects', B / 'objects.git/objects']
        for path in [driver, objects, *alternatives]:
            require(path.is_dir() and path.resolve() == path and not path.is_symlink(), 'Unsafe/missing private read store')
        env = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
        env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1', GIT_TERMINAL_PROMPT='0', GIT_NO_LAZY_FETCH='1',
                   GIT_OBJECT_DIRECTORY=str(objects), GIT_ALTERNATE_OBJECT_DIRECTORIES=os.pathsep.join(map(str, alternatives)))
        base = ['git', '--no-replace-objects', '--git-dir', str(driver)]
        config = subprocess.run(base + ['config', '--local', '--get-regexp', '^remote\\.'], env=env, capture_output=True, timeout=10)
        require(config.returncode == 1 and config.stdout == b'', 'Private reader remote configuration present')
        self.p = subprocess.Popen(base + ['cat-file', '--batch'], env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.cache = {}
        self.calls = 0

    def get(self, sha):
        require(re.fullmatch('[0-9a-f]{40}', sha), 'Nonliteral object request')
        if sha not in self.cache:
            self.p.stdin.write(sha.encode() + b'\n')
            self.p.stdin.flush()
            head = self.p.stdout.readline().split()
            require(len(head) == 3 and head[0] == sha.encode(), 'Missing/misframed object: ' + sha)
            kind, size = head[1].decode(), int(head[2])
            body = self.p.stdout.read(size)
            require(len(body) == size and self.p.stdout.read(1) == b'\n', 'Short/misframed raw body')
            require(oid(kind, body) == sha, 'Raw object hash mismatch')
            self.cache[sha] = (kind, body)
            self.calls += 1
        return self.cache[sha]

    def tree(self, sha):
        kind, body = self.get(sha)
        require(kind == 'tree', 'Expected raw tree')
        out, at = {}, 0
        while at < len(body):
            space, zero = body.index(b' ', at), body.index(b'\0', at)
            mode, name = body[at:space], body[space + 1:zero]
            require(mode in (b'40000', b'100644', b'100755', b'120000', b'160000'), 'Unknown raw mode')
            require(name and b'/' not in name and name not in (b'.', b'..') and name not in out, 'Unsafe/duplicate raw tree name')
            require(zero + 21 <= len(body), 'Truncated tree entry')
            out[name] = (mode, body[zero + 1:zero + 21].hex())
            at = zero + 21
        require(at == len(body) and encode_tree(out) == body, 'Noncanonical raw tree encoding/order')
        return out

    def walk(self, root, prefix=b''):
        out = {}
        for name, entry in self.tree(root).items():
            path = prefix + name
            out[path] = entry
            if entry[0] == b'40000':
                out.update(self.walk(entry[1], path + b'/'))
        return out

    def close(self):
        self.p.stdin.close()
        require(self.p.wait(timeout=10) == 0, 'Private raw reader failed')

def queue_row(body):
    lines = body.splitlines(keepends=True)
    hit = [i for i,line in enumerate(lines) if len(line.split(b'|')) > 3 and line.split(b'|')[2].strip() == b'30000170 / OWR-783-002']
    require(len(hit) == 1, 'QUEUE census is not exactly one row')
    return lines, hit[0]

def run():
    p = argparse.ArgumentParser()
    p.add_argument('--preparation', required=True)
    p.add_argument('--selection', required=True)
    p.add_argument('--main', required=True)
    p.add_argument('--main-tree', required=True)
    p.add_argument('--commit', required=True)
    p.add_argument('--tree', required=True)
    a = p.parse_args()
    prepdir, selection_path = Path(a.preparation), Path(a.selection)
    require(prepdir.parent == ROOT and selection_path.parent == ROOT and prepdir.resolve() == prepdir, 'Unexpected Root artifact paths')
    for literal in [a.main, a.main_tree, a.commit, a.tree]:
        require(re.fullmatch('[0-9a-f]{40}', literal), 'Expected explicit literal object identity')
    helper = ROOT / 'prepare_native_reconciliation.py'
    require(pin(helper)['sha256'] == HELPER_SHA, 'Preparation helper drift')
    prep = load(prepdir / 'PREPARATION.json')
    require(pin(selection_path)['sha256'] == '6bd7c2fb78f846536695469fc9a26b0b5bd2133581936947cac32de78f5daadc' and pin(selection_path)['bytes'] == 58888, 'Literal Root-selected control drift')
    s = load(selection_path)
    require(prep['schema'] == 'pr263-private-native-reconciliation-v1', 'Unexpected preparation schema')
    require(prep['root_selection'] == pin(selection_path), 'Prepared selection binding differs')
    require(prep['main'] == a.main == s['main'] and prep['main_tree'] == a.main_tree and prep['tree'] == a.tree and prep['commit'] == a.commit, 'Literal Root-delivered output differs')
    require(prep['original_author'] == s['author'] == AUTHOR and prep['ordered_parents'] == [AUTHOR, a.main], 'Ordered parents differ')
    require(prep['provider_mutations'] == 0 and prep['primary_local_Git_mutations'] == 0 and prep['prepared_only_not_execution_authority'] is True, 'Scope declaration differs')
    reused_helper = B / 'checkpoint_resume/prepare_checkpoint.py'
    require(pin(reused_helper)['sha256'] == 'e5399e719a2a93a0e7d34670ff503a897a18cb2c8632a766248d21d50b3dd298' and prep['checked_private_helper'] == pin(reused_helper), 'Reused checked helper drift')
    accepted_path = Path(s['candidate_acceptance']['path'])
    require(pin(accepted_path)['sha256'] == 'a74c8baa80afbf89a83e74fa91b262d1f19844f50d0514d16e15533392493006' and pin(accepted_path)['bytes'] == 26545, 'Literal Root acceptance drift')
    require(pin(accepted_path) == s['candidate_acceptance'] == prep['candidate_acceptance'], 'Candidate acceptance pin differs')
    accepted = load(accepted_path)
    candidate = W / 'publication_candidate/attempts/30000170'
    require(accepted['schema'] == 'pr263-root-final-publication-candidate-acceptance-v1' and accepted['accepted_for_native_preparation'] is True and accepted['candidate_root'] == str(candidate), 'Root acceptance schema/scope differs')
    require(pin(candidate / 'CANDIDATE_MANIFEST.json') == accepted['candidate_manifest'], 'Candidate manifest pin differs')
    bodies, selected = {}, {}
    for e in s['files']:
        require(set(e) == {'path', 'source', 'bytes', 'sha256'}, 'Unexpected selected record fields')
        path = e['path']
        require(path not in bodies and PurePosixPath(path).as_posix() == path and not path.startswith('/') and '..' not in PurePosixPath(path).parts, 'Duplicate/noncanonical selected path')
        require(path == QUEUE or path.startswith(TARGET + '/'), 'Foreign selected destination')
        f = Path(e['source'])
        require(f.resolve() == f and f.is_file() and not f.is_symlink() and f.is_relative_to(W), 'Unsafe selected source')
        if path != QUEUE:
            require(f == candidate / path[len(TARGET) + 1:], 'Wrong selected source/destination mapping')
        body = f.read_bytes()
        require(len(body) == e['bytes'] and hashlib.sha256(body).hexdigest() == e['sha256'], 'Full selected body differs')
        rel = path[len(TARGET) + 1:]
        if rel in BINARIES:
            require((len(body), e['sha256']) == BINARIES[rel], 'Published binary pin differs')
        else:
            require(b'\0' not in body, 'Binary selected as text')
            body.decode('utf8')
        bodies[path], selected[path.encode()] = body, (b'100644', oid('blob', body))
    target_list = [dict(path=path[len(TARGET) + 1:], bytes=len(body), sha256=hashlib.sha256(body).hexdigest()) for path,body in sorted(bodies.items()) if path != QUEUE]
    require(target_list == accepted['target_bodies'], 'Complete Root acceptance body census differs')
    require({e['path'] for e in target_list} == {str(f.relative_to(candidate)) for f in candidate.rglob('*') if f.is_file()}, 'Candidate inventory differs')
    require(len(bodies) == prep['selected_count'] and len(target_list) == prep['target_count'], 'Selection count differs')
    expected_manifest = [dict(path=path, mode='100644', git_blob=oid('blob', body), bytes=len(body), sha256=hashlib.sha256(body).hexdigest(), source=next(e['source'] for e in s['files'] if e['path'] == path)) for path,body in sorted(bodies.items())]
    require(expected_manifest == prep['selected_full_body_manifest'], 'Prepared full-body manifest differs')
    original_path, original_binding = W / 'original_submission/MANIFEST_WITH_MODES.json', W / 'original_submission/BINDING.json'
    require(pin(original_path) == s['original_manifest'] and pin(original_binding) == s['original_binding'], 'Original controls drift')
    originals = [e for e in load(original_path) if e['path'].startswith(TARGET + '/')]
    require(len(originals) == 17 and all(e['mode'] == '100644' and e['path'] in bodies for e in originals), 'Original17 retention/mode differs')
    historical = [e for e in originals if e['path'].split(TARGET + '/', 1)[1] in ('REVIEW_REQUEST.md', 'checks/verify.py', 'checks/CHECKS.json') or e['path'].startswith(TARGET + '/independent_review/')]
    require(len(historical) == 9 and all(oid('blob', bodies[e['path']]) == e['git_blob'] and hashlib.sha256(bodies[e['path']]).hexdigest() == e['sha256'] for e in historical), 'Historical9 bodies differ')
    for e in originals:
        historical_copy = bodies[TARGET + '/historical/original_submission/files/' + e['path']]
        require(oid('blob', historical_copy) == e['git_blob'] and hashlib.sha256(historical_copy).hexdigest() == e['sha256'], 'Portable original17 historical copy differs')
    c = W / 'scoped_candidate/attempts/30000170'
    cfiles = [f for f in c.rglob('*') if f.is_file()]
    require(len(cfiles) == 24, 'Historical delivered C census differs')
    for f in cfiles:
        require(bodies[TARGET + '/historical/source_candidate_v03/' + str(f.relative_to(c))] == f.read_bytes(), 'Historical C body differs')
    km_path = W / 'preprint_package_v03/PACKAGE_MANIFEST.json'
    require(bodies[TARGET + '/preprint/PACKAGE_MANIFEST.json'] == km_path.read_bytes(), 'Frozen package manifest differs')
    km = load(km_path)
    require(len(km['files']) == 21, 'K03 payload count differs')
    for e in km['files']:
        body = bodies[TARGET + '/preprint/' + e['path']]
        require(body == (km_path.parent / e['path']).read_bytes() and len(body) == e['bytes'] and hashlib.sha256(body).hexdigest() == e['sha256'], 'Frozen K03 body differs')
    review_counts = {}
    for number, key in [('01', 'files'), ('02', 'selected_authored_outputs')]:
        orig = W / ('whole_preprint_review_' + number)
        manifest_body = bodies[TARGET + '/whole_preprint_reviews/review' + number + '/REVIEW_MANIFEST.json']
        require(manifest_body == (orig / 'REVIEW_MANIFEST.json').read_bytes(), 'Copied review manifest differs')
        records = load(orig / 'REVIEW_MANIFEST.json')[key]
        review_counts[number] = len(records)
        for e in records:
            body = bodies[TARGET + '/whole_preprint_reviews/review' + number + '/' + e['path']]
            require(body == (orig / e['path']).read_bytes() and len(body) == e['bytes'] and hashlib.sha256(body).hexdigest() == e['sha256'], 'Authored review output differs')
    require(review_counts == {'01':14, '02':19}, 'Whole review authored-output census differs')
    public_receipt_path = W / 'publication_execution_20261011/ROOT_ACTUAL_PUBLICATION_ACCEPTANCE.json'
    public_receipt = load(public_receipt_path)
    require(public_receipt['DOI'] == '10.5281/zenodo.23306332' and public_receipt['submitted_and_published_verified'], 'Actual publication receipt differs')
    require(bodies[TARGET + '/publication_provenance/ROOT_ACTUAL_PUBLICATION_ACCEPTANCE.json'] == public_receipt_path.read_bytes(), 'Copied actual-publication receipt differs')
    public_download_pins = []
    for e in public_receipt['public_files']:
        local = public_receipt_path.parent / 'public_downloads' / e['name']
        local_body = local.read_bytes()
        require(e['HTTP_status'] == 200 and e['frozen_local_byte_exact'] is True and len(local_body) == e['bytes'] and hashlib.sha256(local_body).hexdigest() == e['sha256'], 'Public download receipt/local full bytes differ')
        require(local_body == bodies[TARGET + '/preprint/output/' + ('pdf/' if e['name'].endswith('.pdf') else '') + e['name']], 'Public/downloaded/selected binary differs')
        public_download_pins.append(pin(local))
    tree_payload, commit_payload, cas, binary = [load(prepdir / name) for name in ['TREE_PAYLOAD.json','COMMIT_PAYLOAD.json','AUTHOR_CAS_PAYLOAD.json','BINARY_BLOB_PAYLOADS.json']]
    expected_tree_payload = dict(base_tree=a.main_tree, tree=[dict(path=path,mode='100644',type='blob',**({'sha':oid('blob',body)} if path[len(TARGET) + 1:] in BINARIES else {'content':body.decode('utf8')})) for path,body in sorted(bodies.items())])
    require(tree_payload == expected_tree_payload, 'Native tree payload differs from full bodies')
    expected_binary = [dict(path=path, expected_sha=oid('blob',body), payload=dict(content=base64.b64encode(body).decode(),encoding='base64')) for path,body in sorted(bodies.items()) if path[len(TARGET)+1:] in BINARIES]
    require(sorted(binary,key=lambda e:e['path']) == expected_binary, 'Native binary payload differs')
    message = 'PR263: publish audited complex-quadratic nearest-stability note\n'
    require(commit_payload['tree'] == a.tree and commit_payload['parents'] == [AUTHOR,a.main] and commit_payload['message'] == message and set(commit_payload) == {'tree','parents','message','author','committer'}, 'Commit payload identity differs')
    actor = commit_payload['author']
    require(actor == commit_payload['committer'] and set(actor) == {'name','email','date'} and actor['name'] == 'Alec Kriebel' and actor['email'] == 'me@aleckriebel.com', 'Commit identity metadata differs')
    require(re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', actor['date']), 'Commit timestamp must be literal UTC seconds')
    stamp = dt.datetime.strptime(actor['date'],'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=dt.timezone.utc)
    person = 'Alec Kriebel <me@aleckriebel.com> ' + str(int(stamp.timestamp())) + ' +0000'
    raw_commit = ('tree '+a.tree+'\nparent '+AUTHOR+'\nparent '+a.main+'\nauthor '+person+'\ncommitter '+person+'\n\n'+message).encode()
    require(oid('commit',raw_commit) == a.commit, 'Independent commit bytes/hash differ')
    expected_cas = dict(query='mutation PR263ScopedAuthorCAS($input:UpdateRefsInput!){updateRefs(input:$input){clientMutationId}}', variables=dict(input=dict(repositoryId='R_kgDOTfIvPw',refUpdates=[dict(name='refs/heads/dot/math-30000170',beforeOid=AUTHOR,afterOid=a.commit,force=False)],clientMutationId='pr263-'+a.commit)))
    require(cas == expected_cas, 'Author expected-old/nonforce CAS differs')
    raw = Reader()
    require(raw.get(a.main)[0] == 'commit' and raw.get(a.main)[1].split(b'\n',1)[0] == b'tree '+a.main_tree.encode(), 'Raw MAIN commit/tree binding differs')
    require(raw.get(a.commit) == ('commit',raw_commit), 'Stored prepared commit bytes differ')
    author_kind, author_body = raw.get(AUTHOR)
    require(author_kind == 'commit' and author_body.split(b'\n',1)[0] == b'tree 1603b2bbd482f196b97e8237ecfa206282f44914', 'Original author raw commit/tree differs')
    captured_author_path = W / 'original_submission/COMMIT.json'
    captured_author = load(captured_author_path)
    original_header = 'tree ' + captured_author['tree']['sha'] + '\n' + ''.join('parent '+e['sha']+'\n' for e in captured_author['parents'])
    for role in ['author','committer']:
        e = captured_author[role]
        date = dt.datetime.fromisoformat(e['date'].replace('Z','+00:00'))
        original_header += role+' '+e['name']+' <'+e['email']+'> '+str(int(date.timestamp()))+' -0700\n'
    original_raw = (original_header + '\n' + captured_author['message']).encode()
    require(oid('commit',original_raw) == AUTHOR and author_body == original_raw, 'Raw original commit/captured fields bytes differ')
    before, after = raw.walk(a.main_tree), raw.walk(a.tree)
    before_leaves = {p:e for p,e in before.items() if e[0] != b'40000'}
    after_leaves = {p:e for p,e in after.items() if e[0] != b'40000'}
    require(not any(p == TARGET.encode() or p.startswith((TARGET+'/').encode()) or p == b'unsolved_math_prioritization/attempts/30000170' or p.startswith(b'unsolved_math_prioritization/attempts/30000170/') for p in before), 'An independent target already existed')
    expected = dict(before_leaves)
    expected.update(selected)
    require(after_leaves == expected, 'All raw leaves/path/mode/OID conservation differs')
    require(len(before_leaves) == prep['before_leaf_count'] and len(after_leaves) == prep['after_leaf_count'], 'Leaf count differs')
    unchanged = {p:e for p,e in before_leaves.items() if p not in selected}
    require(len(unchanged) == prep['unselected_leaves_preserved'] and all(after_leaves[p] == e for p,e in unchanged.items()), 'Unselected raw leaves differ')
    for path,body in bodies.items():
        require(raw.get(oid('blob',body)) == ('blob',body), 'Stored selected full blob differs')
    original_tree = raw.walk('14c0617b4dbb7d4d064d527df85a2ab6c212f028')
    require(len(original_tree) == 19 and len([p for p,e in original_tree.items() if e[0] != b'40000']) == 17, 'Raw original target leaf census differs')
    for e in originals:
        require(original_tree[e['path'][len(TARGET)+1:].encode()] == (e['mode'].encode(),e['git_blob']), 'Original captured manifest/raw tree differs')
    siblings, rewritten = {}, []
    def compose(base, edits, prefix=b''):
        old = raw.tree(base) if base else {}
        new, groups = dict(old), {}
        for path,entry in edits.items():
            head,*tail = path.split(b'/',1)
            groups.setdefault(head,{})[tail[0] if tail else b''] = entry
        for name, below in groups.items():
            if b'' in below:
                require(len(below)==1, 'Selected leaf contains another selected path')
                new[name] = below[b'']
            else:
                prior = old.get(name)
                require(prior is None or prior[0] == b'40000', 'Raw selected ancestor collision')
                new[name] = (b'40000',compose(prior[1] if prior else None, below, prefix+name+b'/'))
        for name in old.keys()-groups.keys():
            require(old[name] == new[name], 'Untouched whole sibling identity differs')
            siblings[prefix+name] = old[name]
        body = encode_tree(new)
        sha = oid('tree',body)
        require(raw.get(sha) == ('tree',body), 'Independently composed raw tree differs')
        rewritten.append(dict(directory=prefix.decode().rstrip('/'),before=base,after=sha))
        return sha
    require(compose(a.main_tree,selected) == a.tree, 'Independent Merkle composition root differs')
    old_queue_kind, old_queue = raw.get(before_leaves[QUEUE.encode()][1])
    require(old_queue_kind == 'blob' and before_leaves[QUEUE.encode()][0] == b'100644', 'MAIN QUEUE type/mode differs')
    base = Path(s['base_queue']['path'])
    require(pin(base) == s['base_queue'] and base.read_bytes() == old_queue, 'Whole baseline QUEUE/raw body differs')
    oldlines,i = queue_row(old_queue)
    newlines,j = queue_row(bodies[QUEUE])
    require(i == j and oldlines[:i] == newlines[:i] and oldlines[i+1:] == newlines[i+1:] and oldlines[i] != newlines[j], 'Outside target QUEUE row changed')
    require(oldlines[i] == base64.b64decode(s['queue_before_base64'],validate=True) and newlines[j] == base64.b64decode(s['queue_after_base64'],validate=True), 'Exact Root row controls differ')
    cols = newlines[j].split(b'|')
    require(cols[8].strip() == b'claimed_solved' and cols[9].strip() == b'1/5' and b'../attempts/30000170/PROOF.md' in newlines[j] and b'10.5281/zenodo.23306332' in newlines[j], 'QUEUE status/budget/link/DOI differs')
    top_before,top_after = raw.tree(a.main_tree),raw.tree(a.tree)
    foreign_roots = [dict(path=n.decode(),mode=e[0].decode(),git_oid=e[1]) for n,e in sorted(top_before.items()) if n not in (b'attempts',b'unsolved_math_prioritization')]
    require(all(top_after[e['path'].encode()] == (e['mode'].encode(),e['git_oid']) for e in foreign_roots), 'Foreign root identity differs')
    preserved_attempts = [dict(path=p.decode(),mode=e[0].decode(),git_oid=e[1]) for p,e in sorted(before.items()) if e[0] == b'40000' and (p.startswith(b'attempts/') and p.count(b'/') == 1 or p.startswith(b'unsolved_math_prioritization/attempts/') and p.count(b'/') == 2)]
    require(all(after[e['path'].encode()] == (e['mode'].encode(),e['git_oid']) for e in preserved_attempts), 'A foreign/held case whole tree changed')
    raw_calls = raw.calls
    raw.close()
    turn_state = json.loads(bodies[TARGET + '/TURN_STATE.json'])
    require(turn_state['substantive_turns_completed'] == 1 and turn_state['budget'] == 5 and turn_state['remaining_author_turns'] == 4 and turn_state['substantive_turns_added_by_publication_preparation'] == 0, 'Author counter changed')
    require(turn_state['publication_status'] == 'published_verified' and turn_state['tracker']['written'] is False and turn_state['tracker']['range'] is None and turn_state['native_merge']['merged'] is False, 'Publication/tracker/native pending claims differ')
    proof = bodies[TARGET + '/PROOF.md'].decode()
    priorproof = (c / 'PROOF.md').read_text()
    def analytic_sections(text):
        return text[text.index('## 2.'):text.index('## 8.')]
    require(analytic_sections(proof) == analytic_sections(priorproof), 'Core analytic proof sections2–7 changed')
    for rel in ['checks/verify.py','checks/CHECKS.json','checks/verify_simpler.py','checks/SIMPLER_CHECKS.json','checks/SIMPLER_REPLAY_RECEIPT.json']:
        require(bodies[TARGET+'/'+rel] == (c / rel).read_bytes(), 'Mathematical checker/receipt changed')
    result = dict(schema='pr263-independent-exact-native-preparation-audit-v1', UTC=dt.datetime.now(dt.timezone.utc).isoformat(),
                  verdict='PASS_FOR_LITERAL_PRIVATE_PREPARATION_ONLY',
                  inputs=dict(preparation=pin(prepdir / 'PREPARATION.json'),selection=pin(selection_path),acceptance=pin(accepted_path),helper=pin(helper),original_manifest=pin(original_path),original_binding=pin(original_binding)),
                  prepared_outputs=[pin(prepdir / name) for name in ['PREPARATION.json','TREE_PAYLOAD.json','COMMIT_PAYLOAD.json','AUTHOR_CAS_PAYLOAD.json','BINARY_BLOB_PAYLOADS.json']],
                  checked_reused_helper=pin(reused_helper),audit_source=pin(Path(__file__)),
                  literal_main=a.main, literal_main_tree=a.main_tree,literal_tree=a.tree,literal_commit=a.commit,ordered_parents=[AUTHOR,a.main],
                  selected_full_bodies=expected_manifest, selected_count=len(bodies),target_count=len(target_list),
                  original17_retained=True,historical9_byte_identical=True,portable_original17_copies_exact=True,portable_C24_copies_exact=True,
                  original_author_raw_commit_sha256=hashlib.sha256(author_body).hexdigest(),original_author_raw_commit_bytes=len(author_body),original_author_capture=pin(captured_author_path),
                  original_author_offset_and_message_ending='author and committer -0700; no final message newline; independent raw digest and actual readback agree',
                  frozen_K03_21_plus_manifest_exact=True,whole_review_authored_counts=review_counts,
                  current_core_proof_sections2_through7_unchanged=True,all_mathematical_checker_receipts_unchanged=True,
                  public_receipt=pin(public_receipt_path),public_download_receipt_local_bytes_rechecked=public_download_pins,
                  public_download_checks_are_root_fresh_receipt_local_rechecks_not_new_network_fetches=True,
                  before_raw_leaf_count=len(before_leaves),after_raw_leaf_count=len(after_leaves),unselected_raw_leaves_preserved=len(unchanged),unselected_raw_leaf_census_sha256=census(unchanged),
                  whole_Merkle_siblings_preserved=len(siblings),whole_sibling_census_sha256=census(siblings),rewritten_ancestors=rewritten,foreign_roots=foreign_roots,preserved_foreign_attempt_case_trees=preserved_attempts,
                  queue_target_row_number=i+1,queue_before=oldlines[i].decode(),queue_after=newlines[j].decode(),outside_target_queue_rows_byte_identical=True,
                  raw_selected_blob_bodies_exact=True,independent_raw_commit_bytes_exact=True,ordered_parent_bytes_exact=True,
                  native_tree_commit_binary_payloads_exact=True,author_CAS_expected_old_nonforce_scoped=True,
                  raw_objects_read=raw_calls,provider_calls=0,external_communication=False,primary_local_Git_operations=0,ref_index_object_writes=0,
                  author_turns='1/5',review_completion_estimate_percent=95,
                  remaining_gap='Root native provider object creation/raw equality, fresh author/main/PR readbacks before expected-old CAS/merge, conditional expected-head merge, and actual full post-merge tree/commit/PR readback. This report does not authorize execution, certify firstness, or repeat mathematical review.')
    (OWN / 'EXACT_PREPARATION_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
    (OWN / 'INDEPENDENT_COMMIT.raw').write_bytes(raw_commit)
    print(json.dumps({k:result[k] for k in ['verdict','literal_main','literal_tree','literal_commit','selected_count','before_raw_leaf_count','after_raw_leaf_count','unselected_raw_leaves_preserved','whole_Merkle_siblings_preserved','review_completion_estimate_percent']},indent=2))

if __name__ == '__main__':
    run()
