#!/usr/bin/env python3
"""Bounded independent transport review; no native service commands or credentials.

All hostile candidates exist in memory. Only this review folder receives outputs.
Exit 3 means the narrow gate rejected a candidate; exit 1 means a review failure.
"""
import argparse
import ast
import copy
import datetime
import hashlib
import html
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import socket
import stat
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
F = HERE.parent
AUDIT = F.parent
D = AUDIT.parent.parent
REPO = D.parent
NATIVE = REPO / 'zenodo_deposit_tool/zenodo.py'
OLD = AUDIT / 'preprint_v1_0/zenodo-deposit.json'
WIRE = F / 'zenodo-deposit-html-transport.json'
FROM = ' n >= 1,'
TO = ' n &gt;= 1,'
EXPECTED_ID = 23431313

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def fail(message):
    raise ValueError(message)

def need(condition, message):
    if not condition:
        fail(message)

def no_duplicates(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, 'duplicate JSON key: ' + key)
        out[key] = value
    return out

def read(path):
    return json.loads(path.read_text(), object_pairs_hook=no_duplicates)

def canon(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def digest(path, algorithm='sha256'):
    h = hashlib.new(algorithm)
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def identity(path):
    return {'bytes': path.stat().st_size, 'sha256': digest(path)}

class ExactHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.events = []

    def text(self, value):
        if self.events and self.events[-1][0] == 'text':
            self.events[-1] = ('text', self.events[-1][1] + value)
        else:
            self.events.append(('text', value))

    def handle_starttag(self, tag, attrs):
        self.events.append(('start', self.get_starttag_text(), tag, attrs))

    def handle_startendtag(self, tag, attrs):
        self.events.append(('empty', self.get_starttag_text(), tag, attrs))

    def handle_endtag(self, tag):
        self.events.append(('end', tag))

    def handle_data(self, value):
        self.text(value)

    def handle_entityref(self, name):
        self.text(html.unescape('&' + name + ';'))

    def handle_charref(self, name):
        self.text(html.unescape('&#' + name + ';'))

    def handle_comment(self, value):
        self.events.append(('comment', value))

    def handle_decl(self, value):
        self.events.append(('declaration', value))

    def handle_pi(self, value):
        self.events.append(('pi', value))

def html_events(value):
    parser = ExactHTML()
    parser.feed(value)
    parser.close()
    return parser.events

ORIGINAL = read(F / 'original_manifest.json')
CONFIG = read(F / 'original_config.json')
REMOTE = read(F / 'REMOTE_SELECTED_BEFORE_BINDING.json')
PROTECTED = read(F / 'PROTECTED_BEFORE_PINS.json')
INPUTS = sorted(p for p in F.iterdir() if p.is_file())

def protected_snapshot():
    rows = []
    need(len(PROTECTED) == 163, 'protected row count')
    for expected in PROTECTED:
        path = Path(expected['absolute_path']) if 'absolute_path' in expected else AUDIT / expected['path']
        row = {'path': str(path), **identity(path)}
        if 'mode' in expected:
            row['mode'] = stat.S_IMODE(path.stat().st_mode)
        row['matches'] = all(row[k] == expected[k] for k in ['bytes', 'sha256'] + (['mode'] if 'mode' in expected else []))
        rows.append(row)
    need(len({r['path'] for r in rows}) == 163, 'duplicate protected path')
    need(all(r['matches'] for r in rows), 'protected row changed')
    return rows

def file_binding(actual, expected):
    need(canon(actual) == canon(expected), 'canonical file path/name/size/SHA256/MD5 binding differs')

def expected_files():
    return [
        {'path': str((D / row['path']).resolve()), 'name': row['name'],
         'bytes': row['bytes'], 'sha256': row['sha256'],
         'md5': digest((D / row['path']).resolve(), 'md5')}
        for row in CONFIG['files']
    ]

def acceptance(candidate, selected=REMOTE):
    need(set(candidate) == {'metadata', 'files'}, 'top-level keys differ')
    expected_metadata = copy.deepcopy(ORIGINAL['metadata'])
    old = expected_metadata['description']
    need(old.count(FROM) == 1 and TO not in old, 'baseline exact one occurrence')
    expected_metadata['description'] = old.replace(FROM, TO, 1)
    need(canon(candidate['metadata']) == canon(expected_metadata), 'metadata differs from single authorized replacement')
    need(html_events(old) == html_events(candidate['metadata']['description']), 'HTML event semantics differ')
    need(re.findall(r'<[^>]*>', old) == re.findall(r'<[^>]*>', candidate['metadata']['description']), 'raw HTML tags/attributes differ')
    need(len(candidate['files']) == 2, 'file count differs')
    actual = []
    for item in candidate['files']:
        need(set(item) == {'path', 'name'}, 'file entry keys differ')
        path = (WIRE.parent / item['path']).resolve()
        actual.append({'path': str(path), 'name': item['name'], **identity(path), 'md5': digest(path, 'md5')})
    file_binding(actual, expected_files())
    need(type(selected['id']) is int and selected['id'] == EXPECTED_ID, 'remote ID differs')
    need(selected['submitted'] is False, 'captured remote is not draft')
    need(canon(selected['metadata']) == canon(candidate['metadata']), 'selected remote metadata differs')
    remote_files = selected['files']
    need(len(remote_files) == 2, 'remote file count differs')
    need(len({r['filename'] for r in remote_files}) == 2, 'duplicate remote file')
    remote_map = {r['filename']: r for r in remote_files}
    for item in actual:
        rf = remote_map[item['name']]
        need(type(rf['filesize']) is int and rf['filesize'] == item['bytes'], 'remote size differs')
        need(rf['checksum'] == item['md5'], 'remote MD5 differs')
        need('/23431313/' in rf['links']['self'] and '/23431313/' in rf['links']['download'], 'remote asset URL ID differs')
    return actual

def generator_acceptance(proposed):
    original = (F / 'original_prepare_service_configs.py').read_text()
    plan = read(F / 'GENERATOR_PATH_UPDATE_PLAN.json')
    need(original.count(plan['from']) == 1, 'generator baseline not unique')
    need(proposed == original.replace(plan['from'], plan['to'], 1), 'generator differs beyond one authorized literal')
    need(hashlib.sha256(original.encode()).hexdigest() == plan['original_sha256'], 'generator original SHA differs')
    need(hashlib.sha256(proposed.encode()).hexdigest() == plan['proposed_sha256'], 'generator proposal SHA differs')
    actual = D / 'service_resume_20261016/prepare_service_configs.py'
    need(actual.read_text() == original, 'operative generator changed before adoption')
    def table(source):
        tree = ast.parse(source)
        matches = [n.value for n in tree.body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == 'manifest_paths' for t in n.targets)]
        need(len(matches) == 1, 'generator table ambiguity')
        return ast.literal_eval(matches[0])
    a, b = table(original), table(proposed)
    need(len(a) == len(b) == 13, 'generator table count differs')
    need(set(a) == set(b) and [k for k in a if a[k] != b[k]] == [1094], 'generator changed another PR entry')
    return {'operative_generator': str(actual), 'operative_identity': identity(actual),
            'proposed_identity': identity(F / 'proposed_prepare_service_configs.py'),
            'entries': 13, 'changed_entries': [1094], 'all_other_bytes_identical': True,
            'executed_generator': False,
            'current_final_authority_1094': read(D / 'STATE.json').get('current_final_authorities', {}).get('1094'),
            'adoption_requirement': 'Bind STATE.current_final_authorities[1094] to the new external seal before any later regeneration.'}

