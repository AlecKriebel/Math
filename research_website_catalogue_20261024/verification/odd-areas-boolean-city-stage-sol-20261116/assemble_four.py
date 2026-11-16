#!/usr/bin/env python3
"""Finite private assembly. Default checks inputs only; --build writes here only."""
from pathlib import Path
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib, html, json, re, stat, struct, sys

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
O = P / 'verification/odd-areas-boolean-city-stage-sol-20261116'
ROOTS = {
    '23334001': (4345, '35067743c40008f58f5f89fe5358d8bece590f2cd0b282ab31637808ad1b5b02'),
    '23394004': (4342, 'a03bfee6ad864c35ee8cd322205843568f603396981fcce8da5dc03d8ddf92f0'),
    '23443301': (4367, '9d9e39487f2fca91f95502e506f91f90b250617496e031a154d701e6324cf5a0'),
    '23393139': (4316, 'fe3e276bb17fb83ef3279e13a4125ed2235b60692ceedfd4f83d83cc9eabbf73'),
}
BASELINE_SHA = 'ef118cd1acdf383a8e887f9a9c1a9abd410ce55a83d4a21a8afa3faad32060f4'
CONTRACT_SHA = '1d726305ec66e94f0adbb9b7c427a86bee6a4da4ee2bb81e62bdf37fb7447f52'
ORIGIN = 'https://aleckriebel.com'

def digest(b):
    return hashlib.sha256(b).hexdigest()

def readpin(p, size=None, expected=None):
    assert p.is_file() and not p.is_symlink(), str(p)
    b = p.read_bytes()
    assert size is None or len(b) == size, str(p)
    assert expected is None or digest(b) == expected, str(p)
    return b

def pin(p):
    b = readpin(p)
    return {'path': str(p), 'bytes': len(b), 'SHA256': digest(b),
            'mode': format(stat.S_IMODE(p.stat().st_mode), '04o')}

def checkpin(q, base=None):
    p = Path(q['path']) if base is None else base / q['path']
    readpin(p, q['bytes'], q.get('SHA256', q.get('sha256')))
    if 'mode' in q:
        mode = format(q['mode'], '04o') if isinstance(q['mode'], int) else q['mode']
        assert pin(p)['mode'] == mode, str(p)

def head(root):
    g = root / '.git'
    symbolic = (g / 'HEAD').read_text().strip()
    if not symbolic.startswith('ref: '):
        return {'symbolic': symbolic, 'commit': symbolic}
    ref = symbolic[5:]
    f = g / ref
    commit = f.read_text().strip() if f.exists() else next(
        s.split()[0] for s in (g / 'packed-refs').read_text().splitlines()
        if s.endswith(' ' + ref))
    return {'symbolic': symbolic, 'commit': commit}

def guards(base):
    for g in (base['website_git'], base['Math_git']):
        assert head(Path(g['root'])) == g['HEAD']
        for key in ('index', 'config', 'HEAD_file'):
            checkpin(g[key])
    for q in base['source_guards'] + base['website_configuration_guards'] + base['template_guards']:
        checkpin(q)
    files, dirs = [], [{'path': '.', 'mode': format(stat.S_IMODE((W/'public').stat().st_mode), '04o')}]
    for p in sorted((W/'public').rglob('*')):
        assert not p.is_symlink(), str(p)
        if p.is_file():
            q = pin(p); q['path'] = p.relative_to(W/'public').as_posix(); files.append(q)
        else:
            assert p.is_dir(), str(p)
            dirs.append({'path': p.relative_to(W/'public').as_posix(), 'mode': format(stat.S_IMODE(p.stat().st_mode), '04o')})
    assert files == base['public_files'] and dirs == base['public_directory_modes_including_root']
    b = (W/'.git/index').read_bytes()
    assert b[:4] == b'DIRC' and struct.unpack('>II', b[4:12]) == (2, 58651)
    assert hashlib.sha1(b[:-20]).digest() == b[-20:]
    return {'all711_public_files_and359_child_directory_modes_exact': True,
            'W_and_Math_HEAD_index_config_and28_source_guards_exact': True,
            'W_index_SHA256': digest(b), 'W_native_index_mode': '0644', 'native_index_records': 58651}

class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.meta, self.ids, self.links = {}, [], []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'meta': self.meta[a.get('name', a.get('property'))] = a.get('content')
        for k in ('href', 'src'):
            if k in a: self.links.append(a[k])

