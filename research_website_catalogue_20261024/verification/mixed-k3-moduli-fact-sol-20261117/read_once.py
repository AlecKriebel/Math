"""One passive K3 private fact/custody read, after root's checkpoint release."""
import datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import stat
import traceback

HERE=Path(__file__).resolve().parent;P=HERE.parents[1]
S=P/'papers/23204176/sources';W=P/'verification/mixed-k3-moduli-editorial-sol-20261117'
ORIGINAL=S/'archives/01-source-and-verification.zip.extracted/main.tex'
REVIEW=P/'papers/23204176/reviews/root-continuation-20261117/ROOT_REVIEW.md'
CLEAR=P/'verification/root-clearance-23204176-20261117.json'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def enc(x):return (json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode()
def put(n,x):
    with (HERE/n).open('xb') as f:f.write(enc(x))
def pin(p):
    b=p.read_bytes();return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest(),'MD5':hashlib.md5(b).hexdigest(),'mode':oct(stat.S_IMODE(p.lstat().st_mode))}
def snap(root):
    rows=[]
    for p in [root,*sorted(root.rglob('*'))]:
        st=p.lstat();name='.' if p==root else p.relative_to(root).as_posix();directory=stat.S_ISDIR(st.st_mode)
        assert directory or stat.S_ISREG(st.st_mode),(root,name)
        r={'path':name,'kind':'directory' if directory else 'file','mode':oct(stat.S_IMODE(st.st_mode)),
           'hidden':any(t.startswith('.') and t not in ('.','..') for t in Path(name).parts)}
        if directory:r['empty']=not any(p.iterdir())
        else:r.update(pin(p));r['empty']=r['bytes']==0
        rows.append(r)
    return {'root':str(root),'files':sum(r['kind']=='file' for r in rows),'childdirs':sum(r['kind']=='directory' for r in rows)-1,'entries':rows}
class HTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.meta=[];self.links=[];self.iframes=[];self.scripts=[];self.styles=[]
        self.body=False;self.active_script=None;self.script_text=[];self.instyle=False;self.text=[]
    def handle_starttag(self,t,a):
        a=dict(a)
        if t=='meta':self.meta.append(a)
        if t in ('a','link','base'):self.links.append({'tag':t,**a})
        if t=='iframe':self.iframes.append(a)
        if t=='body':self.body=True
        if t=='style':self.instyle=True;self.styles.append(a)
        if t=='script':self.active_script=a;self.script_text=[]
    def handle_endtag(self,t):
        if t=='script' and self.active_script is not None:self.scripts.append({'attrs':self.active_script,'text':''.join(self.script_text)});self.active_script=None
        if t=='style':self.instyle=False
        if t=='body':self.body=False
    def handle_data(self,x):
        if self.active_script is not None:self.script_text.append(x)
        elif self.body and not self.instyle:self.text.append(x)
