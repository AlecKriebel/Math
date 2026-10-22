#!/usr/bin/env python3
"""Scope-oriented source snippets and first/last-page render; does not execute archived code."""
import pathlib,subprocess,re,json,hashlib
W=pathlib.Path(__file__).resolve().parent
for n in [883,885,888,894,904,905]:
 p=W/'downloads_private'/str(n);pdf=next(p.glob('*.pdf'));info=subprocess.check_output(['pdfinfo',str(pdf)],text=True);pages=int(re.search(r'Pages:\s+(\d+)',info).group(1));src=(p/'note.tex').read_text();lines=src.splitlines();selected=set(range(min(60,len(lines))))
 pattern=r'(scope|disclos|review|unrefereed|priority|firstness|rank|irrational|unimodular|complex|literature|author-approved|Reznick|Laurent|2010|noninject|Markov|background|weighted-list|ordinary undirected|source|sink|attainment|tangency|original_packet)'
 for i,line in enumerate(lines):
  if re.search(pattern,line,re.I):selected.update(range(max(0,i-2),min(len(lines),i+4)))
 snippets='\n'.join(f'{i+1}: {lines[i]}' for i in sorted(selected));(p/'source_scope_snippets.txt').write_text(snippets+'\n')
 for pg in [1,pages]:subprocess.run(['pdftoppm','-f',str(pg),'-l',str(pg),'-scale-to','750','-singlefile','-png',str(pdf),str(p/f'page_{pg}')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 print(n,'source chars',len(src),'scope snippet chars',len(snippets))
