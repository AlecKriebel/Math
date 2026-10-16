#!/usr/bin/env python3
"""Tiny inert regression fixtures for exact scientific ZIP-format conformance."""
import ast
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import zipfile
import zlib

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('fixture_helpers', HERE / 'test_tooling.py')
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)


def main():
    helpers.need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode, 'run -I -S -B')
    positive, rejected, bodies = [], [], []
    compressor = zlib.compressobj(wbits=-15)
    second = compressor.compress(b'second inert stream') + compressor.flush()
    for module_name in ('check_originals', 'verify_package', 'build_verification', 'verify_current_publication'):
        module = helpers.load(module_name)
        source = (helpers.TOOLS / (module_name + '.py')).read_text()
        tree = ast.parse(source)
        body = ast.get_source_segment(source, next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'zip_payloads'))
        bodies.append(hashlib.sha256(body.encode()).hexdigest())
        for generated in (False, True):
            for label, payload in [('normal', {'a.txt': b'inert fixture'}), ('empty', {'a.txt': b''}), ('multiple', {'a.json': b'{"n":1}', 'b.txt': b'inert fixture'})]:
                raw = helpers.zip_bytes(payload)
                helpers.need(module.zip_payloads(raw, payload, generated) == payload, 'valid fixture rejected')
                positive.append({'module': module_name, 'generated': generated, 'fixture': label, 'passed': True})
                for mutation, changed in [('surplus-byte', helpers.add_deflate_suffix(raw, b'X')), ('second-stream', helpers.add_deflate_suffix(raw, second)), ('reserved-block-type', helpers.invalid_deflate_block(raw))]:
                    if mutation != 'reserved-block-type':
                        # Confirm this fixture reaches the reported library
                        # interpretation: legacy ZipExtFile returns every exact
                        # member despite the surplus declared compressed bytes.
                        with zipfile.ZipFile(io.BytesIO(changed)) as archive:
                            helpers.need({name: archive.read(name) for name in archive.namelist()} == payload, 'fixture does not reproduce ignored suffix')
                    try:
                        module.zip_payloads(changed, payload, generated)
                    except (ValueError, zlib.error, zipfile.BadZipFile) as exc:
                        rejected.append({'module': module_name, 'generated': generated, 'fixture': label, 'mutation': mutation, 'rejected': True, 'reason': str(exc)})
                    else:
                        raise ValueError('malformed DEFLATE region accepted: ' + module_name + ':' + mutation)
    helpers.need(len(set(bodies)) == 1 and len(positive) == 24 and len(rejected) == 72, 'exact guard/count contract')
    result = {'status': 'PASS', 'scope': 'Internal finite ZIP-format regression only; separate independent format review still required.', 'optimized': bool(sys.flags.optimize), 'same_guard_in_all_four': True, 'guard_sha256': bodies[0], 'negative_control_count': len(rejected), 'positive_control_count': len(positive), 'negative_controls': rejected, 'positive_controls': positive, 'archival_bodies_executed': False, 'large_inputs_or_copies_used': False}
    name = 'FORMAT_REPAIR_OPTIMIZED.json' if sys.flags.optimize else 'FORMAT_REPAIR_NORMAL.json'
    (HERE / name).write_bytes(helpers.js(result))
    print(json.dumps({'status': 'PASS', 'negative_controls': len(rejected), 'positive_controls': len(positive), 'guard_sha256': bodies[0]}, sort_keys=True))


if __name__ == '__main__':
    main()
