"""Plain read-only extraction, not browser execution of source scripts."""
from pathlib import Path
from html.parser import HTMLParser

class Plain(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ('script','style'):self.skip+=1
 def handle_endtag(self,tag):
  if tag in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,data):
  if not self.skip and data.strip():self.parts.append(data.strip())

if __name__=='__main__':
 for p in (Path(__file__).resolve().parent/'_local'/'primary').glob('*.html'):
  parser=Plain();parser.feed(p.read_text());text='\n'.join(parser.parts)
  p.with_suffix('.txt').write_text(text+'\n')
  if p.stem=='eulersolve_index':
   for term in ['Lasserre','16633','density','Convergence','Endpoint','convex bod','quadratic proxy']:
    hits=[];pos=0
    while (pos:=text.casefold().find(term.casefold(),pos))>=0:
     hits.append(text[max(0,pos-90):pos+170]);pos+=len(term)
    print(term,len(hits),hits[:12])
