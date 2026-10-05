#!/usr/bin/env python3
"""Bounded KOU-21.90 v1-to-v2 editorial-delta verification.

Usage: python verify_delta.py V1_AUTHOR.zip V2_AUTHOR.zip ORIGINAL_AUDIT.zip
Read-only inputs; prints deterministic acceptance metadata. Standard library.
"""
import difflib,hashlib,json,sys,zipfile
from pathlib import Path

PINS={
 'v1':'2c4530b0d0daf358e64d8e701ee739bbe97d5a83fa87037a2a2e5d1b47643bba',
 'v2':'f4f6c13056b5053795c076b6a62f61930e3b757a181c4ffa0bed00f23dc4e5f5',
 'audit':'a6ff5aecfe81e64af531953837b8ce60b72bcf1a609080e5386c9f37f47dd845',
 'v2_manifest':'15ce6b84aa22e1c5d217bf6fbe82e6768fbf2e27c654df6bbd7846f3360ed89c',
 'patch':'5da0af578c19592c526e01e7bf4e0713f716a88d1590750faaa962e26ac3b07a',
 'corrections':'8e3dd393c2cdb4ed0d9f96c11259fd4ef8baf962aeaa45c1de9ad2bc5c4a1b86',
}

def digest(b): return hashlib.sha256(b).hexdigest()

def load(path,pin):
 b=Path(path).read_bytes();assert digest(b)==pin
 with zipfile.ZipFile(path) as z:
  names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None
  assert all(Path(n).name==n and not n.endswith('/') for n in names)
  for info in z.infolist(): assert ((info.external_attr>>16)&0o170000)!=0o120000
  return {n:z.read(n) for n in names},len(b)

def manifest(files,name):
 m=json.loads(files[name]);seen=set()
 for f in m['files']:
  n=f['name'];assert n not in seen;seen.add(n)
  assert n in files and len(files[n])==f['bytes'] and digest(files[n])==f['sha256']
 assert seen|{name}==set(files)
 return m

def main(paths):
 assert len(paths)==3,'Need v1 author, v2 author and original audit ZIP paths'
 v1,bytes1=load(paths[0],PINS['v1']);v2,bytes2=load(paths[1],PINS['v2']);audit,auditbytes=load(paths[2],PINS['audit'])
 m1=manifest(v1,'AUTHOR_MANIFEST.json');m2=manifest(v2,'AUTHOR_MANIFEST.json');ma=manifest(audit,'AUDIT_MANIFEST.json')
 assert digest(v2['AUTHOR_MANIFEST.json'])==PINS['v2_manifest']
 assert digest(v2['V1_TO_V2.patch'])==PINS['patch']
 assert digest(audit['REQUIRED_CORRECTIONS.json'])==PINS['corrections']
 corrections=json.loads(audit['REQUIRED_CORRECTIONS.json'])
 assert len(corrections['replacements'])==5 and corrections['mathematical_corrections']==[]
 payload=set(v1)-{'AUTHOR_MANIFEST.json'}
 expected={n:v1[n] for n in payload}
 for r in corrections['replacements']:
  old,new=r['old'].encode(),r['new'].encode();assert expected[r['file']].count(old)==1
  expected[r['file']]=expected[r['file']].replace(old,new)
 paragraphs=expected['README.md'].decode().split('\n\n')
 assert paragraphs[1].startswith('**Disposition:') and paragraphs[1].endswith('**')
 paragraphs.insert(2,corrections['additional_required_sentence'])
 expected['README.md']='\n\n'.join(paragraphs).encode()
 for n in payload: assert v2[n]==expected[n],n
 changed=sorted(n for n in payload if v1[n]!=v2[n]);unchanged=sorted(payload-set(changed))
 assert changed==['README.md','RESEARCH_LOG.md','SOURCE_VERIFICATION.json']
 assert set(v2)-set(v1)=={'V1_TO_V2.patch','VERSION_PROVENANCE.json'}
 assert not set(v1)-set(v2)
 expected_diff=''.join(''.join(difflib.unified_diff(v1[n].decode().splitlines(True),v2[n].decode().splitlines(True),fromfile='v1/'+n,tofile='v2/'+n)) for n in changed).encode()
 assert expected_diff==v2['V1_TO_V2.patch']
 provenance=json.loads(v2['VERSION_PROVENANCE.json'])
 assert provenance['replacements']==corrections['replacements']
 assert provenance['added_sentence']==corrections['additional_required_sentence']
 assert sorted(provenance['changed_original_payload_files'])==changed
 assert sorted(provenance['unchanged_original_payload_files'])==unchanged
 for key,data in [('original_manifest',v1['AUTHOR_MANIFEST.json']),('required_corrections',audit['REQUIRED_CORRECTIONS.json']),('exact_content_diff',v2['V1_TO_V2.patch'])]:
  assert provenance[key]['bytes']==len(data) and provenance[key]['sha256']==digest(data)
 for key,length,pin in [('original_archive',bytes1,PINS['v1']),('audit_archive',auditbytes,PINS['audit'])]:
  assert provenance[key]['bytes']==length and provenance[key]['sha256']==pin
 assert provenance['original_preserved'] is True and provenance['remote_writes'] is False
 # Manifest differences are limited to revision bookkeeping and updated pins.
 common=set(m1)|set(m2)
 allowed={'files','author_freeze','independent_audit','version'}
 assert all(m1.get(key)==m2.get(key) for key in common-allowed)
 assert m2['version']=='v2'
 result={'verdict':'PASS_V2_DELTA_ACCEPTED','problem_id':2599,'problem_number':'KOU-21.90','rank':770,'v1_archive':{'bytes':bytes1,'sha256':PINS['v1']},'v2_archive':{'bytes':bytes2,'sha256':PINS['v2'],'manifest_sha256':PINS['v2_manifest']},'original_audit_archive_sha256':PINS['audit'],'patch_sha256':PINS['patch'],'exact_required_replacements':5,'clarification_sentences_added':1,'changed_original_payload_files':changed,'unchanged_original_payload_files':unchanged,'new_files':['V1_TO_V2.patch','VERSION_PROVENANCE.json'],'math_proofs_code_certificates_outputs_unchanged':True,'remaining_required_corrections':[],'original_archive_preserved':True,'original_audit_preserved':True,'remote_writes':False,'scope':'Accepts only this pinned editorial revision and inherits the original mathematical audit. Connected/nondegenerate interpretation remains unresolved; 5/5 approaches. No novelty or solved-status claim.'}
 print(json.dumps(result,indent=2))

if __name__=='__main__': main(sys.argv[1:])
