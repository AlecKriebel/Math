#!/usr/bin/env python3
"""Read-only rendering of existing private primary PDFs; outputs stay ignored."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

here=Path(__file__).resolve().parent
private=here/'private';private.mkdir(exist_ok=True)
source_root=here.parent/'primary_scope_family/tmp'
spec=[('owr_literal_2552',source_root/'owr_44_2008.pdf',76),
      ('simon_density',source_root/'simon_gmt_2018.pdf',13),
      ('simon_rademacher',source_root/'simon_gmt_2018.pdf',26),
      ('simon_area',source_root/'simon_gmt_2018.pdf',32)]
records=[]
for name,path,page in spec:
    argv=['/opt/homebrew/bin/pdftoppm','-f',str(page),'-l',str(page),'-r','130','-singlefile','-png',str(path),str(private/name)]
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    proc=subprocess.Popen(argv,cwd=here,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr=proc.communicate()
    (private/(name+'.stdout.bin')).write_bytes(stdout);(private/(name+'.stderr.bin')).write_bytes(stderr)
    png=private/(name+'.png')
    row={'source':str(path),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'argv':argv,'actual_pid':proc.pid,'started_utc':start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':proc.returncode,'stdout_bytes':len(stdout),'stderr_bytes':len(stderr),'rendered_png':str(png),'rendered_sha256':hashlib.sha256(png.read_bytes()).hexdigest() if png.exists() else None}
    records.append(row)
    if proc.returncode:raise RuntimeError(name+' rendering failed')
(here/'primary_render_receipt.json').write_text(json.dumps(records,indent=2)+'\n')
print('Rendered four primary source pages privately; genuine PIDs/times/streams preserved.')
