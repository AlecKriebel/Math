"""Passive HTML document extraction, preserving MathML TeX alttext."""
from pathlib import Path
from html.parser import HTMLParser
A=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23204176/reviews/adversarial-sol-continuation-20261117/classical-primary')
class Reader(HTMLParser):
    def __init__(self):super().__init__();self.rows=[];self.ignore=0;self.math=0
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if t in ['script','style']:self.ignore+=1
        if t=='math':
            if 'alttext' in a:self.rows.append(' '+a['alttext']+' ')
            self.math+=1
        if t in ['p','h1','h2','h3','h4','div','section','li','br','tr']:self.rows.append('\n')
    def handle_endtag(self,t):
        if t in ['script','style']:self.ignore-=1
        if t=='math':self.math-=1
        if t in ['p','h1','h2','h3','h4','div','section','li','tr']:self.rows.append('\n')
    def handle_data(self,d):
        if not self.ignore and not self.math:self.rows.append(d)
r=Reader();r.feed((A/'AFOOO2606.12257v1.html').read_text());assert r.ignore==0 and r.math==0
out='\n'.join(x.strip() for x in ''.join(r.rows).splitlines() if x.strip())+'\n'
(A/'afooo-extracted.txt').write_text(out);print('Passive primary HTML text extracted; no embedded script execution.')
