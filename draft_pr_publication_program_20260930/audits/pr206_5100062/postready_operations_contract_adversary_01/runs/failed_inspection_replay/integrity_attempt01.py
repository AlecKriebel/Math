from pathlib import Path
import hashlib,json
b=Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr206_5100062/publication_operations_preparation_02')
refs={'SAFE_MANIFEST_02.json':(14220,'d4f432fe81a61ad74ce6b658faeb6ffcddd8ca7de92b744e96bfda04ad15d8fe'),'SEAL_02.json':(2519,'dfec8f531253e0e76cfbc2dfa4827bbee01e636a7305ac027783b4245fac11d6'),'ADOPTION_SOURCE_MAP_ONLY.json':(837,'8483bc7f5dd448ccf12526c10e1a314e16cf1b2d9f34429b58e2117e4177c171'),'verifier02.py':(3356,'faf716cc461a7e347b4ebc3bb553d0fda72800bd4d823c5fa9acda26ebbdeb0d')}
for name,(n,h) in refs.items():
 raw=(b/name).read_bytes()
 if len(raw)!=n or hashlib.sha256(raw).hexdigest()!=h:raise RuntimeError('integrity ref pin differs '+name)
 print(name,'PIN MATCH')
 if name=='SAFE_MANIFEST_02.json':
  m=json.loads(raw);print('MANIFEST KEYS',list(m));print('MANIFEST NONFILES',json.dumps({k:v for k,v in m.items() if not isinstance(v,dict) or len(v)<10},sort_keys=True));print('MAPPING CANDIDATES',[(k,len(v)) for k,v in m.items() if isinstance(v,dict)])
 elif name.endswith('.json'):print(raw.decode())
 else:
  for i,l in enumerate(raw.decode().splitlines(),1):print(f'{i:04}: {l}')
