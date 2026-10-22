"""Offline PR788 administrative audit; bootstrap with externally pinned hashes.

No network, publication, Git mutation, or mathematical proof certification.
"""
from pathlib import Path, PurePosixPath
import argparse, base64, hashlib, json, os, stat, sys
sys.dont_write_bytecode = True
HEAD = '3412d5a074c3f3a03f75735a9ccf1755e172204a'
PARENT = 'f36cb1e34696d460b9cfb5b03425998de48c4669'
MERGE = 'e5ae5c7ad40a379ab39ec884b415f7e0636c95f0'
MAIN_PARENT = '10d2fd06f640869d4102afb44bd01a5cf3b684e3'
SOURCE = '0af7587170f147a5a0075ebeacb007cca8a4a4eee68d536bbe9339125622fd4d'
DOI = '10.5281/zenodo.23422039'
RECORD = 23422039
SHEET = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
QRANGE = "'Math Puzzles'!A128:D128"
QPATH = 'unsolved_math_prioritization/QUEUE.md'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def pairs(rows):
    d = {}
    for k, v in rows:
        need(k not in d, 'Duplicate JSON member')
        d[k] = v
    return d

def parse(raw):
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Nonfinite JSON')))

def safe_path(value):
    p = PurePosixPath(value)
    need(isinstance(value, str) and value and not p.is_absolute()
         and all(x not in ('', '.', '..') for x in value.split('/'))
         and '\\' not in value and '\0' not in value, 'Unsafe relative path')
    return value

def regular(path):
    path = Path(path)
    for p in [path, *path.parents]:
        need(not p.is_symlink(), 'Symlink path')
    s = path.lstat()
    need(stat.S_ISREG(s.st_mode), 'Nonregular input')
    return path.read_bytes()

