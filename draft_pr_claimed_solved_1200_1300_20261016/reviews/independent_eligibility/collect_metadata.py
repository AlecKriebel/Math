#!/usr/bin/env python3
"""Read-only independent eligibility receipts; intentionally requests no PR body."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
fields = 'number title state isDraft headRefName headRefOid updatedAt url'
query = ('query { repository(owner:"AlecKriebel",name:"Math") {'
         ' main:ref(qualifiedName:"refs/heads/main"){target{oid}} '
         + ' '.join(f'p{n}:pullRequest(number:{n}){{{fields}}}'
                    for n in range(1200, 1301)) + ' } }')
started = dt.datetime.now(dt.timezone.utc).isoformat()
raw = subprocess.check_output(['gh', 'api', 'graphql', '-f', f'query={query}'])
data = json.loads(raw)
assert not data.get('errors'), data.get('errors')
repo = data['data']['repository']
receipt = {
    'started_utc': started,
    'completed_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
    'repository': 'AlecKriebel/Math',
    'source': 'GitHub GraphQL API, exact PR number aliases 1200 through 1300 inclusive',
    'query': query,
    'raw_response_sha256': hashlib.sha256(raw).hexdigest(),
    'main_sha': repo['main']['target']['oid'],
    'pull_requests': [{'requested_number': n, 'metadata': repo[f'p{n}']}
                      for n in range(1200, 1301)],
}
(ROOT / 'metadata_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
for item in receipt['pull_requests']:
    p = item['metadata']
    if p:
        print(p['number'], p['state'], p['isDraft'], p['headRefName'], '|', p['title'])
    else:
        print(item['requested_number'], 'NOT_A_PULL_REQUEST')
print('main_sha', receipt['main_sha'])
