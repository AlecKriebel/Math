"""One current-docs data-only check: no network, Git, subprocess or writes."""
from pathlib import Path, PurePosixPath
from html.parser import HTMLParser
from urllib.parse import unquote
import hashlib, json, stat, re, html, unicodedata, datetime, sys

R=Path(__file__).resolve().parent
P=R.parents[1]
if len(sys.argv)!=1: raise SystemExit('One ordinary read-only invocation only')

def need(ok,message):
    if not ok: raise RuntimeError(message)

def sha(b): return hashlib.sha256(b).hexdigest()

def git(kind,b):
    return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()

def read(p):
    s=p.lstat(); need(stat.S_ISREG(s.st_mode),'Not regular: '+str(p))
    b=p.read_bytes()
    return b,{'path':str(p),'bytes':len(b),'SHA256':sha(b),'mode':oct(stat.S_IMODE(s.st_mode))}

def connector(p):
    b,pin=read(p); obj=json.loads(b)
    need(obj['isError'] is False and type(obj['structuredContent']['content']) is str,'Connector shape')
    return json.loads(obj['structuredContent']['content']),pin

def norm(s):
    s=''.join(c for c in unicodedata.normalize('NFKD',s).casefold() if not unicodedata.combining(c))
    return ' '.join(re.sub(r'[^\w]+',' ',s).split())

class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.all=[]; self.visible=[]; self.title=[]; self.h1=[]
        self.title_on=False; self.h1_on=False; self.body=False; self.hidden=0
    def handle_starttag(self,t,a):
        if t=='title': self.title_on=True
        if t=='h1': self.h1_on=True
        if t=='body': self.body=True
        if t in ('script','style'): self.hidden+=1
    def handle_endtag(self,t):
        if t=='title': self.title_on=False
        if t=='h1': self.h1_on=False
        if t=='body': self.body=False
        if t in ('script','style'): self.hidden-=1
    def handle_data(self,d):
        self.all.append(d)
        if self.body and not self.hidden: self.visible.append(d)
        if self.title_on: self.title.append(d)
        if self.h1_on: self.h1.append(d)

def tree_bytes(entries):
    children=sorted(entries,key=lambda x:x['path'].encode()+(b'/' if x['type']=='tree' else b'\0'))
    return b''.join(e['mode'].lstrip('0').encode()+b' '+e['path'].encode()+b'\0'+bytes.fromhex(e['sha']) for e in children)

initial=json.loads((R/'INITIAL.json').read_text())
opening,op=connector(R/'OPEN_REMOTE_REF.connector.json')
commit,cp=connector(R/'OPEN_REMOTE_COMMIT.connector.json')
root,rp=connector(R/'OPEN_ROOT_TREE.connector.json')
need(opening['object']['sha']==commit['sha']==initial['opening_main'],'Current main binding')
need(commit['tree']['sha']==root['sha']==initial['opening_root_tree'],'Current root binding')
need(root['truncated'] is False and git('tree',tree_bytes(root['tree']))==root['sha'],'Whole root tree identity')
need(next(x for x in root['tree'] if x['path']=='docs')['sha']==initial['docs_tree'],'Current docs binding')
tree,tp=connector(P/'verification/odd-areas-boolean-city-stage-audit-sol-20261116/LEGACY160_DOCS_TREE.connector.json')
need(tree['sha']==initial['docs_tree'] and tree['truncated'] is False,'Cached docs identity')
entries=tree['tree']
need(len(entries)==304 and len({e['path'] for e in entries})==304,'Exact metadata membership')
for e in entries:
    path=PurePosixPath(e['path'])
    need(not path.is_absolute() and all(x not in ('','.','..') for x in path.parts),'Unsafe path')
    need((e['mode'],e['type']) in [('100644','blob'),('040000','tree')],'Unexpected metadata mode/type')
objects=[]
for directory,oid in sorted({'':tree['sha'],**{e['path']:e['sha'] for e in entries if e['type']=='tree'}}.items()):
    prefix=directory+'/' if directory else ''
    children=[{**e,'path':e['path'][len(prefix):]} for e in entries if e['path'].startswith(prefix) and '/' not in e['path'][len(prefix):]]
    b=tree_bytes(children); need(git('tree',b)==oid,'Tree identity: '+directory)
    objects.append({'path':directory or '.','Git_SHA1':oid,'bytes':len(b)})
