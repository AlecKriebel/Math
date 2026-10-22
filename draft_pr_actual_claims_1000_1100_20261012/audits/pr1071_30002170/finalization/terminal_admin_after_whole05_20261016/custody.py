from pathlib import Path
import json,hashlib,collections,stat,datetime,struct,zlib,io,zipfile
R=Path(__file__).resolve().parent; A=R.parents[1]; P=A/'NEWpreprint_v1_0'
cache={};documents={};checked=[];resolution_events=[];identity_index=collections.defaultdict(list)
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def load(path):
 path=Path(path);path=path if path.is_absolute()else A/path
 if str(path)not in documents:documents[str(path)]=json.loads(path.read_text())
 return documents[str(path)]
def identity(path):
 path=Path(path);path=path if path.is_absolute()else A/path
 if str(path)not in cache:
  need(path.is_file()and not path.is_symlink(),'Missing/nonregular '+str(path))
  b=path.read_bytes();cache[str(path)]=(len(b),hashlib.sha256(b).hexdigest())
 return cache[str(path)]
def size(row):return row.get('bytes',row.get('size'))
def relpath(path):return str(path.relative_to(A)) if path.is_relative_to(A) else str(path)
def check(path,row,label):
 path=Path(path);path=path if path.is_absolute()else A/path
 expected=(size(row),row['sha256']);actual=path
 def exact(p):
  if not p.is_file() or p.is_symlink():return False
  b=p.read_bytes();return (len(b),hashlib.sha256(b).hexdigest())==expected
 if not exact(actual):
  options=identity_index[expected];need(bool(options),'No exact retained bytes '+label+' '+str(path))
  actual=options[0];need(exact(actual),'Resolved bytes mismatch '+label)
 else:need(exact(actual),'Individual repeat rehash mismatch')
 cache[str(actual)]=expected
 checked.append((label,str(actual),size(row),row['sha256']))
 resolution_events.append({'label':label,'captured_locator':str(path.relative_to(A)) if path.is_relative_to(A) else str(path),'current_exact_resolution':relpath(actual) if actual.is_relative_to(A) else str(actual),'bytes':size(row),'sha256':row['sha256']})
 return actual

def rows(d):
 if type(d)is list:return d
 for key in ['records','files','rows','unchanged_records']:
  if type(d.get(key))is list:return d[key]
 raise RuntimeError('Unknown pin schema '+str(list(d)))
def source_check(row):
 source=rows(load(row['source_manifest']))
 i=row.get('source_row_index',row.get('row_index'));original=source[i]
 need((size(original),original['sha256'])==(size(row),row['sha256']),'Source row identity drift')
 path=original.get('path',original.get('original_path'))
 need(path==row.get('captured_path',row.get('path')),'Source captured locator drift '+row['source_manifest'])
 return original
# Build a full exact before/current index from this terminal baseline, never via symlink parents.
terminalbase=rows(load(R/'BASELINE_INPUT_PINS.json'));terminalbefore=rows(load(R/'BEFORE_PINS.json'));terminalbeforemap={r['original_path']:r for r in terminalbefore}
for row in terminalbase:
 path=A/(terminalbeforemap[row['path']]['before_snapshot'] if row['path'] in terminalbeforemap else row['path'])
 need(path.is_file() and not path.is_symlink(),'Terminal retained baseline absent')
 b=path.read_bytes();need((len(b),hashlib.sha256(b).hexdigest())==(size(row),row['sha256']),'Terminal retained baseline identity')
 identity_index[(size(row),row['sha256'])].append(path)
terminalrows=[]
for idx,row in enumerate(terminalbase):
 path=A/(terminalbeforemap[row['path']]['before_snapshot'] if row['path'] in terminalbeforemap else row['path'])
 actual=check(path,row,'terminal-baseline/'+str(idx));need(stat.S_IMODE(actual.stat().st_mode)==row['mode'] and actual.stat().st_nlink==row['nlink'],'Terminal baseline mode/nlink drift')
 terminalrows.append({'source_manifest':str((R/'BASELINE_INPUT_PINS.json').relative_to(A)),'source_row_index':idx,**row,'before_snapshot':terminalbeforemap.get(row['path'],{}).get('before_snapshot'),'current_exact_resolution':relpath(actual)})
for row in rows(load(R/'PREEXISTING_SYMLINK_FIXTURES.json')):
 p=A/row['path'];need(p.is_symlink() and __import__('os').readlink(p)==row['target'],'Preexisting link target drift')
