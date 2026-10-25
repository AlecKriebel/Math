"""Render one reviewed paper into the existing plain research site."""
from pathlib import Path
from datetime import date
from html import escape
import hashlib, json, re, shutil, sys
from pypdf import PdfReader

def asset_name(item):
    name, filename = item.get('name'), item.get('filename')
    if name is not None and filename is not None and name != filename:
        raise ValueError('Conflicting receipt name and filename')
    value = name if name is not None else filename
    if not isinstance(value, str) or not value:
        raise ValueError('Receipt asset has no valid name or filename')
    return value

ROOT = Path(__file__).resolve().parents[1]
SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')
paper = ROOT / 'papers' / str(int(sys.argv[1]))
c = json.loads((paper/'publication.json').read_text())
gate = json.loads((paper/'promotion.json').read_text())
assert gate['status'] == 'PASS'
receipt = json.loads((paper/'sources/receipt.json').read_text())
if gate.get('publication_sha256'):
    assert gate['publication_sha256'] == hashlib.sha256((paper/'publication.json').read_bytes()).hexdigest()
if gate.get('source_receipt_sha256'):
    assert gate['source_receipt_sha256'] == hashlib.sha256((paper/'sources/receipt.json').read_bytes()).hexdigest()
for item in receipt['files']:
    assert hashlib.sha256((paper/'sources'/asset_name(item)).read_bytes()).hexdigest() == item['sha256']
assert gate['pdf_sha256'] == next(x['sha256'] for x in receipt['files'] if asset_name(x)==c['pdf_filename'])
slug = c['slug']; assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug)
out = SITE/slug; out.mkdir(exist_ok=True)
asset_names = [c['pdf_filename']]
if c.get('supplement_filename'): asset_names.append(c['supplement_filename'])
asset_names += [asset['filename'] for asset in c.get('additional_assets', [])]
assert len(asset_names) == len(set(asset_names))
for name in asset_names:
    assert Path(name).name == name
    assert name in {asset_name(item) for item in receipt['files']}
    shutil.copyfile(paper/'sources'/name,out/name)
h=escape
url=f'https://aleckriebel.com/research/{slug}/'
doi='https://doi.org/'+c['doi']
record_id=receipt['record_id']
published=date.fromisoformat(c['publication_date']); display_date=f'{published.day} {published.strftime("%B %Y")}'
today=date.today().isoformat()
authors=c.get('authors',[c['author']])
article={'@type':'ScholarlyArticle','@id':url+'#article','url':url,'name':c['title'],'headline':c['title'],'description':c['description'],'abstract':c['abstract'],'author':[{'@type':'Person','name':a,**({'sameAs':'https://orcid.org/0009-0001-9320-500X'} if a=='Alec Kriebel' else {})} for a in authors],'datePublished':c['publication_date'],'version':c['version'],'creativeWorkStatus':'Unrefereed preprint','inLanguage':'en','isAccessibleForFree':True,'sameAs':doi,'identifier':{'@type':'PropertyValue','propertyID':'DOI','value':c['doi']},'encoding':{'@type':'MediaObject','contentUrl':url+c['pdf_filename'],'encodingFormat':'application/pdf'}}
schema={'@context':'https://schema.org','@graph':[{'@type':'WebPage','@id':url+'#page','url':url,'name':c['title'],'dateCreated':today,'dateModified':today,'mainEntity':{'@id':url+'#article'}},article]}
def section(anchor,title,paragraphs):
    return f'<section id="{anchor}"><h2>{h(title)}</h2>'+''.join(f'<p>{h(p)}</p>' for p in paragraphs)+'</section>'
