#!/usr/bin/env python3
"""One local editorial/data-integrity verification and finite private freeze."""
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
import datetime
import hashlib
import json
import os
import re
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P / 'verification/fano-rank-two-editorial-sol-20261117'
PAGE = OWN / 'private-page'
SRC = P / 'papers/23411227/sources'
EXPECTED = {
    'private-page/index.html': 'a2ab73136474c3f6a91e1214f8a40d42d096658ffaa6ec6a409e9a395c1179e8',
    'MODEL.json': '3123d9acf8e32d53793cc8a8136006d47cd74f7fb9a2545be275a7cd06edca1a',
    'NATIVE_ASSETS.json': '78b7a5557a6da6504db3aaf1c068a9304565fefa535d34c65c4d5684c291ae32',
    'private-page/citation.bib': 'e54e438d62fc69eddacc43a5341cf38e9509ef196caa0f6a27d1568cce421831',
}

def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)

def read(path):
    require(not any(p.is_symlink() for p in (path,*path.parents)), 'no symbolic paths')
    before = path.stat()
    require(stat.S_ISREG(before.st_mode), 'ordinary complete file')
    raw = path.read_bytes()
    after = path.stat()
    require((before.st_dev,before.st_ino,before.st_mode,before.st_size,before.st_mtime_ns,before.st_ctime_ns) ==
            (after.st_dev,after.st_ino,after.st_mode,after.st_size,after.st_mtime_ns,after.st_ctime_ns) and len(raw)==before.st_size,
            'stable complete raw read')
    return raw

def pin(path):
    raw = read(path)
    return {'bytes':len(raw),'SHA256':hashlib.sha256(raw).hexdigest(),
            'mode':format(stat.S_IMODE(path.stat().st_mode),'04o')}

