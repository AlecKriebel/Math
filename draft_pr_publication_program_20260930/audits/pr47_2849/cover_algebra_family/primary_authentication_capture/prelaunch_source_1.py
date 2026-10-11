#!/usr/bin/env python3
"""Bounded primary reads; temporary foreign files are removed, only hashes remain."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,tempfile,urllib.request
B=Path(__file__).resolve().parent
sources=[
 ('K3 author','https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf',['Problem 3.51.']),
 ('BS published','https://msp.org/gt/2018/22-7/gt-v22-n7-p13-p.pdf',['Proposition 4.4 Suppose','Proposition 4.5 Suppose','Theorem 4.6 Suppose','Proposition 4.7']),
 ('BS author preprint','https://www.ma.imperial.ac.uk/~ssivek/papers/stein_fillings.pdf',['Morse','cyclic']),
 ('Bascape2608v1','https://arxiv.org/pdf/2608.20551v1',['Theorem 3.5.','Definition 5.3.','Corollary 5.4.']),
 ('Bascape2408v2','https://arxiv.org/pdf/2408.16635v2',['if and only if','Theorem 1.5.']),
 ('LiYe2511v1','https://arxiv.org/pdf/2511.17877v1',['Lemma 7.1.']),
 ('SivekZentner surgery','https://spiral.imperial.ac.uk/server/api/core/bitstreams/31fba2ba-24ed-45cb-9374-dad47877adcc/content',['Proposition 4.3.']),
 ('SivekZentner menagerie','https://zentner.app.uni-regensburg.de/menagerie.pdf',['Theorem 1.2.','(2.1)','Proposition 6.1.','Remark 6.2.'])]
rows=[]
for name,url,patterns in sources:
 start=datetime.now(timezone.utc).isoformat();data=urllib.request.urlopen(url,timeout=40).read()
 with tempfile.TemporaryDirectory(prefix='pr47-cover-transient-primary-') as d:
  p=Path(d)/'foreign.pdf';p.write_bytes(data)
  r=subprocess.run(['pdftotext','-layout',str(p),'-'],capture_output=True,check=True)
  text=r.stdout.decode();regions=[]
  for pattern in patterns:
   off=text.find(pattern);assert off>=0,(name,pattern)
   region=text[max(0,off-400):off+4000].encode()
   regions.append({'locator_search':pattern,'character_offset':off,'bounded_region_bytes':len(region),'bounded_region_sha256':hashlib.sha256(region).hexdigest(),'foreign_region_retained':False})
  rows.append({'name':name,'url':url,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),'regions':regions,'temporary_foreign_directory_removed':True})
out={'schema':'pr47-cover-primary-authentication/v1','all_requested_primary_pdfs_authenticated':True,'sources':rows,'body_or_OCR_or_pixels_or_headers_retained':False,'BN90_separate_read':'Author-uploaded original theorem/proof text read in ResearchGate web output; AMS original endpoint403 and RG PDF link404, no authenticated PDF byte receipt. Published BS independently confirms the exact cohomology and surgery assertions used.','bounded_search_not_exhaustive':True}
(B/'PRIMARY_AUTHENTICATION_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'authenticated_pdf_sources':len(rows),'foreign_publication_bodies_retained':False,'source_hashes':{r['name']:r['sha256'] for r in rows}},indent=2))
