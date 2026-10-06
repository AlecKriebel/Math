from html.parser import HTMLParser
from pathlib import Path
import datetime,hashlib,json,os,re
D=Path(__file__).resolve().parent
class Parser(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.skip=0;self.parts=[];self.heading=None;self.headings=[];self.meta={};self.paragraphs=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ('script','style'):self.skip+=1
        if tag=='meta' and a.get('name') in ('citation_doi','citation_title','citation_publication_date'):self.meta[a['name']]=a.get('content')
        if tag in ('h1','h2','h3','h4'):self.heading=[]
        if tag=='p':self.paragraphs+=1
        if tag in ('p','div','section','h1','h2','h3','h4','li'):self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag in ('script','style'):self.skip=max(0,self.skip-1)
        if tag in ('h1','h2','h3','h4') and self.heading is not None:self.headings.append(''.join(self.heading).strip());self.heading=None
    def handle_data(self,data):
        if not self.skip:
            self.parts.append(data)
            if self.heading is not None:self.heading.append(data)
source=D/'private_sources/crossref_fulltext.html';b=source.read_bytes();raw=b.decode('utf-8','replace');parser=Parser();parser.feed(raw)
text=re.sub(r'[ \t\r]+',' ',''.join(parser.parts));text=re.sub(r'\n\s*\n+','\n',text)
target=D/'private_sources/publisher_visible_text.txt';target.write_text(text)
r={'schema':'pr110-publisher-access-diagnostic/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'source_pin':{'path':source.relative_to(D).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()},'derived_text_pin':{'path':target.relative_to(D).as_posix(),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()},'metadata':parser.meta,'headings':parser.headings,'paragraph_tags':parser.paragraphs,'raw_access_No_markers':raw.count('access=No'),'subscription_preview_phrase_present':'preview of subscription content' in text.lower(),'terms':{s:text.lower().find(s.lower()) for s in ['Abstract','Introduction','Conclusions','Theorem','antipedal','Spatial integrals','This is a preview of subscription content']},'no_full_final_body_read_claim':True}
(D/'PUBLISHER_ACCESS_DIAGNOSTIC.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r,indent=2));print('VISIBLE_TEXT_FIRST_4500_CHARS\n'+text[:4500])
