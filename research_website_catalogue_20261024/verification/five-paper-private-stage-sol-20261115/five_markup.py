"""Closed HTML tree and small, fully visible Markdown/TeX presentation subset.
No client runtime, network, imports of production renderers, or hidden article.
Math retains its exact original TeX in data-tex while displaying HTML symbols.
"""
from html import escape as h
from html.parser import HTMLParser
import re
from five_common import need
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
 def __init__(self,source,*,source_math_style=False):
  super().__init__(convert_charrefs=True);self.stack=[];self.roots=[];self.decl=0;self.source_math_style=source_math_style
  self.feed(source);self.close();need(not self.stack and self.decl==1,'complete_balanced_HTML')
  need([x['tag'] for x in self.roots]==['html'],'one_HTML_root')
  need([x['tag'] for x in self.roots[0]['children'] if isinstance(x,dict)]==['head','body'],'ordered_head_body')
 def handle_decl(self,d):need(d.lower()=='doctype html' and self.decl==0 and not self.stack,'doctype');self.decl+=1
 def handle_comment(self,d):raise ValueError('five_stage:document_comment')
 def handle_pi(self,d):raise ValueError('five_stage:processing_instruction')
 def handle_starttag(self,t,attrs):
  parent=self.stack[-1]['tag'] if self.stack else None
  rules={'html':{None},'head':{'html'},'body':{'html'},'title':{'head'},'meta':{'head'},'link':{'head'},'style':{'head'},'script':{'head'},'header':{'body','article'},'nav':{'header','main'},'main':{'body'},'article':{'main'},'section':{'article'},'footer':{'body','article'},'h1':{'header','article'},'h2':{'section','article','footer'},'h3':{'section','article'},'p':{'header','section','article','footer'},'div':{'section','article'},'span':{'p','div','span','a','li','strong','i','em','cite'},'strong':{'p','li','span'},'i':{'p','li','a','span'},'em':{'p','li','a','span'},'cite':{'p'},'sub':{'p','div','span','sub','sup'},'sup':{'p','div','span','sub','sup'},'a':{'body','p','nav','h1','li'},'time':{'p'},'br':{'p','div','span','li'},'hr':{'article','footer'},'ul':{'section','article'},'ol':{'section','article'},'li':{'ul','ol'},'iframe':{'section','article'}}
  need(t in rules and parent in rules[t],'closed_parent_grammar:'+str(parent)+'/'+t)
  a=dict(attrs);need(len(a)==len(attrs),'no_duplicate_attribute')
  allowed={'html':{'lang'},'meta':{'charset','name','property','content'},'link':{'rel','href'},'script':{'type'},'a':{'class','href','target','rel','download'},'p':{'class','id'},'nav':{'aria-label'},'main':{'id'},'h2':{'id'},'time':{'datetime'},'section':{'id','aria-labelledby'},'footer':{'id'},'iframe':{'class','id','src','title','loading'},'div':{'class','role','aria-label','data-tex'},'span':{'class','role','aria-label','data-tex'}}.get(t,set())
  if self.source_math_style and t=='span':allowed=allowed|{'style'}
  need(set(a)<=allowed,'allowed_visible_attributes:'+t)
  need(not any(k in a for k in ['hidden','inert','aria-hidden']) and not any(k.startswith('on') for k in a),'no_hidden_or_event_attributes')
  if 'style' in a:need(self.source_math_style and t=='span' and a['style']=='white-space: nowrap','only_original_inline_math_nowrap')
  if 'class' in a:need(set(a['class'].split())<={'skip-link','site-title','entry-meta','paper-pdf','copyright','byline','formula','equation','result','citation'}|({'meta','skip'} if self.source_math_style else set()),'known_nonhiding_class')
  n=node(t,a);(self.stack[-1]['children'] if self.stack else self.roots).append(n)
  if t not in VOID:self.stack.append(n)
 def handle_endtag(self,t):need(self.stack and self.stack[-1]['tag']==t,'balanced_nesting:'+t);self.stack.pop()
 def handle_data(self,d):
  if not self.stack:need(not d.strip(),'no_outer_document_text');return
  need(not(d.strip() and self.stack[-1]['tag'] in {'html','head','body','main','article','section','footer'}),'no_unlabelled_outer_body_text')
  self.stack[-1]['children'].append(d)
 def find(self,tag):return [x for x in nodes(self.roots[0]) if x['tag']==tag]
