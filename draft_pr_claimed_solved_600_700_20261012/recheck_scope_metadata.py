#!/usr/bin/env python3
"""Read metadata only for the original101 PRs; never inspect skipped math."""
from pathlib import Path
import datetime,json,subprocess
R=Path(__file__).absolute().parent
baseline=json.loads((R/'eligibility_rechecks/live_metadata_20261015T040121Z.json').read_text())
state=json.loads((R/'PROGRAM_STATE.json').read_text());old={r['number']:r for r in baseline['all_101_metadata']}
fields='number state isDraft headRefOid headRefName url'
query='query { repository(owner:"AlecKriebel",name:"Math") {'+' '.join(f'p{n}:pullRequest(number:{n}){{{fields}}}' for n in range(600,701))+'} }'
r=subprocess.run(['gh','api','graphql','-f','query='+query],capture_output=True,text=True,check=True,cwd=R.parent)
data=json.loads(r.stdout)
if data.get('errors'):raise ValueError('Metadata query errors')
items=sorted(data['data']['repository'].values(),key=lambda x:x['number'])
if [x['number'] for x in items]!=list(range(600,701)):raise ValueError('Missing or duplicate PR metadata')
changed=[x['number'] for x in items if x['number'] in state['skipped'] and x['headRefOid']!=old[x['number']]['headRefOid']]
now=datetime.datetime.now(datetime.timezone.utc);report={'utc':now.isoformat(),'metadata_only':True,'target_math_files_read':False,'all_101_metadata':items,'changed_skipped_heads':changed,'unchanged_skipped_head_count':len(state['skipped'])-len(changed),'no_skipped_pr_mutations':True,'scope_basis':'Original immutable selected QUEUE status; changed skipped heads require a fresh selected-row eligibility check before any target read.'}
path=R/'eligibility_rechecks'/('live_metadata_'+now.strftime('%Y%m%dT%H%M%SZ')+'.json')
with path.open('x') as f:f.write(json.dumps(report,indent=2)+'\n')
print(json.dumps({'receipt':str(path),'metadata_records':len(items),'unchanged_skipped_head_count':report['unchanged_skipped_head_count'],'changed_skipped_heads':changed}))
