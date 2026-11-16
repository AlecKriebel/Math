#!/usr/bin/env python3
"""One fixed stdout-only editorial data comparison; no project/helper execution."""
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
import hashlib
import json
import re
import stat

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
N=P/'verification/knudson-editorial-fact-sol-20261116'
R=P/'papers/22929556/reviews/editorial'

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
        self.meta={};self.links=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='meta':self.meta[d.get('name',d.get('property'))]=d.get('content')
        if 'id' in d:self.ids.append(d['id'])
        if tag=='link':self.links.append(d)

def main():
    fixed(N/'INITIAL_SEAL.json',{'bytes':1632,'SHA256':'d4751dd9ba6e6023033c4b6d8d895f94fbd14cc8655ee2ab2151d1772e57cdae'})
    im=json.loads(fixed(N/'INITIAL_MANIFEST.json',{'bytes':1504,'SHA256':'89361d6ee1e2e6566f26d9670447af9d1a151d9d83216ac8757117de74b78b01'}))
    for row in im['payloads']:fixed(N/row['path'],row)
    sources=load(N/'SOURCES.json')
    for name in ('native_record','native_files_endpoint','source_custody_FINAL','source_custody_MANIFEST','native_ACQUIRED','published_PDF','embedded_original_PDF','controlling_TeX','authored_rights'):
        row=sources[name];fixed(Path(row['path']),row)
    authority_path=P/'verification/root-clearance-22929556-20261116.json'
    authority_bytes=fixed(authority_path,{'bytes':1760,'SHA256':'e2caaafe00085906c4de7e50c3b6a80cafdeac5fc33463f1e59f4b323c28baef'})
    authority=json.loads(authority_bytes)
    for row in authority['authority']:fixed(P/row['path'],row)
    final_bytes=fixed(R/'FINAL.json',{'bytes':4468,'SHA256':'7e82e267f9208137789ab6e69c524f354e286808708b4cdc88ed36e4087678dc'})
    final=json.loads(final_bytes)
    manifest=json.loads(fixed(R/'OWNED_MANIFEST.json',final['manifest']))
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
    native=sources['native_record_original_object']
    assert model['native_metadata_original']==native['metadata']
    assert model['native_record_files']==native['files']
    assert model['native_files_response']==sources['native_files_endpoint_original_object']
    assert model['native_version_field']=={'present':False,'original_value':None}
    assert model['printed_version']=='1.0.1' and model['version_metadata_basis'].startswith('Printed manuscript only;')
    assert model['declared_publication_date']==native['metadata']['publication_date']=='2026-09-23'
    assert model['native_created']==native['created'] and model['native_updated']==native['updated']
    abstract=sources['full_original_abstract_plain']
    visible=unescape(one(page,r'<section id="original-abstract"[\s\S]*?<p>([\s\S]*?)</p>'))
    tags=Tags();tags.feed(page)
    article=json.loads(one(page,r'<script type="application/ld\+json">([\s\S]*?)</script>'))
    assert visible==tags.meta['DC.description']==article['abstract']==model['abstract']==abstract
    assert len(tags.ids)==len(set(tags.ids)) and page.count('<main ')==page.count('<h1>')==1
    assert tags.meta['robots']=='noindex, nofollow, noarchive'
    assert not any(x.get('rel')=='canonical' for x in tags.links)
    assert tags.meta['citation_title']==native['metadata']['title']
    assert tags.meta['citation_author_orcid']=='https://orcid.org/0009-0001-9320-500X'
    assert tags.meta['citation_publication_date']=='2026/09/23' and tags.meta['citation_version']=='1.0.1'
    assert tags.meta['citation_doi']==native['doi'] and tags.meta['citation_pdf_url']=='paper.pdf'
    assert article['version']=='1.0.1' and article['datePublished']=='2026-09-23'
    assert article['name']==native['metadata']['title'] and article['identifier']['value']==native['doi']
    assert article['license']=='https://creativecommons.org/licenses/by/4.0/'
    assert 'Printed version 1.0.1' in main_html and 'supplies no version field' in main_html
    assert 'was created on 24 September 2026 UTC' in main_html
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
    assert 'src="paper.pdf#view=FitH"' in main_html
    bib=fixed(R/'preview/citation.bib',final['BibTeX']).decode('utf-8')
    assert native['metadata']['title'] in bib and native['doi'] in bib and 'version = {1.0.1}' in bib
    assert 'Printed manuscript version 1.0.1; native Zenodo version field absent.' in bib
    for text in ('a, b, c, d, cd, bd, ac.','P = {(d, cd), (c, bd), (b, ac)}.','V<sub>P</sub> = {(d, cd)}.','zero gradient paths from ac to b','{ac, a, c}','same example works over every field','No minimality claim is made.','different matching, V′ = {(d, bd), (c, cd)}','ac → c → cd → d → bd → b','no counterexample claim against the ordered cancellation','bounded literature search does not establish first priority','Python and website code use the','MIT License','Cited third-party works retain their own rights.','prior AI-assisted work','unrefereed','formal proof-assistant certification','actual scholarly contributions'):
        assert text in main_html,text
    assert 'Original Zenodo description' not in page and 'native-description' not in tags.ids
    receipt=json.loads(fixed(R/'RENDER_RECEIPT.json',final['render']['receipt']))
    assert receipt['explicit_render_invocations']==receipt['explicit_render_exit']==1
    assert receipt['remote_page_requests'] is None and receipt['page_errors'] is None
    assert len(receipt['images'])==6
    for row in receipt['images']:fixed(R/row['path'],row)
    assert final['render']['actual_embedded_PDF_display_certified'] is False
    assert final['render']['diagnostic_arrays_persisted'] is False
    for key in ('canonical_url','base_url','production_url','AA','follow_up'):assert model[key] is final[key] is None
    assert model['publication_authority'] is final['publication_authority'] is False
    print(json.dumps({'status':'PASS_COPY_FIDELITY_WITH_SAVED_RENDER_LIMITATION','authority':pin(authority_bytes),'writer_FINAL':pin(final_bytes),'writer_packet':[29,2],'whole_page':pin(page_bytes),'whole_MAIN':pin(main_html.encode()),'whole_head':pin(head.encode()),'page_model':pin(model_bytes),'full_actual_abstract_visible_JSONLD_DC_exact':True,'native_metadata_whole_Description_files_original_values_exact':True,'native_version_absent_printed_1_0_1_and_date_distinctions_preserved':True,'native_assets_in_order':asset_results,'BibTeX':final['BibTeX'],'rights_split_credit_scope_status_collaboration_manually_read':True,'all_nine_own_INITIAL_files_unchanged':True,'saved_writer_HTML_images_personally_viewed':6,'render_run_exit':1,'remote_request_and_page_error_entries':'UNKNOWN: diagnostic arrays were not retained','embedded_PDF_in_saved_full_views':'blank; display not certified','new_render_browser_server_network_native_scientific_or_old_helper_execution':False,'publication_authority':False},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
