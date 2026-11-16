#!/usr/bin/env python3
"""One fixed read-only integration audit. Stdout only; no imports of project code."""
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit,unquote
import hashlib,json,os,re,stat,subprocess

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
R=P/'verification/knudson-annular-private-stage-sol-20261116'
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
M=Path('/Users/alec/Documents/Math')

def pin(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def fixed(p,row):
    assert not p.is_symlink(),str(p)
    b=p.read_bytes();assert pin(b)=={k:row[k] for k in ('bytes','SHA256')},str(p)
    if 'mode' in row:
        mode=row['mode'];mode=int(mode,8) if isinstance(mode,str) else mode
        assert stat.S_IMODE(p.stat().st_mode)==mode,str(p)
    return b
def load(p):return json.loads(p.read_bytes())
def one(s,pat):
    hits=re.findall(pat,s);assert len(hits)==1,pat
    return hits[0]
def git(repo,*args):
    return subprocess.run(['git','--no-optional-locks','-C',str(repo),*args],capture_output=True,check=True,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'}).stdout
def repo_guard(repo,expected):
    assert git(repo,'rev-parse','HEAD').decode().strip()==expected['HEAD']
    assert git(repo,'rev-parse','HEAD^{tree}').decode().strip()==expected['tree']
    assert git(repo,'symbolic-ref','HEAD').decode().strip()=='refs/heads/'+expected['branch']
    b=fixed(repo/'.git/index',expected['index'])
    assert b[:4]==b'DIRC' and int.from_bytes(b[8:12],'big')==expected['index']['records']
    return pin(b)
class Tags(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.meta={};self.links=[];self.ids=[];self.labels=[]
    def handle_starttag(self,t,attrs):
        d=dict(attrs)
        if t=='meta':self.meta[d.get('name',d.get('property'))]=d.get('content')
        if 'id' in d:self.ids.append(d['id'])
        self.labels.extend(d.get('aria-labelledby','').split())
        for key in ('href','src'):
            if key in d:self.links.append((t,key,d[key],d.get('rel')))
def article(s):return json.loads(one(s,r'<script type="application/ld\+json">([\s\S]*?)</script>'))
def raw_items(script):
    starts=list(re.finditer(r'"itemListElement"\s*:\s*\[',script));assert len(starts)==1
    pos=starts[0].end();decoder=json.JSONDecoder();out=[]
    while True:
        while script[pos].isspace():pos+=1
        if script[pos]==']':break
        value,end=decoder.raw_decode(script,pos);assert isinstance(value,dict)
        out.append(script[pos:end]);pos=end
        while script[pos].isspace():pos+=1
        if script[pos]==']':break
        assert script[pos]==',';pos+=1
    return out

def main():
    final_bytes=(R/'FINAL.json').read_bytes()
    assert hashlib.sha256(final_bytes).hexdigest()=='32fd7bab7c8af013b65fbf394430df484f5b88711eab089985d3f186f9f6c9cd'
    final=json.loads(final_bytes)
    manifest=json.loads(fixed(R/'MANIFEST.json',{'bytes':4996,'SHA256':'191058232ea998525418fff6cbcf4bf15b4b609a596e6f9acf81a213ae655a06'}))
    assert {str(q.relative_to(R)) for q in R.rglob('*') if q.is_file()}=={x['path'] for x in manifest['files']}|{'MANIFEST.json','FINAL.json'}
    assert sorted(str(q.relative_to(R)) for q in R.rglob('*') if q.is_dir())==manifest['child_directories']
    assert len(manifest['files'])+2==23 and len(manifest['child_directories'])==5
    assert not any(q.is_symlink() for q in R.rglob('*'))
    for row in manifest['files']:fixed(R/row['path'],row)
    base=json.loads(fixed(R/'BASELINE.json',final['BASELINE']))
    inputs=json.loads(fixed(R/'BUILD_INPUTS.json',final['BUILD_INPUTS']))
    assert base['W']['HEAD']=='a4cc214f0e3c6f65357ad5aef132dcea9ef84c5c'
    assert base['W']['tree']=='976ac25353272a6518e06ff5c5ee3159b3001e05'
    assert base['W']['index']['bytes']==9046318 and base['W']['index']['mode']=='0o600'
    assert base['W']['index']['SHA256']=='9ed792033a8d0df38c121b86c36edad16c1a6a86346a7cdf33be7a8d8154aa5a'
    before={'W':repo_guard(W,base['W']),'Math':repo_guard(M,base['Math'])}
    assert len(inputs['source_guards'])==64
    compact=json.dumps(inputs['source_guards'],sort_keys=True,separators=(',',':')).encode()
    assert hashlib.sha256(compact).hexdigest()==final['source_guards']['SHA256_of_sorted_key_compact_JSON_table']
    for row in inputs['source_guards']:fixed(P/row['path'],row)
    C=R/'candidate';candidates={str(q.relative_to(C)):q for q in C.rglob('*') if q.is_file()}
    expected={'public/research/index.html','public/research/sitemap.xml'}
    for row in inputs['pages']:
        prefix='public/research/'+row['slug']+'/'
        expected|={prefix+'index.html',prefix+'citation.bib'}|{prefix+x['name'] for x in row['native_assets_in_order']}
    assert set(candidates)==set(final['candidate_exact_paths'])==set(inputs['candidate_exact_paths'])==expected
    assert len(candidates)==11 and len([q for q in C.rglob('*') if q.is_dir()])==4
    for row in final['candidate_pins']:fixed(candidates[row['path']],row)
    oldfiles={x['path']:x for x in base['public_file_pins']}
    assert len(oldfiles)==base['public_files']==690
    newpaths=expected-set(oldfiles);modified=expected&set(oldfiles)
    assert len(newpaths)==9 and modified=={'public/research/index.html','public/research/sitemap.xml'}
    projected=set(oldfiles)|expected;assert len(projected)==699
    article_results=[];descriptions=[]
    for row in inputs['pages']:
        adoption=json.loads(fixed(P/row['adoption']['path'],row['adoption']))
        assert adoption['proposed_slug']==row['slug'] and adoption['whole_MAIN']==row['whole_MAIN']
        assert adoption['production_install_Git_deploy_or_tracker_authority'] is False
        private=fixed(P/row['source_page']['path'],row['source_page']).decode()
        model=json.loads(fixed(P/row['source_model']['path'],row['source_model']))
        native=load(P/('papers/'+str(row['record_id'])+'/sources/record.response.body'))
        assert model['native_metadata_original']==native['metadata'] and model['native_record_files']==native['files']
        prefix='public/research/'+row['slug']+'/'
        page=candidates[prefix+'index.html'].read_text();tags=Tags();tags.feed(page)
        main_html=one(page,r'<main id="main">[\s\S]*?</main>')
        assert main_html==one(private,r'<main id="main">[\s\S]*?</main>') and pin(main_html.encode())==adoption['whole_MAIN']
        assert page.split('</head>',1)[1]==private.split('</head>',1)[1]
        assert len(tags.ids)==len(set(tags.ids)) and set(tags.labels)<=set(tags.ids)
        assert page.count('<main ')==page.count('<h1>')==1
        canonical='https://aleckriebel.com/research/'+adoption['proposed_slug']+'/'
        assert canonical==row['canonical'] and '<link rel="canonical" href="'+canonical+'">' in page
        assert tags.meta['robots']=='index, follow, max-image-preview:large' and 'editorial-status' not in tags.meta
        assert tags.meta['og:url']==canonical and tags.meta['og:site_name']=='Alec Kriebel'
        assert tags.meta['description']==tags.meta['og:description']==tags.meta['twitter:description']==row['meta_description']
        descriptions.append(tags.meta['description'])
        assert one(page,r'<title>([\s\S]*?)</title>')==row['SEO_title']
        assert tags.meta['citation_title']==tags.meta['og:title']==tags.meta['twitter:title']==native['metadata']['title']
        assert tags.meta['citation_author_orcid']=='https://orcid.org/0009-0001-9320-500X'
        assert tags.meta['citation_doi']==native['doi'] and tags.meta['citation_publication_date']==row['date'].replace('-','/')
        assert tags.meta['article:published_time']==row['date'] and tags.meta['citation_version']==row['version']
        schema=article(page);original_schema=article(private)
        original_schema['@id']=canonical+'#article';original_schema['url']=canonical
        original_schema['mainEntityOfPage']={'@type':'WebPage','@id':canonical}
        for item in original_schema['encoding']:item['contentUrl']=canonical+item['name']
        assert schema==original_schema
        visible=unescape(one(main_html,r'<section id="original-abstract"[\s\S]*?<p>([\s\S]*?)</p>'))
        assert visible==schema['abstract']==tags.meta['DC.description']==model['abstract']==row['full_abstract']
        assert row['rights']==model['rights'] and row['follow_up'] is None
        assert '<link rel="stylesheet" href="/research/research.css">' in page and '<link rel="icon" href="/favicon.ico">' in page
        order=[x['name'] for x in row['native_assets_in_order']]
        assert order==[x['key'] for x in native['files']]
        assert re.findall(r'<a href="([^"]+)" download>',one(main_html,r'<ol id="native-downloads">([\s\S]*?)</ol>'))==order
        for asset,nativefile,encoded in zip(row['native_assets_in_order'],native['files'],schema['encoding']):
            data=fixed(candidates[prefix+asset['name']],asset)
            assert data==(P/row['editorial_folder']/'preview'/asset['name']).read_bytes()
            assert data==(P/('papers/'+str(row['record_id'])+'/sources/assets')/asset['name']).read_bytes()
            assert hashlib.md5(data).hexdigest()==nativefile['checksum'].removeprefix('md5:')
            assert encoded['contentUrl']==canonical+asset['name'] and encoded['sameAs']==nativefile['links']['self']
        pdf=next(x for x in order if x.endswith('.pdf'))
        assert tags.meta['citation_pdf_url']==canonical+pdf and 'src="'+pdf+'#view=FitH"' in main_html
        bib=fixed(candidates[prefix+'citation.bib'],row['BibTeX'])
        assert bib==(P/row['editorial_folder']/'preview/citation.bib').read_bytes()
        if row['record_id']==22929556:assert 'version' not in native['metadata'] and 'Printed version 1.0.1' in main_html and 'supplies no version field' in main_html and 'MIT License' in main_html
        else:assert native['metadata']['version']=='1.0.0' and model['rights']['MIT_not_inferred'] is True and not re.search(r'\bMIT\b',main_html)
        assert model['native_created']==native['created'] and model['native_updated']==native['updated']
        article_results.append({'record_id':row['record_id'],'canonical':canonical,'page':pin(page.encode()),'whole_MAIN':pin(main_html.encode()),'full_abstract_and_metadata_preserved':True})
    assert len(set(descriptions))==2
    oldindex=(W/'public/research/index.html').read_text();index=candidates['public/research/index.html'].read_text()
    oldvisible=re.findall(r'<li(?:\s[^>]*)?>[\s\S]*?</li>',oldindex);visible=re.findall(r'<li(?:\s[^>]*)?>[\s\S]*?</li>',index)
    oldscript=one(oldindex,r'<script type="application/ld\+json">([\s\S]*?)</script>');script=one(index,r'<script type="application/ld\+json">([\s\S]*?)</script>')
    oldtyped=raw_items(oldscript);typed=raw_items(script);collection=json.loads(script)['mainEntity']
    assert len(oldvisible)==len(oldtyped)==109 and len(visible)==len(typed)==collection['numberOfItems']==111
    assert visible[:109]==oldvisible and typed[:109]==oldtyped
    assert pin(''.join(oldvisible).encode())==base['old_visible_item_bytes']
    values=collection['itemListElement'];assert [x['position'] for x in values]==list(range(1,112))
    assert len({x['url'] for x in values})==111
    for row,item,htmlitem in zip(inputs['pages'],values[109:],visible[109:]):
        assert item['name']==row['title'] and item['url']==row['canonical']
        assert 'href="/research/'+row['slug']+'/"' in htmlitem and unescape(row['title']) in unescape(htmlitem)
    oldxml=(W/'public/research/sitemap.xml').read_text();xml=candidates['public/research/sitemap.xml'].read_text()
    oldnodes=re.findall(r'<url>[\s\S]*?</url>',oldxml);nodes=re.findall(r'<url>[\s\S]*?</url>',xml)
    assert len(oldnodes)==110 and len(nodes)==112 and nodes[:110]==oldnodes
    assert pin(''.join(oldnodes).encode())==base['old_sitemap_node_bytes']
    assert [one(x,r'<loc>([\s\S]*?)</loc>') for x in nodes[110:]]==[x['canonical'] for x in inputs['pages']]
    for node in nodes[110:]:assert '<lastmod>'+inputs['build_date']+'</lastmod>' in node
    references=0
    for name,q in candidates.items():
        if not name.endswith('.html'):continue
        tags=Tags();tags.feed(q.read_text());baseurl='https://aleckriebel.com/'+name.removeprefix('public/')
        for _,_,href,_ in tags.links:
            u=urlsplit(urljoin(baseurl,href))
            if u.scheme not in ('http','https') or u.netloc!='aleckriebel.com':continue
            path='public'+unquote(u.path)
            if path.endswith('/'):path+='index.html'
            if path not in projected and path+'/index.html' in projected:path+='/index.html'
            assert path in projected,(name,href)
            if u.fragment and path.endswith('.html'):
                target=Tags();target.feed((candidates[path] if path in candidates else W/path).read_text())
                assert unquote(u.fragment) in target.ids,(name,href)
            references+=1
    current={str(q.relative_to(W)):q for q in (W/'public').rglob('*') if q.is_file()}
    assert set(current)==set(oldfiles) and not any(q.is_symlink() for q in (W/'public').rglob('*'))
    assert sorted(str(q.relative_to(W)) for q in (W/'public').rglob('*') if q.is_dir())==base['public_directories']
    for path,q in current.items():fixed(q,oldfiles[path])
    assert len(base['public_directories'])==354 and len(set(base['public_directories'])|{'public/research/'+x['slug'] for x in inputs['pages']})==356
    raw=git(W,'ls-files','--stage','-z');records=raw.split(b'\0')[:-1]
    assert len(records)==58630 and hashlib.sha256(raw).hexdigest()==base['W']['index']['raw_records_SHA256']
    paths=[x.split(b'\t',1)[1] for x in records]
    target_bytes={x.encode() for x in expected}
    untouched=b''.join(x+b'\0' for x in records if x.split(b'\t',1)[1] not in target_bytes)
    assert len([x for x in paths if x not in target_bytes])==58628
    assert hashlib.sha256(untouched).hexdigest()==base['untargeted_raw_records_SHA256']
    assert {os.fsdecode(x) for x in paths if x in target_bytes}==modified
    tree=git(W,'ls-tree','-r','--full-tree','HEAD','--',*sorted(expected)).split(b'\0')
    treepaths={os.fsdecode(x.split(b'\t',1)[1]):x.split(b'\t',1)[0].split()[2].decode() for x in tree if x}
    assert set(treepaths)==modified
    for path,oid in treepaths.items():
        b=(W/path).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid
        assert candidates[path].read_bytes()!=b
    after={'W':repo_guard(W,base['W']),'Math':repo_guard(M,base['Math'])};assert after==before
    assert final['AA'] is final['follow_up'] is None and final['production_install_Git_deploy_or_tracker_authority'] is False
    print(json.dumps({'status':'PASS_INFORMED_COMBINED_148_149_INTEGRATION_AUDIT','stage_FINAL':pin(final_bytes),'stage_extent':[23,5],'candidate_extent':[11,4],'candidate_pins':final['candidate_pins'],'exact_projected_delta':{'added':sorted(newpaths),'modified':sorted(modified),'counts':'9A2M'},'articles':article_results,'old_visible_HTML_units_exact':109,'old_raw_JSONLD_items_exact':109,'old_XML_nodes_exact':110,'current_counts':[690,109,110],'projected_counts':[699,111,112],'current_native_index_records':58630,'projected_native_index_records':58639,'untargeted_raw_index_records':58628,'untargeted_raw_index_records_SHA256':hashlib.sha256(untouched).hexdigest(),'resolved_local_references':references,'whole_public_namespace_modes_and_bytes_unchanged':True,'W_and_Math_HEAD_tree_shared_indices_before_after':after,'source_guards_unchanged':64,'stage_or_old_helper_native_science_render_browser_network_execution':False,'actual_reader_or_live_download_certification':False,'publication_authority':False},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
