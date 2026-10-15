#!/usr/bin/env python3
"""Own handwritten text revision, never imports/compiles/executes production."""
import datetime as dt
import hashlib
import json
from pathlib import Path
here=Path(__file__).absolute().parent
source=here/'prepare_current_packet.py'
old=source.read_bytes()
saved=here/'INITIAL_GENERATED_BUILDER_SOURCE_SAVED_AFTER_AUTHORING.py'
assert not saved.exists()
saved.write_bytes(old)
prefix,rest=old.decode().split('def build(args, script, audit, repo, attempt):',1)
tail='def main():\n'+rest.split('def main():\n',1)[1]
core=(here/'BUILDER_BODY.source.txt').read_bytes()
new=prefix.encode()+core+b'\n\n'+tail.encode()
assert old!=new
source.write_bytes(new)
def sha(body):return hashlib.sha256(body).hexdigest()
record={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'production_execution':False,
        'old_sha256':sha(old),'new_sha256':sha(new),'current_body_source_sha256':sha(core),
        'old_source_saved_after_authoring_not_claimed_initial_prelaunch':True,
        'reason':'Clarify two evidence C1 captures as combined helpers plus rawSQL; validate every C1 field and prelaunch operator; allow historical DRAFT word in completed proof notes except draft title.'}
(here/'SOURCE_TOOL_EDIT_NOTES.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
