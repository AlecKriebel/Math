from pathlib import Path
import json,os
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');base=P/'papers/23411227';own=P/'verification/fano-root-evidence-custody-sol-20261117';print('OWN_EXISTS',own.exists())
for rel in ['sources','reviews/root-initial-20261117','reviews/adversarial-sol','reviews/scope-sol']:
 p=base/rel;nf=nd=0
 for _,ds,fs in os.walk(p):nf+=len(fs);nd+=len(ds)
 print('ROOT',rel,nf,nd,'TOPFILES',[x.name for x in p.iterdir() if x.is_file()])
 for name in ['SOURCE_FINAL.json','SOURCE_MANIFEST.json','INITIAL_SEAL.json','INITIAL_MANIFEST.json','FINAL.json','OWNED_MANIFEST.json']:
  f=p/name
  if not f.exists():continue
  d=json.loads(f.read_bytes());print('CONTROL',rel+'/'+name,'TYPE',type(d).__name__,'KEYS',list(d) if isinstance(d,dict) else len(d))
  if not isinstance(d,dict):continue
  for k,v in d.items():
   if k in ['files','payloads','payload_files','payload_pins','owned_files']:
    print('PAYLOAD_FIELD',k,type(v).__name__,len(v),'FIRST',str(v[0] if isinstance(v,list) else next(iter(v.items())))[:700],'LAST',str(v[-1] if isinstance(v,list) else list(v.items())[-1])[:700])
   elif any(w in k.lower() for w in ['extent','directory','directories','mode','exclu','terminal','manifest','self_hash','execution','native','source_pin','initial_seal']):
    if len(str(v))<5000:print(k,json.dumps(v))
