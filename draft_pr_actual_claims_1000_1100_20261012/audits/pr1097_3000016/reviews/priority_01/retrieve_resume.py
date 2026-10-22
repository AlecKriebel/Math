#!/usr/bin/env python3
"""Resume custody without replacing any previously retrieved primary body."""
from pathlib import Path
import datetime, hashlib, json, subprocess
from retrieve_sources import ROOT, retrieve

ITEMS = [
 ('Petri_joinfree_2021', 'https://ceur-ws.org/Vol-2907/paper7.pdf'),
 ('Petri_complexity', 'https://citeseerx.ist.psu.edu/document?doi=e35f594805839f40aa7713124cb39f24cc4a13b8&repid=rep1&type=pdf'),
 ('BL_journal_kyoto', 'https://www.kurims.kyoto-u.ac.jp/EMIS/journals/JACO/Volume1_4/l31v67681vv718ll.fulltext.pdf'),
 ('Sandpile_problems_2024', 'https://www.samuelfhopkins.com/docs/birs_sandpile_problems.pdf'),
]

def pin(path):
 b=path.read_bytes()
 return {'path':str(path.relative_to(ROOT)), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()}

if __name__ == '__main__':
 rows=[]
 for key,url in ITEMS:
  path=ROOT/'sources/raw'/(key+'.pdf')
  if path.exists():
   rows.append({'id':key,'url':url,'status':'preserved existing body; original retrieval time not reconstructed',**pin(path)})
  else:
   rows.append(retrieve((key,url)))
 recovered=[]
 for path in sorted((ROOT/'sources/raw').glob('*.pdf')):
  recovered.append(pin(path))
 (ROOT/'RESUMED_SOURCE_CUSTODY.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'new_retrievals':rows,'all_retained_pdf_bodies':recovered,'qualification':'Original SOURCE_RETRIEVAL is preserved. Additional interrupted retrieval receipt did not exist; retained bodies are pinned now without inventing original retrieval times.'},indent=2)+'\n')
 print(json.dumps([{k:r.get(k) for k in ('id','curl_exit','http_code','is_pdf','bytes','pdf_pages','status')} for r in rows]))
