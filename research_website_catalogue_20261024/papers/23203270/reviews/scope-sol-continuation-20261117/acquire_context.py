"""Read-only public primary-source captures for citation and standard interfaces."""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import urllib.request

LANE=Path(__file__).resolve().parent
DEST=LANE/'primary-context'
DEST.mkdir(exist_ok=False)
items=[
 ('nagamine-v2.html','https://arxiv.org/html/1811.04153v2',None),
 ('cddg-v1.html','https://arxiv.org/html/1910.11023v1',None),
 ('cp-v2.html','https://arxiv.org/html/2504.14382v2',None),
 ('en-v1.html','https://arxiv.org/html/1301.3967v1',None),
 ('nagamine-v2.pdf','https://arxiv.org/pdf/1811.04153v2','7d54227d4f00180af7aa36e2415bb61331e1e6f1e73e676f7c6277ff491a84cf'),
 ('cddg-v1.pdf','https://arxiv.org/pdf/1910.11023v1','a3d18bf9d6f5340237894717f492a01b091618629b2a4f3eeb745ecf5b66e66e'),
 ('cp-v2.pdf','https://arxiv.org/pdf/2504.14382v2','cdf29b90ce6f21020053f75182166dfb425693d6088c014b8bca4d5e17889fec'),
 ('stacks-056S.html','https://stacks.math.columbia.edu/tag/056S',None),
 ('stacks-0AG0.html','https://stacks.math.columbia.edu/tag/0AG0',None),
 ('stacks-0BE9.html','https://stacks.math.columbia.edu/tag/0BE9',None),
]

def get(item):
 name,url,expected=item;start=datetime.now(timezone.utc).isoformat()
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent-source-review/1.0'}),timeout=60) as response:
  data=response.read();headers=dict(response.headers.items());status=response.status
 actual=hashlib.sha256(data).hexdigest()
 if expected is not None: assert actual==expected,(name,actual,expected)
 (DEST/name).write_bytes(data)
 return {'file':name,'url':url,'start_utc':start,'end_utc':datetime.now(timezone.utc).isoformat(),
         'status':status,'headers':headers,'bytes':len(data),'sha256':actual,
         'expected_published_sha256':expected,'expected_match':actual==expected if expected else None}

with ThreadPoolExecutor(max_workers=4) as executor: results=list(executor.map(get,items))
(LANE/'CONTEXT_ACQUISITION.json').write_text(json.dumps({'ordinary_public_GET_only':True,'files':results},indent=2)+'\n')
print(json.dumps({'captured_files':len(results),'published_pdf_pins_match':True}))
