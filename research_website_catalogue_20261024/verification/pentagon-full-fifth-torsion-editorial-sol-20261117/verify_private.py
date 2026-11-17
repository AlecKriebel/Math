"""Fresh passive custody/static-validation/finite-seal utility; it never authors the article or runs source code."""
import datetime, hashlib, json, stat, sys
from html.parser import HTMLParser
from pathlib import Path
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN=P/'verification/pentagon-full-fifth-torsion-editorial-sol-20261117'
SRC=P/'papers/23137834/sources';PAGE=OWN/'private-page'
assert sys.argv[1:] in (['before'],['after'],['freeze'])
phase=sys.argv[1]
def encoded(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def save(name,v):
    with (OWN/name).open('xb') as f:f.write(encoded(v))
def pin(p):
    a=p.lstat();assert stat.S_ISREG(a.st_mode) and not p.is_symlink();raw=p.read_bytes();b=p.lstat();key=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
    assert key(a)==key(b) and len(raw)==a.st_size
    return {'bytes':len(raw),'SHA256':hashlib.sha256(raw).hexdigest(),'MD5':hashlib.md5(raw).hexdigest(),'mode':oct(stat.S_IMODE(a.st_mode))}
def census(root):
    files={};dirs={'.':oct(stat.S_IMODE(root.lstat().st_mode))};todo=[root]
    while todo:
        here=todo.pop();a=here.lstat();assert stat.S_ISDIR(a.st_mode) and not here.is_symlink()
        for p in sorted(here.iterdir()):
            n=p.relative_to(root).as_posix();s=p.lstat();assert not p.is_symlink()
            if stat.S_ISDIR(s.st_mode):dirs[n]=oct(stat.S_IMODE(s.st_mode));todo.append(p)
            else:files[n]=pin(p)
        b=here.lstat();assert (a.st_dev,a.st_ino,a.st_mode,a.st_mtime_ns,a.st_ctime_ns)==(b.st_dev,b.st_ino,b.st_mode,b.st_mtime_ns,b.st_ctime_ns)
    paths=set(files)|set(dirs)
    return {'root':str(root),'root_mode':dirs['.'],'files':files,'directories':{n:m for n,m in dirs.items() if n!='.'},'hidden_paths':sorted(n for n in paths if n!='.' and any(s.startswith('.') for s in n.split('/'))),'empty_files':sorted(n for n,p in files.items() if p['bytes']==0),'empty_directories':sorted(n for n in dirs if n!='.' and not any(x.startswith(n+'/') for x in paths))}
def load(p):return json.loads(p.read_bytes())
if phase in ('before','after'):
    source=census(SRC);sm=load(SRC/'SOURCE_MANIFEST.json')
    assert len(source['files'])==sm['ordinary_files_including_controls']==97 and len(source['directories'])==sm['child_directory_count']==7
    assert source['files']['SOURCE_FINAL.json']['SHA256']=='14cbf430570b90574e7c28bba911e7fe2b868c164107591b1783694c30212f80'
    assert source['files']['SOURCE_MANIFEST.json']['SHA256']=='7f2ec5e3f4d6fa358bc9dcc5af3ef5adb4ec3e3b2b8851ff831f8b4574dcd2ed'
    rows={r['path']:{k:r[k] for k in ('bytes','SHA256','mode')} for r in sm['files']}
    assert len(rows)==len(sm['files']) and rows=={n:{k:p[k] for k in ('bytes','SHA256','mode')} for n,p in source['files'].items() if n not in ('SOURCE_FINAL.json','SOURCE_MANIFEST.json')}
    assert {r['path']:r['mode'] for r in sm['directories']}==source['directories']
    expected={'papers/23137834/reviews/root-continuation-20261117/ROOT_REVIEW.md':(15716,'acd210977221457737949db0684d2c60c289fef197b6b4dcaa26d87c8aa99599'),'verification/root-clearance-23137834-20261117.json':(2546,'55ea79efc35b209694e5afd51edd42ffa6994cb6ca755e83c981494b7e291951'),'verification/d4-canonical-potential-editorial-v2-sol-20261117/private-page/research.css':(1170,'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a')}
    inputs={n:pin(P/n) for n in expected};assert all((inputs[n]['bytes'],inputs[n]['SHA256'])==v for n,v in expected.items())
    result={'schema':'complete-pentagon-private-fixed-input-custody-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':phase,'source':source,'fixed_inputs':inputs}
    if phase=='after':
        before=load(OWN/'CUSTODY_BEFORE.json');assert all(before[k]==result[k] for k in ('source','fixed_inputs'))
    save('CUSTODY_'+phase.upper()+'.json',result)
    if phase=='before':print(json.dumps({'phase':'before','source_files_childdirs':[97,7],'whole_bytes_modes_hidden_empty_topology_authenticated':True,'fixed_inputs_exact':True}));raise SystemExit(0)
    model=load(OWN/'MODEL.json');record=load(SRC/'record.response.body');meta=record['metadata'];text=(PAGE/'index.html').read_text()
    assert meta['title']==model['title'] and meta['doi']==model['DOI']=='10.5281/zenodo.23137834' and meta['version']==model['native_version']=='1.0' and meta['publication_date']==model['native_publication_date']=='2026-10-04'
    tex=(SRC/'published-source/container-001/tree/manuscript.tex').read_text();rawabs=tex.split(r'\begin{abstract}',1)[1].split(r'\end{abstract}',1)[0]
    assert ' '.join(rawabs.split())==' '.join(model['abstract']['source_TeX'].split())
    abstract=rawabs
    for r in model['abstract']['literal_rendering_replacements']:abstract=abstract.replace(r['from'],r['to'])
    abstract=' '.join(abstract.split());assert '$' not in abstract and '\\' not in abstract and abstract==model['abstract']['normalized_full_text']
    class Parse(HTMLParser):
        def __init__(self):super().__init__(convert_charrefs=True);self.meta={};self.links=[];self.iframes=[];self.h1=0;self.scripts=[];self.inscript=False;self.inabs=False;self.abstract=[];self.canonical=[]
        def handle_starttag(self,tag,attrs):
            a=dict(attrs)
            if tag=='meta' and 'name' in a:self.meta[a['name']]=a.get('content','')
            if tag=='h1':self.h1+=1
            if tag=='script' and a.get('type')=='application/ld+json':self.scripts.append('');self.inscript=True
            if tag=='p' and a.get('id')=='manuscript-abstract':self.inabs=True
            if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a)
            if tag=='iframe':self.iframes.append(a)
            self.links.extend(a[k] for k in ('href','src') if k in a)
        def handle_endtag(self,tag):
            if tag=='script':self.inscript=False
            if tag=='p':self.inabs=False
        def handle_data(self,data):
            if self.inscript:self.scripts[-1]+=data
            if self.inabs:self.abstract.append(data)
    q=Parse();q.feed(text);q.close();assert q.h1==1 and len(q.scripts)==1
    scholar=json.loads(q.scripts[0]);assert scholar['@type']=='ScholarlyArticle' and '@graph' not in scholar
    assert abstract==''.join(q.abstract)==q.meta['citation_abstract']==q.meta['DC.description']==scholar['abstract']
    assert q.meta['citation_title']==model['title'] and q.meta['citation_doi']==model['DOI'] and q.meta['citation_version']=='1.0' and q.meta['citation_publication_date']=='2026/10/04'
    assert q.meta['robots']=='noindex,nofollow' and not q.canonical and scholar['datePublished']=='2026-10-04'
    assets=model['native_assets_in_original_order'];assert [a['native_filename'] for a in assets]==[f['key'] for f in record['files']]==['pentagonal-torsion-note.pdf','pentagonal-torsion-verification.zip']
    for a,f in zip(assets,record['files']):
        src=pin(SRC/'assets'/a['native_filename']);assert src==pin(PAGE/a['local_filename']) and src['bytes']==a['bytes']==f['size'] and src['SHA256']==a['SHA256'] and 'md5:'+src['MD5']==f['checksum']
    assert [a['name'] for a in scholar['encoding']]==[a['native_filename'] for a in assets]
    assert len(q.iframes)==1 and q.iframes[0]['src']=='pentagonal-torsion-note.pdf' and q.iframes[0]['title']
    for link in q.links:
        if not link.startswith(('http://','https://','#','/')):assert (PAGE/link).is_file(),link
    assert pin(PAGE/'research.css')==inputs['verification/d4-canonical-potential-editorial-v2-sol-20261117/private-page/research.css']
    assert all(model[k] is None for k in ('actual_canonical','base_url','production_url','page_publication_date','AA','legacy_redirect','follow_up'))
    assert model['rights']['original_note_and_authored_verification_material']=='CC-BY-4.0'
    checks={'schema':'directly-authored-private-pentagon-static-checks-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'STATIC_COPY_AND_CUSTODY_CHECKS_PASSED','authoring_route':'Direct plain HTML/JSON/Bib authoring and ordinary unchanged native file copies','builder_invocations':0,'scientific_executions':0,'page':pin(PAGE/'index.html'),'model':pin(OWN/'MODEL.json'),'abstract_normalized_SHA256':hashlib.sha256(abstract.encode()).hexdigest(),'complete_visible_DC_citation_Scholar_abstract_identical':True,'single_ScholarlyArticle_no_graph':True,'native_assets_original_order_bytes_modes_exact':True,'original_CSS_exact':True,'PDF_iframe_open_download_same_original':True,'all_local_targets_present':True,'source97_7_and_fixed_inputs_before_after_exact':True,'noindex_all_production_fields_null':True,'browser_live_UI_collision_legacy_independent_fact_certificate':False,'publication_authority':False}
    save('STATIC_CHECKS.json',checks);print(json.dumps(checks));raise SystemExit(0)
checks=load(OWN/'STATIC_CHECKS.json');assert checks['status']=='STATIC_COPY_AND_CUSTODY_CHECKS_PASSED'
before=load(OWN/'CUSTODY_BEFORE.json');after=load(OWN/'CUSTODY_AFTER.json');assert all(before[k]==after[k] for k in ('source','fixed_inputs'))
names=('FINAL_MANIFEST.json','FINAL.json')
for n in names:
    with (OWN/n).open('xb'):pass
c=census(OWN);files={n:p for n,p in c['files'].items() if n not in names};modes={n:c['files'][n]['mode'] for n in names};now=datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest={'schema':'finite-direct-pentagon-private-whole-namespace-v1','UTC':now,'root':str(OWN),'root_mode':c['root_mode'],'file_count':len(files)+2,'child_directory_count':len(c['directories']),'payload_files':files,'directories':c['directories'],'hidden_paths':c['hidden_paths'],'empty_files':sorted(n for n,p in files.items() if p['bytes']==0),'empty_directories':c['empty_directories'],'terminal_pair':[{'path':n,'bytes':0,'mode':modes[n],'recursive_hash_excluded':True} for n in names]}
final={'schema':'direct-private-pentagon-editorial-FINAL-v1','UTC':now,'record':'23137834','status':'FROZEN_PRIVATE_EDITORIAL_AWAITING_ROOT_FACT_REVIEW','completion_percent_private_preparation':100,'publication_authority':False,'canonical':None,'base_url':None,'production_url':None,'page_publication_date':None,'AA':None,'legacy_redirect':None,'follow_up':None,'builder_invocations':0,'scientific_executions':0,'literal_unexpected_errors':0,'file_count':len(files)+2,'child_directory_count':len(c['directories']),'manifest':{'bytes':0,'SHA256':'0'*64,'mode':modes[names[0]]},'own_bytes':0,'own_mode':modes[names[1]],'page':files['private-page/index.html'],'model':files['MODEL.json'],'report':files['EDITORIAL_REPORT.md'],'static_checks':files['STATIC_CHECKS.json'],'whole_source97_7_and_fixed_inputs_before_after_exact':True,'native_file_order':['pentagonal-torsion-note.pdf','pentagonal-torsion-verification.zip'],'all_publication_fields_null_and_noindex':True,'browser_live_UI_collision_legacy_independent_fact_certificate':False,'only_terminal_recursive_hash_exclusions':list(names),'self_hash_delivered_externally':True,'stop':True}
for unused in range(20):
    lengths=(len(encoded(manifest)),len(encoded(final)))
    for r in manifest['terminal_pair']:r['bytes']=lengths[names.index(r['path'])]
    final['manifest']['bytes']=lengths[0];final['own_bytes']=lengths[1]
    if lengths==(len(encoded(manifest)),len(encoded(final))):break
else:raise AssertionError('terminal length fixed point')
mb=encoded(manifest);final['manifest']['SHA256']=hashlib.sha256(mb).hexdigest();fb=encoded(final);assert lengths==(len(mb),len(fb))
(OWN/names[0]).write_bytes(mb);(OWN/names[1]).write_bytes(fb);end=census(OWN)
assert {n:p for n,p in end['files'].items() if n not in names}==files and end['directories']==c['directories'] and end['root_mode']==c['root_mode']
assert end['files'][names[0]]['SHA256']==final['manifest']['SHA256'] and all(end['files'][n]['bytes']==r['bytes'] and end['files'][n]['mode']==r['mode'] for n,r in zip(names,manifest['terminal_pair']))
print(json.dumps({'status':final['status'],'file_count':len(files)+2,'child_directory_count':len(c['directories']),'FINAL_MANIFEST':pin(OWN/names[0]),'FINAL':pin(OWN/names[1]),'page':pin(PAGE/'index.html'),'model':pin(OWN/'MODEL.json'),'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
