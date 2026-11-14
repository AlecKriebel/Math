"""Bounded new-record semantic faults; never alter scientific/source evidence."""
from pathlib import Path
import copy, datetime, hashlib, json, sys
from html import escape
from bm_body_contract import check_bm_page
from banach_mtp2_source import banach_mtp2_source_view, validate_bm_edition, validate_bm_assets, validate_bm_transports
E=Path(__file__).resolve().parent;P=E.parent.parents[1];S=E/'public';rows=[]
index=(S/'research/index.html').read_text();sitemap=(S/'research/sitemap.xml').read_text()
def attempt(rid,name,fn,positive=False):
    try:
        value=fn();bad=[k for k,v in value.get('checks',{}).items() if not v] if isinstance(value,dict) else []
        rejected=bool(bad);detail=bad
    except Exception as ex:rejected=True;detail=[type(ex).__name__+': '+str(ex)]
    ok=(not rejected) if positive else rejected
    rows.append({'record':rid,'case':name,'positive':positive,'passed':ok,'evidence':detail})
    if not ok:print('UNDETECTED_OR_BAD_POSITIVE',rid,name,detail)
for rid in ['23217863','23146753']:
    paper=P/'papers'/rid;c=json.loads((paper/'publication.json').read_bytes());g=json.loads((paper/'promotion.json').read_bytes());out=S/'research'/c['slug'];file=out/'index.html';original=file.read_text()
    check=lambda:check_bm_page(P,S,rid,index,sitemap)
    attempt(rid,'pristine_full_positive',check,True)
    faults=[]
    def add(name,a,b):
        if a not in original:raise ValueError('fault anchor absent '+name)
        faults.append((name,original.replace(a,b,1)))
    add('extra_body_claim','</article>','<p>A universally strongest result.</p></article>')
    for wrapper in ['template','noscript','textarea','xmp','iframe','div']:
        faults.append(('outer_'+wrapper+'_body_wrapper',original.replace('<body>','<'+wrapper+'><body>',1).replace('</body>','</body></'+wrapper+'>',1)))
    add('hidden_article','<article>','<article hidden>')
    add('inert_article','<article>','<article inert>')
    add('aria_hidden_article','<article>','<article aria-hidden="true">')
    add('inline_hidden_article','<article>','<article style="display:none">')
    add('unknown_article_class','<article>','<article class="hidden">')
    add('known_hiding_class_on_paragraph','<section id="abstract"><h2>Original abstract</h2><p>','<section id="abstract"><h2>Original abstract</h2><p class="skip-link">')
    faults.append(('relocated_known_hiding_class',original.replace('class="skip-link" ','',1).replace('<h1><a href=','<h1><a class="skip-link" href=',1)))
    add('hidden_abstract','<section id="abstract">','<section id="abstract" hidden>')
    add('head_css_hiding_article','</head>','<style>article {display:none}</style></head>')
    add('script_in_body','</article>','<script>document.querySelector("article").remove()</script></article>')
    add('extra_head_stylesheet','</head>','<link rel="stylesheet" href="/hidden.css"></head>')
    add('wrong_stylesheet','/research/research.css','/research/other.css')
    add('changed_h1','<h1><a href="/research/'+c['slug']+'/">'+escape(c['title']),'<h1><a href="/research/'+c['slug']+'/">Other title')
    add('h1_wrong_destination','<h1><a href="/research/'+c['slug']+'/">','<h1><a href="/research/unrelated/">')
    add('research_wrong_destination','href="/research/">Research</a>','href="/blog/">Research</a>')
    add('canonical_wrong','rel="canonical" href="https://aleckriebel.com/research/'+c['slug']+'/"','rel="canonical" href="https://aleckriebel.com/research/other/"')
    add('abstract_word_loss',escape(c['abstract']),escape(c['abstract'].replace('finite','',1) if rid=='23146753' else c['abstract'].replace('every','',1)))
    add('abstract_heading','<h2>Original abstract</h2>','<h2>Summary</h2>')
    for key in ['plain_language','result','why_it_works','limitations']:
        for i,text in enumerate(c[key]):add(key+'_'+str(i),'<p>'+escape(text)+'</p>','<p>'+escape(text)+' Altered.</p>')
    for key in ['status','ai_disclosure','edition_note','collaboration']:
        add('exact_'+key,'<p>'+escape(c[key])+'</p>','<p>'+escape(c[key])+' Altered.</p>')
    for i,x in enumerate(c['background']):add('background_note_'+str(i),escape(x['note']),escape(x['note'])+' Altered.')
    for i,x in enumerate(c['related_resources']):add('related_url_'+str(i),'href="'+escape(x['url'])+'">'+escape(x['label']),'href="https://example.invalid/">'+escape(x['label']))
    add('doi_metadata','name="citation_doi" content="'+c['doi']+'"','name="citation_doi" content="10.0/wrong"')
    add('orcid_metadata','name="citation_author_orcid" content="0009-0001-9320-500X"','name="citation_author_orcid" content="0000-0000-0000-0000"')
    add('date_metadata','name="citation_publication_date" content="'+c['publication_date'].replace('-','/')+'"','name="citation_publication_date" content="2026/01/01"')
    add('description_metadata','name="description" content="'+escape(c['description'])+'"','name="description" content="Other"')
    add('visible_date','datetime="'+c['publication_date']+'"','datetime="2026-01-01"')
    add('schema_DOI','"value": "'+c['doi']+'"','"value": "10.0/wrong"')
    add('schema_abstract','"abstract": '+json.dumps(c['abstract'],ensure_ascii=False),'"abstract": "Omitted"')
    if rid=='23217863':
        add('invented_version','"creativeWorkStatus":','"version": "1.0", "creativeWorkStatus":')
        add('mixed_license_note_loss','<p>'+escape(c['license_note'])+'</p>','<p>All files are CC BY.</p>')
        add('strict_inequality',escape('d_BM(M,N)<1+ε_M'),escape('d_BM(M,N)≤1+ε_M'))
    else:
        add('schema_edition_wrong','"version": "1.0"','"version": "2.0"')
        add('MTP_inequality',escape('p(x∧y)p(x∨y)≥p(x)p(y)'),escape('p(x∧y)p(x∨y)≤p(x)p(y)'))
        add('facial_nonempty_hypothesis',escape('For a nonempty edge set'),escape('For every edge set'))
        add('license_header_loss','href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0','href="https://creativecommons.org/licenses/by/4.0/">MIT')
    add('iframe_wrong_title','title="'+escape(c['title'])+' — complete '+str(c['pdf_pages'])+'-page paper"','title="Wrong reader"')
    add('iframe_wrong_src','src="'+c['pdf_filename']+'#view=FitH"','src="other.pdf"')
    add('iframe_duplicate','</iframe>','</iframe><iframe src="other.pdf"></iframe>')
    prefix='/research/'+c['slug']+'/' if rid=='23146753' else ''
    for label,name,download in [('Open PDF',c['pdf_filename'],False),('Download PDF',c['pdf_filename'],True),('Download complete ZIP',c['supplement_filename'],True),('Download BibTeX','citation.bib',True)]:
        token='<a href="'+prefix+name+'"'+(' download' if download else '')+'>'+label+'</a>'
        add('local_destination_'+label,token,token.replace(prefix+name,'wrong.file'))
        if download:add('download_flag_'+label,token,token.replace(' download',''))
    for label,name in [('Download original PDF from Zenodo',c['pdf_filename']),('Download original complete ZIP from Zenodo',c['supplement_filename'])]:
        url='https://zenodo.org/api/records/'+rid+'/files/'+name+'/content'
        token='<a href="'+url+'" download>'+label+'</a>'
        add('original_destination_'+label,token,token.replace(url,'https://example.invalid/'))
        add('original_download_flag_'+label,token,token.replace(' download',''))
    try:
        for name,mutant in faults:
            file.write_text(mutant);attempt(rid,name,check)
    finally:file.write_text(original)
    for key in ['pdf_filename','supplement_filename']:
        asset=out/c[key];data=asset.read_bytes();mutated=bytearray(data);mutated[-1]^=1
        try:asset.write_bytes(mutated);attempt(rid,'one_byte_'+key,check)
        finally:asset.write_bytes(data)
    bib=out/'citation.bib';data=bib.read_bytes()
    try:bib.write_bytes(data+b'% changed\n');attempt(rid,'citation_bytes_changed',check)
    finally:bib.write_bytes(data)
    attempt(rid,'restored_full_positive',check,True)
    b=c['source_binding'];raw=json.loads((paper/b['source_receipt_path']).read_bytes());meta=json.loads((paper/b['metadata_path']).read_bytes());api=json.loads((paper/b['raw_record_path']).read_bytes());events=json.loads((paper/b['transport_receipt_path']).read_bytes())
    def source_case(name,target,mutator,validator):
        value=copy.deepcopy(target);mutator(value);attempt(rid,name,lambda:validator(value))
    for name,mutator in [('coerced_generic_PASS',lambda x:x.__setitem__('status','PASS')),('unknown_qualified_status',lambda x:x.__setitem__('status',x['status']+'_EXTRA')),('whole_custom_verdict_false_changed',lambda x:x['reviews']['scope']['verdict'].__setitem__('human_peer_review',True)),('whole_root_authority_extra',lambda x:x['root_clearance_record'].__setitem__('invented',True)),('whole_family_entry_extra',lambda x:x['reviews']['analytic']['root_authority_entry'].__setitem__('invented',True)),('historical_false_forged',lambda x:x.__setitem__('public_page_published',True))]:source_case(name,g,mutator,lambda x:banach_mtp2_source_view(paper,c,x))
    for name,mutator in [('raw_metadata_extra',lambda x:x['metadata'].__setitem__('unknown',True)),('raw_version_absent_as_null' if rid=='23217863' else 'raw_version_key_missing',lambda x:x['metadata'].__setitem__('version',None) if rid=='23217863' else x['metadata'].pop('version')),('raw_ID_boolean',lambda x:x.__setitem__('id',True))]:source_case(name,api,mutator,lambda x:validate_bm_edition(rid,c,g,raw,meta,x))
    for name,mutator in [('assets_alias',lambda x:x.__setitem__('assets',x.pop('all_assets'))),('asset_order_reversed',lambda x:x['all_assets'].reverse()),('asset_size_boolean',lambda x:x['all_assets'][0].__setitem__('bytes',True)),('asset_uppercase_md5',lambda x:x['all_assets'][0].__setitem__('md5',x['all_assets'][0]['md5'].upper())),('asset_short_md5',lambda x:x['all_assets'][0].__setitem__('md5',x['all_assets'][0]['md5'][1:])),('asset_original_object_changed',lambda x:x['all_assets'][0]['original_api_file_object'].__setitem__('id','invented')),('asset_extra_field',lambda x:x['all_assets'][0].__setitem__('invented',None))]:source_case(name,raw,mutator,lambda x:validate_bm_assets(paper,rid,x,api))
    for name,mutator in [('transport_status_boolean',lambda x:x[0].__setitem__('status',True)),('transport_record_URL_changed',lambda x:x[0].__setitem__('requested_url','https://example.invalid/')),('transport_asset_order_reversed',lambda x:x.__setitem__(slice(3,5),list(reversed(x[3:])))),('transport_extra_md5',lambda x:x[3].__setitem__('md5','fake')),('transport_header_changed',lambda x:x[-1]['headers'].__setitem__('oc-checksum','MD5:00000000000000000000000000000000'))]:source_case(name,events,mutator,lambda x:validate_bm_transports(paper,rid,x,raw,api))
    if rid=='23146753':source_case('opaque_header_padded',events,lambda x:x[-1]['headers'].__setitem__('oc-checksum','MD5:0afc4fd82272a87b678e0efce8beea0d'),lambda x:validate_bm_transports(paper,rid,x,raw,api))
mode='optimized' if not __debug__ else 'normal';result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':mode,'code_bindings':{n:hashlib.sha256((E/n).read_bytes()).hexdigest() for n in ['fault_campaign.py','banach_mtp2_source.py','bm_body_contract.py','final-content-check.proposed.py']},'cases':rows,'case_count':len(rows),'passed':sum(r['passed'] for r in rows),'status':'PASS' if all(r['passed'] for r in rows) else 'FAIL','source_or_science_files_mutated':False,'static_visibility_boundary':'Closed whole-document parent/nesting grammar rejects inert/raw-text/foreign body wrappers and all hidden/inert/aria-hidden/inline styles/unknown or relocated classes, body scripts and extra stylesheets. Existing stylesheet bytes are bound by baseline; actual browser/mobile/native-PDF remains a separate gate.'}
(E/('FAULTS_'+mode+'.json')).write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(mode,result['passed'],'/',len(rows));raise SystemExit(0 if result['status']=='PASS' else 1)
