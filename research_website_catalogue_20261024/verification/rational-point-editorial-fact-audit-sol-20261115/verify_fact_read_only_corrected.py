"""Independent informed fact/copy custody, standard library and read-only.

No project imports, subprocess, network, scientific computation or writes.
References are the source-first INITIAL, original source/root and exact59-file
editorial FINAL. Strict final extent excludes only two exact root terminals.
"""
from pathlib import Path
from html.parser import HTMLParser
import base64,hashlib,json,re,stat,sys
D=Path(__file__).resolve().parent;B=D.parent.parent
E=B/'papers/23205305/reviews/editorial'
C=0;T=0
def need(ok,why):
 global C
 C+=1
 if not ok:raise RuntimeError(why)
def read(p):
 p=Path(p);need(p.is_absolute() and p.resolve()==p,'ordinary absolute path')
 need(stat.S_ISREG(p.lstat().st_mode),'regular file, not symlink/special')
 return p.read_bytes()
def pairs(rows):
 d={}
 for k,v in rows:need(k not in d,'duplicate JSON key');d[k]=v
 return d
def obj(p):return json.loads(read(p),object_pairs_hook=pairs)
def pin(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def match(p,r):need(pin(read(p))=={k:r[k] for k in ['bytes','SHA256']},'whole original bytes '+str(p))
def lex(xs):need(len(xs)==len(set(xs)),'duplicate full paths');return sorted(xs)
def same(a,b,label):
 global T
 T+=1;need(type(a) is type(b),'literal type '+label)
 if isinstance(a,dict):
  need(list(a)==list(b),'literal ordered keys '+label)
  for k in a:same(a[k],b[k],label+'/'+k)
 elif isinstance(a,list):
  need(len(a)==len(b),'literal list length '+label)
  for i,(x,y) in enumerate(zip(a,b)):same(x,y,label+'/'+str(i))
 else:need(a==b,'literal scalar '+label)
def extent(root):
 root=Path(root);need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary root')
 fs=[];ds=[]
 for p in root.rglob('*'):
  n=p.relative_to(root).as_posix();need(p.resolve()==p,'no escaped entry')
  if stat.S_ISDIR(p.lstat().st_mode):ds.append(n)
  else:need(stat.S_ISREG(p.lstat().st_mode),'regular extent entry');fs.append(n)
 return lex(fs),lex(ds)
def check_extent(root,files,dirs):
 af,ad=extent(root);need(af==lex(list(files)) and ad==lex(dirs),'exact full file/directory identities')
 for n,r in files.items():match(Path(root)/n,r)
 return af,ad
def norm(s):return ' '.join(s.replace('’',"'").split())
def abstract(s):return norm(s.replace(r'\cite{Pinned}','[1]').replace(r'$\Q$','ℚ').replace('$',''))
class Page(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.tags=[];self.text=[]
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
 def handle_data(self,s):self.text.append(s)
def parsed(s):p=Page();p.feed(s);return p
def stream(r):
 b=base64.b64decode(r['base64'],validate=True)
 need(pin(b)=={k:r[k] for k in ['bytes','SHA256']},'whole native stream SHA/size')
 need(b.decode()==r['literal_UTF8'],'whole native stream literal interface')
 return b

need(D==B/'verification/rational-point-editorial-fact-audit-sol-20261115','exact ownroot')
need(sys.argv[1:] in [[],['--preseal']],'only bounded custody modes')
match(D/'INITIAL_SEAL.json',{'bytes':2999,'SHA256':'8e4b3a4e1e72c2eae39750bf4ec30577f5737810c7e9d52b1312902d26359491'})
initial=obj(D/'INITIAL_SEAL.json');match(D/'INITIAL_MANIFEST.json',initial['manifest'])
im=obj(D/'INITIAL_MANIFEST.json')
need(im['exact_root_terminal_exclusions']==['INITIAL_MANIFEST.json','INITIAL_SEAL.json'] and im['future_subtree_exclusions']==[],'initial finite exact terminals')
for n,r in im['files'].items():match(D/n,r)
need(initial['current_editorial_folder_listed_or_read'] is False,'initial before current writer exposure')
refs=obj(D/'SOURCE_ROOT_REFERENCES.json')
for r in refs['namespaces']:check_extent(r['root'],r['files'],r['directories'])
need([(len(r['files']),len(r['directories'])) for r in refs['namespaces']]==[(126,17),(424,7),(292,7),(33,2)],'original875 exact finite extents')
match(refs['authority']['path'],refs['authority'])
authority=obj(refs['authority']['path'])
need(authority['ordinary_editorial_preparation_authorized'] is True and authority['source_repaired_or_claim_narrowed'] is False,'actual full root scientific authority')
need(authority['native_tracker_transition_pending_after_actual_checkpoint'] is True,'historical pending literal')
need(authority['publication_installation_deployment_verified'] is False and authority['canonical_AA_assignment_authorized'] is False and authority['canonical_url'] is None and authority['follow_up'] is None,'root authority limits')
core=refs['qualified_core17_plus_sole405b'];need(len(core)==18,'17original plus sole405b')
for r in core:match(r['path'],r)
match(refs['core_descriptor_prior_immutable_context']['path'],refs['core_descriptor_prior_immutable_context'])
native=obj(D/'EXPECTED_NATIVE_METADATA.json')
wrappers=obj(D/'EXPECTED_NATIVE_API_WRAPPERS.json')
S=Path(refs['namespaces'][0]['root'])
for r in wrappers['original_objects']:
 match(S/r['relative_source_path'],r);same(obj(S/r['relative_source_path']),r['whole_original_object'],'whole native '+r['relative_source_path'])
record=obj(S/'record.response.body');ready=obj(S/'SOURCE_READY.json')
same(record['metadata'],native['whole_original_record_metadata'],'whole original native metadata')
same(ready['all_native_assets_in_original_order'],native['whole_original_SOURCE_READY_asset_custody'],'whole original native asset custody')
for m in native['both_complete_original_manuscripts']:
 match(m['native_PDF']['path'],m['native_PDF']);match(m['TeX_reference']['path'],m['TeX_reference'])
 for r in m['fresh_own_individual_rasters']:match(D/r['path'],r)
for r in native['whole_original_LICENSES']:match(r['path'],r)

er=obj(D/'EDITORIAL_REFERENCE_EXTENT.json')
need(er['root']==str(E),'exact editorialroot')
af,ad=check_extent(E,er['files'],er['directories'])
need(len(af)==59 and len(ad)==5,'editorial59files5dirs')
match(E/'FINAL_SEAL.json',{'bytes':2213,'SHA256':'75ee87613b40d710c6e4dd7d0bcf2046954587bd75474f18a862bf882668b35a'})
seal=obj(E/'FINAL_SEAL.json');om=obj(E/'OWNED_MANIFEST.json')
terms=['CLOSURE.json','FINAL_SEAL.json','OWNED_MANIFEST.json']
need(om['exact_root_terminal_exclusions']==terms and seal['exact_root_terminals']==terms,'exact root terminals no basenamehole')
need(seal['manifest_SHA256']==pin(read(E/'OWNED_MANIFEST.json'))['SHA256'] and seal['closure_SHA256']==pin(read(E/'CLOSURE.json'))['SHA256'],'actual whole manifest and closure')
need([x['path'] for x in om['files']]==lex([x['path'] for x in om['files']]),'sorted duplicatefree manifest payload')
need(lex([x['path'] for x in om['files']]+terms)==af and lex(om['directories'])==ad,'closed owner full identity')
for r in om['files']:match(E/r['path'],r)
protected=obj(E/'PROTECTED_INPUTS.json')
for label,r in zip(['source','scope','adversarial','root'],refs['namespaces']):
 p=protected['namespaces'][label]
 need(p['root']==r['root'] and p['directories']==r['directories'] and p['no_exclusions'] is True,'same source-first protected extent')
 need(lex([x['relative_path'] for x in p['files']])==lex(list(r['files'])),'same protected file identities')
 for x in p['files']:
  need(x['path']==str(Path(r['root'])/x['relative_path']) and {k:x[k] for k in ['bytes','SHA256']}==r['files'][x['relative_path']],'same original protection bytes')
same(protected['qualified_core']['named17_original_plus_sole_authorized405b'],[{k:r[k] for k in ['path','bytes','SHA256']} for r in core],'same qualified18 source inputs')
match(protected['qualified_core']['reference']['path'],protected['qualified_core']['reference'])
c=obj(E/'EDITORIAL_CONFIG.json');copy=obj(E/'COPY.json');expect=obj(E/'SOURCE_EXPECTATIONS.json');pub=c['publication']
same(pub['all_original_assets'],native['whole_original_SOURCE_READY_asset_custody'],'current all4 entire asset wrappers versus pre-exposure')
same(expect['native_metadata_whole_original'],native['whole_original_record_metadata'],'current whole metadata versus pre-exposure')
same(expect['all_four_native_assets_original_order'],native['whole_original_SOURCE_READY_asset_custody'],'current expectation all4 wrappers versus original')
for i,key in enumerate(['main_abstract','companion_abstract']):
 m=native['both_complete_original_manuscripts'][i]
 need(norm(copy[key])==abstract(m['full_original_abstract_TeX']),'entire faithful printed abstract '+key)
 need(pub[['main_printed_abstract_full','companion_printed_abstract_full'][i]]==copy[key],'whole config abstract')
need(norm(copy['companion_title'])==norm(native['both_complete_original_manuscripts'][1]['full_original_title_TeX'].replace(chr(92)*2,' ')),'full actual conditional companion title, explicit TeX linebreak rendered as space')
need(copy['title']==native['whole_original_record_metadata']['title']==c['title'],'full main title')
need(copy['native_description']==pub['native_description_exact']==native['native_full_description_distinct_from_both_printed_abstracts'],'whole separate native description')
need(pub['datePublished']=='2026-10-06' and pub['native_created_separate']==native['native_creation_UTC'],'date versus UTC creation')
need(pub['native_version_field']=={'present':False,'original_value':None} and pub['printed_version_present'] is False and pub['printed_version'] is None,'absent native/printed versions')
need(c['author']['ORCID']=='https://orcid.org/0009-0001-9320-500X' and c['author']['native_affiliation'] is None,'exact native author metadata')
for k in ['canonical_url','AA','follow_up']:need(c['promotion'][k] is None and seal[k] is None,'null nonauthority '+k)
for k in ['root_copy_adopted','production_install_authority','deployment_authority','native_tracker_mutation_authority','live_verified','browser_verified']:need(c['promotion'][k] is False,'false authority '+k)
names=['COPY.md','HEAD.html','PUBLIC_MAIN.html','citation.bib','height-repair.pdf','index.html','paper.pdf','source.zip','style.css','verification.zip']
for mode in ['normal','optimized']:
 fs,ds=extent(E/mode);need(fs==names and ds==[],'exact ten flat outputs')
 for n in names:need(read(E/mode/n)==read(E/'normal'/n),'all ten whole outputs normal/O')
 for a in pub['all_original_assets']:
  key=a['original_api_file_object']['key'];need(read(E/mode/key)==read(a['path']),'whole unchanged nativeasset')
main=read(E/'normal/PUBLIC_MAIN.html').decode();head=read(E/'normal/HEAD.html').decode();md=read(E/'normal/COPY.md').decode()
need(read(E/'normal/index.html')==('<!doctype html>\n<html lang="en">\n<head>\n'+head+'</head>\n<body>\n'+main+'</body>\n</html>\n').encode(),'whole standalone candidate exact head MAIN ending')
page=parsed(main);h=parsed(head);plain=' '.join(page.text)
need([(t,a.get('id')) for t,a in page.tags if t=='main']==[('main','main')],'single semantic main')
ids=[a['id'] for t,a in page.tags if 'id' in a];need(len(ids)==len(set(ids)),'unique semantic ids')
for t,a in page.tags:
 if 'aria-labelledby' in a:need(a['aria-labelledby'] in ids,'existing accessible label')
need([a['src'] for t,a in page.tags if t=='iframe']==['paper.pdf#view=FitH','height-repair.pdf#view=FitH'],'two FitH readers')
need(all(a.get('title') for t,a in page.tags if t=='iframe'),'both titled readers')
need(main.index('height-repair.pdf#view=FitH')<main.index('printed-main-abstract'),'both readers upfront')
need([a['href'] for t,a in page.tags if t=='a' and a.get('data-native-asset')=='true']==['source.zip','verification.zip','paper.pdf','height-repair.pdf'],'original native download order')
paragraphs=[copy[k] for k in ['intro','main_abstract','companion_abstract','native_description','rights_paragraph']]
paragraphs += [p for s in copy['sections'] for p in s['paragraphs']+s.get('items',[])]
for p in paragraphs:need(norm(p) in norm(plain) and p in md,'entire copy paragraph/item in both main and Markdown')
metas={a.get('name',a.get('property')):a.get('content') for t,a in h.tags if t=='meta'}
need(metas['robots']=='noindex,nofollow,noarchive' and metas['citation_pdf_url']=='paper.pdf','private local metadata')
need(metas['citation_doi']=='10.5281/zenodo.23205305' and metas['citation_publication_date']=='2026/10/06','native DOI/date citation')
need('citation_version' not in metas and not any(t=='link' and a.get('rel')=='canonical' for t,a in h.tags),'no invented version/live canonical')
ld=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',head,re.S).group(1),object_pairs_hook=pairs)
need(ld['abstract']==copy['main_abstract'] and 'version' not in ld and ld['datePublished']=='2026-10-06','whole scholarly abstract/date/absence')
need(ld['license']=='https://creativecommons.org/licenses/by/4.0/','article prose license')
need([x['name'] for x in ld['associatedMedia']]==pub['native_asset_order'],'media order')
for a in ld['associatedMedia']:need('license' not in a and a['contentUrl']==a['name'],'no blanket mixedZIP/media license')
need(pub['rights']['original_verification_code']=='MIT' and pub['rights']['mixed_ZIP_blanket_license'] is None,'internal mixed-rights distinction')
need('version =' not in read(E/'normal/citation.bib').decode().lower(),'no invented Bib version')
need('color-scheme:light' in read(E/'normal/style.css').decode() and 'font-family:Arial,Helvetica,sans-serif' in read(E/'normal/style.css').decode(),'light readable Arial CSS')

receipts=obj(E/'EXECUTION_RECEIPTS.json')
for r,label in zip(receipts['runs'],['normal','optimized']):
 need(r['label']==label and r['exit_code']==0,'literal first authoring history exit')
 out=stream(r['stdout']);err=stream(r['stderr'])
 need(out==read(E/('AUTHORING_'+label+'.stdout')) and err==read(E/('AUTHORING_'+label+'.stderr'))==b'','whole actual authoring streams')
 data=json.loads(out,object_pairs_hook=pairs);need(data['output']==label,'literal normal/O wrapper distinction')
 need([x['name'] for x in data['files']]==names,'all ten actual published output receipts')
 for x in data['files']:match(E/label/x['name'],x)
closure=obj(E/'CLOSURE.json');need(closure['status']=='ACTUAL_NORMAL_O_DEFAULTS_PASS','owner actual finalization history')
raw=[]
for r in closure['runs']:
 need(r['exit_code']==0,'actual saved finalizer exit');out=stream(r['stdout']);need(stream(r['stderr'])==b'','actual saved stderr')
 need(json.loads(out)['final_seal_bound'] is False,'honest before-binding saved closure phase');raw.append(out)
need(len(raw)==2 and raw[0]==raw[1],'whole saved normal/O closure bytes')
own_default=obj(D/'OWNER_DEFAULT.stdout.json');need(own_default['final_seal_bound'] is True and own_default['writes']==0 and own_default['scientific_execution'] is False,'actual designated pure current default')
need(read(D/'OWNER_DEFAULT.stderr')==b'','designated pure empty stderr')

of,od=extent(D)
if sys.argv[1:]==['--preseal']:
 spec=obj(D/'FACT_CORRECTED_PRESEAL_NAMESPACE.json');need(of==lex(spec['files']) and od==lex(spec['directories']),'own finite preseal')
else:
 final=obj(D/'FINAL_SEAL.json');manifest=obj(D/'FINAL_MANIFEST.json');match(D/'FINAL_MANIFEST.json',final['manifest'])
 terms=['FINAL_MANIFEST.json','FINAL_SEAL.json'];need(final['exact_root_terminal_exclusions']==terms and final['future_subtree_exclusions']==[],'exact final terminal exclusions')
 need(of==lex(list(manifest['files'])+terms) and od==lex(manifest['directories']),'strict final ordinary file/directory extent')
 for n,r in manifest['files'].items():match(D/n,r)
 need(len(of)==final['actual_files'] and len(manifest['files'])==final['payload_files'],'literal final counts')
print(json.dumps({'status':'PASS_INFORMED_RATIONAL_POINT_EDITORIAL_FACT_CUSTODY','checks':C,'recursive_typed_nodes':T,'original_files':875,'editorial_files':59,'editorial_directories':5,'whole_paired_outputs':10,'native_original_assets':4,'INITIAL_preserved':True,'all_source_root_science_core_originals_preserved':True,'copy_defect_found':False,'new_scientific_verdict':None,'root_adoption':False,'production_authority':False,'canonical_url':None,'AA':None,'follow_up':None,'mode':'preseal' if sys.argv[1:] else 'strict_default'}))
