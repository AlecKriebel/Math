#!/usr/bin/env python3
from fetch_sources import fetch, BASE
from concurrent.futures import ThreadPoolExecutor
import json
SOURCES={
 'homometry0808v1':'https://arxiv.org/pdf/0808.0094v1',
 'deformation0404v2':'https://arxiv.org/pdf/math/0404155v2',
 'frank_multidimensional2005':'https://pages.vassar.edu/nafrank/files/2012/08/bijspec.pdf',
 'bartlett1410v4':'https://arxiv.org/pdf/1410.8106v4',
}
with ThreadPoolExecutor(max_workers=4) as ex: receipts=list(ex.map(fetch,SOURCES.items()))
(BASE/'ADDITIONAL_SOURCE_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n')
print(json.dumps([{k:v for k,v in x.items() if k!='pdfinfo'} for x in receipts],indent=2))
