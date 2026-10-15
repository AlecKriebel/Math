import ast,datetime,hashlib,json,pathlib,re,stat,subprocess,sys,zipfile,io
sys.dont_write_bytecode=True
B=pathlib.Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1031_30002816')
P=B/'publication'; O=B/'reviews/package_04'; E=O/'extracted'; E.mkdir(exist_ok=True)
h=lambda d:hashlib.sha256(d).hexdigest()
archive=P/'grassmann_calibrations_source_verification_v1.zip'
rows=[]; names=[]
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for item in z.infolist():
  name=item.filename; q=pathlib.PurePosixPath(name)
  assert name.isascii() and name.startswith('grassmann_calibrations_v1/') and not q.is_absolute() and '..' not in q.parts and '\\' not in name and not item.is_dir()
  assert not stat.S_ISLNK(item.external_attr>>16)
  data=z.read(item); dest=E.joinpath(*q.parts); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(data)
  names.append(name)
  rows.append({'path':name,'bytes':len(data),'sha256':h(data),'crc':item.CRC,'date_time':item.date_time,'create_system':item.create_system,'external_attr':item.external_attr,'compression':item.compress_type,'flags':item.flag_bits})
 assert names==sorted(names) and len(set(names))==len(names) and len(set(n.casefold() for n in names))==len(names)
 assert len(names)==212
 X=E/'grassmann_calibrations_v1'
 m=json.loads((X/'PACKAGE_MANIFEST.json').read_text()); assert len(m['files'])==211
 assert {r['path'] for r in m['files']}=={n.removeprefix('grassmann_calibrations_v1/') for n in names}-{ 'PACKAGE_MANIFEST.json'}
 for r in m['files']:
  data=(X/r['path']).read_bytes(); assert len(data)==r['bytes'] and h(data)==r['sha256']; assert data==(P/r['path']).read_bytes()
 assert (X/'PACKAGE_MANIFEST.json').read_bytes()==(P/'PACKAGE_MANIFEST.json').read_bytes()
 rebuild=io.BytesIO()
 with zipfile.ZipFile(rebuild,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zz:
  for name in names:
   i=zipfile.ZipInfo(name,(2026,10,12,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_DEFLATED
   zz.writestr(i,z.read(name))
 assert rebuild.getvalue()==archive.read_bytes()
 # Save only digest, not a redundant rebuilt archive.
current=list(P.rglob('*')); originals=json.loads((B/'SUBMITTED_PINS.json').read_text()); original_rows=[]
head=originals['head_commit']; prefix='unsolved_math_prioritization/attempts/30002816'
tree=subprocess.check_output(['git','ls-tree','-r','--name-only',head,'--',prefix],cwd='/Users/alec/Documents/Math',text=True).splitlines()
assert len(tree)==29 and set(tree)=={r['repository_path'] for r in originals['files']}
for r in originals['files']:
 d=subprocess.check_output(['git','show',head+':'+r['repository_path']],cwd=B)
 p=B/'submitted'/r['relative']; xp=X/'evidence/submitted'/r['relative']; pp=P/'evidence/submitted'/r['relative']
 assert d==p.read_bytes()==xp.read_bytes()==pp.read_bytes() and len(d)==r['bytes'] and h(d)==r['sha256']
 original_rows.append({**r,'git_show_matches':True,'submitted_matches':True,'package_matches':True})
copy_rows=[]
for number,count in ((1,29),(2,36),(3,37)):
 cp=json.loads((X/f'evidence/PACKAGE_REVIEW_{number:02d}_COPY.json').read_text());assert len(cp['files'])==count
 for r in cp['files']:
  d=(X/r['path']).read_bytes(); orig=B/'reviews'/f'package_{number:02d}'/pathlib.PurePosixPath(r['path']).relative_to(f'evidence/package_review_{number:02d}')
  assert h(d)==r['sha256'] and len(d)==r['bytes'] and d==orig.read_bytes()
 copy_rows.append({'round':number,'count':count,'all_authored_records_unchanged':True,'actual_original_objects_matched':True})
json_rows=[]
for p in sorted(X.rglob('*.json')):
 o=json.loads(p.read_text());json_rows.append({'path':str(p.relative_to(X)),'root_type':type(o).__name__})
metadata=json.loads((X/'metadata.json').read_text());wrapper=json.loads((P/'zenodo-deposit.json').read_text());assert wrapper['metadata']==metadata
assert metadata['creators'][0]['orcid']=='0009-0001-9320-500X' and metadata['license']=='cc-by-4.0' and metadata['publication_type']=='preprint' and metadata['version']=='1.0' and metadata['publication_date']=='2026-10-12'
nav=[]
for p in sorted(X.rglob('*.md')):
 if p.name not in ('README.md','SUPPLEMENT.md','INDEX.md'):continue
 # Current top-level/index navigation, excluding historical README's own historical-stage relationships.
 if '/evidence/submitted/' in str(p):continue
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'https?://',target) or target.startswith('#'):continue
  target=target.split('#')[0];exists=(p.parent/target).exists();assert exists,(str(p),target)
  nav.append({'source':str(p.relative_to(X)),'target':target,'exists':exists})
for p in X.rglob('*'):
 if p.is_file(): assert p.suffix not in ('.pyc','.png','.jpg','.zip') and '__pycache__' not in p.parts
assert [p for p in X.rglob('*.pdf')]==[X/'research_note.pdf']
state=json.loads((X/'evidence/CURRENT_REVIEW_STATE.json').read_text());assert state['preprint_ready_for_immutable_publication'] is False and state['published'] is False and state['next_gate']=='NEW independent whole-package review 04'
for p in X.rglob('*.py'):ast.parse(p.read_text())
obj={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','entry_count':len(rows),'manifest_records':211,'archive_sha256':h(archive.read_bytes()),'archive_bytes':archive.stat().st_size,'safe_ascii_unique_casefold_sorted_crc_checked':True,'deterministic_in_memory_rebuild_identical':True,'publication_tree_matches_every_archive_payload':True,'entry_records':rows,'original_full_git_tree_29':original_rows,'authored_review_copy_groups':copy_rows,'all_json_parsed':json_rows,'metadata_wrapper_exact':True,'navigation':nav,'redistributed_raw_bodies_renders_caches_duplicate_archives':False,'current_review_state':state}
(O/'ARCHIVE_INSPECTION.json').write_text(json.dumps(obj,indent=2)+'\n')
print(json.dumps({k:v for k,v in obj.items() if k not in ('entry_records','original_full_git_tree_29','all_json_parsed','navigation')},indent=2))
