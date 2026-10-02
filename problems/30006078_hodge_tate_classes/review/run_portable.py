#!/usr/bin/env python3
"""Run the unchanged independent checker at caller-supplied artifact locations."""
import argparse
from pathlib import Path
parser=argparse.ArgumentParser()
parser.add_argument('--packet',type=Path,default=Path(__file__).resolve().parents[1])
parser.add_argument('--source-dir',type=Path,required=True,help='Directory holding the seven PDFs named in the source manifests; not distributed in the repository')
a=parser.parse_args()
original=Path(__file__).with_name('check_independent.py').read_text()
lines=original.splitlines(keepends=True)
indices=[i for i,line in enumerate(lines) if line.startswith('p=Path(') and ';src=Path(' in line and line.rstrip().endswith(';n=0')]
assert len(indices)==1,'Frozen checker location setup changed; inspect before adapting'
lines[indices[0]]=f'p=Path({str(a.packet.resolve())!r});src=Path({str(a.source_dir.resolve())!r});n=0\n'
# Only the location setup is adapted. All mathematical and integrity assertions stay unchanged.
exec(compile(''.join(lines),str(Path(__file__).with_name('check_independent.py')),'exec'),{'__name__':'__main__'})
