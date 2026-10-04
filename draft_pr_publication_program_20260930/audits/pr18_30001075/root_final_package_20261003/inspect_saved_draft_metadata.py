"""Read the existing Zenodo draft; print only intended/public metadata differences."""
import importlib.util
import json
from pathlib import Path
import sys

if sys.flags.optimize or sys.argv[1:]:
    raise RuntimeError('Nonoptimized no-argument execution required')
own = Path(__file__).resolve().parent
repo = own.parents[3]
spec = importlib.util.spec_from_file_location('pr18_zenodo_readonly',repo/'zenodo_deposit_tool/zenodo.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
manifest = own/'zenodo-deposit.json'
expected, files = module.load_manifest(manifest)
place,state = module.local_state(manifest,'production')
if not state or state['id']!=23127955:
    raise RuntimeError('Unexpected/missing saved draft; no request sent')
client = module.ZenodoClient('production',module.token_for('production'))
draft = client.get(state['id'])
module.validate_record(draft,state['id'])
differences = {k:{'intended':v,'remote':draft.get('metadata',{}).get(k)}
               for k,v in expected.items() if draft.get('metadata',{}).get(k)!=v}
remote_files = module.server_files(draft)
result = {'existing_draft_id':state['id'],'submitted':draft['submitted'],
          'metadata_differences':differences,'exact_file_domain':set(remote_files)=={f['name'] for f in files},
          'files':[{'name':f['name'],'remote_size_md5_matches':module.matching_file(remote_files.get(f['name'],{}),f)} for f in files],
          'request_kind':'One authenticated GET; no create/update/upload/publish request'}
(own/'DRAFT_METADATA_READBACK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
