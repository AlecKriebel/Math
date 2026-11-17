"""One explicit private data-only build. No subprocess, Git, network or native code."""
from pathlib import Path
from datetime import datetime, timezone
from html import escape
from html.parser import HTMLParser
import hashlib
import json
import re
import shutil
import stat
import sys
import xml.etree.ElementTree as ET

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
O = P / 'verification/wreath-dyadic-stress-stage-sol-20261116'
AUTH = P / 'verification/root-wreath-dyadic-stress-editorial-adoption-20261116.json'
AUTH_SHA = '4eb948c3cec10111bceac2170efe5922085f1f498fa37d8f8eaf805c6863ddf1'
B_SEAL = P / 'verification/wreath-dyadic-stress-stage-audit-sol-20261116/INITIAL_SEAL.json'
B_SHA = 'e8097351d7f5444520b9b7181d34f7848b589288013296ec5393df9a0d94239a'
CFG = [
    (164, 23203143, 'wreath-planar', 'wreath-products-planar-triangle-bounds', 'article.html', 'public-main.html', 'page-model.json', ['assets/preprint.pdf', 'assets/wreath-planar-verification-v1.0.0-revised.zip'], (121, 20)),
    (177, 23205181, 'dyadic-random-cone', 'sharp-dyadic-threshold-random-cone', 'candidate/research/sharp-dyadic-threshold-random-cone/index.html', 'MAIN.html', 'MODEL.json', ['paper.pdf', 'source-and-audit.zip'], (69, 10)),
    (183, 23331540, 'full-stress-labelled-graph', 'full-stress-stratifications-labelled-graph', 'article.html', 'public-main.html', 'page-model.json', ['assets/full_stress_stratifications_determine_a_labelled_graph.pdf', 'assets/full_stress_stratifications_source_verification_v1.zip'], (133, 14)),
]
MANIFESTS = [
    ('MANIFEST.json', 'payload_files'), ('OWNED_MANIFEST.json', 'files'),
    ('OWNED_MANIFEST.json', 'files'), ('MANIFEST.json', 'files'),
    ('MANIFEST.json', 'payload_files'), ('OWNED_MANIFEST.json', 'files'),
    ('OWNED_MANIFEST.json', 'files'),
]