sections=section('abstract','Abstract',c['abstract'].split('\n\n'))+section('plain-language','The idea in plain English',c['plain_language'])+section('result','The precise result',c['result'])
if c.get('why_it_works'): sections+=section('proof','Why the result holds',c['why_it_works'])
sections+=section('limits','Scope and limitations',c['limitations'])
status_paragraphs=[c.get('ai_disclosure', 'This is an unrefereed preprint. AI tools were used extensively in the research, proof development, computational checks, literature review, and writing. The supporting package contains the published source and verification materials.')]
if c.get('edition_note'): status_paragraphs.append(c['edition_note'])
sections+=section('status','Status and AI use',status_paragraphs)
if c.get('follow_up'): sections+=section('further-research','Further research',c['follow_up'])
sections+=f'<section id="paper"><h2>Read the paper</h2><p><a href="{h(c["pdf_filename"])}">Open PDF in a full window</a> · <a href="https://zenodo.org/records/{record_id}/files/{h(c["pdf_filename"])}">Download the original from Zenodo</a></p><iframe class="paper-pdf" src="{h(c["pdf_filename"])}#view=FitH" title="{h(c["title"])} — full paper PDF" loading="lazy"></iframe></section>'
if c.get('related_resources'):
    sections+='<section id="materials"><h2>Supporting materials</h2><ul>'+''.join(f'<li><a href="{h(x["url"])}">{h(x["label"])}</a>'+(' · DOI '+h(x['doi']) if x.get('doi') else '')+'</li>' for x in c['related_resources'])+'</ul></section>'
sections+=section('collaborate','Collaborate on this result',[c['collaboration'],'Authorship and responsibilities would be discussed in relation to the substantive contributions made.'])+'<p><a href="mailto:me@aleckriebel.com">Contact Alec</a></p>'
citation_edition_label=c.get('citation_edition_label', 'Version '+c['version'])
sections+=f'<section id="cite"><h2>Cite this paper</h2><p>{h("; ".join(authors))}. ({published.year}). <i>{h(c["title"])}</i> ({h(citation_edition_label)}) [Preprint]. Zenodo. <a href="{doi}">{doi}</a></p><p><a href="citation.bib">Download BibTeX</a></p></section>'
sections+='<section id="background"><h2>Background and prior work</h2><ul>'+''.join(f'<li><a href="{h(x["url"])}">{h(x["title"])}</a>{": "+h(x["note"]) if x.get("note") else ""}</li>' for x in c['background'])+'</ul></section>'
author_meta='\n'.join(f'<meta name="citation_author" content="{h(a)}">' for a in authors)
pages=len(PdfReader(out/c['pdf_filename']).pages)
download_links = [f'<a href="{h(c["pdf_filename"])}">Read the paper (PDF, {pages} pages)</a>']
if c.get('supplement_filename'):
    download_links.append(f'<a href="{h(c["supplement_filename"])}" download>{h(c.get("supplement_label", "Source and verification (ZIP)"))}</a>')
for asset in c.get('additional_assets', []):
    assert asset['kind'] in ('pdf', 'zip', 'text')
    download_links.append(f'<a href="{h(asset["filename"])}">{h(asset["label"])}</a>')
download_links.append(f'<a href="{doi}">Zenodo record</a>')
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
<p class="entry-meta">By {h('; '.join(authors))}, independent researcher.<br>Published <time datetime="{c['publication_date']}">{display_date}</time> · {h(c.get('edition_label', 'Version '+c['version']))} · <strong>Unrefereed preprint</strong></p>
<p>{' · '.join(download_links)}</p>
<p><a href="#plain-language">Plain-English explanation</a> · <a href="#paper">Read on this page</a> · <a href="#collaborate">Collaboration</a></p>
</header><hr>{sections}</article></main>
<footer><hr><p><a href="/research/">Research home</a> | <a href="mailto:me@aleckriebel.com">me@aleckriebel.com</a></p><p class="copyright">© 2013–2026 Kriebel LLC.</p></footer>
</body></html>
'''
(out/'index.html').write_text(document)
bibtex_note=c.get('bibtex_note', 'Unrefereed preprint, version '+c['version'])
bib=f'@misc{{kriebel{published.year}_{slug.replace("-","_")},\n  author = {{{" and ".join(authors)}}},\n  title = {{{c["title"]}}},\n  year = {{{published.year}}},\n  doi = {{{c["doi"]}}},\n  url = {{{doi}}},\n  note = {{{bibtex_note}}}\n}}\n'
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
