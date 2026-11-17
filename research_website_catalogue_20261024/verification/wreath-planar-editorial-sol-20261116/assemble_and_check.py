"""One fixed private data assembly/static pass. No renderer, network, Git or source-code execution."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
from urllib.parse import urlsplit, unquote
import datetime, hashlib, json, os, re, stat

R = Path(__file__).resolve().parent
P = R.parents[1]
S = P / 'papers/23203143/sources'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
F = P / 'verification/wreath-planar-regularization-sol-20261116'

def require(test, message):
    if not test:
        raise RuntimeError(message)

def pin(p, root=None):
    st = p.lstat()
    require(stat.S_ISREG(st.st_mode), 'not regular: '+str(p))
    b = p.read_bytes()
    return dict(path=p.relative_to(root).as_posix() if root else str(p), bytes=len(b),
                SHA256=hashlib.sha256(b).hexdigest(), mode=oct(stat.S_IMODE(st.st_mode)))

def inventory(root):
    files, dirs = [], []
    for p in sorted(root.rglob('*')):
        st = p.lstat()
        if stat.S_ISREG(st.st_mode):
            files.append(pin(p, root))
        elif stat.S_ISDIR(st.st_mode):
            dirs.append(dict(path=p.relative_to(root).as_posix(), mode=oct(stat.S_IMODE(st.st_mode))))
        else:
            raise RuntimeError('unexpected topology: '+str(p))
    return files, dirs

def create(name, data):
    p = R / name
    with p.open('xb') as f:
        f.write(data.encode('utf-8') if isinstance(data, str) else data)

def create_json(name, value):
    create(name, json.dumps(value, ensure_ascii=False, indent=2)+'\n')

for name in ('article.html', 'head.html', 'SOURCE_GUARDS.json', 'STATIC_CHECK.json', 'REPORT.md', 'MANIFEST.json', 'FINAL.json', 'research.css', 'assets', 'original-objects'):
    require(not os.path.lexists(R / name), 'already exists: '+name)
require(pin(F / 'FINAL.json')['SHA256']=='0d5f7abaad5b281481573b14c7c0622e1a1cdd910fa567fc7fba3cb6677e60b9', 'focused packet control drift')
require(pin(F / 'MANIFEST.json')['SHA256']=='6dfbed5eab6118b27e1dc8fc600e63beb797d0474e4fbb2adc8b8d9d8d48ee15', 'focused manifest drift')
fm = json.loads((F / 'MANIFEST.json').read_text())
fp = next(q for q in fm['payload_files'] if q['path']=='SOURCE_CUSTODY.json')
require(pin(F / 'SOURCE_CUSTODY.json', F)==fp, 'source guard reference drift')
old = json.loads((F / 'SOURCE_CUSTODY.json').read_text())
sf, sd = inventory(S)
require(sf==old['files'] and sd==old['directories'], 'source byte/mode/topology drift')
require(oct(stat.S_IMODE(S.lstat().st_mode))==old['root_mode'], 'source root mode drift')
require(len(sf)==121 and len(sd)==20, 'source finite extent differs')
clearance = P / 'verification/root-clearance-23203143-20261116.json'
root_review = P / 'papers/23203143/reviews/root/ROOT_REVIEW.md'
require(pin(clearance)['SHA256']=='0b9492a4ef2eb876d7de73d9c3f0a1b802d920d9da8385543161992ef0ed1c17', 'root clearance differs')
require(pin(root_review)['SHA256']=='698212c9dd5c216463cf851537685f2b4863750a137e1cb17fe8b1b630addcdd', 'root review differs')
authority = json.loads(clearance.read_text())
require(authority['scientific_disposition']=='PASS_FULL_ORIGINAL_BOTH_CONSEQUENCES' and authority['publication_or_AA_authority'] is False, 'clearance scope differs')
model = json.loads((R / 'page-model.json').read_text())
record = json.loads((S / 'record.response.body').read_text())
native = record['metadata']
for field in ('title', 'version', 'publication_date', 'doi'):
    actual = model['native_version'] if field=='version' else model[field]
    require(actual==native[field], 'native model field differs: '+field)
require(model['record_created']==record['created'] and model['record_updated']==record['updated'], 'record dates differ')
require(all(model[k] is None for k in ('canonical_url', 'base_url', 'production_url', 'AA', 'follow_up')), 'private/null gate differs')
require(model['publication_authority'] is False and model['robots']=='noindex, nofollow', 'private authority differs')
target = W / 'public/research' / model['deployment_proposal']['slug']
require(not os.path.lexists(target), 'proposed public slug already exists')
css = W / 'public/research/research.css'
css_before = pin(css)
require(css_before['bytes']==1170, 'shared stylesheet size differs')
tex = (S / 'published-source/container-001/tree/publication/preprint.tex').read_text()
original_abstract = re.search(r'\\begin\{abstract\}\s*(.*?)\s*\\end\{abstract\}', tex, re.S).group(1)
rendered = original_abstract
for a, b in (("$H$", "H"), (r'$C_2\wrp H$', 'C₂ wr H'),
             (r'$L_2=2/\sqrt3$', 'L₂ = 2/√3'), (r'$P_2=4/3$', 'P₂ = 4/3'),
             ('Cohn--de Laat--Salmon', 'Cohn–de Laat–Salmon')):
    rendered = rendered.replace(a, b)
rendered = ' '.join(rendered.split())
require(rendered==model['abstract'], 'full original abstract differs')
require([q['name'] for q in model['native_asset_order']]==[q['key'] for q in record['files']], 'native asset order differs')
for directory in ('assets', 'original-objects'):
    (R / directory).mkdir()
copies = []
for q, native_file in zip(model['native_asset_order'], record['files']):
    src = S / 'assets' / q['name']
    b = src.read_bytes()
    require(len(b)==q['bytes']==native_file['size'], 'asset size differs')
    require('md5:'+hashlib.md5(b).hexdigest()==q['native_checksum']==native_file['checksum'], 'native checksum differs')
    create(q['local_path'], b)
    require((R / q['local_path']).read_bytes()==b, 'asset copy differs')
    copies.append(dict(source=pin(src, S), private_copy=pin(R / q['local_path'], R)))
base = 'published-source/container-001/tree/publication/'
originals = [('record.response.body', 'record.json'), ('files-23203143.response.body', 'files.json'),
             (base+'metadata.json', 'authored-metadata.json'),
             (base+'support/LICENSES.md', 'LICENSES.md'), (base+'support/LICENSE_CODE.txt', 'LICENSE_CODE.txt')]
for source, dest in originals:
    create('original-objects/'+dest, (S / source).read_bytes())
    copies.append(dict(source=pin(S / source, S), private_copy=pin(R / 'original-objects' / dest, R)))
create('research.css', css.read_bytes())

def meta(name, value, prop=False):
    return '<meta '+('property' if prop else 'name')+'="'+escape(name, quote=True)+'" content="'+escape(value, quote=True)+'">'

scholar = {'@context':'https://schema.org', '@type':'ScholarlyArticle', 'name':model['title'],
    'headline':model['title'], 'description':model['meta_description'], 'abstract':model['abstract'],
    'author':{'@type':'Person', 'name':model['author']['name'], 'identifier':model['author']['ORCID'],
              'affiliation':{'@type':'Organization', 'name':model['author']['affiliation']}},
    'datePublished':model['publication_date'], 'version':model['native_version'], 'inLanguage':'en',
    'identifier':{'@type':'PropertyValue', 'propertyID':'DOI', 'value':model['doi']},
    'creativeWorkStatus':model['status'], 'isAccessibleForFree':True,
    'license':'https://creativecommons.org/licenses/by/4.0/', 'sameAs':model['doi_url'],
    'keywords':native['keywords'], 'encoding':[{'@type':'MediaObject', 'name':q['name'],
        'contentUrl':q['local_path'], 'encodingFormat':q['format'], 'contentSize':str(q['bytes'])+' bytes',
        'sameAs':q['native_url']} for q in model['native_asset_order']]}
head = ['<head>', '<meta charset="utf-8">', '<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<title>'+escape(model['seo_title'])+'</title>', meta('description', model['meta_description']),
    meta('author', model['author']['name']), meta('robots', model['robots']), meta('googlebot', model['robots']),
    meta('citation_title', model['title']), meta('citation_author', model['author']['name']),
    meta('citation_author_orcid', model['author']['ORCID']), meta('citation_publication_date', model['publication_date'].replace('-', '/')),
    meta('citation_date', model['publication_date'].replace('-', '/')), meta('citation_version', model['native_version']),
    meta('citation_doi', model['doi']), meta('citation_language', 'en'), meta('citation_pdf_url', 'assets/preprint.pdf'),
    meta('DC.title', model['title']), meta('DC.description', model['abstract']), meta('DC.date', model['publication_date']),
    meta('DC.identifier', 'doi:'+model['doi']), meta('DC.rights', 'CC BY 4.0; newly authored Python code in the supporting package is MIT'),
    meta('og:type', 'article', True), meta('og:title', model['title'], True), meta('og:description', model['meta_description'], True),
    meta('article:published_time', model['publication_date'], True), meta('twitter:card', 'summary'),
    meta('twitter:title', model['title']), meta('twitter:description', model['meta_description']),
    '<link rel="stylesheet" href="research.css">',
    '<script type="application/ld+json">'+json.dumps(scholar, ensure_ascii=False)+'</script>', '</head>']
head = '\n'.join(head)+'\n'
create('head.html', head)
main = (R / 'public-main.html').read_text()
before = '<!DOCTYPE html>\n<html lang="en">\n'+head+'<body>\n<a class="skip-link" href="#main">Skip to content</a>\n<header><p class="site-title"><a href="https://aleckriebel.com/">Alec Kriebel</a></p><nav aria-label="Main navigation"><a href="https://aleckriebel.com/">Home</a> · <a href="https://aleckriebel.com/research/">Research</a></nav></header>\n'
after = '<footer><p><a href="https://aleckriebel.com/research/">Research index</a></p><p class="copyright">© 2026 Alec Kriebel</p></footer>\n</body>\n</html>\n'
create('article.html', before+main+after)

class Inspect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[]; self.links=[]; self.meta={}; self.abstract=[]; self.depth=0; self.capture=None
        self.iframe=[]; self.canonical=[]; self.bases=[]; self.scripts=[]
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if a.get('id')=='abstract-text':
            self.capture=tag
        if tag=='meta':
            self.meta[a.get('name', a.get('property'))]=a.get('content')
        if tag=='iframe':
            self.iframe.append(a.get('src'))
        if tag=='link' and a.get('rel')=='canonical':
            self.canonical.append(a.get('href'))
        if tag=='base':
            self.bases.append(a)
        if tag=='script':
            self.scripts.append(a.get('type'))
        for key in ('href','src'):
            if key in a:
                self.links.append(a[key])
    def handle_endtag(self, tag):
        if tag==self.capture:
            self.capture=None
    def handle_data(self, data):
        if self.capture:
            self.abstract.append(data)

html = (R / 'article.html').read_text()
v=Inspect(); v.feed(html)
require(len(v.ids)==len(set(v.ids)), 'duplicate HTML id')
require(' '.join(''.join(v.abstract).split())==rendered, 'visible complete abstract differs')
require(v.meta['DC.description']==rendered and scholar['abstract']==rendered, 'schema/DC abstract differs')
require(v.meta['citation_title']==native['title'] and v.meta['citation_version']==native['version'], 'citation source differs')
require(v.meta['robots']=='noindex, nofollow' and not v.canonical and not v.bases, 'private wrapper differs')
require('og:url' not in v.meta and not any(k in scholar for k in ('url','@id','mainEntityOfPage')), 'active production identity found')
require(v.iframe==['assets/preprint.pdf'] and v.scripts==['application/ld+json'], 'reader/script setup differs')
require(re.search(r'<main\b.*?</main>\n?', html, re.S).group(0)==main, 'whole MAIN assembly differs')
require(re.search(r'<head>.*?</head>\n?', html, re.S).group(0)==head, 'whole head assembly differs')
for link in v.links:
    u=urlsplit(link)
    if not u.scheme and not u.netloc:
        path=unquote(u.path)
        require(not path.startswith('/') and '..' not in Path(path).parts, 'unexpected private relative link: '+link)
        if path:
            require((R / path).is_file(), 'missing local link: '+link)
        if not path and u.fragment:
            require(u.fragment in v.ids, 'missing fragment: '+link)
require(v.links.index('assets/preprint.pdf')<v.links.index('assets/wreath-planar-verification-v1.0.0-revised.zip'), 'visible native order differs')
for q in model['substantive_upstream_inputs']:
    require(q['URL'] in v.links, 'missing substantive input link')
for forbidden in ('Original Zenodo description', 'ROOT_REVIEW', 'INITIAL_SEAL', '2,436', '102 residual', '51 finite nodes'):
    require(forbidden not in main, 'internal/duplicate narrative found: '+forbidden)
bib=(R / 'citation.bib').read_text()
require(all(x in bib for x in (native['title'], native['doi'], '1.0.0', '6 October 2026')), 'Bib native identity differs')
require(pin(R / 'research.css')['SHA256']==css_before['SHA256'] and pin(css)==css_before, 'CSS changed')
require(not os.path.lexists(target), 'proposed slug appeared')
af, ad=inventory(S)
require(af==sf and ad==sd, 'source drift during private pass')
for name in ('STATIC_CHECK.stdout.txt', 'STATIC_CHECK.stderr.txt'):
    require((R / name).read_bytes()==b'', 'unexpected literal pass stream')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
create_json('SOURCE_GUARDS.json', dict(UTC=now, source_root=str(S), root_mode=old['root_mode'], files=sf, directories=sd,
    source121files20dirs_unchanged_before_after=True, original_copies=copies,
    shared_W_css=css_before, shared_private_css=pin(R / 'research.css', R),
    proposed_W_slug_absent_before_after=str(target), root_clearance=pin(clearance, P), root_review=pin(root_review, P),
    prior_focused_manifest=pin(F / 'MANIFEST.json', P), prior_source_guard=pin(F / 'SOURCE_CUSTODY.json', P)))
create_json('STATIC_CHECK.json', dict(UTC=now, status='PASS_PRIVATE_DATA_AND_COPY_CONSISTENCY_ONLY', ordinary_passes=1,
    complete_native_abstract_visible_schema_DC_equal=True, whole_MAIN_and_head_exact=True,
    native_asset_order_bytes_MD5_and_copies_exact=True, native_dates_version_DOI_rights_objects_preserved=True,
    private_noindex_no_active_canonical_base_production_AA=True, shared1170CSS_exact=True,
    local_links_and_ids_valid=True, no_visible_duplicate_Description_or_internal_verification_narrative=True,
    source_regular_files=len(sf), source_child_directories=len(sd), no_source_drift=True,
    native_science_old_helper_network_Git_W_Sheet_render_CUA_or_server_actions=False,
    literal_stdout_bytes=0, literal_stderr_bytes=0,
    reader_limits='No desktop/mobile HTML render, native PDF display, live-link/download or deployment certification', follow_up=None))
create('REPORT.md', '# Private editorial handoff — row164 /23203143\n\nREADY for independent copy-fidelity review. Informed editorial work follows the actual full-original root clearance and whole root report; it is not another scientific family. The complete native abstract is visible and identical in ScholarlyArticle.abstract/DC.description after explicit TeX-to-Unicode math rendering. Both separate consequences, restricted regular C₂ lamp model, explicit split/kernel, exact distance-one Schwartz programs and planar infima limits are retained. OpenAI\'s two substantive inputs are prominent, with established Bradford–Fournier-Facio, embedding, CDLS/Cohn–Elkies/de Laat–Vallentin and lattice credit; no firstness or breakthrough is asserted.\n\nNative PDF then ZIP bytes/order, original publication6October2026/version1.0.0 versus record creation7OctoberUTC, ORCID, actual CC BY4/MIT split, complete raw native metadata/Description and licence objects are preserved. The native Description is archived rather than duplicated visibly. Passive contribution-based collaboration, concise AI/unrefereed status and follow-up null are included.\n\nOne fully read fixed data-only assembly/static pass succeeded. Source121files/20dirs match the frozen source guard before and after; CSS1170bytes is unchanged; local links, whole MAIN/head, Bib and private noindex/null identity gates passed. Literal stdout/stderr are empty. No new science/native/old-helper execution, render/browser/CUA/server/network, W/Git/Sheet/deployment/source/older-packet mutation or outreach occurred.\n\nThe proposed path is /research/wreath-products-planar-triangle-bounds/, absent in a readonly W check; it grants no canonical/AA or production authority. article.html is a private noindex document, with canonical/base/production/AA null in the model. A future wrapper requires separate adoption/integration/publication and actual reader/live verification.\n\nReader limits: eight native manuscript source pages were personally read previously as fresh own pixels and reused by reference; full current TeX/PDF text/native objects were reread. One initial combined text display truncated, followed by an untruncated whole PDF-text read. No new article desktop/mobile view, actual iframe/PDF-reader display, live link/download or deployment check is claimed. Whole raw primary-source science is outside this copy task; root authority and prior roles are disclosed.\n\nFinal packet includes all regular files, ignored/empty literal streams, byte hashes and modes, plus every child directory; terminal controls exclude only themselves. Preserve this packet for independent review; quiescent after FINAL.\n')
with (R / 'RESEARCH_LOG.md').open('a') as f:
    f.write('\n- '+now+' — 100% private preparation: sole data-only assembly/static pass completed; exact finite controls sealed next. No reader/render/live claim. Quiescent after FINAL for independent copy-fact review.\n')
files, dirs=inventory(R)
create_json('MANIFEST.json', dict(schema='whole-private-editorial-manifest-v1', UTC=now, payload_files=files,
    directories=dirs, root_mode=oct(stat.S_IMODE(R.lstat().st_mode)),
    exact_terminal_exclusions=['MANIFEST.json','FINAL.json'], includes_all_ignored_empty_bytes_modes=True))
create_json('FINAL.json', dict(schema='private-editorial-final-v1', UTC=now, record='23203143', row=164,
    status='FROZEN_PRIVATE_EDITORIAL_READY_FOR_INDEPENDENT_COPY_FACT',
    article=pin(R / 'article.html', R), whole_MAIN=pin(R / 'public-main.html', R), head=pin(R / 'head.html', R),
    model=pin(R / 'page-model.json', R), Bib=pin(R / 'citation.bib', R), report=pin(R / 'REPORT.md', R),
    manifest=pin(R / 'MANIFEST.json', R), static_check=pin(R / 'STATIC_CHECK.json', R),
    source_guards=pin(R / 'SOURCE_GUARDS.json', R), actual_authority=pin(clearance, P),
    informed_prior_roles_disclosed=True, new_scientific_family=False, root_editorial_adoption=False,
    static_passes=1, static_exit=0, literal_stdout=pin(R / 'STATIC_CHECK.stdout.txt', R), literal_stderr=pin(R / 'STATIC_CHECK.stderr.txt', R),
    native_assets=copies[:2], source121files20dirs_unchanged=True,
    canonical_url=None, base_url=None, production_url=None, AA=None, publication_authority=False, follow_up=None,
    no_new_render_reader_live_download_or_deployment_certificate=True,
    all_writes_confined_to_owned_folder=True, completion_percent_private_editorial=100,
    extent=dict(regular_files=len(files)+2, child_directories=len(dirs),
        all_paths=sorted([q['path'] for q in files]+['MANIFEST.json','FINAL.json']), directories=dirs),
    all_handles_terminal_at_return=True, quiescent_after_seal=True, terminal_self_hash_excluded=True))
end_files,end_dirs=inventory(R)
require(len(end_files)==len(files)+2 and end_dirs==dirs, 'finite extent drift at closure')
for q in files:
    require(pin(R / q['path'], R)==q, 'owned payload drift at closure')
