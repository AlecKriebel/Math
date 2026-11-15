"""New-only falsification controls; all faults are independent in-memory copies.

No pristine page/source is ever edited. The exact mutant hash, failed checks and
edit recipe are retained in stdout for reproducibility under normal and -O.
"""
from six_common import *
from six_source import load_bundles,native_assets,validate_transports,validate_authorities,_whole_source_objects
from six_body_contract import check_page
from six_presentation import presentation
from verify_stage_read_only import check_overlays
from html import escape as h
from datetime import date
import argparse,copy

def replace(s,a,b):
    require(a in s,'fault_anchor_present:'+a[:80]);return s.replace(a,b,1)
def schema_fault(s,edit):
    m=re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)',s,re.S);require(m is not None,'actual_schema_anchor')
    obj=json.loads(m.group(2));edit(obj);return s[:m.start(2)]+json.dumps(obj,ensure_ascii=False).replace('<','\\u003c')+s[m.end(2):]

def run(stage,build_date):
    stage=safe_output(stage);bundles=load_bundles();frozen=load(OWN/'FROZEN_INPUT_SET.json');base=load(OWN/'FRESH_BASELINE.json');old={x['path']:x for x in base['public_files']}
    original={str(p.relative_to(stage)):bind(p) for p in stage.rglob('*') if p.is_file()};cases=[];positives=[]
    index=(stage/'research/index.html').read_bytes();sitemap=(stage/'research/sitemap.xml').read_bytes()
    for bundle in bundles:
        rid=bundle['rid'];c=bundle['c'];v=presentation(bundle);folder=stage/'research'/c['slug'];files={p.name:p.read_bytes() for p in folder.iterdir() if p.is_file()};text=files['index.html'].decode()
        pristine=check_page(bundle,files['index.html'],files,index_bytes=index,sitemap_bytes=sitemap,build_date=build_date)
        require(all(pristine.values()),'genuine_pristine_positive:'+rid);positives.append({'rid':rid,'checks':len(pristine),'all_passed':True})
        mutations={}
        def add(name,a,b):mutations[name]=(replace(text,a,b),None)
        add('changed_h1_claim','<h1><a href="/research/'+c['slug']+'/">'+h(c['title']),'<h1><a href="/research/'+c['slug']+'/">Changed claim')
        add('wrong_self_canonical','rel="canonical" href="https://aleckriebel.com/research/'+c['slug']+'/"','rel="canonical" href="https://example.org/unrelated/"')
        add('wrong_HTML_language','<html lang="en">','<html lang="xx">')
        add('wrong_viewport','width=device-width, initial-scale=1','width=1200, initial-scale=1')
        add('wrong_description','name="description" content="'+h(c['description'])+'"','name="description" content="Unapproved summary"')
        add('wrong_citation_DOI','name="citation_doi" content="'+c['doi']+'"','name="citation_doi" content="10.5281/zenodo.1"')
        add('wrong_citation_ORCID','name="citation_author_orcid" content="0009-0001-9320-500X"','name="citation_author_orcid" content="0000-0000-0000-0000"')
        add('wrong_citation_date','name="citation_publication_date" content="'+c['publication_date'].replace('-','/')+'"','name="citation_publication_date" content="2099/01/01"')
        add('wrong_citation_PDF','name="citation_pdf_url" content="https://aleckriebel.com/research/'+c['slug']+'/'+c['pdf_filename']+'"','name="citation_pdf_url" content="https://example.org/unrelated.pdf"')
        add('wrong_named_Research_navigation','href="/research/">Research</a>','href="/blog/">Research</a>')
        add('wrong_visible_time_attribute','<time datetime="'+c['publication_date']+'">','<time datetime="2099-01-01">')
        add('changed_visible_edition',' · '+h(c['edition_label'])+' · ',' · Unapproved edition · ')
        add('truncated_original_abstract','<section id="abstract"><h2>'+h(c['abstract_heading'])+'</h2><p>'+h(c['abstract'])+'</p>','<section id="abstract"><h2>'+h(c['abstract_heading'])+'</h2><p>'+h(c['abstract'][:-40])+'</p>')
        for section,key in [('plain-language','plain_language'),('result','result'),('proof','why_it_works'),('limits','limitations')]:
            add('removed_nonleading_'+section,'<p>'+h(c[key][-1])+'</p>','<p>Qualification omitted.</p>')
        add('weakened_AI_status','<p>'+h(c['ai_disclosure'])+'</p>','<p>Peer reviewed.</p>')
        add('changed_full_status','<p>'+h(c['status'])+'</p>','<p>Published theorem.</p>')
        add('changed_collaboration','<p>'+h(c['collaboration'])+'</p>','<p>Endorsement is sufficient for authorship.</p>')
        add('lost_nonleading_background_credit',h(c['background'][-1]['note']),'Prior credit omitted.')
        add('unapproved_extra_article_text','</article>','<p>Unapproved additional conclusion.</p></article>')
        add('raw_TeX_in_article','</article>','<p>\\(unapproved\\)</p></article>')
        add('wrong_reader_source','src="'+h(v['iframe_src'])+'"','src="wrong.pdf"')
        add('wrong_reader_title','title="'+h(v['iframe_title'])+'"','title="Partial reader"')
        iframe=re.search(r'<iframe.*?</iframe>',text,re.S).group()
        mutations['missing_reader']=(replace(text,iframe,''),None);mutations['extra_reader']=(replace(text,iframe,iframe+iframe),None)
        # Select actual link controls by their labels, avoiding accidental header matches.
        for name,x in [('lost_local_PDF_download',v['pdf_links'][1]),('wrong_original_PDF',v['pdf_links'][2]),('lost_complete_ZIP_download',v['zip_links'][0]),('wrong_original_ZIP',v['zip_links'][1]),('lost_BibTeX_download',v['bib_link'])]:
            pattern=r'<a href="'+re.escape(h(x['href']))+r'"[^>]*>'+re.escape(h(x['label']))+r'</a>';m=re.search(pattern,text);require(m is not None,'actual_download_control_anchor')
            if name.startswith('wrong_original'):bad=m.group().replace(h(x['href']),'https://example.org/unrelated',1)
            else:bad=re.sub(r' download(?:="[^"]*")?','',m.group(),count=1)
            mutations[name]=(replace(text,m.group(),bad),None)
        add('wrong_local_PDF_destination','href="'+h(c['pdf_filename'])+'"','href="../../wrong.pdf"')
        add('wrong_article_license_link','href="'+c['license_url']+'">CC BY 4.0','href="https://opensource.org/license/mit/">CC BY 4.0')
        if v['license_notices']:add('lost_record_specific_license_notice','<p>'+h(v['license_notices'][0])+'</p>','<p>All materials are MIT.</p>')
        if v['material_notes']:add('lost_complete_materials_qualification','<p>'+h(v['material_notes'][0])+'</p>','<p>Checks prove the theorem.</p>')
        for attr in ['hidden','inert','aria-hidden="true"','style="display:none"','class="hidden"']:
            add('hidden_article_'+attr.split('=')[0],'<article>','<article '+attr+'>')
        for wrapper in ['template','noscript','details','svg','math','iframe']:
            mutations['inert_outer_'+wrapper]=(text.replace('<body>','<'+wrapper+'><body>',1).replace('</body>','</body></'+wrapper+'>',1),None)
        add('head_inline_visibility_CSS','</head>','<style>article{display:none}</style></head>')
        add('body_active_script','</article>','<script>alert(1)</script></article>')
        add('duplicate_document_body','<body>','<body><body>')
        add('misnested_article','</article>','</main></article>')
        add('duplicate_attribute','<article>','<article hidden hidden>')
        add('extra_empty_paragraph','</article>','<p></p></article>')
        mutations['wrong_schema_date']=(schema_fault(text,lambda s:s['@graph'][1].__setitem__('datePublished','2099-01-01')),None)
        mutations['wrong_schema_version_type']=(schema_fault(text,lambda s:s['@graph'][1].__setitem__('version',1.0)),None)
        mutations['wrong_schema_license']=(schema_fault(text,lambda s:s['@graph'][1].__setitem__('license','https://opensource.org/license/mit/')),None)
        mutations['wrong_schema_asset']=(schema_fault(text,lambda s:s['@graph'][1]['encoding'].__setitem__('contentUrl','https://example.org/partial.pdf')),None)
        mutations['extra_schema_claim']=(schema_fault(text,lambda s:s['@graph'][1].__setitem__('unapprovedClaim','first worldwide')),None)
        mutations['wrong_explicit_build_date']=(schema_fault(text,lambda s:s['@graph'][0].__setitem__('dateModified','2099-01-01')),None)
        needle='"datePublished": "'+c['publication_date']+'"';mutations['duplicate_JSON_property']=(replace(text,needle,needle+', '+needle),None)
        for name in ['citation.bib',c['pdf_filename'],c['supplement_filename']]:
            changed=dict(files);data=changed[name];changed[name]=bytes([data[0]^1])+data[1:];mutations['changed_complete_bytes_'+name]=(text,changed)
        changed=dict(files);changed['extra.txt']=b'not authorized';mutations['extra_article_asset']=(text,changed)
        changed=dict(files);del changed[c['pdf_filename']];mutations['missing_native_PDF_asset']=(text,changed)
        for name,(html,changed) in mutations.items():
            encoded=html.encode();actual=dict(files if changed is None else changed);actual['index.html']=encoded
            result=check_page(bundle,encoded,actual,build_date=build_date);failed=[k for k,vv in result.items() if not vv]
            require(bool(failed),'genuine_semantic_fault_rejected:'+rid+':'+name)
            cases.append({'rid':rid,'family':'public_semantics','name':name,'mutant_HTML_sha256':sha(encoded),'rejected':True,'failed_checks':failed})
        # Actual native objects stay immutable; pure guards receive independent deep copies.
        spec=frozen['native_specs'][rid];ready=load(bundle['paper']/'sources/SOURCE_READY.json');api=load(bundle['paper']/'sources/record.raw.json');science=load(spec['whole_root_science']['path'])
        source_cases=[]
        def source_case(name,fn):
            try:fn()
            except (ValueError,KeyError,TypeError) as e:source_cases.append({'rid':rid,'family':'native_or_authority','name':name,'rejected':True,'exception_type':type(e).__name__,'reason':str(e)})
            else:raise RuntimeError('Native/authority fault accepted:'+rid+':'+name)
        rr=copy.deepcopy(ready);aa=copy.deepcopy(api);rr[spec['ready_array']].reverse();aa['files'].reverse();source_case('reordered_whole_native_assets',lambda:native_assets(rid,bundle['paper'],rr,aa,c,spec))
        rr=copy.deepcopy(ready);item=rr[spec['ready_array']][0];item[spec['digest_key']]='0'*64;source_case('wrong_native_digest',lambda:native_assets(rid,bundle['paper'],rr,api,c,spec))
        rr=copy.deepcopy(ready);item=rr[spec['ready_array']][0];item['path']=str(bundle['paper']/'sources'/api['files'][0]['key']) if rid=='23124601' else api['files'][0]['key'];source_case('native_path_kind_aliased',lambda:native_assets(rid,bundle['paper'],rr,api,c,spec))
        rr=copy.deepcopy(ready);rr['files']=rr.pop(spec['ready_array']);source_case('fabricated_common_source_array',lambda:native_assets(rid,bundle['paper'],rr,api,c,spec))
        rr=copy.deepcopy(ready);aa=copy.deepcopy(api);rr[spec['ready_array']][0][spec['asset_object_key']]['size']=True;aa['files'][0]['size']=True;source_case('boolean_native_size',lambda:native_assets(rid,bundle['paper'],rr,aa,c,spec))
        tr=copy.deepcopy(spec['transport_objects'])
        if len(tr)==1:tr[0].reverse()
        else:tr.reverse()
        source_case('reordered_native_transports',lambda:validate_transports(rid,bundle['paper'],tr,spec))
        tr=copy.deepcopy(spec['transport_objects']);tr[0]={'status':200};source_case('fabricated_universal_transport',lambda:validate_transports(rid,bundle['paper'],tr,spec))
        gg=copy.deepcopy(bundle['g']);gg['status']='PASS';source_case('coerced_generic_PASS',lambda:validate_authorities(rid,c,gg,science))
        gg=copy.deepcopy(bundle['g']);gg['canonical_url']='https://example.org/unverified';source_case('invented_canonical_gate',lambda:validate_authorities(rid,c,gg,science))
        gg=copy.deepcopy(bundle['g']);gg['browser_verified']=True;source_case('fabricated_browser_gate',lambda:validate_authorities(rid,c,gg,science))
        gg=copy.deepcopy(bundle['g']);role=next(iter(gg['reviews']));key='whole_original_custom_verdict' if rid=='23383952' else 'verdict_original' if rid=='23539734' else 'verdict';gg['reviews'][role][key]={'status':'PASS'};source_case('truncated_custom_family_verdict',lambda:validate_authorities(rid,c,gg,science))
        cases+=source_cases
    good=check_overlays(bundles,index,sitemap,build_date,old);require(all(good.values()),'genuine_overlay_positive')
    slugs=[b['c']['slug'] for b in bundles];urls=['https://aleckriebel.com/research/'+s+'/' for s in slugs]
    overlay_faults={
     'missing_new_visible_entry':(index.decode().replace('href="/research/'+slugs[-1]+'/"','href="/unrelated/"',1).encode(),sitemap),
     'changed_old_visible_entry':(index.decode().replace('PDF','Changed old PDF',1).encode(),sitemap),
     'changed_index_Research_metadata':(index.decode().replace('Alec Kriebel','Changed name',1).encode(),sitemap),
     'wrong_ItemList_count':(index.decode().replace('"numberOfItems": 78','"numberOfItems": 79',1).encode(),sitemap),
     'wrong_new_ItemList_URL':(index.decode().replace('"url": "'+urls[-1]+'"','"url": "https://example.org/unrelated/"',1).encode(),sitemap),
     'missing_new_sitemap_URL':(index,sitemap.decode().replace('<loc>'+urls[-1]+'</loc>','<loc>https://example.org/unrelated/</loc>',1).encode()),
     'wrong_sitemap_build_date':(index,sitemap.decode().replace('<lastmod>'+build_date+'</lastmod>','<lastmod>2099-01-01</lastmod>',1).encode()),
     'changed_old_sitemap_URL':(index,sitemap.decode().replace('<loc>https://aleckriebel.com/research/</loc>','<loc>https://example.org/old/</loc>',1).encode())}
    for name,(ix,sm) in overlay_faults.items():
        require(ix!=index or sm!=sitemap,'actual_overlay_mutation:'+name);r=check_overlays(bundles,ix,sm,build_date,old);failed=[k for k,v in r.items() if not v];require(failed,'genuine_overlay_rejection:'+name)
        cases.append({'family':'overlay','name':name,'rejected':True,'mutant_index_sha256':sha(ix),'mutant_sitemap_sha256':sha(sm),'failed_checks':failed})
    after={str(p.relative_to(stage)):bind(p) for p in stage.rglob('*') if p.is_file()};require(after==original,'pristine_tree_never_mutated')
    return {'status':'PASS','positives':positives,'overlay_positive_checks':len(good),'cases':cases,'rejected_faults':len(cases),'pristine_files_unchanged':len(original),'faults_are_independent_in_memory_copies':True,'source_or_stage_writes':0,'old_campaigns_replayed':0}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--stage-root',required=True,type=Path);p.add_argument('--build-date',required=True);a=p.parse_args();print(json.dumps(run(a.stage_root,a.build_date),sort_keys=True))
