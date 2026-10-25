"""Independent, read-only semantic inspection of the sealed two-record overlay.

No renderer/checker campaigns, network, writes, or author parser are invoked.
The optional control function operates only on supplied in-memory HTML strings.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit
from html import unescape
import hashlib, json, re

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
STAGE = P/'verification/local-odd-ear-blocking-stage-sol-20261025'
SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
IDS = ('23576280','23331258')
PIN = {'manifest':'8c1f17bfc3b512a73db5d385cf9c5fa90c9ce9c01a01d3123e8de5f07b67abed',
       'seal':'78ca047a311b84161286d4e42d6e5e769a57b73b8557063c7392a99ff79106ba'}

def need(ok, name):
    if not ok: raise ValueError(name)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s): return ' '.join(s.split())
def literal(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return list(a)==list(b) and all(literal(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(literal(x,y) for x,y in zip(a,b))
    return a==b

class Node:
    def __init__(self, tag='', attrs=(), parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs), parent, []
    def walk(self):
        yield self
        for c in self.children:
            if isinstance(c, Node): yield from c.walk()
    def hidden(self):
        a=self.attrs;style=re.sub(r'\s+','',a.get('style','')).lower()
        return self.tag in ('script','style','template') or 'hidden' in a or a.get('aria-hidden')=='true' or 'display:none' in style or 'visibility:hidden' in style
    def text(self):
        if self.hidden(): return ''
        return norm(' '.join(c.text() if isinstance(c,Node) else c for c in self.children))
    def rawtext(self):
        return ''.join(c.rawtext() if isinstance(c,Node) else c for c in self.children)

class Tree(HTMLParser):
    VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self, text):
        super().__init__(convert_charrefs=True);self.root=Node();self.stack=[self.root];self.feed(text)
    def handle_starttag(self,t,a):
        n=Node(t,a,self.stack[-1]);self.stack[-1].children.append(n)
        if t not in self.VOID:self.stack.append(n)
    def handle_startendtag(self,t,a):
        self.handle_starttag(t,a)
        if t not in self.VOID:self.handle_endtag(t)
    def handle_endtag(self,t):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==t:self.stack=self.stack[:i];break
    def handle_data(self,s):self.stack[-1].children.append(s)
    def nodes(self,t=None):return [n for n in self.root.walk() if t is None or n.tag==t]

def inspect_html(rid, html):
    c=json.loads((P/'papers'/rid/'publication.json').read_text())
    approved=json.loads((P/'papers'/rid/'reviews/editorial/public-prose.json').read_text())
    raw=json.loads((P/'papers'/rid/'sources/record.raw.json').read_text())
    t=Tree(html);base='https://aleckriebel.com/research/'+c['slug']+'/'
    bodies=t.nodes('body');need(len(bodies)==1,'one_body');body=bodies[0]
    need(not any(n.hidden() for n in body.walk()),'body_has_no_hidden_content')
    sections={n.attrs.get('id'):n for n in t.nodes('section')}
    need(len(sections)==len(t.nodes('section')),'unique_sections')
    h1=t.nodes('h1');need(len(h1)==1 and h1[0].text()==approved['title'],'actual_h1')
    links=[n for n in h1[0].walk() if n.tag=='a']
    need(len(links)==1 and urljoin(base,links[0].attrs.get('href',''))==base,'title_resolves_to_own_article')
    nav=[n for n in t.nodes('nav') if n.attrs.get('aria-label')=='Main navigation'];need(len(nav)==1,'one_main_nav')
    research=[n for n in nav[0].walk() if n.tag=='a' and n.text()=='Research']
    need(len(research)==1 and urljoin(base,research[0].attrs.get('href',''))=='https://aleckriebel.com/research/','Research_resolves_to_index')
    need(urljoin(base,research[0].attrs['href'])!=urljoin(base,links[0].attrs['href']),'title_and_Research_destinations_differ')
    for sec,key in [('abstract','abstract'),('plain-language','plain_language'),('result','result'),('proof','why_it_works'),('limits','limitations')]:
        want=approved[key] if isinstance(approved[key],list) else [approved[key]]
        got=[n.text() for n in sections[sec].children if isinstance(n,Node) and n.tag=='p']
        need(got==[norm(x) for x in want],'complete_ordered_'+sec)
    status=[n.text() for n in sections['status'].children if isinstance(n,Node) and n.tag=='p']
    need(status==[norm(approved[k]) for k in ['status','ai_disclosure','edition_note']],'complete_status_qualifications')
    need(approved['collaboration'] in sections['collaborate'].text(),'complete_collaboration')
    background=[n for n in sections['background'].walk() if n.tag=='li']
    need(len(background)==len(approved['background']),'all_background_items')
    for n,x in zip(background,approved['background']):
        aa=[a for a in n.walk() if a.tag=='a'];need(len(aa)==1 and aa[0].text()==x['title'] and aa[0].attrs['href']==x['url'] and norm(x['note']) in n.text(),'exact_background_credit_and_destination')
    note=sections['materials'].text()
    if rid=='23576280':need('Authored prose is CC BY 4.0; authored code is MIT.' in note,'odd_ear_split_licence')
    else:need('Authored manuscript, proofs, code and audits in the deposit are licensed CC BY 4.0' in note and 'MIT' not in note,'blocking_code_CC_BY')
    canonical=[n.attrs.get('href') for n in t.nodes('link') if n.attrs.get('rel')=='canonical'];need(canonical==[base],'canonical_identity')
    schema=[json.loads(n.rawtext()) for n in t.nodes('script') if n.attrs.get('type')=='application/ld+json'];need(len(schema)==1,'one_schema')
    article=[n for n in schema[0]['@graph'] if n['@type']=='ScholarlyArticle'];need(len(article)==1,'one_article_schema');a=article[0]
    need(a['version']==raw['metadata']['version']==c['version'] and a['name']==raw['metadata']['title']==c['title'] and a['datePublished']==raw['metadata']['publication_date']==c['publication_date'],'native_version_title_declared_date')
    need(a['encoding']['contentUrl']==base+c['pdf_filename'] and a['license']=='https://creativecommons.org/licenses/by/4.0/','schema_reader_prose_licence')
    frames=t.nodes('iframe');need(len(frames)==1 and urljoin(base,frames[0].attrs['src'])==base+c['pdf_filename']+'#view=FitH','complete_embedded_reader_identity')
    anchors=t.nodes('a')
    def anchor(label,url,download):
        aa=[x for x in anchors if x.text()==label];need(len(aa)==1 and urljoin(base,aa[0].attrs.get('href',''))==url and ('download' in aa[0].attrs)==download,'anchor_'+label)
    anchor('Download PDF',base+c['pdf_filename'],True)
    anchor('Open PDF in a full window',base+c['pdf_filename'],False)
    originals={f['key']:f['links']['self'] for f in raw['files']}
    anchor('Download the original from Zenodo',originals[c['pdf_filename']],True)
    anchor('Zenodo original complete ZIP',originals[c['supplement_filename']],False)
    aa=[x for x in anchors if x.text()==c['supplement_label']];need(len(aa)==2 and all(urljoin(base,x.attrs['href'])==base+c['supplement_filename'] and 'download' in x.attrs for x in aa),'both_complete_ZIP_downloads')
    need([f['key'] for f in raw['files']]==({'23576280':[c['supplement_filename'],c['pdf_filename']],'23331258':[c['pdf_filename'],c['supplement_filename']]}[rid]),'native_file_order')
    return {'record_id':rid,'canonical':base,'title_destination':urljoin(base,links[0].attrs['href']),'Research_destination':urljoin(base,research[0].attrs['href']),'complete_approved_paragraphs':sum(len(approved[k]) for k in ['plain_language','result','why_it_works','limitations'])+4,'background_items':len(background),'anchors':len(anchors),'native_file_order':[f['key'] for f in raw['files']]}

def verify():
    need(sha(STAGE/'MANIFEST.json')==PIN['manifest'] and sha(STAGE/'SEAL.json')==PIN['seal'],'sealed_stage_envelope')
    manifest=json.loads((STAGE/'MANIFEST.json').read_text());need(len(manifest['files'])==759,'759_payloads')
    for x in manifest['files']:
        p=STAGE/x['relative_path'];need(p.is_file() and not p.is_symlink() and p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'stage_payload:'+x['relative_path'])
    got={str(p.relative_to(STAGE)) for p in STAGE.rglob('*') if p.is_file()};need(got=={x['relative_path'] for x in manifest['files']}|{'MANIFEST.json','SEAL.json'},'exact_stage_file_set')
    baseline=json.loads((STAGE/'BASELINE.json').read_text());need(len(baseline['public_file_set'])==516,'current_public516')
    need(sorted(str(p.relative_to(SITE)) for p in SITE.rglob('*') if p.is_file())==baseline['public_file_set'],'unchanged_public_file_set')
    protected=0
    for x in baseline['files']:
        p=Path(x['path'])
        if p.is_relative_to(SITE) or p.parent==P/'scripts' or any(p.is_relative_to(P/'papers'/rid/'sources') for rid in IDS):
            need(p.is_file() and p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'actual_protected:'+str(p));protected+=1
    rows=[]
    for rid in IDS:
        c=json.loads((P/'papers'/rid/'publication.json').read_text());d=STAGE/'public/research'/c['slug'];h=(d/'index.html').read_text();rows.append(inspect_html(rid,h))
        paper=P/'papers'/rid;g=json.loads((paper/'promotion.json').read_text());b=c['source_binding']
        science=json.loads((P/('verification/root-clearance-'+rid+'-20261025.json')).read_text())
        need(literal(g['root_clearance_record'],science) and g['approved_scope']==science['approved_scope'],'whole_original_root_qualifications')
        need(literal(b['source_receipt_original'],json.loads((paper/b['source_receipt_path']).read_text())) and literal(b['metadata_original'],json.loads((paper/b['metadata_path']).read_text())),'whole_native_source_objects_types_and_key_order')
        need(literal(g['source_receipt_original'],b['source_receipt_original']) and literal(g['all_assets'],b['all_assets']),'whole_native_gate_objects')
        for role,x in g['reviews'].items():
            need(literal(x['root_authority_entry'],science['reviews'][role]),'whole_root_'+role+'_entry')
            original=json.loads((paper/x['verdict_file']).read_text())
            need(literal(x['verdict'],original) and sha(paper/x['verdict_file'])==x['verdict_sha256']==science['reviews'][role]['verdict_sha256'],'whole_custom_'+role+'_verdict')
        need(all(g[k] is False and c['review_metadata'][k] is False for k in ['rendered_public_copy_approved','local_http_verified','live_http_verified','browser_verified','native_sheet_publication_verified','public_page_published']) and all(g[k] is None and c[k] is None for k in ['canonical_url','AA','follow_up']),'private_false_null_gates_preserved')
        need({p.name for p in d.iterdir()}=={'index.html','citation.bib',c['pdf_filename'],c['supplement_filename']},'exact_four_article_files')
        for key in ['pdf_filename','supplement_filename']:need((d/c[key]).read_bytes()==(P/'papers'/rid/'sources'/c[key]).read_bytes(),'whole_unchanged_'+key)
        need((d/'citation.bib').read_text()==c['prepared_bibtex'],'whole_BibTeX')
    ix=Tree((STAGE/'public/research/index.html').read_text());old=Tree((SITE/'research/index.html').read_text())
    ixdata=json.loads([n.rawtext() for n in ix.nodes('script') if n.attrs.get('type')=='application/ld+json'][0]);olddata=json.loads([n.rawtext() for n in old.nodes('script') if n.attrs.get('type')=='application/ld+json'][0])
    items=ixdata['mainEntity']['itemListElement'];olditems=olddata['mainEntity']['itemListElement'];need(len(olditems)==68 and len(items)==70 and items[:68]==olditems,'existing_index_order_and_two_new')
    need(ixdata['mainEntity']['numberOfItems']==70 and [x['url'] for x in items[-2:]]==[x['canonical'] for x in rows],'index_counts_and_actual_new_destinations')
    oldvisible=re.findall(r'<li>.*?</li>',(SITE/'research/index.html').read_text(),re.S);newvisible=re.findall(r'<li>.*?</li>',(STAGE/'public/research/index.html').read_text(),re.S)
    need(len(oldvisible)==68 and len(newvisible)==70 and newvisible[:68]==oldvisible,'old_visible_index_entries_byteidentical')
    for fragment,row in zip(newvisible[-2:],rows):
        anchors=Tree(fragment).nodes('a');need(urljoin('https://aleckriebel.com/research/',anchors[0].attrs['href'])==row['canonical'],'new_visible_index_destination')
        target=STAGE/'public'/urlsplit(row['canonical']).path.lstrip('/')/'index.html';need(target.is_file(),'new_index_destination_exists')
    oldurls=re.findall(r'<loc>(.*?)</loc>',(SITE/'research/sitemap.xml').read_text());newurls=re.findall(r'<loc>(.*?)</loc>',(STAGE/'public/research/sitemap.xml').read_text());need(len(oldurls)==69 and len(newurls)==71 and newurls[:69]==oldurls and newurls[-2:]==[x['canonical'] for x in rows],'sitemap_counts_and_order')
    overlay={str(p.relative_to(STAGE/'public')) for p in (STAGE/'public').rglob('*') if p.is_file()};need(len(overlay)==10,'overlay_ten_files');need(len(set(baseline['public_file_set'])|overlay)==524,'integrated_524_prediction')
    import difflib
    for kind,base,proposal in [('renderer','render_page.py','render_page.proposed.py'),('checker','final-content-check.py','final-content-check.proposed.py')]:
        a=(STAGE/'inputs'/base).read_text().splitlines(keepends=True);b=(STAGE/proposal).read_text().splitlines(keepends=True)
        need(''.join(difflib.unified_diff(a,b,fromfile='current',tofile='proposed'))==(STAGE/('shared-'+kind+'.diff')).read_text(),'complete_'+kind+'_diff')
        current=P/('scripts' if kind=='renderer' else 'verification')/base
        need((STAGE/'inputs'/base).read_bytes()==current.read_bytes(),'current_'+kind+'_base_unchanged')
        private=STAGE/('render_page.stage.py' if kind=='renderer' else 'final-content-check.stage.py')
        need(''.join(difflib.unified_diff((STAGE/proposal).read_text().splitlines(keepends=True),private.read_text().splitlines(keepends=True),fromfile='proposed',tofile='private-execution'))==(STAGE/(kind+'-private-overrides.diff')).read_text(),'exact_'+kind+'_private_overrides')
    own=Path(__file__).resolve().parent;own_count=None
    if (own/'SEAL.json').exists():
        seal=json.loads((own/'SEAL.json').read_text());need(sha(own/'MANIFEST.json')==seal['manifest']['sha256'],'own_manifest_seal')
        m=json.loads((own/'MANIFEST.json').read_text());own_count=len(m['files'])
        for x in m['files']:
            q=own/x['relative_path'];need(q.is_file() and q.stat().st_size==x['bytes'] and sha(q)==x['sha256'],'own_payload:'+x['relative_path'])
        need({str(q.relative_to(own)) for q in own.rglob('*') if q.is_file()}=={x['relative_path'] for x in m['files']}|{'MANIFEST.json','SEAL.json'},'exact_own_packet_file_set')
    return {'status':'VERIFIED_PRIVATE_TWO_RECORD_SCOPE','payload_bindings':759,'protected_selected_bindings':protected,'records':rows,'overlay_files':10,'predicted_public_files':524,'index_items':70,'sitemap_urls':71,'own_sealed_payload_bindings':own_count,'campaigns_replayed':False,'publication_authority':False}

if __name__=='__main__':print(json.dumps(verify(),indent=2,ensure_ascii=False))
