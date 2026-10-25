"""Render one reviewed paper into the existing plain research site."""
from pathlib import Path
from datetime import date
from html import escape
import hashlib, json, re, sys
from pypdf import PdfReader
from published_assets import PublishedAssets, asset_name, normalized_receipt_view
from bosonic_source import bosonic_source_view
from dipole_source import dipole_source_view
from cfh_source import CFH_IDS, cfh_source_view
from cylinder_discotope_source import CD_IDS, cylinder_discotope_source_view, display_cd_abstract
from spanning_sos_gin_source import SG_IDS, PINS as SG_PINS, spanning_sos_gin_source_view, normalize_sg_abstract, display_sg_text

from ambient_block_modulus_source import ABM_IDS, STATUSES as ABM_STATUSES, ambient_block_modulus_source_view, normalize_abm_abstract

ROOT = Path(__file__).resolve().parents[1]
SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')
paper = ROOT / 'papers' / str(int(sys.argv[1]))
c = json.loads((paper/'publication.json').read_text())
gate = json.loads((paper/'promotion.json').read_text())
if paper.name not in ABM_IDS:assert gate['status'] == 'PASS'
receipt_path = paper/'sources/receipt.json'
asset_root = paper/'sources'
if paper.name in ABM_IDS:
    raw_receipt, receipt, asset_root = ambient_block_modulus_source_view(paper,c,gate)
    receipt_path=paper/c['source_binding']['source_receipt_path']
elif paper.name in SG_IDS:
    raw_receipt, receipt, asset_root = spanning_sos_gin_source_view(paper,c,gate)
    receipt_path=paper/c['source_binding']['source_receipt_path']
elif paper.name in CD_IDS:
    raw_receipt, receipt, asset_root = cylinder_discotope_source_view(paper, c, gate)
elif paper.name in CFH_IDS:
    raw_receipt, receipt, asset_root = cfh_source_view(paper, c, gate)
elif paper.name == '23390551':
    raw_receipt, receipt, asset_root = dipole_source_view(paper, c, gate)
    receipt_path = paper/c['source_binding']['receipt_path']
elif paper.name == '23203100':
    raw_receipt, receipt, asset_root = bosonic_source_view(paper, c, gate)
    receipt_path = paper/c['source_binding']['receipt_path']
else:
    raw_receipt = json.loads(receipt_path.read_bytes())
    receipt = normalized_receipt_view(raw_receipt)
assets = PublishedAssets(asset_root, receipt, c.get('source_binding', {}).get('embedded_assets', []))
if gate.get('publication_sha256'):
    assert gate['publication_sha256'] == hashlib.sha256((paper/'publication.json').read_bytes()).hexdigest()
if gate.get('source_receipt_sha256'):
    assert gate['source_receipt_sha256'] == hashlib.sha256(receipt_path.read_bytes()).hexdigest()
for item in receipt['files']:
    assets.resolve(asset_name(item))
assert gate['pdf_sha256'] == next(x['sha256'] for x in receipt['files'] if asset_name(x)==c['pdf_filename'])
slug = c['slug']; assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug)
asset_names = [c['pdf_filename']]
if c.get('supplement_filename'): asset_names.append(c['supplement_filename'])
asset_names += [asset['filename'] for asset in c.get('additional_assets', [])]
assert len(asset_names) == len(set(asset_names))
resolved_assets = {name: assets.resolve(name) for name in asset_names}
out = SITE/slug; out.mkdir(exist_ok=True)
for name in asset_names:
    (out/name).write_bytes(resolved_assets[name].read_bytes())
h=escape
sg_asset_urls={x['name']:x['url'] for x in receipt['files']} if paper.name in SG_IDS or paper.name in ABM_IDS else {}
url=f'https://aleckriebel.com/research/{slug}/'
doi='https://doi.org/'+c['doi']
record_id=receipt['record_id']
original_pdf_url=sg_asset_urls[c['pdf_filename']] if paper.name in SG_IDS or paper.name in ABM_IDS else f'https://zenodo.org/records/{record_id}/files/{c["pdf_filename"]}'
published=date.fromisoformat(c['publication_date']); display_date=f'{published.day} {published.strftime("%B %Y")}'
today=date.today().isoformat()
authors=c.get('authors',[c['author']])
rendered_abstract=display_cd_abstract(paper.name,c['abstract']) if paper.name in CD_IDS else c['abstract']
article={'@type':'ScholarlyArticle','@id':url+'#article','url':url,'name':c['title'],'headline':c['title'],'description':c['description'],'abstract':rendered_abstract,'author':[{'@type':'Person','name':a,**({'sameAs':'https://orcid.org/0009-0001-9320-500X'} if a=='Alec Kriebel' else {})} for a in authors],'datePublished':c['publication_date'],'version':c['version'],'creativeWorkStatus':'Unrefereed preprint','inLanguage':'en','isAccessibleForFree':True,'sameAs':doi,'identifier':{'@type':'PropertyValue','propertyID':'DOI','value':c['doi']},'encoding':{'@type':'MediaObject','contentUrl':url+c['pdf_filename'],'encodingFormat':'application/pdf'}}
if c['version'] is None: article.pop('version')
if paper.name in ('23444606','23440119','23224103','23390551','23430326','23204952','22983138','23409904') or paper.name in CD_IDS or paper.name in SG_IDS or paper.name in ABM_IDS: article['license']='https://creativecommons.org/licenses/by/4.0/'
schema={'@context':'https://schema.org','@graph':[{'@type':'WebPage','@id':url+'#page','url':url,'name':c['title'],'dateCreated':today,'dateModified':today,'mainEntity':{'@id':url+'#article'}},article]}
def section(anchor,title,paragraphs):
    return f'<section id="{anchor}"><h2>{h(title)}</h2>'+''.join(f'<p>{h(display_sg_text(paper.name,p) if paper.name in SG_IDS else p)}</p>' for p in paragraphs)+'</section>'
