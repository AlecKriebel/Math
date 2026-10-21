"""Atomic, program-local JSON output; no shared repository state mutations."""
import json
import os
from pathlib import Path
import uuid


def atomic_bytes(path, payload):
    path=Path(path)
    temporary=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    try:
        temporary.write_bytes(payload)
        os.replace(temporary,path)
    finally:
        temporary.unlink(missing_ok=True)


def atomic_json(path, value):
    atomic_bytes(path,(json.dumps(value,indent=2)+'\n').encode('utf-8'))
