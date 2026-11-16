#!/usr/bin/env python3
"""Fixed private16-path stage. Default verifies read-only; only --build writes.

No subprocess, project/scientific import, native checker, Git operation or
external network call. --serve binds loopback and serves allowlisted bytes only.
Run with python3 -B. Root must read this exact body before its first execution.
"""
import argparse
import copy
from datetime import date
import hashlib
import html
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
import re
import stat
from urllib.parse import unquote, urlsplit

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
O = P / 'verification/next-three-private-stage-sol-20261115'
C = O / 'candidate'
INPUT_SHA = 'bbfed93ad1d1d0906e02a28cfc0b38a388e766c002e8085cf986e1795888f408'
INITIAL_SHA = '4960186f90d20b3c8c47321e67748273770bc93762b7f6996bc0f9314f76930d'
READS = {}


def need(test, message):
    if not test:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def relative(value):
    q = Path(value)
    need(not q.is_absolute() and value and all(x not in ('.', '..') for x in q.parts), 'Unsafe relative path')
    return q


def pinned(path, pin):
    need(stat.S_ISREG(path.lstat().st_mode), 'Nonregular input: ' + str(path))
    data = path.read_bytes()
    expected = pin.get('SHA256', pin.get('sha256'))
    need(digest(data) == expected, 'Input SHA256 mismatch: ' + str(path))
    if 'bytes' in pin:
        need(len(data) == pin['bytes'], 'Input size mismatch: ' + str(path))
    READS[path] = (len(data), expected)
    return data


def source(pin):
    return pinned(P / relative(pin['path']), pin)


def decoded(data):
    return json.loads(data.decode('utf-8'))


def initial():
    seal = decoded(pinned(O / 'INITIAL_SEAL.json', {'SHA256': INITIAL_SHA}))
    for pin in seal['payload_manifest']['pins_exactly']:
        pinned(O / relative(pin['path']), pin)
    pinned(O / 'INITIAL_SHA256SUMS.txt', seal['payload_manifest'])
    return decoded((O / 'SOURCE_ADOPTION_LEDGER.json').read_bytes())


def sealed_namespace(root, manifest, terminals, extra_pins):
    pins = {x['path']: x for x in manifest['files']}
    need(not (set(pins) & set(terminals)), 'Terminal/payload overlap')
    expected = set(pins) | set(terminals)
    nodes = list(root.rglob('*'))
    need(not any(x.is_symlink() for x in nodes), 'Symlink in frozen namespace')
    need({str(x.relative_to(root)) for x in nodes if x.is_file()} == expected, 'Frozen file extent drift')
    need({str(x.relative_to(root)) for x in nodes if x.is_dir()} == set(manifest['directories']), 'Frozen directory extent drift')
    for name, pin in pins.items():
        pinned(root / relative(name), pin)
    for pin in extra_pins:
        pinned(root / relative(pin['path']), pin)


def baseline():
    need((W / '.git/HEAD').read_text() == 'ref: refs/heads/master\n', 'Website HEAD name drift')
    need((W / '.git/refs/heads/master').read_text().strip() == '52c72c60f2913f22d8a323aff1339759fb4ac7b9', 'Website commit drift')
    pinned(W / '.git/index', {'bytes': 9040648, 'SHA256': '6d315ea8f2e029b5fb3bcd769e8f7eb45d14ca93a549b484d2f8992158644458'})
    need(stat.S_IMODE((W / '.git/index').stat().st_mode) == 0o600, 'Website index mode drift')
    names = set()
    for line in (O / 'BASELINE_PUBLIC_NAMESPACE.txt').read_text().splitlines():
        name, kind, mode, size = line.rsplit('|', 3)
        path = Path(name)
        need(path == W / 'public' or (W / 'public') in path.parents, 'Baseline namespace escape')
        s = path.lstat()
        need(stat.S_IMODE(s.st_mode) == int(mode, 8), 'Public mode drift: ' + name)
        need((kind == 'Regular File' and stat.S_ISREG(s.st_mode)) or (kind == 'Directory' and stat.S_ISDIR(s.st_mode)), 'Public type drift: ' + name)
        if kind == 'Regular File':
            need(s.st_size == int(size), 'Public size drift: ' + name)
        names.add(path)
    need(names == {W / 'public', *(W / 'public').rglob('*')}, 'Public finite namespace drift')
    files = {}
    for line in (O / 'BASELINE_PUBLIC_SHA256.txt').read_text().splitlines():
        sha, name = line.split('  ', 1)
        path = Path(name)
        need(path in names, 'Unexpected public hash path')
        pinned(path, {'SHA256': sha})
        files[str(path.relative_to(W / 'public'))] = path
    need(len(files) == 647 and len(names) == 991, 'Public count drift')
    return files


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.meta, self.links, self.ids, self.h1, self.main = {}, [], [], 0, 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta' and ('name' in a or 'property' in a):
            key = a.get('name', a.get('property'))
            need(key not in self.meta, 'Duplicate meta: ' + key)
            self.meta[key] = a.get('content', '')
        if 'id' in a:
            self.ids.append(a['id'])
        self.h1 += tag == 'h1'
        self.main += tag == 'main'
        for key in ('src', 'href'):
            if key in a:
                self.links.append(a[key])