CASES = [
    'positive', 'changed_inequality', 'double_escape', 'numeric_entity_equivalent_but_unapproved',
    'changed_tag', 'added_attribute', 'added_link', 'changed_link_target', 'removed_paragraph',
    'extra_text', 'changed_notes', 'changed_creator', 'extra_metadata', 'missing_metadata',
    'wrong_file_path', 'wrong_file_name', 'extra_file', 'extra_file_binding_key', 'reordered_files',
    'binding_wrong_sha256', 'binding_wrong_size', 'binding_wrong_canonical_path',
    'remote_wrong_id', 'remote_published', 'remote_changed_metadata', 'remote_wrong_checksum',
    'remote_extra_file', 'remote_wrong_asset_url', 'duplicate_json_key',
    'generator_changed_logic', 'generator_changed_other_pr', 'generator_wrong_1094_path',
]

def case(name):
    if name.startswith('generator_'):
        proposed = (F / 'proposed_prepare_service_configs.py').read_text()
        if name == 'generator_changed_logic': proposed = proposed.replace('count>=2', 'count>=1', 1)
        elif name == 'generator_changed_other_pr': proposed = proposed.replace("1097:'preprint_v1_0/zenodo-deposit.json'", "1097:'changed/zenodo-deposit.json'", 1)
        elif name == 'generator_wrong_1094_path': proposed = proposed.replace("1094:'publication_transport_20261017/zenodo-deposit-html-transport.json'", "1094:'preprint_v1_0/zenodo-deposit.json'", 1)
        generator_acceptance(proposed)
        return
    candidate = copy.deepcopy(read(WIRE))
    selected = copy.deepcopy(REMOTE)
    desc = candidate['metadata']['description']
    if name == 'changed_inequality': candidate['metadata']['description'] = desc.replace(' n &gt;= 1,', ' n &gt; 1,')
    elif name == 'double_escape': candidate['metadata']['description'] = desc.replace('&gt;', '&amp;gt;')
    elif name == 'numeric_entity_equivalent_but_unapproved': candidate['metadata']['description'] = desc.replace('&gt;', '&#62;')
    elif name == 'changed_tag': candidate['metadata']['description'] = desc.replace('<p>', '<div>', 1)
    elif name == 'added_attribute': candidate['metadata']['description'] = desc.replace('<p>', '<p title="n &gt;= 1,">', 1)
    elif name == 'added_link': candidate['metadata']['description'] = desc.replace('This note', '<a href="https://example.invalid/">This note</a>', 1)
    elif name == 'changed_link_target': candidate['metadata']['description'] = desc.replace('<p>', '<p><a href="https://example.invalid/changed">source</a>', 1)
    elif name == 'removed_paragraph': candidate['metadata']['description'] = desc.replace('<p>', '', 1)
    elif name == 'extra_text': candidate['metadata']['description'] = desc + ' '
    elif name == 'changed_notes': candidate['metadata']['notes'] += ' Published.'
    elif name == 'changed_creator': candidate['metadata']['creators'][0]['orcid'] = '0000-0000-0000-0000'
    elif name == 'extra_metadata': candidate['metadata']['unknown'] = 'x'
    elif name == 'missing_metadata': del candidate['metadata']['notes']
    elif name == 'wrong_file_path': candidate['files'][0]['path'] = '../preprint_v1_0/kit/paper.tex'
    elif name == 'wrong_file_name': candidate['files'][0]['name'] = 'other.pdf'
    elif name == 'extra_file': candidate['files'].append(copy.deepcopy(candidate['files'][0]))
    elif name == 'extra_file_binding_key': candidate['files'][0]['sha256'] = '0' * 64
    elif name == 'reordered_files': candidate['files'].reverse()
    elif name.startswith('binding_wrong_'):
        actual = copy.deepcopy(expected_files())
        key = {'binding_wrong_sha256': 'sha256', 'binding_wrong_size': 'bytes', 'binding_wrong_canonical_path': 'path'}[name]
        actual[0][key] = {'sha256': '0' * 64, 'bytes': actual[0]['bytes'] + 1, 'path': str(HERE / 'paper.pdf')}[key]
        file_binding(actual, expected_files())
        return
    elif name == 'remote_wrong_id': selected['id'] += 1
    elif name == 'remote_published': selected['submitted'] = True
    elif name == 'remote_changed_metadata': selected['metadata']['description'] += ' '
    elif name == 'remote_wrong_checksum': selected['files'][0]['checksum'] = '0' * 32
    elif name == 'remote_extra_file': selected['files'].append(copy.deepcopy(selected['files'][0]))
    elif name == 'remote_wrong_asset_url': selected['files'][0]['links']['download'] = 'https://zenodo.org/api/records/23431314/draft/files/paper.pdf/content'
    elif name == 'duplicate_json_key':
        json.loads('{"metadata":{},"metadata":{"x":1},"files":[]}', object_pairs_hook=no_duplicates)
        return
    elif name != 'positive': fail('unknown test case')
    acceptance(candidate, selected)

