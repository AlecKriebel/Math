#!/usr/bin/env python3
from pathlib import Path
import hashlib
ROOT=Path('/mnt/data/k2p_identifiability_program')
exclude={'SHA256SUMS','k2p_identifiability_checkpoint.zip'}
rows=[]
for p in sorted(ROOT.rglob('*')):
 if not p.is_file() or p.name in exclude:continue
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 rows.append(f'{h.hexdigest()}  {p.relative_to(ROOT)}')
(ROOT/'SHA256SUMS').write_text('\n'.join(rows)+'\n')
print(len(rows))
