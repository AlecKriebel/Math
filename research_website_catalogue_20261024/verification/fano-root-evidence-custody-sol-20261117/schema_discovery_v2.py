"""Typed schema metadata only; never infer container type from a field name."""
from pathlib import Path
import json,datetime
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');BASE=P/'papers/23411227';OWN=P/'verification/fano-root-evidence-custody-sol-20261117'
rows=[]
payload_names={'files','payloads','payload_files','payload_pins','owned_files'}
meta_words=['extent','directory','directories','mode','exclu','terminal','manifest','self_hash','execution','native','source_pin','initial_seal','initial_packet','immutable_initial']
for rel in ['sources','reviews/root-initial-20261117','reviews/adversarial-sol','reviews/scope-sol']:
 for name in ['SOURCE_FINAL.json','SOURCE_MANIFEST.json','INITIAL_SEAL.json','INITIAL_MANIFEST.json','FINAL.json','OWNED_MANIFEST.json']:
  p=BASE/rel/name
  if not p.is_file():continue
  data=json.loads(p.read_bytes());entry=dict(path=str(p),root_type=type(data).__name__)
  if isinstance(data,dict):
   entry['keys']=list(data);fields={}
   for key,value in data.items():
    if key in payload_names:
     info=dict(type=type(value).__name__)
     if isinstance(value,(list,dict)):
      info['container_length']=len(value)
      if isinstance(value,list) and value:info['first']=value[0];info['last']=value[-1]
      elif isinstance(value,dict) and value:info['first_item']=next(iter(value.items()));info['last_item']=list(value.items())[-1]
     else:info['typed_scalar_value']=value
     fields[key]=info
    elif any(word in key.lower() for word in meta_words):
     if isinstance(value,dict):fields[key]=dict(type='dict',keys=list(value))
     elif isinstance(value,list):fields[key]=dict(type='list',container_length=len(value),value=value if len(json.dumps(value))<2500 else 'LARGE_CONTAINER_KEYS_ONLY')
     else:fields[key]=dict(type=type(value).__name__,typed_scalar_value=value)
   entry['selected_metadata_fields']=fields
  elif isinstance(data,list):entry['container_length']=len(data)
  else:entry['typed_scalar_value']=data
  rows.append(entry)
result=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Only actual control schemas and metadata; no family scientific findings interpreted',controls=rows)
with (OWN/'SCHEMA_DISCOVERY_V2.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
