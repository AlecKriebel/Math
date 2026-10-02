#!/usr/bin/env python3
"""Portable wrapper; the reviewed original script remains byte-for-byte unchanged.
Requires SymPy. Use --sources DIRECTORY for all 5,944 historical assertions,
or --math-only for 5,937 assertions without the seven unavailable PDF hashes.
"""
import argparse, pathlib, tempfile, shutil
parser=argparse.ArgumentParser()
g=parser.add_mutually_exclusive_group(required=True)
g.add_argument('--sources',type=pathlib.Path,help='directory holding the seven source PDFs')
g.add_argument('--math-only',action='store_true',help='explicitly omit seven PDF hash checks')
a=parser.parse_args()
root=pathlib.Path(__file__).resolve().parent.parent
code=(root/'final_review/check_independent.py').read_text()
old="p=pathlib.Path('/workspace/shared/research_separable_30005767'); count=0"
assert code.count(old)==1
with tempfile.TemporaryDirectory(prefix='separable-review-') as temp:
    work=pathlib.Path(temp)
    (work/'checkpoint').mkdir()
    for f in root.iterdir():
        if f.is_file():shutil.copy2(f,work/'checkpoint'/f.name)
    code=code.replace(old,'p=pathlib.Path('+repr(str(work))+'); count=0')
    if a.sources:
        (work/'sources').mkdir()
        import json
        for f in json.loads((root/'SOURCE_MANIFEST.json').read_text())['primary_pdfs']:
            name=pathlib.Path(f['local_audit_file']).name
            shutil.copy2(a.sources/name,work/'sources'/name)
    else:
        start="for f in json.loads((p/'checkpoint/SOURCE_MANIFEST.json').read_text())['primary_pdfs']:"
        end="patterns={(2,3,4,1),(2,4,1,3),(3,1,4,2)}"
        assert code.count(start)==code.count(end)==1
        i,j=code.index(start),code.index(end)
        code=code[:i]+code[j:]
    exec(compile(code,'check_independent.py [portable]','exec'),{'__name__':'__main__'})
