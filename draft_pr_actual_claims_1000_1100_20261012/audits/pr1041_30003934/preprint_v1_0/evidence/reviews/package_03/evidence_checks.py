#!/usr/bin/env python3
"""Independent closed payload, source-copy and historical custody checks."""
from pathlib import Path
import hashlib,json,gzip,tarfile,io,struct,zlib,datetime,re,collections
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent;CAND=BASE/'preprint_v1_0'
def sha(x):return hashlib.sha256(x).hexdigest()
def need(x,t):
 if not x:raise RuntimeError(t)
def check(p,r):
 b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'pin '+str(p));return b
current=json.loads((CAND/'CURRENT_INTEGRITY.json').read_text());entries=current['files'];need(len(entries)==len({r['path'] for r in entries}),'duplicate content')
for r in entries:check(CAND/r['path'],r)
copy_map=json.loads((CAND/'EVIDENCE_COPY_MANIFEST.json').read_text());groups=collections.Counter()
for r in copy_map['files']:
 src=check(BASE/r['source_path'],r);dst=check(CAND/r['package_path'],r);need(src==dst,'copy bytes');groups[r['group']]+=1
need(groups['frozen_original_11']==11,'original11')
originals=[]
for r in json.loads((BASE/'SUBMITTED_PINS.json').read_text())['files']:
 b=check(BASE/r['snapshot_path'],r);need(b==(CAND/'evidence/original'/r['snapshot_path']).read_bytes(),'original package')
 originals.append({'repository_path':r['repository_path'],'snapshot_path':r['snapshot_path'],'bytes':len(b),'sha256':sha(b),'computed_git_blob_oid':hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()})
oldgit=json.loads((BASE/'reviews/package_02/ORIGINAL_GIT_OBJECTS.json').read_text())
old_oids={r['repository_path']:r['git_blob_oid'] for r in oldgit['files']}
need(all(r['computed_git_blob_oid']==old_oids[r['repository_path']] for r in originals),'original computed Git oid identity')
# Record all origin identity evidence without executing git or claiming a fresh service capture.
(HERE/'ORIGINAL_IDENTITIES.json').write_text(json.dumps({'original_head':'ad138ddd5bd1a51c0f225f03342c0c058873f790','fresh_git_or_service_operation':False,'records':originals,'old_git_inventory_sha256':sha((BASE/'reviews/package_02/ORIGINAL_GIT_OBJECTS.json').read_bytes()),'old_inventory_schema':list(oldgit)},indent=2)+'\n')
historic=[];missing=[]
for family in ['flow_source_01','game_certificate_01','priority_01','package_01','package_02']:
 pins=json.loads((CAND/'evidence/reviews'/family/'OUTPUT_PINS.json').read_text())
 for r in pins.get('files',pins.get('entries',[])):
  name=r.get('path',r.get('file'));p=CAND/'evidence/reviews'/family/name
  if p.is_file():check(p,r);historic.append(family+'/'+name)
  else:
   need(any(x in {'raw','rawprivate','__pycache__','render','cache','caches'} for x in p.parts) or family+'/'+name=='priority_01/sources/CITATION_DISCOVERY.json','unexpected historical missing');missing.append(family+'/'+name)
# Repair seals and protected baseline checks, excluding only known authorized changes.
rep=BASE/'repairs/package02';rp=json.loads((rep/'OUTPUT_PINS.json').read_text())
for r in rp['files']:check(rep/r['path'],r)
repair_fields={}
for name in ['BASELINE_ALL_PINS.json','FINAL_CURRENT_INPUT_PINS.json','CHANGE_INVENTORY.json','test_stages/attempt02/NEGATIVE_CONTROLS.json']:
 o=json.loads((rep/name).read_text());repair_fields[name]={'schema':list(o),'sha256':sha((rep/name).read_bytes())}
baseline=json.loads((rep/'BASELINE_ALL_PINS.json').read_text());changes=json.loads((rep/'CHANGE_INVENTORY.json').read_text());changed={r['path'] for r in changes['changed']};protected=0
for r in baseline['files']:
 if r['path'] not in changed:check(BASE/r['path'],r);protected+=1
for r in changes['changed']:
 check(BASE/r['path'],r['after']);check(BASE/r['exact_old_stage_copy'],r['before'])
for r in changes['added']:check(BASE/r['path'],r)
final_current=json.loads((rep/'FINAL_CURRENT_INPUT_PINS.json').read_text())
for r in final_current['files']:check(CAND/r['path'],r)
need(protected==2488 and len(changed)==17 and len(changes['added'])==85 and len(final_current['files'])==224,'repair custody counts')
# Strict all historical pins are source identities, not retargeted current records.
stage=CAND/'history/before_package02_verifier_repair';oldstage=json.loads((stage/'STAGE_PINS.json').read_text())
for r in oldstage.get('files',[]):
 name=r.get('path',r.get('file'));check(stage/name,r)
