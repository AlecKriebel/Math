#!/usr/bin/env python3
"""Render this one private editorial proposal; copy four pinned original assets.

No scientific code imports, network, build, publication or outside writes.
Only --output normal or --output optimized is supported, both owned siblings.
"""
from pathlib import Path
import argparse,hashlib,html,json

R=Path(__file__).absolute().parent
def need(ok,why):
    if not ok:raise ValueError(why)
def pin(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',choices=['normal','optimized'],required=True);args=p.parse_args()
    contract=json.loads((R/'AUTHORING_INPUTS_SEAL.json').read_bytes())
    def owned(name):
        b=(R/name).read_bytes();need(pin(b)==contract['inputs'][name],'same-buffer input '+name);return b
    c=json.loads(owned('EDITORIAL_CONFIG.json'));copy=json.loads(owned('COPY.json'))
    need(c['record_id']==23205305 and c['promotion']['production_install_authority'] is False,'private exact target')
    e=lambda x:html.escape(str(x),quote=True)
    pub=c['publication'];doi='https://doi.org/'+pub['DOI'];orcid=c['author']['ORCID']
    base='https://github.com/openai/math/tree/'+pub['upstream_commit']+'/preprints/'
    refs=[('OpenAI, Hilbert’s tenth problem over the rational numbers, preprint (24 September 2026), pinned source.',base+'Hilberts-tenth-problem-over-the-rational-numbers-September-24-2026'),('OpenAI, A pointwise 2-converse for elliptic curves with rational two-torsion, preprint (24 September 2026), same pinned source.',base+'A-pointwise-2-converse-for-elliptic-curves-with-rational-two-torsion-September-24-2026'),('Bjorn Poonen, Existence of rational points on smooth projective varieties (2009).','https://doi.org/10.4171/JEMS/159'),('Lue Pan, The Fontaine–Mazur conjecture in the residually reducible case (2022), Theorem 1.0.4.','https://doi.org/10.1090/jams/991'),('Alexei N. Skorobogatov and Efthymios Sofos, Schinzel Hypothesis on average and rational points (2023), §1.2.','https://doi.org/10.1007/s00222-022-01153-6')]
    parts=['<main id="main">','<article>','<header>',f'<p><a href="/research/">Research</a></p>',f'<h1>{e(copy["title"])}</h1>',f'<p class="byline"><a href="{e(orcid)}">Alec Kriebel</a> · <time datetime="2026-10-06">6 October 2026</time> · Preprint</p>','</header>',f'<p class="intro">{e(copy["intro"])}</p>','<section aria-labelledby="readers-title">','<h2 id="readers-title">Read the original papers</h2>']
    for key,title in [('paper.pdf','Main paper'),('height-repair.pdf',copy['companion_title'])]:
        parts += [f'<h3>{e(title)}</h3>',f'<p><a href="{key}">Open PDF</a> · <a href="{key}" download>Download PDF</a></p>',f'<iframe src="{key}#view=FitH" title="{e(title)} — original deposited PDF" width="100%" height="660"></iframe>']
    parts += ['</section>','<section aria-labelledby="downloads-title">','<h2 id="downloads-title">Original files</h2>','<p>All four files below are unchanged from the deposit, listed in its original order.</p>','<ul class="native-downloads">']
    for a in pub['all_original_assets']:
        key=a['original_api_file_object']['key'];parts.append(f'<li><a href="{e(key)}" download data-native-asset="true">{e(key)}</a> <span class="bytes">({a["bytes"]:,} bytes)</span></li>')
    parts += ['</ul>',f'<p><a href="{e(pub["native_record"])}">Original Zenodo record</a> · <a href="{doi}">DOI: {e(pub["DOI"])}</a> · <a href="citation.bib" download>BibTeX</a></p>','</section>','<section id="printed-main-abstract">','<h2>Full printed abstract — main paper</h2>',f'<p>{e(copy["main_abstract"])}</p>','</section>','<section id="printed-companion-abstract">',f'<h2>Full printed abstract — {e(copy["companion_title"])}</h2>',f'<p>{e(copy["companion_abstract"])}</p>','<p>The pinned source cited as [1] is the first reference below.</p>','</section>']
    for section in copy['sections']:
        parts+=['<section>',f'<h2>{e(section["heading"])}</h2>']
        parts += [f'<p>{e(t)}</p>' for t in section['paragraphs']]
        if section.get('items'):parts+=['<ol>']+[f'<li>{e(t)}</li>' for t in section['items']]+['</ol>']
        parts+=['</section>']
    parts+=['<section id="native-description">','<h2>Original Zenodo description</h2>','<p>This separate deposit description is reproduced in full; it is distinct from the printed abstracts above.</p>',f'<blockquote><p>{e(copy["native_description"])}</p></blockquote>','</section>','<section>','<h2>References and source credit</h2>','<ol>']
    parts += [f'<li><a href="{e(url)}">{e(label)}</a></li>' for label,url in refs]
    parts += ['</ol>',f'<p>Pinned OpenAI source commit: <code>{pub["upstream_commit"]}</code>.</p>','</section>','<section id="rights">','<h2>Licensing</h2>',f'<p>{e(copy["rights_paragraph"])}</p>','<p><a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> · <a href="https://opensource.org/license/mit">MIT License</a></p>','</section>','</article>','</main>']
    main_html='\n'.join(parts)+'\n'
    seo=c['SEO_proposal']
    ld={'@context':'https://schema.org','@type':'ScholarlyArticle','@id':doi,'headline':copy['title'],'name':copy['title'],'author':{'@type':'Person','name':'Alec Kriebel','identifier':orcid},'datePublished':pub['datePublished'],'identifier':{'@type':'PropertyValue','propertyID':'DOI','value':pub['DOI']},'url':doi,'description':seo['description'],'abstract':copy['main_abstract'],'inLanguage':'en','license':'https://creativecommons.org/licenses/by/4.0/','isBasedOn':[refs[0][1],refs[1][1],refs[2][1]],'associatedMedia':[{'@type':'MediaObject','name':a['original_api_file_object']['key'],'contentUrl':a['original_api_file_object']['key'],'encodingFormat':a['whole_original_native_files_entry']['mimetype']} for a in pub['all_original_assets']]}
    head=['<meta charset="utf-8">','<meta name="viewport" content="width=device-width, initial-scale=1">',f'<title>{e(seo["title"])}</title>',f'<meta name="description" content="{e(seo["description"])}">',f'<meta name="robots" content="{e(c["promotion"]["robots"])}">',f'<meta name="keywords" content="{e(", ".join(seo["keywords"]))}">',f'<meta name="citation_title" content="{e(copy["title"])}">','<meta name="citation_author" content="Alec Kriebel">',f'<meta name="citation_author_orcid" content="{e(orcid)}">','<meta name="citation_publication_date" content="2026/10/06">',f'<meta name="citation_doi" content="{e(pub["DOI"])}">','<meta name="citation_pdf_url" content="paper.pdf">','<meta property="og:type" content="article">',f'<meta property="og:title" content="{e(copy["title"])}">',f'<meta property="og:description" content="{e(seo["description"])}">',f'<meta property="og:url" content="{doi}">','<meta name="twitter:card" content="summary">',f'<meta name="twitter:title" content="{e(copy["title"])}">',f'<meta name="twitter:description" content="{e(seo["description"])}">','<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+'</script>','<link rel="stylesheet" href="style.css">']
    head_html='\n'.join(head)+'\n'
    css='html{color-scheme:light}body{margin:0;background:#fff;color:#171717;font-family:Arial,Helvetica,sans-serif;font-size:18px;line-height:1.65}main{max-width:920px;margin:0 auto;padding:30px 24px 64px}h1{font-size:2.05rem;line-height:1.2;font-weight:600;letter-spacing:-.025em}h2{font-size:1.45rem;line-height:1.3;margin-top:2.1rem}h3{font-size:1.05rem;line-height:1.4}a{color:#174c8c;text-underline-offset:3px}p,li{overflow-wrap:anywhere}.byline,.bytes{color:#5b5b5b}.intro{font-size:1.12rem}iframe{display:block;border:1px solid #ddd;background:#fff;margin:12px 0 28px;box-sizing:border-box}blockquote{margin:1rem 0;padding:0 1.2rem;border-left:2px solid #ddd}code{font-size:.85em;overflow-wrap:anywhere}li{margin:.5rem 0}@media(max-width:600px){body{font-size:16px}main{padding:20px 16px 44px}h1{font-size:1.7rem}iframe{height:520px}}\n'
    bib='@misc{kriebel2026rationalpoint,\n  author = {Kriebel, Alec},\n  title = {Rational-point undecidability for smooth projective varieties over the rational numbers},\n  year = {2026},\n  month = oct,\n  doi = {10.5281/zenodo.23205305},\n  url = {https://doi.org/10.5281/zenodo.23205305},\n  note = {Preprint. Includes a conditional coefficient-prime height supplement.}\n}\n'
    md=['# '+copy['title'],copy['byline'],copy['intro'],'## Original readers','[Main paper](paper.pdf) · ['+copy['companion_title']+'](height-repair.pdf)','## Original files']
    md += ['- ['+a['original_api_file_object']['key']+']('+a['original_api_file_object']['key']+')' for a in pub['all_original_assets']]
    md += ['[Original Zenodo record]('+pub['native_record']+') · [DOI]('+doi+') · [BibTeX](citation.bib)','## Full printed abstract — main paper',copy['main_abstract'],'## Full printed abstract — '+copy['companion_title'],copy['companion_abstract'],'[1] refers to the first reference below.']
    for section in copy['sections']:
        md+=['## '+section['heading'],*section['paragraphs'],*['- '+x for x in section.get('items',[])]]
    md+=['## Original Zenodo description','Separate full deposit description; distinct from the printed abstracts.',copy['native_description'],'## References and source credit',*['- ['+label+']('+url+')' for label,url in refs],'Pinned OpenAI source commit: '+pub['upstream_commit'],'## Licensing',copy['rights_paragraph']]
    outputs={'PUBLIC_MAIN.html':main_html.encode(),'HEAD.html':head_html.encode(),'style.css':css.encode(),'citation.bib':bib.encode(),'COPY.md':('\n\n'.join(md)+'\n').encode(),'index.html':('<!doctype html>\n<html lang="en">\n<head>\n'+head_html+'</head>\n<body>\n'+main_html+'</body>\n</html>\n').encode()}
    for a in pub['all_original_assets']:
        b=Path(a['path']).read_bytes();need(pin(b)=={k:a[k] for k in ['bytes','SHA256']},'unchanged native asset');outputs[a['original_api_file_object']['key']]=b
    destination=R/args.output;destination.mkdir(exist_ok=False)
    for name,b in outputs.items():
        with (destination/name).open('xb') as f:f.write(b)
    print(json.dumps({'status':'PRIVATE_EDITORIAL_RENDERED','record_id':23205305,'output':args.output,'files':[{'name':n,**pin(b)} for n,b in sorted(outputs.items())],'production_authority':False},sort_keys=True))

if __name__=='__main__':main()
