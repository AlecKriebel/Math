"""Bounded source/root/own-buffer custody only; no science or editorial access.

Default closes this INITIAL snapshot exactly. Later separately authorized additive
audit work requires its own final closure; no future subtree is excluded here.
"""
from pathlib import Path
import hashlib,json,stat,sys

D=Path(__file__).resolve().parent
B=D.parent.parent
P=B/'papers/23205305'
checks=0
typed=0
def need(ok,label):
 global checks
 checks+=1
 if not ok:raise RuntimeError(label)
def read(p):
 p=Path(p)
 need(p.is_absolute() and p.resolve()==p,'ordinary unescaped file path')
 need(stat.S_ISREG(p.lstat().st_mode),'regular file, no symlink')
 return p.read_bytes()
def pairs(items):
 d={}
 for k,v in items:
  need(k not in d,'no duplicate JSON key');d[k]=v
 return d
def obj(p):return json.loads(read(p),object_pairs_hook=pairs)
def pin(raw):return {'bytes':len(raw),'SHA256':hashlib.sha256(raw).hexdigest()}
def matches(p,r):need(pin(read(p))=={k:r[k] for k in ['bytes','SHA256']},'whole exact bytes: '+str(p))
def same(a,b,label):
 global typed
 typed+=1
 need(type(a) is type(b),'exact type '+label)
 if isinstance(a,dict):
  need(list(a)==list(b),'whole key order '+label)
  for k in a:same(a[k],b[k],label+'/'+k)
 elif isinstance(a,list):
  need(len(a)==len(b),'whole list length '+label)
  for i,(x,y) in enumerate(zip(a,b)):same(x,y,label+'/'+str(i))
 else:need(a==b,'whole scalar '+label)
def lexical(names):
 need(len(names)==len(set(names)),'duplicate-free full relative paths')
 return sorted(names) # Explicit Python Unicode code-point lexical rule on BOTH lists.
def extent(root):
 root=Path(root)
 need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary extent root')
 files=[];dirs=[]
 for q in root.rglob('*'):
  rel=q.relative_to(root).as_posix()
  need(q.resolve()==q,'no path escape or symlink')
  if stat.S_ISDIR(q.lstat().st_mode):dirs.append(rel)
  else:need(stat.S_ISREG(q.lstat().st_mode),'ordinary extent entry');files.append(rel)
 return lexical(files),lexical(dirs)

need(D==B/'verification/rational-point-editorial-fact-audit-sol-20261115','exact own root')
need(sys.argv[1:] in [[],['--preseal']],'only safe default or initial preseal')
refs=obj(D/'SOURCE_ROOT_REFERENCES.json')
need(refs['current_editorial_folder_listed_or_read'] is False,'source-first exposure')
need(refs['original_science_or_primary_corpora_recopied'] is False,'corpora by reference')
need(len(refs['namespaces'])==4,'exact four original extents')
counts=[]
for r,rel in zip(refs['namespaces'],['sources','reviews/scope','reviews/adversarial','reviews/root']):
 root=P/rel
 need(r['root']==str(root),'fixed original root')
 actual_files,actual_dirs=extent(root)
 need(actual_files==lexical(list(r['files'])),'full original file identities')
 need(actual_dirs==lexical(r['directories']),'full original directory identities')
 for n,v in r['files'].items():matches(root/n,v)
 counts.append([len(actual_files),len(actual_dirs)])