def scholarly(head):
    match = re.findall(r'<script type="application/ld\+json">(.*?)</script>', head, re.S)
    need(len(match) == 1, 'Expected one adopted scholarly object')
    return json.loads(match[0])


def dumps(obj):
    return json.dumps(obj, ensure_ascii=False).replace('<', '\\u003c')


def escape(value):
    return html.escape(str(value), quote=True)


def compose(record, config, main, bib, assets, head, extra, day, site):
    slug = record['proposed_slug']
    route = '/research/' + slug + '/'
    url = site + route
    if head is not None:
        info = Tags(head)
        title = html.unescape(re.search(r'<title>(.*?)</title>', head, re.S)[1])
        description = info.meta['description']
        article = scholarly(head)
    else:
        title, description = extra['model']['page_title'], extra['model']['meta_description']
        article = copy.deepcopy(extra['metadata']['scholarly'])
        article['abstract'] = extra['metadata']['full_printed_abstract']
    article = copy.deepcopy(article)
    abstract = article.get('abstract', article.get('description'))
    need(abstract and description and title, 'Missing adopted abstract or SEO text')
    pdf = next(name for name in assets if name.endswith('.pdf'))
    article.pop('@context', None)
    article.pop('associatedMedia', None)
    article.update({'@id':url+'#article', 'url':url, 'description':description, 'abstract':abstract,
                    'mainEntityOfPage':{'@id':url+'#page'}, 'inLanguage':'en', 'isAccessibleForFree':True,
                    'creativeWorkStatus':'Unrefereed preprint'})
    article['encoding'] = [{'@type':'MediaObject', 'name':Path(name).name,
                            'encodingFormat':mimetypes.guess_type(name)[0] or 'application/octet-stream',
                            'contentUrl':url+name,
                            'sameAs':'https://zenodo.org/api/records/'+str(record['record_id'])+'/files/'+Path(name).name+'/content'} for name in assets]
    page = {'@type':'WebPage','@id':url+'#page','url':url,'name':article['headline'],
            'dateCreated':day,'dateModified':day,'mainEntity':{'@id':url+'#article'}}
    values = [('description',description),('author','Alec Kriebel'),('robots','index,follow'),
              ('citation_title',record['title']),('citation_author','Kriebel, Alec'),
              ('citation_author_orcid','https://orcid.org/0009-0001-9320-500X'),
              ('citation_publication_date',record['publication_date'].replace('-','/')),
              ('citation_doi',record['DOI']),('citation_pdf_url',url+pdf),('citation_language','en'),
              ('DC.identifier','doi:'+record['DOI']),('DC.rights','CC BY 4.0'),('DC.description',abstract),
              ('twitter:card','summary'),('twitter:title',article['headline']),('twitter:description',description)]
    if record['native_version']['present']:
        values.append(('citation_version',record['native_version']['value']))
        article['version'] = record['native_version']['value']
    else:
        need('version' not in article, 'Invented version in adopted article')
    tags = '\n'.join('<meta name="'+escape(k)+'" content="'+escape(v)+'">' for k,v in values)
    og = '\n'.join('<meta property="'+k+'" content="'+escape(v)+'">' for k,v in [
        ('og:type','article'),('og:title',article['headline']),('og:description',description),
        ('og:url',url),('og:site_name','Alec Kriebel'),('article:published_time',record['publication_date'])])
    style = 'main p,main li,main td,main th{overflow-wrap:anywhere}main pre,main code,main .math{white-space:pre-wrap;overflow-wrap:anywhere}main iframe{display:block;width:100%;height:80vh;min-height:500px;max-height:1000px;border:1px solid #ccc;box-sizing:border-box}'
    prefix = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>'+escape(title)+'</title>\n'+tags+'\n'+og+'\n<link rel="canonical" href="'+url+'">\n<link rel="icon" href="/favicon.ico">\n<link rel="stylesheet" href="/research/research.css">\n<script type="application/ld+json">'+dumps({'@context':'https://schema.org','@graph':[page,article]})+'</script>\n<style>'+style+'</style>\n</head>\n<body>\n<a class="skip-link" href="#main">Skip to content</a>\n<header>\n<p class="site-title"><a href="/">Alec Kriebel</a></p>\n<nav aria-label="Main navigation"><a href="/research/">Research</a> | <a href="/blog/">Blog</a> | <a href="https://orcid.org/0009-0001-9320-500X">ORCID</a></nav>\n</header>\n'
    downloads = '<aside aria-labelledby="local-original-downloads"><h2 id="local-original-downloads">Original file downloads</h2>\n<ul>\n'+''.join('<li><a href="'+escape(name)+'" download>'+escape(Path(name).name)+'</a></li>\n' for name in assets)+'</ul>\n<p><a href="citation.bib" download>BibTeX citation</a></p></aside>\n'
    suffix = downloads+'<footer><hr><p><a href="/research/">Research home</a></p><p class="copyright">© 2013–2026 Kriebel LLC.</p></footer>\n</body>\n</html>\n'
    output = {route.lstrip('/')+'index.html':prefix.encode()+main+suffix.encode(),
              route.lstrip('/')+'citation.bib':bib}
    output.update({route.lstrip('/')+name:data for name,data in assets.items()})
    return output, {'route':route,'url':url,'title':article['headline'],'description':description,
                    'PDF':route+pdf,'date':record['publication_date'],'DOI':record['DOI']}


