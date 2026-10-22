#!/usr/bin/env python3
"""Prior73/158 logic, new output custody; add directory data to old tree fixtures."""
from pathlib import Path
import json
import sys
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
FROZEN=HERE/'pre_review03_binding'


def directory_fixture(leaves):
    result={}
    for name in leaves:
        parts=Path(name).parts
        for end in range(1,len(parts)):
            result['/'.join(parts[:end])]={'mode':'040000','type':'tree','sha':'synthetic-directory'}
    return result


def main():
    selected='73' if '--73' in sys.argv else '158'
    relative=('ops_repair_20261021/repair_controls.py' if selected=='73' else
              'publication_operations_preparation/prior_review_02_full/publication_operations_preparation/offline_controls.py')
    source=FROZEN/relative
    code=source.read_text()
    output=HERE/('prior'+selected+('_optimized' if sys.flags.optimize else '_normal'));output.mkdir(exist_ok=True)
    old='HERE=Path(__file__).resolve().parent\nAUDIT=HERE.parent'
    if code.count(old)!=1:raise RuntimeError('Old prior-control entrypoint differs')
    code=code.replace(old,'HERE=Path('+repr(str(output))+')\nAUDIT=Path('+repr(str(AUDIT))+')')
    if selected=='158':
        # Old fixtures omitted selected-subtree directory maps because the old
        # implementation inspected leaves only. Add honest ancestor inventories;
        # no production guard is replaced or bypassed.
        old="patch.object(I,'subtree',lambda commit,path,recursive:c[commit,path])"
        new="patch.object(I,'subtree',lambda commit,path,recursive=True:directory_fixture(a[commit] if commit in a else original) if path==B.PROBLEM else c[commit,path])"
        if code.count(old)!=1:raise RuntimeError('Old integration fixture differs')
        code=code.replace(old,new)
        old="patch.object(I,'subtree',lambda c,p,r:{})"
        new="patch.object(I,'subtree',lambda c,p,r=True:directory_fixture(leaves(c,p)) if p==B.PROBLEM else {})"
        if code.count(old)!=1:raise RuntimeError('Old overlay fixture differs')
        code=code.replace(old,new)
    exec(compile(code,str(source),'exec'),{'__name__':'__main__','__file__':str(source),'directory_fixture':directory_fixture})


if __name__=='__main__':main()