abstract_heading=c.get('abstract_heading','Abstract') if paper.name in ('23383961','23430906','23444606','23440119','23224103','23390551','23430326','23204952','22983138','23409904') or paper.name in SG_IDS or paper.name in ABM_IDS else 'Abstract'
sections=section('abstract',abstract_heading,rendered_abstract.split('\n\n'))+section('plain-language','The idea in plain English',c['plain_language'])+section('result','The precise result',c['result'])
if c.get('why_it_works'): sections+=section('proof','Why the result holds',c['why_it_works'])
sections+=section('limits','Scope and limitations',c['limitations'])
status_paragraphs=[c.get('ai_disclosure', 'This is an unrefereed preprint. AI tools were used extensively in the research, proof development, computational checks, literature review, and writing. The supporting package contains the published source and verification materials.')]
if paper.name in CD_IDS or paper.name in SG_IDS or paper.name in ABM_IDS: status_paragraphs.insert(0,c['status'])
if c.get('edition_note'): status_paragraphs.append(c['edition_note'])
sections+=section('status','Status and AI use',status_paragraphs)
if c.get('follow_up'): sections+=section('further-research','Further research',c['follow_up'])
pdf_download=f'<a href="{h(c["pdf_filename"])}" download>Download PDF</a> · ' if paper.name in ('23203100','23383961','23430906','23444606','23440119','23224103','23390551','23430326') or paper.name in CFH_IDS or paper.name in CD_IDS or paper.name in SG_IDS or paper.name in ABM_IDS else ''
paper_intro={'23387774':'Read the complete 7-page paper in the on-page PDF reader.','23074543':'Read the complete 4-page paper in the on-page PDF reader.','23383961':'The full five-page PDF appears in the on-page reader.','23430906':'Read the full seven-page paper in the on-page PDF reader.','23444606':'Read the complete seven-page paper in the on-page PDF reader.','23440119':'Read the complete five-page paper in the on-page PDF reader.','23224103':'Read the complete six-page paper in the on-page PDF reader.','23390551':'Read the complete 11-page paper in the on-page PDF reader.','23430326':'Read the complete 9-page paper in the on-page PDF reader.','23204952':'Read the complete 8-page paper in the on-page PDF reader.','22983138':'Read the complete 4-page paper in the on-page PDF reader.','23409904':'Read the complete 6-page paper in the on-page PDF reader.'}.get(paper.name)
if paper.name in SG_IDS or paper.name in ABM_IDS:paper_intro=c['reader_intro']
paper_intro_html=f'<p>{h(paper_intro)}</p>' if paper_intro else ''
pdf_reader_word='complete' if paper.name in ('23390551','23430326') or paper.name in CFH_IDS or paper.name in CD_IDS or paper.name in SG_IDS or paper.name in ABM_IDS else 'full'
original_pdf_download=' download' if paper.name in CFH_IDS or paper.name in CD_IDS or paper.name in SG_IDS or paper.name in ABM_IDS else ''
sections+=f'<section id="paper"><h2>Read the paper</h2>{paper_intro_html}<p><a href="{h(c["pdf_filename"])}">Open PDF in a full window</a> · {pdf_download}<a href="{h(original_pdf_url)}"{original_pdf_download}>Download the original from Zenodo</a></p><iframe class="paper-pdf" src="{h(c["pdf_filename"])}#view=FitH" title="{h(c["title"])} — {pdf_reader_word} paper PDF" loading="lazy"></iframe></section>'
if paper.name in ABM_IDS:
    sections+=f'<section id="materials"><h2>Supporting materials</h2><ul><li><a href="{h(c["supplement_filename"])}" download>{h(c["supplement_label"])}</a> · <a href="{h(sg_asset_urls[c["supplement_filename"]])}">Zenodo original complete ZIP</a></li></ul></section>'