def expected():
    ledger = initial()
    settings = decoded(pinned(O/'CONTINUATION_INPUTS.json', {'SHA256':INPUT_SHA}))
    extra = settings['record138']
    for value in extra.values():
        if isinstance(value, dict) and 'path' in value:
            source(value)
    writer = decoded(source(extra['writer_FINAL']))
    wm = decoded(source(extra['writer_manifest']))
    wr = P/'papers/23204591/reviews/editorial'
    sealed_namespace(wr, wm, writer['exact_terminal_exclusions'], writer['terminal_pins'])
    fm = decoded(source(extra['fact_manifest']))
    sealed_namespace(P/'verification/hilbert-variation-editorial-fact-audit-sol-20261115', fm, fm['exact_root_terminal_controls'], [])
    files, rows = {}, []
    for record0 in ledger['records']:
        record = copy.deepcopy(record0)
        source(record['source_ready']); source(record['science_root'])
        if record['row'] == 138:
            record.update({k:extra[k] for k in ('editorial_root','approved_MAIN','approved_BibTeX','proposed_slug')})
            model = {'model':decoded(source(extra['model'])), 'metadata':decoded(source(extra['metadata']))}
            head, config = None, model['metadata']
        else:
            config = decoded(source(record['approved_config']))
            head = source(record['approved_HEAD']).decode()
            model = None
            if record['row'] == 133:
                record['approved_BibTeX'] = settings['record133_BibTeX']
        authority = decoded(source(record['editorial_root']))
        slug = authority['proposed_slug'].strip('/').removeprefix('research/')
        need(slug == record['proposed_slug'] and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug), 'Slug authority mismatch')
        need(not (W/'public/research'/slug).exists(), 'Existing production route collision')
        layout = settings['relative_asset_layout'][str(record['record_id'])]
        assets = {layout+Path(pin['path']).name:source(pin) for pin in record['native_assets_in_order']}
        result, row = compose(record,config,source(record['approved_MAIN']),source(record['approved_BibTeX']),assets,head,model,settings['assembly_day_UTC'],settings['site_base_from_existing_research_canonical'])
        need(not(set(files)&set(result)), 'Duplicate output route')
        files.update(result); rows.append(row)
    old = (W/'public/research/index.html').read_text()
    match = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)',old,re.S)
    obj = json.loads(match[2]); items = obj['mainEntity']['itemListElement']
    need(len(items)==99 and obj['mainEntity']['numberOfItems']==99, 'Original index count mismatch')
    js = match[2]
    need(js.count('"numberOfItems": 99')==1 and js.endswith(']}}'), 'Unexpected existing index representation')
    js = js.replace('"numberOfItems": 99','"numberOfItems": 102')
    additions = [{'@type':'ListItem','position':100+i,'url':r['url'],'name':r['title']} for i,r in enumerate(rows)]
    js = js[:-3]+', '+', '.join(dumps(x) for x in additions)+js[-3:]
    index = old[:match.start(2)]+js+old[match.end(2):]
    marker = '    </ul>\n    <p>I’m gradually'
    need(index.count(marker)==1, 'Unexpected visible-index append point')
    entry = ''.join('      <li><a href="'+r['route']+'">'+escape(r['title'])+'</a><br><span class="entry-meta">'+date.fromisoformat(r['date']).strftime('%-d %B %Y')+' · Unrefereed preprint</span><p>'+escape(r['description'])+'</p><p><a href="'+r['PDF']+'">PDF</a> · <a href="https://doi.org/'+r['DOI']+'">Zenodo</a></p></li>\n' for r in rows)
    files['research/index.html'] = index.replace(marker,entry+marker).encode()
    sitemap = (W/'public/research/sitemap.xml').read_text()
    need(sitemap.count('<loc>')==100 and sitemap.count('</urlset>')==1, 'Original sitemap count mismatch')
    append = ''.join('  <url><loc>'+r['url']+'</loc><lastmod>'+settings['assembly_day_UTC']+'</lastmod></url>\n' for r in rows)
    files['research/sitemap.xml'] = sitemap.replace('</urlset>',append+'</urlset>').encode()
    need(len(files)==16 and len(set(r['url'] for r in rows))==3, 'Fixed output count mismatch')
    return files, rows, ledger


