#!/usr/bin/env python3
"""Run the unchanged frozen review with portable paths and explicit source mode."""
import argparse,pathlib
ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True)
g.add_argument('--sources',type=pathlib.Path,help='directory with the four hash-bound primary PDFs')
g.add_argument('--math-only',action='store_true',help='omit precisely four source PDF hash checks')
a=ap.parse_args();root=pathlib.Path(__file__).resolve().parent.parent
code=(root/'final_review/check_independent.py').read_text()
old="p=Path('/workspace/shared/research_involution_30001554/checkpoint');src=p.parent/'sources';checks=0"
assert code.count(old)==1
code=code.replace(old,'p=Path('+repr(str(root))+');src=Path('+repr(str(a.sources or root))+');checks=0')
if a.math_only:
 line="for name,f in json.loads((p/'SOURCE_MANIFEST.json').read_text())['files'].items():assert hashlib.sha256((src/name).read_bytes()).hexdigest()==f['sha256'];checks+=1"
 assert code.count(line)==1;code=code.replace(line,'# Explicit source-free mode: four source-PDF hash checks omitted.')
exec(compile(code,'check_independent.py [portable]','exec'),{'__name__':'__main__'})
