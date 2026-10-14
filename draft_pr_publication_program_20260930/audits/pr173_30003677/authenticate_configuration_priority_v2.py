from pathlib import Path
import json,hashlib,stat,datetime
A=Path(__file__).resolve().parent;B=A/'priority_config_multiseed'
def require(c,m):
 if not c:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')}
if __name__=='__main__':
 f=B/'public/FINAL_INVENTORY_V2.json';p=pin(f);require(p['sha256']=='08c235ad2595b986ab1eda0d4c91866e49dd27d541cfba35b901f3c1c8f4f52c','External complete inventory anchor differs');j=json.loads(f.read_text());seen=set()
 for r in j['files']:
  n=r['path'];q=Path(n);require(not q.is_absolute() and '..' not in q.parts and n not in seen,'Unsafe/repeated file');seen.add(n);x=B/n;require(x.is_file() and not x.is_symlink(),'Missing/symlink');d=pin(x);require(d['bytes']==r['bytes'] and d['mode']=='0444','Size/mode differs')
  if n=='public/FINAL_INVENTORY_V2.json':require(r['sha256'] is None,'Recursive selfhash prohibited')
  else:require(d['sha256']==r['sha256'],'Byte identity differs '+n)
 require(seen=={x.relative_to(B).as_posix() for x in B.rglob('*') if x.is_file()} and len(seen)==91,'Missing/extra retained files')
 m=pin(B/'public/FINAL_MANIFEST_V2.json');require(m['sha256']=='ccffda21bcfc870a1f438b69740ed195cdada95e2dfbc9b64e3aa4ca1b4f08e5','Final manifest differs')
 f1=B/'public/FIRST_SEAL_MANIFEST.json';require(pin(f1)['sha256']=='b2734be928e4ccab64fccc14a79002a86481502586fd857a9e8e81042ff6f06a','First seal changed')
 for r in json.loads(f1.read_text())['inventory']:
  d=pin(B/r['path']);require(d['bytes']==r['bytes'] and d['sha256']==r['sha256'] and d['mode']=='0444','First inventory evidence changed')
 al=json.loads((B/'public/SAFE_PUBLIC_ALLOWLIST_V2.json').read_text())['safe_paths'];require(len(al)==33 and len(set(al))==33 and set(al)<=seen and all(n.startswith('public/') for n in al),'Public list invalid')
 require('public/NORMALIZATION_CLARIFICATION.md' in al,'Normalization companion missing')
 o=A/'ROOT_CONFIGURATION_PRIORITY_V2_AUTHENTICATION.json';require(not o.exists(),'Preserve previous authentication')
 out={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'COMPLETE_CONFIG_PRIORITY_V2_AND_FIRST_SEAL_AUTHENTICATED','family':'priority_config_multiseed','all_retained_files_authenticated':91,'all_files_mode':'0444','first_seal':pin(f1),'final_inventory':p,'final_manifest':m,'public_allowlist':al,'private_files_excluded':58,'mandatory_companion':'public/NORMALIZATION_CLARIFICATION.md','retained_files':[{'path':n,**pin(B/n)} for n in sorted(seen)],'source_script':pin(Path(__file__))};o.write_text(json.dumps(out,indent=2)+'\n');o.chmod(0o444);print(out['status'])
