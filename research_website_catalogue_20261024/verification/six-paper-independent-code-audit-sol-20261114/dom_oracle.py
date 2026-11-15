"""Independent semantic body oracle, authored before candidate-code access.

Input is approved prose, never builder-produced expected hashes. This is a
bounded static DOM/inline-visibility check; complete CSS/layout needs review.
"""
from html.parser import HTMLParser
import re,unicodedata
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
INACTIVE={'head','script','style','template','noscript','textarea','select','option'}
BLOCK={'p','div','section','article','main','header','footer','nav','pre','blockquote','h1','h2','h3','h4','h5','h6','li','br'}
def norm(s):return ' '.join(unicodedata.normalize('NFC',s).split())
class Node:
 def __init__(self,tag='',attrs=(),parent=None):self.tag=tag;self.attrs=dict(attrs);self.parent=parent;self.children=[]
 def all(self):
  yield self
  for c in self.children:
   if isinstance(c,Node):yield from c.all()
class Parse(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.root=Node('document');self.stack=[self.root]
 def handle_starttag(self,t,a):
  n=Node(t,a,self.stack[-1]);self.stack[-1].children.append(n)
  if t not in VOID:self.stack.append(n)
 def handle_startendtag(self,t,a):
  self.handle_starttag(t,a)
  if t not in VOID:self.handle_endtag(t)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==t:self.stack=self.stack[:i];return
 def handle_data(self,d):self.stack[-1].children.append(d)
def active(n):
 while n:
  a=n.attrs;st=re.sub(r'\s+','',a.get('style','').lower())
  if n.tag in INACTIVE or any(k in a for k in ['hidden','inert']) or a.get('aria-hidden','').lower()=='true':return False
  if any(x in st for x in ['display:none','visibility:hidden','visibility:collapse','content-visibility:hidden','opacity:0;','opacity:0.0;','transform:scale(0)']):return False
  if re.search(r'(?:^|;)opacity:0(?:\.0+)?(?:!important)?(?:;|$)',st):return False
  n=n.parent
 return True
def text(n):
 if not active(n):return ''
 out=''
 for c in n.children:
  if isinstance(c,str):out+=c
  else:
   t=text(c)
   out+=(' '+t+' ') if c.tag in BLOCK else t
 return out
def need(ok,label):
 if not ok:raise ValueError(label)
def validate_body(html,expected):
 p=Parse();p.feed(html);p.close();nodes=list(p.root.all());mains=[n for n in nodes if n.tag=='main' and active(n)];need(len(mains)==1,'exactly one active main wrapper')
 articles=[n for n in mains[0].all() if n.tag=='article' and active(n)];need(len(articles)<=1,'unambiguous active article wrapper');root=articles[0] if articles else mains[0]
 body=norm(text(root));cursor=0
 for block in expected['blocks']:
  want=norm(block['text']);pos=body.find(want,cursor);need(pos>=0,'missing or changed complete body block '+str(block['ordinal']));cursor=pos+len(want)
 headings=[norm(text(n)) for n in root.all() if n.tag=='h2' and active(n)]
 need(headings==expected['h2_headings'],'complete ordered section headings')
 need(body.count(norm(expected['abstract']))==1,'one full visible original abstract')
 links=[n for n in root.all() if n.tag=='a' and active(n)]
 for want in expected.get('visible_links',[]):
  need(any(norm(text(n))==norm(want['label']) and n.attrs.get('href')==want['href'] for n in links),'visible article anchor '+want['label'])
 need(not any(s in body for s in expected.get('forbidden_private_tokens',[])),'no private audit leakage')
 return {'status':'PASS_INDEPENDENT_SEMANTIC_BODY','blocks':len(expected['blocks']),'h2':len(headings),'links':len(links),'body_root':root.tag}
def private_fixture_controls():
 spec={'blocks':[{'ordinal':1,'text':'Complete original abstract.'},{'ordinal':2,'text':'For every t ∈ [0,1], B = −8π.'},{'ordinal':3,'text':'The second paragraph retains the category limitation.'}],'h2_headings':['Original abstract','The result'],'abstract':'Complete original abstract.','visible_links':[{'label':'Prior theorem','href':'https://example.org/primary'}]}
 body='<h2>Original abstract</h2><p>Complete original abstract.</p><h2>The result</h2><p>For every t ∈ [0,1], B = −8π.</p><p>The second paragraph retains the category limitation.</p><a href="https://example.org/primary">Prior theorem</a>'
 good='<html><body><main><article>'+body+'</article></main></body></html>';validate_body(good,spec)
 cases={}
 for tag in ['template','noscript','script','textarea']:cases['all content only in '+tag]='<main><article><'+tag+'>'+body+'</'+tag+'></article></main>'
 for attrs in ['hidden','inert','aria-hidden="true"','style="display:none"','style="visibility:hidden"','style="content-visibility:hidden"','style="opacity:0"']:
  cases['ancestor '+attrs]='<main><article><div '+attrs+'>'+body+'</div></article></main>'
 cases['outside main wrapper']='<div>'+body+'</div><main><article></article></main>'
 cases['outside article wrapper']='<main>'+body+'<article></article></main>'
 cases['nonleading paragraph omitted']=good.replace('<p>The second paragraph retains the category limitation.</p>','')
 cases['nonleading clause removed']=good.replace('the category limitation','a limitation')
 cases['minus sign removed']=good.replace('−8π','8π')
 cases['closed endpoint narrowed']=good.replace('[0,1]','[0,1)')
 cases['reordered section heading']=good.replace('<h2>The result</h2>','<h2>Summary</h2>')
 cases['correct link hidden']=good.replace('<a href=','<a hidden href=')
 cases['correct label wrong link']=good.replace('https://example.org/primary','https://example.org/unrelated')
 rejected=[]
 for name,html in cases.items():
  try:validate_body(html,spec)
  except ValueError:rejected.append(name)
  else:raise ValueError('fixture corruption accepted: '+name)
 return {'status':'PASS_PRIVATE_PREFLIGHT_FIXTURES','positive_fixture':1,'negative_fixtures_rejected':len(rejected),'names':rejected,'not_a_candidate_audit':True,'bounded_static_visibility_not_full_CSS_layout_certification':True}
if __name__=='__main__':
 import json
 print(json.dumps(private_fixture_controls(),indent=2))
