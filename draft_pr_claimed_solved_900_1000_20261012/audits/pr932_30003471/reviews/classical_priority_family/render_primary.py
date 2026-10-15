#!/usr/bin/env python3
"""Render complete cited pages; private QA only, never release raw source pixels."""
from pathlib import Path
import subprocess, json, hashlib, datetime
HERE=Path(__file__).resolve().parent
SOURCES=HERE/'private'/'sources'; OUT=HERE/'private'/'renders'; OUT.mkdir(parents=True,exist_ok=True)
PAGES={
 'owr_mfo':[64], 'ak_v2':[5],
 'winter_stoker_author':[1,2], 'winter_stoker_blog':[1,2],
 'winter_metric_published':[5,6,8,9,10,12,13,15],
 'izmestiev_v3':[7,8,15,16],
 'winter_infinitesimal_v1':[1,2,5],
 'mazzeo_montcouquiol_v3':[1,2],
 'schlenker_2000':[1,2,3], 'schlafli_souam':[1,2],
 'bob_izm_alexandrov':[3],
}
rows=[]
for key,pages in PAGES.items():
 for page in pages:
  prefix=OUT/(key+'_p'+str(page))
  r=subprocess.run(['/opt/homebrew/bin/pdftoppm','-png','-r','105','-f',str(page),'-l',str(page),'-singlefile',str(SOURCES/(key+'.pdf')),str(prefix)],capture_output=True,check=True)
  path=prefix.with_suffix('.png')
  rows.append(dict(source=key,pdf_page_1based=page,path=path.relative_to(HERE).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),rendered_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stderr=r.stderr.decode()[:300]))
(HERE/'private'/'RENDER_RECEIPTS.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps({'rendered_count':len(rows),'raw_pixels_private':True}))
