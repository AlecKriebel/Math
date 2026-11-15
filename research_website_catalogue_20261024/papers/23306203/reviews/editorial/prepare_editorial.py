#!/usr/bin/env python3
"""Explicit fresh private authoring; no source/science execution or network."""
from pathlib import Path
import hashlib
import html
import json
import sys
E=Path(__file__).resolve().parent
CC='https://creativecommons.org/licenses/by/4.0/'
STYLE='body{font-family:Arial,Helvetica,sans-serif;background:#fff;color:#111;max-width:1050px;margin:2rem auto;padding:0 1.25rem;line-height:1.6}h1{line-height:1.2}h2{margin-top:2rem}a{color:#0645ad}p,li{overflow-wrap:anywhere}details{margin:1.5rem 0}summary{cursor:pointer}.paper-pdf{display:block;width:100%;height:80vh;min-height:500px;max-height:1000px;border:1px solid #ccc;box-sizing:border-box}'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def obj(p):return json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def author():
 m=obj(E/'PROTECTED_INPUTS.json');rows={r['path']:r for r in m['files']}
 for ns in m['whole_original_namespaces']:
  d=Path(ns['path']);need(sorted(str(x.relative_to(d)) for x in d.rglob('*') if x.is_file())==ns['files'],'whole original namespace')
 for r in m['files']:need(pin(Path(r['path']))==pin(E/r['copy'])=={'bytes':r['bytes'],'SHA256':r['SHA256']},'original/copy binding')
 p=obj(E/'publication.json');esc=html.escape
 label=p['author']+' · '+p['publication_date_label']+' · '+p['version_label']+' · '+p['status']
 main='<main id="main"><article>\n<header><h1>'+esc(p['title'])+'</h1><p>'+esc(label)+'</p><p><a href="'+p['orcid']+'">ORCID</a> · <a href="https://doi.org/'+p['doi']+'">DOI and Zenodo record</a></p></header>\n'
 main+='<section id="abstract"><h2>Original printed abstract</h2><p>'+esc(p['abstract'])+'</p></section>\n'
 deposit='<details id="native-deposit-description"><summary>Original Zenodo deposit description</summary>'+p['native_deposit_description_html']+'</details>\n'
 need('<script' not in deposit.lower(),'native description must be inert');main+=deposit
 markdown='# '+p['title']+'\n\n'+label+'\n\n## Original printed abstract\n\n'+p['abstract']+'\n\n'+deposit
 for s in obj(E/'public-sections.json'):
  main+='<section id="'+s['id']+'"><h2>'+esc(s['heading'])+'</h2>'+''.join('<p>'+esc(x)+'</p>' for x in s['paragraphs'])
  markdown+='\n## '+s['heading']+'\n\n'+'\n\n'.join(s['paragraphs'])+'\n'
  if s['id']=='read':
   main+='<p><a href="'+p['pdf_filename']+'" target="_blank" rel="noopener">Open the complete PDF</a> · <a href="'+p['pdf_filename']+'" download>Download PDF</a> · <a href="'+p['supplement_filename']+'" download>Complete original source and support ZIP</a> · <a href="citation.bib" download>BibTeX</a></p>'
   main+='<iframe class="paper-pdf" src="'+p['pdf_filename']+'#view=FitH" title="Complete five-page paper" loading="lazy" width="100%" height="900"><p><a href="'+p['pdf_filename']+'">Read the complete paper</a></p></iframe>'
   markdown+='\n[Open or download the complete PDF]('+p['pdf_filename']+') · [Complete original support ZIP]('+p['supplement_filename']+') · [BibTeX](citation.bib)\n'
  if s['id']=='rights':
   main+='<p><a href="'+CC+'">CC BY 4.0</a></p>';markdown+='\n[CC BY 4.0]('+CC+')\n'
  main+='</section>\n'
 main+='<section id="references"><h2>Related literature</h2><ul>';markdown+='\n## Related literature\n\n'
 for r in p['related_resources']:
  main+='<li><a href="'+esc(r['url'],quote=True)+'">'+esc(r['label'])+'</a>. '+esc(r['context'])+'</li>'
  markdown+='- ['+r['label']+']('+r['url']+'). '+r['context']+'\n'
 main+='</ul></section>\n<section id="cite"><h2>Citation</h2><p>'+esc(p['citation_text'])+'</p></section>\n</article></main>\n'
 markdown+='\n## Citation\n\n'+p['citation_text']+'\n'
 enc=[{'@type':'MediaObject','encodingFormat':n['whole_original_native_files_entry']['mimetype'],'contentUrl':n['original_api_file_object']['links']['self'],'license':CC} for n in p['native_assets_in_original_order']]
 scholarly={'@context':'https://schema.org','@type':'ScholarlyArticle','name':p['title'],'headline':p['title'],'description':p['description'],'abstract':p['abstract'],'author':{'@type':'Person','name':p['author'],'identifier':p['orcid']},'datePublished':p['publication_date'],'version':p['version'],'identifier':p['doi'],'url':'https://doi.org/'+p['doi'],'creativeWorkStatus':p['status'],'license':CC,'inLanguage':'en','encoding':enc}
 meta={'description':p['description'],'author':p['author'],'robots':p['seo']['robots_private_candidate'],'citation_title':p['title'],'citation_author':p['author'],'citation_author_orcid':p['orcid'],'citation_publication_date':p['publication_date'].replace('-','/'),'citation_version':p['version'],'citation_doi':p['doi'],'citation_pdf_url':p['native_assets_in_original_order'][1]['original_api_file_object']['links']['self'],'citation_language':'en'}
 head='<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+esc(p['seo']['title'])+'</title>'
 head+=''.join('<meta name="'+k+'" content="'+esc(v,quote=True)+'">' for k,v in meta.items())
 head+='<script type="application/ld+json">'+json.dumps(scholarly,ensure_ascii=False)+'</script><style>'+STYLE+'</style></head><body>\n<a href="#main">Skip to content</a>\n'
 out={'PUBLIC_COPY.md':markdown.encode(),'PUBLIC_MAIN.html':main.encode(),'SCHOLARLY_METADATA.json':(json.dumps(scholarly,ensure_ascii=False,indent=2)+'\n').encode(),'citation.bib':p['prepared_bibtex'].encode(),'candidate/index.html':(head+main+'</body></html>\n').encode(),'candidate/citation.bib':p['prepared_bibtex'].encode()}
 for n in p['native_assets_in_original_order']:out['candidate/'+n['original_api_file_object']['key']]=(E/rows[n['path']]['copy']).read_bytes()
 need(len(out)==8,'exact8 authoring buffers');return out
def main():
 need(len(sys.argv)==2 and sys.argv[1] in ['normal','optimized'],'explicit mode required');mode=sys.argv[1];dest=E if mode=='normal' else E/'optimized-authoring';out=author()
 for n in out:need(not (dest/n).exists(),'refuse output overwrite '+n)
 for n,b in out.items():
  q=dest/n;need(q.is_relative_to(E),'only owned writes');q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 print(json.dumps({'phase':'PRIVATE_FOCAL_PERIOD_EDITORIAL_AUTHORING','mode':mode,'optimization_level':sys.flags.optimize,'actual_buffers_written':len(out),'output_root':str(dest),'native_files':2,'source_scientific_or_native_execution':False,'production_authority':False}))
if __name__=='__main__':main()