(R/'TERMINAL_BASELINE_RECONCILIATION.json').write_text(json.dumps({'status':'PASS','records':terminalrows,'changed_existing':8,'protected_existing':len(terminalbase)-8,'preexisting_fixture_links_unchanged':6},indent=2)+'\n')
hist=load('repairs/history_order01/HISTORICAL_STAGE_RESOLUTION.json')['records'];locators=0;sourcegroups=collections.defaultdict(list)
terminalhist=[]
for idx,row in enumerate(hist):
 need(row['global_index']==idx,'Historical global index')
 source_check(row);sourcegroups[row['source_manifest']].append(row['source_row_index'])
 terminal_locs=[]
 for loc in row['locators']:
  actual=check(loc['current_exact_resolution'],row,'history/'+str(idx)+'/'+loc['field']);locators+=1
  terminal_locs.append({**loc,'terminal_current_exact_resolution':relpath(actual)})
 terminalhist.append({**row,'terminal_exact_locator_resolutions':terminal_locs})
for path,indices in sourcegroups.items():need(indices==list(range(len(rows(load(path))))),'Incomplete historical source '+path)
(R/'HISTORICAL_STAGE_RESOLUTION.json').write_text(json.dumps({'status':'PASS','scope':'All4346 original structured rows and source-array indices retained, all11480 named locators individually rehashed with new exact terminal before/current resolutions. Original fields are preserved.','records':terminalhist},indent=2)+'\n')
additional={}
for name in ['PRIOR_LATER_PIN_RESOLUTION.json','LATEST_STAGE_PIN_RESOLUTION.json']:
 rs=load('repairs/history_order01/'+name)['records'];groups=collections.defaultdict(list);terminal_later=[]
 for row in rs:
  source_check(row);i=row.get('source_row_index',row.get('row_index'));groups[row['source_manifest']].append(i)
  actual=check(row['current_exact_resolution'],row,name+'/'+str(i));terminal_later.append({**row,'terminal_current_exact_resolution':relpath(actual)})
 for path,indices in groups.items():need(indices==list(range(len(rows(load(path))))),'Incomplete later source '+path)
 additional[name]=len(rs)
 (R/name).write_text(json.dumps({'status':'PASS','scope':'Every original structured row/source manifest/index/locator preserved; exact terminal resolution appended.','records':terminal_later},indent=2)+'\n')
copies=load('NEWpreprint_v1_0/INPUT_COPY_MAP.json')['copies']
for i,row in enumerate(copies):
 source=row.get('source_snapshot',row['original_path']);check(source,row,'copy-source/'+str(i));check(P/row['package_copy'],row,'copy-destination/'+str(i))
 need((A/source).read_bytes()==(P/row['package_copy']).read_bytes(),'Source/copy bytes unequal')
prefixes={}
for prefix,name in [(50,'history/preparation01'),(83,'history/whole02_candidate'),(116,'history/pre_case_alias01'),(128,'history/pre_portability01'),(140,'history/pre_history_order01'),(153,'history/pre_terminal_after_whole05')]:
 old=load(P/name/'INPUT_COPY_MAP.json')['copies'];need(len(old)==prefix and copies[:prefix]==old,'Copy prefix '+str(prefix));prefixes[str(prefix)]=True
old140=load(P/'history/pre_history_order01/INPUT_COPY_MAP.json')['copies'];need(copies[:140]==old140,'Immediate140 prefix')
omissions=load('repairs/history_order01/INDIVIDUAL_OMISSIONS_RECHECK.json')['records'];omissiongroups=collections.defaultdict(list)
for i,row in enumerate(omissions):
 check(row['current_exact_resolution'],row,'omission/'+str(i));need(bool(row['reason']),'Omission reason absent');omissiongroups[row['ledger']].append(row)
for name,rs in omissiongroups.items():
 doc=load(P/name);candidates=[]
 for value in doc.values():
  if type(value)is list and value and type(value[0])is dict and 'sha256'in value[0]:candidates.extend(value)
 need(len(candidates)==len(rs),'Omission individual count '+name)
 for old,row in zip(candidates,rs):need((old.get('path'),size(old),old['sha256'])==(row['path'],size(row),row['sha256']),'Omission source row '+name)
base=rows(load('repairs/history_order01/BASELINE_INPUT_PINS.json'));before=rows(load('repairs/history_order01/BEFORE_PINS.json'));protected=rows(load('repairs/history_order01/PROTECTED_UNCHANGED.json'))
beforemap={r['original_path']:r for r in before}
for row in base:check(beforemap[row['path']]['before_snapshot']if row['path']in beforemap else row['path'],row,'repair-baseline')
for row in before:check(row['before_snapshot'],row,'repair-before')
for row in protected:check(row['path'],row,'repair-protected')
need(len(base)==987 and len(before)==8 and len(protected)==979,'Repair coverage counts')
need({r['path']for r in protected}=={r['path']for r in base}-{r['original_path']for r in before},'Baseline partition')
for name,root in [('OUTPUT_PINS.json',A/'repairs/history_order01'),('CURRENT_AUDIT_PINS.json',A),('CURRENT_CANDIDATE_PINS.json',P)]:
 for row in rows(load(A/'repairs/history_order01'/name)):check(root/row['path'],row,'current-repair/'+name)
