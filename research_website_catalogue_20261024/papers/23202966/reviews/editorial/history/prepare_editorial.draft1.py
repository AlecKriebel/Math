#!/usr/bin/env python3
"""Render one fixed private editorial proposal into one new owned directory.

No installed renderer, project/native imports, network, subprocesses or science.
Original assets are read from pinned paths and copied whole; no source is edited.
"""
import argparse
import hashlib
from html import escape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import stat

E = Path(__file__).absolute().parent
AUTHORING_SEAL = '0e9b988265f17b0c5d13b96b538df92e4c18ce579637eacaf7742d9caed24692'

def need(ok, why):
    if not ok:
        raise ValueError(why)

def pin(body):
    return {'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest()}

def read(path):
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode), 'not ordinary input')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        held = os.fstat(fd)
        need((before.st_dev, before.st_ino) == (held.st_dev, held.st_ino), 'open identity')
        pieces = []
        while True:
            piece = os.read(fd, 1048576)
            if not piece:
                break
            pieces.append(piece)
        after = os.fstat(fd)
        need((held.st_size, held.st_mtime_ns, held.st_ctime_ns) == (after.st_size, after.st_mtime_ns, after.st_ctime_ns), 'input changed')
        body = b''.join(pieces)
        need(len(body) == held.st_size, 'short read')
        return body
    finally:
        os.close(fd)

