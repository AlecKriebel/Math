#!/usr/bin/env python3
import pathlib,json,hashlib
W=pathlib.Path(__file__).resolve().parent;by={x['number']:x for x in json.loads((W/'inputs/fixed_inventory.json').read_text())};out=[]
for n in range(883,906):
 d=json.loads((W/'inputs'/f'PR{n:04}_DISPOSITION.json').read_text());e=json.loads((W/'inputs'/f'pr{n:04}.json').read_text());i=by[n]
 out.append({'pr':n,'disposition_head_equals_inventory':d['inventory_head_sha']==i['headRefOid'],'disposition_base_equals_inventory':d['inventory_base_sha']==i['baseRefOid'],'eligibility_head_equals_inventory':e['inventory_head_sha']==i['headRefOid'],'eligibility_base_equals_inventory':e['inventory_base_sha']==i['baseRefOid'],'state_equal':d['pr_state']==i['state'],'body_sha_equal':hashlib.sha256(i['body'].encode()).hexdigest()==d['inventory_body_sha256'],'updated_at_equal':d['inventory_updated_at']==i['updatedAt']})
(W/'INPUT_COHERENCE.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS' if all(all(v for k,v in x.items() if k!='pr') for x in out) else 'FAIL',len(out),'immutable input identity comparisons')