elif paper.name in SG_IDS:
    tex_link=(f'<li><a href="{h(sg_asset_urls["seven_plane_gin.tex"])}">Zenodo original published TeX source</a></li>' if paper.name=='23395703' else '')
    sections+=f'<section id="materials"><h2>Supporting materials</h2><ul><li><a href="{h(c["supplement_filename"])}" download>{h(c["supplement_label"])}</a> · <a href="{h(sg_asset_urls[c["supplement_filename"]])}">Zenodo original complete ZIP</a></li>{tex_link}</ul></section>'
elif paper.name in CFH_IDS or paper.name in CD_IDS:
    checksum_link='<li><a href="https://zenodo.org/records/22983138/files/SHA256SUMS">Zenodo original published checksum file (SHA256SUMS)</a></li>' if paper.name == '22983138' else ''
    sections+=f'<section id="materials"><h2>Supporting materials</h2><ul><li><a href="{h(c["supplement_filename"])}" download>{h(c["supplement_label"])}</a> · <a href="https://zenodo.org/records/{record_id}/files/{h(c["supplement_filename"])}">Zenodo original ZIP</a></li>{checksum_link}</ul></section>'
elif paper.name in ('23383961','23430906','23444606','23440119','23224103','23390551','23430326','23204952','22983138','23409904'):
    sections+=f'<section id="materials"><h2>Supporting materials</h2><ul><li><a href="{h(c["supplement_filename"])}" download>{h(c["supplement_label"])}</a> · <a href="https://zenodo.org/records/{record_id}/files/{h(c["supplement_filename"])}">Zenodo original ZIP</a></li></ul></section>'
elif c.get('related_resources'):
    sections+='<section id="materials"><h2>Supporting materials</h2><ul>'+''.join(f'<li><a href="{h(x["url"])}">{h(x["label"])}</a>'+(' · DOI '+h(x['doi']) if x.get('doi') else '')+'</li>' for x in c['related_resources'])+'</ul></section>'
if paper.name in CD_IDS and c.get('related_resources'):
    sections+='<section id="related"><h2>Related source editions</h2><ul>'+''.join(f'<li><a href="{h(x["url"])}">{h(x["title"])}</a>'+(': '+h(x['note']) if x.get('note') else '')+'</li>' for x in c['related_resources'])+'</ul></section>'
sections+=section('collaborate','Collaborate on this result',[c['collaboration'],'Authorship and responsibilities would be discussed in relation to the substantive contributions made.'])+'<p><a href="mailto:me@aleckriebel.com">Contact Alec</a></p>'
citation_edition_label=c['citation_edition_label'] if 'citation_edition_label' in c else ('Version '+c['version'] if c['version'] is not None else 'No version number supplied')
sections+=f'<section id="cite"><h2>Cite this paper</h2><p>{h("; ".join(authors))}. ({published.year}). <i>{h(c["title"])}</i> ({h(citation_edition_label)}) [Preprint]. Zenodo. <a href="{doi}">{doi}</a></p><p><a href="citation.bib">Download BibTeX</a></p></section>'
def background_entry(x):
    title=h(x['title'])
    link=(f'<span>{title}</span>' if paper.name in CD_IDS and not x['url'] else f'<a href="{h(x["url"])}">{title}</a>')
    return '<li>'+link+(': '+h(x['note']) if x.get('note') else '')+'</li>'
sections+='<section id="background"><h2>Background and prior work</h2><ul>'+''.join(background_entry(x) for x in c['background'])+'</ul></section>'
author_meta='\n'.join(f'<meta name="citation_author" content="{h(a)}">' for a in authors)
pages=len(PdfReader(out/c['pdf_filename']).pages)
download_links = [f'<a href="{h(c["pdf_filename"])}">Read the paper (PDF, {pages} pages)</a>']
if paper.name in ('23203100','23383961','23430906','23444606','23440119','23224103','23390551','23430326'):
    download_links.append(f'<a href="{h(c["pdf_filename"])}" download>Download PDF</a>')
if c.get('supplement_filename'):
    download_links.append(f'<a href="{h(c["supplement_filename"])}" download>{h(c.get("supplement_label", "Source and verification (ZIP)"))}</a>')
for asset in c.get('additional_assets', []):
    assets.additional_asset_kind(asset)
    download_links.append(f'<a href="{h(asset["filename"])}">{h(asset["label"])}</a>')
