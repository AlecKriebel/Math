"""Authenticate actual completed scientific family seals, not advisory messages."""
from pathlib import Path
import datetime,hashlib,json
A=Path(__file__).resolve().parent
families=[('literal_type_source_adversary','FINAL_SEAL.json','a8a5c5cf595897dd5d5d2a691adb7326883eec98baebcbf5a15e7cccf900156c','PUBLIC_ALLOWLIST.json','c9178cef691f5bc6e189fc4fe1cdb51da076cd83fed421dabb74c5b788daefe0'),('exact_reproduction_adversary','FINAL_SHA256.json','151f07da6c2f1117ef12ed0747e5cd1616797f2d1186b38e36da434db4f8dc15','PUBLICATION_ALLOWLIST.json','965ef94184d689477708c94fd1c287da0d3492cf369d71f3e1cc27fce5f75ac9')]
def require(x,msg):
 if not x:raise RuntimeError(msg)
def pin(p):
 require(p.is_file() and not p.is_symlink(),'Nonregular '+str(p));b=p.read_bytes();require((p.stat().st_mode&0o777)==0o444,'Not actually protected '+str(p));return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
rows=[]
for family,seal,sealsha,allow,allowsha in families:
 D=A/family;s=pin(D/seal);q=pin(D/allow);require(s['sha256']==sealsha and q['sha256']==allowsha,'Terminal identity drift '+family)
 manifest=json.loads((D/seal).read_text());public=json.loads((D/allow).read_text());sealed={}
 for x in manifest['files']:
  name=x.get('file',x.get('path'));require(isinstance(name,str) and '..' not in Path(name).parts and not Path(name).is_absolute(),'Unsafe seal path');actual=pin(D/name);require(actual['sha256']==x['sha256'] and actual['bytes']==x['bytes'],'Sealed body drift '+name);sealed[name]=actual
 safe=[]
 for x in public['files']:
  name=x.get('file',x.get('path'));require(name in sealed,'Public file not sealed '+str(name));require(sealed[name]['sha256']==x['sha256'],'Public identity drift '+name);require(not any(z in Path(name).parts for z in ['private','private_source','private_inputs','results']),'Private output selected');safe.append(name)
 rows.append({'family':family,'terminal_seal':s,'public_allowlist':q,'sealed_files_rehashed_and_actual0444':len(sealed),'safe_files_rehashed_and_actual0444':len(safe),'safe_files':safe,'completed_final_report_actually_read_by_Root':True})
out={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'TWO_COMPLETED_MATH_FAMILY_SEALS_AND_ALLOWLISTS_AUTHENTICATED','families':rows,'global_geometry_family_not_yet_adopted_as_completed':True,'mathematical_clearance':False,'priority_clearance':False}
f=A/'ROOT_TWO_MATH_FAMILY_AUTHENTICATION_01.json'
with f.open('x') as w:json.dump(out,w,indent=2);w.write('\n')
f.chmod(0o444);print(json.dumps(out))
