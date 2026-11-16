"""Source/root-only finite custody. No editorial/Git/network/project imports or writes."""
from pathlib import Path
import hashlib,json,stat,sys
D=Path(__file__).resolve().parent;B=D.parent.parent;P=B/'papers/23202966';checks=0;nodes=0
ROOTS=[D,P/'sources',P/'reviews/scope',P/'reviews/adversarial',P/'reviews/root']
AUTH=B/'verification/root-clearance-23202966-20261115.json'
def need(ok,label):
 global checks
 checks+=1
 if not ok:raise RuntimeError(label)
def read(p):
 p=Path(p);need(p==AUTH or any(r in p.parents for r in ROOTS),'only source/root/own allowed')
 need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary original/own file');return p.read_bytes()
def obj(p):return json.loads(read(p))
def pin(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def exact(a,b,label):
 global nodes
 nodes+=1;need(type(a) is type(b),'exact type '+label)
 if isinstance(a,dict):
  need(list(a)==list(b),'whole key/order/absence '+label)
  for k in a:exact(a[k],b[k],label+'/'+k)
 elif isinstance(a,list):
  need(len(a)==len(b),'array size '+label)
  for i,(x,y) in enumerate(zip(a,b)):exact(x,y,label+'/'+str(i))
 else:need(a==b,'literal scalar/null '+label)
def extent(root):
 fs=[];ds=[]
 need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary root')
 for p in root.rglob('*'):
  rel=p.relative_to(root).as_posix();mode=p.lstat().st_mode
  if stat.S_ISDIR(mode):ds.append(rel)
  else:need(stat.S_ISREG(mode),'ordinary namespace');fs.append(rel)
 need(len(fs)==len(set(fs)) and len(ds)==len(set(ds)),'unique actual identities')
 return sorted(fs),sorted(ds)
need(sys.argv[1:] in [[],['--preseal']],'finite source-only modes')
refs=obj(D/'SOURCE_ROOT_REFERENCES.json')
for ns in refs['namespaces']:
 root=Path(ns['root']);fs,ds=extent(root);expected=list(ns['files'])
 need(len(expected)==len(set(expected)) and len(ns['directories'])==len(set(ns['directories'])),'unique expected identities')
 need(fs==sorted(expected) and ds==sorted(ns['directories']),'exact original whole file/directory identities')
 for name,p in ns['files'].items():need(pin(read(root/name))==p,'whole original pinned file')
need([(len(r['files']),len(r['directories'])) for r in refs['namespaces']]==[(82,9),(272,45),(133,21),(35,3)],'actual original extents')
ar=read(AUTH);need(pin(ar)=={k:refs['separate_root_authority'][k] for k in ['bytes','SHA256']},'whole root authority')
root=json.loads(ar);ready=obj(P/'sources/SOURCE_READY.json');exact(ready,root['wholeOriginalSourceReady'],'whole original READY')
need(root['editorialPreparationAuthorized'] is True and root['fullEditorialCopyConfigCodeAdopted'] is False and root['productionInstallationAuthorized'] is False,'bounded root authority')
need(root['canonical_url'] is None and root['AA'] is None and root['follow_up'] is None,'root null flags')
metadata=obj(D/'EXPECTED_NATIVE_METADATA.json');record=obj(P/'sources/record.response.body');files=obj(P/'sources/files.response.body')
exact(record['metadata'],metadata['whole_original_native_metadata'],'whole native metadata')
exact(record['files'],metadata['whole_original_native_record_asset_array'],'whole ordered original native assets')
exact(files,metadata['whole_original_native_files_object'],'whole native files API object')
exact(ready['all_native_assets_in_original_order'],metadata['whole_source_READY_native_asset_entries'],'whole source asset custody')
exact(record,obj(P/'sources/latest.response.body.redirect-01'),'whole native latest')
need(read(P/'sources/record.response.body')==read(P/'sources/latest.response.body.redirect-01'),'whole latest raw bytes')
versions=obj(P/'sources/versions-page001.response.body');expected=json.loads(read(P/'sources/record.response.body'));expected['swh']=None
need(type(versions['hits']['total']) is int and versions['hits']['total']==1 and len(versions['hits']['hits'])==1 and list(versions)==['hits','links'],'whole version envelope')
exact(expected,versions['hits']['hits'][0],'actual version entry except literal swh:null')
need('version' not in record['metadata'] and metadata['API_version_field_present'] is False and metadata['API_version_original_value'] is None,'absent API version distinct from wrapper null')
need(metadata['printed_version_present'] is False and metadata['printed_version'] is None and metadata['declared_publication_date']=='2026-10-06' and metadata['created']=='2026-10-07T04:34:37.920372+00:00','date/printed version distinction')
need(record['metadata']['creators'][0]['affiliation'] is None,'native affiliation null')
need([a['key'] for a in record['files']]==['README.md','paper.pdf','main.tex','verification.zip'],'four actual assets native order')
for a in ready['all_native_assets_in_original_order']:
 raw=read(a['path']);need(pin(raw)=={k:a[k] for k in ['bytes','SHA256']},'whole original asset')
 need('md5:'+hashlib.md5(raw).hexdigest()==a['original_api_file_object']['checksum'],'whole original native checksum')
tex=read(P/'sources/assets/main.tex').decode();abstract=tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
need(abstract==metadata['whole_printed_abstract_TeX'] and len(tex.splitlines())==376,'entire printed abstract and native TeX')
need(read(P/'sources/assets/README.md').decode()==metadata['whole_authored_license_and_disclosure_README'],'actual authored rights/readme')
reading=obj(D/'OWN_PDF_READING.json')
need(reading['full_PDF_pages_personally_read']==6 and reading['native_TeX']['all_lines_personally_read']==376 and len(reading['all_six_fresh_own_rasters'])==6,'complete reading custody')
for r in reading['all_six_fresh_own_rasters']:need(pin(read(D/r['path']))=={k:r[k] for k in ['bytes','SHA256']} and r['individually_visually_read'] is True,'fresh own individual raster')
e=obj(D/'INITIAL_EXPECTATIONS.json');need(e['exposure']['current_editorial_packet_listed'] is False and e['exposure']['current_editorial_packet_read'] is False and e['publication_or_production_installation_authority'] is False,'source-first private scope')
need(e['canonical_url'] is None and e['AA'] is None and e['follow_up'] is None,'null publication gates')
if sys.argv[1:]:
 contract=obj(D/'PRESEAL_NAMESPACE.json');fs,ds=extent(D);need(fs==sorted(contract['files']) and ds==sorted(contract['directories']),'finite exact preseal own extent')
else:
 seal=obj(D/'INITIAL_SEAL.json');mb=read(D/'INITIAL_MANIFEST.json');need(pin(mb)==seal['manifest'],'same buffer initial manifest pin');m=json.loads(mb)
 names=[r['path'] for r in m['files']]+['INITIAL_MANIFEST.json','INITIAL_SEAL.json'];fs,ds=extent(D)
 need(len(names)==len(set(names)) and fs==sorted(names) and ds==sorted(m['directories']),'exact source-only own extent')
 need(m['exact_root_terminal_exclusions']==['INITIAL_MANIFEST.json','INITIAL_SEAL.json'] and m['future_subtree_exclusions']==[],'exact root terminals only')
 for r in m['files']:need(pin(read(D/r['path']))=={k:r[k] for k in ['bytes','SHA256']},'whole immutable initial payload')
print(json.dumps({'status':'PASS_SOURCE_ROOT_ONLY_BINARY_LIVENESS_FACT_INITIAL_CUSTODY','checks':checks,'whole_typed_nodes':nodes,'original_namespaces':[[82,9],[272,45],[133,21],[35,3]],'native_assets':4,'fresh_own_PDF_rasters':6,'printed_and_API_version':'ABSENT','native_scientific_foreign_editorial_campaign_network_Git_or_writes':False,'raw_corpora_recopied':False,'root_editorial_copy_code_adoption':False,'production_authority':False,'canonical_url':None,'AA':None,'follow_up':None},sort_keys=True))
