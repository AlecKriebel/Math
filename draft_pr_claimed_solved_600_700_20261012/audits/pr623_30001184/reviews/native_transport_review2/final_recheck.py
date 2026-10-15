from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
ROOT=Path('/Users/alec/Documents/Math')
HERE=Path(__file__).resolve().parent
binding=json.loads((HERE/'INPUT_BINDING.json').read_bytes())
checks={}
for rel,receipt in binding['inputs'].items():
    data=(ROOT/rel).read_bytes()
    checks[rel]={'size':len(data),'sha256':hashlib.sha256(data).hexdigest(),
                'matches':len(data)==receipt['size'] and hashlib.sha256(data).hexdigest()==receipt['sha256']}
extras={}
for filename in ['NEW_CALIBRATION_BINDING.json','FILE_LINK_PRIMARY_BINDING.json']:
    receipt=json.loads((HERE/filename).read_bytes());data=Path(receipt['path']).read_bytes()
    extras[receipt['path']]={'sha256':hashlib.sha256(data).hexdigest(),'size':len(data),'matches':hashlib.sha256(data).hexdigest()==receipt['sha256'] and len(data)==receipt['size']}
primary=json.loads((HERE/'PRIMARY_SOURCE_BINDING.json').read_bytes())
for n,receipt in primary.items():
    data=Path(receipt['snapshot']).read_bytes()
    extras[receipt['snapshot']]={'sha256':hashlib.sha256(data).hexdigest(),'size':len(data),'matches':hashlib.sha256(data).hexdigest()==receipt['sha256'] and len(data)==receipt['size']}
gate=json.loads((HERE/'tmp/inputs/draft_pr_claimed_solved_600_700_20261012/audits/pr623_30001184/FINAL_PUBLICATION_GATE.json').read_bytes())
index_sha=hashlib.sha256((ROOT/'.git/index').read_bytes()).hexdigest()
result={'checked_utc':datetime.now(timezone.utc).isoformat(),'input_count':len(checks),'all_initial_inputs_unchanged':all(c['matches'] for c in checks.values()),
        'extra_count':len(extras),'all_extra_sources_unchanged':all(c['matches'] for c in extras.values()),'inputs':checks,'extras':extras,
        'main_branch_reference':(ROOT/'.git/HEAD').read_text().strip(),'git_index_sha256':index_sha,'git_index_matches_gate':index_sha==gate['shared_local_state']['index_sha256'],
        'frozen_adapter_sha256':'10525be2c736213116173c2bcc75b32e32c0e6addd5a2c123f23efa812f01af8','frozen_launcher_sha256':'81b41e0dda32122b3c3f3d744829fab365381714107ec63703c337a856cdf72e'}
(HERE/'FINAL_INPUT_RECHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['inputs','extras']},indent=2))
raise SystemExit(not result['all_initial_inputs_unchanged'] or not result['all_extra_sources_unchanged'])