class Copy(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in ('h1', 'h2', 'h3', 'p', 'pre', 'li', 'summary', 'tr', 'caption'):
            self.parts.append('\n\n' + {'h1':'# ', 'h2':'## ', 'h3':'### ', 'li':'- '}.get(tag, ''))
        elif tag in ('th', 'td'):
            self.parts.append(' | ')
    def handle_data(self, data):
        self.parts.append(data)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--mode', choices=['normal', 'optimized'], required=True)
    args = ap.parse_args()
    need((args.mode == 'normal') == __debug__, 'mode/runtime mismatch')
    need(not (E/'FINAL_SEAL.json').exists(), 'sealed packet cannot be rendered')
    sb = read(E/'AUTHORING_INPUTS_SEAL.json')
    need(pin(sb)['SHA256'] == AUTHORING_SEAL, 'fixed authoring seal')
    seal = json.loads(sb)
    bodies = {}
    for row in seal['inputs']:
        need(Path(row['path']).name == row['path'], 'nonleaf owned input')
        body = read(E/row['path'])
        need(pin(body) == {k:row[k] for k in ['bytes','SHA256']}, 'same-buffer authoring input')
        bodies[row['path']] = body
    source = json.loads(bodies['SOURCE_INPUTS.json'])
    cfg = json.loads(bodies['EDITORIAL_CONFIG.json'])
    ready = source['whole_original_SOURCE_READY']
    need(source['whole_root_authority']['editorialPreparationAuthorized'] is True, 'actual source editorial authorization')
    need(source['whole_root_authority']['fullEditorialCopyConfigCodeAdopted'] is False, 'separate copy adoption')
    need(cfg['promotion']['canonical_url'] is None and cfg['promotion']['root_copy_adopted'] is False, 'private proposal')
    main_body = bodies['PUBLIC_MAIN.html']
    need(main_body.startswith(b'<main id="main">') and main_body.rstrip().endswith(b'</main>'), 'whole semantic MAIN')
    version = cfg['publication']['native_version_field']
    need(version == {'present':False, 'original_value':None}, 'do not invent native version')
    assets = []
    for asset in ready['all_native_assets_in_original_order']:
        body = read(Path(asset['path']))
        need(pin(body) == {k:asset[k] for k in ['bytes','SHA256']}, 'original asset identity')
        name = asset['original_api_file_object']['key']
        need(Path(name).name == name, 'nonleaf native asset')
        assets.append((name, body, asset['whole_original_native_files_entry']['mimetype']))
    title = cfg['title']
    desc = 'Explicit fixed-binary consequences of two attributed relation-liveness lower bounds, with exact compilers and full-word complement semantics.'
    base = 'https://zenodo.org/records/23202966/files/'
    encoding = []
    for name, body, mimetype in assets:
        entry = {'@type':'MediaObject', 'encodingFormat':mimetype, 'contentUrl':base+name}
        if name == 'paper.pdf':
            entry['numberOfPages'] = 6
        encoding.append(entry)
    ld = {'@context':'https://schema.org', '@type':'ScholarlyArticle', 'headline':title,
          'author':{'@type':'Person','name':'Alec Kriebel','identifier':cfg['author']['ORCID']},
          'datePublished':'2026-10-06', 'identifier':'https://doi.org/10.5281/zenodo.23202966',
          'url':'https://doi.org/10.5281/zenodo.23202966', 'abstract':cfg['publication']['printed_abstract_readable_math'],
          'creativeWorkStatus':'Unrefereed preprint', 'inLanguage':'en',
          'license':'https://creativecommons.org/licenses/by/4.0/', 'encoding':encoding,
          'citation':[
          'https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026/main.pdf',
          'https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/An-exponential-state-lower-bound-for-two-way-nondeterministic-complementation-September-25-2026/paper.pdf']}
    meta = [('robots','noindex,nofollow,noarchive'),('description',desc),('author','Alec Kriebel'),
            ('citation_title',title),('citation_author','Kriebel, Alec'),('citation_publication_date','2026/10/06'),
            ('citation_doi','10.5281/zenodo.23202966'),('citation_pdf_url',base+'paper.pdf'),('citation_language','en'),
            ('DC.identifier','doi:10.5281/zenodo.23202966'),('DC.rights','CC BY 4.0')]
    head = '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>'+escape(title)+' — Alec Kriebel</title>\n'
    head += ''.join('<meta name="'+escape(k,quote=True)+'" content="'+escape(v,quote=True)+'">\n' for k,v in meta)
    head += '<meta property="og:type" content="article">\n<meta property="og:title" content="'+escape(title,quote=True)+'">\n<meta property="og:description" content="'+escape(desc,quote=True)+'">\n'
    # A literal backslash-u sequence is emitted into JSON; this is not a Unicode no-op.
    inline = json.dumps(ld,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    head += '<script type="application/ld+json">'+inline+'</script>\n'
    css = 'html{color-scheme:light;background:#fff;color:#202124}body{font-family:Arial,Helvetica,sans-serif;font-size:18px;line-height:1.7;margin:0}main{max-width:940px;margin:auto;padding:42px 24px 72px}h1{font-size:2.25rem;line-height:1.18;letter-spacing:-.025em}h2{font-size:1.45rem;line-height:1.3;margin-top:2.4rem}a{color:#1758a5;text-underline-offset:.16em}a:focus-visible,summary:focus-visible{outline:3px solid #2b6cb0;outline-offset:4px}.eyebrow,.byline,.reader-note{color:#555;font-size:.95rem}.lede{font-size:1.15rem}.formula{font:1rem/1.65 Arial,Helvetica,sans-serif;white-space:pre;overflow:auto;padding:18px 20px;border:1px solid #ddd;background:#fafafa}iframe{width:100%;height:78vh;min-height:440px;border:1px solid #ccc}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse;font-size:.95rem}th,td{text-align:left;padding:10px;border-bottom:1px solid #ddd}caption{text-align:left;font-weight:bold;padding:8px 0}.references li{margin-bottom:1rem}details{margin-top:2.5rem;border-top:1px solid #ddd;padding-top:1rem}summary{cursor:pointer;font-weight:bold}.skip{position:absolute;top:-100px;left:12px;background:#fff;padding:8px}.skip:focus{top:8px}@media(max-width:600px){body{font-size:17px}main{padding:24px 16px 48px}h1{font-size:1.8rem}.formula{font-size:.9rem;padding:12px}iframe{height:65vh;min-height:360px}}'
    page = '<!doctype html>\n<html lang="en">\n<head>\n'+head+'<style>'+css+'</style>\n</head>\n<body>\n<a class="skip" href="#main">Skip to article</a>\n'+main_body.decode()+'</body>\n</html>\n'
    bib = '@misc{kriebel2026binaryliveness,\n  author = {Kriebel, Alec},\n  title = {Binary consequences of relation-liveness automata lower bounds},\n  year = {2026},\n  month = oct,\n  day = {6},\n  publisher = {Zenodo},\n  doi = {10.5281/zenodo.23202966},\n  url = {https://doi.org/10.5281/zenodo.23202966},\n  note = {Unrefereed preprint}\n}\n'
    copy = Copy(); copy.feed(main_body.decode()); copy.close()
    output = {'PUBLIC_HEAD.html':head.encode(), 'PUBLIC_MAIN.html':main_body,
              'PUBLIC_COPY.md':(''.join(copy.parts).strip()+'\n').encode(),
              'SCHOLARLY_METADATA.json':(json.dumps(ld,ensure_ascii=False,indent=2)+'\n').encode(),
              'citation.bib':bib.encode(), 'index.html':page.encode()}
    output.update({name:body for name,body,mimetype in assets})
    need(set(output) == set(seal['output_file_names']), 'finite ten-leaf output schema')
    root = E/('candidate' if args.mode == 'normal' else 'optimized-candidate')
    root.mkdir()
    for name, body in output.items():
        need(Path(name).name == name and (root/name).is_relative_to(E), 'outside/nonleaf output')
        with (root/name).open('xb') as stream:
            need(stream.write(body) == len(body), 'incomplete output write')
            stream.flush(); os.fsync(stream.fileno())
    print(json.dumps({'status':'PRIVATE_EDITORIAL_RENDERED','mode':args.mode,'assertions_enabled':__debug__,
                     'directory':root.name,'whole_buffers':{n:pin(b) for n,b in output.items()},
                     'publication_authority':False,'root_copy_adopted':False,'canonical_url':None,'AA':None},sort_keys=True))

if __name__ == '__main__':
    main()
