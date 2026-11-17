"""One offline data-only preparation; never imports a stage/production helper."""
from pathlib import Path
from html.parser import HTMLParser
import datetime, hashlib, json, os, re, stat, struct

N=Path(__file__).resolve().parent
P=N.parents[1]
S=P/'verification/low-exponent-su5-stage-sol-20261116'
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
M=P.parent
ADOPTION=P/'verification/root-low-exponent-su5-stage-adoption-20261116.json'

def pin(p):
    s=p.lstat(); assert stat.S_ISREG(s.st_mode),str(p)
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest(),'mode':stat.S_IMODE(s.st_mode)}

def census(root):
    files={}; dirs={}
    for base,names,leaves in os.walk(root,followlinks=False):
        for name in names:
            p=Path(base)/name; assert not p.is_symlink()
            dirs[p.relative_to(root).as_posix()]=stat.S_IMODE(p.stat().st_mode)
        for name in leaves:
            p=Path(base)/name; files[p.relative_to(root).as_posix()]={k:v for k,v in pin(p).items() if k!='path'}
    return {'root':str(root),'root_mode':stat.S_IMODE(root.stat().st_mode),'files':dict(sorted(files.items())),'directories':dict(sorted(dirs.items()))}

def write(name,obj):
    with (N/name).open('x') as f: json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')

def typed_spans(script):
    pos=script.index('[',script.index('"itemListElement"')); d=json.JSONDecoder(); items,end=d.raw_decode(script,pos); pos+=1; out=[]
    for item in items:
        while script[pos].isspace() or script[pos]==',': pos+=1
        item,end=d.raw_decode(script,pos);out.append(script[pos:end]);pos=end
    return out

class Page(HTMLParser):
    def __init__(self,b):
        super().__init__(convert_charrefs=True);self.meta={};self.canonical=[];self.abstract=[];self.active=False;self.script=None;self.scripts=[];self.feed(b.decode());self.close()
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if t=='meta': self.meta[a.get('name',a.get('property'))]=a.get('content')
        if t=='link' and a.get('rel')=='canonical':self.canonical.append(a['href'])
        if a.get('id')=='original-abstract':self.active=True
        if t=='script' and a.get('type')=='application/ld+json':self.script=[]
    def handle_data(self,d):
        if self.active:self.abstract.append(d)
        if self.script is not None:self.script.append(d)
    def handle_endtag(self,t):
        if t=='p' and self.active:self.active=False
        if t=='script' and self.script is not None:self.scripts.append(json.loads(''.join(self.script)));self.script=None

