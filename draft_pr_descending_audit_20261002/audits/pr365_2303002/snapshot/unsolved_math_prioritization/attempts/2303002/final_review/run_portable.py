#!/usr/bin/env python3
"""Portable paths for the unchanged review; source hashes require explicit mode."""
import argparse,pathlib
ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True)
g.add_argument('--sources',type=pathlib.Path)
g.add_argument('--math-only',action='store_true',help='omit exactly two source PDF hash checks')
a=ap.parse_args();root=pathlib.Path(__file__).resolve().parent.parent
code=(root/'final_review/check_independent.py').read_text()
old="p=Path('/workspace/shared/research_harmonicpath_2303002/checkpoint');src=p.parent/'sources';n=0"
assert code.count(old)==1;code=code.replace(old,'p=Path('+repr(str(root))+');src=Path('+repr(str(a.sources or root))+');n=0')
if a.math_only:
 start="for f in json.loads((p/'SOURCE_MANIFEST.json').read_text())['primary_pdfs']:"
 end='for dim in range(3,21):'
 assert code.count(start)==code.count(end)==1
 i,j=code.index(start),code.index(end);code=code[:i]+'# Two source hash checks explicitly omitted.\n'+code[j:]
exec(compile(code,'check_independent.py [portable]','exec'),{'__name__':'__main__'})
