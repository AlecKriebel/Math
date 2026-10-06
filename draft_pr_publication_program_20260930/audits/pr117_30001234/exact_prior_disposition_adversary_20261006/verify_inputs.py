import ast, hashlib, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
AUTH=ROOT.parent/'original_head_authentication_20261006'
def require(ok,message):
    if not ok: raise ValueError(message)
def pin(p):
    b=p.read_bytes(); return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
auth=json.loads((AUTH/'ORIGINAL_AUTHENTICATION.json').read_text())
require(auth['original_head']=='8163ee0dc7a0f944570925984cef2dc0fb291ad8','head authentication mismatch')
require(auth['problem_id']==30001234 and auth['original_budget']=='1/5','target/ledger mismatch')
original=[]
for item in auth['original_files']:
    actual=pin(AUTH/'original_attempt'/item['path'])
    require(actual['bytes']==item['bytes'] and actual['sha256']==item['sha256'],f'original input changed: {item["path"]}')
    original.append(actual)
require(len(original)==20,'original member count mismatch')
acquisition=json.loads((ROOT/'ACQUISITION_RECEIPTS.json').read_text())
for item in acquisition['immutable_inputs']:
    actual=pin(pathlib.Path(item['path']))
    require(actual==item,'acquisition immutable input changed')
statement=json.loads((AUTH/'SOURCE_STATEMENT.json').read_text())
source=json.loads((AUTH/'original_attempt'/'source_record.json').read_text())
require(statement==source,'full original statement/source record semantic mismatch')
ledger=[json.loads(line) for line in (AUTH/'original_attempt'/'turns.jsonl').read_text().splitlines() if line]
require(len(ledger)==1 and ledger[0]['attempt']==1,'original ledger mutated')
checkpoint=json.loads((ROOT/'SOURCE_SCOPE_CHECKPOINT.json').read_text())
for item in checkpoint['members']+checkpoint['inspected_pixels']:
    require(pin(pathlib.Path(item['path']))==item,'sealed source checkpoint member changed')
require(not checkpoint['root_disposition_read'] and not checkpoint['other_family_reports_read'],'early independence lost')
disposition=json.loads((ROOT/'DISPOSITION_INPUTS.json').read_text())
for item in disposition['inputs']:
    require(pin(pathlib.Path(item['path']))==item,'reviewed root disposition changed')
scripts=[]
for p in sorted(ROOT.glob('*.py')):
    tree=ast.parse(p.read_text())
    require(not any(isinstance(node,ast.Assert) for node in ast.walk(tree)),f'bare assertion in {p.name}')
    scripts.append(pin(p))
goal=pathlib.Path('/Users/alec/.codex/attachments/4df73d3d-641f-4907-b9ad-c47c468f2589/goal-objective.md')
result={'status':'pass','original_head':auth['original_head'],'original_literal_status':auth['original_literal_status'],
    'target':30001234,'original_budget':'1/5','new_proof_search_turns':0,'original_members_unchanged':original,
    'source_statement_matches_original_semantically':True,'sealed_source_scope_unchanged':True,
    'root_proposal_inputs_unchanged':True,'explicit_guard_scripts':scripts,
    'authoritative_goal':pin(goal),'original_authentication':pin(AUTH/'ORIGINAL_AUTHENTICATION.json'),
    'sourcepair_authentication':pin(AUTH/'SOURCEPAIR_AUTHENTICATION.json'),
    'original_status':pin(AUTH/'original_attempt'/'status.json'),
    'original_readiness':pin(AUTH/'original_attempt'/'readiness.json')}
print(json.dumps(result,sort_keys=True))
