"""Default pure terminal custody/positive checks, no project imports.

No network, subprocess, source/scientific execution, renderer/fault replay,
bytecode generation, or writes. --preseal omits only the final owned seal.
"""
import hashlib
import html
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

A = pathlib.Path(__file__).resolve().parent
P = A.parent.parent
checks = 0


def need(ok, why):
    global checks
    checks += 1
    if not ok:
        raise ValueError(why)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read(p):
    need(p.is_file() and not p.is_symlink(), 'regular nonsymlink file: ' + str(p))
    return p.read_bytes()


def obj(p):
    return json.loads(read(p))


def same(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return list(a) == list(b) and all(same(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def names(root):
    paths = list(root.rglob('*'))
    need(not any(p.is_symlink() for p in paths), 'no namespace symlinks: ' + str(root))
    return sorted(str(p) for p in paths if p.is_file())


def main(text):
    found = re.findall(r'<main(?: id="main")?>.*?</main>', text, re.S)
    need(len(found) == text.count('<main') == text.count('</main>') == 1, 'one complete main')
    return found[0]


def structured(text):
    found = list(re.finditer(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', text, re.S))
    need(len(found) == 1, 'one JSONLD object')
    return found[0], json.loads(found[0][1])


need(sys.argv[1:] in ([], ['--preseal']), 'bounded terminal option')
preseal = sys.argv[1:] == ['--preseal']
source, website, core = [obj(A / n) for n in ['SOURCE_INPUTS.json','WEBSITE_BASELINE.json','CORE_INPUTS.json']]
contract = obj(A / 'STAGE_CONTRACT.json')
opaque_rows = obj(A / 'NON_JSON_INPUTS.json')['files']
opaque = {r['path']: r for r in opaque_rows}
need(len(opaque) == 1 and next(iter(opaque)).endswith('/23333002/reviews/scope/native-isolated/native.stdout.json') and
     opaque_rows[0]['bytes'] == 0 and opaque_rows[0]['SHA256'] == sha(b''), 'exact preserved empty historical output')
rows = source['files'] + website['public_files'] + website['site_configs'] + [website['installation_receipt']] + core['files'] + core['authority_metadata']
frozen, typed_objects = {}, 0
for row in rows:
    b = read(A / row['blob'])
    need(len(b) == row['bytes'] and sha(b) == row['SHA256'], 'whole private frozen byte pin')
    need(read(pathlib.Path(row['path'])) == b, 'fresh original whole-byte identity: ' + row['path'])
    frozen[row['path']] = b
    if row['path'].endswith('.json') or pathlib.Path(row['path']).name in {
            'record.response.body','latest.response.body.redirect-01','versions-page001.response.body','files.response.body'}:
        if row['path'] in opaque:
            need(len(b) == opaque[row['path']]['bytes'] and sha(b) == opaque[row['path']]['SHA256'],
                 'whole opaque historical failure bytes preserved')
            try:
                json.loads(b)
            except json.JSONDecodeError as e:
                need(str(e) == opaque[row['path']]['actual_JSON_parse_error'], 'original parse failure retained exactly')
            else:
                raise ValueError('historical non-JSON output silently repaired')
        else:
            original = json.loads(read(pathlib.Path(row['path'])))
            need(same(original, json.loads(b)), 'whole original typed/key/list/order/null/history object')
            typed_objects += 1
for n in source['namespaces']:
    need(names(pathlib.Path(n['root'])) == n['files'] and len(n['files']) == n['count'],
         'complete source/editorial/review namespace: ' + n['root'])
old613 = source['fresh_guarded_originals_613']['files']
need(len(old613) == 613, 'whole613 originals')
for row in old613:
    need(sha(frozen[row['path']]) == row['SHA256'] and len(frozen[row['path']]) == row['bytes'], 'original613 pins')
need([n['count'] for n in source['namespaces'] if n['root'].endswith('/reviews/editorial')] == [56,62,77],
     'complete195 editorial files including125nested seals and3root terminal files')
w = pathlib.Path(website['website_root'])
need(names(w / 'public') == sorted(r['path'] for r in website['public_files']), 'entire593 public namespace')
need(website['root_GO_commit'] == 'e2e064c48755452a56c2a31207fb12d7e55074fb' and
     contract['baseline_counts'] == [593,87,88] and contract['virtual_counts'] == [605,90,91], 'current root GO only')
need(core['historical_qualification_preserved'] is True, '17 original plus only authorized checkpoint qualification')
need(core['original17_files_unchanged'] == 17 and len(core['files']) == 18 and
     core['current_checkpoint_SHA256'] == '405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0' and
     core['claim_all18_unchanged_from_original_baseline'] is False, 'exact bounded core qualification')
need(sorted(str(p) for p in (P/'scripts').glob('*.py')) == core['scripts_namespace'], 'whole17-script namespace')
need('inputs/' in read(A / '.gitignore').decode().splitlines() and
     'blobs/' in read(A / '.gitignore').decode().splitlines(), 'entire raw directories ignored')

overlay = obj(A / 'OVERLAY_MANIFEST.json')['files']
need(len(overlay) == len({r['path'] for r in overlay}) == 14, 'exact14 overlay paths')
need([r['path'] for r in overlay] == contract['overlay_paths'], 'contract whole path order')
paired = {}
for r in overlay:
    rel = pathlib.PurePosixPath(r['path'])
    need(not rel.is_absolute() and '..' not in rel.parts, 'bounded overlay relative path')
    left = read(A / 'candidate-a/public' / r['path'])
    right = read(A / 'candidate-b/public' / r['path'])
    need(left == right and len(left) == r['bytes'] and sha(left) == r['SHA256'], 'actual normal/-O complete buffer bytes')
    paired[r['path']] = left
for name in ['candidate-a','candidate-b']:
    need(names(A / name / 'public') == sorted(str(A / name / 'public' / r['path']) for r in overlay),
         'whole14 candidate namespace, no extra paths')
for prefix, optimize in [('BUILD_NORMAL',0),('BUILD_OPTIMIZED',1)]:
    report = obj(A / (prefix + '.stdout.json'))
    need(read(A / (prefix + '.exitcode')).strip() == b'0' and read(A / (prefix + '.stderr')) == b'', 'actual full build exit0')
    need(report['optimization_level'] == optimize and report['rendered_all14_buffers_and_wrote_exact_bytes'] is True,
         'actual renderer under distinct normal/-O, not checker-only coverage')
controls = obj(A / 'INTEGRATION_CONTROLS.stdout.json')
need(controls['fault_count'] == 6 and all(x['rejected'] is True for x in controls['new_memory_only_faults']), 'six recorded bounded integration falsifiers')
need(read(A / 'INTEGRATION_CONTROLS.exitcode').strip() == b'0' and read(A / 'INTEGRATION_CONTROLS.stderr') == b'', 'recorded controls exit0')

article_details = []
interfaces = ['config/publication.json','configs/publication.json','publication.json']
ids = ['23578599','23423736','23333002']
for rid, config_rel in zip(ids, interfaces):
    ed = P / 'papers' / rid / 'reviews/editorial'
    c = json.loads(frozen[str(ed / config_rel)])
    original = frozen[str(ed / 'candidate/index.html')].decode()
    adopted = main(original)
    expected_main = adopted.replace('<main>', '<main id="main">', 1) if adopted.startswith('<main>') else adopted
    base = 'research/' + c['slug'] + '/'
    text = paired[base + 'index.html'].decode()
    need(main(text) == expected_main, 'whole adopted main with only permitted id addition')
    need(text.count('<style>') == 1 and '<style>' + contract['nonhiding_supplemental_css'] + '</style>' in text,
         'exact supplemental CSS, no hiding addition')
    for tag in re.findall(r'<[a-z][a-z0-9]*[^<>]*>', main(text)):
        attribute_names = re.sub(r'="[^"]*"', '=""', tag)
        need(not re.search(r'\s(?:hidden|style|on[a-z]+)(?:=|\s|>)', attribute_names),
             'no actual main-tag hiding or event attributes')
    url = 'https://aleckriebel.com/' + base
    need('<link rel="canonical" href="' + url + '">' in text and
         '<meta name="robots" content="index,follow">' in text and 'noindex' not in text, 'real canonical/indexfollow')
    for key, value in [('citation_title',c['title']),('citation_author','Alec Kriebel'),
                       ('citation_publication_date',c['publication_date'].replace('-','/')),
                       ('citation_version',c['version']),('citation_doi',c['doi']),
                       ('citation_pdf_url',url+'assets/'+c['pdf_filename'])]:
        need('<meta name="' + key + '" content="' + html.escape(value) + '">' in text, 'accurate complete citation head ' + key)
    am = re.search(r'<h2>Original abstract</h2>\s*<p(?: class="math")?>(.*?)</p>', main(text), re.S)
    need(am is not None and html.unescape(am[1]) == c['abstract'] and text.count('<h2>Original abstract</h2>') == 1,
         'one exact complete visible original abstract')
    _, graph = structured(text)
    page, article = graph['@graph']
    need(page['@type'] == 'WebPage' and article['@type'] == 'ScholarlyArticle' and
         page['mainEntity']['@id'] == article['@id'] == url+'#article' and
         article['mainEntityOfPage']['@id'] == page['@id'] == url+'#page', 'complete mutually linked page/article graph')
    need(page['dateCreated'] == page['dateModified'] == '2026-11-15' and
         article['datePublished'] == c['publication_date'] and article['abstract'] == c['abstract'],
         'separate build dates and original publication/full abstract')
    need(article['creativeWorkStatus'] == 'Unrefereed preprint', 'explicit accurate scholarly review status')
    _, old_article = structured(original)
    changed = {'@id','url','mainEntityOfPage','inLanguage','isAccessibleForFree','encoding'}
    for key in old_article:
        if key not in changed:
            need(key in article and same(old_article[key],article[key]), 'original scholarly field preserved ' + key)
    ready = json.loads(frozen[str(P / 'papers' / rid / 'sources/SOURCE_READY.json')])
    assets = ready['all_native_assets_in_original_order']
    need(len(assets) == len(article['encoding']) == 2, 'complete native asset encoding scope')
    for native, encoding in zip(assets,article['encoding']):
        name = native['original_api_file_object']['key']
        b = paired[base + 'assets/' + name]
        need(b == frozen[native['path']] == frozen[str(ed / 'candidate/assets' / name)], 'whole native/output/candidate PDFZIP identity')
        need(hashlib.md5(b).hexdigest() == native['original_api_file_object']['checksum'].split(':',1)[1], 'original native MD5')
        need(encoding['contentUrl'] == url+'assets/'+name and encoding['sameAs'] == native['original_api_file_object']['links']['self'], 'local and exact native original encoding URLs')
        if rid == '23578599' and name.endswith('.zip'):
            need('license' not in encoding, 'Nash heterogeneous ZIP not given a blanket prose license')
        else:
            need(encoding['license'] == 'https://creativecommons.org/licenses/by/4.0/', 'actual authored asset license')
    need(paired[base+'assets/citation.bib'] == frozen[str(ed/'candidate/assets/citation.bib')], 'whole adopted BibTeX unchanged')
    if rid == '23578599':
        need(main(text).count('<table>') == 1 and main(text).count('<tbody>') == 1, 'actual Nash table')
    if rid == '23333002':
        frame = re.search(r'<iframe\b[^>]*>',main(text))[0]
        need('width="100%"' in frame and 'height="850"' in frame, 'actual Robinson raw dimensions intact')
    need(c['follow_up'] is None and c['canonical_url'] is None and c['AA'] is None, 'original immutable config nulls unchanged')
    article_details.append({'record_id':rid,'main_sha256':sha(expected_main.encode()),'original_date':c['publication_date']})

old_index = frozen[str(w/'public/research/index.html')].decode()
new_index = paired['research/index.html'].decode()
old_m, old_data = structured(old_index)
new_m, new_data = structured(new_index)
need(same(old_data['mainEntity']['itemListElement'],new_data['mainEntity']['itemListElement'][:87]), 'all87 typed ordered prior ListItems')
need(new_data['mainEntity']['numberOfItems'] == len(new_data['mainEntity']['itemListElement']) == 90, 'actual90 typed index')
addition = contract['index_additions']
need(new_index.count(addition) == 1, 'one visible triplet addition')
restored = new_index.replace(addition,'',1)
rm, _ = structured(restored)
need(restored[:rm.start(1)]+old_m[1]+restored[rm.end(1):] == old_index, 'all prior visible index/scaffold bytes unchanged')
sitemap = paired['research/sitemap.xml']
addition = contract['sitemap_additions'].encode()
need(sitemap.count(addition) == 1 and sitemap.replace(addition,b'',1) == frozen[str(w/'public/research/sitemap.xml')],
     'all88 whole prior sitemap nodes and raw bytes retained')
need(len(ET.fromstring(sitemap)) == 91, 'actual91 sitemap nodes')
basepaths = {str(pathlib.Path(r['path']).relative_to(w/'public')) for r in website['public_files']}
need(len(basepaths|set(paired)) == 605 and len(basepaths-set(paired)) == 591 and
     basepaths&set(paired) == {'research/index.html','research/sitemap.xml'}, '605virtual and591unchanged public nonoverlays')

code = obj(A/'CODE_MANIFEST.json')['files']
need(len(code) <= 6, 'at most6 current self-contained helper bodies')
for r in code:
    b = read(A/r['path'])
    need(len(b) == r['bytes'] and sha(b) == r['SHA256'], 'entire current helper body pin')
owned_count = None
if not preseal:
    seal = obj(A/'FINAL_SEAL.json')
    need(sha(read(A/'OWNED_MANIFEST.json')) == seal['owned_manifest_SHA256'], 'whole owned manifest seal')
    owned = obj(A/'OWNED_MANIFEST.json')['files']
    actual = {str(pathlib.Path(p).relative_to(A)) for p in names(A)} - {'OWNED_MANIFEST.json','FINAL_SEAL.json'}
    need(actual == {r['path'] for r in owned} and len(owned) == len(actual), 'entire own namespace; exact root terminal exclusions only')
    for r in owned:
        b = read(A/r['path'])
        need(len(b) == r['bytes'] and sha(b) == r['SHA256'], 'whole owned payload')
    for name, h in seal['critical_files_SHA256'].items():
        need(sha(read(A/name)) == h, 'critical final artifact')
    need(obj(A/'READY.json')['production_install_authorized'] is False and
         obj(A/'VERDICT.json')['follow_up'] is None, 'separate root installation authority and null follow-up')
    owned_count = len(owned)
print(json.dumps({'mode':'preseal' if preseal else 'final','positive_custody_checks':checks,
                  'frozen_source_review_authority_files':len(source['files']),'original613_intact':613,
                  'complete_editorial_namespace_files':195,'source_review_namespace_guards':9,
                  'whole_original_typed_ordered_objects_compared':typed_objects,'whole_paired_overlay_files':14,
                  'opaque_original_empty_historical_failures_preserved':len(opaque),
                  'public_baseline':593,'virtual_public':605,'index':90,'sitemap':91,'unrelated_public_intact':591,
                  'core_files':len(core['files']),'helper_bodies':len(code),'owned_payloads':owned_count,
                  'articles':article_details,'renderer_or_fault_campaign_replayed':False,
                  'source_program_import_or_execution':False,'network_subprocess_or_writes':False},ensure_ascii=False,indent=2))
