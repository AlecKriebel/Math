"""Root read-only, offline binding of saved interfaces; no scientific imports."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[1]
SOURCE = PAPER / 'sources'
REVIEWS = PAPER / 'reviews'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def typed_equal(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(typed_equal(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(typed_equal(x, y) for x, y in zip(a, b))
    return a == b


def exact_namespace(folder, rows, terminals):
    expected = {r['path'] for r in rows} | set(terminals)
    paths = list(folder.rglob('*'))
    need(not any(p.is_symlink() for p in paths), 'symlink in sealed namespace')
    need({p.relative_to(folder).as_posix() for p in paths if p.is_file()} == expected,
         'whole namespace differs: ' + str(folder))
    for row in rows:
        rel = Path(row['path'])
        need(not rel.is_absolute() and '..' not in rel.parts, 'unsafe relative path')
        body = (folder / rel).read_bytes()
        need(len(body) == row['bytes'] and sha(body) == row['SHA256'],
             'whole file binding: ' + str(rel))
    return len(expected)


def main():
    ready = read(SOURCE / 'SOURCE_READY.json')
    custody = read(REVIEWS / 'adversarial/SOURCE_CUSTODY.json')
    need(typed_equal(ready, custody['whole_original_source_ready_object']), 'whole typed READY')
    need(sha((SOURCE / 'SOURCE_READY.json').read_bytes()) ==
         '928fb2b26bd31a0678fc3954c29f8a7897a3d6352e9b5dab791224a72a828235', 'READY pin')
    scope = REVIEWS / 'scope'
    adv = REVIEWS / 'adversarial'
    namespaces = {
        'scope': exact_namespace(scope, read(scope / 'OWNED_MANIFEST.json')['owned_files'],
                                 ['OWNED_MANIFEST.json', 'CLOSURE_RESULT.json', 'FINAL_SEAL.json']),
        'adversarial': exact_namespace(adv, read(adv / 'MANIFEST.json')['owned_files'],
                                       ['MANIFEST.json', 'SEAL.json']),
        'source': exact_namespace(SOURCE, read(SOURCE / 'SOURCE_READY_MANIFEST.json')['files'],
                                  ['SOURCE_READY_MANIFEST.json', 'SOURCE_READY_CLOSURE.json',
                                   'SOURCE_READY_SEAL.json']),
    }
    expected_path = SOURCE / 'published-source/asset-001/verification/expected_results.json'
    expected_bytes = expected_path.read_bytes()
    need(len(expected_bytes) == 6908 and sha(expected_bytes) ==
         '0e337b9ade805e930bd48ec74788dc0cc86ecd3cd05c422a69c604b241ec4806', 'original expected pin')
    expected = json.loads(expected_bytes)
    replay = read(adv / 'NATIVE_REPLAY.json')
    comparison = read(adv / 'NATIVE_WHOLE_COMPARISON.json')
    need(typed_equal(expected, replay['whole_original_expected_object']), 'whole typed replay wrapper')
    need(typed_equal(expected, comparison['whole_original_expected_wrapper']), 'whole typed comparison wrapper')
    streams = []
    for checker in ('geometry', 'topology'):
        encoding = (json.dumps(expected[checker], indent=2, sort_keys=True) + '\n').encode()
        for mode in ('normal', 'optimized'):
            prefix = adv / ('NATIVE_' + checker + '_' + mode)
            body = prefix.with_suffix('.stdout').read_bytes()
            stderr = prefix.with_suffix('.stderr').read_bytes()
            run = next(r for r in replay['runs'] if r['checker'] == checker and r['mode'] == mode)
            need(typed_equal(json.loads(body), expected[checker]), 'whole typed stdout')
            need(body == encoding, 'whole stdout encoding')
            need(run['exit_code'] == 0 and stderr == b'', 'actual saved successful exit and empty stderr')
            need(len(body) == run['stdout_bytes'] and sha(body) == run['stdout_SHA256'], 'stdout receipt pin')
            streams.append({'checker': checker, 'mode': mode, 'bytes': len(body), 'SHA256': sha(body),
                            'whole_typed_object_and_entire_encoder_bytes_equal': True})
    bodies = []
    for name in ['verification/check_geometry.py', 'verification/check_topology.py',
                 'verification/expected_results.json', 'README.md', 'LICENSE.txt']:
        original = SOURCE / 'published-source/asset-001' / name
        body = original.read_bytes()
        need(body == (adv / 'native-isolated' / name).read_bytes(), 'whole selected isolated original')
        bodies.append({'path': str(original), 'bytes': len(body), 'SHA256': sha(body)})
    print(json.dumps({'status': 'PASS_ROOT_SAVED_INTERFACES', 'exact_namespaces': namespaces,
                      'whole_READY_typed_equality': True, 'native_stdout_comparisons': streams,
                      'personally_read_original_bodies': bodies,
                      'source_or_scientific_code_imported_or_executed': False,
                      'writes': False, 'network': False}, indent=2))


if __name__ == '__main__':
    main()