# Independently recompute historical ordering rather than trusting counts.
case=load('repairs/case_alias01/HISTORICAL_STAGE_RESOLUTION.json');port=load('repairs/portability01/HISTORICAL_STAGE_RESOLUTION.json');q=load(P/'HISTORY_ORDER_QUALIFICATION.json')
keys=['stage','captured_path','bytes','sha256']
project=lambda rs:[{k:r[k]for k in keys}for r in rs]
beforeorder=project(case['records']+case['additional_terminal_rows']);afterorder=project(port['records']);currentorder=project(hist)
need(beforeorder[:2788]==afterorder[:2788]==currentorder[:2788],'First2788 order')
need(afterorder==currentorder,'Current historical projected rows drift')
old=beforeorder[2788:];new=afterorder[2788:]
canon=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'))
digest=lambda x:hashlib.sha256(canon(x).encode()).hexdigest()
need(collections.Counter(map(canon,old))==collections.Counter(map(canon,new)),'Additional row multiset')
diff=[i for i,(x,y)in enumerate(zip(old,new))if x!=y]
need(len(diff)==939 and diff[0]==30,'Exact order discrepancy')
need(digest(old)==q['before_projected_rows_sha256']and digest(new)==q['after_projected_rows_sha256'],'Projected array digests')
stages=[]
for item in q['per_stage']:
 s=item['stage'];b=[r for r in old if r['stage']==s];a=[r for r in new if r['stage']==s]
 need(b==a and len(b)==item['count']and digest(b)==item['before_and_after_projected_rows_sha256'],'Per-stage ordered identity')
 stages.append({'stage':s,'count':len(a),'digest':digest(a)})
need(port['additional1558_values_and_order_preserved']is True and q['additional1558_global_order_preserved']is False,'Historical false/current qualification boundary')
for row in q['source_records']:check(row['path'],row,'qualification-source')
# Native outer interface is compared as data here; actual local-only dispatch is separate.
native=load('publication/zenodo-deposit.json');metadata=load(P/'metadata.json')
need(set(native)=={'metadata','files'},'Native uploader shape')
need(native['metadata']==metadata==load(P/'deposit.json')['metadata']==load(P/'metadata_wrapped.json')['metadata'],'Metadata equality')
nativefiles=[]
for row in native['files']:
 path=(A/'publication'/row['path']).resolve();nativefiles.append({'name':row['name'],'path':str(path),'bytes':identity(path)[0],'sha256':identity(path)[1]})
need([r['name']for r in nativefiles]==['paper.pdf','PR1071_preprint_v1_0_support.zip'],'Native exact selection')
# Complete newer source arrays and all whole05 local fixtures, with exact row-index preservation.
newstage=[];newgroups={}
for source,key,basepath,pathfield in [
 ('reviews/package_05/INPUT_FREEZE.json','files',A,'path'),
 ('reviews/package_05/OUTPUT_PINS.json','records',A/'reviews/package_05','path'),
 ('repairs/history_order01/BASELINE_INPUT_PINS.json','records',A,'path'),
 ('repairs/history_order01/BEFORE_PINS.json','records',A,'before_snapshot'),
 ('repairs/history_order01/PROTECTED_UNCHANGED.json','records',A,'path'),
 ('repairs/history_order01/CURRENT_AUDIT_PINS.json','records',A,'path'),
 ('repairs/history_order01/CURRENT_CANDIDATE_PINS.json','records',P,'path'),
 ('repairs/history_order01/OUTPUT_PINS.json','records',A/'repairs/history_order01','path')]:
 source_rows=load(source)[key];newgroups[source]=len(source_rows)
 for idx,row in enumerate(source_rows):
  actual=check(basepath/row[pathfield],row,'newstage/'+source+'/'+str(idx));newstage.append({'source_manifest':source,'source_row_index':idx,**row,'current_exact_resolution':relpath(actual)})
for row in load('reviews/package_05/OUTPUT_PINS.json')['symlink_fixtures']:
 path=A/'reviews/package_05'/row['path'];need(path.is_symlink() and __import__('os').readlink(path)==row['target'],'Whole05 fixture symlink target identity')
(R/'NEW_STAGE_PIN_RESOLUTION.json').write_text(json.dumps({'status':'PASS','source_manifest_complete_row_counts':newgroups,'whole05_regular_rows':903,'whole05_fixture_links':3,'records':newstage},indent=2)+'\n')
# Individually rehash all prior omission records again and this terminal archive/sidecar omission.
for row in load(P/'TERMINAL_AFTER_WHOLE05_COPY_EXCLUSIONS.json')['records']:check(row['path'],row,'terminal-individual-omission')
# Keep complete structured historical/source-row locators and their exact resolutions.

