"""Explicit synthetic child fixture, never a scientific checker."""
from pathlib import Path
import os, sys, time
mode, expected, out = sys.argv[1:]
marker_out=b'OWN SYNTHETIC REAL CHILD stdout\x00\xff\n'
marker_err=b'OWN SYNTHETIC REAL CHILD stderr\x00\xfe\n'
if mode in ('timeout','nonzero'):
    os.write(1,marker_out);os.write(2,marker_err)
    if mode=='timeout':time.sleep(10)
    else:sys.exit(23)
elif mode=='malformed':os.write(1,b'not JSON \x00\xff\n')
elif mode=='missing_result':pass
else:
    raw=Path(expected).read_bytes()
    if out=='-':os.write(1,raw)
    else:
        p=Path(out);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        os.write(1,b'OWN SYNTHETIC REAL CHILD expected-result fixture\n')
