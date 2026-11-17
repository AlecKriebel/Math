"""Fresh installed-state data adapter. No network, Git or project execution."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, urldefrag, unquote
import datetime, difflib, hashlib, json, re, stat

N=Path(__file__).resolve().parent; P=N.parents[1]
S=P/'verification/low-exponent-su5-stage-sol-20261116'
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com'); M=P.parent
ADOPTION=P/'verification/root-low-exponent-su5-stage-adoption-20261116.json'

def pin(p):
    s=p.lstat();assert stat.S_ISREG(s.st_mode),str(p)
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest(),'mode':stat.S_IMODE(s.st_mode)}

def write(name,obj):
    with (N/name).open('x') as f:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')

def typed_spans(script):
    pos=script.index('[',script.index('"itemListElement"'));d=json.JSONDecoder();items,end=d.raw_decode(script,pos);pos+=1;out=[]
    for item in items:
        while script[pos].isspace() or script[pos]==',':pos+=1
        item,end=d.raw_decode(script,pos);out.append(script[pos:end]);pos=end
    return out

class Page(HTMLParser):
    def __init__(self,b):
        super().__init__(convert_charrefs=True);self.tags=[];self.ids=set();self.abstract=[];self.active=False;self.script=None;self.scripts=[];self.feed(b.decode());self.close()
    def handle_starttag(self,t,attrs):
        a=dict(attrs);self.tags.append((t,a))
        if a.get('id'):assert a['id'] not in self.ids;self.ids.add(a['id'])
        if a.get('id')=='original-abstract':self.active=True
        if t=='script' and a.get('type')=='application/ld+json':self.script=[]
    def handle_data(self,d):
        if self.active:self.abstract.append(d)
        if self.script is not None:self.script.append(d)
    def handle_endtag(self,t):
        if t=='p' and self.active:self.active=False
        if t=='script' and self.script is not None:self.scripts.append(json.loads(''.join(self.script)));self.script=None
    def values(self,t,k,v,field):return [a[field] for tag,a in self.tags if tag==t and a.get(k)==v and field in a]

def main():
    assert not (N/'SOURCE_EXPECTATIONS.json').exists()
    final=json.loads((S/'FINAL.json').read_text());plan=json.loads((S/'TARGET_PLAN.json').read_text());adoption=json.loads(ADOPTION.read_text())
    assert pin(S/'FINAL.json')['SHA256']=='aa081369d082b380eabd0722cbc7a5bf3458d123c8f8778dbd2fe43ffbaf74b5'
    assert pin(S/'OWNED_MANIFEST.json')['SHA256']=='0f8f75c60d0ba1ec0780e97db5669f192b6a07055f320a426a039c4df9c81d81'
    assert pin(S/'TARGET_PLAN.json')['SHA256']=='0b9f1bfd79badaf0386748caba2ac195fbb63e2e83717ede89ad1aa3f274253f'
    assert adoption['all15targetpayloads_adopted'] and adoption['install_commit_push_deploy_Sheet_AA_authority'] is False
    guards={label:{n:pin(repo/'.git'/n) for n in ['HEAD','index','config','refs/heads/'+branch]} for label,repo,branch in [('Math',M,'main'),('website',W,'master')]}
    assert (W/'.git/refs/heads/master').read_text().strip()=='b767102567ad89aff909f9f11c0e8b7d72b75c40'
    assert guards['website']['index']['SHA256']=='6e57311ffb524aabe230dec4962ebfa6983085674882606f5b8594aa1d4cee18'
    assert guards['Math']['index']['SHA256']=='91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11'
    native={};record_pins=[]
    for record in ['23331709','23174156']:
        p=P/'papers'/record/'sources/record.response.body';r=json.loads(p.read_text());record_pins.append(pin(p))
        native[record]={x['key']:(P/'papers'/record/'sources/assets'/x['key'],x['checksum']) for x in r['files']}
    rows=[];article_semantics=[];page_bytes={}
    for x in plan['targets']:
        target=x['target'];p=S/'public'/target;a=pin(p);website=pin(W/'public'/target)
        assert (a['bytes'],a['SHA256'],a['mode'])==(x['after']['bytes'],x['after']['sha256'],int(x['after']['mode'],8))
        assert {k:a[k] for k in ['bytes','SHA256','mode']}=={k:website[k] for k in ['bytes','SHA256','mode']}
        record='23331709' if '/low-exponent-supersolvability/' in '/'+target else '23174156' if '/su5-lens-space-counterexample/' in '/'+target else None
        ext=p.suffix.lower();category='article' if p.name=='index.html' and record else 'aggregate' if record is None else 'Bib' if p.name=='citation.bib' else 'native asset'
        url='https://aleckriebel.com/'+target
        if target.endswith('/index.html'):url=url[:-len('index.html')]
        types={'.html':['text/html'],'.pdf':['application/pdf'],'.zip':['application/zip','application/x-zip-compressed'],'.xml':['application/xml','text/xml'],'.bib':['application/x-bibtex','text/x-bibtex','text/plain','application/octet-stream'],'.tex':['application/x-tex','text/x-tex','text/plain','application/octet-stream'],'.md':['text/markdown','text/plain','application/octet-stream'],'.txt':['text/plain']}[ext]
        row={'ordinal':len(rows)+1,'url':url,'website_relative_path':target,'record':record,'category':category,
            'kind':{'.html':'html','.pdf':'pdf','.zip':'zip','.xml':'xml'}.get(ext,'text'),'accepted_content_types':types,'source':a,'website':website,'native_source':None}
        if category=='native asset':
            np,md5=native[record][p.name];n=pin(np)
            assert {k:a[k] for k in ['bytes','SHA256']}=={k:n[k] for k in ['bytes','SHA256']}
            assert 'md5:'+hashlib.md5(np.read_bytes()).hexdigest()==md5;row['native_source']=n;row['native_MD5']=md5
        if ext=='.html':
            page_bytes[url]=p.read_bytes();page=Page(page_bytes[url]);assert page.values('link','rel','canonical','href')==[url]
            if category=='article':
                entity=next(j for j in page.scripts if j.get('@type')=='ScholarlyArticle')
                assert ''.join(page.abstract)==page.values('meta','name','DC.description','content')[0]==entity['abstract']
                article_semantics.append({'url':url,'record':record,'abstract':entity['abstract'],'schema':entity,'citation_PDF_URL':page.values('meta','name','citation_pdf_url','content')[0]})
        rows.append(row)
    css=pin(W/'public/research/research.css');assert css['bytes']==1170 and css['SHA256']=='f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a'
    rows.append({'ordinal':16,'url':'https://aleckriebel.com/research/research.css','website_relative_path':'research/research.css','record':None,'category':'existing CSS','kind':'css','accepted_content_types':['text/css'],'source':css,'website':css,'native_source':None})
    assert len(rows)==len({r['url'] for r in rows})==16 and sum(r['category']=='native asset' for r in rows)==9
    index=page_bytes['https://aleckriebel.com/research/'].decode();script=re.search(r'<script type="application/ld\+json">(.*?)</script>',index,re.S)[1]
    visible=re.findall(r'<li\b[^>]*>[\s\S]*?</li>',index);typed=typed_spans(script)
    nodes=re.findall(r'<url>[\s\S]*?</url>',(S/'public/research/sitemap.xml').read_text())
    assert len(visible)==len(typed)==123 and len(nodes)==124
    assert final['aggregate_proof']['old_visible_prefix_units']==121 and final['aggregate_proof']['old_XML_prefix_nodes']==122
    paths={r['url'] for r in rows};local={}
    for url,b in page_bytes.items():
        for tag,a in Page(b).tags:
            for attr in ['href','src','data']:
                if not a.get(attr):continue
                base,fragment=urldefrag(urljoin(url,a[attr]));u=urlsplit(base)
                if u.scheme!='https' or u.netloc!='aleckriebel.com' or base in paths:continue
                assert not u.query
                name=unquote(u.path).lstrip('/');name=name+'index.html' if not name or name.endswith('/') else name
                p=W/'public'/name;local[name]=pin(p)
                if fragment:assert name.endswith('.html') and unquote(fragment) in Page(p.read_bytes()).ids
    e={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'schema':'fixed16-installed-http-expectations-v1','rows':rows,
        'article_semantics':article_semantics,'adopted_old_prefixes':{'visible':visible[:121],'typed':typed[:121],'XML_nodes':nodes[:122]},
        'linked_existing_source_files':local,'repository_guards':guards,'native_record_pins':record_pins,
        'stage_FINAL':pin(S/'FINAL.json'),'stage_manifest':pin(S/'OWNED_MANIFEST.json'),'target_plan':pin(S/'TARGET_PLAN.json'),'root_stage_adoption':pin(ADOPTION),
        'installed_website_commit':'b767102567ad89aff909f9f11c0e8b7d72b75c40','index_items':123,'sitemap_nodes':124,
        'historical_preinstall_state_only':{'public_files':747,'public_child_dirs':366,'website_commit':'3a6e0709bda08d8c913078b4eaa4e591fed7f3c6','index_SHA256':'71ea221a2bcd9f3919f430d785bbcb940ef2348d9596932778568940fc59d14c'},
        'current_transition_root_confirmed':{'public_files':760,'public_child_dirs':368,'current_census_by_HTTP_lane':False},
        'whole760_preservation_audit':'Separate root release audit; no global old filesystem guard imposed by HTTP lane.',
        'PDF_text_evidence':'Whole-byte native PDF equality preserves already reviewed searchable originals; no new extraction/science/browser certification.'}
    write('SOURCE_EXPECTATIONS.json',e)
    write('PREPARATION_HISTORY.json',{'failed_offline_exit_history':[1,1],'new_installed_data_continuation_expected_exit':0,
        'failures':['Explicit terminal-control rows lack bytes/hash; stopped before W reads or output.','Authorized concurrent install/publication made old747/366 guard obsolete; stopped before output.'],
        'failed_utilities':[pin(N/'prepare_expected.v1.failed.py'),pin(N/'prepare_expected.v2.failed.py')],
        'literal_failed_streams':[pin(N/n) for n in ['preparation.stdout','preparation.stderr','preparation.exit','preparation.corrected.stdout','preparation.corrected.stderr','preparation.corrected.exit']],
        'terminal_adapter_exact_diff':''.join(difflib.unified_diff((N/'prepare_expected.v1.failed.py').read_text().splitlines(True),(N/'prepare_expected.v2.failed.py').read_text().splitlines(True),fromfile='v1',tofile='v2')),
        'root_explicit_fresh_current_installed_data_preparation_GO':True,'no_failed_GETs_or_live_helper_execution':True})
    print(json.dumps({'status':'CURRENT_INSTALLED_EXPECTATIONS_READY_NO_NETWORK','URLs':16,'expectations':pin(N/'SOURCE_EXPECTATIONS.json'),'linked_source_files':len(local)}))

if __name__=='__main__':main()
