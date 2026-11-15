"""Offline private-editorial verifier and in-memory falsifiers; no source replay."""
from pathlib import Path,PurePosixPath
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,hashlib,copy,re,zipfile,zlib,stat,argparse
E=Path(__file__).resolve().parent
P=E.parent.parent
Q=P/'publication/promotion'
S=P/'sources'
checks=0
def ck(ok,label):
    global checks
    checks+=1
    if not ok:raise RuntimeError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def obj(p):return json.loads(p.read_text())
def bind(base,rows):
    for r in rows:
        b=(base/r['path']).read_bytes();ck(len(b)==r['bytes'],'size '+r['path']);ck(sha(b)==r['sha256'],'hash '+r['path'])
class Doc(HTMLParser):
    def __init__(self,text):
        super().__init__();self.meta={};self.links=[];self.iframes=[];self.h1=0;self.canon=[];self.body=[];self.abstract=[];self.ld=[];self.inbody=False;self.inabs=False;self.inld=False;self.title=[];self.intitle=False;self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='body':self.inbody=True
        if tag=='h1':self.h1+=1
        if tag=='meta':self.meta[a.get('name',a.get('property',''))]=a.get('content','')
        if tag=='link' and a.get('rel')=='canonical':self.canon.append(a.get('href'))
        if tag=='a':self.links.append(a)
        if tag=='iframe':self.iframes.append(a)
        if a.get('id')=='original-abstract':self.inabs=True
        if tag=='script' and a.get('type')=='application/ld+json':self.inld=True
        if tag=='title':self.intitle=True
    def handle_endtag(self,tag):
        if tag=='p':self.inabs=False
        if tag=='script':self.inld=False
        if tag=='title':self.intitle=False
    def handle_data(self,data):
        if self.inbody:self.body.append(data)
        if self.inabs:self.abstract.append(data)
        if self.inld:self.ld.append(data)
        if self.intitle:self.title.append(data)
