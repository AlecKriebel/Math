"""Physical byte authentication independent of any reviewed receipt."""
from pathlib import Path
import hashlib,json,datetime,sys
R=Path(__file__).resolve().parent; A=R.parents[1]
EXPECTED='db64f7e4f7e4f0951293c48a22a00c794e34c5f13a9d383a447073f8f0fd8414'
f=R/'INPUT_FREEZE.json'; raw=f.read_bytes(); spec=json.loads(raw)
def physical_exact(p):
    q=Path(p.anchor)
    for part in p.parts[1:]:
        if part not in {x.name for x in q.iterdir()}: return False
        q=q/part
    return q.is_file() and not q.is_symlink()
checks=[]; errors=[]
if hashlib.sha256(raw).hexdigest()!=EXPECTED: errors.append('freeze mismatch')
for group in ('files','external_readonly_inputs'):
    for entry in spec[group]:
        p=Path(entry['path']); p=p if p.is_absolute() else A/p
        try:
            data=p.read_bytes(); exact=physical_exact(p)
            ok=exact and len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256']
            checks.append({'group':group,**entry,'exact_physical_case':exact,'ok':ok})
            if not ok: errors.append(entry['path'])
        except Exception as ex: errors.append({'path':entry['path'],'exception':str(ex)})
result={'schema':'math-pr1274-input-authentication-v1','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_freeze_sha256':EXPECTED,'files':len(spec['files']),'external_readonly_inputs':len(spec['external_readonly_inputs']),'all_ok':not errors,'errors':errors,'bindings':checks}
(R/sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='bindings'}));sys.exit(bool(errors))