def canonical_abstract(s):
    s = html.unescape(re.sub(r'<[^>]+>', '', s))
    for a, b in ((r'\alpha', 'α'), (r'\beta', 'β'), ('⁸', '8'), ('’', "'"), ('−', '-')):
        s = s.replace(a, b)
    return ''.join(c for c in s if c.isalnum() or c in '<>=/')

def packet(a, lane):
    z = a[lane]
    for k in ('FINAL', 'manifest', 'REPORT'): checkpin(z[k], P)
    folder = (P/z['FINAL']['path']).parent
    manifest = json.loads((P/z['manifest']['path']).read_text())
    entries = manifest.get('files', manifest.get('payloads'))
    for q in entries: checkpin(q, folder)
    actual = sorted(p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file())
    assert actual == sorted([q['path'] for q in entries] + ['FINAL.json', 'OWNED_MANIFEST.json'])
    dirs = sorted(p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_dir())
    assert len(actual) == z['whole_files'] and len(dirs) == z['child_directories']
    return {'folder': str(folder), 'files': len(actual), 'child_directories': dirs,
            'root_pinned_controls': z, 'whole_file_pins': [pin(folder/p) for p in actual]}

def main():
    assert sys.argv[1:] in ([], ['--build'])
    build = bool(sys.argv[1:])
    base = json.loads(readpin(O/'BASELINE.json', expected=BASELINE_SHA))
    sources = json.loads(readpin(O/'SOURCE_CONTRACTS.json', expected=CONTRACT_SHA))['contracts']
    initial = json.loads((O/'INITIAL_SEAL.json').read_text())
    for q in initial['payloads']: checkpin(q, O)
    opening = guards(base)
    template = (W/'public/research/three-summand-kato-kernel-counterexample/index.html').read_text()
    body_prefix = template[template.index('<body>'):template.index('<main')]
    body_suffix = template[template.index('</main>')+7:]
    candidates, models, bindings, additions, rows, sitemap = {}, [], [], [], [], []
    for contract in sources:
        rid, slug = contract['record_id'], contract['proposed_slug_from_root_assignment']
        rp = P/f'verification/root-editorial-{rid}-20261116.json'
        a = json.loads(readpin(rp, *ROOTS[rid])); assert a['proposed_slug'] == slug
        assert a['status'] == 'PRIVATE_COPY_ADOPTED_PUBLIC_ASSEMBLY_AND_LIVE_VERIFICATION_PENDING'
        assert a['publication_authority'] is False and a['follow_up'] is None
        owned = {lane: packet(a, lane) for lane in ('writer', 'independent_fact_fidelity')}
        for key in ('MAIN', 'model', 'whole_private_preview'): checkpin(a[key], P)
        d = (P/a['MAIN']['path']).parent
        model = json.loads((P/a['model']['path']).read_text())
        preview = (P/a['whole_private_preview']['path']).read_text()
        main_bytes = (P/a['MAIN']['path']).read_bytes().rstrip(b'\n')
        assert re.search(rb'<main\b.*?</main>', preview.encode(), re.S).group(0) == main_bytes
        assert model['follow_up'] is None and model['publication_authority'] is False
        if 'native_metadata_original' in model:
            assert model['native_metadata_original'] == json.loads((P/'papers'/rid/'sources/record.response.body').read_text())['metadata']
            assert model['native_record_files'] == json.loads((P/'papers'/rid/'sources/record.response.body').read_text())['files']
        original_head = re.search(r'<head>(.*?)</head>', preview, re.S).group(1)
        tags = Tags(original_head); abstract = tags.meta['DC.description']; description = tags.meta['description']
        assert canonical_abstract(contract['original_abstract_TeX']) == canonical_abstract(abstract)
        visible = re.search(r'<(?:section|p)\b[^>]*id="original-abstract".*?</(?:section|p)>', main_bytes.decode(), re.S).group(0)
        if visible.startswith('<section'): visible = re.search(r'<p>(.*?)</p>', visible, re.S).group(1)
        assert canonical_abstract(visible) == canonical_abstract(abstract)
        schema = json.loads(re.search(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', original_head, re.S).group(1))
        assert schema['abstract'] == abstract and description != abstract and description != contract['native_Description']
        url = ORIGIN+'/research/'+slug+'/'
        assets = contract['native_assets_in_original_order']; pdf = next(x['native_name'] for x in assets if x['native_name'].endswith('.pdf'))
        schema.update({'@id': url+'#article', 'url': url, 'mainEntityOfPage': url,
                       'sameAs': 'https://doi.org/'+contract['native_DOI'], 'description': description,
                       'creativeWorkStatus': 'Unrefereed preprint', 'encoding': []})
        for asset in assets:
            name = asset['native_name']; b = readpin(Path(asset['path']), asset['bytes'], asset['SHA256'])
            assert hashlib.md5(b).hexdigest() == asset['native_MD5'].removeprefix('md5:')
            candidates['public/research/'+slug+'/'+name] = b
            schema['encoding'].append({'@type':'MediaObject','name':name,'encodingFormat':'application/pdf' if name.endswith('.pdf') else 'application/zip','contentUrl':url+name,'contentSize':str(len(b))+' bytes','sameAs':f'https://zenodo.org/api/records/{rid}/files/{name}/content'})
        h = re.sub(r'<script[^>]*type="application/ld\+json"[^>]*>.*?</script>', '', original_head, flags=re.S)
        h = re.sub(r'<meta name="(?:robots|editorial-status)"[^>]*>\n?', '', h)
        h = re.sub(r'<link rel="stylesheet"[^>]*>\n?', '', h)
        h = re.sub(r'(<meta name="citation_pdf_url" content=")[^"]*(">)', lambda m:m[1]+url+pdf+m[2], h)
        h = re.sub(r'(<meta name="citation_author_orcid" content=")[^"]*(">)', lambda m:m[1]+'https://orcid.org/0009-0001-9320-500X'+m[2], h)
        extra = {'og:type':'article','og:title':contract['native_title'],'og:description':description,
                 'og:url':url,'article:published_time':contract['metadata_publication_date'],
                 'twitter:card':'summary','twitter:title':contract['native_title'],'twitter:description':description}
        for name, value in extra.items():
            if name not in tags.meta:
                attr = 'property' if name.startswith(('og:','article:')) else 'name'
                h += f'<meta {attr}="{name}" content="{html.escape(value, quote=True)}">\n'
        h += f'<meta name="robots" content="index, follow, max-image-preview:large">\n<link rel="canonical" href="{url}">\n<link rel="icon" href="/favicon.ico">\n<link rel="stylesheet" href="/research/research.css">\n'
        h += '<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('</','<\/')+'</script>\n'
        page = '<!DOCTYPE html>\n<html lang="en">\n<head>'+h+'</head>\n'+body_prefix+main_bytes.decode()+body_suffix
        public_tags = Tags(page)
        assert len(public_tags.ids)==len(set(public_tags.ids))
        assert public_tags.meta['DC.description']==abstract and public_tags.meta['citation_pdf_url']==url+pdf
        assert public_tags.meta['og:url']==url and 'noindex' not in h and 'editorial-status' not in h
        assert schema['name']==contract['native_title'] and schema['version']==contract['native_version'] and schema['datePublished']==contract['metadata_publication_date']
        assert schema['license']=='https://creativecommons.org/licenses/by/4.0/'
        candidates['public/research/'+slug+'/index.html'] = page.encode()
        bib = readpin(d/'preview/citation.bib')
        assert contract['native_DOI'].encode() in bib and contract['native_version'].encode() in bib
        candidates['public/research/'+slug+'/citation.bib'] = bib
        date = datetime.fromisoformat(contract['metadata_publication_date']).strftime('%-d %B %Y')
        rows.append(f'<li><a href="/research/{slug}/">{html.escape(contract["native_title"])}</a><br><span class="entry-meta">{date} · Unrefereed preprint</span><p>{html.escape(description)}</p><p><a href="/research/{slug}/{pdf}">PDF</a> · <a href="https://doi.org/{contract["native_DOI"]}">Zenodo</a></p></li>')
        additions.append({'@type':'ListItem','position':115+len(additions),'url':url,'name':contract['native_title']})
        sitemap.append(f'<url><loc>{url}</loc><lastmod>{contract["metadata_publication_date"]}</lastmod></url>')
        models.append({'record_id':rid,'canonical_url':url,'AA':None,'follow_up':None,'publication_authority':False,'whole_approved_MAIN_file':a['MAIN'],'included_MAIN_bytes':len(main_bytes),'included_MAIN_SHA256':digest(main_bytes),'MAIN_change':'external trailing LF padding removed only','ScholarlyArticle':schema,'full_abstract_DC_description':abstract,'short_description':description,'private_model':a['model']})
        bindings.append({'root_adoption':pin(rp),'writer_and_fact':owned,'approved_MAIN':a['MAIN'],'approved_model':a['model'],'approved_preview':a['whole_private_preview'],'approved_BibTeX':pin(d/'preview/citation.bib')})
    old_index = readpin(O/'BASELINE_RESEARCH_INDEX.html').decode(); old_sitemap = readpin(O/'BASELINE_SITEMAP.xml').decode()
    old_script = base['typed_script_complete_raw']; start = old_script.index('[',old_script.index('"itemListElement"'))
    old_array, consumed = json.JSONDecoder().raw_decode(old_script[start:]); end=start+consumed
    script = old_script[:end-1]+','+json.dumps(additions,ensure_ascii=False)[1:]+old_script[end:]
    script, count = re.subn(r'("numberOfItems"\s*:\s*)114\b',r'\g<1>118',script); assert count==1
    index = old_index.replace(old_script,script,1).replace(base['visible_items_raw'][-1],base['visible_items_raw'][-1]+'\n'+'\n'.join(rows),1)
    sitemap_text=old_sitemap.replace(base['sitemap_nodes_raw'][-1],base['sitemap_nodes_raw'][-1]+'\n'+'\n'.join(sitemap),1)
    for unit in base['visible_items_raw']: assert index.count(unit)==1
    for unit in base['sitemap_nodes_raw']: assert sitemap_text.count(unit)==1
    assert json.loads(script)['mainEntity']['itemListElement']==base['typed_items']+additions
    assert len(re.findall(r'<li\b[^>]*>.*?</li>',index,re.S))==118
    assert len(re.findall(r'<url\b[^>]*>.*?</url>',sitemap_text,re.S))==119
    candidates['public/research/index.html']=index.encode(); candidates['public/research/sitemap.xml']=sitemap_text.encode()
    assert sorted(candidates)==sorted(base['expected_target_paths']) and len(candidates)==18
    for path,b in candidates.items():
        if path.endswith('/index.html') and path!='public/research/index.html':
            for link in Tags(b.decode()).links:
                u=urlsplit(link)
                if u.scheme or u.netloc: continue
                dest=('public'+u.path) if u.path.startswith('/') else str(Path(path).parent / unquote(u.path))
                if not u.path: continue
                if u.path.endswith('/'): dest+='/index.html'
                assert dest in candidates or (W/dest).is_file(), (path,link,dest)
    if build:
        candidate=O/'candidate'; assert not candidate.exists()
        for name in ('PUBLIC_PAYLOADS.json','PUBLIC_MODELS.json','SOURCE_PRIVATE_PINS.json','DATA_RESULT.json'): assert not (O/name).exists()
        for path,b in candidates.items():
            p=candidate/path; p.parent.mkdir(parents=True,exist_ok=True)
            with p.open('xb') as f: f.write(b)
            p.chmod(0o644)
    closing=guards(base); assert opening==closing
    result={'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS_STATIC_DATA_ASSEMBLY_ONLY','build_requested':build,'candidate_files':18,'candidate_child_directories':6,'changes':{'A':16,'M':2},'counts_before':[711,114,115],'counts_after':[727,118,119],'all_four_approved_MAINs_exact_except_external_LF':True,'eight_assets_and_four_Bibs_exact':True,'all_old114_visible_and_typed_units_and115_sitemap_units_preserved':True,'all_complete_abstracts_visible_ScholarlyArticle_DC':True,'native_asset_order_and_absolute_public_metadata':True,'opening_guards':opening,'closing_guards':closing,'render_or_native_PDF_download_live_verification':False,'production_authority':False}
    if build:
        payloads=[]
        for path in sorted(candidates):
            q=pin(candidate/path); q['candidate_relative_path']='candidate/'+path; q['website_relative_path']=path; q['operation']='M' if path in ('public/research/index.html','public/research/sitemap.xml') else 'A'; payloads.append(q)
        for name,value in (('PUBLIC_PAYLOADS.json',payloads),('PUBLIC_MODELS.json',models),('SOURCE_PRIVATE_PINS.json',bindings),('DATA_RESULT.json',result)):
            with (O/name).open('x') as f: json.dump(value,f,indent=2,ensure_ascii=False); f.write('\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
