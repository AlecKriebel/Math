from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,io,subprocess,stat,collections,datetime,re
out=Path(__file__).resolve().parent;base=out.parent.parent;root=base/'preprint'
def sha(b):return hashlib.sha256(b).hexdigest()
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'failures':[]}
def check(label,ok,details=None):
 report[label]={'ok':bool(ok),'details':details}
 if not ok:report['failures'].append(label)
# byte verification of actual Git show, all 10 full tree paths
head='e87236a97c4b87818d2768cd5789043c7c3f4e39';treeprefix='unsolved_math_prioritization/attempts/30003822'
tree=subprocess.check_output(['git','ls-tree','-r','--name-only',head,treeprefix]).decode().splitlines();report['git_full_subtree']=tree
pins=json.loads((base/'SUBMITTED_PINS.json').read_text());rows=[]
for row in pins['files']:
 b=subprocess.check_output(['git','show',head+':'+row['repository_path']]);snap=(base/row['snapshot_path']).read_bytes();copy=(root/'evidence/original_20261009'/Path(row['snapshot_path']).name).read_bytes()
 rows.append({'path':row['repository_path'],'git_bytes':len(b),'git_sha256':sha(b),'submitted_equal':b==snap,'package_equal':b==copy,'matches_record':len(b)==row['bytes'] and sha(b)==row['sha256']})
check('original10_git_show',len(rows)==10 and all(r['submitted_equal'] and r['package_equal'] and r['matches_record'] for r in rows),rows)
check('original_full_tree_only_ten',set(tree)=={r['repository_path'] for r in pins['files']},tree)
# all 76 byte exact copies with stage annotations
index=json.loads((root/'EVIDENCE_INDEX.json').read_text());rows=[]
for row in index['entries']:
 b=(root/row['package_path']).read_bytes();source=(base/row['source_path']).read_bytes()
 rows.append({'package_path':row['package_path'],'source_path':row['source_path'],'stage':row.get('stage'),'source_equal':b==source,'record_equal':len(b)==row['bytes'] and sha(b)==row['sha256']})