def verify(files, rows, ledger, baseline_files):
    nodes = list(C.rglob('*'))
    need(not any(x.is_symlink() for x in nodes), 'Candidate symlink')
    actual = {str(x.relative_to(C/'public')):x for x in nodes if x.is_file()}
    need(set(actual)==set(files), 'Candidate finite namespace mismatch')
    expected_dirs = {C/'public'}
    for name in files:
        expected_dirs.update(x for x in (C/'public'/name).parents if x != C and C in x.parents)
    need({x for x in nodes if x.is_dir()}==expected_dirs, 'Candidate directory extent mismatch')
    for name, data in files.items():
        need(actual[name].read_bytes()==data and stat.S_IMODE(actual[name].stat().st_mode)==0o644, 'Candidate bytes/mode mismatch: '+name)
    for row, rec in zip(rows,ledger['records']):
        text = files[row['route'].lstrip('/')+'index.html'].decode()
        tags = Tags(text)
        need(tags.main==1 and tags.h1==1 and len(tags.ids)==len(set(tags.ids)), 'HTML main/H1/ID mismatch')
        main = source((rec if rec['row']!=138 else decoded((O/'CONTINUATION_INPUTS.json').read_bytes())['record138'])['approved_MAIN'])
        need(text.encode().count(main)==1, 'Approved whole MAIN mismatch')
        for link in tags.links:
            target = urlsplit(link)
            if target.scheme or target.netloc:
                continue
            if target.path:
                base = row['route'] if not target.path.startswith('/') else ''
                path = unquote(base+target.path).lstrip('/')
                need('..' not in Path(path).parts, 'Local traversal in HTML')
                if path.endswith('/'):
                    path += 'index.html'
                need(path in files or path in baseline_files, 'Missing local link: '+link)
            elif target.fragment:
                need(target.fragment in tags.ids, 'Missing fragment: '+link)
    index = files['research/index.html'].decode()
    idx = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',index,re.S)[1])
    need(idx['mainEntity']['numberOfItems']==102 and len(idx['mainEntity']['itemListElement'])==102, 'New index count')
    need(files['research/sitemap.xml'].count(b'<loc>')==103, 'New sitemap count')
    baseline()
    for path,(size,sha) in list(READS.items()):
        pinned(path, {'bytes':size,'SHA256':sha})
    return {'status':'PASS_PRIVATE_STAGE_MECHANICAL','publishable_files':16,'new_pages':3,'index_items':102,'sitemap_urls':103,
            'whole_MAINs_exact':True,'all8native_assets_and3Bibs_exact':True,'W_and_initial_unchanged':True,
            'candidate_pins':[{'path':'public/'+name,'bytes':len(data),'SHA256':digest(data)} for name,data in sorted(files.items())],
            'candidate_directories':sorted(str(x.relative_to(C)) for x in nodes if x.is_dir()),
            'helper_SHA256':digest(Path(__file__).read_bytes()),'input_contract_SHA256':INPUT_SHA,
            'canonical_candidates':[r['url'] for r in rows],'AA':None,'follow_up':None,
            'limits':'Private mechanical composition only; browser/PDF display and independent review pending; no install/deploy/tracker authority'}


