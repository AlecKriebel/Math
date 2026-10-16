"""Offline proof that a current disk hash does not bind the imported kit."""
import hashlib
from pathlib import Path
import sys
import types
import json

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = Path('/Users/alec/Documents/Math')
KIT = ROOT / 'zenodo_deposit_tool/zenodo.py'
ADAPTER = HERE.parent / 'native_transport_author/native_transport.py'
reviewed_kit = KIT.read_bytes()
reviewed_adapter = ADAPTER.read_bytes()
# Model a stale import loaded before the shared file returned to reviewed bytes.
# The genuine hash/load functions remain untouched; only run is different.
stale_kit = reviewed_kit + b'\ndef run(args, client=None):\n    return {"unreviewed_loaded_code_executed": True}\n'
loaded = types.ModuleType('zenodo')
loaded.__file__ = str(KIT)
exec(compile(stale_kit, str(KIT), 'exec'), loaded.__dict__)
sys.modules['zenodo'] = loaded
adapter = types.ModuleType('isolated_adapter_probe')
adapter.__file__ = str(ADAPTER)
exec(compile(reviewed_adapter, str(ADAPTER), 'exec'), adapter.__dict__)
metadata, files = adapter.pinned_inputs()
result = {
    'kit_disk_sha256': hashlib.sha256(KIT.read_bytes()).hexdigest(),
    'kit_loaded_source_sha256': hashlib.sha256(stale_kit).hexdigest(),
    'adapter_disk_sha256': hashlib.sha256(reviewed_adapter).hexdigest(),
    'loaded_kit_file_path_matches_expected': loaded.__file__ == str(KIT),
    'pinned_inputs_accepted': True,
    'files_accepted': len(files),
    'loaded_run_result': adapter.zenodo.run(None),
    'network_requests': 0,
    'shared_files_modified': 0,
}
(HERE / 'IMPORT_BINDING_PROBE.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