download_links.append(f'<a href="{doi}">Zenodo record</a>')
if paper.name in ('23444606','23440119','23224103','23390551','23430326','23204952','22983138','23409904') or paper.name in CD_IDS or paper.name in SG_IDS or paper.name in ABM_IDS: download_links.append('<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>')
document=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{h(c['title'])} | Alec Kriebel</title>
<meta name="description" content="{h(c['description'])}">
<meta name="author" content="{h('; '.join(authors))}">
<link rel="canonical" href="{url}"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="/research/research.css">
<meta name="citation_title" content="{h(c['title'])}">{author_meta}
<meta name="citation_author_orcid" content="0009-0001-9320-500X"><meta name="citation_publication_date" content="{c['publication_date'].replace('-','/')}">
<meta name="citation_doi" content="{c['doi']}"><meta name="citation_pdf_url" content="{url+c['pdf_filename']}"><meta name="citation_language" content="en">
<meta property="og:type" content="article"><meta property="og:title" content="{h(c['title'])}"><meta property="og:description" content="{h(c['description'])}"><meta property="og:url" content="{url}"><meta property="og:site_name" content="Alec Kriebel"><meta property="article:published_time" content="{c['publication_date']}"><meta name="twitter:card" content="summary">
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')}</script>
</head><body>
<a class="skip-link" href="#main">Skip to content</a>
<header><p class="site-title"><a href="/">Alec Kriebel</a></p><nav aria-label="Main navigation"><a href="/research/">Research</a> | <a href="/blog/">Blog</a> | <a href="https://orcid.org/0009-0001-9320-500X">ORCID</a></nav></header>
<main id="main"><article><header>
<h1><a href="/research/{slug}/">{h(c['title'])}</a></h1>
<p class="entry-meta">By {h('; '.join(authors))}, independent researcher.<br>{h('Manuscript and declared publication date' if paper.name in CD_IDS else c.get('publication_date_label', 'Published'))} <time datetime="{c['publication_date']}">{display_date}</time> · {h(c['edition_label'] if 'edition_label' in c else ('Version '+c['version'] if c['version'] is not None else 'No version number supplied'))} · <strong>Unrefereed preprint</strong></p>
<p>{' · '.join(download_links)}</p>
<p><a href="#plain-language">Plain-English explanation</a> · <a href="#paper">Read on this page</a> · <a href="#collaborate">Collaboration</a></p>
</header><hr>{sections}</article></main>
<footer><hr><p><a href="/research/">Research home</a> | <a href="mailto:me@aleckriebel.com">me@aleckriebel.com</a></p><p class="copyright">© 2013–2026 Kriebel LLC.</p></footer>
</body></html>
'''
(out/'index.html').write_text(document)
bibtex_note=c['bibtex_note'] if 'bibtex_note' in c else ('Unrefereed preprint, version '+c['version'] if c['version'] is not None else 'Unrefereed preprint; no version number supplied')
bib=f'@misc{{kriebel{published.year}_{slug.replace("-","_")},\n  author = {{{" and ".join(authors)}}},\n  title = {{{c["title"]}}},\n  year = {{{published.year}}},\n  doi = {{{c["doi"]}}},\n  url = {{{doi}}},\n  note = {{{bibtex_note}}}\n}}\n'
if paper.name in SG_IDS or paper.name in ABM_IDS: bib=(paper/c['source_binding']['prepared_bibtex_path']).read_text()
elif paper.name in ('23444606','23440119','23224103','23390551','23430326','23204952','22983138','23409904') or paper.name in CD_IDS: bib=(paper/'reviews/editorial/citation.bib').read_text()
(out/'citation.bib').write_text(bib)
# Extend the existing plain list without changing the user's other site content.
index=(SITE/'index.html').read_text()
if f'href="/research/{slug}/"' not in index:
    entry=f'<li><a href="/research/{slug}/">{h(c["title"])}</a><br><span class="entry-meta">{display_date} · Unrefereed preprint</span><p>{h(c["description"])}</p><p><a href="/research/{slug}/{c["pdf_filename"]}">PDF</a> · <a href="{doi}">Zenodo</a></p></li>\n'
    index=index.replace('    </ul>','      '+entry+'    </ul>',1)
    match=re.search(r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)',index,re.S)
    data=json.loads(match.group(2));items=data['mainEntity']['itemListElement'];items.append({'@type':'ListItem','position':len(items)+1,'url':url,'name':c['title']});data['mainEntity']['numberOfItems']=len(items)
    index=index[:match.start(2)]+json.dumps(data,ensure_ascii=False)+index[match.end(2):]
    (SITE/'index.html').write_text(index)
sitemap=(SITE/'sitemap.xml').read_text()
if '<loc>'+url+'</loc>' not in sitemap:
    sitemap=sitemap.replace('</urlset>',f'  <url><loc>{url}</loc><lastmod>{today}</lastmod></url>\n</urlset>');(SITE/'sitemap.xml').write_text(sitemap)
print(json.dumps({'record':record_id,'url':url,'output':str(out),'pdf_pages':pages}))
