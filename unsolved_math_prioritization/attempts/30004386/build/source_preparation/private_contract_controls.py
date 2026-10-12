#!/usr/bin/env python3
"""Own finite private contract controls. Never load/run/compile proposed sources.

These independent mechanical probes demonstrate strict JSON scalars, full0444
permissions and macOS absent-only rename semantics in this family's sandbox.
They are not builder execution, scientific controls or a whole-current verdict.
"""
import ctypes
import datetime as dt
import errno
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import stat
import sys

P = Path(__file__).absolute().parent
C = P / 'private_controls'
checks = []


def require(ok, message):
    if not ok:
        raise ValueError(message)


def record(name, ok, **info):
    require(ok, name)
    checks.append(dict(name=name, passed=True, **info))


def strict(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate key')
            result[key] = value
        return result
    def constant(value):
        raise ValueError(value)
    def number(value):
        result = float(value)
        require(math.isfinite(result), 'Nonfinite number')
        return result
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant, parse_float=number)


def rejection(name, callback):
    try:
        callback()
    except ValueError:
        record(name, True)
    else:
        raise ValueError('Control accepted: ' + name)


def bytes_count(obj):
    require(type(obj['bytes']) is int and obj['bytes'] >= 0, 'Typed nonnegative byte count')


def relative(name):
    require(type(name) is str and name and '\\' not in name, 'POSIX path')
    path = PurePosixPath(name)
    require(not path.is_absolute() and path.as_posix() == name and
            not {'.', '..', '.git', '__pycache__'}.intersection(path.parts), 'Unsafe path')


require(P.name == 'current_preparation_family' and not C.exists(), 'New private control sandbox only')
C.mkdir()
for name, raw in [('duplicate_top_key', b'{"x":1,"x":2}'),
                  ('duplicate_nested_key', b'{"a":{"x":1,"x":2}}'),
                  ('NaN_rejected', b'{"x":NaN}'), ('Infinity_rejected', b'{"x":Infinity}'),
                  ('negative_infinity_rejected', b'{"x":-Infinity}'),
                  ('overflow_float_rejected', b'{"x":1e999}')]:
    rejection(name, lambda raw=raw: strict(raw))
for value in [True, False, -1, 0.5, None, '0']:
    rejection('wrong_byte_type_' + repr(value), lambda value=value: bytes_count({'bytes': value}))
record('typed_zero_bytes_accepted', bytes_count({'bytes': 0}) is None)
record('null_and_boolean_distinct', strict(b'{"x":null,"y":false}') == {'x': None, 'y': False})
for name in ['../escape', '/absolute', 'nested//x', 'nested/./x', '.git/x', '__pycache__/x', 'nested\\x']:
    rejection('unsafe_path_' + name, lambda name=name: relative(name))
record('canonical_nested_path_accepted', relative('nested/member') is None)
permissions = []
for value in [0o444, 0o1444, 0o2444, 0o4444]:
    path = C / ('mode_' + format(value, '05o'))
    path.write_bytes(b'own finite full-mode probe\n')
    path.chmod(value)
    observed = stat.S_IMODE(path.stat().st_mode)
    require(observed == value, 'Probe mode not actually retained')
    accepted = observed == 0o444
    record('full_mode_' + format(value, '05o'), accepted == (value == 0o444))
    permissions.append(dict(path=path.relative_to(P).as_posix(),
                            requested_mode=format(value, '05o'), actual_full_mode=format(observed, '05o'),
                            literal0444_accepted=accepted, bytes=path.stat().st_size,
                            sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
require(sys.platform == 'darwin', 'Actual macOS probe required')
source, existing, absent = C / 'rename_source', C / 'rename_existing', C / 'rename_absent'
source.mkdir(); existing.mkdir()
(source / 'member').write_bytes(b'own source retained after failure\n')
(existing / 'sentinel').write_bytes(b'own destination retained\n')
libc = ctypes.CDLL(None, use_errno=True)
rename = libc.renamex_np
rename.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
rename.restype = ctypes.c_int
result = rename(bytes(source), bytes(existing), 4)
number = ctypes.get_errno()
record('RENAME_EXCL_existing_destination_rejected', result == -1 and number in [errno.EEXIST, errno.ENOTEMPTY]
       and (source / 'member').read_bytes() == b'own source retained after failure\n'
       and (existing / 'sentinel').read_bytes() == b'own destination retained\n', actual_errno=number)
record('RENAME_EXCL_absent_destination_accepted', rename(bytes(source), bytes(absent), 4) == 0
       and not source.exists() and (absent / 'member').read_bytes() == b'own source retained after failure\n')
result = dict(schema='PR43_OWN_FINITE_PRIVATE_CONTRACT_CONTROLS_v1',
    utc=dt.datetime.now(dt.timezone.utc).isoformat(), checks=checks, permission_probes=permissions,
    all_passed=True, tested_builder_import_compile_execution=False,
    tested_future_ROOT_operator_execution=False, scientific_helpers_run=False,
    new_whole_current_gate='PENDING', current_whole_verdict=None,
    controls_scope='Independent finite mechanical predicates only; never actual proposed builder execution.')
with (P / 'PRIVATE_CONTRACT_CONTROL_RESULTS.json').open('x') as out:
    json.dump(result, out, indent=2); out.write('\n')
print(json.dumps(result, indent=2))