def content_errors(c,h):
    d=Doc(h);b=' '.join(d.body);err=[]
    def must(ok,label):
        if not ok:err.append(label)
    actual=obj(S/'record.raw.json')
    must(all(v is False or v is None for k,v in c['state'].items() if k!='private_editorial_complete'),'current public flags/canonical/AA')
    must(c['state']['canonical_url'] is None and c['state']['AA'] is None and not d.canon,'unassigned canonical/native AA')
    must(c['science']['domain']=={'integer_n_minimum':3,'integer_n_upper_bound':None,'F0':0,'F1':1,'F2':1,'q':'F_n','p':'F_(n-1)','sphere_radius':1,'longitude':'exact rational 2*pi*p*k/q','latitude':'unshifted 1-2*k/q','index_lower_inclusive':0,'index_upper_exclusive':'q'},'full exact all-n rational unshifted half-open domain')
    must(c['science']['minimum_metric']=='ambient Euclidean chord' and c['science']['minimum_formula']=='2/sqrt(F_n)' and c['science']['unique_unordered_minimizing_pair']==[0,1] and c['science']['geodesic_minimum_formula']=='2*arcsin(1/sqrt(F_n))','metric/minimum/unique pair')
    must(c['science']['follow_up'] is None,'no unsupported or already-covered follow-up')
    must(c['science']['human_peer_review'] is False and c['science']['formal_proof_assistant_certification'] is False and c['science']['AI_tools_used_extensively'] is True,'honest AI/referee/formal status')
    must(c['source']['declared_publication_date']==actual['metadata']['publication_date']=='2026-10-05','original declared publication date')
    must(c['source']['record_created']==actual['created'] and c['source']['record_updated']==actual['updated'],'creation/update kept distinct')
    must(c['source']['native_API_version']==actual['metadata']['version']=='1.0' and c['source']['printed_PDF_version'] is None,'API version unprinted')
    must(c['source']['license_original']==actual['metadata']['license']=={'id':'cc-by-4.0'},'native rights')
    related=c['prior_work']['later_matching_related_work']
    must(related['record_id']==23681420 and related['version']=='1.0' and related['declared_publication_date']=='2026-10-27' and related['same_exact_minimum_and_unique_pair_stated'] is True and related['chronology_only'] is True and all(related[k] is False for k in ['independence_inference','influence_inference','absolute_priority_inference']),'later matching work with neutral chronology')
    must(''.join(d.abstract).strip()==(Q/'abstract.txt').read_text().strip(),'complete original abstract text')
    must(d.h1==1 and ''.join(d.title)==c['copy']['SEO_title'],'one title and descriptive SEO title')
    must(d.meta.get('description')==c['copy']['meta_description'] and 70<=len(d.meta['description'])<=170,'specific meta description')
    must(d.meta.get('robots')=='noindex,nofollow','private preview remains noindex')
    must(d.meta.get('citation_publication_date')=='2026/10/05' and d.meta.get('citation_doi')=='10.5281/zenodo.23174283' and d.meta.get('citation_author')=='Alec Kriebel','citation metadata')
    try:ld=json.loads(''.join(d.ld))
    except Exception:ld={}
    must(ld.get('@type')=='ScholarlyArticle' and ld.get('datePublished')=='2026-10-05' and ld.get('version')=='1.0' and ld.get('creativeWorkStatus')=='Unrefereed preprint' and 'url' not in ld and 'mainEntityOfPage' not in ld,'scholarly draft metadata without assigned site URL')
    for token in ['For every integer n ≥ 3','0 ≤ k < q','2/√Fₙ','{z₀, z₁}','2 arcsin(1/√Fₙ)','k ≡ pj (mod q)','p² ≡ (−1)ⁿ (mod q)','(x, y, z) ↦ (x, −y, −z)','Zaremba','Suryanarayana, Cools and Nuyens','Brauchart–Dick','final graphics editions','27 October 2026','broader rational-lattice criterion','neither independence nor influence nor absolute priority','AI tools were used extensively','This is an unrefereed preprint','no formal proof-assistant certification','PDF itself does not print a version number']:
        must(token in b,'required exact public scope/credit/status '+token)
    must('https://doi.org/10.5281/zenodo.23681420' in [x.get('href') for x in d.links],'actual later primary link')
    must(len(d.iframes)==1 and d.iframes[0].get('title') and urlsplit(d.iframes[0].get('src','')).path=='assets/spherical_fibonacci_separation.pdf','complete unchanged PDF embed')
    must(any(x.get('href')=='assets/spherical_fibonacci_separation.pdf' and 'download' in x for x in d.links),'direct PDF download')
    must(any(x.get('href')=='assets/spherical_fibonacci_verification.zip' and 'download' in x for x in d.links),'whole original support download')
    must('181983' not in b and '630 checks' not in b and 'ROOT_REVIEW' not in b,'internal audit counts/narratives omitted')
    must('background: #fff' in h and 'Arial, sans-serif' in h and 'max-width: 820px' in h and '@media (max-width: 480px)' in h,'plain responsive white Arial column')
    must('Authorship would be discussed in relation to actual contributions.' in b,'contribution-based passive collaboration')
    for link in d.links+d.iframes:
        target=link.get('href',link.get('src',''));u=urlsplit(target)
        if not u.scheme and u.path:must((Q/unquote(u.path)).is_file(),'local linked artifact '+u.path)
    return err
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--falsifiers',action='store_true');args=parser.parse_args()
    c=obj(Q/'promotion.json');h=(Q/'page.html').read_text();errors=content_errors(c,h);ck(not errors,'candidate '+repr(errors))
    ck(c['state']['private_editorial_complete'] is True,'private candidate complete')
    browser=obj(E/'BROWSER_QA.json')
    ck(browser['status']=='PASS_PRIVATE_LOCAL_DESKTOP_MOBILE_LAYOUT' and browser['actual_live_or_public_service_checked'] is False and browser['canonical_or_tracker_assigned'] is False,'local browser receipt not public gate')
    ck([(r['width'],r['height']) for r in browser['records']]==[(1440,1200),(390,844)],'actual desktop/mobile dimensions')
    for r in browser['records']:
        m=r['metrics'];ck(m['body']<=m['viewport'] and 'Arial' in m['font'] and m['background']=='rgb(255, 255, 255)' and m['canonical'] is None and m['robots']=='noindex,nofollow','browser layout and private boundaries')
    authority_path=E/'inputs/root-clearance.json';authority=obj(authority_path)
    ck(sha(authority_path.read_bytes())=='c22dcb687d2065e49b1186b66701687ece05c74468bdf78ae85422432fcd3298','root authority exact pin')
    ck(authority_path.read_bytes()==Path(c['science']['root_clearance_path']).read_bytes(),'whole original root authority unchanged')
    ck((E/'inputs/root-review.md').read_bytes()==Path(authority['root_review']['path']).read_bytes(),'whole root review unchanged')
    literal=obj(E/'LITERAL_INPUT_SNAPSHOT.json')
    ck(literal['source_ready_original']==authority['whole_original_source_ready_object']==obj(S/'SOURCE_READY.json'),'literal ready including old flags')
    ck(literal['whole_native_transport_objects']==authority['whole_native_transport_objects'] and len(literal['whole_native_transport_objects'])==6,'all six native objects and header order')
    for lane,r in authority['reviews'].items():
        vv=Path(r['verdict_path']).read_bytes();ck(sha(vv)==r['verdict_sha256'],'literal custom verdict pin '+lane)
        ck(vv==(E/('inputs/'+lane+'-VERDICT.json')).read_bytes(),'unchanged custom verdict bytes '+lane)
        ck(literal['literal_custom_verdicts'][lane]==json.loads(vv)==r['verdict_original'],'whole custom verdict/flags '+lane)
        ck(sha(Path(r['report_path']).read_bytes())==r['report_sha256'] and sha(Path(r['seal_path']).read_bytes())==r['seal_sha256'],'sealed scientific inputs '+lane)
    for r in authority['whole_native_transport_objects']:
        bb=Path(r['path']).read_bytes();ck(sha(bb)==r['sha256'] and bb==(E/'inputs'/Path(r['path']).name).read_bytes(),'native transport exact bytes')
        ck(json.loads(bb)==r['original'],'native transport whole object/order')
    srcseal=obj(S/'SOURCE_READY_SEAL.json')
    ck(srcseal['source_ready_sha256']==sha((S/'SOURCE_READY.json').read_bytes()),'source-ready seal')
    ck(srcseal['manifest_sha256']==sha((S/'SOURCE_READY_MANIFEST.json').read_bytes()),'source manifest seal');bind(S,obj(S/'SOURCE_READY_MANIFEST.json')['files'])
    record=obj(S/'record.raw.json');ready=obj(S/'SOURCE_READY.json')
    ck(record['files']==[r['original_api_file_object'] for r in ready['all_assets_in_original_order']],'original native ordered assets')
    for asset in ready['all_assets_in_original_order']:
        bb=Path(asset['path']).read_bytes();key=asset['original_api_file_object']['key']
        ck(bb==(Q/'assets'/key).read_bytes(),'byte-identical staged original '+key)
        ck(sha(bb)==asset['sha256'] and 'md5:'+hashlib.md5(bb).hexdigest()==asset['original_api_file_object']['checksum'],'native full SHA/MD5')
    members=obj(S/'archive-members.json')['full_original_ordered_regular_occurrences']
    with zipfile.ZipFile(S/'spherical_fibonacci_verification.zip') as z:
        infos=z.infolist();ck(len(infos)==len(members)==13 and z.testzip() is None,'whole original13-payload ZIP and CRC')
        for i,r in zip(infos,members):
            name=PurePosixPath(i.filename);mode=i.external_attr>>16
            ck(not name.is_absolute() and '..' not in name.parts and '\\' not in i.filename and stat.S_IFMT(mode) in (0,stat.S_IFREG),'safe regular member')
            ck(i.filename==r['original_member_name'] and infos[r['ordinal']] is i,'native ZIP order')
            bb=z.read(i);ck(sha(bb)==r['sha256'] and bb==Path(r['path']).read_bytes() and (zlib.crc32(bb)&0xffffffff)==int(r['CRC32'],16),'original payload bytes/CRC')
    tex=(S/'published-source/spherical_fibonacci_separation.tex').read_text();aa=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1).strip()
    ck((E/'ORIGINAL_ABSTRACT.tex').read_text().strip()==aa,'whole original abstract TeX')
    if (E/'INPUT_MANIFEST.json').exists():bind(Path('/'),obj(E/'INPUT_MANIFEST.json')['files'])
    if (E/'OWNED_MANIFEST.json').exists():
        rows=obj(E/'OWNED_MANIFEST.json')['files'];bind(P,rows)
        actual={str(f.relative_to(P)) for base in [E,Q] for f in base.rglob('*') if f.is_file() and f not in [E/'OWNED_MANIFEST.json',E/'SEAL.json']}
        ck(actual=={r['path'] for r in rows},'complete owned inventory')
    sealed=(E/'SEAL.json').exists()
    if sealed:
        for name,hh in obj(E/'SEAL.json')['bound_files_sha256'].items():ck(sha((P/name).read_bytes())==hh,'editorial seal '+name)
    rejected=[]
    if args.falsifiers:
        tests=[('assigned public canonical',lambda x:x['state'].__setitem__('canonical_url',x['proposed']['page_url'])),('premature deployment flag',lambda x:x['state'].__setitem__('site_deployed',True)),('finite-only n domain',lambda x:x['science']['domain'].__setitem__('integer_n_upper_bound',30)),('irrational golden angle',lambda x:x['science']['domain'].__setitem__('longitude','irrational golden angle')),('both endpoints',lambda x:x['science']['domain'].__setitem__('index_upper_exclusive','q+1')),('chord confused with geodesic',lambda x:x['science'].__setitem__('minimum_metric','geodesic')),('lost unique closest pair',lambda x:x['science'].__setitem__('unique_unordered_minimizing_pair',None)),('updated date substituted',lambda x:x['source'].__setitem__('declared_publication_date','2026-10-10')),('invented printed version',lambda x:x['source'].__setitem__('printed_PDF_version','1.0')),('wrong license',lambda x:x['source'].__setitem__('license_original',{'id':'cc0-1.0'})),('inferred independence',lambda x:x['prior_work']['later_matching_related_work'].__setitem__('independence_inference',True)),('already covered follow-up',lambda x:x['science'].__setitem__('follow_up','Broader rational-lattice Zaremba-index criterion')),('false human peer review',lambda x:x['science'].__setitem__('human_peer_review',True))]
        for label,mutate in tests:
            bad=copy.deepcopy(c);mutate(bad);ee=content_errors(bad,h);ck(bool(ee),'falsifier unexpectedly passed '+label);rejected.append({'mutation':label,'rejected_by':ee})
        for label,bad in [('truncated original abstract',h.replace('We include an elementary proof of the weaker arithmetic estimate needed here, making the argument self-contained.','')),('omitted later primary link',h.replace('https://doi.org/10.5281/zenodo.23681420','https://example.invalid/omitted')),('erased classical credit',h.replace('Suryanarayana, Cools and Nuyens','an unnamed author')),('assigned HTML canonical',h.replace('</head>','<link rel="canonical" href="https://aleckriebel.com/research/fabricated/"></head>'))]:
            ee=content_errors(c,bad);ck(bool(ee),'HTML falsifier unexpectedly passed '+label);rejected.append({'mutation':label,'rejected_by':ee})
    print(json.dumps({'status':'PASS_PRIVATE_EDITORIAL_CUSTODY_AND_COPY','sealed':sealed,'checks':checks,'meaningful_in_memory_falsifiers_rejected':len(rejected),'falsifiers':rejected,'source_or_scientific_programs_executed':False,'network_or_service_mutations':False,'canonical_url':None,'AA':None,'publication_authority':False},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
