import urllib.request,json,pathlib,concurrent.futures,hashlib,re
from html.parser import HTMLParser
h=pathlib.Path(__file__).resolve().parent
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,d):self.parts.append(d)
ids=['0712.0027','0711.1847','0711.0944','2306.15147','1607.07814','1711.07218','1401.7301','2606.10817','1607.00347','math/0510470']
def get(i):
 u='https://arxiv.org/abs/'+i
 try:
  b=urllib.request.urlopen(u,timeout=30).read();p=Text();p.feed(b.decode());t=' '.join(' '.join(p.parts).split());k=t.find('Submission history');j=t.find('Full-text links',k)
  hist=t[k:j] if k>=0 else 'NOT FOUND'
  return {'id':i,'url':u,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'history':hist,'versions':re.findall(r'\[v(\d+)\]',hist)}
 except Exception as e:return {'id':i,'url':u,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:r=list(ex.map(get,ids))
(h/'evidence/ARXIV_VERSION_RECHECK.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
