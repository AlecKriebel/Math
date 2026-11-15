#!/usr/bin/env python3
"""One-shot private editorial preparation. Exclusive writes in this lane only.

This is not a source builder, science checker, deployment or promotion tool.
The separate verify_publication.py helper is the read-only closure interface.
"""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import html
import json
import re
import subprocess

P=Path(__file__).resolve().parent
B=P.parents[1]
CAT=B.parents[1]
S=B/'sources'


def h(body):return sha256(body).hexdigest()


def save(name,value):
    target=P/name
    with target.open('x') as out:
        out.write(json.dumps(value,indent=2,ensure_ascii=False)+'\n' if not isinstance(value,str) else value)


def original_abstract_text(tex):
    text=tex.replace(r'\operatorname{span}_{\Q}\{1,\ell,\ell^2\}', 'span_ℚ{1, ℓ, ℓ²}')
    text=text.replace(r'k\geq2','k ≥ 2').replace(r'0\leq n\leq2','0 ≤ n ≤ 2')
    text=text.replace('$','').replace('--','–')
    return ' '.join(text.split())


def main():
    stamp=datetime.now(timezone.utc).isoformat()
    ready=json.loads((S/'SOURCE_READY.json').read_bytes())
    authority_path=CAT/'verification/root-clearance-23430498-20261115.json'
    authority=json.loads(authority_path.read_bytes())
    record=json.loads((S/'record-attempt2.body').read_bytes())
    latest=json.loads((S/'latest.raw.json').read_bytes())
    versions=json.loads((S/'versions.page-001.raw.json').read_bytes())
    files=json.loads((S/'files.raw.json').read_bytes())
    transport=[{'filename':name,'whole_original_object':json.loads((S/name).read_bytes())}
               for name in ready['transport_files']]
    reviews={}
    for entry in authority['whole_literal_peer_verdicts_and_seal_bindings']:
        lane=entry['lane'];path=B/'reviews'/lane/'VERDICT.json'
        reviews[lane]={'path':str(path),'SHA256':h(path.read_bytes()),
                      'whole_literal_verdict':json.loads(path.read_bytes()),
                      'root_whole_peer_binding':entry}
    tex_path=Path(ready['controlling_TeX']['path']);tex=tex_path.read_text()
    abstract_tex=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1)
    abstract=original_abstract_text(abstract_tex)
    save('abstract-source.tex',abstract_tex)
    title=record['metadata']['title']
    slug='finite-type-invariants-free-exterior-string-links'
    proposed='https://aleckriebel.com/research/'+slug+'/'
    doi=record['doi'];record_url=record['links']['self_html']
    description='Low-degree restrictions and an exact order-seven invariant for ordinary rational string-link invariants on actual free exteriors.'
    plain=[
      'A string link is a collection of knotted strands in a cylinder, with labelled endpoints held fixed. Finite-type invariants are numerical probes of how those strands are knotted and linked.',
      'This note studies the links whose surrounding three-dimensional exterior has a free fundamental group. That simple group condition still allows information beyond the linking number: a component Conway coefficient cannot be recovered by combining the relevant Milnor invariants with invariants that vanish on this whole locus.',
      'Through order two, an ordinary rational invariant that vanishes on every such free exterior must be the zero invariant. On two strands, an existential order-seven invariant behaves differently: it is nonzero as an invariant but vanishes on every free exterior.'
    ]
    definitions=[
      'The category is smooth, ordered and labelled string links with fixed boundary and standard endpoint collars. Strands are oriented from bottom to top; upward orientation does not require height monotonicity. No strand framing is specified. Invariants are ℚ-valued and ordinary finite type, using both self-crossings and mixed crossings.',
      'Let 𝓥ₙ(k) be the space of invariants of order at most n, including constants, and let 𝓕ₖ consist of links whose actual three-dimensional exterior group is abstractly the free group F_k. No preferred-meridian-basis condition is imposed. Define 𝓝ₙ(k) = {v ∈ 𝓥ₙ(k) : v(L) = 0 for every L ∈ 𝓕ₖ}.',
      'Let 𝓜ₙ(k) = 𝓥ₙ(k) ∩ ℚ[μ_I : I any multi-index]. This is the intersection with the entire algebra of finite polynomials in based Milnor invariants, allowing repeated indices, arbitrary lengths and cancellations in a polynomial presentation.'
    ]
    result=[
      'For two strands, with ℓ = μ₁₂ = linking number, the recalled filtered Habegger–Masbaum corollary gives 𝓜₂(2) = span_ℚ{1, ℓ, ℓ²}. If a₁ is the Conway z² coefficient of the first individually closed strand, then a₁ ∉ 𝓜₂(2) + 𝓝₂(2). Thus the universal affirmative spanning assertion fails at (k,n) = (2,2).',
      'For every k ≥ 2 and every 0 ≤ n ≤ 2, 𝓝ₙ(k) = 0.',
      'There exists a nonzero rational invariant in 𝓝₇(2) of exact ordinary order seven. Consequently 𝓝ₙ(2) ≠ 0 for every n ≥ 7; the same invariant supplies these inclusions.'
    ]
    why=[
      'Published classification results describe all order-at-most-two invariants. Known free tangles, pure braids and disk-separated insertions isolate their coefficients, while filtered concordance results control the entire Milnor-algebra intersection.',
      'For two free-exterior strands, the exterior is a genus-two handlebody. Classical hyperelliptic symmetry, with the full boundary marking and collars respected, supplies simultaneous strand reversal. Antisymmetrizing the prior ordinary Duzhin–Karev orientation detector then gives the order-seven vanishing invariant.'
    ]
    limitations=[
      'The order-seven invariant is existential and noncanonical. The note does not supply a canonical evaluator or a nonzero value on a named nonsingular string link; its diagram-weight calculation is not such a link evaluation.',
      'The result does not determine orders three through six, the least positive kernel order, higher-strand higher-order kernels, or a general higher-order spanning classification. Failure of spanning at order two alone does not establish failure at larger order bounds.',
      'Only disk-separated insertion is used for the free-locus construction. Arbitrary stacking or deletion of strands is not asserted to preserve the free-exterior condition. The theorem remains in the stated ordinary, unframed, smooth, rational category.',
      'Historical priority of the combined free-exterior applications is undetermined. The older Morimoto and Li free-tangle papers remain unresolved priority comparisons. No worldwide firstness or current worldwide openness is claimed.'
    ]
    background=[
      'The questions come from Stanford’s Question 2.13 in Ohtsuki’s Problems on invariants of knots and 3-manifolds. The note gives the three stated restricted applications rather than a general classification.',
      'Habegger–Masbaum supply the filtered Milnor/concordance input, with Casson’s concordance attribution through the inspected primary interfaces. Meilhan supplies the complete ordinary order-two classification, and Meilhan–Yasuhara give the relevant Milnor-invariant context.',
      'Nogueira’s known free tangles and Kauffman–Lambropoulou’s rational-tangle geometry supply the geometric examples. The torus-knot Conway coefficients are credited to Alvarez–Labastida through Willerton.',
      'The genus-two argument uses classical Bleiler–Moriah context, Rubinstein–Scharlemann and Bruno–Mecchia symmetry, and Hatcher’s relative-ball theorem. Duzhin–Karev supply the prior ordinary orientation detector; the seven-wheel is credited to Bar-Natan following their journal proof.'
    ]
    collaboration='Independent verification of the marked topology, a well-supported primary-source comparison, or substantive development of a journal submission would be useful contributions. Any collaboration and authorship would be based on the contributions actually made.'
    ai='Extensive AI assistance was used in developing, checking, sourcing and writing this unrefereed application note. Internal AI reviews are not human peer review or formal proof certification.'
    references=[
      ('Stanford’s question in Ohtsuki’s problem collection','https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf'),
      ('Habegger–Masbaum: The Kontsevich integral and Milnor’s invariants','https://webusers.imj-prg.fr/~gregor.masbaum/K39.ps.gz'),
      ('Meilhan: On Vassiliev invariants of order two for string links','https://arxiv.org/pdf/math/0402036v2'),
      ('Meilhan–Yasuhara: Characterization of finite type string link invariants of degree < 5','https://arxiv.org/pdf/0904.1527v1'),
      ('Nogueira: the free-tangle appendix and original artwork','https://www.mat.uc.pt/preprints/ps/p1409.pdf'),
      ('Kauffman–Lambropoulou: On the Classification of Rational Knots','https://arxiv.org/pdf/math/0212011v2'),
      ('Willerton: On the first two Vassiliev invariants','https://arxiv.org/pdf/math/0104061v1'),
      ('Bar-Natan: Vassiliev homotopy string link invariants','https://www.math.toronto.edu/drorbn/papers/homotopy/homotopy.pdf'),
      ('Duzhin–Karev: Detecting the orientation of long links by finite type invariants','https://arxiv.org/pdf/math/0507015v5'),
      ('Duzhin–Karev: journal article','https://doi.org/10.1007/s10688-007-0018-7'),
      ('Rubinstein–Scharlemann: Genus two Heegaard splittings of orientable three-manifolds','https://msp.org/gtm/1999/02/gtm-1999-02-024p.pdf'),
      ('Bruno–Mecchia: On quotient orbifolds of hyperbolic 3-manifolds of genus two','https://rendiconti.dmi.units.it/volumi/46/014.pdf'),
      ('Hatcher: A proof of the Smale Conjecture','https://pi.math.cornell.edu/~hatcher/Papers/SmaleConjecture.pdf'),
      ('Morimoto: older priority lead','https://doi.org/10.1090/S0002-9939-1995-1317043-4'),
      ('Li: older priority lead','https://doi.org/10.1142/S021821650900735X')
    ]
    assets=ready['all_native_assets_in_original_order']
    for asset in assets:
        filename=asset['original_api_file_object']['key'];target=P/'preview/assets'/filename
        body=Path(asset['path']).read_bytes()
        if h(body)!=asset['SHA256']:raise ValueError('frozen asset identity')
        with target.open('xb') as out:out.write(body)
    zip_name=assets[0]['original_api_file_object']['key'];pdf_name=assets[1]['original_api_file_object']['key']
    pdf_url=assets[1]['original_api_file_object']['links']['self']
    gates={k:False for k in ['production_integration_authorized','publication_clearance','ready_to_publish','rendered_copy_verified','local_http_verified','deployed','live_verified','browser_verified','native_verified','canonical_verified']}
    nulls={'canonical_url':None,'native_sheet_aa_url':None,'AA':None}
    binding={'record_id':record['id'],'concept_record_id':record['conceptrecid'],'record_url':record_url,
      'doi':doi,'concept_doi':record['conceptdoi'],'version':'1.0','manuscript_version':'1.0',
      'manuscript_date':'2026-10-13','zenodo_publication_date':'2026-10-13',
      'record_created_utc':record['created'],'record_updated_utc':record['updated'],
      'whole_original_source_ready':ready,'source_ready_sha256':h((S/'SOURCE_READY.json').read_bytes()),
      'whole_native_record':record,'whole_native_latest_record':latest,'whole_native_versions':versions,
      'whole_native_files_object':files,'whole_original_native_transport_objects':transport,
      'all_assets_in_original_order':assets,'source_tex_path':str(tex_path),'source_tex_sha256':h(tex_path.read_bytes()),
      'abstract_source':'complete actual published manuscript abstract; controlling TeX',
      'abstract_tex':abstract_tex,'abstract_tex_sha256':h(abstract_tex.encode()),
      'abstract_normalization':'all original words retained; whitespace flattened, TeX delimiters removed and displayed mathematics/dashes formatted as Unicode',
      'pdf_sha256':assets[1]['SHA256'],'supplement_sha256':assets[0]['SHA256'],
      'archive_payload_occurrences':194,'expanded_bytes':1866967,
      'embedded_reader_pdf':str(P/'preview/assets'/pdf_name),'embedded_reader_byte_identical':True,
      'license_original_object':record['metadata']['license'],'license_text_source':str(tex_path),
      'license_text_original':'CC BY 4.0 for this authored manuscript and authored supporting records; cited third-party source bodies and artwork are excluded.',
      'code_license':'CC BY 4.0','separate_MIT_license_asserted':False,
      'receipt_schema_note':ready['failure_provenance']}
    review={'prepared_utc':stamp,'completion_percent':100,'editorial_only':True,'scientific_clearance_received':True,
      'root_clearance_file':str(authority_path),'root_clearance_sha256':h(authority_path.read_bytes()),
      'scientific_status':authority['status'],'whole_original_review_verdicts':reviews,
      'root_review_file':str(CAT/authority['root_review']['path']),'root_review_sha256':authority['root_review']['sha256'],
      'historical_literal_flags_preserved':True,'publication_state':'PRIVATE_EDITORIAL_PREPARED_UNPUBLISHED',
      'editorial_author_prior_role':'same agent authored sealed adversarial115; informed editorial work, not a new blind scientific review',
      'root_copy_and_config_adoption_required':True,**gates,**nulls}
    config={'title':title,'slug':slug,'description':description,'abstract':abstract,'abstract_heading':'Original abstract',
      'abstract_is_original':True,'plain_language':plain,'definitions':definitions,'result':result,'why_it_works':why,
      'limitations':limitations,'background':background,'collaboration':collaboration,'follow_up':None,
      'followup_rationale':'Default null; missing degrees3–6 alone do not establish a novel substantial research program.',
      'publication_date':'2026-10-13','version':'1.0','doi':doi,'author':'Alec Kriebel',
      'orcid':'https://orcid.org/0009-0001-9320-500X','pdf_filename':pdf_name,'pdf_pages':13,
      'reader_intro':'Read the complete thirteen-page published version 1.0 in the PDF reader.',
      'supplement_filename':zip_name,'supplement_label':'Complete original source and audit kit',
      'additional_assets':[],'related_resources':references,'status':'Unrefereed preprint','ai_disclosure':ai,
      'license':'CC BY 4.0','license_url':'https://creativecommons.org/licenses/by/4.0/','code_license':'CC BY 4.0',
      'publication_date_label':'Original publication date','edition_label':'Version','citation_edition_label':'Version',
      'edition_note':'The manuscript and declared original publication date are 13 October 2026; the Zenodo record was created 17 October 2026.',
      'canonical_url':None,'proposed_canonical_url':proposed,'AA':None,
      'keywords':['finite-type invariants','string links','free exterior groups','free tangles','Milnor invariants','Conway polynomial','genus-two symmetry','order seven'],
      'seo':{'title':'Finite-type invariants of free-exterior string links | Alec Kriebel','description':description,
             'canonical_url':None,'proposed_canonical_url':proposed,'open_graph_url':None,
             'robots_after_authorized_publication':'index,follow','robots_private_preview':'noindex,nofollow'},
      'source_binding':binding,'review_metadata':review}
    save('publication.json',config)
    promotion={'record_id':'23430498','status':'PRIVATE_EDITORIAL_PREPARED_UNPUBLISHED','scientific_status':authority['status'],
      'disposition_by':'root scientific authority; private editorial preparation only','created_utc':stamp,
      'whole_original_mathematical_scope_supported':True,'approved_scope':result,
      'root_clearance_file':str(authority_path),'root_clearance_sha256':h(authority_path.read_bytes()),
      'whole_root_scientific_clearance_record':authority,'root_review_file':review['root_review_file'],
      'root_review_sha256':review['root_review_sha256'],'reviews':reviews,'whole_original_source_ready':ready,
      'source_ready_sha256':binding['source_ready_sha256'],'whole_original_native_record':record,
      'whole_original_native_latest_record':latest,'whole_original_native_versions':versions,
      'whole_original_native_files_object':files,'whole_original_native_transport_objects':transport,
      'pdf_sha256':assets[1]['SHA256'],'supplement_sha256':assets[0]['SHA256'],
      'publication_sha256':h((P/'publication.json').read_bytes()),'source_repair':False,'narrowed_replacement':False,
      'follow_up':None,'human_peer_review':False,'formal_certification':False,'proposed_canonical_url':proposed,
      'all203_complete':False,'root_copy_and_config_adoption_required':True,**gates,**nulls}
    save('promotion.json',promotion)
    save('article-config.json',{'schema':'private-article-adoption-v1','publication_config':'publication.json',
      'publication_sha256':h((P/'publication.json').read_bytes()),'promotion_config':'promotion.json',
      'promotion_sha256':h((P/'promotion.json').read_bytes()),'public_copy':'PUBLIC_COPY.md',
      'private_static_preview':'preview/index.html','root_adoption_required':True,
      'proposed_slug':slug,'proposed_url':proposed,'canonical_url':None,'AA':None,
      'style':{'background':'white','font':'Arial, Helvetica, sans-serif','layout':'single readable column','external_runtime_scripts':[]},
      'publication_authorized':False})
    bib='@misc{kriebel2026freeexterior,\n  author = {Kriebel, Alec},\n  title = {'+title+'},\n  year = {2026},\n  month = {oct},\n  date = {2026-10-13},\n  version = {1.0},\n  publisher = {Zenodo},\n  doi = {'+doi+'},\n  url = {https://doi.org/'+doi+'}\n}\n'
    save('citation.bib',bib)
    schema={'@context':'https://schema.org','@type':'ScholarlyArticle','@id':'https://doi.org/'+doi,
      'headline':title,'name':title,'description':description,'abstract':abstract,
      'author':{'@type':'Person','name':'Alec Kriebel','sameAs':config['orcid']},
      'datePublished':'2026-10-13','version':'1.0','creativeWorkStatus':'Unrefereed preprint',
      'isAccessibleForFree':True,'license':config['license_url'],'url':record_url,
      'identifier':{'@type':'PropertyValue','propertyID':'DOI','value':doi},
      'encoding':[{'@type':'MediaObject','contentUrl':x['original_api_file_object']['links']['self'],
                   'encodingFormat':'application/zip' if i==0 else 'application/pdf'} for i,x in enumerate(assets)],
      'citation':[{'@type':'ScholarlyArticle','name':label,'url':url} for label,url in references]}
    save('SCHOLARLY_METADATA.json',{'scholarly_article':schema,'citation_meta':{
      'citation_title':title,'citation_author':'Alec Kriebel','citation_publication_date':'2026/10/13',
      'citation_doi':doi,'citation_pdf_url':pdf_url,'citation_publisher':'Zenodo','citation_version':'1.0'},
      'canonical_url':None,'proposed_canonical_url':proposed,'private_preview_robots':'noindex,nofollow'})
    md='# '+title+'\n\nAlec Kriebel · [ORCID]('+config['orcid']+')\n\nOriginal publication date: 13 October 2026 · Version 1.0 · Unrefereed preprint\n\n'
    for heading,paragraphs in [('Original abstract',[abstract]),('What this note shows',plain),('Setting and notation',definitions),('Full result',result),('How the argument works',why),('Important limits',limitations),('Prior work and credit',background)]:
        md+='## '+heading+'\n\n'
        md+='\n\n'.join((str(i+1)+'. '+x if heading=='Full result' else x) for i,x in enumerate(paragraphs))+'\n\n'
    md+='\n'.join('- ['+label+']('+url+')' for label,url in references)+'\n\n'
    md+='## Read the paper\n\n'+config['reader_intro']+'\n\n'
    md+='<iframe title="Complete published paper, thirteen pages" src="preview/assets/'+pdf_name+'#view=FitH" width="100%" height="860"></iframe>\n\n'
    md+='[Open the published PDF](preview/assets/'+pdf_name+') · [Download the PDF](preview/assets/'+pdf_name+') · [Zenodo record]('+record_url+')\n\n'
    md+='## Original materials\n\n- [Complete original source and audit kit](preview/assets/'+zip_name+')\n- [Published PDF](preview/assets/'+pdf_name+')\n\n'
    md+='The authored manuscript and authored supporting records are licensed [CC BY 4.0]('+config['license_url']+'). Cited third-party source bodies and artwork are excluded.\n\n'
    md+='## Citation\n\nAlec Kriebel. '+title+'. Version 1.0. Zenodo, 2026. [doi:'+doi+'](https://doi.org/'+doi+').\n\n[BibTeX](citation.bib)\n\n'
    md+='## Collaboration\n\n'+collaboration+'\n\n## AI use and review status\n\n'+ai+'\n'
    save('PUBLIC_COPY.md',md)
    esc=html.escape
    head='<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
    head+='<title>'+esc(config['seo']['title'])+'</title><meta name="description" content="'+esc(description,quote=True)+'">'
    head+='<meta name="robots" content="noindex,nofollow"><meta property="og:type" content="article">'
    for k,v in [('og:title',config['seo']['title']),('og:description',description)]:head+='<meta property="'+k+'" content="'+esc(v,quote=True)+'">'
    for k,v in json.loads((P/'SCHOLARLY_METADATA.json').read_text())['citation_meta'].items():head+='<meta name="'+k+'" content="'+esc(v,quote=True)+'">'
    head+='<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('</','<\\/')+'</script>'
    css='body{margin:0;background:#fff;color:#1c1c1c;font:18px/1.6 Arial,Helvetica,sans-serif}main{max-width:780px;margin:48px auto;padding:0 24px 64px}h1{font-size:40px;line-height:1.16;margin:28px 0 18px}h2{font-size:25px;line-height:1.25;margin:2em 0 .7em}a{color:#0645ad;text-decoration:underline}p{margin:0 0 1.1em}li{margin:.5em 0}.meta,nav{font-size:16px;color:#555}iframe{display:block;box-sizing:border-box;width:100%;height:860px;border:1px solid #ccc;margin:1.5em 0}li,p{overflow-wrap:anywhere}.skip{position:absolute;left:-10000px}.skip:focus{left:12px;top:12px}blockquote{margin-left:0}footer{margin-top:2em;font-size:16px}@media(max-width:600px){body{font-size:16px}main{margin:24px auto;padding:0 18px 48px}h1{font-size:30px}h2{font-size:23px}iframe{height:620px}}'
    body='<a class="skip" href="#main">Skip to article</a><main id="main"><nav aria-label="Site"><a href="/">Alec Kriebel</a> · <a href="/research/">Research</a></nav><article><header><h1>'+esc(title)+'</h1><p><a href="'+config['orcid']+'">Alec Kriebel · ORCID</a></p><p class="meta">Original publication date: <time datetime="2026-10-13">13 October 2026</time> · Version 1.0 · Unrefereed preprint</p></header>'
    for ident,heading,paragraphs in [('abstract','Original abstract',[abstract]),('explanation','What this note shows',plain),('setting','Setting and notation',definitions),('result','Full result',result),('argument','How the argument works',why),('limits','Important limits',limitations),('credit','Prior work and credit',background)]:
        body+='<section id="'+ident+'" aria-labelledby="'+ident+'-heading"><h2 id="'+ident+'-heading">'+heading+'</h2>'
        if ident=='result':body+='<ol>'+''.join('<li>'+esc(x)+'</li>' for x in paragraphs)+'</ol>'
        else:body+=''.join('<p>'+esc(x)+'</p>' for x in paragraphs)
        if ident=='credit':body+='<ul>'+''.join('<li><a href="'+esc(url,quote=True)+'">'+esc(label)+'</a></li>' for label,url in references)+'</ul>'
        body+='</section>'
    body+='<section id="reader" aria-labelledby="reader-heading"><h2 id="reader-heading">Read the paper</h2><p>'+config['reader_intro']+'</p><iframe title="Complete published paper, thirteen pages" src="assets/'+pdf_name+'#view=FitH"></iframe><p><a href="assets/'+pdf_name+'">Open the published PDF</a> · <a download href="assets/'+pdf_name+'">Download the PDF</a> · <a href="'+record_url+'">Zenodo record</a></p></section>'
    body+='<section id="materials"><h2>Original materials</h2><ul><li><a download href="assets/'+zip_name+'">Complete original source and audit kit</a></li><li><a download href="assets/'+pdf_name+'">Published PDF</a></li></ul><p>The authored manuscript and authored supporting records are licensed <a href="'+config['license_url']+'">CC BY 4.0</a>. Cited third-party source bodies and artwork are excluded.</p></section>'
    body+='<section id="citation"><h2>Citation</h2><p>Alec Kriebel. '+esc(title)+'. Version 1.0. Zenodo, 2026. <a href="https://doi.org/'+doi+'">doi:'+doi+'</a>.</p><p><a href="../citation.bib">BibTeX</a></p></section>'
    body+='<section id="collaboration"><h2>Collaboration</h2><p>'+esc(collaboration)+'</p></section><footer id="disclosure"><h2>AI use and review status</h2><p>'+esc(ai)+'</p></footer></article></main>'
    save('preview/index.html','<!doctype html><html lang="en"><head>'+head+'<style>'+css+'</style></head><body>'+body+'</body></html>\n')
    text=subprocess.run(['pdftotext','-layout',str(P/'preview/assets'/pdf_name),'-'],capture_output=True,timeout=30)
    if text.returncode:raise RuntimeError(text.stderr.decode())
    pages=text.stdout.decode().split('\f');pages=pages[:-1] if not pages[-1].strip() else pages
    if len(pages)!=13 or not all(len(x.strip())>100 for x in pages):raise ValueError('searchable complete PDF')
    save('PDF_SEARCHABILITY.json',{'UTC':stamp,'source_PDF_SHA256':assets[1]['SHA256'],'copied_PDF_SHA256':h((P/'preview/assets'/pdf_name).read_bytes()),'page_count':len(pages),'per_page_text_characters':[len(x.strip()) for x in pages],'extraction_exit_code':text.returncode,'stderr':text.stderr.decode(),'published_PDF_unchanged':True})
    print(json.dumps({'created':'private editorial configs, full public copy and static preview','abstract_words':len(abstract.split()),'native_asset_order':[x['original_api_file_object']['key'] for x in assets],'publication_SHA256':h((P/'publication.json').read_bytes()),'promotion_SHA256':h((P/'promotion.json').read_bytes())},indent=2))


if __name__=='__main__':main()
