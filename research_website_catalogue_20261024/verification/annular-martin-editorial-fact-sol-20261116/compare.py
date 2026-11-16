#!/usr/bin/env python3
"""Fixed, stdout-only annular editorial comparison; no project/helper execution."""
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
import hashlib
import json
import re
import stat

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
N=P/'verification/annular-martin-editorial-fact-sol-20261116'
R=P/'papers/23332261/reviews/editorial'

def pin(data):
    return {'bytes':len(data),'SHA256':hashlib.sha256(data).hexdigest()}

def fixed(path,row):
    assert not path.is_symlink()
    data=path.read_bytes()
    assert pin(data)=={k:row[k] for k in ('bytes','SHA256')},str(path)
    if 'mode' in row:
        mode=row['mode']
        if isinstance(mode,str):mode=int(mode,8)
        assert stat.S_IMODE(path.stat().st_mode)==mode
    return data

def load(path):
    return json.loads(path.read_bytes())

def one(text,pattern):
    found=re.findall(pattern,text)
    assert len(found)==1,pattern
    return found[0]

class Tags(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta={};self.links=[];self.ids=[];self.labels=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='meta':self.meta[d.get('name',d.get('property'))]=d.get('content')
        if 'id' in d:self.ids.append(d['id'])
        if tag=='link':self.links.append(d)
        self.labels.extend(d.get('aria-labelledby','').split())

def main():
    seal=json.loads(fixed(N/'INITIAL_SEAL.json',{'bytes':1872,'SHA256':'735fd6eeaab63eaec4ccbd181b7f36a85e915de3d633490f89b2159ef3007df4'}))
    im=json.loads(fixed(N/'INITIAL_MANIFEST.json',{'bytes':1857,'SHA256':'8579f0cdd37ee14859a6f316ae0690d0ddb7d9e0a1bb4e013a8733db5e2d48c0'}))
    for row in im['payloads']:fixed(N/row['path'],row)
    assert seal['incidental_native_archived_support_opinion_exposure_before_INITIAL'] is True
    assert seal['pre_support_opinion_independence_claim'] is False
    intake=json.loads(fixed(N/'AUTHORITY_INTAKE.json',{'bytes':1635,'SHA256':'2593d1364d24855b9df970cf8f2e0171c5c49aaf6f1d088ea33d1bb215881935'}))
    for name in ('root_clearance','root_review'):
        row=intake[name];fixed(Path(row['path']),row)
    sources=load(N/'SOURCES.json')
    for name in ('native_record','native_files_endpoint','native_ACQUIRED','source_custody_FINAL','source_custody_MANIFEST','controlling_TeX'):
        row=sources[name];fixed(Path(row['path']),row)
    row=sources['rights_basis']['file'];fixed(Path(row['path']),row)
    assert sources['rights_basis']['exact_statement']=='Paper and authored supplementary materials: CC BY4.0.'
    final_bytes=fixed(R/'FINAL.json',{'bytes':5128,'SHA256':'88233379d02e3e7bad965ccab40e9c164fd71e04318849aab1798099e7207132'})
    final=json.loads(final_bytes)
    manifest=json.loads(fixed(R/'OWNED_MANIFEST.json',{'bytes':5268,'SHA256':'b63d20289ca29ba28582aaaa255934090491d04a8b5f414c47467fe15f4cd08b'}))
    assert len(manifest['files'])==27
    assert {str(q.relative_to(R)) for q in R.rglob('*') if q.is_file()}=={x['path'] for x in manifest['files']}|{'OWNED_MANIFEST.json','FINAL.json'}
    assert sorted(str(q.relative_to(R)) for q in R.rglob('*') if q.is_dir())==['preview','renders']
    assert not any(q.is_symlink() for q in R.rglob('*'))
    for row in manifest['files']:fixed(R/row['path'],row)
    page_bytes=fixed(R/'preview/index.html',final['whole_page']);page=page_bytes.decode('utf-8')
    main_html=one(page,r'<main id="main">[\s\S]*?</main>')
    head=one(page,r'<head>[\s\S]*?</head>')
    assert pin(main_html.encode())==final['whole_MAIN']
    assert pin(head.encode())==final['whole_head']
    model_bytes=fixed(R/'PAGE_MODEL.json',final['page_model']);model=json.loads(model_bytes)
    native=sources['native_record_original_object'];meta=native['metadata']
    assert model['native_metadata_original']==meta
    assert model['native_Description_archived_not_duplicate_visible']==meta['description']
    assert model['native_record_files']==native['files']
    assert model['native_files_response']==sources['native_files_endpoint_original_object']
    assert model['native_version']==model['printed_version']==meta['version']=='1.0.0'
    assert model['declared_publication_date']==meta['publication_date']=='2026-10-12'
    assert model['native_created']==native['created'] and model['native_updated']==native['updated']
    abstract=sources['full_original_abstract_plain_math_serialization']
    # Only spaces around the literal source abstract's annulus inequalities differ.
    expected=abstract.replace('1<|z|<e','1 < |z| < e')
    visible=unescape(one(page,r'<section id="original-abstract"[\s\S]*?<p>([\s\S]*?)</p>'))
    tags=Tags();tags.feed(page)
    article=json.loads(one(page,r'<script type="application/ld\+json">([\s\S]*?)</script>'))
    assert visible==tags.meta['DC.description']==article['abstract']==model['abstract']==expected
    assert len(tags.ids)==len(set(tags.ids)) and set(tags.labels)<=set(tags.ids)
    assert page.count('<main ')==page.count('<h1>')==1
    assert tags.meta['robots']=='noindex, nofollow, noarchive'
    assert not any(x.get('rel')=='canonical' for x in tags.links)
    assert tags.meta['citation_title']==meta['title']
    assert tags.meta['citation_author_orcid']=='https://orcid.org/0009-0001-9320-500X'
    assert tags.meta['citation_publication_date']=='2026/10/12' and tags.meta['citation_version']=='1.0.0'
    assert tags.meta['citation_doi']==native['doi']
    assert article['version']=='1.0.0' and article['datePublished']=='2026-10-12'
    assert article['name']==meta['title'] and article['identifier']['value']==native['doi']
    assert article['license']=='https://creativecommons.org/licenses/by/4.0/'
    assert 'record was created on 13 October 2026 UTC' in main_html
    assert 'not a separate certification of when it first became publicly visible' in main_html
    order=[x['key'] for x in native['files']]
    downloads=one(main_html,r'<ol id="native-downloads">([\s\S]*?)</ol>')
    assert re.findall(r'<a href="([^"]+)" download>',downloads)==order
    assert [x['name'] for x in article['encoding']]==order
    asset_results=[]
    for source,encoded in zip(sources['native_assets_in_original_order'],article['encoding']):
        original=source['native_file_object'];name=original['key']
        data=fixed(Path(source['path']),source)
        assert (R/'preview'/name).read_bytes()==data
        assert hashlib.md5(data).hexdigest()==original['checksum'].removeprefix('md5:')
        assert encoded['contentUrl']==name and encoded['sameAs']==original['links']['self']
        asset_results.append({'name':name,**pin(data),'native_MD5':original['checksum']})
    pdf=order[0]
    assert tags.meta['citation_pdf_url']==pdf and 'src="'+pdf+'#view=FitH"' in main_html
    bib=fixed(R/'preview/citation.bib',final['BibTeX']).decode('utf-8')
    title=one(bib,r'  title = \{([^\n]+)\},')
    assert title.replace('{','').replace('}','')==meta['title']
    assert native['doi'] in bib and 'version = {1.0.0}' in bib
    assert 'Declared publication date 12 October 2026; record created 13 October 2026 UTC.' in bib
    assert model['rights']['MIT_not_inferred'] is True and not re.search(r'\bMIT\b',main_html)
    for text in ('a = e<sup>1/2</sup>','ξ = −1','h(a) ≤ 1','K<sub>ξ</sub>(a) = 1','for every z ∈ U ∖ {a}','does not exclude isolated contact farther away','every kernel or every annulus','p(x, t) = sin(πx) / [2(cosh(πt) − cos(πx))]','K(x, y) = P(x, y) / P(A)','including tangential approaches','1 ± (x − 1/2)','1 ± b sin(y) cosh(x − 1/2)','0 &lt; c &lt; 8/83 &lt; 1/10','b &gt; 1/4','&gt; |d|/10','does not assume that the envelope is smooth','equality <em>along</em> a Green line','Arsove and Johnson','Köhn','does not yield the smooth-annulus theorem','No first historical resolution','authored supplementary materials use','Cited third-party works retain their own rights.','unrefereed','no completed human peer review or formal proof-assistant certification','actual scholarly contributions'):
        assert text in main_html,text
    assert 'Original Zenodo description' not in page and 'native-description' not in tags.ids
    receipt=json.loads(fixed(R/'RENDER_RECEIPT.json',final['render']['receipt']))
    diagnostics=receipt['diagnostics']
    assert receipt['explicit_render_invocations']==1 and final['render']['exit']==0
    assert len(receipt['captures'])==6
    for row in receipt['captures']:fixed(R/row['path'],row)
    assert len(diagnostics['nonlocal_page_routes_aborted'])==len(diagnostics['console_errors'])==len(diagnostics['failed_requests'])==12
    assert diagnostics['page_errors']==[]
    assert all(x.startswith('chrome://resources/') for x in diagnostics['nonlocal_page_routes_aborted'])
    assert all(x['url'].startswith('chrome://resources/') for x in diagnostics['failed_requests'])
    assert final['render']['HTTP_HTTPS_page_route_entries_observed']==0
    assert final['render']['PDF_iframe_blank_in_saved_full_views'] is True
    assert final['render']['actual_embedded_PDF_display_certified'] is False
    for key in ('canonical_url','base_url','production_url','AA','follow_up'):assert model[key] is final[key] is None
    assert model['publication_authority'] is final['publication_authority'] is False
    print(json.dumps({'status':'PASS_INFORMED_COPY_FIDELITY_WITH_HEADLESS_PDF_LIMITATION','writer_FINAL':pin(final_bytes),'writer_packet':[29,2],'whole_page':pin(page_bytes),'whole_MAIN':pin(main_html.encode()),'whole_head':pin(head.encode()),'page_model':pin(model_bytes),'full_abstract_visible_JSONLD_DC_exact_content':True,'only_source_abstract_serialization_difference':'spaces around 1 < |z| < e','native_metadata_whole_Description_and_file_objects_exact':True,'version_dates_CC_BY_rights_scope_credit_status_fidelity':True,'native_assets_in_order':asset_results,'BibTeX':final['BibTeX'],'all_eleven_own_INITIAL_files_unchanged':True,'incidental_archived_support_opinion_exposure_before_INITIAL_disclosed':True,'pre_support_opinion_independence_claim':False,'saved_writer_HTML_images_personally_viewed':6,'writer_render_exit':0,'blocked_chrome_resource_failures':12,'console_errors':12,'page_errors':0,'HTTP_HTTPS_page_route_entries_observed':0,'saved_embedded_PDF_frames':'blank; no actual native or live display certification','new_HTML_render_browser_server_network_science_old_or_writer_helper_execution':False,'publication_authority':False},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
