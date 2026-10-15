#!/usr/bin/env python3
"""Parent integrity/readback of reviewed own-byte artifacts; no peer execution."""
from pathlib import Path, PurePosixPath
import ast
import datetime
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

def need(value, message):
    if not value:
        raise RuntimeError(message)

def pairs(items):
    out = {}
    for key, value in items:
        need(key not in out, 'duplicate JSON key')
        out[key] = value
    return out

def parse(data):
    return json.loads(data, object_pairs_hook=pairs)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def package(name, count):
    folder = HERE / 'reviews' / name
    raw = (folder / 'PUBLIC_FILES.json').read_bytes()
    manifest = parse(raw)
    need(len(manifest['files']) == count, 'unexpected positive file count')
    seen = set()
    records = []
    for entry in manifest['files']:
        rel = PurePosixPath(entry['path'])
        need(not rel.is_absolute() and '..' not in rel.parts and rel.parts,
             'unsafe path')
        need(not set(rel.parts) & {'private_sources', 'private_cases', '__pycache__'},
             'private path in public index')
        need(str(rel) not in seen, 'duplicate indexed path')
        seen.add(str(rel))
        target = folder.joinpath(*rel.parts)
        need(target.is_file() and not target.is_symlink(), 'nonregular payload')
        data = target.read_bytes()
        need(type(entry['bytes']) is int and len(data) == entry['bytes'],
             'payload byte count mismatch')
        need(digest(data) == entry['sha256'], 'payload hash mismatch')
        if target.suffix == '.json':
            parse(data)
        elif target.suffix == '.py':
            ast.parse(data, filename=str(target))
        else:
            data.decode('utf-8')
        records.append({'path': str(target.relative_to(ROOT)),
                        'bytes': len(data), 'sha256': digest(data)})
    return {'manifest_sha256': digest(raw), 'positive_files': records,
            'self_excluded_manifest_checked': True}

def stable(obj):
    return {k:v for k,v in obj.items() if k not in
            {'utc_completed', 'elapsed_seconds', 'python'}}

def main():
    packages = {name: package(name, count) for name, count in
                [('prior_classification_adversary', 9),
                 ('spin_numerical_validation', 13)]}
    producer = HERE / 'reviews' / 'spin_numerical_validation'
    need(digest((producer / 'certify_integral.py').read_bytes()) ==
         '027dc38ea76f1a4e69d8976a4845caefc4429e48b551afa7c327dc243b3dac20',
         'controlling producer hash mismatch')
    classification = parse((HERE / 'reviews' / 'prior_classification_adversary' /
                            'RESULT.json').read_bytes())
    need(classification['classification_blockers'] == 0 and
         classification['unresolved_independently_certified_numerical_reproduction_gaps'] == 1,
         'historical classification qualification changed')
    certified = parse((producer / 'certificate_N13_M65536.json').read_bytes())
    need(certified['status'] == 'CERTIFIED', 'not certified')
    upper = int(certified['sum_cell_log_upper_scaled'])
    rhs = int(certified['comparison_M_N_log2_lower_scaled'])
    need(rhs > upper and rhs-upper == int(certified['strict_integer_margin']),
         'integer comparison mismatch')
    parent = parse((HERE / 'ROOT_SPIN_CERTIFICATE_REPLAY.json').read_bytes())
    need(len(parent['records']) == 2, 'parent replay count')
    for record in parent['records']:
        need(record['exit_code'] == 0 and record['stderr'] == '', 'parent replay failure')
        need(stable(parse(record['stdout'])) == stable(certified),
             'parent replay differs')
    output = {'recorded_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'scope': 'Byte/schema/integer/replay readback, not an inferred mathematical approval',
              'packages': packages,
              'parent_actual_replays': 2,
              'strict_N13_margin': str(rhs-upper),
              'classification_local_gap_preserved': 1,
              'reviewed_code_reexecution': False,
              'peer_sealed_files_overwritten': False}
    (HERE / 'SPIN_REVIEWS_READBACK.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps({'packages_checked': len(packages),
                      'positive_payloads_checked': sum(len(v['positive_files']) for v in packages.values()),
                      'strict_N13_margin': str(rhs-upper)}))

if __name__ == '__main__':
    main()
