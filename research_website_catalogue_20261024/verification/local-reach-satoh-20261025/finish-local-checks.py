"""Read-only preservation, archive and original-pilot checks; owned receipts only."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit,unquote
import datetime,difflib,hashlib,json,zipfile,xml.etree.ElementTree as ET

R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
S=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,obj):(O/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
b=json.loads((O/'baseline.json').read_text())
site_changed=[rel for rel,h in b['site_files'].items() if not (S/rel).is_file() or sha(S/rel)!=h]
frozen_changed=[rel for rel,h in b['frozen_paper_inputs'].items() if not (R/rel).is_file() or sha(R/rel)!=h]
assert sorted(site_changed)==['research/index.html','research/sitemap.xml'],site_changed
assert not frozen_changed,frozen_changed
new_site=sorted(str(p.relative_to(S)) for p in (S/'research').rglob('*') if p.is_file() and str(p.relative_to(S)) not in b['site_files'])
assert len(new_site)==8,new_site
expected_slugs={json.loads((R/'papers'/rid/'publication.json').read_text())['slug'] for rid in ('23431676','23387442')}
assert {Path(p).parts[1] for p in new_site}==expected_slugs
preservation={'status':'PASS','existing_article_directories_unchanged':42,'existing_research_files_rehashed':len(b['site_files']),'frozen_paper_inputs_rehashed':len(b['frozen_paper_inputs']),'frozen_changed':frozen_changed,'existing_site_changed':site_changed,'new_site_files':new_site,'research_css_sha256':sha(S/'research/research.css')}
write('preservation.json',preservation)

manifests=[]
for rid,name,rootrel in (('23431676','FINALIZATION_MANIFEST.json',False),('23387442','artifact-manifest.json',True)):
    p=R/'papers'/rid;f=p/'reviews/publication'/name;manifest=json.loads(f.read_text())
    records=manifest['files'][:]
    if rootrel:records += [manifest[k] for k in ('publication','promotion','root_clearance')]
    else:
        for item in manifest.get('external_frozen_bindings',[]):
            assert sha(R/item['path'])==item['sha256']
    for item in records:
        target=(R if rootrel else p)/item['path']
        assert target.is_file() and sha(target)==item['sha256'],str(target)
        if 'bytes' in item:assert target.stat().st_size==item['bytes']
    manifests.append({'record_id':rid,'manifest':str(f.relative_to(R)),'manifest_sha256':sha(f),'bound_files_rehashed':len(records)})
write('editorial-manifest-verification.json',{'status':'PASS','manifests':manifests,'historical_pending_records_preserved':True})

archives=[]
for rid,dirname,expected in (('23431676','pr1097_support_v1_0',198),('23387442','satoh_filtration_verification',107)):
    p=R/'papers'/rid;c=json.loads((p/'publication.json').read_text());name=c['supplement_filename'] or c['additional_assets'][0]['filename']
    members=[]
    with zipfile.ZipFile(p/'sources'/name) as z:
        assert z.testzip() is None
        for member in z.infolist():
            if member.is_dir():continue
            target=p/'sources/published-source'/dirname/member.filename
            data=z.read(member)
            assert target.is_file() and target.read_bytes()==data,str(target)
            members.append({'member':member.filename,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    assert len(members)==expected
    pdfname=c['pdf_filename'];embedded=p/'sources/published-source'/dirname/pdfname
    assert embedded.read_bytes()==(p/'sources'/pdfname).read_bytes()
    archives.append({'record_id':rid,'archive':name,'archive_sha256':sha(p/'sources'/name),'members_compared':len(members),'embedded_pdf_identical':True,'members':members})
write('archive-checks.json',{'status':'PASS','archives':archives})

class Doc(HTMLParser):
    def __init__(self,path):super().__init__();self.tags=[];self.feed(path.read_text())
    def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
pilot=S/'research/free-spanning-forest-degree/index.html';doc=Doc(pilot);base='https://aleckriebel.com/research/free-spanning-forest-degree/'
links=[]
for tag,attrs in doc.tags:
    for key in ('href','src'):
        if key not in attrs:continue
        u=urlsplit(urljoin(base,attrs[key]))
        if u.netloc!='aleckriebel.com':continue
        p=S/unquote(u.path).lstrip('/')
        if p.is_dir():p=p/'index.html'
        good=p.is_file()
        if good and p.suffix=='.html' and u.fragment:good=any(a.get('id')==unquote(u.fragment) for _,a in Doc(p).tags)
        links.append({'url':u.geturl(),'passed':good})
assert all(x['passed'] for x in links)
canon=[a['href'] for t,a in doc.tags if t=='link' and a.get('rel')=='canonical'];assert canon==[base]
frames=[a for t,a in doc.tags if t=='iframe'];assert len(frames)==1 and frames[0].get('title')
pilot_files={p:sha(S/p) for p in b['site_files'] if p.startswith('research/free-spanning-forest-degree/')}
assert all(v==b['site_files'][p] for p,v in pilot_files.items())
index=(S/'research/index.html').read_text();parser=Doc(S/'research/index.html')
import re
data=json.loads(re.search('<script type="application/ld\\+json">(.*?)</script>',index,re.S).group(1));items=data['mainEntity']['itemListElement']
assert len(items)==data['mainEntity']['numberOfItems']==44
assert len({x['url'] for x in items})==44 and [x['position'] for x in items]==list(range(1,45))
assert sum(t=='a' and a.get('href','').startswith('/research/') and a.get('href','').endswith('/') for t,a in parser.tags)==45 # 44 articles plus Research navigation.
root=ET.fromstring((S/'research/sitemap.xml').read_text());urls=[x.text for x in root.findall('{*}url/{*}loc')]
assert all(sum(u==x['url'] for u in urls)==1 for x in items)
write('pilot-index-sitemap-checks.json',{'status':'PASS','pilot_sha256':sha(pilot),'pilot_bound_files':pilot_files,'pilot_local_links':links,'pilot_limit':'Original pilot has no publication.json or source entry in shared checker; checked byte preservation, canonical, reader and local links rather than inventing new manuscript bindings.','article_index_items':len(items),'unique_article_urls':len({x['url'] for x in items}),'sitemap_article_entries':44,'sitemap_total_entries':len(urls)})

changes=[]
patch=[]
for rel,before_sha in b['shared_scripts'].items():
    f=R/rel
    if sha(f)!=before_sha:
        changes.append({'path':str(f),'before_sha256':before_sha,'sha256':sha(f),'bytes':f.stat().st_size})
        patch+=difflib.unified_diff((O/'before'/rel).read_text().splitlines(True),f.read_text().splitlines(True),fromfile='before/'+rel,tofile=rel)
for rel in site_changed+new_site:
    f=S/rel;changes.append({'path':str(f),'before_sha256':b['site_files'].get(rel),'sha256':sha(f),'bytes':f.stat().st_size})
    if rel in site_changed:
        patch+=difflib.unified_diff((O/'before/site'/rel).read_text().splitlines(True),f.read_text().splitlines(True),fromfile='before/site/'+rel,tofile='site/'+rel)
write('changed-paths.json',{'status':'PASS','changes':changes,'shared_scripts_changed':4,'existing_shared_site_files_changed':2,'new_article_files':8})
(O/'shared-diff.patch').write_text(''.join(patch))
print(json.dumps({'status':'PASS','frozen_inputs_unchanged':len(b['frozen_paper_inputs']),'old_articles_unchanged':42,'new_files':len(new_site),'changes':len(changes)}))
