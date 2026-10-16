import sys
sys.dont_write_bytecode=True
import pathlib,json,hashlib,zipfile,os,datetime
A=pathlib.Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr204_5100012");D=A/'publication_package_v1'
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(b):return {'bytes':len(b),'sha256':sha(b)}
def js(p):return json.loads(p.read_bytes())
def encode(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()+b'\n'
def put(p,b):
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);need(p.read_bytes()==b,'write readback '+str(p))
need(not (D/'PACKAGE_SEAL.json').exists(),'do not reseal a version')
portable=A/'portable_verification_01'; allow=js(portable/'AUTHORED_ALLOWLIST.json')
scientific=js(portable/'INPUT_PINS.json')['files']
curated=js(A/'package_preparation_01/CURATED_PUBLIC_PROVENANCE_01.json')['public_provenance_files']
expected={}
for rel,p in scientific.items():expected['materials/'+rel]=p
for rel,p in curated.items():
 need(rel not in expected,'curated/science collision');expected[rel]=p
for rel,p in allow['files'].items():expected['portable_verification_01/'+rel]=p
expected['portable_verification_01/AUTHORED_ALLOWLIST.json']=pin((portable/'AUTHORED_ALLOWLIST.json').read_bytes())
for rel in ['README.md','LICENSE.txt','centered_pedal_dn.tex','centered_pedal_dn.pdf','zenodo-deposit.json']:expected[rel]=pin((D/rel).read_bytes())
need(len(scientific)==142 and len(curated)==19 and len(allow['files'])==11 and len(expected)==178,'expected actual count')
actual={str(p.relative_to(D)) for p in D.rglob('*') if p.is_file()}
need(actual==set(expected),'unexpected/missing package files '+str(sorted(actual.symmetric_difference(expected))))
for rel,p in expected.items():
 q=D/rel
 need(not q.is_symlink() and q.resolve()==q,'symlink '+rel)
 need(pin(q.read_bytes())==p,'package pin '+rel)
