import sys,os,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
assert sys.flags.isolated and sys.flags.optimize==0
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';D=A/'preprint';O=A/'reviews/full_package_06'
pins=['2f1a4ba73839b83280e9daba44fbe79e70b52a80761deded5314e0db99c7e834','e0361044f313b540f8a46b6a417a00a1777e22a33439e9a097aa0f9e7b54c3e6','28f08795caf265a412463b3b30880f29bcbc615eb84baf4b92010d1720326370','7fb99b465473a17ad54a363c4ee6f410023b3857343a5df2c356a705d50180d0','4d60602995d799a0850c4657b3401ad9c353460800f1fbd752c532b73b6963b2']
raw=(P/'accept_pr946.py').read_bytes();assert hashlib.sha256(raw).hexdigest()=='8e1a0d7b3ca6e5d72e76415541b393fbfbe52e307368bc86b9e7982d5be27cd7'
N={'__file__':str(P/'accept_pr946.py'),'__name__':'read_only_history06'};exec(compile(raw,str(P/'accept_pr946.py'),'exec'),N)
ctx=N['capture_inventory']('f4742eca6ddd628ecac1e704fed772a17837d42d4d0fdef42c73d3cda3bed254')
rows=[];issues={}
for i,pin in enumerate(pins,1):
 F=A/'reviews'/('full_package_'+str(i).zfill(2));b=N['read_regular'](F/'MANIFEST.json');assert N['sha'](b)==pin;m=N['strict_json'](b);assert set(m['files'])==set(m['explicit_public_allowlist'])
 for name,identity in m['files'].items():N['read_regular'](F/name,pin=identity)
 result=N['load'](F/'RESULT.json');old=D/'reviewed_candidates'/('candidate'+str(i).zfill(2));f=N['freeze_check'](N['read_regular'](old/'FREEZE.json'),result['candidate_pins']['freeze'],ctx,old,historical=True)
 for finding in result['required_issues']+result['optional_issues']:issues[finding['id']]=finding
 rows.append({'round':i,'manifest_sha256':pin,'curated_payloads':len(m['files']),'files':m['files'],'historical_candidate_files':len(f['files']),'historical_dependencies':7,'result':result})
(O/'HISTORY_AUTHENTICATION.json').write_text(json.dumps({'status':'PASS','utc':N['utc_now'](),'rounds':rows,'unique_prior_issues':issues},indent=2)+'\n')
print(json.dumps({'status':'PASS','rounds':[{'round':r['round'],'count':r['curated_payloads']} for r in rows],'issues':issues},indent=2))
