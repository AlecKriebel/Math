#!/usr/bin/env python3
"""Trusted reviewed bootstrap: capture/hash adapter bytes before executing them."""
import hashlib
from pathlib import Path
import sys
import types
import uuid

sys.dont_write_bytecode = True
ADAPTER = Path(__file__).resolve().with_name('native_transport.py')
ADAPTER_SHA256 = '954d909ee6a8388c36d93bfa74387b24e9383a90c113d6f8eece89a0fa54f32b'


def load_reviewed_adapter(source_path=ADAPTER):
    try:
        source = source_path.read_bytes()
    except OSError as exc:
        raise RuntimeError('Cannot capture reviewed native adapter; nothing was executed') from exc
    if hashlib.sha256(source).hexdigest() != ADAPTER_SHA256:
        raise RuntimeError('Native adapter source differs from reviewed snapshot; nothing was executed')
    module = types.ModuleType('_pr623_reviewed_adapter_' + uuid.uuid4().hex)
    module.__file__ = str(ADAPTER)
    module.__package__ = ''
    exec(compile(source, str(ADAPTER), 'exec', dont_inherit=True), module.__dict__)
    module.__verified_source_sha256__ = ADAPTER_SHA256
    return module


def main():
    try:
        return load_reviewed_adapter().main()
    except RuntimeError as exc:
        print('Error: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
