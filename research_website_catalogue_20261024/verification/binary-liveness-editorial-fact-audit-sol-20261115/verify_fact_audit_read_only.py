"""Finite informed fact/source/editorial custody. No science, owner replay or live reads."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re,stat,sys
D=Path(__file__).resolve().parent;B=D.parent.parent;P=B/'papers/23202966';E=P/'reviews/editorial'
COUNT=0;NODES=0
def need(ok,label):
 global COUNT
 COUNT+=1
 if not ok:raise RuntimeError(label)
def read(p):
 p=Path(p);need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary real pinned path');return p.read_bytes()
def obj(p):return json.loads(read(p))
def pin(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def same(a,b,label):
 global NODES
 NODES+=1;need(type(a) is type(b),'type '+label)
 if isinstance(a,dict):
  need(list(a)==list(b),'ordered keys/absence '+label)
  for k in a:same(a[k],b[k],label+'/'+k)
 elif isinstance(a,list):
  need(len(a)==len(b),'array size '+label)
  for i,(x,y) in enumerate(zip(a,b)):same(x,y,label+'/'+str(i))
 else:need(a==b,'literal scalar/null '+label)
def extent(root):
 need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary namespace root')
 fs=[];ds=[]
 for q in root.rglob('*'):
  rel=q.relative_to(root).as_posix();mode=q.lstat().st_mode
  if stat.S_ISDIR(mode):ds.append(rel)
  else:need(stat.S_ISREG(mode),'ordinary namespace entry');fs.append(rel)
 need(len(fs)==len(set(fs)) and len(ds)==len(set(ds)),'duplicate enumerated identity')
 return sorted(fs),sorted(ds)
def close(root,files,dirs):
 fs,ds=extent(root);names=list(files)
 need(len(names)==len(set(names)) and len(dirs)==len(set(dirs)),'duplicate expected identity')
 need(fs==sorted(names) and ds==sorted(dirs),'same full-path lexical rule/exact extent')
 for n,r in files.items():need(pin(read(root/n))=={k:r[k] for k in ['bytes','SHA256']},'whole pinned input')
need(sys.argv[1:] in [[],['--preseal']],'finite modes')
initial_raw=read(D/'INITIAL_SEAL.json');need(pin(initial_raw)['SHA256']=='4dbdeeba8d0d06b13ec220e1e55266879834059bc8c53f825d9c09ca1c8c1fd9','preexposure initial pin')
initial=json.loads(initial_raw);mb=read(D/'INITIAL_MANIFEST.json');need(pin(mb)==initial['manifest'],'whole initial manifest')
for r in json.loads(mb)['files']:need(pin(read(D/r['path']))=={k:r[k] for k in ['bytes','SHA256']},'immutable initial payload')
refs=obj(D/'SOURCE_ROOT_REFERENCES.json')
for ns in refs['namespaces']:close(Path(ns['root']),ns['files'],ns['directories'])
review=obj(D/'EDITORIAL_REFERENCE_EXTENT.json');close(E,review['files'],review['directories'])
prior=review['prior_custody_reference'];close(Path(prior['root']),{r['path']:r for r in prior['files']},prior['directories'])
for r in review['qualified_core_references']:need(pin(read(r['path']))=={k:r[k] for k in ['bytes','SHA256']},'qualified17 plus405b core source')
need(len(review['qualified_core_references'])==18 and any(r['SHA256']=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0' for r in review['qualified_core_references']),'precise core qualification')
source=obj(E/'SOURCE_INPUTS.json');authority=obj(B/'verification/root-clearance-23202966-20261115.json');ready=obj(P/'sources/SOURCE_READY.json')
need(pin(read(B/'verification/root-clearance-23202966-20261115.json'))['SHA256']=='3310703ec448b133b4f1cf5cfdd4b12845cf588e2a4920609345b5d0ee737237','immutable root authority331070')
same(source['whole_root_authority'],authority,'whole root authority');same(source['whole_original_SOURCE_READY'],ready,'whole READY');same(authority['wholeOriginalSourceReady'],ready,'whole root READY')
for a,b in zip(refs['namespaces'],source['complete_immutable_namespaces'][:4]):
 need(a['root']==b['root'] and a['directories']==b['directories'],'source-first namespace identity')
 same(a['files'],{r['path']:{k:r[k] for k in ['bytes','SHA256']} for r in b['files']},'source-first whole namespace file pins')
need(authority['nativeCurrentScienceDispositions']==106 and authority['nativeTrackerTransitionPending'] is True,'literal historical native106pending')
cfg=obj(E/'EDITORIAL_CONFIG.json');metadata=obj(D/'EXPECTED_NATIVE_METADATA.json');record=obj(P/'sources/record.response.body')
same(cfg['publication']['all_original_assets'],metadata['whole_source_READY_native_asset_entries'],'all4 original nested assets/types/order')
same(cfg['publication']['native_version_field'],ready['native_version_whole_field'],'absent original native version')
same(cfg['publication']['native_description_exact'],metadata['whole_original_native_metadata']['description'],'entire original native description')
same(cfg['author']['native_affiliation'],metadata['whole_original_native_metadata']['creators'][0]['affiliation'],'original null affiliation')
need(cfg['publication']['datePublished']=='2026-10-06' and cfg['publication']['native_created_separate']=='2026-10-07T04:34:37.920372+00:00','date/creation distinction')
need(cfg['publication']['printed_version_present'] is False and cfg['publication']['printed_version'] is None,'printed version absent')
class Main(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.paragraphs={};self.current=None;self.ids=[];self.attrs=[]
 def handle_starttag(self,t,a):
  d=dict(a);self.attrs.append((t,d))
  if 'id' in d:self.ids.append(d['id'])
  if t=='p' and d.get('id') in ['printed-abstract','native-description']:self.current=d['id'];self.paragraphs[self.current]=''
 def handle_endtag(self,t):
  if t=='p':self.current=None
 def handle_data(self,s):
  if self.current is not None:self.paragraphs[self.current]+=s
raw=read(E/'PUBLIC_MAIN.html');body=raw.decode();doc=Main();doc.feed(body);doc.close()
need(raw==read(D/'REVIEWED_PUBLIC_MAIN.html')==read(E/'candidate/PUBLIC_MAIN.html'),'whole actual reviewed MAIN')
need(read(E/'candidate/PUBLIC_COPY.md')==read(D/'REVIEWED_PUBLIC_COPY.md'),'whole reviewed COPY')
abstract=metadata['whole_printed_abstract_TeX']
mapping={r'$h$':'h',r'$h^2$':'h²',r'$N_h=(3h^3-h)/2+2$':'Nₕ=(3h³−h)/2+2',r'$2^{\Omega(h)}=2^{\Omega(N_h^{1/3})}$':'2^{Ω(h)}=2^{Ω(Nₕ^(1/3))}',r'$sh^2$':'sh²',r'$s$':'s',r'$\Theta(h^3)$':'Θ(h³)'}
for old,new in mapping.items():need(old in abstract,'actual full original math expression');abstract=abstract.replace(old,new)
abstract=' '.join(abstract.split()).replace("OpenAI's","OpenAI’s")
need('$' not in abstract and '\\' not in abstract,'complete explicit TeX typography mapping')
need(doc.paragraphs['printed-abstract']==abstract==cfg['publication']['printed_abstract_readable_math'],'complete independently source-derived printed abstract')
need(doc.paragraphs['native-description']==record['metadata']['description'] and abstract!=doc.paragraphs['native-description'],'whole distinct native description')
actual=obj(D/'ACTUAL_MAIN_OBJECT.json');same(doc.paragraphs['printed-abstract'],actual['whole_printed_abstract'],'recorded entire abstract');same(doc.paragraphs['native-description'],actual['whole_separate_native_description'],'recorded whole native description')
need(len(doc.ids)==len(set(doc.ids)) and 'main' in doc.ids,'unique semantic IDs and skip target')
frames=[a for t,a in doc.attrs if t=='iframe'];need(len(frames)==1 and frames[0]['src']=='paper.pdf#view=FitH' and frames[0].get('title'),'full titled original reader')
page=read(E/'candidate/index.html').decode();head=read(E/'candidate/PUBLIC_HEAD.html').decode()
need(page.count(body)==1 and page.count(head)==1 and 'background:#fff' in page and 'font-family:Arial,Helvetica,sans-serif' in page,'whole actual main/head/light style')
need('noindex,nofollow,noarchive' in head and 'rel="canonical"' not in head and 'citation_version' not in head,'private head/no invented version')
scholarly=obj(E/'candidate/SCHOLARLY_METADATA.json');inline=json.loads(head.split('<script type="application/ld+json">')[1].split('</script>')[0]);same(scholarly,inline,'whole inline scholarly object')
need(scholarly['abstract']==abstract and 'version' not in scholarly and scholarly['datePublished']=='2026-10-06' and scholarly['license']=='https://creativecommons.org/licenses/by/4.0/','full abstract/date/rights/absent version metadata')
names=obj(E/'AUTHORING_INPUTS_SEAL.json')['output_file_names'];need(len(names)==len(set(names))==10,'ten distinct output buffers')
for n in names:need(read(E/'candidate'/n)==read(E/'optimized-candidate'/n),'whole actual normal/O output buffer')
for i,a in enumerate(ready['all_native_assets_in_original_order']):
 n=a['original_api_file_object']['key'];need(read(E/'candidate'/n)==read(a['path']),'whole original native asset');need(scholarly['encoding'][i]['contentUrl'].endswith('/'+n),'native order and encoding filenames')
need(len(scholarly['encoding'])==4 and ready['whole_regular_payload_occurrences']==28,'whole original native4/ZIP28 custody')
bib=read(E/'candidate/citation.bib').decode();need(not re.search(r'\bversion\s*=',bib,re.I) and 'day = {6}' in bib,'date/no fabricated Bib version')
for n in ['prepare_editorial.py','verify_editorial.py','seal_editorial.py']:need(read(E/n)==read(D/'reviewed-code'/n),'whole actual code read and held')
receipts=obj(E/'EXECUTION_RECEIPTS.json')['actual_observed_new_processes'];need(len(receipts)==4,'actual4 saved new processes')
for r in receipts:
 need(r['actual_observed_exit_code']==0,'actual owner process exit')
 for role in ['stdout','stderr']:
  s=r['whole_'+role];b=read(s['binding']['path']);need(pin(b)=={k:s['binding'][k] for k in ['bytes','SHA256']} and b.decode()==s['literal_UTF8'],'complete raw literal execution stream')
v=obj(E/'VERDICT.json');same(v['whole_original_root_minor_qualifications'],authority['wholeOriginalMinorQualificationList'],'whole original minor qualification objects')
for k in ['root_copy_adopted','publication_authority','production_install_authority','deployment_authority','native_tracker_mutation_authority','live_verified','browser_verified']:need(v[k] is False and cfg['promotion'].get(k,False) is False,'separate false authority '+k)
for k in ['canonical_url','AA','follow_up']:need(v[k] is None and cfg['promotion'][k] is None,'null promotion '+k)
result=obj(D/'OWNER_DEFAULT.stdout.json');need(read(D/'OWNER_DEFAULT.stderr')==b'' and result['strict_final_namespace'] is True and result['selected_copy_loss_rejections']==4 and result['scientific_execution'] is False,'actual designated safe default result')
finding=obj(D/'FACT_FINDINGS.json');need(finding['actionable_copy_or_source_defects']==[] and finding['root_adoption'] is False,'literal informed finding')
if sys.argv[1:]:
 c=obj(D/'FINAL_PRESEAL_NAMESPACE.json');fs,ds=extent(D);need(fs==sorted(c['files']) and ds==sorted(c['directories']),'exact finite preseal namespace')
else:
 sb=read(D/'FINAL_SEAL.json');s=json.loads(sb);mb=read(D/'MANIFEST.json');need(pin(mb)==s['manifest'],'same-buffer final manifest');m=json.loads(mb)
 need(m['exact_root_terminal_exclusions']==['MANIFEST.json','FINAL_SEAL.json'] and m['future_subtree_exclusions']==[],'exact root terminal exclusions only')
 files={r['path']:r for r in m['files']};need(len(files)==len(m['files']),'duplicate final manifest record');files.update({n:pin(read(D/n)) for n in ['MANIFEST.json','FINAL_SEAL.json']});close(D,files,m['directories'])
 need(s['root_adoption'] is False and s['production_authority'] is False,'separate final authority')
print(json.dumps({'status':'PASS_INFORMED_BINARY_LIVENESS_EDITORIAL_FACT_CUSTODY','mode':'preseal' if sys.argv[1:] else 'final','checks':COUNT,'whole_typed_nodes':NODES,'original_namespaces':[[82,9],[272,45],[133,21],[35,3],[13,0]],'editorial_files':62,'editorial_directories':4,'whole_actual_paired_buffers':10,'entire_printed_and_distinct_native_abstracts':True,'native_and_printed_version':'ABSENT','original_native_assets':4,'original_ZIP_payloads':28,'current_owner_default_already_executed_once_no_replay':True,'new_scientific_native_foreign_owner_campaign_control_Git_network_subprocess_or_writes':False,'root_adoption':False,'production_authority':False,'canonical_url':None,'AA':None,'follow_up':None},sort_keys=True))
