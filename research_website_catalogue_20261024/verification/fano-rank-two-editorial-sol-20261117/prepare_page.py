#!/usr/bin/env python3
"""Prepare one private factual HTML page; no network, Git or scientific programs."""
from pathlib import Path
from html import escape, unescape
from html.parser import HTMLParser
import datetime
import hashlib
import json
import os
import re
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P / 'verification/fano-rank-two-editorial-sol-20261117'
SRC = P / 'papers/23411227/sources'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
SLUG = 'rank-two-fano-entropy-degeneration'
CANONICAL = 'https://aleckriebel.com/research/' + SLUG + '/'
PAGE = OWN / 'private-page'

def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)

def read(path):
    require(not any(p.is_symlink() for p in (path, *path.parents)), 'ordinary source paths only')
    before = path.stat()
    require(stat.S_ISREG(before.st_mode), 'ordinary source file')
    raw = path.read_bytes()
    after = path.stat()
    keys = ('st_dev', 'st_ino', 'st_mode', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
    require(all(getattr(before,k) == getattr(after,k) for k in keys) and len(raw) == before.st_size, 'stable complete source read')
    return raw

def pin(path):
    raw = read(path)
    info = path.stat()
    return {'path': str(path), 'bytes': len(raw), 'SHA256': hashlib.sha256(raw).hexdigest(),
            'mode': format(stat.S_IMODE(info.st_mode), '04o'),
            'mtime_ns': info.st_mtime_ns, 'ctime_ns': info.st_ctime_ns}

def write_new(path, raw):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    try:
        os.fchmod(fd, 0o644)
        offset = 0
        while offset < len(raw):
            count = os.write(fd, raw[offset:])
            require(count > 0, 'complete private write')
            offset += count
        os.fsync(fd)
    finally:
        os.close(fd)

def write_json(name, value):
    write_new(OWN / name, (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())

require(Path(__file__).absolute() == OWN / 'prepare_page.py', 'exact private authoring path')
fixed = [SRC/'record.response.body', SRC/'files-23411227.response.body',
         SRC/'assets/rank-two-fano-note.pdf', SRC/'assets/rank-two-fano-verification.zip',
         SRC/'published-source/container-001/tree/note.tex',
         P/'verification/root-clearance-23411227-20261117.json',
         P/'papers/23411227/reviews/root-continuation-20261117/ROOT_REVIEW.md',
         W/'public/research/research.css',
         W/'public/research/positive-tangent-seshadri-projective-space/index.html']
fixed += [P / ('papers/23411227/reviews/root-initial-20261117/png/page-' + str(n) + '.png') for n in range(1,6)]
before = [pin(path) for path in fixed]
require(before[5]['bytes'] == 2273 and before[5]['SHA256'] == '1f8d4c9a3d80f1685233e04c1ebcedb3d321944a9ea057f384491a65f96dfc73', 'exact root final clearance')
require(before[6]['bytes'] == 14970 and before[6]['SHA256'] == '4753c243b4b3a88c122e1480a3ef2995a266def28fe17fc83fce5956f70f58d3', 'exact root complete scientific review')
require(before[4]['bytes'] == 17432 and before[4]['SHA256'] == '58fc08b947c20e4d00fb6a379a109e8489aa6a22b1f2161587980ada95c318bc', 'exact complete controlling TeX')
record = json.loads(read(SRC/'record.response.body'))
files = json.loads(read(SRC/'files-23411227.response.body'))
metadata = record['metadata']
require(metadata['version'] == '1.0.0' and metadata['publication_date'] == '2026-10-16' and metadata['license']['id'] == 'cc-by-4.0', 'native date/version/rights')
require(record['doi'] == '10.5281/zenodo.23411227', 'exact record DOI')
names = ['rank-two-fano-note.pdf', 'rank-two-fano-verification.zip']
require([r['key'] for r in record['files']] == [r['key'] for r in files['entries']] == names, 'exact native two-asset order')
abstract_html = metadata['description']
require(len(re.findall(r'<p>', abstract_html)) == 3 and not re.search(r'<(?!/?p[> ])', abstract_html), 'three complete native abstract paragraphs only')
abstract_text = unescape(re.sub(r'<[^>]+>', ' ', abstract_html))
abstract_text = ' '.join(abstract_text.split())
license_url = 'https://creativecommons.org/licenses/by/4.0/'
description = 'An explicit smooth Fano fivefold with a unique global entropy-minimizing valuation of rational rank two and a singular canonical first central variety.'
assets = []
require(not os.path.lexists(PAGE), 'fresh private page directory')
PAGE.mkdir(mode=0o755)
for n, row in enumerate(record['files'], 1):
    source = SRC / 'assets' / row['key']
    raw = read(source)
    require(len(raw) == row['size'] and 'md5:' + hashlib.md5(raw).hexdigest() == row['checksum'], 'exact native asset length/MD5')
    destination = PAGE / row['key']
    write_new(destination, raw)
    require(read(destination) == raw, 'unchanged full native asset copy')
    assets.append({'native_order': n, 'native_filename': row['key'], 'local_filename': row['key'],
                   'bytes': len(raw), 'SHA256': hashlib.sha256(raw).hexdigest(),
                   'native_checksum': row['checksum'], 'media_type': files['entries'][n-1]['mimetype'],
                   'native_content_url': files['entries'][n-1]['links']['content'],
                   'native_file_url': 'https://zenodo.org/records/23411227/files/' + row['key'],
                   'source_path': str(source), 'private_path': str(destination), 'whole_bytes_equal': True})
write_new(PAGE/'research.css', read(W/'public/research/research.css'))
schema = {'@context':'https://schema.org', '@type':'ScholarlyArticle',
          'name': metadata['title'], 'headline': metadata['title'], 'description': description,
          'abstract': abstract_text, 'url': record['doi_url'],
          'identifier': {'@type':'PropertyValue', 'propertyID':'DOI', 'value':record['doi']},
          'author': {'@type':'Person','name':'Alec Kriebel','sameAs':'https://orcid.org/0009-0001-9320-500X'},
          'publisher': {'@type':'Organization','name':'Zenodo'},
          'datePublished': metadata['publication_date'], 'version':metadata['version'],
          'creativeWorkStatus':'Unrefereed preprint', 'inLanguage':'en', 'isAccessibleForFree':True,
          'license': license_url, 'sameAs':[record['links']['self_html']],
          'keywords':metadata['keywords'],
          'citation':['https://arxiv.org/abs/2401.13999v2','https://doi.org/10.1016/j.aim.2003.09.009',
                      'https://arxiv.org/abs/2009.01010v1','https://doi.org/10.1002/cpa.22053',
                      'https://doi.org/10.1017/fmp.2023.5','https://doi.org/10.1007/s42543-022-00054-0',
                      'https://doi.org/10.4171/OWR/2022/17'],
          'encoding':[{'@type':'MediaObject','name':r['native_filename'],'encodingFormat':r['media_type'],
                       'contentSize':str(r['bytes'])+' bytes','contentUrl':r['native_content_url']} for r in assets]}
template = read(OWN/'page.html.in').decode()
for marker, value in [('__ABSTRACT_ATTRIBUTE__',escape(abstract_text,quote=True)),
                      ('__SCHEMA_JSON__',json.dumps(schema,ensure_ascii=False,indent=2)),
                      ('__FULL_NATIVE_ABSTRACT__',abstract_html.rstrip())]:
    require(template.count(marker) == 1, 'single exact template insertion')
    template = template.replace(marker,value)
require('__' not in template and '<section id="abstract">\n<h2>Abstract</h2>\n'+abstract_html.rstrip()+'\n</section>' in template, 'complete unchanged native abstract in saved page')
write_new(PAGE/'index.html', template.encode())
bib = '''@misc{kriebel2026ranktwofano,
  author = {Kriebel, Alec},
  title = {An explicit rank-two entropy-minimizing Fano degeneration},
  year = {2026},
  month = oct,
  day = {16},
  version = {1.0.0},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.23411227},
  url = {https://doi.org/10.5281/zenodo.23411227},
  note = {Unrefereed preprint. CC BY 4.0}
}
'''
write_new(PAGE/'citation.bib',bib.encode())
model = {'private_only':True,'publication_authority':False,'proposed_slug':SLUG,
         'proposed_path':'/research/'+SLUG+'/', 'proposed_canonical':CANONICAL,
         'actual_canonical':None,'production_url':None,'page_publication_date':None,'AA':None,
         'legacy_redirect':None,'follow_up':None,'robots':'noindex, nofollow',
         'title':metadata['title'],'author':{'name':'Alec Kriebel','ORCID':'https://orcid.org/0009-0001-9320-500X'},
         'DOI':record['doi'],'concept_DOI':record['conceptdoi'],'native_record':record['links']['self_html'],
         'native_version':metadata['version'],'native_publication_date':metadata['publication_date'],
         'abstract':{'source':'record.response.body metadata.description','native_html':abstract_html,
                     'full_normalized_text':abstract_text,'whole_native_paragraphs_preserved':True},
         'native_assets_in_original_order':assets,'generated_citation_file':'citation.bib',
         'stylesheet':{'private_reference':'research.css','source':str(W/'public/research/research.css'),
                       'SHA256':before[7]['SHA256'],'changed':False,'private_copy_only':True},
         'SEO':{'title':metadata['title']+' | Alec Kriebel','description':description,'canonical':None,
                'proposed_canonical':CANONICAL,'future_local_PDF_URL':CANONICAL+names[0],
                'structured_data':schema},
         'rights':{'native_license':'CC-BY-4.0','license_URL':license_url,'native_MIT_split':False},
         'scientific_scope':{'global_competitors':'ALL valuations on this exact smooth Fano fivefold',
                             'absolute_unique_minimizer':True,'rational_rank':2,'ordered_rank':1,
                             'singular_canonical_first_center':'Bl_C(Q_0) × F_1',
                             'second_underlying_variety_unchanged':True,'imported_theorems_explicit':True},
         'native_replay_limit_private_notes_only':'Earlier auxiliary native attempt stopped at missing SymPy; not all checks reproduced here. No native scientific execution by this editorial task.',
         'future_activation_requirements':['Remove private noindex/nofollow only under separate publication authority.',
             'Add canonical and og:url '+CANONICAL+'; replace native citation_pdf_url with '+CANONICAL+names[0]+'.',
             'Bind structured-data page/encoding URLs to the separately accepted public page; use existing /research/research.css without publishing its private copy.',
             'Separate site integration, native-index protection, deploy, live/PDF/mobile verification and AA evidence remain required.'],
         'collision_scope':'Proposed exact current public directory absent at private authoring; no historical/live slug claim.'}
require(not os.path.lexists(W/'public/research'/SLUG), 'proposed current public directory absent')
write_json('MODEL.json',model)
write_json('NATIVE_ASSETS.json',{'record':23411227,'files_entry_order_empty':files['order']==[],
           'effective_native_array_order':names,'assets':assets,'license':'CC-BY-4.0','native_MIT_split':False})
write_new(OWN/'NATIVE_ABSTRACT.html',abstract_html.encode())
after = [pin(path) for path in fixed]
require(after == before, 'all fixed source/control/style/render files unchanged')
write_json('SOURCE_PINS.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'before':before,'after':after,'whole_selected_inputs_unchanged':True,
          'complete_TeX_personally_read':True,'all_five_original_PDF_page_images_personally_read':True,
          'native_API_abstract_rights_files_and_root_review_personally_read_complete':True,
          'scientific_executions':0,'network_Git_Wwrites_Sheet_runtime_deploy_actions':0})
print(json.dumps({'status':'PRIVATE_PAGE_PREPARED_NOT_PUBLISHED','private_page':str(PAGE/'index.html'),
                   'native_assets_unchanged_in_order':names,'scientific_executions':0,'publication_authority':False},sort_keys=True))
