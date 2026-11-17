"""One bounded data-only current-docs authentication/search; no network/Git/subprocess/writes."""
from pathlib import Path,PurePosixPath
from html.parser import HTMLParser
from urllib.parse import unquote
import hashlib,json,stat,re,html,unicodedata,datetime,sys
R=Path(__file__).resolve().parent
P=R.parents[1]
if len(sys.argv)!=1:raise SystemExit('ordinary read-only default only')
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def gh(kind,b):return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def read(p):
    st=p.lstat();need(stat.S_ISREG(st.st_mode),'not ordinary file '+str(p))
    b=p.read_bytes()
    return b,dict(path=str(p),bytes=len(b),SHA256=sha(b),mode=oct(stat.S_IMODE(st.st_mode)))
def connector(p):
    b,pin=read(p);o=json.loads(b)
    need(o['isError'] is False and type(o['structuredContent']['content']) is str,'connector shape')
    return json.loads(o['structuredContent']['content']),pin
def norm(s):
    s=''.join(x for x in unicodedata.normalize('NFKD',s).casefold() if not unicodedata.combining(x))
    return ' '.join(re.sub(r'[^\w]+',' ',s).split())
class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.all=[];self.title=[];self.h1=[];self.t=False;self.h=False
    def handle_starttag(self,t,a):
        if t=='title':self.t=True
        if t=='h1':self.h=True
    def handle_endtag(self,t):
        if t=='title':self.t=False
        if t=='h1':self.h=False
    def handle_data(self,d):
        self.all.append(d)
        if self.t:self.title.append(d)
        if self.h:self.h1.append(d)
initial=json.loads((R/'INITIAL.json').read_text())
opening,op=connector(R/'OPEN_REMOTE_REF.connector.json')
commit,cp=connector(R/'OPEN_REMOTE_COMMIT.connector.json')
root,rp=connector(R/'OPEN_ROOT_TREE.connector.json')
expected=initial['opening_remote']
need(opening['object']['sha']==commit['sha']==expected['main'],'opening branch binding')
need(commit['tree']['sha']==root['sha']==expected['root_tree'] and root['truncated'] is False,'root binding')
need(next(x for x in root['tree'] if x['path']=='docs')['sha']==expected['docs_tree'],'docs root binding')
tree_path=P/'verification/odd-areas-boolean-city-stage-audit-sol-20261116/LEGACY160_DOCS_TREE.connector.json'
tree,tp=connector(tree_path)
need(tree['sha']==expected['docs_tree'] and tree['truncated'] is False,'current cached docs identity')
entries=tree['tree'];need(len(entries)==304 and len({x['path'] for x in entries})==304,'304 unique metadata entries')
for e in entries:
    q=PurePosixPath(e['path'])
    need(not q.is_absolute() and all(x not in ('','.','..') for x in q.parts),'unsafe path')
    need((e['mode'],e['type']) in [('100644','blob'),('040000','tree')],'unexpected mode/type')
ids={'':tree['sha'],**{x['path']:x['sha'] for x in entries if x['type']=='tree'}}
objects=[]
for name,expected_sha in sorted(ids.items()):
    prefix=name+'/' if name else '';children=[]
    for e in entries:
        if e['path'].startswith(prefix):
            leaf=e['path'][len(prefix):]
            if '/' not in leaf:children.append((leaf,e))
    children.sort(key=lambda t:t[0].encode()+ (b'/' if t[1]['type']=='tree' else b'\0'))
    b=b''.join(e['mode'].lstrip('0').encode()+b' '+leaf.encode()+b'\0'+bytes.fromhex(e['sha']) for leaf,e in children)
    actual=gh('tree',b);need(actual==expected_sha,'tree identity '+name)
    objects.append(dict(path=name or '.',bytes=len(b),Git_SHA1=actual))
