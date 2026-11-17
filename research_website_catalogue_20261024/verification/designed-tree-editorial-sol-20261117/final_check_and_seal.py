"""Final bounded own-data check and finite seal; never import source/helper programs."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import datetime
import hashlib
import json
import os
import re
import stat

R = Path(__file__).resolve().parent
P = R.parents[1]
def require(value, message):
    if not value: raise RuntimeError(message)
def pin(path, relative=None):
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), 'not regular: ' + str(path))
    data = path.read_bytes()
    return {'path': path.relative_to(relative).as_posix() if relative else str(path), 'bytes': len(data),
            'SHA256': hashlib.sha256(data).hexdigest(), 'mode': oct(stat.S_IMODE(st.st_mode))}
def inventory(root):
    files, directories = [], []
    for path in sorted(root.rglob('*')):
        st = path.lstat()
        if stat.S_ISREG(st.st_mode): files.append(pin(path, root))
        elif stat.S_ISDIR(st.st_mode): directories.append({'path':path.relative_to(root).as_posix(),'mode':oct(stat.S_IMODE(st.st_mode))})
        else: raise RuntimeError('unexpected file type: ' + str(path))
    return files, directories
def create_json(name, value):
    with (R / name).open('x') as stream: json.dump(value, stream, ensure_ascii=False, indent=2); stream.write('\n')

require(not os.path.lexists(R / 'MANIFEST.json') and not os.path.lexists(R / 'FINAL.json'), 'already sealed')
guards = json.loads((R / 'SOURCE_GUARDS.json').read_text())
source = Path(guards['source_root'])
sf, sd = inventory(source)
require(sf == guards['files'] and sd == guards['directories'] and oct(stat.S_IMODE(source.lstat().st_mode)) == guards['root_mode'], 'source changed after initial static pass')
for key in ('actual_clearance','actual_root_report','complete_native_metadata','native_files_returned_order','controlling_manuscript','actual_license'):
    q = guards[key]; require(pin(P / q['path'], P) == q, 'controlling input changed: ' + key)
for q in guards['reference_files_unchanged']:
    require(pin(Path(q['path'])) == q, 'reference changed')
require(not os.path.lexists(guards['proposed_slug_absent_before_after']), 'proposed slug appeared')
for q in guards['asset_copies']:
    require(pin(source / q['source']['path'], source) == q['source'] and pin(R / q['private_copy']['path'], R) == q['private_copy'], 'asset copy changed')
require(pin(R / 'research.css', R) == guards['private_css_copy'], 'private CSS changed')
m = json.loads((R / 'page-model.json').read_text())
require(all(m[key] is None for key in ('canonical_url','base_url','production_url','actual_publication_date','AA','follow_up')) and m['publication_authority'] is False, 'private null gates changed')
html = (R / 'article.html').read_text(); main = (R / 'public-main.html').read_text(); head = (R / 'head.html').read_text()
require(re.search(r'<main\b.*?</main>\n?', html, re.S).group(0) == main and re.search(r'<head>.*?</head>\n?', html, re.S).group(0) == head, 'whole MAIN/head differs')
sch = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', head, re.S).group(1))
class Inspect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.ids=[]; self.links=[]; self.meta={}; self.abstract=[]; self.capturing=False; self.canonical=[]; self.bases=[]
    def handle_starttag(self, tag, attrs):
        q=dict(attrs)
        if 'id' in q: self.ids.append(q['id'])
        if q.get('id')=='abstract-text': self.capturing=True
        if tag=='meta': self.meta[q.get('name',q.get('property'))]=q.get('content')
        if tag=='link' and q.get('rel')=='canonical': self.canonical.append(q.get('href'))
        if tag=='base': self.bases.append(q)
        for key in ('href','src'):
            if key in q: self.links.append(q[key])
    def handle_endtag(self, tag):
        if tag=='p': self.capturing=False
    def handle_data(self, data):
        if self.capturing: self.abstract.append(data)
v=Inspect(); v.feed(html)
require(''.join(v.abstract)==m['abstract']==v.meta['DC.description']==sch['abstract'], 'final abstract differs')
require(v.meta['robots']==v.meta['googlebot']=='noindex, nofollow' and not v.canonical and not v.bases and 'og:url' not in v.meta, 'private wrapper changed')
require(len(v.ids)==len(set(v.ids)), 'duplicate final ids')
require(not any(key in sch for key in ('url','@id','mainEntityOfPage')), 'production schema identity active')
for link in v.links:
    u=urlsplit(link)
    if not u.scheme and not u.netloc:
        path=unquote(u.path)
        require(not path.startswith('/') and '..' not in Path(path).parts, 'unconfined local link')
        if path: require((R/path).is_file(), 'missing final local target')
        elif u.fragment: require(u.fragment in v.ids, 'missing fragment')
require('Hassin–Zemel’s sufficient exponent separation does not directly cover this balanced near-capacity regime.' in main, 'HZ clarification absent')
require('Here the transportation reduction has continuous unbounded stream capacities and vanishing normalized surplus.' in main, 'stream-capacity clarification absent')
require('The final 1993 journal body was not inspected.' in main, 'edition limit absent')
review=(R/'COPY_REVIEW.md').read_text()
require('PASS — no actionable editorial defects found.' in review and 'not a new independent scientific review' in review, 'read-only copy review absent')
for name in ('STATIC_CHECK.stdout.txt','STATIC_CHECK.stderr.txt','FINAL_CHECK.stdout.txt','FINAL_CHECK.stderr.txt'):
    require((R/name).read_bytes()==b'', 'nonempty literal own data-check stream: '+name)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
create_json('FINAL_DATA_CHECK.json', {'UTC':now,'status':'PASS_FINAL_PRIVATE_DATA_CONSISTENCY','initial_assembly_passes':1,'final_bounded_consistency_passes':1,
    'editorial_change':'HZ/KMN hypothesis comparison clarified after initial assembly; no mathematical claim or abstract changed',
    'complete_MAIN_head_abstract_model_consistent':True,'native_asset_order_and_bytes_modes_preserved':True,'source162files23dirs_unchanged':True,
    'private_noindex_null_actual_publication_canonical_base_production_AA':True,'copy_review':'PASS_READ_ONLY_EDITORIAL_COMPARISON',
    'browser_display_live_download_or_deployment_certification':False,'new_independent_scientific_review':False,'source_or_archived_program_execution':False,
    'network_Git_W_Sheet_deploy_or_outreach_actions':False})
with (R/'REPORT.md').open('a') as stream:
    stream.write('\nFinal editorial clarification: Hassin–Zemel sufficient separation is explicitly outside this balanced near-capacity regime. The KMN comparison explicitly names continuous unbounded stream capacities in the transportation reduction, avoiding confusion with the deterministic physical capacities. A fresh no-history GPT-6.1 Sol ultra subagent read the whole corrected draft/model/Bib and native controlling materials and returned PASS, with editorial/static limits only (COPY_REVIEW.md). One subsequent bounded own data consistency pass rechecked the complete assembled head/MAIN and abstract/private gates, exact original copies, and unchanged source/reference files. No scientific execution or current browser/display certification was added.\n\nPrivate preparation is complete and frozen at the final manifest; root adoption and separate staging/publication remain pending.\n')
with (R/'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n- '+now+' — 100% private editorial preparation. Whole actual assembled article/head/model/Bib personally read. HZ/KMN comparison clarified in both whole MAIN and article; a fresh GPT-6.1 Sol ultra read-only editorial subagent independently read the final corrected copy and native materials and returned PASS. Final bounded data consistency passed, preserving all inputs and exact native copies; finite all-file/mode/directory seal follows. No current browser/display, live or publication claim. The earlier65% entry reused the intake timestamp; drafting occurred after intake and before the actual05:19:36 assembly check.\n')
files, directories=inventory(R)
create_json('MANIFEST.json', {'schema':'whole-private-editorial-manifest-v1','UTC':now,'root':str(R),'root_mode':oct(stat.S_IMODE(R.lstat().st_mode)),
    'payload_files':files,'directories':directories,'exact_terminal_exclusions':['MANIFEST.json','FINAL.json'],
    'all_hidden_ignored_empty_files_and_modes_included':True,'no_future_or_subtree_exclusions':True})
create_json('FINAL.json', {'schema':'private-editorial-final-v1','UTC':now,'record':'23527793','row':185,
    'status':'FROZEN_PRIVATE_EDITORIAL_READY_FOR_ROOT_ADOPTION','completion_percent_private_editorial':100,
    'article':pin(R/'article.html',R),'whole_MAIN':pin(R/'public-main.html',R),'head':pin(R/'head.html',R),'model':pin(R/'page-model.json',R),'Bib':pin(R/'citation.bib',R),
    'report':pin(R/'REPORT.md',R),'manifest':pin(R/'MANIFEST.json',R),'source_guards':pin(R/'SOURCE_GUARDS.json',R),
    'initial_static_check':pin(R/'STATIC_CHECK.json',R),'final_data_check':pin(R/'FINAL_DATA_CHECK.json',R),'read_only_copy_review':pin(R/'COPY_REVIEW.md',R),
    'native_assets':guards['asset_copies'],'source162files23dirs_unchanged':True,
    'scientific_clearance_inherited':True,'new_independent_scientific_review':False,'root_editorial_adoption':False,
    'initial_data_passes':1,'final_consistency_passes':1,'all_data_check_streams_empty':True,
    'actual_publication_date':None,'canonical_url':None,'base_url':None,'production_url':None,'AA':None,'publication_authority':False,'follow_up':None,
    'no_current_render_reader_live_download_or_deployment_certificate':True,'all_writes_confined_to_owned_folder':True,
    'extent':{'regular_files':len(files)+2,'child_directories':len(directories),'all_paths':sorted([q['path'] for q in files]+['MANIFEST.json','FINAL.json']),'directories':directories},
    'all_handles_terminal_at_return':True,'quiescent_after_seal':True,'terminal_self_hash_excluded':True})
final_files, final_directories=inventory(R)
require(len(final_files)==len(files)+2 and final_directories==directories,'final finite extent drift')
for q in files: require(pin(R/q['path'],R)==q,'payload drift during final seal')
