#!/usr/bin/env python3
"""Create only ignored inspection intermediates from freshly downloaded PDFs."""
from pathlib import Path
import subprocess
p=Path(__file__).resolve().parent/'tmp'
for name in ['owr','cck_final','gmm']:
 subprocess.run(['pdftotext','-layout',str(p/(name+'.pdf')),str(p/(name+'.txt'))],check=True)
for name,page in [('owr',36),('cck_final',6),('gmm',2),('gmm',4)]:
 subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-r','100','-singlefile','-png',str(p/(name+'.pdf')),str(p/(name+'_page'+str(page)))],check=True)
print('Inspect OWR printed1480, EJP printed5, GMM printed2 and4. Source remains ignored.')