# Closed byte-level ZIP parser: every local/central field, CRC, offsets and EOF.
archive=P/'PR1071_preprint_v1_0_support.zip';blob=archive.read_bytes();manifest=load(P/'PACKAGE_MANIFEST.json');names=sorted([r['path']for r in manifest['members']]+['PACKAGE_MANIFEST.json'])
need(len(names)==len(set(names))==225,'Closed allowlist count')
rebuilt=io.BytesIO();locals_=[];offset=0
with zipfile.ZipFile(rebuilt,'w',compression=zipfile.ZIP_STORED,allowZip64=False)as z:
 for name in names:
  payload=(P/name).read_bytes();info=zipfile.ZipInfo(name,(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_STORED;z.writestr(info,payload)
  fields=struct.unpack_from('<4s5H3I2H',blob,offset);sig,version,flag,method,tim,date,crc,compressed,uncompressed,nlen,xlen=fields
  encoded=name.encode();need((sig,version,flag,method,tim,date,crc,compressed,uncompressed,nlen,xlen)==(b'PK\x03\x04',20,0,0,0,23886,zlib.crc32(payload)&0xffffffff,len(payload),len(payload),len(encoded),0),'Local ZIP header '+name)
  need(blob[offset+30:offset+30+nlen]==encoded and blob[offset+30+nlen:offset+30+nlen+len(payload)]==payload,'Local ZIP name/data '+name)
  locals_.append((name,offset,len(payload),crc));offset+=30+nlen+len(payload)
centralstart=offset
for name,local,size_,crc in locals_:
 f=struct.unpack_from('<4s6H3I5H2I',blob,offset)
 sig,made,needed,flag,method,tim,date,ccrc,compressed,uncompressed,nlen,xlen,comment,disk,internal,external,localoffset=f
 need((sig,made,needed,flag,method,tim,date,ccrc,compressed,uncompressed,nlen,xlen,comment,disk,internal,external,localoffset)==(b'PK\x01\x02',788,20,0,0,0,23886,crc,size_,size_,len(name.encode()),0,0,0,0,0o100644<<16,local),'Central ZIP header '+name)
 need(blob[offset+46:offset+46+nlen]==name.encode(),'Central ZIP name');offset+=46+nlen
end=struct.unpack_from('<4s4H2IH',blob,offset)
need(end==(b'PK\x05\x06',0,0,len(names),len(names),offset-centralstart,centralstart,0)and offset+22==len(blob),'Closed EOCD boundary')
need(rebuilt.getvalue()==blob,'Independent closed reconstruction exact bytes')
for row in manifest['members']:check(P/row['path'],row,'manifest')
(R/'FULL_SOURCE_POINTER_RESOLUTION.json').write_text(json.dumps({'status':'PASS','records':resolution_events,'scope':'Every actual old historical locator, complete source-array row/index, current copy source/destination and terminal before/current resolution; each named check rereads and hashes bytes.'},indent=2)+'\n')
output={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','terminal_baseline':len(terminalbase),'terminal_before':len(terminalbefore),'terminal_protected':len(terminalbase)-len(terminalbefore),'preexisting_fixture_links_preserved':6,'complete_new_stage_source_array_counts':newgroups,'baseline':len(base),'before':len(before),'protected':len(protected),'copy_pairs':len(copies),'prefixes':prefixes,'historical_rows':len(hist),'historical_locator_fields_individually_hashed':locators,'complete_source_manifest_rows_checked':{k:len(v)for k,v in sourcegroups.items()},'later_pin_rows':additional,'individual_omissions':len(omissions),'all_hash_checks':len(checked),'distinct_named_locator_paths_hashed':len(cache),'distinct_device_inode_pairs_hashed':len({(Path(p).stat().st_dev,Path(p).stat().st_ino)for p in cache}),'identity_event_sequence_sha256':digest(checked),'native_files':nativefiles,'original2788_exact_global_order':True,'additional1558_multiset_and_per_stage_order':True,'additional1558_global_order_false':True,'mismatched_positions':len(diff),'first_additional_position':diff[0],'first_global_position':2788+diff[0],'per_stage':stages,'source_pair_and_before_pointer_reconstruction':True,'closed_zip':{'bytes':len(blob),'sha256':hashlib.sha256(blob).hexdigest(),'members':len(names),'all_local_and_central_fields_CRC_offsets_names_payloads_EOCD_exact':True,'independent_reconstruction_byte_equal':True},'historical_false_claims_retained_as_dated_history':True,'summary_labels_not_used_as_identity_substitutes':True}
(R/'CUSTODY_FULL_REPLAY.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
