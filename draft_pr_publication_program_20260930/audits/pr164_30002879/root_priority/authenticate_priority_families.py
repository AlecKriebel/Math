from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat
A=Path(__file__).resolve().parents[1]
def require(ok,msg):
 if not ok: raise RuntimeError(msg)
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')}
def check(p,r):
 x=pin(p);require(x['sha256']==r['sha256'],str(p)+' digest')
 if 'bytes' in r:require(x['bytes']==r['bytes'],str(p)+' size')
 if 'mode' in r:require(int(x['mode'],8)==int(r['mode'],8),str(p)+' mode')
 return x
families=[
 ('priority_historical_versions','MANIFEST.json','0e16e1c488d8426f678de7aaac92504bbdb290cafafcdf825b00ec2e6747cfe6','INPUTS.json','external_workspace_inputs'),
 ('priority_triangular_gerstenhaber','FILE_MANIFEST.json','685a75bc5749bdeee9784f564b6adf19aace39f3fe366f849a571b0b189de94e','INPUT_PINS.json','inputs'),
 ('priority_current_question_quotient','PRESERVED_FILE_MANIFEST.json','eb4a9f7800825372ee8cd5d50a9e00111328d2a21187ec850505157b0a4f4fbd','SOURCE_IDENTITIES.json','inputs')]
o={'UTC':datetime.now(timezone.utc).isoformat(),'status':'ALL_THREE_PRIORITY_FAMILY_EXACT_MANIFESTS_AUTHENTICATED','families':[],'publication_clearance':False}
for fam,n,external,inp,key in families:
 f=A/fam;p=f/n;j=json.loads(p.read_text());require(pin(p)['sha256']==external,fam+' external manifest identity')
 arts=[check(f/r['path'],r) for r in j['files']]
 actual={p.relative_to(f).as_posix() for p in f.rglob('*') if p.is_file()}
 require(actual=={r['path'] for r in j['files']}|{n},fam+' complete inventory')
 inputs=[check(Path(r.get('absolute_path',r.get('source',r.get('path')))),r) for r in json.loads((f/inp).read_text())[key]]
 for nseal in ('FIRST_ASSESSMENT.md','FIRST_ASSESSMENT_SEAL.json'):require(pin(f/nseal)['mode']=='0444',fam+' seal frozen')
 if fam=='priority_historical_versions':
  wl=json.loads((f/'PUBLIC_WHITELIST.json').read_text());public=[r['path'] for r in wl['entries']]
  for r in wl['entries']:check(f/r['path'],r)
 elif fam=='priority_triangular_gerstenhaber':
  public=[r['path'] for r in j['files'] if r.get('visibility')=='public']
 else:public=json.loads((f/'PUBLIC_WHITELIST.json').read_text())['files'];require(set(public)==set(j['public_whitelist']),fam+' whitelist differs')
 require(all(not p.startswith('private/') for p in public),fam+' private body allowlisted')
 for rel in public:require((f/rel).is_file(),fam+' public missing')
 o['families'].append({'family':fam,'manifest_identity':pin(p),'all_preserved_artifact_identities':arts,'external_input_identities':inputs,'complete_inventory_verified':True,'first_seals_frozen':True,'public_allowlist':public,'private_source_bodies_excluded':True})
out=A/'root_priority/PRIORITY_FAMILY_MANIFEST_AUTHENTICATION.json';out.write_text(json.dumps(o,indent=2)+'\n')
print(json.dumps({'receipt':pin(out),'families':3,'artifacts':sum(len(f['all_preserved_artifact_identities']) for f in o['families']),'inputs':sum(len(f['external_input_identities']) for f in o['families']),'status':o['status']},indent=2))