check('all76_evidence_copies',len(rows)==76 and all(r['source_equal'] and r['record_equal'] and r['stage'] for r in rows),rows)
# manifest and ZIP bytes, path safety, regular modes, CRC
manifest=json.loads((root/'MANIFEST.json').read_text());mr={r['path']:r for r in manifest['files']};report['manifest_payload_count']=len(mr)
check('manifest_unique_payloads',len(mr)==len(manifest['files'])==92)
check('manifest_no_self_or_archive',not any(x in mr for x in ['MANIFEST.json','ARCHIVE_PIN.json','pr1037_supportkit_v1.0.zip']))
archive=root/'pr1037_supportkit_v1.0.zip';archiveb=archive.read_bytes();zr=[]
with zipfile.ZipFile(archive) as z:
 names=z.namelist();check('zip_unique_sorted',len(names)==len(set(names))==93 and names==sorted(names))
 check('zip_manifest_members_exact',set(names)==set(mr)|{'MANIFEST.json'})
 check('zip_all_crc',z.testzip() is None)
 for zi in z.infolist():
  name=zi.filename;path=PurePosixPath(name);b=z.read(zi)
  safe=not path.is_absolute() and '..' not in path.parts and '\\' not in name and name.isascii() and not any(ord(x)<32 or ord(x)==127 for x in name)
  equal=b==(root/name).read_bytes();record=(name=='MANIFEST.json') or (sha(b)==mr[name]['sha256'] and len(b)==mr[name]['bytes'])
  zr.append({'path':name,'bytes':len(b),'sha256':sha(b),'safe':safe,'regular0644':zi.external_attr>>16==0o100644,'create_system':zi.create_system,'fixed_time':zi.date_time==(2026,10,13,0,0,0),'content_equal':equal,'manifest_equal':record,'magic':b[:10].hex(),'extension':path.suffix,'utf8':True})
  try:b.decode('utf8')
  except UnicodeDecodeError:zr[-1]['utf8']=False
 check('zip_every_member',all(r['safe'] and r['regular0644'] and r['fixed_time'] and r['content_equal'] and r['manifest_equal'] and r['create_system']==3 for r in zr),zr)
 # independent archive reconstruction, do not execute candidate builder
 bio=io.BytesIO()
 with zipfile.ZipFile(bio,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=True) as nz:
  for name in names:
   zi=zipfile.ZipInfo(name,(2026,10,13,0,0,0));zi.create_system=3;zi.external_attr=0o100644<<16;zi.compress_type=zipfile.ZIP_DEFLATED
   nz.writestr(zi,(root/name).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
 rebuilt=bio.getvalue();(out/'sources/raw/independent_rebuilt.zip').write_bytes(rebuilt)
 check('independent_zip_rebuild',rebuilt==archiveb,{'bytes':len(rebuilt),'sha256':sha(rebuilt)})
pin=json.loads((root/'ARCHIVE_PIN.json').read_text());mb=(root/'MANIFEST.json').read_bytes()
check('external_archive_pin',pin['sha256']==sha(archiveb) and pin['bytes']==len(archiveb) and pin['manifest_sha256']==sha(mb) and pin['manifest_bytes']==len(mb) and pin['archive_members']==93 and pin['payload_members']==92,pin)
check('metadata_exact',json.loads((root/'.zenodo.json').read_text())==json.loads((root/'zenodo_metadata.json').read_text())['metadata'])
# content-level scan of all actual archive members: raw/image/extracted/cache detections, not declared exclusions
bad_extensions={'.png','.jpg','.jpeg','.webp','.gif','.bmp','.svg','.pyc','.pyo','.zip','.tar','.gz','.log','.aux','.out','.bib','.html'}
bad=[];duplicate=collections.defaultdict(list);text_scan=[]
for r in zr:
 b=(root/r['path']).read_bytes();duplicate[r['sha256']].append(r['path'])
 if r['extension'] in bad_extensions or (not r['utf8'] and r['path']!='paper/forest_transfer_catalan.pdf') or any(x.lower() in {'raw','rawprivate','cache','render','extractedcache','__pycache__','.venv'} for x in PurePosixPath(r['path']).parts):bad.append(r['path'])
 if r['utf8']:
  s=b.decode('utf8');text_scan.append({'path':r['path'],'characters_scanned':len(s),'embedded_binary_or_base64':bool(re.search(r'data:(?:image|application/pdf)/[^;]+;base64|JVBERi0|iVBORw0KGgo',s)),'thirdparty_extract_signal':bool(re.search(r'^arXiv:.*\[.*\]|^Grassmann Integral Representation for Spanning Hyperforests\s*$',s,re.M))})
check('all_actual_payload_types',not bad,{'bad':bad,'type_counts':dict(collections.Counter(r['extension'] for r in zr)),'all_nontext_members':[r['path'] for r in zr if not r['utf8']]})
check('content_scan_no_encoded_raw',not any(r['embedded_binary_or_base64'] or r['thirdparty_extract_signal'] for r in text_scan),text_scan)
report['duplicate_sha256_groups']=[v for v in duplicate.values() if len(v)>1]
# Record whole-file full content inventory for human reads and navigation targets
navigation=[]
for f in ['README.md','SUPPLEMENT.md','SOURCE_PRIORITY_ADDENDUM_20261013.md']:
 s=(root/f).read_text()
 for target in re.findall(r'`([^`]+)`',s):
  if '/' in target or target.endswith(('.md','.json','.py','.tex','.pdf','.zip')):navigation.append({'document':f,'target':target,'exists':(root/target).exists()})
report['navigation_scan']=navigation
# all candidate/originals remain frozen
initial=json.loads((out/'INPUT_PIN.json').read_text());changed=[]
for r in initial['files']:
 p=Path(r['path']);b=p.read_bytes()
 if len(b)!=r['bytes'] or sha(b)!=r['sha256']:changed.append(r['path'])
check('inputs_unchanged_at_package_audit',not changed,changed)
(out/'PACKAGE_CHECK_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'failures':report['failures'],'git_files':len(tree),'evidence_entries':len(rows),'members':len(zr),'independent_rebuild':report['independent_zip_rebuild'],'duplicate_groups':report['duplicate_sha256_groups'],'types':report['all_actual_payload_types']},indent=2))
