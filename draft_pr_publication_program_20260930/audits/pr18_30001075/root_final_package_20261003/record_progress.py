"""Record ROOT's actual package checkpoint; no publication/merge claim."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys

if sys.flags.optimize or sys.argv[1:]:
    raise RuntimeError('Nonoptimized no-argument execution required')
own = Path(__file__).resolve().parent
a18 = own.parent
program = a18.parents[1]
record = json.loads((own/'ROOT_REPRODUCTION.json').read_bytes())
for name, sha in record['pins'].items():
    if hashlib.sha256((a18/'preprint_v1'/name).read_bytes()).hexdigest() != sha:
        raise RuntimeError('Package changed: '+name)
utc = dt.datetime.now(dt.timezone.utc).isoformat()
text = ('\n## '+utc+' — PR18 fixed preprint checkpoint\n\n'
        'The complete supplied 2024 article was read and compared with the precise '
        'supporting-line spatial-nullness claim. The bounded priority assessment '
        'resolves that named access hold without claiming exhaustive priority. '
        'All eight final PDF pages were visually inspected by ROOT through the image '
        'tool; no clipping or overlap was observed. The exact final portable archive '
        'rebuilds byte for byte from its own frozen inputs; a fresh extraction passes '
        '2,826 exact finite controls. These checks do not replace the universal proof. '
        'The fresh first adversary is completing its exact whole-package examination; '
        'a new second reviewer remains required. No deposit, DOI, tracker row or native '
        'acceptance is claimed. The Workspace CLI login returned expired/revoked '
        'credentials, and the human reconnect question remains pending. '
        'Best estimate: PR18 review/publication workflow75%; unchanged original1/5 '
        'research accounting, no new mathematical-attempt credit.\n')
receipts = []
for path in [a18/'RESEARCH_LOG.md',program/'RESEARCH_LOG.md']:
    old = path.read_bytes()
    with path.open('ab') as f:
        f.write(text.encode())
    receipts.append({'path':str(path),'before_sha256':hashlib.sha256(old).hexdigest(),
                     'after_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
output = {'UTC':utc,'actual_pid':os.getpid(),'workflow_percent':75,
          'package_pins':record['pins'],'log_appends':receipts,
          'publication':False,'merge':False,'source_central_attempts':0}
(own/'ROOT_PROGRESS.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