need(len(objects)==51,'51 reconstructed tree objects')
refs_path=P/'verification/negative-gramian-legacy-sol-20261116/REFERENCE_PINS.json'
rb,rpin=read(refs_path);refs=json.loads(rb)['all47_HTML_rows']
htmlmeta={'docs/'+x['path']:x for x in entries if x['type']=='blob' and x['path'].lower().endswith('.html')}
need(len(refs)==47 and {x['HTML_path'] for x in refs}==set(htmlmeta),'exact47HTML membership')
queries={
 '23331709':[r'23331709',r'\bsupersolv\w*',r'\btoh[aăâ]neanu',r'low[\s_-]*exponent',r'relation[\s_-]*incidence',r'(?:/pull/|\bpr\s*#?)618\b'],
 '23174156':[r'23174156',r'\bguadagnini\b',r'\bpilo\b',r'\bsu\s*\(?\s*5\s*\)?',r'lens[\s_-]*space',r'\bohtsuki\b',r'10400120',r'(?:/pull/|\bpr\s*#?)95\b']}
rows=[];total=0;typed=0
for row in refs:
    ref=row['actual_reference_file'];p=Path(ref['absolute_path']);b,pn=read(p)
    need((len(b),sha(b),pn['mode'])==(ref['bytes'],ref['sha256'],ref['mode']),'exact cache bytes/mode '+str(p))
    if row['typed_wrapper']:
        need(row['HTML_path']=='docs/papers/knudson-gradient-path/index.html' and len(b)==1863 and sha(b)=='ae49d075d4397ea90e634042a41c463251e7bc7e47d4ee836a0f2520167c59e3','only named exact typed wrapper')
        c=json.loads(b);need(c['isError'] is False and type(c['structuredContent']['content']) is str,'typed payload shape')
        b=c['structuredContent']['content'].encode('utf-8');typed+=1
    m=htmlmeta[row['HTML_path']]
    need(len(b)==row['HTML_bytes']==m['size'] and sha(b)==row['HTML_SHA256'] and gh('blob',b)==row['Git_blob']==m['sha'],'current whole HTML blob '+row['HTML_path'])
    need(row['Git_mode']==m['mode']=='100644','current HTML Git mode')
    text=b.decode('utf-8','strict');parser=Text();parser.feed(text);data=' '.join(parser.all)
    channels={'raw':text,'entities':html.unescape(text),'URL_decoded':unquote(text),'tag_text':data,'normalized':norm(data)}
    hits=[]
    for record,patterns in queries.items():
        matches=[]
        for pattern in patterns:
            for channel,value in channels.items():
                match=re.search(pattern,value,re.I)
                if match:matches.append(dict(pattern=pattern,channel=channel,snippet=value[max(0,match.start()-100):match.end()+130]))
        title=next(t['title'] for t in initial['targets'] if t['record']==record)
        if norm(title) in norm(data):matches.append(dict(channel='full_normalized_title',title=title))
        if matches:hits.append(dict(record=record,matches=matches))
    rows.append(dict(path=row['HTML_path'],title=' '.join(parser.title),h1=' '.join(parser.h1),bytes=len(b),SHA256=sha(b),Git_blob=m['sha'],Git_mode=m['mode'],reference=pn,typed_wrapper=row['typed_wrapper'],hits=hits))
    total+=len(b)
need(total==612221 and typed==1,'whole47HTML byte/typed extent')
metadata_hits=[]
for e in entries:
    hits=[record for record,patterns in queries.items() if any(re.search(pattern,e['path'],re.I) for pattern in patterns)]
    if hits:metadata_hits.append(dict(entry=e,records=hits))
print(json.dumps(dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS_CURRENT_DOCS_AUTHENTICATED_AND_BOUNDED_SEARCH_COMPLETE',
    remote_main=commit['sha'],docs_tree=tree['sha'],metadata_entries=len(entries),blob_metadata=sum(e['type']=='blob' for e in entries),tree_metadata=sum(e['type']=='tree' for e in entries),
    reconstructed_tree_objects=objects,complete_HTML_buffers=len(rows),complete_HTML_bytes=total,typed_wrappers=typed,queries=queries,
    input_pins=[op,cp,rp,tp,rpin],rows=rows,metadata_path_hits=metadata_hits,candidate_paths=[r['path'] for r in rows if r['hits']],
    semantic_correspondence_verdict=None,no_history_or_priority_claim=True,no_native_math_or_other_helper_execution=True,writes=0,redirect_authority=False),ensure_ascii=False,indent=2))
