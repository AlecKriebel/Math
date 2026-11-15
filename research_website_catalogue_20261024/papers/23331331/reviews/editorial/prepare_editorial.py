#!/usr/bin/env python3
"""Bounded source-only private renderer. Never imports project/source code."""
import argparse
import hashlib
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import stat

E=Path(__file__).absolute().parent

def need(ok,why):
    if not ok:
        raise ValueError(why)

def read(p):
    need(stat.S_ISREG(p.lstat().st_mode),'not ordinary input '+str(p))
    return p.read_bytes()

def pin(b):
    return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}

def new(p,b):
    with p.open('xb') as f:
        need(f.write(b)==len(b),'incomplete output')

class CopyText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('h1','h2','h3','p','pre','li','summary'):
            self.parts.append('\n\n'+({'h1':'# ','h2':'## ','h3':'### ','li':'- '}.get(tag,'')))
    def handle_data(self,data):
        self.parts.append(data)
    def body(self):
        return ''.join(self.parts).strip()+'\n'

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--mode',choices=('normal','optimized'),required=True)
    args=ap.parse_args()
    need(not (E/'FINAL_SEAL.json').exists(),'sealed packet cannot be rendered')
    need((args.mode=='normal')==__debug__,'requested mode/runtime mismatch')
    initial=read(E/'INITIAL_SEAL.json')
    need(pin(initial)['SHA256']=='ac719e6cbf6a5a2a891d5712aec7a9fdc3e9842d369d95f686f81681652c53cb','initial seal')
    ib=read(E/'INPUTS_SEAL.json')
    need(pin(ib)['SHA256']=='da2d2c58e3fc723197118823e64e7d9ce1f3b46c015be176d0e3accebc55f7dc','inputs seal')
    seal=json.loads(ib)
    sb=read(E/'SOURCE_INPUTS.json')
    need(pin(sb)==seal['SOURCE_INPUTS'],'same-buffer source authentication')
    source=json.loads(sb)
    c=json.loads(read(E/'EDITORIAL_CONFIG.json'))
    need(c['record_id']=='23331331' and c['promotion']['canonical_url'] is None,'private identity')
    ready=source['whole_original_SOURCE_READY']
    assets=ready['all_native_assets_in_original_order']
    rows={r['path']:r for r in source['original_files']}
    asset_buffers={}
    for asset in assets:
        row=rows[asset['path']]
        b=read(E/row['copy'])
        need(pin(b)=={k:asset[k] for k in ('bytes','SHA256')},'native asset identity')
        asset_buffers[asset['original_api_file_object']['key']]=b
    main_bytes=read(E/'PUBLIC_MAIN.html')
    body=main_bytes.decode('utf-8')
    need(body.count('<main id="main">')==1 and body.rstrip().endswith('</main>'),'complete main')
    title=c['title']
    desc='Explicit phase-independent signed-area centroid for least even-period elliptic billiards, with its exact domain and an eight-star diagnostic.'
    pdf='https://zenodo.org/records/23331331/files/outer_pedal_centroid.pdf'
    zipurl='https://zenodo.org/records/23331331/files/outer-pedal-centroid-verification.zip'
    abstract=body.split('<p id="printed-abstract">',1)[1].split('</p>',1)[0]
    ld={'@context':'https://schema.org','@type':'ScholarlyArticle',
      'headline':title,'name':title,'author':{'@type':'Person','name':'Alec Kriebel','identifier':c['author']['ORCID']},
      'datePublished':'2026-10-13','version':'1.0','identifier':'https://doi.org/10.5281/zenodo.23331331',
      'url':'https://doi.org/10.5281/zenodo.23331331','abstract':abstract,
      'creativeWorkStatus':'Unrefereed preprint','inLanguage':'en','license':'https://creativecommons.org/licenses/by/4.0/',
      'keywords':ready['title']+'; elliptic billiards; Poncelet polygons; pedal polygons; signed area centroid; k307; confocal caustics',
      'encoding':[{'@type':'MediaObject','encodingFormat':'application/zip','contentUrl':zipurl},
                  {'@type':'MediaObject','encodingFormat':'application/pdf','contentUrl':pdf,'numberOfPages':5}],
      'citation':['https://doi.org/10.1007/s40598-021-00174-y','https://arxiv.org/abs/2004.12497v11',
                  'https://doi.org/10.1007/s40879-020-00428-7','https://arxiv.org/abs/1607.04766v1']}
    meta=[('robots','noindex,nofollow,noarchive'),('description',desc),('author','Alec Kriebel'),
      ('citation_title',title),('citation_author','Kriebel, Alec'),('citation_publication_date','2026/10/13'),
      ('citation_doi','10.5281/zenodo.23331331'),('citation_pdf_url',pdf),('citation_language','en'),
      ('DC.identifier','doi:10.5281/zenodo.23331331'),('DC.rights','CC BY 4.0')]
    head='<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>'+escape(title)+' — Alec Kriebel</title>\n'
    head+=''.join('<meta name="'+escape(k,quote=True)+'" content="'+escape(v,quote=True)+'">\n' for k,v in meta)
    head+='<meta property="og:type" content="article">\n<meta property="og:title" content="'+escape(title,quote=True)+'">\n<meta property="og:description" content="'+escape(desc,quote=True)+'">\n'
    head+='<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False,separators=(',',':')).replace('<','\u003c')+'</script>\n'
    css='''html{color-scheme:light;background:#fff;color:#202124}body{font-family:Arial,Helvetica,sans-serif;font-size:18px;line-height:1.65;margin:0}main{max-width:960px;margin:auto;padding:40px 24px 72px}h1{font-size:2.2rem;line-height:1.18;letter-spacing:-.025em}h2{font-size:1.45rem;line-height:1.3;margin-top:2.5rem}a{color:#1758a5;text-underline-offset:.16em}a:focus-visible,summary:focus-visible{outline:3px solid #2b6cb0;outline-offset:4px}.eyebrow,.byline,.reader-note{color:#555;font-size:.95rem}.lede{font-size:1.15rem}.formula{font:1rem/1.65 Arial,Helvetica,sans-serif;white-space:pre;overflow:auto;padding:18px 20px;border:1px solid #ddd;background:#fafafa}.math{white-space:normal}iframe{width:100%;height:78vh;min-height:440px;border:1px solid #ccc;background:#f8f8f8}section{margin-top:1.5rem}.references li{margin-bottom:1rem}details{margin-top:2.5rem;border-top:1px solid #ddd;padding-top:1rem}summary{cursor:pointer;font-weight:bold}.skip{position:absolute;left:12px;top:-100px;background:#fff;padding:8px}.skip:focus{top:8px}@media(max-width:600px){body{font-size:17px}main{padding:24px 16px 48px}h1{font-size:1.8rem}.formula{font-size:.9rem;padding:12px}iframe{height:65vh;min-height:360px}}'''
    page='<!doctype html>\n<html lang="en">\n<head>\n'+head+'<style>'+css+'</style>\n</head>\n<body>\n<a class="skip" href="#main">Skip to article</a>\n'+body+'</body>\n</html>\n'
    bib='''@misc{kriebel2026outerpedal,
  author = {Kriebel, Alec},
  title = {The outer-pedal area centroid in even-period elliptic billiards},
  year = {2026},
  month = oct,
  day = {13},
  version = {1.0},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.23331331},
  url = {https://doi.org/10.5281/zenodo.23331331},
  note = {Unrefereed preprint}
}
'''
    plain=CopyText();plain.feed(body);plain.close()
    outputs={'PUBLIC_HEAD.html':head.encode(),'PUBLIC_MAIN.html':main_bytes,'index.html':page.encode(),
      'PUBLIC_COPY.md':plain.body().encode(),'SCHOLARLY_METADATA.json':(json.dumps(ld,ensure_ascii=False,indent=2)+'\n').encode(),
      'citation.bib':bib.encode(),**asset_buffers}
    out=E/('candidate' if args.mode=='normal' else 'optimized-candidate')
    out.mkdir()
    for name,b in outputs.items():
        need(Path(name).name==name,'nonleaf output')
        new(out/name,b)
    print(json.dumps({'status':'PRIVATE_RENDERED','mode':args.mode,'assertions_enabled':__debug__,
      'output_directory':out.name,'buffers':{n:pin(b) for n,b in outputs.items()},
      'publication_authority':False,'canonical_url':None,'AA':None},ensure_ascii=False,sort_keys=True))

if __name__=='__main__':
    main()