need(len(objects)==51,'Exact 51 tree objects')
refs_b,refs_pin=read(P/'verification/negative-gramian-legacy-sol-20261116/REFERENCE_PINS.json')
refs=json.loads(refs_b)['all47_HTML_rows']
metadata={'docs/'+e['path']:e for e in entries if e['type']=='blob' and e['path'].lower().endswith('.html')}
need(len(refs)==47 and {r['HTML_path'] for r in refs}==set(metadata),'Exact 47 HTML membership')
targets=[]
for t in initial['targets']:
    b,pin=read(P/'papers'/t['record']/'sources/record.response.body'); native=json.loads(b)
    need(native['doi']==t['DOI'] and native['metadata']['title']==t['title'],'Native identity')
    need([x['key'] for x in native['files']]==t['native_filenames'],'Native filenames')
    query=[('record',t['record']),('DOI',t['DOI']),('full title',t['title'])]
    query += [('distinctive alias',s) for s in t['distinctive_aliases']]
    query += [('native filename',s) for s in t['native_filenames']]
    targets.append({**t,'native_record_pin':pin,'queries':query})
rows=[]; total=0; wrappers=0
for r in refs:
    ref=r['actual_reference_file']; p=Path(ref['absolute_path']); b,pin=read(p)
    need((len(b),sha(b),pin['mode'])==(ref['bytes'],ref['sha256'],ref['mode']),'Cache custody: '+str(p))
    if r['typed_wrapper']:
        need(r['HTML_path']=='docs/papers/knudson-gradient-path/index.html' and len(b)==1863 and sha(b)=='ae49d075d4397ea90e634042a41c463251e7bc7e47d4ee836a0f2520167c59e3','Only exact named typed container')
        obj=json.loads(b); need(obj['isError'] is False,'Typed payload')
        b=obj['structuredContent']['content'].encode('utf-8'); wrappers+=1
    e=metadata[r['HTML_path']]
    need(len(b)==r['HTML_bytes']==e['size'] and sha(b)==r['HTML_SHA256'] and git('blob',b)==r['Git_blob']==e['sha'],'Current whole blob: '+r['HTML_path'])
    need(e['mode']==r['Git_mode']=='100644','HTML Git mode')
    raw=b.decode('utf-8','strict'); parser=Text(); parser.feed(raw)
    channels={'raw':raw,'entity_decoded':html.unescape(raw),'URL_decoded':unquote(raw),'entity_URL_decoded':html.unescape(unquote(raw)),
        'visible_body':' '.join(parser.visible),'tag_text':' '.join(parser.all)}
    channels.update({'normalized_'+k:norm(v) for k,v in list(channels.items())})
    hits=[]
    for t in targets:
        matches=[]
        for kind,q in t['queries']:
            for channel,value in channels.items():
                needle=norm(q) if channel.startswith('normalized_') else q.casefold()
                hay=value if channel.startswith('normalized_') else value.casefold()
                at=hay.find(needle)
                if at>=0:
                    matches.append({'kind':kind,'query':q,'channel':channel,'snippet':value[max(0,at-80):at+len(needle)+130]})
        if matches: hits.append({'record':t['record'],'matches':matches})
    rows.append({'path':r['HTML_path'],'title':' '.join(parser.title),'h1':' '.join(parser.h1),'bytes':len(b),'SHA256':sha(b),
        'Git_blob':e['sha'],'Git_mode':e['mode'],'actual_reference':pin,'typed_wrapper':r['typed_wrapper'],'hits':hits})
    total+=len(b)
need(total==612221 and wrappers==1,'Exact whole HTML byte extent')
path_hits=[]
for e in entries:
    found=[]
    for t in targets:
        for kind,q in t['queries']:
            if q.casefold() in unquote(e['path']).casefold() or norm(q) in norm(unquote(e['path'])):
                found.append({'record':t['record'],'kind':kind,'query':q})
    if found: path_hits.append({'entry':e,'matches':found})
print(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'CURRENT_DOCS_WHOLEBYTE_AUTHENTICATION_AND_BOUNDED_SEARCH_COMPLETE',
    'remote_main':commit['sha'],'root_tree':root['sha'],'docs_tree':tree['sha'],'root_metadata_entries':len(root['tree']),
    'metadata_entries':len(entries),'blob_metadata':sum(e['type']=='blob' for e in entries),'tree_metadata':sum(e['type']=='tree' for e in entries),
    'reconstructed_docs_tree_objects':objects,'complete_HTML_buffers':len(rows),'complete_HTML_bytes':total,'typed_wrappers':wrappers,
    'input_pins':[op,cp,rp,tp,refs_pin],'targets':targets,'rows':rows,'metadata_path_hits':path_hits,
    'candidate_paths':[r['path'] for r in rows if r['hits']],'semantic_correspondence_verdict':None,'no_history_priority_global_traffic_claim':True,
    'native_math_old_helper_or_Git_execution':False,'writes':0,'redirect_authority':False},ensure_ascii=False,indent=2))
