"""Render selected pinned primary pages once, outside the frozen primary payload."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import subprocess
import time

R=Path(__file__).resolve().parent
P=R.parents[3]
assert R==P/'papers/23411227/reviews/root-continuation-20261117'
MAP=P/'verification/fano-primary-acquisition-sol-20261117/SOURCE_EDITION_MAP.json'
assert hashlib.sha256(MAP.read_bytes()).hexdigest()=='6ac06417e83f6c432d40c5b9875dde0954aae6141585f8f667cef8c75fea7139'
records={r['label']:r for r in json.loads(MAP.read_bytes())['records']}
OUT=R/'primary-rasters/batch1'
assert not OUT.exists()
OUT.mkdir(parents=True)
jobs=[('OWR',28,29),('MW',10,12),('WZ',1,3)]
sha=lambda b:hashlib.sha256(b).hexdigest()
def render(job):
 label,first,last=job;record=records[label];source=Path(record['payload_pdf']['path'])
 before=source.read_bytes()
 assert sha(before)==record['declared_SHA256'] and len(before)==record['declared_bytes']
 dest=OUT/label;dest.mkdir()
 argv=['/opt/homebrew/bin/pdftoppm','-f',str(first),'-l',str(last),'-png','-scale-to','1800',str(source),str(dest/'page')]
 start=datetime.now(timezone.utc).isoformat();clock=time.monotonic()
 run=subprocess.run(argv,capture_output=True);elapsed=time.monotonic()-clock
 (dest/'stdout').write_bytes(run.stdout);(dest/'stderr').write_bytes(run.stderr)
 current=source.read_bytes();same=current==before
 row={'label':label,'argv':argv,'UTC_start':start,'UTC_end':datetime.now(timezone.utc).isoformat(),
      'seconds':elapsed,'exit':run.returncode,'attempts':1,'retries':0,'input_SHA256':sha(before),
      'whole_input_unchanged':same,'stdout_bytes':len(run.stdout),'stderr_bytes':len(run.stderr),
      'stdout_SHA256':sha(run.stdout),'stderr_SHA256':sha(run.stderr)}
 (dest/'EXECUTION.json').write_text(json.dumps(row,indent=2)+'\n')
 assert run.returncode==0 and same
 width=len(str(record['pdf_pages']))
 expected=[f'page-{i:0{width}d}.png' for i in range(first,last+1)]
 actual=sorted(p.name for p in dest.glob('*.png'))
 assert actual==expected,(label,actual,expected)
 row['rendered_pages']=[{'page':i,'path':str(dest/name),'bytes':(dest/name).stat().st_size,
                          'SHA256':sha((dest/name).read_bytes())} for i,name in zip(range(first,last+1),expected)]
 return row
with ThreadPoolExecutor(max_workers=3) as pool:
 result=list(pool.map(render,jobs))
(OUT/'RESULT.json').write_text(json.dumps({'status':'SELECTED_PRIMARY_RASTERS_CREATED','jobs':result,
    'scientific_program_executions':0,'primary_payload_files_not_added_or_modified':True},indent=2)+'\n')
print(json.dumps({'jobs':3,'pages':8,'all_exits0':True,'scientific_program_executions':0}))