meta=js(D/'zenodo-deposit.json')
need([x['path'] for x in meta['files']]==['centered_pedal_dn.pdf','centered_pedal_dn.tex','verification-package.zip'],'upload names')
need(meta['metadata']['title']=='A two-pole proof of the centered pedal-area invariant','title')
need(meta['metadata']['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'creator')
archive_files={rel:p for rel,p in expected.items() if rel not in ['centered_pedal_dn.tex','centered_pedal_dn.pdf']}
manifest={'schema':'pr204-public-materials-manifest-v1','files':archive_files,'file_count_excluding_this_manifest':len(archive_files),'self_allowed_not_self_hashed':'PUBLIC_MATERIALS_MANIFEST.json','external_manuscript_uploads':{r:expected[r] for r in ['centered_pedal_dn.pdf','centered_pedal_dn.tex']},'scientific_input_pin_manifest':expected['portable_verification_01/INPUT_PINS.json'],'scope':'Authoritative exact archive contents. Upstream historical manifests are provenance records, not archive-completeness claims.','excluded_private_direct_inventory':{'path':'math_direct_geometry_01/RUNTIME_CACHE_INCIDENT_01.json','bytes':512477,'sha256':'a68a3f8b1fa83bc1a40818dc61f0ca3deb6bc45e8927a565085dc9b1d3aa7a5b'},'primary_PDFs_dependencies_caches_credentials_UI_excluded':True}
mb=encode(manifest);put(D/'PUBLIC_MATERIALS_MANIFEST.json',mb)
archive_files['PUBLIC_MATERIALS_MANIFEST.json']=pin(mb)
zip_path=D/'verification-package.zip'
with zipfile.ZipFile(zip_path,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=True) as z:
 for rel in sorted(archive_files):
  need(not rel.startswith('/') and '..' not in pathlib.PurePosixPath(rel).parts,'unsafe zip name')
  b=(D/rel).read_bytes();need(pin(b)==archive_files[rel],'pre-zip pin')
  info=zipfile.ZipInfo(rel,date_time=(2026,10,16,0,0,0));info.create_system=3;info.external_attr=0o100444<<16;info.compress_type=zipfile.ZIP_DEFLATED;info.extra=b''
  z.writestr(info,b,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(zip_path) as z:
 need(z.namelist()==sorted(archive_files) and len(z.namelist())==len(set(z.namelist())),'zip entries')
 need(z.testzip() is None,'zip crc')
 for rel,p in archive_files.items():need(pin(z.read(rel))==p,'zip content '+rel)
zip_path.chmod(0o444)
expected['PUBLIC_MATERIALS_MANIFEST.json']=pin(mb)
expected['verification-package.zip']=pin(zip_path.read_bytes())
need(len(expected)==180 and len(archive_files)==177,'final counts')
for rel,p in expected.items():
 q=D/rel;need(pin(q.read_bytes())==p,'seal content drift');q.chmod(0o444)
seal={'schema':'pr204-publication-package-seal-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':expected,'file_count_excluding_seal':len(expected),'self_allowed_not_self_hashed':'PACKAGE_SEAL.json','archive_entries':len(archive_files),'exact_intended_Zenodo_metadata':expected['zenodo-deposit.json'],'intended_uploads':{r:expected[r] for r in ['centered_pedal_dn.pdf','centered_pedal_dn.tex','verification-package.zip']},'manuscript_pages':6,'mathematics_qualified_valid':True,'exact_contemporary_overlap':True,'theorem_formula_method_novelty_established':False,'package_prepared':True,'whole_package_reviews_complete':False,'publication_ready':False,'release_authorized_by_this_seal':False}
sb=encode(seal);put(D/'PACKAGE_SEAL.json',sb)
need({str(p.relative_to(D)) for p in D.rglob('*') if p.is_file()}==set(expected)|{'PACKAGE_SEAL.json'},'final package exactness')
receipt={'schema':'pr204-Root-package-preparation-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':204,'original_head':'551a524e2db65fec90684485ef676d0b4179378d','estimate_case_completion_percent':75,'package':'publication_package_v1','package_preparation_accepted':True,'publication_ready':False,'release_authorized_by_this_gate':False,'whole_package_reviews_complete':False,'NEW_whole_package_reviews_completed':0,'package_seal':{'path':'publication_package_v1/PACKAGE_SEAL.json',**pin(sb)},'original_scientific_142_and_portable_12_byte_copies_verified':True,'curated_public_provenance_19_verified':True,'external_source_PDFs_runtime_and_private_inventory_excluded':True,'current_manuscript_governs_claims_over_historical_records':True,'finite_portable_controls_28_Root_accepted':True,'all_six_final_PDF_pages_visually_inspected':True,'exact_177_ZIP_entry_CRC_content_pins_verified':True,'metadata_and_three_uploads_exactly_pinned':True,'novelty_or_firstness_or_independent_discovery_cleared':False,'qualified_attributed_note_preparation_allowed':True,'safe_files':{}}
for rel,p in expected.items():receipt['safe_files']['publication_package_v1/'+rel]=p
receipt['safe_files']['publication_package_v1/PACKAGE_SEAL.json']=pin(sb)
for rel in ['ROOT_PORTABLE_VERIFICATION_ACCEPTANCE_01.json','ROOT_PDF_VISUAL_QA_V1.json','package_preparation_01/CURATED_PUBLIC_PROVENANCE_01.json','package_preparation_01/PORTABLE_SOURCE_MODE_SEAL_01.json','package_preparation_01/assemble_curated.py','package_preparation_01/seal_package.py','package_preparation_01/RESEARCH_LOG.md']:
 (A/rel).chmod(0o444);receipt['safe_files'][rel]=pin((A/rel).read_bytes())
for p in sorted((A/'materials_assembly_01').iterdir()):
 need(p.is_file() and not p.is_symlink(),'unexpected assembly directory')
 if p.suffix in ['.py','.md','.json']:p.chmod(0o444);receipt['safe_files'][str(p.relative_to(A))]=pin(p.read_bytes())
put(A/'ROOT_PACKAGE_PREPARATION_ACCEPTANCE_01.json',encode(receipt))
print(json.dumps({'package_files_including_seal':181,'ZIP_entries':177,'ZIP':expected['verification-package.zip'],'seal':pin(sb),'Root_gate':pin((A/'ROOT_PACKAGE_PREPARATION_ACCEPTANCE_01.json').read_bytes()),'package_prepared':True,'publication_ready':False,'fresh_whole_package_reviews_remaining':True}))