def native_checks():
    # Deny accidental use of the network. No credential lookup is permitted.
    def denied(*args, **kwargs):
        raise AssertionError('network/credential access forbidden in this local review')
    socket.create_connection = denied
    socket.socket.connect = denied
    spec = importlib.util.spec_from_file_location('reviewed_native', NATIVE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.token_for = denied
    module.doi_status = lambda doi: {'status': 'not_assigned' if doi is None else 'local_simulation_only'}
    md, files = module.load_manifest(WIRE.resolve())
    module.validate_record(REMOTE, EXPECTED_ID)
    normalization = module.verify(REMOTE, md, files)
    need(normalization == [], 'native wire verify has unexpected normalization')
    try:
        module.verify(REMOTE, ORIGINAL['metadata'], files)
    except module.DepositError as exc:
        original_rejection = str(exc)
        need("'description'" in original_rejection, 'original rejection is not description')
    else:
        fail('original metadata unexpectedly passes strict native verify')
    intended = {'manifest': str(WIRE.resolve()), 'environment': 'production', 'id': EXPECTED_ID}
    module.local_state = lambda path, env: (module.state_path(path, env), intended)
    calls = []
    receipts = []
    module.save_state = lambda path, value: receipts.append({'path': str(path), 'id': value['id'], 'publication': value.get('publication', {}).get('state')})

    class FakeClient:
        published = False
        publish_error = False
        def get(self, deposit_id):
            calls.append(['GET', deposit_id])
            result = copy.deepcopy(REMOTE)
            result['submitted'] = self.published
            return result
        def create(self, *args): denied()
        def upload(self, *args): denied()
        def update(self, *args): denied()
        def publish(self, deposit_id):
            calls.append(['PUBLISH_SIMULATED', deposit_id])
            self.published = True
            if self.publish_error:
                raise module.DepositError('simulated response lost after success')

    client = FakeClient()
    args = argparse.Namespace(command='inspect', manifest=WIRE, sandbox=False, check_doi=False)
    inspect_result = module.run(args, client)
    need(calls == [['GET', EXPECTED_ID]], 'native inspect mutated or changed ID')
    need(inspect_result['state'] == 'ready_to_publish', 'simulated inspect state')
    inspect_calls = calls.copy()
    calls.clear()
    args.command = 'publish'
    args.confirm_id = EXPECTED_ID + 1
    try:
        module.run(args, client)
    except module.DepositError as exc:
        wrong_confirmation = str(exc)
    else:
        fail('wrong publication confirmation accepted')
    need(calls == [['GET', EXPECTED_ID]], 'wrong confirmation attempted publication')
    calls.clear()
    args.confirm_id = EXPECTED_ID
    published = module.run(args, client)
    expected_calls = [['GET', EXPECTED_ID], ['PUBLISH_SIMULATED', EXPECTED_ID], ['GET', EXPECTED_ID]]
    need(calls == expected_calls and published['state'] == 'published', 'same-ID single simulated publication failed')
    publish_calls = calls.copy()
    calls.clear()
    already = module.run(args, client)
    need(calls == [['GET', EXPECTED_ID]] and already['already_published'], 'published rerun simulated POST repeated')
    rerun_calls = calls.copy()
    calls.clear()
    client.published = False
    client.publish_error = True
    recovered = module.run(args, client)
    need(calls == expected_calls and recovered['recovered_after_publish_error'], 'ambiguous simulated publish repeated POST')
    return {'wire_verify_normalizations': normalization, 'original_strict_rejection': original_rejection,
            'wrong_confirmation_rejected': wrong_confirmation,
            'inspect_simulated_calls': inspect_calls, 'publish_simulated_calls': publish_calls,
            'already_published_simulated_calls': rerun_calls, 'lost_response_simulated_calls': calls,
            'native_state_writes_redirected_to_memory': len(receipts), 'all_native_service_actions_simulated': True,
            'network_and_credential_lookup_guarded': True}

def run_all():
    started = utc()
    before = protected_snapshot()
    input_before = {p.name: identity(p) for p in INPUTS}
    need((F / 'original_manifest.json').read_bytes() == OLD.read_bytes(), 'old manifest bytecopy differs')
    cfg_path = D / 'service_resume_20261016/PR1094_SERVICE_CONFIG.json'
    need((F / 'original_config.json').read_bytes() == cfg_path.read_bytes(), 'original config bytecopy differs')
    need(identity(OLD) == CONFIG['manifest_identity'], 'source manifest pin mismatch')
    need(identity(D / CONFIG['final_seal']) == CONFIG['final_seal_identity'], 'old final seal pin mismatch')
    # Match the driver's ASCII-escaped canonical JSON metadata pin exactly.
    metadata_hash = hashlib.sha256(json.dumps(ORIGINAL['metadata'], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    need(metadata_hash == CONFIG['metadata_sha256'], 'old metadata pin mismatch')
    rows = []
    for name in CASES:
        argv = [sys.executable, '-B', str(Path(__file__).resolve()), '--case', name]
        result = subprocess.run(argv, capture_output=True, text=True, cwd=REPO)
        row = {'argv': argv, 'exit': result.returncode, 'stdout': result.stdout.strip(), 'stderr': result.stderr.strip(),
               'expected_exit': 0 if name == 'positive' else 3}
        rows.append(row)
        need(result.returncode == row['expected_exit'], 'unexpected adversarial exit: ' + name)
    argv = [sys.executable, '-B', str(NATIVE), 'check', str(WIRE)]
    result = subprocess.run(argv, capture_output=True, text=True, cwd=REPO)
    rows.append({'argv': argv, 'exit': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
    need(result.returncode == 0, 'actual native LOCAL check failed')
    native = native_checks()
    generator = generator_acceptance((F / 'proposed_prepare_service_configs.py').read_text())
    old_sp = REPO / '.zenodo-state' / (hashlib.sha256(str(OLD.resolve()).encode()).hexdigest()[:24] + '-production.json')
    new_sp = REPO / '.zenodo-state' / (hashlib.sha256(str(WIRE.resolve()).encode()).hexdigest()[:24] + '-production.json')
    old_state = read(old_sp)
    need(old_state == {'manifest': str(OLD.resolve()), 'environment': 'production', 'id': EXPECTED_ID}, 'old saved draft differs')
    need(not new_sp.exists(), 'wire alias exists before planned adoption')
    need('.zenodo-state/' in (REPO / '.gitignore').read_text().splitlines(), 'native state not ignored')
    after = protected_snapshot()
    need(before == after, 'protected integrity changed during review')
    need(input_before == {p.name: identity(p) for p in INPUTS}, 'review input changed during review')
    events = html_events(ORIGINAL['metadata']['description'])
    preprint_listed = {r['path'] for r in PROTECTED if 'path' in r}
    preprint_actual = {str(p.relative_to(AUDIT)) for p in (AUDIT / 'preprint_v1_0').rglob('*') if p.is_file()}
    need(preprint_actual == preprint_listed, 'preprint file set differs from frozen inventory')
    result = {'started_utc': started, 'finished_utc': utc(), 'scope': 'metadata transport only',
              'verdict': 'ZERO_ACTIONABLE_ISSUES_WITHIN_BOUNDED_SCOPE', 'completion_percent': 100,
              'adversarial_candidates': len(CASES) - 1, 'positive_candidates': 1,
              'raw_commands': rows, 'native_local_results': native, 'file_bindings': acceptance(read(WIRE)),
              'generator_local_static_results': generator,
              'html': {'start_p': sum(e[0] == 'start' and e[2] == 'p' for e in events),
                       'end_p': sum(e[0] == 'end' and e[1] == 'p' for e in events),
                       'attributes': [attr for e in events if e[0] in {'start', 'empty'} for attr in e[3]],
                       'links': [e for e in events if e[0] in {'start', 'empty'} and e[2] == 'a'],
                       'full_event_stream_equal': True, 'raw_tag_sequence_equal': True,
                       'authorized_text_replacements': 1, 'generic_unescape_acceptance': False},
              'old_state': {'path': str(old_sp), 'identity': identity(old_sp), 'value': old_state},
              'planned_new_state_path': str(new_sp), 'new_state_currently_absent': True,
              'frozen_input_identities': input_before, 'protected_rows': len(after),
              'protected_rows_matching': sum(r['matches'] for r in after),
              'preprint_inventory_matches': True, 'preprint_file_count': len(preprint_actual),
              'protected_snapshot_sha256': hashlib.sha256(canon(after).encode()).hexdigest(),
              'protected_before_equals_after': True, 'publication_or_merge_performed': False}
    (HERE / 'checks.json').write_text(json.dumps(result, indent=2) + '\n')
    (HERE / 'integrity_snapshot.json').write_text(json.dumps({'utc': utc(), 'protected': after}, separators=(',', ':')) + '\n')
    print(json.dumps({k: result[k] for k in ['verdict', 'completion_percent', 'adversarial_candidates', 'protected_rows_matching', 'publication_or_merge_performed']}))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=CASES)
    args = parser.parse_args()
    if args.case:
        try:
            case(args.case)
        except (ValueError, KeyError, FileNotFoundError) as exc:
            print(json.dumps({'case': args.case, 'accepted': False, 'reason': str(exc)}))
            raise SystemExit(3)
        print(json.dumps({'case': args.case, 'accepted': True}))
    else:
        run_all()
