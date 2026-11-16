"""Independent full source/HTML/aggregate/native-index custody audit.
Default only, read-only. No writer imports, subprocess, network or file writes.
Own strict FINAL closure is additionally checked when its two controls exist.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,urljoin,unquote
import difflib,hashlib,html,json,os,re,stat,struct,sys
import xml.etree.ElementTree as ET
N=Path(__file__).absolute().parent
P=N.parent.parent
S=P/'verification/three-research-private-stage-sol-20261115'
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
COUNT=0
def need(x,s):
    global COUNT
    COUNT+=1
    if not x:raise ValueError(s)
def pin(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def read(p):
    need(p.is_absolute() and p.resolve()==p,'ordinary canonical path '+str(p))
    first=p.lstat();need(stat.S_ISREG(first.st_mode),'ordinary file')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        before=os.fstat(fd);need((first.st_dev,first.st_ino)==(before.st_dev,before.st_ino),'held identity')
        chunks=[]
        while True:
            b=os.read(fd,1048576)
            if not b:break
            chunks.append(b)
        after=os.fstat(fd);last=p.lstat();b=b''.join(chunks)
        need((before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns),'stable full body')
        need((last.st_dev,last.st_ino)==(before.st_dev,before.st_ino) and len(b)==before.st_size,'stable path/full read')
        return b
    finally:os.close(fd)
def obj(p):return json.loads(read(p))
def bound(r):
    b=read(Path(r['path']));need(pin(b)=={k:r[k] for k in ['bytes','SHA256']},'whole pin '+r['path']);return b
def typed(a,b):
    need(type(a) is type(b),'JSON literal type')
    if type(a) is dict:
        need(list(a)==list(b),'whole JSON key/order')
        for k in a:typed(a[k],b[k])
    elif type(a) is list:
        need(len(a)==len(b),'whole JSON list extent')
        for x,y in zip(a,b):typed(x,y)
    else:need(a==b,'literal scalar/null/history')
def extent(root):
    need(root.resolve()==root,'ordinary namespace root');fs,ds=[],[]
    def walk(d):
        first=d.lstat();need(stat.S_ISDIR(first.st_mode),'ordinary directory')
        for e in sorted(os.scandir(d),key=lambda x:x.name):
            p=Path(e.path);r=p.relative_to(root).as_posix();m=p.lstat().st_mode
            if stat.S_ISDIR(m):ds.append(r);walk(p)
            else:need(stat.S_ISREG(m),'reject special/symlink');fs.append(r)
        last=d.lstat();need((first.st_dev,first.st_ino,first.st_mtime_ns,first.st_ctime_ns)==(last.st_dev,last.st_ino,last.st_mtime_ns,last.st_ctime_ns),'stable namespace')
    walk(root);return sorted(fs),sorted(ds)
def manifest(root,sealsha,manifestsha):
    sb=read(root/'FINAL_SEAL.json');mb=read(root/'OWNED_MANIFEST.json')
    need(pin(sb)['SHA256']==sealsha and pin(mb)['SHA256']==manifestsha,'forwarded exact closed writer controls')
    s=json.loads(sb);m=json.loads(mb);need(s['manifest']==pin(mb),'writer manifest binding')
    fs,ds=extent(root);terms=['FINAL_SEAL.json','OWNED_MANIFEST.json']
    need(m['exact_root_terminal_exclusions']==terms and m['subtree_or_future_exclusions']==[],'only exact root terminals')
    need(fs==sorted([r['path'] for r in m['files']]+terms) and ds==m['directories'],'entire writer namespace closed')
    for r in m['files']:need(pin(read(root/r['path']))=={k:r[k] for k in ['bytes','SHA256']},'every writer payload')
    need(len(fs)==85 and len(ds)==14,'writer85/14')
    return s,m
class Page(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.tags=[];self.ids=[];self.data=[];self.title=False;self.titles=[]
    def handle_starttag(self,t,attrs):
        need(len(attrs)==len(dict(attrs)),'no duplicate HTML attribute')
        a=dict(attrs);self.tags.append((t,a))
        if 'id' in a:self.ids.append(a['id'])
        if t=='title':self.title=True
    def handle_endtag(self,t):
        if t=='title':self.title=False
    def handle_data(self,x):
        self.data.append(x)
        if self.title:self.titles.append(x)
def jsonld(text):
    blocks=re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S)
    need(len(blocks)==1,'exactly one scholarly JSON script');return json.loads(blocks[0])
def native(raw):
    need(raw[:4]==b'DIRC' and hashlib.sha1(raw[:-20]).digest()==raw[-20:],'native index header/SHA1')
    version,count=struct.unpack('>II',raw[4:12]);need((version,count)==(2,58571),'whole native v2/58571')
    p=12;end=len(raw)-20;rows=[]
    for _ in range(count):
        start=p;need(p+62<=end,'whole native record');flags=struct.unpack('>H',raw[p+60:p+62])[0]
        need(flags&0xf000==0,'native stage0 flags');stop=raw.find(b'\0',p+62,end);need(stop>=0,'native path terminator')
        name=raw[p+62:stop];need(name and flags&0xfff==min(len(name),4095),'native path byte length')
        p=start+((stop-start+1+7)//8)*8;need(p<=end and not any(raw[stop:p]),'whole native padding')
        rows.append((name,raw[start:p]))
    need(p==end,'actual native extension extent0')
    need([n for n,r in rows]==sorted({n for n,r in rows}),'all native paths unique/order')
    excluded={b'firebase.json',b'public/research/index.html',b'public/research/sitemap.xml'}
    need(excluded<={n for n,r in rows},'three tracked replacements')
    kept=[(n,r) for n,r in rows if n not in excluded];need(len(kept)==58568,'19path scope protects58568')
    return {'records':count,'extension_bytes':0,'proposed_tracked_replacements':3,'proposed_protected_records':len(kept),'protected_whole_native_record_SHA256':hashlib.sha256(b''.join(n+b'\0'+r for n,r in kept)).hexdigest()}
def baseline(old):
    fs,ds=extent(W/'public');need(fs==old['public_files'] and ds==old['public_directories'],'fresh entire public namespace')
    for r in old['public_configs_controls']:bound(r)
    raw=read(W/'.git/index');need(raw==bound(old['complete_raw_index']),'fresh raw index exact original bytes')
    need(stat.S_IMODE((W/'.git/index').lstat().st_mode)==384 and not os.path.lexists(W/'.git/index.lock'),'fresh0600 and no indexlock')
    need((W/'.git/HEAD').read_bytes()==b'ref: refs/heads/master\n','current master branch')
    need((W/'.git/refs/heads/master').read_bytes()==b'2b78e689e571e658daa859f29b97a61b9ec479ed\n','current fixed master HEAD')
    return native(raw)
def main():
    need(sys.argv[1:]==[],'only pure default')
    initial=obj(N/'INITIAL_SEAL.json')
    need(pin(read(N/'INITIAL_SEAL.json'))['SHA256']=='2b902a2ba26423ad090f8fc9e11639b95f43bc6e3d3b4b2f9dc67a2a8cbc3930','own preexposure INITIAL')
    for r in initial['files']:bound(r)
    scope=obj(N/'ADDITIONAL_PRIVATE_HOSTING_SCOPE_SEAL.json');bound(scope['payload']);bound(scope['root_scope']);proposed=bound(scope['root_proposed_config'])
    approved=obj(N/'APPROVED_INPUTS.json');expect=obj(N/'INITIAL_EXPECTATIONS.json');old=obj(N/'PRE_BASELINE.json')
    for r in approved['all_original_files']:bound(r)
    for group in approved['closed_original_namespaces']:
        need(extent(Path(group['path']))==(group['files'],group['directories']),'all14 original namespace extents')
    writer_seal,writer_manifest=manifest(S,'4f9cb2f5c8779a586bbfa34efc6f498d677bcd15826f28f7c4f4ecf33cd43b11','6dda8ccc7e599d5dfff04d6c45a00ddff21ad55c7f0195153ed594aa2539db9f')
    code=read(S/'stage_three.py');need(pin(code)=={'bytes':24045,'SHA256':'44ed6c1ffa36b5f2a853516c4de6346d2903cafe35e462fadf4e0e295454ded6'},'personally read current helper')
    change=obj(S/'CURRENT_CODE_UPDATE.json');prior=bound(change['prepare_time_code_preserved']);bound(change['current_code'])
    diff=''.join(difflib.unified_diff(prior.decode().splitlines(keepends=True),code.decode().splitlines(keepends=True),fromfile='first-prepare',tofile='current'))
    need(diff==change['exact_unified_diff'],'actual first/current exact diff, only sealing metadata/receipt binding')
    tracked=read(S/'TRACKED_SCOPE_ADDENDUM.json');need(pin(tracked)=={'bytes':1529,'SHA256':'2f44866d923a0880719c8d7acbcfa21db7aa1241a687eb2773460bb80a3f7ec8'},'actual additive tracked scope')
    refs=obj(S/'REFERENCE_INPUTS.json');extra=0
    for group in refs['complete_frozen_namespaces_by_reference'].values():
        root=Path(group['root']);need(extent(root)==(sorted(r['relative_path'] for r in group['files']),group['directories']),'writer all7 original frozen extents')
        for r in group['files']:bound(r);extra+=1
    need(extra==2743,'all2743 wider source/editorial/fact/prior-interface files')
    bound(refs['qualified_core']['reference'])
    for r in refs['qualified_core']['named17_original_plus_sole_authorized405b']:bound(r)
    need(len(refs['qualified_core']['named17_original_plus_sole_authorized405b'])==18,'17 original plus sole405b qualification')
    before=baseline(old)
    expected_paths={'firebase.json','public/research/index.html','public/research/sitemap.xml'}
    for r in approved['records']:
        expected_paths.update('public/research/'+r['slug']+'/'+name for name in ['index.html','citation.bib',*[a['key'] for a in r['native_assets_in_original_order']]])
    fs,ds=extent(S/'candidate');need(set(fs)==expected_paths and len(fs)==19,'independent exact19 candidate pathset')
    need(ds==sorted({p.as_posix() for name in fs for p in Path(name).parents if p.as_posix()!='.'}),'exact candidate directories')
    actual_frames=[];native_count=0;abstracts=[];pdf_readers=0;media_orders={}
    for r,e in zip(approved['records'],expect['records']):
        root='public/research/'+r['slug']+'/';page=read(S/'candidate'/root/'index.html');mainb=bound(r['approved_MAIN'])
        need(page.count(mainb)==1,'entire approved MAIN exactly once')
        text=page.decode();body=text.split('<body>',1)[1];start=body.index(mainb.decode());end=start+len(mainb.decode())
        prefix=body[:start];suffix=body[end:]
        need(prefix==expect['native_frame']['body_prefix_before_MAIN'].replace('href="#main"','href="'+e['skip_target']+'"'),'exact native header/skip/navigation')
        need(suffix==expect['native_frame']['body_suffix_after_MAIN'],'exact native footer/ending after complete MAIN buffer')
        doc=Page();doc.feed(text);doc.close();need(len(doc.ids)==len(set(doc.ids)),'unique HTML IDs')
        need([a.get('id') for t,a in doc.tags if t=='main']==[e['semantic_main_id']],'semantic MAIN')
        need(doc.titles==[e['SEO']['title']],'exact approved descriptive title')
        named=[(a['name'],a.get('content')) for t,a in doc.tags if t=='meta' and 'name' in a];need(len(named)==len(dict(named)),'unique name metadata');meta=dict(named)
        props=[(a['property'],a.get('content')) for t,a in doc.tags if t=='meta' and 'property' in a];need(len(props)==len(dict(props)),'unique social metadata');props=dict(props)
        for k,v in {'description':e['SEO']['description'],'robots':'index,follow','citation_title':e['title'],'citation_publication_date':e['datePublished'].replace('-','/'),'citation_doi':e['DOI'],'citation_author_orcid':e['ORCID'],'citation_pdf_url':e['canonical_proposal']+'paper.pdf','citation_language':'en','author':'Alec Kriebel'}.items():need(meta[k]==v,'exact scholarly/meta '+k)
        need(('citation_version' in meta)==e['version']['present'],'original citation version presence')
        if e['version']['present']:need(meta['citation_version']=='1.0','literal132version1.0')
        need(props['og:url']==e['canonical_proposal'] and props['og:type']=='article' and props['article:published_time']==e['datePublished'],'social canonical/date')
        need([a['href'] for t,a in doc.tags if t=='link' and a.get('rel')=='canonical']==[e['canonical_proposal']],'one exact proposed canonical')
        need([a['href'] for t,a in doc.tags if t=='link' and a.get('rel')=='stylesheet']==['/research/research.css'],'native shared stylesheet only')
        need([a.get('href') for t,a in doc.tags if t=='a' and a.get('class')=='skip-link']==[e['skip_target']],'correct skip anchor')
        need([a for t,a in doc.tags if t=='script']==[{'type':'application/ld+json'}],'no executable or external scripts')
        need(not any(t in ['form','input','button'] or any(k.startswith('on') for k in a) for t,a in doc.tags),'no contact or executable UI')
        graph=jsonld(text);need(graph['@context']=='https://schema.org' and len(graph['@graph'])==2,'WebPage/ScholarlyArticle graph')
        web,article=graph['@graph'];need(web['@type']=='WebPage' and article['@type']=='ScholarlyArticle','accurate schema roles')
        need(web['@id']==e['canonical_proposal']+'#page' and web['mainEntity']=={'@id':e['canonical_proposal']+'#article'} and article['mainEntityOfPage']=={'@id':web['@id']},'bidirectional page/article linkage')
        need(article['url']==web['url']==e['canonical_proposal'] and article['@id']==e['canonical_proposal']+'#article','all proposed scholarly page identities')
        need(article['abstract']==e['full_main_abstract'] and article['datePublished']==e['datePublished'],'complete abstract and actual original date')
        need(('version' in article)==e['version']['present'],'original schema version presence')
        if e['version']['present']:need(article['version']=='1.0','literal132schema1.0')
        sourcepath=Path(e['full_approved_scholarly_source']['path']);sourcebody=bound(e['full_approved_scholarly_source'])
        source=json.loads(sourcebody) if sourcepath.suffix=='.json' else jsonld(sourcebody.decode())
        mediakey='encoding' if 'encoding' in source else 'associatedMedia';before_media=source[mediakey];after_media=article[mediakey]
        need(len(before_media)==len(after_media)==len(r['native_assets_in_original_order']),'all original scholarly media')
        native={a['key']:a for a in r['native_assets_in_original_order']};order=[]
        for src,dst in zip(before_media,after_media):
            name=Path(urlsplit(src['contentUrl']).path).name;order.append(name);need(name in native,'original scholarly media basename')
            back={k:v for k,v in dst.items() if k!='sameAs'};back['contentUrl']=src['contentUrl'];typed(src,back)
            need(dst['contentUrl']==e['canonical_proposal']+name and dst['sameAs']==native[name]['original_asset_object']['original_api_file_object']['links']['self'],'absolute local scholarly media and exact native sameAs')
        for k,v in source.items():
            if k not in ['@id','url',mediakey]:typed(v,article[k])
        need(set(article)-set(source)<=set(['@id','mainEntityOfPage','isAccessibleForFree','creativeWorkStatus','description']),'only permitted schema additions')
        need(article['creativeWorkStatus']=='Unrefereed preprint' and article['isAccessibleForFree'] is True,'truthful status/access')
        media_orders[r['record_id']]={'native_asset_order':list(native),'unchanged_approved_scholarly_order':order}
        for a in r['native_assets_in_original_order']:
            b=read(Path(a['native_path']));need(pin(b)=={k:a[k] for k in ['bytes','SHA256']} and b==read(S/'candidate'/root/a['key']),'every complete original native asset unchanged')
            need(hashlib.md5(b).hexdigest()==a['original_asset_object']['original_api_file_object']['checksum'].split(':')[1],'original native checksum');native_count+=1
        need(bound(r['approved_Bib'])==read(S/'candidate'/root/'citation.bib'),'entire approved Bib unchanged')
        for t,a in doc.tags:
            link=a.get('src') if t=='iframe' else a.get('href') if t in ['a','link'] else None
            if not link:continue
            split=urlsplit(link)
            need(split.scheme in ['', 'https'],'safe original link scheme')
            if t=='iframe':need(a.get('title') and split.fragment=='view=FitH','original titled FitH reader');pdf_readers+=1
            if split.scheme:continue
            if not split.path:
                need(not split.fragment or unquote(split.fragment) in doc.ids,'local fragment resolves');continue
            path=urlsplit(urljoin(e['canonical_proposal'],link)).path
            relative=unquote(path).lstrip('/')+('index.html' if path.endswith('/') else '')
            need('..' not in Path(relative).parts,'bounded virtual target')
            candidate=S/'candidate/public'/relative
            actual=candidate if candidate.is_file() else W/'public'/relative
            need(actual.is_file() and actual.resolve()==actual,'all local virtual reader/download/nav/style/icon links resolve')
        actual_frames.append({'record_id':r['record_id'],'page':pin(page),'whole_MAIN':pin(mainb),'head_prefix':pin(page.split(mainb)[0]),'unchanged_native_assets':len(native),'whole_Bib':r['approved_Bib']})
        abstracts.append(article['abstract'])
    need(native_count==10 and pdf_readers==4 and len(set(abstracts))==3,'10native assets/4readers/3unique complete abstracts')
    old_index=read(N/'private/pre-index.html');new_index=read(S/'candidate/public/research/index.html')
    old_ld=jsonld(old_index.decode());new_ld=jsonld(new_index.decode());need(new_ld['mainEntity']['numberOfItems']==len(new_ld['mainEntity']['itemListElement'])==99,'99ItemList')
    back=json.loads(json.dumps(new_ld));back['mainEntity']['numberOfItems']=96;del back['mainEntity']['itemListElement'][96:];typed(old_ld,back)
    for pos,(item,r) in enumerate(zip(new_ld['mainEntity']['itemListElement'][96:],expect['records']),97):need(item=={'@type':'ListItem','position':pos,'url':r['canonical_proposal'],'name':r['title']},'exact addedItemList position/title/url')
    restored=new_index
    for r in expect['records']:
        href=urlsplit(r['canonical_proposal']).path.encode();pattern=rb'(?m)^      <li><a href="'+re.escape(href)+rb'">.*?</li>\n'
        hits=re.findall(pattern,restored);need(len(hits)==1,'one new rendered index entry')
        h=Page();h.feed(hits[0].decode());visible=''.join(h.data)
        need(r['title'] in visible and r['SEO']['description'] in visible and 'Unrefereed preprint' in visible,'accurate index title/status/description')
        need(any(t=='a' and a.get('href')==r['canonical_proposal'].replace('https://aleckriebel.com','')+'paper.pdf' for t,a in h.tags),'indexPDF')
        need(any(t=='a' and a.get('href')=='https://doi.org/'+r['DOI'] for t,a in h.tags),'indexDOI')
        restored=restored.replace(hits[0],b'',1)
    script_pattern=rb'(<script type="application/ld\+json">)(.*?)(</script>)';old_script=re.search(script_pattern,old_index,re.S).group(2);new_script=re.search(script_pattern,new_index,re.S).group(2)
    restored=restored.replace(new_script,old_script,1);need(restored==old_index,'all original index bytes recovered exactly')
    oldmap=read(N/'private/pre-sitemap.xml');newmap=read(S/'candidate/public/research/sitemap.xml');oldxml=ET.fromstring(oldmap);newxml=ET.fromstring(newmap)
    need(len(newxml)==100 and [ET.tostring(x).strip() for x in newxml[:97]]==[ET.tostring(x).strip() for x in oldxml],'all prior97sitemap objects unchanged')
    restored=newmap
    for r in expect['records']:
        pattern=rb'  <url><loc>'+re.escape(r['canonical_proposal'].encode())+rb'</loc><lastmod>\d{4}-\d{2}-\d{2}</lastmod></url>\n';hits=re.findall(pattern,restored);need(len(hits)==1,'one new sitemapURL');restored=restored.replace(hits[0],b'',1)
    need(restored==oldmap,'all original sitemap bytes recovered exactly')
    config=read(S/'candidate/firebase.json');current=read(W/'firebase.json');line=b'      "**/README.md",\n'
    need(config==proposed==current.replace(line,b'',1) and current.count(line)==1,'exact sole hostingignoreline removal')
    need('**/README.md' not in json.loads(config)['hosting']['ignore'],'native README unsuppressed by original broad ignore')
    need(not [x for x in old['public_files'] if Path(x).name=='README.md'],'prior existing README footprint0')
    need(len(old['public_files'])+16==647 and len(expected_paths)==19,'647virtualpublic/19totalpaths')
    need(baseline(old)==before,'whole final public/control/index fence exact')
    # Once sealed, every owned path, including private raw historical buffers, is finite.
    finalized=False
    if (N/'FINAL_SEAL.json').exists():
        seal=obj(N/'FINAL_SEAL.json');mb=read(N/'OWNED_MANIFEST.json');m=json.loads(mb);need(seal['manifest']==pin(mb),'own final manifest binding')
        fs,ds=extent(N);terms=['FINAL_SEAL.json','OWNED_MANIFEST.json'];need(fs==sorted([r['path'] for r in m['files']]+terms) and ds==m['directories'],'own entire strict FINAL namespace')
        need(m['exact_root_terminal_exclusions']==terms and m['subtree_or_future_exclusions']==[],'own only exact root terminals')
        for r in m['files']:need(pin(read(N/r['path']))=={k:r[k] for k in ['bytes','SHA256']},'own entire final payload unchanged')
        finalized=True
    print(json.dumps({'status':'PASS_PRIVATE_THREE_INDEPENDENT_INTEGRATION_WITH_RECORDED_EXPECTATION_QUALIFICATION','checks':COUNT,'strict_own_FINAL':finalized,'writer_owned_extent':[85,14],'original_initial_paths_rehashed':2212,'original_initial_namespaces_rechecked':14,'wider_frozen_files_rehashed':extra,'wider_frozen_namespaces_rechecked':7,'source_core':'17 original plus sole405b','candidate_paths':19,'virtual_counts':[647,99,100],'whole_MAIN_bytes':40599,'unchanged_native_assets':10,'unchanged_Bibs':3,'titled_original_PDF_readers':4,'native_index':before,'metadata_media_order_qualification':media_orders,'all_original_index_sitemap_bytes_recovered':True,'whole_current_baseline_public_files':631,'writer_helper_imported_or_executed_by_this_guard':False,'writes':0,'network_requests':0,'new_scientific_verdict':None,'browser_or_live_verified':False,'production_authority':False,'canonical_url':None,'AA':None,'follow_up':None},ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
