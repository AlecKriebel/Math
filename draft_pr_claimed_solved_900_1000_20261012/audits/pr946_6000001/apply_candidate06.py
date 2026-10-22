"""Apply only the externally tested workflow repair; preserve submission bytes."""
import sys
if not sys.flags.isolated or sys.flags.optimize:
    raise RuntimeError('Use -I -B without optimization')
from pathlib import Path
import ast, datetime, hashlib, json, os, stat

ROOT = Path('/Users/alec/Documents/Math')
P = ROOT/'draft_pr_claimed_solved_900_1000_20261012'
A = P/'audits/pr946_6000001'
D = A/'preprint'
OLD = '62fa159687104c889195863303fa5642d877e52257bc9e4fb2bc97e89ea2b919'
NEW = '8e1a0d7b3ca6e5d72e76415541b393fbfbe52e307368bc86b9e7982d5be27cd7'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def fp(path):
    raw=path.read_bytes()
    return {'bytes':len(raw),'sha256':sha(raw)}

def obj(path):
    return json.loads(path.read_bytes())

oldfreezeraw=(D/'reviewed_candidates/candidate05/FREEZE.json').read_bytes()
assert sha(oldfreezeraw)=='adf39584e2645b7b530447523f690ca7e2bf68587c647f7bd5b218b758fa8068'
assert (D/'FREEZE.json').read_bytes()==oldfreezeraw
freeze=json.loads(oldfreezeraw)
assert obj(A/'CANDIDATE05_PRESERVATION.json')['status']=='PASS'
test=obj(A/'REVIEW05_GLOBAL_CLOSURE_CONTROLS.json')
assert test['status']=='PASS' and test['root_control_count']==105
assert test['subject_core_sha256']==NEW and test['actual_external_mutations']==0
source=(A/'private/planned_review05_repair/accept_candidate06_proposal.py').read_bytes()
assert sha(source)==NEW
oldsource=(D/'reviewed_candidates/candidate05/operations'/P.name/'accept_pr946.py').read_bytes()
assert sha(oldsource)==OLD
oldtree,newtree=(ast.parse(raw) for raw in (oldsource,source))
functions=lambda tree:{node.name:ast.dump(node,include_attributes=False) for node in tree.body
                       if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef))}
of,nf=functions(oldtree),functions(newtree)
assert set(nf)-set(of)=={'candidate_state_check','review_state_check'} and not(set(of)-set(nf))
changed=sorted(name for name in set(of)&set(nf) if of[name]!=nf[name])
assert changed==['accept','accepted_review_check','accepted_state_check']
outside=lambda tree:ast.dump(ast.Module(body=[n for n in tree.body if not isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))],type_ignores=[]),include_attributes=False)
assert outside(oldtree)==outside(newtree)
for name,pin in freeze['files'].items():
    assert fp(D/name)==pin
originals=obj(A/'ORIGINAL_SNAPSHOT.json')['files']
assert len(originals)==33
for name,pin in originals.items():
    original=A/'original'/name
    assert stat.S_ISREG(original.lstat().st_mode)
    assert fp(original)['sha256']==pin and stat.S_IMODE(original.stat().st_mode)==0o644
oldinvraw=(D/'reviewed_candidates/candidate05/OPERATIONS_INVENTORY.json').read_bytes()
oldinv=json.loads(oldinvraw)
assert sha(oldinvraw)==freeze['operations_inventory_sha256']
newinv=json.loads(oldinvraw)
corekey=P.relative_to(ROOT).as_posix()+'/accept_pr946.py'
newinv['files'][corekey]={'bytes':len(source),'sha256':NEW}
newinvraw=(json.dumps(newinv,indent=2)+'\n').encode()
core=P/'accept_pr946.py'
assert sha(core.read_bytes()) in (OLD,NEW)
assert (A/'OPERATIONS_INVENTORY.json').read_bytes() in (oldinvraw,newinvraw)
for name,pin in oldinv['files'].items():
    if name!=corekey:
        assert fp(ROOT/name)==pin
ct, it = P/'accept_pr946.py.root-tmp', A/'OPERATIONS_INVENTORY.json.root-tmp'
ct.write_bytes(source); ct.chmod(stat.S_IMODE(core.stat().st_mode))
it.write_bytes(newinvraw); it.chmod(0o644)
assert sha(ct.read_bytes())==NEW
os.replace(ct,core);os.replace(it,A/'OPERATIONS_INVENTORY.json')
record={
    'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'APPLIED_TESTED_FOCUSED_REPAIR',
    'baseline_candidate':5,'next_candidate':6,'old_core_sha256':OLD,'new_core_sha256':NEW,
    'added_functions':sorted(set(nf)-set(of)),'changed_functions':changed,
    'every_other_function_AST_and_module_AST_unchanged':True,
    'all223_submission_payload_fingerprints_unchanged':True,
    'changed_operations_files':[corekey],
    'old_operations_inventory_sha256':sha(oldinvraw),'new_operations_inventory_sha256':sha(newinvraw),
    'root_old_controls':82,'root_new_controls':105,'all_original33_unchanged':True,
    'no_acceptance_or_external_action':True,'new_proof_responses':0}
with (A/'ROOT_CANDIDATE06_CHANGE_SCOPE.json').open('x') as handle:
    json.dump(record,handle,indent=2);handle.write('\n')
print(json.dumps({'status':record['status'],'core_sha256':NEW,
                  'operations_inventory_sha256':sha(newinvraw),'all223_payloads_unchanged':True}))
