"""Offline editorial custody/content check and in-memory falsifiers only."""
from pathlib import Path,PurePosixPath
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,hashlib,re,copy,zipfile,zlib,stat,argparse
E=Path(__file__).resolve().parent;P=E.parent.parent;S=P/'sources';Q=P/'publication/promotion'
checks=0
def ck(ok,label):
    global checks
    checks+=1
    if not ok:raise RuntimeError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def obj(p):return json.loads(p.read_text())
def bind(base,rows,digest='sha256'):
    for r in rows:
        b=(base/r['path']).read_bytes();ck(len(b)==r['bytes'] and sha(b)==r[digest],'binding '+r['path'])
class Doc(HTMLParser):
    def __init__(self,h):
        super().__init__();self.meta={};self.canonical=[];self.links=[];self.iframes=[];self.text=[];self.abstract=[];self.ld=[];self.title=[];self.body=False;self.inabs=False;self.inld=False;self.intitle=False;self.h1=0;self.feed(h)
    def handle_starttag(self,t,a):
        a=dict(a)
        if t=='body':self.body=True
        if t=='h1':self.h1+=1
        if t=='meta':self.meta[a.get('name',a.get('property',''))]=a.get('content','')
        if t=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
        if t=='a':self.links.append(a)
        if t=='iframe':self.iframes.append(a)
        if a.get('id')=='original-abstract':self.inabs=True
        if t=='script' and a.get('type')=='application/ld+json':self.inld=True
        if t=='title':self.intitle=True
    def handle_endtag(self,t):
        if t=='p':self.inabs=False
        if t=='script':self.inld=False
        if t=='title':self.intitle=False
    def handle_data(self,d):
        if self.body:self.text.append(d)
        if self.inabs:self.abstract.append(d)
        if self.inld:self.ld.append(d)
        if self.intitle:self.title.append(d)
