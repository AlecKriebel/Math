#!/usr/bin/env python3
"""Bind actual publication custody and fresh exact-row GWS GETs. No mutations."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CASE = HERE.parent

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--helper-sha256', required=True)
    p.add_argument('--tracker-evidence', required=True)
    p.add_argument('--tracker-result-sha256', required=True)
    p.add_argument('--run-name', required=True)
    a = p.parse_args()
    if not a.run_name.replace('_', '').isalnum():
        raise ValueError('unsafe run name')
    helper = CASE / 'publication_preparation/admin_helper_v3/publication_admin_v3.py'
    raw = helper.read_bytes()
    if sha(raw) != a.helper_sha256:
        raise ValueError('reviewed helper drift')
    spec = importlib.util.spec_from_file_location('binding_publisher', helper)
    m = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(helper), 'exec'), m.__dict__)
    tracker = m.own(Path(a.tracker_evidence))

    def ref(path):
        data, _ = m.g.read_regular(path, private=True)
        return {'path': str(path.relative_to(CASE)), 'sha256': sha(data)}

    def doc(path):
        return json.loads(m.g.read_regular(path, private=True)[0])

    result_path = tracker / 'RESULT.json'
    result = doc(result_path)
    m.need(ref(result_path)['sha256'] == a.tracker_result_sha256
           and result['evidence_kind'] == 'native_production_api'
           and result['status'] in ('tracker_verified', 'tracker_already_exact')
           and result['id'] == 23331232 and result['doi'] == '10.5281/zenodo.23331232',
           'actual root-confirmed tracker result differs')
    records = []
    for path in sorted(tracker.glob('*_intent.json')):
        intent = doc(path)['intent']
        response = path.with_name(path.name.replace('_intent.json', '_response.json'))
        records.append((intent, path, response))

    def pick(service, operation, predicate=lambda x: True):
        matches = [(i, p, r) for i, p, r in records
                   if i['service'] == service and i['operation'] == operation and predicate(doc(r))]
        m.need(matches, 'missing actual administrative receipt')
        return matches[-1]

    _, submit_i, submit_r = pick('zenodo', 'GET /api/deposit/depositions/23331232',
                               lambda x: x.get('submitted') is True)
    _, auth_i, auth_r = pick('zenodo', 'GET /api/records/23331232')
    publics = {}
    for native in (False, True):
        matches = [(i, p, r) for i, p, r in records
                   if i['service'] == 'public_json' and i['params'] == {'id': 23331232, 'native': native}]
        m.need(len(matches) == 1, 'ambiguous actual public record custody')
        publics[native] = matches[0][1:]
    legacy_r, native_r = publics[False][1], publics[True][1]
    publication = {
        'submitted_intent': ref(submit_i), 'submitted_response': ref(submit_r),
        'legacy_public_response': ref(legacy_r),
        'legacy_public_native': ref(legacy_r.with_name(legacy_r.name.replace('_response.json', '_native.json'))),
        'authenticated_native_response': ref(auth_r), 'public_native_response': ref(native_r),
        'public_native_native': ref(native_r.with_name(native_r.name.replace('_response.json', '_native.json'))),
        'approved_native_snapshot': ref(m.v2.ROOT_SNAPSHOT), 'result': ref(result_path)}
    e = m.Admin(m.v1.Production(), m.PRIVATE / ('root_merge_bindings_' + a.run_name))
    expected_row = e.sheet_gate(result['tracker_range'])
    m.need(isinstance(expected_row, list) and len(expected_row) == 1, 'exact returned tracker row missing')
    row = expected_row[0]
    original_spec = e.check_original()['spec']
    m.need(row == [original_spec['tracker']['original_problem'], original_spec['tracker']['solution_chat'],
                   'https://doi.org/10.5281/zenodo.23331232', original_spec['tracker']['notes']],
           'fresh four-cell tracker readback differs')
    sheet = {'row_range': result['tracker_range'], 'expected_row': row}
    for field, index in (('metadata', 0), ('batch', 1)):
        for kind in ('intent', 'native', 'response'):
            sheet[field + '_' + kind] = ref(e.evidence / f'{index:04d}_{kind}.json')
    append = [(i, p, r) for i, p, r in records if i['service'] == 'sheet' and i['operation'] == 'append']
    m.need(len(append) == (1 if result['status'] == 'tracker_verified' else 0), 'original append custody differs')
    for kind in ('intent', 'native', 'response'):
        sheet['append_' + kind] = None if not append else ref(
            append[0][1].with_name(append[0][1].name.replace('_intent.json', '_' + kind + '.json')))
    binding = {'format': 'pr411-native-administration-bindings-v1', 'doi': result['doi'],
               'publication': publication, 'sheet': sheet}
    output = HERE / ('ACTUAL_NATIVE_BINDINGS_' + a.run_name + '.json')
    m.g.durable(output, binding, exclusive=True)
    print(json.dumps({'result': 'ACTUAL_NATIVE_BINDINGS_CREATED', 'path': str(output.relative_to(CASE)),
                      'sha256': ref(output)['sha256'], 'remote_GETs': 2, 'remote_mutations': 0,
                      'tracker_range': result['tracker_range']}))

if __name__ == '__main__':
    main()
