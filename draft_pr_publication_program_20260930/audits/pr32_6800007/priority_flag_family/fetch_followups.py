"""Adaptive public-source retrieval; never messages an individual."""
from pathlib import Path
import json, subprocess
from fetch_priority_sources import fetch, utc, ROOT

ITEMS=[
 ('derdzinski_arxiv.pdf','https://arxiv.org/pdf/math/0612855v1'),
 ('hal_survey_response.pdf','https://hal.sorbonne-universite.fr/hal-03377097/document'),
 ('hal_survey_science_response.pdf','https://hal.science/hal-03377097/document'),
 ('global_publisher_response.pdf','https://www.sciencedirect.com/science/article/pii/S0926224524001177/pdfft?isDTMRedir=true&download=true'),
 ('reductions_publisher_response.pdf','https://link.springer.com/content/pdf/10.1007/s00031-025-09937-9.pdf'),
 ('survey_publisher_response.pdf','https://link.springer.com/content/pdf/10.1007/s40863-020-00175-3.pdf'),
 ('global_crossref.json','https://api.crossref.org/works/10.1016/j.difgeo.2024.102224'),
 ('reductions_crossref.json','https://api.crossref.org/works/10.1007/s00031-025-09937-9'),
 ('surgeries_crossref.json','https://api.crossref.org/works/10.1090/tran/9532'),
 ('fv_arxiv_abs.html','https://arxiv.org/abs/1804.11096'),
 ('global_arxiv_abs.html','https://arxiv.org/abs/2306.17705'),
 ('reductions_arxiv_abs.html','https://arxiv.org/abs/2406.11509'),
 ('surgeries_arxiv_abs.html','https://arxiv.org/abs/2406.02053'),
 ('derdzinski_arxiv_abs.html','https://arxiv.org/abs/math/0612855'),
]

if __name__=='__main__':
 from concurrent.futures import ThreadPoolExecutor
 with ThreadPoolExecutor(max_workers=8) as pool: r=list(pool.map(fetch,ITEMS))
 (ROOT/'FOLLOWUP_SOURCE_RECEIPTS.json').write_text(json.dumps({'utc':utc(),'receipts':r},indent=2)+'\n')
 print(json.dumps([{'name':x['name'],'status':x.get('status'),'bytes':x['bytes'],'pdf':x['is_pdf'],'error':x.get('error')} for x in r],indent=2))