def content_errors(c,h):
    d=Doc(h);body=' '.join(d.text);errs=[];native=obj(Path(c['source']['native_record_path']))
    def must(ok,label):
        if not ok:errs.append(label)
    must(all(v is False or v is None for k,v in c['state'].items() if k!='private_editorial_complete'),'all current public gates false/null')
    must(c['state']['canonical_url'] is None and c['state']['AA'] is None and not d.canonical,'canonical and native AA unassigned')
    must(c['science']['domain']=={'ellipse':'fixed noncircular','caustic':'strictly nested nondegenerate confocal elliptical','primitive_N_minimum':3,'primitive_N_upper_bound':None,'turning':'coprime 0<tau<N/2','convex_orbits':True,'star_orbits':True,'phase':'every real phase','feet':'ordered infinite supporting lines','area':'signed cyclic shoelace'},'full primitive convex/star signed elliptical domain')
    must(c['science']['full_claim']=='B_plus=C0*A_plus and B_minus=C0*A_minus' and all(c['science'][k] is True for k in ['C0_positive','C0_common_both_foci','C0_phase_independent','four_areas_strictly_positive_positive_orientation']) and c['science']['common_focal_ratio_phase_constant_claimed'] is False,'positive common fixed multiplier versus variable focal ratio')
    must(c['science']['circle']=='separate coincident-focus regular-star case; focal ratios1 and C0=sec^2(pi*tau/N)','separate exact circle case')
    must(c['science']['exclusions']==['hyperbolic caustics','collapsed caustics','two-period diameter walks','unsigned sums of lobe areas','segment-clamped projections'],'essential exclusions')
    must(c['science']['native_runtime']=='assertions enabled; normal execution only','native assertion semantics')
    must(c['science']['follow_up'] is None and c['science']['firstness_certified'] is False,'no unsupported follow-up or firstness')
    must(c['science']['human_peer_review'] is False and c['science']['formal_proof_assistant_certification'] is False and c['science']['AI_tools_used_extensively'] is True,'AI/unrefereed/no human or formal certification')
    must(c['source']['declared_printed_publication_date']==native['metadata']['publication_date']=='2026-10-04','original declared/printed date')
    must(c['source']['record_created']==native['created'] and c['source']['record_updated']==native['updated'],'created and updated kept distinct')
    must(c['source']['native_API_version']==native['metadata']['version']=='1.0' and c['source']['printed_PDF_version']=='1.0','actual printed version')
    must(c['source']['native_license_original']==native['metadata']['license']=={'id':'cc-by-4.0'} and c['source']['paper_prose_license']=='CC BY 4.0' and c['source']['original_code_license']=='MIT','paper CC BY and code MIT distinct')
    must(c['credit']['RGK_primitive_even_symmetry_prior'] is True and c['credit']['triangle_and_classical_nonconstancy_cases_prior'] is True and c['credit']['related_even_multiplier_antecedents_credited'] is True,'prior even/triangle/multiplier credit')
    must(''.join(d.abstract).strip()==(Q/'abstract.txt').read_text().strip(),'full original abstract')
    must(d.h1==1 and ''.join(d.title)==c['copy']['SEO_title'] and d.meta.get('description')==c['copy']['meta_description'] and 70<=len(d.meta.get('description',''))<=170,'specific title/description and one H1')
    must(d.meta.get('robots')=='noindex,nofollow' and d.meta.get('citation_publication_date')=='2026/10/04' and d.meta.get('citation_doi')=='10.5281/zenodo.23149775','private/citation metadata')
    try:ld=json.loads(''.join(d.ld))
    except Exception:ld={}
    must(ld.get('@type')=='ScholarlyArticle' and ld.get('datePublished')=='2026-10-04' and ld.get('version')=='1.0' and ld.get('creativeWorkStatus')=='Unrefereed preprint' and 'url' not in ld and 'mainEntityOfPage' not in ld,'scholarly metadata without live site assignment')
    for phrase in ['strictly nested, nondegenerate confocal elliptical caustic','N ≥ 3','coprime turning number 0 < τ < N/2','infinite supporting line','signed shoelace sum','B₊(w) = C₀ A₊(w)','B₋(w) = C₀ A₋(w)','all four signed areas are strictly positive','The equality of the two focal ratios does not make their common value constant.','reciprocal, below one','C₀ = sec²(πτ/N)','Reversal negates all four areas','positive integral repetition','hyperbolic or collapsed caustics','unsigned sums of lobe areas','projections clamped to side segments','nonvanishing','Reznik, Garcia and Koiller','primitive-even equality proof','triangular positive case and classical nonconstancy','earlier even-period multiplier consequences are credited','AI tools were used extensively','This is an unrefereed preprint','no formal proof-assistant certification','Original verification code:','MIT License','Authorship would be discussed in relation to actual contributions.']:
        must(phrase in body,'required scientific/editorial phrase '+phrase)
    hrefs=[x.get('href') for x in d.links]
    for link in ['https://doi.org/10.5281/zenodo.23079799','https://doi.org/10.5281/zenodo.23089778','https://doi.org/10.5281/zenodo.23088516']:
        must(link in hrefs,'actual related primary '+link)
    must(len(d.iframes)==1 and d.iframes[0].get('title') and urlsplit(d.iframes[0].get('src','')).path=='assets/focal-pedal-ratios-note.pdf','complete original PDF embed')
    for file in ['assets/focal-pedal-ratios-note.pdf','assets/focal-pedal-ratios-verification.zip']:
        must(any(x.get('href')==file and 'download' in x for x in d.links),'original download '+file)
    for x in d.links+d.iframes:
        u=urlsplit(x.get('href',x.get('src','')))
        if not u.scheme and u.path:must((Q/unquote(u.path)).is_file(),'local artifact '+u.path)
    must('background: #fff' in h and 'Arial, sans-serif' in h and 'max-width: 820px' in h and '@media (max-width: 480px)' in h,'plain white responsive Arial column')
    must('9414' not in body and '3133' not in body and 'ROOT_REVIEW' not in body,'no internal audit counts/narratives')
    return errs
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--falsifiers',action='store_true');args=parser.parse_args();c=obj(Q/'promotion.json');h=(Q/'page.html').read_text();ck(not content_errors(c,h),repr(content_errors(c,h)))
    ck(c['state']['private_editorial_complete'] is True,'private copy complete')
    auth=obj(E/'inputs/root-clearance.json');ck(sha((E/'inputs/root-clearance.json').read_bytes())=='b1ae0e007d98f9ece4c712556239c0a9802befd93154972a3d5af39ea9c583b7','root exact authority')
    ck((E/'inputs/root-clearance.json').read_bytes()==Path(c['science']['root_clearance_path']).read_bytes(),'whole unchanged root authority')
    ck((E/'inputs/root-review.md').read_bytes()==Path(auth['root_review']['path']).read_bytes(),'whole unchanged root review')
    ready=obj(S/'SOURCE_READY.json');snap=obj(E/'LITERAL_INPUT_SNAPSHOT.json');ck(ready==snap['source_ready_original']==auth['source_ready']['original'],'literal ready and old flags')
    ck((E/'inputs/SOURCE_READY.json').read_bytes()==(S/'SOURCE_READY.json').read_bytes(),'raw ready copy')
    record=Path(ready['native_record_body_path']);ck(record.read_bytes()==(E/'inputs/record-attempt2.body').read_bytes() and obj(record)==snap['native_record_original']==auth['native_record_original'],'whole native record/order')
    trs=snap['four_heterogeneous_transport_objects_in_native_order'];ck([x['name'] for x in trs]==ready['transport_files'] and [type(x['original_object']).__name__ for x in trs]==['list','dict','list','list'],'four literal heterogeneous schemas/order')
    for r in trs:
        b=Path(r['original_source_path']).read_bytes();ck(sha(b)==r['sha256'] and b==(E/'inputs'/r['name']).read_bytes() and json.loads(b)==r['original_object'],'literal full transport and opaque header order')
    for lane,r in auth['reviews'].items():
        b=Path(r['verdict_path']).read_bytes();ck(sha(b)==r['verdict_sha256'] and b==(E/('inputs/'+lane+'-VERDICT.json')).read_bytes() and json.loads(b)==snap['literal_custom_verdicts'][lane]==r['verdict_original'],'whole literal custom verdict/flags '+lane)
        ck(sha(Path(r['report_path']).read_bytes())==r['report_sha256'] and sha(Path(r['seal_path']).read_bytes())==r['seal_sha256'],'unchanged scientific packet '+lane)
    ss=obj(S/'SOURCE_READY_SEAL.json');ck(ss['SOURCE_READY_SHA256']==sha((S/'SOURCE_READY.json').read_bytes()) and ss['manifest_SHA256']==sha((S/'SOURCE_READY_MANIFEST.json').read_bytes()),'native source seal fields');bind(S,obj(S/'SOURCE_READY_MANIFEST.json')['files'],'SHA256')
    ck(obj(record)['files']==[r['original_api_file_object'] for r in ready['all_native_assets_in_original_order']],'whole native file order')
    for r in ready['all_native_assets_in_original_order']:
        b=Path(r['path']).read_bytes();key=r['original_api_file_object']['key'];ck(b==(Q/'assets'/key).read_bytes() and sha(b)==r['SHA256'] and 'md5:'+hashlib.md5(b).hexdigest()==r['original_api_file_object']['checksum'],'byte-identical actual full asset '+key)
    ck((Q/'assets/focal-pedal-ratios-note.pdf').read_bytes().startswith(b'%PDF') and (Q/'assets/focal-pedal-ratios-note.pdf').stat().st_size==73905,'successful actual PDF selected, not88B failure')
    searchable=(P/'reviews/scope/actual_pdf_text.txt').read_text()
    ck(searchable.count('\f')==6 and 'Focal pedal area ratios of closed elliptic billiards' in searchable,'existing complete searchable actual-PDF text evidence')
    custody=obj(S/'archive-custody.json');members=custody['regular_members']
    with zipfile.ZipFile(Q/'assets/focal-pedal-ratios-verification.zip') as z:
        infos=z.infolist();ck(len(infos)==len(members)==24 and z.testzip() is None,'whole24-payload archive/CRC')
        for i,r in zip(infos,members):
            pp=PurePosixPath(i.filename);ck(not pp.is_absolute() and '..' not in pp.parts and '\\' not in i.filename and stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG),'safe regular original member')
            b=z.read(i);ck(i.filename==r['original_member_name'] and infos[r['entry_ordinal']-1] is i and sha(b)==r['SHA256'] and b==Path(r['extracted_path']).read_bytes() and (zlib.crc32(b)&0xffffffff)==int(r['CRC32'],16),'exact member/order/CRC/bytes')
    tex=Path(ready['controlling_TeX']['path']).read_text();aa=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1).strip();ck(aa==(E/'ORIGINAL_ABSTRACT.tex').read_text().strip() and ' '.join(aa.split())==(Q/'abstract.txt').read_text().strip(),'full original abstract TeX/text')
    ck('MIT License' in Path(c['source']['code_license_source']).read_text() and 'Creative Commons Attribution 4.0' in Path(c['source']['paper_license_source']).read_text(),'actual distinct licenses')
    browser=obj(E/'BROWSER_QA.json');ck(browser['actual_live_or_public_service_checked'] is False and browser['canonical_or_tracker_assigned'] is False,'private browser receipt only')
    ck([(x['width'],x['height']) for x in browser['records']]==[(1440,1200),(390,844)],'desktop/mobile actual dimensions')
    for x in browser['records']:
        m=x['metrics'];ck(m['body']<=m['viewport'] and 'Arial' in m['font'] and m['background']=='rgb(255, 255, 255)' and m['canonical'] is None and m['robots']=='noindex,nofollow','private responsive layout')
    if (E/'INPUT_MANIFEST.json').exists():bind(Path('/'),obj(E/'INPUT_MANIFEST.json')['files'])
    if (E/'OWNED_MANIFEST.json').exists():
        rows=obj(E/'OWNED_MANIFEST.json')['files'];bind(P,rows);actual={str(f.relative_to(P)) for root in [E,Q] for f in root.rglob('*') if f.is_file() and f not in [E/'OWNED_MANIFEST.json',E/'SEAL.json']};ck(actual=={r['path'] for r in rows},'complete owned inventory')
    sealed=(E/'SEAL.json').exists()
    if sealed:
        for n,digest in obj(E/'SEAL.json')['bound_files_sha256'].items():ck(sha((P/n).read_bytes())==digest,'editorial final seal '+n)
    rejected=[]
    if args.falsifiers:
        cases=[('premature live gate',lambda x:x['state'].__setitem__('site_deployed',True)),('assigned canonical',lambda x:x['state'].__setitem__('canonical_url',x['proposed']['page_url'])),('hyperbolic scope',lambda x:x['science']['domain'].__setitem__('caustic','confocal hyperbolic')),('stars omitted',lambda x:x['science']['domain'].__setitem__('star_orbits',False)),('finite-only period scope',lambda x:x['science']['domain'].__setitem__('primitive_N_upper_bound',24)),('clamped segment feet',lambda x:x['science']['domain'].__setitem__('feet','clamped segments')),('unsigned lobe area',lambda x:x['science']['domain'].__setitem__('area','unsigned lobe sum')),('false constant focal ratio',lambda x:x['science'].__setitem__('common_focal_ratio_phase_constant_claimed',True)),('lost strict positivity',lambda x:x['science'].__setitem__('four_areas_strictly_positive_positive_orientation',False)),('wrong circle factor',lambda x:x['science'].__setitem__('circle','C0=cos^2(pi*tau/N)')),('creation used as publication date',lambda x:x['source'].__setitem__('declared_printed_publication_date','2026-10-05')),('code wrongly CC BY',lambda x:x['source'].__setitem__('original_code_license','CC BY 4.0')),('optimized native assert PASS accepted',lambda x:x['science'].__setitem__('native_runtime','optimized execution accepted')),('new follow-up inserted',lambda x:x['science'].__setitem__('follow_up','Generic extension')),('human review invented',lambda x:x['science'].__setitem__('human_peer_review',True))]
        for name,mutate in cases:
            bad=copy.deepcopy(c);mutate(bad);ee=content_errors(bad,h);ck(bool(ee),'falsifier passed '+name);rejected.append({'mutation':name,'rejected_by':ee})
        for name,bad in [('truncated original abstract',h.replace('Known even and triangular cases and classical methods are credited explicitly.','')),('false focal-ratio constancy in body',h.replace('The equality of the two focal ratios does not make their common value constant.','The equality of the two focal ratios makes their common value constant.')),('old even credit erased',h.replace('primitive-even equality proof','new even equality discovery')),('related note omitted',h.replace('https://doi.org/10.5281/zenodo.23088516','https://example.invalid/omitted')),('HTML live canonical assigned',h.replace('</head>','<link rel="canonical" href="https://aleckriebel.com/research/fabricated/"></head>'))]:
            ee=content_errors(c,bad);ck(bool(ee),'HTML falsifier passed '+name);rejected.append({'mutation':name,'rejected_by':ee})
    print(json.dumps({'status':'PASS_PRIVATE_EDITORIAL116_CUSTODY_AND_FULL_COPY','sealed':sealed,'checks':checks,'meaningful_in_memory_falsifiers_rejected':len(rejected),'falsifiers':rejected,'source_builders_or_scientific_programs_executed':False,'network_or_service_mutations':False,'public_promotion_authority':False,'canonical_url':None,'AA':None},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
