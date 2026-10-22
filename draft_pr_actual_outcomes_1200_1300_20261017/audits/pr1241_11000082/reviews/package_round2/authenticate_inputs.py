"""Authenticate every declared original input and the external manifest anchor."""
from pathlib import Path
import datetime,hashlib,json,sys
HERE=Path(__file__).resolve().parent
ANCHOR='e7f5c3a83a264da8978c6f95cb18e60bfa68d74b2a365ae98d1632874b5edefd'
freeze=HERE/'INPUT_FREEZE.json';spec=json.loads(freeze.read_text());root=Path(spec['root']);rows=[]
for e in spec['files']+spec['external_readonly_inputs']:
    p=Path(e['path']);p=p if p.is_absolute() else root/p;b=p.read_bytes();actual=hashlib.sha256(b).hexdigest()
    rows.append({**e,'actual_bytes':len(b),'actual_sha256':actual,'ok':len(b)==e['bytes'] and actual==e['sha256']})
digest=hashlib.sha256(freeze.read_bytes()).hexdigest()
report={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest_sha256':digest,'outside_anchor':ANCHOR,'anchor_ok':digest==ANCHOR,'file_count':len(spec['files']),'external_count':len(spec['external_readonly_inputs']),'all_ok':digest==ANCHOR and all(e['ok'] for e in rows),'files':rows}
(HERE/('INPUT_AUTHENTICATION_'+sys.argv[1]+'.json')).write_text(json.dumps(report,indent=2)+'\n')
if not report['all_ok']:raise RuntimeError('Input authentication failed')
print(json.dumps({k:v for k,v in report.items() if k!='files'}))
