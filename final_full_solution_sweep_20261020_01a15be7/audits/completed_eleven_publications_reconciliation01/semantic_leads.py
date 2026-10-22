#!/usr/bin/env python3
from pathlib import Path
import gzip,json,re,datetime
O=Path(__file__).resolve().parent
rows=json.loads(gzip.decompress((O/'private/opening_ledger.json.gz').read_bytes()))
patterns={292:r'30001608|OWR.4530.006|deterministic.first.chunk|\bDFC\b|file.sharing',397:r'9700002|AMR.096.0002|congestion|fragmentation',399:r'30001179|OWR.3392.00[45]|tensor.core|free.product.system',280:r'30000156|OWR.768.006|birational|cycle.distribution',1329:r'30003208|30002897|OWR.14748.016|\bDKW\b|tail.algebra|symmetric.free.product',1337:r'30004534|Lefschetz|symmetric.ideal',1391:r'30005740|Nakayama|BV.generator|Gerstenhaber|Hochschild',1348:r'10000037|AMR.099.0037|Benjamini|supercritical|rough.isometr',1407:r'1200024|AMR.011.0024|grandparent|spanning.forest|expected.degree',1372:r'30002726|initial.odd.ear|ear.decompos|Seb[oő]|Benchetrit',1330:r'30003185|Bray|strong.involutions|involution.centralis'}
leads={}
for pr,pattern in patterns.items():
 rg=re.compile(pattern+rf'|github\.com/AlecKriebel/Math/pull/{pr}(?:\D|$)',re.I);out=[]
 for i,row in enumerate(rows):
  s=' '.join(map(str,row));m=list(rg.finditer(s))
  if m:out.append({'row':i+1,'matches':list(dict.fromkeys(x.group()for x in m)),'all_cells':row})
 leads[str(pr)]={'pattern':rg.pattern,'leads':out}
(O/'private/SEMANTIC_LEDGER_LEADS.json.gz').write_bytes(gzip.compress(json.dumps(leads,ensure_ascii=False).encode(),mtime=0));print(json.dumps({p:[{'row':x['row'],'matches':x['matches']}for x in v['leads']]for p,v in leads.items()},ensure_ascii=False,indent=2))
