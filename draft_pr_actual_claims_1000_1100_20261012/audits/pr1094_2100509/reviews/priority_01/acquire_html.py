from pathlib import Path
import urllib.request,hashlib,json,datetime,sys
from html.parser import HTMLParser
class Text(HTMLParser):
 def __init__(self):super().__init__(); self.parts=[]; self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ('script','style'):self.skip+=1
  if tag in ('p','div','h1','h2','h3','li','br'):self.parts.append('\n')
 def handle_endtag(self,tag):
  if tag in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,data):
  if not self.skip:self.parts.append(data)
R=Path(__file__).resolve().parent; P=R/'private_sources'; ledger=R/'HTML_FETCH_LEDGER.json'; rows=json.loads(ledger.read_text()) if ledger.exists() else []
for j,url in enumerate(sys.argv[1:]):
 name='html_'+hashlib.sha256(url.encode()).hexdigest()[:12]; target=P/(name+'.html');row={'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as response: data=response.read();row['final_url']=response.url; row['http']=response.status
  target.write_bytes(data); text=data.decode('utf8',errors='replace');parser=Text();parser.feed(text);out=''.join(parser.parts);target.with_suffix('.txt').write_text(out)
  row.update(status='HTML_FETCHED',bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),local_path=str(target.relative_to(R)),text_bytes=len(out.encode()))
 except Exception as e:row.update(status='FETCH_FAILED',error=str(e))
 rows.append(row); ledger.write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(row))
