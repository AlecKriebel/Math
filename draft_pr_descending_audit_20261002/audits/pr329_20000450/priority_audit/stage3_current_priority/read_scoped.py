"""Read-only bounded original-extract display, for receipted reading."""
from pathlib import Path
import sys
s=Path(__file__).resolve().parent
name,selection=sys.argv[1:]
pages=(s/'private_evidence'/name/'fulltext.layout.txt').read_text().split('\f')
for segment in selection.split(','):
    a,b=map(int,segment.split('-')) if '-' in segment else (int(segment),int(segment))
    for p in range(a,b+1):
        print(f'ORIGINAL EXTRACT {name} PHYSICAL PAGE {p}')
        print(pages[p-1])
