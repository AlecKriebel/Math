"""Create foreign-source text derivatives, with exact PDF read limits recorded."""
import hashlib, json, pathlib
from pypdf import PdfReader
ROOT=pathlib.Path(__file__).resolve().parent
for filename in ['erdos1995.pdf','janzer2411.07188.pdf']:
 p=ROOT/'foreign_primary'/filename
 reader=PdfReader(p)
 texts=[page.extract_text() or '' for page in reader.pages]
 out=p.with_suffix('.extracted.txt')
 out.write_text('\n'.join(f'\n=== PDF page {i+1} ===\n{text}' for i,text in enumerate(texts)))
 print(filename,'pages',len(texts),'sha256',hashlib.sha256(p.read_bytes()).hexdigest())
 if filename=='erdos1995.pdf':
  for i in [13,14]: print(f'PDF page {i+1}:\n{texts[i]}')
 else:
  for i,text in enumerate(texts):
   if 'Corollary 1.12' in text: print(f'PDF page {i+1}:\n{text}')
print('Full PDFs were parsed to text, but only the displayed relevant pages are proof-reading inputs. No full-proof reading claimed for Janzer.')