need(counts==[[126,17],[424,7],[292,7],[33,2]],'original finite exact counts')
matches(refs['authority']['path'],refs['authority'])
a=obj(refs['authority']['path'])
need(a['scientific_review_complete'] is True and a['substantive_defect_found'] is False,'actual original root disposition')
need(a['ordinary_editorial_preparation_authorized'] is True,'editorial-only authorization')
need(a['publication_installation_deployment_verified'] is False and a['canonical_AA_assignment_authorized'] is False,'no production/AA authority')
need(a['canonical_url'] is None and a['follow_up'] is None,'literal root nulls')
need(a['native_tracker_transition_pending_after_actual_checkpoint'] is True,'historical pending flag kept literal')
core=refs['qualified_core17_plus_sole405b']
need(len(core)==18,'qualified17 plus405b')
need(sum(x['SHA256']=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0' for x in core)==1,'sole405b')
for x in core:matches(x['path'],x)
matches(refs['core_descriptor_prior_immutable_context']['path'],refs['core_descriptor_prior_immutable_context'])

n=obj(D/'EXPECTED_NATIVE_METADATA.json')
w=obj(D/'EXPECTED_NATIVE_API_WRAPPERS.json')
for r in w['original_objects']:
 q=P/'sources'/r['relative_source_path'];matches(q,r)
 same(obj(q),r['whole_original_object'],'API/'+r['relative_source_path'])
need([r['relative_source_path'] for r in w['original_objects']]==['record.response.body','latest.response.body','latest.response.body.redirect-01','versions-page001.response.body','files.response.body'],'exact five wrapper order')
record=obj(P/'sources/record.response.body')
files=obj(P/'sources/files.response.body')
ready=obj(P/'sources/SOURCE_READY.json')
same(record['metadata'],n['whole_original_record_metadata'],'record/metadata')
same(record['files'],n['whole_original_record_asset_array'],'record/files')
same(files,n['whole_original_files_API_object'],'files API')
same(ready['all_native_assets_in_original_order'],n['whole_original_SOURCE_READY_asset_custody'],'complete READY asset wrappers')
same(record,obj(P/'sources/latest.response.body.redirect-01'),'actual redirected latest200')
need(read(P/'sources/latest.response.body.redirect-01')==read(P/'sources/record.response.body'),'redirected200 whole bytes')
same(obj(P/'sources/latest.response.body'),{'status':301,'message':'Redirecting...','location':'https://zenodo.org/api/records/23205305'},'literal301')
versions=obj(P/'sources/versions-page001.response.body')
need(type(versions['hits']['total']) is int and versions['hits']['total']==1,'one integer total')
need(len(versions['hits']['hits'])==1 and 'next' not in versions['links'],'one exhaustive version')
expected_hit=dict(record);expected_hit['swh']=None
same(versions['hits']['hits'][0],expected_hit,'version hit swhnull versus recordemptyobject')
need(record['swh']=={} and versions['hits']['hits'][0]['swh'] is None,'distinct original swh fields')
need('version' not in record['metadata'],'native version absent')
need(ready['version_field_present'] is False and ready['version'] is None,'original version wrapper null')
need(ready['printed_version'] is None and a['printed_version_present'] is False,'printed version absent')
need(record['metadata']['publication_date']=='2026-10-06' and record['created']=='2026-10-07T06:43:32.613843+00:00','declared date and UTC creation')
need(record['metadata']['creators'][0]['affiliation'] is None,'literal affiliationnull')
need([x['key'] for x in record['files']]==['source.zip','verification.zip','paper.pdf','height-repair.pdf'],'ZIP ZIP PDF PDF native order')
need(ready['whole_regular_payload_occurrences']==61 and ready['all_native_reader_total_pages']==10,'archive occurrence and PDF totals')
need([x['opaque_byte_splitlines_count'] for x in ready['controlling_TeX_sources_in_original_archive_order']]==[325,371],'original TeX archive order')
need(ready['mathematical_PDF_TeX_or_pixels_read'] is False and ready['TeX_preamble_or_mathematical_body_read'] is False,'literal historical intake unread flags')
need(ready['source_scientific_proofs_code_results_triage_reviews_or_opinions_read'] is False and ready['source_programmes_executed']==[],'literal historical intake execution flags')
need(ready['scientific_verdict'] is None and ready['publication_authority'] is False,'literal source null verdict/falseauthority')
for r in ready['all_native_assets_in_original_order']:
 matches(r['path'],r)
 raw=read(r['path'])
 need('md5:'+hashlib.md5(raw).hexdigest()==r['original_api_file_object']['checksum'],'native MD5 exact asset')
for m,lines,pages in zip(n['both_complete_original_manuscripts'],[371,325],[6,4]):
 matches(m['native_PDF']['path'],m['native_PDF'])
 matches(m['TeX_reference']['path'],m['TeX_reference'])
 tex=read(m['TeX_reference']['path']).decode()
 need(len(tex.splitlines())==lines==m['TeX_reference']['lines_personally_read'],'complete TeX line extent')
 need(tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]==m['full_original_abstract_TeX'],'complete printed abstract')
 need(tex.split('\\title{',1)[1].split('}\n\\author',1)[0]==m['full_original_title_TeX'],'complete printed title')
 need(m['PDF_pages_personally_read']==pages and len(m['fresh_own_individual_rasters'])==pages,'complete page and fresh raster extent')
 for i,r in enumerate(m['fresh_own_individual_rasters'],1):
  need(r['page']==i and r['fresh_own_individually_visually_read'] is True,'individual fresh page reading')
  matches(D/r['path'],r)
for r in n['whole_original_LICENSES']:
 matches(r['path'],r);need(read(r['path']).decode()==r['whole_original_license_text'],'whole original license text')
need(n['prose']=='CC BY4.0' and n['authored_code']=='MIT','actual mixed authored rights')
e=obj(D/'INITIAL_EXPECTATIONS.json')
need(e['source_first_exposure']['current_editorial_folder_listed'] is False and e['source_first_exposure']['current_editorial_body_or_code_read'] is False,'INITIAL before writer exposure')
need(e['root_editorial_copy_code_adoption'] is False and e['production_authority'] is False,'no adoption or install authority')
need(e['canonical_url'] is None and e['AA'] is None and e['follow_up'] is None,'own null assignment/followup')

own_files,own_dirs=extent(D)
if sys.argv[1:]==['--preseal']:
 spec=obj(D/'PRESEAL_NAMESPACE.json')
 need(own_files==lexical(spec['files']) and own_dirs==lexical(spec['directories']),'exact finite preseal own extent')
else:
 seal=obj(D/'INITIAL_SEAL.json');manifest=obj(D/'INITIAL_MANIFEST.json')
 matches(D/'INITIAL_MANIFEST.json',seal['manifest'])
 need(seal['exact_root_terminal_exclusions']==['INITIAL_MANIFEST.json','INITIAL_SEAL.json'],'exact two terminal exclusions')
 expected=lexical(list(manifest['files'])+seal['exact_root_terminal_exclusions'])
 need(own_files==expected and own_dirs==lexical(manifest['directories']),'exact closed INITIAL files/directories')
 for rel,r in manifest['files'].items():matches(D/rel,r)
 need(len(manifest['files'])==seal['payload_files'] and len(own_files)==seal['actual_files'],'literal INITIAL counts')
print(json.dumps({'status':'PASS_SOURCE_ROOT_ONLY_INITIAL_CUSTODY','checks':checks,'recursive_typed_nodes':typed,'original_extents':counts,'original_files':sum(x[0] for x in counts),'native_assets':4,'complete_PDF_pages':[6,4],'complete_TeX_lines':[371,325],'fresh_individual_rasters':10,'qualified_core':'17original_plus405b','current_editorial_exposure':False,'new_scientific_native_build_foreign_or_network_execution':False,'production_authority':False,'root_adoption':False,'AA':None,'follow_up':None,'mode':'preseal' if sys.argv[1:] else 'strict_default'},ensure_ascii=False))
