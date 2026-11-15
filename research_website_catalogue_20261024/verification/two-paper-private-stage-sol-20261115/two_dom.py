"""Closed static document tree for the two new articles. Source-only direct main sections are explicitly permitted when reading the frozen118 preview; candidates require article containment. No production imports or client runtime.
"""
from html import escape as h
from html.parser import HTMLParser
import re
from two_common import need
VOID={'meta','link','br','hr'}
def node(tag,attrs=None,children=None):return {'tag':tag,'attrs':dict(attrs or {}),'children':list(children or [])}
def text(n):return ''.join(text(x) if isinstance(x,dict) else x for x in n['children'])
def nodes(n):
 yield n
 for c in n['children']:
  if isinstance(c,dict):yield from nodes(c)
def serialize(n):
 if isinstance(n,str):return h(n,quote=False)
 a=''.join(' '+k if v is None else ' '+k+'="'+h(v,quote=True)+'"' for k,v in n['attrs'].items())
 return '<'+n['tag']+a+'>'+('' if n['tag'] in VOID else ''.join(serialize(x) for x in n['children'])+'</'+n['tag']+'>')
class Tree(HTMLParser):
 def __init__(self,source,*,source_editorial=False):
  super().__init__(convert_charrefs=True);self.stack=[];self.roots=[];self.decl=0;self.source_editorial=source_editorial
  self.feed(source);self.close();need(not self.stack and self.decl==1,'complete_balanced_HTML')
  need([x['tag'] for x in self.roots]==['html'],'one_HTML_root')
  need([x['tag'] for x in self.roots[0]['children'] if isinstance(x,dict)]==['head','body'],'ordered_head_body')
 def handle_decl(self,d):need(d.lower()=='doctype html' and self.decl==0 and not self.stack,'doctype');self.decl+=1
 def handle_comment(self,d):raise ValueError('five_stage:document_comment')
 def handle_pi(self,d):raise ValueError('five_stage:processing_instruction')
 def handle_starttag(self,t,attrs):
  parent=self.stack[-1]['tag'] if self.stack else None
  rules={'html':{None},'head':{'html'},'body':{'html'},'title':{'head'},'meta':{'head'},'link':{'head'},'style':{'head'},'script':{'head'},'header':{'body','article'},'nav':{'header','main'},'main':{'body'},'article':{'main'},'section':{'article'},'footer':{'body','article'},'h1':{'header','article'},'h2':{'section','article','footer'},'h3':{'section','article'},'p':{'header','section','article','footer'},'div':{'section','article'},'span':{'p','div','span','a','li','strong','i','em','cite'},'strong':{'p','li','span'},'i':{'p','li','a','span'},'em':{'p','li','a','span'},'cite':{'p'},'sub':{'p','div','span','sub','sup'},'sup':{'p','div','span','sub','sup'},'a':{'body','p','nav','h1','li'},'time':{'p'},'br':{'p','div','span','li'},'hr':{'article','footer'},'ul':{'section','article'},'ol':{'section','article'},'li':{'ul','ol'},'iframe':{'section','article'}}
  if self.source_editorial:
   rules['header']=rules['header']|{'main'};rules['section']=rules['section']|{'main'}
  rules['p']=rules['p']|{'iframe'}
  rules['pre']={'section','article'};rules['code']={'pre','div'}
  need(t in rules and parent in rules[t],'closed_parent_grammar:'+str(parent)+'/'+t)
  a=dict(attrs);need(len(a)==len(attrs),'no_duplicate_attribute')
  allowed={'html':{'lang'},'meta':{'charset','name','property','content'},'link':{'rel','href'},'script':{'type'},'a':{'class','href','target','rel','download'},'p':{'class','id'},'nav':{'aria-label'},'main':{'id'},'h2':{'id'},'time':{'datetime'},'section':{'id','aria-labelledby'},'footer':{'id'},'iframe':{'class','id','src','title','loading'},'div':{'class','role','aria-label','data-tex'},'span':{'class','role','aria-label','data-tex'}}.get(t,set())
  if self.source_editorial and t=='span':allowed=allowed|{'style'}
  need(set(a)<=allowed,'allowed_visible_attributes:'+t)
  need(not any(k in a for k in ['hidden','inert','aria-hidden']) and not any(k.startswith('on') for k in a),'no_hidden_or_event_attributes')
  if 'style' in a:need(self.source_editorial and t=='span' and a['style']=='white-space: nowrap','only_original_inline_math_nowrap')
  if 'class' in a:need(set(a['class'].split())<={'skip-link','site-title','entry-meta','paper-pdf','copyright','byline','formula','equation','result','citation'}|({'meta','skip'} if self.source_editorial else set()),'known_nonhiding_class')
  n=node(t,a);(self.stack[-1]['children'] if self.stack else self.roots).append(n)
  if t not in VOID:self.stack.append(n)
 def handle_endtag(self,t):need(self.stack and self.stack[-1]['tag']==t,'balanced_nesting:'+t);self.stack.pop()
 def handle_data(self,d):
  if not self.stack:need(not d.strip(),'no_outer_document_text');return
  need(not(d.strip() and self.stack[-1]['tag'] in {'html','head','body','main','article','section','footer'}),'no_unlabelled_outer_body_text')
  self.stack[-1]['children'].append(d)
 def find(self,tag):return [x for x in nodes(self.roots[0]) if x['tag']==tag]
