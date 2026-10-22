#!/usr/bin/env python3
"""Portable standard-library wrapper; frozen original script is unchanged.
--sources DIRECTORY replays all 38 historical controls.
--math-only explicitly omits the eight source PDF hashes, running 30 controls.
"""
import argparse, pathlib, tempfile, shutil, json
parser=argparse.ArgumentParser()
g=parser.add_mutually_exclusive_group(required=True)
g.add_argument('--sources',type=pathlib.Path,help='directory containing the eight source PDFs')
g.add_argument('--math-only',action='store_true',help='explicitly omit eight source-PDF hash checks')
a=parser.parse_args()
root=pathlib.Path(__file__).resolve().parent.parent
code=(root/'final_review/check_independent.py').read_text()
old="p=Path('/workspace/shared/research_nonlocal_30003221');checks=0"
assert code.count(old)==1
with tempfile.TemporaryDirectory(prefix='nonlocal-review-') as temp:
    work=pathlib.Path(temp)
    (work/'checkpoint').mkdir()
    for f in root.iterdir():
        if f.is_file():shutil.copy2(f,work/'checkpoint'/f.name)
    code=code.replace(old,'p=Path('+repr(str(work))+');checks=0')
    if a.sources:
        (work/'sources').mkdir()
        for f in json.loads((root/'SOURCE_MANIFEST.json').read_text())['primary_pdfs']:
            name=pathlib.Path(f['local_audit_file']).name
            shutil.copy2(a.sources/name,work/'sources'/name)
    else:
        start="for f in json.loads((p/'checkpoint/SOURCE_MANIFEST.json').read_text())['primary_pdfs']:"
        end="for alpha in ["
        assert code.count(start)==code.count(end)==1
        i,j=code.index(start),code.index(end)
        code=code[:i]+code[j:]
    exec(compile(code,'check_independent.py [portable]','exec'),{'__name__':'__main__'})
