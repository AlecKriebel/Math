from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OUT=P/'papers/23318851/reviews/root-continuation-20261117/FINAL_EVIDENCE_AUTHENTICATION.json'
assert not OUT.exists()
specs=[
 ('papers/23318851/sources','SOURCE_MANIFEST.json',95,16,{'SOURCE_MANIFEST.json':'ed5c217040b7a0d72df7de7ef1d5cbce9bc516ab32c1f20ed6466ef153a6bac8','SOURCE_FINAL.json':'c61fb0473f0954877ab5af49e7b6139732eb4afab7cfab3377864a91dd98b317'}),
 ('papers/23318851/reviews/root-initial-20261117','INITIAL_MANIFEST.json',22,0,{'INITIAL_MANIFEST.json':'b213e33ab531d1e98a4ec3ea30bedf7745e049abb753f52f07b71850b4b21653','INITIAL_SEAL.json':'0f723c3fc47c9ea18c486f3a3a3ba6aaaa2c032117993e67b32afe17c2ff2ae5'}),
 ('papers/23318851/reviews/adversarial-continuation-20261117','FINAL_MANIFEST.json',98,10,{'FINAL_MANIFEST.json':'d7a25669b161de9b9a4edbf255b9d4ba7e9039c9bdadab25b4196c1c475549ee','FINAL_SEAL.json':'26b2ed0e66948b646f75f0af0f8639442521666d5559c2b9198c2faf88d8a575','FINAL.json':'36b1566daecee13a9dc32b20e312429e8c71b5f714631dd2a09b7d1e9cf9c0fe'}),
 ('papers/23318851/reviews/scope-continuation-20261117','FINAL_MANIFEST.json',94,2,{'FINAL_MANIFEST.json':'8151c0d1ce9dbdc96099a9f177c006e9a103cf7dbd5621e6c297aaaadbfa5f39','FINAL_SEAL.json':'7837aca7bf2ace94305e21b1a6db18abb3237d04f0e5a310a0a47fd59e74705a'}),
 ('papers/23318851/reviews/followup-ghz11-adversarial-sol','MANIFEST.json',56,1,{'MANIFEST.json':'4744d3ca147157d05e45af2c4c0ceb5659f12cc7e647d755fcf8edc12e66368e','FINAL.json':'d0a6671355886e39dd1bcc7cf12670c1e01e740b3f96edead4b89f6d02c3b933'}),
 ('verification/mink-riesz-k3-stage-sol-20261117','OWNED_MANIFEST.json',1635,770,{'OWNED_MANIFEST.json':'cd6b884ff5efce7c5873307cdc7bf308b72c801c3ba5868660ba261dcc22c8dc','FINAL.json':'2aa8bb250f77212d60903f69f64390f86a8ce7544218453b2d169c957d8e588f'})]
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
results=[]
for rel,mname,nf,nd,pins in specs:
 root=P/rel
 for n,pin in pins.items():assert sha(root/n)==pin,(rel,n)
 m=json.loads((root/mname).read_text())
 if 'entries' in m:entries=m['entries'][:]
 elif 'payload' in m:entries=m['payload'][:]+m['terminal_controls']
 else:
  entries=[dict(e,kind='file') for e in m['payload_files']]+[dict(e,kind='directory') for e in m['directories']]
  entries += [dict(e,kind='file') for e in m.get('terminal_controls',[])]
  if not any(e['path']=='.' for e in entries):entries.append({'path':'.','kind':'directory','mode':m['root_mode']})
 for n,mode in m.get('terminal_modes',{}).items():entries.append({'path':n,'kind':'file','mode':mode})
 for e in m.get('terminal_control_topology',[]):entries.append(e)
 expected={e['path']:e for e in entries};assert len(expected)==len(entries),(rel,'duplicate')
 actual={'.':root};actual.update({str(f.relative_to(root)):f for f in root.rglob('*')})
 assert set(actual)==set(expected),(rel,set(actual)^set(expected))
 files=dirs=0;rows=[]
 for n,f in sorted(actual.items()):
  e=expected[n];st=f.stat();assert not f.is_symlink()
  assert f.is_dir()==(e['kind']=='directory') and stat.S_IMODE(st.st_mode)==int(e.get('mode',e.get('mode_octal')),8),(rel,n,'type/mode')
  if f.is_dir():
   dirs+=n!='.'
   if 'empty' in e:assert (not any(f.iterdir()))==e['empty'],(rel,n,'emptydir')
   rows.append({'path':n,'kind':'directory','mode':oct(stat.S_IMODE(st.st_mode))})
  else:
   files+=1;b=f.read_bytes();digest=hashlib.sha256(b).hexdigest()
   if 'bytes' in e:assert len(b)==e['bytes'],(rel,n,'size')
   pin=e.get('SHA256',e.get('sha256'))
   if pin not in [None,'EXCLUDED_TERMINAL_RECURSIVE_HASH']:assert digest==pin,(rel,n,'SHA')
   else:assert n in pins and digest==pins[n],(rel,n,'unboundcontrol')
   if 'MD5' in e:assert hashlib.md5(b).hexdigest()==e['MD5']
   if 'md5' in e:assert hashlib.md5(b).hexdigest()==e['md5']
   if 'empty' in e:assert (not b)==e['empty'],(rel,n,'emptyfile')
   rows.append({'path':n,'kind':'file','bytes':len(b),'SHA256':digest,'mode':oct(stat.S_IMODE(st.st_mode))})
 assert (files,dirs)==(nf,nd),(rel,files,dirs)
 results.append({'root':rel,'files':files,'childdirs':dirs,'pins':pins,'complete_actual_objects':rows})
assert sum(x['files'] for x in results)==2000 and sum(x['childdirs'] for x in results)==799
result={'UTC':datetime.now(timezone.utc).isoformat(),'status':'FRESH_FINITE_CUSTODY_AUTHENTICATED','files':2000,'childdirs':799,'packets':results,'scientific_disposition_not_inferred_from_hashing':True,'original_source_and_INITIALs_unmodified':True,'third_party_primary_copies_are_private':True,'routine_readonly_schema_discovery_error':'Initial len(int) while printing metadata schema; no writes, source/scientific execution or scientific route; subsequent typed schema discovery read actual heterogeneous forms. Not a manuscript defect.','scientific_execution_by_this_reader':False,'follow_up':None,'publication_authority':False}
OUT.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'files':2000,'childdirs':799,'receipt_SHA256':sha(OUT)}))
