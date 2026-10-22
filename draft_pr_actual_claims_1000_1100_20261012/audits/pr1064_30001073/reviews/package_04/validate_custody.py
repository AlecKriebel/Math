from pathlib import Path
import json,hashlib,collections,struct,zlib,datetime
O=Path(__file__).resolve().parent;A=O.parent.parent;P=A/'preprint_v1_0'
def req(c,m):
 if not c:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
freeze=json.loads((O/'PREEXISTING_AUDIT_FREEZE.json').read_text())['files'];byhash=collections.defaultdict(list)
for r in freeze:byhash[(r['bytes'],r['sha256'])].append(A/r['path'])
baseline=json.loads((A/'repairs/case_alias01/INPUT_PINS.json').read_text())['records'];ledger=json.loads((A/'repairs/case_alias01/PRIOR_PIN_RESOLUTIONS.json').read_text());decl={m['manifest']['path']:m for m in ledger['manifests']}
labels=['path','snapshot_path','source_path','package_path','image','name'];njson=0;nrefs=0;resolved=0;omissions=[];permanifest=[]
for r in baseline:
 matches=byhash[(r['bytes'],r['sha256'])];req(bool(matches),'baseline no retained artifact '+r['path'])
 actual=next((p for p in matches if p==A/r['path']),matches[0])
 if actual.suffix!='.json':continue
 try:obj=json.loads(actual.read_text())
 except (ValueError,UnicodeError):continue
 njson+=1;refs=[]
 def walk(x,loc='$'):
  if isinstance(x,dict):
   if isinstance(x.get('sha256'),str) and len(x['sha256'])==64 and any(isinstance(x.get(k),str) for k in labels):
    ref={'locator':loc,'identifiers':{k:x[k] for k in labels if k in x},'sha256':x['sha256']};size=x.get('bytes',x.get('size'))
    if isinstance(size,int):ref['bytes']=size
    refs.append(ref)
   for k,v in x.items():walk(v,loc+'/'+k)
  elif isinstance(x,list):
   for k,v in enumerate(x):walk(v,loc+'/'+str(k))
 walk(obj)
 if not refs:continue
 m=decl[r['path']];req(m['manifest']==r,'original manifest pin');req(sha(A/m['resolved_manifest_path'])==r['sha256'],'manifest artifact identity');req(len(refs)==len(m['records']),'reference coverage')
 for expected,record in zip(refs,m['records']):
  nrefs+=1
  req(all(record[k]==v for k,v in expected.items()),'exact reference metadata')
  if record['status']=='RESOLVED_EXACT_RETAINED_BYTES':
   p=A/record['resolved_path'];req(p.is_file() and sha(p)==record['sha256'],'resolution bytes');req(p.stat().st_size==record['actual_bytes'],'resolution size')
   if 'bytes' in record:req(p.stat().st_size==record['bytes'],'requested size')
   resolved+=1
  else:
   matches=[p for (size,digest),paths in byhash.items() if digest==record['sha256'] and ('bytes' not in record or size==record['bytes']) for p in paths];req(not matches,'supposed omission resolves')
   omissions.append(dict(manifest=r['path'],**record))
 permanifest.append({'manifest':r['path'],'actual_artifact':m['resolved_manifest_path'],'bytes':r['bytes'],'sha256':r['sha256'],'references':len(refs)})
req(njson==487 and nrefs==14818 and resolved==14813 and len(omissions)==5,'historical counts')
req(omissions==json.loads((A/'repairs/case_alias01/INDIVIDUAL_OMISSIONS.json').read_text())['records'],'individual omissions exact')
# All current package pins and repaired outputs, independently read every row.
current=json.loads((A/'repairs/case_alias01/FINAL_CURRENT_PINS.json').read_text())
print('current keys',list(current))
for field in ['records','entries']:
 if field in current:cur=current[field];break
for r in cur:
 p=P/r['path'];req(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'current repaired pin '+r['path'])
outputs=json.loads((A/'repairs/case_alias01/OUTPUT_PINS.json').read_text())['entries']
for r in outputs:
 p=A/'repairs/case_alias01'/r['path'];req(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'repair output '+r['path'])
# Raw CLOSED ZIP parse with no prefix, inter-member gaps, hidden extras or trailer.
b=(P/'support.zip').read_bytes();pos=0;locals=[]
while b[pos:pos+4]==b'PK\x03\x04':
 fields=struct.unpack_from('<I5H3I2H',b,pos);_,need,flags,method,time,date,crc,cs,us,nl,xl=fields
 name=b[pos+30:pos+30+nl].decode();data=b[pos+30+nl+xl:pos+30+nl+xl+cs];plain=zlib.decompress(data,-15)
 req(need==20 and flags==0 and method==8 and time==0 and date==((2026-1980)<<9 |10<<5|14) and xl==0,'raw local header')
 req(len(plain)==us and zlib.crc32(plain)&0xffffffff==crc and plain==(P/name).read_bytes(),'raw deflate/CRC/payload')
 locals.append((name,pos,crc,cs,us));pos+=30+nl+xl+cs
central=pos;centralrows=[]
while b[pos:pos+4]==b'PK\x01\x02':
 f=struct.unpack_from('<I6H3I5H2I',b,pos)
 _,made,need,flags,method,time,date,crc,cs,us,nl,xl,cl,disk,internal,external,offset=f
 name=b[pos+46:pos+46+nl].decode();req(made==(3<<8|20) and need==20 and flags==0 and method==8 and time==0 and date==((2026-1980)<<9|10<<5|14) and xl==0 and cl==0 and disk==0 and internal==0 and external==0o100644<<16,'raw central header')
 centralrows.append((name,offset,crc,cs,us));pos+=46+nl+xl+cl
req(locals==centralrows,'all local/central records')
eocd=struct.unpack_from('<I4H2IH',b,pos);req(eocd==(0x06054b50,0,0,198,198,pos-central,central,0) and pos+22==len(b),'raw exact EOCD/no trailer')
req([r[0] for r in locals]==json.loads((P/'SUPPORT_ALLOWLIST.json').read_text())['members'],'raw complete member order')
(O/'HISTORICAL_CUSTODY_RECHECK.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_artifacts_retained':len(baseline),'valid_original_JSON':njson,'reference_occurrences':nrefs,'resolved_exact_bytes':resolved,'unsupported_occurrences':omissions,'individually_rechecked_manifests':permanifest,'current_repair_pins_rehashed':len(cur),'repair_outputs_rehashed':len(outputs),'raw_CLOSED_ZIP_all_headers_payloads_CRCS_exact':True,'raw_ZIP_member_count':len(locals),'historical_replay_claim':False,'historical_unsupported_digest_recreated':False},indent=2)+'\n')
print('PASS',nrefs,'references;',resolved,'exact;',len(omissions),'individually unsupported;',len(cur),'current pins;',len(outputs),'repair outputs')