def write_new(path, data):
    need(path == O/'BUILD_RECEIPT.json' or (C/'public') in path.parents, 'Fixed write boundary')
    need(O in path.parents and not any(x.is_symlink() for x in [O,*path.parents] if x.exists()), 'Symlink/ownership write boundary')
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as out:
        out.write(data)
    path.chmod(0o644)


def serve(files, baseline_files):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.respond(False)
        def do_HEAD(self):
            self.respond(True)
        def respond(self, head):
            name = unquote(urlsplit(self.path).path).lstrip('/')
            if not name or name.endswith('/'):
                name += 'index.html'
            if '..' in Path(name).parts or name not in set(files)|set(baseline_files):
                self.send_error(404); return
            data = files[name] if name in files else baseline_files[name].read_bytes()
            self.send_response(200)
            self.send_header('Content-Type',mimetypes.guess_type(name)[0] or 'application/octet-stream')
            self.send_header('Content-Length',str(len(data)))
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Robots-Tag','noindex,nofollow,noarchive')
            self.send_header('Content-Security-Policy',"default-src 'self'; style-src 'self' 'unsafe-inline'; frame-src 'self'; object-src 'self'; img-src 'self' data:; connect-src 'none'; base-uri 'none'; form-action 'none'")
            self.end_headers()
            if not head:
                self.wfile.write(data)
    server = ThreadingHTTPServer(('127.0.0.1',0),Handler)
    print(json.dumps({'private_loopback_URL':'http://127.0.0.1:'+str(server.server_port),'external_requests_authorized':False}),flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def main():
    args = argparse.ArgumentParser(description=__doc__)
    modes = args.add_mutually_exclusive_group()
    modes.add_argument('--build',action='store_true',help='Explicit exclusive-create16 private payloads and one build receipt')
    modes.add_argument('--serve',action='store_true',help='Verify then read-only loopback preview; no public interface')
    mode = args.parse_args()
    baseline_files = baseline()
    files, rows, ledger = expected()
    if mode.build:
        need(not C.exists() and not (O/'BUILD_RECEIPT.json').exists(), 'Build refuses existing outputs')
        for name,data in files.items():
            write_new(C/'public'/relative(name),data)
    report = verify(files,rows,ledger,baseline_files)
    if mode.build:
        write_new(O/'BUILD_RECEIPT.json',(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
    if mode.serve:
        serve(files,baseline_files)


if __name__ == '__main__':
    main()
