from pathlib import Path
import datetime, hashlib, json, sys
R = Path('/Users/alec/Documents/Math')
D = R / 'draft_pr_claimed_solved_700_800_20261012'
T = D / 'audits/pr799_30002364/tmp'
sys.path.insert(0, str(D))
from graphql_scoped_commit import Remote, get_pr
from remote_scoped_commit import oid
I = T / 'intake'
identity = json.loads((I / 'ROOT_SOURCE_IDENTITY.json').read_text())
H = 'cc45ec9dc93515593c3b2a228def86c3a562e13f'
P = 'c40562362d60cce52a3128fa17313ad729f0d835'
assert identity['reviewed_head'] == H and len(identity['original_files']) == 54
assert hashlib.sha256((I / 'ROOT_SOURCE_IDENTITY.json').read_bytes()).hexdigest() == 'a875b05b2fd00b21dde0328993d8ae6492588c9b02f03f2655ee6cdb0d51b9fe'
chain=json.loads((I / 'PR_COMMIT_CHAIN.json').read_text())
assert chain['headRefOid']==H and chain['commits']['totalCount']==2 and not chain['commits']['pageInfo']['hasNextPage']
nodes=[x['commit'] for x in chain['commits']['nodes']]
assert [(n['oid'],[x['oid'] for x in n['parents']['nodes']])for n in nodes]==[('d0198704b65fb1d058536b360eabb91f3717661d',[P]),(H,['d0198704b65fb1d058536b360eabb91f3717661d'])]
before, after = Remote(P), Remote(H)
changes = {}
for row in identity['original_files']:
    assert row['changeType'] == 'ADDED' and before.entry(row['path']) is None
    entry = {'mode': '100644', 'type': 'blob', 'sha': row['git_blob']}
    assert after.entry(row['path']) == entry
    changes[row['path']] = entry
queue = 'unsolved_math_prioritization/QUEUE.md'
old, new = before.read(queue), after.read(queue)
def own(raw):
    lines = raw.splitlines(keepends=True)
    places = [i for i,l in enumerate(lines) if l.startswith('| ') and ' 30002364 / ' in l]
    assert len(places) == 1
    i = places[0]
    return lines[i], lines[:i] + lines[i+1:]
b, bo = own(old)
a, ao = own(new)
assert bo == ao and a.split('|')[8].strip() == 'claimed_solved' and a.split('|')[9].strip() == '5/5'
bc, ac = b.split('|'), a.split('|')
assert len(bc) == len(ac) == 14
assert all(bc[i] == ac[i] for i in range(14) if i not in (8,9,11))
changes[queue] = {'mode': '100644', 'type': 'blob', 'sha': oid('blob', new.encode())}
assert before.expected_tree(changes) == after.root == 'd9d018cb8f2253b16ea410f7c45707682dde94ba'
assert get_pr(799)['head']['sha'] == H
rec = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'result': 'PASS',
       'head': H, 'original_PR_branch_base': P, 'original_commit_chain': nodes, 'full_tree': after.root, 'original_regular_additions': 54,
       'only_other_change_exact_own_QUEUE_three_cells': True,
       'all_other_paths_modes_and_QUEUE_bytes_preserved': True,
       'original_explicit_budget': '5/5', 'new_substantive_proof_turns': 0,
       'own_baseline_status': bc[8].strip(), 'own_baseline_turns': bc[9].strip(),
       'scope_precondition_correction': 'The first harmless readonly scope attempt used the immediate parent, which already contains the candidate. Actual PR has two commits; aggregate exact scope is verified from the first commit parent. No mutation occurred.', 'allowed_paths': sorted(changes)}
(T / 'root-receipts/ROOT_ORIGINAL_SCOPE.json').write_text(json.dumps(rec, indent=2) + '\n')
print(json.dumps({k: v for k, v in rec.items() if k != 'allowed_paths'}))