raw=(CAND/'supportkit-v1.0.tar.gz').read_bytes();expanded=gzip.decompress(raw);crc,size=struct.unpack('<II',raw[-8:]);need(crc==zlib.crc32(expanded)&0xffffffff and size==len(expanded)&0xffffffff,'gzip trailer');need(raw[:10]==b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff','gzip header')
receipt=json.loads((CAND/'BUILD_RECEIPT.json').read_text());names=sorted([r['path'] for r in entries]+['CURRENT_INTEGRITY.json','BUILD_RECEIPT.json']);wanted=set(names)
stream=io.BytesIO()
with tarfile.open(fileobj=stream,mode='w',format=tarfile.PAX_FORMAT) as out:
 for name in names:
  b=(CAND/name).read_bytes();info=tarfile.TarInfo('rank_one_uniqueness_v1_0/'+name);info.size=len(b);info.mtime=1791849600;info.mode=0o644;info.uid=info.gid=0;info.uname=info.gname='';out.addfile(info,io.BytesIO(b))
need(stream.getvalue()==expanded,'independent complete tar bytes')
rebuilt=gzip.compress(stream.getvalue(),compresslevel=9,mtime=0);need(rebuilt==raw,'independent gzip bytes')
with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as t:
 actual=[]
 for m in t.getmembers():
  need(m.isfile(),'nonregular member');need(m.name.startswith('rank_one_uniqueness_v1_0/'),'prefix');name=m.name[23:] if False else m.name[len('rank_one_uniqueness_v1_0/'):];actual.append(name)
  need(name in wanted and re.fullmatch(r'[A-Za-z0-9_.\-/]+',name) and not name.startswith('/') and all(s not in {'','..','.'} for s in name.split('/')),'unsafe path')
  need(m.mode==0o644 and m.uid==m.gid==0 and m.uname==m.gname=='' and m.mtime==1791849600,'metadata');need(t.extractfile(m).read()==(CAND/name).read_bytes(),'full member bytes')
 need(actual==names and len(actual)==len(set(actual))==len({x.casefold() for x in actual}),'member closure')
textfiles=[];jsonfiles=[];binary=[]
for name in names:
 data=(CAND/name).read_bytes()
 if name=='output/pdf/paper.pdf':need(data.startswith(b'%PDF-'),'authored pdf');binary.append(name);continue
 need(not any(sig in data for sig in [b'%PDF-',b'\x89PNG\r\n\x1a\n',b'\x1f\x8b\x08']),'hidden source binary')
 text=data.decode('utf8');textfiles.append(name)
 if name.endswith('.json'):json.loads(text);jsonfiles.append(name)
 need(not any(x in {'raw','rawprivate','private','tmp','replay','render','__pycache__','extracted','cache'} for x in Path(name).parts),'excluded path')
wrapper=json.loads((CAND/'zenodo-deposit.json').read_text());need(wrapper['metadata']==json.loads((CAND/'publication/zenodo.json').read_text()),'metadata equality');need(wrapper['files']==[{'path':'output/pdf/paper.pdf','name':'paper.pdf'},{'path':'supportkit-v1.0.tar.gz','name':'supportkit-v1.0.tar.gz'}],'bindings');need('zenodo-deposit.json' not in wanted,'wrapper selfreference')
# Actual replay semantic equality excluding only timestamp.
replays=[]
for file,source,target in [('CHECKS_NORMAL.json','flow_source_01','replay_flow'),('CHECKS_OPTIMIZED.json','flow_source_01','replay_flow'),('EXACT_RESULTS.json','game_certificate_01','replay_game')]:
 a=json.loads((CAND/'evidence/reviews'/source/file).read_text());b=json.loads((HERE/'private'/target/file).read_text());a.pop('utc');b.pop('utc');need(a==b,'semantic replay '+file);replays.append(file)
normal=json.loads((HERE/'MATH_NORMAL.json').read_text());opt=json.loads((HERE/'MATH_OPTIMIZED.json').read_text());normal.pop('utc');opt.pop('utc');normal.pop('mode');opt.pop('mode');need(normal==opt,'independent normal optimized results')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','current_content_files':len(entries),'archive_members':len(actual),'copied_source_equal_records':len(copy_map['files']),'copy_groups':dict(groups),'original_files':len(originals),'historic_pin_members_verified':len(historic),'intentional_historical_exclusions':missing,'repair_terminal_pin_members_verified':len(rp['files']),'repair_metadata':repair_fields,'unchanged_baseline_outside_authorized_changes':protected,'authorized_changed_with_exact_old_copies':len(changed),'repair_added_files_verified':len(changes['added']),'repair_final_current_pins_verified':len(final_current['files']),'independent_closed_tar_and_gzip_bytes_identical':True,'gzip_crc_and_isize':True,'safe_sorted_casefold_unique_regular_members':True,'utf8_files_including_receipt':len(textfiles),'parseable_json_files':len(jsonfiles),'binary_members':binary,'semantic_replays_equal_except_utc':replays,'independent_modes_semantically_equal_except_utc_mode':True,'archive_sha256':sha(raw)}
(HERE/'EVIDENCE_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