try:
    assert not (HERE/'BEFORE.json').exists(),'single audit attempt'
    before={'UTC':now(),'SOURCE':snap(S),'WRITER':snap(W)};put('BEFORE.json',before)
    assert (before['SOURCE']['files'],before['SOURCE']['childdirs'])==(43,7)
    assert (before['WRITER']['files'],before['WRITER']['childdirs'])==(28,1)
    protected={W/'FINAL.json':'245fcc03a3105d4a3a093821bd79e995d13225246a5e0f96b7a6c3e322a814b8',
      W/'MANIFEST.json':'1aa3d7271c59f80db746b41005b605d2e68ec448cdf3125b3b282ae7e6acb171',
      W/'article.html':'fa80a828093717d9648e8a806aed891f0e52e9c517c17f7200624e67915c37e5',
      REVIEW:'726d07488144fb2a7e4cbc0351c235a4a422a42346e71410000833596c2f6b94',
      CLEAR:'ea5472784dffe99ee849d40700541b9453466b2f3edf064a3a02fe091e7f55cd',
      S/'SOURCE_MANIFEST.json':'53be96c6f47deccccc173286d10bdf46b50df4f237c985f42f2da8a69d8c8ffb',
      S/'SOURCE_FINAL.json':'f7bc05f4e7d56f0fbad45d77bdb4992d9fd92de8d976bdc5ff3b446f7dbfe9c8'}
    pins=[]
    for p,h in protected.items():
        r=pin(p);assert r['SHA256']==h,('protected pin',str(p));pins.append({'path':str(p),**r})
    assert pin(REVIEW)['bytes']==20893 and pin(W/'article.html')['bytes']==19913
    manifest=json.loads((W/'MANIFEST.json').read_text());names=set()
    for row in manifest['payload_files']:
        actual=pin(W/row['path']);assert actual=={k:row[k] for k in actual};names.add(row['path'])
    assert names|{'FINAL.json','MANIFEST.json'}=={r['path'] for r in before['WRITER']['entries'] if r['kind']=='file'}
    for n in ['head.html','main.html','page-model.json','citation.bib','ABSTRACT.txt','ABSTRACT_SOURCE.json','REPORT.md']:
        pins.append({'path':str(W/n),**pin(W/n)})
    put('INPUT_PINS.json',pins)
    article=(W/'article.html').read_text();reader=HTML();reader.feed(article);reader.close()
    model=json.loads((W/'page-model.json').read_text());api=json.loads((S/'native-metadata/record-api.json').read_text())
    clearance=json.loads(CLEAR.read_text());abstract_source=json.loads((W/'ABSTRACT_SOURCE.json').read_text())
    tex=ORIGINAL.read_text();literal=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1)
    accent='B'+chr(92)+'"ulles';rendered=' '.join(literal.split()).replace(accent,'Bülles')
    assert abstract_source['declared_rendering_replacements']=={accent:'Bülles'}
    visible=' '.join(''.join(reader.text).split());schema=[json.loads(x['text']) for x in reader.scripts if x['attrs'].get('type')=='application/ld+json']
    checks={'literal_original':abstract_source['literal_original_abstract']==literal,
        'visible_complete_once':visible.count(rendered)==1,'ABSTRACT_txt':(W/'ABSTRACT.txt').read_text().strip()==rendered,
        'model':model['abstract']==rendered,'DC':any(m.get('name')=='DC.description' and m.get('content')==rendered for m in reader.meta),
        'single_ScholarlyArticle':len(schema)==1 and schema[0].get('@type')=='ScholarlyArticle' and schema[0].get('abstract')==rendered}
    assert all(checks.values()),checks
    assert re.search(r'<head\b[^>]*>.*?</head>',article,re.S).group(0).strip()==(W/'head.html').read_text().strip()
    assert re.search(r'<main\b[^>]*>.*?</main>',article,re.S).group(0).strip()==(W/'main.html').read_text().strip()
    assert 'version' not in api['metadata'] and model['native_version'] is None and model['native_API_version_field_present'] is False
    assert 'version' not in schema[0] and not any(m.get('name')=='citation_version' for m in reader.meta)
    assert api['metadata']['license']['id']=='cc-by-4.0' and api['metadata']['publication_date']=='2026-10-06'
    assert len(api['files'])==len(model['native_asset_order'])==len(schema[0]['encoding'])==2
    assets=[]
    for native,prepared,encoding in zip(api['files'],model['native_asset_order'],schema[0]['encoding']):
        original=S/'zenodo-files'/native['key'];copy=W/prepared['local_path'];a,b=pin(original),pin(copy)
        assert a==b and 'md5:'+a['MD5']==native['checksum'] and native['key']==prepared['name']==encoding['name']
        assert encoding['contentUrl']==prepared['local_path'] and encoding['sameAs']==native['links']['self']
        assets.append({'name':native['key'],'native_original':str(original),'prepared':str(copy),'pin':a})
    assert [a['name'] for a in assets]==['paper.pdf','source-and-verification.zip']
    nulls={k:model.get(k) for k in ['canonical_url','base_url','production_url','actual_publication_date','AA','follow_up']}
    assert all(v is None for v in nulls.values()) and model['publication_authority'] is False
    assert not any(a['tag']=='base' or a.get('rel')=='canonical' for a in reader.links)
    assert all(any(m.get('name')==n and m.get('content')=='noindex, nofollow' for m in reader.meta) for n in ['robots','googlebot'])
    assert clearance['status']=='PASS_BOUNDED_SUBSTANTIVE_REVIEW' and clearance['reviewer_reservation']
    put('FACTS.json',{'UTC':now(),'protected_pins_and_whole_writer_payloads_match':True,'abstract_checks':checks,
        'complete_abstract':rendered,'head_main_exact':True,'native_API_version_absent':True,'no_invented_version':True,
        'native_metadata':api['metadata'],'native_created':api['created'],'native_updated':api['updated'],
        'assets_in_native_order':assets,'article_metas':reader.meta,'article_links':reader.links,'article_iframes':reader.iframes,
        'schemas':schema,'inline_style_elements':reader.styles,'private_nulls':nulls,'publication_authority':False,
        'root_scientific_status':clearance['status'],'root_reviewer_reservation':clearance['reviewer_reservation'],
        'root_formal_geometric_certificate':clearance['formal_geometric_certificate'],'root_human_peer_review':clearance['human_peer_review'],
        'W_access_or_guard':False,'scientific_program_runs':0,'producer_runs':0,'source_imports':0,'network':0,'Git':0,'Sheet':0})
    after={'UTC':now(),'SOURCE':snap(S),'WRITER':snap(W)};put('AFTER.json',after)
    assert before['SOURCE']==after['SOURCE'] and before['WRITER']==after['WRITER']
    put('READER_RECEIPT.json',{'UTC':after['UTC'],'reader':pin(Path(__file__)),
        'complete_saved_reader_read_before_execution':True,'attempts':1,'explicit_root_checkpoint_release':'15482acd0ef864af280a864758b2ac6aa24dfbe8',
        'source43_7_and_writer28_1_full_exact':True,'W_access_or_whole_W_guard':False,
        'new_scientific_or_producer_runs':0,'source_import_AST_compile_tests':0,'network_Git_Sheet':0})
    print(json.dumps({'passive_audit_complete':True,'source':[43,7],'writer':[28,1],'full_before_after_exact':True,
        'abstract_all_exact':True,'API_version_absent':True,'native_assets_exact_PDF_ZIP':True,'W_access':False}))
except Exception:
    with (HERE/'LITERAL_FAILURE.txt').open('x') as f:f.write(now()+'\n'+traceback.format_exc())
    raise
