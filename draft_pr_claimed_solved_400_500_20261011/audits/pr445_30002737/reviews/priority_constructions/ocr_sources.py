#!/usr/bin/env python3
"""Render and OCR historical PDFs with broken text encodings, privately."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess, json
BASE=Path(__file__).resolve().parent
names=['frank_hadamard2003','frank_multidimensional2005']
def run(item):
 name,n=item
 b=BASE/'private_sources'/f'{name}_p{n}'
 subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-r','150','-png','-singlefile',str(BASE/'private_sources'/f'{name}.pdf'),str(b)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 subprocess.run(['tesseract',str(b.with_suffix('.png')),str(b),'--psm','3'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 return {'source':name,'page':n,'image':str(b.with_suffix('.png').relative_to(BASE)),'ocr':str(b.with_suffix('.txt').relative_to(BASE))}
items=[]
for name in names:
 info=(BASE/'private_sources'/f'{name}.pdfinfo.txt').read_text()
 count=int(next(s.split(':',1)[1] for s in info.splitlines() if s.startswith('Pages:')))
 items += [(name,n) for n in range(1,count+1)]
with ThreadPoolExecutor(max_workers=6) as ex: receipts=list(ex.map(run,items))
for name in names:
 rs=[r for r in receipts if r['source']==name]
 (BASE/'private_sources'/f'{name}.ocr.txt').write_text('\f'.join((BASE/r['ocr']).read_text() for r in rs)+'\f')
(BASE/'OCR_READ_RECEIPTS.json').write_text(json.dumps({'method':'pdftoppm 150dpi; tesseract --psm 3; OCR is discovery aid, formulas require visual verification','pages':receipts},indent=2)+'\n')
print('OCR completed privately:',len(receipts),'pages')
