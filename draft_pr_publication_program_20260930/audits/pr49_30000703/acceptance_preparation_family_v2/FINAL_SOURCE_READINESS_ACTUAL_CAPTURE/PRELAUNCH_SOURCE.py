"""Own admin-only readback; imports only own checks, no proposed production helper."""
import json,os
from source_package_checks import F,inspect
q=inspect()
with (F/'READINESS_CHECK.json').open('x') as f:json.dump(q,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(q,sort_keys=True))
