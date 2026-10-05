from pathlib import Path
from capture import capture
import hashlib, json

p=Path(__file__).resolve().parent
b=(p/'process_evidence/download_cao2006_pdf/stdout.bin').read_bytes()
assert b.startswith(b'%PDF')
assert hashlib.sha256(b).hexdigest()=='986bb7080fe7d26cd03bbdca52c2d03a266ef3d43620dbb5e5ae59a9e3c07dd0'
(p/'private/cao_song2006.pdf').write_bytes(b)
jobs=[('extract_cao2006',['/opt/homebrew/bin/pdftotext','-layout',str(p/'private/cao_song2006.pdf'),str(p/'private/cao_song2006.txt')]),('render_cao2006',['/opt/homebrew/bin/pdftoppm','-png','-r','100',str(p/'private/cao_song2006.pdf'),str(p/'private/cao_song2006_page')])]
for label,argv in jobs:
 r,_,_=capture(label,argv,cwd=str(p),sources=[str(p/'private/cao_song2006.pdf')])
 print(json.dumps(r))
 assert r['exit_code']==0,(label,r['exit_code'])