def need(test, message):
    if not test:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def pin(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Nonregular object: ' + str(path))
    data = path.read_bytes()
    return dict(bytes=len(data), SHA256=sha(data), mode=format(stat.S_IMODE(info.st_mode), '04o'))

def snapshot(root):
    need(root.is_dir() and not root.is_symlink(), 'Invalid root: ' + str(root))
    files, dirs = [], []
    for path in sorted(root.rglob('*')):
        info = path.lstat()
        rel = path.relative_to(root).as_posix()
        if stat.S_ISDIR(info.st_mode):
            dirs.append(dict(path=rel, mode=format(stat.S_IMODE(info.st_mode), '04o')))
        else:
            files.append(dict(path=rel, **pin(path)))
    return dict(root=str(root), root_mode=format(stat.S_IMODE(root.stat().st_mode), '04o'), files=files, directories=dirs, regular_files=len(files), child_directories=len(dirs))

def mode(value):
    return value if type(value) is int else int(value, 8)

def store(name, value):
    with (O / name).open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')

def raw_write(path, data, bits=0o644):
    with path.open('xb') as stream:
        stream.write(data)
    path.chmod(bits)

def validate_manifest(root, name, rows_key, snap):
    obj = json.loads((root / name).read_text())
    observed = {row['path']: row for row in snap['files']}
    controls = {'FINAL.json', name}
    seen = set()
    for row in obj[rows_key]:
        rel = row['path']
        need(rel not in seen and rel in observed, 'Manifest duplicate/missing: ' + str(root / rel))
        seen.add(rel)
        need(int(observed[rel]['mode'], 8) == mode(row['mode']), 'Manifest file mode: ' + rel)
        if row.get('terminal_control') is True:
            need(rel in controls and 'SHA256' not in row and 'bytes' not in row, 'Unexpected control row')
        else:
            need(observed[rel]['SHA256'] == row['SHA256'] and observed[rel]['bytes'] == row['bytes'], 'Manifest bytes: ' + rel)
    need(set(observed) == seen | controls, 'Manifest complete file extent: ' + str(root))
    expected_dirs = {row['path']: mode(row['mode']) for row in obj['directories'] if row['path'] != '.'}
    need(expected_dirs == {row['path']: int(row['mode'], 8) for row in snap['directories']}, 'Manifest topology: ' + str(root))
    if root.name == 'dyadic-random-cone-fact-sol-20261116':
        need('root_mode' not in obj, 'Changed dyadic fact manifest schema')
    else:
        need(mode(obj['root_mode']) == int(snap['root_mode'], 8), 'Manifest root mode')

def prep_guard():
    need(pin(O / 'PREP_INPUT_SEAL.json')['SHA256'] == '39ded8fe882a58f85c5e61d39dfd2f6eb5aeac9ec4ac52b038d9259a42c5a4a1', 'Original preparation seal')
    need(pin(O / 'PREP_MANIFEST.json')['SHA256'] == '2044ccac276bd7b7b1edac9bb0752ae3583091847ad02c926f4de09cfe282503', 'Original preparation manifest')
    obj = json.loads((O / 'PREP_MANIFEST.json').read_text())
    need(len(obj['files']) == 15, 'Preparation extent')
    rows = []
    for row in obj['files']:
        actual = pin(O / row['path'])
        need(actual['mode'] == row['mode'], 'Preparation file mode')
        if row.get('terminal_control') is not True:
            need(actual['bytes'] == row['bytes'] and actual['SHA256'] == row['SHA256'], 'Preparation payload changed')
        rows.append(dict(path=row['path'], **actual))
    return rows

def native_git(root):
    git = root / '.git'
    need(git.is_dir() and not git.is_symlink(), 'Expected native Git directory')
    head = (git / 'HEAD').read_text()
    need(head.startswith('ref: refs/heads/'), 'Expected local branch HEAD')
    ref = head.strip()[5:]
    packed = {}
    packed_path = git / 'packed-refs'
    if packed_path.exists():
        for line in packed_path.read_text().splitlines():
            fields = line.split()
            if len(fields) == 2 and fields[1].startswith('refs/heads/'):
                packed[fields[1]] = dict(OID=fields[0], raw_line=line)
    loose_root = git / 'refs/heads'
    loose = snapshot(loose_root) if loose_root.is_dir() else None
    branch_path = git / ref
    oid = branch_path.read_text().strip() if branch_path.is_file() else packed[ref]['OID']
    return dict(root=str(root), HEAD=dict(raw=head, **pin(git / 'HEAD')), index=pin(git / 'index'), config=pin(git / 'config'), local_branch=ref, local_branch_OID=oid, loose_local_heads=loose, packed_local_heads=packed,
                remote_tracking_FETCH_HEAD_and_nonlocal_packed_lines_deliberately_not_bound=True)

class HeadMeta(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta = {}
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'meta' and ('name' in d or 'property' in d):
            key = d.get('name', d.get('property'))
            need(key not in self.meta, 'Duplicate meta key: ' + key)
            self.meta[key] = d.get('content')

def activate(article, canonical, native_rels):
    matches = list(re.finditer(r'<head>.*?</head>', article, re.S))
    need(len(matches) == 1, 'Exactly one complete head')
    match = matches[0]
    old = match.group()
    before_meta = HeadMeta(); before_meta.feed(old)
    script_pattern = r'(<script type="application/ld\+json">)(.*?)(</script>)'
    scripts = list(re.finditer(script_pattern, old, re.S))
    need(len(scripts) == 1, 'Exactly one scholarly schema')
    schema_old = json.loads(scripts[0].group(2))
    need(schema_old['@type'] == 'ScholarlyArticle' and len(schema_old['encoding']) == 2, 'Scholarly schema shape')
    schema_new = json.loads(json.dumps(schema_old))
    schema_new.update(url=canonical, mainEntityOfPage={'@type': 'WebPage', '@id': canonical})
    schema_new['@id'] = canonical + '#article'
    for item, rel in zip(schema_new['encoding'], native_rels):
        item['contentUrl'] = canonical + rel
    head = re.sub(script_pattern, lambda m: m.group(1) + json.dumps(schema_new, ensure_ascii=False) + m.group(3), old, flags=re.S)
    head, removed = re.subn(r'<meta name="(?:robots|googlebot)" content="[^"]*">\n?', '', head)
    need(removed in (1, 2), 'Private robots count')
    head, changed = re.subn(r'(<meta name="citation_pdf_url" content=")[^"]*(">)', lambda m: m.group(1) + canonical + native_rels[0] + m.group(2), head)
    need(changed == 1, 'Citation PDF count')
    head, changed = re.subn(r'<link rel="stylesheet" href="(?:research\.css|\.\./research\.css)">', '<link rel="stylesheet" href="/research/research.css">', head)
    need(changed == 1, 'Shared stylesheet count')
    need('rel="canonical"' not in head and 'property="og:url"' not in head and '<base' not in head, 'Unexpected existing active identity')
    insertion = '<link rel="canonical" href="' + canonical + '">\n<meta property="og:url" content="' + canonical + '">\n<meta property="og:site_name" content="Alec Kriebel">\n'
    head = head.replace('</head>', insertion + '</head>')
    after_meta = HeadMeta(); after_meta.feed(head)
    for key, value in before_meta.meta.items():
        if key in ('robots', 'googlebot'):
            need(key not in after_meta.meta, 'Private robots retained')
        elif key == 'citation_pdf_url':
            need(after_meta.meta[key] == canonical + native_rels[0], 'Activated citation PDF')
        else:
            need(after_meta.meta[key] == value, 'Unapproved old meta change: ' + key)
    for key in schema_old:
        if key != 'encoding':
            need(schema_new[key] == schema_old[key], 'Unapproved old schema change: ' + key)
    for previous, current in zip(schema_old['encoding'], schema_new['encoding']):
        need({k:v for k,v in previous.items() if k != 'contentUrl'} == {k:v for k,v in current.items() if k != 'contentUrl'}, 'Encoding metadata changed')
    need(schema_old['abstract'] == before_meta.meta['DC.description'] == after_meta.meta['DC.description'], 'Complete original abstract altered')
    result = article[:match.start()] + head + article[match.end():]
    need(result[result.index('</head>')+7:] == article[article.index('</head>')+7:], 'Body changed')
    return result, head, schema_new, dict(old_head_SHA256=sha(old.encode()), activated_head_SHA256=sha(head.encode()), complete_abstract_SHA256=sha(schema_old['abstract'].encode()), all_prior_meta_except_robots_and_PDF_unchanged=True, body_byte_identical=True)

def json_units(text):
    marker = re.search(r'"itemListElement"\s*:\s*(\[)', text)
    need(marker is not None, 'Collection list marker')
    start = marker.start(1)
    decoder = json.JSONDecoder()
    parsed, end = decoder.raw_decode(text, start)
    raw, pos = [], start + 1
    while True:
        while text[pos].isspace(): pos += 1
        if text[pos] == ']': break
        _, stop = decoder.raw_decode(text, pos)
        raw.append(text[pos:stop]); pos = stop
        while text[pos].isspace(): pos += 1
        if text[pos] == ',': pos += 1
        else: need(text[pos] == ']', 'Collection delimiter')
    need(pos == end - 1 and len(parsed) == len(raw), 'Collection raw unit boundaries')
    return parsed, raw, end

def append_aggregates(index, sitemap, items, today):
    script = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', index, re.S)
    need(script is not None, 'Index schema script')
    original_schema = json.loads(script.group(2))
    old_typed, old_raw, end = json_units(script.group(2))
    need(len(old_typed) == original_schema['mainEntity']['numberOfItems'] == 123, 'Original typed article count')
    new_units = [dict(**{'@type':'ListItem'}, position=124+i, url=item['canonical'], name=item['title']) for i,item in enumerate(items)]
    changed = script.group(2)[:end-1] + ', ' + ', '.join(json.dumps(item, ensure_ascii=False) for item in new_units) + script.group(2)[end-1:]
    changed, count = re.subn(r'("numberOfItems"\s*:\s*)123(?!\d)', r'\g<1>126', changed)
    need(count == 1, 'Index count substitution')
    updated = index[:script.start(2)] + changed + index[script.end(2):]
    ul = list(re.finditer(r'<ul>(.*?)</ul>', updated, re.S))
    need(len(ul) == 1, 'Exactly one visible index list')
    old_html = re.findall(r'<li\b[^>]*>.*?</li>', ul[0].group(1), re.S)
    need(len(old_html) == 123, 'Original visible article count')
    additions = []
    for item in items:
        date = datetime.strptime(item['date'], '%Y-%m-%d')
        human_date = str(date.day) + date.strftime(' %B %Y')
        additions.append('<li><a href="'+item['site_path']+'">'+escape(item['title'])+'</a><br><span class="entry-meta">'+human_date+' · '+escape(item['status'])+'</span><p>'+escape(item['description'])+'</p><p><a href="'+item['site_path']+item['native_rels'][0]+'">PDF</a> · <a href="https://doi.org/10.5281/zenodo.'+str(item['record'])+'">Zenodo</a></p></li>\n')
    updated = updated[:ul[0].end(1)] + '\n' + ''.join(additions) + updated[ul[0].end(1):]
    new_script = re.search(r'<script type="application/ld\+json">(.*?)</script>', updated, re.S).group(1)
    typed, raw, _ = json_units(new_script)
    new_html = re.findall(r'<li\b[^>]*>.*?</li>', re.search(r'<ul>(.*?)</ul>', updated, re.S).group(1), re.S)
    need(len(typed) == len(raw) == len(new_html) == 126 and typed[:123] == old_typed and raw[:123] == old_raw and new_html[:123] == old_html, 'Index ordered prefix not preserved')
    old_nodes = re.findall(r'<url\b[^>]*>.*?</url>', sitemap, re.S)
    need(len(old_nodes) == 124 and sitemap.count('</urlset>') == 1, 'Original sitemap count')
    appended = ''.join('<url><loc>'+item['canonical']+'</loc><lastmod>'+today+'</lastmod></url>\n' for item in items)
    new_sitemap = sitemap.replace('</urlset>', appended+'</urlset>')
    nodes = re.findall(r'<url\b[^>]*>.*?</url>', new_sitemap, re.S)
    need(len(nodes) == 127 and nodes[:124] == old_nodes, 'Sitemap raw ordered prefix')
    old_xml, new_xml = ET.fromstring(sitemap), ET.fromstring(new_sitemap)
    need([ET.tostring(e) for e in new_xml][:124] == [ET.tostring(e) for e in old_xml], 'Sitemap typed prefix')
    return updated, new_sitemap, dict(old_visible_units=old_html, old_typed_JSON_units=old_typed, old_raw_JSON_units=old_raw, old_raw_sitemap_nodes=old_nodes, new_typed_JSON_units=typed[123:], new_raw_sitemap_nodes=nodes[124:], counts_before=[123,123,123,124], counts_after=[126,126,126,127], all_old_ordered_prefixes_exact=True, sitemap_lastmod_is_private_build_date=today)

def build():
    need(sys.argv[1:] == ['--build-private-once'], 'Only explicit --build-private-once is supported')
    need(pin(AUTH)['SHA256'] == AUTH_SHA and pin(B_SEAL)['SHA256'] == B_SHA, 'Root adoption or independent pre-producer seal')
    authority = json.loads(AUTH.read_text())
    need(authority['one_fresh_private_data_only_stage_build_permitted_after_whole_actual_builder_read'] is True and authority['install_Git_push_deploy_Sheet_AA_authority'] is False, 'Authority scope')
    original_prep = prep_guard()
    inputs = []
    for check, (manifest, key) in zip(authority['checks'], MANIFESTS):
        root = Path(check['root']); snap = snapshot(root)
        need((snap['regular_files'], snap['child_directories']) == (check['files'],check['child_directories']), 'Adopted packet extent')
        need(pin(root / 'FINAL.json')['SHA256'] == check['FINAL_SHA256'] and pin(root / manifest)['SHA256'] == check['manifest_SHA256'], 'Adopted packet control pin')
        validate_manifest(root, manifest, key, snap)
        inputs.append(snap)
    need(len(inputs) == 7 and sum(s['regular_files'] for s in inputs) == 155, 'All seven adopted inputs')
    sources = [snapshot(P/'papers'/str(cfg[1])/'sources') for cfg in CFG]
    for cfg, snap in zip(CFG, sources):
        need((snap['regular_files'],snap['child_directories']) == cfg[-1], 'Original source extent')
    native = [native_git(Path('/Users/alec/Documents/Math')), native_git(W)]
    need(native[0]['local_branch'] == 'refs/heads/main', 'Math local main')
    need(native[1]['local_branch_OID'] == 'b767102567ad89aff909f9f11c0e8b7d72b75c40' and native[1]['index']['SHA256'] == '6e57311ffb524aabe230dec4962ebfa6983085674882606f5b8594aa1d4cee18', 'Actual W HEAD/index baseline')
    baseline = snapshot(W/'public')
    need((baseline['regular_files'],baseline['child_directories']) == (760,368), 'Public baseline extent')
    need(sum(Path(row['path']).name == '.DS_Store' for row in baseline['files']) == 17, 'Public ignored DSStore baseline')
    before = dict(preparation15=original_prep, native=native, public=baseline, adopted_inputs=inputs, original_sources=sources, root_authority=pin(AUTH), B_INITIAL_SEAL=pin(B_SEAL))
    store('BUILD_GUARDS_BEFORE.json', before)
    candidate = O/'candidate'
    candidate.mkdir(mode=0o755)
    public = candidate/'public'; public.mkdir(mode=int(baseline['root_mode'],8))
    for row in baseline['directories']:
        (public/row['path']).mkdir(mode=int(row['mode'],8))
    for row in baseline['files']:
        shutil.copy2(W/'public'/row['path'], public/row['path'])
    for row in baseline['directories']:
        (public/row['path']).chmod(int(row['mode'],8))
    public.chmod(int(baseline['root_mode'],8))
    items, target_rows, body_receipts = [], [], []
    for row, record, stem, slug, article_rel, main_rel, model_rel, rels, _ in CFG:
        root = P/('verification/'+stem+'-editorial-sol-20261116')
        article = (root/article_rel).read_bytes().decode('utf-8')
        main = (root/main_rel).read_bytes()
        need(article.encode().count(main.rstrip(b'\n')) == 1, 'Accepted whole MAIN span')
        model = json.loads((root/model_rel).read_text())
        site_path = '/research/'+slug+'/'
        canonical = 'https://aleckriebel.com'+site_path
        activated, head, schema, receipt = activate(article,canonical,rels)
        directory = public/'research'/slug; directory.mkdir(mode=0o755)
        if rels[0].startswith('assets/'):
            (directory/'assets').mkdir(mode=0o755)
        raw_write(directory/'index.html',activated.encode())
        raw_write(O/('ACTIVATED_HEAD_'+str(row)+'.html'),head.encode()+b'\n')
        for rel in rels:
            original = P/'papers'/str(record)/'sources/assets'/Path(rel).name
            writer_asset = root/(str(Path(article_rel).parent/rel) if row == 177 else rel)
            data = writer_asset.read_bytes()
            need(data == original.read_bytes(), 'Native original bytes: '+str(record)+' '+rel)
            raw_write(directory/rel,data,int(pin(writer_asset)['mode'],8))
        raw_write(directory/'citation.bib',(root/'citation.bib').read_bytes(),int(pin(root/'citation.bib')['mode'],8))
        need(main.rstrip(b'\n') in (directory/'index.html').read_bytes(), 'Activated whole MAIN preserved')
        for rel in ['index.html']+rels+['citation.bib']:
            target_rows.append(dict(path='public/research/'+slug+'/'+rel, action='A', baseline=None, candidate=pin(directory/rel)))
        receipt.update(row=row,record=record,canonical=canonical,MAIN_file=pin(root/main_rel),MAIN_article_span_SHA256=sha(main.rstrip(b'\n')),native_order=rels,Bib=pin(root/'citation.bib'))
        body_receipts.append(receipt)
        items.append(dict(row=row,record=record,site_path=site_path,canonical=canonical,title=model['title'],description=model['description'] if row == 177 else model['meta_description'],date=model['publication_date'],status=schema['creativeWorkStatus'],native_rels=rels))
    old_index=(W/'public/research/index.html').read_bytes().decode('utf-8'); old_sitemap=(W/'public/research/sitemap.xml').read_bytes().decode('utf-8')
    raw_write(O/'BASELINE_INDEX.html',old_index.encode())
    raw_write(O/'BASELINE_SITEMAP.xml',old_sitemap.encode())
    today=datetime.now(timezone.utc).date().isoformat()
    new_index,new_sitemap,aggregate=append_aggregates(old_index,old_sitemap,items,today)
    (public/'research/index.html').write_bytes(new_index.encode('utf-8'))
    (public/'research/sitemap.xml').write_bytes(new_sitemap.encode('utf-8'))
    for rel in ('research/index.html','research/sitemap.xml'):
        target_rows.append(dict(path='public/'+rel,action='M',baseline=pin(W/'public'/rel),candidate=pin(public/rel)))
    successor=snapshot(public)
    need((successor['regular_files'],successor['child_directories']) == (772,373), 'Prospective public extent')
    old_files={row['path']:row for row in baseline['files']}; new_files={row['path']:row for row in successor['files']}
    modified={'research/index.html','research/sitemap.xml'}
    for rel,previous in old_files.items():
        need(rel in new_files and previous['mode']==new_files[rel]['mode'], 'Old public file/mode absent')
        if rel not in modified: need(new_files[rel]==previous,'Untargeted old public bytes changed: '+rel)
    old_dirs={row['path']:row for row in baseline['directories']}; new_dirs={row['path']:row for row in successor['directories']}
    need(all(new_dirs.get(rel)==value for rel,value in old_dirs.items()), 'Old directory mode changed')
    need(len(set(new_dirs)-set(old_dirs))==5 and len(target_rows)==14 and sum(row['action']=='A' for row in target_rows)==12, 'Exact target/topology extent')
    need(set(new_files)-set(old_files)=={row['path'][7:] for row in target_rows if row['action']=='A'}, 'Exact added files')
    after=dict(preparation15=prep_guard(),native=[native_git(Path('/Users/alec/Documents/Math')),native_git(W)],public=snapshot(W/'public'),adopted_inputs=[snapshot(Path(check['root'])) for check in authority['checks']],original_sources=[snapshot(P/'papers'/str(cfg[1])/'sources') for cfg in CFG],root_authority=pin(AUTH),B_INITIAL_SEAL=pin(B_SEAL))
    store('BUILD_GUARDS_AFTER.json',after)
    need(after==before,'Input/native/website/preparation source guard changed')
    store('AGGREGATE_PRESERVATION.json',aggregate)
    store('BODY_AND_HEAD_RECEIPTS.json',body_receipts)
    store('PUBLIC_PAYLOADS.json',dict(schema='exact-private-stage-target-plan-v1',targets=target_rows,new_directories=sorted(set(new_dirs)-set(old_dirs)),new_directory_count=5,additions=12,modifications=2,production_authority=False))
    store('PROSPECTIVE_PUBLIC.json',successor)
    store('BUILD_RESULT.json',dict(UTC=datetime.now(timezone.utc).isoformat(),status='READY_PRIVATE_STAGE_DATA_ONLY',ordinary_builder_invocations=1,root_adoption_SHA256=AUTH_SHA,B_INITIAL_SHA256=B_SHA,counts_before=[760,368,123,124],counts_after=[772,373,126,127],target_leaves=14,new_directories=5,complete_body_MAIN_abstract_Bib_native_bytes_preserved=True,all_old_public_files_modes_and_17_DSStore_preserved=True,all_old_index_visible_typed_raw_and_sitemap_prefixes_preserved=True,all_source_private_prep_native_and_W_guards_unchanged=True,private_candidate_only=True,production_authority=False,browser_render_live_PDF_download_certification=False,follow_up=None))
    print('READY_PRIVATE_STAGE_DATA_ONLY: 14 targets (12A2M), 5 new directories; 760/368/123/124 -> 772/373/126/127; exact old prefixes and native/input guards preserved.')

if __name__ == '__main__':
    build()
