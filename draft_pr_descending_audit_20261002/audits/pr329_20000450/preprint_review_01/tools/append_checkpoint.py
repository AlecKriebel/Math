#!/usr/bin/env python3
"""Append a native-UTC checkpoint from an own-folder message body."""
from pathlib import Path
import subprocess
import sys
R=Path(__file__).resolve().parents[1]
body=Path(sys.argv[1]).resolve()
assert body.is_relative_to(R)
clock=subprocess.check_output(['/bin/date','-u','+%Y-%m-%dT%H:%M:%SZ']).decode().strip()
with (R/'RESEARCH_LOG.md').open('a') as log:
    log.write('\n## '+clock+' - '+sys.argv[2]+'\n\n'+body.read_text().rstrip()+'\n')
print(clock)
print('Append-only checkpoint completed from '+str(body.relative_to(R)))
