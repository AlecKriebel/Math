"""PR73 operational guards. No scientific interpretation is chosen here."""
from pathlib import Path
import base64
import datetime as dt
import hashlib
import json
import os
import re
import sqlite3
import stat
import subprocess
import sys

PREP = Path(__file__).resolve().parent
ROOT = Path('/Users/alec/Documents/Math')
AUDIT = PREP.parent
AUTH = AUDIT / 'original_source_authentication_20261004'
HEAD = '6f82e81631fd43abc0140a831acfb43c150f4210'
ID = '2985'
CODE = 'KP-4.109'
PR = 73
REPO = 'AlecKriebel/Math'
PREFIX = 'unsolved_math_prioritization/attempts/2985'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
STATE = 'unsolved_math_prioritization/state.json'
HISTORY = 'unsolved_math_prioritization/history.jsonl'
ACK = ROOT / 'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'
ACK_REL = str(ACK.relative_to(ROOT))
TAG = 'PR73 native integration v2 20261004'
DOCUMENTS = {'CURRENT_RESULT.md', 'CURRENT_PRIORITY.md', 'PR_BODY.md', 'DISPOSITION_PROPOSAL.json'}
ACCEPT_PATHS = {PREFIX + '/' + x for x in ('CURRENT_RESULT.md', 'CURRENT_PRIORITY.md', 'acceptance.json')} | {STATE, HISTORY}

def require(ok, msg):
    if not ok:
        raise RuntimeError(msg + '; STOP, retain partial state and full streams for ROOT')
def sha(b):
    return hashlib.sha256(b).hexdigest()