def git_oid(kind, raw):
    return hashlib.sha1(kind.encode() + b' ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

def git_tree(rows):
    body = b''
    for name, row in sorted(rows.items(), key=lambda x: x[0].encode() +
                            (b'/' if x[1]['type'] == 'tree' else b'')):
        need('/' not in name and name not in ('', '.', '..'), 'Invalid tree entry')
        body += (format(int(row['mode'], 8), 'o').encode() + b' ' + name.encode()
                 + b'\0' + bytes.fromhex(row['sha']))
    return git_oid('tree', body)

def check_eligibility(e, catalogs, gate):
    need(e['head_commit']['oid'] == HEAD, 'Wrong reviewed head')
    need([x['oid'] for x in e['head_commit']['parents']['nodes']] == [PARENT], 'Wrong original parent')
    rows = e['rows']
    need(rows['candidate']['commit'] == HEAD and rows['original_parent']['commit'] == PARENT,
         'Eligibility commit binding')
    for r in rows.values():
        need(sha(r['row'].encode()) == r['row_sha256'], 'Eligibility row digest')
        need(not r['acceptance_present'], 'Existing acceptance')
    need(rows['candidate']['status'] == 'claimed_solved'
         and rows['candidate']['budget'] == '2/5', 'Candidate not eligible')
    need(rows['candidate']['row'].split('|')[8].strip() == 'claimed_solved', 'Candidate row not claimed')
    need(rows['original_parent']['status'] == 'queued'
         and rows['original_parent']['budget'] == '0/5', 'Wrong baseline disposition')
    need(rows['current_main']['row'] == rows['original_parent']['row'], 'Changed baseline row')
    need(gate['original_reviewed_candidate_head'] == HEAD and gate['result'] == 'PASS'
         and gate['source_manifest_sha256'] == SOURCE, 'Readiness identity mismatch')
    need(gate['actual_whole_preprint_rounds'] == 2 and gate['final_current_round_clean'],
         'Uncompleted preprint review loop')
    need(len(catalogs['records']) == 3, 'Missing own catalog snapshots')
    for r in catalogs['records']:
        own = r['selected_catalog_record']
        need(own['id'] == '30001522' and own['statement_hash'] == gate['statement_hash']
             and own['review_hash'] == gate['review_hash'], 'Source statement/review identity')
        need(sha(json.dumps(own, sort_keys=True).encode()) == r['record_sha256'], 'Own catalog digest')

def check_public(local, record, stage, publish, inspect, independent):
    remote = record['metadata']
    need(record['id'] == RECORD and remote['doi'] == DOI, 'Wrong public record')
    need(set(local) == {'title', 'upload_type', 'publication_type', 'publication_date', 'version',
                       'language', 'creators', 'description', 'access_right', 'license',
                       'keywords', 'related_identifiers'}, 'Unexpected metadata field set')
    for k, v in local.items():
        if k == 'upload_type':
            actual = remote['resource_type']['type']
        elif k == 'publication_type':
            actual = remote['resource_type']['subtype']
        elif k == 'license':
            actual = remote['license']['id']
        else:
            actual = remote[k]
        need(actual == v, 'Public metadata differs: ' + k)
    expected = {'paper.pdf': (82418, '3c144a4b5e5c814a59db6456bc1c22f958717131fe3f4f900e52fe01ce5a3a53'),
                'source-and-verification.zip': (404378, 'f2d2a1abf9a0916992e69355010aafb81f88ccd6ad3d0976fade67d4a6e61905')}
    need({f['key'] for f in record['files']} == set(expected), 'Public file set differs')
    for r in [stage, publish, inspect]:
        need(r['id'] == RECORD and r['environment'] == 'production'
             and r['metadata_normalizations'] == [], 'Deposit identity or metadata normalization')
        need({f['name']: (f['size'], f['sha256']) for f in r['files']} == expected,
             'Staged/published file identity differs')
    need(stage['state'] == 'ready_to_publish' and publish['state'] == inspect['state'] == 'published',
         'Publication state incorrect')
    need(publish['doi'] == inspect['doi'] == DOI, 'Publication DOI differs')
    need(independent['record_id'] == RECORD and independent['doi'] == DOI
         and independent['result'] == 'PASS', 'Independent public check absent')
    need({f['name']: (f['bytes'], f['sha256']) for f in independent['public_files']} == expected,
         'Independent public downloads differ')
    need(all(f['status'] == 200 for f in independent['public_files'])
         and independent['doi_resolution']['status'] == 200, 'Unresolved public payload/DOI')

def check_tracker(receipt, append, independent, scope):
    need(receipt['result'] == independent['result'] == 'PASS'
         and receipt['spreadsheetId'] == independent['spreadsheetId'] == SHEET,
         'Wrong tracker identity')
    need(receipt['updated_range'] == independent['range'] == QRANGE, 'Wrong tracker cells')
    values = receipt['intended_values']
    need(len(values) == 4 and values[:3] == ['https://www.unsolvedmath.com/problems/30001522', '',
                                          'https://doi.org/' + DOI], 'Tracker identifiers differ')
    need(receipt['readback']['values'] == independent['values'] == [values], 'Tracker readbacks differ')
    updates = append['updates']
    need(updates['updatedCells'] == 4 and updates['updatedRows'] == 1
         and updates['updatedColumns'] == 4 and updates['updatedRange'] == QRANGE
         and updates['updatedData']['values'] == [values], 'Append scope differs')
    need(scope['summary'] in values[3] and scope['priority_summary'] in values[3], 'Tracker scope text differs')
    for term in ['actual free cyclic actions for every odd prime', 'no nontrivial continuous circle action',
                 'nonabelian fundamental groups', 'Priority remains unresolved',
                 'unrefereed', 'no external human peer review']:
        need(term in values[3], 'Tracker qualification missing: ' + term)

def check_merge(proof, witness, original):
    need(proof['result'] == 'PASS' and proof['exact_reviewed_head'] == HEAD
         and proof['merge_commit']['oid'] == MERGE, 'Wrong exact merge')
    need([x['oid'] for x in proof['merge_commit']['parents']['nodes']] == [MAIN_PARENT, HEAD],
         'Wrong merge parents')
    need(not proof['branch_repair_needed'] and proof['fresh_merged_pr']['merged'], 'Merge state')
    expected = {r['path']: {'mode': '100644', 'type': 'blob', 'sha': r['git_blob']}
                for r in original['original_files']}
    need(len(expected) == 48 and proof['original_candidate_files'] == original['original_files'],
         'Original candidate bindings differ')
    before = base64.b64decode(witness['before_base64'], validate=True)
    after = base64.b64decode(witness['after_base64'], validate=True)
    old = before.splitlines(keepends=True)
    indices = [i for i, row in enumerate(old) if row.startswith(b'| ') and b' 30001522 / ' in row]
    need(len(indices) == 1, 'Queue own row missing/duplicated')
    i = indices[0]
    candidate = witness['candidate_own_row'].encode()
    need(candidate.decode().split('|')[8:10] == [' claimed_solved ', ' 2/5 '], 'Candidate queue scope')
    need(after == b''.join(old[:i] + [candidate] + old[i + 1:]), 'Unrelated queue bytes changed')
    q = proof['queue_proof']
    need(git_oid('blob', before) == q['base_blob_sha1'], 'Queue baseline identity')
    need(git_oid('blob', after) == q['expected_result_blob_sha1'] == q['actual_result_blob_sha1'],
         'Queue merge identity')
    need(sha(b''.join(old[:i] + old[i + 1:])) == q['other_rows_projection_sha256'], 'Queue projection identity')
    expected[QPATH] = {'mode': '100644', 'type': 'blob', 'sha': git_oid('blob', after)}
    need(proof['updates'] == expected, 'Unexpected merge update path or blob')
    trees = proof['base_tree_objects_used']
    for h, entries in trees.items():
        need(git_tree(entries) == h, 'Base Git tree object differs')
    trie = {}
    for path, value in expected.items():
        safe_path(path)
        parts = path.split('/')
        node = trie
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = value
    def apply(h, node):
        rows = dict(trees[h]) if h else {}
        for name, value in node.items():
            if 'sha' in value:
                rows[name] = value
            else:
                existing = rows.get(name)
                need(existing is None or existing['type'] == 'tree', 'Non-tree ancestor')
                rows[name] = {'mode': '040000', 'type': 'tree',
                              'sha': apply(existing['sha'] if existing else None, value)}
        return git_tree(rows)
    root = apply(proof['main_parent_tree'], trie)
    need(root == proof['expected_resulting_tree'] == proof['actual_resulting_tree']
         == proof['merge_commit']['tree']['oid'], 'Full resulting Merkle tree differs')

def verify(packet, case, expected_manifest, expected_checker):
    need(sha(regular(Path(__file__))) == expected_checker, 'Checker hash differs')
    mfraw = regular(packet / 'MANIFEST.json')
    need(sha(mfraw) == expected_manifest, 'Packet manifest hash differs')
    mf = parse(mfraw)
    names = [safe_path(x['path']) for x in mf['files']]
    need(len(names) == len(set(names)), 'Duplicate packet path')
    actual = {p.relative_to(packet).as_posix() for p in packet.rglob('*')
              if p.relative_to(packet).parts[0] != 'scratch' and not p.is_dir()}
    need(actual == set(names) | {'MANIFEST.json'}, 'Open packet')
    for row in mf['files']:
        raw = regular(packet / row['path'])
        need(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Packet payload differs')
    bindings = parse(regular(packet / 'INPUT_BINDINGS.json'))
    external = [safe_path(x['path']) for x in bindings['files']]
    need(len(external) == len(set(external)), 'Duplicate input path')
    for row in bindings['files']:
        raw = regular(case / row['path'])
        need(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Bound external input differs')
    get = lambda name: parse(regular(packet / name))
    ext = lambda name: parse(regular(case / name))
    gate = get('FINAL_READINESS_PREPUBLICATION_SNAPSHOT.json')
    check_eligibility(get('ELIGIBILITY_INDEPENDENT_READ.json'), get('OWN_SOURCE_CATALOG_BINDINGS.json'), gate)
    inventory = ext('preprint/PACKAGE_INVENTORY.json')
    need(inventory['source_manifest_sha256'] == SOURCE and inventory['files'] == gate['publication_files'],
         'Frozen package inventory differs')
    raw = regular(case / 'preprint/source/MANIFEST.json')
    need(sha(raw) == SOURCE, 'Source manifest differs')
    source = parse(raw)
    paths = [safe_path(r['path']) for r in source['files']]
    need(len(paths) == len(set(paths)) == 194, 'Source count differs')
    for row in source['files']:
        raw = regular(case / 'preprint/source' / row['path'])
        need(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Source file differs')
    actual = {p.relative_to(case / 'preprint/source').as_posix()
              for p in (case / 'preprint/source').rglob('*') if not p.is_dir()}
    need(actual == set(paths) | {'MANIFEST.json'}, 'Source closure differs')
    check_public(ext('preprint/zenodo-metadata.json')['metadata'], get('ZENODO_PUBLIC_RECORD.json'),
                 ext('publication/STAGE_RECEIPT.json'), ext('publication/PUBLISH_RECEIPT.json'),
                 ext('publication/INSPECT_AFTER_PUBLISH.json'), get('PUBLICATION_INDEPENDENT_CHECK.json'))
    check_tracker(ext('publication/SHEET_VERIFICATION.json'), ext('publication/SHEET_APPEND_RECEIPT.json'),
                  get('TRACKER_INDEPENDENT_READBACK.json'), ext('TRACKER_SCOPE.json'))
    check_merge(get('MERGE_SCOPE_PROOF.json'), get('QUEUE_SCOPE_WITNESS.json'),
                ext('intake/ROOT_SOURCE_IDENTITY.json'))
    controls = get('GUARD_CONTROL_RESULTS.json')
    need(controls['positive_controls'] == 2 and controls['negative_controls'] == 21,
         'Guard controls incomplete')
    need(all(x['accepted'] == x['expected_accept'] for x in controls['controls']), 'Guard control failure')
    return {'result': 'PASS', 'scope': 'administrative custody and exact merge; not a new mathematical review',
            'record_id': RECORD, 'doi': DOI, 'merged_head': HEAD, 'merge_commit': MERGE,
            'source_manifest_sha256': SOURCE, 'closed_source_files': 195,
            'packet_files_including_manifest': len(names) + 1, 'bound_external_inputs': len(external)}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet-root', type=Path, required=True)
    p.add_argument('--case-root', type=Path, required=True)
    p.add_argument('--expected-manifest-sha256', required=True)
    p.add_argument('--expected-checker-sha256', required=True)
    a = p.parse_args()
    print(json.dumps(verify(a.packet_root, a.case_root,
                            a.expected_manifest_sha256, a.expected_checker_sha256), sort_keys=True))

if __name__ == '__main__':
    main()
