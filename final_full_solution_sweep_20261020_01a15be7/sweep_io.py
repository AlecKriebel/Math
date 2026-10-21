"""Atomic, program-local JSON output; no shared repository state mutations."""
import json
import os
from pathlib import Path
import uuid


def atomic_json(path, value):
    path=Path(path)
    temporary=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    try:
        temporary.write_text(json.dumps(value,indent=2)+'\n')
        os.replace(temporary,path)
    finally:
        temporary.unlink(missing_ok=True)
