#!/usr/bin/env python3
"""Private renderer for record23203732 only. No scientific code, network/build,
publication or outside writes. Two exclusive owned output destinations only.
"""
from pathlib import Path
from html.parser import HTMLParser
import argparse,hashlib,html,json
R=Path(__file__).absolute().parent
def need(ok,why):
    if not ok:raise ValueError(why)
def pin(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
class NativeHTML(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.depth=0
    def handle_starttag(self,t,a):need(t=='p' and a==[] and self.depth==0,'native description p-only');self.depth+=1
    def handle_endtag(self,t):need(t=='p' and self.depth==1,'native description balanced');self.depth-=1
    def handle_comment(self,t):raise ValueError('unexpected native HTML comment')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',choices=['normal','optimized'],required=True);args=ap.parse_args()
    inputs=json.loads((R/'AUTHORING_INPUTS_SEAL.json').read_bytes())['inputs']
    def load(n):
        b=(R/n).read_bytes();need(pin(b)==inputs[n],'same-buffer owned input '+n);return json.loads(b)
    c=load('EDITORIAL_CONFIG.json');copy=load('COPY.json');need(c['record_id']==23203732 and c['promotion']['production_install_authority'] is False,'exact private target')
    pub=c['publication'];esc=lambda x:html.escape(str(x),quote=True);doi='https://doi.org/'+pub['DOI'];orcid=c['author']['ORCID']
    safe=NativeHTML();safe.feed(copy['native_description_HTML']);need(safe.depth==0,'native HTML complete')
    refs=[('OpenAI, A group without fixed price, manuscript dated 5 October 2026, exact pinned source.','https://github.com/openai/math/blob/'+pub['upstream_commit']+'/preprints/A-group-without-fixed-price-October-5-2026/unequal-costs-rank-100-amalgam.pdf'),('Damien Gaboriau, Invariants ℓ² de relations d’équivalence et de groupes (2002), comparison and action invariance.','https://doi.org/10.1007/s102400200002'),('Damien Gaboriau, Coût des relations d’équivalence et des groupes (2000), group infimum convention.','https://doi.org/10.1007/s002229900019'),('Sorin Popa, Dimitri Shlyakhtenko and Stefaan Vaes, Classification of regular subalgebras of the hyperfinite II₁ factor, Remark 6.6; first arXiv version 2018.','https://arxiv.org/abs/1811.06929v1'),('Published Popa–Shlyakhtenko–Vaes article (2020).','https://doi.org/10.1016/j.matpur.2020.02.009'),('Alec Kriebel, public preliminary conditional cost–Betti observation, pinned source.','https://github.com/AlecKriebel/Math/tree/387962dc519c86b1d1833cb0a41bd3fbddd2b446/openai_followon_triage_20261006')]
    p=['<main id="main">','<article>','<header>','<p><a href="/research/">Research</a></p>',f'<h1>{esc(copy["title"])}</h1>',f'<p class="byline"><a href="{orcid}">Alec Kriebel</a> · <time datetime="2026-10-06">6 October 2026</time> · Preprint</p>','</header>',f'<p class="intro">{esc(copy["intro"])}</p>','<section aria-labelledby="paper-reader">','<h2 id="paper-reader">Read the original paper</h2>','<p><a href="paper.pdf">Open PDF</a> · <a href="paper.pdf" download>Download PDF</a></p>','<iframe src="paper.pdf#view=FitH" title="L²-acyclicity and cost for a rank-100 amalgam — original deposited paper" width="100%" height="700"></iframe>','</section>','<section>','<h2>Original files</h2>','<p>The two original files are unchanged and listed in their native order.</p>','<ul>']
    for a in pub['all_original_assets']:
        key=a['original_api_file_object']['key'];p.append(f'<li><a href="{esc(key)}" download data-native-asset="true">{esc(key)}</a> <span class="bytes">({a["bytes"]:,} bytes)</span></li>')
    p+=['</ul>',f'<p><a href="{pub["native_record"]}">Original Zenodo record</a> · <a href="{doi}">DOI: {pub["DOI"]}</a> · <a href="citation.bib" download>BibTeX</a></p>','</section>','<section id="printed-abstract">','<h2>Full printed abstract</h2>',f'<p>{esc(copy["printed_abstract"])}</p>','</section>']
    for section in copy['sections']:
        p+=['<section>',f'<h2>{esc(section["heading"])}</h2>',*[f'<p>{esc(t)}</p>' for t in section['paragraphs']],'</section>']
    p+=['<section id="native-description">','<h2>Original Zenodo description</h2>','<p>This is the separate full deposit description, distinct from the printed abstract above.</p>','<blockquote>',copy['native_description_HTML'],'</blockquote>','</section>','<section>','<h2>References and credit</h2>','<ul>',*[f'<li><a href="{esc(url)}">{esc(label)}</a></li>' for label,url in refs],'</ul>',f'<p>Pinned OpenAI source commit: <code>{pub["upstream_commit"]}</code>.</p>','</section>','<section id="rights">','<h2>Licensing</h2>',f'<p>{esc(copy["rights_paragraph"])}</p>','<p><a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0 terms</a></p>','</section>','</article>','</main>']
    mainbody='\n'.join(p)+'\n';seo=c['SEO_proposal']
    ld={'@context':'https://schema.org','@type':'ScholarlyArticle','@id':doi,'name':c['title'],'headline':copy['title'],'author':{'@type':'Person','name':'Alec Kriebel','identifier':orcid},'datePublished':pub['datePublished'],'identifier':{'@type':'PropertyValue','propertyID':'DOI','value':pub['DOI']},'url':doi,'abstract':copy['printed_abstract'],'description':seo['description'],'inLanguage':'en','license':'https://creativecommons.org/licenses/by/4.0/','isBasedOn':[refs[0][1],refs[1][1],refs[2][1],refs[3][1]],'associatedMedia':[{'@type':'MediaObject','name':a['original_api_file_object']['key'],'contentUrl':a['original_api_file_object']['key'],'encodingFormat':a['whole_original_native_files_entry']['mimetype']} for a in pub['all_original_assets']]}
    head=['<meta charset="utf-8">','<meta name="viewport" content="width=device-width, initial-scale=1">',f'<title>{esc(seo["title"])}</title>',f'<meta name="description" content="{esc(seo["description"])}">',f'<meta name="DC.description" content="{esc(copy["printed_abstract"])}">',f'<meta name="keywords" content="{esc(", ".join(seo["keywords"]))}">',f'<meta name="robots" content="{c["promotion"]["robots"]}">',f'<meta name="citation_title" content="{esc(c["title"])}">','<meta name="citation_author" content="Alec Kriebel">',f'<meta name="citation_author_orcid" content="{orcid}">','<meta name="citation_publication_date" content="2026/10/06">',f'<meta name="citation_doi" content="{pub["DOI"]}">','<meta name="citation_pdf_url" content="paper.pdf">','<meta property="og:type" content="article">',f'<meta property="og:title" content="{esc(copy["title"])}">',f'<meta property="og:description" content="{esc(seo["description"])}">',f'<meta property="og:url" content="{doi}">','<meta name="twitter:card" content="summary">',f'<meta name="twitter:title" content="{esc(copy["title"])}">',f'<meta name="twitter:description" content="{esc(seo["description"])}">','<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+'</script>','<link rel="stylesheet" href="style.css">']
    headbody='\n'.join(head)+'\n'
    css='html{color-scheme:light}body{margin:0;background:#fff;color:#171717;font-family:Arial,Helvetica,sans-serif;font-size:18px;line-height:1.65}main{max-width:920px;margin:0 auto;padding:30px 24px 64px}h1{font-size:2.05rem;line-height:1.2;font-weight:600;letter-spacing:-.025em}h2{font-size:1.45rem;line-height:1.3;margin-top:2.1rem}a{color:#174c8c;text-underline-offset:3px}p,li{overflow-wrap:anywhere}.byline,.bytes{color:#5b5b5b}.intro{font-size:1.12rem}iframe{display:block;border:1px solid #ddd;background:#fff;margin:12px 0 28px;box-sizing:border-box}blockquote{margin:1rem 0;padding:0 1.2rem;border-left:2px solid #ddd}code{font-size:.85em;overflow-wrap:anywhere}li{margin:.5rem 0}@media(max-width:600px){body{font-size:16px}main{padding:20px 16px 44px}h1{font-size:1.7rem}iframe{height:540px}}\n'
    bib='@misc{kriebel2026costbetti,\n  author = {Kriebel, Alec},\n  title = {L2-acyclicity and cost for a rank-100 amalgam},\n  year = {2026},\n  month = oct,\n  doi = {10.5281/zenodo.23203732},\n  url = {https://doi.org/10.5281/zenodo.23203732},\n  note = {Preprint}\n}\n'
    md=['# '+copy['title'],copy['byline'],copy['intro'],'## Original paper','[Open original PDF](paper.pdf)','## Original files',*['- ['+a['original_api_file_object']['key']+']('+a['original_api_file_object']['key']+')' for a in pub['all_original_assets']],'[Original Zenodo record]('+pub['native_record']+') · [DOI]('+doi+') · [BibTeX](citation.bib)','## Full printed abstract',copy['printed_abstract']]
    for sec in copy['sections']:md+=['## '+sec['heading'],*sec['paragraphs']]
    md+=['## Original Zenodo description','Separate full native HTML description; distinct from the printed abstract.',copy['native_description_HTML'],'## References and credit',*['- ['+label+']('+url+')' for label,url in refs],'Pinned OpenAI source commit: '+pub['upstream_commit'],'## Licensing',copy['rights_paragraph']]
    outputs={'PUBLIC_MAIN.html':mainbody.encode(),'HEAD.html':headbody.encode(),'style.css':css.encode(),'citation.bib':bib.encode(),'COPY.md':('\n\n'.join(md)+'\n').encode(),'index.html':('<!doctype html>\n<html lang="en">\n<head>\n'+headbody+'</head>\n<body>\n'+mainbody+'</body>\n</html>\n').encode()}
    for a in pub['all_original_assets']:
        b=Path(a['path']).read_bytes();need(pin(b)=={k:a[k] for k in ['bytes','SHA256']},'whole original asset');outputs[a['original_api_file_object']['key']]=b
    out=R/args.output;out.mkdir(exist_ok=False)
    for n,b in outputs.items():
        with (out/n).open('xb') as f:f.write(b)
    print(json.dumps({'status':'PRIVATE_EDITORIAL_RENDERED','record_id':23203732,'output':args.output,'files':[{'name':n,**pin(b)} for n,b in sorted(outputs.items())],'production_authority':False},sort_keys=True))
if __name__=='__main__':main()
