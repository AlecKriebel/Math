from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O=P/'verification/root-six-original-INITIAL-authentication-20261117.json'
assert not O.exists()
specs=[
 ('23318851','root-initial-20261117',22,0,'b213e33ab531d1e98a4ec3ea30bedf7745e049abb753f52f07b71850b4b21653','0f723c3fc47c9ea18c486f3a3a3ba6aaaa2c032117993e67b32afe17c2ff2ae5'),
 ('23318851','adversarial-sol',18,1,'dbb198866601fd68216f11628a508407e5a98d90c8228204f2e3d72ae39c20e6','9e314a96b491a96f18ad3cdaa1cdcc9c1c3c125e69a16bbb3a60fae5e8cf4d86'),
 ('23318851','scope-sol',24,0,'d8c5cae0c0a22d22b33f42650d0a6f5481cf7c65f4723e2256e854035a3450e7','4577c9660992856d5762f93019d92ff4a4f144d27b1696c28beefbe7b5fce7e6'),
 ('23204212','root-initial-20261117',21,0,'6d7391ebdb60c59b7b622c6fbd5a60c320f2c22bf8fc49ee02908e05d187537e','3abdabfd35529755468a8f489afbee537b3b82d26b8743434f69a9878b5e5993'),
 ('23204212','adversarial-sol',18,0,'25ce42f37df872ba62a7bd5e33d017133217e1e1854735a48f7c439ee3a13590','1736dd12f41d54b4b1177114d1c4f5e47400ff9e8d48f66616ff8a86ded6cda7'),
 ('23204212','scope-sol',37,1,'fa6bb1278a64cc254daf3d8e06ca05b6707cc24e4784b5752b901dcb0bd10550','43cf3fa2f6135f43581e09fef77ce811d481d535eaf23f2827a443c2c9b746a9')]
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
verified=[]
for rec,lane,files,dirs,mpin,spin in specs:
 root=P/'papers'/rec/'reviews'/lane
 pins={'INITIAL_MANIFEST.json':mpin,'INITIAL_SEAL.json':spin}
 for n,pin in pins.items():assert sha(root/n)==pin,(rec,lane,n)
 m=json.loads((root/'INITIAL_MANIFEST.json').read_text())
 if 'entries' in m:entries=m['entries']
 elif 'payload' in m:entries=m['payload']+m['terminal_controls']
 else:entries=[dict(e,kind='file') for e in m['payload_files']]+[dict(e,kind='directory') for e in m['directories']]+[dict(e,kind='file') for e in m['terminal_control_topology']]+[{'path':'.','kind':'directory','mode':m['root_mode']}]
 expected={e['path']:e for e in entries};assert len(expected)==len(entries)
 actual={'.':root};actual.update({str(f.relative_to(root)):f for f in root.rglob('*')})
 assert set(actual)==set(expected),(rec,lane,set(actual)^set(expected))
 payload=[];nf=nd=0
 for n,f in sorted(actual.items()):
  e=expected[n];st=f.stat();assert not f.is_symlink()
  assert f.is_dir()==(e['kind']=='directory')
  assert stat.S_IMODE(st.st_mode)==int(e.get('mode',e.get('mode_octal')),8),(rec,lane,n,'mode')
  if 'mtime_ns' in e:assert st.st_mtime_ns==e['mtime_ns'],(rec,lane,n,'mtime')
  if f.is_dir():
   nd+=n!='.'
   if 'empty' in e:assert (not any(f.iterdir()))==e['empty']
  else:
   nf+=1;data=f.read_bytes();digest=hashlib.sha256(data).hexdigest()
   if 'bytes' in e:assert len(data)==e['bytes'],(rec,lane,n,'size')
   pin=e.get('SHA256',e.get('sha256'))
   if pin not in [None,'EXCLUDED_TERMINAL_RECURSIVE_HASH']:assert digest==pin,(rec,lane,n,'SHA')
   else:assert n in pins and digest==pins[n],(rec,lane,n,'terminal')
   if 'MD5' in e:assert hashlib.md5(data).hexdigest()==e['MD5']
   if 'empty' in e:assert (len(data)==0)==e['empty']
   payload.append({'path':n,'bytes':len(data),'SHA256':digest,'mode':oct(stat.S_IMODE(st.st_mode))})
 assert (nf,nd)==(files,dirs),(rec,lane,nf,nd)
 verified.append({'record_id':rec,'lane':lane,'files':nf,'childdirs':nd,'manifest_SHA256':mpin,'seal_SHA256':spin,'payload':payload})
result={'UTC':datetime.now(timezone.utc).isoformat(),'status':'SIX_FROZEN_ORIGINAL_ONLY_INITIALS_AUTHENTICATED','files':sum(x['files'] for x in verified),'childdirs':sum(x['childdirs'] for x in verified),'packets':verified,'peer_mathematical_texts_opened':False,'root_original_gate_complete':True,'primary_support_scientific_exposure_before_checkpoint':0,'scientific_verdict':None,'follow_up':None,'next_gate':'Scoped checkpoint then explicit continuation; no original INITIAL writes'}
O.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'files':result['files'],'childdirs':result['childdirs'],'receipt_SHA256':sha(O)}))