def main():
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    final=json.loads((S/'FINAL.json').read_text()); plan=json.loads((S/'TARGET_PLAN.json').read_text()); adoption=json.loads(ADOPTION.read_text())
    assert pin(S/'FINAL.json')['SHA256']=='aa081369d082b380eabd0722cbc7a5bf3458d123c8f8778dbd2fe43ffbaf74b5'
    assert pin(S/'OWNED_MANIFEST.json')['SHA256']=='0f8f75c60d0ba1ec0780e97db5669f192b6a07055f320a426a039c4df9c81d81'
    assert pin(S/'TARGET_PLAN.json')['SHA256']=='0b9f1bfd79badaf0386748caba2ac195fbb63e2e83717ede89ad1aa3f274253f'
    assert adoption['all15targetpayloads_adopted'] and adoption['install_commit_push_deploy_Sheet_AA_authority'] is False
    stage=census(S); assert len(stage['files'])==34 and len(stage['directories'])==4
    manifest=json.loads((S/'OWNED_MANIFEST.json').read_text())
    for x in manifest['files']:
        if x.get('terminal_control'):
            assert x['path'] in ['FINAL.json','OWNED_MANIFEST.json']
            assert stage['files'][x['path']]['mode']==int(x['mode'],8)
            continue  # Both exact terminal hashes were checked above.
        a=stage['files'][x['path']];assert (a['bytes'],a['SHA256'],a['mode'])==(x['bytes'],x['sha256'],int(x['mode'],8))
    baseline=census(W/'public'); assert len(baseline['files'])==747 and len(baseline['directories'])==366
    old=json.loads((S/'GUARDS_BEFORE.json').read_text())['public']
    assert all((baseline['files'][x['path']]['bytes'],baseline['files'][x['path']]['SHA256'],baseline['files'][x['path']]['mode'])==(x['bytes'],x['sha256'],int(x['mode'],8)) for x in old['files'])
    guards={}
    for label,repo,branch in [('Math',M,'main'),('website',W,'master')]:
        guards[label]={n:pin(repo/'.git'/n) for n in ['HEAD','index','config','refs/heads/'+branch]}
        b=(repo/'.git/index').read_bytes(); assert b[:4]==b'DIRC';guards[label]['index_version_records']=list(struct.unpack('>II',b[4:12]))
    assert guards['website']['index']['SHA256']=='71ea221a2bcd9f3919f430d785bbcb940ef2348d9596932778568940fc59d14c'
    assert guards['website']['index_version_records']==[2,58687]
    assert guards['Math']['index']['SHA256']=='91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11'
    baseline['raw_repository_guards']=guards
    raw=(W/'public/research/index.html').read_text();script=re.search(r'<script type="application/ld\+json">(.*?)</script>',raw,re.S)[1]
    baseline['old_visible_items']=re.findall(r'<li\b[^>]*>[\s\S]*?</li>',raw)
    baseline['old_typed_spans']=typed_spans(script)
    baseline['old_sitemap_nodes']=re.findall(r'<url>[\s\S]*?</url>',(W/'public/research/sitemap.xml').read_text())
    assert len(baseline['old_visible_items'])==len(baseline['old_typed_spans'])==121 and len(baseline['old_sitemap_nodes'])==122
    sources={};native={}
    for record in ['23331709','23174156']:
        root=P/'papers'/record/'sources';sources[record]=census(root)
        r=json.loads((root/'record.response.body').read_text())
        native[record]={x['key']:root/'assets'/x['key'] for x in r['files']}
    assert sum(len(x['files']) for x in sources.values())==306
    rows=[]; html=[]
    for x in plan['targets']:
        target=x['target'];source=S/'public'/target;a=pin(source)
        assert (a['bytes'],a['SHA256'],a['mode'])==(x['after']['bytes'],x['after']['sha256'],int(x['after']['mode'],8))
        record='23331709' if '/low-exponent-supersolvability/' in '/'+target else '23174156' if '/su5-lens-space-counterexample/' in '/'+target else None
        name=source.name;ext=source.suffix.lower();kind='html' if ext=='.html' else 'pdf' if ext=='.pdf' else 'zip' if ext=='.zip' else 'xml' if ext=='.xml' else 'text'
        url='https://aleckriebel.com/'+target
        if target.endswith('/index.html'):url=url[:-len('index.html')]
        category='article' if name=='index.html' and record else 'aggregate' if record is None else 'Bib' if name=='citation.bib' else 'native asset'
        types={'.html':['text/html'],'.pdf':['application/pdf'],'.zip':['application/zip','application/x-zip-compressed'],'.xml':['application/xml','text/xml'],'.bib':['application/x-bibtex','text/x-bibtex','text/plain','application/octet-stream'],'.tex':['application/x-tex','text/x-tex','text/plain','application/octet-stream'],'.md':['text/markdown','text/plain','application/octet-stream'],'.txt':['text/plain']}[ext]
        row={'ordinal':len(rows)+1,'url':url,'website_relative_path':target,'record':record,'category':category,'kind':kind,'accepted_content_types':types,'source':a,'native_source':None}
        if category=='native asset':
            native_pin=pin(native[record][name]);assert {k:a[k] for k in ('bytes','SHA256')}=={k:native_pin[k] for k in ('bytes','SHA256')};row['native_source']=native_pin
        if category=='article':
            page=Page(source.read_bytes());assert page.canonical==[url] and page.meta['og:url']==url
            entity=next(j for j in page.scripts if j.get('@type')=='ScholarlyArticle')
            assert ''.join(page.abstract)==page.meta['DC.description']==entity['abstract']
            html.append({'url':url,'record':record,'abstract':entity['abstract'],'schema':entity,'metadata':page.meta,'citation_PDF_URL':page.meta['citation_pdf_url']})
        rows.append(row)
    css=pin(W/'public/research/research.css');assert css['bytes']==1170 and css['SHA256']=='f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a'
    rows.append({'ordinal':16,'url':'https://aleckriebel.com/research/research.css','website_relative_path':'research/research.css','record':None,'category':'existing CSS','kind':'css','accepted_content_types':['text/css'],'source':css,'native_source':None})
    assert len(rows)==len({x['url'] for x in rows})==16
    write('BASELINE.json',baseline);write('SOURCE_CUSTODY.json',sources);write('STAGE_CUSTODY.json',stage)
    write('SOURCE_EXPECTATIONS.json',{'UTC':now,'schema':'fixed16-http-expectations-v1','rows':rows,'article_semantics':html,
        'baseline':pin(N/'BASELINE.json'),'sources':pin(N/'SOURCE_CUSTODY.json'),'stage':pin(N/'STAGE_CUSTODY.json'),
        'stage_FINAL':pin(S/'FINAL.json'),'stage_manifest':pin(S/'OWNED_MANIFEST.json'),'target_plan':pin(S/'TARGET_PLAN.json'),'root_stage_adoption':pin(ADOPTION),
        'installed_public_files':760,'installed_public_child_directories':368,'index_items':123,'sitemap_nodes':124,
        'baseline_is_historical_preinstall':True,'PDF_text_evidence':'Exact whole native PDF bytes preserve the already reviewed searchable originals; no text extraction/science/browser/reader certification is added.'})
    print(json.dumps({'status':'OFFLINE_EXPECTATIONS_READY_NO_NETWORK','URL_count':16,'expectations':pin(N/'SOURCE_EXPECTATIONS.json'),'baseline':pin(N/'BASELINE.json')}))

if __name__=='__main__':main()