def git_blob(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
def canonical(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
def same(x, y):
    return canonical(x) == canonical(y)
def json_bytes(x):
    return (json.dumps(x, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()
def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()
def timestamp(x):
    require(type(x) is str, 'UTC field is not a string')
    v = dt.datetime.fromisoformat(x.replace('Z', '+00:00'))
    require(v.tzinfo is not None, 'UTC field lacks timezone')
    return v.astimezone(dt.timezone.utc)
def safe_path(rel):
    require(type(rel) is str and rel and not Path(rel).is_absolute(), 'Expected repository-relative path')
    p = ROOT / rel
    require('..' not in Path(rel).parts and p.resolve().is_relative_to(ROOT.resolve()), 'Path escaped repository')
    require(not any(q.is_symlink() for q in (p, *p.parents) if q.is_relative_to(ROOT)), 'Symlink in evidence path')
    return p
def load(path):
    def unique(pairs):
        d = {}
        for k, v in pairs:
            require(k not in d, 'Duplicate JSON key')
            d[k] = v
        return d
    return json.loads(Path(path).read_bytes(), object_pairs_hook=unique)
def pin(path):
    p = Path(path)
    require(p.is_file() and not p.is_symlink(), 'Regular evidence file is missing')
    b = p.read_bytes()
    return {'path': str(p.relative_to(ROOT)), 'bytes': len(b), 'sha256': sha(b)}
def check_pin(row):
    require(type(row) is dict and set(row) == {'path', 'bytes', 'sha256'}, 'Evidence pin schema differs')
    require(type(row['bytes']) is int and row['bytes'] >= 0 and type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}', row['sha256']), 'Evidence pin value differs')
    require(pin(safe_path(row['path'])) == row, 'Bound evidence changed: ' + row['path'])
def fields(obj, names):
    require(type(obj) is dict and set(obj) == set(names), 'Exact object schema differs')

def originals():
    m = load(AUTH / 'ORIGINAL_BLOB_MANIFEST.json')
    require(m['head'] == HEAD and m['artifact_count'] == 29 and len(m['artifacts']) == 29, 'Original manifest identity/count differs')
    seen = set()
    for row in m['artifacts']:
        require(row['path'] not in seen and row['mode'] == '100644', 'Original duplicate path/mode')
        seen.add(row['path'])
        p = AUTH / row['retained_path']
        require(p.resolve().is_relative_to((AUTH / 'original').resolve()) and p.is_file() and not p.is_symlink(), 'Retained original path differs')
        b = p.read_bytes()
        require(len(b) == row['bytes'] and sha(b) == row['sha256'] and git_blob(b) == row['git_blob_SHA1'] == row['computed_git_blob_SHA1'], 'Original bytes/hash/Git blob differ')
        require(stat.S_IMODE(p.stat().st_mode) == 0o644, 'Retained original filesystem mode differs')
    files = [x for x in m['artifacts'] if x['path'].startswith(PREFIX + '/')]
    require(len(files) == 19 and all(x['incoming_changed_domain'] is True for x in files), 'Original 19-file domain differs')
    require({x['path'] for x in m['artifacts'] if x['incoming_changed_domain']} == {x['path'] for x in files} | {QUEUE}, 'Incoming 20-path domain differs')
    require(PREFIX + '/status.json' not in seen, 'Original status.json must be ABSENT')
    a = AUTH / 'original' / PREFIX
    readiness = load(a / 'readiness.json')
    require(readiness['status'] == 'candidate_independently_reviewed' and type(readiness['substantive_attempts']) is int and readiness['substantive_attempts'] == 1 and type(readiness['attempt_limit']) is int and readiness['attempt_limit'] == 5, 'Native original readiness/accounting differs')
    ledger = (a / 'turns.jsonl').read_bytes()
    events = [json.loads(x) for x in ledger.splitlines()]
    require(len(events) == 1 and type(events[0]['turn']) is int and events[0]['turn'] == 1, 'Original ledger must contain exactly one turn1 event')
    source = load(a / 'source_record.json')
    require(set(source) == {'dataset', 'dataset_revision', 'license', 'problem', 'exact_separate_prior_report'}, 'Original native wrapper keys differ')
    require(source['dataset'] == 'ulamai/UnsolvedMath' and source['dataset_revision'] == '37e53eabe540fb458758e198be61634bd02ee008' and source['license'] == 'CC-BY-4.0', 'Original native source identity differs')
    require(type(source['problem']) is dict and type(source['problem']['id']) is int and source['problem']['id'] == 2985 and source['problem']['problem_number'] == CODE and source['exact_separate_prior_report'] is None, 'Native problem/prior typed values differ')
    require(load(AUTH / 'original' / STATE) == {} and (AUTH / 'original' / HISTORY).read_bytes() == b'', 'Original globals are not empty as authenticated')
    submitted = target_row((AUTH / 'original' / QUEUE).read_bytes())
    require(submitted.decode().split('|')[8].strip() == 'claimed_solved' and submitted.decode().split('|')[9].strip() == '1/5', 'Original literal eligibility/budget differs')
    frozen = load(a / 'frozen_artifacts.json')
    require(type(frozen['sha256']) is dict and len(frozen['sha256']) == 3, 'Original frozen-artifact shape differs')
    for name, digest in frozen['sha256'].items():
        require(sha((a / name).read_bytes()) == digest, 'Original frozen-artifact hash differs')
    return m, files, source

def target_row(body):
    rows = [x for x in body.splitlines(keepends=True) if b'| 2985 /' in x]
    require(len(rows) == 1, 'Target QUEUE row is not unique')
    require(len(rows[0].decode().split('|')) == 14, 'Target QUEUE cell schema differs')
    return rows[0]

def sourcepair(base, source):
    """Full raw hashes plus typed raw/native/SQL joins; never normalize native null."""
    manifest_path = base / 'manifest.json'
    manifest = load(manifest_path)
    authenticated = load(AUTH / 'SOURCEPAIR_AUTHENTICATION.json')
    manifest_bytes = manifest_path.read_bytes()
    require(len(manifest_bytes) == authenticated['current_manifest_bytes'] and sha(manifest_bytes) == authenticated['current_manifest_sha256'] and manifest_bytes == (AUTH / 'original/unsolved_math_prioritization/manifest.json').read_bytes(), 'Current manifest differs from authenticated whole original manifest')
    require(manifest['dataset'] == source['dataset'] and manifest['revision'] == source['dataset_revision'], 'Raw manifest revision/dataset differs')
    cache = base / 'cache'
    values = {}
    whole_pins = [pin(manifest_path)]
    source_pins = {Path(x['path']).name: x for x in authenticated['local_snapshots_before'] if x['presence'] == 'present'}
    for name in ('problems.json', 'research_results.json'):
        p = cache / name
        require(p.is_file() and not p.is_symlink(), 'Raw source missing')
        b = p.read_bytes()
        require({'bytes': len(b), 'sha256': sha(b)} == manifest['files'][name], 'Full raw bytes differ from manifest')
        require(len(b) == source_pins[name]['bytes'] and sha(b) == source_pins[name]['sha256'] and stat.S_IMODE(p.stat().st_mode) == 0o644, 'Full raw byte/mode pins differ from completed authentication')
        whole_pins.append(pin(p))
        values[name] = json.loads(b)
    problems, reports = values['problems.json'], values['research_results.json']
    require(type(problems) is list and type(reports) is dict and same([x for x in problems if str(x['id']) == ID], [source['problem']]), 'Raw/native full problem differs')
    require(CODE not in reports, 'Raw prior-report lookup must remain ABSENT')
    dbpath = cache / 'catalog.sqlite'
    require(dbpath.is_file() and not dbpath.is_symlink(), 'SQL source missing')
    sql_bytes = dbpath.read_bytes()
    require(len(sql_bytes) == source_pins['catalog.sqlite']['bytes'] and sha(sql_bytes) == source_pins['catalog.sqlite']['sha256'] and stat.S_IMODE(dbpath.stat().st_mode) == 0o644, 'Full SQL bytes/mode differ from completed authentication')
    whole_pins.append(pin(dbpath))
    require(all(not Path(str(dbpath) + s).exists() for s in ('-wal', '-shm', '-journal')), 'SQL sidecar appeared; immutable read unsafe')
    with sqlite3.connect('file:' + str(dbpath) + '?mode=ro&immutable=1', uri=True) as db:
        require(db.execute('PRAGMA integrity_check').fetchall() == [('ok',)], 'SQL integrity differs')
        require(db.execute('SELECT revision FROM metadata').fetchall() == [(source['dataset_revision'],)], 'SQL revision differs')
        rows = db.execute('SELECT payload,report FROM records WHERE key=?', (ID,)).fetchall()
        require(len(rows) == 1 and rows[0][0] is not None and rows[0][1] is not None and same(json.loads(rows[0][0]), source['problem']) and type(json.loads(rows[0][1])) is dict and json.loads(rows[0][1]) == {}, 'SQL typed problem/normalized empty prior differs')
        require(db.execute('SELECT count(*) FROM records').fetchone()[0] == manifest['records'] == 15458, 'SQL/source record count differs')
    for row in whole_pins: check_pin(row)
    pair = [source['problem'], {}] # Existing catalog uses SQL-normalized report solely for its own fingerprint.
    review_hash = sha(json.dumps(pair, sort_keys=True).encode())
    return {'dataset': source['dataset'], 'dataset_revision': source['dataset_revision'],
            'native_prior_field': 'exact_separate_prior_report', 'native_prior_presence': 'present',
            'native_prior_json_type': 'null', 'raw_prior_lookup_presence': 'absent',
            'SQL_prior_json_type': 'object', 'SQL_prior_is_empty_object': True,
            'review_hash_SQL_normalized_only': review_hash,
            'native_problem_hash': sha(canonical(source['problem']).encode()),
            'native_report_hash': sha(b'null'), 'statement_hash': sha(source['problem']['statement'].encode()),
            'whole_current_source_pins': whole_pins}

def validate_gate(gate_path):
    gate_path = Path(gate_path).resolve()
    require(gate_path.is_relative_to(AUDIT.resolve()) and gate_path.name != 'ROOT_GATE_TEMPLATE_V2.json', 'Fresh ROOT gate must be in PR73 audit; template is unusable')
    g = load(gate_path)
    fields(g, ('schema', 'stage', 'UTC', 'authorizer', 'PR', 'problem_id', 'expected_submitted_head', 'audited_outcome',
               'ROOT_authorizes_sequential_native_integration', 'ROOT_personally_read_required_reports',
               'mathematics_validated', 'historical_classification_certified', 'historical_classification_meaning', 'final_adversarial_review_clean',
               'explicit_scope_interpretation_approved', 'scope_interpretation', 'original_proof_turns',
               'new_original_proof_turns', 'ROOT_reviewed_frozen_exact_plan', 'exact_plan', 'bound_evidence',
               'bound_operators', 'current_readiness_evidence', 'minimum_writer_ack_utc', 'claimed_solved_gates', 'already_solved_gates', 'partial_gates'))
    require(g['schema'] == 'pr73-root-scientific-native-gate/v2' and g['stage'] == 'FRESH_FINAL_ROOT_SCIENTIFIC_GATE' and g['authorizer'] == 'ROOT' and g['PR'] == PR and g['problem_id'] == ID and g['expected_submitted_head'] == HEAD, 'ROOT gate identity/stage differs')
    require(g['audited_outcome'] in ('claimed_solved', 'already_solved', 'partial'), 'ROOT has not selected an eligible audited outcome')
    require(g['historical_classification_meaning'] == 'precise_bounded_classification_without_inferred_prior_target_resolution', 'Historical classification must not infer prior target resolution')
    for key in ('ROOT_authorizes_sequential_native_integration', 'ROOT_personally_read_required_reports', 'mathematics_validated', 'historical_classification_certified', 'final_adversarial_review_clean', 'explicit_scope_interpretation_approved', 'ROOT_reviewed_frozen_exact_plan'):
        require(g[key] is True, 'ROOT scientific gate incomplete: ' + key)
    fields(g['scope_interpretation'], ('id', 'text', 'excluded_scopes'))
    require(all(type(g['scope_interpretation'][x]) is str and g['scope_interpretation'][x].strip() for x in ('id', 'text')) and type(g['scope_interpretation']['excluded_scopes']) is list and g['scope_interpretation']['excluded_scopes'] and all(type(x) is str and x.strip() for x in g['scope_interpretation']['excluded_scopes']), 'Scope interpretation is unspecified')
    require(len(g['scope_interpretation']['excluded_scopes']) == len(set(g['scope_interpretation']['excluded_scopes'])), 'Duplicate excluded scope interpretation')
    require(g['original_proof_turns'] == '1/5' and type(g['new_original_proof_turns']) is int and g['new_original_proof_turns'] == 0, 'Original budget/history authority differs')
    timestamp(g['UTC'])
    original_utc = load(AUTH / 'ORIGINAL_AUTHENTICATION.json')['UTC']
    require(timestamp(original_utc) <= timestamp(g['UTC']) <= timestamp(now()), 'ROOT gate predates completed custody or is future-dated')
    require(timestamp(g['minimum_writer_ack_utc']) >= timestamp(g['UTC']), 'Minimum writer ack predates ROOT gate')
    require(type(g['bound_evidence']) is list and g['bound_evidence'] and type(g['bound_operators']) is list, 'Bound evidence/operators missing')
    for rows in (g['bound_evidence'], g['bound_operators']):
        require(len(rows) == len({r['path'] for r in rows}), 'Duplicate bound evidence/operator path')
        require(all(r['path'] != ACK_REL for r in rows), 'Dynamic acknowledgment control body cannot be a frozen scientific/operator input')
    for row in [g['exact_plan'], g['current_readiness_evidence'], *g['bound_evidence'], *g['bound_operators']]: check_pin(row)
    required_evidence = {str((AUTH / x).relative_to(ROOT)) for x in ('ORIGINAL_AUTHENTICATION.md', 'ORIGINAL_AUTHENTICATION.json', 'ORIGINAL_BLOB_MANIFEST.json', 'SOURCEPAIR_AUTHENTICATION.json')}
    required_evidence |= {str((AUTH / 'original' / PREFIX / x).relative_to(ROOT)) for x in ('CANDIDATE.md', 'source_record.json', 'readiness.json', 'turns.jsonl')}
    required_evidence |= {'unsolved_math_prioritization/' + x for x in ('manifest.json', 'catalog.json', 'queue.py', 'policy.json', 'cache/problems.json', 'cache/research_results.json', 'cache/catalog.sqlite')}
    require(required_evidence <= {r['path'] for r in g['bound_evidence']}, 'ROOT gate does not bind original proof/schema/accounting/custody')
    require({str((PREP / x).relative_to(ROOT)) for x in ('native_common_v2.py', 'ROOT_native_integration_v2.py', 'ROOT_native_readback_v2.py', 'ROOT_GATE_SCHEMA_V2.json', 'FROZEN_PLAN_SCHEMA_V2.json')} <= {r['path'] for r in g['bound_operators']}, 'ROOT gate does not bind all operators/schemas')
    plan_path = safe_path(g['exact_plan']['path'])
    require(plan_path.resolve().is_relative_to(AUDIT.resolve()) and plan_path.name != 'FROZEN_PLAN_TEMPLATE_V2.json', 'Frozen plan must be explicit and non-template')
    p = load(plan_path)
    fields(p, ('schema', 'stage', 'PR', 'problem_id', 'expected_submitted_head', 'execution_id', 'audited_outcome', 'scope_interpretation', 'expected_base_main',
               'packet', 'pr_title', 'submitted_pr_title', 'submitted_pr_body_sha256', 'queue_before_row_sha256',
               'queue_after_row_base64', 'acceptance_scientific_fields', 'merge_commit_message', 'acceptance_commit_message', 'checkpoint_commit_message', 'checkpoint_files'))
    require(p['schema'] == 'pr73-frozen-native-plan/v2' and p['stage'] == 'ROOT_REVIEWED_FROZEN_EXACT_BYTES' and p['PR'] == PR and p['problem_id'] == ID and p['expected_submitted_head'] == HEAD and p['audited_outcome'] == g['audited_outcome'] and same(p['scope_interpretation'], g['scope_interpretation']), 'Frozen plan identity/outcome/scope differs')
    require(type(p['execution_id']) is str and re.fullmatch('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', p['execution_id']), 'Unique frozen execution UUID missing')
    require(type(p['expected_base_main']) is str and re.fullmatch('[0-9a-f]{40}', p['expected_base_main']), 'Frozen current base is absent')
    for key in ('pr_title', 'submitted_pr_title', 'merge_commit_message', 'acceptance_commit_message', 'checkpoint_commit_message'):
        require(type(p[key]) is str and p[key].strip(), 'Frozen metadata missing')
    for key in ('submitted_pr_body_sha256', 'queue_before_row_sha256'):
        require(type(p[key]) is str and re.fullmatch('[0-9a-f]{64}', p[key]), 'Frozen hash missing')
    require(type(p['packet']) is list and len(p['packet']) == 4 and {Path(r['path']).name for r in p['packet']} == DOCUMENTS, 'Exactly four frozen packet files required')
    for row in p['packet']: check_pin(row)
    require(len({safe_path(r['path']).parent for r in p['packet']}) == 1 and all(safe_path(r['path']).resolve().is_relative_to(AUDIT.resolve()) for r in p['packet']), 'Packet files must be in one PR73 directory')
    packet = {Path(r['path']).name: safe_path(r['path']).read_bytes() for r in p['packet']}
    proposal = json.loads(packet['DISPOSITION_PROPOSAL.json'])
    require(proposal.get('PR') == PR and proposal.get('problem_id') == ID and proposal.get('submitted_head') == HEAD and proposal.get('original_budget') == '1/5', 'Frozen prospective disposition identity differs')
    science = p['acceptance_scientific_fields']
    fields(science, ('status', 'accepted_as', 'scope_interpretation', 'credited_prior_disposition', 'attributed_partial_disposition', 'novelty_clearance', 'new_paper', 'publication_DOI', 'tracker_append', 'scientific_claims'))
    require(science['status'] == g['audited_outcome'] == proposal.get('proposed_current_status') and same(science['scope_interpretation'], g['scope_interpretation']) and type(science['scientific_claims']) is dict and science['scientific_claims'] and type(science['accepted_as']) is str and science['accepted_as'].strip() and science['accepted_as'] == proposal.get('proposed_accepted_as'), 'Explicit frozen-plan scientific fields are absent or differ from ROOT gate/proposal')
    after = base64.b64decode(p['queue_after_row_base64'], validate=True)
    require(target_row(after) == after and len(after.splitlines()) == 1 and after.endswith(b'\n'), 'Frozen QUEUE replacement must be one exact target row')
    cells = after.decode().split('|')
    require(cells[8].strip() == g['audited_outcome'] and cells[9].strip() == '1/5', 'Frozen target status/budget differs')
    if g['audited_outcome'] == 'claimed_solved':
        require(g['already_solved_gates'] is None and g['partial_gates'] is None, 'Multiple outcome paths selected')
        fields(g['claimed_solved_gates'], ('publication', 'tracker', 'whole_package'))
        for key, row in g['claimed_solved_gates'].items():
            check_pin(row)
            receipt = load(safe_path(row['path']))
            require(receipt.get('status') == 'PASS' and receipt.get('PR') == PR and receipt.get('reviewed_head') == HEAD and receipt.get('gate_kind') == key and receipt.get('ROOT_verified') is True and same(receipt.get('scope_interpretation'), g['scope_interpretation']) and receipt.get('accepted_as') == science['accepted_as'] and receipt.get('publication_DOI') == science['publication_DOI'] and same(receipt.get('frozen_packet'), p['packet']) and receipt.get('native_scientific_fields_sha256') == sha(canonical(science).encode()), 'Successful exact-scope/packet/science ' + key + ' gate absent')
        require(science['novelty_clearance'] is True and science['new_paper'] is True and science['tracker_append'] is True and type(science['publication_DOI']) is str and science['publication_DOI'].strip() and science['credited_prior_disposition'] is None and science['attributed_partial_disposition'] is None and cells[12].strip() == science['publication_DOI'], 'Claimed-solved publication/tracker identity differs')
    elif g['audited_outcome'] == 'already_solved':
        require(g['claimed_solved_gates'] is None and g['partial_gates'] is None, 'Multiple outcome paths selected')
        fields(g['already_solved_gates'], ('certified_credited_prior_disposition', 'no_new_paper', 'no_publication_action', 'no_tracker_append'))
        for key in ('no_new_paper', 'no_publication_action', 'no_tracker_append'): require(g['already_solved_gates'][key] is True, 'Already-solved no-paper path differs')
        row = g['already_solved_gates']['certified_credited_prior_disposition']; check_pin(row)
        receipt = load(safe_path(row['path']))
        require(receipt.get('status') == 'PASS' and receipt.get('PR') == PR and receipt.get('reviewed_head') == HEAD and receipt.get('ROOT_certified_credited_prior_disposition') is True and same(receipt.get('scope_interpretation'), g['scope_interpretation']) and receipt.get('accepted_as') == science['accepted_as'], 'Certified precise credited-prior disposition absent')
        require(science['novelty_clearance'] is False and science['new_paper'] is False and science['tracker_append'] is False and science['publication_DOI'] is None and science['credited_prior_disposition'] == row and science['attributed_partial_disposition'] is None and not cells[12].strip(), 'Already-solved no-paper scientific fields differ')
    else:
        require(g['claimed_solved_gates'] is None and g['already_solved_gates'] is None, 'Multiple outcome paths selected')
        fields(g['partial_gates'], ('certified_attributed_partial_disposition', 'no_novelty_clearance', 'no_new_paper', 'no_publication_action', 'no_tracker_append'))
        for key in ('no_novelty_clearance', 'no_new_paper', 'no_publication_action', 'no_tracker_append'):
            require(g['partial_gates'][key] is True, 'Attributed-partial no-paper/no-novelty path differs')
        row = g['partial_gates']['certified_attributed_partial_disposition']; check_pin(row)
        receipt = load(safe_path(row['path']))
        require(receipt.get('status') == 'PASS' and receipt.get('PR') == PR and receipt.get('reviewed_head') == HEAD and receipt.get('ROOT_certified_attributed_partial_disposition') is True and same(receipt.get('scope_interpretation'), g['scope_interpretation']) and receipt.get('accepted_as') == science['accepted_as'] and receipt.get('novelty_clearance') is False and receipt.get('no_prior_target_resolution_inferred') is True and receipt.get('new_paper') is False and receipt.get('publication_DOI') is None and receipt.get('tracker_append') is False and same(receipt.get('frozen_packet'), p['packet']), 'Certified exact interpreted partial disposition absent')
        require(science['novelty_clearance'] is False and science['new_paper'] is False and science['tracker_append'] is False and science['publication_DOI'] is None and science['credited_prior_disposition'] is None and science['attributed_partial_disposition'] == row and not cells[12].strip(), 'Partial cannot become solved/novel/published by inference')
    ready = load(safe_path(g['current_readiness_evidence']['path']))
    require(ready.get('status') == 'PASS' and ready.get('PR') == PR and ready.get('reviewed_head') == HEAD and ready.get('mathematics_validated') is True and ready.get('native_current_status') == g['audited_outcome'] and ready.get('original_readiness_preserved') is True and ready.get('original_budget') == '1/5' and type(ready.get('new_original_proof_turns')) is int and ready.get('new_original_proof_turns') == 0 and ready.get('novelty_clearance') is science['novelty_clearance'], 'Current separately bound readiness evidence differs')
    catalog_rows = [x for x in load(ROOT / 'unsolved_math_prioritization/catalog.json') if str(x['id']) == ID]
    require(len(catalog_rows) == 1 and ready.get('review_hash') == catalog_rows[0]['review_hash'] and same(ready.get('scope_interpretation'), g['scope_interpretation']), 'Current readiness source fingerprint/exact interpreted scope differs')
    require(type(p['checkpoint_files']) is list and p['checkpoint_files'], 'Explicit public-safe checkpoint allowlist missing')
    require(len(p['checkpoint_files']) == len({r['pin']['path'] for r in p['checkpoint_files']}), 'Duplicate public-safe checkpoint path')
    for row in p['checkpoint_files']:
        fields(row, ('pin', 'ROOT_certifies_public_safe', 'git_mode'))
        require(row['ROOT_certifies_public_safe'] is True, 'ROOT public-safe certification absent')
        require(row['git_mode'] in ('100644', '100755'), 'Frozen checkpoint Git mode absent')
        check_pin(row['pin']); public_safe(row['pin']['path'])
    return g, p, packet, science, pin(gate_path)

def public_safe(rel):
    require(rel.startswith(str(AUDIT.relative_to(ROOT)) + '/'), 'Checkpoint path outside PR73 audit')
    prohibited = ('/original/', '/current_sourcepair/', '/cache/', '/commands/', '/operations/', '/controller_receipts/')
    require(not any(x in rel for x in prohibited), 'Private raw/command/operational data cannot enter checkpoint')
    require(Path(rel).suffix.lower() in ('.md', '.json', '.py', '.txt'), 'Checkpoint suffix not public-safe')
    require(not any(x in Path(rel).name for x in ('ORIGINAL_AUTHENTICATION', 'BLOB_MANIFEST', 'DEEP_CUSTODY', 'SOURCEPAIR_AUTHENTICATION')), 'Private custody/source inventory excluded from checkpoint')

class Session:
    def __init__(self, phase, gate_pin):
        require(not sys.flags.optimize and sys.flags.ignore_environment and sys.flags.dont_write_bytecode, 'Invoke python3 -E -B without optimization')
        require(Path.cwd().resolve() == ROOT.resolve(), 'Actual operational controller cwd must be repository root')
        self.phase = phase
        self.dest = PREP / 'operations' / (phase + '_' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
        self.dest.mkdir(parents=True, exist_ok=False)
        self.commands = []
        self.gate_pin = gate_pin
        gate = load(safe_path(gate_pin['path']))
        plan = load(safe_path(gate['exact_plan']['path']))
        inputs = [gate_pin, gate['exact_plan'], gate['current_readiness_evidence'], *gate['bound_evidence'], *gate['bound_operators'], *plan['packet']]
        for row in inputs: check_pin(row)
        (self.dest / 'SOURCE_PRELAUNCH_SNAPSHOT.json').write_bytes(json_bytes(inputs))
        self.source_snapshot_pin = pin(self.dest / 'SOURCE_PRELAUNCH_SNAPSHOT.json')
        self.writer_ack_nonce = None
        (self.dest / 'CONTROLLER.json').write_bytes(json_bytes({'PID': os.getpid(), 'cwd': os.getcwd(), 'argv': sys.argv, 'UTC': now(), 'phase': phase, 'upstream_launcher_metadata': 'Not observable: the tool/shell prelaunch PID/argv/UTC is unavailable. No fabricated launcher metadata.', 'gate': gate_pin}))
        for name in ('native_common_v2.py', 'ROOT_native_integration_v2.py', 'ROOT_native_readback_v2.py'):
            (self.dest / ('PRELAUNCH_' + name)).write_bytes((PREP / name).read_bytes())
    def run(self, argv, allowed=(0,)):
        started = now()
        source_pins = [pin(PREP / x) for x in ('native_common_v2.py', 'ROOT_native_integration_v2.py', 'ROOT_native_readback_v2.py')]
        c = subprocess.Popen(argv, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = c.communicate()
        stem = '%03d' % (len(self.commands) + 1)
        (self.dest / (stem + '.stdout.bin')).write_bytes(out)
        (self.dest / (stem + '.stderr.bin')).write_bytes(err)
        row = {'PID': c.pid, 'cwd': str(ROOT), 'argv': argv, 'started_utc': started, 'finished_utc': now(), 'exit': c.returncode, 'source_prelaunch_pins': source_pins, 'bound_input_prelaunch_snapshot': self.source_snapshot_pin,
               'stdout': {'path': stem + '.stdout.bin', 'bytes': len(out), 'sha256': sha(out)}, 'stderr': {'path': stem + '.stderr.bin', 'bytes': len(err), 'sha256': sha(err)}}
        self.commands.append(row)
        (self.dest / 'ACTUAL_COMMANDS.json').write_bytes(json_bytes(self.commands))
        require(c.returncode in allowed, 'Child command failed')
        return out, c.returncode
    def git(self, *args):
        return self.run(['git', '--no-optional-locks', *args])[0]
    def pr(self):
        o = json.loads(self.run(['gh', 'pr', 'view', '73', '--repo', REPO, '--json', 'number,state,isDraft,headRefOid,headRefName,baseRefName,mergeCommit,mergedAt,title,body,url'])[0])
        require(o['number'] == PR and o['headRefOid'] == HEAD and o['headRefName'] == 'dot/math-2985' and o['baseRefName'] == 'main', 'Fresh PR exact identity differs')
        return o
    def finish(self, data):
        data.update({'status': 'PASS', 'phase': self.phase, 'UTC': now(), 'PR': PR, 'reviewed_head': HEAD, 'gate': self.gate_pin, 'actual_directory': str(self.dest.relative_to(ROOT)), 'actual_controller_PID': os.getpid(), 'actual_command_count': len(self.commands), 'actual_writer_ack_nonce': self.writer_ack_nonce, 'actual_writer_acknowledgment': pin(self.dest / 'ACKNOWLEDGED_WINDOW.json'), 'completion_scope': 'Only this operational phase; no overall-program completion conferred'})
        (self.dest / 'RECEIPT.json').write_bytes(json_bytes(data))
        print(json.dumps(data, indent=2))
        return pin(self.dest / 'RECEIPT.json')

def names0(b):
    return {x.decode() for x in b.split(b'\0') if x}
def check_remote_identity(s):
    allowed = {'https://github.com/AlecKriebel/Math.git', 'https://github.com/AlecKriebel/Math',
               'git@github.com:AlecKriebel/Math.git', 'ssh://git@github.com/AlecKriebel/Math.git'}
    for kind in ((), ('--push',)):
        urls = s.git('remote', 'get-url', *kind, '--all', 'origin').decode().splitlines()
        require(len(urls) == 1 and urls[0] in allowed, 'Canonical origin fetch/push repository identity differs')
def current_baseline(s):
    check_remote_identity(s)
    require(s.git('branch', '--show-current').strip() == b'main', 'Shared repository must stay on main')
    base = s.git('rev-parse', 'HEAD').decode().strip()
    remote = s.git('ls-remote', 'origin', 'refs/heads/main').decode().split()
    require(remote and remote[0] == base, 'Local/remote main differ')
    require(not s.git('diff', '--cached', '--name-only', '-z'), 'Shared index must be empty; preserve nonempty state and stop')
    flags = [x for x in s.git('ls-files', '-v', '-z').split(b'\0') if x]
    require(all(x.startswith(b'H ') for x in flags), 'Assume-unchanged/skip-worktree or nonordinary index flags present; preserve and stop')
    require(not (ROOT / '.git/MERGE_HEAD').exists(), 'Prior merge state exists')
    return base

class WriterWindow:
    def __init__(self, s, gate, current, owned, newer_than, required_nonce):
        self.s, self.owned = s, set(owned)
        require(ACK_REL not in self.owned and safe_path(ACK_REL).is_file(), 'Acknowledgment is coordination evidence, never an owned/staged native path')
        self.ack_bytes = ACK.read_bytes()
        self.ack_mode = ACK.lstat().st_mode
        w = json.loads(self.ack_bytes)
        require(w['shared_git_writes_paused'] is True and w['paused_for'] == TAG + ':' + s.phase, 'Actual fresh phase-specific shared-writer acknowledgment absent')
        require(w['dirty_tracked_bodies_modes_frozen_after_acknowledgement'] is True and type(w['all_staged_path_count']) is int and w['all_staged_path_count'] == 0 and w['owned_staged_paths'] == [], 'Actual dirty-body/mode/index freeze absent')
        require(w['local_main_at_pause'] == w['remote_main_at_pause'] == current, 'Writer acknowledgment baseline differs')
        require(timestamp(gate['minimum_writer_ack_utc']) <= timestamp(w.get('UTC', w.get('utc'))) <= timestamp(now()) and timestamp(w.get('UTC', w.get('utc'))) >= timestamp(newer_than), 'Writer acknowledgment is stale/future-dated; no checkpoint acknowledgment reuse')
        plan = load(safe_path(gate['exact_plan']['path']))
        require(type(required_nonce) is str and re.fullmatch('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', required_nonce) and w.get('ack_nonce') == required_nonce and w.get('execution_id') == plan['execution_id'] and w.get('ROOT_gate_sha256') == s.gate_pin['sha256'] and w.get('frozen_plan_sha256') == gate['exact_plan']['sha256'], 'Actual writer nonce/gate/frozen-plan binding absent')
        s.writer_ack_nonce = required_nonce
        self.current = current
        self.index = self.foreign_index()
        self.index_flags = self.foreign_index_flags()
        self.all_foreign = self.actual_foreign_inventory()
        self.dirty = names0(s.git('diff', '--name-only', '-z')) - self.owned
        actual_dirty = {r['path'] for r in self.all_foreign if not r['exists'] or r['git_blob_SHA1'] != r['index_blob_SHA1'] or bool(r['lstat_mode'] & 0o111) != (r['index_mode'] == '100755')}
        require(actual_dirty == self.dirty, 'Tracked worktree differs from index behind diff visibility; preserve and stop')
        self.bodies = {}
        for i, rel in enumerate(sorted(self.dirty)):
            p = safe_path(rel)
            if p.exists():
                require(p.is_file() and not p.is_symlink(), 'Foreign dirty path is not a regular file')
                b = p.read_bytes(); mode = p.lstat().st_mode
                private = s.dest / ('FOREIGN_%03d.bin' % i); private.write_bytes(b)
                self.bodies[rel] = {'exists': True, 'lstat_mode': mode, 'bytes': len(b), 'sha256': sha(b), 'private_path': str(private.relative_to(ROOT))}
            else:
                require(not p.is_symlink(), 'Foreign dangling symlink unsupported')
                self.bodies[rel] = {'exists': False}
        (s.dest / 'ACKNOWLEDGED_WINDOW.json').write_bytes(self.ack_bytes)
        (s.dest / 'FOREIGN_INDEX.bin').write_bytes(self.index)
        (s.dest / 'FOREIGN_INDEX_FLAGS.bin').write_bytes(self.index_flags)
        (s.dest / 'FOREIGN_TRACKED_WHOLE_INVENTORY.json').write_bytes(json_bytes(self.all_foreign))
        (s.dest / 'FOREIGN_BODIES.json').write_bytes(json_bytes(self.bodies))
    def foreign_index(self):
        return b'\0'.join(x for x in self.s.git('ls-files', '--stage', '-z').split(b'\0') if x and x.split(b'\t', 1)[1].decode() not in self.owned)
    def foreign_index_flags(self):
        values = [x for x in self.s.git('ls-files', '-v', '-z').split(b'\0') if x]
        foreign = [x for x in values if x[2:].decode() not in self.owned]
        require(all(x.startswith(b'H ') for x in foreign), 'Nonordinary/assume-unchanged/skip-worktree foreign index flag appeared')
        return b'\0'.join(foreign)
    def actual_foreign_inventory(self):
        result = []
        for item in self.foreign_index().split(b'\0'):
            if not item: continue
            meta, path = item.split(b'\t', 1); mode, digest, stage = meta.decode().split(); rel = path.decode()
            require(mode in ('100644', '100755') and stage == '0' and digest != '0' * 40, 'Unsupported foreign index type/stage/intent-to-add state')
            p = safe_path(rel)
            row = {'path': rel, 'index_mode': mode, 'index_blob_SHA1': digest, 'exists': p.exists()}
            if p.exists():
                require(p.is_file() and not p.is_symlink(), 'Foreign tracked body is not a regular file')
                b = p.read_bytes(); row.update({'lstat_mode': p.lstat().st_mode, 'bytes': len(b), 'sha256': sha(b), 'git_blob_SHA1': git_blob(b)})
            else: require(not p.is_symlink(), 'Foreign tracked dangling symlink unsupported')
            result.append(row)
        return result
    def check(self):
        require(ACK.is_file() and not ACK.is_symlink() and ACK.lstat().st_mode == self.ack_mode and ACK.read_bytes() == self.ack_bytes, 'Actual current writer acknowledgment body/mode changed within phase')
        check_remote_identity(self.s)
        require(self.s.git('branch', '--show-current').strip() == b'main' and self.s.git('rev-parse', 'HEAD').decode().strip() == self.current, 'Shared branch/head changed')
        require(self.foreign_index() == self.index and self.foreign_index_flags() == self.index_flags and same(self.actual_foreign_inventory(), self.all_foreign) and names0(self.s.git('diff', '--name-only', '-z')) - self.owned == self.dirty, 'Foreign whole tracked inventory/index flags/dirty scope changed')
        for rel, row in self.bodies.items():
            p = safe_path(rel)
            if row['exists']:
                require(p.is_file() and not p.is_symlink() and p.lstat().st_mode == row['lstat_mode'] and p.read_bytes() == safe_path(row['private_path']).read_bytes(), 'Foreign dirty whole body/mode changed')
            else:
                require(not p.exists() and not p.is_symlink(), 'Foreign deleted body recreated')
    def restore_foreign_after_merge(self):
        """Restore the captured foreign dirty bodies only after index/scope guards."""
        require(ACK.read_bytes() == self.ack_bytes and self.foreign_index() == self.index, 'Writer/index changed; restoration unsafe')
        # A foreign change is not assumed to be merge output: stop rather than
        # overwrite an unexpected write, even if the writer acknowledgment stayed.
        self.check()
        for rel, row in self.bodies.items():
            p = safe_path(rel)
            if rel == ACK_REL:
                # Coordination evidence remains read-only within this phase.
                continue
            if row['exists']:
                require(not p.is_symlink(), 'Foreign symlink appeared; stop')
                p.write_bytes(safe_path(row['private_path']).read_bytes())
                p.chmod(stat.S_IMODE(row['lstat_mode']))
            elif p.exists():
                require(p.is_file() and not p.is_symlink(), 'Foreign deletion restoration unsafe')
                p.unlink()
        self.check()

def check_original_git(s, commit, files, native=False):
    for row in files:
        b = s.git('show', commit + ':' + row['path'])
        require(len(b) == row['bytes'] and sha(b) == row['sha256'] and git_blob(b) == row['git_blob_SHA1'], 'Original commit body/blob changed')
        require(s.git('ls-tree', commit, '--', row['path']).decode().split()[:3] == [row['mode'], 'blob', row['git_blob_SHA1']], 'Original committed Git mode differs')
        if native:
            p = safe_path(row['path'])
            require(p.is_file() and not p.is_symlink() and p.read_bytes() == (AUTH / row['retained_path']).read_bytes() and stat.S_IMODE(p.stat().st_mode) == 0o644, 'Original native byte/mode differs')
    require(not safe_path(PREFIX + '/status.json').exists() if native else True, 'status.json was invented')

def check_queue_plan(before, after, plan):
    old = target_row(before)
    require(sha(old) == plan['queue_before_row_sha256'], 'Frozen current target-row baseline differs')
    new = base64.b64decode(plan['queue_after_row_base64'], validate=True)
    require(after == before.replace(old, new, 1), 'QUEUE replacement changed other rows/bytes')
    a, b = old.decode().split('|'), new.decode().split('|')
    require(all(a[i] == b[i] for i in range(14) if i not in (8, 9, 11, 12)), 'Frozen row changed unapproved target cells')

def read_receipt(row, phase, gate_pin):
    check_pin(row)
    r = load(safe_path(row['path']))
    require(r['status'] == 'PASS' and r['phase'] == phase and r['PR'] == PR and r['reviewed_head'] == HEAD and r['gate'] == gate_pin, 'Predecessor phase receipt differs')
    require(safe_path(r['actual_directory']).resolve().is_relative_to((PREP / 'operations').resolve()), 'Predecessor evidence directory escaped')
    d = safe_path(r['actual_directory'])
    require(safe_path(row['path']).resolve() == (d / 'RECEIPT.json').resolve(), 'Predecessor receipt is not in its actual evidence directory')
    controller = load(d / 'CONTROLLER.json')
    require(controller['phase'] == phase and controller['gate'] == gate_pin and controller['PID'] == r['actual_controller_PID'] and controller['cwd'] == str(ROOT), 'Predecessor actual controller metadata differs')
    require(type(controller['argv']) is list and len(controller['argv']) >= 2 and controller['argv'][1] == phase and timestamp(controller['UTC']) <= timestamp(r['UTC']), 'Predecessor actual argv/time differs')
    g = load(safe_path(gate_pin['path']))
    approved = {x['path']: x for x in g['bound_operators']}
    snapshots = []
    for name in ('native_common_v2.py', 'ROOT_native_integration_v2.py', 'ROOT_native_readback_v2.py'):
        b = (d / ('PRELAUNCH_' + name)).read_bytes()
        rel = str((PREP / name).relative_to(ROOT))
        require(rel in approved and len(b) == approved[rel]['bytes'] and sha(b) == approved[rel]['sha256'], 'Predecessor executed-source snapshot differs from ROOT-approved operator')
        snapshots.append(approved[rel])
    commands = load(d / 'ACTUAL_COMMANDS.json')
    source_snapshot = load(d / 'SOURCE_PRELAUNCH_SNAPSHOT.json')
    plan = load(safe_path(g['exact_plan']['path']))
    expected_inputs = [gate_pin, g['exact_plan'], g['current_readiness_evidence'], *g['bound_evidence'], *g['bound_operators'], *plan['packet']]
    require(same(source_snapshot, expected_inputs), 'Predecessor full-input prelaunch snapshot differs from frozen gate/plan')
    source_snapshot_pin = pin(d / 'SOURCE_PRELAUNCH_SNAPSHOT.json')
    require(type(commands) is list and commands and type(r['actual_command_count']) is int and len(commands) == r['actual_command_count'], 'Predecessor complete command-count evidence absent')
    for i, command in enumerate(commands, start=1):
        require(command['cwd'] == str(ROOT) and type(command['PID']) is int and command['PID'] > 0 and type(command['argv']) is list and command['argv'] and all(type(x) is str for x in command['argv']), 'Predecessor actual child cwd/PID/argv differs')
        require(timestamp(controller['UTC']) <= timestamp(command['started_utc']) <= timestamp(command['finished_utc']) <= timestamp(r['UTC']), 'Predecessor command UTC interval differs')
        require(type(command['exit']) is int and command['exit'] in (0, 1, 128) and same(command['source_prelaunch_pins'], snapshots) and command['bound_input_prelaunch_snapshot'] == source_snapshot_pin, 'Predecessor command exit/full-input source prelaunch pins differ')
        for stream in ('stdout', 'stderr'):
            entry = command[stream]
            require(entry['path'] == '%03d.%s.bin' % (i, stream), 'Predecessor fullstream path differs')
            b = (d / entry['path']).read_bytes()
            require(len(b) == entry['bytes'] and sha(b) == entry['sha256'], 'Predecessor fullstream bytes/hash differ')
    ack = load(d / 'ACKNOWLEDGED_WINDOW.json')
    check_pin(r['actual_writer_acknowledgment'])
    require(r['actual_writer_acknowledgment'] == pin(d / 'ACKNOWLEDGED_WINDOW.json'), 'Predecessor retained actual acknowledgment whole-byte pin differs')
    require(ack['paused_for'] == TAG + ':' + phase and ack['ROOT_gate_sha256'] == gate_pin['sha256'] and ack['frozen_plan_sha256'] == g['exact_plan']['sha256'] and ack['execution_id'] == plan['execution_id'], 'Predecessor actual writer gate/plan/phase identity differs')
    require(ack['ack_nonce'] == r['actual_writer_ack_nonce'] and '--writer-ack-nonce' in controller['argv'] and controller['argv'][controller['argv'].index('--writer-ack-nonce') + 1] == ack['ack_nonce'], 'Predecessor requested/actual writer nonce differs')
    require(ack['shared_git_writes_paused'] is True and ack['dirty_tracked_bodies_modes_frozen_after_acknowledgement'] is True and type(ack['all_staged_path_count']) is int and ack['all_staged_path_count'] == 0 and ack['owned_staged_paths'] == [] and ack['local_main_at_pause'] == ack['remote_main_at_pause'], 'Predecessor actual writer freeze/index declaration differs')
    require(timestamp(g['minimum_writer_ack_utc']) <= timestamp(ack.get('UTC', ack.get('utc'))) <= timestamp(controller['UTC']), 'Predecessor actual acknowledgment UTC differs from gate/controller interval')
    baseline_commands = [c for c in commands if c['argv'] == ['git', '--no-optional-locks', 'rev-parse', 'HEAD']]
    require(baseline_commands and (d / baseline_commands[0]['stdout']['path']).read_bytes().decode().strip() == ack['local_main_at_pause'], 'Predecessor actual acknowledgment base differs from observed pre-phase HEAD')
    return r

def verify_current_source(s, source):
    identity = sourcepair(ROOT / 'unsolved_math_prioritization', source)
    rows = [x for x in load(ROOT / 'unsolved_math_prioritization/catalog.json') if str(x['id']) == ID]
    require(len(rows) == 1 and rows[0]['review_hash'] == identity['review_hash_SQL_normalized_only'], 'Current catalog fingerprint differs')
    import ast
    tree = ast.parse((ROOT / 'unsolved_math_prioritization/queue.py').read_bytes())
    definitions = [n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'STATES' for t in n.targets)]
    require(len(definitions) == 1 and 'partial' in ast.literal_eval(definitions[0].value), 'Native partial status registration changed')
    require(load(ROOT / 'unsolved_math_prioritization/policy.json')['turn_limit'] == 5, 'Current native attempt-limit policy differs')
    return identity

def event_identity(gate_pin, plan_pin, merge, status):
    return sha(canonical({'schema': 'pr73-present-day-native-import-id/v2', 'PR': PR, 'problem_id': ID, 'reviewed_head': HEAD,
                          'gate_sha256': gate_pin['sha256'], 'plan_sha256': plan_pin['sha256'], 'merge_commit': merge, 'status': status}).encode())

def insert_state_key(original, state, event):
    require(type(state) is dict and ID not in state, 'Current native target state already exists')
    end = len(original.rstrip()) - 1
    require(original[end:end+1] == b'}', 'Current state object delimiter differs')
    prefix = original[:end]
    cut = len(prefix.rstrip())
    pretty = json.dumps(event, ensure_ascii=False, sort_keys=True, indent=2).replace('\n', '\n  ').encode()
    insertion = (b',' if state else b'') + b'\n  ' + json.dumps(ID).encode() + b': ' + pretty
    result = prefix[:cut] + insertion + prefix[cut:] + original[end:]
    require(same({k: v for k, v in json.loads(result).items() if k != ID}, state), 'Foreign state entries changed')
    # Delete exactly the inserted segment to independently recover every original byte.
    require(result[:cut] + result[cut + len(insertion):] == original, 'Original state byte preservation failed')
    return result
