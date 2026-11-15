"""Pure full approved-body presentation. No proof/source programme execution."""
from two_common import *
from two_dom import Tree,node,nodes,text,serialize
from html import escape as h
import copy,re
def inline_md(raw):
 # This bounded source uses only ordinary Markdown links and Unicode math.
 out=[];pos=0
 for m in re.finditer(r'\[([^\]]+)\]\(([^\s)]+)\)',raw):
  out.append(h(raw[pos:m.start()]));url=m.group(2);need(url.startswith('https://') or url in {'paper.pdf','source-and-verification.zip','SHA256SUMS.txt','citation.bib'},'119_approved_link_kind');out.append('<a href="'+h(url,quote=True)+'">'+h(m.group(1))+'</a>');pos=m.end()
 out.append(h(raw[pos:]));return ''.join(out)
def markdown_blocks(raw):
 lines=raw.splitlines();out=[];i=0
 while i<len(lines):
  line=lines[i]
  if not line.strip():i+=1;continue
  if line.startswith('```'):
   need(line=='```bibtex','only_original_bibtex_fence');i+=1;body=[]
   while i<len(lines) and lines[i]!='```':body.append(lines[i]);i+=1
   need(i<len(lines),'closed_original_bibtex_fence');out.append(('code','\n'.join(body)+'\n'));i+=1
  elif line.startswith('# '):out.append(('h1',line[2:]));i+=1
  elif line.startswith('## '):out.append(('h2',line[3:]));i+=1
  elif line.startswith('- '):
   items=[]
   while i<len(lines) and lines[i].startswith('- '):items.append(lines[i][2:]);i+=1
   out.append(('ul',items))
  else:
   body=[]
   while i<len(lines) and lines[i].strip() and not lines[i].startswith(('# ','## ','- ','```')):body.append(lines[i]);i+=1
   out.append(('p',' '.join(body)))
 return out
def body119(b):
 blocks=markdown_blocks(b['public_copy']);need(blocks[0]==('h1',b['title']),'119_complete_copy_title');html=['<main id="main"><article><header><h1><a href="/research/'+b['slug']+'/">'+h(b['title'])+'</a></h1>'];section=False;header=True;sid=0;reader=False
 def close_section():
  nonlocal reader
  if reader:
   html.append('<iframe class="paper-pdf" src="paper.pdf" title="'+h(b['original']['whole_requirements_original']['reader']['accessible_title'],quote=True)+'" loading="lazy"></iframe>');reader=False
  html.append('</section>')
 for kind,value in blocks[1:]:
  if kind=='h2':
   if header:html.append('</header>');header=False
   if section:close_section()
   sid+=1;reader=value=='Read the complete paper';section=True
   ident='abstract' if value=='Original abstract' else 'reader' if reader else 'part-'+str(sid)
   html.append('<section id="'+ident+'"><h2>'+h(value)+'</h2>')
  elif kind=='p':
   chunk=inline_md(value)
   # Add real download semantics only to already approved source links in
   # the complete reader paragraph; no words or destinations are changed.
   if reader:
    for name in ['paper.pdf','source-and-verification.zip','SHA256SUMS.txt','citation.bib']:
     if name=='paper.pdf':chunk=chunk.replace('<a href="paper.pdf">download it</a>','<a href="paper.pdf" download="paper.pdf">download it</a>')
     else:chunk=chunk.replace('<a href="'+name+'">','<a href="'+name+'" download="'+name+'">')
   html.append('<p>'+chunk+'</p>')
  elif kind=='ul':html.append('<ul>'+''.join('<li>'+inline_md(item)+'</li>' for item in value)+'</ul>')
  elif kind=='code':
   need(value==b['bib'].decode(),'whole119_printed_BibTeX');lines=value.splitlines(keepends=True);html.append('<div class="equation"><code>'+''.join(h(line)+('<br>' if i<len(lines)-1 else '') for i,line in enumerate(lines))+'</code></div>')
  else:raise ValueError('two_stage:unexpected119_copy_block')
 if section:close_section()
 if header:html.append('</header>')
 html.append('</article></main>');doc='<!doctype html><html><head><title>x</title></head><body>'+''.join(html)+'</body></html>';return Tree(doc).find('main')[0]
def main_tree(b):
 if b['rid']=='22983513':return body119(b)
 original=copy.deepcopy(Tree(b['source_html'],source_editorial=True).find('main')[0]);original['attrs']={'id':'main'};original['children']=[node('article',{},original['children'])]
 for n in nodes(original):
  a=n['attrs']
  for field in ['href','src']:
   if a.get(field,'').startswith('assets/'):
    name=a[field][7:];need(name in {x['name'] for x in b['assets']}|{'citation.bib'},'118_exact_approved_asset_rebase');a[field]=name
  if a.get('class')=='byline':a['class']='entry-meta'
  if n['tag']=='h1':need(text(n)==b['title'],'118_exact_title');n['children']=[node('a',{'href':'/research/'+b['slug']+'/'},n['children'])]
  if n['tag']=='iframe':a['class']='paper-pdf';a['loading']='lazy'
 return original
