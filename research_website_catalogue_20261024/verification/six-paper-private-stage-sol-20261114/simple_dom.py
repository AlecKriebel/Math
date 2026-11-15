"""Closed static-document grammar and independent visible text collector."""
from html.parser import HTMLParser

class Document(HTMLParser):
    def __init__(self,html):
        super().__init__(convert_charrefs=True);self.tags=[];self.stack=[];self.faults=[];self.doctypes=[];self.body=False;self.bodies=0;self.parts=[];self.anchors=[];self.anchor=None;self.h1s=[];self.h1=None
        self.feed(html);self.close()
        if self.stack:self.faults.append('unclosed_document')
    def handle_decl(self,d):
        self.doctypes.append(d.casefold())
        if d.casefold()!='doctype html' or self.stack:self.faults.append('unexpected_declaration')
    def unknown_decl(self,d):self.faults.append('unknown_declaration')
    def handle_pi(self,d):self.faults.append('processing_instruction')
    def handle_starttag(self,t,attrs):
        parent=self.stack[-1] if self.stack else None
        parents={'html':{None},'head':{'html'},'body':{'html'},'meta':{'head'},'link':{'head'},'title':{'head'},'script':{'head'},'a':{'body','p','nav','h1','li'},'header':{'body','article'},'p':{'header','section','article','footer'},'nav':{'header'},'main':{'body'},'article':{'main'},'h1':{'header'},'h2':{'section'},'br':{'p'},'time':{'p'},'strong':{'p'},'hr':{'article','footer'},'section':{'article'},'iframe':{'section'},'ul':{'section'},'li':{'ul'},'i':{'p'},'footer':{'body'}}
        if t not in parents or parent not in parents[t]:self.faults.append('unknown_or_misnested:'+str(parent)+'/'+t)
        if t not in {'meta','link','br','hr'}:self.stack.append(t)
        a=dict(attrs);self.tags.append((t,a))
        if len(a)!=len(attrs):self.faults.append('duplicate_attribute')
        if any(k in a for k in ('hidden','inert','style','aria-hidden')) or any(k.startswith('on') for k in a):self.faults.append('visibility_or_event_attribute')
        allowed={'html':{'lang'},'meta':{'charset','name','property','content'},'link':{'rel','href'},'script':{'type'},'a':{'class','href','download'},'p':{'class'},'nav':{'aria-label'},'main':{'id'},'time':{'datetime'},'section':{'id'},'iframe':{'class','src','title','loading'}}.get(t,set())
        if set(a)-allowed:self.faults.append('unknown_attribute:'+t)
        if 'class' in a and a['class'] not in ('skip-link','site-title','entry-meta','paper-pdf','copyright'):self.faults.append('unknown_class')
        if t=='body':self.body=True;self.bodies+=1
        if self.body:
            self.parts.append(' ')
            if t=='a':self.anchor=[a,[]]
            if t=='h1':self.h1=[]
    def handle_endtag(self,t):
        if self.body:
            self.parts.append(' ')
            if t=='a' and self.anchor:
                self.anchors.append((self.anchor[0],' '.join(''.join(self.anchor[1]).split())));self.anchor=None
            if t=='h1' and self.h1 is not None:self.h1s.append(' '.join(''.join(self.h1).split()));self.h1=None
        if not self.stack or self.stack[-1]!=t:self.faults.append('unbalanced:'+t)
        else:self.stack.pop()
        if t=='body':self.body=False
    def handle_data(self,d):
        if d.strip() and (not self.stack or self.stack[-1] in {'html','head'}):self.faults.append('unexpected_document_text')
        if self.body:
            self.parts.append(d)
            if self.anchor:self.anchor[1].append(d)
            if self.h1 is not None:self.h1.append(d)
    def handle_comment(self,d):self.faults.append('comment')
    @property
    def text(self):return ' '.join(''.join(self.parts).split())
