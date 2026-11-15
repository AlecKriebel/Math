"""Explicit new-stage pure render control. Does not call the builder CLI or write.

Not imported by the default custody helper. Only the unchanged current staging
modules are imported when run() is explicitly invoked; no scientific code.
"""
from pathlib import Path
import hashlib
import json
import sys


def run(writer):
    writer = Path(writer).resolve()
    sys.path.insert(0, str(writer))
    import build_private
    import stage_model
    if Path(build_private.__file__).resolve() != writer / 'build_private.py':
        raise ValueError('wrong staging renderer imported')
    manifest = json.loads((writer / 'CODE_MANIFEST.json').read_bytes())
    for row in manifest['implementation_files']:
        raw = (writer / row['path']).read_bytes()
        if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['SHA256']:
            raise ValueError('renderer code pin differs')
    frozen = stage_model.Frozen(writer)
    records = stage_model.load_records(frozen)
    outputs = build_private.build_bytes(records, frozen, '2026-11-15')
    actual_paths = {p.relative_to(writer / 'candidate-a/public').as_posix()
                    for p in (writer / 'candidate-a/public').rglob('*') if p.is_file()}
    if set(outputs) != actual_paths or len(outputs) != 10:
        raise ValueError('pure renderer output namespace differs')
    rows = []
    for relative, raw in sorted(outputs.items()):
        if raw != (writer / 'candidate-a/public' / relative).read_bytes() or raw != (writer / 'candidate-b/public' / relative).read_bytes():
            raise ValueError('whole pure rendered bytes differ: ' + relative)
        rows.append({'path': relative, 'bytes': len(raw), 'SHA256': hashlib.sha256(raw).hexdigest(),
                     'whole_bytes_equal_both_sealed_trees': True})
    return {'literal_custom_status': 'UNCHANGED_NEW_STAGE_PURE_RENDER_BUFFERS_EQUAL_ALL_TEN_SEALED_OUTPUTS',
            'optimization': sys.flags.optimize, 'actual_python': sys.version,
            'outputs': rows, 'builder_CLI_called': False, 'output_files_created': False,
            'science_or_old_campaign_replayed': False}


if __name__ == '__main__':
    if len(sys.argv) != 2: raise ValueError('supply sealed current writer root')
    print(json.dumps(run(Path(sys.argv[1])), indent=2))
