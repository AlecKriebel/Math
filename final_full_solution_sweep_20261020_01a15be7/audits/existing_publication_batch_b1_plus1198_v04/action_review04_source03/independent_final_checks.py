"""Read-only final exact checks of complete native policy and own evidence."""
from pathlib import Path
import copy, datetime, gzip, hashlib, json, stat, types
D = Path(__file__).resolve().parent
A = D.parent/'actor01'
S = A/'private/sourceprep03'

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def canonical(value):
    # Independent comparison preserves JSON Boolean/integer/float/signed-zero.
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode()

def file_from(inv, relative):
    entry = next(x for x in inv['files'] if x['relative'] == relative)
    raw = gzip.decompress(Path(entry['blob']).read_bytes())
    need(len(raw) == entry['bytes'] and sha(raw) == entry['sha256'], 'Custody entry mismatch')
    return raw

core = types.ModuleType('independent_readonly_core')
source = (S/'ops_core.py').read_bytes()
need(sha(source) == '3029474e348ca39c30a37b7d11cd1da2f4f7e985fa71e7c42fb17df4bfd65d96',
     'Core drift')
exec(compile(source, str(S/'ops_core.py'), 'exec', optimize=0), core.__dict__)
plan = json.loads((S/'PROPOSAL.json').read_text())
shared = json.loads((S/'SHARED_INPUTS.json').read_text())
expected = json.loads(Path(shared[plan['items'][-1]['expected_full_record_path']]['path']).read_text())
passed = []

def accepts(name, current):
    core.compare_1198_record(expected, current)
    passed.append(name)

def rejects(name, current):
    try:
        core.compare_1198_record(expected, current)
    except core.GateError:
        passed.append(name)
        return
    raise RuntimeError('False native policy variant accepted: '+name)

for key in ['views', 'unique_views', 'version_views', 'version_unique_views']:
    current = copy.deepcopy(expected)
    current['stats'][key] += 7
    accepts('allow_exact_integer_increase_'+key, current)
    for label, value in [('Boolean', False), ('float', float(expected['stats'][key])),
                         ('decrease', expected['stats'][key]-1)]:
        current = copy.deepcopy(expected)
        current['stats'][key] = value
        rejects('reject_'+label+'_'+key, current)
current = copy.deepcopy(expected)
for key in ['views', 'unique_views', 'version_views', 'version_unique_views']:
    current['stats'][key] += 3
accepts('allow_all_four_exact_counters', current)
current = copy.deepcopy(expected)
current['stats']['unknown_new_counter'] = 0
rejects('reject_unknown_stats_field', current)
current = copy.deepcopy(expected)
del current['stats']['views']
rejects('reject_missing_counter', current)
current = copy.deepcopy(expected)
current['submitted'] = 1
rejects('reject_top_level_Boolean_integer_coercion', current)
current = copy.deepcopy(expected)
current['files'] = list(reversed(current['files']))
rejects('reject_native_file_order_change', current)
current = copy.deepcopy(expected)
current['unknown_top_level'] = None
rejects('reject_new_unknown_top_level_field', current)
need(not core.typed_equal(False, 0) and not core.typed_equal(1, 1.0)
     and not core.typed_equal(-0.0, 0.0), 'Recursive JSON type/signed-zero failure')
passed.append('typed_Boolean_integer_float_signed_zero')
for text in ['{"same":1,"same":2}', '{"value":NaN}']:
    try:
        core.strict_json(text)
    except core.GateError:
        passed.append('reject_json_'+sha(text.encode())[:12])
    else:
        raise RuntimeError('Noncanonical JSON accepted')

results = json.loads((D/'RESULTS.json').read_text())
need(results['status'] == 'PASS_REVIEW_CONTROLS' and results['completed'] == 16, 'Incomplete own controls')
old_rows = 0
attempts = 0
applications = 0
for case in results['results']:
    c = case['custody']
    path = Path(c['inventory'])
    need(sha(path.read_bytes()) == c['inventory_sha256'], 'Own inventory drift')
    inv = json.loads(path.read_text())
    data = json.loads(file_from(inv, 'CASE_RESULT.json'))
    need(data['outcome'] == 'PASS' and data['issues'] == [] and not data['external_attempts'],
         'Own control has a failure')
    need(not data['provider_infrastructure_errors'] and not data['unchecked_bytes_selected'],
         'Infrastructure/source selection failure')
    need(all(x['optimize'] == 0 for x in data['compiled']), 'Wrong compile policy')
    attempts += data['simulated_append_attempts']
    applications += data['simulated_applications']
    if data['actor_status'] == 'verified':
        before_v = json.loads(file_from(inv, 'mirror/private_action/action01/BEFORE_VALUE.json'))
        before_f = json.loads(file_from(inv, 'mirror/private_action/action01/BEFORE_FORMULA.json'))
        after_v = json.loads(file_from(inv, 'mirror/private_action/action01/AFTER_VALUE.json'))
        after_f = json.loads(file_from(inv, 'mirror/private_action/action01/AFTER_FORMULA.json'))
        before_m = json.loads(file_from(inv, 'mirror/private_action/action01/BEFORE_FULL_METADATA.json'))
        after_m = json.loads(file_from(inv, 'mirror/private_action/action01/AFTER_FULL_METADATA.json'))
        need(canonical(before_v) == canonical(before_f) and canonical(after_v) == canonical(after_f),
             'Full dual raw responses not equal')
        need(canonical(before_m) == canonical(after_m), 'Full raw metadata changed')
        rows = before_v['valueRanges'][0]['valueRange']['values']
        need(len(rows) == 194, 'Wrong then-current old-row population')
        target = copy.deepcopy(before_v)
        target['valueRanges'][0]['valueRange']['values'] = rows + [i['row'] for i in plan['items']]
        need(canonical(after_v) == canonical(target), 'Any raw metadata/old typed cell/new row mismatch')
        old_rows = len(rows)

for e in json.loads((D/'INPUT_PINS.json').read_text())['inputs']:
    p = Path(e['path'])
    raw = p.read_bytes()
    s = p.stat()
    need(len(raw) == e['bytes'] and sha(raw) == e['sha256']
         and stat.S_IMODE(s.st_mode) == e['mode'] and s.st_mtime_ns == e['mtime_ns'],
         'An original reviewed source/input changed')
need(not (S/'private_action').exists() and not (S/'private_readonly').exists(),
     'Production action namespace created')
need(not list((D/'private/active').iterdir()), 'Own active/partial parser case remains')
report = {'at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'status': 'INDEPENDENT_POLICY_AND_OWN_EVIDENCE_PASS',
          'native_and_JSON_policy_checks': passed, 'native_and_JSON_policy_check_count': len(passed),
          'own_actual_parser_cases': 16, 'own_simulated_append_attempts': attempts,
          'own_simulated_applications': applications, 'typed_old_rows_verified': old_rows,
          'all43columns_unknown_raw_metadata_and_FORMULA_preserved': True,
          'original_inputs_byte_mode_nsmtime_preserved': True,
          'real_external_attempts': 0, 'real_service_writes': 0,
          'root_action_accepted': False, 'publication_ready': False}
out = D/'FINAL_CHECKS.json'
with out.open('x') as f:
    json.dump(report, f, indent=2)
    f.write('\n')
print(json.dumps(report, indent=2))
