"""Pure static contract for this one draft, not an application helper."""
from html.parser import HTMLParser
import re
DEST='https://aleckriebel.com/research/lipschitz-nonincreasing-unitary-deformation/'
TITLE='A Lipschitz-nonincreasing deformation of small unitary-valued maps'
class Page(HTMLParser):
 def __init__(self,text):super().__init__(convert_charrefs=True);self.tags=[];self.scripts=[];self.script=None;self.feed(text)
 def handle_starttag(self,t,a):
  self.tags.append((t,dict(a)))
  if t=='script':self.script=''
 def handle_data(self,d):
  if self.script is not None:self.script+=d
 def handle_endtag(self,t):
  if t=='script' and self.script is not None:self.scripts.append(self.script);self.script=None
def need(ok,s):
 if not ok:raise ValueError(s)
def validate(text):
 p=Page(text)
 need(text.startswith('<!doctype html>'),'standard HTML doctype')
 need([a for t,a in p.tags if t=='link']==[{'rel':'canonical','href':DEST}],'one exact clean canonical')
 need([a for t,a in p.tags if t=='meta' and 'http-equiv' in a]==[{'http-equiv':'refresh','content':'0; url='+DEST}],'clean static meta refresh fallback')
 need([a for t,a in p.tags if t=='a']==[{'href':DEST}],'one visible fallback destination')
 need('<h1>Paper moved</h1>' in text and TITLE+'</a> is now on AlecKriebel.com.' in text,'clear visible fallback')
 need([a for t,a in p.tags if t=='script']==[{}] and len(p.scripts)==1,'one inline script, no external code')
 source=p.scripts[0]
 for s in ['new URL("'+DEST+'")','target.search = window.location.search;','target.hash = window.location.hash;','window.location.replace(target.href);']:need(s in source,'actual fixed URL/search/hash/replace '+s)
 need(not any(t in {'iframe','img','base','form'} for t,a in p.tags),'no other content/assets/redirect base')
 return True
def static_controls(text):
 validate(text);changes={
 'wrong canonical':text.replace('rel="canonical" href="'+DEST+'"','rel="canonical" href="https://example.org/"',1),
 'wrong meta destination':text.replace('content="0; url='+DEST+'"','content="0; url=https://example.org/"',1),
 'wrong fallback destination':text.replace('<a href="'+DEST+'"','<a href="https://example.org/"',1)}
 rejected=[]
 for name,bad in changes.items():
  need(bad!=text,'actual mutation')
  try:validate(bad)
  except ValueError:rejected.append(name)
  else:raise ValueError('accepted static defect '+name)
 return rejected