class Math:
 def __init__(self,s):self.s=s;self.i=0;self.env=[]
 def skip(self):
  while self.i<len(self.s) and self.s[self.i].isspace():self.i+=1
 def raw_atom(self):
  self.skip();need(self.i<len(self.s),'TeX_atom')
  if self.s[self.i]=='{':
   self.i+=1;start=self.i;depth=1
   while self.i<len(self.s) and depth:
    if self.s[self.i]=='{':depth+=1
    elif self.s[self.i]=='}':depth-=1
    self.i+=1
   need(depth==0,'balanced_TeX_group');return self.s[start:self.i-1]
  a=self.s[self.i];self.i+=1;return a
 def atom(self):
  self.skip();need(self.i<len(self.s),'TeX_script_atom')
  if self.s[self.i]=='{':return Math(self.raw_atom()).run()
  if self.s[self.i]=='\\':return self.command()
  c=self.s[self.i];self.i+=1;return h(c)
 def command(self):
  self.i+=1;need(self.i<len(self.s),'TeX_command')
  if not self.s[self.i].isalpha():
   c=self.s[self.i];self.i+=1
   return {'\\':'<br>','{':'{','}':'}',' ':' ', ',':'\u2009',';':' ','!':'','_':'_','%':'%','&':'&amp;'}.get(c,h(c))
  m=re.match(r'[A-Za-z]+',self.s[self.i:]);cmd=m.group();self.i+=len(cmd)
  symbols={'alpha':'α','beta':'β','phi':'φ','epsilon':'ε','ell':'ℓ','mu':'μ','lambda':'λ','tau':'τ','delta':'δ','infty':'∞','in':'∈','notin':'∉','to':'→','mapsto':'↦','ne':'≠','neq':'≠','le':'≤','leq':'≤','ge':'≥','geq':'≥','forall':'∀','exists':'∃','times':'×','oplus':'⊕','cap':'∩','cup':'∪','subset':'⊂','subseteq':'⊆','langle':'⟨','rangle':'⟩','cdot':'·','ldots':'…','cdots':'…','quad':' ','qquad':'\u2003','left':'','right':''}
  if cmd in symbols:return symbols[cmd]
  if cmd in {'mathrm','operatorname','text'}:return h(self.raw_atom())
  if cmd in {'mathbb','mathcal'}:
   a=self.raw_atom();tables={'mathbb':{'R':'ℝ','Z':'ℤ','N':'ℕ','Q':'ℚ','C':'ℂ'},'mathcal':{'A':'𝒜','B':'ℬ','G':'𝒢','M':'ℳ','N':'𝒩'}}
   need(a in tables[cmd],'explicit_TeX_alphabet:'+cmd+':'+a);return tables[cmd][a]
  if cmd in {'bar','overline'}:
   a=self.atom();need(re.fullmatch(r'[^<](?:<sub>.*</sub>)?',a) is not None,'explicit_single_base_overbar')
   return a[0]+'\u0304'+a[1:]
  if cmd=='frac':return '('+self.atom()+')/('+self.atom()+')'
  if cmd in {'begin','end'}:
   a=self.raw_atom();need(a=='cases','only_explicit_cases_environment')
   if cmd=='begin':self.env.append(a);return '{ '
   need(self.env and self.env.pop()==a,'balanced_cases_environment');return ' }'
  raise ValueError('five_stage:unknown_TeX_command:'+cmd)
 def run(self):
  out=[]
  while self.i<len(self.s):
   c=self.s[self.i]
   if c=='\\':out.append(self.command())
   elif c in '^_':self.i+=1;tag='sup' if c=='^' else 'sub';out.append('<'+tag+'>'+self.atom()+'</'+tag+'>')
   elif c=='{':out.append(Math(self.raw_atom()).run())
   elif c=='}':raise ValueError('five_stage:unexpected_TeX_closing_group')
   else:out.append(' ' if c=='&' else h(c));self.i+=1
  need(not self.env,'closed_TeX_environment');return ''.join(out)
def math_html(raw,block=False):
 tag='div' if block else 'span';return '<'+tag+' class="equation" role="math" data-tex="'+h(raw,quote=True)+'" aria-label="'+h(raw,quote=True)+'">'+Math(raw).run()+'</'+tag+'>'
def inline(s):
 out=[];i=0
 while i<len(s):
  if s[i]=='$':
   j=s.find('$',i+1);need(j>i+1,'balanced_inline_math');out.append(math_html(s[i+1:j]));i=j+1
  elif s.startswith('**',i):
   j=s.find('**',i+2);need(j>=0,'balanced_bold');out.append('<strong>'+inline(s[i+2:j])+'</strong>');i=j+2
  elif s[i]=='*':
   j=s.find('*',i+1);need(j>=0,'balanced_italics');out.append('<i>'+inline(s[i+1:j])+'</i>');i=j+1
  elif s[i]=='[' and (j:=s.find('](',i+1))>=0:
   k=j+2;depth=1;start=k
   while k<len(s) and depth:
    if s[k]=='(':depth+=1
    elif s[k]==')':depth-=1
    k+=1
   need(depth==0,'balanced_link');url=s[start:k-1];need(url.startswith(('https://','/research/')),'ordinary_MD_link')
   out.append('<a href="'+h(url,quote=True)+'">'+inline(s[i+1:j])+'</a>');i=k
  else:out.append(h(s[i]));i+=1
 return ''.join(out)
def block(s):
 if s.startswith('$$') and s.endswith('$$'):return math_html(s[2:-2],True)
 if s.startswith('### '):return '<h3>'+inline(s[4:])+'</h3>'
 return '<p>'+inline(s)+'</p>'
def background(s):
 out=[];items=[]
 for line in s.splitlines():
  if line.startswith('* '):items.append('<li>'+inline(line[2:])+'</li>')
  elif line.strip():
   if items:out.append('<ul>'+''.join(items)+'</ul>');items=[]
   out.append(block(line))
 if items:out.append('<ul>'+''.join(items)+'</ul>')
 return ''.join(out)