def write_new(name,value):
    raw = (json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()
    fd = os.open(OWN/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    try:
        os.fchmod(fd,0o644)
        offset=0
        while offset<len(raw):
            count=os.write(fd,raw[offset:])
            require(count>0,'complete final evidence write')
            offset+=count
        os.fsync(fd)
    finally:
        os.close(fd)

class PageData(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[]
        self.links=[]
        self.meta={}
        self.canonicals=[]
        self.iframes=[]
    def handle_starttag(self,tag,attrs):
        values=dict(attrs)
        if 'id' in values:
            self.ids.append(values['id'])
        if tag=='meta':
            key=values.get('name',values.get('property'))
            require(key not in self.meta,'unique named/property metadata')
            self.meta[key]=values.get('content')
        if tag in ('a','link') and values.get('href'):
            self.links.append(values['href'])
        if tag=='link' and values.get('rel')=='canonical':
            self.canonicals.append(values['href'])
        if tag=='iframe':
            self.iframes.append(values)

require(Path(__file__).absolute()==OWN/'verify_and_freeze.py','exact private verifier path')
for name,digest in EXPECTED.items():
    require(pin(OWN/name)['SHA256']==digest,'exact independently reviewed candidate')
model=json.loads(read(OWN/'MODEL.json'))
record=json.loads(read(SRC/'record.response.body'))
inventory=json.loads(read(OWN/'NATIVE_ASSETS.json'))
source_pins=json.loads(read(OWN/'SOURCE_PINS.json'))
require(source_pins['before']==source_pins['after'] and source_pins['whole_selected_inputs_unchanged'] is True,'complete selected before/after source equality')
for row in source_pins['after']:
    path=Path(row['path'])
    require(pin(path)=={k:row[k] for k in ('bytes','SHA256','mode')},'same exact source/control/render/style bytes at freeze')
    info=path.stat()
    require((info.st_mtime_ns,info.st_ctime_ns)==(row['mtime_ns'],row['ctime_ns']),'same exact source/control/render/style timestamps at freeze')
html=read(PAGE/'index.html').decode()
parser=PageData()
parser.feed(html)
require(len(parser.ids)==len(set(parser.ids)),'unique page anchors')
for target in parser.links:
    if target.startswith('#'):
        require(target[1:] in parser.ids,'all fragment links resolve')
    elif not target.startswith(('https://','mailto:','/')):
        require((PAGE/target.split('#',1)[0]).is_file(),'all page-relative links resolve locally')
require(parser.canonicals==[] and 'og:url' not in parser.meta,'private canonical/og:url not activated')
require(parser.meta['robots']=='noindex, nofollow','private robots retained')
require(all(model[k] is None for k in ('actual_canonical','production_url','page_publication_date','AA','legacy_redirect','follow_up')),'all private publication/action fields remain null')
require(model['proposed_canonical']=='https://aleckriebel.com/research/rank-two-fano-entropy-degeneration/','exact proposed canonical')
native_abstract=record['metadata']['description']
visible=html.split('<section id="abstract">\n<h2>Abstract</h2>\n',1)[1].split('\n</section>',1)[0]
require(visible==native_abstract.rstrip(),'entire exact native abstract visible')
abstract_text=' '.join(unescape(re.sub(r'<[^>]+>',' ',native_abstract)).split())
schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',html,re.S).group(1))
require(schema==model['SEO']['structured_data'] and schema['abstract']==abstract_text==parser.meta['citation_abstract'],'entire exact structured/citation abstract')
require(schema['version']==parser.meta['citation_version']==model['native_version']=='1.0.0','exact native version')
require(schema['datePublished']==model['native_publication_date']=='2026-10-16' and parser.meta['citation_publication_date']=='2026/10/16','exact original native date')
require(schema['identifier']['value']==parser.meta['citation_doi']=='10.5281/zenodo.23411227','exact record DOI')
require(schema['license']==model['rights']['license_URL']=='https://creativecommons.org/licenses/by/4.0/' and inventory['native_MIT_split'] is False,'native CC BY 4.0 without MIT split')
require([r['native_filename'] for r in inventory['assets']]==[r['key'] for r in record['files']]==['rank-two-fano-note.pdf','rank-two-fano-verification.zip'],'exact native asset order')
for row in inventory['assets']:
    require(read(PAGE/row['local_filename'])==read(Path(row['source_path'])),'whole unchanged native asset bytes')
    require(pin(PAGE/row['local_filename'])=={'bytes':row['bytes'],'SHA256':row['SHA256'],'mode':'0644'},'exact copied asset complete pin')
require(len(parser.iframes)==1 and parser.iframes[0]['src']=='rank-two-fano-note.pdf#view=FitH' and parser.iframes[0]['title'],'local five-page PDF embed')
require('among all valuations on X' in html and 'rational rank two' in html and 'ordered rank one' in html,'full global/rank explanatory scope present')
require('SymPy' not in html and '2026-11-17' not in html,'internal replay/date narrative absent from page')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
checks={'UTC':now,'status':'PASS_PRIVATE_STATIC_EDITORIAL_AND_COPY_CHECKS',
        'reviewed_candidate_pins':{name:pin(OWN/name) for name in EXPECTED},
        'selected_fixed_source_files':len(source_pins['after']),
        'selected_inputs_unchanged_through_freeze':True,
        'full_native_abstract_HTML_and_metadata_match':True,'native_assets_whole_bytes_equal_in_order':True,
        'local_links_and_fragments_resolve':True,'date_version_DOI_rights_and_PDF_embed_match':True,
        'independent_editorial_review':'BOUNDED_PASS_NO_CONCRETE_CORRECTION',
        'browser_rendering_live_site_scientific_or_publication_certificate':False}
write_new('CHECKS.json',checks)
final={'schema':'private-fano-editorial-final-v1','UTC':now,
       'status':'PRIVATE_EDITORIAL_COMPLETE_PENDING_ROOT_ACCEPTANCE','completion_percent_assigned_editorial':100,
       'scope':str(OWN),'page':pin(PAGE/'index.html'),'MODEL':pin(OWN/'MODEL.json'),
       'native_assets':inventory['assets'],'independent_editorial_result':'BOUNDED_PASS',
       'scientific_clearance':'verification/root-clearance-23411227-20261117.json',
       'scientific_executions':0,'release_helper_invocations_all_modes':0,
       'network_Git_Wwrites_Sheet_runtime_install_deploy_redirect_external_contact_actions':0,
       'private_only':True,'publication_or_future_action_authority':False,
       'actual_canonical':None,'production_url':None,'AA':None,'redirect':None,'follow_up':None}
write_new('FINAL.json',final)
paths=sorted(OWN.rglob('*'))
require(all(p.is_dir() or p.is_file() for p in paths) and not any(p.is_symlink() for p in paths),'ordinary finite owned namespace')
entries=[{'path':'.','kind':'directory','mode':format(stat.S_IMODE(OWN.stat().st_mode),'04o'),'empty':False}]
for path in paths:
    name=path.relative_to(OWN).as_posix()
    if path.is_dir():
        entries.append({'path':name,'kind':'directory','mode':format(stat.S_IMODE(path.stat().st_mode),'04o'),'empty':not any(path.iterdir())})
    else:
        entries.append({'path':name,'kind':'file',**pin(path)})
entries.append({'path':'MANIFEST.json','kind':'file','mode':'0644',
                'content_hash_exclusion':'Self-referential manifest only; actual complete external SHA256/bytes reported to root.'})
manifest={'schema':'finite-private-fano-editorial-manifest-v1','scope':str(OWN),
          'file_count':sum(row['kind']=='file' for row in entries),
          'child_directory_count':sum(row['kind']=='directory' for row in entries)-1,
          'entries':sorted(entries,key=lambda r:r['path']),
          'terminal_content_hash_exclusions_exact':['MANIFEST.json'],
          'private_only':True,'publication_or_future_action_authority':False}
write_new('MANIFEST.json',manifest)
require({p.relative_to(OWN).as_posix() for p in OWN.rglob('*')}=={row['path'] for row in entries if row['path']!='.'},'complete final finite path census')
for directory in [PAGE,OWN]:
    fd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
print(json.dumps({'status':final['status'],'files':manifest['file_count'],'child_directories':manifest['child_directory_count'],
                  'FINAL':pin(OWN/'FINAL.json'),'MANIFEST':pin(OWN/'MANIFEST.json'),
                  'page':pin(PAGE/'index.html'),'MODEL':pin(OWN/'MODEL.json'),
                  'publication_or_future_action_authority':False},sort_keys=True))
