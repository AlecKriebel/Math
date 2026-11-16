"""One read-only cached current-corpus authentication/search. No network, Git, subprocess or writes."""
from pathlib import Path,PurePosixPath
from html.parser import HTMLParser
from urllib.parse import unquote
import datetime,hashlib,html,json,re,stat,sys,unicodedata
O=Path(__file__).resolve().parent
if len(sys.argv)!=1:raise SystemExit('Only the ordinary read-only default is supported')
def need(x,m):
 if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def exact(q,v):
 b=q.read_bytes();need(q.is_file() and not q.is_symlink() and len(b)==v['bytes'] and sha(b)==v['sha256'],'Exact input pin '+str(q));return b
def objhash(kind,b):return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def norm(s):return ' '.join(re.sub(r'[^\w]+',' ',unicodedata.normalize('NFKC',s).casefold(),flags=re.UNICODE).split())
class Text(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.data=[];self.titles=[];self.h1=[];self.in_title=False;self.in_h1=False
 def handle_starttag(self,t,a):
  if t=='title':self.in_title=True
  if t=='h1':self.in_h1=True
 def handle_endtag(self,t):
  if t=='title':self.in_title=False
  if t=='h1':self.in_h1=False
 def handle_data(self,d):
  self.data.append(d)
  if self.in_title:self.titles.append(d)
  if self.in_h1:self.h1.append(d)
plan=json.loads((O/'TARGETS.json').read_text());refs=json.loads((O/'CURRENT_REFS.json').read_text())
need(refs['remote_commit_docs_tree']==plan['docs_tree'] and refs['ordinary_remote_main']==refs['local_tracking_main'],'Current ref/tree binding')
inv=json.loads(exact(Path(plan['input_inventory']['path']),plan['input_inventory']))
outer=json.loads(exact(Path(plan['input_tree']['path']),plan['input_tree']))
need(outer['isError'] is False and type(outer['structuredContent']) is dict and type(outer['structuredContent']['content']) is str,'Exact tree connector type')
tree=json.loads(outer['structuredContent']['content']);need(tree['sha']==plan['docs_tree'] and tree['truncated'] is False,'Complete expected native tree')
entries=tree['tree'];need(len(entries)==304 and len({x['path'] for x in entries})==304,'Complete unique tree304')
for x in entries:
 pp=PurePosixPath(x['path']);need(not pp.is_absolute() and all(y not in ('','..','.') for y in pp.parts),'Safe metadata path')
 need((x['mode'],x['type']) in [('100644','blob'),('040000','tree')],'Expected current tree mode/type')
treeids={'':tree['sha'],**{x['path']:x['sha'] for x in entries if x['type']=='tree'}}
reconstructed=[]
for name,expected in sorted(treeids.items()):
 prefix=name+'/' if name else '';children=[]
 for x in entries:
  if not x['path'].startswith(prefix):continue
  leaf=x['path'][len(prefix):]
  if '/' not in leaf:children.append((leaf,x))
 children.sort(key=lambda q:q[0].encode()+(b'/' if q[1]['type']=='tree' else b'\0'))
 body=b''.join(x['mode'].lstrip('0').encode()+b' '+leaf.encode()+b'\0'+bytes.fromhex(x['sha']) for leaf,x in children)
 actual=objhash('tree',body);need(actual==expected,'Git tree identity '+name)
 reconstructed.append({'path':name or '.', 'sha':actual,'bytes':len(body),'children':len(children)})
need(len(reconstructed)==51,'Exactly51 reconstructed Git tree objects')
htmlentries={'docs/'+x['path']:x for x in entries if x['type']=='blob' and x['path'].lower().endswith('.html')}
rows=inv['rows'];need(len(rows)==47 and set(htmlentries)=={x['path'] for x in rows},'Exact47 current HTML paths')
result=[];total=0;typed=0;rawcount=0;candidate=[]
for row in rows:
 ref=row['body_reference'];q=Path(ref['path']);k=plan['typed_Knudson']
 if row['path']==k['HTML_path']:
  need(set(ref)=={'path','container'} and ref['path']==k['container_path'] and ref['container']=='structuredContent.content UTF-8','Only named typed Knudson reference')
  container=exact(q,{'bytes':k['container_bytes'],'sha256':k['container_sha256']});x=json.loads(container)
  need(x['isError'] is False and type(x['structuredContent']) is dict and type(x['structuredContent']['content']) is str,'Exact Knudson container type')
  b=x['structuredContent']['content'].encode('utf-8');need(len(b)==k['decoded_bytes'] and sha(b)==k['decoded_sha256'],'Exact Knudson decoded body');typed+=1
 else:
  need(set(ref)=={'path','bytes','SHA256'},'Other46 refs must be raw byte locators')
  b=exact(q,{'bytes':ref['bytes'],'sha256':ref['SHA256']});rawcount+=1
 meta=htmlentries[row['path']]
 need(len(b)==row['bytes']==meta['size'] and sha(b)==row['SHA256'] and objhash('blob',b)==row['Git_blob']==meta['sha'],'Whole HTML row/Git blob identity '+row['path'])
 need(stat.S_IMODE(q.stat().st_mode)==0o644,'Observed reference file mode0644')
 text=b.decode('utf-8','strict');parser=Text();parser.feed(text);data=' '.join(parser.data)
 channels={'raw':text,'entity':html.unescape(text),'tag_data':data,'URL':unquote(text),'normalized':norm(html.unescape(data))};compact=re.sub(r'[^\w]','',norm(html.unescape(text)))
 hits=[]
 for query in plan['queries']:
  evidence=[]
  for label,value in channels.items():
   m=re.search(query['regex'],value,re.I|re.S)
   if m:evidence.append({'channel':label,'span':list(m.span()),'snippet':value[max(0,m.start()-80):min(len(value),m.end()+100)]})
  for literal in query['compact']:
   target=re.sub(r'[^\w]','',norm(literal));pos=compact.find(target)
   if pos>=0:evidence.append({'channel':'specified_compact','literal':literal,'offset':pos})
  if evidence:hits.append({'query':query['name'],'evidence':evidence})
 if hits:candidate.append(row['path'])
 total+=len(b);result.append({'path':row['path'],'title':' '.join(parser.titles),'h1':' '.join(parser.h1),'bytes':len(b),'SHA256':sha(b),'Git_blob':meta['sha'],'Git_mode':meta['mode'],'reference_file':str(q),'reference_mode':'0644','typed_wrapper':row['path']==k['HTML_path'],'matched_queries':hits})
need(total==612221 and rawcount==46 and typed==1,'Whole current47 corpus byte/typed extent')
print(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_AUTHENTICATED_SEARCH_COMPLETE','remote_main':refs['ordinary_remote_main'],'docs_tree':tree['sha'],'metadata_entries':304,'reconstructed_tree_objects':reconstructed,'complete_HTML_buffers':47,'complete_HTML_bytes':total,'raw_references':rawcount,'exact_typed_Knudson':typed,'UTF8_errors':[],'queries':plan['queries'],'rows':result,'candidate_paths':candidate,'semantic_verdict':None,'no_history_or_global_absence_claim':True,'no_scripts_executed':True,'writes':0,'publication_or_redirect_authority':False},ensure_ascii=False,indent=2))
